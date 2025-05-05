/** @odoo-module */

console.log("🚀 js_template.js is loaded!");


import { Component, useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";

// ✅ Correct Import Paths (Ensure files exist at these paths!)
// import { IfcViewerComponent } from "./ifc_viewer/ifc_viewer";
import { ChartRenderer } from "./chart_renderer/chart_renderer";
import { KpiCard } from "./kpi_card/kpi_card";


class Dashboard extends Component {
    // static template = "owl.js_template";
    // static components = { ChartRenderer, KpiCard };
  
    setup() {
    //   // Reactive state for filters and metrics
    //   this.state = useState({
    //     filterDays: 7,
    //     metrics: {
    //       projectCount: 0,
    //       openIssues: 0,
    //       pendingDocs: 0,
    //       approvedDocs: 0,
    //       needsSync: 0,
    //       avgSyncProgress: 0,
    //       overdueReviews: 0,
    //       avgIssueResolution: 0,
    //       avgDocApproval: 0,
    //       issueChart: { labels: [], datasets: [] },
    //     },
    //   });
  
    //   // Load everything before rendering
    //   onWillStart(async () => {
    //     // 1. Active Projects
    //     this.state.metrics.projectCount = await rpc({
    //       model: "bim.project",
    //       method: "search_count",
    //       args: [[["status", "=", "active"]]],
    //     });
  
    //     // 2. Open Issues
    //     this.state.metrics.openIssues = await rpc({
    //       model: "bim.issue",
    //       method: "search_count",
    //       args: [[["status", "=", "open"]]],
    //     });
  
    //     // 3. Document statuses
    //     this.state.metrics.pendingDocs = await rpc({
    //       model: "bim.document",
    //       method: "search_count",
    //       args: [[["status", "=", "to_review"]]],
    //     });
    //     this.state.metrics.approvedDocs = await rpc({
    //       model: "bim.document",
    //       method: "search_count",
    //       args: [[["status", "=", "approved"]]],
    //     });
  
    //     // 4. Digital Twin sync metrics
    //     this.state.metrics.needsSync = await rpc({
    //       model: "bim.digital.twin",
    //       method: "search_count",
    //       args: [[["status", "=", "needs_sync"]]],
    //     });
    //     const twins = await rpc({
    //       model: "bim.digital.twin",
    //       method: "search_read",
    //       args: [[], ["sync_progress"]],
    //     });
    //     this.state.metrics.avgSyncProgress = (
    //       twins.reduce((sum, t) => sum + (t.sync_progress || 0), 0) / (twins.length || 1)
    //     ).toFixed(1);
  
    //     // 5. Overdue document reviews
    //     this.state.metrics.overdueReviews = await rpc({
    //       model: "bim.document",
    //       method: "search_count",
    //       args: [[["is_overdue", "=", true]]],
    //     });
  
    //     // 6. Average resolution & approval times (server methods)
    //     this.state.metrics.avgIssueResolution = await rpc({
    //       model: "bim.issue",
    //       method: "calculate_avg_resolution",
    //       args: [],
    //     });
    //     this.state.metrics.avgDocApproval = await rpc({
    //       model: "bim.document",
    //       method: "calculate_avg_approval",
    //       args: [],
    //     });
  
    //     // 7. Issue status chart data
    //     const statusLabels = ["Open", "In Progress", "Resolved", "Closed"];
    //     const statuses = ["open", "in_progress", "resolved", "closed"];
    //     const counts = await Promise.all(statuses.map(s =>
    //       rpc({
    //         model: "bim.issue",
    //         method: "search_count",
    //         args: [[["status", "=", s]]],
    //       })
    //     ));
    //     this.state.metrics.issueChart = {
    //       labels: statusLabels,
    //       datasets: [{
    //         data: counts,
    //         backgroundColor: ["#f44336","#ff9800","#4caf50","#9e9e9e"],
    //       }],
    //     };
    //   });
  
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
Dashboard.template = "owl.js_template";
Dashboard.components = {KpiCard, ChartRenderer}
// Register the client action under a custom tag
registry.category("actions").add("owl.js_template", Dashboard);

console.log("✅ registry:", registry);
const actions = registry.category("actions").getAll();
console.log("✅ Registered Actions:", actions.map(a => a.name || "unnamed"));
