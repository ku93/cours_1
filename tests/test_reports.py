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


@pytest.mark.parametrize("category, date, expected_len, expected_sum, raises_exception", [
    ("Продукты", "2024-10-19", 2, 2500, None),
    ("Неизвестная категория", "2024-10-19", 0, 0, None),
    ("Продукты", None, 2, 2500, None),
    ("Продукты", "invalid-date", None, None, ValueError)
])
def test_spending_by_category(mock_transactions, category, date, expected_len, expected_sum, raises_exception):
    """Параметризованный тест для проверки фильтрации транзакций по категории и обработки исключений."""
    if raises_exception:
        with pytest.raises(raises_exception):
            spending_by_category(mock_transactions, category, date=date)
    else:
        result = spending_by_category(mock_transactions, category, date=date)
        assert len(result) == expected_len
        assert result['Сумма платежа'].sum() == expected_sum
