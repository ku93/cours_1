import json
import logging
from typing import Dict, List


def simple_search(search_string: str, transactions: List[Dict[str, str]]) -> str:
    """
    Ищет транзакции, содержащие заданную строку в описании или категории,
    и возвращает результат в формате JSON.
    """
    logging.info("Поиск транзакций по строке: '%s'", search_string)

    search_string = search_string.lower()
    filtered_transactions = []
    for transaction in transactions:
        description = transaction.get('Описание', '').lower()
        category = transaction.get('Категория', '').lower()
        if search_string in description or search_string in category:
            filtered_transactions.append(transaction)

    logging.info("Найдено %d транзакций.", len(filtered_transactions))

    return json.dumps(filtered_transactions, ensure_ascii=False)
