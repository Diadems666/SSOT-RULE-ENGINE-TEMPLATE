# Template Manifest

This document lists all components included in the original SSOT Rule Engine template.

## Core Components

### Rule Engine
- Basic rule processing engine
- Rule definition templates
- Rule validation system

### SSOT System
- Core state files
- State synchronization
- Basic version control

### Communication Layer
- Inter-component messaging
- Basic event system
- State updates

## Files and Directories

### Deployment Scripts
- deploy.ps1 (Windows)
- deploy.sh (Unix/Linux/MacOS)
- requirements.txt

### Core Directories
```
.cursor/CORE/RULE_ENGINE/
  __init__.py
  rule_generator.py
  engine_integration.py

.cursor/CORE/SSOT/
  .INIT
  .HISTORY
  .CONTINUE
  .CONTEXT
  .FACTS
  .MEMORY
  .PROGRESS

.cursor/CORE/COMS/
  __init__.py
  message_handler.py
  event_system.py
```

## Dependencies
- Flask
- Flask-CORS
- Python-dotenv
- Requests
- Watchdog
- JSONSchema
- PyYAML

## Version Information
- Template Version: 1.0.0
- Last Updated: 2024-05-07
- Compatibility: Cursor AI v2.0+ 