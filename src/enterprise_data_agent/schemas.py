
from pydantic import BaseModel, ConfigDict, Field


class OrderRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product_name: str = Field(min_length=1)
    price: float = Field(ge=0)
    quantity: int = Field(gt=0)


class OrderResponse(BaseModel):
    product_name: str
    price: float
    quantity: int
    total: float

class DiscountRequest(BaseModel):
    price: float = Field(ge=0)
    quantity: int = Field(gt=0)
    discount: float = Field(ge=0, le=1)


class DiscountResponse(BaseModel):
    original_total: float
    final_total: float
    saved: float