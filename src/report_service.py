from typing import Dict, List
from .database import Database


class ReportService:
    def __init__(self, database: Database) -> None:
        self.db = database

    def monthly_summary(self, month: str) -> Dict[str, float]:
        rows = self.db.execute(
            "SELECT category, SUM(amount) AS total FROM expenses WHERE substr(expense_date,1,7)=? GROUP BY category ORDER BY total DESC",
            (month,), fetch=True,
        )
        by_category = {row["category"]: round(float(row["total"]), 2) for row in rows}
        total = round(sum(by_category.values()), 2)
        return {"total": total, "by_category": by_category}

    def budget_status(self, month: str) -> List[Dict[str, float]]:
        budget_rows = self.db.execute("SELECT category, amount FROM budgets WHERE month=? ORDER BY category", (month,), fetch=True)
        result = []
        for row in budget_rows:
            spent_row = self.db.get_one(
                "SELECT COALESCE(SUM(amount), 0) AS spent FROM expenses WHERE substr(expense_date,1,7)=? AND category=?",
                (month, row["category"]),
            )
            spent = round(float(spent_row["spent"]), 2)
            budget = round(float(row["amount"]), 2)
            result.append({"category": row["category"], "budget": budget, "spent": spent, "remaining": round(budget - spent, 2)})
        return result

    def top_category(self, month: str):
        summary = self.monthly_summary(month)["by_category"]
        return max(summary.items(), key=lambda item: item[1]) if summary else None
