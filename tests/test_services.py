import tempfile
import unittest
from pathlib import Path

from src.budget_service import BudgetService
from src.database import Database
from src.expense_service import ExpenseService
from src.report_service import ReportService


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        db_path = str(Path(self.temp_dir.name) / "test.db")
        self.db = Database(db_path)
        self.expenses = ExpenseService(self.db)
        self.budgets = BudgetService(self.db)
        self.reports = ReportService(self.db)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_list_expense(self):
        expense_id = self.expenses.add_expense(120, "Food", "Lunch", "2026-09-30")
        items = self.expenses.list_expenses("2026-09")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].expense_id, expense_id)
        self.assertEqual(items[0].amount, 120.0)

    def test_update_and_delete_expense(self):
        expense_id = self.expenses.add_expense(200, "Travel", "Bus", "2026-09-30")
        self.assertTrue(self.expenses.update_expense(expense_id, 250, "Travel", "Cab", "2026-09-29"))
        updated = self.expenses.get_expense(expense_id)
        self.assertEqual(updated.amount, 250.0)
        self.assertTrue(self.expenses.delete_expense(expense_id))
        self.assertIsNone(self.expenses.get_expense(expense_id))

    def test_report_and_budget_status(self):
        self.expenses.add_expense(300, "Food", "Dinner", "2026-09-01")
        self.expenses.add_expense(200, "Travel", "Metro", "2026-09-02")
        self.budgets.set_budget("2026-09", "Food", 500)
        self.budgets.set_budget("2026-09", "Travel", 150)
        report = self.reports.monthly_summary("2026-09")
        self.assertEqual(report["total"], 500.0)
        status = self.reports.budget_status("2026-09")
        travel = next(x for x in status if x["category"] == "Travel")
        self.assertEqual(travel["remaining"], -50.0)
        self.assertEqual(self.reports.top_category("2026-09"), ("Food", 300.0))

    def test_invalid_amount_is_rejected(self):
        with self.assertRaises(ValueError):
            self.expenses.add_expense(-10, "Food", "Bad data", "2026-09-30")


if __name__ == "__main__":
    unittest.main()
