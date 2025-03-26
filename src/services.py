import json
import logging
import re

logger = logging.getLogger("services")
file_handler = logging.FileHandler("C:/Users/owner/PycharmProjects/Coursework_01/logs/services.log", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def main_services_function(transactions: list[dict], search_str: str) -> str:
    """Функция, принимает на вход строку для поиска и возвращает в ответ строку со всеми транзакциями,
    содержащими запрос в описании или категории в формате JSON"""

    pattern = re.compile(re.escape(search_str), re.IGNORECASE)
    result = [
        transaction
        for transaction in transactions
        if (type(transaction.get("Категория")) != float and pattern.search(transaction.get("Категория", "")))
        or (type(transaction.get("Описание")) != float and pattern.search(transaction.get("Описание", "")))
    ]
    if result:
        logger.info(f"Функция сработала штатно, получена выборка: {result}")
        return json.dumps(result, ensure_ascii=False)
    else:
        logger.error("По указанным параметрам нет возвращаемых данных")
        return "[{}]"
