import os
import sys
import importlib.util
from pathlib import Path

# 載入設定檔 (讀取 tcfd_config.py)
import tcfd_config as config

def load_module_from_path(module_name, file_path):
    """
    動態載入 Python 模組的工具函數
    Dynamic module loader used to import the table scripts.
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"Cannot find file: {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def get_dummy_data(page_key):
    """
    產生假資料 (用於測試，未來會換成 LLM)
    Mock Data Generator (Placeholder for LLM)
    """
    print(f"   [Data] Fetching mock data for {page_key}...")
    # 這裡回傳符合 ||| 分隔格式的假資料
    return [
        "Risk/Opp Item A;Detail 1 ||| Impact $100K ||| Action Plan A;Budget $50K",
        "Risk/Opp Item B;Detail 2 ||| Impact $200K ||| Action Plan B;Budget $80K"
    ]

def main():
    print("="*60)
    print(f"🚀 TCFD Report Engine - Using files in: {config.ASSETS_DIR}")
    print("="*60)
    
    # 建立 output 資料夾
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)
        print(f"📁 Created output directory: {config.OUTPUT_DIR}")

    # 依序執行 Config 中定義的所有頁面
    for page_key, page_info in config.TCFD_PAGES.items():
        print(f"\n📄 Processing: {page_info['title']} ({page_key})")
        
        # 1. 組合正確的檔案路徑
        # Logic: Current Dir + Filename from Config (e.g., TCFD_table01_W.py)
        script_path = config.ASSETS_DIR / page_info['script_file']
        
        # 檢查檔案是否存在
        if not script_path.exists():
            print(f"   ❌ CRITICAL ERROR: File missing -> {page_info['script_file']}")
            print(f"      Expected path: {script_path}")
            continue
            
        try:
            # 2. 動態載入 _W.py 檔案
            # Load the W File as a module
            module_name = f"mod_{page_key}"
            table_module = load_module_from_path(module_name, script_path)
            print(f"   ✅ Loaded module: {page_info['script_file']}")
            
            # 3. 獲取資料 (目前是假資料)
            # Get Data (Mock or LLM)
            data_lines = get_dummy_data(page_key)
            
            # 4. 執行對應的繪圖函數
            # Execute the specific function defined in config (e.g., generate_table_01)
            entry_func_name = page_info['entry_function']
            
            if hasattr(table_module, entry_func_name):
                func = getattr(table_module, entry_func_name)
                
                # 設定輸出檔名
                # Output filename: TCFD_page_1_TCFD_table01_W.pptx
                safe_script_name = page_info['script_file'].replace('.py', '')
                out_name = f"TCFD_{page_key}_{safe_script_name}.pptx"
                
                # 呼叫函數！(傳入資料與檔名)
                # Run the generation function
                func(data_lines, filename=out_name)
                
                full_out_path = config.OUTPUT_DIR / out_name
                print(f"   ✨ Generated successfully: output/{out_name}")
                
            else:
                print(f"   ⚠️ Function '{entry_func_name}' not found in {page_info['script_file']}")
                print(f"      Please ensure you define 'def {entry_func_name}(lines, filename=None):' inside the file.")
                
        except Exception as e:
            print(f"   ❌ Execution Failed: {str(e)}")
            # import traceback
            # traceback.print_exc()

    print("\n" + "="*60)
    print("🎉 Sequence Complete. Please check the 'output' folder.")

if __name__ == "__main__":
    main()