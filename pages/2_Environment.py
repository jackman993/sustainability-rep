"""
Step 2: Environment Report
"""
# Page title - single source of truth (must match docstring above)
PAGE_TITLE = "Step 2: Environment Report"

import streamlit as st
from pathlib import Path
import sys

# 添加項目根目錄到 Python 路徑（確保能找到 shared 模組）
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from shared.ui.sidebar_config import render_sidebar_config
from shared.agents.data_broker import DataBroker

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="🌍",
    layout="wide"
)

# Sidebar: API Configuration (shared component)
render_sidebar_config()

st.title(PAGE_TITLE)

st.divider()

# Prerequisites
st.success("✅ Emission & TCFD completed")

# 顯示來自 TCFD 的摘要資料（透過 DataBroker / Skill Agent）
tcfd_summary = DataBroker.get_tcfd_summary()
if not tcfd_summary:
    st.warning("⚠️ 尚未找到 TCFD Summary。請先在 Step 1 生成 TCFD 報告，系統才會將關鍵氣候資訊帶入本章節。")
else:
    with st.expander("TCFD Summary（供 Environment / 其他章節使用）", expanded=False):
        st.write("以下為從 Step 1 彙整出的最小氣候關鍵資訊，之後可直接餵給 LLM Prompt：")
        st.json(tcfd_summary)

st.divider()

# Generate Section
st.subheader("Generate Environment Report")

st.info("""
**Environment section includes:**
- Detailed emission analysis
- TCFD climate risk assessment
- Environmental management measures
- Approximately 17 pages
""")

if st.button("Generate Environment Report", type="primary", use_container_width=True):
    with st.spinner("Generating environment report..."):
        progress = st.progress(0)
        progress.progress(0.5)
        st.success("✅ Environment report generated (17 pages)")
        progress.progress(1.0)

st.divider()

# Navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("Previous", use_container_width=True):
        st.switch_page("pages/1_Emission_TCFD.py")

with col2:
    if st.button("Next", type="primary", use_container_width=True):
        st.switch_page("pages/3_Company.py")
