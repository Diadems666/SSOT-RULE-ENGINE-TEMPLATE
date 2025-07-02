# SSOT-RULE-ENGINE-TEMPLATE: Comprehensive Documentation

## System Overview

The **SSOT-RULE-ENGINE-TEMPLATE** is a sophisticated AI-powered development framework that combines three core systems:

1. **SSOT (Single Source of Truth) System** - Centralized project state management
2. **Rule Engine** - Context-aware AI behavior configuration
3. **MCP (Model Context Protocol) Integration** - Enhanced AI capabilities through specialized servers

This template provides an intelligent, self-organizing development environment that maintains consistent project context, enables advanced AI reasoning, and creates persistent knowledge representations of codebases.

## Architecture & Core Components

### 1. SSOT (Single Source of Truth) System
Located in `.cursor/CORE/SSOT/`, this system maintains centralized project state through several key files:

#### Core SSOT Files:
- **`.ENGINE`** - Central workflow orchestrator containing trigger logic for all system operations
- **`.INIT`** - Project initialization summary and technology stack
- **`.CONTEXT`** - High-level project overview and business context  
- **`.FACTS`** - Technical decisions, constraints, and configuration details
- **`.MEMORY`** - Structured summaries of project components and concepts
- **`.HISTORY`** - Timestamped log of all project activities and changes
- **`.CONTINUE`** - Next steps and development priorities
- **`.PROGRESS`** - Task completion tracking
- **`.PROMPT`** - Original project description (created only via `!!-INIT-.ENGINE-!!`)

### 2. Rule Engine System
The Rule Engine provides context-aware AI behavior through `.mdc` (Markdown Configuration) files:

#### Structure:
- **`.cursor/rules/`** - Active rules directory
- **`.cursor/CORE/RULE-ENGINE/`** - Staging area for AI-generated rules
- **`.cursor/USER-RULES.md`** - Core behavioral guidelines

#### Rule Types:
- **Global Rules** (`alwaysApply: true`) - Applied to all interactions
- **Context-Specific Rules** - Applied based on file patterns and project context
- **Task-Specific Rules** - Applied for particular development scenarios

### 3. MCP (Model Context Protocol) Integration
Three specialized MCP servers enhance AI capabilities:

#### MCP Servers:
1. **Knowledge Graph Server** (`knowledge-graph/`)
   - Persistent memory storage using graph database
   - Entity-relationship modeling of project components
   - JSONL-based storage in `.cursor/CORE/MEMORY/memory.jsonl`

2. **Sequential Thinking Server** (`sequentialthinking/`)
   - Multi-step reasoning and problem-solving capabilities
   - Dynamic thought process with revision support

3. **Filesystem Server** (`filesystem/`)
   - Enhanced file system operations
   - Recursive project analysis capabilities

## System Triggers & Workflows

The system uses specific trigger phrases to initiate workflows defined in `.cursor/CORE/SSOT/.ENGINE`:

### Primary Setup Triggers:

#### `!!-INIT-.ENGINE-!!`
**Purpose:** Initialize SSOT/Rule Engine for new projects
**Usage:** Provide detailed project description in chat, then use this trigger
**Actions:**
- Creates `.PROMPT` file with full chat input
- Auto-populates all SSOT files based on description
- Creates core directory structure
- Sets up MCP configuration

#### `!!-ADD-.ENGINE-!!`
**Purpose:** Add SSOT/Rule Engine to existing projects
**Usage:** Use alone without preceding description
**Actions:**
- Performs comprehensive codebase analysis
- Auto-populates SSOT files based on analysis findings
- Creates core directory structure
- Does NOT create `.PROMPT` file

#### `!!-INSTALL-MCP-!!`
**Purpose:** Install MCP servers
**Prerequisites:** Core structure must exist, `mcp.json` configured
**Actions:**
- Runs `npm install` for all MCP servers
- Updates `.HISTORY` with installation log
- Verifies server readiness

#### `!!-BUILD-KG-!!`
**Purpose:** Build initial Knowledge Graph
**Prerequisites:** MCP servers installed and configured
**Actions:**
- Analyzes entire codebase structure
- Creates entities for files, directories, classes, functions
- Establishes relationships between components
- Adds detailed observations to entities
- Updates SSOT `.HISTORY`

