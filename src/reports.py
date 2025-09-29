import json
from typing import Optional

import pandas as pd

from src.utils import load_transactions


def save_to_file(filename: Optional[str] = None):
    """
    Декоратор для записи отчета в файл.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if filename is None:
                default_filename = f"{func.__name__}.json"
            else:
                default_filename = filename
            with open(default_filename, 'w') as f:
                json.dump(result, f, indent=4)
            return result

        return wrapper

    return decorator


@save_to_file(filename="spending_by_category.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Траты по категории за последние 3 месяца.
    """
    if date is None:
        date = pd.to_datetime('today').strftime('%Y-%m-%d')
    end_date = pd.to_datetime(date)
    start_date = end_date - pd.DateOffset(months=3)

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], errors='coerce')
    filtered = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date) &
        (transactions['Категория'] == category) &
        (transactions['Сумма операции'] < 0)  # Только расходы
        ]
    return filtered


# Пример
if __name__ == "__main__":
    text_data = """Вставьте текст"""  # Полный
    df = load_transactions(text_data=text_data)
    result = spending_by_category(df, "Супермаркеты", "2021-12-31")
    print(result)
