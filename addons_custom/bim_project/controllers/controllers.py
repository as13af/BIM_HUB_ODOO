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

        # 6. Average resolution & approval times
        avg_issue_resolution = env['bim.issue'].calculate_avg_resolution()
        avg_doc_approval = env['bim.document'].calculate_avg_approval()

        # 7. Issue status chart
        status_labels = ["Open", "In Progress", "Resolved", "Closed"]
        statuses = ["open", "in_progress", "resolved", "closed"]
        issue_counts = [
            env['bim.issue'].search_count([('status', '=', status)])
            for status in statuses
        ]
        issue_chart = {
            'labels': status_labels,
            'datasets': [{
                'data': issue_counts,
                'backgroundColor': ["#f44336", "#ff9800", "#4caf50", "#9e9e9e"],
            }],
        }

        # 8. Project status distribution
        project_statuses = ['draft', 'active', 'completed', 'archived']
        project_status_labels = ['Draft', 'Active', 'Completed', 'Archived']
        project_status_counts = [
            env['bim.project'].search_count([('status', '=', status)])
            for status in project_statuses
        ]
        project_status_chart = {
            'labels': project_status_labels,
            'datasets': [{
                'data': project_status_counts,
                'backgroundColor': ['#607d8b', '#2196f3', '#4caf50', '#9e9e9e'],
            }],
        }

        # 9. Issue priority distribution
        priorities = ['low', 'medium', 'high']
        priority_labels = ['Low', 'Medium', 'High']
        priority_counts = [
            env['bim.issue'].search_count([('priority', '=', level)])
            for level in priorities
        ]
        issue_priority_chart = {
            'labels': priority_labels,
            'datasets': [{
                'data': priority_counts,
                'backgroundColor': ['#8bc34a', '#ffc107', '#f44336'],
            }],
        }

        # 10. Document status distribution
        doc_statuses = ['draft', 'to_review', 'approved', 'rejected']
        doc_status_labels = ['Draft', 'To Review', 'Approved', 'Rejected']
        doc_status_counts = [
            env['bim.document'].search_count([('status', '=', status)])
            for status in doc_statuses
        ]
        document_status_chart = {
            'labels': doc_status_labels,
            'datasets': [{
                'data': doc_status_counts,
                'backgroundColor': ['#9e9e9e', '#ffc107', '#4caf50', '#f44336'],
            }],
        }

        # 11. Digital Twin status distribution
        twin_statuses = ['draft', 'active', 'needs_sync', 'archived']
        twin_status_labels = ['Draft', 'Active', 'Needs Sync', 'Archived']
        twin_status_counts = [
            env['bim.digital.twin'].search_count([('status', '=', status)])
            for status in twin_statuses
        ]
        digital_twin_status_chart = {
            'labels': twin_status_labels,
            'datasets': [{
                'data': twin_status_counts,
                'backgroundColor': ['#9e9e9e', '#2196f3', '#ff9800', '#607d8b'],
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
            'projectStatusChart': project_status_chart,
            'issuePriorityChart': issue_priority_chart,
            'documentStatusChart': document_status_chart,
            'digitalTwinStatusChart': digital_twin_status_chart,
        }
