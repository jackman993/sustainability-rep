"""
TCFD Main Engine
主邏輯：協調配置、內容生成和表格生成
"""
import os
import sys
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import re

from . import config
from . import content

# 嘗試導入 Claude API
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


def load_table_module(script_file: str):
    """
    動態載入表格生成模組
    
    Args:
        script_file: 表格腳本文件名（如 'table01.py'）
    
    Returns:
        載入的模組對象
    """
    script_path = config.TABLES_DIR / script_file
    
    if not script_path.exists():
        raise FileNotFoundError(f"Table script not found: {script_path}")
    
    module_name = f"tcfd_table_{script_file.replace('.py', '')}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    
    if spec is None:
        raise ImportError(f"Cannot load module: {script_path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    return module


def call_claude_api(prompt: str, api_key: str, model: str = "claude-3-5-sonnet-20241022") -> str:
    """
    調用 Claude API 生成內容
    
    Args:
        prompt: 完整的 prompt
        api_key: Anthropic API Key
        model: Claude 模型名稱
    
    Returns:
        API 返回的文本內容
    """
    if not ANTHROPIC_AVAILABLE:
        raise ImportError("anthropic package not installed. Install with: pip install anthropic")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


def parse_llm_response(response: str) -> List[str]:
    """
    解析 LLM 返回的內容，提取表格行數據
    
    Args:
        response: LLM 返回的文本
    
    Returns:
        表格內容列表（每行是 ||| 分隔的字符串）
    """
    lines = []
    # 尋找包含 ||| 分隔符的行
    for line in response.split('\n'):
        line = line.strip()
        if '|||' in line:
            lines.append(line)
    
    # 如果沒有找到 ||| 分隔的行，嘗試其他格式
    if not lines:
        # 嘗試尋找列表格式
        for line in response.split('\n'):
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or re.match(r'^\d+\.', line)):
                # 嘗試解析為表格格式
                cleaned = re.sub(r'^[-•\d+\.]\s*', '', line)
                if cleaned:
                    lines.append(cleaned)
    
    # 如果還是沒有，返回原始響應的第一部分
    if not lines:
        lines = [response[:200] + " ||| N/A ||| N/A"]
    
    return lines[:10]  # 最多返回 10 行


def generate_mock_data(prompt_id: str, industry: str = None, carbon_emission: Dict[str, Any] = None) -> List[str]:
    """
    生成模擬數據（用於測試）
    
    Args:
        prompt_id: Prompt ID
        industry: 產業名稱
        carbon_emission: 碳排放數據
    
    Returns:
        模擬的表格內容列表
    """
    industry = industry or "Manufacturing"
    
    # 根據不同的表格類型生成不同的模擬數據
    if 'trans' in prompt_id:
        return [
            f"Policy & Regulation Risk;{industry} sector faces new carbon tax regulations ||| Financial Impact: $500K-1M annually ||| Mitigation: Invest in carbon offset programs; Budget: $200K",
            f"Market & Technology Risk;Shift to green technology may disrupt traditional {industry} markets ||| Financial Impact: $2M-5M revenue risk ||| Mitigation: Develop green product lines; Budget: $1M"
        ]
    elif 'physical' in prompt_id:
        return [
            f"Acute Risk (Short Term);Extreme weather events affecting {industry} operations ||| Financial Impact: $300K-800K per event ||| Mitigation: Strengthen facility resilience; Budget: $500K",
            f"Chronic Risk (Long Term);Rising temperatures impacting {industry} supply chain ||| Financial Impact: $1M-3M annually ||| Mitigation: Diversify supply sources; Budget: $800K"
        ]
    elif 'opp_resource' in prompt_id:
        return [
            f"Resource Efficiency;Implement energy-efficient processes in {industry} operations ||| Financial Benefit: $400K-600K annual savings ||| Investment: Upgrade equipment; Budget: $1.5M",
            f"Energy Source;Transition to renewable energy for {industry} facilities ||| Financial Benefit: $200K-400K annual savings ||| Investment: Solar panel installation; Budget: $2M"
        ]
    elif 'opp_product' in prompt_id:
        return [
            f"Products & Services;Develop sustainable {industry} products for green market ||| Financial Benefit: $5M-10M new revenue ||| Investment: R&D and marketing; Budget: $3M",
            f"New Markets & Resilience;Expand {industry} business to climate-resilient regions ||| Financial Benefit: $3M-7M new revenue ||| Investment: Market entry and setup; Budget: $2M"
        ]
    elif 'metrics' in prompt_id:
        total_emission = carbon_emission.get('total_tco2e', 100) if carbon_emission else 100
        return [
            f"GHG Emissions Target;Reduce total emissions by 30% by 2030 (Current: {total_emission:.1f} tCO2e) ||| Progress: 15% reduction achieved ||| Action Plan: Energy efficiency projects; Budget: $1M",
            f"Other Climate Target;Increase renewable energy usage to 50% by 2028 ||| Progress: 25% renewable energy achieved ||| Action Plan: Solar and wind investments; Budget: $2M"
        ]
    elif 'systemic' in prompt_id:
        return [
            f"Industry Certification;Obtain ISO 14001 environmental management certification ||| Driver: Customer requirements; Gap: Missing documentation ||| Action: Complete certification process; Budget: $150K",
            f"Supply Chain Visibility;Enhance visibility into {industry} supply chain emissions ||| Driver: Regulatory compliance; Gap: Limited supplier data ||| Action: Implement supplier reporting system; Budget: $300K"
        ]
    elif 'resilience' in prompt_id:
        return [
            f"Workforce Capability;Train {industry} workforce on climate adaptation strategies ||| Stressor: Climate-related disruptions; Impact: Operational delays ||| Action: Comprehensive training program; Budget: $200K",
            f"Supply Chain Security;Diversify {industry} supply sources to reduce climate risks ||| Stressor: Single-source dependency; Impact: Supply disruptions ||| Action: Identify and onboard alternative suppliers; Budget: $500K"
        ]
    else:
        # 默認模擬數據
        return [
            f"{industry} Item A;Detail 1 ||| Impact $100K ||| Action Plan A;Budget $50K",
            f"{industry} Item B;Detail 2 ||| Impact $200K ||| Action Plan B;Budget $80K"
        ]


