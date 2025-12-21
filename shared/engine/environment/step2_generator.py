"""
Environment Step 2 報告生成引擎
生成 12 頁 Environment 報告：
- 第 1 頁：Cover 頁
- 第 2 頁：環境政策
- 第 3 頁：環境管理架構
- 第 4 頁：環境目標與指標
- 第 5-11 頁：TCFD 報告（7 頁，插入）
- 第 12 頁：總結/附錄
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pathlib import Path
import streamlit as st
import logging

from ..path_manager import get_environment_output_path, update_session_activity
from ..tcfd_merger import insert_tcfd_slides
from ..session_cleanup import smart_cleanup

logger = logging.getLogger(__name__)

def generate_environment_report() -> Path:
    """
    生成 Environment 報告（12 頁）
    
    Returns:
        生成的報告文件路徑
    """
    # 清理過期會話
    smart_cleanup()
    
    logger.info("開始生成 Environment 報告")
    
    # 創建新的 Presentation
    prs = Presentation()
    
    # 第 1 頁：Cover 頁
    logger.info("生成第 1 頁：Cover 頁")
    add_cover_page(prs)
    
    # 第 2 頁：環境政策
    logger.info("生成第 2 頁：環境政策")
    add_environment_policy_page(prs)
    
    # 第 3 頁：環境管理架構
    logger.info("生成第 3 頁：環境管理架構")
    add_environment_management_page(prs)
    
    # 第 4 頁：環境目標與指標
    logger.info("生成第 4 頁：環境目標與指標")
    add_environment_targets_page(prs)
    
    # 第 5-11 頁：插入 TCFD 報告（7 頁）
    logger.info("插入 TCFD 報告（第 5-11 頁，7 頁）")
    prs = insert_tcfd_slides(prs, insert_position=5)
    
    # 第 12 頁：總結/附錄（在 TCFD 插入後添加）
    logger.info("生成第 12 頁：總結/附錄")
    add_summary_page(prs)
    
    # 更新活動時間
    update_session_activity()
    
    # 保存報告
    output_path = get_environment_output_path()
    prs.save(str(output_path))
    
    logger.info(f"Environment 報告已保存: {output_path}")
    
    # 更新 session_state
    st.session_state["environment_report_file"] = str(output_path)
    
    return output_path

def add_cover_page(prs: Presentation):
    """添加 Cover 頁（第 1 頁）"""
    # 使用標題幻燈片佈局
    slide_layout = prs.slide_layouts[0]  # 標題幻燈片
    slide = prs.slides.add_slide(slide_layout)
    
    # 設置標題
    title = slide.shapes.title
    title.text = "環境報告"
    
    # 設置副標題（如果存在）
    if len(slide.placeholders) > 1:
        subtitle = slide.placeholders[1]
        subtitle.text = "Environment Report"
    
    logger.debug("Cover 頁已添加")

def add_environment_policy_page(prs: Presentation):
    """添加環境政策頁（第 2 頁）"""
    slide_layout = prs.slide_layouts[1]  # 標題和內容
    slide = prs.slides.add_slide(slide_layout)
    
    # 設置標題
    title = slide.shapes.title
    title.text = "環境政策"
    
    # 添加內容
    if len(slide.placeholders) > 1:
        content = slide.placeholders[1]
        content.text = "環境政策內容..."
        # TODO: 根據實際需求填充內容
    
    logger.debug("環境政策頁已添加")

def add_environment_management_page(prs: Presentation):
    """添加環境管理架構頁（第 3 頁）"""
    slide_layout = prs.slide_layouts[1]  # 標題和內容
    slide = prs.slides.add_slide(slide_layout)
    
    # 設置標題
    title = slide.shapes.title
    title.text = "環境管理架構"
    
    # 添加內容
    if len(slide.placeholders) > 1:
        content = slide.placeholders[1]
        content.text = "環境管理架構內容..."
        # TODO: 根據實際需求填充內容
    
    logger.debug("環境管理架構頁已添加")

def add_environment_targets_page(prs: Presentation):
    """添加環境目標與指標頁（第 4 頁）"""
    slide_layout = prs.slide_layouts[1]  # 標題和內容
    slide = prs.slides.add_slide(slide_layout)
    
    # 設置標題
    title = slide.shapes.title
    title.text = "環境目標與指標"
    
    # 添加內容
    if len(slide.placeholders) > 1:
        content = slide.placeholders[1]
        content.text = "環境目標與指標內容..."
        # TODO: 根據實際需求填充內容
    
    logger.debug("環境目標與指標頁已添加")

def add_summary_page(prs: Presentation):
    """添加總結/附錄頁（第 12 頁）"""
    slide_layout = prs.slide_layouts[1]  # 標題和內容
    slide = prs.slides.add_slide(slide_layout)
    
    # 設置標題
    title = slide.shapes.title
    title.text = "總結與附錄"
    
    # 添加內容
    if len(slide.placeholders) > 1:
        content = slide.placeholders[1]
        content.text = "總結與附錄內容..."
        # TODO: 根據實際需求填充內容
    
    logger.debug("總結/附錄頁已添加")

