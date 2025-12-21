"""
統一輸出配置模組
定義標準化的輸出目錄結構和文件命名規則

路徑結構（兩層，output 在項目根目錄）：
output\{session_id}\TCFD_table.pptx
output\{session_id}\Environment_report.pptx
output\{session_id}\Company_report.pptx

項目結構：
項目根目錄/
├── output/              ← 輸出目錄（兩層：output/{session_id}/）
│   └── {session_id}/
│       └── TCFD_table.pptx
└── shared/
    └── engine/          ← 引擎代碼
"""
from pathlib import Path
import uuid

# 延遲導入 streamlit，避免在非 Streamlit 環境中出錯
def _get_streamlit():
    """延遲導入 streamlit"""
    try:
        import streamlit as st
        return st
    except ImportError:
        return None

# 輸出根目錄（直接寫死，不查找）
# 從 shared/engine/output_config.py 向上三級到項目根目錄
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_ROOT = PROJECT_ROOT / "output"
SESSIONS_DIR = OUTPUT_ROOT  # 直接使用 output 作為會話根目錄

def get_session_id():
    """獲取當前會話 ID"""
    st = _get_streamlit()
    if st is None:
        # 非 Streamlit 環境，返回臨時 ID
        session_id = str(uuid.uuid4())
        print(f"[DEBUG] Non-Streamlit environment, generated temp session_id: {session_id}")
        return session_id
    
    try:
        # 確保 session_state 可用
        if not hasattr(st, 'session_state'):
            session_id = str(uuid.uuid4())
            print(f"[WARNING] session_state not available, generated temp session_id: {session_id}")
            # 嘗試在 Streamlit UI 中顯示警告
            try:
                st.warning(f"⚠️ session_state 不可用，使用臨時 session_id: {session_id}")
            except:
                pass
            return session_id
        
        if 'session_id' not in st.session_state:
            session_id = str(uuid.uuid4())
            st.session_state['session_id'] = session_id
            print(f"[DEBUG] Created new session_id: {session_id}")
        else:
            session_id = st.session_state['session_id']
            print(f"[DEBUG] Using existing session_id: {session_id}")
        
        return session_id
    except Exception as e:
        # 如果訪問 session_state 失敗，返回臨時 ID
        session_id = str(uuid.uuid4())
        error_msg = f"[ERROR] Failed to get session_id: {e}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        # 嘗試在 Streamlit UI 中顯示錯誤
        try:
            st.error(f"❌ 獲取 session_id 失敗: {str(e)}")
            with st.expander("詳細錯誤信息", expanded=False):
                st.code(traceback.format_exc())
        except:
            pass
        return session_id

def get_session_output_dir():
    """獲取當前會話的輸出目錄（兩層結構：output\{session_id}）"""
    session_id = get_session_id()
    session_dir = SESSIONS_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

# 各步驟的輸出目錄（簡化：直接返回會話目錄，文件通過文件名區分）
def get_step_output_dir(step_name: str) -> Path:
    """
    獲取指定步驟的輸出目錄
    
    注意：現在所有文件都在同一個會話目錄下，通過文件名區分步驟
    """
    return get_session_output_dir()

# 標準化文件名
OUTPUT_FILENAMES = {
    'tcfd': 'TCFD_table.pptx',
    'environment': 'Environment_report.pptx',
    'company': 'Company_report.pptx',
}

