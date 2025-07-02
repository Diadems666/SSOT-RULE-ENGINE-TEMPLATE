#!/usr/bin/env python3
"""
Enhanced SSOT-RULE-ENGINE Analytics Dashboard
Provides real-time analytics, Rule Engine management, and USER-RULES access
"""

import http.server
import socketserver
import json
import os
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import subprocess

# Import analytics engine
sys.path.append(str(Path(__file__).parent))
from analytics_engine import AnalyticsEngine

class EnhancedDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.analytics_engine = AnalyticsEngine()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_dashboard()
        elif parsed_path.path == '/api/analytics':
            self.serve_analytics_data()
        elif parsed_path.path == '/api/rules':
            self.serve_rules_data()
        elif parsed_path.path == '/api/user-rules':
            self.serve_user_rules()
        elif parsed_path.path == '/api/ssot':
            self.serve_ssot_data()
        else:
            super().do_GET()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/rules/save':
            self.save_rule()
        elif parsed_path.path == '/api/rules/delete':
            self.delete_rule()
        elif parsed_path.path == '/api/launch-analytics':
            self.launch_analytics()
        else:
            self.send_error(404)

    def serve_dashboard(self):
        """Serve the enhanced dashboard HTML"""
        html_content = self.generate_dashboard_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())

    def serve_analytics_data(self):
        """Serve analytics data as JSON"""
        try:
            # Run analytics and get results
            results = self.analytics_engine.run_comprehensive_analysis()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(results, indent=2).encode())
        except Exception as e:
            self.send_error(500, f"Analytics error: {str(e)}")

    def serve_rules_data(self):
        """Serve rule engine data"""
        try:
            rules_data = self.get_rules_data()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(rules_data, indent=2).encode())
        except Exception as e:
            self.send_error(500, f"Rules error: {str(e)}")

    def serve_user_rules(self):
        """Serve USER-RULES content for easy copying"""
        try:
            user_rules_content = self.get_user_rules_content()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps({
                'content': user_rules_content,
                'filename': 'USER-RULES.md'
            }, indent=2).encode())
        except Exception as e:
            self.send_error(500, f"USER-RULES error: {str(e)}")

    def serve_ssot_data(self):
        """Serve SSOT system data"""
        try:
            ssot_data = self.get_ssot_data()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(ssot_data, indent=2).encode())
        except Exception as e:
            self.send_error(500, f"SSOT error: {str(e)}")

    def get_rules_data(self):
        """Get comprehensive rule engine data"""
        rules_data = {
            'active_rules': [],
            'staged_rules': [],
            'rule_stats': {},
            'effectiveness_metrics': {}
        }
        
        # Get active rules from .cursor/rules/
        rules_dir = Path('.cursor/rules')
        if rules_dir.exists():
            for rule_file in rules_dir.glob('*.md'):
                try:
                    with open(rule_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        rules_data['active_rules'].append({
                            'filename': rule_file.name,
                            'path': str(rule_file),
                            'content': content,
                            'size': len(content),
                            'modified': rule_file.stat().st_mtime
                        })
                except Exception as e:
                    print(f"Error reading rule file {rule_file}: {e}")
        
        # Get staged rules from .cursor/CORE/RULE-ENGINE/
        staged_dir = Path('.cursor/CORE/RULE-ENGINE')
        if staged_dir.exists():
            for rule_file in staged_dir.glob('*.mdc'):
                try:
                    with open(rule_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        rules_data['staged_rules'].append({
                            'filename': rule_file.name,
                            'path': str(rule_file),
                            'content': content,
                            'size': len(content),
                            'modified': rule_file.stat().st_mtime
                        })
                except Exception as e:
                    print(f"Error reading staged rule file {rule_file}: {e}")
        
        # Calculate stats
        rules_data['rule_stats'] = {
            'total_active': len(rules_data['active_rules']),
            'total_staged': len(rules_data['staged_rules']),
            'total_size': sum(rule['size'] for rule in rules_data['active_rules'] + rules_data['staged_rules'])
        }
        
        return rules_data

    def get_user_rules_content(self):
        """Get the USER-RULES content for easy copying"""
        user_rules_template = """# Core AI Behavior & Workflow Management
- As an AI assistant within the Cursor AI IDE for default_developer, provide efficient, accurate, and contextually relevant assistance, leveraging all available tools including the Knowledge Graph Memory Server.
- Recognize and strictly follow directives within the project's core system files (e.g., in ./.cursor/CORE/SSOT/).
- Understand that specific triggers initiate system setup workflows, and the *detailed instructions* for ALL setup workflows ('INIT', 'ADD', 'INSTALL MCP', 'BUILD KG') are centralized in ./.cursor/CORE/SSOT/.ENGINE.
- When encountering ANY of the following triggers ('!!-INIT-.ENGINE-!!', '!!-ADD-.ENGINE-!!', '!!-INSTALL-MCP-!!', '!!-BUILD-KG-!!'), immediately consult and execute the relevant steps defined within ./.cursor/CORE/SSOT/.ENGINE for the specific trigger identified.

# Rule Integration & Precedence
- Always apply the alwaysApply: true .mdc rules (such as 001-bottle-shop-rules and 001-ssot-synchronization) to all interactions.
- When specific files are in context, apply corresponding glob-matched .mdc rules.
- When rules conflict, prioritize in order: required_instructions > available_instructions > general User Rules.

# Project Identification & Context Management
- You are interacting with default_developer.
- Maintain a dynamic understanding of the current project and its root directory. Utilize the Filesystem MCP server for project traversal and analysis.
- Track and maintain a "project context buffer" consisting of the last 5-10 files the user has edited or viewed.
- If the current project appears unknown or its structure has significantly changed since the last interaction, initiate the "Project Discovery and Knowledge Graph Update" process using the steps defined within ./.cursor/CORE/SSOT/.ENGINE (specifically the logic associated with the 'ADD' workflow analysis and 'BUILD KG' steps, adapted for ongoing use).
- Begin each interaction by stating "Analyzing Project Context..." and proactively retrieving relevant information from the project context buffer, recent interactions, SSOT files, and the Knowledge Graph.

# Analytics System Integration
- When projects are first initialized (!!-INIT-.ENGINE-!! or !!-ADD-.ENGINE-!!), automatically launch the analytics dashboard
- Use !!-ANALYZE-PROJECT-!! for comprehensive project analysis and health scoring
- Use !!-VIEW-DASHBOARD-!! to launch the interactive analytics dashboard
- Use !!-HEALTH-CHECK-!! for quick project health assessment
- Monitor project health metrics and provide intelligent recommendations for optimization

# Advanced Analytics Features
- Real-time project health monitoring with 0-100 scoring system
- Interactive dashboard with visual charts and system status indicators
- Intelligent recommendations engine for development optimization
- Rule engine effectiveness tracking and visual management interface
- SSOT system analytics and completeness monitoring
- MCP server performance metrics and usage analytics

# Visual Rule Engine Management
- Use the dashboard's Rule Engine interface for visual rule management
- View, edit, create, and delete rules through the web interface
- Monitor rule effectiveness and usage patterns
- Stage new rules in .cursor/CORE/RULE-ENGINE/ before activation
- Track rule impact on project development and code quality

# USER-RULES Template Access
- Access complete USER-RULES template through analytics dashboard
- Easy copy/paste functionality for setting up new projects
- Version-controlled rule templates with best practices
- Integration guides for existing projects"""
        
        return user_rules_template

    def get_ssot_data(self):
        """Get SSOT system data"""
        ssot_data = {
            'files': {},
            'system_status': {},
            'recent_activity': []
        }
        
        ssot_dir = Path('.cursor/CORE/SSOT')
        if ssot_dir.exists():
            ssot_files = ['.INIT', '.CONTEXT', '.FACTS', '.MEMORY', '.HISTORY', '.CONTINUE', '.PROGRESS', '.ENGINE']
            
            for filename in ssot_files:
                file_path = ssot_dir / filename
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            ssot_data['files'][filename] = {
                                'content': content,
                                'size': len(content),
                                'modified': file_path.stat().st_mtime,
                                'exists': True
                            }
                    except Exception as e:
                        ssot_data['files'][filename] = {
                            'error': str(e),
                            'exists': False
                        }
                else:
                    ssot_data['files'][filename] = {'exists': False}
        
        # System status
        ssot_data['system_status'] = {
            'ssot_completeness': len([f for f in ssot_data['files'].values() if f.get('exists', False)]) / 8 * 100,
            'mcp_configured': Path('.cursor/mcp.json').exists(),
            'analytics_active': True
        }
        
        return ssot_data

    def launch_analytics(self):
        """Launch analytics engine"""
        try:
            # Run analytics
            subprocess.run([sys.executable, str(Path(__file__).parent / 'analytics_engine.py')], 
                         cwd=Path.cwd(), check=True)
            
            response = {'status': 'success', 'message': 'Analytics launched successfully'}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error(500, f"Failed to launch analytics: {str(e)}")

    def generate_dashboard_html(self):
        """Generate the enhanced dashboard HTML with Rule Engine management"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SSOT-RULE-ENGINE Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .header p {
            color: #7f8c8d;
            font-size: 1.1rem;
        }
        
        .nav-tabs {
            display: flex;
            background: rgba(255, 255, 255, 0.9);
            border-bottom: 1px solid #ddd;
            margin-top: 1rem;
        }
        
        .nav-tab {
            padding: 1rem 2rem;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        
        .nav-tab:hover {
            background: rgba(52, 152, 219, 0.1);
        }
        
        .nav-tab.active {
            border-bottom-color: #3498db;
            background: rgba(52, 152, 219, 0.1);
            color: #2980b9;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        }
        
        .card h3 {
            color: #2c3e50;
            margin-bottom: 1rem;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .health-score {
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            margin: 1rem 0;
        }
        
        .health-excellent { color: #27ae60; }
        .health-good { color: #f39c12; }
        .health-fair { color: #e67e22; }
        .health-poor { color: #e74c3c; }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 0.5rem;
        }
        
        .status-online { background: #27ae60; }
        .status-warning { background: #f39c12; }
        .status-offline { background: #e74c3c; }
        
        .metric-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 0;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .metric-item:last-child {
            border-bottom: none;
        }
        
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
            text-decoration: none;
            margin: 0.25rem;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #27ae60, #229954);
        }
        
        .chart-container {
            position: relative;
            height: 300px;
            margin: 1rem 0;
        }
        
        .rule-editor {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .rule-header {
            background: #e9ecef;
            padding: 1rem;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .rule-content {
            padding: 1rem;
        }
        
        textarea {
            width: 100%;
            min-height: 200px;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 1rem;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.9rem;
            resize: vertical;
        }
        
        .user-rules-container {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 2rem;
            margin: 1rem 0;
        }
        
        .copy-btn {
            position: absolute;
            top: 1rem;
            right: 1rem;
            padding: 0.5rem 1rem;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        
        pre {
            background: #2d3748;
            color: #e2e8f0;
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            position: relative;
            margin: 1rem 0;
        }
        
        .refresh-indicator {
            display: inline-block;
            margin-left: 1rem;
            color: #7f8c8d;
            font-size: 0.9rem;
        }
        
        .loading {
            text-align: center;
            padding: 2rem;
            color: #7f8c8d;
        }
        
        .error {
            background: #ffe6e6;
            color: #d63031;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .loading {
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 SSOT-RULE-ENGINE Analytics Dashboard</h1>
        <p>Real-time project health monitoring, rule management, and intelligent insights</p>
        
        <div class="nav-tabs">
            <div class="nav-tab active" onclick="showTab('analytics')">📊 Analytics</div>
            <div class="nav-tab" onclick="showTab('rules')">⚙️ Rule Engine</div>
            <div class="nav-tab" onclick="showTab('user-rules')">📋 USER-RULES</div>
            <div class="nav-tab" onclick="showTab('ssot')">🗂️ SSOT System</div>
        </div>
    </div>

    <div class="container">
        <!-- Analytics Tab -->
        <div id="analytics" class="tab-content active">
            <div class="dashboard-grid">
                <div class="card">
                    <h3>🎯 Project Health Score</h3>
                    <div id="health-score" class="health-score">--</div>
                    <div id="health-breakdown"></div>
                </div>
                
                <div class="card">
                    <h3>📈 System Status</h3>
                    <div id="system-status"></div>
                </div>
                
                <div class="card">
                    <h3>💡 Recommendations</h3>
                    <div id="recommendations"></div>
                </div>
            </div>
            
            <div class="dashboard-grid">
                <div class="card">
                    <h3>📊 Health Distribution</h3>
                    <div class="chart-container">
                        <canvas id="healthChart"></canvas>
                    </div>
                </div>
                
                <div class="card">
                    <h3>📋 Project Overview</h3>
                    <div class="chart-container">
                        <canvas id="overviewChart"></canvas>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <button class="btn" onclick="refreshAnalytics()">🔄 Refresh Analytics</button>
                <button class="btn btn-success" onclick="launchAnalytics()">🚀 Run Full Analysis</button>
                <span id="last-refresh" class="refresh-indicator"></span>
            </div>
        </div>

        <!-- Rules Tab -->
        <div id="rules" class="tab-content">
            <div class="card">
                <h3>⚙️ Rule Engine Management</h3>
                <div id="rules-stats"></div>
                <button class="btn" onclick="refreshRules()">🔄 Refresh Rules</button>
                <button class="btn btn-success" onclick="createNewRule()">➕ Create New Rule</button>
            </div>
            
            <div id="active-rules">
                <h3>📋 Active Rules (.cursor/rules/)</h3>
                <div id="active-rules-list"></div>
            </div>
            
            <div id="staged-rules">
                <h3>🔄 Staged Rules (.cursor/CORE/RULE-ENGINE/)</h3>
                <div id="staged-rules-list"></div>
            </div>
        </div>

        <!-- USER-RULES Tab -->
        <div id="user-rules" class="tab-content">
            <div class="card">
                <h3>📋 USER-RULES Template</h3>
                <p>Copy and paste this template into your Cursor AI settings for optimal SSOT-RULE-ENGINE integration:</p>
                
                <div class="user-rules-container">
                    <button class="copy-btn" onclick="copyUserRules()">📋 Copy to Clipboard</button>
                    <pre id="user-rules-content">Loading...</pre>
                </div>
                
                <div style="margin-top: 1rem;">
                    <h4>📖 Setup Instructions:</h4>
                    <ol style="padding-left: 2rem; margin-top: 0.5rem;">
                        <li>Copy the template above using the "Copy to Clipboard" button</li>
                        <li>Open Cursor AI settings (Cmd/Ctrl + ,)</li>
                        <li>Navigate to "Rules for AI" or "USER-RULES" section</li>
                        <li>Paste the template into your rules configuration</li>
                        <li>Save and restart Cursor AI for changes to take effect</li>
                    </ol>
                </div>
            </div>
        </div>

        <!-- SSOT Tab -->
        <div id="ssot" class="tab-content">
            <div class="card">
                <h3>🗂️ SSOT System Overview</h3>
                <div id="ssot-status"></div>
                <button class="btn" onclick="refreshSSOT()">🔄 Refresh SSOT</button>
            </div>
            
            <div id="ssot-files">
                <h3>📁 SSOT Files</h3>
                <div id="ssot-files-list"></div>
            </div>
        </div>
    </div>

    <script>
        let analyticsData = null;
        let rulesData = null;
        let ssotData = null;
        let healthChart = null;
        let overviewChart = null;

        // Tab Management
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            // Load tab-specific data
            if (tabName === 'analytics') {
                loadAnalytics();
            } else if (tabName === 'rules') {
                loadRules();
            } else if (tabName === 'user-rules') {
                loadUserRules();
            } else if (tabName === 'ssot') {
                loadSSOT();
            }
        }

        // Analytics Functions
        async function loadAnalytics() {
            try {
                const response = await fetch('/api/analytics');
                analyticsData = await response.json();
                updateAnalyticsDisplay();
            } catch (error) {
                console.error('Error loading analytics:', error);
                document.getElementById('health-score').innerHTML = '<div class="error">Error loading analytics data</div>';
            }
        }

        function updateAnalyticsDisplay() {
            if (!analyticsData) return;

            // Health Score
            const healthScore = analyticsData.project_health_score || 0;
            const healthElement = document.getElementById('health-score');
            healthElement.textContent = healthScore.toFixed(1);
            
            // Color coding
            if (healthScore >= 80) healthElement.className = 'health-score health-excellent';
            else if (healthScore >= 60) healthElement.className = 'health-score health-good';
            else if (healthScore >= 40) healthElement.className = 'health-score health-fair';
            else healthElement.className = 'health-score health-poor';

            // Health Breakdown
            const breakdown = analyticsData.health_breakdown || {};
            const breakdownHtml = Object.entries(breakdown).map(([key, value]) => 
                `<div class="metric-item">
                    <span>${key.replace('_', ' ').toUpperCase()}</span>
                    <span>${value.toFixed(1)}%</span>
                </div>`
            ).join('');
            document.getElementById('health-breakdown').innerHTML = breakdownHtml;

            // System Status
            const statusHtml = `
                <div class="metric-item">
                    <span><span class="status-indicator status-online"></span>Analytics Engine</span>
                    <span>Online</span>
                </div>
                <div class="metric-item">
                    <span><span class="status-indicator ${analyticsData.mcp_configured ? 'status-online' : 'status-offline'}"></span>MCP Servers</span>
                    <span>${analyticsData.mcp_configured ? 'Configured' : 'Not Configured'}</span>
                </div>
                <div class="metric-item">
                    <span><span class="status-indicator status-online"></span>Rule Engine</span>
                    <span>Active</span>
                </div>
            `;
            document.getElementById('system-status').innerHTML = statusHtml;

            // Recommendations
            const recommendations = analyticsData.recommendations || [];
            const recommendationsHtml = recommendations.slice(0, 5).map(rec => 
                `<div class="metric-item">
                    <span>${rec.category}</span>
                    <span style="font-size: 0.9em; color: #7f8c8d;">${rec.description}</span>
                </div>`
            ).join('');
            document.getElementById('recommendations').innerHTML = recommendationsHtml || '<p>No recommendations at this time.</p>';

            // Update charts
            updateCharts();
            
            // Update timestamp
            document.getElementById('last-refresh').textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
        }

        function updateCharts() {
            if (!analyticsData) return;

            // Health Distribution Chart
            const healthCtx = document.getElementById('healthChart').getContext('2d');
            if (healthChart) healthChart.destroy();
            
            const breakdown = analyticsData.health_breakdown || {};
            healthChart = new Chart(healthCtx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(breakdown).map(k => k.replace('_', ' ').toUpperCase()),
                    datasets: [{
                        data: Object.values(breakdown),
                        backgroundColor: ['#3498db', '#2ecc71', '#f39c12', '#e74c3c'],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });

            // Overview Chart
            const overviewCtx = document.getElementById('overviewChart').getContext('2d');
            if (overviewChart) overviewChart.destroy();
            
            const metrics = analyticsData.project_metrics || {};
            overviewChart = new Chart(overviewCtx, {
                type: 'bar',
                data: {
                    labels: ['Files', 'Rules', 'SSOT Files', 'MCP Servers'],
                    datasets: [{
                        label: 'Count',
                        data: [
                            metrics.total_files || 0,
                            metrics.total_rules || 0,
                            metrics.ssot_files || 0,
                            metrics.mcp_servers || 0
                        ],
                        backgroundColor: '#3498db',
                        borderColor: '#2980b9',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        // Rules Functions
        async function loadRules() {
            try {
                const response = await fetch('/api/rules');
                rulesData = await response.json();
                updateRulesDisplay();
            } catch (error) {
                console.error('Error loading rules:', error);
            }
        }

        function updateRulesDisplay() {
            if (!rulesData) return;

            // Rules Stats
            const stats = rulesData.rule_stats || {};
            const statsHtml = `
                <div class="metric-item">
                    <span>Active Rules</span>
                    <span>${stats.total_active || 0}</span>
                </div>
                <div class="metric-item">
                    <span>Staged Rules</span>
                    <span>${stats.total_staged || 0}</span>
                </div>
                <div class="metric-item">
                    <span>Total Size</span>
                    <span>${(stats.total_size || 0)} bytes</span>
                </div>
            `;
            document.getElementById('rules-stats').innerHTML = statsHtml;

            // Active Rules
            const activeRulesHtml = rulesData.active_rules.map(rule => `
                <div class="rule-editor">
                    <div class="rule-header">
                        <strong>${rule.filename}</strong>
                        <div>
                            <button class="btn" onclick="editRule('${rule.path}')">✏️ Edit</button>
                            <button class="btn btn-danger" onclick="deleteRule('${rule.path}')">🗑️ Delete</button>
                        </div>
                    </div>
                    <div class="rule-content">
                        <pre style="white-space: pre-wrap; margin: 0;">${rule.content.substring(0, 200)}${rule.content.length > 200 ? '...' : ''}</pre>
                    </div>
                </div>
            `).join('');
            document.getElementById('active-rules-list').innerHTML = activeRulesHtml || '<p>No active rules found.</p>';

            // Staged Rules
            const stagedRulesHtml = rulesData.staged_rules.map(rule => `
                <div class="rule-editor">
                    <div class="rule-header">
                        <strong>${rule.filename}</strong>
                        <div>
                            <button class="btn btn-success" onclick="activateRule('${rule.path}')">✅ Activate</button>
                            <button class="btn" onclick="editRule('${rule.path}')">✏️ Edit</button>
                            <button class="btn btn-danger" onclick="deleteRule('${rule.path}')">🗑️ Delete</button>
                        </div>
                    </div>
                    <div class="rule-content">
                        <pre style="white-space: pre-wrap; margin: 0;">${rule.content.substring(0, 200)}${rule.content.length > 200 ? '...' : ''}</pre>
                    </div>
                </div>
            `).join('');
            document.getElementById('staged-rules-list').innerHTML = stagedRulesHtml || '<p>No staged rules found.</p>';
        }

        // USER-RULES Functions
        async function loadUserRules() {
            try {
                const response = await fetch('/api/user-rules');
                const data = await response.json();
                document.getElementById('user-rules-content').textContent = data.content;
            } catch (error) {
                console.error('Error loading USER-RULES:', error);
                document.getElementById('user-rules-content').textContent = 'Error loading USER-RULES template';
            }
        }

        function copyUserRules() {
            const content = document.getElementById('user-rules-content').textContent;
            navigator.clipboard.writeText(content).then(() => {
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✅ Copied!';
                setTimeout(() => {
                    btn.textContent = originalText;
                }, 2000);
            });
        }

        // SSOT Functions
        async function loadSSOT() {
            try {
                const response = await fetch('/api/ssot');
                ssotData = await response.json();
                updateSSOTDisplay();
            } catch (error) {
                console.error('Error loading SSOT:', error);
            }
        }

        function updateSSOTDisplay() {
            if (!ssotData) return;

            // SSOT Status
            const status = ssotData.system_status || {};
            const statusHtml = `
                <div class="metric-item">
                    <span>SSOT Completeness</span>
                    <span>${status.ssot_completeness?.toFixed(1) || 0}%</span>
                </div>
                <div class="metric-item">
                    <span>MCP Configured</span>
                    <span>${status.mcp_configured ? 'Yes' : 'No'}</span>
                </div>
                <div class="metric-item">
                    <span>Analytics Active</span>
                    <span>${status.analytics_active ? 'Yes' : 'No'}</span>
                </div>
            `;
            document.getElementById('ssot-status').innerHTML = statusHtml;

            // SSOT Files
            const files = ssotData.files || {};
            const filesHtml = Object.entries(files).map(([filename, data]) => `
                <div class="card" style="margin: 1rem 0;">
                    <h4>${filename}</h4>
                    ${data.exists ? `
                        <div class="metric-item">
                            <span>Size</span>
                            <span>${data.size} bytes</span>
                        </div>
                        <div class="metric-item">
                            <span>Modified</span>
                            <span>${new Date(data.modified * 1000).toLocaleString()}</span>
                        </div>
                        <details style="margin-top: 1rem;">
                            <summary>View Content</summary>
                            <pre style="margin-top: 0.5rem; max-height: 200px; overflow-y: auto;">${data.content}</pre>
                        </details>
                    ` : `
                        <p style="color: #e74c3c; font-style: italic;">File does not exist</p>
                    `}
                </div>
            `).join('');
            document.getElementById('ssot-files-list').innerHTML = filesHtml;
        }

        // Utility Functions
        async function refreshAnalytics() {
            document.getElementById('health-score').innerHTML = '<div class="loading">Loading...</div>';
            await loadAnalytics();
        }

        async function refreshRules() {
            await loadRules();
        }

        async function refreshSSOT() {
            await loadSSOT();
        }

        async function launchAnalytics() {
            try {
                const response = await fetch('/api/launch-analytics', { method: 'POST' });
                const result = await response.json();
                if (result.status === 'success') {
                    setTimeout(() => refreshAnalytics(), 2000);
                }
            } catch (error) {
                console.error('Error launching analytics:', error);
            }
        }

        function createNewRule() {
            const ruleName = prompt('Enter rule name (without .mdc extension):');
            if (ruleName) {
                // TODO: Implement rule creation
                alert('Rule creation functionality will be implemented in a future update.');
            }
        }

        function editRule(rulePath) {
            // TODO: Implement rule editing
            alert('Rule editing functionality will be implemented in a future update.');
        }

        function deleteRule(rulePath) {
            if (confirm('Are you sure you want to delete this rule?')) {
                // TODO: Implement rule deletion
                alert('Rule deletion functionality will be implemented in a future update.');
            }
        }

        function activateRule(rulePath) {
            if (confirm('Are you sure you want to activate this rule?')) {
                // TODO: Implement rule activation
                alert('Rule activation functionality will be implemented in a future update.');
            }
        }

        // Auto-refresh every 30 seconds
        setInterval(() => {
            if (document.getElementById('analytics').classList.contains('active')) {
                loadAnalytics();
            }
        }, 30000);

        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', () => {
            loadAnalytics();
        });
    </script>
</body>
</html>"""

def start_dashboard(port=8080):
    """Start the enhanced dashboard server"""
    try:
        os.chdir(Path(__file__).parent)
        
        with socketserver.TCPServer(("", port), EnhancedDashboardHandler) as httpd:
            print(f"\n🚀 Enhanced SSOT-RULE-ENGINE Analytics Dashboard")
            print(f"📊 Dashboard URL: http://localhost:{port}")
            print(f"⚙️ Features: Analytics | Rule Engine | USER-RULES | SSOT Management")
            print(f"🔄 Auto-refresh: Every 30 seconds")
            print(f"⭐ Press Ctrl+C to stop the server\n")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print(f"\n👋 Dashboard server stopped")
                
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    start_dashboard(port) 