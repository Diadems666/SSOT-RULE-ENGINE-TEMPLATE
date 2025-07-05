#!/usr/bin/env python3
"""
SSOT-RULE-ENGINE Startup Script
Automatically launches analytics dashboard and initializes system monitoring
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import json
import os

def find_available_port(start_port=8080, max_attempts=10):
    """Find an available port for the dashboard"""
    import socket
    
    for i in range(max_attempts):
        port = start_port + i
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    return start_port  # Fallback to default

def ensure_analytics_directory():
    """Ensure analytics directory exists with required files"""
    analytics_dir = Path('.cursor/CORE/ANALYTICS')
    analytics_dir.mkdir(parents=True, exist_ok=True)
    
    # Ensure analytics engine exists
    engine_file = analytics_dir / 'analytics_engine.py'
    if not engine_file.exists():
        print("⚠️ Analytics engine not found. Please ensure analytics_engine.py exists.")
        return False
    
    return True

def create_user_rules_template():
    """Create or update USER-RULES template file"""
    analytics_dir = Path('.cursor/CORE/ANALYTICS')
    user_rules_file = analytics_dir / 'USER-RULES-TEMPLATE.md'
    
    template_content = """# SSOT-RULE-ENGINE USER-RULES Template
# Copy this content to your Cursor AI settings for optimal integration

# Core AI Behavior & Workflow Management
- As an AI assistant within the Cursor AI IDE for default_developer, provide efficient, accurate, and contextually relevant assistance, leveraging all available tools including the Knowledge Graph Memory Server.
- Recognize and strictly follow directives within the project's core system files (e.g., in ./.cursor/CORE/SSOT/).
- Understand that specific triggers initiate system setup workflows, and the *detailed instructions* for ALL setup workflows ('INIT', 'ADD', 'INSTALL MCP', 'BUILD KG') are centralized in ./.cursor/CORE/SSOT/.ENGINE.
- When encountering ANY of the following triggers ('!!-INIT-.ENGINE-!!', '!!-ADD-.ENGINE-!!', '!!-INSTALL-MCP-!!', '!!-BUILD-KG-!!'), immediately consult and execute the relevant steps defined within ./.cursor/CORE/SSOT/.ENGINE for the specific trigger identified.

# Analytics System Integration
- When projects are first initialized (!!-INIT-.ENGINE-!! or !!-ADD-.ENGINE-!!), automatically launch the analytics dashboard using !!-LAUNCH-DASHBOARD-!!
- Use !!-ANALYZE-PROJECT-!! for comprehensive project analysis and health scoring
- Use !!-VIEW-DASHBOARD-!! to launch the interactive analytics dashboard
- Use !!-HEALTH-CHECK-!! for quick project health assessment
- Monitor project health metrics and provide intelligent recommendations for optimization

# Advanced Analytics Features
- Real-time project health monitoring with 0-100 scoring system
- Interactive dashboard with visual charts and system status indicators
- Intelligent recommendations engine for development optimization
- Rule engine effectiveness tracking and visual management interface
- SSOT system analytics and completeness monitoring
- MCP server performance metrics and usage analytics

# Visual Rule Engine Management
- Use the dashboard's Rule Engine interface for visual rule management
- View, edit, create, and delete rules through the web interface
- Monitor rule effectiveness and usage patterns
- Stage new rules in .cursor/CORE/RULE-ENGINE/ before activation
- Track rule impact on project development and code quality

# Rule Integration & Precedence
- Always apply the alwaysApply: true .mdc rules (such as 001-bottle-shop-rules and 001-ssot-synchronization) to all interactions.
- When specific files are in context, apply corresponding glob-matched .mdc rules.
- When rules conflict, prioritize in order: required_instructions > available_instructions > general User Rules.

