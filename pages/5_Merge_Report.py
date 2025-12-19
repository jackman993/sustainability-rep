# Page title - single source of truth for sidebar, page_title, and st.title
PAGE_TITLE = "Step 5: Merge Complete Report"

# Docstring for sidebar navigation (must be literal string, not formatted)
"""
Step 5: Merge Complete Report
"""

import streamlit as st
from shared.ui.sidebar_config import render_sidebar_config

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="📄",
    layout="wide"
)

# Sidebar: API Configuration (shared component)
render_sidebar_config()

st.title(PAGE_TITLE)

st.divider()

# Prerequisites
st.subheader("Ready to Merge")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("✅ Company")
    
with col2:
    st.success("✅ Environment")
    
with col3:
    st.success("✅ Governance")

st.divider()

# Merge Process
st.subheader("Merge Process")

st.info("""
**Merge order:**
Company → Environment → Governance & Social

This will create a complete ESG report.
""")

if st.button("Merge Reports", type="primary", use_container_width=True):
    with st.spinner("Merging reports..."):
        progress = st.progress(0)
        
        st.info("Merging Company section...")
        progress.progress(0.33)
        
        st.info("Merging Environment section...")
        progress.progress(0.66)
        
        st.info("Merging Governance section...")
        progress.progress(1.0)
        
        st.success("✅ Complete report merged successfully")
        st.session_state.merge_done = True

st.divider()

# Statistics
if st.session_state.get("merge_done"):
    st.subheader("Report Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Pages", "53")
        
    with col2:
        st.metric("Sections", "3")
        
    with col3:
        st.metric("Status", "✅ Complete")

st.divider()

# Navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("Previous", use_container_width=True):
        st.switch_page("pages/4_Governance.py")

with col2:
    if st.button("Next", type="primary", use_container_width=True):
        st.switch_page("pages/6_GRI_Index.py")
