// Utility function to copy text to clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!');
    } catch (err) {
        console.error('Failed to copy text: ', err);
        showToast('Failed to copy to clipboard', 'error');
    }
}

// Toast notification system
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Remove after animation
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Fetch and display health metrics
async function updateHealthMetrics() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        const healthScores = document.getElementById('health-scores');
        healthScores.innerHTML = '';
        
        for (const [metric, value] of Object.entries(data)) {
            const card = document.createElement('div');
            card.className = 'metric-card';
            
            // Add appropriate icon based on score
            const scoreClass = value >= 80 ? 'excellent' : value >= 60 ? 'good' : value >= 40 ? 'warning' : 'critical';
            
            card.innerHTML = `
                <h4>${metric.replace(/_/g, ' ').toUpperCase()}</h4>
                <div class="metric-value ${scoreClass}">${value.toFixed(1)}%</div>
                <div class="metric-trend">
                    <span class="trend-indicator ${value >= 50 ? 'up' : 'down'}"></span>
                    <span class="trend-text">${value >= 50 ? 'Good' : 'Needs Attention'}</span>
                </div>
            `;
            healthScores.appendChild(card);
        }
    } catch (error) {
        console.error('Error fetching health metrics:', error);
        showToast('Failed to update health metrics', 'error');
    }
}

// Fetch and display rule engine status
async function updateRuleEngine() {
    try {
        const response = await fetch('/api/rule-engine/status');
        const data = await response.json();
        
        // Display triggers
        const triggerList = document.getElementById('trigger-list');
        triggerList.innerHTML = '';
        
        for (const [trigger, description] of Object.entries(data.available_triggers)) {
            const triggerItem = document.createElement('div');
            triggerItem.className = 'trigger-item';
            triggerItem.innerHTML = `
                <div class="trigger-header">
                    <h4>${trigger}</h4>
                    <button class="copy-btn" onclick="copyToClipboard('${trigger}')">
                        <i class="fas fa-copy"></i>
                    </button>
                </div>
                <p>${description}</p>
                <div class="trigger-actions">
                    <button class="action-btn" onclick="executeTrigger('${trigger}')">
                        Execute
                    </button>
                    <button class="info-btn" onclick="showTriggerInfo('${trigger}')">
                        <i class="fas fa-info-circle"></i>
                    </button>
                </div>
            `;
            triggerList.appendChild(triggerItem);
        }
        
        // Display rule statistics
        const ruleStats = document.getElementById('rule-stats');
        ruleStats.innerHTML = `
            <div class="rule-stat">
                <div class="stat-icon"><i class="fas fa-file-code"></i></div>
                <div class="stat-info">
                    <span>Template Count</span>
                    <span class="stat-value">${data.template_count}</span>
                </div>
            </div>
            <div class="rule-stat">
                <div class="stat-icon"><i class="fas fa-check-circle"></i></div>
                <div class="stat-info">
                    <span>Active Rules</span>
                    <span class="stat-value">${data.active_rules}</span>
                </div>
            </div>
            <div class="rule-stat">
                <div class="stat-icon"><i class="fas fa-clock"></i></div>
                <div class="stat-info">
                    <span>Staged Rules</span>
                    <span class="stat-value">${data.staged_rules}</span>
                </div>
            </div>
        `;

        // Update rule effectiveness chart if it exists
        if (data.rule_effectiveness) {
            updateRuleEffectivenessChart(data.rule_effectiveness);
        }
    } catch (error) {
        console.error('Error fetching rule engine status:', error);
        showToast('Failed to update rule engine status', 'error');
    }
}

// Execute a trigger
async function executeTrigger(trigger) {
    try {
        const context = await getTriggerContext(trigger);
        if (!context) return;

        const response = await fetch('/api/rule-engine/trigger', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                trigger,
                context
            })
        });

        const data = await response.json();
        if (data.error) {
            showToast(data.error, 'error');
        } else {
            showToast(`Successfully executed ${trigger}`);
            updateRuleEngine(); // Refresh the display
        }
    } catch (error) {
        console.error('Error executing trigger:', error);
        showToast('Failed to execute trigger', 'error');
    }
}

