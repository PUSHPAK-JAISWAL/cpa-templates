# Maintenance: Security

> How to handle security alerts, audits, and hardening in the `create-python-app` ecosystem.
>
> Read after the top-level [MAINTENANCE_RUNBOOK.md](./MAINTENANCE_RUNBOOK.md).

---

## 1. Sources of alerts

There are three main channels:

1. **GitHub Dependabot alerts** — vulnerabilities in direct and transitive dependencies.
2. **OSV-Scanner CI** — runs in `create-python-app` via `.github/workflows/osv-scanner.yml`.
3. **CodeQL alerts** — code scanning alerts in `create-python-app` and `cpa-templates`.

Check all three when doing security work:

```bash
# Dependabot alerts
gh api repos/Create-Python-App/create-python-app/dependabot/alerts --jq '.[] | {number, severity, package: .dependency.package.name, title}' | head -n 20
gh api repos/Create-Python-App/cpa-templates/dependabot/alerts --jq '.[] | {number, severity, package: .dependency.package.name, title}' | head -n 20

# CodeQL
gh code-scanning alerts list --repo Create-Python-App/create-python-app --state open
gh code-scanning alerts list --repo Create-Python-App/cpa-templates --state open
```

---

## 2. Triage

| Severity | Action |
|---|---|
| Critical / High in CLI code path | P0 — fix immediately and release |
| High in transitive dependency of a template | P1 — fix within the sprint |
| Moderate / Low | Batch with other maintenance |
| Informational only | Document and close if not actionable |

Questions to ask:

- Is the vulnerable dependency in the **CLI execution path** or only in generated projects?
- Can we bump the dependency without breaking the template/extension?
- Is the fix already available upstream on PyPI?
- Can we mitigate with `pyproject.toml` constraints while waiting for upstream?

---

## 3. Fixing in `create-python-app`

The CLI monorepo uses uv. Root-level dependency constraints can pin transitive packages across workspace members.

In the workspace root `pyproject.toml`, use `[tool.uv]` constraint overrides or bump direct dependencies, then:

```bash
uv sync --group dev
uv run pytest
uv run ruff check .
```

Document the rationale in the PR when pinning a transitive dependency for a CVE.

---

## 4. Fixing in `cpa-templates`

Templates and extensions declare dependencies in `pyproject.toml`. The fix must be in version ranges, constraint overrides, or explicit pins—not ad hoc edits in generated projects.

### 4.1 Direct dependency bump

If the vulnerable package is a direct dependency of a template or extension, bump it in that layer's `pyproject.toml`.

### 4.2 Transitive dependency override

If the vulnerable package is transitive, add an explicit pin in the owning template or extension:

```toml
[project]
dependencies = [
  "some-safe-pkg>=1.2.3",
  # Pin transitive fix until upstream releases
  "vulnerable-transitive>=2.0.1",
]
```

When uv override syntax is available in your target template, prefer documented `[tool.uv]` override fields over duplicating unrelated deps.

### 4.3 Cannot fix quickly

If no fixed version exists or the bump is breaking, open a tracking issue and document:

- The CVE or advisory ID.
- Why it cannot be fixed yet.
- The planned remediation date.

---

## 5. Running audits locally

```bash
# In create-python-app (requires pip-audit or osv-scanner)
uv run pip-audit
osv-scanner -r .

# In a generated project
cd my-app && uv run pip-audit
osv-scanner -r .

# uv may expose audit subcommands as they stabilize; prefer project docs when available
```

---

## 6. CodeQL fixes

CodeQL alerts often relate to:

- Unsafe shell command construction from environment variables or user input.
- Injection via template strings in CLI code.
- Path traversal when resolving `file://` template URLs.

### General fix pattern

- Validate and sanitize inputs before passing them to `subprocess` or shell templates.
- Prefer structured arguments (`subprocess.run` with a list) over string shell commands.
- Avoid interpolating user-controlled values directly into commands or file paths.

If an alert is a false positive, dismiss it with a comment explaining why.

---

## 7. Validation

After any security change:

1. Run the relevant audit command until the alert is gone or mitigated.
2. Run the normal CI checks (`pytest`, `ruff`, type-check).
3. For `cpa-templates`: scaffold the affected template + extensions and validate.
4. For `create-python-app`: run the full test suite and security workflows when possible.

---

## 8. Checklist

- [ ] Alert has been triaged and prioritized.
- [ ] Fix is minimal and scoped.
- [ ] Audit no longer reports the vulnerability (or it is documented as unfixable).
- [ ] CI passes.
- [ ] Generated projects still install, lint, and test.
- [ ] A release tag is planned if the fix affects a published PyPI package.
