from odoo import models, fields

class Issue(models.Model):
    _name = 'bim.issue'
    _description = 'BIM Issue'

    name = fields.Char(string='Issue Name', required=True)
