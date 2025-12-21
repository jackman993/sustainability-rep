# TCFD 輸出問題診斷

## 問題現象
- 文件路徑顯示：`/mount/src/sustainability-rep/output/463ed628-aa06-4853-9f17-1dffd951757b/TCFD_table.pptx`
- 顯示"成功"，但實際上文件沒有生成或無法訪問

## 關鍵發現

### 1. 路徑計算
```python
# output_config.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
# 從 shared/engine/output_config.py 向上三級
# shared/engine/output_config.py -> shared/engine -> shared -> 項目根目錄
```

### 2. Streamlit Cloud 路徑
- `/mount/src/` 是 Streamlit Cloud 的典型路徑
- 文件可能保存到了臨時文件系統
- Streamlit Cloud 的文件系統可能是只讀的或臨時的

### 3. 可能的問題點

#### 問題 A：PROJECT_ROOT 計算錯誤
- `Path(__file__).resolve()` 在 Streamlit Cloud 中可能返回不同的路徑
- 需要驗證實際的 PROJECT_ROOT 是什麼

#### 問題 B：Streamlit Cloud 文件系統限制
- Streamlit Cloud 可能不允許寫入 `/mount/src/` 目錄
- 文件可能保存失敗但沒有拋出異常
- 需要使用 Streamlit 的臨時文件系統或 session 存儲

#### 問題 C：路徑權限問題
- 目錄可能沒有寫入權限
- `mkdir(parents=True, exist_ok=True)` 可能失敗但沒有檢查

#### 問題 D：prs.save() 靜默失敗
- `prs.save()` 可能沒有真正保存文件
- 需要檢查返回值或異常

## 需要檢查的點

1. **終端輸出中的 [DEBUG] 日誌**
   - PROJECT_ROOT 的實際值是什麼？
   - output_path 的實際值是什麼？
   - 文件保存後是否存在？

2. **Streamlit Cloud 環境**
   - 是否在 Streamlit Cloud 上運行？
   - 文件系統是否可寫？

3. **文件實際位置**
   - 文件是否真的保存了？
   - 保存到了哪裡？

## 建議的診斷步驟

1. 在終端輸出中查找 `[DEBUG]` 日誌
2. 檢查 PROJECT_ROOT 的實際值
3. 檢查 output_path 的實際值
4. 檢查文件是否真的存在
5. 檢查 Streamlit Cloud 的文件系統限制

