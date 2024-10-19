from unittest.mock import mock_open, patch

import pandas as pd

from src.utils import (create_currency_json_response, get_cbr_exchange_rates,
                       get_greeting, get_top_transactions, load_user_settings,
                       process_card_data)


def test_get_greeting():
    """Тест на проверку приветствия в зависимости от времени суток."""
    assert get_greeting(pd.Timestamp("2024-10-19 05:00:00")) == "Доброй ночи"
    assert get_greeting(pd.Timestamp("2024-10-19 10:00:00")) == "Доброе утро"
    assert get_greeting(pd.Timestamp("2024-10-19 14:00:00")) == "Добрый день"
    assert get_greeting(pd.Timestamp("2024-10-19 20:00:00")) == "Добрый вечер"


def test_get_top_transactions():
    """Тест на получение топ-5 транзакций."""
    transactions = pd.DataFrame({
        "Дата платежа": [
            "2024-01-01",
            "2024-01-02",
            "2024-01-03",
            "2024-01-04",
            "2024-01-05",
            "2024-01-06"],
        "Сумма платежа": [100, 200, 300, 400, 500, 10],
        "Категория": ["A", "B", "C", "D", "E", "F"],
        "Описание": ["desc1", "desc2", "desc3", "desc4", "desc5", "desc6"]
    })

    top_transactions = get_top_transactions(transactions)

    assert len(top_transactions) == 5
    assert top_transactions[0]["amount"] == 500


def test_process_card_data():
    """Тест обработки данных по картам."""
    transactions = pd.DataFrame({
        "Номер карты": ["1234", "5678", "1234", "5678"],
        "Сумма платежа": [-100, -200, -50, -30]
    })

    card_data = process_card_data(transactions)

    assert len(card_data) == 2
    assert card_data[0]["total_spent"] == 150
    assert card_data[0]["cashback"] == 1.5


@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
def test_load_user_settings(mock_file):
    """Тест загрузки настроек пользователя."""
    settings = load_user_settings("dummy_path.json")

    assert settings == {"user_currencies": ["USD", "EUR"]}
    mock_file.assert_called_once_with("dummy_path.json", "r")


@patch("requests.get")
def test_get_cbr_exchange_rates(mock_get):
    """Тест на получение курсов валют с сайта ЦБ."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"""
    <ValCurs>
        <Valute>
            <CharCode>USD</CharCode>
            <Value>73,4567</Value>
        </Valute>
        <Valute>
            <CharCode>EUR</CharCode>
            <Value>85,1234</Value>
        </Valute>
    </ValCurs>
    """

    rates = get_cbr_exchange_rates()
    assert rates == {"USD": 73.4567, "EUR": 85.1234}


def test_create_currency_json_response():
    """Тест на создание JSON ответа с курсами валют."""
    user_currencies = ["USD", "EUR"]
    rates = {"USD": 73.4567, "EUR": 85.1234}

    json_response = create_currency_json_response(user_currencies, rates)

    assert json_response == [
        {"currency": "USD", "rate": 73.4567},
        {"currency": "EUR", "rate": 85.1234}
    ]
