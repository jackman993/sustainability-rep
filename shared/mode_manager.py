"""
Mode Manager - Handles three execution modes:
- Mock: Skip LLM, use mock data
- LLM-Test: Test single module with LLM
- Production: Full LLM execution for all modules
"""
import os
from enum import Enum
from typing import Optional, Dict, Any
import json


class ExecutionMode(Enum):
    """Three execution modes"""
    MOCK = "mock"
    LLM_TEST = "llm-test"
    PRODUCTION = "production"


class ModeManager:
    """Manages execution mode and provides mode-specific behavior"""
    
    def __init__(self, mode: Optional[str] = None):
        """
        Initialize mode manager
        
        Priority: command line arg > environment variable > config file > default (MOCK)
        """
        self.mode = self._determine_mode(mode)
        self.config = self._load_config()
    
    def _determine_mode(self, mode_arg: Optional[str]) -> ExecutionMode:
        """Determine execution mode based on priority"""
        # Priority 1: Command line argument
        if mode_arg:
            try:
                return ExecutionMode(mode_arg.lower())
            except ValueError:
                print(f"Warning: Invalid mode '{mode_arg}', using default MOCK")
        
        # Priority 2: Environment variable
        env_mode = os.getenv('MODE', '').lower()
        if env_mode:
            try:
                return ExecutionMode(env_mode)
            except ValueError:
                print(f"Warning: Invalid MODE env var '{env_mode}', using default MOCK")
        
        # Priority 3: Config file (if exists)
        config_path = os.path.join('config', 'config.yaml')
        if os.path.exists(config_path):
            # For now, default to MOCK. Can be extended to read YAML
            pass
        
        # Priority 4: Default
        return ExecutionMode.MOCK
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config file"""
        config_path = os.path.join('config', 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def should_use_llm(self, module_name: Optional[str] = None) -> bool:
        """
        Determine if LLM should be used for a specific module
        
        Args:
            module_name: Name of the module (environment, company, governance)
        
        Returns:
            True if LLM should be used, False otherwise
        """
        if self.mode == ExecutionMode.MOCK:
            return False
        
        if self.mode == ExecutionMode.LLM_TEST:
            # Only use LLM for the specified test module
            test_module = self.config.get('test_module') or os.getenv('TEST_MODULE', '').lower()
            if module_name:
                return module_name.lower() == test_module.lower()
            return False
        
        if self.mode == ExecutionMode.PRODUCTION:
            return True
        
        return False
    
    def get_mock_data_path(self, module_name: str) -> str:
        """Get path to mock data for a module"""
        default_path = os.path.join('shared', 'mock_data', 'default', f'{module_name}.json')
        custom_path = os.path.join('shared', 'mock_data', 'custom', f'{module_name}.json')
        
        # Use custom mock data if exists, otherwise use default
        if os.path.exists(custom_path):
            return custom_path
        return default_path
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from environment variable or config"""
        # Priority: environment variable > config file
        api_key = os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            return api_key
        
        return self.config.get('api_key')
    
    def log_mode_info(self):
        """Log current mode information"""
        print(f"Execution Mode: {self.mode.value.upper()}")
        if self.mode == ExecutionMode.LLM_TEST:
            test_module = self.config.get('test_module') or os.getenv('TEST_MODULE', 'not specified')
            print(f"Test Module: {test_module}")
        print(f"LLM Enabled: {self.should_use_llm()}")
    
    @property
    def current_mode(self) -> ExecutionMode:
        """Get current execution mode"""
        return self.mode

