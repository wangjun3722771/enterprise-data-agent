
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class SQLPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    can_answer: bool
    sql: str
    explanation: str = Field(min_length=1)
    tables: list[str]

    @model_validator(mode="after")
    def check_answer_consistency(self):
        if self.can_answer and not self.sql.strip():
            raise ValueError(
                "can_answer=True 时 SQL 不能为空"
            )

        if not self.can_answer and self.sql.strip():
            raise ValueError(
                "无法回答时 SQL 必须为空"
            )

        return self
