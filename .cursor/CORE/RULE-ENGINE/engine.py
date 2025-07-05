import json
import os
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import logging

@dataclass
class Rule:
    id: str
    name: str
    pattern: str
    priority: int
    is_active: bool
    description: str
    created_at: str
    updated_at: str
    tags: List[str]
    conditions: Dict[str, any]
    actions: Dict[str, any]
    metadata: Dict[str, any]

class RuleEngine:
    def __init__(self, rules_dir: str = ".cursor/CORE/RULE-ENGINE/rules"):
        self.rules_dir = rules_dir
        self.rules: Dict[str, Rule] = {}
        self.logger = self._setup_logger()
        self._load_rules()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("RuleEngine")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(".cursor/CORE/RULE-ENGINE/engine.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_rules(self) -> None:
        """Load all rules from the rules directory"""
        if not os.path.exists(self.rules_dir):
            os.makedirs(self.rules_dir)
            self.logger.info(f"Created rules directory: {self.rules_dir}")
            return

        for filename in os.listdir(self.rules_dir):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(self.rules_dir, filename), 'r') as f:
                        rule_data = json.load(f)
                        rule = Rule(**rule_data)
                        self.rules[rule.id] = rule
                        self.logger.info(f"Loaded rule: {rule.id}")
                except Exception as e:
                    self.logger.error(f"Error loading rule {filename}: {str(e)}")

    def add_rule(self, rule_data: Dict[str, any]) -> Optional[str]:
        """Add a new rule to the engine"""
        try:
            rule_data["created_at"] = datetime.now().isoformat()
            rule_data["updated_at"] = rule_data["created_at"]
            rule = Rule(**rule_data)
            
            # Save rule to file
            rule_path = os.path.join(self.rules_dir, f"{rule.id}.json")
            with open(rule_path, 'w') as f:
                json.dump(rule_data, f, indent=2)
            
            self.rules[rule.id] = rule
            self.logger.info(f"Added new rule: {rule.id}")
            return rule.id
        except Exception as e:
            self.logger.error(f"Error adding rule: {str(e)}")
            return None

    def update_rule(self, rule_id: str, updates: Dict[str, any]) -> bool:
        """Update an existing rule"""
        if rule_id not in self.rules:
            self.logger.warning(f"Rule not found: {rule_id}")
            return False

        try:
            rule_data = self.rules[rule_id].__dict__
            rule_data.update(updates)
            rule_data["updated_at"] = datetime.now().isoformat()
            
            # Update rule file
            rule_path = os.path.join(self.rules_dir, f"{rule_id}.json")
            with open(rule_path, 'w') as f:
                json.dump(rule_data, f, indent=2)
            
            self.rules[rule_id] = Rule(**rule_data)
            self.logger.info(f"Updated rule: {rule_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating rule {rule_id}: {str(e)}")
            return False

    def delete_rule(self, rule_id: str) -> bool:
        """Delete a rule from the engine"""
        if rule_id not in self.rules:
            self.logger.warning(f"Rule not found: {rule_id}")
            return False

        try:
            rule_path = os.path.join(self.rules_dir, f"{rule_id}.json")
            os.remove(rule_path)
            del self.rules[rule_id]
            self.logger.info(f"Deleted rule: {rule_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting rule {rule_id}: {str(e)}")
            return False

    def evaluate_rules(self, context: Dict[str, any]) -> List[Dict[str, any]]:
        """Evaluate all active rules against the given context"""
        results = []
        for rule in sorted(self.rules.values(), key=lambda x: x.priority, reverse=True):
            if not rule.is_active:
                continue

            try:
                if self._evaluate_conditions(rule.conditions, context):
                    action_results = self._execute_actions(rule.actions, context)
                    results.append({
                        "rule_id": rule.id,
                        "rule_name": rule.name,
                        "actions_executed": action_results
                    })
                    self.logger.info(f"Rule {rule.id} executed successfully")
            except Exception as e:
                self.logger.error(f"Error evaluating rule {rule.id}: {str(e)}")

        return results

    def _evaluate_conditions(self, conditions: Dict[str, any], context: Dict[str, any]) -> bool:
        """Evaluate rule conditions against the context"""
        # Implement condition evaluation logic here
        # This is a placeholder implementation
        return True

    def _execute_actions(self, actions: Dict[str, any], context: Dict[str, any]) -> List[str]:
        """Execute rule actions based on the context"""
        # Implement action execution logic here
        # This is a placeholder implementation
        return ["action_executed"]

    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """Get a rule by ID"""
        return self.rules.get(rule_id)

    def list_rules(self, active_only: bool = False) -> List[Rule]:
        """List all rules, optionally filtering for active ones only"""
        if active_only:
            return [rule for rule in self.rules.values() if rule.is_active]
        return list(self.rules.values())

    def export_rules(self, output_path: str) -> bool:
        """Export all rules to a JSON file"""
        try:
            rules_data = {rule_id: rule.__dict__ for rule_id, rule in self.rules.items()}
            with open(output_path, 'w') as f:
                json.dump(rules_data, f, indent=2)
            self.logger.info(f"Exported rules to: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting rules: {str(e)}")
            return False

    def import_rules(self, input_path: str) -> bool:
        """Import rules from a JSON file"""
        try:
            with open(input_path, 'r') as f:
                rules_data = json.load(f)
            
            for rule_data in rules_data.values():
                self.add_rule(rule_data)
            
            self.logger.info(f"Imported rules from: {input_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error importing rules: {str(e)}")
            return False 