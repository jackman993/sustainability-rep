"""
Unified interfaces for all modules
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class ModuleInterface(ABC):
    """Base interface for all report modules"""
    
    @abstractmethod
    def generate(self, input_data: Dict[str, Any], mode_manager) -> Dict[str, Any]:
        """
        Generate report content for the module
        
        Args:
            input_data: Input data dictionary
            mode_manager: ModeManager instance to determine execution mode
        
        Returns:
            Dictionary containing generated report content
        """
        pass
    
    @abstractmethod
    def get_module_name(self) -> str:
        """Get the name of the module"""
        pass

