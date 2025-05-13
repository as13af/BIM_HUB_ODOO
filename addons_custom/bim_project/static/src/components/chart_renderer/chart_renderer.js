/** @odoo-module */

import { Component, onWillStart, onMounted, onWillUpdateProps, onWillUnmount, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";

export class ChartRenderer extends Component {
    setup() {
        this.chartRef = useRef("chart");
        this.chartInstance = null;
        this.chartLoaded = false;

        onWillStart(async () => {
            await loadJS("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js");
            this.chartLoaded = true;
        });

        onMounted(() => {
            if (this.chartLoaded) {
                this.renderChart();
            }
        });

        onWillUpdateProps(() => {
            if (this.chartLoaded) {
                this.updateChart();
            }
        });

        onWillUnmount(() => {
            this.destroyChart();
        });
    }

    renderChart() {
        const canvas = this.chartRef.el;
        if (!canvas) {
            console.warn("⚠️ Canvas not found");
            return;
        }

        const ctx = canvas.getContext('2d');
        if (!ctx) {
            console.warn("⚠️ Failed to get 2D context from canvas");
            return;
        }

        this.chartInstance = new Chart(ctx, {
            type: this.props.type || "doughnut",
            data: this.props.data || { labels: [], datasets: [] },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: !!this.props.title,
                        text: this.props.title,
                        position: 'bottom',
                    },
                },
            },
        });
    }

    updateChart() {
        if (!this.chartInstance || !this.chartInstance.canvas) {
            this.destroyChart();
            this.renderChart(); // Recreate chart if needed
            return;
        }
        
        // Only update if data structure exists
        if (this.props.data?.datasets?.length) {
            this.chartInstance.data = this.props.data;
            this.chartInstance.options.plugins.title.text = this.props.title;
            this.chartInstance.update();
        }
    }

    destroyChart() {
        if (this.chartInstance) {
            this.chartInstance.destroy();
            this.chartInstance = null;
        }
    }
}

ChartRenderer.template = "owl.ChartRenderer";
