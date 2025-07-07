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
from ..mcp.sequential_thinking import SequentialThinking
import asyncio

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
        """Generate a new rule using AI"""
        try:
            # Initialize sequential thinking
            thoughts = []
            total_thoughts = 5
            
            # Generate initial thoughts
            for i in range(total_thoughts):
                thought = await self.sequential_thinking.think({
                    'context': context,
                    'previous_thoughts': thoughts,
                    'thought_number': i + 1,
                    'total_thoughts': total_thoughts
                })
                thoughts.append(thought)
                
            # Extract rule from thoughts
            rule = self._extract_rule_from_thoughts(thoughts)
            
            # Update knowledge graph
            await self.kg_client.add_rule(rule)
            
            return {
                'success': True,
                'rule': rule,
                'thoughts': thoughts,
                'confidence': self._calculate_confidence(thoughts)
            }
            
        except Exception as e:
            logger.error(f"Error generating rule: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def _extract_rule_from_thoughts(self, thoughts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract rule from sequential thinking output"""
        # Combine thoughts into a coherent rule
        rule = {
            'name': '',
            'description': '',
            'conditions': [],
            'actions': [],
            'metadata': {}
        }
        
        for thought in thoughts:
            if 'rule_name' in thought:
                rule['name'] = thought['rule_name']
            if 'rule_description' in thought:
                rule['description'] = thought['rule_description']
            if 'conditions' in thought:
                rule['conditions'].extend(thought['conditions'])
            if 'actions' in thought:
                rule['actions'].extend(thought['actions'])
            if 'metadata' in thought:
                rule['metadata'].update(thought['metadata'])
                
        return rule
        
    def _calculate_confidence(self, thoughts: List[Dict[str, Any]]) -> float:
        """Calculate confidence score from thoughts"""
        if not thoughts:
            return 0.0
            
        # Average confidence across all thoughts
        confidence_sum = sum(thought.get('confidence', 0.0) for thought in thoughts)
        return confidence_sum / len(thoughts)
        
    async def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a natural language query"""
        try:
            # Update context buffer
            if context:
                self.context_buffer.append(context)
                if len(self.context_buffer) > self.max_context_items:
                    self.context_buffer.pop(0)
                    
            # Initialize sequential thinking
            thoughts = []
            total_thoughts = 3
            
            # Generate thoughts
            for i in range(total_thoughts):
                thought = await self.sequential_thinking.think({
                    'query': query,
                    'context': self.context_buffer,
                    'previous_thoughts': thoughts,
                    'thought_number': i + 1,
                    'total_thoughts': total_thoughts
                })
                thoughts.append(thought)
                
            # Extract response
            response = self._extract_response_from_thoughts(thoughts)
            
            # Update last query time
            self.last_query_time = datetime.now()
            
            return {
                'success': True,
                'response': response,
                'thoughts': thoughts,
                'confidence': self._calculate_confidence(thoughts)
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
            
    def _extract_response_from_thoughts(self, thoughts: List[Dict[str, Any]]) -> str:
        """Extract response from sequential thinking output"""
        if not thoughts:
            return ""
            
        # Get final thought's response
        final_thought = thoughts[-1]
        return final_thought.get('response', "")
    
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
    
    def _extract_docs_from_thoughts(self, thoughts: List[Dict[str, Any]]) -> str:
        """Extract documentation from sequential thinking output"""
        # Get the final thought that contains the documentation
        final_thought = thoughts[-1]
        return final_thought.get('documentation', '')
    
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