#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TCFD 本地測試橋接腳本
用途：在本地測試 TCFD 生成功能，確認無誤後再推送到 Streamlit

使用方法：
1. Mock 數據模式：python test_tcfd_bridge.py
2. LLM API 模式：python test_tcfd_bridge.py --api-key YOUR_API_KEY
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any

# 添加項目路徑
sys.path.insert(0, str(Path(__file__).parent))

def create_test_data():
    """創建測試數據（模擬 Streamlit session_state）"""
    return {
        'industry': 'Manufacturing',
        'revenue_str': '50K USD',
        'carbon_emission': {
            'total_tco2e': 1250.5,
            'scope1': 300.2,
            'scope2': 450.8,
            'scope3': 499.5
        }
    }

def test_mock_mode():
    """測試 Mock 數據模式"""
    print("=" * 60)
    print("測試 1: Mock 數據模式")
    print("=" * 60)
    
    try:
        from shared.engine.tcfd import generate_combined_pptx
        from shared.engine.tcfd import config
        
        test_data = create_test_data()
        
        # 模板路徑（使用 config.BASE_DIR，避免路徑問題）
        template_path = config.BASE_DIR / "handdrawppt.pptx"
        if not template_path.exists():
            print(f"⚠️  模板文件不存在: {template_path}")
            print("   將使用默認模板")
            template_path = None
        
        print(f"\n📊 測試參數:")
        print(f"   產業: {test_data['industry']}")
        print(f"   營收: {test_data['revenue_str']}")
        print(f"   碳排放: {test_data['carbon_emission']['total_tco2e']} tCO2e")
        print(f"   模板路徑: {template_path}")
        print(f"   使用 Mock 數據: True")
        
        print(f"\n🔄 開始生成 PPTX...")
        output_file = generate_combined_pptx(
            output_filename="TCFD_table_test_mock.pptx",
            template_path=template_path if template_path and template_path.exists() else None,
            industry=test_data['industry'],
            revenue=test_data['revenue_str'],
            carbon_emission=test_data['carbon_emission'],
            llm_api_key=None,
            llm_provider=None,
            use_mock=True
        )
        
        if output_file and output_file.exists():
            print(f"\n✅ 成功！")
            print(f"   輸出文件: {output_file}")
            print(f"   文件大小: {output_file.stat().st_size / 1024:.2f} KB")
            return True
        else:
            print(f"\n❌ 失敗！")
            print(f"   輸出文件: {output_file}")
            print(f"   文件存在: {output_file.exists() if output_file else False}")
            return False
            
    except Exception as e:
        print(f"\n❌ 錯誤發生:")
        import traceback
        traceback.print_exc()
        return False

def test_llm_api_mode(api_key: str):
    """測試 LLM API 模式"""
    print("\n" + "=" * 60)
    print("測試 2: LLM API 模式（Claude）")
    print("=" * 60)
    
    try:
        from shared.engine.tcfd import generate_combined_pptx
        from shared.engine.tcfd import config
        
        test_data = create_test_data()
        
        # 模板路徑
        template_path = config.BASE_DIR / "handdrawppt.pptx"
        if not template_path.exists():
            print(f"⚠️  模板文件不存在: {template_path}")
            template_path = None
        
        print(f"\n📊 測試參數:")
        print(f"   產業: {test_data['industry']}")
        print(f"   營收: {test_data['revenue_str']}")
        print(f"   碳排放: {test_data['carbon_emission']['total_tco2e']} tCO2e")
        print(f"   API Key: {api_key[:10]}..." if api_key else "None")
        print(f"   使用 Mock 數據: False")
        
        print(f"\n🔄 開始生成 PPTX（調用 Claude API）...")
        print("   ⚠️  注意：這會消耗 API 額度")
        
        output_file = generate_combined_pptx(
            output_filename="TCFD_table_test_api.pptx",
            template_path=template_path if template_path and template_path.exists() else None,
            industry=test_data['industry'],
            revenue=test_data['revenue_str'],
            carbon_emission=test_data['carbon_emission'],
            llm_api_key=api_key,
            llm_provider="anthropic",
            use_mock=False
        )
        
        if output_file and output_file.exists():
            print(f"\n✅ 成功！")
            print(f"   輸出文件: {output_file}")
            print(f"   文件大小: {output_file.stat().st_size / 1024:.2f} KB")
            return True
        else:
            print(f"\n❌ 失敗！")
            print(f"   輸出文件: {output_file}")
            print(f"   文件存在: {output_file.exists() if output_file else False}")
            return False
            
    except Exception as e:
        print(f"\n❌ 錯誤發生:")
        import traceback
        traceback.print_exc()
        return False

