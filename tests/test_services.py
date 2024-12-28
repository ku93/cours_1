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


@pytest.mark.parametrize("search_string, expected_result", [
    (
        "покупка",
        [
            {'Описание': 'Покупка в магазине', 'Категория': 'Продукты', 'Сумма платежа': 1000},
            {'Описание': 'Покупка онлайн', 'Категория': 'Интернет-магазин', 'Сумма платежа': 2000}
        ]
    ),
    (
        "неизвестная строка",
        []
    ),
    (
        "возврат",
        [{'Описание': 'Возврат товара', 'Категория': 'Возвраты', 'Сумма платежа': 1500}]
    ),
    (
        "магазин",
        [
            {'Описание': 'Покупка в магазине', 'Категория': 'Продукты', 'Сумма платежа': 1000},
            {'Описание': 'Покупка онлайн', 'Категория': 'Интернет-магазин', 'Сумма платежа': 2000}
        ]
    ),
])
def test_simple_search(mock_transactions, search_string, expected_result):
    """Параметризованный тест для проверки поиска транзакций."""
    result = simple_search(search_string, mock_transactions)
    assert json.loads(result) == expected_result
