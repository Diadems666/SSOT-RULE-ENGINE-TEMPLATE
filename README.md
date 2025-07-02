# SSOT-RULE-ENGINE-TEMPLATE

An intelligent AI-powered development framework that combines Single Source of Truth (SSOT) project state management, context-aware Rule Engine, and Model Context Protocol (MCP) integration to create a self-organizing, learning development environment.

## 🎯 Overview

The SSOT-RULE-ENGINE-TEMPLATE transforms your development workflow by providing:

- **🧠 Persistent AI Memory**: Knowledge Graph-based project understanding that grows over time
- **📋 Centralized State Management**: Single Source of Truth for all project information
- **🎛️ Context-Aware AI Behavior**: Dynamic rule system that adapts to your project needs
- **🔧 Advanced AI Capabilities**: Specialized MCP servers for enhanced reasoning and analysis
- **📊 Intelligent Project Tracking**: Automated progress monitoring and documentation
- **📈 Advanced Analytics**: Real-time project health monitoring and performance insights

## ✨ Key Features

### 🏗️ SSOT (Single Source of Truth) System
- Centralized project state in `.cursor/CORE/SSOT/`
- Automated project history and progress tracking
- Intelligent workflow orchestration via trigger system
- Project portability with snapshot/restore capabilities

### 🎯 Rule Engine
- Context-aware AI behavior through `.mdc` files
- Global and file-specific rule application
- Automated rule generation and staging
- Consistent development standards enforcement

### 🚀 MCP Integration
- **Knowledge Graph Server**: Persistent entity-relationship project modeling
- **Sequential Thinking Server**: Multi-step reasoning and problem solving
- **Filesystem Server**: Enhanced file system operations and analysis

### 🔄 Intelligent Workflows
- Automated project initialization and analysis
- Smart codebase understanding and documentation
- GitHub preparation and repository optimization
- Comprehensive testing and quality assurance

### 📈 Advanced Analytics System
- Real-time project health scoring (0-100 scale)
- Interactive web dashboard with live visualizations
- Multi-dimensional analysis (SSOT, MCP, Rules, Project structure)
- Intelligent recommendations engine with priority suggestions
- Development velocity tracking and trend analysis
- System performance monitoring and optimization insights

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Cursor IDE with AI capabilities

### Installation

#### For New Projects
1. **Describe Your Project** in Cursor chat, then initialize:
```
!!-INIT-.ENGINE-!!
```

2. **Install MCP Servers**:
```
!!-INSTALL-MCP-!!
```

3. **Build Knowledge Graph**:
```
!!-BUILD-KG-!!
```

#### For Existing Projects
1. **Analyze Existing Codebase**:
```
!!-ADD-.ENGINE-!!
```

2. **Install MCP Servers**:
```
!!-INSTALL-MCP-!!
```

3. **Build Knowledge Graph**:
```
!!-BUILD-KG-!!
```

## 🎮 Core Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `!!-INIT-.ENGINE-!!` | Initialize new project *(auto-launches dashboard)* | After providing project description |
| `!!-ADD-.ENGINE-!!` | Add to existing project *(auto-launches dashboard)* | For existing codebases |
| `!!-INSTALL-MCP-!!` | Install MCP servers | After INIT or ADD |
| `!!-BUILD-KG-!!` | Build Knowledge Graph | After MCP installation |
| `!!-LAUNCH-DASHBOARD-!!` | Launch analytics dashboard with visual rule engine | Manual dashboard launch anytime |
| `!!-ANALYZE-PROJECT-!!` | Run comprehensive project analysis | For detailed health scoring |
| `!!-VIEW-DASHBOARD-!!` | Open analytics dashboard in browser | Quick dashboard access |
| `!!-HEALTH-CHECK-!!` | Quick system assessment | For rapid status overview |
| `!!-UPDATE-SSOT-!!` | Sync project state | After significant changes |
| `!!-CREATE-PORTABLE-!!` | Create project snapshot | For backup/transfer |
| `!!-LOAD-PORTABLE-!!` | Load project snapshot | To restore state |
| `!!-UPDATE-DOCS-!!` | Update documentation | For doc synchronization |
| `!!-PREPARE-GITHUB-!!` | Prepare for GitHub | Before repository upload |

