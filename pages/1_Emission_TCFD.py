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
    
    # 顯示當前數據
    st.info(f"📊 **Current Data**: Industry: {industry} | Emissions: {carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e | Revenue: {revenue_str}")
    
    st.divider()
    
    # API Key 狀態檢查
    api_key = st.session_state.get("claude_api_key")
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
        st.info(f"ℹ️ **API Key**: ✅ 已配置 ({masked_key})")
    else:
        st.warning("⚠️ **API Key**: 未配置，請在左側 sidebar 配置 API Key")
    
    st.divider()
    
    # 顯示報告內容說明
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
    
    # 生成按鈕
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
        
        # 獲取 API Key（必須配置）
        api_key = st.session_state.get("claude_api_key") or ""
        
        # 調試信息
        print(f"[DEBUG] api_key exists: {bool(api_key)}")
        print(f"[DEBUG] api_key length: {len(api_key) if api_key else 0}")
        print(f"[DEBUG] api_key_locked: {st.session_state.get('api_key_locked', False)}")
        
        # 如果沒有 API Key，顯示錯誤並停止
        if not api_key:
            st.error(f"❌ API Key 未配置！")
            st.info("💡 請在左側 sidebar 的 API Configuration 中配置 Claude API Key")
            st.info("💡 或創建 `.streamlit/secrets.toml` 文件並添加：ANTHROPIC_API_KEY = \"your-key-here\"")
            st.stop()
        
        # 創建進度顯示
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # 步驟 1: 生成摘要
            status_text.text("Step 1/3: Generating executive summary...")
            progress_bar.progress(20)
            
            # 使用 LLM API 生成摘要（必須有 API Key）
            summary = ""
            try:
                from shared.engine.tcfd.main import call_claude_api
                summary_prompt = f"""Please write a 250-word summary for the following TCFD climate risk report:

Industry: {industry}
Total Carbon Emissions: {carbon_emission.get('total_tco2e', 'N/A') if carbon_emission else 'N/A'} tCO2e
Revenue: {revenue_str}

The report contains 7 tables covering: Transformation Risks, Physical Risks, Opportunities (Resource & Energy Efficiency, Products & Services), Metrics and Targets, Systemic Risk Control, and Operational Resilience.

Please write a concise summary in English, approximately 250 words, that highlights the key climate risks, opportunities, and strategic recommendations for the {industry} industry based on the TCFD framework analysis."""
                print(f"[DEBUG] 調用 Claude API 生成摘要，API Key 長度: {len(api_key)}")
                summary = call_claude_api(summary_prompt, api_key)
                print(f"[DEBUG] Claude API 調用成功，摘要長度: {len(summary)}")
                summary = summary.split('\n\n')[0].strip()
                if len(summary.split()) > 300:
                    words = summary.split()[:250]
                    summary = ' '.join(words) + "..."
                st.success("✅ LLM 摘要生成成功")
            except Exception as e:
                error_msg = str(e)
                print(f"[ERROR] Claude API 調用失敗: {error_msg}")
                import traceback
                traceback.print_exc()
                st.error(f"❌ LLM 調用失敗: {error_msg}")
                st.info("💡 請檢查：1) API Key 是否正確 2) 網絡連接 3) 查看終端輸出中的詳細錯誤信息")
                st.stop()
            
            # 步驟 2: 生成 PPTX
            status_text.text("Step 2/3: Generating TCFD tables (this may take a few minutes)...")
            progress_bar.progress(50)
            
            from pathlib import Path
            template_path = Path(__file__).parent.parent / "shared" / "engine" / "tcfd" / "handdrawppt.pptx"
            
            # 顯示調試信息
            debug_info = st.empty()
            debug_info.info("🔍 調試模式：顯示詳細執行信息...")
            
            # 顯示 session_id（如果可用）
            try:
                session_id = st.session_state.get('session_id', '未設置')
                debug_info.text(f"📋 Session ID: {session_id}")
            except:
                debug_info.text("📋 Session ID: 無法獲取")
            
            # 創建錯誤顯示容器（確保錯誤一定會顯示）
            error_container = st.container()
            
            # 調試信息
            print(f"[DEBUG] 調用 generate_combined_pptx:")
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
                # 捕獲生成過程中的異常
                error_container.error(f"❌ TCFD 報告生成過程發生錯誤: {str(gen_error)}")
                with error_container.expander("🔍 詳細錯誤信息", expanded=True):
                    import traceback
                    error_container.code(traceback.format_exc())
                error_container.info("💡 請同時查看終端輸出中的詳細日誌")
                progress_bar.empty()
                status_text.empty()
                debug_info.empty()
                st.stop()
            
            # 步驟 3: 完成
            status_text.text("Step 3/3: Finalizing report...")
            progress_bar.progress(90)
            
            # 詳細的錯誤檢查和報告
            debug_info.empty()  # 清除調試信息
            
            # 顯示文件保存確認訊息（如果 generate_combined_pptx 內部沒有顯示）
            # 注意：generate_combined_pptx 內部已經會顯示成功訊息，這裡作為備份確認
            if output_file and hasattr(output_file, 'exists') and output_file.exists():
                try:
                    file_size = output_file.stat().st_size
                    file_size_kb = file_size / 1024
                    st.info(f"📦 **文件確認**: 文件已存在於 `{output_file}`\n\n"
                           f"📊 **文件大小**: {file_size_kb:.2f} KB")
                except:
                    pass
            
            if output_file is None:
                error_container.error("❌ 生成 PPTX 失敗：函數返回 None")
                error_container.info("💡 這通常意味著生成過程中發生了異常，但被內部處理了")
                error_container.info("💡 請查看終端輸出中的 [ERROR] 和 [DEBUG] 日誌")
                progress_bar.empty()
                status_text.empty()
                st.stop()
            
            if not hasattr(output_file, 'exists'):
                error_detail = f"❌ 返回的路徑對象無效：{type(output_file)}"
                st.error(error_detail)
                st.code(f"返回對象: {output_file}")
                raise Exception(error_detail)
            
            if not output_file.exists():
                error_detail = f"❌ 文件不存在（預期路徑：{output_file}）"
                st.error(error_detail)
                
                # 顯示詳細的調試信息
                with st.expander("🔍 調試信息", expanded=True):
                    st.write(f"**返回的路徑類型**: {type(output_file)}")
                    st.write(f"**返回的路徑**: {output_file}")
                    st.write(f"**絕對路徑**: {output_file.resolve() if hasattr(output_file, 'resolve') else 'N/A'}")
                    st.write(f"**父目錄**: {output_file.parent if hasattr(output_file, 'parent') else 'N/A'}")
                    st.write(f"**父目錄是否存在**: {output_file.parent.exists() if hasattr(output_file, 'parent') else 'N/A'}")
                    
                    # 檢查 output 目錄
                    from pathlib import Path
                    output_root = Path(__file__).parent.parent / "output"
                    st.write(f"**Output 根目錄**: {output_root}")
                    st.write(f"**Output 根目錄是否存在**: {output_root.exists()}")
                    
                    if output_root.exists():
                        session_dirs = [d for d in output_root.iterdir() if d.is_dir()]
                        st.write(f"**會話目錄數量**: {len(session_dirs)}")
                        for session_dir in session_dirs[:5]:
                            files = list(session_dir.glob("*.pptx"))
                            st.write(f"  - {session_dir.name}: {len(files)} 個 PPTX 文件")
                
                st.info("💡 請查看終端輸出中的詳細錯誤信息和調試日誌")
                raise Exception(error_detail)
            
            progress_bar.progress(100)
            status_text.text("✅ Report generation completed!")
            
            # 保存到 session_state
            st.session_state["tcfd_report_file"] = output_file
            st.session_state["tcfd_report_summary"] = summary
            st.session_state["tcfd_report_generated_tab2"] = True
            
            # 顯示成功訊息
            st.success("✅ TCFD Report generated successfully!")
            
            # 顯示摘要
            st.info(f"**Report Summary**：\n\n{summary}")
            
            # 顯示下載按鈕
            try:
                # 確保 output_file 是字符串路徑
                file_path = str(output_file) if hasattr(output_file, '__str__') else output_file
                
                # 確認文件存在
                if not Path(file_path).exists():
                    st.warning(f"⚠️ 文件路徑存在但文件無法訪問: {file_path}")
                    st.info("💡 文件可能已保存，但當前會話無法訪問。請檢查文件系統權限。")
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
                        st.caption(f"文件大小: {file_size / 1024:.2f} KB")
            except Exception as download_error:
                st.error(f"❌ 無法創建下載按鈕: {str(download_error)}")
                st.info(f"💡 文件已保存到: `{output_file}`")
                st.info("💡 請手動從服務器下載文件")
                import traceback
                with st.expander("詳細錯誤信息", expanded=False):
                    st.code(traceback.format_exc())
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"生成失敗：{str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    # 如果已經生成過報告，顯示摘要和下載按鈕
    elif st.session_state.get("tcfd_report_file") and st.session_state.get("tcfd_report_file").exists():
        st.success("✅ TCFD Report available!")
        
        # 顯示摘要
        summary = st.session_state.get("tcfd_report_summary", "")
        if summary:
            st.info(f"**Report Summary**：\n\n{summary}")
        
        # 顯示下載按鈕
        output_file = st.session_state.get("tcfd_report_file")
        try:
            # 確保 output_file 是字符串路徑
            if isinstance(output_file, Path):
                file_path = str(output_file)
            else:
                file_path = output_file
            
            # 確認文件存在
            if not Path(file_path).exists():
                st.warning(f"⚠️ 文件路徑存在但文件無法訪問: {file_path}")
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
                    st.caption(f"文件大小: {file_size / 1024:.2f} KB")
        except Exception as download_error:
            st.error(f"❌ 無法創建下載按鈕: {str(download_error)}")
            st.info(f"💡 文件路徑: `{output_file}`")
            import traceback
            with st.expander("詳細錯誤信息", expanded=False):
                st.code(traceback.format_exc())

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
    
    # 獲取 API Key（必須配置）
    api_key = st.session_state.get("claude_api_key") or ""
    
    # 如果沒有 API Key，顯示錯誤並停止
    if not api_key:
        st.error("❌ API Key 未配置！")
        st.info("💡 請在左側 sidebar 的 API Configuration 中配置 Claude API Key")
        st.stop()
    
    # 獲取數據
    industry = st.session_state.get("carbon_calc_industry", "Manufacturing")    
    carbon_emission = st.session_state.get("carbon_emission")
    estimated_revenue = st.session_state.get("estimated_annual_revenue", {})    
    revenue_k = estimated_revenue.get("k_value", 0)
    revenue_currency = estimated_revenue.get("currency", "USD")
    revenue_str = f"{revenue_k:.0f}K {revenue_currency}" if revenue_k > 0 else "N/A"

    with st.spinner("正在生成 TCFD 報告...（使用 Claude API）"):
        # 1. 生成摘要（使用 LLM API，輸出英文）
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
            st.success("✅ LLM 摘要生成成功")
        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ LLM 調用失敗: {error_msg}")
            st.info("💡 請檢查：1) API Key 是否正確 2) 網絡連接 3) 查看終端輸出中的詳細錯誤信息")
            st.stop()
        
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
                llm_api_key=api_key,  # 必須提供 API Key
                llm_provider="anthropic",  # 使用 Anthropic
                use_mock=False  # 不使用 Mock
            )
            
            if not output_file or not output_file.exists():
                # 提供更詳細的錯誤信息
                error_detail = "生成 PPTX 失敗"
                if output_file is None:
                    error_detail += "：函數返回 None（請查看終端輸出中的詳細錯誤信息）"
                elif not output_file.exists():
                    error_detail += f"：文件不存在（預期路徑：{output_file}）"
                raise Exception(error_detail)
            
            # 保存到 session_state（與 tab2 共享）
            st.session_state["tcfd_report_file"] = output_file
            st.session_state["tcfd_report_summary"] = summary
            
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
