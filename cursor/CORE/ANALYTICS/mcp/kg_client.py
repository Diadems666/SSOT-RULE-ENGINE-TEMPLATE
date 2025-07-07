"""
Knowledge Graph Client for SSOT Rule Engine
Handles communication with the MCP Knowledge Graph server
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import aiohttp
import asyncio

# Configure logging
logger = logging.getLogger(__name__)

class KGClient:
    def __init__(self):
        self.config = self._load_config()
        self.base_url = f"http://{self.config['servers']['knowledge_graph']['host']}:{self.config['servers']['knowledge_graph']['port']}"
        self.session = None
        self.retry_attempts = self.config['clientOptions']['retryAttempts']
        self.retry_delay = self.config['clientOptions']['retryDelay']
        
    def _load_config(self) -> Dict[str, Any]:
        """Load MCP configuration"""
        try:
            with open('mcp.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading MCP config: {str(e)}")
            return {
                'servers': {
                    'knowledge_graph': {
                        'host': 'localhost',
                        'port': 5002
                    }
                },
                'clientOptions': {
                    'retryAttempts': 3,
                    'retryDelay': 1
                }
            }
            
    async def _ensure_session(self):
        """Ensure aiohttp session exists"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def close(self):
        """Close the client session"""
        if self.session:
            await self.session.close()
            self.session = None
            
    async def add_rule(self, rule: Dict[str, Any]) -> bool:
        """Add a rule to the knowledge graph"""
        try:
            await self._ensure_session()
            
            # Create rule entity
            entity = {
                'name': rule['name'],
                'entityType': 'Rule',
                'observations': [
                    rule['description'],
                    json.dumps({
                        'conditions': rule['conditions'],
                        'actions': rule['actions'],
                        'metadata': rule['metadata']
                    })
                ]
            }
            
            # Add to knowledge graph
            async with self.session.post(f"{self.base_url}/entities", json=entity) as response:
                if response.status == 200:
                    return True
                else:
                    logger.error(f"Error adding rule: {await response.text()}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error adding rule: {str(e)}")
            return False
            
    async def search_nodes(self, query: str) -> List[Dict[str, Any]]:
        """Search knowledge graph nodes"""
        try:
            await self._ensure_session()
            
            async with self.session.get(f"{self.base_url}/search", params={'query': query}) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Error searching nodes: {await response.text()}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error searching nodes: {str(e)}")
            return []
            
    async def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific node from the knowledge graph"""
        try:
            await self._ensure_session()
            
            async with self.session.get(f"{self.base_url}/nodes/{node_id}") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Error getting node: {await response.text()}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting node: {str(e)}")
            return None
            
    async def create_relation(self, from_id: str, to_id: str, relation_type: str) -> bool:
        """Create a relation between nodes"""
        try:
            await self._ensure_session()
            
            relation = {
                'from': from_id,
                'to': to_id,
                'type': relation_type
            }
            
            async with self.session.post(f"{self.base_url}/relations", json=relation) as response:
                if response.status == 200:
                    return True
                else:
                    logger.error(f"Error creating relation: {await response.text()}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error creating relation: {str(e)}")
            return False
            
    async def get_related_nodes(self, node_id: str, relation_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get nodes related to a specific node"""
        try:
            await self._ensure_session()
            
            params = {'node_id': node_id}
            if relation_type:
                params['relation_type'] = relation_type
                
            async with self.session.get(f"{self.base_url}/related", params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Error getting related nodes: {await response.text()}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting related nodes: {str(e)}")
            return []
        
    async def create_entities(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create new entities in the Knowledge Graph"""
        return await self._request('POST', '/entities/create', {'entities': entities})
        
    async def create_relations(self, relations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create new relations in the Knowledge Graph"""
        return await self._request('POST', '/relations/create', {'relations': relations})
        
    async def add_observations(self, observations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add observations to existing entities"""
        return await self._request('POST', '/entities/observations/add', {'observations': observations})
        
    async def get_relevant_context(self, query: str) -> Dict[str, Any]:
        """Get relevant context for a query"""
        return await self._request('POST', '/context/relevant', {'query': query})
        
    async def add_interaction(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Add an interaction to the Knowledge Graph"""
        return await self._request('POST', '/interactions/add', {'interaction': interaction})
        
    async def add_feedback(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Add feedback to the Knowledge Graph"""
        return await self._request('POST', '/feedback/add', {'feedback': feedback})
        
    async def get_health(self) -> Dict[str, Any]:
        """Get Knowledge Graph health status"""
        return await self._request('GET', '/health')
        
    async def get_context(self) -> Dict[str, Any]:
        """Get current Knowledge Graph context"""
        return await self._request('GET', '/context')
        
    async def update_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Update Knowledge Graph context"""
        return await self._request('POST', '/context/update', {'context': context})
        
    async def get_visualization_data(self) -> Dict[str, Any]:
        """Get data for Knowledge Graph visualization"""
        return await self._request('GET', '/visualize')
        
    async def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        await self._ensure_session()
        
        for attempt in range(self.retry_attempts):
            try:
                async with self.session.request(
                    method, 
                    f"{self.base_url}{endpoint}",
                    json=data if data else None
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        text = await response.text()
                        raise Exception(f"Request failed with status {response.status}: {text}")
                        
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    raise
                await asyncio.sleep(self.retry_delay * (2 ** attempt))
                
    async def create_entities(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create new entities in the Knowledge Graph"""
        return await self._request('POST', '/entities/create', {'entities': entities})
        
    async def create_relations(self, relations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create new relations in the Knowledge Graph"""
        return await self._request('POST', '/relations/create', {'relations': relations})
        
    async def add_observations(self, observations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add observations to existing entities"""
        return await self._request('POST', '/entities/observations/add', {'observations': observations})
        
    async def search_nodes(self, query: str) -> Dict[str, Any]:
        """Search for nodes in the Knowledge Graph"""
        return await self._request('POST', '/search', {'query': query})
        
    async def get_relevant_context(self, query: str) -> Dict[str, Any]:
        """Get relevant context for a query"""
        return await self._request('POST', '/context/relevant', {'query': query})
        
    async def add_interaction(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Add an interaction to the Knowledge Graph"""
        return await self._request('POST', '/interactions/add', {'interaction': interaction})
        
    async def add_feedback(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Add feedback to the Knowledge Graph"""
        return await self._request('POST', '/feedback/add', {'feedback': feedback})
        
    async def get_health(self) -> Dict[str, Any]:
        """Get Knowledge Graph health status"""
        return await self._request('GET', '/health')
        
    async def get_context(self) -> Dict[str, Any]:
        """Get current Knowledge Graph context"""
        return await self._request('GET', '/context')
        
    async def update_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Update Knowledge Graph context"""
        return await self._request('POST', '/context/update', {'context': context})
        
    async def get_visualization_data(self) -> Dict[str, Any]:
        """Get data for Knowledge Graph visualization"""
        return await self._request('GET', '/visualize') 