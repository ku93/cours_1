from datetime import datetime


data = datetime.now()
hour = data.hour


def data(current_time):
    """Функция принимает текущую дату и приветствует пользователя"""

    if hour < 6:
        return "Доброй ночи"
    elif 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"


# dt = data(data)
# print(dt)
