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
            logger.error(f"Failed to load MCP config: {str(e)}")
            raise
            
    async def _ensure_session(self):
        """Ensure aiohttp session is initialized"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config['clientOptions']['timeout'])
            )
            
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
        
    async def close(self):
        """Close the client session"""
        if self.session and not self.session.closed:
            await self.session.close() 