// Get context for trigger execution
async function getTriggerContext(trigger) {
    const contextTemplate = {
        "!!-GENERATE-RULES-!!": {
            project_type: "web",
            framework: "react",
            language: "typescript"
        },
        "!!-UPDATE-RULES-!!": {
            rules_dir: ".cursor/rules"
        },
        "!!-ANALYZE-CODEBASE-!!": {
            codebase_path: "."
        },
        "!!-IMPORT-RULES-!!": {
            source_path: ".cursor/CORE/RULE-ENGINE/rule_templates"
        }
    };

    // Show context dialog
    const context = contextTemplate[trigger] || {};
    return new Promise((resolve) => {
        const dialog = document.createElement('div');
        dialog.className = 'context-dialog';
        dialog.innerHTML = `
            <div class="dialog-content">
                <h3>Configure ${trigger}</h3>
                <form id="contextForm">
                    ${Object.entries(context).map(([key, value]) => `
                        <div class="form-group">
                            <label for="${key}">${key}:</label>
                            <input type="text" id="${key}" value="${value}">
                        </div>
                    `).join('')}
                    <div class="dialog-actions">
                        <button type="submit" class="primary-btn">Execute</button>
                        <button type="button" class="secondary-btn" onclick="this.closest('.context-dialog').remove()">Cancel</button>
                    </div>
                </form>
            </div>
        `;

        document.body.appendChild(dialog);

        document.getElementById('contextForm').onsubmit = (e) => {
            e.preventDefault();
            const formData = {};
            Object.keys(context).forEach(key => {
                formData[key] = document.getElementById(key).value;
            });
            dialog.remove();
            resolve(formData);
        };
    });
}

// Show trigger information
function showTriggerInfo(trigger) {
    const triggerInfo = {
        "!!-GENERATE-RULES-!!": {
            description: "Generates new project-specific rules based on project type, framework, and language.",
            usage: "Use this trigger when starting a new project or adding new rule templates.",
            examples: [
                "Generate React/TypeScript rules",
                "Generate Python/Django rules"
            ]
        },
        "!!-UPDATE-RULES-!!": {
            description: "Updates existing rules with new context or changes.",
            usage: "Use when project requirements or standards change.",
            examples: [
                "Update coding standards",
                "Modify existing rules"
            ]
        },
        "!!-ANALYZE-CODEBASE-!!": {
            description: "Analyzes the codebase to generate appropriate rules.",
            usage: "Use for existing projects to create matching rules.",
            examples: [
                "Analyze current patterns",
                "Generate rules from code"
            ]
        },
        "!!-IMPORT-RULES-!!": {
            description: "Imports and adapts external rules to your project.",
            usage: "Use when incorporating rules from other sources.",
            examples: [
                "Import company standards",
                "Adapt external rules"
            ]
        }
    };

    const info = triggerInfo[trigger];
    if (!info) return;

    const dialog = document.createElement('div');
    dialog.className = 'info-dialog';
    dialog.innerHTML = `
        <div class="dialog-content">
            <h3>${trigger}</h3>
            <div class="info-section">
                <h4>Description</h4>
                <p>${info.description}</p>
            </div>
            <div class="info-section">
                <h4>When to Use</h4>
                <p>${info.usage}</p>
            </div>
            <div class="info-section">
                <h4>Examples</h4>
                <ul>
                    ${info.examples.map(example => `<li>${example}</li>`).join('')}
                </ul>
            </div>
            <button class="close-btn" onclick="this.closest('.info-dialog').remove()">Close</button>
        </div>
    `;

    document.body.appendChild(dialog);
}

// Update rule effectiveness chart
function updateRuleEffectivenessChart(data) {
    const ctx = document.getElementById('ruleEffectivenessChart');
    if (!ctx) return;

    if (window.ruleChart) {
        window.ruleChart.destroy();
    }

    window.ruleChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.rule),
            datasets: [{
                label: 'Effectiveness Score',
                data: data.map(d => d.score),
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    updateHealthMetrics();
    updateRuleEngine();
    
    // Refresh every 30 seconds
    setInterval(() => {
        updateHealthMetrics();
        updateRuleEngine();
    }, 30000);
});

// Dashboard main functionality
document.addEventListener('DOMContentLoaded', function() {
    initializeRuleEngine();
    initializeKnowledgeGraph();
    initializeClipboard();
    setupEventListeners();
});

// Rule Engine Functionality
function initializeRuleEngine() {
    const ruleEditor = document.getElementById('rule-editor');
    const rulePreview = document.getElementById('rule-preview');
    const generateButton = document.getElementById('generate-rule');
    const templateSelect = document.getElementById('rule-template');
    const ruleList = document.getElementById('rule-list');

    // Rule Templates
    const templates = {
        'python': {
            name: 'Python Rule',
            extension: '.py',
            template: `def rule_{{name}}(context):
    """
    {{description}}
    """
    # Rule logic here
    pass`
        },
        'typescript': {
            name: 'TypeScript Rule',
            extension: '.ts',
            template: `export function rule{{name}}(context: any): void {
    // {{description}}
    // Rule logic here
}`
        },
        'markdown': {
            name: 'Documentation Rule',
            extension: '.md',
            template: `# {{name}}

## Description
{{description}}

## Usage
- Context requirements
- Expected behavior
- Examples`
        }
    };

    // Populate template select
    Object.entries(templates).forEach(([key, value]) => {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = value.name;
        templateSelect.appendChild(option);
    });

    // Rule Generation
    generateButton.addEventListener('click', () => {
        const name = document.getElementById('rule-name').value;
        const description = document.getElementById('rule-description').value;
        const template = templates[templateSelect.value];

        if (!name || !description) {
            showToast('Please fill in all fields', 'error');
            return;
        }

        const ruleContent = template.template
            .replace(/{{name}}/g, name)
            .replace(/{{description}}/g, description);

        rulePreview.textContent = ruleContent;
        rulePreview.setAttribute('data-filename', `${name}${template.extension}`);

        // Add to rule list
        const ruleItem = document.createElement('div');
        ruleItem.className = 'rule-item';
        ruleItem.innerHTML = `
            <span>${name}${template.extension}</span>
            <div class="rule-actions">
                <button onclick="copyRule(this)">Copy</button>
                <button onclick="saveRule(this)">Save</button>
                <button onclick="deleteRule(this)">Delete</button>
            </div>
        `;
        ruleList.appendChild(ruleItem);

        showToast('Rule generated successfully', 'success');
    });
}

