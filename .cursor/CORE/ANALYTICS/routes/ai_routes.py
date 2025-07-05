"""
Flask routes for AI integration with the SSOT Rule Engine dashboard.
"""

from flask import Blueprint, jsonify, request
from ..services.ai_service import AIService
import asyncio
import logging

# Initialize logging
logger = logging.getLogger(__name__)

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')
ai_service = AIService()

@ai_bp.route('/generate-rule', methods=['POST'])
async def generate_rule():
    """Generate a new rule using AI."""
    try:
        context = request.json
        rule_config = await ai_service.generate_rule(context)
        return jsonify({
            "success": True,
            "rule": rule_config.__dict__
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@ai_bp.route('/generate-docs', methods=['POST'])
async def generate_docs():
    """Generate documentation for a rule."""
    try:
        rule_config = request.json
        docs = await ai_service.generate_documentation(rule_config)
        return jsonify({
            "success": True,
            "documentation": docs
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@ai_bp.route('/enhance-memory', methods=['POST'])
async def enhance_memory():
    """Enhance MCP memory with AI insights."""
    try:
        memory_entry = request.json
        enhanced = await ai_service.enhance_mcp_memory(memory_entry)
        return jsonify({
            "success": True,
            "enhanced_memory": enhanced
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@ai_bp.route('/analyze-codebase', methods=['POST'])
async def analyze_codebase():
    """Analyze codebase for rule suggestions."""
    try:
        paths = request.json.get('paths', [])
        analysis = await ai_service.analyze_codebase(paths)
        return jsonify({
            "success": True,
            "analysis": analysis
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@ai_bp.route('/query', methods=['POST'])
def query():
    """Handle AI queries"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "No query provided"}), 400

        response = ai_service.process_query(data['query'])
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error processing AI query: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/status', methods=['GET'])
def status():
    """Get AI system status"""
    try:
        status = ai_service.get_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error getting AI status: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback for AI responses"""
    try:
        data = request.get_json()
        if not data or 'feedback' not in data:
            return jsonify({'error': 'No feedback provided'}), 400

        feedback = data['feedback']
        query_id = data.get('query_id')
        
        result = ai_service.process_feedback(feedback, query_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/context', methods=['GET'])
def get_context():
    """Get current AI context"""
    try:
        context = ai_service.get_context()
        return jsonify(context)
    except Exception as e:
        logger.error(f"Error getting AI context: {str(e)}")
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/context', methods=['POST'])
def update_context():
    """Update AI context"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No context data provided"}), 400

        ai_service.update_context(data)
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error updating AI context: {str(e)}")
        return jsonify({"error": str(e)}), 500 