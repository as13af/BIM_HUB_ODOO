from odoo import models, fields

class DigitalTwin(models.Model):
    _name = 'bim.digital.twin'
    _description = 'Digital Twin'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    model_file = fields.Binary(string='Model File')
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    ], string='Status', default='active')
    last_updated = fields.Datetime(string='Last Updated')
    project_id = fields.Many2one('bim.project', string='Project')
    issues = fields.One2many('bim.issue', 'digital_twin_id', string='Issues')
    location = fields.Char(string='Location')
    viewpoint = fields.Binary(string='Viewpoint Image')
