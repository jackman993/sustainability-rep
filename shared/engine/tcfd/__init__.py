"""
TCFD Module
TCFD 表格生成模組
"""
from .config import (
    TCFD_PAGES,
    BASE_DIR,
    TABLES_DIR,
    OUTPUT_DIR,
    DEFAULT_INDUSTRY,
    DEFAULT_REVENUE
)
from .content import (
    get_common_role,
    get_prompt,
    PROMPTS
)
from .main import (
    generate_table,
    generate_all_tables,
    generate_table_content,
    load_table_module
)

__all__ = [
    # Config
    'TCFD_PAGES',
    'BASE_DIR',
    'TABLES_DIR',
    'OUTPUT_DIR',
    'DEFAULT_INDUSTRY',
    'DEFAULT_REVENUE',
    # Content
    'get_common_role',
    'get_prompt',
    'PROMPTS',
    # Main
    'generate_table',
    'generate_all_tables',
    'generate_table_content',
    'load_table_module'
]

