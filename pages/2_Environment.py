"""
Step 2: Environment Report
"""
# Page title - single source of truth (must match docstring above)
PAGE_TITLE = "Step 2: Environment Report"

import streamlit as st
from pathlib import Path
import sys

# Add project root to Python path (make sure we can import shared)
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

# Show TCFD / Emission summaries (via DataBroker / Skill Agent)
tcfd_summary = DataBroker.get_tcfd_summary()
emission_summary = DataBroker.get_emission_summary()

if not tcfd_summary:
    st.warning("⚠️ No TCFD summary found. Please complete Step 1 and generate the TCFD report so key climate information can be reused in this chapter.")
else:
    with st.expander("TCFD Summary (for Environment / other chapters)", expanded=False):
        st.write("Minimal climate key information aggregated from Step 1, which can be reused in LLM prompts for other chapters:")
        st.json(tcfd_summary)

if emission_summary:
    with st.expander("Emission Summary (for Environment / other chapters)", expanded=False):
        st.write("Carbon emission summary from Step 1, which can be used for subsequent chapter text and charts:")
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
    # Generate full Environment PPTX (LLM content + 7 TCFD pages)
    with st.spinner("Generating environment report... (this may take a while)"):
        progress = st.progress(0)
        status = st.empty()

        try:
            # 0. Check API Key
            api_key = get_claude_api_key()
            if not api_key:
                st.error("❌ Claude API Key is not configured.")
                st.info("💡 Please configure `ANTHROPIC_API_KEY` in server secrets or environment variables.")
                st.stop()

            # 1. Prepare data
            status.text("Step 1/4: Preparing data & templates...")
            progress.progress(10)

            # Industry and emission data from Step 1
            industry = st.session_state.get("carbon_calc_industry", "Manufacturing")
            emission_data = st.session_state.get("carbon_emission") or {}

            # Get total emissions from Skill Agent or raw result (prefer Skill Agent)
            total_emission = None
            if emission_summary and isinstance(emission_summary, dict):
                total_emission = emission_summary.get("total_tco2e")
            if total_emission is None and isinstance(emission_data, dict):
                total_emission = (
                    emission_data.get("total_tco2e")
                    or emission_data.get("Total_S1S2")
                    or (emission_data.get("full_result") or {}).get("Total_S1S2")
                )

            # Company size / budget / revenue info (if available)
            estimated_revenue = st.session_state.get("estimated_annual_revenue", {})
            revenue_k = estimated_revenue.get("k_value")
            revenue_currency = estimated_revenue.get("currency", "USD")
            revenue_display = (
                f"{revenue_k:.0f}K {revenue_currency}" if revenue_k else "Unknown"
            )

            company_profile = {
                "size": st.session_state.get("company_size", "Small and Medium"),
                "industry": industry,
                "revenue_display": revenue_display,
                "budget_display": st.session_state.get(
                    "energy_saving_budget_display", "appropriate"
                ),
                "total_emission_tco2e": total_emission,
            }

            # TCFD output folder: prefer our app's standard path
            tcfd_report_path = get_tcfd_report_path()
            tcfd_output_folder = (
                str(tcfd_report_path.parent) if tcfd_report_path else None
            )

            # 2. Call Environment engine (runs LLM + inserts TCFD)
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

            # 3. Save to standard output path
            status.text("Step 3/4: Saving PPTX file...")
            progress.progress(70)

            output_path = get_environment_output_path()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            prs.save(str(output_path))

            # 4. Check file exists + show download button
            status.text("Step 4/4: Preparing download...")
            progress.progress(90)

            if not output_path.exists():
                st.error("❌ Failed to generate Environment report: output file not found. Please check backend logs for [DEBUG] / [ERROR] messages.")
            else:
                progress.progress(100)
                status.text("✅ Done.")

                file_size_kb = output_path.stat().st_size / 1024
                st.success("✅ Environment report generated successfully! (includes TCFD slides & LLM content)")
                st.caption(f"File path: `{output_path}`; size ≈ {file_size_kb:.2f} KB")

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
                    st.error(f"❌ Report generated, but failed to create download button: {e}")
                    st.info("💡 Please download the file directly from the server file system.")

        except Exception as e:
            import traceback

            st.error(f"❌ Error occurred during Environment report generation: {e}")
            with st.expander("Detailed error trace", expanded=True):
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
