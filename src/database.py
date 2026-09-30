import sqlite3
from pathlib import Path
from typing import Iterable, Optional


class Database:
    def __init__(self, db_path: str = "data/expenses.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL CHECK(amount > 0),
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    expense_date TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    month TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    UNIQUE(month, category)
                );
                """
            )

    def execute(self, query: str, params: Iterable = (), fetch: bool = False):
        with self._connect() as conn:
            cursor = conn.execute(query, tuple(params))
            if fetch:
                return cursor.fetchall()
            return cursor.lastrowid

    def get_one(self, query: str, params: Iterable = ()) -> Optional[sqlite3.Row]:
        rows = self.execute(query, params, fetch=True)
        return rows[0] if rows else None
