from typing import List, Optional
from .database import Database
from .models import Expense
from .validators import validate_amount, validate_date, validate_text


class ExpenseService:
    def __init__(self, database: Database) -> None:
        self.db = database

    def add_expense(self, amount: float, category: str, description: str, expense_date: str) -> int:
        amount = validate_amount(str(amount))
        category = validate_text(category, "Category")
        description = validate_text(description, "Description", 150)
        expense_date = validate_date(expense_date)
        return int(self.db.execute(
            "INSERT INTO expenses(amount, category, description, expense_date) VALUES (?, ?, ?, ?)",
            (amount, category, description, expense_date),
        ))

    def list_expenses(self, month: Optional[str] = None) -> List[Expense]:
        if month:
            rows = self.db.execute(
                "SELECT * FROM expenses WHERE substr(expense_date, 1, 7) = ? ORDER BY expense_date DESC, id DESC",
                (month,), fetch=True,
            )
        else:
            rows = self.db.execute("SELECT * FROM expenses ORDER BY expense_date DESC, id DESC", fetch=True)
        return [Expense(row["id"], row["amount"], row["category"], row["description"], row["expense_date"]) for row in rows]

    def get_expense(self, expense_id: int) -> Optional[Expense]:
        row = self.db.get_one("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        if not row:
            return None
        return Expense(row["id"], row["amount"], row["category"], row["description"], row["expense_date"])

    def update_expense(self, expense_id: int, amount: float, category: str, description: str, expense_date: str) -> bool:
        amount = validate_amount(str(amount))
        category = validate_text(category, "Category")
        description = validate_text(description, "Description", 150)
        expense_date = validate_date(expense_date)
        with self.db._connect() as conn:
            cursor = conn.execute(
                "UPDATE expenses SET amount=?, category=?, description=?, expense_date=? WHERE id=?",
                (amount, category, description, expense_date, expense_id),
            )
            return cursor.rowcount > 0

    def delete_expense(self, expense_id: int) -> bool:
        with self.db._connect() as conn:
            cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            return cursor.rowcount > 0
