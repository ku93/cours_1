import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def mock_transactions():
    """Создает фиктивные данные транзакций для тестирования."""
    data = {
        'Дата платежа': [
            '2024-09-15',
            '2024-09-20',
            '2024-10-05',
            '2024-08-10',
            '2024-07-15'
        ],
        'Описание': [
            'Покупка продуктов',
            'Оплата услуг',
            'Покупка онлайн',
            'Покупка продуктов',
            'Покупка в магазине'
        ],
        'Категория': [
            'Продукты',
            'Услуги',
            'Интернет-магазин',
            'Продукты',
            'Продукты'
        ],
        'Сумма платежа': [1000, -500, 2000, 1500, 300]
    }
    return pd.DataFrame(data)


def test_spending_by_category_found(mock_transactions):
    """Тест на успешную фильтрацию транзакций по категории."""
    category = "Продукты"
    result = spending_by_category(mock_transactions, category, date="2024-10-19")

    assert len(result) == 2
    assert result['Сумма платежа'].sum() == 2500


def test_spending_by_category_not_found(mock_transactions):
    """Тест на случай, если категория не найдена."""
    category = "Неизвестная категория"
    result = spending_by_category(mock_transactions, category, date="2024-10-19")

    assert result.empty


def test_spending_by_category_without_date(mock_transactions):
    """Тест на фильтрацию транзакций без передачи даты (используется текущая дата)."""
    category = "Продукты"
    result = spending_by_category(mock_transactions, category)

    assert len(result) == 2
    assert result['Сумма платежа'].sum() == 2500


def test_spending_by_category_invalid_date(mock_transactions):
    """Тест на случай передачи некорректной даты."""
    category = "Продукты"
    with pytest.raises(ValueError):
        spending_by_category(mock_transactions, category, date="invalid-date")
