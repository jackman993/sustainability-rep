"""
Step 2: Environment Report
"""
# Page title - single source of truth (must match docstring above)
PAGE_TITLE = "Step 2: Environment Report"

import streamlit as st
from pathlib import Path
import sys

# 添加項目根目錄到 Python 路徑（確保能找到 shared 模組）
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from shared.ui.sidebar_config import render_sidebar_config
from shared.agents.data_broker import DataBroker
from shared.engine.environment.step2_generator import generate_environment_report

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="🌍",
    layout="wide"
)

# Sidebar: API Configuration (shared component)
render_sidebar_config()

st.title(PAGE_TITLE)

st.divider()

# Prerequisites
st.success("✅ Emission & TCFD completed")

# 顯示來自 TCFD 的摘要資料（透過 DataBroker / Skill Agent）
tcfd_summary = DataBroker.get_tcfd_summary()
if not tcfd_summary:
    st.warning("⚠️ 尚未找到 TCFD Summary。請先在 Step 1 生成 TCFD 報告，系統才會將關鍵氣候資訊帶入本章節。")
else:
    with st.expander("TCFD Summary（供 Environment / 其他章節使用）", expanded=False):
        st.write("以下為從 Step 1 彙整出的最小氣候關鍵資訊，之後可直接餵給 LLM Prompt：")
        st.json(tcfd_summary)

st.divider()

# Generate Section
st.subheader("Generate Environment Report")

st.info("""
**Environment section includes:**
- Detailed emission analysis
- TCFD climate risk assessment
- Environmental management measures
- Approximately 17 pages
""")

if st.button("Generate Environment Report", type="primary", use_container_width=True):
    # 產生實際的 Environment PPTX 報告
    with st.spinner("Generating environment report... (this may take a while)"):
        progress = st.progress(0)
        status = st.empty()

        try:
            status.text("Step 1/3: Preparing data & templates...")
            progress.progress(20)

            # 呼叫後端引擎，實際產出檔案（含 TCFD 7 頁）
            report_path = generate_environment_report()

            status.text("Step 2/3: Finalizing slides & saving file...")
            progress.progress(70)

            # 檔案存在性檢查
            if not report_path or not report_path.exists():
                st.error("❌ Environment 報告生成失敗：找不到輸出檔案。請查看終端日誌中的 [DEBUG] / [ERROR] 訊息。")
            else:
                progress.progress(100)
                status.text("Step 3/3: Ready to download.")

                file_size_kb = report_path.stat().st_size / 1024
                st.success("✅ Environment report generated successfully! (includes TCFD slides)")
                st.caption(f"檔案路徑：`{report_path}`，大小約 {file_size_kb:.2f} KB")

                # 建立下載按鈕
                try:
                    with open(report_path, "rb") as f:
                        file_bytes = f.read()
                    st.download_button(
                        "📥 Download Environment Report (Environment_report.pptx)",
                        data=file_bytes,
                        file_name="Environment_report.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True,
                        key="download_environment_report",
                    )
                except Exception as e:
                    st.error(f"❌ 報告已生成，但建立下載按鈕失敗：{e}")
                    st.info("💡 請從伺服器檔案系統手動下載此檔案。")

        except Exception as e:
            import traceback

            st.error(f"❌ Environment 報告生成過程發生錯誤：{e}")
            with st.expander("詳細錯誤資訊", expanded=True):
                st.code(traceback.format_exc())
        finally:
            progress.empty()
            status.empty()

st.divider()

# Navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("Previous", use_container_width=True):
        st.switch_page("pages/1_Emission_TCFD.py")

with col2:
    if st.button("Next", type="primary", use_container_width=True):
        st.switch_page("pages/3_Company.py")
