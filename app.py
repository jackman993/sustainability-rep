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

# Sidebar: API Configuration
with st.sidebar:
    st.header("🔑 API Configuration")
    
    # Execution Mode Selection
    execution_mode = st.selectbox(
        "Execution Mode",
        options=["mock", "llm-test", "production"],
        index=0,
        help="Mock: Use mock data (no API key needed)\nLLM-Test: Test single module with LLM\nProduction: Full LLM execution"
    )
    st.session_state.execution_mode = execution_mode
    
    st.divider()
    
    # Claude API Key Input
    st.subheader("Claude API Settings")
    
    # API Key input (password type for security)
    # Using key="claude_api_key" automatically syncs with session_state
    api_key_input = st.text_input(
        "Claude API Key",
        value="",
        type="password",
        help="Enter your Anthropic Claude API key. Get one at https://console.anthropic.com/",
        key="claude_api_key"
    )
    
    # Show status based on session state (which is automatically updated by text_input with key)
    if st.session_state.get("claude_api_key"):
        masked_key = st.session_state.claude_api_key[:8] + "..." + st.session_state.claude_api_key[-4:] if len(st.session_state.claude_api_key) > 12 else "***"
        st.success(f"✅ API Key saved: {masked_key}")
    else:
        st.info("ℹ️ Enter your Claude API key above")
    
    # Claude API Version Selection
    claude_api_version = st.selectbox(
        "Claude API Version",
        options=["2023-06-01", "2024-01-01", "2024-10-22"],
        index=2,
        help="Select the Claude API version to use. Latest recommended: 2024-10-22"
    )
    st.session_state.claude_api_version = claude_api_version
    
    # Claude Model Selection
    claude_model = st.selectbox(
        "Claude Model",
        options=["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
        index=0,
        help="Select the Claude model to use"
    )
    st.session_state.claude_model = claude_model
    
    st.divider()
    
    # Info about API usage
    if execution_mode == "mock":
        st.info("ℹ️ Mock mode: No API key required")
    elif execution_mode in ["llm-test", "production"]:
        if not st.session_state.claude_api_key:
            st.warning("⚠️ API key required for LLM modes")
        else:
            st.success("✅ Ready for LLM generation")

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
    st.info("✅ Please use the sidebar navigation menu (☰) to navigate to '1_Emission_TCFD' page")
