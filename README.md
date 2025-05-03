# Cursor AI SSOT, Rule Engine, and MCP Template System

This template provides a structured foundation for leveraging Cursor AI's advanced features – specifically the Single Source of Truth (SSOT), Project Rules, and Model Context Protocol (MCP) with a Knowledge Graph – within your projects. It includes necessary directories, initial configuration files, and core instruction files for the AI agent, designed for easy integration into new or existing codebases and suitable for GitHub.

## 🚀 Features

* **Centralized AI Logic:** Core setup and workflow instructions are consolidated in `./.cursor/CORE/SSOT/.ENGINE`.
* **Dual Initialization:** Supports setting up the system in a **new project** (via prompt description) or integrating into an **existing project** (via codebase analysis).
* **MCP Integration:** Includes structure and commands for installing and configuring standard MCP servers (Knowledge Graph, Sequential Thinking, Filesystem).
* **Knowledge Graph Building:** Provides a workflow to build an initial Knowledge Graph representation of your project codebase using the installed MCP server.
* **SSOT Management:** Defines a core SSOT file structure (`.INIT`, `.HISTORY`, `.CONTINUE`, `.CONTEXT`, `.FACTS`, `.MEMORY`, `.PROGRESS`) for project state tracking.
* **Staged Project Rules:** Generated project-specific `.mdc` rules are placed in a staging directory (`./.cursor/CORE/RULE-ENGINE/`) for manual review and integration into `./.cursor/rules/`.
* **Command Reference:** Includes a simple file (`./.cursor/CORE/COMS/.COMS`) listing available AI command triggers for easy access.
* **Containerized Configuration:** Places core system configuration (`mcp.json`) within the `.cursor` directory.
* **GitHub Ready:** Designed with version control in mind, excluding common build artifacts and potentially sensitive paths via `.gitignore` (not included in template, must be added per project).

## 📂 Template Structure

This template provides the following directory and file structure within your project's root:
```
.cursor/
├── CORE/
│ ├── COMS/ # AI Commands & Documentation
│ │ ├── .COMS # User-friendly command list
│ │ └── .COMS-ENGINE # AI documentation for commands (Logic defined in .ENGINE)
│ ├── MCP/ # MCP Server Directories (initially empty, npm install needed)
│ │ ├── filesystem/
│ │ ├── knowledge-graph/
│ │ └── sequentialthinking/
│ ├── MEMORY/ # Persistent Memory Storage (JSONL Knowledge Graph backup)
│ │ └── memory.jsonl # Primary memory file
│ ├── PROMPTS/ # Storage for initial prompt, etc.
│ │ └── .PROMPT # Created by !!-INIT-.ENGINE-!!
│ ├── RULE-ENGINE/ # Staging area for AI-generated .mdc rules
│ └── SSOT/ # Single Source of Truth files
│ ├── .ENGINE # CENTRAL Setup & Workflow Logic
│ ├── .CONTINUE # Next steps/focus
│ ├── .CONTEXT # High-level overview
│ ├── .FACTS # Technical decisions/constraints
│ ├── .HISTORY # Timestamped action log
│ ├── .INIT # Initial directives from setup
│ ├── .MEMORY # Structured project entities/details
│ └── .PROGRESS # Task completion status
├── rules/ # Standard Cursor Project Rules directory (Manual Integration Target)
│ └── 999-mdc-format.mdc # Guide for MDC format (Copy from ./CORE/RULE-ENGINE)
└── USER-RULES.md # Rules to copy to Cursor AI settings
└── mcp.json # MCP Server Configuration
└── .cursorrules # Legacy rules file (minimal pointer)
```
## 🛠️ Getting Started

1. **Copy Template:** Copy the entire `.cursor` directory from this template into the root of your new or existing project. Copy the contents of `USER-RULES.md` to the User-Rules in Cursor AI settings panel (Settings > Cursor AI > User Rules).

2. **Configure `mcp.json`:** Open `./.cursor/mcp.json` and review the configuration. **Crucially, update the `"backup-dir"` path for the `memory` server to a location appropriate for your operating system and preferences.**

3. **Initial SSOT/Rule Engine Setup:**
   * **New Project (from Description):** In your Cursor chat, provide a detailed project description, then on a new line, type `!!-INIT-.ENGINE-!!`.
   * **Existing Project (from Codebase Analysis):** In your Cursor chat for the project, type `!!-ADD-.ENGINE-!!`.
   
   *(The AI will create directories, populate initial SSOT files, handle the legacy rule, and place generated rules in `./.cursor/CORE/RULE-ENGINE/`)*

