# Simple PowerShell Script - Direct API Test
# Usage: powershell -ExecutionPolicy Bypass -File test_api_simple.ps1 YOUR_API_KEY

param(
    [Parameter(Mandatory=$true)]
    [string]$ApiKey
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Testing API with Key: $($ApiKey.Substring(0,10))..." -ForegroundColor Green
python test_api_quick.py $ApiKey

