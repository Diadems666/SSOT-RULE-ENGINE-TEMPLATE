"""
Knowledge Graph Client for SSOT Rule Engine Dashboard
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class KGClient:
    def __init__(self):
        self.memory_file = os.path.join('.cursor', 'CORE', 'MEMORY', 'memory.jsonl')
        self.connected = False
        self.last_sync = None
        self._ensure_memory_file()
        
    def is_connected(self) -> bool:
        """Check if connected to Knowledge Graph"""
        return self.connected
        
    def get_relevant_context(self, query: str) -> Dict[str, Any]:
        """Get relevant context from Knowledge Graph for a query"""
        try:
            # Load memory entries
            entries = self._load_memory()
            
            # TODO: Implement actual context retrieval logic
            relevant_entries = self._filter_relevant_entries(entries, query)
            
            return {
                'entries': relevant_entries,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_visualization_data(self) -> Dict[str, Any]:
        """Get data for Knowledge Graph visualization"""
        try:
            entries = self._load_memory()
            
            # Transform entries into visualization format
            nodes = []
            edges = []
            
            for entry in entries:
                nodes.append({
                    'id': entry.get('id'),
                    'label': entry.get('title'),
                    'type': entry.get('type', 'memory')
                })
                
                # Add edges based on relationships
                for rel in entry.get('relationships', []):
                    edges.append({
                        'from': entry.get('id'),
                        'to': rel.get('target_id'),
                        'label': rel.get('type')
                    })
            
            return {
                'nodes': nodes,
                'edges': edges,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _ensure_memory_file(self) -> None:
        """Ensure memory file exists"""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            if not os.path.exists(self.memory_file):
                with open(self.memory_file, 'w') as f:
                    f.write('')
            self.connected = True
            self.last_sync = datetime.now()
        except Exception as e:
            self.connected = False
            raise Exception(f"Failed to initialize memory file: {str(e)}")
    
    def _load_memory(self) -> List[Dict[str, Any]]:
        """Load memory entries from file"""
        entries = []
        try:
            with open(self.memory_file, 'r') as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))
            return entries
        except Exception as e:
            raise Exception(f"Failed to load memory entries: {str(e)}")
    
    def _filter_relevant_entries(self, entries: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Filter entries relevant to the query"""
        # TODO: Implement actual relevance filtering logic
        return entries[:5]  # Return first 5 entries for now 