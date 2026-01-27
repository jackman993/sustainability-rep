"""
Data Broker (Skill Agent) - 統一管理跨步驟共享的摘要資料

目前只實作 TCFD Summary，未來可以在這裡擴充：
- Emission Summary
- Environment Summary
- SASB / GRI Summary
"""
from typing import Any, Dict, Optional

import streamlit as st


class DataBroker:
    """薄層 Skill Agent：負責在 session_state 中讀寫共享資料。"""

    # ---------- TCFD Summary ----------
    TCFD_KEY = "tcfd_summary"

    @staticmethod
    def set_tcfd_summary(summary: Dict[str, Any]) -> None:
        """寫入或更新 TCFD Summary。"""
        if not isinstance(summary, dict):
            raise ValueError("tcfd_summary 必須是 dict")
        st.session_state[DataBroker.TCFD_KEY] = summary

    @staticmethod
    def get_tcfd_summary(default: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """讀取 TCFD Summary，如果不存在則回傳 default。"""
        return st.session_state.get(DataBroker.TCFD_KEY, default)

    @staticmethod
    def has_tcfd_summary() -> bool:
        """是否已經有 TCFD Summary。"""
        return DataBroker.TCFD_KEY in st.session_state

    # ---------- Emission Summary（碳排摘要） ----------
    EMISSION_KEY = "emission_summary"

    @staticmethod
    def set_emission_summary(summary: Dict[str, Any]) -> None:
        """寫入或更新碳排摘要（供 Environment / Company / Governance 共用）。"""
        if not isinstance(summary, dict):
            raise ValueError("emission_summary 必須是 dict")
        st.session_state[DataBroker.EMISSION_KEY] = summary

    @staticmethod
    def get_emission_summary(default: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """讀取碳排摘要，如果不存在則回傳 default。"""
        return st.session_state.get(DataBroker.EMISSION_KEY, default)

    @staticmethod
    def has_emission_summary() -> bool:
        """是否已經有碳排摘要。"""
        return DataBroker.EMISSION_KEY in st.session_state


