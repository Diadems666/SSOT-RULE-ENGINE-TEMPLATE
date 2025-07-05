from typing import Dict, Any, Union
import re
from datetime import datetime

class VariableResolver:
    def __init__(self):
        self.variable_pattern = re.compile(r'\${([^}]+)}')

    def resolve(self, template: Union[str, Dict, list], context: Dict[str, Any]) -> Any:
        """Resolve variables in a template using the context"""
        if isinstance(template, str):
            return self._resolve_string(template, context)
        elif isinstance(template, dict):
            return self._resolve_dict(template, context)
        elif isinstance(template, list):
            return self._resolve_list(template, context)
        return template

    def _resolve_string(self, template: str, context: Dict[str, Any]) -> str:
        """Resolve variables in a string template"""
        def replace(match):
            path = match.group(1)
            
            # Handle special variables
            if path == "current_timestamp":
                return datetime.now().isoformat()
            
            # Get value from context using dot notation
            value = self._get_value_from_path(context, path)
            return str(value) if value is not None else match.group(0)
            
        return self.variable_pattern.sub(replace, template)

    def _resolve_dict(self, template: Dict, context: Dict[str, Any]) -> Dict:
        """Resolve variables in a dictionary template"""
        result = {}
        for key, value in template.items():
            resolved_key = self.resolve(key, context)
            resolved_value = self.resolve(value, context)
            result[resolved_key] = resolved_value
        return result

    def _resolve_list(self, template: list, context: Dict[str, Any]) -> list:
        """Resolve variables in a list template"""
        return [self.resolve(item, context) for item in template]

    def _get_value_from_path(self, data: Dict[str, Any], path: str) -> Any:
        """Get a value from a nested dictionary using dot notation"""
        current = data
        for key in path.split('.'):
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