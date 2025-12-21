"""
路徑管理工具
處理文件路徑的獲取和管理
"""
from pathlib import Path
import os
from .output_config import get_step_output_dir, OUTPUT_FILENAMES

# 延遲導入 streamlit，避免在非 Streamlit 環境中出錯
def _get_streamlit():
    """延遲導入 streamlit"""
    try:
        import streamlit as st
        return st
    except ImportError:
        return None

def get_tcfd_report_path() -> Path | None:
    """
    獲取 TCFD 報告路徑（兩層結構：output/{session_id}/TCFD_table.pptx）
    優先順序：session_state > 標準路徑
    """
    st = _get_streamlit()
    
    # 優先從 session_state 獲取
    if st is not None:
        try:
            if path := st.session_state.get("tcfd_report_file"):
                path_obj = Path(path)
                if path_obj.exists():
                    return path_obj
        except Exception as e:
            # session_state 訪問失敗，繼續使用標準路徑
            print(f"Warning: Failed to access session_state: {e}")
    
    # 從標準輸出目錄查找（兩層結構）
    try:
        session_dir = get_step_output_dir('tcfd')  # 現在直接返回會話目錄
        tcfd_file = session_dir / OUTPUT_FILENAMES['tcfd']
        if tcfd_file.exists():
            return tcfd_file
    except Exception as e:
        print(f"Warning: Failed to get standard output path: {e}")
    
    return None

def get_tcfd_output_path() -> Path:
    """獲取 TCFD 報告輸出路徑（兩層結構：output/{session_id}/TCFD_table.pptx）"""
    try:
        print("[DIAGNOSIS] ========== 路徑診斷開始 ==========")
        print("[DEBUG] Getting TCFD output path...")
        session_dir = get_step_output_dir('tcfd')  # 現在直接返回會話目錄
        print(f"[DIAGNOSIS] Session directory: {session_dir}")
        print(f"[DIAGNOSIS] Session directory (absolute): {session_dir.resolve()}")
        print(f"[DIAGNOSIS] Session directory 是否存在: {session_dir.exists()}")
        print(f"[DIAGNOSIS] Session directory 是否可寫: {os.access(session_dir.parent, os.W_OK) if session_dir.parent.exists() else False}")
        output_path = session_dir / OUTPUT_FILENAMES['tcfd']
        print(f"[DIAGNOSIS] Output path: {output_path}")
        print(f"[DIAGNOSIS] Output path (absolute): {output_path.resolve()}")
        print(f"[DIAGNOSIS] Output path 父目錄是否存在: {output_path.parent.exists()}")
        print(f"[DIAGNOSIS] Output path 父目錄是否可寫: {os.access(output_path.parent, os.W_OK) if output_path.parent.exists() else False}")
        print("[DIAGNOSIS] ========== 路徑診斷結束 ==========")
        return output_path
    except Exception as e:
        error_msg = f"[ERROR] Failed to get TCFD output path: {str(e)}"
        print(error_msg)
        import traceback
        full_traceback = traceback.format_exc()
        print(full_traceback)
        # 嘗試在 Streamlit UI 中顯示錯誤
        try:
            st = _get_streamlit()
            if st is not None:
                st.error(f"❌ 獲取 TCFD 輸出路徑失敗: {str(e)}")
                with st.expander("詳細錯誤信息", expanded=False):
                    st.code(full_traceback)
        except:
            pass
        raise Exception(error_msg) from e

def get_environment_output_path() -> Path:
    """獲取 Environment 報告輸出路徑（兩層結構：output/{session_id}/Environment_report.pptx）"""
    session_dir = get_step_output_dir('environment')  # 現在直接返回會話目錄
    return session_dir / OUTPUT_FILENAMES['environment']

def update_session_activity():
    """更新會話最後活動時間（通過更新目錄修改時間）"""
    try:
        from .output_config import get_session_output_dir
        session_dir = get_session_output_dir()
        # 觸摸目錄以更新修改時間
        try:
            import os
            os.utime(session_dir, None)
        except Exception as utime_error:
            # 失敗不影響主流程，只記錄警告
            print(f"Warning: Failed to update session activity time: {utime_error}")
    except Exception as e:
        # 失敗不影響主流程，只記錄警告
        print(f"Warning: Failed to update session activity: {e}")

