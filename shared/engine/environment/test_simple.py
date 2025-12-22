"""
Simple Test Script - No API Required
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from environment_pptx import EnvironmentPPTXEngine
    from datetime import datetime
except ImportError as e:
    print(f"✗ Import Error: {e}")
    print("Please make sure you're in the correct directory")
    sys.exit(1)

def main():
    """Simple test without API"""
    import sys
    sys.stdout.flush()  # Force flush output
    
    print("="*60)
    print("Simple Test - Environment Chapter PPTX Generation")
    print("="*60)
    sys.stdout.flush()
    
    # Configuration
    template_path = None
    tcfd_output_folder = None  # Will auto-find from assets/TCFD
    emission_output_folder = None
    test_mode = True  # IMPORTANT: Test mode, no API calls
    industry = "Technology"
    api_key = None
    
    print(f"\n✓ Test Mode: ON (No API calls)")
    print(f"✓ Industry: {industry}")
    
    # Check TCFD file
    tcfd_path = Path(__file__).parent / "assets" / "TCFD"
    tcfd_file = list(tcfd_path.glob("TCFD*.pptx")) if tcfd_path.exists() else []
    if tcfd_file:
        print(f"✓ TCFD file found: {tcfd_file[0].name}")
    else:
        print(f"⚠ TCFD file not found in: {tcfd_path}")
        print(f"  Will create placeholder pages")
    
    try:
        # Initialize engine
        print(f"\n[Initializing Engine...]")
        engine = EnvironmentPPTXEngine(
            template_path=template_path,
            test_mode=test_mode,
            industry=industry,
            tcfd_output_folder=tcfd_output_folder,
            emission_output_folder=emission_output_folder,
            api_key=api_key
        )
        
        # Generate report
        print(f"\n[Generating Report...]")
        pptx = engine.generate()
        
        # Save file
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = output_dir / f"ESG_Environment_Chapter_{timestamp}.pptx"
        
        engine.save(str(filename))
        
        print(f"\n{'='*60}")
        print(f"✓ Test Completed Successfully!")
        print(f"✓ Output: {filename}")
        print(f"✓ Total Slides: {len(pptx.slides)}")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

