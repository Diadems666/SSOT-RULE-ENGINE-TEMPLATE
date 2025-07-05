#!/usr/bin/env python3
"""
Quick Launch Script for SSOT-RULE-ENGINE Analytics Dashboard
Place in project root for easy access
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import webbrowser
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS

# Import rule engine components
rule_engine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                               '.cursor', 'CORE', 'RULE_ENGINE')
sys.path.insert(0, rule_engine_path)

from rule_generator import RuleGenerator
from engine_integration import RuleEngineIntegration

# Initialize Flask app
app = Flask(__name__, 
    static_folder='.cursor/CORE/ANALYTICS/static',
    template_folder='.cursor/CORE/ANALYTICS/templates')
CORS(app)

# Initialize components
rule_engine = RuleEngineIntegration()
logger = logging.getLogger(__name__)

class DashboardManager:
    def __init__(self):
        self.base_dir = ".cursor/CORE"
        self.analytics_dir = os.path.join(self.base_dir, "ANALYTICS")
        self.ssot_dir = os.path.join(self.base_dir, "SSOT")
        self.rule_engine_dir = os.path.join(self.base_dir, "RULE-ENGINE")
        self._ensure_directories()
        self._setup_logging()

    def _ensure_directories(self):
        """Ensure required directories exist"""
        directories = [
            self.analytics_dir,
            self.ssot_dir,
            self.rule_engine_dir,
            os.path.join(self.analytics_dir, "static"),
            os.path.join(self.analytics_dir, "templates"),
            os.path.join(self.analytics_dir, "data")
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            filename=os.path.join(self.analytics_dir, 'dashboard.log'),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def get_project_health(self) -> Dict:
        """Calculate project health metrics"""
        try:
            metrics = {
                "ssot_completeness": self._calculate_ssot_completeness(),
                "rule_coverage": self._calculate_rule_coverage(),
                "mcp_health": self._check_mcp_health(),
                "kg_health": self._check_kg_health()
            }
            
            # Calculate overall health score
            weights = {"ssot_completeness": 0.3, "rule_coverage": 0.3, 
                      "mcp_health": 0.2, "kg_health": 0.2}
            overall_score = sum(score * weights[metric] 
                              for metric, score in metrics.items())
            
            metrics["overall_health"] = round(overall_score, 2)
            return metrics
        except Exception as e:
            logger.error(f"Error calculating project health: {str(e)}")
            return {"error": str(e)}

    def _calculate_ssot_completeness(self) -> float:
        """Calculate SSOT system completeness score"""
        required_files = [".INIT", ".HISTORY", ".CONTINUE", ".CONTEXT", 
                         ".FACTS", ".MEMORY", ".PROGRESS"]
        existing_files = [f for f in required_files 
                         if os.path.exists(os.path.join(self.ssot_dir, f))]
        return len(existing_files) / len(required_files) * 100

    def _calculate_rule_coverage(self) -> float:
        """Calculate rule coverage score"""
        try:
            rules_dir = ".cursor/rules"
            if not os.path.exists(rules_dir):
                return 0
            
            rule_files = [f for f in os.listdir(rules_dir) if f.endswith('.mdc')]
            if not rule_files:
                return 0
            
            # Analyze rule coverage
            coverage_score = 0
            total_rules = len(rule_files)
            
            for rule_file in rule_files:
                with open(os.path.join(rules_dir, rule_file), 'r') as f:
                    content = f.read()
                    # Check for key components
                    has_description = '---' in content
                    has_globs = 'globs:' in content
                    has_content = len(content.split('---')[1].strip()) > 0
                    
                    # Calculate rule score
                    rule_score = (has_description + has_globs + has_content) / 3
                    coverage_score += rule_score
            
            return (coverage_score / total_rules) * 100
        except Exception as e:
            logger.error(f"Error calculating rule coverage: {str(e)}")
            return 0

    def _check_mcp_health(self) -> float:
        """Check MCP servers health"""
        try:
            mcp_dir = os.path.join(self.base_dir, "MCP")
            if not os.path.exists(mcp_dir):
                return 0
            
            # Check for key MCP components
            components = ["mcp.json", "package.json", "node_modules"]
            existing = sum(1 for c in components 
                         if os.path.exists(os.path.join(mcp_dir, c)))
            
            return (existing / len(components)) * 100
        except Exception as e:
            logger.error(f"Error checking MCP health: {str(e)}")
            return 0

    def _check_kg_health(self) -> float:
        """Check Knowledge Graph health"""
        try:
            # Read the graph
            graph = self._read_knowledge_graph()
            if not graph:
                return 0
            
            # Calculate health metrics
            metrics = {
                "has_entities": len(graph.get("entities", [])) > 0,
                "has_relations": len(graph.get("relations", [])) > 0,
                "has_observations": len(graph.get("observations", [])) > 0,
                "is_connected": self._check_graph_connectivity(graph)
            }
            
            return (sum(metrics.values()) / len(metrics)) * 100
        except Exception as e:
            logger.error(f"Error checking KG health: {str(e)}")
            return 0

    def _read_knowledge_graph(self) -> Optional[Dict]:
        """Read the Knowledge Graph data"""
        try:
            kg_file = os.path.join(self.analytics_dir, "data", "knowledge_graph.json")
            if not os.path.exists(kg_file):
                return None
            
            with open(kg_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading knowledge graph: {str(e)}")
            return None

    def _check_graph_connectivity(self, graph: Dict) -> bool:
        """Check if the Knowledge Graph is properly connected"""
        if not graph:
            return False
        
        entities = graph.get("entities", [])
        relations = graph.get("relations", [])
        
        if not entities or not relations:
            return False
        
        # Check if relations connect existing entities
        entity_ids = {e["id"] for e in entities}
        for relation in relations:
            if relation["from"] not in entity_ids or relation["to"] not in entity_ids:
                return False
        
        return True

    def get_rule_engine_status(self) -> Dict:
        """Get rule engine status and available triggers"""
        try:
            return {
                "available_triggers": rule_engine.list_available_triggers(),
                "template_count": self._count_rule_templates(),
                "active_rules": self._count_active_rules(),
                "staged_rules": self._count_staged_rules()
            }
        except Exception as e:
            logger.error(f"Error getting rule engine status: {str(e)}")
            return {"error": str(e)}

    def _count_rule_templates(self) -> int:
        """Count available rule templates"""
        try:
            templates_dir = os.path.join(self.rule_engine_dir, "rule_templates")
            if not os.path.exists(templates_dir):
                return 0
            return len([f for f in os.listdir(templates_dir) if f.endswith('.json')])
        except Exception:
            return 0

    def _count_active_rules(self) -> int:
        """Count active rules in the project"""
        try:
            rules_dir = ".cursor/rules"
            if not os.path.exists(rules_dir):
                return 0
            return len([f for f in os.listdir(rules_dir) if f.endswith('.mdc')])
        except Exception:
            return 0

    def _count_staged_rules(self) -> int:
        """Count rules in staging"""
        try:
            staging_dir = os.path.join(self.rule_engine_dir, "staging")
            if not os.path.exists(staging_dir):
                return 0
            
            count = 0
            for root, _, files in os.walk(staging_dir):
                count += len([f for f in files if f.endswith('.mdc')])
            return count
        except Exception:
            return 0

# Initialize dashboard manager
dashboard = DashboardManager()

@app.route('/')
def index():
    """Render dashboard homepage"""
    return render_template('index.html')

@app.route('/api/health')
def health():
    """Get project health metrics"""
    return jsonify(dashboard.get_project_health())

@app.route('/api/rule-engine/status')
def rule_engine_status():
    """Get rule engine status"""
    return jsonify(dashboard.get_rule_engine_status())

@app.route('/api/rule-engine/trigger', methods=['POST'])
def trigger_rule_engine():
    """Handle rule engine trigger"""
    try:
        data = request.json
        trigger = data.get('trigger')
        context = data.get('context', {})
        
        if not trigger:
            return jsonify({"error": "No trigger specified"}), 400
        
        result = rule_engine.handle_trigger(trigger, context)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files"""
    return send_from_directory(app.static_folder, path)

