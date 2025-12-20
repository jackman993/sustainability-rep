"""
Shared Sidebar Configuration Component
Used across all pages for API key and mode configuration
"""
import streamlit as st


def render_sidebar_config():
    """Render API configuration in sidebar (shared across all pages)"""
    with st.sidebar:
        st.header("🔑 API Configuration")
        
        # Data Source Selection (簡化版：只有 Mock 和 API 兩個選項)
        data_source = st.radio(
            "Data Source",
            options=["Mock Data", "Claude API"],
            index=0,
            help="Mock Data: 使用模擬數據（無需 API Key）\nClaude API: 使用 Claude API 生成內容（需要 API Key）",
            key="sidebar_data_source"
        )
        st.session_state.data_source = data_source
        
        st.divider()
        
        # Claude API Key Input (只在選擇 Claude API 時顯示)
        if data_source == "Claude API":
            st.subheader("Claude API Settings")
            
            # API Key input (password type for security)
            api_key_input = st.text_input(
                "Claude API Key",
                value="",
                type="password",
                help="Enter your Anthropic Claude API key. Get one at https://console.anthropic.com/",
                key="claude_api_key"
            )
            
            # Show status
            if st.session_state.get("claude_api_key"):
                masked_key = st.session_state.claude_api_key[:8] + "..." + st.session_state.claude_api_key[-4:] if len(st.session_state.claude_api_key) > 12 else "***"
                st.success(f"✅ API Key saved: {masked_key}")
            else:
                st.warning("⚠️ Please enter your Claude API key")
        else:
            st.info("ℹ️ Mock Data mode: No API key required")
        
        # 模型在代碼中寫死，不在 UI 中顯示
        # 備選模型：claude-3-5-sonnet-20240620, claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307

