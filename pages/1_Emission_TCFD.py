"""
Step 1: Emission & TCFD
"""
# Page title - single source of truth (must match docstring above)
PAGE_TITLE = "Step 1: Emission & TCFD"

import streamlit as st
from pathlib import Path
import sys

# Add project root to Python path (make sure we can import shared)
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from shared.engine.carbon import render_calculator
from shared.ui.sidebar_config import render_sidebar_config
from shared.agents.data_broker import DataBroker
from shared.config.api_keys import get_claude_api_key

# TCFD 模組導入 - 延遲導入，避免頁面崩潰
TCFD_AVAILABLE = False
TCFD_PAGES = {}
generate_table = None
generate_all_tables = None

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="🌱",
    layout="wide"
)

# Sidebar: API Configuration (shared component)
render_sidebar_config()

st.title(PAGE_TITLE)

st.divider()

# Sub-steps
st.subheader("Sub-steps")

tab1, tab2 = st.tabs(["1.1 Emission", "1.2 TCFD Tables"])

with tab1:
    # Embed emission calculator component
    # Compact mode: no title (page already has title), show region selection
    render_calculator(
        show_title=False,      # Don't show calculator title (page already has title)
        show_region=True,       # Show region selection
        compact_mode=True,      # Compact mode for better fit in tab
        default_region="TW"     # Default region
    )
    
    # Show calculation summary if available
    if st.session_state.get("carbon_calc_done") and st.session_state.get("carbon_emission"):
        st.divider()
        st.success("✅ Emission calculation completed! Results are saved and can be used in subsequent steps.")

