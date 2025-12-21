"""
會話清理工具 - 方案 A
在請求時檢查並清理過期會話（基於文件修改時間）
"""
import time
import shutil
from pathlib import Path
import logging
import streamlit as st
from .output_config import SESSIONS_DIR

logger = logging.getLogger(__name__)

MAX_SESSION_AGE_HOURS = 2  # 會話最大保留時間（2 小時）

def cleanup_expired_sessions(max_age_hours: int = MAX_SESSION_AGE_HOURS):
    """
    清理超過指定時間未活動的會話（方案 A）
    
    Args:
        max_age_hours: 會話最大保留時間（小時）
    """
    if not SESSIONS_DIR.exists():
        return
    
    cutoff_time = time.time() - (max_age_hours * 3600)
    cleaned_count = 0
    
    for session_dir in SESSIONS_DIR.iterdir():
        if not session_dir.is_dir():
            continue
        
        # 檢查目錄修改時間（最後活動時間）
        mtime = session_dir.stat().st_mtime
        
        if mtime < cutoff_time:
            try:
                shutil.rmtree(session_dir)
                cleaned_count += 1
                logger.info(f"已清理過期會話: {session_dir.name}")
            except Exception as e:
                logger.error(f"清理會話失敗 {session_dir.name}: {e}")
    
    if cleaned_count > 0:
        logger.info(f"共清理 {cleaned_count} 個過期會話")

def smart_cleanup():
    """
    智能清理：在請求時檢查並清理過期會話
    只在第一次請求時執行（避免每次都執行）
    """
    # 只在第一次請求時執行（避免每次都執行）
    if 'cleanup_done' not in st.session_state:
        try:
            cleanup_expired_sessions()
            st.session_state['cleanup_done'] = True
        except Exception as e:
            logger.error(f"清理任務錯誤: {e}")
            # 清理失敗不影響主流程

