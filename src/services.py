from typing import List, Dict
from src.utils import load_transactions


def simple_search(transactions: List[Dict], query: str) -> List[Dict]:
    """
    Простой поиск: возвращает транзакции, содержащие query в описании или категории.
    """
    result = []
    for trans in transactions:
        desc = trans.get("description", "").lower()
        category = trans.get("Категория", "").lower()  # Из Excel
        if query.lower() in desc or query.lower() in category:
            result.append(trans)
    return result


# Пример
if __name__ == "__main__":
    text_data = """Вставьте текст"""  # Полный текст
    df = load_transactions(text_data=text_data)
    transactions = df.to_dict('records')
    result = simple_search(transactions, "Супермаркеты")
    print(result)
