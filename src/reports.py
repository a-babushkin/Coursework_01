import logging
from datetime import datetime, timedelta
from typing import Optional, Callable, Any

import pandas as pd

logger = logging.getLogger("reports")
file_handler = logging.FileHandler("C:/Users/owner/PycharmProjects/Coursework_01/logs/reports.log", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def report_decorator(file_name: str="report.txt") -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            report_data = func(*args, **kwargs)

            with open(file_name, "w", encoding="UTF-8") as f:
                f.write(f"Отчет за {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(report_data + "\n\n")

            return report_data

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(transactions_dfr: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    formated_date = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")
    if formated_date is None:
        formated_date = datetime.now()

    start_date = formated_date - timedelta(days=90)

    filtered = transactions_dfr[
        (transactions_dfr["Категория"] == category)
        & (transactions_dfr["Дата платежа"] >= start_date.strftime("%d-%m-%Y"))
        & (transactions_dfr["Дата платежа"] <= formated_date.strftime("%d-%m-%Y"))
    ]

    return filtered