def create_dashboard_files():
    """Create necessary dashboard template and static files"""
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(app.template_folder)
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create index.html template
    index_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SSOT Rule Engine Dashboard</title>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <div class="dashboard">
            <header>
                <h1>SSOT Rule Engine Dashboard</h1>
            </header>
            
            <main>
                <section class="health-metrics">
                    <h2>Project Health</h2>
                    <div id="health-scores"></div>
                </section>
                
                <section class="rule-engine">
                    <h2>Rule Engine</h2>
                    <div class="triggers">
                        <h3>Available Triggers</h3>
                        <div id="trigger-list"></div>
                    </div>
                    <div class="rule-stats">
                        <h3>Rule Statistics</h3>
                        <div id="rule-stats"></div>
                    </div>
                </section>
            </main>
        </div>
        <script src="/static/js/dashboard.js"></script>
    </body>
    </html>
    """
    
    with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
        f.write(index_html)
    
    # Create static directory if it doesn't exist
    static_dir = os.path.join(app.static_folder, 'css')
    os.makedirs(static_dir, exist_ok=True)
    
    # Create CSS file
    css = """
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
            Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
        line-height: 1.6;
        color: #333;
        background-color: #f5f5f5;
    }

    .dashboard {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    header {
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #eee;
    }

    h1 {
        color: #2c3e50;
    }

    section {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }

    h2 {
        color: #2c3e50;
        margin-bottom: 1rem;
    }

    h3 {
        color: #34495e;
        margin: 1rem 0;
    }

    .health-metrics {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }

    .metric-card {
        padding: 1rem;
        border: 1px solid #eee;
        border-radius: 4px;
        text-align: center;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3498db;
    }

    .rule-engine {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 2rem;
    }

    .trigger-item {
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }

    .rule-stat {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem;
        border-bottom: 1px solid #eee;
    }

    @media (max-width: 768px) {
        .rule-engine {
            grid-template-columns: 1fr;
        }
    }
    """
    
    with open(os.path.join(static_dir, 'style.css'), 'w') as f:
        f.write(css)
    
    # Create js directory and dashboard.js
    js_dir = os.path.join(app.static_folder, 'js')
    os.makedirs(js_dir, exist_ok=True)
    
    js = """
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
                card.innerHTML = `
                    <h4>${metric.replace(/_/g, ' ').toUpperCase()}</h4>
                    <div class="metric-value">${value.toFixed(1)}%</div>
                `;
                healthScores.appendChild(card);
            }
        } catch (error) {
            console.error('Error fetching health metrics:', error);
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
                    <h4>${trigger}</h4>
                    <p>${description}</p>
                `;
                triggerList.appendChild(triggerItem);
            }
            
            // Display rule statistics
            const ruleStats = document.getElementById('rule-stats');
            ruleStats.innerHTML = `
                <div class="rule-stat">
                    <span>Template Count:</span>
                    <span>${data.template_count}</span>
                </div>
                <div class="rule-stat">
                    <span>Active Rules:</span>
                    <span>${data.active_rules}</span>
                </div>
                <div class="rule-stat">
                    <span>Staged Rules:</span>
                    <span>${data.staged_rules}</span>
                </div>
            `;
        } catch (error) {
            console.error('Error fetching rule engine status:', error);
        }
    }

    // Update dashboard data periodically
    function initDashboard() {
        updateHealthMetrics();
        updateRuleEngine();
        
        // Refresh every 30 seconds
        setInterval(() => {
            updateHealthMetrics();
            updateRuleEngine();
        }, 30000);
    }

    // Initialize dashboard when page loads
    document.addEventListener('DOMContentLoaded', initDashboard);
    """
    
    with open(os.path.join(js_dir, 'dashboard.js'), 'w') as f:
        f.write(js)

def main():
    """Main function to launch the dashboard"""
    try:
        # Create dashboard files
        create_dashboard_files()
        
        # Get port from environment or use default
        port = int(os.environ.get('PORT', 5000))
        
        # Open dashboard in browser
        webbrowser.open(f'http://localhost:{port}')
        
        # Start the Flask app
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(f"Error launching dashboard: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 