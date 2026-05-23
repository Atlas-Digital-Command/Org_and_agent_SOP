# Roadmap

A phased build plan. Each phase ends with a working, demonstrable artifact — no half-finished scaffolding lingering between phases.

## Phase 0 — Scaffold ✅ in progress

**Goal:** A repo someone can clone, install, and inspect — even though nothing real runs yet.

- [x] Apache-2.0 LICENSE + NOTICE
- [x] `.gitignore` with overlay protection
- [x] Top-level directory structure
- [x] README, CONTRIBUTING, CODE_OF_CONDUCT
- [x] GitHub issue + PR templates
- [x] Claude Code plugin manifest
- [x] `pyproject.toml` with CLI entry point
- [x] `governance/` and `org-map/` schemas
- [x] Python package skeleton + overlay loader + tests for the loader
- [x] Roadmap + architecture docs
- [ ] Initial commit + push

**Demonstrable:** `pip install -e .` works. `sop-agent --version` returns. `sop-agent overlay` correctly resolves overlay precedence. `pytest` passes.

---

## Phase 1 — Atlas-complete (privately)

**Goal:** End-to-end SOP generation working for one pillar, validated against Atlas's real governance overlay.

- [ ] Conductor agent definition (the top-level orchestrator)
- [ ] Three foundational subagents:
  - [ ] Governance Validator — checks drafts against governance/
  - [ ] SOP Author — produces the human-facing Markdown
  - [ ] QA Evaluator — scores against rubric, blocks on fail
- [ ] Three meta-SOPs (`.sop.md`):
  - [ ] `new-sop.sop.md` — the canonical "create an SOP" workflow
  - [ ] `onboard-org.sop.md` — the onboarding interview
  - [ ] `audit-sop.sop.md` — review and refresh an existing SOP
- [ ] One pillar fully fleshed out: **Acquisition → SEO** (proof slice)
  - [ ] `skills/acquisition/seo/SKILL.md`
  - [ ] Pillar-specialist subagent for Acquisition
  - [ ] Tool category reference
- [ ] Output template: `templates/sop-employee.md.j2`
- [ ] Real CLI wired:
  - [ ] `sop-agent onboard` runs the onboarding subagent
  - [ ] `sop-agent new <description>` runs the full Conductor flow
  - [ ] `sop-agent validate <path>` runs the format checker
- [ ] Three example tenants populated:
  - [ ] `examples/lean-operator/`
  - [ ] `examples/coordinated-specialist/`
  - [ ] `examples/compliance-forward/`
- [ ] Atlas overlay populated privately (not committed)
- [ ] Generate 5-10 real Atlas SOPs as dogfooding

**Demonstrable:** Atlas runs `sop-agent new "Monthly technical SEO audit"` and gets a usable SOP shaped to its archetype.

---

## Phase 2 — All pillars + public launch

**Goal:** Ship publicly with full coverage of the six pillars.

- [ ] Five additional pillar specialists (strategy, branding, website, retention, agentic-ai)
- [ ] All service-line skills filled in
- [ ] Tool Mapper subagent
- [ ] Org Mapper subagent with gap analysis
- [ ] `examples/atlas-public/` — 2-3 sanitized real Atlas SOPs for credibility
- [ ] PDF exporter (`weasyprint`)
- [ ] CI pipeline (tests + lint + skill validation on every PR)
- [ ] Publish to:
  - [ ] PyPI as `sop-agent`
  - [ ] Claude Code marketplace via this repo
- [ ] Announce (Atlas blog, Reddit r/AI_Agents, HN Show)

**Demonstrable:** Anyone can `pip install sop-agent` and generate SOPs for their org.

---

## Phase 3 — Visual renderer

**Goal:** Scribe-style step-by-step visuals as an opt-in feature.

- [ ] `pip install sop-agent[visual]` brings in Playwright + Pillow
- [ ] Visual Renderer subagent
- [ ] Sandboxed Chromium execution
- [ ] Screenshot annotation pipeline
- [ ] Mermaid diagram renderer for non-visual SOPs
- [ ] HTML exporter for self-hosted Scribe-style viewing

**Demonstrable:** An SOP with the `visual: true` flag generates a Scribe-style HTML walkthrough with screenshots.

---

## Phase 4 — Exporter expansion + steady state

**Goal:** Meet teams where their docs already live.

- [ ] Notion exporter (`pip install sop-agent[exporters-notion]`)
- [ ] Confluence exporter
- [ ] Google Docs exporter
- [ ] ClickUp doc exporter
- [ ] Webhook + REST export targets

**Then:** triage incoming issues, review pillar/service contributions, maintain.

---

## Non-goals (explicit)

To prevent scope creep:

- ❌ A hosted SaaS version (the framework is OSS; users run it themselves)
- ❌ A web UI for editing SOPs (use Nimbalyst, Cursor, or any markdown editor)
- ❌ Real-time multi-user editing
- ❌ Built-in billing, auth, or tenant isolation
- ❌ Replacing existing knowledge-base tools (we export *into* them, not over them)
- ❌ Generating compliance attestations (we can reference compliance frameworks, not certify against them)
