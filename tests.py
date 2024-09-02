import pytest
from datetime import datetime
from io import StringIO
from dataclasses import dataclass
from typing import Optional, List

from main import Currency, OperationAmount, Operation, mask_card_number, mask_account_number, print_last_operations


operations = [
    Operation(
        id=1,
        state="EXECUTED",
        date=datetime(2018, 10, 14),
        operation_amount=OperationAmount(amount=82771.72, currency=Currency(name="руб.", code="RUB")),
        description="Перевод организации",
        from_account="Visa Platinum 700079******6361",
        to_account="Счет **9638"
    ),
    Operation(
        id=2,
        state="EXECUTED",
        date=datetime(2019, 8, 10),
        operation_amount=OperationAmount(amount=12345.67, currency=Currency(name="USD", code="USD")),
        description="Оплата услуг",
        from_account="MasterCard 123456******7890",
        to_account="Счет **1234"
    ),
    Operation(
        id=3,
        state="CANCELLED",
        date=datetime(2020, 1, 1),
        operation_amount=OperationAmount(amount=98765.43, currency=Currency(name="EUR", code="EUR")),
        description="Неудачная операция",
        from_account="Visa Classic 111122******3333",
        to_account="Счет **4444"
    ),
]

def test_mask_card_number():
    assert mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert mask_card_number("6543210987654321") == "6543 21** **** 4321"

def test_mask_account_number():
    assert mask_account_number("1234567890") == "**7890"
    assert mask_account_number("9876543210") == "**3210"

def test_print_last_operations(capsys):
    
    expected_output = (
        "10.08.2019 Оплата услуг\n"
        "MasterCard 1234 56** **** 7890 -> Счет **1234\n"
        "12345.67 USD\n\n"
        "14.10.2018 Перевод организации\n"
        "Visa Platinum 7000 79** **** 6361 -> Счет **9638\n"
        "82771.72 руб.\n\n"
    )

    
    print_last_operations(operations, n=5)

   
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_empty_operations(capsys):
    
    print_last_operations([], n=5)
    captured = capsys.readouterr()
    assert captured.out == ""

def test_operations_with_cancelled(capsys):
    
    executed_operations = [op for op in operations if op.state == "EXECUTED"]

    print_last_operations(executed_operations, n=5)
    captured = capsys.readouterr()
    
    
    assert "Неудачная операция" not in captured.out

