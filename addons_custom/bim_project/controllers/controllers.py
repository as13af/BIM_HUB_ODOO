from odoo import http
from odoo.http import request

def generate_chart_data(model, field, keys, labels, colors):
    counts = [
        request.env[model].search_count([(field, '=', key)])
        for key in keys
    ]
    return {
        'labels': labels,
        'datasets': [{
            'data': counts,
            'backgroundColor': colors,
        }],
    }

class BimDashboardController(http.Controller):
    @http.route('/bim/dashboard/metrics', type='json', auth='user')
    def get_dashboard_metrics(self):
        env = request.env

        # Basic counts
        project_count = env['bim.project'].search_count([('status', '=', 'active')])
        open_issues = env['bim.issue'].search_count([('status', '=', 'open')])
        pending_docs = env['bim.document'].search_count([('status', '=', 'to_review')])
        approved_docs = env['bim.document'].search_count([('status', '=', 'approved')])
        needs_sync = env['bim.digital.twin'].search_count([('status', '=', 'needs_sync')])
        overdue_reviews = env['bim.document'].search_count([('is_overdue', '=', True)])

        # Sync progress average
        twins = env['bim.digital.twin'].search_read([], ['sync_progress'])
        sync_values = [t.get('sync_progress', 0) or 0 for t in twins]
        avg_sync_progress = round(sum(sync_values) / len(sync_values), 1) if sync_values else 0.0

        # Averages
        avg_issue_resolution = env['bim.issue'].calculate_avg_resolution()
        avg_doc_approval = env['bim.document'].calculate_avg_approval()

        return {
            'projectCount': project_count,
            'openIssues': open_issues,
            'pendingDocs': pending_docs,
            'approvedDocs': approved_docs,
            'needsSync': needs_sync,
            'avgSyncProgress': avg_sync_progress,
            'overdueReviews': overdue_reviews,
            'avgIssueResolution': avg_issue_resolution,
            'avgDocApproval': avg_doc_approval,
            'issueChart': generate_chart_data(
                'bim.issue', 'status',
                ['open', 'in_progress', 'resolved', 'closed'],
                ['Open', 'In Progress', 'Resolved', 'Closed'],
                ["#f44336", "#ff9800", "#4caf50", "#9e9e9e"]
            ),
            'projectStatusType': generate_chart_data(
                'bim.project', 'status',
                ['draft', 'active', 'completed', 'archived'],
                ['Draft', 'Active', 'Completed', 'Archived'],
                ['#607d8b', '#2196f3', '#4caf50', '#9e9e9e']
            ),
            'issuePriorityType': generate_chart_data(
                'bim.issue', 'priority',
                ['low', 'medium', 'high'],
                ['Low', 'Medium', 'High'],
                ['#8bc34a', '#ffc107', '#f44336']
            ),
            'documentStatusType': generate_chart_data(
                'bim.document', 'status',
                ['draft', 'to_review', 'approved', 'rejected'],
                ['Draft', 'To Review', 'Approved', 'Rejected'],
                ['#9e9e9e', '#ffc107', '#4caf50', '#f44336']
            ),
            'digital_twinStatusType': generate_chart_data(
                'bim.digital.twin', 'status',
                ['draft', 'active', 'needs_sync', 'archived'],
                ['Draft', 'Active', 'Needs Sync', 'Archived'],
                ['#9e9e9e', '#2196f3', '#ff9800', '#607d8b']
            ),
        }
