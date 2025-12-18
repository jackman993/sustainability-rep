# Three-Channel Parallel Architecture

## Overview

This system implements a flexible three-channel parallel architecture for ESG report generation:

**3 Execution Modes × 3 Entry Points = Flexible Testing Architecture**

## Execution Modes

### Mode A: Mock Mode
- **Purpose**: Fast testing of workflow, UI, and data flow
- **Features**: No API key needed, fast execution, repeatable
- **Use Cases**: Development phase, workflow validation

### Mode B: LLM-Test Mode
- **Purpose**: Test single module's LLM calls
- **Features**: Test only specified module, saves API costs
- **Use Cases**: Prompt optimization, single module development

### Mode C: Production Mode
- **Purpose**: Full report generation
- **Features**: All modules use real LLM
- **Use Cases**: Final testing, actual usage

## Entry Points

### Entry 1: CLI Command Line
```bash
python cli.py --mode mock --module environment
python cli.py --mode llm-test --module company
python cli.py --mode production --module all
```

**Advantages**: Fast, automatable, suitable for batch testing
**Scenarios**: Development debugging, CI/CD, batch generation

### Entry 2: Localhost Server API
```bash
python server.py --port 8000
# Access at http://localhost:8000
```

**Advantages**: RESTful API, integrable with other systems, cross-language calls
**Scenarios**: Integration testing, API calls, microservice architecture

### Entry 3: Streamlit Cloud
```bash
streamlit run app_new.py
```

**Advantages**: Web UI, visual, suitable for demonstrations
**Scenarios**: User usage, demonstrations, interactive operations

## Directory Structure

```
sustainability-rep/
├── shared/                    # Shared core logic
│   ├── engine/               # Core business logic (shared by all entries)
│   │   ├── environment/      # Environment module
│   │   ├── company/          # Company module
│   │   └── governance/       # Governance module
│   ├── mode_manager.py       # Mode switching (Mock/LLM-Test/Production)
│   ├── interfaces/           # Unified interface definitions
│   └── mock_data/            # Mock data files
│       └── default/          # Default mock data
├── config/                    # Configuration files
├── cli.py                     # CLI entry point
├── server.py                  # Server API entry point
└── app_new.py                 # Streamlit UI entry point
```

## Architecture Pattern

### Interface Adapter Pattern

```
Entry Layer (Thin)          Core Layer (Thick)           Output Layer
──────────                  ──────────                   ────────
CLI Entry ──┐                │                            │
Server API ─┤                ├──→ Unified Engine ←──┐   │  Unified Output Format
Streamlit UI ─┘              │      (CLI=file/        │   │  Adapted by Entry
                             │       Server=JSON/      │   │  (CLI=file/Server=JSON/UI=display)
                             │       UI=display)       │   │
                             │                        │   │
                             │  Mode Manager          │   │
                             │  (Mock/LLM-Test/      │   │
                             │   Production)          │   │
                             │                        │   │
                             │  Core Business Logic   │   │
```

## Module Design

Each module (Environment/Company/Governance) is independent:
- Can be tested separately
- Can be called separately
- Can be deployed separately
- Core logic doesn't depend on entry method

## Usage Examples

### CLI Examples

```bash
# Mock mode - test environment module
python cli.py --mode mock --module environment

# LLM test mode - test company module only
python cli.py --mode llm-test --module company --output company_report.json

# Production mode - generate all modules
python cli.py --mode production --module all --output full_report.json
```

### Server API Examples

```bash
# Start server
python server.py --port 8000

# Generate report via API
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

### Streamlit Examples

```bash
# Run Streamlit app
streamlit run app_new.py

# Access at http://localhost:8501
```

## Configuration

### Mode Priority
1. Command line argument
2. Environment variable (`MODE`)
3. Config file (`config/config.json`)
4. Default (Mock)

### API Key Configuration
- Environment variable: `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- Streamlit secrets: `.streamlit/secrets.toml`

## Development Workflow

1. **Core Engine** (Priority): Build `shared/engine/` core logic
2. **Mode Manager**: Implement mode switching
3. **Three Entries** (Parallel Development):
   - CLI entry: Wrap engine with command-line argument parsing
   - Server entry: FastAPI/Flask wrapper, provide REST API
   - Streamlit entry: UI wrapper, call same engine
4. **Demo Version**: 5-page simplified version per section
   - Use Mock mode for quick workflow validation
   - Deploy to Streamlit Cloud for testing

## Efficiency Optimizations

1. **Shared Core Logic**: All entries use the same engine
2. **Interface Adapter Pattern**: Entry layer only adapts, core layer is thick
3. **Modular Design**: Each module is independent
4. **Mock Data**: Fast testing without API costs

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure `shared/` directory is in Python path
2. **API Key Not Found**: Set environment variable or Streamlit secrets
3. **Module Not Found**: Check module name spelling (environment, company, governance)

## Future Enhancements

- [ ] Implement LLM integration for Production mode
- [ ] Add PowerPoint/PDF output format
- [ ] Add logging system
- [ ] Add unit tests
- [ ] Add CI/CD pipeline

