from odoo import models, fields, api, _


class BIMIssue(models.Model):
    _name = 'bim.issue'
    _description = 'BIM Issue'

    name = fields.Char(string='Issue Title', readonly=True, store=True)
    description = fields.Text(string='Description')
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='open', index=True)
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Priority', default='medium', index=True)
    issue_type = fields.Selection([
        ('design', 'Designing Phase'),
        ('construction', 'Construction Phase'),
        ('post_construction', 'Post Construction'),
    ], string='Issue Type', index=True)
    created_date = fields.Date(string='Issue Created Date', default=fields.Date.context_today)
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
    def create(self, vals):
        record = super(BIMIssue, self).create(vals)

        def safe_get_name(entity, default='UNKNOWN'):
            return entity.name.upper() if entity and entity.name else default

        def abbreviate(name):
            # Better abbreviation logic: first 3 characters or uppercase initials
            words = name.split()
            if len(words) == 1:
                return name[:3].upper()
            return ''.join([w[0] for w in words]).upper()

        # Extract and format info
        reporter_abbr = abbreviate(safe_get_name(record.reporter_id))
        assignee_abbr = abbreviate(safe_get_name(record.assignee_id))
        project_name = (record.model_id.name or 'UNNAMED').upper().replace(" ", "_")
        issue_id_str = str(record.id).zfill(3)  # Padded issue ID like 001, 012

        created_str = record.created_date.strftime('%Y%m%d') if record.created_date else 'XXXXXX'
        due_str = record.due_date.strftime('%Y%m%d') if record.due_date else 'XXXXXX'

        priority_abbr = {'low': 'L', 'medium': 'M', 'high': 'H'}.get(record.priority, 'M')
        project_type_abbr = {
            'construction': 'C',
            'renovation': 'R',
            'maintenance': 'M',
            'other': 'O'
        }.get(record.model_id.project_type, 'O')

        issue_type_abbr = {
            'design': 'DES',
            'construction': 'CONS',
            'post_construction': 'PC'
        }.get(record.issue_type, 'NA')

        # Construct the final name
        record.name = (
            f"ISSUE-{issue_id_str}-"
            f"{reporter_abbr}-{assignee_abbr}-"
            f"{created_str}-{project_name}-"
            f"{due_str}-{priority_abbr}-"
            f"{project_type_abbr}-{issue_type_abbr}"
        )

        return record


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

    
    def action_mark_in_progress(self):
        self.write({'status': 'in_progress'})

    def action_mark_resolved(self):
        self.write({'status': 'resolved'})

    def action_mark_closed(self):
        self.write({'status': 'closed'})