"""
Engine Integration Module
Handles integration with Cursor AI and rule application
"""

import os
from typing import Dict, List, Optional
from .rule_generator import RuleGenerator

class EngineIntegration:
    def __init__(self, rules_dir: str = ".cursor/rules"):
        self.rules_dir = rules_dir
        self.rule_generator = RuleGenerator(rules_dir)
        
    def apply_rules(self, context: Dict) -> List[Dict]:
        """Apply rules to given context and return results"""
        results = []
        rules = self._load_rules()
        
        for rule in rules:
            if rule.get('enabled', True):
                result = self._apply_rule(rule, context)
                if result:
                    results.append(result)
                    
        return results
        
    def _load_rules(self) -> List[Dict]:
        """Load all rules from rules directory"""
        rules = []
        
        if not os.path.exists(self.rules_dir):
            return rules
            
        for filename in os.listdir(self.rules_dir):
            if filename.endswith('.mdc'):
                filepath = os.path.join(self.rules_dir, filename)
                with open(filepath, 'r') as f:
                    rule = json.load(f)
                    rules.append(rule)
                    
        return sorted(rules, key=lambda x: x.get('priority', 1))
        
    def _apply_rule(self, rule: Dict, context: Dict) -> Optional[Dict]:
        """Apply single rule to context"""
        pattern = rule.get('pattern')
        if not pattern:
            return None
            
        # Basic pattern matching logic
        if pattern in str(context):
            return {
                'rule_id': rule.get('id'),
                'rule_name': rule.get('name'),
                'matched': True,
                'context': context
            }
            
        return None 