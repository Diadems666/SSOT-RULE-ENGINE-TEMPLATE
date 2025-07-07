"""
Flask routes for AI integration with the SSOT Rule Engine dashboard.
Handles AI queries, rule generation, and knowledge graph integration.
"""

from quart import Blueprint, jsonify, request, current_app
from ..services.ai_service import AIService
from ..mcp.kg_client import KGClient
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')
ai_service = AIService()
kg_client = KGClient()

async def handle_error(e: Exception, status_code: int = 500) -> tuple:
    """Standardized error handling for routes"""
    error_id = datetime.now().strftime('%Y%m%d%H%M%S')
    logger.error(f"Error {error_id}: {str(e)}", exc_info=True)
    return await jsonify({
        "success": False,
        "error": str(e),
        "error_id": error_id
    }), status_code

@ai_bp.route('/generate-rule', methods=['POST'])
async def generate_rule():
    """Generate a new rule using AI."""
    try:
        context = await request.get_json()
        if not context:
            return await jsonify({"success": False, "error": "No context provided"}), 400

        rule_config = await ai_service.generate_rule(context)
        return await jsonify({
            "success": True,
            "rule": rule_config.__dict__,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return await handle_error(e)

@ai_bp.route('/generate-docs', methods=['POST'])
async def generate_docs():
    """Generate documentation for a rule."""
    try:
        rule_config = await request.get_json()
        if not rule_config:
            return await jsonify({"success": False, "error": "No rule configuration provided"}), 400

        docs = await ai_service.generate_documentation(rule_config)
        return await jsonify({
            "success": True,
            "documentation": docs,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return await handle_error(e)

@ai_bp.route('/enhance-memory', methods=['POST'])
async def enhance_memory():
    """Enhance MCP memory with AI insights."""
    try:
        memory_entry = await request.get_json()
        if not memory_entry:
            return await jsonify({"success": False, "error": "No memory entry provided"}), 400

        enhanced = await ai_service.enhance_mcp_memory(memory_entry)
        return await jsonify({
            "success": True,
            "enhanced_memory": enhanced,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return await handle_error(e)

@ai_bp.route('/analyze-codebase', methods=['POST'])
async def analyze_codebase():
    """Analyze codebase for rule suggestions."""
    try:
        data = await request.get_json()
        if not data:
            return await jsonify({"success": False, "error": "No analysis parameters provided"}), 400

        paths = data.get('paths', [])
        depth = data.get('depth', 2)
        include_patterns = data.get('include_patterns', [])
        exclude_patterns = data.get('exclude_patterns', [])

        analysis = await ai_service.analyze_codebase(
            paths=paths,
            depth=depth,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns
        )

        return await jsonify({
            "success": True,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return await handle_error(e)

@ai_bp.route('/query', methods=['POST'])
async def query():
    """Handle AI queries with context and knowledge graph integration"""
    try:
        data = await request.get_json()
        if not data or 'query' not in data:
            return await jsonify({"success": False, "error": "No query provided"}), 400

        # Get context and process query
        context = data.get('context', {})
        query = data['query']

        # Process query with context
        response = await ai_service.process_query(query, context)

        # Update knowledge graph with query and response
        if response.get('success', False):
            try:
                await kg_client.add_interaction({
                    'query': query,
                    'response': response['response'],
                    'timestamp': datetime.now().isoformat(),
                    'context': context
                })
            except Exception as e:
                logger.warning(f"Failed to update knowledge graph: {str(e)}")

        return await jsonify({
            "success": True,
            "response": response.get('response'),
            "context": response.get('context', {}),
            "confidence": response.get('confidence', 1.0),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return await handle_error(e)

@ai_bp.route('/status', methods=['GET'])
async def status():
    """Get AI system status including KG health"""
    try:
        ai_status = await ai_service.get_status()
        kg_status = await kg_client.get_health()

        return await jsonify({
            "success": True,
            "ai_status": ai_status,
            "kg_status": kg_status,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return await handle_error(e)

@ai_bp.route('/feedback', methods=['POST'])
async def submit_feedback():
    """Submit feedback for AI responses with KG updates"""
    try:
        data = await request.get_json()
        if not data or 'feedback' not in data:
            return await jsonify({'success': False, 'error': 'No feedback provided'}), 400

        feedback = data['feedback']
        query_id = data.get('query_id')
        
        # Process feedback
        result = await ai_service.process_feedback(feedback, query_id)

        # Update knowledge graph with feedback
        try:
            await kg_client.add_feedback({
                'query_id': query_id,
                'feedback': feedback,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            logger.warning(f"Failed to update knowledge graph with feedback: {str(e)}")

        return await jsonify({
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return await handle_error(e)

@ai_bp.route('/context', methods=['GET'])
async def get_context():
    """Get current AI context including KG context"""
    try:
        ai_context = await ai_service.get_context()
        kg_context = await kg_client.get_context()

        return await jsonify({
            "success": True,
            "ai_context": ai_context,
            "kg_context": kg_context,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return await handle_error(e)

@ai_bp.route('/context', methods=['POST'])
async def update_context():
    """Update AI context and sync with KG"""
    try:
        data = await request.get_json()
        if not data:
            return await jsonify({"success": False, "error": "No context data provided"}), 400

        # Update AI service context
        await ai_service.update_context(data)

        # Sync with knowledge graph
        try:
            await kg_client.update_context(data)
        except Exception as e:
            logger.warning(f"Failed to sync context with knowledge graph: {str(e)}")

        return await jsonify({
            "success": True,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return await handle_error(e)

@ai_bp.route('/kg/visualize', methods=['GET'])
async def get_kg_visualization():
    """Get knowledge graph visualization data"""
    try:
        data = await kg_client.get_visualization_data()
        return await jsonify({
            "success": True,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return await handle_error(e)

@ai_bp.route('/kg/search', methods=['POST'])
async def search_kg():
    """Search knowledge graph"""
    try:
        data = await request.get_json()
        if not data or 'query' not in data:
            return await jsonify({"success": False, "error": "No search query provided"}), 400

        results = await kg_client.search(data['query'])
        return await jsonify({
            "success": True,
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return await handle_error(e) 