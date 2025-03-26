import json
import unittest
from typing import Any
from unittest.mock import patch

from src.views import main_view_function


class TestMainViewFunction(unittest.TestCase):

    @patch("src.external_api.get_exchange_curse_currency")
    @patch("src.external_api.get_stock_prices")
    @patch("src.files_reader.get_transaction_from_excel_file")
    @patch("src.files_reader.read_json_file")
    @patch("src.utils.get_greeting")
    @patch("src.utils.total_expenses_on_card")
    @patch("src.utils.top_transactions_by_payment_amount")
    def test_main_view_function(
        self,
        mock_top_transactions: Any,
        mock_total_expenses: Any,
        mock_get_greeting: Any,
        mock_read_json_file: Any,
        mock_get_transaction_from_excel_file: Any,
        mock_get_stock_prices: Any,
        mock_get_exchange_curse_currency: Any,
    ) -> None:
        # Настройка подмены возвращаемых значений
        check_date = "2021-10-16 12:01:00"
        mock_get_transaction_from_excel_file.return_value = [
            {
                "Дата платежа": "31.12.2021",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма платежа": -160.89,
                "Валюта платежа": "RUB",
                "Категория": "Супермаркеты",
                "Описание": "Колхоз",
            },
            {
                "Дата платежа": "31.12.2021",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма операции": -64.0,
                "Валюта платежа": "RUB",
                "Категория": "Супермаркеты",
                "Описание": "Колхоз",
            },
        ]
        mock_read_json_file.side_effect = [["USD", "EUR"], ["AAPL"]]  # user_currencies  # user_stocks
        mock_get_greeting.return_value = "Добрый день"
        mock_total_expenses.return_value = [{"last_digits": "7197", "total_spent": 224.89, "cashback": 2.25}]
        mock_top_transactions.return_value = [
            {"date": "31.12.2021", "amount": -160.89, "category": "Супермаркеты", "description": "Колхоз"},
            {"date": "31.12.2021", "amount": -64.0, "category": "Супермаркеты", "description": "Колхоз"},
        ]
        mock_get_exchange_curse_currency.return_value = [
            {"currency": "USD", "rate": 84.5},
            {"currency": "EUR", "rate": 91.67},
        ]
        mock_get_stock_prices.return_value = [{"stock": "AAPL", "price": "217.8000"}]

        # Вызов тестируемой функции
        response = main_view_function(check_date)

        # Проверка результата
        expected_output = {
            "greeting": "Добрый день",
            "cards": [{"last_digits": "7197", "total_spent": 224.89, "cashback": 2.25}],
            "top_transactions": [
                {"date": "31.12.2021", "amount": -160.89, "category": "Супермаркеты", "description": "Колхоз"},
                {"date": "31.12.2021", "amount": -64.0, "category": "Супермаркеты", "description": "Колхоз"},
            ],
            "currency_rates": [{"currency": "USD", "rate": 84.5}, {"currency": "EUR", "rate": 91.67}],
            "stock_prices": [{"stock": "AAPL", "price": "217.8000"}],
        }

        self.assertEqual(json.loads(response), expected_output)

        # Проверка вызовов подменяемых функций
        mock_get_transaction_from_excel_file.assert_called_once()
        mock_read_json_file.assert_any_call("path/to/user_settings.json", "user_currencies")
        mock_read_json_file.assert_any_call("path/to/user_settings.json", "user_stocks")
        mock_get_greeting.assert_called_once()
        mock_total_expenses.assert_called_once()
        mock_top_transactions.assert_called_once()
        mock_get_exchange_curse_currency.assert_called_once_with(["USD"], "RUB")
        mock_get_stock_prices.assert_called_once_with(["AAPL"])
