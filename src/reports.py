import json
from datetime import datetime, timedelta
from time import strftime

import pandas as pd

# Чтение данных из Excel
ex = pd.read_excel("../data/operations.xlsx")


def spending_by_category(transactions: pd.DataFrame, category: str, inp_data: str):
    t = transactions.loc[transactions["Категория"] == category]
    start_date = datetime.strptime(inp_data, "%d.%m.%Y %H:%M:%S") - timedelta(days=90)
    result = t[t["Дата операции"] >= start_date]
    return result


s = spending_by_category(ex, "Аптеки", "28.12.2021 00:00:00")
print(s)
