from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import (create_currency_json_response, get_cbr_exchange_rates,
                       get_greeting, get_top_transactions, load_user_settings,
                       process_card_data)


@pytest.mark.parametrize("timestamp, expected_greeting", [
    (pd.Timestamp("2024-10-19 05:00:00"), "Доброй ночи"),
    (pd.Timestamp("2024-10-19 10:00:00"), "Доброе утро"),
    (pd.Timestamp("2024-10-19 14:00:00"), "Добрый день"),
    (pd.Timestamp("2024-10-19 20:00:00"), "Добрый вечер"),
])
def test_get_greeting(timestamp, expected_greeting):
    """Тест на проверку приветствия в зависимости от времени суток."""
    assert get_greeting(timestamp) == expected_greeting


@pytest.mark.parametrize("transactions, expected_amount", [
    (
        pd.DataFrame({
            "Дата платежа": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-06"],
            "Сумма платежа": [100, 200, 300, 400, 500, 10],
            "Категория": ["A", "B", "C", "D", "E", "F"],
            "Описание": ["desc1", "desc2", "desc3", "desc4", "desc5", "desc6"]
        }),
        500
    ),
    (
        pd.DataFrame({
            "Дата платежа": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "Сумма платежа": [50, 20, 5],
            "Категория": ["A", "B", "C"],
            "Описание": ["desc1", "desc2", "desc3"]
        }),
        50
    ),
])
def test_get_top_transactions(transactions, expected_amount):
    """Тест на получение топ-5 транзакций."""
    top_transactions = get_top_transactions(transactions)
    assert len(top_transactions) <= 5
    assert top_transactions[0]["amount"] == expected_amount


@pytest.mark.parametrize("transactions, expected_total_spent, expected_cashback", [
    (
        pd.DataFrame({
            "Номер карты": ["1234", "5678", "1234", "5678"],
            "Сумма платежа": [-100, -200, -50, -30]
        }),
        150,
        1.5
    ),
    (
        pd.DataFrame({
            "Номер карты": ["4321", "8765", "4321", "8765"],
            "Сумма платежа": [-300, -150, -200, -100]
        }),
        500,
        5.0
    ),
])
def test_process_card_data(transactions, expected_total_spent, expected_cashback):
    """Тест обработки данных по картам."""
    card_data = process_card_data(transactions)
    assert len(card_data) >= 1
    assert card_data[0]["total_spent"] == expected_total_spent
    assert card_data[0]["cashback"] == expected_cashback


@pytest.mark.parametrize("file_content, expected_settings", [
    ('{"user_currencies": ["USD", "EUR"]}', {"user_currencies": ["USD", "EUR"]}),
    ('{"user_currencies": ["GBP"]}', {"user_currencies": ["GBP"]}),
])
@patch("builtins.open", new_callable=mock_open)
def test_load_user_settings(mock_file, file_content, expected_settings):
    """Тест загрузки настроек пользователя."""
    mock_file.return_value.read.return_value = file_content
    settings = load_user_settings("dummy_path.json")
    assert settings == expected_settings
    mock_file.assert_called_once_with("dummy_path.json", "r")


@pytest.mark.parametrize("mock_response_content, expected_rates", [
    (
        b"""
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
        """,
        {"USD": 73.4567, "EUR": 85.1234}
    ),
    (
        b"""
        <ValCurs>
            <Valute>
                <CharCode>GBP</CharCode>
                <Value>95,5678</Value>
            </Valute>
        </ValCurs>
        """,
        {"GBP": 95.5678}
    ),
])
@patch("requests.get")
def test_get_cbr_exchange_rates(mock_get, mock_response_content, expected_rates):
    """Тест на получение курсов валют с сайта ЦБ."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = mock_response_content
    rates = get_cbr_exchange_rates()
    assert rates == expected_rates


@pytest.mark.parametrize("user_currencies, rates, expected_response", [
    (
        ["USD", "EUR"],
        {"USD": 73.4567, "EUR": 85.1234},
        [{"currency": "USD", "rate": 73.4567}, {"currency": "EUR", "rate": 85.1234}]
    ),
    (
        ["GBP"],
        {"GBP": 95.5678},
        [{"currency": "GBP", "rate": 95.5678}]
    ),
])
def test_create_currency_json_response(user_currencies, rates, expected_response):
    """Тест на создание JSON ответа с курсами валют."""
    json_response = create_currency_json_response(user_currencies, rates)
    assert json_response == expected_response
