from __future__ import annotations

"""
統一的 API Key 存取工具
- dev 環境：允許 sidebar / session_state 覆蓋，並可回退到 secrets / 環境變數
- prod 環境：只允許從伺服器端設定（secrets / 環境變數），不讀 session_state
"""

import os
from typing import Optional

from .env import get_app_env, AppEnv


def get_claude_api_key() -> Optional[str]:
    """
    統一取得 Anthropic Claude API Key 的入口。

    優先順序：
    - PROD: secrets.toml > 環境變數
    - DEV:  session_state > secrets.toml > 環境變數
    """
    env = get_app_env()

    # 延遲導入 streamlit，避免在非 Streamlit 環境中出錯
    try:
        import streamlit as st  # type: ignore
    except ImportError:  # 非 Streamlit 環境
        st = None  # type: ignore

    # ===== 正式環境：只允許伺服器端設定 =====
    if env == AppEnv.PROD:
        # 1) Streamlit secrets
        if st is not None:
            try:
                key = st.secrets.get("ANTHROPIC_API_KEY", None)
                if key:
                    return key
            except Exception:
                # 讀取失敗時忽略，改用環境變數
                pass

        # 2) 環境變數
        key = os.environ.get("ANTHROPIC_API_KEY")
        return key or None

    # ===== 開發環境：允許 sidebar / session_state 覆蓋 =====
    if st is not None:
        # 1) session_state（sidebar 設定）
        try:
            key = st.session_state.get("claude_api_key")
            if key:
                return key
        except Exception:
            pass

        # 2) secrets.toml
        try:
            key = st.secrets.get("ANTHROPIC_API_KEY", None)
            if key:
                return key
        except Exception:
            pass

    # 3) 環境變數（最終回退）
    key = os.environ.get("ANTHROPIC_API_KEY")
    return key or None

