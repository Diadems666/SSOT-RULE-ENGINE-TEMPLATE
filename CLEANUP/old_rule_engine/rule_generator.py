import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Union
import logging
from pathlib import Path

class RuleGenerator:
    def __init__(self, base_dir: str = ".cursor/CORE/RULE-ENGINE"):
        self.base_dir = base_dir
        self.templates_dir = os.path.join(base_dir, "rule_templates")
        self.output_dir = os.path.join(base_dir, "generated_rules")
        self.logger = self._setup_logger()
        self._ensure_directories()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("RuleGenerator")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join(self.base_dir, "rule_generator.log"))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def handle_trigger(self, trigger: str, context: Dict[str, any]) -> Optional[str]:
        """Handle a rule generation trigger"""
        try:
            if trigger == "!!-GENERATE-RULES-!!":
                return self._generate_project_rules(context)
            elif trigger == "!!-UPDATE-RULES-!!":
                return self._update_existing_rules(context)
            elif trigger == "!!-ANALYZE-CODEBASE-!!":
                return self._generate_from_codebase(context)
            elif trigger == "!!-IMPORT-RULES-!!":
                return self._import_external_rules(context)
            else:
                self.logger.warning(f"Unknown trigger: {trigger}")
                return None
        except Exception as e:
            self.logger.error(f"Error handling trigger {trigger}: {str(e)}")
            return None

    def _generate_project_rules(self, context: Dict[str, any]) -> str:
        """Generate project-specific rules based on context"""
        try:
            project_type = context.get("project_type", "generic")
            framework = context.get("framework", "")
            language = context.get("language", "")
            
            # Load appropriate templates
            templates = self._load_templates(project_type, framework, language)
            
            # Generate rules
            generated_rules = []
            for template in templates:
                rule = self._process_template(template, context)
                if rule:
                    generated_rules.append(rule)
            
            # Save generated rules
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"generated_rules_{timestamp}")
            os.makedirs(output_path, exist_ok=True)
            
            for rule in generated_rules:
                self._save_rule(rule, output_path)
            
            return output_path
        except Exception as e:
            self.logger.error(f"Error generating project rules: {str(e)}")
            return ""

    def _update_existing_rules(self, context: Dict[str, any]) -> str:
        """Update existing rules based on new context"""
        try:
            rules_dir = context.get("rules_dir", ".cursor/rules")
            if not os.path.exists(rules_dir):
                self.logger.error(f"Rules directory not found: {rules_dir}")
                return ""

            # Load existing rules
            existing_rules = self._load_existing_rules(rules_dir)
            
            # Update rules
            updated_rules = []
            for rule in existing_rules:
                updated_rule = self._update_rule(rule, context)
                if updated_rule:
                    updated_rules.append(updated_rule)
            
            # Save updated rules
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"updated_rules_{timestamp}")
            os.makedirs(output_path, exist_ok=True)
            
            for rule in updated_rules:
                self._save_rule(rule, output_path)
            
            return output_path
        except Exception as e:
            self.logger.error(f"Error updating rules: {str(e)}")
            return ""

    def _generate_from_codebase(self, context: Dict[str, any]) -> str:
        """Generate rules by analyzing the codebase"""
        try:
            codebase_path = context.get("codebase_path", ".")
            
            # Analyze codebase
            analysis = self._analyze_codebase(codebase_path)
            
            # Generate rules based on analysis
            rules = self._generate_rules_from_analysis(analysis)
            
            # Save generated rules
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"codebase_rules_{timestamp}")
            os.makedirs(output_path, exist_ok=True)
            
            for rule in rules:
                self._save_rule(rule, output_path)
            
            return output_path
        except Exception as e:
            self.logger.error(f"Error generating rules from codebase: {str(e)}")
            return ""

    def _import_external_rules(self, context: Dict[str, any]) -> str:
        """Import and adapt external rules"""
        try:
            source_path = context.get("source_path")
            if not source_path or not os.path.exists(source_path):
                self.logger.error(f"Invalid source path: {source_path}")
                return ""

            # Import rules
            imported_rules = self._load_external_rules(source_path)
            
            # Adapt rules to current project
            adapted_rules = []
            for rule in imported_rules:
                adapted_rule = self._adapt_rule(rule, context)
                if adapted_rule:
                    adapted_rules.append(adapted_rule)
            
            # Save adapted rules
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.output_dir, f"imported_rules_{timestamp}")
            os.makedirs(output_path, exist_ok=True)
            
            for rule in adapted_rules:
                self._save_rule(rule, output_path)
            
            return output_path
        except Exception as e:
            self.logger.error(f"Error importing external rules: {str(e)}")
            return ""

    def _load_templates(self, project_type: str, framework: str, language: str) -> List[Dict]:
        """Load appropriate rule templates based on project characteristics"""
        templates = []
        template_paths = [
            os.path.join(self.templates_dir, f"{project_type}.json"),
            os.path.join(self.templates_dir, f"{framework}.json"),
            os.path.join(self.templates_dir, f"{language}.json")
        ]
        
        for path in template_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        templates.extend(json.load(f))
                except Exception as e:
                    self.logger.error(f"Error loading template {path}: {str(e)}")
        
        return templates

    def _process_template(self, template: Dict, context: Dict[str, any]) -> Optional[Dict]:
        """Process a rule template with context"""
        try:
            rule = template.copy()
            
            # Replace variables in template
            for key, value in rule.items():
                if isinstance(value, str):
                    for ctx_key, ctx_value in context.items():
                        placeholder = f"${{{ctx_key}}}"
                        if placeholder in value:
                            rule[key] = value.replace(placeholder, str(ctx_value))
            
            return rule
        except Exception as e:
            self.logger.error(f"Error processing template: {str(e)}")
            return None

    def _save_rule(self, rule: Dict, output_path: str):
        """Save a generated rule"""
        try:
            rule_name = rule.get("name", "unnamed_rule").lower().replace(" ", "_")
            file_path = os.path.join(output_path, f"{rule_name}.mdc")
            
            # Convert rule to MDC format
            mdc_content = self._convert_to_mdc(rule)
            
            with open(file_path, 'w') as f:
                f.write(mdc_content)
            
            self.logger.info(f"Saved rule: {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving rule: {str(e)}")

    def _convert_to_mdc(self, rule: Dict) -> str:
        """Convert a rule dictionary to MDC format"""
        try:
            # Extract metadata
            metadata = {
                "description": rule.get("description", ""),
                "globs": rule.get("globs", []),
                "alwaysApply": rule.get("alwaysApply", False)
            }
            
            # Format metadata section
            mdc = "---\n"
            for key, value in metadata.items():
                if isinstance(value, list):
                    mdc += f"{key}: {json.dumps(value)}\n"
                else:
                    mdc += f"{key}: {value}\n"
            mdc += "---\n\n"
            
            # Add content
            if "content" in rule:
                mdc += rule["content"]
            
            return mdc
        except Exception as e:
            self.logger.error(f"Error converting to MDC: {str(e)}")
            return ""

    def _analyze_codebase(self, path: str) -> Dict:
        """Analyze codebase for rule generation"""
        analysis = {
            "languages": set(),
            "frameworks": set(),
            "patterns": set(),
            "dependencies": set()
        }
        
        try:
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Analyze file type and content
                    self._analyze_file(file_path, analysis)
        except Exception as e:
            self.logger.error(f"Error analyzing codebase: {str(e)}")
        
        return {k: list(v) for k, v in analysis.items()}

    def _analyze_file(self, file_path: str, analysis: Dict):
        """Analyze a single file"""
        try:
            ext = Path(file_path).suffix.lower()
            
            # Detect language
            if ext in ['.py']:
                analysis['languages'].add('python')
            elif ext in ['.js', '.jsx', '.ts', '.tsx']:
                analysis['languages'].add('javascript')
                if ext in ['.tsx', '.jsx']:
                    analysis['frameworks'].add('react')
            
            # Analyze content for patterns and dependencies
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self._analyze_content(content, analysis)
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {str(e)}")

    def _analyze_content(self, content: str, analysis: Dict):
        """Analyze file content for patterns and dependencies"""
        # Add pattern detection logic here
        pass

    def _generate_rules_from_analysis(self, analysis: Dict) -> List[Dict]:
        """Generate rules based on codebase analysis"""
        rules = []
        
        try:
            # Generate language-specific rules
            for language in analysis['languages']:
                template_path = os.path.join(self.templates_dir, f"{language}.json")
                if os.path.exists(template_path):
                    with open(template_path, 'r') as f:
                        rules.extend(json.load(f))
            
            # Generate framework-specific rules
            for framework in analysis['frameworks']:
                template_path = os.path.join(self.templates_dir, f"{framework}.json")
                if os.path.exists(template_path):
                    with open(template_path, 'r') as f:
                        rules.extend(json.load(f))
        except Exception as e:
            self.logger.error(f"Error generating rules from analysis: {str(e)}")
        
        return rules 