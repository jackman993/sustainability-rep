"""
詳細診斷腳本：逐步檢查 generate_combined_pptx 的每個環節
"""
import sys
from pathlib import Path
import traceback

sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("TCFD 生成詳細診斷腳本")
print("=" * 70)

try:
    # 1. 檢查導入
    print("\n[步驟 1] 檢查模組導入...")
    from shared.engine.tcfd import generate_combined_pptx, config
    from shared.engine.tcfd.main import load_table_module, generate_table_content
    print("   ✅ 模組導入成功")
    
    # 2. 檢查配置
    print("\n[步驟 2] 檢查配置...")
    print(f"   TCFD_PAGES 數量: {len(config.TCFD_PAGES)}")
    print(f"   OUTPUT_DIR: {config.OUTPUT_DIR}")
    print(f"   BASE_DIR: {config.BASE_DIR}")
    
    # 3. 檢查模板文件
    print("\n[步驟 3] 檢查模板文件...")
    template_path = Path(__file__).parent / "shared" / "engine" / "tcfd" / "handdrawppt.pptx"
    print(f"   模板路徑: {template_path}")
    print(f"   模板存在: {template_path.exists()}")
    
    if template_path.exists():
        try:
            from pptx import Presentation
            test_prs = Presentation(str(template_path))
            print(f"   ✅ 模板可以加載，包含 {len(test_prs.slides)} 個 slide")
        except Exception as e:
            print(f"   ❌ 模板加載失敗: {e}")
            traceback.print_exc()
    
    # 4. 檢查表格模組
    print("\n[步驟 4] 檢查表格生成模組...")
    slide_order = ['page_1', 'page_2', 'page_3', 'page_4', 'page_5', 'page_6', 'page_7']
    for page_key in slide_order:
        if page_key not in config.TCFD_PAGES:
            print(f"   ⚠️ {page_key} 不在 TCFD_PAGES 中")
            continue
        
        page_info = config.TCFD_PAGES[page_key]
        print(f"\n   檢查 {page_key} ({page_info['title']}):")
        print(f"     Script: {page_info['script_file']}")
        print(f"     函數: {page_info['entry_function']}")
        
        try:
            # 載入模組
            table_module = load_table_module(page_info['script_file'])
            print(f"     ✅ 模組載入成功: {table_module}")
            
            # 檢查函數
            if not hasattr(table_module, page_info['entry_function']):
                print(f"     ❌ 函數 {page_info['entry_function']} 不存在")
            else:
                func = getattr(table_module, page_info['entry_function'])
                print(f"     ✅ 函數存在: {func}")
                
                # 檢查函數簽名
                import inspect
                sig = inspect.signature(func)
                print(f"     參數: {list(sig.parameters.keys())}")
                
        except Exception as e:
            print(f"     ❌ 載入失敗: {type(e).__name__}: {e}")
            traceback.print_exc()
    
    # 5. 測試生成表格內容
    print("\n[步驟 5] 測試生成表格內容（Mock 數據）...")
    try:
        data_lines = generate_table_content(
            prompt_id='prompt_table_1_trans',
            industry="製造業",
            revenue="1000K USD",
            carbon_emission={"total_tco2e": 100},
            llm_api_key=None,
            llm_provider=None,
            use_mock=True
        )
        print(f"   ✅ 生成成功，獲得 {len(data_lines)} 行數據")
        if data_lines:
            print(f"   第一行示例: {data_lines[0][:100]}...")
    except Exception as e:
        print(f"   ❌ 生成失敗: {type(e).__name__}: {e}")
        traceback.print_exc()
    
    # 6. 測試完整生成流程
    print("\n[步驟 6] 測試完整生成流程...")
    print("-" * 70)
    
    output_file = generate_combined_pptx(
        output_filename="TCFD_table_debug.pptx",
        template_path=template_path if template_path.exists() else None,
        industry="製造業",
        revenue="1000K USD",
        carbon_emission={"total_tco2e": 100},
        llm_api_key=None,
        llm_provider=None,
        use_mock=True
    )
    
    print("-" * 70)
    
    if output_file:
        print(f"\n✅ 完整流程成功！")
        print(f"   輸出文件: {output_file}")
        print(f"   文件存在: {output_file.exists()}")
        if output_file.exists():
            print(f"   文件大小: {output_file.stat().st_size} bytes")
    else:
        print(f"\n❌ 完整流程失敗：函數返回 None")
        print("   請查看上方的錯誤信息")
        
except Exception as e:
    print(f"\n❌ 診斷過程發生錯誤: {type(e).__name__}: {e}")
    print("=" * 70)
    traceback.print_exc()
    print("=" * 70)

