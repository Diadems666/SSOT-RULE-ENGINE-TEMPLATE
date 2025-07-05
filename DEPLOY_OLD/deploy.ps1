# SSOT Rule Engine Deployment Script (Windows)
param(
    [string]$targetDir = ".",
    [switch]$force = $false
)

# Configuration
$templateRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$coreDirectories = @(
    ".cursor/CORE/RULE_ENGINE",
    ".cursor/CORE/SSOT",
    ".cursor/CORE/COMS"
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

# Create directories
foreach ($dir in $coreDirectories) {
    $path = Join-Path $targetDir $dir
    if (-not (Test-Path $path)) {
        Write-Host "Creating directory: $path"
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

# Copy template files
Write-Host "Copying template files..."
Copy-Item -Path (Join-Path $templateRoot ".cursor/CORE/RULE_ENGINE/*") -Destination (Join-Path $targetDir ".cursor/CORE/RULE_ENGINE/") -Recurse -Force
Copy-Item -Path (Join-Path $templateRoot ".cursor/CORE/SSOT/*") -Destination (Join-Path $targetDir ".cursor/CORE/SSOT/") -Recurse -Force
Copy-Item -Path (Join-Path $templateRoot ".cursor/CORE/COMS/*") -Destination (Join-Path $targetDir ".cursor/CORE/COMS/") -Recurse -Force

# Install dependencies
Write-Host "Installing Python dependencies..."
pip install -r (Join-Path $templateRoot "requirements.txt")

Write-Host "SSOT Rule Engine template deployed successfully!" 