### Maintenance & Utility Triggers:

#### `!!-UPDATE-SSOT-!!`
**Purpose:** Synchronize SSOT with recent changes
**Actions:**
- Synthesizes recent project changes
- Updates all relevant SSOT files
- Optionally updates Knowledge Graph
- Logs changes to `.HISTORY`

#### `!!-CREATE-PORTABLE-!!`
**Purpose:** Create portable project snapshot
**Actions:**
- Synthesizes comprehensive project state
- Creates `.PORTABLE` file with self-contained snapshot
- Includes SSOT summaries, rules, codebase analysis
- Updates `.HISTORY`

#### `!!-LOAD-PORTABLE-!!`
**Purpose:** Load project state from `.PORTABLE`
**Actions:**
- Reads and parses `.PORTABLE` file
- Populates/overwrites SSOT files
- Optionally rebuilds Knowledge Graph
- Restores complete project context

#### Additional Triggers:
- `!!-CREATE-CHAT-HISTORY-!!` - Save current chat to `.CHAT`
- `!!-UPDATE-DOCS-!!` - Update project documentation
- `!!-PREPARE-GITHUB-!!` - Prepare for GitHub upload

## Knowledge Graph System

The Knowledge Graph provides persistent, queryable memory through entity-relationship modeling:

### Entity Types:
- **project** - Root entity for entire project
- **directory** - Project directories
- **file** - Individual files
- **module** - Dependencies and modules
- **class** - Class definitions
- **function** - Function definitions
- **interface** - Interface definitions
- **config_item** - Configuration variables
- **service** - External services/resources

### Relationship Types:
- **contains** - Hierarchical containment
- **depends_on** - Dependencies between components
- **calls** - Function/method calls
- **uses** - Configuration usage
- **implements** - Interface implementation
- **extends** - Class inheritance
- **integrates_with** - External service integration
- **has_test_file** - Test file associations
- **defined_in** - Definition location

### Observations:
Each entity can have multiple string observations containing:
- File paths and metadata
- Function signatures and parameters
- Code comments and documentation
- Configuration details
- Performance metrics
- Error patterns

## Usage Instructions

### Getting Started

#### For New Projects:
1. **Provide Project Description**: Write detailed project requirements in chat
2. **Initialize System**: Use `!!-INIT-.ENGINE-!!`
3. **Install MCP Servers**: Use `!!-INSTALL-MCP-!!`
4. **Build Knowledge Graph**: Use `!!-BUILD-KG-!!`

#### For Existing Projects:
1. **Analyze Existing Code**: Use `!!-ADD-.ENGINE-!!`
2. **Install MCP Servers**: Use `!!-INSTALL-MCP-!!`
3. **Build Knowledge Graph**: Use `!!-BUILD-KG-!!`

### Best Practices

#### SSOT Maintenance:
- Update `.HISTORY` after significant changes
- Keep `.CONTINUE` current with next priorities
- Record key decisions in `.FACTS`
- Maintain `.CONTEXT` accuracy

#### Rule Engine Usage:
- Create specific rules for repetitive patterns
- Use glob patterns effectively
- Set `alwaysApply: true` sparingly
- Stage rules in `RULE-ENGINE/` before moving to `rules/`

#### Knowledge Graph Optimization:
- Regular updates via `!!-UPDATE-SSOT-!!`
- Query specific entities with `search_nodes`
- Add observations for important discoveries
- Maintain entity relationships

### Advanced Features

#### Project Portability:
- Create snapshots with `!!-CREATE-PORTABLE-!!`
- Transfer context between environments
- Load complete project state with `!!-LOAD-PORTABLE-!!`

#### Documentation Synchronization:
- Auto-update docs with `!!-UPDATE-DOCS-!!`
- Maintain README.md alignment with SSOT
- Generate architecture documentation from Knowledge Graph

#### GitHub Integration:
- Prepare repositories with `!!-PREPARE-GITHUB-!!`
- Auto-generate appropriate `.gitignore`
- Verify documentation completeness

