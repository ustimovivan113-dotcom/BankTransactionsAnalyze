from src.views import home_view
from src.services import simple_search
from src.reports import spending_by_category
from src.utils import load_transactions

# Полный текст данных из сообщения пользователя
TEXT_DATA = """row1: Дата операции,Дата платежа,Номер карты,Статус,Сумма операции,Валюта операции,Сумма платежа,Валюта платежа,Кэшбэк,Категория,MCC,Описание,Бонусы (включая кэшбэк),Округление на инвесткопилку,Сумма операции с округлением
row2: 31.12.2021 16:44:00,31.12.2021,*7197,OK,-160.89,RUB,-160.89,RUB,,Супермаркеты,5411,Колхоз,3,0,160.89
..."""  # Вставьте полный текст здесь!!!

df = load_transactions(text_data=TEXT_DATA)
transactions = df.to_dict('records')

# Главная
print("Главная:")
print(home_view("2021-12-31 23:59:59"))

# Сервис: Простой поиск
print("\nПростой поиск:")
print(simple_search(transactions, "Колхоз"))

# Отчет: Траты по категории
print("\nТраты по категории:")
print(spending_by_category(df, "Супермаркеты", "2021-12-31"))
