# Pre-commit (extension bank)

Maintainer-facing notes for the **all-pre-commit** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `.pre-commit-config.yaml` | Hooks for Ruff, YAML validation, whitespace, and EOF checks |
| `pyproject.toml` | Adds the `pre-commit` dependency |
| `docs/PRE_COMMIT_GUIDE.md` | Local usage, install steps, and verification |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons pre-commit \
  --yes
```

## Verify after scaffold

```sh
uv sync
uv run pre-commit install
uv run pre-commit run --all-files
```

See `template/docs/PRE_COMMIT_GUIDE.md` for the full workflow and troubleshooting notes.
