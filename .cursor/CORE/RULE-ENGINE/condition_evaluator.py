from typing import Dict, Any, List, Callable
import operator
import re

class ConditionEvaluator:
    def __init__(self):
        self.operators = {
            "eq": operator.eq,
            "ne": operator.ne,
            "gt": operator.gt,
            "lt": operator.lt,
            "ge": operator.ge,
            "le": operator.le,
            "in": lambda x, y: x in y,
            "not_in": lambda x, y: x not in y,
            "contains": lambda x, y: y in x,
            "not_contains": lambda x, y: y not in x,
            "matches": lambda x, y: bool(re.match(y, x)),
            "not_matches": lambda x, y: not bool(re.match(y, x)),
            "type": lambda x, y: isinstance(x, eval(y)),
            "length": lambda x, y: len(x) == y,
            "empty": lambda x, _: not bool(x),
            "not_empty": lambda x, _: bool(x)
        }

    def evaluate(self, conditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """
        Evaluate a set of conditions against a context
        
        conditions format:
        {
            "operator": "and|or",
            "conditions": [
                {
                    "field": "path.to.field",
                    "operator": "eq|ne|gt|lt|ge|le|in|not_in|contains|not_contains|matches|not_matches|type|length|empty|not_empty",
                    "value": any
                },
                {
                    "operator": "and|or",
                    "conditions": [...] # nested conditions
                }
            ]
        }
        """
        if not conditions:
            return True

        operator_type = conditions.get("operator", "and").lower()
        conditions_list = conditions.get("conditions", [])

        if operator_type == "and":
            return all(self._evaluate_condition(condition, context) for condition in conditions_list)
        elif operator_type == "or":
            return any(self._evaluate_condition(condition, context) for condition in conditions_list)
        else:
            raise ValueError(f"Unknown operator type: {operator_type}")

    def _evaluate_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate a single condition"""
        # Handle nested conditions
        if "conditions" in condition:
            return self.evaluate(condition, context)

        field = condition.get("field")
        operator_name = condition.get("operator")
        expected_value = condition.get("value")

        if not field or not operator_name:
            raise ValueError("Invalid condition format: missing field or operator")

        # Get actual value from context using dot notation
        actual_value = self._get_field_value(context, field)
        
        # Get operator function
        operator_func = self.operators.get(operator_name)
        if not operator_func:
            raise ValueError(f"Unknown operator: {operator_name}")

        try:
            return operator_func(actual_value, expected_value)
        except Exception as e:
            raise ValueError(f"Error evaluating condition: {str(e)}")

    def _get_field_value(self, data: Dict[str, Any], field_path: str) -> Any:
        """Get a value from a nested dictionary using dot notation"""
        current = data
        for key in field_path.split('.'):
            if isinstance(current, dict):
                if key in current:
                    current = current[key]
                else:
                    return None
            elif isinstance(current, (list, tuple)) and key.isdigit():
                index = int(key)
                if 0 <= index < len(current):
                    current = current[index]
                else:
                    return None
            else:
                return None
        return current 