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
        """Generate report using LLM"""
        # TODO: Implement LLM call
        api_key = mode_manager.get_api_key()
        if not api_key:
            raise ValueError("API key required for LLM mode")
        
        # Placeholder for LLM implementation
        return {
            "module": "environment",
            "pages": [],
            "content": "LLM generation not yet implemented",
            "mode": "llm"
        }
    
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

