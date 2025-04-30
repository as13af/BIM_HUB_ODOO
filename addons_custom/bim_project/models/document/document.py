from odoo import models, fields
from datetime import timedelta, datetime

class BIMDocument(models.Model):
    _name = 'bim.document'
    _description = 'BIM Document'

    name = fields.Char(string='Document Name', required=True)
    description = fields.Text(string='Description')
    file = fields.Binary(string='File')
    file_name = fields.Char(string='File Name')
    file_type = fields.Selection([
        ('ifc', 'IFC'),
        ('bcf', 'BCF'),
        ('pdf', 'PDF'),
        ('dwg', 'DWG'),
        ('jpg', 'JPEG'),
        ('png', 'PNG'),
        ('other', 'Other'),
    ], string='File Type', default='other')
    classification_code = fields.Char(string='Classification Code')
    classification_name = fields.Char(string='Classification Name')
    classification_description = fields.Text(string='Classification Description')
    revision = fields.Char(string='Revision')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft')
    created_by = fields.Many2one('res.users', string='Created By')
    created_date = fields.Datetime(string='Created Date', default=fields.Datetime.now)
    modified_by = fields.Many2one('res.users', string='Modified By')
    modified_date = fields.Datetime(string='Modified Date')
    project_id = fields.Many2one('bim.project', string='Project')
    issue_ids = fields.One2many('bim.issue', 'document_id', string='Issues')
    comments = fields.One2many('bim.document.comment', 'document_id', string='Comments')
