from typing import Dict, List, Optional
from ..mcp.kg_client import KGClient

class KGService:
    def __init__(self):
        self.client = KGClient()

    def get_all_data(self) -> Dict:
        """Get all Knowledge Graph data for visualization"""
        try:
            # Read the entire graph
            graph = self.client.read_graph()
            
            # Transform data for vis.js format
            nodes = []
            edges = []
            
            # Process entities
            for entity in graph['entities']:
                nodes.append({
                    'id': entity['id'],
                    'label': entity['name'],
                    'title': entity['name'],
                    'type': entity['entityType']
                })
            
            # Process relations
            for relation in graph['relations']:
                edges.append({
                    'id': relation['id'],
                    'from': relation['from'],
                    'to': relation['to'],
                    'label': relation['relationType']
                })
            
            return {
                'nodes': nodes,
                'edges': edges
            }
        except Exception as e:
            raise Exception(f"Failed to get Knowledge Graph data: {str(e)}")

    def get_node_details(self, node_id: str) -> Dict:
        """Get detailed information about a specific node"""
        try:
            # Get node data
            nodes = self.client.open_nodes([node_id])
            if not nodes:
                raise Exception("Node not found")
            
            node = nodes[0]
            
            # Get relations involving this node
            graph = self.client.read_graph()
            relations = [
                rel for rel in graph['relations']
                if rel['from'] == node_id or rel['to'] == node_id
            ]
            
            return {
                'id': node['id'],
                'label': node['name'],
                'type': node['entityType'],
                'observations': node['observations'],
                'relations': relations
            }
        except Exception as e:
            raise Exception(f"Failed to get node details: {str(e)}")

    def create_entity(self, name: str, entity_type: str, observations: List[str] = None) -> Dict:
        """Create a new entity in the Knowledge Graph"""
        try:
            entity = {
                'name': name,
                'entityType': entity_type,
                'observations': observations or []
            }
            
            self.client.create_entities([entity])
            return entity
        except Exception as e:
            raise Exception(f"Failed to create entity: {str(e)}")

    def update_entity(self, old_name: str, new_name: str, entity_type: str) -> Dict:
        """Update an existing entity in the Knowledge Graph"""
        try:
            # Search for the entity
            results = self.client.search_nodes(old_name)
            if not results:
                raise Exception("Entity not found")
            
            entity = results[0]
            
            # Create new entity with updated data
            new_entity = {
                'name': new_name,
                'entityType': entity_type,
                'observations': entity['observations']
            }
            
            # Delete old entity and create new one
            self.client.delete_entities([entity['id']])
            self.client.create_entities([new_entity])
            
            return new_entity
        except Exception as e:
            raise Exception(f"Failed to update entity: {str(e)}")

    def delete_entity(self, entity_id: str):
        """Delete an entity from the Knowledge Graph"""
        try:
            self.client.delete_entities([entity_id])
        except Exception as e:
            raise Exception(f"Failed to delete entity: {str(e)}")

    def create_relation(self, from_entity: str, to_entity: str, relation_type: str) -> Dict:
        """Create a new relation in the Knowledge Graph"""
        try:
            relation = {
                'from': from_entity,
                'to': to_entity,
                'relationType': relation_type
            }
            
            self.client.create_relations([relation])
            return relation
        except Exception as e:
            raise Exception(f"Failed to create relation: {str(e)}")

    def delete_relation(self, relation_id: str):
        """Delete a relation from the Knowledge Graph"""
        try:
            self.client.delete_relations([{
                'id': relation_id
            }])
        except Exception as e:
            raise Exception(f"Failed to delete relation: {str(e)}")

    def search_nodes(self, query: str) -> List[Dict]:
        """Search for nodes in the Knowledge Graph"""
        try:
            results = self.client.search_nodes(query)
            return results
        except Exception as e:
            raise Exception(f"Failed to search nodes: {str(e)}")

    def add_observation(self, entity_id: str, observation: str):
        """Add an observation to an entity"""
        try:
            self.client.add_observations([{
                'entityName': entity_id,
                'contents': [observation]
            }])
        except Exception as e:
            raise Exception(f"Failed to add observation: {str(e)}")

    def delete_observation(self, entity_id: str, observation: str):
        """Delete an observation from an entity"""
        try:
            self.client.delete_observations([{
                'entityName': entity_id,
                'observations': [observation]
            }])
        except Exception as e:
            raise Exception(f"Failed to delete observation: {str(e)}")

    def get_entity_types(self) -> List[str]:
        """Get a list of all entity types in the Knowledge Graph"""
        try:
            graph = self.client.read_graph()
            types = set(entity['entityType'] for entity in graph['entities'])
            return sorted(list(types))
        except Exception as e:
            raise Exception(f"Failed to get entity types: {str(e)}")

    def get_relation_types(self) -> List[str]:
        """Get a list of all relation types in the Knowledge Graph"""
        try:
            graph = self.client.read_graph()
            types = set(relation['relationType'] for relation in graph['relations'])
            return sorted(list(types))
        except Exception as e:
            raise Exception(f"Failed to get relation types: {str(e)}")

    def get_entity_stats(self) -> Dict:
        """Get statistics about entities in the Knowledge Graph"""
        try:
            graph = self.client.read_graph()
            
            # Count entities by type
            type_counts = {}
            for entity in graph['entities']:
                entity_type = entity['entityType']
                type_counts[entity_type] = type_counts.get(entity_type, 0) + 1
            
            # Count relations
            relation_count = len(graph['relations'])
            
            return {
                'total_entities': len(graph['entities']),
                'total_relations': relation_count,
                'entities_by_type': type_counts
            }
        except Exception as e:
            raise Exception(f"Failed to get entity statistics: {str(e)}")

    def analyze_graph(self) -> Dict:
        """Analyze the Knowledge Graph for insights"""
        try:
            graph = self.client.read_graph()
            
            # Calculate basic metrics
            entity_count = len(graph['entities'])
            relation_count = len(graph['relations'])
            
            # Find most connected entities
            entity_connections = {}
            for relation in graph['relations']:
                entity_connections[relation['from']] = entity_connections.get(relation['from'], 0) + 1
                entity_connections[relation['to']] = entity_connections.get(relation['to'], 0) + 1
            
            most_connected = sorted(
                entity_connections.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            # Calculate density
            max_relations = entity_count * (entity_count - 1)
            density = relation_count / max_relations if max_relations > 0 else 0
            
            return {
                'metrics': {
                    'entity_count': entity_count,
                    'relation_count': relation_count,
                    'density': density
                },
                'most_connected_entities': most_connected
            }
        except Exception as e:
            raise Exception(f"Failed to analyze graph: {str(e)}") 