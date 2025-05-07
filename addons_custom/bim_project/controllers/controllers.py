from odoo import http
from odoo.http import request

class BimDashboardController(http.Controller):
    @http.route('/bim/dashboard/metrics', type='json', auth='user')
    def get_dashboard_metrics(self):
        env = request.env

        # 1. Active Projects
        project_count = env['bim.project'].search_count([('status', '=', 'active')])

        # 2. Open Issues
        open_issues = env['bim.issue'].search_count([('status', '=', 'open')])

        # 3. Document statuses
        pending_docs = env['bim.document'].search_count([('status', '=', 'to_review')])
        approved_docs = env['bim.document'].search_count([('status', '=', 'approved')])

        # 4. Digital Twin sync metrics
        needs_sync = env['bim.digital.twin'].search_count([('status', '=', 'needs_sync')])
        twins = env['bim.digital.twin'].search_read([], ['sync_progress'])
        avg_sync_progress = (
            sum(twin.get('sync_progress', 0) or 0 for twin in twins) / len(twins)
        ) if twins else 0.0

        # 5. Overdue document reviews
        overdue_reviews = env['bim.document'].search_count([('is_overdue', '=', True)])

        # 6. Average resolution & approval times (assuming these methods are defined)
        avg_issue_resolution = env['bim.issue'].calculate_avg_resolution()
        avg_doc_approval = env['bim.document'].calculate_avg_approval()

        # 7. Issue status chart data
        status_labels = ["Open", "In Progress", "Resolved", "Closed"]
        statuses = ["open", "in_progress", "resolved", "closed"]
        counts = [
            env['bim.issue'].search_count([('status', '=', status)])
            for status in statuses
        ]
        issue_chart = {
            'labels': status_labels,
            'datasets': [{
                'data': counts,
                'backgroundColor': ["#f44336", "#ff9800", "#4caf50", "#9e9e9e"],
            }],
        }

        return {
            'projectCount': project_count,
            'openIssues': open_issues,
            'pendingDocs': pending_docs,
            'approvedDocs': approved_docs,
            'needsSync': needs_sync,
            'avgSyncProgress': round(avg_sync_progress, 1),
            'overdueReviews': overdue_reviews,
            'avgIssueResolution': avg_issue_resolution,
            'avgDocApproval': avg_doc_approval,
            'issueChart': issue_chart,
        }
