from odoo import models, fields, api, _

class BIMIssue(models.Model):
    _name = 'bim.issue'
    _description = 'BIM Issue'

    name = fields.Char(string='Issue Title', required=True)
    description = fields.Text(string='Description')
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='open')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Priority', default='medium')
    due_date = fields.Date(string='Due Date')
    assignee_id = fields.Many2one('res.partner', string='Assigned To')
    reporter_id = fields.Many2one('res.partner', string='Reported By')
    model_id = fields.Many2one('bim.project', string='BIM Model', ondelete='cascade')
    location = fields.Char(string='Location')
    viewpoint = fields.Binary(string='Viewpoint Image')
    bcf_file = fields.Binary(string='BCF File')
    comments = fields.One2many('bim.issue.comment', 'issue_id', string='Comments', ondelete='cascade')
    digital_twin_id = fields.Many2one('bim.digital.twin', string='Digital Twin', ondelete='cascade')
    document_id = fields.Many2one('bim.document', string ='Document', ondelete='cascade')

    @api.model
    def calculate_avg_resolution(self):
        """
        Compute average resolution time (in days) for all issues
        that have been resolved or closed.
        """
        # find all issues that have transitioned to resolved/closed
        issues = self.search([('status', 'in', ['resolved', 'closed']), ('create_date', '!=', False)])
        if not issues:
            return 0.0
        total_days = 0.0
        count = 0
        for issue in issues:
            # use 'write_date' or track a custom resolved_date field
            resolved_date = issue.write_date if issue.status in ('resolved','closed') else None
            if resolved_date:
                delta = resolved_date - issue.create_date
                total_days += delta.days + delta.seconds / 86400.0
                count += 1
        return round(total_days / count, 1) if count else 0.0