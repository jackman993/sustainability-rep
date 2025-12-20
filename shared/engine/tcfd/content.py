"""
TCFD Prompt Content
Prompt 內容模板：所有表格的 prompt 定義
"""
from .config import DEFAULT_INDUSTRY, DEFAULT_REVENUE


def get_common_role(industry: str = None, revenue: str = None) -> str:
    """
    獲取通用角色提示詞
    
    Args:
        industry: 產業名稱（可選，從 session_state 獲取）
        revenue: 營收（可選，從 session_state 獲取）
    
    Returns:
        角色提示詞字符串
    """
    industry = industry or DEFAULT_INDUSTRY
    revenue = revenue or DEFAULT_REVENUE
    return f"Act as the CSO of a {industry} company. Revenue: {revenue}."


def get_prompt(prompt_id: str, industry: str = None, revenue: str = None, **kwargs) -> str:
    """
    獲取指定表格的完整 prompt
    
    Args:
        prompt_id: Prompt ID（如 'prompt_table_1_trans'）
        industry: 產業名稱
        revenue: 營收
        **kwargs: 其他動態參數（如 carbon_emission 數據）
    
    Returns:
        完整的 prompt 字符串
    """
    common_role = get_common_role(industry, revenue)
    
    # 獲取特定表格的 prompt 模板
    prompt_template = PROMPTS.get(prompt_id, "")
    
    # 構建完整 prompt
    full_prompt = f"{common_role}\n\n{prompt_template}"
    
    # 如果有額外的上下文數據（如 carbon_emission），可以添加到 prompt
    if kwargs.get('carbon_emission'):
        emission_data = kwargs['carbon_emission']
        emission_context = f"""
Context: Current carbon emission data
- Total Emissions: {emission_data.get('total_tco2e', 'N/A')} tCO2e
- Scope 1: {emission_data.get('scope1', 'N/A')} tCO2e
- Scope 2: {emission_data.get('scope2', 'N/A')} tCO2e
- Industry: {emission_data.get('industry', industry)}
- Region: {emission_data.get('region', 'N/A')}
"""
        full_prompt = f"{full_prompt}\n\n{emission_context}"
    
    return full_prompt


# ==================================================
# Prompt Templates (Aligned with Table 1-7)
# ==================================================
PROMPTS = {
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

