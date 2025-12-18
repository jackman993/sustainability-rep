"""
Governance Report Generator
"""
import json
import os
from typing import Dict, Any
from shared.interfaces import ModuleInterface
from shared.mode_manager import ModeManager


class GovernanceGenerator(ModuleInterface):
    """Generate Governance section report"""
    
    def __init__(self):
        self.module_name = "governance"
    
    def get_module_name(self) -> str:
        return self.module_name
    
    def generate(self, input_data: Dict[str, Any], mode_manager: ModeManager) -> Dict[str, Any]:
        """
        Generate governance report
        
        Args:
            input_data: Input data
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
        api_key = mode_manager.get_api_key()
        if not api_key:
            raise ValueError("API key required for LLM mode")
        
        # Placeholder for LLM implementation
        return {
            "module": "governance",
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
            mock_data = self._get_default_mock_data()
        
        result = {
            "module": "governance",
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
                    "title": "Governance Report Cover",
                    "content": "Governance & Social Responsibility Report"
                },
                {
                    "page_number": 2,
                    "title": "Governance Structure",
                    "content": "Organizational structure and decision-making processes"
                },
                {
                    "page_number": 3,
                    "title": "Compliance Assessment",
                    "content": "Regulatory compliance status"
                },
                {
                    "page_number": 4,
                    "title": "Risk Management",
                    "content": "Governance risk identification"
                },
                {
                    "page_number": 5,
                    "title": "Improvement Path",
                    "content": "Governance optimization recommendations"
                }
            ],
            "content": {
                "structure": "Mock governance structure",
                "compliance": {"status": "Compliant", "issues": []},
                "recommendations": ["Enhance board diversity", "Improve transparency"]
            }
        }

