import json
from datetime import datetime
from typing import Dict, List

import requests

from src.utils import load_transactions


def get_greeting() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_currency_rates(currencies: List[str]) -> List[Dict]:
    rates = []
    for currency in currencies:
        response = requests.get(f"https://api.exchangerate.host/convert?from={currency}&to=RUB")
        if response.status_code == 200:
            rate = response.json().get("result", 0)
            rates.append({"currency": currency, "rate": rate})
    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict]:
    prices = []
    api_key = "your_alpha_vantage_key"  # Из .env
    for stock in stocks:
        response = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}")
        if response.status_code == 200:
            price = response.json().get("Global Quote", {}).get("05. price", 0)
            prices.append({"stock": stock, "price": float(price)})
    return prices


def home_view(date_str: str) -> Dict:
    """
    Главная страница: JSON с данными.
    """
    # Парсим дату, берем начало месяца
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_date = dt.replace(day=1)
    end_date = dt

    # Загружаем транзакции (из текста или файла)
    text_data = """Вставьте полный текст из <DOCUMENT> сюда"""  # Замените на полный текст из сообщения
    df = load_transactions(text_data=text_data)

    # Фильтруем по дате (примерно, используйте реальные даты)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S', errors='coerce')
    df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)]

    # Карты: группируем по номеру карты
    cards = df.groupby('Номер карты').agg(
        total_spent=('Сумма операции', lambda x: abs(x[x < 0].sum())),
        cashback=('Кэшбэк', 'sum')
    ).reset_index().to_dict('records')

    # Топ-транзакции: топ 5 по сумме
    top_transactions = df.sort_values('Сумма операции', ascending=False).head(5)[
        ['Дата операции', 'Сумма операции', 'Категория', 'Описание']
    ].to_dict('records')

    # Настройки из user_settings.json
    with open('user_settings.json', 'r') as f:
        settings = json.load(f)

    # Курсы и акции
    currency_rates = get_currency_rates(settings['user_currencies'])
    stock_prices = get_stock_prices(settings['user_stocks'])

    return {
        "greeting": get_greeting(),
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }


# Пример вызова
if __name__ == "__main__":
    json_response = home_view("2025-09-29 00:00:00")
    print(json.dumps(json_response, indent=4, ensure_ascii=False))
