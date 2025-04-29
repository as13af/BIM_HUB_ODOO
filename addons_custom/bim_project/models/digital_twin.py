from odoo import models, fields

class DigitalTwin(models.Model):
    _name = 'bim.digital_twin'
    _description = 'BIM Digital Twin'

    name = fields.Char(string='Digital Twin Name', required=True)
