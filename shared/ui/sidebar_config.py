"""
Shared Sidebar Configuration Component
- dev 環境：允許在 sidebar 手動輸入 / 覆蓋 API Key
- prod 環境：API Key 只從伺服器端設定（secrets / 環境變數），不允許使用者輸入
"""
import streamlit as st

from shared.config.env import get_app_env, AppEnv
from shared.config.api_keys import get_claude_api_key


def render_sidebar_config():
    """Render API configuration in sidebar (shared across all pages)"""
    with st.sidebar:
        st.header("🔑 API Configuration")

        env = get_app_env()

        # ===== 開發環境：允許在 sidebar 手動輸入 API Key =====
        if env == AppEnv.DEV:
            st.subheader("Claude API Settings (Dev)")

            api_key_input = st.text_input(
                "Claude API Key",
                value=st.session_state.get("claude_api_key", ""),
                type="password",
                help="開發環境：可在此輸入 / 覆蓋 Anthropic Claude API Key。",
                key="claude_api_key_input",
            )

            if api_key_input:
                st.session_state["claude_api_key"] = api_key_input
                st.success("✅ API Key 已保存到當前開發 session")

        # ===== 共用：顯示目前「實際生效」的 Key 狀態（dev / prod 都顯示） =====
        effective_key = get_claude_api_key()
        st.subheader("Claude API Status")

        if effective_key:
            masked = (
                effective_key[:4] + "..." + effective_key[-4:]
                if len(effective_key) > 8
                else "***"
            )
            if env == AppEnv.PROD:
                st.info(f"Claude Key（PROD）: ✅ 已由伺服器配置 ({masked})")
                st.caption("此環境不允許在前端輸入 API Key，請由系統管理員在伺服器上設定。")
            else:
                st.info(f"Claude Key（DEV）: ✅ 有效 ({masked})")
        else:
            st.error("Claude Key: ❌ 尚未設定")
            st.caption("請在伺服器環境變數或 `.streamlit/secrets.toml` 中設定 `ANTHROPIC_API_KEY`。")

        # 強制使用 API 模式（保留原本行為）
        st.session_state["data_source"] = "Claude API"

