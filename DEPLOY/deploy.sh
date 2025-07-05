#!/bin/bash

# SSOT Rule Engine Deployment Script (Unix)

# Default target directory is current directory
TARGET_DIR=${1:-.}
FORCE=${2:-false}

# Get script directory
TEMPLATE_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Core directories to create
CORE_DIRS=(
    ".cursor/CORE/RULE-ENGINE"
    ".cursor/CORE/ANALYTICS"
    ".cursor/CORE/SSOT"
    ".cursor/CORE/MCP"
    ".cursor/CORE/MEMORY"
    ".cursor/CORE/PROMPTS"
)

# Config files
CONFIG_FILES=(
    "mcp.json"
    ".cursor/CORE/RULE-ENGINE/config.json"
    ".cursor/CORE/ANALYTICS/config.json"
)

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo "Error: Python 3.8+ or pip not found"
    exit 1
fi

# Check Node.js installation
echo "Checking Node.js installation..."
if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
    echo "Error: Node.js 14+ or npm not found"
    exit 1
fi

# Create directory structure
echo "Creating directory structure..."
for dir in "${CORE_DIRS[@]}"; do
    mkdir -p "$TARGET_DIR/$dir"
done

# Copy template files
echo "Copying template files..."
cp -r "$TEMPLATE_ROOT/.cursor/CORE/RULE-ENGINE/"* "$TARGET_DIR/.cursor/CORE/RULE-ENGINE/"
cp -r "$TEMPLATE_ROOT/.cursor/CORE/ANALYTICS/"* "$TARGET_DIR/.cursor/CORE/ANALYTICS/"
cp -r "$TEMPLATE_ROOT/.cursor/CORE/SSOT/"* "$TARGET_DIR/.cursor/CORE/SSOT/"
cp -r "$TEMPLATE_ROOT/.cursor/CORE/MCP/"* "$TARGET_DIR/.cursor/CORE/MCP/"
cp "$TEMPLATE_ROOT/mcp.json" "$TARGET_DIR/"

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r "$TEMPLATE_ROOT/requirements.txt"

# Install Node.js dependencies (if any)
if [ -f "$TARGET_DIR/package.json" ]; then
    echo "Installing Node.js dependencies..."
    (cd "$TARGET_DIR" && npm install --yes)
fi

# Initialize SSOT system
echo "Initializing SSOT system..."
cp "$TEMPLATE_ROOT/.cursor/CORE/SSOT/.INIT.template" "$TARGET_DIR/.cursor/CORE/SSOT/.INIT"
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$timestamp] Initial deployment" >> "$TARGET_DIR/.cursor/CORE/SSOT/.HISTORY"

# Configure MCP
echo "Configuring MCP..."
if [ ! -f "$TARGET_DIR/mcp.json" ]; then
    cp "$TEMPLATE_ROOT/mcp.json" "$TARGET_DIR/"
fi

# Generate initial rules
echo "Generating initial rules..."
python3 -c "from cursor.core.rule_engine import generate_initial_rules; generate_initial_rules()"

# Launch dashboard
echo "Launching dashboard..."
python3 "$TARGET_DIR/launch-dashboard.py" &

echo "Deployment complete! The dashboard should now be accessible at http://localhost:5000" 