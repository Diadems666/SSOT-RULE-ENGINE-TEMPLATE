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

.cursor/
├── CORE/
│   ├── COMS/               # AI Commands & Documentation
│   │   ├── .COMS           # User-friendly command list
│   │   └── .COMS-ENGINE    # AI documentation for commands (Logic defined in .ENGINE)
│   ├── MCP/                # MCP Server Directories (initially empty, npm install needed)
│   │   ├── filesystem/
│   │   ├── knowledge-graph/
│   │   └── sequentialthinking/
│   ├── MEMORY/             # Persistent Memory Storage (JSONL Knowledge Graph backup)
│   │   └── memory.jsonl    # Primary memory file
│   ├── PROMPTS/            # Storage for initial prompt, etc.
│   │   └── .PROMPT         # Created by !! - INIT SSOT & RULE ENGINE - !!
│   ├── RULE-ENGINE/        # Staging area for AI-generated .mdc rules
│   └── SSOT/               # Single Source of Truth files
│       ├── .ENGINE         # CENTRAL Setup & Workflow Logic
│       ├── .CONTINUE       # Next steps/focus
│       ├── .CONTEXT        # High-level overview
│       ├── .FACTS          # Technical decisions/constraints
│       ├── .HISTORY        # Timestamped action log
│       ├── .INIT           # Initial directives from setup
│       ├── .MEMORY         # Structured project entities/details
│       └── .PROGRESS       # Task completion status
├── rules/                  # Standard Cursor Project Rules directory (Manual Integration Target)
│   └── 999-mdc-format.mdc  # Guide for MDC format (Copy from ./CORE/RULE-ENGINE)
└── USER-RULES.md           # Rules to copy to Cursor AI settings
└── mcp.json                # MCP Server Configuration
└── .cursorrules            # Legacy rules file (minimal pointer)

## 🛠️ Getting Started

1. **Copy Template:** Copy the entire `.cursor` directory from this template into the root of your new or existing project. Copy the `mcp.json` file to the root of your project. Copy the contents of `USER-RULES.md` to the User-Rules in Cursor AI settings.

2. **Configure `mcp.json`:** Open `mcp.json` and review the configuration. **Crucially, update the `"backup-dir"` path for the `memory` server to a location appropriate for your operating system and preferences.**

3. **Initial SSOT/Rule Engine Setup:**
   * **New Project (from Description):** In your Cursor chat, provide a detailed project description, then on a new line, type `!! - INIT SSOT & RULE ENGINE - !!`.
   * **Existing Project (from Codebase Analysis):** In your Cursor chat for the project, type `!! - ADD SSOT & RULE ENGINE - !!`.
   
   *(The AI will create directories, populate initial SSOT files, handle the legacy rule, and place generated rules in `./.cursor/CORE/RULE-ENGINE/`)*

4. **Manually Integrate Rules:** Review the `.mdc` files generated and placed in `./.cursor/CORE/RULE-ENGINE/`. Copy the ones you want to actively use into `./.cursor/rules/`. You may need to edit them or the base `999-mdc-format.mdc` in `./.cursor/rules/` to fit your preferences.

5. **Install MCP Servers:** Once the initial setup is confirmed complete, type `!! - INSTALL MCP - !!` in your Cursor chat.
   
   *(The AI will attempt to run `npm install` in the MCP server subdirectories. Be prepared to grant administrator permissions if prompted by your OS/npm setup.)*

6. **Restart & Build Knowledge Graph:** After `!! - INSTALL MCP - !!` confirms completion, restart Cursor to ensure `mcp.json` is loaded and servers can start. Then, type `!! - BUILD KG - !!` in your Cursor chat.
   
   *(The AI will perform a comprehensive codebase analysis and build the initial Knowledge Graph in the running MCP memory server.)*

7. **Explore Commands:** Refer to `./.cursor/CORE/COMS/.COMS` for a list of other available commands you can use in chat to interact with the system (e.g., updating SSOT, creating portable state).

## 📝 Available Commands

See the `./.cursor/CORE/COMS/.COMS` file in your project for a list of commands you can copy and paste into the Cursor chat.

## 👥 Contributing

This template is designed to be a starting point. Feel free to fork, modify, and enhance it for your specific workflows and project types. Contributions to improve the core `.ENGINE` logic, add more sophisticated rule generation, or support additional MCP servers are welcome.

## 📜 License

[Specify your desired license, e.g., MIT, Apache 2.0, etc.]