def check_dependencies():
    """檢查依賴"""
    print("=" * 60)
    print("檢查依賴...")
    print("=" * 60)
    
    issues = []
    
    # 檢查 Python 版本
    if sys.version_info < (3, 7):
        issues.append(f"Python 版本過低: {sys.version}")
    else:
        print(f"✅ Python 版本: {sys.version.split()[0]}")
    
    # 檢查必要模組
    try:
        import pptx
        print(f"✅ python-pptx: {pptx.__version__}")
    except ImportError:
        issues.append("❌ python-pptx 未安裝: pip install python-pptx")
    
    try:
        import anthropic
        print(f"✅ anthropic: {anthropic.__version__}")
    except ImportError:
        issues.append("⚠️  anthropic 未安裝（LLM API 模式需要）: pip install anthropic")
    
    # 檢查 TCFD 模組
    try:
        from shared.engine.tcfd import generate_combined_pptx, config
        print(f"✅ TCFD 模組: 已導入")
        print(f"   BASE_DIR: {config.BASE_DIR}")
        print(f"   OUTPUT_DIR: {config.OUTPUT_DIR}")
    except Exception as e:
        issues.append(f"❌ TCFD 模組導入失敗: {e}")
    
    # 檢查模板文件
    try:
        from shared.engine.tcfd import config
        template_path = config.BASE_DIR / "handdrawppt.pptx"
        if template_path.exists():
            print(f"✅ 模板文件: {template_path}")
        else:
            issues.append(f"⚠️  模板文件不存在: {template_path}")
    except:
        pass
    
    if issues:
        print("\n⚠️  發現問題:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print("\n✅ 所有依賴檢查通過")
        return True

def main():
    parser = argparse.ArgumentParser(description='TCFD 本地測試橋接腳本')
    parser.add_argument('--api-key', type=str, help='Claude API Key（測試 LLM API 模式）')
    parser.add_argument('--mock-only', action='store_true', help='只測試 Mock 模式')
    parser.add_argument('--api-only', action='store_true', help='只測試 LLM API 模式')
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("TCFD 本地測試橋接腳本")
    print("=" * 60)
    
    # 檢查依賴
    if not check_dependencies():
        print("\n❌ 依賴檢查失敗，請先解決問題")
        sys.exit(1)
    
    results = []
    
    # 測試 Mock 模式
    if not args.api_only:
        result = test_mock_mode()
        results.append(("Mock 模式", result))
    
    # 測試 LLM API 模式
    if args.api_key and not args.mock_only:
        result = test_llm_api_mode(args.api_key)
        results.append(("LLM API 模式", result))
    elif not args.mock_only and not args.api_key:
        print("\n" + "=" * 60)
        print("跳過 LLM API 模式測試（需要 --api-key 參數）")
        print("=" * 60)
    
    # 總結
    print("\n" + "=" * 60)
    print("測試總結")
    print("=" * 60)
    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 所有測試通過！可以推送到 Streamlit 了")
        sys.exit(0)
    else:
        print("\n⚠️  部分測試失敗，請檢查錯誤信息")
        sys.exit(1)

if __name__ == "__main__":
    main()

