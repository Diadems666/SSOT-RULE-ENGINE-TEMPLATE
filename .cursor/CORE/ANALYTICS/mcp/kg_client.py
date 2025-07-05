from typing import Dict, List, Optional
import uuid

class KGClient:
    def __init__(self):
        self._graph = {
            'entities': [],
            'relations': []
        }
        self._load_graph()

    def _load_graph(self):
        """Load the graph from MCP memory"""
        try:
            from mcp_memory_read_graph import mcp_memory_read_graph
            response = mcp_memory_read_graph({'random_string': 'dummy'})
            if response and isinstance(response, dict):
                self._graph = response
        except Exception:
            # If MCP is not available, use in-memory graph
            pass

    def _save_graph(self):
        """Save the graph to MCP memory"""
        try:
            from mcp_memory_create_entities import mcp_memory_create_entities
            from mcp_memory_create_relations import mcp_memory_create_relations
            
            # Clear existing graph
            self._clear_graph()
            
            # Create entities
            if self._graph['entities']:
                entities = [{
                    'name': entity['name'],
                    'entityType': entity['entityType'],
                    'observations': entity['observations']
                } for entity in self._graph['entities']]
                mcp_memory_create_entities({'entities': entities})
            
            # Create relations
            if self._graph['relations']:
                relations = [{
                    'from': relation['from'],
                    'to': relation['to'],
                    'relationType': relation['relationType']
                } for relation in self._graph['relations']]
                mcp_memory_create_relations({'relations': relations})
        except Exception:
            # If MCP is not available, keep using in-memory graph
            pass

    def _clear_graph(self):
        """Clear the existing graph from MCP memory"""
        try:
            from mcp_memory_delete_entities import mcp_memory_delete_entities
            
            # Get all entity names
            entity_names = [entity['name'] for entity in self._graph['entities']]
            if entity_names:
                mcp_memory_delete_entities({'entityNames': entity_names})
        except Exception:
            # If MCP is not available, continue
            pass

    def read_graph(self) -> Dict:
        """Read the entire graph"""
        return self._graph

    def create_entities(self, entities: List[Dict]):
        """Create new entities in the graph"""
        for entity in entities:
            entity_id = str(uuid.uuid4())
            self._graph['entities'].append({
                'id': entity_id,
                'name': entity['name'],
                'entityType': entity['entityType'],
                'observations': entity.get('observations', [])
            })
        self._save_graph()

    def delete_entities(self, entity_ids: List[str]):
        """Delete entities from the graph"""
        self._graph['entities'] = [
            entity for entity in self._graph['entities']
            if entity['id'] not in entity_ids
        ]
        
        # Remove related relations
        self._graph['relations'] = [
            relation for relation in self._graph['relations']
            if relation['from'] not in entity_ids and relation['to'] not in entity_ids
        ]
        
        self._save_graph()

    def create_relations(self, relations: List[Dict]):
        """Create new relations in the graph"""
        for relation in relations:
            relation_id = str(uuid.uuid4())
            self._graph['relations'].append({
                'id': relation_id,
                'from': relation['from'],
                'to': relation['to'],
                'relationType': relation['relationType']
            })
        self._save_graph()

    def delete_relations(self, relations: List[Dict]):
        """Delete relations from the graph"""
        relation_ids = [relation['id'] for relation in relations]
        self._graph['relations'] = [
            relation for relation in self._graph['relations']
            if relation['id'] not in relation_ids
        ]
        self._save_graph()

    def search_nodes(self, query: str) -> List[Dict]:
        """Search for nodes in the graph"""
        query = query.lower()
        return [
            entity for entity in self._graph['entities']
            if query in entity['name'].lower() or
            query in entity['entityType'].lower() or
            any(query in obs.lower() for obs in entity['observations'])
        ]

    def open_nodes(self, node_ids: List[str]) -> List[Dict]:
        """Get specific nodes by their IDs"""
        return [
            entity for entity in self._graph['entities']
            if entity['id'] in node_ids
        ]

    def add_observations(self, observations: List[Dict]):
        """Add observations to entities"""
        for obs in observations:
            for entity in self._graph['entities']:
                if entity['name'] == obs['entityName']:
                    entity['observations'].extend(obs['contents'])
        self._save_graph()

    def delete_observations(self, deletions: List[Dict]):
        """Delete observations from entities"""
        for deletion in deletions:
            for entity in self._graph['entities']:
                if entity['name'] == deletion['entityName']:
                    entity['observations'] = [
                        obs for obs in entity['observations']
                        if obs not in deletion['observations']
                    ]
        self._save_graph() 