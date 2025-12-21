"""
Claude API Client
Wrapper for Anthropic Claude API calls
支持全局單例模式，確保整個系統只有一個 client 實例
"""
from typing import Optional, Dict, Any, List
import threading
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


# ==================================================
# 全局單例 Client 管理器（新增）
# ==================================================

class APIClientManager:
    """
    全局 API Client 管理器（單例模式）
    
    確保整個系統只有一個 Anthropic client 實例
    支持線程安全，可在多線程環境中使用
    所有引擎（TCFD, Environment, Company, Governance, Carbon）共用同一個 client
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """單例模式實現"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(APIClientManager, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化（只執行一次）"""
        if self._initialized:
            return
        
        self._client: Optional[anthropic.Anthropic] = None
        self._api_key: Optional[str] = None
        self._api_version: str = "2023-06-01"
        self._initialized = True
    
    def initialize(self, api_key: str, api_version: str = "2023-06-01") -> None:
        """
        初始化 Client（只需要調用一次）
        
        Args:
            api_key: Anthropic API Key
            api_version: Anthropic API Version（可選）
        """
        if self._client is None or self._api_key != api_key:
            with self._lock:
                if self._client is None or self._api_key != api_key:
                    self._client = anthropic.Anthropic(
                        api_key=api_key,
                        default_headers={
                            "anthropic-version": api_version
                        }
                    )
                    self._api_key = api_key
                    self._api_version = api_version
    
    def get_client(self) -> anthropic.Anthropic:
        """
        獲取 Client 實例
        
        Returns:
            Anthropic client 實例
            
        Raises:
            RuntimeError: 如果 Client 尚未初始化
        """
        if self._client is None:
            raise RuntimeError(
                "API Client not initialized. Call initialize(api_key) first."
            )
        return self._client
    
    def is_initialized(self) -> bool:
        """檢查 Client 是否已初始化"""
        return self._client is not None
    
    def reset(self) -> None:
        """重置 Client（用於測試或重新初始化）"""
        with self._lock:
            self._client = None
            self._api_key = None
            self._api_version = "2023-06-01"


# 全局單例實例
_global_client_manager = APIClientManager()


def get_client_manager() -> APIClientManager:
    """
    獲取全局 Client 管理器實例
    
    Returns:
        全局 APIClientManager 實例
        
    使用範例:
        from shared.llm.claude_client import get_client_manager
        manager = get_client_manager()
    """
    return _global_client_manager


def initialize_client(api_key: str, api_version: str = "2023-06-01") -> None:
    """
    初始化全局 Client（便捷函數）
    
    Args:
        api_key: Anthropic API Key
        api_version: Anthropic API Version（可選）
        
    使用範例:
        from shared.llm.claude_client import initialize_client
        initialize_client("your-api-key")
    """
    _global_client_manager.initialize(api_key, api_version)


def get_client() -> anthropic.Anthropic:
    """
    獲取全局 Client 實例（便捷函數）
    
    Returns:
        Anthropic client 實例
        
    使用範例:
        from shared.llm.claude_client import get_client
        client = get_client()
        response = client.messages.create(...)
    """
    return _global_client_manager.get_client()


def call_claude_api(
    prompt: str,
    model: str = "claude-3-5-sonnet-20240620",
    max_tokens: int = 2000,
    system_prompt: Optional[str] = None
) -> str:
    """
    調用 Claude API（使用全局 Client）
    
    Args:
        prompt: 完整的 prompt
        model: Claude 模型名稱（可選）
        max_tokens: 最大 token 數（可選）
        system_prompt: 系統 prompt（可選）
    
    Returns:
        API 返回的文本內容
        
    Raises:
        RuntimeError: 如果 Client 尚未初始化
        
    使用範例:
        from shared.llm.claude_client import initialize_client, call_claude_api
        initialize_client("your-api-key")
        response = call_claude_api("Your prompt here")
    """
    client = get_client()
    
    # 備選模型列表（按優先順序）
    model_list = [
        model,  # 優先使用指定的模型
        "claude-3-5-sonnet-20240620",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]
    
    # 去重
    model_list = list(dict.fromkeys(model_list))
    
    # 準備 messages
    messages = [{"role": "user", "content": prompt}]
    
    # 嘗試每個模型，直到成功
    last_error = None
    for model_name in model_list:
        try:
            message = client.messages.create(
                model=model_name,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=messages
            )
            # 提取文本內容
            if message.content:
                text_content = ""
                for block in message.content:
                    if block.type == "text":
                        text_content += block.text
                return text_content
            else:
                return ""
        except Exception as e:
            last_error = e
            # 如果是模型不存在的錯誤，嘗試下一個模型
            if "not_found_error" in str(e) or "404" in str(e):
                continue
            # 其他錯誤直接拋出
            raise
    
    # 所有模型都失敗
    raise Exception(f"All models failed. Last error: {str(last_error)}")