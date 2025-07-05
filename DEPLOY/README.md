# SSOT-RULE-ENGINE-TEMPLATE Deployment Package

This directory contains the complete template for deploying the SSOT-RULE-ENGINE system to any new or existing project.

## 🚀 Quick Start

1. **Copy the `.cursor` folder** from this DEPLOY directory to your project root
2. **Copy the `launch-dashboard.py`** script to your project root
3. **Run the initialization trigger** in your project:
   ```
   !!-ADD-.ENGINE-!!
   ```

## 📁 What's Included

```
DEPLOY/
├── .cursor/
│   ├── CORE/
│   │   ├── SSOT/
│   │   │   └── .ENGINE           # Core workflow orchestrator
│   │   ├── MCP/                  # Model Context Protocol servers
│   │   │   ├── knowledge-graph/  # Entity-relationship modeling
│   │   │   ├── sequential-thinking/  # Multi-step reasoning
│   │   │   └── filesystem/       # Enhanced file operations
│   │   ├── ANALYTICS/            # Project health monitoring
│   │   │   ├── analytics_engine.py
│   │   │   ├── dashboard.py
│   │   │   ├── cli.py
│   │   │   └── startup.py
│   │   ├── RULE-ENGINE/          # Staged rules directory
│   │   ├── MEMORY/              # Persistent storage
│   │   └── PROMPTS/             # Prompt templates
│   ├── rules/
│   │   └── 999-mdc-format.mdc   # Rule format specification
│   ├── mcp.json                 # MCP server configuration
│   └── USER-RULES.md           # User rules template
├── launch-dashboard.py          # Quick dashboard launcher
└── README.md                   # This file
```

## 🔧 Installation Process

### Step 1: Copy Template Files
Copy the entire `.cursor` folder and `launch-dashboard.py` to your project root:

```bash
# Copy the template structure
cp -r DEPLOY/.cursor /path/to/your/project/
cp DEPLOY/launch-dashboard.py /path/to/your/project/
```

### Step 2: Initialize the System
Navigate to your project and run the ADD trigger:

```
!!-ADD-.ENGINE-!!
```

This will:
- ✅ Analyze your existing codebase
- ✅ Populate SSOT state files
- ✅ Install MCP servers
- ✅ Build Knowledge Graph
- ✅ Launch analytics dashboard

### Step 3: Install Dependencies (if needed)
If MCP servers aren't installed, run:

```
!!-INSTALL-MCP-!!
```

### Step 4: Build Knowledge Graph
To populate the Knowledge Graph with your project data:

```
!!-BUILD-KG-!!
```

## 🎯 Available Triggers

| Trigger | Purpose |
|---------|---------|
| `!!-ADD-.ENGINE-!!` | Add SSOT system to existing project |
| `!!-INSTALL-MCP-!!` | Install MCP servers |
| `!!-BUILD-KG-!!` | Build Knowledge Graph |
| `!!-LAUNCH-DASHBOARD-!!` | Launch analytics dashboard |
| `!!-ANALYZE-PROJECT-!!` | Run comprehensive analysis |
| `!!-VIEW-DASHBOARD-!!` | Open dashboard in browser |
| `!!-HEALTH-CHECK-!!` | Quick health assessment |

## 📊 Analytics Dashboard

The system includes a comprehensive analytics dashboard that provides:

- **Project Health Score** (0-100)
- **SSOT System Status**
- **MCP Server Performance**
- **Knowledge Graph Metrics**
- **Rule Engine Effectiveness**
- **Interactive Rule Management**

Access via: `http://localhost:8080`

## 🧠 Core Components

### SSOT (Single Source of Truth) System
- **Purpose**: Centralized project state management
- **Files**: `.ENGINE`, `.INIT`, `.CONTEXT`, `.FACTS`, `.MEMORY`, `.HISTORY`, `.CONTINUE`, `.PROGRESS`
- **Function**: Workflow orchestration and state persistence

### MCP (Model Context Protocol) Servers
- **knowledge-graph**: Entity-relationship project modeling
- **sequential-thinking**: Multi-step reasoning and problem solving
- **filesystem**: Enhanced file operations and analysis

### Analytics Engine
- **Real-time monitoring**: Project health metrics
- **Intelligent recommendations**: Development optimization
- **Visual dashboard**: Interactive charts and status indicators

### Rule Engine
- **Context-aware rules**: Behavior modification based on file patterns
- **Visual management**: Web-based rule editing interface
- **Effectiveness tracking**: Monitor rule impact on development

## 🔒 System Requirements

- **Python 3.8+** (for analytics engine)
- **Node.js 18+** (for MCP servers)
- **npm** (for MCP dependencies)
- **Git** (for version control integration)

## 📝 Template Customization

### Adding Custom MCP Servers
1. Create new server directory in `.cursor/CORE/MCP/`
2. Add server configuration to `mcp.json`
3. Run `!!-INSTALL-MCP-!!` to install dependencies

### Custom Analytics
- Modify `analytics_engine.py` for custom metrics
- Update `dashboard.py` for custom visualizations
- Add custom rules in `.cursor/CORE/RULE-ENGINE/`

### Rule Development
- Create `.mdc` files in `.cursor/CORE/RULE-ENGINE/`
- Use the dashboard's Rule Engine interface
- Move tested rules to `.cursor/rules/` for activation

## 🚨 Troubleshooting

### Common Issues

1. **MCP Servers Not Installing**
   - Check Node.js version (18+)
   - Verify npm is available
   - Run `!!-INSTALL-MCP-!!` manually

2. **Dashboard Not Loading**
   - Check if Python 3.8+ is installed
   - Verify port 8080 is available
   - Run `python launch-dashboard.py` manually

3. **Knowledge Graph Empty**
   - Run `!!-BUILD-KG-!!` to populate
   - Check MCP servers are running
   - Verify project has analyzable content

### Getting Help
- Check `.cursor/CORE/SSOT/.HISTORY` for system events
- Run `!!-HEALTH-CHECK-!!` for quick diagnostics
- Use `!!-ANALYZE-PROJECT-!!` for comprehensive report

## 🎉 Success Indicators

After successful deployment, you should see:
- ✅ Analytics dashboard running on http://localhost:8080
- ✅ SSOT files populated in `.cursor/CORE/SSOT/`
- ✅ MCP servers installed and configured
- ✅ Knowledge Graph populated with project entities
- ✅ Project health score > 60

## 🔗 Next Steps

1. **Explore the Dashboard**: Visit http://localhost:8080
2. **Review SSOT State**: Check `.cursor/CORE/SSOT/` files
3. **Test Knowledge Graph**: Use search and entity exploration
4. **Create Custom Rules**: Use the Rule Engine interface
5. **Monitor Health**: Set up regular health checks

---

**Template Version**: 1.0.0  
**Last Updated**: 2025-01-27  
**Compatibility**: Cursor AI IDE with MCP support 