
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from enterprise_data_agent.calculator import calculate_total
from enterprise_data_agent.schemas import (
    DiscountRequest,
    DiscountResponse,
    OrderRequest,
    OrderResponse,
)

app = FastAPI(
    title="Enterprise Data Agent API",
    description="企业数据分析 Agent 后端服务",
    version="0.1.0",
)


# 暂时使用模拟商品数据
PRODUCTS = {
    1001: {"name": "机械键盘", "price": 299.0},
    1002: {"name": "无线鼠标", "price": 99.0},
    1003: {"name": "显示器", "price": 1299.0},
}


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float


# 接口 1：健康检查
@app.get("/health")
def health():
    return {"status": "ok"}


# 接口 2：查询商品
@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    product = PRODUCTS.get(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="商品不存在",
        )

    return ProductResponse(
        id=product_id,
        **product,
    )


# 接口 3：计算订单金额
@app.post("/orders/calculate", response_model=OrderResponse)
def calculate_order(order: OrderRequest):
    total = calculate_total(
        price=order.price,
        quantity=order.quantity,
    )

    return OrderResponse(
        product_name=order.product_name,
        price=order.price,
        quantity=order.quantity,
        total=total,
    )

@app.post("/orders/discount", response_model=DiscountResponse)
def calculate_discount(order: DiscountRequest):
    original_total = calculate_total(
        price=order.price,
        quantity=order.quantity,
    )
    
    final_total = original_total * order.discount
    
    saved = original_total - final_total

    return DiscountResponse(
        original_total=original_total,
        final_total=final_total,
        saved=saved,
    )


from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from enterprise_data_agent.analytics import get_revenue_by_region
from enterprise_data_agent.database import get_db


@app.get("/analytics/revenue-by-region")
def revenue_by_region(
    session: Annotated[Session, Depends(get_db)],
):
    return get_revenue_by_region(session)
