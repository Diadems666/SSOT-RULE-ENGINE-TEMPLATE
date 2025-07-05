"""
AI Service for LLM integration with the SSOT Rule Engine dashboard.
Handles rule generation, documentation, and Cursor AI integration.
"""

import os
import json
import aiohttp
import asyncio
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

@dataclass
class RuleConfig:
    name: str
    description: str
    pattern: str
    template: str
    language: str
    cursor_settings: Dict[str, any]

class AIService:
    def __init__(self, config_path: str = ".cursor/CORE/ANALYTICS/config/ai_config.json"):
        self.config_path = config_path
        self.cursor_api_url = os.getenv("CURSOR_API_URL", "http://localhost:3000")
        self.cursor_api_key = os.getenv("CURSOR_API_KEY")
        self.load_config()

    def load_config(self):
        """Load AI service configuration."""
        with open(self.config_path) as f:
            self.config = json.load(f)

    async def generate_rule(self, context: Dict[str, any]) -> RuleConfig:
        """
        Generate a rule using LLM with proper MDC format and Cursor guidelines.
        """
        prompt = self._build_rule_prompt(context)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.cursor_api_url}/ai/generate",
                headers={"Authorization": f"Bearer {self.cursor_api_key}"},
                json={
                    "prompt": prompt,
                    "context": context,
                    "options": {
                        "temperature": 0.7,
                        "max_tokens": 1000,
                        "format": "mdc"
                    }
                }
            ) as response:
                result = await response.json()
                
                return RuleConfig(
                    name=result["name"],
                    description=result["description"],
                    pattern=result["pattern"],
                    template=result["template"],
                    language=result["language"],
                    cursor_settings=result["cursor_settings"]
                )

    async def generate_documentation(self, rule_config: RuleConfig) -> str:
        """
        Generate comprehensive documentation for a rule using LLM.
        """
        prompt = self._build_doc_prompt(rule_config)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.cursor_api_url}/ai/generate",
                headers={"Authorization": f"Bearer {self.cursor_api_key}"},
                json={
                    "prompt": prompt,
                    "context": {"rule": rule_config.__dict__},
                    "options": {
                        "temperature": 0.7,
                        "max_tokens": 1500,
                        "format": "markdown"
                    }
                }
            ) as response:
                result = await response.json()
                return result["documentation"]

    async def enhance_mcp_memory(self, memory_entry: Dict[str, any]) -> Dict[str, any]:
        """
        Enhance MCP memory entries with AI-generated insights and connections.
        """
        prompt = self._build_memory_prompt(memory_entry)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.cursor_api_url}/ai/enhance",
                headers={"Authorization": f"Bearer {self.cursor_api_key}"},
                json={
                    "prompt": prompt,
                    "memory": memory_entry,
                    "options": {
                        "temperature": 0.5,
                        "max_tokens": 500
                    }
                }
            ) as response:
                result = await response.json()
                return result["enhanced_memory"]

    async def analyze_codebase(self, paths: List[str]) -> Dict[str, any]:
        """
        Analyze codebase for rule suggestions and documentation needs.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.cursor_api_url}/ai/analyze",
                headers={"Authorization": f"Bearer {self.cursor_api_key}"},
                json={
                    "paths": paths,
                    "options": {
                        "analysis_type": "rule_suggestions",
                        "include_docs": True
                    }
                }
            ) as response:
                return await response.json()

    def _build_rule_prompt(self, context: Dict[str, any]) -> str:
        """Build prompt for rule generation."""
        return f"""
        Generate a Cursor AI rule following MDC format and guidelines:
        
        Context:
        {json.dumps(context, indent=2)}
        
        Requirements:
        1. Follow .mdc file format
        2. Include proper cursor_settings
        3. Define clear pattern matching
        4. Provide comprehensive description
        5. Include usage examples
        6. Consider rule precedence
        
        Generate the rule configuration in JSON format.
        """

    def _build_doc_prompt(self, rule_config: RuleConfig) -> str:
        """Build prompt for documentation generation."""
        return f"""
        Generate comprehensive documentation for the following rule:
        
        Rule Configuration:
        {json.dumps(rule_config.__dict__, indent=2)}
        
        Include:
        1. Overview and purpose
        2. Usage examples
        3. Pattern explanation
        4. Configuration options
        5. Best practices
        6. Related rules
        7. Troubleshooting
        
        Format in Markdown.
        """

    def _build_memory_prompt(self, memory_entry: Dict[str, any]) -> str:
        """Build prompt for memory enhancement."""
        return f"""
        Enhance the following MCP memory entry with AI insights:
        
        Memory Entry:
        {json.dumps(memory_entry, indent=2)}
        
        Provide:
        1. Additional relevant connections
        2. Pattern recognition
        3. Usage suggestions
        4. Optimization opportunities
        5. Related documentation needs
        
        Return enhanced memory entry in JSON format.
        """ 