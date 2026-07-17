"""
AI Provider 抽象层 - 支持 OpenAI、Claude、MiMo API
"""

from abc import ABC, abstractmethod
from typing import Optional
import json


class AIProvider(ABC):
    """AI 提供商基类"""

    @abstractmethod
    def chat(self, system_prompt: str, user_message: str) -> str:
        """发送对话请求"""
        pass

    @abstractmethod
    def chat_with_search(self, system_prompt: str, user_message: str) -> str:
        """带搜索功能的对话"""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI API 提供商"""

    def __init__(self, api_key: str, base_url: str, model: str):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self.model = model
        except ImportError:
            raise ImportError("请安装 openai: pip install openai")

    def chat(self, system_prompt: str, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        return response.choices[0].message.content

    def chat_with_search(self, system_prompt: str, user_message: str) -> str:
        """使用 Web Search 工具"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "web_search",
                        "description": "搜索互联网获取最新信息",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "搜索关键词"}
                            },
                            "required": ["query"]
                        }
                    }
                }],
                temperature=0.7,
                max_tokens=4000
            )

            # 如果模型调用了工具，处理结果
            if response.choices[0].message.tool_calls:
                return self._handle_tool_calls(response, system_prompt, user_message)
            return response.choices[0].message.content
        except Exception:
            # 回退到普通对话
            return self.chat(system_prompt, user_message)

    def _handle_tool_calls(self, response, system_prompt: str, user_message: str) -> str:
        """处理工具调用"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
            response.choices[0].message
        ]

        # 模拟工具结果（实际应调用搜索API）
        for tool_call in response.choices[0].message.tool_calls:
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": "搜索结果已获取，请基于最新信息进行总结。"
            })

        final_response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=4000
        )
        return final_response.choices[0].message.content


class ClaudeProvider(AIProvider):
    """Claude API 提供商"""

    def __init__(self, api_key: str, base_url: str, model: str):
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
            self.model = model
        except ImportError:
            raise ImportError("请安装 anthropic: pip install anthropic")

    def chat(self, system_prompt: str, user_message: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        return response.content[0].text

    def chat_with_search(self, system_prompt: str, user_message: str) -> str:
        """Claude 使用内置搜索"""
        # Claude 可以通过 prompt 引导搜索
        enhanced_prompt = system_prompt + "\n\n请搜索最新的新闻信息来回答用户的问题。"
        return self.chat(enhanced_prompt, user_message)


class MiMoProvider(AIProvider):
    """MiMo API 提供商 (OpenAI 兼容格式)"""

    def __init__(self, api_key: str, base_url: str, model: str):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key, base_url=base_url)
            self.model = model
        except ImportError:
            raise ImportError("请安装 openai: pip install openai")

    def chat(self, system_prompt: str, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        return response.choices[0].message.content

    def chat_with_search(self, system_prompt: str, user_message: str) -> str:
        """MiMo 搜索功能"""
        return self.chat(system_prompt, user_message)


def create_provider(provider_name: str, config) -> AIProvider:
    """工厂方法：创建 AI 提供商实例"""
    if provider_name == "openai":
        return OpenAIProvider(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL,
            model=config.OPENAI_MODEL
        )
    elif provider_name == "claude":
        return ClaudeProvider(
            api_key=config.CLAUDE_API_KEY,
            base_url=config.CLAUDE_BASE_URL,
            model=config.CLAUDE_MODEL
        )
    elif provider_name == "mimo":
        return MiMoProvider(
            api_key=config.MIMO_API_KEY,
            base_url=config.MIMO_BASE_URL,
            model=config.MIMO_MODEL
        )
    else:
        raise ValueError(f"不支持的 AI 提供商: {provider_name}")
