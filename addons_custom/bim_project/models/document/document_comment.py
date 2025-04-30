from odoo import models, fields

class BIMDocumentComment(models.Model):
    _name = 'bim.document.comment'
    _description = 'BIM Document Comment'
    _order = 'create_date desc'

    document_id = fields.Many2one('bim.document', string='Document', required=True, ondelete='cascade')
    parent_comment_id = fields.Many2one('bim.document.comment', string='Reply To', ondelete='cascade')
    child_comment_ids = fields.One2many('bim.document.comment', 'parent_comment_id', string='Replies')

    author_id = fields.Many2one('res.users', string='Author', default=lambda self: self.env.user, required=True)
    comment = fields.Text(string='Comment', required=True)
    status = fields.Selection([
        ('open', 'Open'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='open')

    attachment = fields.Binary(string='Attachment')
    attachment_name = fields.Char(string='Attachment Name')

    create_date = fields.Datetime(string='Created On', readonly=True)
    write_date = fields.Datetime(string='Last Updated', readonly=True)
