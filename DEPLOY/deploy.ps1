# SSOT-RULE-ENGINE-TEMPLATE Deployment Script
# PowerShell script to deploy the template to a target project

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetPath,
    
    [Parameter(Mandatory=$false)]
    [switch]$Force = $false
)

Write-Host "🚀 SSOT-RULE-ENGINE-TEMPLATE Deployment Script" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

# Validate target path
if (-not (Test-Path $TargetPath)) {
    Write-Host "❌ Error: Target path does not exist: $TargetPath" -ForegroundColor Red
    exit 1
}

# Check if target already has .cursor directory
$targetCursorPath = Join-Path $TargetPath ".cursor"
if ((Test-Path $targetCursorPath) -and -not $Force) {
    Write-Host "⚠️  Warning: Target project already has .cursor directory!" -ForegroundColor Yellow
    Write-Host "Use -Force parameter to overwrite, or choose a different target." -ForegroundColor Yellow
    exit 1
}

Write-Host "📁 Target Project: $TargetPath" -ForegroundColor Cyan
Write-Host "📦 Deploying SSOT-RULE-ENGINE-TEMPLATE..." -ForegroundColor Cyan

try {
    # Get the script directory (where DEPLOY folder is)
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $deployDir = $scriptDir
    
    # Copy .cursor directory
    Write-Host "📋 Copying .cursor directory..." -ForegroundColor Yellow
    $sourceCursorPath = Join-Path $deployDir ".cursor"
    
    if (Test-Path $targetCursorPath) {
        Remove-Item $targetCursorPath -Recurse -Force
    }
    
    Copy-Item $sourceCursorPath $TargetPath -Recurse -Force
    Write-Host "✅ .cursor directory copied successfully" -ForegroundColor Green
    
    # Copy launch-dashboard.py
    Write-Host "📋 Copying launch-dashboard.py..." -ForegroundColor Yellow
    $sourceDashboard = Join-Path $deployDir "launch-dashboard.py"
    $targetDashboard = Join-Path $TargetPath "launch-dashboard.py"
    
    if (Test-Path $sourceDashboard) {
        Copy-Item $sourceDashboard $targetDashboard -Force
        Write-Host "✅ launch-dashboard.py copied successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Warning: launch-dashboard.py not found in template" -ForegroundColor Yellow
    }
    
    # Copy .gitignore if it doesn't exist
    $sourceGitignore = Join-Path $deployDir ".gitignore"
    $targetGitignore = Join-Path $TargetPath ".gitignore"
    
    if ((Test-Path $sourceGitignore) -and -not (Test-Path $targetGitignore)) {
        Write-Host "📋 Copying .gitignore..." -ForegroundColor Yellow
        Copy-Item $sourceGitignore $targetGitignore -Force
        Write-Host "✅ .gitignore copied successfully" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "🎉 DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
    Write-Host "=========================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 Next Steps:" -ForegroundColor Cyan
    Write-Host "1. Navigate to your project: cd `"$TargetPath`"" -ForegroundColor White
    Write-Host "2. Run the initialization trigger: !!-ADD-.ENGINE-!!" -ForegroundColor White
    Write-Host "3. Wait for the analytics dashboard to launch" -ForegroundColor White
    Write-Host "4. Access dashboard at: http://localhost:8080" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 For help, check the README.md or run: !!-HEALTH-CHECK-!!" -ForegroundColor Yellow
    
} catch {
    Write-Host "❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🏁 Deployment completed successfully!" -ForegroundColor Green 