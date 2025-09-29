import pytest
from unittest.mock import patch
from src.utils import parse_text_to_df, load_transactions


def test_parse_text_to_df():
    sample_text = """row1: A,B,C
row2: 1,2,3
row3: 4,5,6"""
    df = parse_text_to_df(sample_text)
    assert len(df) == 2
    assert list(df.columns) == ['A', 'B', 'C']

@patch('os.path.exists', return_value=False)  # Mock: файла нет


def test_load_transactions_empty(mock_exists):
    df = load_transactions(text_data="")
    assert df.empty
