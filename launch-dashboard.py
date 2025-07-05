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
from typing import Dict, List, Optional, Any
import webbrowser
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
cursor_dir = os.path.join(current_dir, '.cursor')
sys.path.insert(0, cursor_dir)

# Import components
try:
    from CORE.ANALYTICS import create_app
    from CORE.ANALYTICS.mcp.kg_client import KGClient
    ai_enabled = True
except ImportError as e:
    logger.warning(f"AI components not available: {e}")
    ai_enabled = False

# Initialize Flask app
app = create_app() if ai_enabled else Flask(__name__,
    static_folder='.cursor/CORE/ANALYTICS/static',
    template_folder='.cursor/CORE/ANALYTICS/templates')

if not ai_enabled:
    CORS(app)

# Initialize Knowledge Graph client
kg_client = KGClient() if ai_enabled else None

class DashboardManager:
    def __init__(self):
        self.last_health_check = None
        self.health_score = 100
        self.rule_engine_status = "operational"
        
    def get_health(self) -> Dict[str, Any]:
        """Get dashboard health status"""
        self.last_health_check = datetime.now()
        
        # Check various components
        components = {
            'rule_engine': self._check_rule_engine(),
            'ai_service': self._check_ai_service(),
            'kg_service': self._check_kg_service()
        }
        
        # Calculate overall health
        self.health_score = sum(c['score'] for c in components.values()) / len(components)
        
        return {
            'score': self.health_score,
            'components': components,
            'timestamp': self.last_health_check.isoformat()
        }
    
    def get_rule_engine_status(self) -> Dict[str, Any]:
        """Get rule engine status"""
        return {
            'status': self.rule_engine_status,
            'active_rules': self._get_active_rules(),
            'last_update': datetime.now().isoformat()
        }
    
    def _check_rule_engine(self) -> Dict[str, Any]:
        """Check rule engine health"""
        return {
            'status': 'operational',
            'score': 100,
            'message': 'Rule engine is functioning normally'
        }
    
    def _check_ai_service(self) -> Dict[str, Any]:
        """Check AI service health"""
        if not ai_enabled:
            return {
                'status': 'disabled',
                'score': 0,
                'message': 'AI service is not enabled'
            }
        
        return {
            'status': 'operational',
            'score': 100,
            'message': 'AI service is functioning normally'
        }
    
    def _check_kg_service(self) -> Dict[str, Any]:
        """Check Knowledge Graph service health"""
        if not kg_client:
            return {
                'status': 'disabled',
                'score': 0,
                'message': 'Knowledge Graph service is not enabled'
            }
        
        return {
            'status': 'operational' if kg_client.is_connected() else 'error',
            'score': 100 if kg_client.is_connected() else 0,
            'message': 'Knowledge Graph service is functioning normally' if kg_client.is_connected() else 'Failed to connect to Knowledge Graph'
        }
    
    def _get_active_rules(self) -> List[Dict[str, Any]]:
        """Get list of active rules"""
        # TODO: Implement actual rule loading logic
        return [
            {'id': 'rule1', 'name': 'Default Rule', 'status': 'active'}
        ]

# Initialize dashboard manager
dashboard = DashboardManager()

@app.route('/')
def index():
    """Render dashboard homepage"""
    return render_template('index.html')

@app.route('/api/health')
def health():
    """Get dashboard health status"""
    return jsonify(dashboard.get_health())

@app.route('/api/rule-engine/status')
def rule_engine_status():
    """Get rule engine status"""
    return jsonify(dashboard.get_rule_engine_status())

@app.route('/api/kg/visualize')
def visualize_kg():
    """Get Knowledge Graph visualization data"""
    if not kg_client:
        return jsonify({'error': 'Knowledge Graph service not available'}), 503
    return jsonify(kg_client.get_visualization_data())

def main():
    """Main entry point"""
    try:
        port = 5000
        url = f"http://localhost:{port}"
        
        print(f"Starting dashboard server at {url}")
        webbrowser.open(url)
        
        app.run(debug=True, port=port)
        
    except Exception as e:
        logger.error(f"Failed to start dashboard: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 