from odoo import models, fields, api, _
from datetime import datetime

class DigitalTwin(models.Model):
    _name = 'bim.digital.twin'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Digital Twin'
    _order = 'name'

    name                = fields.Char(string='Name', required=True, tracking=True)
    description         = fields.Text(string='Description')
    model_file          = fields.Binary(string='Model File', tracking=True)
    model_filename      = fields.Char(string='Model Filename')
    status              = fields.Selection([
        ('draft',       'Draft'),
        ('active',      'Active'),
        ('needs_sync',  'Needs Sync'),
        ('archived',    'Archived'),
    ], string='Status', default='draft', tracking=True, index=True)
    last_updated        = fields.Datetime(string='Last Updated', readonly=True, tracking=True)
    project_id          = fields.Many2one('bim.project', string='Project', required=True)
    issue_ids           = fields.One2many('bim.issue', 'digital_twin_id', string='Issues')
    issue_count         = fields.Integer(string='Total Issues', compute='_compute_issue_metrics', store=True)
    issue_resolved      = fields.Integer(string='Resolved Issues', compute='_compute_issue_metrics', store=True)
    sync_progress       = fields.Float(string='Sync Progress (%)', compute='_compute_issue_metrics', store=True)
    location            = fields.Char(string='Location')
    viewpoint           = fields.Binary(string='Current Viewpoint Image')
    viewpoint_date      = fields.Datetime(string='Viewpoint Captured On', readonly=True)
    viewpoint_history   = fields.One2many(
        'bim.digital.twin.viewpoint', 'twin_id',
        string='Viewpoint History', readonly=True)

    # Automatically update last_updated when model_file or model_filename changes
    @api.model
    def create(self, vals):
        if vals.get('model_file'):
            vals['last_updated'] = fields.Datetime.now()
        twin = super().create(vals)
        return twin

    def write(self, vals):
        if 'model_file' in vals or 'model_filename' in vals:
            vals['last_updated'] = fields.Datetime.now()
            # schedule a sync request activity for the project manager
            for twin in self:
                if twin.project_id.project_manager_id:
                    twin.activity_schedule(
                        'mail.mail_activity_data_todo',
                        user_id=twin.project_id.project_manager_id.id,
                        summary=_('Sync digital twin: %s') % twin.name,
                        date_deadline=fields.Date.context_today(self) + timedelta(days=1)
                    )
        # capture viewpoint changes
        if 'viewpoint' in vals:
            for twin in self:
                twin._create_viewpoint_history(vals.get('viewpoint'))
                vals['viewpoint_date'] = fields.Datetime.now()
        return super().write(vals)

    def _create_viewpoint_history(self, img):
        for twin in self:
            self.env['bim.digital.twin.viewpoint'].create({
                'twin_id': twin.id,
                'image': img,
                'captured_on': fields.Datetime.now(),
            })

    @api.depends('issue_ids', 'issue_ids.status')
    def _compute_issue_metrics(self):
        for twin in self:
            total = len(twin.issue_ids)
            done  = len(twin.issue_ids.filtered(lambda i: i.status in ['resolved','closed']))
            twin.issue_count    = total
            twin.issue_resolved = done
            twin.sync_progress  = (done / total * 100) if total else 0.0

    # Workflow buttons
    def action_activate(self):
        for twin in self:
            twin.status = 'active'
            twin.message_post(body=_("Marked as Active"), subtype_xmlid='mail.mt_note')

    def action_request_sync(self):
        for twin in self:
            twin.status = 'needs_sync'
            twin.message_post(body=_("Sync Requested"), subtype_xmlid='mail.mt_note')

    def action_archive(self):
        for twin in self:
            twin.status = 'archived'
            twin.message_post(body=_("Archived"), subtype_xmlid='mail.mt_note')

    # Prevent archive if unresolved issues exist
    @api.constrains('status')
    def _check_unresolved_before_archive(self):
        for twin in self:
            if twin.status == 'archived' and any(i.status != 'closed' for i in twin.issue_ids):
                raise ValidationError(_("Cannot archive while there are open issues."))
