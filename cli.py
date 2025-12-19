"""
CLI Entry Point - Command Line Interface
Usage:
    python cli.py --mode mock --module environment
    python cli.py --mode llm-test --module company
    python cli.py --mode production --module all
"""
import argparse
import json
import sys
from pathlib import Path
from shared.engine import ReportEngine


def main():
    parser = argparse.ArgumentParser(
        description='ESG Report Generation System - CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Mock mode - test environment module
  python cli.py --mode mock --module environment
  
  # LLM test mode - test company module only
  python cli.py --mode llm-test --module company
  
  # Production mode - generate all modules
  python cli.py --mode production --module all
  
  # Save output to file
  python cli.py --mode mock --module all --output report.json
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['mock', 'llm-test', 'production'],
        default='mock',
        help='Execution mode: mock (skip LLM), llm-test (test single module), production (full LLM)'
    )
    
    parser.add_argument(
        '--module',
        choices=['environment', 'company', 'governance', 'all'],
        default='all',
        help='Module to generate: environment, company, governance, or all'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (JSON format). If not specified, print to stdout'
    )
    
    parser.add_argument(
        '--input',
        type=str,
        help='Input JSON file path. If not specified, use default input data'
    )
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = ReportEngine(mode=args.mode)
    engine.log_mode_info()
    
    # Load input data
    if args.input and Path(args.input).exists():
        with open(args.input, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
    else:
        # Default input data
        input_data = {
            "company_name": "Sample Company",
            "year": "2025"
        }
    
    # Determine modules to generate
    if args.module == 'all':
        modules = None  # Generate all
    else:
        modules = [args.module]
    
    # Generate reports
    print(f"\nGenerating report(s) in {args.mode} mode...")
    print(f"Module(s): {args.module}")
    print("-" * 50)
    
    try:
        results = engine.generate_all(input_data, modules)
        
        # Format output
        output = {
            "mode": args.mode,
            "modules": list(results.keys()),
            "results": results,
            "metadata": {
                "input_data": input_data
            }
        }
        
        # Output results
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Report saved to: {output_path}")
        else:
            print("\n" + json.dumps(output, indent=2, ensure_ascii=False))
        
        # Summary
        print("\n" + "=" * 50)
        print("Summary:")
        for module_name, result in results.items():
            if "error" in result:
                print(f"  ❌ {module_name}: FAILED - {result['error']}")
            else:
                pages_count = len(result.get('pages', []))
                print(f"  ✅ {module_name}: SUCCESS - {pages_count} pages generated")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

