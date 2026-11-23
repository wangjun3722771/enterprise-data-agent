
import asyncio
import os

from dotenv import load_dotenv

from enterprise_data_agent.llm_client import (
    create_llm_client,
)


async def main():
    load_dotenv()
    client = create_llm_client()

    try:
        response = await client.chat.completions.create(
            model=os.environ["LLM_MODEL"],
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的企业数据分析助手。",
                },
                {
                    "role": "user",
                    "content": "用一句话解释什么是 SQL GROUP BY。",
                },
            ],
            stream=False,
        )

        print("模型回复：")
        print(response.choices[0].message.content)

        if response.usage:
            print("Token 用量：", response.usage.total_tokens)

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
