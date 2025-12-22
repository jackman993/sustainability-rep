"""
Test Script with API Key - Test LLM Content Generation
"""
import os
import sys
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from environment_pptx import EnvironmentPPTXEngine
    from content_engine import ContentEngine
except ImportError as e:
    print(f"✗ Import Error: {e}")
    print("Please make sure you're in the correct directory")
    sys.exit(1)

def test_llm_content(api_key):
    """Test LLM content generation with API key"""
    print("="*60)
    print("Testing LLM Content Generation")
    print("="*60)
    
    if not api_key:
        print("✗ API Key is required!")
        return False
    
    try:
        # Test ContentEngine with API key
        print(f"\n[Testing ContentEngine with API Key...]")
        print(f"API Key: {api_key[:10]}...{api_key[-4:]}")
        
        content_engine = ContentEngine(
            test_mode=False,  # Use API
            api_key=api_key
        )
        
        # Test generating cover content
        print("\n[Testing: Environmental Cover Content]")
        from config import ENVIRONMENT_CONFIG
        cover_text = content_engine.generate_environmental_cover(ENVIRONMENT_CONFIG)
        print(f"✓ Generated {len(cover_text)} characters")
        print(f"Preview: {cover_text[:100]}...")
        
        # Test generating policy content
        print("\n[Testing: Policy Description Content]")
        policy_text = content_engine.generate_policy_description(ENVIRONMENT_CONFIG)
        print(f"✓ Generated {len(policy_text)} characters")
        print(f"Preview: {policy_text[:100]}...")
        
        print("\n" + "="*60)
        print("✓ LLM API Test Successful!")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n✗ LLM API Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_generation(api_key, template_path=None):
    """Test full PPTX generation with API key"""
    print("\n" + "="*60)
    print("Testing Full PPTX Generation with API")
    print("="*60)
    
    if not api_key:
        print("✗ API Key is required!")
        return False
    
    try:
        # Configuration
        tcfd_output_folder = None
        emission_output_folder = None
        test_mode = False  # Use API
        industry = "Technology"
        
        print(f"\n✓ API Key: {api_key[:10]}...{api_key[-4:]}")
        print(f"✓ Industry: {industry}")
        print(f"✓ Test Mode: OFF (Using API)")
        
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
        print(f"\n[Generating Report with LLM Content...]")
        print("  This may take a few minutes as it calls Claude API...")
        pptx = engine.generate()
        
        # Save file
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = output_dir / f"ESG_Environment_Chapter_API_{timestamp}.pptx"
        
        engine.save(str(filename))
        
        print(f"\n{'='*60}")
        print(f"✓ Full Generation Test Completed Successfully!")
        print(f"✓ Output: {filename}")
        print(f"✓ Total Slides: {len(pptx.slides)}")
        print(f"{'='*60}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Full Generation Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("="*60)
    print("Environment Chapter PPTX - API Test Script")
    print("="*60)
    
    # Get API Key
    print("\n[API Key Input]")
    print("Please enter your Claude API Key:")
    print("(You can also set it as environment variable: ANTHROPIC_API_KEY)")
    
    # Try to get from environment variable first
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if api_key:
        print(f"✓ Found API Key from environment variable")
        use_env_key = input("Use environment variable API Key? (Y/n): ").strip().lower()
        if use_env_key == 'n':
            api_key = None
    
    # If not using env var, get from input
    if not api_key:
        api_key = input("API Key: ").strip()
        if not api_key:
            print("✗ API Key is required!")
            return
    
    # Test mode selection
    print("\n[Test Mode Selection]")
    print("1. Test LLM Content Generation Only (Quick)")
    print("2. Test Full PPTX Generation with API (Takes longer)")
    print("3. Both")
    
    choice = input("Select (1/2/3): ").strip()
    
    if choice == "1":
        test_llm_content(api_key)
    elif choice == "2":
        # Optional: template path
        template_path = None
        use_template = input("\nUse default template (handdrawppt.pptx)? (Y/n): ").strip().lower()
        if use_template == 'n':
            custom_template = input("Enter custom template path (or press Enter for None): ").strip()
            if custom_template and os.path.exists(custom_template):
                template_path = custom_template
        
        test_full_generation(api_key, template_path)
    elif choice == "3":
        if test_llm_content(api_key):
            print("\n" + "-"*60)
            proceed = input("LLM test passed. Continue with full generation? (Y/n): ").strip().lower()
            if proceed != 'n':
                template_path = None
                use_template = input("Use default template (handdrawppt.pptx)? (Y/n): ").strip().lower()
                if use_template == 'n':
                    custom_template = input("Enter custom template path (or press Enter for None): ").strip()
                    if custom_template and os.path.exists(custom_template):
                        template_path = custom_template
                test_full_generation(api_key, template_path)
    else:
        print("✗ Invalid choice!")

if __name__ == "__main__":
    main()

