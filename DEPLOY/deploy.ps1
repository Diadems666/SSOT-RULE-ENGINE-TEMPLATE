# SSOT Rule Engine Deployment Script (Windows)
param(
    [string]$targetDir = ".",
    [switch]$force = $false
)

# Configuration
$templateRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$coreDirectories = @(
    ".cursor/CORE/RULE-ENGINE",
    ".cursor/CORE/ANALYTICS",
    ".cursor/CORE/SSOT",
    ".cursor/CORE/MCP",
    ".cursor/CORE/MEMORY",
    ".cursor/CORE/PROMPTS"
)
$configFiles = @(
    "mcp.json",
    ".cursor/CORE/RULE-ENGINE/config.json",
    ".cursor/CORE/ANALYTICS/config.json"
)

# Verify Python installation
Write-Host "Checking Python installation..."
try {
    python --version
    pip --version
} catch {
    Write-Error "Python or pip not found. Please install Python 3.8 or later."
    exit 1
}

# Verify Node.js installation
Write-Host "Checking Node.js installation..."
try {
    node --version
    npm --version
} catch {
    Write-Error "Node.js or npm not found. Please install Node.js 14 or later."
    exit 1
}

# Create directory structure
Write-Host "Creating directory structure..."
foreach ($dir in $coreDirectories) {
    $path = Join-Path $targetDir $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

# Copy template files
Write-Host "Copying template files..."
Copy-Item -Path "$templateRoot/.cursor/CORE/RULE-ENGINE/*" -Destination "$targetDir/.cursor/CORE/RULE-ENGINE/" -Recurse -Force
Copy-Item -Path "$templateRoot/.cursor/CORE/ANALYTICS/*" -Destination "$targetDir/.cursor/CORE/ANALYTICS/" -Recurse -Force
Copy-Item -Path "$templateRoot/.cursor/CORE/SSOT/*" -Destination "$targetDir/.cursor/CORE/SSOT/" -Recurse -Force
Copy-Item -Path "$templateRoot/.cursor/CORE/MCP/*" -Destination "$targetDir/.cursor/CORE/MCP/" -Recurse -Force
Copy-Item -Path "$templateRoot/mcp.json" -Destination "$targetDir/" -Force

# Install Python dependencies
Write-Host "Installing Python dependencies..."
pip install -r "$templateRoot/requirements.txt"

# Install Node.js dependencies (if any)
if (Test-Path "$targetDir/package.json") {
    Write-Host "Installing Node.js dependencies..."
    Push-Location $targetDir
    npm install --yes
    Pop-Location
}

# Initialize SSOT system
Write-Host "Initializing SSOT system..."
Copy-Item -Path "$templateRoot/.cursor/CORE/SSOT/.INIT.template" -Destination "$targetDir/.cursor/CORE/SSOT/.INIT" -Force
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path "$targetDir/.cursor/CORE/SSOT/.HISTORY" -Value "[$timestamp] Initial deployment"

# Configure MCP
Write-Host "Configuring MCP..."
if (-not (Test-Path "$targetDir/mcp.json")) {
    Copy-Item -Path "$templateRoot/mcp.json" -Destination "$targetDir/" -Force
}

# Generate initial rules
Write-Host "Generating initial rules..."
python -c "from cursor.core.rule_engine import generate_initial_rules; generate_initial_rules()"

# Launch dashboard
Write-Host "Launching dashboard..."
Start-Process python -ArgumentList "$targetDir/launch-dashboard.py"

Write-Host "Deployment complete! The dashboard should now be accessible at http://localhost:5000" 