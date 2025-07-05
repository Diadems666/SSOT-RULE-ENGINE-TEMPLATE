"""
Message Handler Module
Handles communication between components
"""

from typing import Dict, List, Callable
from .event_system import EventSystem

class MessageHandler:
    def __init__(self):
        self.event_system = EventSystem()
        self.handlers: Dict[str, List[Callable]] = {}
        
    def register_handler(self, message_type: str, handler: Callable):
        """Register a handler for a specific message type"""
        if message_type not in self.handlers:
            self.handlers[message_type] = []
        self.handlers[message_type].append(handler)
        
    def send_message(self, message_type: str, data: Dict):
        """Send a message to all registered handlers"""
        if message_type in self.handlers:
            for handler in self.handlers[message_type]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"Error handling message {message_type}: {e}")
                    
        # Emit event for message sent
        self.event_system.emit('message_sent', {
            'type': message_type,
            'data': data
        }) 