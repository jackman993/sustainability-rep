"""
TCFD Prompt Content
Prompt 內容模板：所有表格的 prompt 定義
"""
from .config import DEFAULT_INDUSTRY, DEFAULT_REVENUE


def get_common_role(industry: str = None, revenue: str = None) -> str:
    """
    獲取通用角色提示詞（優化版本）
    
    Args:
        industry: 產業名稱（可選，從 session_state 獲取）
        revenue: 營收（可選，從 session_state 獲取）
    
    Returns:
        角色提示詞字符串
    """
    industry = industry or DEFAULT_INDUSTRY
    revenue = revenue or DEFAULT_REVENUE
    
    # 使用優化的 common_role prompt
    common_role_template = PROMPTS.get('common_role', '')
    # 替換變量
    return common_role_template.replace('{INDUSTRY}', industry).replace('{REVENUE}', revenue)


def get_prompt(prompt_id: str, industry: str = None, revenue: str = None, **kwargs) -> str:
    """
    獲取指定表格的完整 prompt（優化版本）
    
    Args:
        prompt_id: Prompt ID（如 'prompt_table_1_trans'）
        industry: 產業名稱
        revenue: 營收
        **kwargs: 其他動態參數（如 carbon_emission 數據）
    
    Returns:
        完整的 prompt 字符串
    """
    # 獲取 common_role（已替換變量）
    common_role = get_common_role(industry, revenue)
    
    # 獲取特定表格的 prompt 模板
    prompt_template = PROMPTS.get(prompt_id, "")
    
    # 替換 prompt 模板中的 {INDUSTRY} 變量
    industry = industry or DEFAULT_INDUSTRY
    prompt_template = prompt_template.replace('{INDUSTRY}', industry)
    
    # 構建完整 prompt（common_role + specific prompt）
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
# Enhanced Prompt Templates (Optimized for Table Engines)
# ==================================================
# These prompts force the LLM to output data in "Desc ||| Impact ||| Action" format.

