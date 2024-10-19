import json
import logging
from datetime import datetime

import pandas as pd

from src import utils

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main_page(date_string: str):
    """
    Генерирует JSON-ответ для главной страницы с данными о транзакциях,
    курсах валют и ценах акций.
    """
    logging.info("Запрос на главную страницу с датой: %s", date_string)

    try:
        current_time = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        greeting = utils.get_greeting(current_time)

        transactions = pd.read_excel('../data/operations.xlsx')
        top_transactions = utils.get_top_transactions(transactions)

        cards_data = utils.process_card_data(transactions)

        currency_rates = utils.get_currency_rates()
        stock_prices = utils.get_stock_prices()

        response = {
            "greeting": greeting,
            "cards": cards_data,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices,
        }

        logging.info("Успешно сформирован JSON-ответ.")
        return json.dumps(response, ensure_ascii=False)

    except Exception as e:
        logging.error("Ошибка в main_page: %s", str(e))
        return json.dumps({"error": "Произошла ошибка."}, ensure_ascii=False)


print(main_page("2024-10-19 14:15:10"))
