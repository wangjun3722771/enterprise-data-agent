
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from enterprise_data_agent.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    region: Mapped[str] = mapped_column(String(50))


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id")
    )

    order_date: Mapped[date] = mapped_column(Date)


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    quantity: Mapped[int] = mapped_column()

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )
