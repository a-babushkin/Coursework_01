import logging
from datetime import datetime

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("C:/Users/owner/PycharmProjects/Coursework_01/logs/utils.log", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_greeting() -> str:
    """Функция определения приветствия в зависимости от ткущего времени"""
    current_hour = datetime.now().hour
    if current_hour < 6:
        data = "Доброй ночи"
    elif current_hour < 12:
        data = "Доброе утро"
    elif current_hour < 18:
        data = "Добрый день"
    else:
        data = "Добрый вечер"
    logger.info(f"Функция сработала штатно, приветствие: {data}")
    return data


def total_expenses_on_card(incoming_transactions: list[dict], start: datetime, finish: datetime) -> list[dict]:
    """Функция получения общих расходов и кэшбэка по карте"""
    filtering_transactions = [
        transaction
        for transaction in incoming_transactions
        if type(transaction.get("Номер карты")) != float
        # Это условие, что бы убрать транзакции без номеров карты
        and transaction.get("Статус") != "FAILED"
        # Это условие, что бы убрать битые транзакции
        and start <= datetime.strptime(str(transaction.get("Дата платежа")), "%d.%m.%Y") <= finish
        # Это условие задает временной диапазон для выборки
        and float(transaction.get("Сумма платежа", 0)) < 0
        # Это условие выбирает только траты
    ]
    if filtering_transactions:
        cards_info = {}
        for transaction in filtering_transactions:
            card_number = transaction["Номер карты"]
            amount = abs(transaction["Сумма платежа"])

            if card_number not in cards_info:
                cards_info[card_number] = {"last_digits": card_number[-4:], "total_spent": 0, "cashback": 0}
            cards_info[card_number]["total_spent"] = round(cards_info[card_number]["total_spent"], 2) + round(
                amount, 2
            )
            cards_info[card_number]["cashback"] = round(cards_info[card_number]["cashback"], 2) + round(
                amount / 100, 2
            )
        logger.info("Работа функции завершилась штатно.")
        return list(cards_info.values())
    else:
        logger.error("По указанным параметрам нет возвращаемых данных")
        return [{}]


def top_transactions_by_payment_amount(
    incoming_transactions: list[dict], start: datetime, finish: datetime
) -> list[dict]:
    """Функция получения пяти наибольших транзакций по сумме платежа"""
    filtering_transactions = [
        transaction
        for transaction in incoming_transactions
        if type(transaction.get("Номер карты")) != float
        # Это условие, что бы убрать транзакции без номеров карты
        and transaction.get("Статус") != "FAILED"
        # Это условие, что бы убрать битые транзакции
        and start <= datetime.strptime(str(transaction.get("Дата платежа")), "%d.%m.%Y") <= finish
        # Это условие задает временной диапазон для выборки
    ]
    if filtering_transactions:
        cards_info = []
        filtering_transactions.sort(key=lambda x: abs(x["Сумма платежа"]), reverse=True)
        for item in filtering_transactions[:5]:
            cards_info.append(
                {
                    "date": item["Дата платежа"],
                    "amount": item["Сумма платежа"],
                    "category": item["Категория"],
                    "description": item["Описание"],
                }
            )
        logger.info("Работа функции завершилась штатно.")
        return cards_info
    else:
        logger.error("По указанным параметрам нет возвращаемых данных")
        return [{}]
