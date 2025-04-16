import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv

logger = logging.getLogger("external_api")
file_handler = logging.FileHandler(
    "C:/Users/owner/PycharmProjects/Coursework_01/logs/external_api.log", encoding="UTF-8"
)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def find_value(d: dict[str, Any], key: str) -> Any | None:
    """Рекурсивная функция ищет значение по ключу во вложенном словаре с
    переменной степенью вложенности и изменяемыми ключами"""
    if key in d:
        return d[key]

    for k, v in d.items():
        if isinstance(v, dict):
            result = find_value(v, key)
            if result is not None:
                return result

    return None


def get_exchange_curse_currency(currencies: list[str], base: str) -> list[dict]:
    """Получение текущих курсов валюты с помощью внешнего API"""
    load_dotenv()
    exchange_curse = []
    api_token = os.getenv("API_LAYER_KEY")
    url = os.getenv("CURSE_CURRENCY_URL")
    for currency in currencies:
        payload = {"from": currency, "to": base, "amount": 1}
        headers = {"apikey": api_token}
        response = requests.get(str(url), headers=headers, params=str(payload))
        if response.status_code == 200:
            exchange_curse.append({"currency": currency, "rate": round(response.json()["result"], 2)})
    if exchange_curse:
        logger.info(f"Функция сработала штатно, получены данные: {exchange_curse}")
        return exchange_curse
    else:
        logger.error("Произошла ошибка при обращении ко внешнему API")
        return [{}]


def get_stock_prices(stocks: list[str]) -> list[dict]:
    """Получение текущих стоимостей акций с помощью внешнего API"""
    load_dotenv()
    stock_list = []
    api_token = os.getenv("ALPHA_VANTAGE_API_KEY")
    url = os.getenv("STOCK_PRICE_URL")
    for symbol in stocks:
        response = requests.get(
            f"{url}?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=60min&apikey={api_token}"
        )
        price_value = find_value(response.json(), "4. close")
        if price_value:
            stock_list.append({"stock": symbol, "price": price_value})
    if stock_list:
        logger.info(f"Функция сработала штатно, получены данные: {stock_list}")
        return stock_list
    else:
        logger.error("По указанным параметрам нет возвращаемых данных")
        return [{}]