PROMPTS = {
    # 共用角色設定 (會被安插在每個 Prompt 的開頭)
    'common_role': """
Role: You are a dual expert combining deep industry expertise and ESG knowledge:

1. INDUSTRY EXPERT specializing in {INDUSTRY} sector:
   - Deep knowledge of {INDUSTRY}-specific regulations, standards, and compliance requirements
   - Understanding of {INDUSTRY} market dynamics, competitive landscape, and customer/client characteristics
   - Expertise in {INDUSTRY} technical processes, supply chains, operational challenges, and business models
   - Familiarity with {INDUSTRY}-specific terminology, technologies, and industry trends
   - Knowledge of {INDUSTRY} risk factors, opportunities, and strategic considerations

2. ESG & CLIMATE RISK EXPERT:
   - Expertise in TCFD framework, climate risk assessment, and sustainability reporting
   - Understanding of ESG best practices, stakeholder expectations, and regulatory trends
   - Knowledge of climate-related financial impacts and adaptation strategies

Company Context: {INDUSTRY} company with revenue of {REVENUE}.
Your analysis MUST be deeply rooted in {INDUSTRY} sector specifics. Provide detailed, industry-specific insights with comprehensive explanations.

Style: Technical, precise, detailed, and industry-specific. Use {INDUSTRY}-specific terminology, regulations, market insights, and technical details. Provide comprehensive analysis with sufficient detail to demonstrate deep industry knowledge.

Constraint: Output PURE TEXT only. Do not use Markdown tables.
Separator: Use "|||" to separate columns.
Bullet points: Use ";" to separate multiple points within a cell.
Detail Level: Provide comprehensive, detailed content. Include specific examples, quantifiable impacts, and actionable strategies relevant to {INDUSTRY} sector.
""",

    # [Table 1] Transformation Risks - Focused on Policy & Regulation and Product & Tech
    'prompt_table_1_trans': """
Task: Generate comprehensive, highly detailed content for 'Table 1: Transformation Risks' for {INDUSTRY} industry.

FOCUS: This table focuses exclusively on TWO critical transformation risks:
1. Policy & Regulation Risk
2. Green Product & Technology Risk

As an industry expert specializing in {INDUSTRY} sector, you MUST provide EXTENSIVE, DETAILED analysis for each risk category.

Structure: Output exactly 2 lines. Each line MUST be comprehensive, detailed, and industry-specific (minimum 150-200 words per line).

Line 1: Policy & Regulation Risk (Short/Medium Term) - MUST be EXTENSIVELY detailed
As an industry expert, provide COMPREHENSIVE analysis including:

REGULATORY LANDSCAPE:
- Identify SPECIFIC regulations, policies, laws, and compliance requirements currently affecting {INDUSTRY} sector
- List actual or anticipated policy changes (e.g., sector-specific carbon pricing mechanisms, emission standards, product regulations, trade policies, environmental permits, industry-specific compliance frameworks)
- Analyze regulatory trends and evolution in {INDUSTRY} sector
- Include regional, national, and international regulations relevant to {INDUSTRY}

COMPLIANCE ANALYSIS:
- Detailed analysis of compliance deadlines, requirements, and enforcement mechanisms
- Assessment of compliance costs and resource requirements
- Evaluation of penalties, sanctions, or operational restrictions for non-compliance
- Analysis of regulatory reporting and disclosure requirements

FINANCIAL IMPACT:
- Provide DETAILED financial impact analysis based on {INDUSTRY} operations, including:
  * Direct costs (carbon taxes, compliance fees, permit costs)
  * Indirect costs (operational changes, process modifications, staff training)
  * Opportunity costs (restricted operations, delayed projects)
  * Quantified impacts with specific amounts, percentages, and timeframes
- Analyze impact on profit margins, operating costs, and cash flow
- Include industry-specific cost structures and financial metrics

STRATEGIC RESPONSE:
- Specific, actionable strategies tailored to {INDUSTRY} sector
- Detailed action plans with timelines and milestones
- Budget breakdown with specific cost allocations
- Risk mitigation measures and contingency plans

Line 2: Green Product & Technology Risk (Short/Medium Term) - MUST be EXTENSIVELY detailed
As an industry expert, provide COMPREHENSIVE analysis including:

TECHNOLOGY DISRUPTION ANALYSIS:
- Analyze technology disruptions and innovations in {INDUSTRY} sector:
  * Green alternatives and sustainable technologies replacing traditional {INDUSTRY} processes
  * Low-carbon processes, materials, and production methods
  * Digitalization and automation trends affecting {INDUSTRY}
  * Emerging technologies that could disrupt {INDUSTRY} business model
- Include SPECIFIC technologies, processes, equipment, or innovations relevant to {INDUSTRY}
- Analyze technology adoption rates and market penetration

COMPETITIVE LANDSCAPE:
- Detailed assessment of competitive landscape:
  * How competitors are adopting green technologies
  * Market leaders and innovators in {INDUSTRY} sustainability
  * Competitive advantages/disadvantages from technology adoption
  * Market positioning and differentiation strategies
- Analyze competitive threats from technology-enabled new entrants

BUSINESS MODEL IMPACT:
- Evaluate impact of technology shifts on {INDUSTRY} business model:
  * Changes to production processes and operational efficiency
  * Impact on product/service offerings and value proposition
  * Supply chain and distribution channel transformations
  * Customer expectations and market demands
- Analyze business model risks and opportunities

FINANCIAL IMPACT:
- Provide DETAILED financial impact analysis:
  * R&D investment requirements for technology adoption
  * Capital expenditure needs for new equipment/processes
  * Revenue risks from technology obsolescence
  * Cost savings or efficiency gains from new technologies
  * Market share risks and competitive positioning costs
- Quantify impacts with specific amounts, percentages, and ROI projections

STRATEGIC RESPONSE:
- Specific technology adoption strategies for {INDUSTRY} sector
- Detailed R&D and innovation roadmaps
- Technology partnership and collaboration plans
- Budget breakdown with specific investment allocations
- Risk mitigation and technology transition plans

CRITICAL REQUIREMENTS:
- Each line MUST contain EXTENSIVE, comprehensive content (minimum 150-200 words per line)
- All analysis MUST be deeply {INDUSTRY}-specific, demonstrating expert knowledge
- Include specific examples, regulations, technologies, processes, and market dynamics relevant to {INDUSTRY}
- Provide detailed, quantifiable impacts with comprehensive financial analysis
- Use {INDUSTRY}-specific terminology, technical details, and industry insights
- Demonstrate deep understanding of {INDUSTRY} operations, challenges, and opportunities

Format: Risk Description (EXTENSIVE, comprehensive, industry-specific, highly detailed) ||| Financial Impact (DETAILED quantification with specific amounts, percentages, timeframes, and multiple cost components) ||| Response Action & Budget (SPECIFIC, actionable strategies with detailed budget breakdown, timelines, and implementation plans)

Example Output (for {INDUSTRY}):
[EXTENSIVE policy analysis with specific regulations, compliance requirements, financial impacts, and detailed action plans] ||| [COMPREHENSIVE financial impact with multiple cost components, percentages, and timeframes] ||| [SPECIFIC action plan with detailed budget allocation, timelines, and implementation steps]
[EXTENSIVE technology analysis with specific technologies, competitive landscape, business model impacts, and detailed adoption strategies] ||| [COMPREHENSIVE financial impact with R&D costs, revenue risks, and ROI projections] ||| [SPECIFIC technology adoption strategy with detailed budget, partnerships, and transition plans]
""",

    # [Table 2] Physical Risks
    'prompt_table_2_physical': """
Task: Generate content for 'Table 2: Physical Risks'.
Structure: Output exactly 2 lines.
Line 1: Acute Risk (Short/Medium Term) - Focus on Extreme Weather (Floods/Droughts) hitting specific assets.
Line 2: Chronic Risk (Long Term >2026) - Focus on Rising Temp/Sea Levels affecting efficiency.
Format: Risk Description ||| Financial Impact (Asset damage/Opex in 'K') ||| Response Action & Budget
Example Output:
Flash floods threatening Fab 3; Typhoon disrupting logistics ||| Asset repair cost est. $120,000K; Production halt for 5 days ||| Install flood gates (Budget: $30,000K); Establish backup logistics hub
Rising mean temperature reducing cooling efficiency ||| Electricity cooling cost increase $25,000K/year ||| Upgrade to magnetic bearing chillers (Budget: $60,000K); AI-based energy management
""",

    # [Table 3] Opportunities (Resource & Energy)
    'prompt_table_3_opp_resource': """
Task: Generate content for 'Table 3: Opportunities (Resource & Energy)'.
Structure: Output exactly 2 lines.
Line 1: Resource Efficiency - Focus on Water/Waste/Material recycling.
Line 2: Energy Source - Focus on Renewables/Electrification.
Format: Opportunity Description ||| Financial Benefit (Savings in 'K') ||| Strategy & Cost
Example Output:
Water recycling system optimization; Waste heat recovery ||| Cost savings of $45,000K/year; Reduced water withdrawal fee ||| Install RO recycling system (Budget: $100,000K); Closed-loop waste process
Adoption of solar PV and wind power PPA ||| Energy cost reduction of $30,000K/year; Carbon tax avoidance ||| Sign 20-year PPA; Install rooftop solar panels (Budget: $40,000K)
""",

    # [Table 4] Opportunities (Products & Markets)
    'prompt_table_4_opp_product': """
Task: Generate content for 'Table 4: Opportunities (Products & Markets)'.
Structure: Output exactly 2 lines.
Line 1: Products & Services - Focus on Low-carbon products/R&D.
Line 2: New Markets - Focus on Green Supply Chain access.
Format: Opportunity Description ||| Financial Benefit (Revenue in 'K') ||| Strategy & Cost
Example Output:
Development of ultra-low power chips; Green label products ||| New revenue stream of $500,000K; Market share growth 2% ||| R&D for 3nm low-power node (Budget: $300,000K); Eco-product certification
Entry into EU market via low-carbon compliance ||| Retention of Tier-1 client status ($800,000K value) ||| Establish EU green hub; Supply chain transparency platform (Budget: $20,000K)
""",

    # [Table 5] Metrics & Targets
    'prompt_table_5_metrics': """
Task: Generate content for 'Table 5: Metrics & Targets'.
Structure: Output exactly 2 lines.
Line 1: GHG Emissions Target (Scope 1, 2, 3).
Line 2: Other Climate Target (Water or Waste).
Format: Metric & Target Year ||| Current Progress ||| Action Plan to achieve Target
Example Output:
Reduce Scope 1&2 by 50% by 2030 (Base year 2020) ||| Achieved -15% reduction; Behind schedule on Scope 3 ||| Accelerate tool electrification; Supplier engagement program (Budget: $10,000K)
Achieve 90% Water Recycling Rate by 2028 ||| Current rate 75%; Water intensity decreased 5% ||| Upgrade wastewater treatment plant Phase II (Budget: $55,000K)
""",

    # [Table 6] Systemic Risk Control
    'prompt_table_6_systemic': """
Task: Generate content for 'Table 6: Systemic Risk Control'.
Constraint: Cite specific standards (e.g., RBA, ISO, IATF) relevant to the industry.
Structure: Output exactly 2 lines.
Line 1: Industry Certification / Compliance (License to sell).
Line 2: Supply Chain Visibility (Raw material tracking).
Format: Compliance Area ||| Driver / Gap Analysis ||| Action & Budget
Example Output:
RBA VAP Platinum Certification; EU Battery Regulation ||| Key clients require 100% compliance; Current gap in labor audit ||| Conduct 3rd party mock audits (Budget: $5,000K); Upgrade HR system
Conflict Minerals (3TG) & Cobalt Traceability ||| EU Demand for digital product passport; Lack of Tier-2 data ||| Implement Blockchain tracking system (Budget: $15,000K); Supplier training
""",

    # [Table 7] Operational Resilience
    'prompt_table_7_resilience': """
Task: Generate content for 'Table 7: Operational Resilience'.
Constraint: Focus on HUMAN and RESOURCE bottlenecks.
Structure: Output exactly 2 lines.
Line 1: Workforce Capability (Skill & Safety).
Line 2: Ecosystem/Resource Security (Water/Power access).
Format: Focus Unit ||| Stressor & Impact ||| Action & Budget
Example Output:
EHS & High-Voltage Safety Team ||| Skill gap in handling new EV equipment; High injury risk ||| Establish Safety Training Academy (Budget: $8,000K); VR safety simulation
Water Resource Resilience Team ||| Competition for local water rights during drought; Production risk ||| Joint water reclamation project with local gov (Budget: $25,000K); Community engagement
"""
}

