import json

import pytest

from src.services import main_services_function


@pytest.mark.parametrize(
    "transactions, search_str,  result",
    [
        (
                [
                    {"Категория": "Продукты", "Описание": "Покупка яблок"},
                    {"Категория": "Билеты", "Описание": "Билет на концерт"},
                    {"Категория": "Развлечения", "Описание": "Поход в кино"},
                    {"Категория": "Транспорт", "Описание": "Бензин для машины"},
                ],
                "билет",
                [{"Категория": "Билеты", "Описание": "Билет на концерт"}],
        ),
        (
                [
                    {"Категория": "Продукты", "Описание": "Покупка яблок"},
                    {"Категория": "Билеты", "Описание": "Билет на концерт"},
                    {"Категория": "Развлечения", "Описание": "Поход в кино"},
                    {"Категория": "Транспорт", "Описание": "Бензин для машины"},
                ],
                "Неизвестный продукт",
                [{}],
        ),
        (
                [
                    {},
                ],
                "Тест",
                [{}],
        ),
    ],
)
def test_main_services_function_found(transactions: list[dict], search_str: str, result: list[dict]) -> None:
    func_result = main_services_function(transactions, search_str)
    assert func_result == json.dumps(result, ensure_ascii=False)
