from datetime import date
from .budget_service import BudgetService
from .database import Database
from .expense_service import ExpenseService
from .report_service import ReportService
from .validators import validate_amount, validate_month


class ExpenseTrackerApp:
    def __init__(self, db_path: str = "data/expenses.db") -> None:
        db = Database(db_path)
        self.expenses = ExpenseService(db)
        self.budgets = BudgetService(db)
        self.reports = ReportService(db)

    def run(self) -> None:
        print("\n=== Campus Expense Tracker ===")
        while True:
            self._menu()
            choice = input("Choose an option: ").strip()
            try:
                if choice == "1": self._add_expense()
                elif choice == "2": self._list_expenses()
                elif choice == "3": self._update_expense()
                elif choice == "4": self._delete_expense()
                elif choice == "5": self._set_budget()
                elif choice == "6": self._show_report()
                elif choice == "7": self._show_budget_status()
                elif choice == "8": print("Goodbye!"); return
                else: print("Invalid choice. Please select 1-8.")
            except (ValueError, TypeError) as exc:
                print(f"Error: {exc}")

    @staticmethod
    def _menu() -> None:
        print("\n1. Add expense\n2. List expenses\n3. Update expense\n4. Delete expense\n5. Set/update budget\n6. Monthly report\n7. Budget status\n8. Exit")

    def _add_expense(self) -> None:
        amount = validate_amount(input("Amount (INR): "))
        category = input("Category: ")
        description = input("Description: ")
        expense_date = input(f"Date [YYYY-MM-DD, default {date.today()}]: ").strip() or str(date.today())
        expense_id = self.expenses.add_expense(amount, category, description, expense_date)
        print(f"Expense added with ID {expense_id}.")

    def _list_expenses(self) -> None:
        month = input("Filter month YYYY-MM (blank for all): ").strip() or None
        if month: validate_month(month)
        items = self.expenses.list_expenses(month)
        if not items:
            print("No expenses found."); return
        print("\nID | Date       | Category        | Amount (INR) | Description")
        print("-" * 72)
        for item in items:
            print(f"{item.expense_id:>2} | {item.expense_date} | {item.category:<15} | {item.amount:>12.2f} | {item.description}")

    def _update_expense(self) -> None:
        expense_id = int(input("Expense ID: "))
        existing = self.expenses.get_expense(expense_id)
        if not existing:
            print("Expense not found."); return
        amount = input(f"Amount [{existing.amount}]: ").strip() or str(existing.amount)
        category = input(f"Category [{existing.category}]: ").strip() or existing.category
        description = input(f"Description [{existing.description}]: ").strip() or existing.description
        expense_date = input(f"Date [{existing.expense_date}]: ").strip() or existing.expense_date
        updated = self.expenses.update_expense(expense_id, validate_amount(amount), category, description, expense_date)
        print("Expense updated." if updated else "Expense not found.")

    def _delete_expense(self) -> None:
        expense_id = int(input("Expense ID: "))
        deleted = self.expenses.delete_expense(expense_id)
        print("Expense deleted." if deleted else "Expense not found.")

    def _set_budget(self) -> None:
        month = validate_month(input("Month YYYY-MM: ").strip())
        category = input("Category: ")
        amount = validate_amount(input("Budget amount (INR): "))
        self.budgets.set_budget(month, category, amount)
        print("Budget saved.")

    def _show_report(self) -> None:
        month = validate_month(input("Month YYYY-MM: ").strip())
        summary = self.reports.monthly_summary(month)
        print(f"\nMonthly report for {month}")
        print(f"Total spending: INR {summary['total']:.2f}")
        if not summary["by_category"]:
            print("No spending recorded."); return
        for category, total in summary["by_category"].items(): print(f"- {category}: INR {total:.2f}")
        top = self.reports.top_category(month)
        if top: print(f"Top category: {top[0]} (INR {top[1]:.2f})")

    def _show_budget_status(self) -> None:
        month = validate_month(input("Month YYYY-MM: ").strip())
        statuses = self.reports.budget_status(month)
        if not statuses:
            print("No budgets found for this month."); return
        print(f"\nBudget status for {month}")
        for item in statuses:
            status = "OVER" if item["remaining"] < 0 else "OK"
            print(f"{item['category']}: budget INR {item['budget']:.2f}, spent INR {item['spent']:.2f}, remaining INR {item['remaining']:.2f} [{status}]")
