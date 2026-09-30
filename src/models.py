from dataclasses import dataclass
from typing import Optional


@dataclass
class Expense:
    expense_id: Optional[int]
    amount: float
    category: str
    description: str
    expense_date: str


@dataclass
class Budget:
    budget_id: Optional[int]
    month: str
    category: str
    amount: float
