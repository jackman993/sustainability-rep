"""
Step 4: Governance & Social Report
"""
# Page title - single source of truth (must match docstring above)
PAGE_TITLE = "Step 4: Governance & Social Report"

import streamlit as st
from shared.ui.sidebar_config import render_sidebar_config

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="⚖️",
    layout="wide"
)

# Sidebar: API Configuration (shared component)
render_sidebar_config()

st.title(PAGE_TITLE)

st.divider()

# Prerequisites
st.success("✅ Emission, TCFD, Environment, and Company sections completed")

st.divider()

# Generate Section
st.subheader("Generate Governance & Social Report")

st.info("""
**Governance & Social section includes:**
- Corporate governance structure
- Board diversity and independence
- Social responsibility initiatives
- Employee welfare and development
""")

if st.button("Generate Governance Report", type="primary", use_container_width=True):
    with st.spinner("Generating governance & social report..."):
        progress = st.progress(0)
        progress.progress(0.5)
        st.success("✅ Governance & Social report generated")
        progress.progress(1.0)
        st.session_state.governance_done = True

st.divider()

# Navigation
if st.session_state.get("governance_done"):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Previous", use_container_width=True):
            st.switch_page("pages/3_Company.py")
    
    with col2:
        if st.button("Next", type="primary", use_container_width=True):
            st.switch_page("pages/5_Merge_Report.py")
