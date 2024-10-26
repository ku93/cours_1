import pandas as pd

from reports import spending_by_category
from services import simple_search
from views import main_page

if __name__ == '__main__':
    transactions = pd.read_excel('../data/operations.xlsx')
    print(main_page("2024-10-19 14:15:10"))
    print(simple_search('Billa', transactions.to_dict(orient='records')))
    print(spending_by_category(transactions, 'Супермаркеты', '2021-10-19'))
