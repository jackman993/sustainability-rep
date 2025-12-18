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

# Sidebar Guide
with st.sidebar:
    st.title("📖 User Guide")
    st.divider()
    
    st.subheader("🚀 Quick Start")
    st.markdown("""
    1. **Navigate** through pages using the sidebar menu
    2. **Fill in** required information on each page
    3. **Generate** reports step by step
    4. **Review** and download your reports
    """)
    
    st.divider()
    
    st.subheader("📋 Workflow Steps")
    st.markdown("""
    **Step 1**: Carbon & TCFD
    - Carbon emission data
    - TCFD climate risk assessment
    
    **Step 2**: Environment
    - Environmental analysis
    - Risk assessment
    
    **Step 3**: Company
    - Company information
    - Material topics
    
    **Step 4**: Governance
    - Governance structure
    - Social responsibility
    
    **Step 5**: Merge Report
    - Combine all sections
    
    **Step 6**: GRI Index
    - GRI standards mapping
    """)
    
    st.divider()
    
    st.subheader("⚙️ Execution Modes")
    st.markdown("""
    **Mock Mode** 🎭
    - Fast testing
    - No API key needed
    - Uses sample data
    
    **LLM-Test Mode** 🧪
    - Test single module
    - Saves API costs
    - Requires API key
    
    **Production Mode** 🚀
    - Full LLM execution
    - All modules
    - Requires API key
    """)
    
    # Mode selector
    st.divider()
    st.subheader("🔧 Settings")
    execution_mode = st.radio(
        "Execution Mode",
        ["Mock", "LLM-Test", "Production"],
        index=0,
        help="Select execution mode for report generation"
    )
    # Map display name to mode value
    mode_map = {"Mock": "mock", "LLM-Test": "llm-test", "Production": "production"}
    st.session_state.execution_mode = mode_map[execution_mode]
    
    if execution_mode in ["LLM-Test", "Production"]:
        test_module = st.selectbox(
            "Test Module (LLM-Test only)",
            ["environment", "company", "governance"],
            disabled=(execution_mode != "LLM-Test"),
            help="Select which module to test with LLM"
        )
        if execution_mode == "LLM-Test":
            st.session_state.test_module = test_module
    
    st.divider()
    
    st.subheader("💡 Tips")
    st.info("""
    - Use **Mock Mode** for quick testing
    - Use **LLM-Test Mode** to test specific modules
    - Use **Production Mode** for final reports
    - All data is saved in session state
    """)
    
    st.divider()
    
    st.caption("🌍 ESG Report Generation System v1.0")

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
