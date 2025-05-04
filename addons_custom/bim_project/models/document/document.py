from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class BIMDocument(models.Model):
    _name = 'bim.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'BIM Document'
    _order = 'name, revision desc'

    # Core fields
    name                     = fields.Char(string='Document Name', required=True, tracking=True)
    description              = fields.Text(string='Description')
    file                     = fields.Binary(string='File')
    file_name                = fields.Char(string='File Name')
    file_type                = fields.Selection([
        ('ifc', 'IFC'), ('bcf', 'BCF'), ('pdf', 'PDF'),
        ('dwg', 'DWG'), ('jpg', 'JPEG'), ('png', 'PNG'),
        ('other', 'Other'),
    ], string='File Type', default='other', tracking=True)

    # Classification & revision
    classification_code      = fields.Char(string='Classification Code')
    classification_name      = fields.Char(string='Classification Name')
    classification_description = fields.Text(string='Classification Description')
    revision                 = fields.Char(string='Revision', readonly=True, default='1', tracking=True)
    revision_history_ids     = fields.One2many(
        'bim.document.history', 'document_id',
        string='Revision History', readonly=True)

    # Workflow & dates
    status                   = fields.Selection([
        ('draft',     'Draft'),
        ('to_review', 'To Review'),
        ('approved',  'Approved'),
        ('rejected',  'Rejected'),
    ], string='Status', default='draft', tracking=True)

    review_requested_by      = fields.Many2one('res.users', string='Review Requested By', readonly=True)
    review_requested_on      = fields.Datetime(string='Review Requested On', readonly=True)
    reviewed_by              = fields.Many2one('res.users', string='Reviewed By', readonly=True)
    reviewed_on              = fields.Datetime(string='Reviewed On', readonly=True)

    created_by               = fields.Many2one('res.users', string='Created By', readonly=True,
                                               default=lambda self: self.env.user)
    created_date             = fields.Datetime(string='Created Date', readonly=True,
                                              default=fields.Datetime.now)
    modified_by              = fields.Many2one('res.users', string='Modified By', readonly=True)
    modified_date            = fields.Datetime(string='Modified Date', readonly=True)

    # Relations
    project_id               = fields.Many2one('bim.project', string='Project', required=True, ondelete='cascade')
    issue_ids                = fields.One2many('bim.issue', 'document_id', string='Issues', ondelete='cascade')
    comments                 = fields.One2many('bim.document.comment', 'document_id', string='Comments', ondelete='cascade')

    # Computed metrics
    days_since_creation      = fields.Integer(string='Days Since Creation',
                                              compute='_compute_days_since_creation', store=True)
    days_since_modification  = fields.Integer(string='Days Since Modification',
                                              compute='_compute_days_since_modification', store=True)
    is_overdue               = fields.Boolean(string='Review Overdue',
                                              compute='_compute_is_overdue', store=True)
    approval_duration        = fields.Float(string='Review Turnaround (days)',
                                            compute='_compute_approval_duration', store=True)

    # --- Create / Write overrides for versioning ---
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for doc in records:
            doc._create_history_entry()
        return records

    def write(self, vals):
        # Snapshot old revision when file changes
        if 'file' in vals or 'file_name' in vals:
            for doc in self:
                doc._create_history_entry()
            # Auto-increment revision
            vals['revision'] = str(int(self.revision) + 1)
        # Track modification info
        vals['modified_by'] = self.env.uid
        vals['modified_date'] = fields.Datetime.now()
        return super().write(vals)

    def _create_history_entry(self):
        self.env['bim.document.history'].create({
            'document_id': self.id,
            'revision': self.revision,
            'updated_by': self.env.uid,
            'updated_date': fields.Datetime.now(),
            'file': self.file,
            'file_name': self.file_name,
        })

    # --- Approval Workflow Methods ---
    def action_request_review(self):
        for doc in self:
            doc.write({
                'status': 'to_review',
                'review_requested_by': self.env.uid,
                'review_requested_on': fields.Datetime.now(),
            })
            # Schedule activity for reviewer (project manager)
            if doc.project_id.project_manager_id:
                doc.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=doc.project_id.project_manager_id.id,
                    summary=_('Please review document %s') % doc.name,
                    date_deadline=fields.Date.context_today(self) + timedelta(days=2)
                )
            doc.message_post(body=_("Review requested"), subtype_xmlid='mail.mt_note')

    def action_approve(self):
        for doc in self:
            doc.write({
                'status': 'approved',
                'reviewed_by': self.env.uid,
                'reviewed_on': fields.Datetime.now(),
            })
            doc.message_post(body=_("Document approved by %s") % self.env.user.name,
                             subtype_xmlid='mail.mt_comment')

    def action_reject(self):
        for doc in self:
            doc.write({'status': 'rejected'})
            doc.message_post(body=_("Document rejected by %s") % self.env.user.name,
                             subtype_xmlid='mail.mt_comment')

    # --- Computed Metrics ---
    @api.depends('created_date')
    def _compute_days_since_creation(self):
        today = fields.Date.context_today(self)
        for doc in self:
            doc.days_since_creation = (today - doc.created_date.date()).days

    @api.depends('modified_date')
    def _compute_days_since_modification(self):
        today = fields.Date.context_today(self)
        for doc in self:
            if doc.modified_date:
                doc.days_since_modification = (today - doc.modified_date.date()).days
            else:
                doc.days_since_modification = 0

    @api.depends('status', 'review_requested_on')
    def _compute_is_overdue(self):
        for doc in self:
            if doc.status == 'to_review' and doc.review_requested_on:
                delta = fields.Datetime.now() - doc.review_requested_on
                doc.is_overdue = delta.days > 2
            else:
                doc.is_overdue = False

    @api.depends('review_requested_on', 'reviewed_on')
    def _compute_approval_duration(self):
        for doc in self:
            if doc.review_requested_on and doc.reviewed_on:
                delta = doc.reviewed_on - doc.review_requested_on
                doc.approval_duration = delta.total_seconds() / 86400.0
            else:
                doc.approval_duration = 0.0

    # --- Constraints and Onchange ---
    @api.constrains('name', 'status')
    def _check_unique_approved(self):
        for doc in self:
            if doc.status == 'approved':
                others = self.search([
                    ('id', '!=', doc.id),
                    ('name', '=', doc.name),
                    ('status', '=', 'approved'),
                ])
                if others:
                    raise ValidationError(
                        _("Only one approved revision allowed for document %s") % doc.name
                    )

    # @api.onchange('classification_code')
    # def _onchange_classification(self):
    #     if self.classification_code:
    #         record = self.env['bim.classification'].search(
    #             [('code', '=', self.classification_code)], limit=1)
    #         if record:
    #             self.classification_name = record.name
    #             self.classification_description = record.description


class BIMDocumentHistory(models.Model):
    _name = 'bim.document.history'
    _description = 'BIM Document Revision History'
    _order = 'updated_date desc'

    document_id  = fields.Many2one('bim.document', required=True, ondelete='cascade')
    revision     = fields.Char(string='Revision', readonly=True)
    updated_by   = fields.Many2one('res.users', string='Updated By', readonly=True)
    updated_date = fields.Datetime(string='Updated On', readonly=True, default=fields.Datetime.now)
    file         = fields.Binary(string='File', readonly=True)
    file_name    = fields.Char(string='File Name', readonly=True)
