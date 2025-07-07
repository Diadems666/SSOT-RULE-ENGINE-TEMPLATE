#!/usr/bin/env python3
"""
SSOT Rule Engine Dashboard
Launches the analytics dashboard with AI and Knowledge Graph integration
"""

import os
import sys
import json
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import webbrowser
from quart import Quart, render_template, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException
from quart_cors import cors

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Import application components
from cursor.CORE.ANALYTICS.routes import ai_bp
from cursor.CORE.ANALYTICS.services import AIService
from cursor.CORE.ANALYTICS.mcp import KGClient

# Enable AI service
ai_enabled = True

# Create Quart application
app = Quart(__name__, 
            static_folder=os.path.join(project_root, 'cursor/CORE/ANALYTICS/static'),
            template_folder=os.path.join(project_root, 'cursor/CORE/ANALYTICS/templates'))

# Enable CORS
app = cors(app)

# Initialize services
app.ai_service = AIService()
app.kg_client = KGClient()

# Register blueprints
app.register_blueprint(ai_bp, url_prefix='/api/ai')

@app.route('/')
async def index():
    """Render dashboard"""
    return await render_template('dashboard.html')

class DashboardManager:
    def __init__(self):
        self.last_health_check = None
        self.health_score = 100
        self.rule_engine_status = "operational"
        
    async def get_health(self) -> Dict[str, Any]:
        """Get dashboard health status"""
        self.last_health_check = datetime.now()
        
        # Check various components
        components = {
            'rule_engine': await self._check_rule_engine(),
            'ai_service': await self._check_ai_service(),
            'kg_service': await self._check_kg_service()
        }
        
        # Calculate overall health
        self.health_score = sum(c['score'] for c in components.values()) / len(components)
        
        return {
            'score': self.health_score,
            'components': components,
            'timestamp': self.last_health_check.isoformat()
        }
    
    async def get_rule_engine_status(self) -> Dict[str, Any]:
        """Get rule engine status"""
        return {
            'status': self.rule_engine_status,
            'active_rules': await self._get_active_rules(),
            'last_update': datetime.now().isoformat()
        }
    
    async def _check_rule_engine(self) -> Dict[str, Any]:
        """Check rule engine health"""
        return {
            'status': 'operational',
            'score': 100,
            'message': 'Rule engine is functioning normally'
        }
    
    async def _check_ai_service(self) -> Dict[str, Any]:
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
    
    async def _check_kg_service(self) -> Dict[str, Any]:
        """Check Knowledge Graph service health"""
        if not app.kg_client:
            return {
                'status': 'disabled',
                'score': 0,
                'message': 'Knowledge Graph service is not enabled'
            }
        
        is_connected = await app.kg_client.is_connected()
        return {
            'status': 'operational' if is_connected else 'error',
            'score': 100 if is_connected else 0,
            'message': 'Knowledge Graph service is functioning normally' if is_connected else 'Failed to connect to Knowledge Graph'
        }
    
    async def _get_active_rules(self) -> List[Dict[str, Any]]:
        """Get list of active rules"""
        # TODO: Implement actual rule loading logic
        return [
            {'id': 'rule1', 'name': 'Default Rule', 'status': 'active'}
        ]

# Initialize dashboard manager
dashboard = DashboardManager()

@app.route('/api/health')
async def health():
    """Get dashboard health status"""
    return await jsonify(await dashboard.get_health())

@app.route('/api/rule-engine/status')
async def rule_engine_status():
    """Get rule engine status"""
    return await jsonify(await dashboard.get_rule_engine_status())

@app.route('/api/kg/visualize')
async def visualize_kg():
    """Get Knowledge Graph visualization data"""
    if not app.kg_client:
        return await jsonify({'error': 'Knowledge Graph service not available'}), 503
    data = await app.kg_client.get_visualization_data()
    return await jsonify(data)

async def main():
    """Main entry point"""
    try:
        # Run app
        await app.run_task(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
        
    except Exception as e:
        logger.error(f"Failed to launch dashboard: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main()) 