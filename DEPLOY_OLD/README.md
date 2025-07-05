# SSOT Rule Engine Template (Original Version)

This is the original version of the SSOT Rule Engine template deployment package. It provides a basic setup for integrating the Rule Engine with Cursor AI.

## Features

- Basic Rule Engine integration
- SSOT (Single Source of Truth) system
- Core communication layer
- Simple deployment scripts

## Directory Structure

```
.cursor/
  CORE/
    RULE_ENGINE/  # Core rule engine components
    SSOT/         # Single Source of Truth files
    COMS/         # Communication layer
```

## Installation

### Windows
```powershell
.\deploy.ps1 [targetDir] [-force]
```

### Unix/Linux/MacOS
```bash
./deploy.sh [targetDir] [force]
```

## Requirements

- Python 3.8 or later
- pip package manager
- PowerShell (Windows) or Bash (Unix)

## Configuration

The deployment scripts will:
1. Create necessary directories
2. Copy template files
3. Install Python dependencies
4. Set up basic configuration

## Support

For issues or questions, please refer to the documentation or contact support. 