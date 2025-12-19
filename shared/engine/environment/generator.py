"""
Environment Report Generator
"""
import json
import os
from typing import Dict, Any
from shared.interfaces import ModuleInterface
from shared.mode_manager import ModeManager


class EnvironmentGenerator(ModuleInterface):
    """Generate Environment section report"""
    
    def __init__(self):
        self.module_name = "environment"
    
    def get_module_name(self) -> str:
        return self.module_name
    
    def generate(self, input_data: Dict[str, Any], mode_manager: ModeManager) -> Dict[str, Any]:
        """
        Generate environment report
        
        Args:
            input_data: Input data (company info, carbon data, etc.)
            mode_manager: ModeManager instance
        
        Returns:
            Dictionary with generated report content
        """
        if mode_manager.should_use_llm(self.module_name):
            return self._generate_with_llm(input_data, mode_manager)
        else:
            return self._generate_with_mock(input_data, mode_manager)
    
    def _generate_with_llm(self, input_data: Dict[str, Any], mode_manager: ModeManager) -> Dict[str, Any]:
        """Generate report using Claude LLM"""
        from shared.llm import ClaudeClient
        
        # Initialize Claude client
        try:
            claude_client = ClaudeClient(mode_manager)
        except ValueError as e:
            raise ValueError(f"Failed to initialize Claude client: {str(e)}")
        
        # Prepare prompt with input data
        company_name = input_data.get("company_name", "Company")
        year = input_data.get("year", "2025")
        carbon_data = input_data.get("carbon_emission", {})
        revenue_data = input_data.get("estimated_annual_revenue", {})
        
        # Build system prompt
        system_prompt = """You are an expert ESG report writer specializing in environmental sustainability reports.
Generate comprehensive, professional environmental reports based on the provided data.
The report should be structured, factual, and aligned with international ESG standards."""
        
        # Build user prompt
        prompt = f"""Generate an environmental sustainability report for {company_name} for the year {year}.

Company Information:
- Company Name: {company_name}
- Year: {year}"""

        if revenue_data:
            revenue_k = revenue_data.get("k_value", 0)
            currency = revenue_data.get("currency", "NTD")
            prompt += f"\n- Estimated Annual Revenue: {revenue_k:,.2f} K {currency}"

        if carbon_data:
            total_emissions = carbon_data.get("total_tco2e", 0)
            scope1 = carbon_data.get("scope1", 0)
            scope2 = carbon_data.get("scope2", 0)
            prompt += f"""
Carbon Emissions Data:
- Total Emissions (Scope 1+2): {total_emissions} tCO2e
- Scope 1 Emissions: {scope1} tCO2e
- Scope 2 Emissions: {scope2} tCO2e"""

        prompt += """

Please generate a comprehensive environmental report including:
1. Executive Summary
2. Environmental Risk Analysis
3. Carbon Emission Analysis
4. Environmental Management Measures
5. Improvement Recommendations

Format the response as JSON with the following structure:
{
  "pages": [
    {{"page_number": 1, "title": "...", "content": "..."}},
    ...
  ],
  "content": {{
    "summary": "...",
    "risks": ["...", "..."],
    "recommendations": ["...", "..."]
  }}
}"""

        # Generate report using Claude
        try:
            result = claude_client.generate_structured(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=4096,
                temperature=0.7
            )
            
            return {
                "module": "environment",
                "mode": "llm",
                "pages": result.get("pages", []),
                "content": result.get("content", {}),
                "metadata": {
                    "generated_at": "2025-12-19",
                    "model": claude_client.model,
                    "api_version": claude_client.api_version,
                    "input_data_keys": list(input_data.keys())
                }
            }
        except Exception as e:
            raise ValueError(f"Failed to generate report with Claude: {str(e)}")
    
    def _generate_with_mock(self, input_data: Dict[str, Any], mode_manager: ModeManager) -> Dict[str, Any]:
        """Generate report using mock data"""
        mock_path = mode_manager.get_mock_data_path(self.module_name)
        
        if os.path.exists(mock_path):
            with open(mock_path, 'r', encoding='utf-8') as f:
                mock_data = json.load(f)
        else:
            # Default mock data
            mock_data = self._get_default_mock_data()
        
        # Merge with input data
        result = {
            "module": "environment",
            "mode": "mock",
            "pages": mock_data.get("pages", []),
            "content": mock_data.get("content", {}),
            "metadata": {
                "generated_at": "2025-12-18",
                "input_data_keys": list(input_data.keys())
            }
        }
        
        return result
    
    def _get_default_mock_data(self) -> Dict[str, Any]:
        """Get default mock data if file doesn't exist"""
        return {
            "pages": [
                {
                    "page_number": 1,
                    "title": "Environment Report Cover",
                    "content": "Environment Sustainability Report"
                },
                {
                    "page_number": 2,
                    "title": "Executive Summary",
                    "content": "Key environmental indicators and achievements"
                },
                {
                    "page_number": 3,
                    "title": "Environmental Risk Analysis",
                    "content": "Main environmental risks and impacts"
                },
                {
                    "page_number": 4,
                    "title": "Improvement Recommendations",
                    "content": "Prioritized action plans"
                },
                {
                    "page_number": 5,
                    "title": "Appendix",
                    "content": "Data sources and methodology"
                }
            ],
            "content": {
                "summary": "Mock environment report content",
                "risks": ["Climate change", "Resource depletion"],
                "recommendations": ["Reduce emissions", "Improve efficiency"]
            }
        }

