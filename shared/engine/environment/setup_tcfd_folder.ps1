# PowerShell Script to Setup TCFD Folder Structure
# 建立 TCFD 測試資料夾結構

$basePath = "C:\Users\User\Desktop\TCFD generator\output"
$testFolder = Join-Path $basePath "TCFD_Test_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# 建立資料夾
Write-Host "Creating TCFD folder structure..." -ForegroundColor Green
New-Item -ItemType Directory -Path $basePath -Force | Out-Null
New-Item -ItemType Directory -Path $testFolder -Force | Out-Null

Write-Host "`n✓ Folder created: $testFolder" -ForegroundColor Green

# 顯示需要的檔名格式
Write-Host "`n請將以下 5 個 TCFD PPTX 文件放入此資料夾：" -ForegroundColor Yellow
Write-Host "  1. TCFD_01_Transition_Risk_*.pptx" -ForegroundColor Cyan
Write-Host "  2. TCFD_02_Market_Risk_*.pptx" -ForegroundColor Cyan
Write-Host "  3. TCFD_03_Physical_Risk_*.pptx" -ForegroundColor Cyan
Write-Host "  4. TCFD_04_Temperature_Rise_*.pptx" -ForegroundColor Cyan
Write-Host "  5. TCFD_05_Resource_Efficiency_*.pptx" -ForegroundColor Cyan

Write-Host "`n範例檔名（* 可以是任意字元）：" -ForegroundColor Yellow
Write-Host "  - TCFD_01_Transition_Risk_20241220.pptx" -ForegroundColor White
Write-Host "  - TCFD_02_Market_Risk_20241220.pptx" -ForegroundColor White
Write-Host "  - TCFD_03_Physical_Risk_20241220.pptx" -ForegroundColor White
Write-Host "  - TCFD_04_Temperature_Rise_20241220.pptx" -ForegroundColor White
Write-Host "  - TCFD_05_Resource_Efficiency_20241220.pptx" -ForegroundColor White

Write-Host "`n資料夾路徑：" -ForegroundColor Green
Write-Host "  $testFolder" -ForegroundColor White

Write-Host "`n完成！請將 TCFD 文件放入上述資料夾。" -ForegroundColor Green

