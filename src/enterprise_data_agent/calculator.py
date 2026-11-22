def calculate_total(price: float, quantity: int) -> float:
    """计算订单总金额。"""

    if price < 0:
        raise ValueError("商品价格不能为负数")

    if quantity < 0:
        raise ValueError("购买数量不能为负数")

    return round(price * quantity, 2)
