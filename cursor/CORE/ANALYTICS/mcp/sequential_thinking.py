"""
Sequential Thinking Module for SSOT Rule Engine
Implements sequential thinking for complex problem solving
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

class SequentialThinking:
    def __init__(self):
        self.config = self._load_config()
        self.base_url = f"http://{self.config['servers']['sequential_thinking']['host']}:{self.config['servers']['sequential_thinking']['port']}"
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
                    'sequential_thinking': {
                        'host': 'localhost',
                        'port': 5001
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
            
    async def think(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a thought using sequential thinking"""
        try:
            await self._ensure_session()
            
            # Add timestamp to context
            context['timestamp'] = datetime.now().isoformat()
            
            # Send request to sequential thinking server
            async with self.session.post(f"{self.base_url}/think", json=context) as response:
                if response.status == 200:
                    thought = await response.json()
                    return {
                        'content': thought.get('content', ''),
                        'confidence': thought.get('confidence', 0.0),
                        'rule_name': thought.get('rule_name', ''),
                        'rule_description': thought.get('rule_description', ''),
                        'conditions': thought.get('conditions', []),
                        'actions': thought.get('actions', []),
                        'metadata': thought.get('metadata', {}),
                        'response': thought.get('response', ''),
                        'timestamp': thought.get('timestamp', datetime.now().isoformat())
                    }
                else:
                    logger.error(f"Error generating thought: {await response.text()}")
                    return {
                        'content': 'Error generating thought',
                        'confidence': 0.0,
                        'timestamp': datetime.now().isoformat()
                    }
                    
        except Exception as e:
            logger.error(f"Error generating thought: {str(e)}")
            return {
                'content': f"Error: {str(e)}",
                'confidence': 0.0,
                'timestamp': datetime.now().isoformat()
            } 