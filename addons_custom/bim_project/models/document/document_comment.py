from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BIMDocumentComment(models.Model):
    _name = 'bim.document.comment'
    _inherit = ['mail.thread']
    _description = 'BIM Document Comment'
    _order = 'create_date desc'

    document_id        = fields.Many2one(
        'bim.document', string='Document', required=True, ondelete='cascade', tracking=True)
    parent_comment_id  = fields.Many2one('bim.document.comment', string='Reply To', ondelete='cascade')
    child_comment_ids  = fields.One2many('bim.document.comment', 'parent_comment_id', string='Replies')
    author_id          = fields.Many2one('res.users', string='Author',
                                         default=lambda self: self.env.user, required=True)
    comment            = fields.Text(string='Comment', required=True, tracking=True)
    status             = fields.Selection([
        ('open',     'Open'),
        ('resolved', 'Resolved'),
        ('closed',   'Closed'),
    ], string='Status', default='open', tracking=True)
    attachment         = fields.Binary(string='Attachment')
    attachment_name    = fields.Char(string='Attachment Name')
    create_date        = fields.Datetime(string='Created On', readonly=True)
    write_date         = fields.Datetime(string='Last Updated', readonly=True)

    @api.model
    def create(self, vals):
        comment = super().create(vals)
        # Post to document chatter
        comment.document_id.message_post(
            body=_("Comment by %s: %s") % (
                comment.author_id.name, comment.comment),
            subtype_xmlid='mail.mt_comment'
        )
        return comment

    @api.constrains('parent_comment_id')
    def _check_no_cyclic_comments(self):
        for c in self:
            ancestor = c.parent_comment_id
            while ancestor:
                if ancestor == c:
                    raise ValidationError(_("You cannot reply to yourself recursively."))
                ancestor = ancestor.parent_comment_id
