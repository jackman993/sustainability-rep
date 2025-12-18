# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Quick Test

```bash
# Test the architecture
python test_architecture.py
```

## Usage

### 1. CLI Entry (Command Line)

```bash
# Mock mode - test environment module
python cli.py --mode mock --module environment

# LLM test mode - test company module only
python cli.py --mode llm-test --module company

# Production mode - generate all modules
python cli.py --mode production --module all --output report.json
```

### 2. Server API Entry

```bash
# Start the server
python server.py --port 8000

# Access API documentation
# Open browser: http://localhost:8000/docs

# Test with curl
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "module": "environment",
    "mode": "mock",
    "input_data": {
      "company_name": "Sample Company",
      "year": "2025"
    }
  }'
```

### 3. Streamlit UI Entry

```bash
# Run Streamlit app
streamlit run app_new.py

# Access at http://localhost:8501
```

## Configuration

### Environment Variables

```bash
# Set execution mode
export MODE=mock  # or llm-test, production

# Set API key (for LLM modes)
export OPENAI_API_KEY=your_key_here
# or
export ANTHROPIC_API_KEY=your_key_here

# Set test module (for llm-test mode)
export TEST_MODULE=environment
```

### Streamlit Secrets

Create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your_key_here"
# or
ANTHROPIC_API_KEY = "your_key_here"
```

## Project Structure

```
sustainability-rep/
├── shared/                    # Core shared logic
│   ├── engine/               # Business logic engines
│   │   ├── environment/      # Environment module
│   │   ├── company/          # Company module
│   │   └── governance/       # Governance module
│   ├── mode_manager.py       # Mode management
│   ├── interfaces/           # Unified interfaces
│   └── mock_data/            # Mock data
├── config/                    # Configuration files
├── cli.py                     # CLI entry point
├── server.py                  # API server entry point
├── app_new.py                 # Streamlit UI entry point
└── test_architecture.py      # Test script
```

## Three Execution Modes

1. **Mock Mode** (`--mode mock`): Skip LLM, use mock data
   - Fast execution
   - No API key needed
   - Good for development and testing

2. **LLM-Test Mode** (`--mode llm-test`): Test single module with LLM
   - Test only specified module
   - Saves API costs
   - Good for prompt optimization

3. **Production Mode** (`--mode production`): Full LLM execution
   - All modules use real LLM
   - Requires API key
   - For final reports

## Troubleshooting

### Import Errors
Make sure you're running from the project root directory.

### API Key Not Found
- Set environment variable: `export OPENAI_API_KEY=your_key`
- Or use Streamlit secrets file: `.streamlit/secrets.toml`

### Module Not Found
Check module name spelling: `environment`, `company`, or `governance`

## Next Steps

1. Run test script to verify installation
2. Try Mock mode to test workflow
3. Configure API key for LLM modes
4. Test each entry point (CLI, Server, Streamlit)
5. Customize mock data in `shared/mock_data/default/`

