"""
Step 2: Environment Report
"""
# Page title - single source of truth (must match docstring above)
PAGE_TITLE = "Step 2: Environment Report"

import streamlit as st
from shared.ui.sidebar_config import render_sidebar_config

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
        st.switch_page("pages/1_Carbon_TCFD.py")

with col2:
    if st.button("Next", type="primary", use_container_width=True):
        st.switch_page("pages/3_Company.py")
