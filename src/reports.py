import logging
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает DataFrame с тратами по заданной категории за последние три месяца от переданной даты."""
    logging.info("Запрос на траты по категории: '%s'", category)


    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    logging.info("Используемая дата: %s", date)

    current_date = datetime.strptime(date, "%Y-%m-%d")
    three_months_ago = current_date - timedelta(days=90)

    filtered_transactions = transactions[
        (transactions['Категория'] == category)
        & (pd.to_datetime(transactions['Дата платежа']) >= three_months_ago)
        & (pd.to_datetime(transactions['Дата платежа']) <= current_date)
    ]

    total_spending = filtered_transactions['Сумма платежа'].sum()
    logging.info("Общая сумма трат по категории '%s': %f", category, total_spending)

    return filtered_transactions
