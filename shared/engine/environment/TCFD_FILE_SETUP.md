# TCFD 文件設置說明

## 📁 文件路徑與檔名格式

### ✅ 當前設置（已配置）

**TCFD 文件位置：**
```
C:\Users\User\Desktop\environment4.1-4.9\assets\TCFD\TCFD_table (26).pptx
```

程式會**優先**查找這個本地資料夾！

### 查找順序：

1. **優先：本地 assets/TCFD 資料夾**（開發/測試用）
   ```
   C:\Users\User\Desktop\environment4.1-4.9\assets\TCFD\
   ```

2. **其次：手動指定的資料夾**（透過 `tcfd_output_folder` 參數）

3. **最後：預設 TCFD Generator 輸出資料夾**
   ```
   C:\Users\User\Desktop\TCFD generator\output\
   ```

### 檔名格式（支援多種格式）：

- `TCFD*.pptx` ✅ （例如：`TCFD_table (26).pptx`）
- `TCFD_*.pptx` ✅ （例如：`TCFD_20241220.pptx`）
- `TCFD_7pages_*.pptx` ✅
- `TCFD_Complete_*.pptx` ✅

### 重要要求：

1. ✅ **單一 PPTX 檔案**（不是 5 個分開的檔案）
2. ✅ **必須包含 7 頁投影片**
3. ✅ **檔名以 `TCFD` 開頭**
4. ✅ **檔案格式為 `.pptx`**

---

## 🧪 測試步驟

1. **確認文件存在**：
   ```
   C:\Users\User\Desktop\environment4.1-4.9\assets\TCFD\TCFD_table (26).pptx
   ```

2. **執行測試腳本**：
   ```bash
   cd C:\Users\User\Desktop\environment4.1-4.9
   python test_local.py
   ```

3. **程式會自動找到並插入 TCFD 7 頁**（從第 5 頁開始）

---

## 📝 注意事項

- 如果文件不存在，程式會建立佔位頁面
- 程式會自動驗證 TCFD 文件包含的頁數
- 支援檔名中包含空格和括號（如 `TCFD_table (26).pptx`）
