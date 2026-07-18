# Pre-commit hooks

This extension adds lightweight quality gates so local changes are checked before they are committed.

## What it adds

- Ruff lint/format hooks
- YAML validation
- Trailing whitespace and EOF checks
- A `pre-commit` dependency for the generated project

## Install

```sh
uv sync
uv run pre-commit install
```

## Run manually

```sh
uv run pre-commit run --all-files
```

## Recommended workflow

1. Make changes.
2. Run `uv run pre-commit run --all-files`.
3. Fix any issues and commit.

Pre-commit is especially useful alongside CI so developers catch formatting and hygiene problems before pushing.
