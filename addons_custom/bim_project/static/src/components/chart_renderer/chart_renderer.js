// /** @odoo-module */

// import { registry } from "@web/core/registry";
// import { loadJS } from "@web/core/assets";
// const { Component, onWillStart, useRef, onMounted } = owl;

// export class ChartRenderer extends Component {
//     setup() {
//         this.chartRef = useRef("chart");
//         this.chart = null;

//         // Load Chart.js before rendering the component
//         onWillStart(async () => {
//             await loadJS("https://cdn.jsdelivr.net/npm/chart.js");
//         });

//         // Once the component is mounted, render the chart
//         onMounted(() => this.renderChart());
//     }

//     renderChart() {
//         if (this.chart) {
//             this.chart.destroy();  // Destroy previous chart instance before re-rendering
//         }

//         const ctx = this.chartRef.el;

//         // Extracting labels and values from `props.data`
//         const labels = this.props.data.map(d => d.label || d.date);
//         const values = this.props.data.map(d => d.value);

//         this.chart = new Chart(ctx, {
//             type: this.props.type || "bar",  // Default type is 'bar'
//             data: {
//                 labels: labels,
//                 datasets: [{
//                     label: this.props.title || "Chart Data",
//                     data: values,
//                     backgroundColor: [
//                         "rgba(255, 99, 132, 0.5)",
//                         "rgba(54, 162, 235, 0.5)",
//                         "rgba(255, 206, 86, 0.5)",
//                         "rgba(75, 192, 192, 0.5)",
//                         "rgba(153, 102, 255, 0.5)",
//                         "rgba(255, 159, 64, 0.5)"
//                     ],
//                     borderWidth: 1
//                 }]
//             },
//             options: {
//                 responsive: true,
//                 plugins: {
//                     legend: {
//                         position: "bottom",
//                     },
//                     title: {
//                         display: true,
//                         text: this.props.title,
//                         position: "top",
//                     }
//                 }
//             }
//         });
//     }
// }

// ChartRenderer.template = "owl.ChartRenderer";
/** @odoo-module */

import { registry } from "@web/core/registry"
import { loadJS } from "@web/core/assets"
const { Component, onWillStart, useRef, onMounted } = owl

export class ChartRenderer extends Component {
    setup(){
        this.chartRef = useRef("chart")
        onWillStart(async ()=>{
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js")
        })

        onMounted(()=>this.renderChart())
    }

    renderChart(){
        new Chart(this.chartRef.el,
        {
          type: this.props.type,
          data: {
            labels: [
                'Red',
                'Blue',
                'Yellow'
              ],
              datasets: [
              {
                label: 'My First Dataset',
                data: [300, 50, 100],
                hoverOffset: 4
              },{
                label: 'My Second Dataset',
                data: [100, 70, 150],
                hoverOffset: 4
              }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'bottom',
              },
              title: {
                display: true,
                text: this.props.title,
                position: 'bottom',
              }
            }
          },
        }
      );
    }
}

ChartRenderer.template = "owl.ChartRenderer"