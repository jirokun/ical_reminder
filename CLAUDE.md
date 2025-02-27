# Development Guidelines

## Commands
- Run script: `python cal.py`
- Install dependencies: `uv add -r requirements.txt` (when created)
- Run tests: `uv run pytest test_*.py`
- Run single test: `uv run pytest test_file.py::test_function_name -v`
- Type check: `mypy *.py`
- Lint: `uv run ruff check *.py`
- Format: `uv run ruff format *.py`

## Code Style
- **Imports**: Standard library first, then third-party, then local modules (grouped by blank lines)
- **Docstrings**: All functions and modules should have docstrings using triple quotes
- **Type hints**: Use type hints for function parameters and return values
- **Naming**: 
  - snake_case for functions, variables, and modules
  - CamelCase for classes
  - UPPER_CASE for constants
- **Error handling**: Use try/except blocks with specific exception types
- **Line length**: Maximum 100 characters
- **Function length**: Keep functions focused and under 50 lines where possible
- **Comments**: Comments explain "why", code explains "how"