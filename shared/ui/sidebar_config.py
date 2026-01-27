"""
Shared Sidebar Configuration Component
- dev: allow entering / overriding API Key in sidebar
- prod: API Key only from server-side config (secrets / env), no user input
"""
import streamlit as st

from shared.config.env import get_app_env, AppEnv
from shared.config.api_keys import get_claude_api_key


def render_sidebar_config():
    """Render API configuration in sidebar (shared across all pages)"""
    with st.sidebar:
        st.header("🔑 API Configuration")

        env = get_app_env()

        # ===== Dev environment: allow manual API Key input in sidebar =====
        if env == AppEnv.DEV:
            st.subheader("Claude API Settings (Dev)")

            api_key_input = st.text_input(
                "Claude API Key",
                value=st.session_state.get("claude_api_key", ""),
                type="password",
                help="Dev only: input / override Anthropic Claude API Key here.",
                key="claude_api_key_input",
            )

            if api_key_input:
                st.session_state["claude_api_key"] = api_key_input
                st.success("✅ API Key saved to current dev session")

        # ===== Shared: show effective Key status (dev / prod) =====
        effective_key = get_claude_api_key()
        st.subheader("Claude API Status")

        if effective_key:
            masked = (
                effective_key[:4] + "..." + effective_key[-4:]
                if len(effective_key) > 8
                else "***"
            )
            if env == AppEnv.PROD:
                st.info(f"Claude Key (PROD): ✅ Configured on server ({masked})")
                st.caption("Front-end input is disabled in this environment. Please configure the key on the server.")
            else:
                st.info(f"Claude Key (DEV): ✅ Active ({masked})")
        else:
            st.error("Claude Key: ❌ Not configured")
            st.caption("Please configure `ANTHROPIC_API_KEY` in server environment variables or `.streamlit/secrets.toml`.")

        # 強制使用 API 模式（保留原本行為）
        st.session_state["data_source"] = "Claude API"

