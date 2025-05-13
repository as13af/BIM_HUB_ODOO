/** @odoo-module */

console.log("🚀 js_template.js is loaded!");


import { Component, useState, onWillStart } from "@odoo/owl";
// import { rpc } from "@web/core/network/rpc_service";
import { rpc } from "@web/core/network/rpc_service";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";

// ✅ Correct Import Paths (Ensure files exist at these paths!)
// import { IfcViewerComponent } from "./ifc_viewer/ifc_viewer";
import { ChartRenderer } from "./chart_renderer/chart_renderer";
import { KpiCard } from "./kpi_card/kpi_card";


const CHART_CONFIG = {
    projectTypes: [
        { key: "construction", label: "Construction" },
        { key: "renovation", label: "Renovation" },
        { key: "maintenance", label: "Maintenance" },
        { key: "other", label: "Other" },
    ],
    projectStatuses: [
        { key: "draft", label: "Draft" },
        { key: "active", label: "Active" },
        { key: "completed", label: "Completed" },
        { key: "archived", label: "Archived" },
    ],
    issuePriorities: [
        { key: "low", label: "Low" },
        { key: "medium", label: "Medium" },
        { key: "high", label: "High" },
    ],
    documentStatuses: [
        { key: "draft", label: "Draft" },
        { key: "to_review", label: "To Review" },
        { key: "approved", label: "Approved" },
        { key: "rejected", label: "Rejected" },
    ],
    twinStatuses: [
        { key: "draft", label: "Draft" },
        { key: "active", label: "Active" },
        { key: "needs_sync", label: "Needs Sync" },
        { key: "archived", label: "Archived" },
    ]
};