## 📁 Project Structure

```
.cursor/
├── CORE/
│   ├── SSOT/                   # Single Source of Truth files
│   │   ├── .ENGINE             # Central workflow orchestrator
│   │   ├── .INIT               # Project initialization
│   │   ├── .CONTEXT            # High-level overview
│   │   ├── .FACTS              # Technical decisions
│   │   ├── .MEMORY             # Component summaries
│   │   ├── .HISTORY            # Activity log
│   │   ├── .CONTINUE           # Next steps
│   │   └── .PROGRESS           # Task tracking
│   ├── MCP/                    # MCP server implementations
│   │   ├── knowledge-graph/    # Graph database server
│   │   ├── sequentialthinking/ # Reasoning server
│   │   └── filesystem/         # File operations server
│   ├── RULE-ENGINE/            # Generated rules staging
│   ├── MEMORY/                 # Persistent memory storage
│   ├── PROMPTS/                # System prompts
│   ├── ANALYTICS/              # Analytics engine and dashboard
│   │   ├── analytics_engine.py # Project health analysis
│   │   ├── dashboard.py        # Web dashboard with visual rule engine
│   │   ├── startup.py          # Dashboard auto-launch script
│   │   ├── USER-RULES-TEMPLATE.md # Template for easy USER-RULES setup
│   │   └── dashboard/          # Generated dashboard files
│   └── DOCS/                   # Documentation
├── rules/                      # Active rule files
├── mcp.json                    # MCP configuration
└── launch-dashboard.py         # Quick dashboard launcher
```

## 🔧 Configuration

### MCP Servers Configuration
The template includes three pre-configured MCP servers:

1. **Knowledge Graph Server** - Persistent project memory
2. **Sequential Thinking Server** - Advanced reasoning capabilities  
3. **Filesystem Server** - Enhanced file operations

Configuration is handled automatically through the trigger system.

### Rule Engine Configuration
Rules are defined in `.mdc` files with frontmatter:

```markdown
---
description: Rule description
globs: **/*.js, **/*.ts
alwaysApply: false
---

# Rule Content
Your guidelines and instructions...
```

## 📊 Example Use Cases

### Web Application Development
```bash
# Describe your Flask/Django/Express app, then:
!!-INIT-.ENGINE-!!
!!-INSTALL-MCP-!!
!!-BUILD-KG-!!
```

### Existing Codebase Integration
```bash
# For any existing project:
!!-ADD-.ENGINE-!!
!!-INSTALL-MCP-!!
!!-BUILD-KG-!!
```

### Team Collaboration
```bash
# Create portable state for sharing:
!!-CREATE-PORTABLE-!!

# Team member loads state:
!!-LOAD-PORTABLE-!!
```

### Project Analytics & Monitoring
```bash
# Quick health assessment:
!!-HEALTH-CHECK-!!

# Comprehensive analysis:
!!-ANALYZE-PROJECT-!!

# Launch interactive dashboard with visual rule engine:
!!-LAUNCH-DASHBOARD-!!

# Open dashboard in browser (if already running):
!!-VIEW-DASHBOARD-!!

# Manual launch options:
python launch-dashboard.py                    # Quick launcher from project root
python .cursor/CORE/ANALYTICS/startup.py     # Direct startup script
```

**Dashboard Features:**
- 📊 **Analytics Tab**: Real-time health scoring and project metrics
- ⚙️ **Rule Engine Tab**: Visual rule management interface
- 📋 **USER-RULES Tab**: Template copying for easy setup  
- 🗂️ **SSOT Tab**: System state monitoring and file inspection

## 🎯 Benefits

### For Developers
- **Persistent Context**: AI remembers your project across sessions
- **Intelligent Assistance**: Context-aware suggestions and code generation
- **Automated Documentation**: Self-updating project documentation
- **Quality Assurance**: Consistent coding standards and best practices

