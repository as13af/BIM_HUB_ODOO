from odoo import models, fields, api, exceptions

class BIMProject(models.Model):
    _name = 'bim.project'
    _description = 'BIM Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Project Name', required=True, tracking=True)
    project_code = fields.Char(string='Project Code', index=True, tracking=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date', tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True)
    location = fields.Char(string='Location')
    project_type = fields.Selection([
        ('construction', 'Construction'),
        ('renovation', 'Renovation'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other')
    ], string='Project Type')

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

    @api.depends('bim_issue_id', 'bim_issue_id.status')
    def _compute_progress(self):
        for project in self:
            total = len(project.issue_id)
            if total:
                done = len(project.issue_id.filtered(lambda i: i.status in ['resolved', 'closed']))
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
            # default duration 30 days
            self.end_date = self.start_date + relativedelta(days=30)

    def action_set_active(self):
        for rec in self:
            rec.status = 'active'

    def action_set_completed(self):
        for rec in self:
            rec.status = 'completed'

    def action_archive(self):
        for rec in self:
            rec.status = 'archived'

    def export_ifc(self):
        """
        Placeholder method to trigger IFC export logic.
        Actual implementation should integrate with an external BIM service or library.
        """
        for rec in self:
            # TODO: call external service, generate IFC, attach to record
            pass
