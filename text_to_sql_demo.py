
import asyncio

from enterprise_data_agent.llm_client import (
    create_llm_client,
)
from enterprise_data_agent.text_to_sql import (
    generate_sql,
)


async def main():
    question = "查询每个地区的销售额，按销售额降序排列"

    client = create_llm_client()

    try:
        result = await generate_sql(client, question)

        print("\n原始问题：")
        print(result.query)

        print("\n是否能回答：")
        print(result.can_answer)

        print("\n生成的 SQL（未执行）：")
        print(result.sql)

        print("\n查询思路：")
        print(result.explanation)

        print("\n使用的表：")
        print(result.tables)

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
