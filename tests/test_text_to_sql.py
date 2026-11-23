
import json

import pytest

from enterprise_data_agent.text_to_sql import (
    parse_sql_plan,
)


def make_valid_data():
    return {
        "query": "查询各地区销售额",
        "can_answer": True,
        "sql": "SELECT region FROM customers",
        "explanation": "根据客户地区进行查询",
        "tables": ["customers"],
    }


def test_valid_sql_plan():
    content = json.dumps(make_valid_data())

    result = parse_sql_plan(content)

    assert result.can_answer is True
    assert result.tables == ["customers"]
    assert result.sql.startswith("SELECT")


def test_missing_field():
    data = make_valid_data()
    del data["sql"]

    with pytest.raises(ValueError):
        parse_sql_plan(json.dumps(data))


def test_invalid_json():
    with pytest.raises(ValueError):
        parse_sql_plan("这不是合法 JSON")


def test_empty_content():
    with pytest.raises(ValueError):
        parse_sql_plan("")


def test_inconsistent_answer():
    data = make_valid_data()
    data["can_answer"] = False

    with pytest.raises(ValueError):
        parse_sql_plan(json.dumps(data))


def test_unanswerable_question():
    data = {
        "query": "查询公司员工薪资",
        "can_answer": False,
        "sql": "",
        "explanation": "数据库没有员工薪资表",
        "tables": [],
    }

    result = parse_sql_plan(json.dumps(data))

    assert result.can_answer is False
    assert result.sql == ""
