"""
TCFD Configuration
配置：路徑、設定、表格定義
"""
import os
from pathlib import Path

# ==================================================
# 1. Base Paths
# ==================================================
BASE_DIR = Path(__file__).parent
TABLES_DIR = BASE_DIR / "tables"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ==================================================
# 2. Global Settings
# ==================================================
PROJECT_NAME = "TCFD_Report_2025"
# 這些值可以從 session_state 動態獲取
DEFAULT_INDUSTRY = "Manufacturing"
DEFAULT_REVENUE = "50B USD"

# ==================================================
# 3. Page & File Mapping (Table 1 to 7)
# ==================================================
TCFD_PAGES = {
    # [Table 1] Transformation Risks
    'page_1': {
        'title': 'Transformation Risks',
        'script_file': 'table01.py',
        'entry_function': 'generate_table_01',
        'prompt_id': 'prompt_table_1_trans'
    },
    
    # [Table 2] Physical Risks
    'page_2': {
        'title': 'Physical Risks',
        'script_file': 'table02.py',
        'entry_function': 'generate_table_02',
        'prompt_id': 'prompt_table_2_physical'
    },
    
    # [Table 3] Opportunities (Resource Efficiency)
    'page_3': {
        'title': 'Opportunities: Resource & Energy',
        'script_file': 'table03.py',
        'entry_function': 'generate_table_03',
        'prompt_id': 'prompt_table_3_opp_resource'
    },
    
    # [Table 4] Opportunities (Products & Markets)
    'page_4': {
        'title': 'Opportunities: Products & Services',
        'script_file': 'table04.py',
        'entry_function': 'generate_table_04',
        'prompt_id': 'prompt_table_4_opp_product'
    },
    
    # [Table 5] Metrics & Targets
    'page_5': {
        'title': 'Metrics and Targets',
        'script_file': 'table05.py',
        'entry_function': 'generate_table_05',
        'prompt_id': 'prompt_table_5_metrics'
    },
    
    # [Table 6] Systemic Risk Control
    'page_6': {
        'title': 'Systemic Risk Control',
        'script_file': 'table0607.py',
        'entry_function': 'generate_table_06',
        'prompt_id': 'prompt_table_6_systemic'
    },
    
    # [Table 7] Operational Resilience
    'page_7': {
        'title': 'Operational Resilience',
        'script_file': 'table0607.py',
        'entry_function': 'generate_table_07',
        'prompt_id': 'prompt_table_7_resilience'
    }
}

