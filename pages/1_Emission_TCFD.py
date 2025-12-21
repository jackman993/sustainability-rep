"""
Step 1: Emission & TCFD
"""
# Page title - single source of truth (must match docstring above)
PAGE_TITLE = "Step 1: Emission & TCFD"

import streamlit as st
from pathlib import Path
import sys

# 添加項目根目錄到 Python 路徑（確保能找到 shared 模組）
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from shared.engine.carbon import render_calculator
from shared.ui.sidebar_config import render_sidebar_config

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
    st.subheader("🏭 TCFD Climate Risk Tables Generator")
    
    # 按鈕 - 最簡單的版本，確保一定會顯示
    generate_btn = st.button("🚀 Generate TCFD Tables", type="primary", use_container_width=True, key="tcfd_btn")
    
    # 嘗試導入 TCFD 模組（延遲導入）
    if not TCFD_AVAILABLE:
        try:
            from shared.engine.tcfd import TCFD_PAGES, generate_table, generate_all_tables
            TCFD_AVAILABLE = True
        except Exception as e:
            st.error(f"TCFD module error: {str(e)}")
            TCFD_AVAILABLE = False
    
    # 如果按鈕被點擊
    if generate_btn:
        st.success("✅ Button clicked!")
    
    # 如果 TCFD 模組可用，顯示完整功能
    if TCFD_AVAILABLE and TCFD_PAGES:
        # 獲取數據
        industry = st.session_state.get("carbon_calc_industry", "Manufacturing")
        carbon_emission = st.session_state.get("carbon_emission")
        estimated_revenue = st.session_state.get("estimated_annual_revenue", {})
        revenue_k = estimated_revenue.get("k_value", 0)
        revenue_currency = estimated_revenue.get("currency", "USD")
        revenue_str = f"{revenue_k:.0f}K {revenue_currency}" if revenue_k > 0 else "N/A"
        
        # 顯示當前數據
        st.info(f"📊 **Current Data**: Industry: {industry} | Emissions: {carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e | Revenue: {revenue_str}")
        
        st.divider()
        
        # 數據源選擇已移至 sidebar，這裡只顯示當前選擇
        data_source = st.session_state.get("data_source", "Mock Data")
        if data_source == "Mock Data":
            st.info("ℹ️ **數據源**: Mock Data（在左側 sidebar 可切換）")
        else:
            api_key_status = "✅ 已設置" if st.session_state.get("claude_api_key") else "⚠️ 未設置"
            st.info(f"ℹ️ **數據源**: Claude API（在左側 sidebar 可切換）| API Key: {api_key_status}")
        
        st.divider()
        
        # 表格選擇
        st.subheader("📋 Select Tables to Generate")
        
        # 顯示所有可用的表格
        selected_tables = []
        cols = st.columns(4)
        for idx, (page_key, page_info) in enumerate(TCFD_PAGES.items()):
            with cols[idx % 4]:
                if st.checkbox(
                    f"**Table {idx + 1}**: {page_info['title']}",
                    key=f"tcfd_table_{page_key}",
                    value=True
                ):
                    selected_tables.append(page_key)
        
        st.divider()
        
        # 從 sidebar 獲取數據源
        data_source = st.session_state.get("data_source", "Mock Data")
        use_mock_bool = (data_source == "Mock Data")
        claude_api_key = st.session_state.get("claude_api_key") or ""
        
        # 如果按鈕被點擊，執行生成邏輯
        if generate_btn:
            if not selected_tables:
                st.warning("⚠️ Please select at least one table to generate")
            elif not use_mock_bool and not claude_api_key:
                st.warning("⚠️ Please enter Claude API Key in sidebar or select Mock Data")
            else:
                # 即使沒有碳排放數據，也可以使用 Mock 數據生成
                if not carbon_emission:
                    carbon_emission = None
                with st.spinner(f"Generating TCFD tables using {'Mock Data' if use_mock_bool else 'Claude API'}..."):
                    generated_files = {}
                    errors = []
                    
                    # 準備 API 參數
                    llm_api_key = None if use_mock_bool else claude_api_key
                    llm_provider = None if use_mock_bool else "anthropic"
                    
                    for page_key in selected_tables:
                        try:
                            file_path = generate_table(
                                page_key=page_key,
                                industry=industry,
                                revenue=revenue_str,
                                carbon_emission=carbon_emission,
                                llm_api_key=llm_api_key,
                                llm_provider=llm_provider,
                                use_mock=use_mock_bool
                            )
                            if file_path:
                                generated_files[page_key] = file_path
                        except Exception as e:
                            errors.append(f"{TCFD_PAGES[page_key]['title']}: {str(e)}")
                    
                    # 顯示結果
                    if generated_files:
                        st.success(f"✅ Successfully generated {len(generated_files)} table(s)")
                        st.session_state["tcfd_generated_files"] = generated_files
                        
                        # 顯示下載鏈接
                        st.subheader("Download Generated Tables")
                        for page_key, file_path in generated_files.items():
                            page_info = TCFD_PAGES[page_key]
                            with open(file_path, "rb") as f:
                                st.download_button(
                                    label=f"📥 Download {page_info['title']}",
                                    data=f.read(),
                                    file_name=Path(file_path).name,
                                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                    key=f"download_{page_key}"
                                )
                    
                    if errors:
                        st.error("❌ Errors occurred:")
                        for error in errors:
                            st.error(f"  - {error}")
    else:
        # TCFD 模組不可用時的處理
        if generate_btn:
            st.error("❌ TCFD module is not available. Please check the module files.")

