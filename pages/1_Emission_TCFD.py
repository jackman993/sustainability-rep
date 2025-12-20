"""
Step 1: Emission & TCFD
"""
# Page title - single source of truth (must match docstring above)
PAGE_TITLE = "Step 1: Emission & TCFD"

import streamlit as st
from pathlib import Path
from shared.engine.carbon import render_calculator
from shared.ui.sidebar_config import render_sidebar_config
from shared.engine.tcfd import TCFD_PAGES, generate_table, generate_all_tables

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
    st.write("**TCFD Climate Risk Tables**")
    
    # 獲取數據
    industry = st.session_state.get("carbon_calc_industry", "Manufacturing")
    carbon_emission = st.session_state.get("carbon_emission")
    estimated_revenue = st.session_state.get("estimated_annual_revenue", {})
    revenue_k = estimated_revenue.get("k_value", 0)
    revenue_currency = estimated_revenue.get("currency", "USD")
    revenue_str = f"{revenue_k:.0f}K {revenue_currency}" if revenue_k > 0 else "N/A"
    
    # 顯示當前數據
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Industry**: {industry}")
    with col2:
        if carbon_emission:
            st.info(f"**Total Emissions**: {carbon_emission.get('total_tco2e', 'N/A')} tCO2e")
        else:
            st.warning("⚠️ Please complete emission calculation first")
    with col3:
        st.info(f"**Revenue**: {revenue_str}")
    
    st.divider()
    
    # 數據生成方式選擇
    st.subheader("Data Generation Method")
    col1, col2 = st.columns(2)
    with col1:
        use_mock = st.radio(
            "Choose data source:",
            ["Mock Data (測試用)", "Claude API"],
            key="tcfd_data_source",
            index=0
        )
        use_mock_bool = use_mock == "Mock Data (測試用)"
    
    with col2:
        if not use_mock_bool:
            claude_api_key = st.text_input(
                "Claude API Key:",
                type="password",
                key="tcfd_claude_api_key",
                help="Enter your Anthropic Claude API key"
            )
        else:
            claude_api_key = None
            st.info("💡 Using mock data for testing")
    
    st.divider()
    
    # 表格選擇
    st.subheader("Select Tables to Generate")
    
    # 顯示所有可用的表格
    selected_tables = []
    cols = st.columns(4)
    for idx, (page_key, page_info) in enumerate(TCFD_PAGES.items()):
        with cols[idx % 4]:
            if st.checkbox(
                f"Table {idx + 1}: {page_info['title']}",
                key=f"tcfd_table_{page_key}",
                value=True
            ):
                selected_tables.append(page_key)
    
    st.divider()
    
    # 生成按鈕
    if st.button("Generate Selected TCFD Tables", type="primary", use_container_width=True):
        if not selected_tables:
            st.warning("⚠️ Please select at least one table to generate")
        elif not use_mock_bool and not claude_api_key:
            st.warning("⚠️ Please enter Claude API Key or select Mock Data")
        else:
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

st.divider()

# Navigation
col1, col2 = st.columns(2)

with col1:
    if st.button("Previous", use_container_width=True):
        st.switch_page("pages/0_Home.py")

with col2:
    if st.button("Next", type="primary", use_container_width=True):
        st.switch_page("pages/2_Environment.py")
