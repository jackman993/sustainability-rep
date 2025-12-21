# Streamlit 環境問題分析

## 問題現象
- ✅ CMD 測試成功（文件正常生成）
- ❌ Streamlit 環境中失敗（沒有文件生成）

## 關鍵發現

### 1. Streamlit 導入時機問題

**問題點：**
```python
# output_config.py - get_session_id()
st = _get_streamlit()  # 延遲導入
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())
```

**可能的原因：**
- `_get_streamlit()` 每次調用都重新導入 streamlit 模組
- 在 Streamlit 執行上下文中，模組級別的導入可能獲取不到正確的 session_state
- Streamlit 的執行上下文（ScriptRunContext）可能在不同模組間不一致

### 2. 執行上下文問題

**調用鏈：**
```
generate_combined_pptx() (在函數內 import streamlit)
  → get_tcfd_output_path()
    → get_step_output_dir()
      → get_session_output_dir()
        → get_session_id()
          → _get_streamlit()  # 重新導入 streamlit
            → st.session_state  # 可能訪問失敗
```

**問題：**
- `generate_combined_pptx()` 在函數內部導入 streamlit
- 但 `get_session_id()` 通過 `_get_streamlit()` 重新導入
- 兩次導入可能獲取到不同的 Streamlit 實例或上下文

### 3. session_state 訪問失敗的後果

**當前處理：**
```python
except Exception as e:
    print(f"[WARNING] Failed to get session_id: {e}")
    return str(uuid.uuid4())  # 返回臨時 ID
```

**問題：**
- 每次失敗都返回新的 UUID
- 導致每次調用路徑都不同
- 文件可能保存到不同的目錄
- UI 無法找到文件

## 可能的根本原因

### 假設 1：Streamlit 執行上下文丟失
- `generate_combined_pptx()` 在異常處理中導入 streamlit
- 此時可能已經不在 Streamlit 的執行上下文中
- `st.session_state` 訪問失敗

### 假設 2：模組級導入 vs 函數級導入
- `path_manager.py` 使用延遲導入
- `main.py` 在函數內導入
- 兩者獲取的 streamlit 實例可能不一致

### 假設 3：異常被吞掉
- `get_session_id()` 失敗時返回臨時 UUID
- 錯誤被 `print()` 輸出，UI 看不到
- 函數繼續執行，但路徑錯誤

## 需要驗證的點

1. **Streamlit 終端輸出**
   - 是否有 `[WARNING] Failed to get session_id` 的輸出？
   - 是否有其他錯誤信息？

2. **session_id 一致性**
   - 每次調用 `get_session_id()` 是否返回相同的值？
   - 還是每次都返回新的 UUID？

3. **路徑計算**
   - `get_tcfd_output_path()` 返回的路徑是什麼？
   - 路徑是否包含正確的 session_id？

4. **文件實際保存位置**
   - 文件是否真的沒有生成？
   - 還是生成到了錯誤的位置？

## 建議的解決方案

### 方案 1：統一 Streamlit 導入
- 在頁面層級獲取 session_id
- 作為參數傳遞給 `generate_combined_pptx()`
- 避免在引擎層訪問 session_state

### 方案 2：增強錯誤處理
- 在 `get_session_id()` 失敗時，不要返回臨時 UUID
- 而是拋出異常，讓上層處理
- 確保錯誤能被 UI 看到

### 方案 3：使用 Streamlit 的 session_state 直接傳遞
- 在頁面層級獲取 session_id
- 保存到 session_state
- 引擎層從 session_state 讀取（如果可用）

### 方案 4：添加調試日誌
- 在關鍵點添加 `st.write()` 或 `st.error()` 顯示調試信息
- 確認每個步驟的路徑和狀態

