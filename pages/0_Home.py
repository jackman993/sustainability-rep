"""
Home
"""
import streamlit as st
from shared.ui.sidebar_config import render_sidebar_config

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

# Sidebar: API Configuration (shared component)
render_sidebar_config()

st.title("🌍 ESG Report Generation System")

st.divider()

# Process Navigation
st.subheader("System Workflow")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.info("**Step 1**\nEmission & TCFD")
    
with col2:
    st.info("**Step 2**\nEnvironment")
    
with col3:
    st.info("**Step 3**\nCompany")
    
with col4:
    st.info("**Step 4**\nGovernance & Social")

with col5:
    st.info("**Step 5**\nMerge Report")
    
with col6:
    st.info("**Step 6**\nGRI Index")

st.divider()

# Start Button
if st.button("Get Started", type="primary", use_container_width=True):
    st.switch_page("pages/1_Carbon_TCFD.py")