// Knowledge Graph Integration
function initializeKnowledgeGraph() {
    const graphContainer = document.getElementById('knowledge-graph');
    if (!graphContainer) return;

    // Initialize vis.js network
    const nodes = new vis.DataSet();
    const edges = new vis.DataSet();
    const data = { nodes, edges };
    
    const options = {
        nodes: {
            shape: 'dot',
            size: 16,
            font: {
                size: 12,
                face: 'Arial'
            }
        },
        edges: {
            width: 0.15,
            color: { inherit: 'both' },
            smooth: {
                type: 'continuous'
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
            addNode: function(data, callback) {
                // Node creation form
                document.getElementById('node-operation').textContent = 'Add Node';
                document.getElementById('node-form').style.display = 'block';
                document.getElementById('saveButton').onclick = saveNodeData.bind(
                    this, data, callback
                );
            },
            editNode: function(data, callback) {
                // Node edit form
                document.getElementById('node-operation').textContent = 'Edit Node';
                document.getElementById('node-form').style.display = 'block';
                document.getElementById('node-id').value = data.id;
                document.getElementById('node-label').value = data.label;
                document.getElementById('saveButton').onclick = saveNodeData.bind(
                    this, data, callback
                );
            }
        }
    };

    const network = new vis.Network(graphContainer, data, options);

    // Load initial data from memory.jsonl
    fetch('/.cursor/CORE/MEMORY/memory.jsonl')
        .then(response => response.text())
        .then(text => {
            if (text.trim()) {
                const lines = text.trim().split('\n');
                lines.forEach(line => {
                    const entry = JSON.parse(line);
                    if (entry.type === 'node') {
                        nodes.add(entry.data);
                    } else if (entry.type === 'edge') {
                        edges.add(entry.data);
                    }
                });
            }
        })
        .catch(error => console.error('Error loading graph data:', error));

    // Save graph data
    network.on('afterDrawing', () => {
        const graphData = {
            nodes: nodes.get(),
            edges: edges.get()
        };
        localStorage.setItem('graphData', JSON.stringify(graphData));
    });
}

// Clipboard Functionality
function initializeClipboard() {
    document.querySelectorAll('[data-clipboard]').forEach(element => {
        element.addEventListener('click', (e) => {
            const target = e.target.getAttribute('data-clipboard-target');
            const text = document.querySelector(target).textContent;
            
            navigator.clipboard.writeText(text).then(() => {
                showToast('Copied to clipboard!', 'success');
            }).catch(err => {
                showToast('Failed to copy', 'error');
                console.error('Copy failed:', err);
            });
        });
    });
}

// Event Listeners
function setupEventListeners() {
    // Rule copy functionality
    window.copyRule = function(button) {
        const ruleContent = button.closest('.rule-item')
            .querySelector('span').textContent;
        navigator.clipboard.writeText(ruleContent)
            .then(() => showToast('Rule copied to clipboard', 'success'))
            .catch(() => showToast('Failed to copy rule', 'error'));
    };

    // Rule save functionality
    window.saveRule = function(button) {
        const filename = button.closest('.rule-item')
            .querySelector('span').textContent;
        const content = document.getElementById('rule-preview').textContent;
        
        fetch('/save-rule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename,
                content
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('Rule saved successfully', 'success');
            } else {
                showToast('Failed to save rule', 'error');
            }
        })
        .catch(() => showToast('Error saving rule', 'error'));
    };

    // Rule delete functionality
    window.deleteRule = function(button) {
        const ruleItem = button.closest('.rule-item');
        const filename = ruleItem.querySelector('span').textContent;
        
        if (confirm(`Delete rule ${filename}?`)) {
            fetch('/delete-rule', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ filename })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    ruleItem.remove();
                    showToast('Rule deleted successfully', 'success');
                } else {
                    showToast('Failed to delete rule', 'error');
                }
            })
            .catch(() => showToast('Error deleting rule', 'error'));
        }
    };
}

// Utility Functions
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }, 100);
}

function saveNodeData(data, callback) {
    data.label = document.getElementById('node-label').value;
    document.getElementById('node-form').style.display = 'none';
    callback(data);
}
    