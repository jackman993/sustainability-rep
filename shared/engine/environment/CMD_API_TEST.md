# CMD/PowerShell API 測試指令

## 🚀 PowerShell 指令（正確語法）

### 方式1：分開執行（推薦）

```powershell
cd C:\Users\User\Desktop\environment4.1-4.9
python test_api_quick.py YOUR_API_KEY
```

**範例：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9
python test_api_quick.py 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
```

---

### 方式2：使用分號（PowerShell）

```powershell
cd C:\Users\User\Desktop\environment4.1-4.9; python test_api_quick.py YOUR_API_KEY
```

**範例：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9; python test_api_quick.py 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
```

---

### 方式3：CMD 指令（CMD 支援 &&）

```cmd
cd C:\Users\User\Desktop\environment4.1-4.9 && python test_api_quick.py YOUR_API_KEY
```

---

## 📋 完整指令範例

### PowerShell（分開執行）
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9
python test_api_quick.py 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
```

### PowerShell（一行指令）
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9; python test_api_quick.py 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
```

### CMD（支援 &&）
```cmd
cd C:\Users\User\Desktop\environment4.1-4.9 && python test_api_quick.py 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
```

---

## ⚠️ 注意事項

- **PowerShell**：使用 `;` 或分開執行（不支援 `&&`）
- **CMD**：支援 `&&` 語法
- **API Key**：直接貼在指令後面即可

---

## 🔧 快速測試

**PowerShell：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9
python test_api_quick.py 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
```

**或一行：**
```powershell
cd C:\Users\User\Desktop\environment4.1-4.9; python test_api_quick.py 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
```