## Configuration Details

### MCP Configuration (`mcp.json`):
```json
{
  "mcpServers": {
    "memory": {
      "command": "node",
      "args": ["./.cursor/CORE/MCP/knowledge-graph/dist/index.js"],
      "env": {
        "NODE_ENV": "production",
        "MCP_SERVER_PORT": "3100"
      }
    }
  }
}
```

### Rule Format (`.mdc`):
```markdown
---
description: Brief description of rule purpose
globs: **/*.js, **/*.ts
alwaysApply: false
---

# Rule Content
Detailed instructions and guidelines...
```

## Current Project State

Based on the system analysis, this template currently contains:

### Implemented Features:
- ✅ Complete SSOT system with all core files
- ✅ Comprehensive rule engine with MDC format
- ✅ Three MCP servers (Knowledge Graph, Sequential Thinking, Filesystem)
- ✅ Detailed workflow orchestration via `.ENGINE`
- ✅ Project portability system
- ✅ Documentation automation
- ✅ GitHub preparation tools

### Example Implementation:
The template includes a complete **Bottle Shop End-of-Trade Web Application** as a reference implementation, demonstrating:
- Flask web application with SQLite database
- Australian currency denomination handling
- Float management ($1,500 safe float, $500 till float)
- End-of-trade reconciliation with variance calculation
- Comprehensive testing suite
- Python 3.13 compatibility

## Benefits & Use Cases

### Development Efficiency:
- **Persistent Context**: AI maintains deep understanding across sessions
- **Intelligent Automation**: Smart workflow orchestration
- **Knowledge Accumulation**: Learning from project patterns
- **Consistent Standards**: Rule-based behavior enforcement

### Project Management:
- **State Tracking**: Complete project history and progress
- **Decision Recording**: Technical choices and constraints
- **Context Sharing**: Easy team onboarding
- **Quality Assurance**: Automated documentation and standards

### Advanced AI Capabilities:
- **Multi-hop Reasoning**: Complex problem solving via Knowledge Graph
- **Pattern Recognition**: Learning from accumulated project data
- **Predictive Assistance**: Anticipating needs based on context
- **Error Prevention**: Historical error pattern awareness

## Directory Structure Analysis

### Core System Files:
```
.cursor/
├── CORE/
│   ├── SSOT/                   # Single Source of Truth System
│   │   ├── .ENGINE             # Central workflow orchestrator (156 lines)
│   │   ├── .INIT               # Project initialization (47 lines)
│   │   ├── .CONTEXT            # High-level overview (39 lines)
│   │   ├── .FACTS              # Technical decisions (59 lines)
│   │   ├── .MEMORY             # Component summaries (59 lines)
│   │   ├── .HISTORY            # Activity log (115 lines)
│   │   ├── .CONTINUE           # Next steps (89 lines)
│   │   ├── .PROGRESS           # Task tracking (34 lines)
│   │   └── .PROMPT             # Original description (84 lines)
│   ├── MCP/                    # Model Context Protocol Servers
│   │   ├── knowledge-graph/    # Graph database server
│   │   │   ├── package.json    # v1.0.1, TypeScript implementation
│   │   │   ├── index.ts        # Main server logic (426 lines)
│   │   │   └── dist/           # Compiled JavaScript
│   │   ├── sequentialthinking/ # Advanced reasoning server
│   │   │   ├── package.json    # v0.6.2, Anthropic implementation
│   │   │   ├── index.ts        # Thinking logic (279 lines)
│   │   │   └── dist/           # Compiled JavaScript
│   │   └── filesystem/         # File operations server
│   │       ├── package.json    # v0.6.2, Anthropic implementation
│   │       ├── index.ts        # File system logic (648 lines)
│   │       └── dist/           # Compiled JavaScript
│   ├── RULE-ENGINE/            # Rule staging area (currently empty)
│   ├── MEMORY/                 # Persistent storage
│   │   └── memory.jsonl        # Knowledge Graph storage (empty)
│   ├── PROMPTS/                # System prompts and instructions
│   │   ├── PROMPTS.md          # Trigger documentation (62 lines)
│   │   └── .MEMORIZE           # KG construction guide (233 lines)
│   └── DOCS/                   # Documentation
│       └── .STRUCTURE          # Directory layout guide (27 lines)
├── rules/                      # Active Cursor rules
│   └── 999-mdc-format.mdc     # MDC format guide (137 lines)
├── BACKUP/                     # Backup configurations
│   ├── rules/                  # Rule backups
│   ├── mcp.json               # MCP backup config
│   ├── USER-RULES.md          # User rules backup
│   └── CORE/                  # Core system backups
├── mcp.json                   # MCP server configuration (46 lines)
└── USER-RULES.md              # Core behavioral guidelines (91 lines)
```

