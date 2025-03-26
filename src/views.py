import json
import logging
import os
from datetime import datetime

from src.external_api import get_exchange_curse_currency, get_stock_prices
from src.files_reader import get_transaction_from_excel_file, read_json_file
from src.utils import get_greeting, top_transactions_by_payment_amount, total_expenses_on_card

logger = logging.getLogger("views")
file_handler = logging.FileHandler("C:/Users/owner/PycharmProjects/Coursework_01/logs/views.log", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def main_view_function(check_date: str) -> str:
    """Функция, принимает на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращает в ответ строку в формате JSON"""

    current_time = datetime.strptime(check_date, "%Y-%m-%d %H:%M:%S")
    start_day = current_time.replace(day=1)
    finish_day = current_time

    output_dict = {}
    file_name = os.path.dirname(__file__)
    transactions = get_transaction_from_excel_file(os.path.join(file_name, "../data", "operations.xlsx"))

    user_currency_list = read_json_file(os.path.join(file_name, "../data", "user_settings.json"), "user_currencies")
    user_stocks_list = read_json_file(os.path.join(file_name, "../data", "user_settings.json"), "user_stocks")

    output_dict["greeting"] = get_greeting()
    output_dict["cards"] = str(total_expenses_on_card(transactions, start_day, finish_day))
    output_dict["top_transactions"] = str(top_transactions_by_payment_amount(transactions, start_day, finish_day))
    output_dict["currency_rates"] = str(get_exchange_curse_currency(user_currency_list, "RUB"))
    output_dict["stock_prices"] = str(get_stock_prices(user_stocks_list))

    logger.info(f"Функция сработала штатно, получена выборка: {output_dict}")
    return json.dumps(output_dict, ensure_ascii=False)
