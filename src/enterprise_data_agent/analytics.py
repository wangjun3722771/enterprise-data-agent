
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from enterprise_data_agent.models import (
    Customer,
    Order,
    OrderItem,
)


def get_revenue_by_region(session: Session) -> list[dict]:
    # 计算地区销售额
    revenue = func.sum(
        OrderItem.quantity * OrderItem.unit_price
    ).label("revenue")

    stmt = (
        select(Customer.region, revenue)
        .join(
            Order,
            Order.customer_id == Customer.id,
        )
        .join(
            OrderItem,
            OrderItem.order_id == Order.id,
        )
        .group_by(Customer.region)
        .order_by(revenue.desc())
    )

    rows = session.execute(stmt).all()

    return [
        {
            "region": row.region,
            "revenue": float(row.revenue),
        }
        for row in rows
    ]
