"""
ESG Report Generation System - Minimal Version
"""
import streamlit as st
from pathlib import Path
import sys

# 添加項目根目錄到 Python 路徑（確保能找到 shared 模組）
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

st.set_page_config(
    page_title="ESG Report System",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session_state
if "current_step" not in st.session_state:
    st.session_state.current_step = 0

# Initialize mode manager state
if "execution_mode" not in st.session_state:
    st.session_state.execution_mode = "mock"

# Sidebar: API Configuration (shared component)
from shared.ui.sidebar_config import render_sidebar_config
render_sidebar_config()

# Show home page content directly
# Streamlit will automatically show pages/ directory files in sidebar navigation
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
    st.info("**Step 4**\nGovernance")

with col5:
    st.info("**Step 5**\nMerge Report")
    
with col6:
    st.info("**Step 6**\nGRI Index")

st.divider()

st.info("💡 **Tip**: Use the sidebar navigation menu to access different pages, or click the 'Get Started' button below.")

# Start Button
if st.button("Get Started", type="primary", use_container_width=True):
    st.info("✅ Please use the sidebar navigation menu (☰) to navigate to 'Emission & TCFD' page")
