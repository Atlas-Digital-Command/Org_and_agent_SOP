# Contributing

Thanks for considering a contribution. This project ships a small, opinionated framework — contributions that fit the philosophy land quickly; ones that don't, less so. Please skim this file before opening a PR.

## Philosophy

A few principles that shape every decision here:

1. **Lean wins by default.** When in doubt, the framework should generate the shortest workable SOP, not the most thorough. Compliance and depth scale up *only* when the org profile explicitly demands them.
2. **Governance over scripts.** Workflows are expressed as natural language with RFC 2119 constraints (`MUST`, `SHOULD`, `MAY`), never as rigid procedural code that fights the agent's reasoning.
3. **Overlay, never override.** Your organization's specifics live in a private overlay. The public framework never assumes who you are.
4. **Brand-neutral inside, attributed outside.** Subagents, slash commands, and skill names contain no organization branding. Atlas attribution lives in `README.md`, `NOTICE`, and `plugin.json` only.

If your contribution conflicts with one of these, surface that in the PR description so we can discuss before you invest time.

## What we welcome

| Type of contribution | Path to merge |
|---|---|
| Bug fix in existing code or skill | Open a PR; small fixes merge fast |
| New exporter (e.g., Confluence, GDocs) | Open an issue first to discuss interface; then PR |
| New service line under an existing pillar | Open an issue with the proposed scope; if approved, PR with skill + tests + example |
| **New pillar** (top-level) | Open an issue for design review *before* writing code. New pillars go through a stricter review (see below) |
| New archetype | Open an issue; archetypes are foundational and we'll want to review the dimensional framing carefully |
| Doc improvements | Open a PR directly |
| Refactor / cleanup | Open an issue first if it touches more than one module |

## New-pillar review checklist

New top-level pillars (peers of `strategy`, `branding`, `website`, `acquisition`, `retention`, `agentic-ai`) get reviewed against the following before acceptance:

- [ ] **Non-overlapping.** Does this pillar carve out work that genuinely doesn't fit under existing ones?
- [ ] **Service-line list.** Does it include at least 2 concrete service lines, with clear naming?
- [ ] **Skill structure.** Does each service line ship a `SKILL.md` with progressive-disclosure references?
- [ ] **Example SOP per service line.** Is there at least one end-to-end example SOP per service line in all three archetypes?
- [ ] **Tool-agnostic.** Does the pillar avoid hardcoding a specific vendor (e.g., "Klaviyo email" → "ESP for transactional email")?
- [ ] **Brand-neutral language.** No organization names except in `examples/<org>-public/`?
- [ ] **RACI examples.** Does the pillar's example SOPs cover the role-mapping vocabulary clearly?
- [ ] **Tests.** Unit tests for the new skill loader paths, plus a validation pass with `validate-sop.sh`.

A maintainer will mark these off in the PR before approval.

## New service line under an existing pillar

Lighter-touch review:

- [ ] Service line name follows kebab-case
- [ ] Has its own folder under the pillar's `skills/`
- [ ] Ships at least one example SOP in `examples/*/`
- [ ] Doesn't duplicate an existing service line under another pillar

## Code style

- Python 3.11+. Type hints required on public functions.
- Format with `ruff format`. Lint with `ruff check`.
- No new runtime dependencies without discussion.
- Tests use `pytest`. Aim for 80%+ coverage on new code.

## SOP / skill style

- All `.sop.md` files MUST validate via `agent-sops/validate-sop.sh`.
- All skill `SKILL.md` files MUST include frontmatter (`name`, `description`).
- Negative constraints (`MUST NOT`, `SHOULD NOT`) MUST include reasoning (`...because <reason>`).
- Use Mermaid for all diagrams. No ASCII art.

## Commit / PR conventions

- Conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`).
- One logical change per PR.
- PRs against `main`. Rebase or squash-merge — no merge commits.
- Reference the issue: `Closes #123`.

## Local development

```bash
git clone https://github.com/Atlas-Digital-Command/Org_and_agent_SOP.git
cd Org_and_agent_SOP

python -m venv .venv
. .venv/bin/activate           # or: .venv\Scripts\activate on Windows

pip install -e ".[dev]"
pytest
```

To dogfood while developing:

```bash
sop-agent onboard --overlay ./examples/lean-operator
sop-agent new "Quarterly content audit" --overlay ./examples/lean-operator
```

## Reporting bugs and security issues

- Bugs: open a GitHub issue with the bug template.
- Security issues: email security@atlasdigitalusa.com — do **not** open a public issue.

## Code of conduct

See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md). Be kind, be specific, assume good faith.
