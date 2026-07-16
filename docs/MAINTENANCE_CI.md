# Maintenance: CI and Workflows

> How to diagnose, fix, and extend the CI workflows that validate the `create-python-app` ecosystem.
>
> Read after the top-level [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md).

---

## 1. Workflows overview

### `create-python-app`

| Workflow | Purpose |
|---|---|
| `test.yml` | Unit and integration tests |
| `type-check.yml` | Static type checking |
| `lint.yml` | Ruff and formatting checks |
| `mega-linter.yml` | MegaLinter across the repo |
| `osv-scanner.yml` | Security scanning |
| `publish.yml` | Tag-triggered PyPI release |
| `smoke-distribution.yml` | End-to-end install smoke tests |
| `pr-review.yml` | PR automation |

### `cpa-templates`

| Workflow | Purpose |
|---|---|
| `smoke-test.yml` | Quick end-to-end smoke tests on PRs (scaffold + `uv sync` + ruff + pytest) |
| `test-combinations.yml` | Random + full matrix of template × extension combinations |

---

## 2. Reading CI failures

Always start with the failed logs:

```bash
gh run view <run-id> --repo Create-Python-App/<repo> --log-failed
```

For long logs, filter:

```bash
gh run view <run-id> --repo Create-Python-App/<repo> --log-failed | grep -iE "error|fail|cannot|unable|resolution"
```

List recent runs:

```bash
gh run list --repo Create-Python-App/<repo> --limit 20
```

---

## 3. Running workflows manually

```bash
# cpa-templates smoke test
gh workflow run "Smoke Test" \
  --repo Create-Python-App/cpa-templates --ref main

# cpa-templates random + full matrix
gh workflow run "Test Template and Extension Combinations" \
  --repo Create-Python-App/cpa-templates --ref main

# Watch until it finishes
gh run watch <run-id> --repo Create-Python-App/cpa-templates --exit-status

# create-python-app tests
gh workflow run "Tests" --repo Create-Python-App/create-python-app --ref main
```

Use `--ref <branch>` to test a PR branch before merging.

---

## 4. The `smoke-test.yml` workflow

This workflow runs on every PR to `main`. It:

1. Checks out `cpa-templates` and `create-python-app`.
2. Installs the CLI from PyPI (falls back to source checkout).
3. Scaffolds `fastapi-starter` with selected extensions via `file://` URLs.
4. Runs `uv sync`, `uv run ruff check .`, and `uv run pytest -q`.

### 4.1 Matrix cases

The workflow matrix covers template-only and common single-extension combinations. When adding a new extension, add a matrix row if it should be smoke-tested on every PR.

### 4.2 Common failures

| Symptom | Likely cause |
|---|---|
| Scaffold step fails | Invalid `templates.json`, broken `file://` path, CLI regression |
| `uv sync` fails | Conflicting `pyproject.toml` merge or bad version pin |
| `ruff check` fails | Generated code or extension files violate lint rules |
| `pytest` fails | Broken template tests or missing env defaults |

Reproduce locally using the commands in [docs/TESTING.md](./TESTING.md).

---

## 5. The `test-combinations.yml` generator

This workflow is the deepest validation layer. It mirrors the CNA pattern and has four jobs:

1. `generate-combinations` — builds a JSON matrix of random, non-conflicting combinations.
2. `test-combinations` — runs the random matrix.
3. `generate-full-matrix` — builds a JSON matrix of every template with **all** compatible extensions.
4. `test-full-matrix` — runs the full matrix.

### 5.1 Random matrix logic

For each template:

- Filter compatible extensions by `type`.
- Group by `category`.
- Pick one random extension per category.
- Skip any extension that conflicts with already-selected ones (`incompatibleWith`).

### 5.2 Full matrix logic

For each template:

- Filter compatible extensions by `type`.
- Add every mutually-compatible extension to a single job per template.

This is the worst-case scenario and catches dependency blowups when all extensions merge into one `pyproject.toml`.

### 5.3 Validation steps per job

Each combination typically:

1. Scaffolds with `CI=true` and `file://` URLs.
2. Runs `uv sync`.
3. Runs `uv run ruff check .` when ruff is configured.
4. Runs `uv run pytest -q` when tests exist.

---

## 6. Common workflow failures

### 6.1 Syntax error in embedded generator script

**Cause:** The Python or shell script embedded in the YAML has a duplicate function or variable declaration, or invalid heredoc escaping.

**Fix:** Remove the duplicate or fix escaping in `.github/workflows/test-combinations.yml`.

When the generator uses JavaScript (CNA parity), validate Node blocks locally before pushing—see section 7.

### 6.2 Empty `templateUrl` like `file://?subdir=templates/`

**Cause:** Escaped template variables (`\${repoDir}`, `\${tplDir}`) are passed as literal strings instead of being interpolated by the embedded script.

**Fix:** Use `${repoDir}` and `${tplDir}` without backslashes. GitHub Actions does not interpolate `${...}`, only `${{ ... }}`, so the heredoc receives raw `${repoDir}` text that Node evaluates correctly.

### 6.3 `uv sync` resolution errors

See [MAINTENANCE_DEPENDENCIES.md](./MAINTENANCE_DEPENDENCIES.md).

### 6.4 Full matrix passes but random fails (or vice versa)

This usually means:

- The random matrix hit an unlucky combination not covered by the all-at-once full matrix.
- The full matrix selects all extensions, shadowing a per-extension failure.

Re-run the exact combination locally using the failed job's `templateUrl` and `extensions`.

---

## 7. Testing embedded generator scripts locally

When `test-combinations.yml` embeds Node code inside `<<EOF` heredocs, validate syntax before pushing:

```bash
node - <<'PY'
const fs = require('fs');
const txt = fs.readFileSync('.github/workflows/test-combinations.yml', 'utf8');
let idx = 0;
for (const match of txt.matchAll(/node <<EOF\n([\s\S]*?)\n          EOF/g)) {
  let code = match[1].replace(/^          /gm, '');
  code = code.replace(/\\\`/g, '`').replace(/\\\$/g, '$');
  try {
    new Function(code);
    console.log(`Block ${idx}: OK`);
  } catch (e) {
    console.error(`Block ${idx}: SYNTAX ERROR — ${e.message}`);
    process.exit(1);
  }
  idx++;
}
PY
```

Run this from the `cpa-templates` root.

---

## 8. Modifying a workflow safely

1. Make the change in a branch.
2. Run the syntax validator above when the workflow embeds generator scripts.
3. Push and open a PR.
4. Run the workflow manually on the branch if possible:
   ```bash
   gh workflow run "Smoke Test" \
     --repo Create-Python-App/cpa-templates --ref <branch>
   gh workflow run "Test Template and Extension Combinations" \
     --repo Create-Python-App/cpa-templates --ref <branch>
   ```
5. Merge only after the manual run succeeds.

---

## 9. Checklist

- [ ] Embedded generator scripts pass local syntax validation.
- [ ] Workflow YAML is valid (visual check or YAML linter).
- [ ] Manual workflow run on the branch passes.
- [ ] The full matrix is green for risky changes.
- [ ] Changes do not introduce new secret exposure or permissions escalation.
