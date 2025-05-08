/** @odoo-module */

import { registry } from "@web/core/registry"
import { Component, onWillStart, useRef, onMounted, onWillUpdateProps, onWillUnmount } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class ChartRenderer extends Component {
    setup() {
        this.chartRef = useRef("chart");
        this.chartInstance = null;

        onWillStart(async () => {
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js");
        });

        onMounted(() => {
            this.renderChart();
        });

        onWillUpdateProps(() => {
            this.updateChart();
        });

        onWillUnmount(() => {
            this.destroyChart();
        });
    }

    renderChart() {
        const ctx = this.chartRef.el.getContext('2d');
        this.chartInstance = new Chart(ctx, {
            type: this.props.type,
            data: this.props.data,
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
                    },
                },
            },
        });
    }

    updateChart() {
        if (this.chartInstance) {
            this.chartInstance.data = this.props.data;
            this.chartInstance.options.plugins.title.text = this.props.title;
            this.chartInstance.update();
        } else {
            this.renderChart();
        }
    }

    destroyChart() {
        if (this.chartInstance) {
            this.chartInstance.destroy();
            this.chartInstance = null;
        }
    }
}

ChartRenderer.template = "owl.ChartRenderer"