import json
import unittest
from typing import Any
from unittest.mock import patch

from src.services import main_services_function


class TestMainServicesFunction(unittest.TestCase):

    @patch("src.services.get_transaction_from_excel_file")
    def test_main_services_function_found(self, mock_get_transactions: Any) -> None:
        # Подготовим тестовые данные
        mock_get_transactions.return_value = [
            {"Категория": "Продукты", "Описание": "Покупка яблок"},
            {"Категория": "Билеты", "Описание": "Билет на концерт"},
            {"Категория": "Развлечения", "Описание": "Поход в кино"},
            {"Категория": "Транспорт", "Описание": "Бензин для машины"},
        ]

        search_str = "билет"
        expected_output = [{"Категория": "Билеты", "Описание": "Билет на концерт"}]

        # Выполним функцию
        result = main_services_function(search_str)

        # Проверим, что результат соответствует ожиданиям
        self.assertEqual(result, json.dumps(expected_output, ensure_ascii=False))

    @patch("src.services.get_transaction_from_excel_file")
    def test_main_services_function_not_found(self, mock_get_transactions: Any) -> None:
        # Подготовим тестовые данные
        mock_get_transactions.return_value = [
            {"Категория": "Продукты", "Описание": "Покупка яблок"},
            {"Категория": "Билеты", "Описание": "Билет на концерт"},
            {"Категория": "Развлечения", "Описание": "Поход в кино"},
            {"Категория": "Транспорт", "Описание": "Бензин для машины"},
        ]

        search_str = "Неизвестный продукт"
        expected_output: list[dict] = [{}]

        # Выполним функцию
        result = main_services_function(search_str)

        # Проверим, что результат соответствует ожиданиям
        self.assertEqual(result, expected_output)

    @patch("src.services.get_transaction_from_excel_file")
    def test_main_services_function_empty_input(self, mock_get_transactions: Any) -> None:
        # Подготовим тестовые данные
        mock_get_transactions.return_value = []

        search_str = "Тест"
        expected_output: list[dict] = [{}]

        # Выполним функцию
        result = main_services_function(search_str)

        # Проверим, что результат соответствует ожиданиям
        self.assertEqual(result, expected_output)
