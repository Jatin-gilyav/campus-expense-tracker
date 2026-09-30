# Design Notes

## Architecture
The application uses a small layered structure. `app.py` handles command-line interaction, service classes contain business operations, `validators.py` centralizes input checks, and `database.py` isolates SQLite access.

## Functional Modules
1. Expense Management - create, read, update, and delete expense records.
2. Budget Management - set or update a monthly category budget.
3. Reporting & Analytics - calculate monthly totals, category summaries, top category, and budget status.

## Non-Functional Requirements
1. **Usability:** the application exposes a numbered terminal menu and readable messages.
2. **Reliability:** invalid inputs are caught and reported without crashing the main loop.
3. **Maintainability:** responsibilities are separated into focused modules and service classes.
4. **Resource efficiency:** SQLite is used locally, avoiding a separate database server for a small personal dataset.
5. **Data integrity:** SQLite constraints prevent non-positive monetary values, while service-level validation checks user input.

## Technical Decisions
- SQLite was selected because it is included with Python, persists data, and does not require a separate server.
- Dataclasses represent domain objects with minimal boilerplate.
- Service classes keep database details separate from the command-line interface.
- Standard-library `unittest` avoids unnecessary third-party testing dependencies.
