from odoo import models, fields

class Project(models.Model):
    _name = 'bim.project'
    _description = 'BIM Project'

    name = fields.Char(string='Project Name', required=True)
