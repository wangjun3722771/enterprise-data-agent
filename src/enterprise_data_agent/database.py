
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 数据库存储位置
DB_PATH = PROJECT_ROOT / "data" / "sales.db"

# SQLite 数据库连接
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"


# ORM 模型的基类
class Base(DeclarativeBase):
    pass


# 创建数据库 Engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
)


# Session 工厂
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


from collections.abc import Generator

from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    """为每个 API 请求创建一个数据库 Session。"""
    with SessionLocal() as session:
        yield session
