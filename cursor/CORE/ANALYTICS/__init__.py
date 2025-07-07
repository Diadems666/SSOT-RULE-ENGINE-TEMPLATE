"""
SSOT Rule Engine Analytics Package
Provides analytics dashboard and AI integration for the SSOT Rule Engine
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(os.path.dirname(__file__), 'dashboard.log')
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__,
        static_folder='static',
        template_folder='templates')
    CORS(app)
    
    # Configure error handling
    @app.errorhandler(Exception)
    def handle_error(error):
        """Convert all errors to JSON responses"""
        code = 500
        if isinstance(error, HTTPException):
            code = error.code
        
        response = jsonify({
            'success': False,
            'error': str(error),
            'status_code': code
        })
        response.status_code = code
        return response
    
    # Import and register blueprints
    try:
        from .routes.ai_routes import ai_bp
        app.register_blueprint(ai_bp, url_prefix='/api/ai')
        logger.info("AI routes registered successfully")
    except Exception as e:
        logger.error(f"Failed to register AI routes: {str(e)}")
        
    # Initialize services
    try:
        from .services.ai_service import AIService
        from .mcp.kg_client import KGClient
        
        app.ai_service = AIService()
        app.kg_client = KGClient()
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
    
    # Register health check route
    @app.route('/api/health')
    def health_check():
        """Check system health"""
        try:
            ai_status = app.ai_service.get_status() if hasattr(app, 'ai_service') else {'status': 'not_initialized'}
            kg_status = app.kg_client.get_status() if hasattr(app, 'kg_client') else {'status': 'not_initialized'}
            
            return jsonify({
                'success': True,
                'ai_service': ai_status,
                'kg_service': kg_status,
                'api_version': '1.0.0'
            })
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    logger.info("Application created successfully")
    return app 

__version__ = '1.0.0' 