st.divider()

# Generate TCFD Button - 在 Next 按鈕之上
if st.button("🚀 Generate TCFD Tables", type="primary", use_container_width=True, key="generate_tcfd_main"):
    # 檢查 TCFD 模組是否可用
    if not TCFD_AVAILABLE:
        try:
            from shared.engine.tcfd import TCFD_PAGES, generate_table, generate_all_tables, generate_combined_pptx
            TCFD_AVAILABLE = True
        except Exception as e:
            st.error(f"TCFD module error: {str(e)}")
            st.stop()
    
    # 確保導入 generate_combined_pptx
    from shared.engine.tcfd import generate_combined_pptx
    
    # 從 sidebar 獲取數據源選擇
    data_source = st.session_state.get("data_source", "Mock Data")
    use_api = (data_source == "Claude API")
    
    # 獲取 API Key（從 sidebar）
    api_key = st.session_state.get("claude_api_key") or ""
    
    # 如果選擇 Claude API 但沒有 API Key，顯示警告
    if use_api and not api_key:
        st.warning("⚠️ 請在左側 sidebar 輸入 Claude API Key")
        st.stop()
    
    # 獲取數據
    industry = st.session_state.get("carbon_calc_industry", "Manufacturing")    
    carbon_emission = st.session_state.get("carbon_emission")
    estimated_revenue = st.session_state.get("estimated_annual_revenue", {})    
    revenue_k = estimated_revenue.get("k_value", 0)
    revenue_currency = estimated_revenue.get("currency", "USD")
    revenue_str = f"{revenue_k:.0f}K {revenue_currency}" if revenue_k > 0 else "N/A"

    with st.spinner(f"正在生成 TCFD 報告...({'使用 Claude API' if use_api else '使用 Mock 數據'})"):
        # 1. 生成摘要（使用 LLM API，輸出英文）
        if use_api:
            # 使用 Claude API 生成英文摘要
            try:
                from shared.engine.tcfd.main import call_claude_api
                summary_prompt = f"""Please write a 250-word summary for the following TCFD climate risk report:

Industry: {industry}
Total Carbon Emissions: {carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e
Revenue: {revenue_str}

The report contains 7 tables covering: Transformation Risks, Physical Risks, Opportunities (Resource & Energy Efficiency, Products & Services), Metrics and Targets, Systemic Risk Control, and Operational Resilience.

Please write a concise summary in English, approximately 250 words, that highlights the key climate risks, opportunities, and strategic recommendations for the {industry} industry based on the TCFD framework analysis."""
                summary = call_claude_api(summary_prompt, api_key)
                # 清理摘要，確保大約 250 字
                summary = summary.split('\n\n')[0].strip()
                # 如果超過 300 字，截斷到合適的長度
                if len(summary.split()) > 300:
                    words = summary.split()[:250]
                    summary = ' '.join(words) + "..."
            except Exception as e:
                summary = f"This TCFD climate risk report provides a comprehensive analysis for the {industry} industry. The report includes 7 tables covering transformation risks, physical risks, opportunities, metrics and targets, systemic risk control, and operational resilience. Based on current carbon emission data (Total: {carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e) and revenue data ({revenue_str}), this report offers strategic insights for climate risk management and sustainable development."
                st.warning(f"Summary generation failed, using default summary: {str(e)}")
        else:
            # 使用 Mock 數據時，也使用 LLM API 生成英文摘要（如果 API Key 可用）
            api_key_for_summary = st.session_state.get("claude_api_key") or ""
            if api_key_for_summary:
                try:
                    from shared.engine.tcfd.main import call_claude_api
                    summary_prompt = f"""Please write a 250-word summary for the following TCFD climate risk report:

Industry: {industry}
Total Carbon Emissions: {carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e
Revenue: {revenue_str}

The report contains 7 tables covering: Transformation Risks, Physical Risks, Opportunities (Resource & Energy Efficiency, Products & Services), Metrics and Targets, Systemic Risk Control, and Operational Resilience.

Please write a concise summary in English, approximately 250 words, that highlights the key climate risks, opportunities, and strategic recommendations for the {industry} industry based on the TCFD framework analysis."""
                    summary = call_claude_api(summary_prompt, api_key_for_summary)
                    summary = summary.split('\n\n')[0].strip()
                    if len(summary.split()) > 300:
                        words = summary.split()[:250]
                        summary = ' '.join(words) + "..."
                except Exception as e:
                    # 如果 API 調用失敗，使用英文默認摘要
                    summary = f"This TCFD climate risk report provides a comprehensive analysis for the {industry} industry. The report includes 7 tables covering transformation risks, physical risks, opportunities, metrics and targets, systemic risk control, and operational resilience. Based on current carbon emission data (Total: {carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e) and revenue data ({revenue_str}), this report offers strategic insights for climate risk management and sustainable development."
            else:
                # 如果沒有 API Key，使用英文默認摘要
                summary = f"This TCFD climate risk report provides a comprehensive analysis for the {industry} industry. The report includes 7 tables covering transformation risks, physical risks, opportunities, metrics and targets, systemic risk control, and operational resilience. Based on current carbon emission data (Total: {carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e) and revenue data ({revenue_str}), this report offers strategic insights for climate risk management and sustainable development."
        
        # 2. 生成包含 7 個表格的 PPTX（使用 handdrawppt.pptx 模板）
        try:
            from pathlib import Path
            
            # 模板路徑
            template_path = Path(__file__).parent.parent / "shared" / "engine" / "tcfd" / "handdrawppt.pptx"
            
            # 使用 generate_combined_pptx 生成合併的 PPTX
            output_file = generate_combined_pptx(
                output_filename="TCFD_table.pptx",
                template_path=template_path if template_path.exists() else None,
                industry=industry,
                revenue=revenue_str,
                carbon_emission=carbon_emission,
                llm_api_key=api_key if use_api else None,
                llm_provider="anthropic" if use_api else None,
                use_mock=not use_api
            )
            
            if not output_file or not output_file.exists():
                # 提供更詳細的錯誤信息
                error_detail = "生成 PPTX 失敗"
                if output_file is None:
                    error_detail += "：函數返回 None（請查看終端輸出中的詳細錯誤信息）"
                elif not output_file.exists():
                    error_detail += f"：文件不存在（預期路徑：{output_file}）"
                raise Exception(error_detail)
            
            st.success("✅ TCFD 報告生成完成！")
            
            # 3. 顯示摘要
            st.info(f"**Report Summary**：\n\n{summary}")
            
            # 4. 顯示下載按鈕
            with open(output_file, "rb") as f:
                st.download_button(
                    "📥 下載 TCFD 報告 (TCFD_table.pptx)",
                    data=f.read(),
                    file_name="TCFD_table.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True,
                    key="download_tcfd_report"
                )
            
        except Exception as e:
            st.error(f"生成失敗：{str(e)}")
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
