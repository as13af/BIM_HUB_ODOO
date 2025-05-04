from odoo import models, fields

class BIMIssue(models.Model):
    _name = 'bim.issue'
    _description = 'BIM Issue'

    name = fields.Char(string='Issue Title', required=True)
    description = fields.Text(string='Description')
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='open')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Priority', default='medium')
    due_date = fields.Date(string='Due Date')
    assignee_id = fields.Many2one('res.partner', string='Assigned To')
    reporter_id = fields.Many2one('res.partner', string='Reported By')
    model_id = fields.Many2one('bim.project', string='BIM Model', ondelete='cascade')
    location = fields.Char(string='Location')
    viewpoint = fields.Binary(string='Viewpoint Image')
    bcf_file = fields.Binary(string='BCF File')
    comments = fields.One2many('bim.issue.comment', 'issue_id', string='Comments', ondelete='cascade')
    digital_twin_id = fields.Many2one('bim.digital.twin', string='Digital Twin', ondelete='cascade')
    document_id = fields.Many2one('bim.document', string ='Document', ondelete='cascade')