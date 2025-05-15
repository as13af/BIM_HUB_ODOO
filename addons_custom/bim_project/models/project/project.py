from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError
from datetime import timedelta


class BIMProject(models.Model):
    _name = 'bim.project'
    _description = 'BIM Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Project Name', required=True, tracking=True)
    project_code = fields.Char(string='Project Code', index=True, tracking=True)
    description = fields.Text(string='Description')
    created_date = fields.Date(string='Project Created', default=fields.Date.context_today)
    start_date = fields.Date(string='Start Date', tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True, index=True)
    location = fields.Char(string='Location')
    project_type = fields.Selection([
        ('construction', 'Construction'),
        ('renovation', 'Renovation'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other')
    ], string='Project Type', index=True)

    owner_id = fields.Many2one('res.partner', string='Owner')
    contractor_id = fields.Many2one('res.partner', string='Contractor')
    architect_id = fields.Many2one('res.partner', string='Architect')
    project_manager_id = fields.Many2one('res.users', string='Project Manager')

    budget = fields.Float(string='Budget')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    ifc_model = fields.Binary(string='IFC Model')
    bcf_file = fields.Binary(string='BCF File')
    cobie_file = fields.Binary(string='COBie File')

    document_ids = fields.One2many(
        'ir.attachment', 'res_id', string='Documents',
        domain=[('res_model', '=', 'bim.project')]
    )
    bim_issue_id = fields.One2many('bim.issue', 'model_id', string='Issues', ondelete='cascade')
    bim_digital_twin_id = fields.One2many('bim.digital.twin', 'project_id', string='Digital Twins', ondelete='cascade')
    bim_document_id = fields.One2many('bim.document', 'project_id', string='BIM Documents', ondelete='cascade')

    # Computed progress percentage based on issues completed vs total
    progress = fields.Float(
        string='Progress (%)', compute='_compute_progress',
        store=True, digits=(5, 2)
    )

    approval_1 = fields.Many2one('res.users', string='1st Approval', tracking=True)
    approval_2 = fields.Many2one('res.users', string='2nd Approval', tracking=True)
    approval_3 = fields.Many2one('res.users', string='3rd Approval', tracking=True)

    # APPROVAL METHODS (same for all statuses)
    def action_approve_1(self):
        self._approve_stage('approval_1')

    def action_approve_2(self):
        self._approve_stage('approval_2', prev_approval='approval_1')

    def action_approve_3(self):
        self._approve_stage('approval_3', prev_approval='approval_2')

    # GENERIC APPROVAL LOGIC
    def _approve_stage(self, approval_field, prev_approval=None):
        for rec in self:
            if prev_approval and not rec[prev_approval]:
                raise UserError(f"Previous approval ({prev_approval.replace('_', ' ')}) is required!")
            if not rec[approval_field]:
                rec[approval_field] = self.env.user

    @api.model
    def create(self, vals):
        record = super(BIMProject, self).create(vals)

        def abbreviate(name):
            words = name.upper().split()
            if len(words) == 1:
                return words[0][:3]
            return ''.join([w[0] for w in words])[:3]

        architect_abbr = abbreviate(record.architect_id.name) if record.architect_id else 'ARC'
        contractor_abbr = abbreviate(record.contractor_id.name) if record.contractor_id else 'CTR'
        owner_abbr = abbreviate(record.owner_id.name) if record.owner_id else 'OWN'

        date_str = record.created_date.strftime('%Y%m%d') if record.created_date else 'YYYYMMDD'

        project_type_abbr = {
            'construction': 'C',
            'renovation': 'R',
            'maintenance': 'M',
            'other': 'O'
        }.get(record.project_type, 'O')

        record.project_code = f"{architect_abbr}-{contractor_abbr}-{owner_abbr}-{date_str}-{project_type_abbr}"

        return record
        
    @api.depends('bim_issue_id', 'bim_issue_id.status')
    def _compute_progress(self):
        for project in self:
            total = len(project.bim_issue_id)
            if total:
                done = len(project.bim_issue_id.filtered(lambda i: i.status in ['resolved', 'closed']))
                project.progress = (done / total) * 100
            else:
                project.progress = 0.0

    @api.constrains('end_date', 'start_date')
    def _check_dates(self):
        for record in self:
            if record.end_date and record.start_date and record.end_date < record.start_date:
                raise exceptions.ValidationError('End Date must be after Start Date.')

    @api.onchange('start_date', 'end_date')
    def _onchange_dates(self):
        if self.start_date and not self.end_date:
            # Default duration of 30 days
            self.end_date = self.start_date + timedelta(days=30)

    # STATUS TRANSITIONS (reset approvals on change)
    def action_set_active(self):
        for rec in self:
            if rec.status != 'draft':
                raise UserError("Only draft projects can be activated!")
            if not (rec.approval_1 and rec.approval_2 and rec.approval_3):
                raise UserError("All 3 approvals are required to activate!")
            rec.status = 'active'
            rec._reset_approvals()  # Clear approvals after transition

    def action_set_completed(self):
        for rec in self:
            if rec.status != 'active':
                raise UserError("Only active projects can be completed!")
            if not (rec.approval_1 and rec.approval_2 and rec.approval_3):
                raise UserError("All 3 approvals are required to complete!")
            rec.status = 'completed'
            rec._reset_approvals()

    def action_set_archived(self):
        for rec in self:
            if rec.status != 'completed':
                raise UserError("Only completed projects can be archived!")
            if not (rec.approval_1 and rec.approval_2 and rec.approval_3):
                raise UserError("All 3 approvals are required to archive!")
            rec.status = 'archived'
            rec._reset_approvals()

    def _reset_approvals(self):
        """Reset all approvals after status change."""
        self.write({
            'approval_1': False,
            'approval_2': False,
            'approval_3': False,
        })

    def export_ifc(self):
        """
        Placeholder method to trigger IFC export logic.
        Actual implementation should integrate with an external BIM service or library.
        """
        for rec in self:
            # TODO: call external service, generate IFC, attach to record
            pass
