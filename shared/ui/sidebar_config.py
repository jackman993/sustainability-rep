"""
Shared Sidebar Configuration Component
Used across all pages for API key and mode configuration
"""
import streamlit as st
import os


def render_sidebar_config():
    """Render API configuration in sidebar (shared across all pages)"""
    with st.sidebar:
        st.header("🔑 API Configuration")
        
        # ========== 自動讀取 API Key（優先級：session_state > secrets > 環境變數） ==========
        if 'claude_api_key' not in st.session_state or not st.session_state.get('api_key_locked', False):
            # 第一次運行或未鎖定：嘗試從 secrets/環境變數讀取
            api_key = None
            
            # 優先級 1: Streamlit secrets
            try:
                if hasattr(st, 'secrets'):
                    api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
                    if api_key:
                        print(f"[API_KEY] 從 secrets 讀取成功")
            except Exception as e:
                print(f"[API_KEY] 讀取 secrets 失敗: {e}")
            
            # 優先級 2: 環境變數
            if not api_key:
                api_key = os.getenv("ANTHROPIC_API_KEY", None)
                if api_key:
                    print(f"[API_KEY] 從環境變數讀取成功")
            
            # 如果找到，保存到 session_state 並鎖定
            if api_key:
                st.session_state.claude_api_key = api_key
                st.session_state.api_key_locked = True
                print(f"[API_KEY] 已保存到 session_state 並鎖定")
            else:
                print(f"[API_KEY] 未找到 secrets 或環境變數")
        
        # Data Source Selection (簡化版：只有 Mock 和 API 兩個選項)
        # 如果 API Key 已自動配置，強制使用 Claude API
        if st.session_state.get("api_key_locked", False) and st.session_state.get("claude_api_key"):
            # API Key 已配置，強制使用 Claude API
            st.session_state.data_source = "Claude API"
            data_source = "Claude API"
            st.info("💡 API Key 已自動配置，已切換到 Claude API 模式")
        else:
            # 沒有 API Key，允許選擇
            default_index = 0
            if "data_source" in st.session_state:
                # 保持用戶之前的選擇
                default_index = 1 if st.session_state.data_source == "Claude API" else 0
            
            data_source = st.radio(
                "Data Source",
                options=["Mock Data", "Claude API"],
                index=default_index,
                help="Mock Data: 使用模擬數據（無需 API Key）\nClaude API: 使用 Claude API 生成內容（需要 API Key）",
                key="sidebar_data_source"
            )
            st.session_state.data_source = data_source
        
        st.divider()
        
        # Claude API Key Display/Input (只在選擇 Claude API 時顯示)
        if data_source == "Claude API":
            st.subheader("Claude API Settings")
            
            # 檢查是否已鎖定（從 secrets/環境變數自動配置）
            if st.session_state.get("api_key_locked", False) and st.session_state.get("claude_api_key"):
                # 已鎖定：只顯示狀態，不顯示輸入框
                masked_key = st.session_state.claude_api_key[:8] + "..." + st.session_state.claude_api_key[-4:] if len(st.session_state.claude_api_key) > 12 else "***"
                st.success(f"✅ API Key 已自動配置: {masked_key}")
                st.caption("💡 API Key 已從配置自動讀取，無需手動輸入")
            else:
                # 未鎖定：顯示輸入框（本地開發或手動輸入）
                api_key_input = st.text_input(
                    "Claude API Key",
                    value=st.session_state.get("claude_api_key", ""),
                    type="password",
                    help="Enter your Anthropic Claude API key. Get one at https://console.anthropic.com/",
                    key="claude_api_key_input"
                )
                
                if api_key_input:
                    st.session_state.claude_api_key = api_key_input
                    st.session_state.api_key_locked = True
                    st.success("✅ API Key 已保存")
                    st.rerun()
                else:
                    st.warning("⚠️ Please enter your Claude API key or configure in secrets.toml")
        else:
            st.info("ℹ️ Mock Data mode: No API key required")
        
        # 模型在代碼中寫死，不在 UI 中顯示
        # 備選模型：claude-3-5-sonnet-20240620, claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307

