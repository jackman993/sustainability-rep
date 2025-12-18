"""
ESG Report Generation System - Minimal Version
"""
import streamlit as st

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

# Show home page content directly
# Streamlit will automatically show pages/ directory files in sidebar navigation
st.title("🌍 ESG Report Generation System")

st.divider()

# Process Navigation
st.subheader("System Workflow")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.info("**Step 1**\nCarbon & TCFD")
    
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
    st.info("✅ Please use the sidebar navigation menu (☰) to navigate to '1_Carbon_TCFD' page")
