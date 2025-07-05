#!/bin/bash

# SSOT-RULE-ENGINE-TEMPLATE Deployment Script
# Bash script to deploy the template to a target project

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    echo -e "${1}${2}${NC}"
}

# Function to print usage
usage() {
    echo "Usage: $0 <target_path> [--force]"
    echo "  target_path: Path to the project where you want to deploy the template"
    echo "  --force:     Overwrite existing .cursor directory if it exists"
    echo ""
    echo "Example:"
    echo "  $0 /path/to/your/project"
    echo "  $0 /path/to/your/project --force"
    exit 1
}

# Parse arguments
TARGET_PATH=""
FORCE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --force)
            FORCE=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            if [[ -z "$TARGET_PATH" ]]; then
                TARGET_PATH="$1"
            else
                print_color $RED "Error: Too many arguments"
                usage
            fi
            shift
            ;;
    esac
done

# Validate arguments
if [[ -z "$TARGET_PATH" ]]; then
    print_color $RED "Error: Target path is required"
    usage
fi

print_color $GREEN "🚀 SSOT-RULE-ENGINE-TEMPLATE Deployment Script"
print_color $GREEN "==============================================="

# Validate target path
if [[ ! -d "$TARGET_PATH" ]]; then
    print_color $RED "❌ Error: Target path does not exist: $TARGET_PATH"
    exit 1
fi

# Check if target already has .cursor directory
TARGET_CURSOR_PATH="$TARGET_PATH/.cursor"
if [[ -d "$TARGET_CURSOR_PATH" ]] && [[ "$FORCE" == false ]]; then
    print_color $YELLOW "⚠️  Warning: Target project already has .cursor directory!"
    print_color $YELLOW "Use --force parameter to overwrite, or choose a different target."
    exit 1
fi

print_color $CYAN "📁 Target Project: $TARGET_PATH"
print_color $CYAN "📦 Deploying SSOT-RULE-ENGINE-TEMPLATE..."

# Get the script directory (where DEPLOY folder is)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="$SCRIPT_DIR"

# Copy .cursor directory
print_color $YELLOW "📋 Copying .cursor directory..."
SOURCE_CURSOR_PATH="$DEPLOY_DIR/.cursor"

if [[ -d "$TARGET_CURSOR_PATH" ]]; then
    rm -rf "$TARGET_CURSOR_PATH"
fi

if [[ -d "$SOURCE_CURSOR_PATH" ]]; then
    cp -r "$SOURCE_CURSOR_PATH" "$TARGET_PATH/"
    print_color $GREEN "✅ .cursor directory copied successfully"
else
    print_color $RED "❌ Error: .cursor directory not found in template"
    exit 1
fi

# Copy launch-dashboard.py
print_color $YELLOW "📋 Copying launch-dashboard.py..."
SOURCE_DASHBOARD="$DEPLOY_DIR/launch-dashboard.py"
TARGET_DASHBOARD="$TARGET_PATH/launch-dashboard.py"

if [[ -f "$SOURCE_DASHBOARD" ]]; then
    cp "$SOURCE_DASHBOARD" "$TARGET_DASHBOARD"
    print_color $GREEN "✅ launch-dashboard.py copied successfully"
else
    print_color $YELLOW "⚠️  Warning: launch-dashboard.py not found in template"
fi

# Copy .gitignore if it doesn't exist
SOURCE_GITIGNORE="$DEPLOY_DIR/.gitignore"
TARGET_GITIGNORE="$TARGET_PATH/.gitignore"

if [[ -f "$SOURCE_GITIGNORE" ]] && [[ ! -f "$TARGET_GITIGNORE" ]]; then
    print_color $YELLOW "📋 Copying .gitignore..."
    cp "$SOURCE_GITIGNORE" "$TARGET_GITIGNORE"
    print_color $GREEN "✅ .gitignore copied successfully"
fi

echo ""
print_color $GREEN "🎉 DEPLOYMENT SUCCESSFUL!"
print_color $GREEN "========================="
echo ""
print_color $CYAN "📍 Next Steps:"
print_color $WHITE "1. Navigate to your project: cd \"$TARGET_PATH\""
print_color $WHITE "2. Run the initialization trigger: !!-ADD-.ENGINE-!!"
print_color $WHITE "3. Wait for the analytics dashboard to launch"
print_color $WHITE "4. Access dashboard at: http://localhost:8080"
echo ""
print_color $YELLOW "💡 For help, check the README.md or run: !!-HEALTH-CHECK-!!"

echo ""
print_color $GREEN "🏁 Deployment completed successfully!" 