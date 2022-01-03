# past - a Python AST experiment

![past](past.png)

Simple experimental linter showing how you might go about building something like [flake8](https://github.com/pycqa/flake8).

## Setup and usage

With [poetry](https://python-poetry.org/) installed:

```bash
poetry install
poetry shell

# Lint a file
past file_you_want_to_lint.py

# Run the unit tests
pytest -vvv
```

---

[![codecov](https://codecov.io/gh/lucasmelin/past/branch/main/graph/badge.svg?token=NGCH824FON)](https://codecov.io/gh/lucasmelin/past)