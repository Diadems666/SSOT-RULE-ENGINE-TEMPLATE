# Cursor AI Agent Prompts (Enhanced for SSOT/MCP/Rules)

## --- Core System Setup ---

!! - INIT SSOT & RULE ENGINE - !!
# Usage: Provide a detailed project description in the chat immediately BEFORE using this trigger. Initializes SSOT (.PROMPT, .INIT, etc.) and Rule Engine based on the description. Creates core directory structure (including for MCP).

!! - ADD SSOT & RULE ENGINE - !!
# Usage: Use on an existing project WITHOUT a preceding description. Initiates SSOT and Rule Engine setup based on comprehensive codebase analysis. Creates core directory structure (including for MCP).

!! - INSTALL MCP - !!
# Usage: Use AFTER initial SSOT/Rule Engine setup (INIT or ADD) is complete. Installs MCP servers (knowledge-graph, sequentialthinking, filesystem) via npm and configures './mcp.json'. Requires './.cursor/CORE/MCP/' subdirectories to exist.

## --- State Synchronization & Context Loading ---

!! - LOAD .PORTABLE - !!
# Usage: Instructs the AI to:
# 1. Read and parse the './.cursor/CORE/SSOT/.PORTABLE' file.
# 2. Populate/overwrite the current project's SSOT files (.CONTEXT, .FACTS, .MEMORY, .HISTORY, .CONTINUE, etc.) based *solely* on the information within .PORTABLE.
# 3. [Optional/Advanced] If the MCP knowledge-graph server is running and configured, attempt to populate it based on entities/relationships described in .PORTABLE.
# 4. Acknowledge completion and confirm readiness to proceed based on the loaded state.

## --- Development & Task Execution ---

Please consult the current development plan in `./.cursor/CORE/SSOT/.CONTINUE`, the high-level overview in `.CONTEXT`, key decisions in `.FACTS`, project details in `.MEMORY` (and potentially querying the MCP knowledge-graph for relevant entities/relationships if active), and all applicable project rules in `./.cursor/rules/`. Then, proceed with the next logical development step or task as outlined in `.CONTINUE`. Upon completing a significant work unit, please report progress and update the relevant SSOT files (`.HISTORY`, `.FACTS`, `.MEMORY`, `.CONTINUE`).

## --- System Maintenance & Updates ---

Based on the recent changes/completed task [Optional: briefly describe task, e.g., "after implementing feature X"], please update the SSOT system state. This involves:
1.  Appending a descriptive entry to `.HISTORY`.
2.  Updating `.FACTS` with any new significant technical decisions, constraints, or architectural changes.
3.  Refining project `.MEMORY` with details about new/modified components, files, or concepts.
4.  [Optional/Advanced] Interacting with the active MCP knowledge-graph server (via its defined protocol) to update its representation of the project state based on these changes.
5.  Reviewing and potentially updating the high-level `.CONTEXT` overview.
6.  Defining the next logical task or focus area in `.CONTINUE`.
Confirm when SSOT and relevant MCP updates (if applicable) are complete.

Please perform a comprehensive analysis of the entire project state by synthesizing information from:
1.  All SSOT files (`.INIT`, `.HISTORY`, `.CONTINUE`, `.CONTEXT`, `.FACTS`, `.MEMORY`, `.PROMPT` if exists, `.CHAT` if exists).
2.  All project rules (`./.cursor/rules/*.mdc`).
3.  The entire codebase and file structure.
4.  Current MCP configuration (`mcp.json`).
5.  [Optional/Advanced] Queryable state from active MCP servers (especially knowledge-graph).
6.  Core setup instructions (`.ENGINE`, `.MCP-ENGINE`).
Based on this complete synthesis, create or update the `./.cursor/CORE/SSOT/.PORTABLE` file. Ensure it contains a thorough, self-contained snapshot suitable for onboarding a new AI agent or transferring the project context. Confirm when the `.PORTABLE` file is ready.

Please create and/or update the `./.cursor/CORE/SSOT/.CHAT` file with a complete copy of our current chat history (both user and agent messages up to this point).

## --- Documentation & Repository Management ---

Please review the project's current state based on SSOT files (`.CONTEXT`, `.FACTS`, `.MEMORY`), project rules (`./.cursor/rules/`), and direct codebase analysis. Then, create or update detailed project documentation, focusing on:
1.  Ensuring the main `README.md` provides an accurate overview, setup guide (referencing triggers like `!! - INSTALL MCP - !!` if applicable), and usage examples, reflecting the state in `.CONTEXT` and `.FACTS`.
2.  Adding/updating code comments (docstrings, block comments) for public APIs, complex algorithms, or non-obvious logic sections, consistent with project rules.
3.  [Optional] Generating or updating architecture descriptions/diagrams (e.g., in a `docs/` folder) based on `.FACTS` and code structure.
Confirm when documentation updates aligned with the current project state are complete.

Please prepare the project for upload to GitHub. Perform the following actions, ensuring consistency with SSOT files and project rules:
1.  Analyze the codebase and working directory for temporary files, sensitive data (keys, passwords), build artifacts, or logs that should not be committed.
2.  Review and update the `.gitignore` file comprehensively based on the project's technologies (identified via SSOT `.FACTS` or analysis) and the findings from step 1.
3.  Verify the main `README.md` and other core documentation are current (consider running the documentation update prompt first if unsure).
4.  [Optional: Run linters, formatters, or pre-commit checks defined in project rules or common practices].
5.  Report any potential issues found and confirm when the project workspace is clean and ready for staging commits.