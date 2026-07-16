# GitHub Setup

Adds GitHub Actions CI, Dependabot, issue templates, and a pull request template to a generated Python project.

## When to use

- You plan to host the project on GitHub and want CI from day one.
- You want Dependabot to keep GitHub Actions up to date.
- You want structured bug reports, feature requests, and PR descriptions without writing YAML from scratch.

Skip this extension if you use another CI provider (GitLab CI, CircleCI, etc.) — copy the workflow patterns manually instead.

## What it adds

| Path | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | Lint + test on push/PR to `main` |
| `.github/dependabot.yml` | Weekly GitHub Actions updates |
| `.github/ISSUE_TEMPLATE/` | Bug report and feature request forms |
| `.github/PULL_REQUEST_TEMPLATE.md` | Default PR description |

## CI workflow

The `ci.yml` workflow runs on push and pull requests targeting `main`:

1. Checkout
2. Install [uv](https://docs.astral.sh/uv/) via `astral-sh/setup-uv@v5` (with caching)
3. `uv python install 3.12`
4. `uv sync`
5. `uv run ruff check .`
6. `uv run pytest`

Customize steps in `.github/workflows/ci.yml` as your project grows (type checking, coverage, Docker builds, etc.).

## Usage

Apply during scaffold:

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons github-setup
```

Or add manually by copying this extension directory into an existing project.

## Verification

After pushing to GitHub:

1. Open the **Actions** tab — the CI workflow should appear.
2. Push a commit or open a PR against `main` — the **CI** workflow should run and pass.
3. Open **Issues → New issue** — bug report and feature request templates should be available.
4. Open a PR — the PR template body should pre-fill.

Locally (before pushing):

```sh
uv sync
uv run ruff check .
uv run pytest
```

These are the same commands CI runs.

## Customization

- **Python version:** Change `uv python install 3.12` to match your `pyproject.toml` `requires-python`.
- **Branches:** Edit `on.push.branches` and `on.pull_request.branches` if your default branch is not `main`.
- **Extra jobs:** Add matrix builds, deploy steps, or `uv run mypy` in separate jobs as needed.