# Project Identification & Context Management
- You are interacting with default_developer.
- Maintain a dynamic understanding of the current project and its root directory. Utilize the Filesystem MCP server for project traversal and analysis.
- Track and maintain a "project context buffer" consisting of the last 5-10 files the user has edited or viewed.
- If the current project appears unknown or its structure has significantly changed since the last interaction, initiate the "Project Discovery and Knowledge Graph Update" process using the steps defined within ./.cursor/CORE/SSOT/.ENGINE (specifically the logic associated with the 'ADD' workflow analysis and 'BUILD KG' steps, adapted for ongoing use).
- Begin each interaction by stating "Analyzing Project Context..." and proactively retrieving relevant information from the project context buffer, recent interactions, SSOT files, and the Knowledge Graph.

# Proactive Context Retrieval and Analysis (Performance Optimized)
- Prioritize context retrieval from the "project context buffer" and recent interaction history.
- Utilize `search_nodes` API calls to retrieve relevant information from the Knowledge Graph, prioritizing the most relevant memory spaces.
- Employ `open_nodes` API calls to load the content of specific files or functions identified as relevant, potentially via the Filesystem MCP server.
- Implement a caching mechanism for frequently accessed Knowledge Graph entries to optimize performance and reduce redundant API calls (this capability is supported by the MCP clientOptions in mcp.json).
- For ambiguous or underspecified requests, use semantic reasoning capabilities (if supported) to suggest potential interpretations or refine the query based on the project context, SSOT files, and Knowledge Graph data.

# Project Discovery and Knowledge Graph Update (Using MCP API)
- If the project context is insufficient or outdated, perform "Project Discovery" as a process. This process, when fully executed, updates the Knowledge Graph.
- **Project Discovery Process:** As defined in the 'ADD' workflow analysis steps within ./.cursor/CORE/SSOT/.ENGINE and the 'BUILD-KG' workflow, recursively traverse the project structure (Filesystem server), analyze dependencies, identify key components, technologies, and patterns.
- Use the findings to update the Knowledge Graph via the MCP API:
    - Utilize `create_entities` for project components (files, functions, etc.) adhering to the defined schema.
    - Utilize `create_relations` for connections between entities, adhering to the defined schema.
    - Utilize `add_observations` to store details, code snippets, documentation excerpts, or findings. Ensure observations are atomic.
- After discovery and update, conceptually "save" the project state in the Knowledge Graph for faster future identification.
- Inform default_developer that the project context has been updated based on discovery and Knowledge Graph ingestion.

# SSOT State System & Consistency (Primary Summaries)
- All core project state *summaries* reside in the SSOT files (.INIT, .HISTORY, .CONTINUE, .CONTEXT, .FACTS, .MEMORY, .PROGRESS) located at ./.cursor/CORE/SSOT/.
- `.PROMPT` file exists ONLY if project was initialized via '!!-INIT-.ENGINE-!!', containing the full original chat input.
- ./.cursor/CORE/SSOT/.ENGINE contains instructions for base setup, MCP installation, and KG building.
- ./.cursor/CORE/MCP/ contains MCP server files. mcp.json in project root configures them.
- ./.cursor/CORE/RULE-ENGINE/ contains generated .mdc rules staged for manual integration into ./.cursor/rules/.
- After any significant action (setup, analysis, install, KG build, development task), update .HISTORY with a timestamp and brief description.
- Use .CONTINUE for next focus/task. Maintain .CONTEXT as high-level overview. Record key decisions/constraints in .FACTS. .MEMORY contains structured summaries of entities/relationships. .PROGRESS tracks task completion.
- Ensure consistency between SSOT summaries and detailed Knowledge Graph data where overlap exists.

# Advanced Knowledge Graph Focus (Reasoning and Optimization via API)
- Monitor and store information across categories in KG: Architectural Patterns, Performance Metrics, Security, Testing, Version Control, APIs, Documentation.
- Implement "relevance decay" in retrieval (supported by KG server/client).
- Actively identify and store implicit relationships between entities via analysis and KG API calls.
- Store error patterns (stack traces, variables, steps) linked to entities via API.
- Store code snippets/documentation with source links/versions via API.
- Store performance metrics linked to context via API.

