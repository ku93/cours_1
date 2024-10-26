import json
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import main_page


@pytest.fixture
def mock_transactions():
    """Создает фиктивные данные транзакций для тестирования."""
    data = {
        'Описание': ['Покупка в магазине', 'Оплата услуги'],
        'Категория': ['Продукты', 'Услуги'],
        'Сумма платежа': [1000, -500]
    }
    return pd.DataFrame(data)


@pytest.mark.parametrize("greeting, top_transactions, card_data, currency_rates, stock_prices, expected_response", [
    (
        "Добрый день",
        [{'Описание': 'Покупка в магазине', 'Категория': 'Продукты', 'Сумма платежа': 1000}],
        [{'last_digits': '1234', 'total_spent': 1000, 'cashback': 10}],
        [{'currency': 'USD', 'rate': 75.5}],
        {'AAPL': 150.00},
        {
            "greeting": "Добрый день",
            "cards": [{'last_digits': '1234', 'total_spent': 1000, 'cashback': 10}],
            "top_transactions": [{'Описание': 'Покупка в магазине', 'Категория': 'Продукты', 'Сумма платежа': 1000}],
            "currency_rates": [{'currency': 'USD', 'rate': 75.5}],
            "stock_prices": {'AAPL': 150.00},
        }
    ),
    (
        "Добрый вечер",
        [{'Описание': 'Оплата услуги', 'Категория': 'Услуги', 'Сумма платежа': -500}],
        [{'last_digits': '5678', 'total_spent': 500, 'cashback': 5}],
        [{'currency': 'EUR', 'rate': 90.0}],
        {'GOOGL': 2800.00},
        {
            "greeting": "Добрый вечер",
            "cards": [{'last_digits': '5678', 'total_spent': 500, 'cashback': 5}],
            "top_transactions": [{'Описание': 'Оплата услуги', 'Категория': 'Услуги', 'Сумма платежа': -500}],
            "currency_rates": [{'currency': 'EUR', 'rate': 90.0}],
            "stock_prices": {'GOOGL': 2800.00},
        }
    )
])
@patch('src.utils.get_greeting')
@patch('src.utils.get_top_transactions')
@patch('src.utils.process_card_data')
@patch('src.utils.get_currency_rates')
@patch('src.utils.get_stock_prices')
@patch('pandas.read_excel')
def test_main_page_success(mock_read_excel, mock_get_stock_prices, mock_get_currency_rates,
                           mock_process_card_data, mock_get_top_transactions,
                           mock_get_greeting, mock_transactions,
                           greeting, top_transactions, card_data, currency_rates, stock_prices, expected_response):
    """Тест на успешное получение данных главной страницы."""
    mock_read_excel.return_value = mock_transactions
    mock_get_greeting.return_value = greeting
    mock_get_top_transactions.return_value = top_transactions
    mock_process_card_data.return_value = card_data
    mock_get_currency_rates.return_value = currency_rates
    mock_get_stock_prices.return_value = stock_prices

    date_string = "2024-10-19 14:15:10"
    response = main_page(date_string)

    assert json.loads(response) == expected_response


@pytest.mark.parametrize("date_string, expected_response", [
    ("неверная дата", {"error": "Произошла ошибка."}),
    ("2024-13-45 25:61:61", {"error": "Произошла ошибка."}),
])
@patch('pandas.read_excel')
def test_main_page_invalid_date(mock_read_excel, date_string, expected_response):
    """Тест на обработку ошибок при неверном формате даты."""
    mock_read_excel.return_value = pd.DataFrame()

    response = main_page(date_string)

    assert json.loads(response) == expected_response


@patch('pandas.read_excel')
def test_main_page_error_handling(mock_read_excel):
    """Тест на обработку ошибок при получении данных."""
    mock_read_excel.side_effect = Exception("Ошибка чтения файла.")

    date_string = "2024-10-19 14:15:10"
    response = main_page(date_string)

    expected_response = {"error": "Произошла ошибка."}
    assert json.loads(response) == expected_response
