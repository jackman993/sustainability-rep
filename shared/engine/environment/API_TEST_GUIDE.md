# API 測試指南

## 🚀 測試指令說明

### 1. 快速 API 測試（不生成文件）
**只測試 LLM API 連接和內容生成**

**PowerShell：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9
python test_api_quick.py YOUR_API_KEY
```

**功能：**
- ✅ 測試 API 連接
- ✅ 生成內容預覽
- ❌ **不生成 PPTX 文件**

---

### 2. 完整生成測試（會生成 PPTX 文件）⭐

**PowerShell：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9
python test_api_full.py YOUR_API_KEY
```

**範例：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9
python test_api_full.py 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
```

**功能：**
- ✅ 測試 API 連接
- ✅ 生成所有頁面的 LLM 內容
- ✅ **生成完整 PPTX 文件**
- ⏱️ 需要 2-5 分鐘（調用多次 API）

**輸出文件：**
```
C:\Users\User\Desktop\environment4.1-4.9\output\ESG_Environment_Chapter_API_YYYYMMDD_HHMMSS.pptx
```

---

### 3. 互動式測試

**PowerShell：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9
python test_with_api.py
```

然後選擇：
- 選項1：快速測試（不生成文件）
- 選項2：完整生成（會生成文件）

---

## 📋 測試腳本對照表

| 腳本 | 功能 | 生成文件 | 時間 |
|------|------|----------|------|
| `test_api_quick.py` | 快速 API 測試 | ❌ 否 | ~10-30秒 |
| `test_api_full.py` | 完整生成測試 | ✅ 是 | ~2-5分鐘 |
| `test_with_api.py` | 互動式選擇 | 可選 | 依選擇 |

---

## ⚡ 快速指令（生成文件）

**PowerShell：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9; python test_api_full.py YOUR_API_KEY
```

**或分開執行：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9
python test_api_full.py YOUR_API_KEY
```

---

## 📝 注意事項

- `test_api_quick.py` 只測試 API，**不生成文件**
- `test_api_full.py` 會生成完整的 PPTX 文件
- 完整生成需要較長時間（因為要調用多次 API）
