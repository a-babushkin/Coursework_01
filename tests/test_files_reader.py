import json
from typing import Any
from unittest.mock import mock_open, patch

import pandas as pd

from src.files_reader import get_transaction_from_excel_file, read_json_file


@patch("builtins.open")
@patch("json.load")
def test_read_json_file_success(mock_load: Any, mock_open_file: Any) -> None:
    """Тестируем функцию на успешную работу"""
    mock_open_file.new = mock_open()
    result = ["USD", "EUR"]
    mock_load.return_value = {"user_currencies": result}

    assert read_json_file("", "user_currencies") == ["USD", "EUR"]


@patch("builtins.open")
@patch("json.load")
def test_read_json_file_json_decode_error(mock_load: Any, mock_open_file: Any) -> None:
    """Тестируем на неверный формат JSON"""
    mock_open_file.new = mock_open()
    mock_load.side_effect = json.JSONDecodeError("Error", "", 1)
    result = read_json_file("", "")
    assert result == []


@patch("builtins.open", side_effect=FileNotFoundError)
def test_file_not_found(mock_open_file: Any) -> None:
    """Тестируем на файл не найден"""
    mock_open_file.new = mock_open()
    result = read_json_file("wrong_path.json", "transactions")
    assert result == []
    mock_open_file.assert_called_once_with("wrong_path.json", "r", encoding="utf-8")


@patch("pandas.read_excel")
def test_get_transaction_from_excel_file_success(mock_read_excel: Any) -> None:
    """Тестируем функцию на успешную работу"""
    mock_data = pd.DataFrame({"column1": [1, 2], "column2": ["A", "B"]})
    mock_read_excel.return_value = mock_data
    result = get_transaction_from_excel_file("dummy_path.xlsx")
    expected_result = [{"column1": 1, "column2": "A"}, {"column1": 2, "column2": "B"}]
    assert result == expected_result
    mock_read_excel.assert_called_once_with("dummy_path.xlsx")


@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_get_transaction_from_excel_file_file_not_found(mock_read_excel: Any) -> None:
    result = get_transaction_from_excel_file("dummy_path.xlsx")
    assert result == [{}]
