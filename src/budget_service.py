from typing import List, Optional
from .database import Database
from .models import Budget
from .validators import validate_amount, validate_month, validate_text


class BudgetService:
    def __init__(self, database: Database) -> None:
        self.db = database

    def set_budget(self, month: str, category: str, amount: float) -> None:
        month = validate_month(month)
        category = validate_text(category, "Category")
        amount = validate_amount(str(amount))
        with self.db._connect() as conn:
            conn.execute(
                "INSERT INTO budgets(month, category, amount) VALUES (?, ?, ?) "
                "ON CONFLICT(month, category) DO UPDATE SET amount=excluded.amount",
                (month, category, amount),
            )

    def list_budgets(self, month: Optional[str] = None) -> List[Budget]:
        if month:
            rows = self.db.execute("SELECT * FROM budgets WHERE month=? ORDER BY category", (month,), fetch=True)
        else:
            rows = self.db.execute("SELECT * FROM budgets ORDER BY month DESC, category", fetch=True)
        return [Budget(row["id"], row["month"], row["category"], row["amount"]) for row in rows]