with tab2:
    st.subheader("🏭 TCFD Complete Report Generator")
    
    # 嘗試導入 TCFD 模組（延遲導入）
    if not TCFD_AVAILABLE:
        try:
            from shared.engine.tcfd import generate_combined_pptx
            TCFD_AVAILABLE = True
        except Exception as e:
            st.error(f"TCFD module error: {str(e)}")
            TCFD_AVAILABLE = False
    
    # 獲取數據
    industry = st.session_state.get("carbon_calc_industry", "Manufacturing")
    carbon_emission = st.session_state.get("carbon_emission")
    estimated_revenue = st.session_state.get("estimated_annual_revenue", {})
    revenue_k = estimated_revenue.get("k_value", 0)
    revenue_currency = estimated_revenue.get("currency", "USD")
    revenue_str = f"{revenue_k:.0f}K {revenue_currency}" if revenue_k > 0 else "N/A"
    
    # Show current data
    st.info(f"📊 **Current Data**: Industry: {industry} | Emissions: {carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e | Revenue: {revenue_str}")
    
    st.divider()
    
    # API Key status (via unified get_claude_api_key)
    api_key = get_claude_api_key()
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        st.info(f"ℹ️ **API Key**: ✅ Configured ({masked_key})")
    else:
        st.warning("⚠️ **API Key**: Not configured. Please configure in the left sidebar.")
    
    st.divider()
    
    # Show report contents description
    st.markdown("""
    **Report Contents:**
    - Complete TCFD report with 7 tables:
      1. Transformation Risks
      2. Physical Risks  
      3. Opportunities (Resource & Energy)
      4. Opportunities (Products & Services)
      5. Metrics and Targets
      6. Systemic Risk Control
      7. Operational Resilience
    - Executive summary (English, ~250 words)
    """)
    
    # Generate button
    generate_btn = st.button("🚀 Generate Complete TCFD Report", type="primary", use_container_width=True, key="tcfd_btn_tab2")
    
    # 顯示生成狀態（如果有）
    if st.session_state.get("tcfd_report_generated_tab2"):
        st.success("✅ TCFD Report generated successfully!")
        st.session_state["tcfd_report_generated_tab2"] = False
    
    # 如果按鈕被點擊，執行生成邏輯
    if generate_btn:
        if not TCFD_AVAILABLE:
            st.error("❌ TCFD module is not available. Please check the module files.")
            st.stop()
        
        # 確保導入 generate_combined_pptx
        from shared.engine.tcfd import generate_combined_pptx
        
        # 統一取得 API Key（必須配置）
        api_key = get_claude_api_key() or ""
        
        # 調試信息
        print(f"[DEBUG] api_key exists: {bool(api_key)}")
        print(f"[DEBUG] api_key length: {len(api_key) if api_key else 0}")
        print(f"[DEBUG] api_key_locked: {st.session_state.get('api_key_locked', False)}")
        
        # If no API Key, show error and stop
        if not api_key:
            st.error("❌ API Key is not configured!")
            st.info("💡 Please configure the Claude API Key in the left sidebar (API Configuration).")
            st.info("💡 Or create a `.streamlit/secrets.toml` file and add `ANTHROPIC_API_KEY = \"your-key-here\"`.")
            st.stop()
        
        # 創建進度顯示
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Generate executive summary
            status_text.text("Step 1/3: Generating executive summary...")
            progress_bar.progress(20)
            
            # Use LLM API to generate summary (requires API Key)
            summary = ""
            try:
                from shared.engine.tcfd.main import call_claude_api
                summary_prompt = f"""Please write a 250-word summary for the following TCFD climate risk report:

Industry: {industry}
Total Carbon Emissions: {carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e
Revenue: {revenue_str}

The report contains 7 tables covering: Transformation Risks, Physical Risks, Opportunities (Resource & Energy Efficiency, Products & Services), Metrics and Targets, Systemic Risk Control, and Operational Resilience.

Please write a concise summary in English, approximately 250 words, that highlights the key climate risks, opportunities, and strategic recommendations for the {industry} industry based on the TCFD framework analysis."""
                print(f"[DEBUG] Calling Claude API to generate summary, API Key length: {len(api_key)}")
                summary = call_claude_api(summary_prompt, api_key)
                print(f"[DEBUG] Claude API call succeeded, summary length: {len(summary)}")
                summary = summary.split('\n\n')[0].strip()
                if len(summary.split()) > 300:
                    words = summary.split()[:250]
                    summary = ' '.join(words) + "..."
                st.success("✅ LLM summary generated successfully")
            except Exception as e:
                error_msg = str(e)
                print(f"[ERROR] Claude API call failed: {error_msg}")
                import traceback
                traceback.print_exc()
                st.error(f"❌ LLM call failed: {error_msg}")
                st.info("💡 Please check: 1) API Key correctness 2) Network connection 3) Backend logs for detailed error messages.")
                st.stop()
            
            # Step 2: Generate PPTX
            status_text.text("Step 2/3: Generating TCFD tables (this may take a few minutes)...")
            progress_bar.progress(50)
            
            from pathlib import Path
            template_path = Path(__file__).parent.parent / "shared" / "engine" / "tcfd" / "handdrawppt.pptx"
            
            # Show debug info
            debug_info = st.empty()
            debug_info.info("🔍 Debug mode: showing detailed execution information...")
            
            # Show session_id (if available)
            try:
                session_id = st.session_state.get('session_id', 'NOT SET')
                debug_info.text(f"📋 Session ID: {session_id}")
            except:
                debug_info.text("📋 Session ID: unavailable")
            
            # Error display container (ensure errors are visible)
            error_container = st.container()
            
            # Debug info
            print(f"[DEBUG] Calling generate_combined_pptx:")
            print(f"  - api_key exists: {bool(api_key)}")
            print(f"  - api_key length: {len(api_key) if api_key else 0}")
            
            try:
                output_file = generate_combined_pptx(
                    output_filename="TCFD_table.pptx",
                    template_path=template_path if template_path.exists() else None,
                    industry=industry,
                    revenue=revenue_str,
                    carbon_emission=carbon_emission,
                    llm_api_key=api_key,  # 必須提供 API Key
                    llm_provider="anthropic",  # 使用 Anthropic
                    use_mock=False  # 不使用 Mock
                )
            except Exception as gen_error:
                # Capture exceptions during generation
                error_container.error(f"❌ Error occurred during TCFD report generation: {str(gen_error)}")
                with error_container.expander("🔍 Detailed error trace", expanded=True):
                    import traceback
                    error_container.code(traceback.format_exc())
                error_container.info("💡 Please also check backend logs for detailed diagnostics.")
                progress_bar.empty()
                status_text.empty()
                debug_info.empty()
                st.stop()
            
            # Step 3: Finalize
            status_text.text("Step 3/3: Finalizing report...")
            progress_bar.progress(90)
            
            # Clear debug info
            debug_info.empty()
            
            # Show file confirmation (backup check even if generate_combined_pptx already reported success)
            if output_file and hasattr(output_file, 'exists') and output_file.exists():
                try:
                    file_size = output_file.stat().st_size
                    file_size_kb = file_size / 1024
                    st.info(
                        f"📦 **File confirmed**: `{output_file}`\n\n"
                        f"📊 **File size**: {file_size_kb:.2f} KB"
                    )
                except Exception:
                    pass
            
            if output_file is None:
                error_container.error("❌ Failed to generate PPTX: function returned None.")
                error_container.info("💡 This usually means an internal exception was handled but not surfaced.")
                error_container.info("💡 Please check backend logs for [ERROR] / [DEBUG] entries.")
                progress_bar.empty()
                status_text.empty()
                st.stop()
            
            if not hasattr(output_file, 'exists'):
                error_detail = f"❌ Invalid return path object: {type(output_file)}"
                st.error(error_detail)
                st.code(f"Return object: {output_file}")
                raise Exception(error_detail)
            
            if not output_file.exists():
                error_detail = f"❌ File does not exist (expected path: {output_file})"
                st.error(error_detail)
                
                # Show detailed debug information
                with st.expander("🔍 Debug information", expanded=True):
                    st.write(f"**Return path type**: {type(output_file)}")
                    st.write(f"**Return path**: {output_file}")
                    st.write(f"**Absolute path**: {output_file.resolve() if hasattr(output_file, 'resolve') else 'N/A'}")
                    st.write(f"**Parent dir**: {output_file.parent if hasattr(output_file, 'parent') else 'N/A'}")
                    st.write(f"**Parent dir exists**: {output_file.parent.exists() if hasattr(output_file, 'parent') else 'N/A'}")
                    
                    # 檢查 output 目錄
                    from pathlib import Path
                    output_root = Path(__file__).parent.parent / "output"
                    st.write(f"**Output root**: {output_root}")
                    st.write(f"**Output root exists**: {output_root.exists()}")
                    
                    if output_root.exists():
                        session_dirs = [d for d in output_root.iterdir() if d.is_dir()]
                        st.write(f"**Session dir count**: {len(session_dirs)}")
                        for session_dir in session_dirs[:5]:
                            files = list(session_dir.glob("*.pptx"))
                            st.write(f"  - {session_dir.name}: {len(files)} PPTX file(s)")
                
                st.info("💡 Please check backend logs for detailed error information and diagnostics.")
                raise Exception(error_detail)
            
            progress_bar.progress(100)
            status_text.text("✅ Report generation completed!")
            
            # 保存到 session_state
            st.session_state["tcfd_report_file"] = output_file
            st.session_state["tcfd_report_summary"] = summary
            st.session_state["tcfd_report_generated_tab2"] = True

            # Build and save simplified TCFD Summary (for other chapters)
            try:
                total_emission = None
                if carbon_emission and isinstance(carbon_emission, dict):
                    # Prefer total_tco2e; fall back to full_result["Total_S1S2"] if needed
                    total_emission = carbon_emission.get("total_tco2e")
                    if total_emission is None and isinstance(carbon_emission.get("full_result"), dict):
                        total_emission = carbon_emission["full_result"].get("Total_S1S2")
                # Ensure numeric or None
                total_emission = float(total_emission) if total_emission is not None else None

                tcfd_summary = {
                    "industry": industry,
                    "total_emission_tco2e": total_emission,
                    "revenue_k_ntd": float(revenue_k) if revenue_k else None,
                    "key_climate_points": [
                        f"Our company operates in the {industry} sector and faces significant climate-related transition and physical risks as the global economy moves toward net zero.",
                        f"The most recent greenhouse gas inventory indicates total Scope 1 and 2 emissions of approximately {total_emission} tCO₂e (covering direct fuel use and purchased electricity), highlighting our current dependency on energy- and carbon-intensive activities.",
                        f"With annual revenue of around {revenue_k:.0f} K {revenue_currency}, we recognize that systematic investments in energy efficiency, renewable energy, and emissions reduction measures are essential to reduce operating costs, enhance competitiveness, and strengthen our sustainability performance."
                    ]
                }
                DataBroker.set_tcfd_summary(tcfd_summary)
                print(f"[DEBUG] TCFD Summary 已寫入 DataBroker：{tcfd_summary}")

                # Sync carbon emission summary (Emission Summary) for Step2 / other chapters
                try:
                    emission_full = carbon_emission.get("full_result", {}) if isinstance(carbon_emission, dict) else {}
                except Exception:
                    emission_full = {}
                emission_summary = {
                    "industry": industry,
                    "region": emission_full.get("Region") if isinstance(emission_full, dict) else None,
                    "total_tco2e": total_emission,
                    "scope1_tco2e": emission_full.get("Scope1_Total") if isinstance(emission_full, dict) else None,
                    "scope2_tco2e": emission_full.get("Scope2_Electricity") if isinstance(emission_full, dict) else None,
                    "scope3_minor_tco2e": emission_full.get("Scope3_Minor") if isinstance(emission_full, dict) else None,
                    "share_percent": emission_full.get("Share_Percent") if isinstance(emission_full, dict) else None,
                }
                DataBroker.set_emission_summary(emission_summary)
                print(f"[DEBUG] Emission Summary written to DataBroker: {emission_summary}")
            except Exception as e:
                print(f"[WARNING] Unable to build or save TCFD / Emission Summary: {e}")
            
            # Show success message
            st.success("✅ TCFD Report generated successfully!")
            
            # Show summary
            st.info(f"**Report Summary**:\n\n{summary}")
            
            # 顯示下載按鈕
            try:
                # 確保 output_file 是字符串路徑
                file_path = str(output_file) if hasattr(output_file, '__str__') else output_file
                
                # Confirm file exists
                if not Path(file_path).exists():
                    st.warning(f"⚠️ File path recorded but file is not accessible: {file_path}")
                    st.info("💡 File may have been saved but is not accessible in this session. Please check file system permissions.")
                else:
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        file_size = len(file_data)
                        st.download_button(
                            "📥 Download TCFD Report (TCFD_table.pptx)",
                            data=file_data,
                            file_name="TCFD_table.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True,
                            key="download_tcfd_report_tab2"
                        )
                        st.caption(f"File size: {file_size / 1024:.2f} KB")
            except Exception as download_error:
                st.error(f"❌ Failed to create download button: {str(download_error)}")
                st.info(f"💡 File saved at: `{output_file}`")
                st.info("💡 Please download the file manually from the server.")
                import traceback
                with st.expander("詳細錯誤信息", expanded=False):
                    st.code(traceback.format_exc())
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Generation failed: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    # If report already exists, show summary and download button
    elif st.session_state.get("tcfd_report_file") and st.session_state.get("tcfd_report_file").exists():
        st.success("✅ TCFD Report available!")
        
        # Show summary
        summary = st.session_state.get("tcfd_report_summary", "")
        if summary:
            st.info(f"**Report Summary**:\n\n{summary}")
        
        # Show download button
        output_file = st.session_state.get("tcfd_report_file")
        try:
            # 確保 output_file 是字符串路徑
            if isinstance(output_file, Path):
                file_path = str(output_file)
            else:
                file_path = output_file
            
            # Confirm file exists
            if not Path(file_path).exists():
                st.warning(f"⚠️ File path recorded but file is not accessible: {file_path}")
            else:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    file_size = len(file_data)
                    st.download_button(
                        "📥 Download TCFD Report (TCFD_table.pptx)",
                        data=file_data,
                        file_name="TCFD_table.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True,
                        key="download_tcfd_report_tab2_existing"
                    )
                    st.caption(f"File size: {file_size / 1024:.2f} KB")
        except Exception as download_error:
            st.error(f"❌ Failed to create download button: {str(download_error)}")
            st.info(f"💡 File path: `{output_file}`")
            import traceback
            with st.expander("詳細錯誤信息", expanded=False):
                st.code(traceback.format_exc())

