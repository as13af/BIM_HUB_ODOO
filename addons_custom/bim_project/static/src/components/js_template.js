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


const projectTypes = [
{ key: "construction", label: "Construction" },
{ key: "renovation", label: "Renovation" },
{ key: "maintenance", label: "Maintenance" },
{ key: "other", label: "Other" },
];

const projectStatuses = [
  { key: "draft", label: "Draft" },
  { key: "active", label: "Active" },
  { key: "completed", label: "Completed" },
  { key: "archived", label: "Archived" },
];

const issuePriorities = [
  { key: "low", label: "Low" },
  { key: "medium", label: "Medium" },
  { key: "high", label: "High" },
];

const documentStatuses = [
  { key: "draft", label: "Draft" },
  { key: "to_review", label: "To Review" },
  { key: "approved", label: "Approved" },
  { key: "rejected", label: "Rejected" },
];

const twinStatuses = [
  { key: "draft", label: "Draft" },
  { key: "active", label: "Active" },
  { key: "needs_sync", label: "Needs Sync" },
  { key: "archived", label: "Archived" },
];

export class Dashboard extends Component {
    static template = "owl.js_template";
    static components = { ChartRenderer, KpiCard };
  
    setup() {
      this.orm = useService("orm")
      // this.rpc = useService("rpc");
      // Reactive state for filters and metrics
      this.state = useState({
        filterDays: 7,
        metrics: {
          projectCount: 0,
          openIssues: 0,
          pendingDocs: 0,
          approvedDocs: 0,
          needsSync: 0,
          avgSyncProgress: 0,
          overdueReviews: 0,
          avgIssueResolution: 0,
          avgDocApproval: 0,
          issueChart: { labels: [], datasets: [] },
          projectTypeCounts:{},
          projectStatusType:{},
          issuePriorityType:{},
          documentStatusType:{},
          digital_twinStatusType:{},
        },
      });
  
      // Load everything before rendering
      onWillStart(async () => {
        try {
          // 1. Active Projects
          this.state.metrics.projectCount = await this.orm.call(
            "bim.project",
            "search_count",
            [[["status", "=", "active"]]]
          );
  
          // 2. Open Issues
          this.state.metrics.openIssues = await this.orm.call(
            "bim.issue",
            "search_count",
            [[["status", "=", "open"]]]
          );
  
          // 3. Document statuses
          this.state.metrics.pendingDocs = await this.orm.call(
            "bim.document",
            "search_count",
            [[["status", "=", "to_review"]]]
          );
  
          this.state.metrics.approvedDocs = await this.orm.call(
            "bim.document",
            "search_count",
            [[["status", "=", "approved"]]]
          );
  
          // 4. Digital Twin sync metrics
          this.state.metrics.needsSync = await this.orm.call(
            "bim.digital.twin",
            "search_count",
            [[["status", "=", "needs_sync"]]]
          );
  
          const twins = await this.orm.call(
            "bim.digital.twin",
            "search_read",
            [[], ["sync_progress"]]
          );
  
          const totalProgress = twins.reduce(
            (sum, t) => sum + (t.sync_progress || 0),
            0
          );
          this.state.metrics.avgSyncProgress = (
            totalProgress / (twins.length || 1)
          ).toFixed(1);
  
          // 5. Overdue document reviews
          this.state.metrics.overdueReviews = await this.orm.call(
            "bim.document",
            "search_count",
            [[["is_overdue", "=", true]]]
          );
  
          // 6. Average resolution & approval times (server methods)
          this.state.metrics.avgIssueResolution = await this.orm.call(
            "bim.issue",
            "calculate_avg_resolution",
            []
          );
  
          this.state.metrics.avgDocApproval = await this.orm.call(
            "bim.document",
            "calculate_avg_approval",
            []
          );
  
          // 7. Issue status chart data
          const statusLabels = ["Open", "In Progress", "Resolved", "Closed"];
          const statuses = ["open", "in_progress", "resolved", "closed"];
  
          const counts = await Promise.all(
            statuses.map((s) =>
              this.orm.call("bim.issue", "search_count", [[["status", "=", s]]])
            )
          );

          this.state.metrics.issueChart = {
            labels: statusLabels,
            datasets: [
              {
                data: counts,
                backgroundColor: ["#f44336", "#ff9800", "#4caf50", "#9e9e9e"],
              },
            ],
          };
                // 8. Project Type Distribution
              const typeCounts = await Promise.all(
                  projectTypes.map((type) =>
                      this.orm.call("bim.project", "search_count", [[["project_type", "=", type.key]]])
                  )
              );

              this.state.metrics.projectTypeChart = {
                  labels: projectTypes.map((type) => type.label),
                  datasets: [
                      {
                          data: typeCounts,
                          backgroundColor: ["#2196f3", "#4caf50", "#ff9800", "#9e9e9e"],
                      },
                  ],
              };

        //9. Fetch counts for project statuses
        const projectCounts = await Promise.all(
          projectStatuses.map((status) =>
            this.orm.call("bim.project", "search_count", [[["status", "=", status.key]]])
          )
        );
        this.state.metrics.projectStatusType = projectStatuses.reduce((acc, status, idx) => {
          acc[status.label] = projectCounts[idx];
          return acc;
        }, {});

        //10. Fetch counts for issue priorities
        const issueCounts = await Promise.all(
          issuePriorities.map((priority) =>
            this.orm.call("bim.issue", "search_count", [[["priority", "=", priority.key]]])
          )
        );
        this.state.metrics.issuePriorityType = issuePriorities.reduce((acc, priority, idx) => {
          acc[priority.label] = issueCounts[idx];
          return acc;
        }, {});

        //11. Fetch counts for document statuses
        const documentCounts = await Promise.all(
          documentStatuses.map((status) =>
            this.orm.call("bim.document", "search_count", [[["status", "=", status.key]]])
          )
        );
        this.state.metrics.documentStatusType = documentStatuses.reduce((acc, status, idx) => {
          acc[status.label] = documentCounts[idx];
          return acc;
        }, {});

        //12. Fetch counts for digital twin statuses
        const twinCounts = await Promise.all(
          twinStatuses.map((status) =>
            this.orm.call("bim.digital.twin", "search_count", [[["status", "=", status.key]]])
          )
        );
        this.state.metrics.digital_twinStatusType = twinStatuses.reduce((acc, status, idx) => {
          acc[status.label] = twinCounts[idx];
          return acc;
        }, {});
        } catch (error) {
          console.error("Error fetching dashboard metrics:", error);
        }

      });
  
    //   // Optionally do chart re-init or dynamic updates here
    //   onMounted(() => {/* no-op */});
    }
  
    // Handler for date-range filter
    // onFilterChange(ev) {
    //   this.state.filterDays = parseInt(ev.target.value, 10) || 0;
    //   // Ideally re-fetch metrics scoped to the last N days
    // }
  }

// Update template and registry
// Dashboard.template = "owl.js_template";
// Dashboard.components = {KpiCard, ChartRenderer}
// Register the client action under a custom tag
registry.category("actions").add("owl.js_template", Dashboard);

console.log("✅ registry:", registry);
const actions = registry.category("actions").getAll();
console.log("✅ Registered Actions:", actions.map(a => a.name || "unnamed"));
