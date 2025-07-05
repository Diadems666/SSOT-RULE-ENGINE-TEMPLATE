import os
import json
import shutil
from typing import Dict, Optional
from rule_generator import RuleGenerator

class RuleEngineIntegration:
    def __init__(self):
        self.rule_generator = RuleGenerator()
        self.rules_dir = ".cursor/rules"
        self.staging_dir = ".cursor/CORE/RULE-ENGINE/staging"
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.rules_dir, exist_ok=True)
        os.makedirs(self.staging_dir, exist_ok=True)

    def handle_trigger(self, trigger: str, context: Dict[str, any]) -> Optional[str]:
        """Handle rule engine triggers"""
        try:
            # Generate rules
            generated_path = self.rule_generator.handle_trigger(trigger, context)
            if not generated_path:
                return None

            # Stage rules
            staged_path = self._stage_rules(generated_path)
            if not staged_path:
                return None

            # Integrate rules
            return self._integrate_rules(staged_path)
        except Exception as e:
            print(f"Error handling trigger: {str(e)}")
            return None

    def _stage_rules(self, generated_path: str) -> Optional[str]:
        """Stage generated rules for review"""
        try:
            # Create staging directory with timestamp
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            stage_path = os.path.join(self.staging_dir, f"staged_rules_{timestamp}")
            
            # Copy generated rules to staging
            shutil.copytree(generated_path, stage_path)
            
            # Create staging manifest
            manifest = {
                "timestamp": timestamp,
                "source": generated_path,
                "rules": []
            }
            
            # Add rules to manifest
            for root, _, files in os.walk(stage_path):
                for file in files:
                    if file.endswith(".mdc"):
                        rule_path = os.path.join(root, file)
                        manifest["rules"].append({
                            "name": file,
                            "path": os.path.relpath(rule_path, stage_path)
                        })
            
            # Save manifest
            manifest_path = os.path.join(stage_path, "manifest.json")
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            return stage_path
        except Exception as e:
            print(f"Error staging rules: {str(e)}")
            return None

    def _integrate_rules(self, staged_path: str) -> Optional[str]:
        """Integrate staged rules into the project"""
        try:
            # Load staging manifest
            manifest_path = os.path.join(staged_path, "manifest.json")
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Copy rules to project rules directory
            for rule in manifest["rules"]:
                source = os.path.join(staged_path, rule["path"])
                dest = os.path.join(self.rules_dir, rule["name"])
                shutil.copy2(source, dest)
            
            return self.rules_dir
        except Exception as e:
            print(f"Error integrating rules: {str(e)}")
            return None

    def list_available_triggers(self) -> Dict[str, str]:
        """List available rule generation triggers"""
        return {
            "!!-GENERATE-RULES-!!": "Generate new project-specific rules",
            "!!-UPDATE-RULES-!!": "Update existing rules with new context",
            "!!-ANALYZE-CODEBASE-!!": "Generate rules by analyzing the codebase",
            "!!-IMPORT-RULES-!!": "Import and adapt external rules"
        }

    def get_trigger_context(self, trigger: str) -> Dict[str, any]:
        """Get required context for a trigger"""
        context_map = {
            "!!-GENERATE-RULES-!!": {
                "project_type": "Type of project (e.g., web, mobile, desktop)",
                "framework": "Main framework used (e.g., react, django)",
                "language": "Primary programming language"
            },
            "!!-UPDATE-RULES-!!": {
                "rules_dir": "Directory containing rules to update"
            },
            "!!-ANALYZE-CODEBASE-!!": {
                "codebase_path": "Path to the codebase to analyze"
            },
            "!!-IMPORT-RULES-!!": {
                "source_path": "Path to external rules to import"
            }
        }
        return context_map.get(trigger, {}) 