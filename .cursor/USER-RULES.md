# Core AI Behavior & Workflow Management
- Recognize and strictly follow directives within the project's core system files (e.g., in ./.cursor/CORE/SSOT/).
- Understand that specific triggers initiate system setup workflows, and the instructions for THESE workflows are centralized in ./.cursor/CORE/SSOT/.ENGINE.
- When encountering '!! - INIT SSOT & RULE ENGINE - !!' or '!! - ADD SSOT & RULE ENGINE - !!', immediately consult and execute the relevant steps defined within ./.cursor/CORE/SSOT/.ENGINE for the specific trigger identified.

# Memory Management
- Before starting a task, access and summarize relevant information stored in project memory (e.g., ./.cursor/CORE/SSOT/.MEMORY and any user-specific memory). State "Consulting project memory..."
- Reference retrieved knowledge as "project memory" or "stored context".
- Upon task completion or at natural breakpoints:
  1. Identify new key entities (components, concepts, files).
  2. Define relationships between entities or with existing knowledge.
  3. Store these findings concisely in ./.cursor/CORE/SSOT/.MEMORY.
  4. Record observations about the task or new learnings.

# SSOT State System & Consistency
- All project knowledge converges in the SSOT files located at ./.cursor/CORE/SSOT/.
- The specific files present and their contents reflect either the initial project prompt (.PROMPT file, created only during INIT workflow) or the derived state from codebase analysis.
- ./.cursor/CORE/SSOT/.ENGINE contains the instructions for how the SSOT/Rule Engine system itself is initially set up or added to a project, dictating the steps based on the trigger used.
- After any significant action (including initial setup/analysis as per .ENGINE), update .HISTORY with a timestamp and brief description.
- Keep .CONTINUE current with the next primary focus area or task.
- Maintain .CONTEXT as a high-level overview of the project's current state and scope.
- Record significant technical decisions, constraints, or discoveries in .FACTS.
- Continuously update .MEMORY with details about project entities, components, and their state.
- Track ongoing task completion status and milestones in .PROGRESS.
- Ensure consistency and cross-referencing between relevant SSOT files when changes occur.
- SSOT files are the primary source for understanding the project's current state, history, and planned direction, regardless of how they were initially populated.

# Project Setup & Initialization Trigger Handling
- This rule defines how the AI reacts to setup triggers by delegating the detailed execution to ./.cursor/CORE/SSOT/.ENGINE.
- When the trigger '!! - INIT SSOT & RULE ENGINE - !!' is received, the AI MUST execute the 'INIT' workflow defined in ./.cursor/CORE/SSOT/.ENGINE. This workflow involves processing the preceding chat prompt description, saving the full original chat input to ./.cursor/CORE/SSOT/.PROMPT, and populating SSOT files from that description.
- When the trigger '!! - ADD SSOT & RULE ENGINE - !!' is received, the AI MUST execute the 'ADD' workflow defined in ./.cursor/CORE/SSOT/.ENGINE. This workflow involves performing comprehensive codebase analysis. As part of that workflow (defined in .ENGINE), perform a recursive examination of all project files, identify technologies, architecture, components, dependencies, patterns, and existing documentation to build the project understanding necessary for SSOT population and rule generation *as directed by .ENGINE*. Do NOT create a .PROMPT file for this workflow.
- For either workflow, the AI must adhere to the directory creation, .cursorrules handling, .mdc rule generation, and workflow rule updating steps also defined in ./.cursor/CORE/SSOT/.ENGINE.
- Only ask for clarification if absolutely necessary *after* attempting to execute the instructions in ./.cursor/CORE/SSOT/.ENGINE and process the required input source (prompt description for INIT, codebase analysis for ADD).

# Development Process & Rule Adherence
- Before starting any development task, read and internalize relevant SSOT files (.CONTINUE, .CONTEXT, .FACTS, .MEMORY), applicable project rules (.mdc in ./.cursor/rules/), and understand the setup source/instructions (.PROMPT if it exists, and .ENGINE).
- Refer back to the SSOT files if the task's purpose or original requirements/inferred structure are unclear.
- Plan work based on the current state defined in SSOT.
- After completing significant work units or making key decisions, report changes made to relevant SSOT files.
- Maintain continuous project context across interactions by referencing SSOT and rule-derived knowledge.
- Ensure all generated code and documentation adheres to project conventions outlined in SSOT (.FACTS) and .mdc rules.
- Reference past decisions recorded in .FACTS and .HISTORY to avoid revisiting resolved issues.
- Proactively identify opportunities to update SSOT or create new .mdc rules based on recurring patterns or decisions.

# Troubleshooting and Debugging Assistance
- When assisting with errors or unexpected behavior, first consult relevant SSOT files (.CONTEXT, .FACTS, .MEMORY) and applicable project rules for clues about the intended or current system state or known issues. Reference .PROMPT or .ENGINE if the issue seems related to initial setup or structure derived from analysis.
- Ask clarifying questions to narrow down the scope of the problem.
- Propose debugging steps based on the error context and project knowledge.
- Upon resolution, update relevant SSOT files (.HISTORY, .FACTS, .MEMORY) if new information or decisions emerge from the process.

# System Learning and Rule Maintenance
- Continuously learn from project interactions, user feedback, and outcomes.
- If a recurring task or pattern of instructions emerges that is not covered by existing rules, suggest creating a new .mdc project rule.
- If an existing rule is unclear, ineffective, or contradictory based on practical application, suggest reviewing and updating it, referencing ./.cursor/rules/999-mdc-format.mdc for guidance.
- Periodically review the SSOT files and rules for consistency and relevance.