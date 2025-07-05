"""
SSOT Rule Engine Analytics Package
"""

from flask import Flask
from flask_cors import CORS

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__,
        static_folder='static',
        template_folder='templates')
    CORS(app)
    
    # Import and register blueprints
    from .routes.ai_routes import ai_bp
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    
    return app 