st.divider()

# Generate TCFD Button - above Next button
if st.button("🚀 Generate TCFD Tables", type="primary", use_container_width=True, key="generate_tcfd_main"):
    # Check if TCFD module is available
    if not TCFD_AVAILABLE:
        try:
            from shared.engine.tcfd import TCFD_PAGES, generate_table, generate_all_tables, generate_combined_pptx
            TCFD_AVAILABLE = True
        except Exception as e:
            st.error(f"TCFD module error: {str(e)}")
            st.stop()
    
    # Ensure generate_combined_pptx is imported
    from shared.engine.tcfd import generate_combined_pptx
    
    # Get API Key (required)
    api_key = get_claude_api_key() or ""
    
    # If no API Key, show error and stop
    if not api_key:
        st.error("❌ API Key is not configured!")
        st.info("💡 Please configure Claude API Key in the left sidebar API Configuration.")
        st.stop()
    
    # Collect data
    industry = st.session_state.get("carbon_calc_industry", "Manufacturing")    
    carbon_emission = st.session_state.get("carbon_emission")
    estimated_revenue = st.session_state.get("estimated_annual_revenue", {})    
    revenue_k = estimated_revenue.get("k_value", 0)
    revenue_currency = estimated_revenue.get("currency", "USD")
    revenue_str = f"{revenue_k:.0f}K {revenue_currency}" if revenue_k > 0 else "N/A"

    with st.spinner("Generating TCFD report... (using Claude API)"):
        # 1. Generate executive summary (using LLM API, English)
        try:
            from shared.engine.tcfd.main import call_claude_api
            summary_prompt = f"""Please write a 250-word summary for the following TCFD climate risk report:

Industry: {industry}
Total Carbon Emissions: {carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e
Revenue: {revenue_str}

The report contains 7 tables covering: Transformation Risks, Physical Risks, Opportunities (Resource & Energy Efficiency, Products & Services), Metrics and Targets, Systemic Risk Control, and Operational Resilience.

Please write a concise summary in English, approximately 250 words, that highlights the key climate risks, opportunities, and strategic recommendations for the {industry} industry based on the TCFD framework analysis."""
            summary = call_claude_api(summary_prompt, api_key)
            # Clean summary, keep around 250 words
            summary = summary.split('\n\n')[0].strip()
            # If >300 words, truncate to ~250
            if len(summary.split()) > 300:
                words = summary.split()[:250]
                summary = ' '.join(words) + "..."
            st.success("✅ LLM summary generated successfully")
        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ LLM call failed: {error_msg}")
            st.info("💡 Please check: 1) API Key correctness 2) Network connection 3) Backend logs for detailed error messages.")
            st.stop()
        
        # 2. Generate PPTX with 7 tables (using handdrawppt.pptx template)
        try:
            from pathlib import Path
            
            # 模板路徑
            template_path = Path(__file__).parent.parent / "shared" / "engine" / "tcfd" / "handdrawppt.pptx"
            
            # Use generate_combined_pptx to generate combined PPTX
            output_file = generate_combined_pptx(
                output_filename="TCFD_table.pptx",
                template_path=template_path if template_path.exists() else None,
                industry=industry,
                revenue=revenue_str,
                carbon_emission=carbon_emission,
                llm_api_key=api_key,  # 必須提供 API Key
                llm_provider="anthropic",  # 使用 Anthropic
                use_mock=False  # 不使用 Mock
            )
            
            if not output_file or not output_file.exists():
                # Provide more detailed error info
                error_detail = "Failed to generate PPTX"
                if output_file is None:
                    error_detail += ": function returned None (please check backend logs for detailed error info)."
                elif not output_file.exists():
                    error_detail += f": file does not exist (expected path: {output_file})."
                raise Exception(error_detail)
            
            # Save to session_state (shared with tab2)
            st.session_state["tcfd_report_file"] = output_file
            st.session_state["tcfd_report_summary"] = summary
            
            st.success("✅ TCFD report generated successfully!")
            
            # 3. Show summary
            st.info(f"**Report Summary**:\n\n{summary}")
            
            # 4. Show download button
            with open(output_file, "rb") as f:
                st.download_button(
                    "📥 Download TCFD Report (TCFD_table.pptx)",
                    data=f.read(),
                    file_name="TCFD_table.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True,
                    key="download_tcfd_report"
                )

            # 5. Build and save simplified TCFD summary (for other chapters)
            try:
                total_emission = None
                if carbon_emission and isinstance(carbon_emission, dict):
                    total_emission = carbon_emission.get("total_tco2e")
                    if total_emission is None and isinstance(carbon_emission.get("full_result"), dict):
                        total_emission = carbon_emission["full_result"].get("Total_S1S2")
                total_emission = float(total_emission) if total_emission is not None else None

                tcfd_summary = {
                    "industry": industry,
                    "total_emission_tco2e": total_emission,
                    "revenue_k_ntd": float(revenue_k) if revenue_k else None,
                    "key_climate_points": [
                        f"本公司所屬產業：{industry}，在氣候變遷與淨零轉型情境下，營運活動面臨顯著的氣候風險與轉型壓力。",
                        f"最近一次盤查的溫室氣體排放總量約為 {total_emission} tCO2e（僅含範疇一與範疇二），顯示營運高度依賴能源與碳密集設備。",
                        f"在約 {revenue_k:.0f} K {revenue_currency} 的年度營收規模下，若能系統性導入節能設備、再生能源與排放管理機制，將同時降低營運成本並提升永續形象與客戶信任。"
                    ]
                }
                DataBroker.set_tcfd_summary(tcfd_summary)
                print(f"[DEBUG] TCFD Summary 已寫入 DataBroker（main 按鈕）：{tcfd_summary}")
            except Exception as e:
                print(f"[WARNING] Unable to build or save TCFD Summary (main button): {e}")
            
        except Exception as e:
            st.error(f"Generation failed: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

st.divider()

# Navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("Previous", use_container_width=True):
        st.switch_page("pages/0_Home.py")

with col2:
    if st.button("Next", type="primary", use_container_width=True):
        st.switch_page("pages/2_Environment.py")
