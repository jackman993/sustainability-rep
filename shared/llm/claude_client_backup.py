"""
Claude API Client
Wrapper for Anthropic Claude API calls
"""
from typing import Optional, Dict, Any, List
import anthropic
from shared.mode_manager import ModeManager


class ClaudeClient:
    """Claude API client wrapper"""
    
    def __init__(self, mode_manager: ModeManager):
        """
        Initialize Claude client
        
        Args:
            mode_manager: ModeManager instance for API key and configuration
        """
        self.mode_manager = mode_manager
        self.api_key = mode_manager.get_api_key()
        self.api_version = mode_manager.get_claude_api_version()
        self.model = mode_manager.get_claude_model()
        
        if not self.api_key:
            raise ValueError("Claude API key is required. Please set it in the sidebar or environment variable.")
        
        # Initialize Anthropic client with API version in default headers
        self.client = anthropic.Anthropic(
            api_key=self.api_key,
            default_headers={
                "anthropic-version": self.api_version
            }
        )
    
    def generate_message(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        model: Optional[str] = None
    ) -> str:
        """
        Generate a message using Claude API
        
        Args:
            prompt: User prompt/message
            system_prompt: System prompt (optional)
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation (0.0-1.0)
            model: Model to use (overrides default)
        
        Returns:
            Generated text response
        """
        model = model or self.model
        
        # Prepare messages
        messages = [{"role": "user", "content": prompt}]
        
        # Prepare system message if provided
        system_message = system_prompt if system_prompt else None
        
        try:
            # Call Claude API (API version is set in client initialization)
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message,
                messages=messages
            )
            
            # Extract text content
            if response.content:
                # Claude returns a list of content blocks
                text_content = ""
                for block in response.content:
                    if block.type == "text":
                        text_content += block.text
                return text_content
            else:
                return ""
                
        except anthropic.APIError as e:
            raise ValueError(f"Claude API error: {e.message}")
        except Exception as e:
            raise ValueError(f"Error calling Claude API: {str(e)}")
    
    def generate_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate structured JSON response
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            response_format: JSON schema for structured output
            max_tokens: Maximum tokens
            temperature: Temperature
        
        Returns:
            Parsed JSON response
        """
        import json
        
        # Add JSON format instruction to system prompt
        if system_prompt:
            enhanced_system = f"{system_prompt}\n\nRespond in valid JSON format."
        else:
            enhanced_system = "Respond in valid JSON format."
        
        if response_format:
            enhanced_system += f"\n\nRequired JSON schema: {json.dumps(response_format, indent=2)}"
        
        response_text = self.generate_message(
            prompt=prompt,
            system_prompt=enhanced_system,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        # Parse JSON response
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            # Try to find JSON object directly
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            raise ValueError(f"Failed to parse JSON from response: {response_text[:200]}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model configuration"""
        return {
            "model": self.model,
            "api_version": self.api_version,
            "api_key_set": bool(self.api_key),
            "api_key_preview": f"{self.api_key[:8]}..." if self.api_key else None
        }


