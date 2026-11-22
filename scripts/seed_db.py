
from datetime import date
from decimal import Decimal

from sqlalchemy import select

from enterprise_data_agent.database import (
    Base,
    SessionLocal,
    engine,
)
from enterprise_data_agent.models import (
    Customer,
    Order,
    OrderItem,
    Product,
)


def seed_database():
    # 确保四张表的模型已导入
    Base.metadata.create_all(bind=engine)

    with SessionLocal.begin() as session:
        # 防止重复插入
        existing = session.scalar(select(Customer.id).limit(1))
        if existing is not None:
            print("数据库已有客户数据，跳过初始化")
            return

        session.add_all([
            Customer(id=1, name="客户A", region="华东"),
            Customer(id=2, name="客户B", region="华北"),
            Customer(id=3, name="客户C", region="华南"),
        ])

        session.add_all([
            Product(
                id=1001,
                name="机械键盘",
                price=Decimal("299.00"),
            ),
            Product(
                id=1002,
                name="无线鼠标",
                price=Decimal("99.00"),
            ),
            Product(
                id=1003,
                name="显示器",
                price=Decimal("1299.00"),
            ),
        ])

        session.add_all([
            Order(id=1, customer_id=1,
                  order_date=date(2026, 11, 1)),
            Order(id=2, customer_id=2,
                  order_date=date(2026, 11, 2)),
            Order(id=3, customer_id=3,
                  order_date=date(2026, 11, 3)),
        ])

        session.add_all([
            OrderItem(
                id=1,
                order_id=1,
                product_id=1001,
                quantity=4,
                unit_price=Decimal("299.00"),
            ),
            OrderItem(
                id=2,
                order_id=2,
                product_id=1001,
                quantity=2,
                unit_price=Decimal("299.00"),
            ),
            OrderItem(
                id=3,
                order_id=3,
                product_id=1002,
                quantity=3,
                unit_price=Decimal("99.00"),
            ),
        ])

    print("数据库初始化成功")


if __name__ == "__main__":
    seed_database()
