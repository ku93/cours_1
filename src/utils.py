import json
import logging
import os
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv('../.env')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_greeting(current_time: pd.Timestamp) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = current_time.hour
    if hour < 6:
        return "Доброй ночи"
    elif hour < 12:
        return "Доброе утро"
    elif hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def get_top_transactions(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """Получает топ-5 транзакций по сумме платежа."""
    logging.info("Получение топ-транзакций.")
    top_transactions = transactions.assign(
        absolute_amount=transactions['Сумма платежа'].abs()
    ).nlargest(5, 'absolute_amount').to_dict(orient='records')

    result_top_transactions = []
    for transaction in top_transactions:
        result_top_transactions.append({
            "date": transaction["Дата платежа"],
            "amount": transaction["Сумма платежа"],
            "category": transaction["Категория"],
            "description": transaction["Описание"]
        })

    logging.info("Топ-транзакции успешно получены.")
    return result_top_transactions


def process_card_data(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """Обрабатывает данные по картам и возвращает информацию о тратах."""
    logging.info("Обработка данных по картам.")
    card_data = {}
    for index, transaction in transactions.iterrows():
        card_number = transaction['Номер карты']
        amount = transaction['Сумма платежа']

        if isinstance(card_number, str):
            if card_number not in card_data:
                card_data[card_number] = 0
            if amount < 0:
                card_data[card_number] += amount * -1

    result_card_data = []
    for k, v in card_data.items():
        result_card_data.append(
            {
                "last_digits": k[1:],
                "total_spent": round(v, 2),
                "cashback": round(v * 0.01, 2)
            }
        )

    logging.info("Данные по картам успешно обработаны.")
    return result_card_data


def load_user_settings(file_path: str) -> Optional[Dict[str, Any]]:
    """Загружает настройки пользователя из JSON-файла."""
    try:
        with open(file_path, 'r') as file:
            settings = json.load(file)
        logging.info("Настройки пользователя загружены.")
        return settings
    except FileNotFoundError:
        logging.error("Файл настроек не найден.")
        return None
    except json.JSONDecodeError:
        logging.error("Ошибка при чтении файла настроек.")
        return None


def get_cbr_exchange_rates() -> Optional[Dict[str, float]]:
    """Получает курсы валют с сайта Центробанка России."""
    logging.info("Получение курсов валют с сайта ЦБ.")
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)
    if response.status_code == 200:
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()
        rates = {}
        for currency in root.findall('Valute'):
            code = currency.find('CharCode').text
            value = currency.find('Value').text
            rates[code] = float(value.replace(',', '.'))
        logging.info("Курсы валют успешно получены.")
        return rates
    else:
        logging.error("Ошибка при получении курсов валют: %s", response.status_code)
        return None


def create_currency_json_response(user_currencies: List[str], rates: Dict[str, float]) -> List[Dict[str, Any]]:
    """Создает JSON-ответ с курсами валют для заданных пользователем валют."""
    currency_rates = []
    for currency in user_currencies:
        if currency in rates:
            currency_rates.append({
                "currency": currency,
                "rate": rates[currency]
            })
    return currency_rates


def get_currency_rates() -> Optional[List[Dict[str, Any]]]:
    """Получает курсы валют для заданных пользователем валют."""
    user_settings = load_user_settings('../user_settings.json')

    if user_settings:
        user_currencies = user_settings.get("user_currencies", [])

        rates = get_cbr_exchange_rates()

        if rates:
            json_response = create_currency_json_response(user_currencies, rates)
            return json_response
        else:
            logging.warning("Не удалось получить курсы валют.")
    else:
        logging.warning("Не удалось загрузить настройки.")


def get_stock_prices() -> Optional[Dict[str, Optional[float]]]:
    """Получает текущие цены акций для заданных пользователем акций."""
    logging.info("Получение цен акций.")
    user_settings = load_user_settings('../user_settings.json')
    if user_settings:
        user_stocks = user_settings.get("user_stocks", [])
        stock_data = {}
        for stock in user_stocks:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": stock,
                "apikey": os.getenv('APIKEY')
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if "Global Quote" in data:
                    price = float(data["Global Quote"]["05. price"])
                    stock_data[stock] = price
                else:
                    stock_data[stock] = None
            else:
                stock_data[stock] = None
                logging.error("Ошибка при получении данных для акции %s: %s", stock, response.status_code)
        logging.info("Цены акций успешно получены.")
        return stock_data
    else:
        logging.warning("Не удалось загрузить настройки пользователя.")

g=get_stock_prices()
print(g)