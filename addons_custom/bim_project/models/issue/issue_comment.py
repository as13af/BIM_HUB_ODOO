from odoo import models, fields

class BIMIssueComment(models.Model):
    _name = 'bim.issue.comment'
    _description = 'BIM Issue Comment'
    _order = 'create_date asc'

    issue_id = fields.Many2one('bim.issue', string='Issue', required=True, ondelete='cascade')
    author_id = fields.Many2one('res.users', string='Author', default=lambda self: self.env.user, required=True)
    comment = fields.Text(string='Comment', required=True)
    viewpoint = fields.Binary(string='Viewpoint Image')
    viewpoint_name = fields.Char(string='Viewpoint Name')
    status = fields.Selection([
        ('open', 'Open'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='open')
    create_date = fields.Datetime(string='Created On', readonly=True)
    write_date = fields.Datetime(string='Last Updated', readonly=True)
