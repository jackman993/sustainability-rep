"""
路徑管理工具
處理文件路徑的獲取和管理
"""
from pathlib import Path
import streamlit as st
from .output_config import get_step_output_dir, OUTPUT_FILENAMES

def get_tcfd_report_path() -> Path | None:
    """
    獲取 TCFD 報告路徑（兩層結構：output/{session_id}/TCFD_table.pptx）
    優先順序：session_state > 標準路徑
    """
    # 優先從 session_state 獲取
    if path := st.session_state.get("tcfd_report_file"):
        path_obj = Path(path)
        if path_obj.exists():
            return path_obj
    
    # 從標準輸出目錄查找（兩層結構）
    session_dir = get_step_output_dir('tcfd')  # 現在直接返回會話目錄
    tcfd_file = session_dir / OUTPUT_FILENAMES['tcfd']
    if tcfd_file.exists():
        return tcfd_file
    
    return None

def get_environment_output_path() -> Path:
    """獲取 Environment 報告輸出路徑（兩層結構：output/{session_id}/Environment_report.pptx）"""
    session_dir = get_step_output_dir('environment')  # 現在直接返回會話目錄
    return session_dir / OUTPUT_FILENAMES['environment']

def update_session_activity():
    """更新會話最後活動時間（通過更新目錄修改時間）"""
    from .output_config import get_session_output_dir
    session_dir = get_session_output_dir()
    # 觸摸目錄以更新修改時間
    try:
        import os
        os.utime(session_dir, None)
    except Exception:
        pass  # 失敗不影響主流程

