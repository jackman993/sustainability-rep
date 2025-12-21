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
import streamlit as st

def _get_project_root() -> Path:
    """獲取項目根目錄（包含 app.py 的目錄）"""
    # 從當前文件位置向上查找，直到找到包含 app.py 的目錄
    current = Path(__file__).resolve()
    # 當前文件在 shared/engine/output_config.py，向上兩級到項目根目錄
    # 路徑結構：項目根目錄/shared/engine/output_config.py
    # 所以向上兩級：current.parent.parent 就是項目根目錄
    for parent in [current.parent.parent, current.parent.parent.parent]:
        if (parent / "app.py").exists():
            return parent
    # 如果找不到，假設當前目錄向上兩級是項目根目錄
    return current.parent.parent

# 輸出根目錄（放在項目根目錄下，兩層結構）
PROJECT_ROOT = _get_project_root()
OUTPUT_ROOT = PROJECT_ROOT / "output"
SESSIONS_DIR = OUTPUT_ROOT  # 直接使用 output 作為會話根目錄

def get_session_id():
    """獲取當前會話 ID"""
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())
    return st.session_state['session_id']

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