### File Size and Content Analysis:
- **Total System Files**: 20+ core configuration files
- **Documentation**: Comprehensive with examples and detailed instructions
- **MCP Servers**: Three fully-implemented TypeScript servers with npm packages
- **SSOT System**: Complete with all required state management files
- **Rule Engine**: Framework in place with staging and production areas

## Technical Implementation Details

### MCP Server Specifications:

#### Knowledge Graph Server:
- **Technology**: TypeScript + Node.js
- **Dependencies**: @modelcontextprotocol/sdk v1.0.1
- **Storage**: JSONL format for persistent memory
- **Capabilities**: Entity-relationship modeling, graph queries, observations

#### Sequential Thinking Server:
- **Technology**: TypeScript + Node.js  
- **Dependencies**: @modelcontextprotocol/sdk v0.5.0, chalk, yargs
- **Capabilities**: Multi-step reasoning, thought revision, problem decomposition

#### Filesystem Server:
- **Technology**: TypeScript + Node.js
- **Dependencies**: @modelcontextprotocol/sdk v0.5.0, diff, glob, minimatch
- **Capabilities**: Enhanced file operations, directory traversal, diff analysis

### Rule Engine Implementation:
- **Format**: Markdown Configuration (MDC) files
- **Frontmatter**: YAML-like configuration with description, globs, alwaysApply
- **Staging**: Rules generated in `RULE-ENGINE/` before manual integration
- **Global vs. Contextual**: Support for both always-applied and context-specific rules

### SSOT System Architecture:
- **Centralized State**: All project knowledge in structured files
- **Trigger-Based**: Workflow automation through chat triggers
- **Versioned History**: Complete audit trail of project evolution
- **Portable State**: Snapshot and restore capabilities

## Troubleshooting

### Common Issues:

#### MCP Server Installation:
- Ensure Node.js is installed
- Check npm permissions
- Verify TypeScript compilation
- Confirm `mcp.json` configuration

#### SSOT Synchronization:
- Use `!!-UPDATE-SSOT-!!` after major changes
- Check file permissions in `.cursor/CORE/SSOT/`
- Verify trigger syntax exactly

#### Knowledge Graph Issues:
- Restart MCP servers if needed
- Check memory.jsonl file accessibility
- Rebuild graph with `!!-BUILD-KG-!!` if corrupted

### Error Recovery:
- **Corrupted SSOT**: Use `!!-LOAD-PORTABLE-!!` if `.PORTABLE` exists
- **Missing MCP Servers**: Re-run `!!-INSTALL-MCP-!!`
- **Knowledge Graph Corruption**: Delete `memory.jsonl` and rebuild with `!!-BUILD-KG-!!`
- **Rule Conflicts**: Check `rules/` directory for syntax errors

## Future Enhancements

### Planned Features:
- Visual Knowledge Graph explorer interface
- Advanced analytics and project metrics
- Integration with popular development tools (VS Code, IntelliJ)
- Multi-language support expansion
- Cloud-based Knowledge Graph synchronization
- Team collaboration features
- CI/CD pipeline integration

### Extension Points:
- Custom MCP server development
- Additional rule types and behaviors
- Enhanced trigger system with parameters
- Plugin architecture for third-party integrations
- Advanced query languages for Knowledge Graph

This SSOT-RULE-ENGINE-TEMPLATE represents a powerful foundation for AI-assisted development, providing intelligent context management, persistent memory, and sophisticated workflow automation. It transforms the traditional development environment into an adaptive, learning system that grows more capable over time. 