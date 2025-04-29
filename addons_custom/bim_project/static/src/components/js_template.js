/** @odoo-module */

console.log("🚀 js_template.js is loaded!");


import { Component, useState, onWillStart } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc_service";
import { registry } from "@web/core/registry";

// ✅ Correct Import Paths (Ensure files exist at these paths!)
// import { IfcViewerComponent } from "./ifc_viewer/ifc_viewer";
import { ChartRenderer } from "./chart_renderer/chart_renderer";
import { KpiCard } from "./kpi_card/kpi_card";


export class JsTemplate extends Component {
    setup() {
        // this.modelId = 1;  // or dynamically passed in from context/view
    }

    // async loadIFCModel() {
    //     const container = document.getElementById("ifc-viewer-container");

    //     // ✅ Initialize Three.js + IFC.js
    //     const viewer = new IfcViewerAPI({ container });
    //     viewer.grid.setGrid();
    //     viewer.axes.setAxes();

    //     // ✅ Load IFC
    //     const ifcURL = `/bim/ifc/${this.modelId}`;
    //     await viewer.IFC.loadIfcUrl(ifcURL);
    // }

    // onMounted() {
    //     this.loadIFCModel();
    // }
}

// Update template and registry
JsTemplate.template = "owl.js_template";
JsTemplate.components = {KpiCard, ChartRenderer}

// ✅ Register the Component in OWL Registry
registry.category("actions").add("owl.js_template", JsTemplate);

// ✅ Debugging the registry
console.log("✅ registry:", registry);
console.log("✅ Actions in registry:", registry.category("actions").keys());
