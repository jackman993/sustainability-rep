"""
Test script to verify pages directory structure
"""
import os
from pathlib import Path

def test_pages_structure():
    """Test if pages directory structure is correct for Streamlit"""
    base_path = Path(__file__).parent
    pages_dir = base_path / "pages"
    
    print("=" * 60)
    print("Testing Streamlit Pages Structure")
    print("=" * 60)
    
    # Check if pages directory exists
    if not pages_dir.exists():
        print("❌ pages/ directory not found!")
        return False
    
    print(f"✅ pages/ directory exists: {pages_dir}")
    
    # List all Python files in pages directory
    py_files = list(pages_dir.glob("*.py"))
    print(f"\n📄 Found {len(py_files)} Python files in pages/ directory:")
    
    for py_file in sorted(py_files):
        print(f"  - {py_file.name}")
        
        # Check if file has st.set_page_config
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'st.set_page_config' in content:
                print(f"    ✅ Has st.set_page_config")
            else:
                print(f"    ⚠️  Missing st.set_page_config")
    
    print("\n" + "=" * 60)
    print("Structure Check Complete!")
    print("=" * 60)
    print("\n💡 Note: Streamlit should automatically show these pages")
    print("   in the sidebar navigation when you run: streamlit run app.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_pages_structure()

