"""
Step 1: Emission & TCFD
"""
# Page title - single source of truth (must match docstring above)
PAGE_TITLE = "Step 1: Emission & TCFD"

import streamlit as st
from pathlib import Path
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
        
        # 數據生成方式選擇
        col1, col2 = st.columns([1, 1])
        with col1:
            use_mock = st.radio(
                "**Data Source**:",
                ["Mock Data (測試用)", "Claude API"],
                key="tcfd_data_source",
                index=0
            )
            use_mock_bool = use_mock == "Mock Data (測試用)"
        
        with col2:
            if not use_mock_bool:
                claude_api_key = st.text_input(
                    "**Claude API Key**:",
                    type="password",
                    key="tcfd_claude_api_key",
                    help="Enter your Anthropic Claude API key"
                )
            else:
                claude_api_key = None
                st.success("✅ Using mock data for testing")
        
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
        
        # 如果按鈕被點擊，執行生成邏輯
        if generate_btn:
            if not selected_tables:
                st.warning("⚠️ Please select at least one table to generate")
            elif not use_mock_bool and not claude_api_key:
                st.warning("⚠️ Please enter Claude API Key or select Mock Data")
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
    
    # 獲取 API Key（從 sidebar 或 session_state）
    api_key = st.session_state.get("claude_api_key") or st.session_state.get("anthropic_api_key") or st.session_state.get("api_key")
    
    if not api_key:
        # 讓用戶輸入 API Key
        api_key = st.text_input("請輸入 Claude API Key:", type="password", key="tcfd_api_key_input")
        if not api_key:
            st.warning("⚠️ 請輸入 Claude API Key")
            st.stop()
    
    # 根據是否有 API Key 決定使用 API 還是 Mock
    use_api = bool(api_key)

    # 獲取數據
    industry = st.session_state.get("carbon_calc_industry", "Manufacturing")
    carbon_emission = st.session_state.get("carbon_emission")
    estimated_revenue = st.session_state.get("estimated_annual_revenue", {})
    revenue_k = estimated_revenue.get("k_value", 0)
    revenue_currency = estimated_revenue.get("currency", "USD")
    revenue_str = f"{revenue_k:.0f}K {revenue_currency}" if revenue_k > 0 else "N/A"
    
    with st.spinner(f"正在生成 TCFD 報告...({'使用 Claude API' if use_api else '使用 Mock 數據'})"):
        # 1. 生成摘要
        if use_api:
            # 使用 Claude API 生成摘要
            try:
                from shared.engine.tcfd.main import call_claude_api
                summary_prompt = f"""請為以下 TCFD 氣候風險報告寫一個 250 字的摘要：

產業：{industry}
總碳排放量：{carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e
營收：{revenue_str}

報告包含 7 個表格：轉型風險、實體風險、機會分析、指標目標、系統性風險控制、營運韌性。

請用中文寫一個簡潔的摘要。"""
                summary = call_claude_api(summary_prompt, api_key)
                summary = summary.split('\n\n')[0].strip()[:300]
            except Exception as e:
                summary = f"TCFD 氣候風險報告已生成，包含 7 個表格，涵蓋轉型風險、實體風險、機會分析、指標目標等內容。"
                st.warning(f"摘要生成失敗，使用默認摘要：{str(e)}")
        else:
            # 使用 Mock 數據，直接生成摘要
            summary = f"""本 TCFD 氣候風險報告針對 {industry} 產業進行全面分析。報告基於當前碳排放數據（總排放量：{carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e）和營收數據（{revenue_str}），涵蓋七大核心領域：轉型風險分析包括政策法規風險和市場技術風險；實體風險評估涵蓋短期極端事件和長期氣候變化影響；機會分析聚焦資源能源效率和產品服務創新；指標目標設定明確的 GHG 排放和氣候相關目標；系統性風險控制強調產業認證和供應鏈透明度；營運韌性評估人力資源能力和供應鏈安全。本報告為企業氣候風險管理和永續發展提供決策依據。"""
        
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
                raise Exception("生成 PPTX 失敗")
            
            st.success("✅ TCFD 報告生成完成！")
            
            # 3. 顯示摘要
            st.info(f"**報告摘要**：\n\n{summary}")
            
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
