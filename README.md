<div align="center">

# SOP Agent

**An open-source agent framework that authors high-quality Standard Operating Procedures for the people who actually do the work.**

Built on the [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk) · Distributed as a Claude Code plugin + Python CLI · Apache-2.0 licensed

</div>

---

## What this is

Most "SOP generators" produce shelfware: bloated procedural documents nobody reads. This framework takes the opposite approach.

The SOP Agent interviews your organization, learns your services, roles, tools, and brand voice, then authors SOPs sized to how your team actually operates. A 6-person lean agency gets a one-page action checklist. A 200-person compliance-forward firm gets a full RACI with risk register and audit trail. Same framework, output shaped to fit.

It is governance-first (rules apply across every SOP it produces), department-aware (six service pillars covering modern digital-services work), and role-conscious (it flags when your proposed workflow needs a hire you don't have).

## Quick start

> Requires Python 3.11+ and either the Claude Code CLI or an Anthropic API key.

```bash
# Install via pip
pip install sop-agent

# Or install as a Claude Code plugin
claude plugin marketplace add Atlas-Digital-Command/Org_and_agent_SOP
claude plugin install sop-agent
```

First run kicks off an onboarding interview that builds your `governance/` and `org-map/` content:

```bash
sop-agent onboard
```

After onboarding, generate an SOP:

```bash
sop-agent new "Monthly technical SEO audit for ecommerce clients"
```

In Claude Code, the same flow is available as slash commands:

```
/sop-onboard
/sop-new Monthly technical SEO audit for ecommerce clients
```

## The overlay pattern — keep your real org content private

Your governance, role map, tool inventory, and brand voice are *yours*. They don't belong in a public fork.

The framework loads an **overlay** at runtime in this resolution order:

1. `--overlay <path>` flag (explicit, wins)
2. `$SOP_AGENT_OVERLAY` environment variable
3. `~/.sop-agent/overlay/` (auto-discovered)
4. None → falls back to the bundled `examples/` archetypes

Your overlay folder is structured the same as the repo's `governance/` and `org-map/` directories. You can keep it in a private Git repo, a synced folder, or just locally. Nothing under any of those paths is ever committed to this repo (the `.gitignore` enforces it).

```bash
# Atlas's pattern
sop-agent new "Brand voice audit" --overlay ~/atlas-overlay/

# Or set once
export SOP_AGENT_OVERLAY=~/atlas-overlay
sop-agent new "Brand voice audit"
```

## The three archetypes

When the agent generates an SOP, it sizes the output to match how your team actually works. The scale runs along a single axis:

```
Directness + Efficiency  ←———————————————————————→  Compliance + Thoroughness
```

| | **A. Lean Operator** | **B. Coordinated Specialist** | **C. Compliance-Forward** |
|---|---|---|---|
| Role multiplicity | Generalists wear many hats | Light specialization | Deep specialization |
| Hands per deliverable | 1–2 | 2–4 | 4+ |
| Approval depth | Single decider | Department lead | Multi-tier (analyst → lead → director) |
| Compliance posture | None | Vendor / client SLAs | SOC 2 / HIPAA / ISO active |
| Version control | Whoever updated last | Lightweight changelog | Formal audit trail |
| Onboarding cadence | Rare | Quarterly | Monthly or weekly |
| **SOP format** | ≤1 pg action checklist | ~2 pp w/ light RACI + KPIs | ~5 pp full RACI + risk register + change-mgmt + appendices |

When your overlay is ambiguous, the agent defaults to **A (Lean)**. It scales up only when your governance or the SOP's subject matter demands it — the opposite of how most SOP tooling behaves.

A full reference implementation of each archetype lives in [`examples/`](./examples).

## Architecture overview

```
governance/         (your design + measurement principles, brand voice, tool inventory)
       │
       ▼
  [Conductor agent]  ← user request enters here
       │
       ├─► Pillar specialists (6: strategy, branding, website, acquisition, retention, agentic-ai)
       ├─► Org-mapper (matches steps to your roles, flags hiring gaps)
       ├─► Tool-mapper (matches steps to your stack)
       ├─► Governance validator (checks every draft against the rules)
       └─► QA evaluator (scores against rubric; blocks on fail)
       │
       ▼
  [SOP author]  +  [Visual renderer]  ← run in parallel
       │
       ▼
  Output: Markdown / PDF / HTML / Notion / Confluence
```

Each subagent runs in its own isolated context per the Claude Agent SDK's parallel-execution pattern. See [`docs/architecture.md`](./docs/architecture.md) for the full picture.

## What's in the box

| Directory | Purpose |
|---|---|
| [`.claude-plugin/`](./.claude-plugin) | Claude Code plugin manifest |
| [`agents/`](./agents) | Subagent definitions (conductor, validators, pillar specialists) |
| [`agent-sops/`](./agent-sops) | Meta-SOPs — the workflows the agent itself follows |
| [`skills/`](./skills) | Progressive-disclosure knowledge packs per pillar / service line |
| [`templates/`](./templates) | Human-output templates (Markdown, Mermaid, HTML) |
| [`governance/`](./governance) | Schema for your private overlay (empty by default) |
| [`org-map/`](./org-map) | Schema for your role + RACI overlay (empty by default) |
| [`examples/`](./examples) | Three reference archetypes + sanitized Atlas SOPs |
| [`src/sop_agent/`](./src/sop_agent) | Python CLI + overlay loader + renderer |
| [`docs/`](./docs) | Architecture, contribution guide, design decisions |

## Status

**Phase 0 — Scaffold.** The framework is being actively built. See [`docs/roadmap.md`](./docs/roadmap.md) for the phased plan.

## Contributing

We welcome new pillar skills, service lines, archetype refinements, and exporter formats. New pillars / services go through a lightweight review process — see [CONTRIBUTING.md](./CONTRIBUTING.md).

## Acknowledgments

The framework is built and maintained by [Atlas Digital](https://atlasdigitalusa.com), an agency that ships SOPs for itself and its clients. The `.sop.md` meta-engine format is inspired by the excellent [strands-agents/agent-sop](https://github.com/strands-agents/agent-sop) project.

## License

[Apache License 2.0](./LICENSE). See [NOTICE](./NOTICE) for attribution requirements.
