import os

import pandas as pd

from src.files_reader import get_transaction_from_excel_file
from src.reports import spending_by_category
from src.services import main_services_function
from src.views import main_view_function

if __name__ == "__main__":
    transactions = get_transaction_from_excel_file(os.path.join(os.path.dirname(__file__), "data", "operations.xlsx"))
    filtering_transactions = [
        transaction
        for transaction in transactions
        if type(transaction.get("Номер карты")) != float
           # Это условие, что бы убрать транзакции без номеров карты
           and transaction.get("Статус") != "FAILED"
        # Это условие, что бы убрать битые транзакции
    ]

    # print(main_view_function(input("Введите дату:")))

    print(main_services_function(filtering_transactions, input("Введите строку поиска:")))

    transaction_df = pd.DataFrame(filtering_transactions)
    spending_by_category(pd.DataFrame(transaction_df), input("Введите категорию:"), input("Введите дату:"))
