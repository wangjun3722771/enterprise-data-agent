
DATABASE_SCHEMA = """
数据库类型：SQLite

表 customers：
- id INTEGER PRIMARY KEY
- name TEXT
- region TEXT

表 products：
- id INTEGER PRIMARY KEY
- name TEXT
- price NUMERIC

表 orders：
- id INTEGER PRIMARY KEY
- customer_id INTEGER
- order_date DATE

表 order_items：
- id INTEGER PRIMARY KEY
- order_id INTEGER
- product_id INTEGER
- quantity INTEGER
- unit_price NUMERIC

外键关系：
- orders.customer_id -> customers.id
- order_items.order_id -> orders.id
- order_items.product_id -> products.id

业务规则：
- 销售额 = SUM(order_items.quantity * order_items.unit_price)
- 使用成交时单价 unit_price，而不是商品当前 price
- 不允许假设不存在的字段
"""


SYSTEM_PROMPT = """
你是一个企业经营数据分析 Text-to-SQL 助手。

根据用户的问题和数据库 Schema，
生成 SQLite 查询方案。

要求：
1. 只生成查询类 SQL。
2. 不要生成 INSERT、UPDATE、DELETE、DROP 等修改语句。
3. 只能使用数据库 Schema 中存在的表和字段。
4. 若用户问题无法从数据库中回答，应标记无法回答。
5. 不要虚构查询结果。
6. 必须返回合法 JSON 对象，不能输出 Markdown 代码块。

JSON 字段：
- query: 原始用户问题，字符串
- can_answer: 是否能够根据 Schema 回答，布尔值
- sql: SQL 字符串；无法回答时为空字符串
- explanation: 查询思路说明，字符串
- tables: 使用到的表名数组
"""


def build_messages(question: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": (
                f"数据库 Schema：\n{DATABASE_SCHEMA}\n\n"
                f"用户问题：\n{question}\n\n"
                "请生成 JSON 格式的 SQL 查询方案。"
            ),
        },
    ]
