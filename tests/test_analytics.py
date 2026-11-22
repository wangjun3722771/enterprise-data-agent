
from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from enterprise_data_agent.analytics import get_revenue_by_region
from enterprise_data_agent.database import Base
from enterprise_data_agent.models import (
    Customer,
    Order,
    OrderItem,
)


def test_revenue_by_region():
    # 独立的测试数据库，不影响 sales.db
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=test_engine)

    try:
        with Session(test_engine) as session:
            session.add_all([
                Customer(id=1, name="测试客户A", region="华东"),
                Customer(id=2, name="测试客户B", region="华北"),
                Order(
                    id=1,
                    customer_id=1,
                    order_date=date(2026, 11, 1),
                ),
                Order(
                    id=2,
                    customer_id=2,
                    order_date=date(2026, 11, 2),
                ),
                OrderItem(
                    id=1,
                    order_id=1,
                    product_id=1001,
                    quantity=2,
                    unit_price=Decimal("100.00"),
                ),
                OrderItem(
                    id=2,
                    order_id=2,
                    product_id=1002,
                    quantity=3,
                    unit_price=Decimal("50.00"),
                ),
            ])

            session.commit()

            result = get_revenue_by_region(session)

            assert result == [
                {"region": "华东", "revenue": 200.0},
                {"region": "华北", "revenue": 150.0},
            ]
    finally:
        test_engine.dispose()