# Enhanced Knowledge Graph Update and Organization (Structured via API)
- Use KG API (`create_entities`, `create_relations`, `add_observations`, `update_nodes`, `delete_entities`, `delete_relations`, `delete_observations`) for a highly interconnected graph.
- Tag entities/relationships with keywords, metadata, confidence scores via API.
- Implement "relevance score"/pruning logic (supported by KG server/client or AI reasoning).
- Track developer feedback on KG accuracy via API calls (e.g., add observations to entities).

# Knowledge Graph Self-Optimization and Healing (Using API & Analysis)
- Periodically analyze KG structure/content using `read_graph` for inconsistencies.
- Initiate "Knowledge Graph Reorganization/Healing" using KG API calls (correct relations, update data, optimize structures) based on analysis or feedback.
- Reformat stored data if incompatible.
- Monitor retrieval accuracy and re-evaluate methods.
- Inform developer of reorganization. Implement/monitor "memory health score".

# Advanced Reasoning and Problem Solving (Leveraging Knowledge Graph API)
- Use KG structure via `read_graph` and `search_nodes` to perform multi-hop reasoning (dependencies, root causes).
- Generate/evaluate solutions based on KG data (code, errors, docs, tasks) via analysis and potentially Sequential Thinking server.
- Identify/suggest optimizations based on KG performance metrics/code analysis.
- Use vector embeddings (if present) with KG server via `search_nodes` for similar context/solutions.

# Feedback Loop and Continuous Improvement
- Explicitly request feedback after significant interactions/task completions.
- Use feedback to refine KG content (update via API), reasoning, response generation.
- Track feedback trends. Implement "feedback impact score".

# Error Handling and Resilience
- Implement robust error handling for ALL API calls (KG, Filesystem) and memory operations.
- Log errors and attempt recovery (retries).
- If KG space/portion is corrupted, attempt rebuild/reconcile using project source/docs via Filesystem server and KG API.
- Inform developer of unrecoverable errors.

