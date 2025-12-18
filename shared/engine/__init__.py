"""
Unified Engine - Entry point for all report generation
"""
from typing import Dict, Any, Optional, List
from shared.mode_manager import ModeManager
from shared.engine.environment import EnvironmentGenerator
from shared.engine.company import CompanyGenerator
from shared.engine.governance import GovernanceGenerator


class ReportEngine:
    """Unified report generation engine"""
    
    def __init__(self, mode: Optional[str] = None):
        """
        Initialize report engine
        
        Args:
            mode: Execution mode (mock, llm-test, production)
        """
        self.mode_manager = ModeManager(mode)
        self.generators = {
            "environment": EnvironmentGenerator(),
            "company": CompanyGenerator(),
            "governance": GovernanceGenerator()
        }
    
    def generate_module(self, module_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate report for a specific module
        
        Args:
            module_name: Name of the module (environment, company, governance)
            input_data: Input data dictionary
        
        Returns:
            Generated report content
        """
        if module_name not in self.generators:
            raise ValueError(f"Unknown module: {module_name}. Available: {list(self.generators.keys())}")
        
        generator = self.generators[module_name]
        return generator.generate(input_data, self.mode_manager)
    
    def generate_all(self, input_data: Dict[str, Any], modules: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate reports for all modules or specified modules
        
        Args:
            input_data: Input data dictionary
            modules: List of module names to generate. If None, generate all.
        
        Returns:
            Dictionary with all generated reports
        """
        if modules is None:
            modules = list(self.generators.keys())
        
        results = {}
        for module_name in modules:
            try:
                results[module_name] = self.generate_module(module_name, input_data)
            except Exception as e:
                results[module_name] = {
                    "error": str(e),
                    "module": module_name,
                    "status": "failed"
                }
        
        return results
    
    def get_available_modules(self) -> List[str]:
        """Get list of available modules"""
        return list(self.generators.keys())
    
    def log_mode_info(self):
        """Log current mode information"""
        self.mode_manager.log_mode_info()

