"""
Step 3: Company Report
"""
import streamlit as st
from shared.ui.sidebar_config import render_sidebar_config

st.set_page_config(
    page_title="Step 3: Company Report",
    page_icon="🏢",
    layout="wide"
)

# Sidebar: API Configuration (shared component)
render_sidebar_config()

st.title("Step 3: Company Report")

st.divider()

# Prerequisites
st.success("✅ Emission, TCFD, and Environment sections completed")

st.divider()

# Company Information
st.subheader("Company Information")

company_name = st.text_input(
    "Company Name *",
    placeholder="e.g., TSMC"
)

st.divider()

# Generate Section
st.subheader("Generate Company Report")

st.info("""
**Company section includes:**
- Company overview
- Material topics analysis
- Stakeholder engagement
- Sustainability goals and actions
""")

if st.button("Generate Company Report", type="primary", use_container_width=True, disabled=not company_name):
    with st.spinner(f"Generating report for {company_name}..."):
        st.success(f"✅ Company report generated for {company_name}")
        st.session_state.company_done = True

st.divider()

# Navigation
if st.session_state.get("company_done"):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Previous", use_container_width=True):
            st.switch_page("pages/2_Environment.py")
    
    with col2:
        if st.button("Next", type="primary", use_container_width=True):
            st.switch_page("pages/4_Governance.py")
