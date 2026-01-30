"""
模型交互模块

支持与多种LLM API交互（DeepSeek、OpenAI、Anthropic等）
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import requests
import json
from dataclasses import dataclass


@dataclass
class ModelResponse:
    """模型响应"""
    content: str
    model: str
    tokens_used: int
    stop_reason: str


class LLMClient(ABC):
    """LLM客户端基类"""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> ModelResponse:
        """生成文本"""
        pass


class DeepSeekClient(LLMClient):
    """DeepSeek API客户端"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.deepseek.com/chat/completions"
    
    def generate(self, prompt: str, system_prompt: str = "", 
                temperature: float = 0.7, max_tokens: int = 2000, **kwargs) -> ModelResponse:
        """使用DeepSeek API生成文本"""
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 0.95,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return ModelResponse(
                content=result['choices'][0]['message']['content'],
                model=self.model,
                tokens_used=result.get('usage', {}).get('total_tokens', 0),
                stop_reason=result['choices'][0].get('finish_reason', 'stop')
            )
        except Exception as e:
            print(f"DeepSeek API Error: {e}")
            # 返回模拟响应用于测试
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> ModelResponse:
        """模拟响应（用于测试或API不可用时）"""
        return ModelResponse(
            content="这是一个测试响应。实际使用时请配置正确的API密钥。",
            model=self.model,
            tokens_used=100,
            stop_reason="mock"
        )


class OpenAIClient(LLMClient):
    """OpenAI API客户端"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    def generate(self, prompt: str, system_prompt: str = "",
                temperature: float = 0.7, max_tokens: int = 2000, **kwargs) -> ModelResponse:
        """使用OpenAI API生成文本"""
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return ModelResponse(
                content=result['choices'][0]['message']['content'],
                model=self.model,
                tokens_used=result.get('usage', {}).get('total_tokens', 0),
                stop_reason=result['choices'][0].get('finish_reason', 'stop')
            )
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> ModelResponse:
        """模拟响应"""
        return ModelResponse(
            content="这是一个测试响应。实际使用时请配置正确的API密钥。",
            model=self.model,
            tokens_used=100,
            stop_reason="mock"
        )


class LocalModelClient(LLMClient):
    """本地模型客户端"""
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        # 可集成 ollama、vllm 等本地推理框架
    
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> ModelResponse:
        """使用本地模型生成文本"""
        # 实现本地模型推理逻辑
        return ModelResponse(
            content="本地模型响应（需要配置推理框架）",
            model="local",
            tokens_used=0,
            stop_reason="local"
        )


class ModelFactory:
    """模型客户端工厂"""
    
    @staticmethod
    def create_client(provider: str, **kwargs) -> LLMClient:
        """创建指定提供商的客户端"""
        
        if provider.lower() == "deepseek":
            return DeepSeekClient(
                api_key=kwargs.get('api_key'),
                model=kwargs.get('model', 'deepseek-chat')
            )
        elif provider.lower() == "openai":
            return OpenAIClient(
                api_key=kwargs.get('api_key'),
                model=kwargs.get('model', 'gpt-4')
            )
        elif provider.lower() == "local":
            return LocalModelClient(
                model_path=kwargs.get('model_path')
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")


class DialogueGenerator:
    """对话生成器"""
    
    def __init__(self, generator_client: LLMClient):
        self.client = generator_client
    
    def generate_response(self, user_input: str, system_prompt: str = "",
                         temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """生成对话回答"""
        
        response = self.client.generate(
            prompt=user_input,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.content


if __name__ == "__main__":
    # 测试模型客户端
    
    # 模拟生成客户端
    generator = ModelFactory.create_client("deepseek", api_key="test_key")
    response = generator.generate(
        prompt="今天天气怎么样？",
        system_prompt="你是一个有帮助的助手。"
    )
    print(f"Response: {response.content}")
    print(f"Tokens: {response.tokens_used}")
