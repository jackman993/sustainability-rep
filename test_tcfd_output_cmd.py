"""
TCFD 輸出測試腳本（CMD 執行）
測試 TCFD 報告生成和路徑管理，不依賴 Streamlit
"""
import sys
from pathlib import Path

# 添加項目根目錄到 Python 路徑
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("=" * 60)
print("TCFD 輸出測試（CMD 模式）")
print("=" * 60)

# 測試 1: 檢查模組導入
print("\n[測試 1] 檢查模組導入...")
try:
    from shared.engine.path_manager import get_tcfd_output_path
    print("✅ path_manager 導入成功")
except Exception as e:
    print(f"❌ path_manager 導入失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from shared.engine.output_config import get_session_id, get_session_output_dir, OUTPUT_FILENAMES
    print("✅ output_config 導入成功")
except Exception as e:
    print(f"❌ output_config 導入失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from shared.engine.tcfd import generate_combined_pptx
    print("✅ TCFD 模組導入成功")
except Exception as e:
    print(f"❌ TCFD 模組導入失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 測試 2: 檢查路徑獲取（不使用 Streamlit）
print("\n[測試 2] 檢查路徑獲取（非 Streamlit 環境）...")
try:
    # 測試 get_session_id（應該返回臨時 UUID）
    session_id = get_session_id()
    print(f"✅ session_id 獲取成功: {session_id}")
except Exception as e:
    print(f"❌ session_id 獲取失敗: {e}")
    import traceback
    traceback.print_exc()

try:
    # 測試 get_session_output_dir
    session_dir = get_session_output_dir()
    print(f"✅ session_output_dir 獲取成功: {session_dir}")
    print(f"   目錄是否存在: {session_dir.exists()}")
except Exception as e:
    print(f"❌ session_output_dir 獲取失敗: {e}")
    import traceback
    traceback.print_exc()

try:
    # 測試 get_tcfd_output_path
    output_path = get_tcfd_output_path()
    print(f"✅ TCFD 輸出路徑獲取成功: {output_path}")
    print(f"   完整路徑: {output_path.resolve()}")
    print(f"   父目錄: {output_path.parent}")
    print(f"   父目錄是否存在: {output_path.parent.exists()}")
except Exception as e:
    print(f"❌ TCFD 輸出路徑獲取失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 測試 3: 檢查目錄創建
print("\n[測試 3] 檢查目錄創建...")
try:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"✅ 目錄創建成功: {output_path.parent}")
    print(f"   目錄是否存在: {output_path.parent.exists()}")
except Exception as e:
    print(f"❌ 目錄創建失敗: {e}")
    import traceback
    traceback.print_exc()

# 測試 4: 測試生成 TCFD 報告（使用 Mock 數據）
print("\n[測試 4] 測試生成 TCFD 報告（Mock 模式）...")
try:
    # 準備測試數據
    test_industry = "Manufacturing"
    test_revenue = "50K USD"
    test_carbon_emission = {
        "total_tco2e": 100.5,
        "scope1": 50.0,
        "scope2": 30.0,
        "scope3": 20.5
    }
    
    print(f"   產業: {test_industry}")
    print(f"   營收: {test_revenue}")
    print(f"   碳排放: {test_carbon_emission}")
    print("   使用 Mock 數據模式...")
    
    # 調用生成函數
    result_path = generate_combined_pptx(
        output_filename="TCFD_table.pptx",
        template_path=None,  # 不使用模板
        industry=test_industry,
        revenue=test_revenue,
        carbon_emission=test_carbon_emission,
        llm_api_key=None,
        llm_provider=None,
        use_mock=True  # 使用 Mock 數據
    )
    
    if result_path:
        print(f"✅ TCFD 報告生成成功!")
        print(f"   返回路徑: {result_path}")
        print(f"   路徑類型: {type(result_path)}")
        print(f"   路徑是否存在: {result_path.exists() if hasattr(result_path, 'exists') else 'N/A'}")
        
        if hasattr(result_path, 'exists') and result_path.exists():
            file_size = result_path.stat().st_size if hasattr(result_path, 'stat') else 'N/A'
            print(f"   文件大小: {file_size} bytes")
    else:
        print("❌ TCFD 報告生成失敗: 函數返回 None")
        print("   請檢查終端輸出中的錯誤信息")
        
except Exception as e:
    print(f"❌ TCFD 報告生成失敗: {e}")
    import traceback
    print("\n完整錯誤信息:")
    traceback.print_exc()

# 測試 5: 檢查實際文件
print("\n[測試 5] 檢查實際生成的文件...")
try:
    if result_path and hasattr(result_path, 'exists') and result_path.exists():
        print(f"✅ 文件存在: {result_path}")
        print(f"   完整路徑: {result_path.resolve()}")
        
        # 檢查 output 目錄結構
        output_root = project_root / "output"
        print(f"\n   檢查 output 目錄結構:")
        print(f"   output 根目錄: {output_root}")
        print(f"   output 根目錄是否存在: {output_root.exists()}")
        
        if output_root.exists():
            session_dirs = [d for d in output_root.iterdir() if d.is_dir()]
            print(f"   找到 {len(session_dirs)} 個會話目錄:")
            for session_dir in session_dirs[:5]:  # 只顯示前5個
                files = list(session_dir.glob("*.pptx"))
                print(f"     - {session_dir.name}: {len(files)} 個 PPTX 文件")
                for f in files:
                    print(f"       * {f.name}")
    else:
        print("❌ 文件不存在或路徑無效")
        print(f"   預期路徑: {output_path}")
        
except Exception as e:
    print(f"❌ 檢查文件失敗: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("測試完成")
print("=" * 60)

