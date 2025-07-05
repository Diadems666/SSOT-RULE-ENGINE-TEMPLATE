#!/usr/bin/env python3
"""
SSOT Analytics Command Line Interface

Provides easy access to analytics and dashboard functionality.
"""

import sys
import os
from pathlib import Path
import argparse
import json
from datetime import datetime
import webbrowser

# Add the analytics directory to the path
sys.path.append(str(Path(__file__).parent))

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='SSOT-RULE-ENGINE-TEMPLATE Analytics CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py analyze              # Run full analytics analysis
  python cli.py dashboard            # Start analytics dashboard
  python cli.py dashboard --port 8080  # Start dashboard on specific port
  python cli.py quick                # Quick health check
  python cli.py export --format json  # Export analytics data

Commands:
  analyze    - Run comprehensive analytics analysis
  dashboard  - Start web-based analytics dashboard
  quick      - Quick health check
  export     - Export analytics data to file
  help       - Show this help message
"""
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Run comprehensive analytics analysis')
    analyze_parser.add_argument('--output', '-o', choices=['json', 'markdown', 'both'], 
                               default='both', help='Output format')
    analyze_parser.add_argument('--verbose', '-v', action='store_true', 
                               help='Verbose output')
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Start analytics dashboard')
    dashboard_parser.add_argument('--port', '-p', type=int, help='Port for dashboard server')
    dashboard_parser.add_argument('--no-browser', action='store_true', 
                                 help='Don\'t auto-open browser')
    dashboard_parser.add_argument('--generate-only', action='store_true',
                                 help='Generate dashboard files without starting server')
    
    # Quick command
    quick_parser = subparsers.add_parser('quick', help='Quick health check')
    quick_parser.add_argument('--format', choices=['text', 'json'], default='text',
                             help='Output format')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export analytics data')
    export_parser.add_argument('--format', choices=['json', 'csv', 'markdown'], 
                              default='json', help='Export format')
    export_parser.add_argument('--output', '-o', help='Output file path')
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show help message')
    
    args = parser.parse_args()
    
    if not args.command or args.command == 'help':
        parser.print_help()
        return 0
    
    try:
        if args.command == 'analyze':
            return run_analyze(args)
        elif args.command == 'dashboard':
            return run_dashboard(args)
        elif args.command == 'quick':
            return run_quick(args)
        elif args.command == 'export':
            return run_export(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            parser.print_help()
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        if hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()
        return 1

def run_analyze(args):
    """Run comprehensive analytics analysis"""
    print("🔍 Starting comprehensive analytics analysis...")
    
    try:
        from analytics_engine import SSOTAnalyticsEngine
        engine = SSOTAnalyticsEngine()
        metrics = engine.generate_comprehensive_report()
        
        print("\n" + "="*60)
        print("📊 ANALYTICS SUMMARY")
        print("="*60)
        print(f"Project: {metrics.project_name}")
        print(f"Health Score: {metrics.ssot_health_score}/100")
        print(f"Total Files: {metrics.total_files}")
        print(f"Total Lines: {metrics.total_lines:,}")
        print(f"Active Rules: {metrics.active_rules}")
        print(f"KG Entities: {metrics.knowledge_graph_entities}")
        print(f"Development Velocity: {metrics.development_velocity:.1f}/10")
        
        # Show health indicators
        print("\n🏥 HEALTH INDICATORS")
        print("-" * 40)
        health = metrics.health_indicators
        print(f"SSOT System: {health['ssot']['completeness'].title()} ({health['ssot']['consistency'].title()} consistency)")
        print(f"MCP Servers: {health['mcp']['server_status'].replace('_', ' ').title()} ({health['mcp']['memory_status'].title()} memory)")
        print(f"Rule Engine: {health['rules']['coverage'].title()} coverage ({health['rules']['effectiveness'].title()} effectiveness)")
        
        print(f"\n📅 Last Activity: {metrics.last_activity}")
        print("="*60)
        
        if args.verbose:
            # Show detailed analysis
            report_path = Path(".cursor/CORE/ANALYTICS/analytics_report.json")
            if report_path.exists():
                print("\n📋 DETAILED ANALYSIS")
                print("-" * 40)
                with open(report_path, 'r') as f:
                    detailed_data = json.load(f)
                    
                recommendations = detailed_data.get('detailed_analytics', {}).get('recommendations', [])
                if recommendations:
                    print("\n💡 RECOMMENDATIONS:")
                    for i, rec in enumerate(recommendations, 1):
                        print(f"  {i}. {rec}")
        
        return 0
        
    except ImportError:
        print("❌ Analytics engine not available. Please ensure all dependencies are installed.")
        return 1
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return 1

def run_dashboard(args):
    """Start analytics dashboard"""
    print("🚀 Starting analytics dashboard...")
    
    try:
        from dashboard import AnalyticsDashboard
        dashboard = AnalyticsDashboard()
        
        if args.port:
            dashboard.port = args.port
            
        if args.generate_only:
            dashboard_file = dashboard.generate_dashboard()
            print(f"📊 Dashboard generated: {dashboard_file}")
            return 0
        else:
            dashboard.start_server(auto_open=not args.no_browser)
            return 0
            
    except ImportError:
        print("❌ Dashboard not available. Please ensure all dependencies are installed.")
        return 1
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return 1

def run_quick(args):
    """Run quick health check"""
    print("⚡ Running quick health check...")
    
    try:
        # Basic project structure check
        project_root = Path(".")
        cursor_path = project_root / ".cursor"
        core_path = cursor_path / "CORE"
        ssot_path = core_path / "SSOT"
        
        if not cursor_path.exists():
            print("❌ .cursor directory not found")
            return 1
            
        if not ssot_path.exists():
            print("❌ SSOT directory not found")
            return 1
        
        # Check SSOT files
        ssot_files = ['.ENGINE', '.INIT', '.CONTEXT', '.FACTS', '.MEMORY', 
                     '.HISTORY', '.CONTINUE', '.PROGRESS']
        
        existing_files = 0
        for file_name in ssot_files:
            if (ssot_path / file_name).exists():
                existing_files += 1
        
        # Check MCP configuration
        mcp_config = cursor_path / "mcp.json"
        mcp_configured = mcp_config.exists()
        
        # Check rules
        rules_path = cursor_path / "rules"
        rule_count = len(list(rules_path.glob("*.mdc"))) if rules_path.exists() else 0
        
        # Calculate quick health score
        ssot_score = (existing_files / len(ssot_files)) * 30
        mcp_score = 25 if mcp_configured else 0
        rules_score = min(25, rule_count * 5)
        general_score = 20  # Base score
        
        total_score = ssot_score + mcp_score + rules_score + general_score
        
        if args.format == 'json':
            result = {
                'timestamp': datetime.now().isoformat(),
                'health_score': round(total_score, 1),
                'ssot_files': f"{existing_files}/{len(ssot_files)}",
                'mcp_configured': mcp_configured,
                'active_rules': rule_count,
                'status': 'excellent' if total_score >= 80 else 'good' if total_score >= 60 else 'needs_attention'
            }
            print(json.dumps(result, indent=2))
        else:
            print("\n" + "="*50)
            print("⚡ QUICK HEALTH CHECK")
            print("="*50)
            print(f"Overall Health: {total_score:.1f}/100")
            print(f"SSOT Files: {existing_files}/{len(ssot_files)} ({'✅' if existing_files >= 6 else '⚠️'})")
            print(f"MCP Config: {'✅ Configured' if mcp_configured else '❌ Not configured'}")
            print(f"Active Rules: {rule_count} ({'✅' if rule_count > 0 else '⚠️'})")
            
            if total_score >= 80:
                print("\n🎉 System is in excellent condition!")
            elif total_score >= 60:
                print("\n👍 System is in good condition")
            else:
                print("\n⚠️ System needs attention")
                
            print("\n💡 For detailed analysis, run: python cli.py analyze")
            print("="*50)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error running quick check: {e}")
        return 1

def run_export(args):
    """Export analytics data"""
    print("📤 Exporting analytics data...")
    
    try:
        # Determine output file
        if args.output:
            output_path = Path(args.output)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(f"analytics_export_{timestamp}.{args.format}")
        
        # Try to get full analytics data
        try:
            from analytics_engine import SSOTAnalyticsEngine
            engine = SSOTAnalyticsEngine()
            metrics = engine.generate_comprehensive_report()
            
            # Load detailed report
            report_path = Path(".cursor/CORE/ANALYTICS/analytics_report.json")
            if report_path.exists():
                with open(report_path, 'r') as f:
                    detailed_data = json.load(f)
            else:
                detailed_data = {}
                
        except ImportError:
            print("⚠️ Full analytics not available, using basic data")
            detailed_data = {
                'timestamp': datetime.now().isoformat(),
                'basic_export': True,
                'message': 'Full analytics engine not available'
            }
        
        # Export based on format
        if args.format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(detailed_data, f, indent=2, default=str)
                
        elif args.format == 'csv':
            import csv
            # Create CSV with basic metrics
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Metric', 'Value'])
                
                if 'summary' in detailed_data:
                    summary = detailed_data['summary']
                    writer.writerow(['Project Name', summary.get('project_name', 'Unknown')])
                    writer.writerow(['Health Score', summary.get('ssot_health_score', 0)])
                    writer.writerow(['Total Files', summary.get('total_files', 0)])
                    writer.writerow(['Active Rules', summary.get('active_rules', 0)])
                    writer.writerow(['KG Entities', summary.get('knowledge_graph_entities', 0)])
                
        elif args.format == 'markdown':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# SSOT Analytics Export\n\n")
                f.write(f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if 'summary' in detailed_data:
                    summary = detailed_data['summary']
                    f.write("## Summary\n\n")
                    f.write(f"- **Project:** {summary.get('project_name', 'Unknown')}\n")
                    f.write(f"- **Health Score:** {summary.get('ssot_health_score', 0)}/100\n")
                    f.write(f"- **Total Files:** {summary.get('total_files', 0):,}\n")
                    f.write(f"- **Active Rules:** {summary.get('active_rules', 0)}\n")
                    f.write(f"- **Knowledge Graph Entities:** {summary.get('knowledge_graph_entities', 0)}\n\n")
                
                if 'detailed_analytics' in detailed_data:
                    recommendations = detailed_data['detailed_analytics'].get('recommendations', [])
                    if recommendations:
                        f.write("## Recommendations\n\n")
                        for i, rec in enumerate(recommendations, 1):
                            f.write(f"{i}. {rec}\n")
        
        print(f"✅ Analytics data exported to: {output_path}")
        return 0
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 