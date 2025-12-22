"""
Full API Test - Generate Complete PPTX with API Key
Usage: python test_api_full.py YOUR_API_KEY
"""
import sys
from pathlib import Path
from datetime import datetime
import os

sys.path.insert(0, str(Path(__file__).parent))

from environment_pptx import EnvironmentPPTXEngine

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_api_full.py YOUR_API_KEY")
        print("Example: python test_api_full.py sk-ant-api03-...")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    print("="*60)
    print("Full PPTX Generation Test with API")
    print("="*60)
    print(f"API Key: {api_key[:10]}...{api_key[-4:]}\n")
    
    try:
        # Configuration
        template_path = None  # Will use default handdrawppt.pptx
        tcfd_output_folder = None
        emission_output_folder = None
        test_mode = False  # Use API
        industry = "Technology"
        
        print("[Initializing Engine...]")
        engine = EnvironmentPPTXEngine(
            template_path=template_path,
            test_mode=test_mode,
            industry=industry,
            tcfd_output_folder=tcfd_output_folder,
            emission_output_folder=emission_output_folder,
            api_key=api_key
        )
        
        print("\n[Generating Report with LLM Content...]")
        print("  This may take 2-5 minutes as it calls Claude API multiple times...")
        print("  Please wait...\n")
        
        pptx = engine.generate()
        
        # Save file
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = output_dir / f"ESG_Environment_Chapter_API_{timestamp}.pptx"
        
        engine.save(str(filename))
        
        print("\n" + "="*60)
        print("✓ Full Generation Test Completed Successfully!")
        print("="*60)
        print(f"✓ Output File: {filename}")
        print(f"✓ Total Slides: {len(pptx.slides)}")
        print(f"✓ File Size: {os.path.getsize(filename) / 1024 / 1024:.2f} MB")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Generation Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

