"""
AI Service for SSOT Rule Engine Dashboard
Integrates with MCP for knowledge graph and memory management
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from ..mcp.kg_client import KGClient
import asyncio
from mcp.sequential_thinking import SequentialThinking

# Configure logging
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.kg_client = KGClient()
        self.sequential_thinking = SequentialThinking()
        self.model_loaded = True
        self.last_query_time = None
        self.context_buffer = []
        self.max_context_items = 10
        
    async def generate_rule(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a new rule using AI and context"""
        try:
            # Get relevant knowledge from KG
            kg_data = await self.kg_client.search_nodes(context.get('description', ''))
            
            # Use sequential thinking to generate rule
            thoughts = await self.sequential_thinking.think({
                'task': 'generate_rule',
                'description': context.get('description', ''),
                'kg_data': kg_data,
                'context': context
            })
            
            # Extract rule configuration from thoughts
            rule_config = self._extract_rule_from_thoughts(thoughts)
            
            # Store in Knowledge Graph
            await self.kg_client.create_entities([{
                'name': rule_config['name'],
                'entityType': 'Rule',
                'observations': [rule_config['description']]
            }])
            
            return rule_config
            
        except Exception as e:
            logger.error(f"Error generating rule: {str(e)}")
            raise
    
    async def generate_documentation(self, rule_config: Dict[str, Any]) -> str:
        """Generate documentation for a rule"""
        try:
            # Get rule context from KG
            kg_data = await self.kg_client.search_nodes(rule_config['name'])
            
            # Use sequential thinking to generate documentation
            thoughts = await self.sequential_thinking.think({
                'task': 'generate_documentation',
                'rule_config': rule_config,
                'kg_data': kg_data
            })
            
            # Extract documentation from thoughts
            docs = self._extract_docs_from_thoughts(thoughts)
            
            # Store in Knowledge Graph
            await self.kg_client.add_observations([{
                'entityName': rule_config['name'],
                'contents': [docs]
            }])
            
            return docs
            
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}")
            raise
    
    async def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process an AI query using sequential thinking"""
        try:
            # Record query time
            self.last_query_time = datetime.now()
            
            # Get context from Knowledge Graph
            kg_context = await self.kg_client.get_relevant_context(query)
            
            # Combine contexts
            full_context = {
                **(context or {}),
                'kg_context': kg_context,
                'buffer': self.context_buffer
            }
            
            # Use sequential thinking to process query
            thoughts = await self.sequential_thinking.think({
                'task': 'process_query',
                'query': query,
                'context': full_context
            })
            
            # Extract response from thoughts
            response = self._extract_response_from_thoughts(thoughts)
            
            # Update context buffer
            self._update_context_buffer({
                'query': query,
                'response': response,
                'timestamp': self.last_query_time.isoformat(),
                'context': full_context
            })
            
            # Store interaction in Knowledge Graph
            await self.kg_client.create_entities([{
                'name': f"Query_{self.last_query_time.isoformat()}",
                'entityType': 'Interaction',
                'observations': [
                    query,
                    json.dumps(response)
                ]
            }])
            
            return {
                'success': True,
                'response': response['answer'],
                'context': response['context_used'],
                'confidence': response['confidence'],
                'timestamp': self.last_query_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current status of the AI service"""
        kg_status = await self.kg_client.get_health()
        return {
            'model_loaded': self.model_loaded,
            'last_query_time': self.last_query_time.isoformat() if self.last_query_time else None,
            'kg_status': kg_status,
            'context_buffer_size': len(self.context_buffer)
        }
    
    async def process_feedback(self, feedback: str, query_id: Optional[str] = None) -> Dict[str, Any]:
        """Process user feedback using sequential thinking"""
        try:
            # Use sequential thinking to process feedback
            thoughts = await self.sequential_thinking.think({
                'task': 'process_feedback',
                'feedback': feedback,
                'query_id': query_id,
                'context': self.context_buffer
            })
            
            # Extract feedback results from thoughts
            feedback_results = self._extract_feedback_from_thoughts(thoughts)
            
            # Store feedback in Knowledge Graph
            await self.kg_client.create_entities([{
                'name': f"Feedback_{datetime.now().isoformat()}",
                'entityType': 'Feedback',
                'observations': [json.dumps(feedback_results)]
            }])
            
            return {
                'success': True,
                'results': feedback_results,
                'message': 'Feedback processed successfully'
            }
            
        except Exception as e:
            logger.error(f"Error processing feedback: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def get_context(self) -> Dict[str, Any]:
        """Get current AI context"""
        kg_status = await self.kg_client.get_health()
        return {
            'buffer': self.context_buffer,
            'kg_status': kg_status
        }
    
    async def update_context(self, context_data: Dict[str, Any]) -> None:
        """Update AI context"""
        self._update_context_buffer(context_data)
    
    def _update_context_buffer(self, context_item: Dict[str, Any]) -> None:
        """Update the context buffer with new information"""
        self.context_buffer.append(context_item)
        if len(self.context_buffer) > self.max_context_items:
            self.context_buffer.pop(0)
    
    def _extract_rule_from_thoughts(self, thoughts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract rule configuration from sequential thinking output"""
        # Get the final thought that contains the rule
        final_thought = thoughts[-1]
        
        return {
            'name': final_thought.get('rule_name', 'Generated Rule'),
            'description': final_thought.get('rule_description', ''),
            'pattern': final_thought.get('rule_pattern', ''),
            'actions': final_thought.get('rule_actions', []),
            'metadata': {
                'generated': datetime.now().isoformat(),
                'source': 'sequential_thinking',
                'confidence': final_thought.get('confidence', 1.0),
                'thought_process': thoughts
            }
        }
    
    def _extract_docs_from_thoughts(self, thoughts: List[Dict[str, Any]]) -> str:
        """Extract documentation from sequential thinking output"""
        # Get the final thought that contains the documentation
        final_thought = thoughts[-1]
        return final_thought.get('documentation', '')
    
    def _extract_response_from_thoughts(self, thoughts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract response from sequential thinking output"""
        # Get the final thought that contains the response
        final_thought = thoughts[-1]
        
        return {
            'answer': final_thought.get('answer', ''),
            'context_used': final_thought.get('context_used', {}),
            'confidence': final_thought.get('confidence', 1.0),
            'thought_process': thoughts
        }
    
    def _extract_feedback_from_thoughts(self, thoughts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract feedback results from sequential thinking output"""
        # Get the final thought that contains the feedback results
        final_thought = thoughts[-1]
        
        return {
            'processed_feedback': final_thought.get('processed_feedback', ''),
            'impact': final_thought.get('impact', {}),
            'suggestions': final_thought.get('suggestions', []),
            'confidence': final_thought.get('confidence', 1.0)
        } 