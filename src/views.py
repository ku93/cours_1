from time import strftime
import requests
import pandas as pd
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

logger = logging.getLogger("xlsx_read")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("../logs/xlsx_read.log", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

xlsx_path = "../data/operations.xlsx"


def xlsx_read(path):
    """Функция, которая принимает на вход путь к excel"""
    try:
        logger.info("Открываем файл excel")
        excel_data = pd.read_excel(path)
        return excel_data.to_dict(orient="records")
    except FileNotFoundError as ex:
        logger.error(f"Произошла ошибка: файл не найден - {ex}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame вместо списка
    except pd.errors.ParserError as ex:
        logger.error(f"Произошла ошибка при разборе csv - {ex}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame вместо списка
    except Exception as ex:
        logger.error(f"Произошла непредвиденная ошибка - {ex}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame вместо списка


ex = xlsx_read(xlsx_path)
# print(ex)


def filter_operations_by_date(path: str, inp_data):
    """
    Функция для фильтрации операций по дате.

    :param path: str - путь к Excel-файлу с данными.
    :param incoming_date_str: str - строка с входящей датой в формате 'DD.MM.YYYY'.
    :return: pd.DataFrame - отфильтрованный DataFrame с операциями в заданном диапазоне дат.
    """
    inp_data_dt = datetime.strptime(inp_data, "%d.%m.%Y %H:%M:%S")

    start_data = inp_data_dt.replace(day=1)
    logger.info("Фильтруем даты за указанный период")
    filt_op = []
    for i in path:

        op_data = datetime.strptime(i["Дата операции"], "%d.%m.%Y %H:%M:%S")
        if start_data <= op_data <= inp_data_dt:
            filt_op.append(i)
            return filt_op


t = filter_operations_by_date(ex, "28.12.2021 00:00:00")
# print(t)


def nub_card(filt):
    """Функция создает список номеров карт"""
    lists = []
    for i in filt:
        if i["Номер карты"] not in lists:
            lists.append(i["Номер карты"])
    return lists


nc = nub_card(t)
# print(nc)


def sum_op(filt):
    """Функция считает общую сумму расходов"""
    logger.info("Считаем общую сумму расходов за указанный период")
    count = 0
    for i in nc:
        for s in filt:
            if i == s["Номер карты"]:
                if s["Сумма платежа"] < 0:
                    count -= s["Сумма платежа"]

        return round(count, 2)


so = sum_op(t)
# print(so)


def cash(filt):
    """"""
    count = 0
    for i in filt:
        if i["Сумма платежа"] < 0:
            if i["Сумма платежа"]:
                result = i["Сумма платежа"] / 100
                count -= result
    return count


ch = cash(t)
# print(ch)


def top(filt):
    """"""
    sorted_transactions = sorted(filt, key=lambda x: x["Сумма платежа"], reverse=True)
    top_5 = sorted_transactions[:5]

    for index, filt in enumerate(top_5, start=1):
        return f"Transaction {index}: Amount - {filt['Сумма платежа']}, Description - {filt['Описание']}"


t = top(t)
# print(t)
