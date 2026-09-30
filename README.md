# Campus Expense Tracker

A command-line Python application for recording personal/campus expenses, maintaining monthly category budgets, and generating spending reports.

## Overview
Campus Expense Tracker provides a simple local budgeting workflow. Expenses are stored in SQLite, users manage records from a terminal menu, and monthly reports compare spending with configured category budgets.

## Features
- Add, list, update, and delete expenses
- Filter expenses by month
- Store data locally in SQLite
- Set or update monthly category budgets
- Generate monthly spending and category summaries
- Identify the highest-spending category
- Show budget remaining or overspending status
- Validate user inputs and handle common errors
- Automated unit tests for core business logic

## Technologies
- Python 3.10+
- SQLite3 (Python standard library)
- unittest (Python standard library)
- Git / GitHub

## Setup
1. Install Python 3.10 or newer.
2. Clone the repository and open a terminal in its root.
3. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   ```
4. Activate it:
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
   - Windows CMD: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run
```bash
python main.py
```

The SQLite database is created automatically at `data/expenses.db`.

## Testing
```bash
python -m unittest discover -s tests -v
```

## Project Structure
```text
campus-expense-tracker/
├── main.py
├── requirements.txt
├── README.md
├── statement.md
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── budget_service.py
│   ├── database.py
│   ├── expense_service.py
│   ├── models.py
│   ├── report_service.py
│   └── validators.py
├── tests/
│   └── test_services.py
├── data/
│   └── .gitkeep
└── docs/
    ├── design_notes.md
    └── *.mmd
```

## Documentation
The `docs/` folder contains the architecture, workflow, use-case, class/component, sequence, and ER design sources in Mermaid format. The detailed PDF project report is supplied separately for portal submission.

## Data and Configuration
No external service is required. Each installation uses its own local SQLite database. The generated database file is ignored by Git.

## Educational Scope
This is a local educational project. It does not connect to banking services or transmit financial data over a network.
