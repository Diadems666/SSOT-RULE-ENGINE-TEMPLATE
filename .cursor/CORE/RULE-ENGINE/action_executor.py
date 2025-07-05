from typing import Dict, Any, List, Callable
import logging
import json
import os
import importlib.util
import sys

class ActionExecutor:
    def __init__(self, custom_actions_dir: str = ".cursor/CORE/RULE-ENGINE/custom_actions"):
        self.logger = logging.getLogger("ActionExecutor")
        self.custom_actions_dir = custom_actions_dir
        self.actions: Dict[str, Callable] = self._load_built_in_actions()
        self._load_custom_actions()

    def _load_built_in_actions(self) -> Dict[str, Callable]:
        """Load built-in actions"""
        return {
            "log": self._action_log,
            "set_value": self._action_set_value,
            "delete_value": self._action_delete_value,
            "append_value": self._action_append_value,
            "increment_value": self._action_increment_value,
            "decrement_value": self._action_decrement_value,
            "multiply_value": self._action_multiply_value,
            "divide_value": self._action_divide_value,
            "create_file": self._action_create_file,
            "append_to_file": self._action_append_to_file,
            "delete_file": self._action_delete_file,
            "http_request": self._action_http_request,
            "publish_event": self._action_publish_event,
            "send_notification": self._action_send_notification
        }

    def _load_custom_actions(self) -> None:
        """Load custom actions from Python files in the custom actions directory"""
        if not os.path.exists(self.custom_actions_dir):
            os.makedirs(self.custom_actions_dir)
            return

        sys.path.append(self.custom_actions_dir)
        
        for filename in os.listdir(self.custom_actions_dir):
            if filename.endswith('.py'):
                try:
                    module_name = filename[:-3]
                    spec = importlib.util.spec_from_file_location(
                        module_name,
                        os.path.join(self.custom_actions_dir, filename)
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        # Look for action functions (marked with @action decorator)
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            if hasattr(attr, '_is_action'):
                                self.actions[attr._action_name] = attr
                                self.logger.info(f"Loaded custom action: {attr._action_name}")
                except Exception as e:
                    self.logger.error(f"Error loading custom action file {filename}: {str(e)}")

    def execute(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action with the given context"""
        action_type = action.get("type")
        if not action_type:
            raise ValueError("Action type not specified")

        action_func = self.actions.get(action_type)
        if not action_func:
            raise ValueError(f"Unknown action type: {action_type}")

        try:
            params = action.get("params", {})
            result = action_func(context, **params)
            return {
                "success": True,
                "action_type": action_type,
                "result": result
            }
        except Exception as e:
            self.logger.error(f"Error executing action {action_type}: {str(e)}")
            return {
                "success": False,
                "action_type": action_type,
                "error": str(e)
            }

    # Built-in actions
    def _action_log(self, context: Dict[str, Any], level: str = "info", message: str = "") -> None:
        """Log a message at the specified level"""
        log_func = getattr(self.logger, level.lower(), self.logger.info)
        log_func(message)

    def _action_set_value(self, context: Dict[str, Any], path: str, value: Any) -> None:
        """Set a value in the context at the specified path"""
        parts = path.split('.')
        current = context
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value

    def _action_delete_value(self, context: Dict[str, Any], path: str) -> None:
        """Delete a value from the context at the specified path"""
        parts = path.split('.')
        current = context
        for part in parts[:-1]:
            if part not in current:
                return
            current = current[part]
        if parts[-1] in current:
            del current[parts[-1]]

    def _action_append_value(self, context: Dict[str, Any], path: str, value: Any) -> None:
        """Append a value to a list in the context at the specified path"""
        parts = path.split('.')
        current = context
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        if parts[-1] not in current:
            current[parts[-1]] = []
        elif not isinstance(current[parts[-1]], list):
            raise ValueError(f"Value at {path} is not a list")
        
        current[parts[-1]].append(value)

    def _action_increment_value(self, context: Dict[str, Any], path: str, amount: float = 1) -> None:
        """Increment a numeric value in the context at the specified path"""
        parts = path.split('.')
        current = context
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        if parts[-1] not in current:
            current[parts[-1]] = 0
        elif not isinstance(current[parts[-1]], (int, float)):
            raise ValueError(f"Value at {path} is not numeric")
        
        current[parts[-1]] += amount

    def _action_decrement_value(self, context: Dict[str, Any], path: str, amount: float = 1) -> None:
        """Decrement a numeric value in the context at the specified path"""
        self._action_increment_value(context, path, -amount)

    def _action_multiply_value(self, context: Dict[str, Any], path: str, factor: float) -> None:
        """Multiply a numeric value in the context at the specified path"""
        parts = path.split('.')
        current = context
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        if parts[-1] not in current:
            current[parts[-1]] = 0
        elif not isinstance(current[parts[-1]], (int, float)):
            raise ValueError(f"Value at {path} is not numeric")
        
        current[parts[-1]] *= factor

    def _action_divide_value(self, context: Dict[str, Any], path: str, divisor: float) -> None:
        """Divide a numeric value in the context at the specified path"""
        if divisor == 0:
            raise ValueError("Cannot divide by zero")
        self._action_multiply_value(context, path, 1/divisor)

    def _action_create_file(self, context: Dict[str, Any], path: str, content: str = "") -> None:
        """Create a file with the specified content"""
        with open(path, 'w') as f:
            f.write(content)

    def _action_append_to_file(self, context: Dict[str, Any], path: str, content: str) -> None:
        """Append content to a file"""
        with open(path, 'a') as f:
            f.write(content)

    def _action_delete_file(self, context: Dict[str, Any], path: str) -> None:
        """Delete a file"""
        if os.path.exists(path):
            os.remove(path)

    def _action_http_request(self, context: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Make an HTTP request (placeholder - implement with proper HTTP client)"""
        # TODO: Implement with requests library
        return {"status": "not_implemented"}

    def _action_publish_event(self, context: Dict[str, Any], event_type: str, payload: Dict[str, Any]) -> None:
        """Publish an event (placeholder - implement with proper event system)"""
        # TODO: Implement with proper event system
        self.logger.info(f"Event published - Type: {event_type}, Payload: {json.dumps(payload)}")

    def _action_send_notification(self, context: Dict[str, Any], message: str, channel: str = "default") -> None:
        """Send a notification (placeholder - implement with proper notification system)"""
        # TODO: Implement with proper notification system
        self.logger.info(f"Notification sent - Channel: {channel}, Message: {message}")

def action(name: str):
    """Decorator to mark custom action functions"""
    def decorator(func):
        func._is_action = True
        func._action_name = name
        return func
    return decorator 