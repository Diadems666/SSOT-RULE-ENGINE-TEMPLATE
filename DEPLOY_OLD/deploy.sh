#!/bin/bash

# SSOT Rule Engine Deployment Script (Unix)

# Default target directory is current directory
TARGET_DIR=${1:-.}
FORCE=${2:-false}

# Get script directory
TEMPLATE_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Core directories to create
CORE_DIRS=(
    ".cursor/CORE/RULE_ENGINE"
    ".cursor/CORE/SSOT"
    ".cursor/CORE/COMS"
)

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null || ! command -v pip3 &> /dev/null; then
    echo "Error: Python 3.8+ or pip not found"
    exit 1
fi

# Create directories
for dir in "${CORE_DIRS[@]}"; do
    path="$TARGET_DIR/$dir"
    if [ ! -d "$path" ]; then
        echo "Creating directory: $path"
        mkdir -p "$path"
    fi
done

# Copy template files
echo "Copying template files..."
cp -rf "$TEMPLATE_ROOT/.cursor/CORE/RULE_ENGINE/"* "$TARGET_DIR/.cursor/CORE/RULE_ENGINE/"
cp -rf "$TEMPLATE_ROOT/.cursor/CORE/SSOT/"* "$TARGET_DIR/.cursor/CORE/SSOT/"
cp -rf "$TEMPLATE_ROOT/.cursor/CORE/COMS/"* "$TARGET_DIR/.cursor/CORE/COMS/"

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r "$TEMPLATE_ROOT/requirements.txt"

echo "SSOT Rule Engine template deployed successfully!" 