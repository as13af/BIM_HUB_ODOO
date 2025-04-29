from odoo import models, fields

class Document(models.Model):
    _name = 'bim.document'
    _description = 'BIM Document'

    name = fields.Char(string='Document Name', required=True)
