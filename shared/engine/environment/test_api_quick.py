"""
Quick API Test - Simple command line version
Usage: python test_api_quick.py YOUR_API_KEY
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from content_engine import ContentEngine
from config import ENVIRONMENT_CONFIG

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_api_quick.py YOUR_API_KEY")
        print("Example: python test_api_quick.py sk-ant-api03-...")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    print("="*60)
    print("Quick LLM API Test")
    print("="*60)
    print(f"API Key: {api_key[:10]}...{api_key[-4:]}\n")
    
    try:
        engine = ContentEngine(test_mode=False, api_key=api_key)
        
        print("[Testing: Environmental Cover Content]")
        cover_text = engine.generate_environmental_cover(ENVIRONMENT_CONFIG)
        print(f"✓ Success! Generated {len(cover_text)} characters")
        print(f"\nPreview:\n{cover_text[:200]}...\n")
        
        print("="*60)
        print("✓ API Test Successful!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ API Test Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

