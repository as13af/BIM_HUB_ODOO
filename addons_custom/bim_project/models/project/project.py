from odoo import models, fields, api

class BIMProject(models.Model):
    _name = 'bim.project'
    _description = 'BIM Project'

    name = fields.Char(string='Project Name', required=True)
    project_code = fields.Char(string='Project Code')
    description = fields.Text(string='Description')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ], string='Status', default='draft')
    location = fields.Char(string='Location')
    project_type = fields.Char(string='Project Type')
    owner_id = fields.Many2one('res.partner', string='Owner')
    contractor_id = fields.Many2one('res.partner', string='Contractor')
    architect_id = fields.Many2one('res.partner', string='Architect')
    project_manager_id = fields.Many2one('res.partner', string='Project Manager')
    budget = fields.Float(string='Budget')
    currency_id = fields.Many2one('res.currency', string='Currency')
    ifc_model = fields.Binary(string='IFC Model')
    bcf_file = fields.Binary(string='BCF File')
    cobie_file = fields.Binary(string='COBie File')
    documents = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'bim.project')], string='Documents')
