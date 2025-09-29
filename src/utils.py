import json
import logging
import os
from pathlib import Path
from typing import Dict, List

import pandas as pd

MODULE_DIR = Path(__file__).resolve().parent
LOG_DIR = MODULE_DIR.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
log_file = LOG_DIR / "utils.log"
file_handler = logging.FileHandler(log_file, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def parse_text_to_df(text_data: str) -> pd.DataFrame:
    """
    Парсит текст с rowN: values в DataFrame (симуляция Excel).
    """
    lines = text_data.strip().split('\n')
    rows = []
    headers = None
    for line in lines:
        if line.startswith('row'):
            # Извлекаем данные после ': '
            values_str = line.split(':', 1)[1].strip()
            values = [v.strip() for v in values_str.split(',')]
            if headers is None:
                headers = values  # Первая row - заголовки
            else:
                rows.append(values)

    df = pd.DataFrame(rows, columns=headers)
    # Преобразуем числовые колонки
    numeric_cols = ['Сумма операции', 'Сумма платежа', 'Кэшбэк', 'Бонусы (включая кэшбэк)',
                    'Округление на инвесткопилку', 'Сумма операции с округлением']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    logger.info(f"Parsed {len(df)} rows from text data")
    return df


def load_transactions(file_path: str = 'data/operations.xlsx', text_data: str = None) -> pd.DataFrame:
    """
    Загружает транзакции из Excel или текста.
    """
    if text_data:
        return parse_text_to_df(text_data)

    if not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        return pd.DataFrame()

    try:
        df = pd.read_excel(file_path)
        logger.info(f"Loaded {len(df)} transactions from {file_path}")
        return df
    except Exception as e:
        logger.error(f"Error loading Excel: {e}")
        return pd.DataFrame()


def load_json_data(file_path: str) -> list[dict]:
    """
    Возвращает данные о финансовых транзакция из JSON
    """
    try:
        if not os.path.exists(file_path):
            logger.warning("File not found")
            return []

        if os.path.getsize(file_path) == 0:
            logger.warning("File is empty")
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            logger.info(f"Reading file from: {file_path}")
            data = json.load(file)

        if not isinstance(data, list):
            logger.warning("File does not contain valid data")
            return []

        return data

    except (json.JSONDecodeError, FileNotFoundError, PermissionError, OSError):
        logger.error("Incorrect data")
        return []


def read_transactions_csv(file_path: str) -> List[Dict]:
    """
    Функция для считывания финансовых операций из CSV
    """
    csv_data = pd.read_csv(file_path, sep=";")
    return csv_data.to_dict(orient="records")


def read_transactions_xlsx(file_path: str) -> List[Dict]:
    """
    Функция для считывания финансовых операций из Excel
    """
    xlsx_data = pd.read_excel(file_path)
    return xlsx_data.to_dict(orient="records")
