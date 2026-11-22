import pytest

from enterprise_data_agent.calculator import calculate_total


def test_normal_order():
    result = calculate_total(10.5, 3)
    assert result == 31.5


def test_zero_quantity():
    assert calculate_total(10, 0) == 0


def test_negative_price():
    with pytest.raises(ValueError):
        calculate_total(-10, 2)


def test_negative_quantity():
    with pytest.raises(ValueError):
        calculate_total(10, -1)


def test_decimal_price():
    assert calculate_total(19.9, 3) == 59.7