4. **Manually Integrate Rules:** Review the `.mdc` files generated and placed in `./.cursor/CORE/RULE-ENGINE/`. Copy the ones you want to actively use into `./.cursor/rules/`. You may need to edit them or the base `999-mdc-format.mdc` in `./.cursor/rules/` to fit your preferences.

5. **Install MCP Servers:** Once the initial setup is confirmed complete, type `!!-INSTALL-MCP-!!` in your Cursor chat.
   
   *(The AI will attempt to run `npm install` in the MCP server subdirectories. Be prepared to grant administrator permissions if prompted by your OS/npm setup.)*

6. **Restart & Build Knowledge Graph:** After `!!-INSTALL-MCP-!!` confirms completion, restart Cursor to ensure `mcp.json` is loaded and servers can start. Then, type `!!-BUILD-KG-!!` in your Cursor chat.
   
   *(The AI will perform a comprehensive codebase analysis and build the initial Knowledge Graph in the running MCP memory server.)*

7. **Explore Commands:** Refer to the Available Commands section below for a list of commands you can use in the Cursor chat to interact with the system.

## 📝 Available Commands

Here are the key commands you can use in the Cursor chat:

### System Setup Commands

| Command | Description |
|---------|-------------|
| `!!-INIT-.ENGINE-!!` | Initialize the system in a **new project**. Provide a detailed project description in the chat **before** this command. |
| `!!-ADD-.ENGINE-!!` | Integrate the system into an **existing project**. The AI will analyze your codebase. |
| `!!-INSTALL-MCP-!!` | Install MCP servers (Knowledge Graph, etc.). Run after initialization. Ensures `mcp.json` is properly configured. |
| `!!-BUILD-KG-!!` | Build the initial Knowledge Graph from codebase analysis. Run after installing MCP and restarting Cursor. |

### State & Context Commands

| Command | Description |
|---------|-------------|
| `!!-LOAD-PORTABLE-!!` | Load project state, SSOT files, and potentially populate Knowledge Graph from `./.cursor/CORE/SSOT/.PORTABLE`. |
| `!!-UPDATE-SSOT-!!` | Update SSOT files based on recent changes. Use after completing tasks. |
| `!!-CREATE-PORTABLE-!!` | Create a snapshot of current project state for transfer or backup. |
| `!!-CREATE-CHAT-HISTORY-!!` | Copy current chat history into `./.cursor/CORE/SSOT/.CHAT`. |

### Maintenance & Documentation Commands

| Command | Description |
|---------|-------------|
| `!!-UPDATE-DOCS-!!` | Analyze project state and update documentation, including README.md and code comments. |
| `!!-PREPARE-GITHUB-!!` | Analyze project for GitHub readiness - update .gitignore, check for sensitive data, and verify documentation. |

For the complete list and detailed documentation, see `./.cursor/CORE/COMS/.COMS` in your project.

## ⚙️ Additional Configuration

### Setting up .gitignore

To properly set up your repository for GitHub, make sure to add the following to your `.gitignore` file:

# Ignore BACKUP directory
.cursor/BACKUP/

# Node.js dependencies
node_modules/

# Build outputs
dist/
build/

# Logs
*.log
logs/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

## 👥 Contributing

This template is designed to be a starting point. Feel free to fork, modify, and enhance it for your specific workflows and project types. Contributions to improve the core `.ENGINE` logic, add more sophisticated rule generation, or support additional MCP servers are welcome.

## 📜 License

MIT License

Copyright (c) 2023 [Your Name or Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

You can also run the `!!-PREPARE-GITHUB-!!` command to automatically analyze your project and configure an appropriate `.gitignore` file.

## GitHub About Section

### Project Description
Cursor AI SSOT & Rule Engine Template: A comprehensive framework for integrating Cursor AI's advanced features into any project. Includes Single Source of Truth (SSOT) tracking, custom project rules, and Model Context Protocol (MCP) with Knowledge Graph for intelligent context management.

### Topics
- cursor-ai
- knowledge-graph
- ai-assistant
- mcp-server
- ssot
- rule-engine
- development-tools
- productivity
- code-intelligence
- project-management
- documentation-automation