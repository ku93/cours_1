import json
from idlelib.iomenu import encoding

from src.views import filter_operations_by_date, xlsx_read
import os
import re


ex = xlsx_read("../data/operations.xlsx")
op = filter_operations_by_date(ex, "28.12.2021 00:00:00")


def search_transactions(transactions: list[dict], search_string: str) -> list[dict]:
    result = []
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    for transaction in transactions:
        desc = transaction.get("Категория")
        if search_string == desc:
            if type(desc) and type(desc) is not str:
                pass
            elif re.search(pattern, desc):
                result.append(transaction)
        elif search_string != desc:
            desc_2 = transaction.get("Описание")
            if type(desc) and type(desc) is not str:
                pass
            elif re.search(pattern, desc_2):
                result.append(transaction)

    return result


# t = json.dumps(search_transactions(op, 'Аптеки'), ensure_ascii=False)
# print(t)
