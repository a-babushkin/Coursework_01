from typing import Any
from unittest.mock import patch

import pytest

from src.external_api import find_value, get_exchange_curse_currency, get_stock_prices


@pytest.mark.parametrize("search_key, result", [("e", 213.60), ("r", None)])
def test_find_value_ok(fixture_dict: dict, search_key: str, result: float) -> None:
    """Тестирование поиска значения по ключу"""
    assert find_value(fixture_dict, search_key) == result


@patch("requests.get")
def test_get_exchange_curse_currency_ok(mock_get: Any) -> None:
    """Тестирование функции конвертирования валюты корректный ответ"""
    mock_get.return_value.status_code = 200
    # result = {'USD': 0.011906, 'EUR': 0.01096}
    mock_get.return_value.json.return_value = {"result": 83.601157}
    assert get_exchange_curse_currency(["USD"], "RUB") == [{"currency": "USD", "rate": 83.60}]


@patch("requests.get")
def test_get_exchange_curse_currency_wrong(mock_get: Any) -> None:
    """Тестирование функции конвертирования валюты не корректный ответ"""
    mock_get.return_value.status_code = 500
    mock_get.return_value.json.return_value = {"result": 83.601157}
    assert get_exchange_curse_currency(["USD", "EUR"], "RUB") == [{}]


@patch("src.external_api.find_value")
@patch("requests.get")
def test_get_stock_prices_ok(mock_get: Any, mock_find_value: Any) -> None:
    """Тестирование функции получения стоимостей акций"""
    mock_find_value.return_value = 213.60
    mock_get.return_value.json.return_value = {"4. close": 213.60}
    assert get_stock_prices(["MSFT"]) == [{"stock": "MSFT", "price": 213.60}]


@patch("src.external_api.find_value")
@patch("requests.get")
def test_get_stock_prices_wrong(mock_get: Any, mock_find_value: Any) -> None:
    """Тестирование функции получения стоимостей акций"""
    mock_find_value.return_value = None
    mock_get.return_value.json.return_value = {"5. open": 213.60}
    assert get_stock_prices(["MSFT"]) == [{}]
