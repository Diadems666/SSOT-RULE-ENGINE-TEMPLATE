from flask import Blueprint, jsonify, request
from ..services.kg_service import KGService

kg_bp = Blueprint('kg', __name__, url_prefix='/api/kg')
kg_service = KGService()

@kg_bp.route('/data', methods=['GET'])
def get_kg_data():
    """Get all Knowledge Graph data for visualization"""
    try:
        data = kg_service.get_all_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@kg_bp.route('/node/<node_id>', methods=['GET'])
def get_node_details(node_id):
    """Get detailed information about a specific node"""
    try:
        node_data = kg_service.get_node_details(node_id)
        return jsonify(node_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@kg_bp.route('/entity', methods=['POST'])
def create_entity():
    """Create a new entity in the Knowledge Graph"""
    try:
        data = request.json
        entity = kg_service.create_entity(
            name=data['name'],
            entity_type=data['entityType'],
            observations=data.get('observations', [])
        )
        return jsonify(entity)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@kg_bp.route('/entity', methods=['PUT'])
def update_entity():
    """Update an existing entity in the Knowledge Graph"""
    try:
        data = request.json
        entity = kg_service.update_entity(
            old_name=data['oldName'],
            new_name=data['newName'],
            entity_type=data['entityType']
        )
        return jsonify(entity)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@kg_bp.route('/entity/<entity_id>', methods=['DELETE'])
def delete_entity(entity_id):
    """Delete an entity from the Knowledge Graph"""
    try:
        kg_service.delete_entity(entity_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@kg_bp.route('/relation', methods=['POST'])
def create_relation():
    """Create a new relation in the Knowledge Graph"""
    try:
        data = request.json
        relation = kg_service.create_relation(
            from_entity=data['from'],
            to_entity=data['to'],
            relation_type=data['relationType']
        )
        return jsonify(relation)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@kg_bp.route('/relation/<relation_id>', methods=['DELETE'])
def delete_relation(relation_id):
    """Delete a relation from the Knowledge Graph"""
    try:
        kg_service.delete_relation(relation_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@kg_bp.route('/search', methods=['GET'])
def search_nodes():
    """Search for nodes in the Knowledge Graph"""
    try:
        query = request.args.get('q', '')
        results = kg_service.search_nodes(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 