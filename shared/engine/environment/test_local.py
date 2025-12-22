"""
Local Test Script for Environment Chapter PPTX Generation
"""
from environment_pptx import EnvironmentPPTXEngine
from datetime import datetime
import os

def main():
    """Local test function"""
    
    # ============ 配置參數 ============
    # Template path (可選，預設使用 assets/handdrawppt.pptx)
    template_path = None  # None = 使用預設模板 (assets/handdrawppt.pptx)
    # 或指定自訂路徑: r"C:\Users\User\Desktop\custom_template.pptx"
    
    # TCFD 輸出資料夾路徑（如果有的話）
    # 方式1: 指定具體的 TCFD 輸出資料夾（包含 TCFD PPTX 檔案）
    tcfd_output_folder = None  # 例如: r"C:\Users\User\Desktop\TCFD generator\output\TCFD_20241220_123456"
    
    # 方式2: 如果沒有指定，會自動按以下順序查找：
    #   1. 本地 assets/TCFD 資料夾: C:\Users\User\Desktop\environment4.1-4.9\assets\TCFD
    #   2. 預設路徑: C:\Users\User\Desktop\TCFD generator\output
    # TCFD 檔案檔名格式: TCFD*.pptx（例如: TCFD_table (26).pptx，必須包含7頁投影片）
    
    # Emission 輸出資料夾（如果有的話）
    emission_output_folder = None  # 例如: r"C:\Users\User\Desktop\environment4.1-4.9\output"
    
    # 測試模式（跳過 LLM API 呼叫）
    test_mode = True  # 設為 True 可以跳過 API 呼叫，使用佔位文字
    
    # 產業名稱
    industry = "Technology"  # 例如: "Technology", "Manufacturing", "Finance"
    
    # API Key（如果 test_mode=False 才需要）
    api_key = None  # 例如: "sk-ant-api03-..."
    
    # ============ 生成報告 ============
    print("="*60)
    print("Environment Chapter PPTX Generation - Local Test")
    print("="*60)
    
    # 檢查 TCFD 文件
    if tcfd_output_folder:
        print(f"\n✓ Using specified TCFD folder: {tcfd_output_folder}")
        if not os.path.exists(tcfd_output_folder):
            print(f"  ⚠ Warning: TCFD folder does not exist!")
        else:
            # Check if TCFD PPTX file exists
            import glob
            tcfd_files = glob.glob(os.path.join(tcfd_output_folder, "TCFD*.pptx"))
            if tcfd_files:
                print(f"  ✓ Found TCFD file: {os.path.basename(tcfd_files[0])}")
            else:
                print(f"  ⚠ Warning: No TCFD*.pptx file found in folder!")
    else:
        # Check local assets folder first
        local_assets_path = os.path.join(os.path.dirname(__file__), "assets", "TCFD")
        default_tcfd_path = r"C:\Users\User\Desktop\TCFD generator\output"
        
        print(f"\nℹ TCFD folder not specified, will search in:")
        print(f"  1. Local assets: {local_assets_path}")
        print(f"  2. Default path: {default_tcfd_path}")
        
        if os.path.exists(local_assets_path):
            import glob
            tcfd_files = glob.glob(os.path.join(local_assets_path, "TCFD*.pptx"))
            if tcfd_files:
                print(f"  ✓ Found TCFD file in local assets: {os.path.basename(tcfd_files[0])}")
            else:
                print(f"  ℹ No TCFD*.pptx file found in local assets")
        else:
            print(f"  ℹ Local assets folder does not exist")
        
        if not os.path.exists(default_tcfd_path):
            print(f"  ⚠ Warning: Default TCFD path does not exist!")
            print(f"  ℹ TCFD pages will be created as placeholders if file not found")
    
    # 初始化引擎
    engine = EnvironmentPPTXEngine(
        template_path=template_path,
        test_mode=test_mode,
        industry=industry,
        tcfd_output_folder=tcfd_output_folder,
        emission_output_folder=emission_output_folder,
        api_key=api_key
    )
    
    # 生成報告
    pptx = engine.generate()
    
    # 儲存檔案
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"ESG_Environment_Chapter_{timestamp}.pptx")
    
    engine.save(filename)
    
    print(f"\n{'='*60}")
    print(f"✓ Test completed!")
    print(f"✓ Output file: {filename}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

