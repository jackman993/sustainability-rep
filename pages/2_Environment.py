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
from shared.config.api_keys import get_claude_api_key
from shared.engine.environment import generate_environment_pptx_for_streamlit
from shared.engine.path_manager import get_environment_output_path, get_tcfd_report_path

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

# 顯示來自 TCFD / Emission 的摘要資料（透過 DataBroker / Skill Agent）
tcfd_summary = DataBroker.get_tcfd_summary()
emission_summary = DataBroker.get_emission_summary()

if not tcfd_summary:
    st.warning("⚠️ 尚未找到 TCFD Summary。請先在 Step 1 生成 TCFD 報告，系統才會將關鍵氣候資訊帶入本章節。")
else:
    with st.expander("TCFD Summary（供 Environment / 其他章節使用）", expanded=False):
        st.write("以下為從 Step 1 彙整出的最小氣候關鍵資訊，之後可直接餵給 LLM Prompt：")
        st.json(tcfd_summary)

if emission_summary:
    with st.expander("Emission Summary（供 Environment / 其他章節使用）", expanded=False):
        st.write("以下為從 Step 1 彙整出的碳排摘要，可用於後續章節的文字與圖表：")
        st.json(emission_summary)

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
    # 產生完整的 Environment PPTX（包含 LLM 文字 + TCFD 7 頁）
    with st.spinner("Generating environment report... (this may take a while)"):
        progress = st.progress(0)
        status = st.empty()

        try:
            # 0. 檢查 API Key
            api_key = get_claude_api_key()
            if not api_key:
                st.error("❌ 系統尚未設定 Claude API Key。")
                st.info("💡 請在伺服器 secrets 或環境變數中設定 `ANTHROPIC_API_KEY`。")
                st.stop()

            # 1. 準備資料
            status.text("Step 1/4: Preparing data & templates...")
            progress.progress(10)

            # 產業與排放資料來自 Step1
            industry = st.session_state.get("carbon_calc_industry", "Manufacturing")
            emission_data = st.session_state.get("carbon_emission") or {}

            # 公司規模 / 預算資訊（如果有）
            estimated_revenue = st.session_state.get("estimated_annual_revenue", {})
            revenue_k = estimated_revenue.get("k_value")
            revenue_currency = estimated_revenue.get("currency", "USD")
            revenue_display = (
                f"{revenue_k:.0f}K {revenue_currency}" if revenue_k else "Unknown"
            )

            company_profile = {
                "size": st.session_state.get("company_size", "Small and Medium"),
                "revenue_display": revenue_display,
                "budget_display": st.session_state.get(
                    "energy_saving_budget_display", "appropriate"
                ),
            }

            # TCFD 輸出資料夾：優先使用我們 app 的標準路徑
            tcfd_report_path = get_tcfd_report_path()
            tcfd_output_folder = (
                str(tcfd_report_path.parent) if tcfd_report_path else None
            )

            # 2. 呼叫 Environment 引擎（會跑 LLM + 插入 TCFD）
            status.text("Step 2/4: Generating slides with LLM content...")
            progress.progress(40)

            prs = generate_environment_pptx_for_streamlit(
                api_key=api_key,
                industry=industry,
                emission_data=emission_data,
                tcfd_output_folder=tcfd_output_folder,
                emission_output_folder=None,
                company_profile=company_profile,
                test_mode=False,
            )

            # 3. 儲存到標準輸出路徑
            status.text("Step 3/4: Saving PPTX file...")
            progress.progress(70)

            output_path = get_environment_output_path()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            prs.save(str(output_path))

            # 4. 檔案存在性檢查 + 下載按鈕
            status.text("Step 4/4: Preparing download...")
            progress.progress(90)

            if not output_path.exists():
                st.error(
                    "❌ Environment 報告生成失敗：找不到輸出檔案。請查看終端日誌中的 [DEBUG] / [ERROR] 訊息。"
                )
            else:
                progress.progress(100)
                status.text("✅ Done.")

                file_size_kb = output_path.stat().st_size / 1024
                st.success(
                    "✅ Environment report generated successfully! (includes TCFD slides & LLM content)"
                )
                st.caption(f"檔案路徑：`{output_path}`，大小約 {file_size_kb:.2f} KB")

                # 建立下載按鈕
                try:
                    with open(output_path, "rb") as f:
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
