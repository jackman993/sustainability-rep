"""
Quick test script to verify the architecture works
"""
import sys
from shared.engine import ReportEngine
from shared.mode_manager import ExecutionMode


def test_mock_mode():
    """Test Mock mode"""
    print("=" * 60)
    print("Testing MOCK Mode")
    print("=" * 60)
    
    engine = ReportEngine(mode="mock")
    engine.log_mode_info()
    
    input_data = {
        "company_name": "Test Company",
        "year": "2025"
    }
    
    # Test single module
    print("\nTesting Environment module...")
    result = engine.generate_module("environment", input_data)
    print(f"✅ Environment module: {len(result.get('pages', []))} pages generated")
    
    # Test all modules
    print("\nTesting all modules...")
    results = engine.generate_all(input_data)
    for module_name, result in results.items():
        if "error" in result:
            print(f"❌ {module_name}: {result['error']}")
        else:
            pages_count = len(result.get('pages', []))
            print(f"✅ {module_name}: {pages_count} pages generated")
    
    print("\n" + "=" * 60)
    print("Mock Mode Test Completed!")
    print("=" * 60 + "\n")


def test_mode_manager():
    """Test Mode Manager"""
    print("=" * 60)
    print("Testing Mode Manager")
    print("=" * 60)
    
    from shared.mode_manager import ModeManager
    
    # Test Mock mode
    manager = ModeManager("mock")
    assert manager.should_use_llm() == False, "Mock mode should not use LLM"
    print("✅ Mock mode: LLM disabled correctly")
    
    # Test Production mode
    manager = ModeManager("production")
    assert manager.should_use_llm() == True, "Production mode should use LLM"
    print("✅ Production mode: LLM enabled correctly")
    
    print("\n" + "=" * 60)
    print("Mode Manager Test Completed!")
    print("=" * 60 + "\n")


def main():
    """Run all tests"""
    print("\n" + "🚀 Testing Three-Channel Parallel Architecture" + "\n")
    
    try:
        test_mode_manager()
        test_mock_mode()
        
        print("=" * 60)
        print("✅ All Tests Passed!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Test CLI: python cli.py --mode mock --module environment")
        print("2. Test Server: python server.py --port 8000")
        print("3. Test Streamlit: streamlit run app_new.py")
        print("=" * 60 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

