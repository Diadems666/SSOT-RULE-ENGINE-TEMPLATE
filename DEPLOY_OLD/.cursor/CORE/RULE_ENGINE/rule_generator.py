"""
Rule Generator Module
Handles the generation and validation of rules
"""

import json
import os
from typing import Dict, List, Optional

class RuleGenerator:
    def __init__(self, rules_dir: str = ".cursor/rules"):
        self.rules_dir = rules_dir
        
    def generate_rule(self, rule_data: Dict) -> str:
        """Generate a new rule file from rule data"""
        rule_id = rule_data.get('id', 'unknown')
        rule_content = self._format_rule(rule_data)
        
        filename = f"{rule_id}.mdc"
        filepath = os.path.join(self.rules_dir, filename)
        
        os.makedirs(self.rules_dir, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(rule_content, f, indent=2)
            
        return filepath
        
    def validate_rule(self, rule_data: Dict) -> List[str]:
        """Validate rule data and return list of errors"""
        errors = []
        required_fields = ['id', 'name', 'description', 'pattern']
        
        for field in required_fields:
            if field not in rule_data:
                errors.append(f"Missing required field: {field}")
                
        return errors
        
    def _format_rule(self, rule_data: Dict) -> Dict:
        """Format rule data into proper structure"""
        return {
            'id': rule_data.get('id'),
            'name': rule_data.get('name'),
            'description': rule_data.get('description'),
            'pattern': rule_data.get('pattern'),
            'enabled': rule_data.get('enabled', True),
            'priority': rule_data.get('priority', 1),
            'metadata': rule_data.get('metadata', {})
        } 