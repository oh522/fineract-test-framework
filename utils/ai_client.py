"""
mimo-v2.5-pro AI 客户端封装
统一管理 AI 调用，供 ai_case_gen.py 和其他模块使用
"""
import os
import time
import logging
import yaml
from pathlib import Path
from openai import OpenAI, APIError, APITimeoutError, RateLimitError

logger = logging.getLogger(__name__)


class MimoClient:
    """
    mimo-v2.5-pro 客户端
    - 从 config.yaml 读取配置
    - 支持重试（限流时自动等待）
    - 统一异常处理
    - 支持代理配置
    """

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parents[1] / "config" / "config.yaml"

        with open(config_path, encoding="utf-8") as f:
            full_cfg = yaml.safe_load(f)

        env = os.environ.get("TEST_ENV", full_cfg.get("env", "test"))
        cfg = full_cfg[env]["ai"]

        # 优先读环境变量，其次读配置文件
        api_key = os.environ.get("MIMO_API_KEY") or cfg["api_key"]

        self._model = cfg["model"]
        self._max_tokens = cfg["max_tokens"]
        self._temperature = cfg["temperature"]
        self._timeout = cfg["timeout"]
        self._base_url = cfg["base_url"]

        # 支持代理配置（按优先级检查多个环境变量）
        proxy_url = (
            os.environ.get("HTTP_PROXY") or 
            os.environ.get("http_proxy") or 
            os.environ.get("HTTPS_PROXY") or 
            os.environ.get("https_proxy")
        )
        
        if proxy_url:
            logger.info(f"🔧 检测到代理配置：{proxy_url}")
            try:
                import httpx
                transport = httpx.HTTPTransport(proxy=proxy_url)
                self._client = OpenAI(
                    api_key=api_key,
                    base_url=self._base_url,
                    timeout=float(self._timeout),
                    http_client=httpx.Client(transport=transport),
                )
                logger.info("✅ 已启用代理连接")
            except ImportError:
                logger.warning("⚠️ 未安装 httpx，代理可能无法使用。请执行：pip install httpx")
                self._client = OpenAI(
                    api_key=api_key,
                    base_url=self._base_url,
                    timeout=float(self._timeout),
                )
        else:
            self._client = OpenAI(
                api_key=api_key,
                base_url=self._base_url,
                timeout=float(self._timeout),
            )

        logger.info(f"✅ MimoClient 初始化完成 model={self._model}, base_url={self._base_url}")

    def chat(
        self,
        user_prompt: str,
        system_prompt: str = "你是专业的接口测试工程师，只输出纯 Python 代码。",
        max_tokens: int = None,
        temperature: float = None,
        max_retries: int = 3,
    ) -> str:
        """
        发送对话请求，返回文本内容
        自动重试：限流时等待后重试，超时时快速重试
        """
        max_tokens = max_tokens or self._max_tokens
        temperature = temperature or self._temperature

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"→ AI 请求 第{attempt}次 model={self._model}")

                response = self._client.chat.completions.create(
                    model=self._model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user",   "content": user_prompt},
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                )

                content = response.choices[0].message.content
                usage = response.usage
                logger.info(
                    f"← AI 响应成功 "
                    f"prompt_tokens={usage.prompt_tokens} "
                    f"completion_tokens={usage.completion_tokens}"
                )
                return content

            except RateLimitError as e:
                wait = 2 ** attempt
                logger.warning(f"  限流，等待 {wait}s 后重试：{e}")
                time.sleep(wait)
                last_error = e

            except APITimeoutError as e:
                logger.warning(f"  超时，第{attempt}次重试：{e}")
                time.sleep(1)
                last_error = e

            except APIError as e:
                error_type = type(e).__name__
                logger.error(f"  API 错误 {error_type}（不重试）：{e}")
                raise

            except Exception as e:
                error_type = type(e).__name__
                logger.error(f"  未知错误 {error_type}，第{attempt}次重试：{e}")
                logger.error(f"  Base URL: {self._base_url}")
                logger.error(f"  Model: {self._model}")
                time.sleep(2)
                last_error = e

        raise RuntimeError(f"AI 请求失败，已重试 {max_retries} 次。最后错误：{type(last_error).__name__}: {last_error}")

    def chat_json(
        self,
        user_prompt: str,
        system_prompt: str = "只输出 JSON，不含任何 markdown 标记。",
        **kwargs,
    ) -> dict:
        """
        发送请求并解析 JSON 响应
        适用于需要结构化输出的场景
        """
        import json
        import re

        raw = self.chat(user_prompt, system_prompt, **kwargs)

        # 清理 markdown 代码块
        raw = re.sub(r"\s*",     "", raw)
        raw = raw.strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败：{e}\n原始内容：{raw[:200]}")
            raise

    def test_connection(self) -> bool:
        """测试 API 连通性"""
        try:
            print(f"🔍 正在测试 AI API 连通性...")
            print(f"   Base URL: {self._base_url}")
            print(f"   Model: {self._model}")

            result = self.chat(
                user_prompt="回复数字 1",
                system_prompt="只回复数字",
                max_tokens=10,
            )
            print(f"✅ 连通性测试通过，响应：{result}")
            return True
        except Exception as e:
            print(f"❌ 连通性测试失败：{type(e).__name__}: {e}")
            return False


# 单例，全局复用
_client_instance: MimoClient = None


def get_mimo_client() -> MimoClient:
    """获取全局单例客户端"""
    global _client_instance
    if _client_instance is None:
        _client_instance = MimoClient()
    return _client_instance
