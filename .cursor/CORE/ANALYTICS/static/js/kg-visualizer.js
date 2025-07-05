// Initialize the Knowledge Graph visualization
let network = null;
let nodes = new vis.DataSet([]);
let edges = new vis.DataSet([]);

// Configuration for the vis.js network
const options = {
    nodes: {
        shape: 'dot',
        size: 16,
        font: {
            size: 14,
            color: '#2c3e50'
        },
        borderWidth: 2,
        shadow: true
    },
    edges: {
        width: 2,
        color: { color: '#2c3e50', highlight: '#4a90e2' },
        smooth: {
            type: 'continuous'
        },
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
    },
    manipulation: {
        enabled: true,
        addNode: function(nodeData, callback) {
            document.getElementById('node-operation').innerHTML = "Add Node";
            document.getElementById('node-label').value = nodeData.label || "";
            document.getElementById('node-type').value = "";
            document.getElementById('node-modal').style.display = 'block';
            
            document.getElementById('node-saveButton').onclick = async () => {
                nodeData.label = document.getElementById('node-label').value;
                nodeData.title = document.getElementById('node-label').value;
                nodeData.type = document.getElementById('node-type').value;
                nodeData.color = getNodeColor(nodeData.type);
                document.getElementById('node-modal').style.display = 'none';
                
                try {
                    await createKGEntity(nodeData);
                    callback(nodeData);
                } catch (error) {
                    showToast('Failed to create entity: ' + error.message, 'error');
                }
            };
        },
        editNode: function(nodeData, callback) {
            document.getElementById('node-operation').innerHTML = "Edit Node";
            document.getElementById('node-label').value = nodeData.label;
            document.getElementById('node-type').value = nodeData.type || "";
            document.getElementById('node-modal').style.display = 'block';
            
            document.getElementById('node-saveButton').onclick = async () => {
                const oldLabel = nodeData.label;
                nodeData.label = document.getElementById('node-label').value;
                nodeData.title = document.getElementById('node-label').value;
                nodeData.type = document.getElementById('node-type').value;
                nodeData.color = getNodeColor(nodeData.type);
                document.getElementById('node-modal').style.display = 'none';
                
                try {
                    await updateKGEntity(oldLabel, nodeData);
                    callback(nodeData);
                } catch (error) {
                    showToast('Failed to update entity: ' + error.message, 'error');
                }
            };
        },
        deleteNode: async function(data, callback) {
            try {
                await deleteKGEntity(data.nodes[0]);
                callback(data);
            } catch (error) {
                showToast('Failed to delete entity: ' + error.message, 'error');
            }
        },
        addEdge: function(edgeData, callback) {
            document.getElementById('edge-operation').innerHTML = "Add Relation";
            document.getElementById('edge-label').value = "";
            document.getElementById('edge-modal').style.display = 'block';
            
            document.getElementById('edge-saveButton').onclick = async () => {
                edgeData.label = document.getElementById('edge-label').value;
                document.getElementById('edge-modal').style.display = 'none';
                
                try {
                    await createKGRelation(edgeData);
                    callback(edgeData);
                } catch (error) {
                    showToast('Failed to create relation: ' + error.message, 'error');
                }
            };
        },
        deleteEdge: async function(data, callback) {
            try {
                await deleteKGRelation(data.edges[0]);
                callback(data);
            } catch (error) {
                showToast('Failed to delete relation: ' + error.message, 'error');
            }
        }
    }
};

// Initialize the visualization
function initKGVisualizer() {
    const container = document.getElementById('kg-visualizer');
    network = new vis.Network(container, { nodes, edges }, options);
    
    // Add event listeners
    network.on('selectNode', function(params) {
        if (params.nodes.length === 1) {
            const nodeId = params.nodes[0];
            showNodeDetails(nodeId);
        }
    });
    
    // Load initial data
    loadKGData();
}

// Color scheme for different node types
function getNodeColor(type) {
    const colors = {
        'file': '#27ae60',
        'function': '#2980b9',
        'class': '#8e44ad',
        'module': '#c0392b',
        'package': '#d35400',
        'default': '#2c3e50'
    };
    return colors[type] || colors.default;
}

// Load Knowledge Graph data from the backend
async function loadKGData() {
    try {
        const response = await fetch('/api/kg/data');
        const data = await response.json();
        
        // Clear existing data
        nodes.clear();
        edges.clear();
        
        // Add nodes
        data.nodes.forEach(node => {
            nodes.add({
                id: node.id,
                label: node.label,
                title: node.title || node.label,
                type: node.type,
                color: getNodeColor(node.type)
            });
        });
        
        // Add edges
        data.edges.forEach(edge => {
            edges.add({
                id: edge.id,
                from: edge.from,
                to: edge.to,
                label: edge.label
            });
        });
    } catch (error) {
        console.error('Error loading KG data:', error);
        showToast('Failed to load Knowledge Graph data', 'error');
    }
}

// Show node details in the sidebar
async function showNodeDetails(nodeId) {
    try {
        const response = await fetch(`/api/kg/node/${nodeId}`);
        const nodeData = await response.json();
        
        const detailsContainer = document.getElementById('node-details');
        detailsContainer.innerHTML = `
            <h3>${nodeData.label}</h3>
            <p><strong>Type:</strong> ${nodeData.type}</p>
            <div class="node-observations">
                <h4>Observations</h4>
                <ul>
                    ${nodeData.observations.map(obs => `<li>${obs}</li>`).join('')}
                </ul>
            </div>
            <div class="node-relations">
                <h4>Relations</h4>
                <ul>
                    ${nodeData.relations.map(rel => `
                        <li>${rel.from} <strong>${rel.type}</strong> ${rel.to}</li>
                    `).join('')}
                </ul>
            </div>
        `;
    } catch (error) {
        console.error('Error loading node details:', error);
        showToast('Failed to load node details', 'error');
    }
}

// API functions for Knowledge Graph operations
async function createKGEntity(nodeData) {
    const response = await fetch('/api/kg/entity', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: nodeData.label,
            entityType: nodeData.type,
            observations: []
        })
    });
    
    if (!response.ok) {
        throw new Error('Failed to create entity');
    }
}

async function updateKGEntity(oldName, nodeData) {
    const response = await fetch('/api/kg/entity', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            oldName,
            newName: nodeData.label,
            entityType: nodeData.type
        })
    });
    
    if (!response.ok) {
        throw new Error('Failed to update entity');
    }
}

async function deleteKGEntity(nodeId) {
    const response = await fetch(`/api/kg/entity/${nodeId}`, {
        method: 'DELETE'
    });
    
    if (!response.ok) {
        throw new Error('Failed to delete entity');
    }
}

async function createKGRelation(edgeData) {
    const response = await fetch('/api/kg/relation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            from: edgeData.from,
            to: edgeData.to,
            relationType: edgeData.label
        })
    });
    
    if (!response.ok) {
        throw new Error('Failed to create relation');
    }
}

async function deleteKGRelation(edgeId) {
    const response = await fetch(`/api/kg/relation/${edgeId}`, {
        method: 'DELETE'
    });
    
    if (!response.ok) {
        throw new Error('Failed to delete relation');
    }
}

// Initialize when the page loads
document.addEventListener('DOMContentLoaded', initKGVisualizer); 