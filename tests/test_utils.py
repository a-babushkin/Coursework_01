from datetime import datetime
from typing import Any
from unittest.mock import patch

import pytest

from src.utils import get_greeting, top_transactions_by_payment_amount, total_expenses_on_card


@patch("src.utils.datetime")
def test_get_greetings(mock_datetime: Any) -> None:
    mock_datetime.now.return_value.hour = 7
    assert get_greeting() == "Доброе утро"
    mock_datetime.now.return_value.hour = 15
    assert get_greeting() == "Добрый день"
    mock_datetime.now.return_value.hour = 20
    assert get_greeting() == "Добрый вечер"
    mock_datetime.now.return_value.hour = 1
    assert get_greeting() == "Доброй ночи"


@pytest.mark.parametrize(
    "start, finish,  result",
    [
        (
            datetime.strptime("2020-12-16 14:06:11", "%Y-%m-%d %H:%M:%S"),
            datetime.strptime("2020-12-18 14:06:11", "%Y-%m-%d %H:%M:%S"),
            ([{"last_digits": "7197", "total_spent": 15000.0, "cashback": 150.0}]),
        ),
        (
            datetime.strptime("2026-12-16 14:06:11", "%Y-%m-%d %H:%M:%S"),
            datetime.strptime("2026-12-18 14:06:11", "%Y-%m-%d %H:%M:%S"),
            [{}],
        ),
    ],
)
def test_total_expenses_on_card_ok_and_wrong(
    fixture_transaction: list[dict], start: datetime, finish: datetime, result: list[dict]
) -> None:
    """Тестирование затраты по карточке в указанный период"""
    assert total_expenses_on_card(fixture_transaction, start, finish) == result


@pytest.mark.parametrize(
    "start, finish,  result",
    [
        (
            datetime.strptime("2020-12-16 14:06:11", "%Y-%m-%d %H:%M:%S"),
            datetime.strptime("2020-12-18 14:06:11", "%Y-%m-%d %H:%M:%S"),
            (
                [
                    {
                        "date": "17.12.2020",
                        "amount": -15000.0,
                        "category": "Автоуслуги",
                        "description": "Kia Odisseya-Spb",
                    }
                ]
            ),
        ),
        (
            datetime.strptime("2026-12-16 14:06:11", "%Y-%m-%d %H:%M:%S"),
            datetime.strptime("2026-12-18 14:06:11", "%Y-%m-%d %H:%M:%S"),
            [{}],
        ),
    ],
)
def test_top_transactions_by_payment_amount_ok_and_wrong(
    fixture_transaction: list[dict], start: datetime, finish: datetime, result: list[dict]
) -> None:
    """Тестирование затраты по карточке в указанный период"""
    assert top_transactions_by_payment_amount(fixture_transaction, start, finish) == result
