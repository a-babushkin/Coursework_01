import json
import logging
from typing import Any

import pandas as pd

logger = logging.getLogger("files_reader")
file_handler = logging.FileHandler(
    "C:/Users/owner/PycharmProjects/Coursework_01/logs/files_reader.log", encoding="UTF-8"
)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_transaction_from_excel_file(path_to_file: str) -> list[dict]:
    """Получение списка трансакций из Excell файла"""
    try:
        transactions = pd.read_excel(path_to_file)
        logger.info(f"Функция сработала штатно, получены данные: {transactions}")
        return transactions.to_dict("records")
    except FileNotFoundError:
        logger.error(f"Файл по пути {path_to_file} не найден")
        return [{}]


def read_json_file(path_to_file: str, target: str) -> Any:
    """Принимает на вход путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях."""
    try:
        with open(path_to_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info(f"Функция сработала штатно, получены данные: {data}")
            return data[target]
    except FileNotFoundError:
        logger.error(f"Файл по пути {path_to_file} не найден")
        return []
    except json.JSONDecodeError:
        logger.error("Произошла ошибка декодирования JSON в данных")
        return []
