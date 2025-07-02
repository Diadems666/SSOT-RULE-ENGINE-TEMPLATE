#!/usr/bin/env python3
"""
SSOT-RULE-ENGINE-TEMPLATE Analytics Engine

Comprehensive analytics and metrics system for tracking project health,
system performance, and development insights.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import re
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import statistics

@dataclass
class ProjectMetrics:
    """Core project metrics container"""
    project_name: str
    analysis_timestamp: str
    total_files: int
    total_lines: int
    ssot_health_score: float
    mcp_servers_status: Dict[str, str]
    knowledge_graph_entities: int
    active_rules: int
    development_velocity: float
    last_activity: str
    health_indicators: Dict[str, Any]

@dataclass
class SSOTAnalytics:
    """SSOT system analytics"""
    files_analyzed: int
    total_content_size: int
    last_updates: Dict[str, str]
    content_distribution: Dict[str, int]
    state_completeness: float
    consistency_score: float
    
@dataclass
class MCPAnalytics:
    """MCP server analytics"""
    servers_configured: int
    servers_ready: int
    knowledge_graph_size: int
    memory_usage_mb: float
    server_versions: Dict[str, str]
    performance_metrics: Dict[str, Any]

@dataclass
class RuleEngineAnalytics:
    """Rule Engine analytics"""
    total_rules: int
    active_rules: int
    staged_rules: int
    rule_types: Dict[str, int]
    coverage_percentage: float
    effectiveness_score: float

class SSOTAnalyticsEngine:
    """Main analytics engine for SSOT-RULE-ENGINE-TEMPLATE"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.cursor_path = self.project_root / ".cursor"
        self.core_path = self.cursor_path / "CORE"
        self.ssot_path = self.core_path / "SSOT"
        self.mcp_path = self.core_path / "MCP"
        self.rules_path = self.cursor_path / "rules"
        self.analytics_path = self.core_path / "ANALYTICS"
        
        # Ensure analytics directory exists
        self.analytics_path.mkdir(exist_ok=True)
        
    def generate_comprehensive_report(self) -> ProjectMetrics:
        """Generate comprehensive project analytics report"""
        print("🔍 Starting comprehensive analytics analysis...")
        
        # Collect all metrics
        ssot_analytics = self._analyze_ssot_system()
        mcp_analytics = self._analyze_mcp_system()
        rule_analytics = self._analyze_rule_engine()
        project_analytics = self._analyze_project_structure()
        health_score = self._calculate_project_health_score(
            ssot_analytics, mcp_analytics, rule_analytics
        )
        
        # Create comprehensive metrics
        metrics = ProjectMetrics(
            project_name=self._get_project_name(),
            analysis_timestamp=datetime.now().isoformat(),
            total_files=project_analytics['total_files'],
            total_lines=project_analytics['total_lines'],
            ssot_health_score=health_score,
            mcp_servers_status=mcp_analytics.performance_metrics.get('status', {}),
            knowledge_graph_entities=mcp_analytics.knowledge_graph_size,
            active_rules=rule_analytics.active_rules,
            development_velocity=self._calculate_development_velocity(),
            last_activity=self._get_last_activity(),
            health_indicators=self._generate_health_indicators(
                ssot_analytics, mcp_analytics, rule_analytics
            )
        )
        
        # Save detailed analytics
        self._save_analytics_report(metrics, ssot_analytics, mcp_analytics, rule_analytics)
        
        return metrics
    
    def _analyze_ssot_system(self) -> SSOTAnalytics:
        """Analyze SSOT system health and metrics"""
        print("📋 Analyzing SSOT system...")
        
        ssot_files = ['.ENGINE', '.INIT', '.CONTEXT', '.FACTS', '.MEMORY', 
                     '.HISTORY', '.CONTINUE', '.PROGRESS']
        
        files_analyzed = 0
        total_size = 0
        last_updates = {}
        content_distribution = {}
        
        for file_name in ssot_files:
            file_path = self.ssot_path / file_name
            if file_path.exists():
                files_analyzed += 1
                stat = file_path.stat()
                size = stat.st_size
                total_size += size
                content_distribution[file_name] = size
                last_updates[file_name] = datetime.fromtimestamp(stat.st_mtime).isoformat()
        
        # Calculate completeness and consistency
        completeness = files_analyzed / len(ssot_files)
        consistency_score = self._calculate_ssot_consistency()
        
        return SSOTAnalytics(
            files_analyzed=files_analyzed,
            total_content_size=total_size,
            last_updates=last_updates,
            content_distribution=content_distribution,
            state_completeness=completeness,
            consistency_score=consistency_score
        )
    
    def _analyze_mcp_system(self) -> MCPAnalytics:
        """Analyze MCP server configuration and status"""
        print("🚀 Analyzing MCP system...")
        
        mcp_config_path = self.cursor_path / "mcp.json"
        servers_configured = 0
        servers_ready = 0
        server_versions = {}
        
        if mcp_config_path.exists():
            try:
                with open(mcp_config_path, 'r') as f:
                    config = json.load(f)
                    servers = config.get('mcpServers', {})
                    servers_configured = len(servers)
                    
                    # Check server readiness
                    for server_name, server_config in servers.items():
                        server_path = self.mcp_path / server_name
                        if server_path.exists():
                            # Check if compiled
                            dist_path = server_path / "dist"
                            package_path = server_path / "package.json"
                            
                            if dist_path.exists() and package_path.exists():
                                servers_ready += 1
                                # Get version
                                try:
                                    with open(package_path, 'r') as pf:
                                        package_info = json.load(pf)
                                        server_versions[server_name] = package_info.get('version', 'unknown')
                                except:
                                    server_versions[server_name] = 'unknown'
            except Exception as e:
                print(f"⚠️ Error analyzing MCP config: {e}")
        
        # Analyze Knowledge Graph size
        kg_size = self._get_knowledge_graph_size()
        memory_usage = self._estimate_memory_usage()
        
        performance_metrics = {
            'status': {server: 'ready' if server in server_versions else 'not_ready' 
                      for server in ['knowledge-graph', 'sequentialthinking', 'filesystem']},
            'readiness_ratio': servers_ready / max(servers_configured, 1),
            'config_completeness': 1.0 if mcp_config_path.exists() else 0.0
        }
        
        return MCPAnalytics(
            servers_configured=servers_configured,
            servers_ready=servers_ready,
            knowledge_graph_size=kg_size,
            memory_usage_mb=memory_usage,
            server_versions=server_versions,
            performance_metrics=performance_metrics
        )
    
    def _analyze_rule_engine(self) -> RuleEngineAnalytics:
        """Analyze Rule Engine effectiveness and coverage"""
        print("🎯 Analyzing Rule Engine...")
        
        total_rules = 0
        active_rules = 0
        staged_rules = 0
        rule_types = defaultdict(int)
        
        # Analyze active rules
        if self.rules_path.exists():
            for rule_file in self.rules_path.glob("*.mdc"):
                total_rules += 1
                active_rules += 1
                
                # Analyze rule type
                try:
                    with open(rule_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Parse frontmatter
                        if content.startswith('---'):
                            frontmatter_end = content.find('---', 3)
                            if frontmatter_end > 0:
                                frontmatter = content[3:frontmatter_end]
                                if 'alwaysApply: true' in frontmatter:
                                    rule_types['global'] += 1
                                else:
                                    rule_types['contextual'] += 1
                except Exception as e:
                    print(f"⚠️ Error analyzing rule {rule_file}: {e}")
        
        # Analyze staged rules
        rule_engine_path = self.core_path / "RULE-ENGINE"
        if rule_engine_path.exists():
            staged_rules = len(list(rule_engine_path.glob("*.mdc")))
            total_rules += staged_rules
        
        # Calculate coverage and effectiveness
        project_files = len(list(self.project_root.rglob("*.*")))
        coverage_percentage = min(100.0, (active_rules / max(project_files / 10, 1)) * 100)
        effectiveness_score = self._calculate_rule_effectiveness()
        
        return RuleEngineAnalytics(
            total_rules=total_rules,
            active_rules=active_rules,
            staged_rules=staged_rules,
            rule_types=dict(rule_types),
            coverage_percentage=coverage_percentage,
            effectiveness_score=effectiveness_score
        )
    
    def _analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze overall project structure"""
        print("📁 Analyzing project structure...")
        
        total_files = 0
        total_lines = 0
        file_types = defaultdict(int)
        
        # Skip certain directories
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.pytest_cache', 'dist'}
        
        for file_path in self.project_root.rglob("*.*"):
            # Skip if in excluded directory
            if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                continue
                
            total_files += 1
            suffix = file_path.suffix.lower()
            file_types[suffix] += 1
            
            # Count lines for text files
            try:
                if suffix in {'.py', '.js', '.ts', '.md', '.json', '.mdc', '.txt', '.yml', '.yaml'}:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        total_lines += sum(1 for _ in f)
            except:
                pass
        
        return {
            'total_files': total_files,
            'total_lines': total_lines,
            'file_types': dict(file_types),
            'complexity_score': min(100, total_files / 10)  # Simple complexity metric
        }
    
    def _calculate_project_health_score(self, ssot: SSOTAnalytics, 
                                      mcp: MCPAnalytics, rules: RuleEngineAnalytics) -> float:
        """Calculate overall project health score (0-100)"""
        
        # SSOT health (30%)
        ssot_score = (ssot.state_completeness * 0.5 + ssot.consistency_score * 0.5) * 30
        
        # MCP health (30%)
        mcp_score = (mcp.performance_metrics.get('readiness_ratio', 0) * 0.7 + 
                    mcp.performance_metrics.get('config_completeness', 0) * 0.3) * 30
        
        # Rule Engine health (25%)
        rule_score = (rules.effectiveness_score * 0.6 + 
                     min(rules.coverage_percentage / 100, 1.0) * 0.4) * 25
        
        # General project health (15%)
        general_score = min(15, self._get_activity_score())
        
        return round(ssot_score + mcp_score + rule_score + general_score, 2)
    
    def _calculate_development_velocity(self) -> float:
        """Calculate development velocity based on recent activity"""
        history_path = self.ssot_path / ".HISTORY"
        if not history_path.exists():
            return 0.0
        
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Count entries in last 30 days
            recent_entries = 0
            lines = content.split('\n')
            for line in lines:
                if line.startswith('## ') and any(str(year) in line for year in range(2020, 2030)):
                    recent_entries += 1
            
            # Simple velocity metric
            return min(10.0, recent_entries / 10)
        except:
            return 0.0
    
    def _get_last_activity(self) -> str:
        """Get timestamp of last significant activity"""
        try:
            history_path = self.ssot_path / ".HISTORY"
            if history_path.exists():
                stat = history_path.stat()
                return datetime.fromtimestamp(stat.st_mtime).isoformat()
        except:
            pass
        return datetime.now().isoformat()
    
    def _generate_health_indicators(self, ssot: SSOTAnalytics, 
                                  mcp: MCPAnalytics, rules: RuleEngineAnalytics) -> Dict[str, Any]:
        """Generate detailed health indicators"""
        indicators = {}
        
        # SSOT indicators
        indicators['ssot'] = {
            'completeness': 'excellent' if ssot.state_completeness > 0.8 else 'good' if ssot.state_completeness > 0.6 else 'needs_attention',
            'consistency': 'high' if ssot.consistency_score > 0.8 else 'medium' if ssot.consistency_score > 0.6 else 'low',
            'last_update': max(ssot.last_updates.values()) if ssot.last_updates else 'unknown'
        }
        
        # MCP indicators  
        indicators['mcp'] = {
            'server_status': 'all_ready' if mcp.servers_ready == mcp.servers_configured else 'partial' if mcp.servers_ready > 0 else 'none',
            'knowledge_graph': 'populated' if mcp.knowledge_graph_size > 0 else 'empty',
            'memory_status': 'optimal' if mcp.memory_usage_mb < 100 else 'high' if mcp.memory_usage_mb < 500 else 'critical'
        }
        
        # Rule Engine indicators
        indicators['rules'] = {
            'coverage': 'excellent' if rules.coverage_percentage > 75 else 'good' if rules.coverage_percentage > 50 else 'needs_improvement',
            'effectiveness': 'high' if rules.effectiveness_score > 0.8 else 'medium' if rules.effectiveness_score > 0.6 else 'low',
            'staging_queue': rules.staged_rules
        }
        
        return indicators
    
    def _calculate_ssot_consistency(self) -> float:
        """Calculate SSOT internal consistency score"""
        # Simple consistency check - could be enhanced
        essential_files = ['.CONTEXT', '.FACTS', '.MEMORY']
        existing_files = sum(1 for f in essential_files if (self.ssot_path / f).exists())
        return existing_files / len(essential_files)
    
    def _get_knowledge_graph_size(self) -> int:
        """Get Knowledge Graph entity count"""
        memory_path = self.core_path / "MEMORY" / "memory.jsonl"
        if not memory_path.exists():
            return 0
        
        try:
            with open(memory_path, 'r') as f:
                lines = f.readlines()
                return len(lines)
        except:
            return 0
    
    def _estimate_memory_usage(self) -> float:
        """Estimate memory usage in MB"""
        total_size = 0
        memory_path = self.core_path / "MEMORY"
        if memory_path.exists():
            for file_path in memory_path.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        return round(total_size / (1024 * 1024), 2)
    
    def _calculate_rule_effectiveness(self) -> float:
        """Calculate rule effectiveness score"""
        # Placeholder - could be enhanced with actual usage metrics
        if self.rules_path.exists():
            rule_count = len(list(self.rules_path.glob("*.mdc")))
            return min(1.0, rule_count / 5)  # Assume 5 rules is optimal
        return 0.0
    
    def _get_activity_score(self) -> float:
        """Get activity score based on recent modifications"""
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        
        recent_activity = 0
        for file_path in self.cursor_path.rglob("*"):
            if file_path.is_file():
                try:
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime > week_ago:
                        recent_activity += 1
                except:
                    pass
        
        return min(15.0, recent_activity)
    
    def _get_project_name(self) -> str:
        """Get project name from context or directory"""
        context_path = self.ssot_path / ".CONTEXT"
        if context_path.exists():
            try:
                with open(context_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract project name from first line or title
                    lines = content.split('\n')
                    for line in lines:
                        if line.startswith('#') and 'project' in line.lower():
                            return line.strip('# ').split(' - ')[0]
            except:
                pass
        
        return self.project_root.name
    
    def _save_analytics_report(self, metrics: ProjectMetrics, ssot: SSOTAnalytics, 
                             mcp: MCPAnalytics, rules: RuleEngineAnalytics):
        """Save comprehensive analytics report"""
        
        # Create detailed report
        report = {
            'summary': asdict(metrics),
            'detailed_analytics': {
                'ssot_system': asdict(ssot),
                'mcp_system': asdict(mcp),
                'rule_engine': asdict(rules),
                'recommendations': self._generate_recommendations(ssot, mcp, rules)
            },
            'generated_at': datetime.now().isoformat(),
            'report_version': '1.0'
        }
        
        # Save JSON report
        report_path = self.analytics_path / "analytics_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Save human-readable summary
        self._save_readable_summary(metrics, report_path.with_suffix('.md'))
        
        print(f"📊 Analytics report saved to: {report_path}")
        print(f"📖 Human-readable summary: {report_path.with_suffix('.md')}")
    
    def _generate_recommendations(self, ssot: SSOTAnalytics, 
                                mcp: MCPAnalytics, rules: RuleEngineAnalytics) -> List[str]:
        """Generate actionable recommendations based on analytics"""
        recommendations = []
        
        # SSOT recommendations
        if ssot.state_completeness < 0.8:
            recommendations.append("Complete missing SSOT files to improve state tracking")
        
        if ssot.consistency_score < 0.7:
            recommendations.append("Review SSOT files for consistency and update outdated information")
        
        # MCP recommendations
        if mcp.servers_ready < mcp.servers_configured:
            recommendations.append("Install and compile MCP servers using '!!-INSTALL-MCP-!!'")
        
        if mcp.knowledge_graph_size == 0:
            recommendations.append("Build Knowledge Graph using '!!-BUILD-KG-!!' to enable persistent memory")
        
        # Rule Engine recommendations
        if rules.coverage_percentage < 50:
            recommendations.append("Add more rules to improve project coverage and AI behavior consistency")
        
        if rules.staged_rules > 0:
            recommendations.append(f"Review and integrate {rules.staged_rules} staged rules from RULE-ENGINE/")
        
        if rules.effectiveness_score < 0.6:
            recommendations.append("Review rule effectiveness and consider updating rule patterns")
        
        return recommendations
    
    def _save_readable_summary(self, metrics: ProjectMetrics, output_path: Path):
        """Save human-readable summary report"""
        
        summary = f"""# SSOT-RULE-ENGINE-TEMPLATE Analytics Report

## Project Overview
- **Project**: {metrics.project_name}
- **Analysis Date**: {metrics.analysis_timestamp}
- **Overall Health Score**: {metrics.ssot_health_score}/100

## Key Metrics
- **Total Files**: {metrics.total_files}
- **Total Lines of Code**: {metrics.total_lines:,}
- **Active Rules**: {metrics.active_rules}
- **Knowledge Graph Entities**: {metrics.knowledge_graph_entities}
- **Development Velocity**: {metrics.development_velocity}/10
- **Last Activity**: {metrics.last_activity}

## System Health Status

### SSOT System
- **Status**: {metrics.health_indicators['ssot']['completeness'].title()}
- **Consistency**: {metrics.health_indicators['ssot']['consistency'].title()}
- **Last Update**: {metrics.health_indicators['ssot']['last_update']}

### MCP Servers
- **Server Status**: {metrics.health_indicators['mcp']['server_status'].replace('_', ' ').title()}
- **Knowledge Graph**: {metrics.health_indicators['mcp']['knowledge_graph'].title()}
- **Memory Usage**: {metrics.health_indicators['mcp']['memory_status'].title()}

### Rule Engine
- **Coverage**: {metrics.health_indicators['rules']['coverage'].title()}
- **Effectiveness**: {metrics.health_indicators['rules']['effectiveness'].title()}
- **Staged Rules**: {metrics.health_indicators['rules']['staging_queue']}

## Health Score Breakdown
- **SSOT Health**: Contributing 30% to overall score
- **MCP Health**: Contributing 30% to overall score  
- **Rule Engine**: Contributing 25% to overall score
- **General Activity**: Contributing 15% to overall score

## Quick Actions
To improve your project health score:
1. Use `!!-UPDATE-SSOT-!!` to sync recent changes
2. Use `!!-INSTALL-MCP-!!` if MCP servers need setup
3. Use `!!-BUILD-KG-!!` to populate the Knowledge Graph
4. Review and integrate staged rules from RULE-ENGINE/

---
*Report generated by SSOT-RULE-ENGINE-TEMPLATE Analytics Engine v1.0*
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)

def main():
    """Main entry point for analytics engine"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SSOT-RULE-ENGINE-TEMPLATE Analytics Engine')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--output-format', choices=['json', 'markdown', 'both'], default='both',
                       help='Output format for analytics report')
    
    args = parser.parse_args()
    
    try:
        engine = SSOTAnalyticsEngine(args.project_root)
        metrics = engine.generate_comprehensive_report()
        
        print("\n" + "="*60)
        print("📊 ANALYTICS SUMMARY")
        print("="*60)
        print(f"Project: {metrics.project_name}")
        print(f"Health Score: {metrics.ssot_health_score}/100")
        print(f"Total Files: {metrics.total_files}")
        print(f"Active Rules: {metrics.active_rules}")
        print(f"KG Entities: {metrics.knowledge_graph_entities}")
        print(f"Last Activity: {metrics.last_activity}")
        print("="*60)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating analytics: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 