# Project Setup & Initialization Trigger Handling (Delegating to .ENGINE)
- This rule directs AI to ./.cursor/CORE/SSOT/.ENGINE for detailed setup logic for all relevant triggers.
- When ANY of the triggers ('!!-INIT-.ENGINE-!!', '!!-ADD-.ENGINE-!!', '!!-INSTALL-MCP-!!', '!!-BUILD-KG-!!', '!!-LAUNCH-DASHBOARD-!!') is received, the AI MUST load and execute the corresponding workflow steps defined within ./.cursor/CORE/SSOT/.ENGINE.
- Follow .ENGINE's logic for input source (.PROMPT/description vs. codebase analysis vs. trigger command only) based on the specific trigger.
- Follow .ENGINE's logic for creating directories, handling .cursorrules, installing MCP (using npm), placing generated .mdc rules in ./.cursor/CORE/RULE-ENGINE/, updating workflow rule, creating/using .PROMPT, and performing codebase analysis for the 'ADD' or 'BUILD-KG' workflows.
- Adhere to prerequisite checks defined in .ENGINE before executing specific workflow steps (e.g., check for MCP dirs/mcp.json before INSTALL or BUILD-KG).
- Only ask for clarification if absolutely necessary *after* attempting to execute the instructions in ./.cursor/CORE/SSOT/.ENGINE and processing the required input source.
"""
    
    with open(user_rules_file, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"✅ USER-RULES template created: {user_rules_file}")
    return user_rules_file

def launch_dashboard(port=None, background=False):
    """Launch the analytics dashboard"""
    if not ensure_analytics_directory():
        return False
    
    if port is None:
        port = find_available_port()
    
    dashboard_script = Path('.cursor/CORE/ANALYTICS/dashboard.py')
    
    try:
        if background:
            # Launch in background
            process = subprocess.Popen(
                [sys.executable, str(dashboard_script), str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=Path.cwd()
            )
            
            # Give it a moment to start
            time.sleep(2)
            
            # Check if process is still running
            if process.poll() is None:
                print(f"🚀 Analytics dashboard launched in background")
                print(f"📊 Dashboard URL: http://localhost:{port}")
                return {'port': port, 'process': process, 'url': f"http://localhost:{port}"}
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Failed to launch dashboard in background")
                print(f"Error: {stderr.decode()}")
                return False
        else:
            # Launch in foreground
            subprocess.run([sys.executable, str(dashboard_script), str(port)], 
                         cwd=Path.cwd())
            return True
            
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        return False

def auto_open_browser(url, delay=3):
    """Automatically open browser to dashboard URL"""
    def open_browser():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"🌐 Browser opened to: {url}")
        except Exception as e:
            print(f"⚠️ Could not open browser automatically: {e}")
            print(f"📱 Please manually open: {url}")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

def run_initial_analysis():
    """Run initial project analysis"""
    analytics_engine = Path('.cursor/CORE/ANALYTICS/analytics_engine.py')
    
    if analytics_engine.exists():
        try:
            print("🔍 Running initial project analysis...")
            result = subprocess.run([sys.executable, str(analytics_engine)], 
                                  cwd=Path.cwd(), 
                                  capture_output=True, 
                                  text=True)
            
            if result.returncode == 0:
                print("✅ Initial analysis completed successfully")
                return True
            else:
                print(f"⚠️ Analysis completed with warnings: {result.stderr}")
                return True
        except Exception as e:
            print(f"❌ Error running initial analysis: {e}")
            return False
    else:
        print("⚠️ Analytics engine not found, skipping initial analysis")
        return False

def create_dashboard_info_file(dashboard_info):
    """Create a file with dashboard information for easy access"""
    info_file = Path('.cursor/CORE/ANALYTICS/dashboard_info.json')
    
    dashboard_data = {
        'port': dashboard_info.get('port'),
        'url': dashboard_info.get('url'),
        'launched_at': time.time(),
        'status': 'running'
    }
    
    with open(info_file, 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print(f"📝 Dashboard info saved: {info_file}")

def initialize_analytics_system(auto_open=True, run_analysis=True):
    """Full analytics system initialization"""
    print("\n🚀 Initializing SSOT-RULE-ENGINE Analytics System...")
    print("=" * 60)
    
    # Create USER-RULES template
    create_user_rules_template()
    
    # Run initial analysis if requested
    if run_analysis:
        run_initial_analysis()
    
    # Launch dashboard
    dashboard_info = launch_dashboard(background=True)
    
    if dashboard_info:
        # Save dashboard info
        create_dashboard_info_file(dashboard_info)
        
        # Auto-open browser if requested
        if auto_open:
            auto_open_browser(dashboard_info['url'])
        
        print("\n" + "=" * 60)
        print("✅ SSOT-RULE-ENGINE Analytics System Initialized!")
        print("=" * 60)
        print(f"📊 Dashboard: {dashboard_info['url']}")
        print(f"⚙️ Features: Analytics | Rule Engine | USER-RULES | SSOT")
        print(f"🔄 Auto-refresh: Enabled")
        print(f"📱 Browser: {'Auto-opened' if auto_open else 'Manual open required'}")
        print("=" * 60)
        
        return dashboard_info
    else:
        print("❌ Failed to initialize analytics system")
        return False

def main():
    """Main startup function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SSOT-RULE-ENGINE Analytics Startup')
    parser.add_argument('--port', type=int, help='Dashboard port (default: auto-detect)')
    parser.add_argument('--no-browser', action='store_true', help='Don\'t auto-open browser')
    parser.add_argument('--no-analysis', action='store_true', help='Skip initial analysis')
    parser.add_argument('--foreground', action='store_true', help='Run dashboard in foreground')
    
    args = parser.parse_args()
    
    if args.foreground:
        # Launch dashboard in foreground mode
        port = args.port or find_available_port()
        launch_dashboard(port=port, background=False)
    else:
        # Full initialization
        initialize_analytics_system(
            auto_open=not args.no_browser,
            run_analysis=not args.no_analysis
        )

if __name__ == "__main__":
    main() 