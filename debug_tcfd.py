"""
臨時診斷腳本：測試 generate_combined_pptx 函數並顯示完整錯誤
模擬 Streamlit 頁面的實際調用情況
"""
import sys
from pathlib import Path

# 添加項目路徑
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("TCFD 生成診斷腳本")
print("=" * 60)

try:
    from shared.engine.tcfd import generate_combined_pptx
    
    # 模擬 Streamlit 頁面中的實際調用
    # 1. 模板路徑（模擬 pages/1_Emission_TCFD.py 中的路徑計算）
    script_path = Path(__file__).parent / "pages" / "1_Emission_TCFD.py"
    if script_path.exists():
        template_path = script_path.parent.parent / "shared" / "engine" / "tcfd" / "handdrawppt.pptx"
        print(f"\n1. 模板路徑計算：")
        print(f"   Script: {script_path}")
        print(f"   模板: {template_path}")
        print(f"   模板存在: {template_path.exists()}")
    else:
        # 如果找不到 script，使用項目根目錄
        template_path = Path(__file__).parent / "shared" / "engine" / "tcfd" / "handdrawppt.pptx"
        print(f"\n1. 模板路徑（備用）：{template_path}")
        print(f"   模板存在: {template_path.exists()}")
    
    # 2. 測試參數（模擬實際 Streamlit 調用）
    print(f"\n2. 測試參數：")
    print(f"   產業: 製造業")
    print(f"   營收: 1000K USD")
    print(f"   碳排放: {{'total_tco2e': 100}}")
    print(f"   使用 Mock 數據: True")
    
    # 3. 檢查輸出文件是否已存在
    output_filename = "TCFD_table.pptx"  # 與 Streamlit 頁面中使用相同的文件名
    output_dir = Path(__file__).parent / "shared" / "engine" / "tcfd" / "output"
    output_path = output_dir / output_filename
    print(f"\n3. 輸出文件檢查：")
    print(f"   輸出目錄: {output_dir}")
    print(f"   輸出目錄存在: {output_dir.exists()}")
    print(f"   輸出文件: {output_path}")
    print(f"   輸出文件已存在: {output_path.exists()}")
    
    if output_path.exists():
        try:
            # 嘗試打開文件檢查是否被鎖定
            with open(output_path, 'rb') as f:
                f.read(1)
            print(f"   文件可讀取: ✅")
        except PermissionError:
            print(f"   文件被鎖定: ⚠️ (可能被 PowerPoint 打開)")
        except Exception as e:
            print(f"   文件檢查錯誤: {e}")
    
    # 4. 執行生成
    print(f"\n4. 開始生成 PPTX...")
    print("-" * 60)
    
    output_file = generate_combined_pptx(
        output_filename=output_filename,  # 使用與 Streamlit 相同的文件名
        template_path=template_path if template_path.exists() else None,
        industry="製造業",
        revenue="1000K USD",
        carbon_emission={"total_tco2e": 100},
        llm_api_key=None,
        llm_provider=None,
        use_mock=True  # 使用 Mock 數據避免 API 調用
    )
    
    print("-" * 60)
    
    if output_file:
        print(f"\n✅ 成功生成文件：{output_file}")
        print(f"   文件存在: {output_file.exists()}")
        print(f"   文件大小: {output_file.stat().st_size} bytes")
    else:
        print("\n❌ 函數返回 None，但沒有拋出異常")
        print("   這表示函數內部發生了錯誤，但被 try-except 捕獲了")
        print("   請查看上方的錯誤信息（Error generating combined PPTX）")
        
except Exception as e:
    print(f"\n❌ 捕獲到異常：{type(e).__name__}")
    print(f"錯誤信息：{str(e)}")
    import traceback
    print("\n完整 traceback：")
    print("=" * 60)
    traceback.print_exc()
    print("=" * 60)

