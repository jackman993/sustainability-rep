# Streamlit 自動導航說明

## 結構檢查 ✅

所有文件結構已正確設置：

```
sustainability-rep/
├── app.py                    # 主入口文件（在根目錄）
├── pages/                    # 頁面目錄
│   ├── 0_Home.py            ✅ 有 st.set_page_config
│   ├── 1_Carbon_TCFD.py     ✅ 有 st.set_page_config
│   ├── 2_Environment.py     ✅ 有 st.set_page_config
│   ├── 3_Company.py         ✅ 有 st.set_page_config
│   ├── 4_Governance.py      ✅ 有 st.set_page_config
│   ├── 5_Merge_Report.py    ✅ 有 st.set_page_config
│   └── 6_GRI_Index.py       ✅ 有 st.set_page_config
└── .streamlit/
    └── config.toml          ✅ 配置文件
```

## 如何顯示側邊欄導航

Streamlit 會自動：
1. 掃描 `pages/` 目錄中的所有 `.py` 文件
2. 在側邊欄顯示頁面導航
3. 使用 `st.set_page_config()` 中的 `page_title` 作為顯示名稱
4. 使用 `page_icon` 作為圖標

## 如果側邊欄沒有出現

### 本地測試：
```bash
# 停止當前運行的 Streamlit
# 然後重新啟動
streamlit run app.py
```

### Streamlit Cloud：
1. 確保所有文件已提交到 Git
2. 在 Streamlit Cloud 上重新部署應用
3. 等待部署完成後，側邊欄應該會自動出現

## 驗證步驟

1. ✅ 確認 `pages/` 目錄存在
2. ✅ 確認所有頁面文件都有 `st.set_page_config()`
3. ✅ 確認 `app.py` 在根目錄，不在 `pages/` 目錄中
4. ✅ 確認 Streamlit 版本 >= 1.28.0（當前版本：1.51.0）

## 測試命令

```bash
# 運行測試腳本檢查結構
python test_pages.py

# 運行 Streamlit 應用
streamlit run app.py
```

## 注意事項

- Streamlit 會自動按文件名順序排列頁面（0_Home, 1_Carbon_TCFD...）
- 側邊欄導航會在運行 `streamlit run app.py` 時自動出現
- 如果使用 Streamlit Cloud，確保所有文件都已提交到 Git