def generate_table_content(
    prompt_id: str,
    industry: str = None,
    revenue: str = None,
    carbon_emission: Dict[str, Any] = None,
    llm_api_key: str = None,
    llm_provider: str = None,
    use_mock: bool = False
) -> List[str]:
    """
    生成表格內容（調用 LLM 或使用模擬數據）
    
    Args:
        prompt_id: Prompt ID（如 'prompt_table_1_trans'）
        industry: 產業名稱
        revenue: 營收
        carbon_emission: 碳排放數據字典
        llm_api_key: LLM API Key（可選）
        llm_provider: LLM 提供商（可選，如 'anthropic'）
        use_mock: 是否使用模擬數據（True = Mock, False = 嘗試 API）
    
    Returns:
        表格內容列表（每行是 ||| 分隔的字符串）
    """
    # 構建完整 prompt
    full_prompt = content.get_prompt(
        prompt_id=prompt_id,
        industry=industry,
        revenue=revenue,
        carbon_emission=carbon_emission
    )
    
    # 如果明確要求使用 Mock，或沒有提供 API Key，使用模擬數據
    if use_mock or not llm_api_key or not llm_provider:
        return generate_mock_data(prompt_id, industry, carbon_emission)
    
    # 嘗試調用 LLM API
    try:
        if llm_provider.lower() == 'anthropic' or llm_provider.lower() == 'claude':
            response = call_claude_api(full_prompt, llm_api_key)
            return parse_llm_response(response)
        else:
            # 不支持的提供商，使用 Mock
            return generate_mock_data(prompt_id, industry, carbon_emission)
    except Exception as e:
        print(f"Error calling LLM API: {str(e)}")
        # API 調用失敗，回退到 Mock
        return generate_mock_data(prompt_id, industry, carbon_emission)


def generate_table(
    page_key: str,
    output_dir: Path = None,
    industry: str = None,
    revenue: str = None,
    carbon_emission: Dict[str, Any] = None,
    llm_api_key: str = None,
    llm_provider: str = None,
    use_mock: bool = False
) -> Optional[Path]:
    """
    生成單個 TCFD 表格
    
    Args:
        page_key: 頁面鍵（如 'page_1'）
        output_dir: 輸出目錄（默認為 config.OUTPUT_DIR）
        industry: 產業名稱
        revenue: 營收
        carbon_emission: 碳排放數據
        llm_api_key: LLM API Key
        llm_provider: LLM 提供商
    
    Returns:
        生成的 PowerPoint 文件路徑，失敗返回 None
    """
    if page_key not in config.TCFD_PAGES:
        raise ValueError(f"Invalid page_key: {page_key}")
    
    page_info = config.TCFD_PAGES[page_key]
    output_dir = output_dir or config.OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    
    try:
        # 1. 載入表格生成模組
        table_module = load_table_module(page_info['script_file'])
        
        # 2. 生成表格內容
        # 如果沒有明確指定 use_mock，則根據是否有 API key 決定
        if use_mock is None:
            use_mock = (not llm_api_key or not llm_provider)
        
        data_lines = generate_table_content(
            prompt_id=page_info['prompt_id'],
            industry=industry,
            revenue=revenue,
            carbon_emission=carbon_emission,
            llm_api_key=llm_api_key,
            llm_provider=llm_provider,
            use_mock=use_mock
        )
        
        # 3. 調用表格生成函數
        entry_func_name = page_info['entry_function']
        
        if not hasattr(table_module, entry_func_name):
            raise AttributeError(
                f"Function '{entry_func_name}' not found in {page_info['script_file']}"
            )
        
        func = getattr(table_module, entry_func_name)
        
        # 4. 設定輸出檔名
        safe_script_name = page_info['script_file'].replace('.py', '')
        out_filename = f"TCFD_{page_key}_{safe_script_name}.pptx"
        out_path = output_dir / out_filename
        
        # 5. 生成表格（傳入數據和完整路徑）
        func(data_lines, filename=str(out_path))
        
        return out_path
        
    except Exception as e:
        print(f"Error generating table {page_key}: {str(e)}")
        return None


def generate_all_tables(
    output_dir: Path = None,
    industry: str = None,
    revenue: str = None,
    carbon_emission: Dict[str, Any] = None,
    llm_api_key: str = None,
    llm_provider: str = None
) -> Dict[str, Optional[Path]]:
    """
    生成所有 TCFD 表格
    
    Args:
        output_dir: 輸出目錄
        industry: 產業名稱
        revenue: 營收
        carbon_emission: 碳排放數據
        llm_api_key: LLM API Key
        llm_provider: LLM 提供商
    
    Returns:
        字典：{page_key: 文件路徑}
    """
    results = {}
    
    for page_key in config.TCFD_PAGES.keys():
        results[page_key] = generate_table(
            page_key=page_key,
            output_dir=output_dir,
            industry=industry,
            revenue=revenue,
            carbon_emission=carbon_emission,
            llm_api_key=llm_api_key,
            llm_provider=llm_provider
        )
    
    return results

