/**
 * Knowledge Graph Visualizer for SSOT Rule Engine Dashboard
 */

class KGVisualizer {
    constructor() {
        this.container = document.getElementById('kg-container');
        this.network = null;
        this.data = {
            nodes: new vis.DataSet(),
            edges: new vis.DataSet()
        };
        this.options = {
            nodes: {
                shape: 'dot',
                size: 16,
                font: {
                    size: 12,
                    face: 'Arial'
                }
            },
            edges: {
                width: 1,
                color: { color: '#666666' },
                arrows: {
                    to: { enabled: true, scaleFactor: 0.5 }
                }
            },
            physics: {
                stabilization: false,
                barnesHut: {
                    gravitationalConstant: -80000,
                    springConstant: 0.001,
                    springLength: 200
                }
            }
        };
    }

    async initialize() {
        if (!this.container) {
            console.error('KG container not found');
            return;
        }

        try {
            // Create network
            this.network = new vis.Network(
                this.container,
                this.data,
                this.options
            );

            // Setup event listeners
            this.network.on('selectNode', this._handleNodeSelect.bind(this));
            this.network.on('stabilized', this._handleStabilized.bind(this));

            // Load initial data
            await this.refreshData();

        } catch (error) {
            console.error('Failed to initialize KG visualizer:', error);
            throw error;
        }
    }

    async refreshData() {
        try {
            const response = await fetch('/api/kg/visualize');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Update visualization
            this.data.nodes.clear();
            this.data.edges.clear();
            
            this.data.nodes.add(data.nodes);
            this.data.edges.add(data.edges);

            // Update timestamp
            this._updateTimestamp(data.timestamp);

        } catch (error) {
            console.error('Failed to refresh KG data:', error);
            this._showError(error.message);
        }
    }

    _handleNodeSelect(params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = this.data.nodes.get(nodeId);
            this._showNodeDetails(node);
        }
    }

    _handleStabilized() {
        console.log('Network stabilized');
    }

    _showNodeDetails(node) {
        const detailsElement = document.getElementById('kg-node-details');
        if (!detailsElement) return;

        detailsElement.innerHTML = `
            <h3>${this._escapeHtml(node.label)}</h3>
            <p>Type: ${this._escapeHtml(node.type)}</p>
            <p>ID: ${this._escapeHtml(node.id)}</p>
        `;
    }

    _updateTimestamp(timestamp) {
        const element = document.getElementById('kg-last-update');
        if (element) {
            element.textContent = new Date(timestamp).toLocaleString();
        }
    }

    _showError(message) {
        const element = document.getElementById('kg-error');
        if (element) {
            element.textContent = `Error: ${message}`;
            element.style.display = 'block';
        }
    }

    _escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}

// Initialize visualizer
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const visualizer = new KGVisualizer();
        await visualizer.initialize();

        // Setup refresh button
        const refreshButton = document.getElementById('kg-refresh');
        if (refreshButton) {
            refreshButton.addEventListener('click', () => visualizer.refreshData());
        }

    } catch (error) {
        console.error('Failed to setup KG visualizer:', error);
    }
}); 