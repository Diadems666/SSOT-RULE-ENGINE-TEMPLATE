"""
Flask routes for AI integration with the SSOT Rule Engine dashboard.
"""

from flask import Blueprint, jsonify, request
from ..services.ai_service import AIService
import asyncio

ai_bp = Blueprint('ai', __name__)
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