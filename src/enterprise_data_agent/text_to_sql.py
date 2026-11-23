
import os

from openai import AsyncOpenAI
from pydantic import ValidationError

from enterprise_data_agent.prompts import build_messages
from enterprise_data_agent.sql_schema import SQLPlan


def parse_sql_plan(content: str) -> SQLPlan:
    """将模型返回的 JSON 转换为 SQLPlan。"""

    if not content.strip():
        raise ValueError("模型返回了空内容")

    try:
        return SQLPlan.model_validate_json(content)

    except ValidationError as exc:
        raise ValueError(
            "模型输出未通过 SQLPlan 校验"
        ) from exc


async def generate_sql(
    client: AsyncOpenAI,
    question: str,
) -> SQLPlan:
    """根据用户问题生成结构化 SQL 查询方案。"""

    question = question.strip()

    if not question:
        raise ValueError("用户问题不能为空")

    model = os.getenv("LLM_MODEL", "deepseek-chat")

    response = await client.chat.completions.create(
        model=model,
        messages=build_messages(question),
        response_format={"type": "json_object"},
        stream=False,
    )

    if not response.choices:
        raise ValueError("模型没有返回候选结果")

    choice = response.choices[0]

    if choice.finish_reason == "length":
        raise ValueError(
            "模型输出被截断，请调整输出 Token 上限"
        )

    if choice.finish_reason != "stop":
        raise ValueError(
            f"模型未正常结束：{choice.finish_reason}"
        )

    content = choice.message.content

    if content is None:
        raise ValueError("模型没有返回文本内容")

    result = parse_sql_plan(content)

    if result.query != question:
        raise ValueError("模型返回的 query 与原始问题不一致")

    return result
