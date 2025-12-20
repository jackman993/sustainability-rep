import os
from pathlib import Path

# ==================================================
# 1. Base Paths
# ==================================================
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ==================================================
# 2. Global Settings
# ==================================================
PROJECT_NAME = "TCFD_Report_2025"
INDUSTRY = "Semiconductor"
REVENUE = "50B USD"

# ==================================================
# 3. Page & File Mapping (Corrected Order)
# ==================================================
# Mapping logic based on your Prompt structure (Table 1 to 7)

TCFD_PAGES = {
    # [Table 1] Transformation Risks (Policy & Market combined in Prompt)
    'page_1': {
        'title': 'Transformation Risks',
        'script_file': 'TCFD_table01_W.py',     
        'entry_function': 'generate_table_01', 
        'prompt_id': 'prompt_table_1_trans'
    },
    
    # [Table 2] Physical Risks (Changed from Market to Physical)
    'page_2': {
        'title': 'Physical Risks',
        'script_file': 'TCFD_table02_W.py',     # Corrected: Now points to Physical Risk
        'entry_function': 'generate_table_02',
        'prompt_id': 'prompt_table_2_physical'
    },
    
    # [Table 3] Opportunities (Resource Efficiency)
    'page_3': {
        'title': 'Opportunities: Resource & Energy',
        'script_file': 'TCFD_table03_W.py',     
        'entry_function': 'generate_table_03',
        'prompt_id': 'prompt_table_3_opp_resource'
    },
    
    # [Table 4] Opportunities (Products & Markets)
    'page_4': {
        'title': 'Opportunities: Products & Services',
        'script_file': 'TCFD_table04_W.py',     
        'entry_function': 'generate_table_04',
        'prompt_id': 'prompt_table_4_opp_product'
    },
    
    # [Table 5] Metrics & Targets
    'page_5': {
        'title': 'Metrics and Targets',
        'script_file': 'TCFD_table05_W.py',     
        'entry_function': 'generate_table_05',
        'prompt_id': 'prompt_table_5_metrics'
    },
    
    # [Table 6] Systemic Risk Control (Shared File)
    'page_6': {
        'title': 'Systemic Risk Control',
        'script_file': 'TCFD_table0607_W.py',   
        'entry_function': 'generate_table_06',  
        'prompt_id': 'prompt_table_6_systemic'
    },
    
    # [Table 7] Operational Resilience (Shared File)
    'page_7': {
        'title': 'Operational Resilience',
        'script_file': 'TCFD_table0607_W.py',   
        'entry_function': 'generate_table_07',  
        'prompt_id': 'prompt_table_7_resilience'
    }
}

# ==================================================
# 4. Prompt Library (Aligned with Table 1-7)
# ==================================================
PROMPTS = {
    'common_role': f"Act as the CSO of a {INDUSTRY} company. Revenue: {REVENUE}.",
    
    'prompt_table_1_trans': """
Task: Generate Table 1 (Transformation Risks).
Format: Pure text (||| separator).
Row 1: Policy & Regulation Risk
Row 2: Market & Technology Risk
Columns: Risk Description ||| Financial Impact ||| Mitigation Action
""",

    'prompt_table_2_physical': """
Task: Generate Table 2 (Physical Risks).
Format: Pure text (||| separator).
Row 1: Acute Risk (Short Term)
Row 2: Chronic Risk (Long Term)
Columns: Risk Description ||| Financial Impact ||| Mitigation Action
""",

    'prompt_table_3_opp_resource': """
Task: Generate Table 3 (Opportunities - Resource).
Format: Pure text (||| separator).
Row 1: Resource Efficiency
Row 2: Energy Source
Columns: Opportunity ||| Financial Benefit ||| Investment Action
""",

    'prompt_table_4_opp_product': """
Task: Generate Table 4 (Opportunities - Products).
Format: Pure text (||| separator).
Row 1: Products & Services
Row 2: New Markets & Resilience
Columns: Opportunity ||| Financial Benefit ||| Investment Action
""",

    'prompt_table_5_metrics': """
Task: Generate Table 5 (Metrics & Targets).
Format: Pure text (||| separator).
Row 1: GHG Emissions Target
Row 2: Other Climate Target
Columns: Metric Category ||| Progress Status ||| Action Plan
""",

    'prompt_table_6_systemic': """
Task: Generate Table 6 (Systemic Risk).
Format: Pure text (||| separator).
Row 1: Industry Certification
Row 2: Supply Chain Visibility
Columns: Area ||| Driver/Gap ||| Action & Budget
""",

    'prompt_table_7_resilience': """
Task: Generate Table 7 (Operational Resilience).
Format: Pure text (||| separator).
Row 1: Workforce Capability
Row 2: Supply Chain Security
Columns: Focus Unit ||| Stressor & Impact ||| Action & Budget
"""
}