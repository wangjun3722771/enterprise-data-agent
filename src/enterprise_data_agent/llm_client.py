
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI


def create_llm_client() -> AsyncOpenAI:
    """根据环境变量创建异步 LLM 客户端。"""

    load_dotenv()

    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")

    if not api_key:
        raise ValueError("未配置 LLM_API_KEY")

    if not base_url:
        raise ValueError("未配置 LLM_BASE_URL")

    return AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=30.0,
        max_retries=1,
    )
