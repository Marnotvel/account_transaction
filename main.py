import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Currency:
    name: str
    code: str


@dataclass
class OperationAmount:
    amount: float
    currency: Currency

@dataclass
class Operation:
    id: int
    state: str
    date: datetime
    operation_amount: OperationAmount
    description: str
    from_account: Optional[str] = None
    to_account: Optional[str] = None


def operation_from_dict(data: dict) -> Operation:
    if data == {}:
        return None
    currency = Currency(name=data["operationAmount"]["currency"]["name"], code=data["operationAmount"]["currency"]["code"])
    operation_amount = OperationAmount(amount=float(data["operationAmount"]["amount"]), currency=currency)
    date = datetime.fromisoformat(data["date"])
    return Operation(
        id=data["id"],
        state=data["state"],
        date=date,
        operation_amount=operation_amount,
        description=data["description"],
        from_account=data.get("from"),
        to_account=data.get("to")
    )

def mask_card_number(card_number: str) -> str:
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

def mask_account_number(account_number: str) -> str:
    return f"**{account_number[-4:]}"

def print_last_operations(operations: List[Operation], n: int = 5):
    executed_operations = [op for op in operations if op != None and op.state == "EXECUTED"]
    executed_operations.sort(key=lambda op: op.date, reverse=True)
    
    for op in executed_operations[:n]:

        formatted_date = op.date.strftime("%d.%m.%Y")
        

        description = op.description
        
        if(op.from_account):
            fr = op.from_account.split()
            if len(fr) > 2:
                fr = [' '.join(fr[:-1]), fr[-1]]
            to = op.to_account.split()
            if len(to) > 2:
                to = [' '.join(to[:-1]), to[-1]]
        else:
            fr = "  "
            to = "  "

        from_account = (fr[0] + " " + mask_card_number(fr[1])) if op.from_account and len(op.from_account) > 6 else mask_account_number(fr[1]) if op.from_account else ""
        to_account = (to[0] + " " + mask_card_number(to[1])) if op.to_account and len(op.to_account) > 6 else mask_account_number(to[1]) if op.to_account else ""
        

        print(f"{formatted_date} {description}")
        if from_account and to_account:
            print(f"{from_account} -> {to_account}")
        elif to_account:
            print(f"{to_account}")
        print(f"{op.operation_amount.amount} {op.operation_amount.currency.name}\n")

with open("operations.json", "r", encoding="utf-8") as file:
    operations_data = json.load(file)
    
    operations = [operation_from_dict(item) for item in operations_data]

print_last_operations(operations)
