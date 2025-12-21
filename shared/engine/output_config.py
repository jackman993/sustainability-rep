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
import os

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

# 診斷信息：打印路徑計算結果
print(f"[DIAGNOSIS] output_config.py 位置: {Path(__file__).resolve()}")
print(f"[DIAGNOSIS] PROJECT_ROOT 計算結果: {PROJECT_ROOT}")
print(f"[DIAGNOSIS] OUTPUT_ROOT: {OUTPUT_ROOT}")
print(f"[DIAGNOSIS] OUTPUT_ROOT 是否存在: {OUTPUT_ROOT.exists()}")
print(f"[DIAGNOSIS] OUTPUT_ROOT 父目錄是否存在: {OUTPUT_ROOT.parent.exists()}")
print(f"[DIAGNOSIS] OUTPUT_ROOT 父目錄是否可寫: {OUTPUT_ROOT.parent.exists() and os.access(OUTPUT_ROOT.parent, os.W_OK) if OUTPUT_ROOT.parent.exists() else False}")
print(f"[DIAGNOSIS] OUTPUT_ROOT 是否可寫: {OUTPUT_ROOT.exists() and os.access(OUTPUT_ROOT, os.W_OK) if OUTPUT_ROOT.exists() else False}")

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
    
    # 強制創建目錄（多次嘗試）
    print(f"[DIAGNOSIS] 嘗試創建目錄: {session_dir}")
    print(f"[DIAGNOSIS] SESSIONS_DIR: {SESSIONS_DIR}")
    print(f"[DIAGNOSIS] SESSIONS_DIR 是否存在: {SESSIONS_DIR.exists()}")
    print(f"[DIAGNOSIS] SESSIONS_DIR 是否可寫: {SESSIONS_DIR.exists() and os.access(SESSIONS_DIR, os.W_OK) if SESSIONS_DIR.exists() else False}")
    
    # 先確保父目錄（SESSIONS_DIR）存在
    if not SESSIONS_DIR.exists():
        print(f"[DIAGNOSIS] 父目錄不存在，先創建父目錄: {SESSIONS_DIR}")
        try:
            SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as parent_ex:
            print(f"[WARNING] 創建父目錄失敗: {parent_ex}")
            try:
                os.makedirs(str(SESSIONS_DIR), exist_ok=True, mode=0o777)
            except Exception as parent_ex2:
                print(f"[ERROR] os.makedirs 創建父目錄也失敗: {parent_ex2}")
                raise Exception(f"無法創建父目錄 {SESSIONS_DIR}: {parent_ex}, {parent_ex2}")
    
    # 方法 1: 標準 mkdir
    try:
        session_dir.mkdir(parents=True, exist_ok=True)
        print(f"[DIAGNOSIS] mkdir() 調用完成")
    except Exception as e1:
        print(f"[WARNING] mkdir() 失敗: {e1}")
        # 方法 2: 逐級創建
        try:
            session_dir.mkdir(exist_ok=True)
            print(f"[DIAGNOSIS] 逐級創建成功")
        except Exception as e2:
            print(f"[WARNING] 逐級創建失敗: {e2}")
            # 方法 3: 使用 os.makedirs 強制創建
            try:
                os.makedirs(str(session_dir), exist_ok=True, mode=0o777)
                print(f"[DIAGNOSIS] os.makedirs() 成功")
            except Exception as e3:
                print(f"[ERROR] 所有創建方法都失敗: {e3}")
                raise Exception(f"無法創建輸出目錄 {session_dir}: {e3}")
    
    # 驗證目錄是否真的存在
    if not session_dir.exists():
        raise Exception(f"目錄創建失敗，目錄不存在: {session_dir}")
    
    # 驗證目錄是否可寫，並嘗試修復權限
    if not os.access(session_dir, os.W_OK):
        print(f"[WARNING] 目錄存在但不可寫: {session_dir}")
        # 嘗試修改權限
        try:
            os.chmod(str(session_dir), 0o777)
            print(f"[DIAGNOSIS] 嘗試修改權限成功")
            # 再次檢查
            if not os.access(session_dir, os.W_OK):
                print(f"[WARNING] 修改權限後仍不可寫: {session_dir}")
        except Exception as e:
            print(f"[WARNING] 無法修改權限: {e}")
    
    print(f"[DIAGNOSIS] 最終目錄狀態: 存在={session_dir.exists()}, 可寫={os.access(session_dir, os.W_OK)}")
    print(f"[DIAGNOSIS] Session directory 是否可寫: {os.access(session_dir, os.W_OK)}")
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

