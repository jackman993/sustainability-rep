# 本地測試指南

## 📁 測試路徑

**工作目錄：**
```
C:\Users\User\Desktop\environment4.1-4.9
```

**TCFD 文件位置（已配置）：**
```
C:\Users\User\Desktop\environment4.1-4.9\assets\TCFD\TCFD_table (26).pptx
```

**輸出文件位置：**
```
C:\Users\User\Desktop\environment4.1-4.9\output\ESG_Environment_Chapter_YYYYMMDD_HHMMSS.pptx
```

---

## 🚀 測試指令

### 方式1：使用測試腳本（推薦）

**PowerShell 指令：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9
python test_local.py
```

**CMD 指令：**
```cmd
cd C:\Users\User\Desktop\environment4.1-4.9
python test_local.py
```

---

### 方式2：直接執行主程式

**PowerShell 指令：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9
python main_pptx.py --test
```

---

## ⚙️ 測試配置

### 測試模式（test_mode = True）
- ✅ 跳過 LLM API 呼叫
- ✅ 使用佔位文字
- ✅ 快速測試版面結構

### 正式模式（test_mode = False）
- 需要設定 API Key
- 會呼叫 Claude API 生成內容
- 需要較長時間

---

## 📋 測試前檢查清單

- [ ] 確認 TCFD 文件存在：`assets\TCFD\TCFD_table (26).pptx`
- [ ] 確認 Python 環境正常
- [ ] 確認已安裝必要套件：`python-pptx`, `anthropic` 等
- [ ] 確認 `output` 資料夾存在（會自動建立）

---

## 📊 預期輸出

測試成功後會顯示：
```
============================================================
Environment Chapter PPTX Generation - Local Test
============================================================

[Generating Cover Page]
✓ Cover page completed

[Generating Environmental Policy Pages]
✓ Environmental policy pages completed

[Generating TCFD Pages]
  Pages 5-11: Inserting TCFD PPTX file (7 pages)
  ✓ Found TCFD file: TCFD_table (26).pptx
  ✓ Inserted 7 slides from TCFD 7 Pages: TCFD_table (26).pptx
✓ TCFD pages completed (Pages 5-11: 7 pages from single PPTX file)

[Generating SASB Page]
  Page 12: SASB Industry Classification
✓ SASB page completed (Page 12)

[Generating GHG Management Pages]
  Pages 13-15: GHG Management
✓ GHG management pages completed (Pages 13-15)

[Generating Environmental Management Pages]
  Pages 16-19: Environmental Management
✓ Environmental management pages completed (Pages 16-19)

============================================================
PPTX Report Generation Completed!
Total 19 slides
============================================================

============================================================
✓ Test completed!
✓ Output file: C:\Users\User\Desktop\environment4.1-4.9\output\ESG_Environment_Chapter_20241221_123456.pptx
============================================================
```

---

## 🔧 疑難排解

### 問題1：找不到 TCFD 文件
**解決方案：**
- 確認文件路徑：`C:\Users\User\Desktop\environment4.1-4.9\assets\TCFD\TCFD_table (26).pptx`
- 確認檔名以 `TCFD` 開頭

### 問題2：模組找不到
**解決方案：**
```powershell
pip install python-pptx anthropic
```

### 問題3：權限錯誤
**解決方案：**
- 確認有寫入 `output` 資料夾的權限
- 以管理員身份執行 PowerShell

---

## 📝 頁面結構確認

測試完成後，請檢查生成的 PPTX 文件：

- ✅ 第1頁：Cover
- ✅ 第2-3頁：Policy (4.1, 4.2)
- ✅ 第5-11頁：TCFD（7頁，從 TCFD_table (26).pptx 插入）
- ✅ 第12頁：SASB
- ✅ 第13-15頁：GHG Management
- ✅ 第16-19頁：Environmental Management

**總共：19 頁**