### For Teams
- **Knowledge Sharing**: Easy context transfer between team members
- **Onboarding**: New developers quickly understand project structure
- **Standards Enforcement**: Consistent development patterns across team
- **Progress Tracking**: Comprehensive project history and progress monitoring

### For Projects
- **Reduced Technical Debt**: Continuous quality monitoring and improvement
- **Better Architecture**: AI-guided architectural decisions and refactoring
- **Enhanced Testing**: Intelligent test generation and coverage analysis
- **Documentation**: Always up-to-date project documentation
- **Health Monitoring**: Real-time project health scoring and trend analysis
- **Performance Insights**: Actionable recommendations for optimization
- **Visual Analytics**: Interactive dashboards for comprehensive project oversight

## 📈 Advanced Features

### Knowledge Graph Queries
The system builds a comprehensive knowledge graph of your project:
- **Entities**: Files, functions, classes, modules, configurations
- **Relationships**: Dependencies, calls, implementations, contains
- **Observations**: Comments, metrics, patterns, decisions

### Advanced Analytics Dashboard
Real-time project monitoring and insights:
- **Health Scoring**: Comprehensive 0-100 scale project health assessment
- **System Analysis**: SSOT (30%), MCP (30%), Rules (25%), General (15%) breakdown
- **Interactive Visualizations**: Charts, graphs, and real-time data displays
- **Intelligent Recommendations**: Priority-based suggestions for improvement
- **Development Velocity**: Activity tracking and productivity metrics
- **Web Interface**: Responsive dashboard with auto-refresh capabilities

```bash
# Launch analytics dashboard
cd .cursor/CORE/ANALYTICS
python dashboard.py  # Opens browser automatically

# Generate static reports
python analytics_engine.py  # Creates JSON and Markdown reports
```

### Project Portability
Create and restore complete project snapshots:
- Full SSOT state preservation
- Knowledge Graph backup/restore
- Rule configuration transfer
- Cross-environment compatibility

### GitHub Integration
Automated repository preparation:
- Intelligent `.gitignore` generation
- Documentation synchronization
- Code quality checks
- Release preparation

## 🛠️ Troubleshooting

### MCP Server Issues
```bash
# Check MCP server status
npm run build  # In each MCP server directory

# Restart servers
# Restart Cursor IDE
```

### SSOT Synchronization
```bash
# Update SSOT after major changes
!!-UPDATE-SSOT-!!

# Rebuild Knowledge Graph if needed
!!-BUILD-KG-!!
```

### Rule Engine Problems
- Check `.mdc` file syntax in `rules/` directory
- Verify glob patterns match intended files
- Review rule staging in `CORE/RULE-ENGINE/`

### Analytics Dashboard Issues
```bash
# Generate dashboard without starting server
cd .cursor/CORE/ANALYTICS
python dashboard.py --generate-only

# Start dashboard on custom port
python dashboard.py --port 8080 --no-browser

# Run analytics analysis only
python analytics_engine.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Use the SSOT system for development tracking
4. Update documentation using `!!-UPDATE-DOCS-!!`
5. Prepare for submission with `!!-PREPARE-GITHUB-!!`
6. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Model Context Protocol (MCP)** - For the foundational server architecture
- **Cursor AI** - For the intelligent IDE integration
- **Anthropic** - For advanced AI reasoning capabilities

## 📞 Support

- **Documentation**: See `DOCS/Comprehensive Documentation.md`
- **Issues**: Report issues through GitHub Issues
- **Discussions**: Use GitHub Discussions for questions and ideas

## 🗺️ Roadmap

- [ ] Visual Knowledge Graph explorer
- [x] Advanced analytics and metrics
- [ ] Integration with popular development tools
- [ ] Multi-language support expansion
- [ ] Cloud-based Knowledge Graph synchronization
- [ ] Machine learning-based project predictions
- [ ] Team collaboration analytics
- [ ] CI/CD pipeline integration

---

**Start building smarter with AI-powered development today!** 🚀 