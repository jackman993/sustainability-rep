"""
Step 6: GRI Index
"""
# Page title - single source of truth (must match docstring above)
PAGE_TITLE = "Step 6: GRI Index"

import streamlit as st
from pathlib import Path
import sys

# 添加項目根目錄到 Python 路徑（確保能找到 shared 模組）
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from shared.ui.sidebar_config import render_sidebar_config

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="📊",
    layout="wide"
)

# Sidebar: API Configuration (shared component)
render_sidebar_config()

st.title(PAGE_TITLE)

st.divider()

# Success Message
st.success("🎉 Complete ESG Report Generated!")

st.divider()

# Report Summary
st.subheader("Report Summary")

col1, col2 = st.columns(2)

with col1:
    st.write("**Report Contents:**")
    st.write("- Emission Analysis")
    st.write("- TCFD Climate Risk Assessment")
    st.write("- Environment Report (17 pages)")
    st.write("- Company Report")
    st.write("- Governance & Social Report")

with col2:
    st.write("**Report Information:**")
    st.write("- Company: TSMC")
    st.write("- Industry: Manufacturing")
    st.write("- Total Pages: 53")

st.divider()

# GRI Index Generation
st.subheader("Generate GRI Index")

st.info("""
**GRI Index includes:**
- GRI Standards reference table
- Page number mapping
- Disclosure status tracking
""")

if st.button("Generate GRI Index", type="primary", use_container_width=True):
    with st.spinner("Generating GRI Index..."):
        st.success("✅ GRI Index generated")
        st.session_state.gri_done = True

st.divider()

# Download Section
st.subheader("Download Complete Report")

st.download_button(
    "📥 Download Complete ESG Report",
    data=b"",  # Placeholder
    file_name="Complete_ESG_Report.pptx",
    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    type="primary",
    use_container_width=True
)

st.divider()

# Actions
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate New Report", use_container_width=True):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("pages/1_Emission_TCFD.py")

with col2:
    if st.button("Return Home", use_container_width=True):
        st.switch_page("pages/0_Home.py")
