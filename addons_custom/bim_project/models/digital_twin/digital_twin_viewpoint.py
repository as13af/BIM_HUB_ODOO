from odoo import models, fields, api, _
from datetime import datetime

class DigitalTwinViewpoint(models.Model):
    _name = 'bim.digital.twin.viewpoint'
    _description = 'Digital Twin Viewpoint History'
    _order = 'captured_on desc'

    twin_id     = fields.Many2one('bim.digital.twin', ondelete='cascade', required=True)
    image       = fields.Binary(string='Viewpoint Image')
    captured_on = fields.Datetime(string='Captured On', readonly=True, default=fields.Datetime.now)
    issue_id = fields.Many2one('bim.issue', string='Related Issue')
