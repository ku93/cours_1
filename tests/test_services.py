import json

import pytest

from src.services import simple_search


@pytest.fixture
def mock_transactions():
    """Создает фиктивные данные транзакций для тестирования."""
    return [
        {"Описание": "Покупка в магазине", "Категория": "Продукты", "Сумма платежа": 1000},
        {"Описание": "Оплата услуги", "Категория": "Услуги", "Сумма платежа": -500},
        {"Описание": "Возврат товара", "Категория": "Возвраты", "Сумма платежа": 1500},
        {"Описание": "Покупка онлайн", "Категория": "Интернет-магазин", "Сумма платежа": 2000}
    ]


def test_simple_search_found(mock_transactions):
    """Тест на успешный поиск транзакций."""
    search_string = "покупка"
    expected_result = [
        {'Описание': 'Покупка в магазине', 'Категория': 'Продукты', 'Сумма платежа': 1000},
        {'Описание': 'Покупка онлайн', 'Категория': 'Интернет-магазин', 'Сумма платежа': 2000}
    ]

    result = simple_search(search_string, mock_transactions)

    assert json.loads(result) == expected_result


def test_simple_search_not_found(mock_transactions):
    """Тест на отсутствие найденных транзакций."""
    search_string = "неизвестная строка"
    expected_result = []

    result = simple_search(search_string, mock_transactions)

    assert json.loads(result) == expected_result


def test_simple_search_case_insensitive(mock_transactions):
    """Тест на регистронезависимый поиск."""
    search_string = "возврат"
    expected_result = [{'Описание': 'Возврат товара', 'Категория': 'Возвраты', 'Сумма платежа': 1500}]

    result = simple_search(search_string, mock_transactions)

    assert json.loads(result) == expected_result


def test_simple_search_partial_match(mock_transactions):
    """Тест на частичное совпадение строки поиска."""
    search_string = "магазин"
    expected_result = [
        {'Описание': 'Покупка в магазине', 'Категория': 'Продукты', 'Сумма платежа': 1000},
        {'Описание': 'Покупка онлайн', 'Категория': 'Интернет-магазин', 'Сумма платежа': 2000}
    ]

    result = simple_search(search_string, mock_transactions)

    assert json.loads(result) == expected_result
