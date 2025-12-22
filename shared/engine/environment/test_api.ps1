# PowerShell Script for API Testing
# Usage: powershell -ExecutionPolicy Bypass -File test_api.ps1 YOUR_API_KEY
# Or: .\test_api.ps1 YOUR_API_KEY

param(
    [Parameter(Mandatory=$true)]
    [string]$ApiKey
)

Write-Host "="*60 -ForegroundColor Cyan
Write-Host "Environment Chapter PPTX - API Test" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan
Write-Host ""

# Change to script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Working Directory: $scriptDir" -ForegroundColor Green
Write-Host "API Key: $($ApiKey.Substring(0,10))...$($ApiKey.Substring($ApiKey.Length-4))" -ForegroundColor Green
Write-Host ""

# Test mode selection
Write-Host "Select Test Mode:" -ForegroundColor Yellow
Write-Host "  1. Quick LLM Test (Fast)" -ForegroundColor White
Write-Host "  2. Full PPTX Generation (Takes longer)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1 or 2)"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "[Quick LLM Test]" -ForegroundColor Cyan
    Write-Host "Testing API connection and content generation..." -ForegroundColor Gray
    
    $env:ANTHROPIC_API_KEY = $ApiKey
    python test_api_quick.py $ApiKey
    
} elseif ($choice -eq "2") {
    Write-Host ""
    Write-Host "[Full PPTX Generation Test]" -ForegroundColor Cyan
    Write-Host "This will generate complete report with LLM content..." -ForegroundColor Gray
    Write-Host "Estimated time: 2-5 minutes" -ForegroundColor Yellow
    Write-Host ""
    
    $confirm = Read-Host "Continue? (Y/n)"
    if ($confirm -eq "n" -or $confirm -eq "N") {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit
    }
    
    $env:ANTHROPIC_API_KEY = $ApiKey
    
    # Create a temporary Python script to run full test
    $tempScript = @"
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from test_with_api import test_full_generation
import os

api_key = os.environ.get('ANTHROPIC_API_KEY')
if api_key:
    test_full_generation(api_key, None)
else:
    print('API Key not found in environment')
"@
    
    $tempScriptPath = Join-Path $scriptDir "temp_test_full.py"
    $tempScript | Out-File -FilePath $tempScriptPath -Encoding utf8
    
    python $tempScriptPath
    
    # Clean up
    Remove-Item $tempScriptPath -ErrorAction SilentlyContinue
    
} else {
    Write-Host "Invalid choice!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "Test Completed!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Cyan