export class Dashboard extends Component {
    static template = "owl.js_template";
    static components = { ChartRenderer, KpiCard };
  
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            filterDays: 7,
            loading: true,
            error: null,
            metrics: this.initializeMetrics()
        });

        onWillStart(async () => {
            try {
                await this.loadData();
                this.state.loading = false;
                console.log("✅ Metrics Loaded:");
                console.log("  - projectStatusType:", this.state.metrics.projectStatusType);
                console.log("  - issuePriorityType:", this.state.metrics.issuePriorityType);
                console.log("  - documentStatusType:", this.state.metrics.documentStatusType);
                console.log("  - digital_twinStatusType:", this.state.metrics.digital_twinStatusType);
            } catch (error) {
                console.error("Dashboard initialization failed:", error);
                this.state.error = error;
                this.state.loading = false;
            }
        });
    }
    initializeMetrics() {
        return {
            projectCount: 0,
            openIssues: 0,
            pendingDocs: 0,
            approvedDocs: 0,
            needsSync: 0,
            avgSyncProgress: 0,
            overdueReviews: 0,
            avgIssueResolution: 0,
            avgDocApproval: 0,
            issueChart: this.createChartConfig([], []),
            projectTypeChart: this.createChartConfig([], []),
            projectStatusType: this.createChartConfig([], []),
            issuePriorityType: this.createChartConfig([], []),
            documentStatusType: this.createChartConfig([], []),
            digital_twinStatusType: this.createChartConfig([], [])
        };
    }

    async loadData() {
        const [basicMetrics, twinsData] = await Promise.all([
            this.fetchBasicMetrics(),
            this.fetchTwinsData()
        ]);

        const [calculations, charts] = await Promise.all([
            this.fetchCalculations(),
            this.fetchChartData()
        ]);

        this.state.metrics = {
            ...this.state.metrics,
            ...basicMetrics,
            ...twinsData,
            ...calculations,
            ...charts
        };
    }

    async fetchBasicMetrics() {
        const [
            projectCount,
            openIssues,
            pendingDocs,
            approvedDocs,
            needsSync,
            overdueReviews
        ] = await Promise.all([
            this.orm.call("bim.project", "search_count", [[["status", "=", "active"]]]),
            this.orm.call("bim.issue", "search_count", [[["status", "=", "open"]]]),
            this.orm.call("bim.document", "search_count", [[["status", "=", "to_review"]]]),
            this.orm.call("bim.document", "search_count", [[["status", "=", "approved"]]]),
            this.orm.call("bim.digital.twin", "search_count", [[["status", "=", "needs_sync"]]]),
            this.orm.call("bim.document", "search_count", [[["is_overdue", "=", true]]])
        ]);

        return { projectCount, openIssues, pendingDocs, approvedDocs, needsSync, overdueReviews };
    }

    async fetchTwinsData() {
        const twins = await this.orm.call(
            "bim.digital.twin",
            "search_read",
            [[], ["sync_progress"]],
            { limit: 1000 }
        );

        const totalProgress = twins.reduce((sum, t) => sum + (t.sync_progress || 0), 0);
        return {
            avgSyncProgress: twins.length ? (totalProgress / twins.length).toFixed(1) : 0
        };
    }

    async fetchCalculations() {
        const [avgIssueResolution, avgDocApproval] = await Promise.all([
            this.orm.call("bim.issue", "calculate_avg_resolution", []),
            this.orm.call("bim.document", "calculate_avg_approval", [])
        ]);

        return { avgIssueResolution, avgDocApproval };
    }

    async fetchChartData() {
        const [
            issueStatusCounts,
            typeCounts,
            projectStatusCounts,
            issuePriorityCounts,
            documentStatusCounts,
            twinStatusCounts
        ] = await Promise.all([
            this.fetchStatusCounts("bim.issue", ["open", "in_progress", "resolved", "closed"], "status"),
            this.fetchTypeCounts("bim.project", CHART_CONFIG.projectTypes, "project_type"),
            this.fetchStatusCounts("bim.project", CHART_CONFIG.projectStatuses, "status"),
            this.fetchStatusCounts("bim.issue", CHART_CONFIG.issuePriorities, "priority"),
            this.fetchStatusCounts("bim.document", CHART_CONFIG.documentStatuses, "status"),
            this.fetchStatusCounts("bim.digital.twin", CHART_CONFIG.twinStatuses, "status")
        ]);

        return {
            issueChart: this.createChartConfig(
                ["Open", "In Progress", "Resolved", "Closed"],
                issueStatusCounts,
                ["#f44336", "#ff9800", "#4caf50", "#9e9e9e"]
            ),
            projectTypeChart: this.createChartConfig(
                CHART_CONFIG.projectTypes.map(t => t.label),
                typeCounts,
                ["#2196f3", "#4caf50", "#ff9800", "#9e9e9e"]
            ),
            projectStatusType: this.createChartConfig(
                CHART_CONFIG.projectStatuses.map(s => s.label),
                projectStatusCounts,
                ["#2196f3", "#4caf50", "#ff9800", "#9e9e9e"]
            ),
            issuePriorityType: this.createChartConfig(
                CHART_CONFIG.issuePriorities.map(p => p.label),
                issuePriorityCounts,
                ["#4caf50", "#ff9800", "#f44336"]
            ),
            documentStatusType: this.createChartConfig(
                CHART_CONFIG.documentStatuses.map(s => s.label),
                documentStatusCounts,
                ["#9e9e9e", "#ff9800", "#4caf50", "#f44336"]
            ),
            digital_twinStatusType: this.createChartConfig(
                CHART_CONFIG.twinStatuses.map(s => s.label),
                twinStatusCounts,
                ["#2196f3", "#4caf50", "#ff9800", "#9e9e9e"]
            )
        };
    }

    async fetchStatusCounts(model, items, field) {
        return Promise.all(
            items.map(item => 
                this.orm.call(model, "search_count", [[[field, "=", item.key]]])
            )
        );
    }

    async fetchTypeCounts(model, types, field) {
        return Promise.all(
            types.map(type => 
                this.orm.call(model, "search_count", [[[field, "=", type.key]]])
            )
        );
    }

    createChartConfig(labels = [], data = [], colors = []) {
        const filledData = labels.map((_, i) => data[i] || 0);
        const filledColors = labels.map((_, i) => colors[i] || '#ccc');

        return {
            labels,
            datasets: [{
                data: filledData,
                backgroundColor: filledColors,
                hoverOffset: 4
            }]
        };
    }

}

// Update template and registry
// Dashboard.template = "owl.js_template";
// Dashboard.components = {KpiCard, ChartRenderer}
// Register the client action under a custom tag
registry.category("actions").add("owl.js_template", Dashboard);

console.log("✅ registry:", registry);
const actions = registry.category("actions").getAll();
console.log("✅ Registered Actions:", actions.map(a => a.name || "unnamed"));
// console.log("Project Status Data:", this.state.metrics.projectStatusType);
// console.log("Issue Priority Data:", this.state.metrics.issuePriorityType);
// console.log("Document Status Data:", this.state.metrics.documentStatusType);
// console.log("Twin Status Data:", this.state.metrics.digital_twinStatusType);