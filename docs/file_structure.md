# Project Directory Structure

This document describes the directory structure for the Simple Stock Strategy Backtester (S3B) project. It is kept up-to-date with the codebase and should be referenced for any architectural or onboarding questions.

## Root Directories

- `src/` — Source code for all modules and business logic.
    - `__init__.py` — Ensures the directory is recognized as a Python package.
- `configs/` — Configuration files for strategies, data sources, and environment settings.
    - `README.md` — Placeholder and documentation for configuration conventions.
- `tests/` — All pytest-based tests for business logic and modules.
    - `__init__.py` — Ensures the directory is recognized as a Python package.
- `docs/` — Project documentation (including this file, codebase overview, PRD, and tasks).

## Notes
- Each directory contains a placeholder file to ensure it is tracked in version control.
- All code and documentation changes must be reflected here and in docs/codebase_overview.md.
- If you add, remove, or rename directories, update this file immediately.
