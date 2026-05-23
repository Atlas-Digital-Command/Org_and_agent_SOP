# Architecture

How the framework is wired. Read this once and you'll understand every file in the repo.

## Three layers

```
┌──────────────────────────────────────────────────────────────────┐
│ Layer 1 — GOVERNANCE                                              │
│ Loaded first. Applies to every subsequent decision.               │
│                                                                   │
│   governance/                                                     │
│     design-principles.md      ← how SOPs should look              │
│     measurement-principles.md ← how outcomes get scored           │
│     brand-voice.md            ← how things should sound           │
│     tool-inventory.md         ← what tools the org owns           │
│     org-profile.md            ← archetype + service list          │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│ Layer 2 — DEPARTMENT (pillars + service lines)                    │
│ Loaded on demand, based on the user's request.                    │
│                                                                   │
│   skills/                                                         │
│     strategy/                                                     │
│     branding/                                                     │
│     website/                                                      │
│     acquisition/                                                  │
│       seo/SKILL.md                                                │
│       paid-media/SKILL.md                                         │
│       ...                                                         │
│     retention/                                                    │
│     agentic-ai/                                                   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│ Layer 3 — ROLE / ORG MAP                                          │
│ Loaded to assign ownership and run gap analysis.                  │
│                                                                   │
│   org-map/                                                        │
│     roles.yaml                ← who exists at the org             │
│     team-structure.md         ← reporting + departments           │
│     raci-defaults.md          ← default ownership rules           │
│     hiring-priorities.md      ← what gaps we'll staff for         │
└──────────────────────────────────────────────────────────────────┘
```

These three layers live in the **overlay** — your private, gitignored content. The public repo ships only schemas and the three reference archetype overlays in `examples/`.

## Agent topology

```
                          ┌─────────────────┐
                  user ──►│   Conductor     │ ← reads governance/* always
                          │ (main agent)    │
                          └────────┬────────┘
                                   │
                ┌──────────────────┴──────────────────┐
                │ Parallel fan-out (Claude Agent SDK) │
                └──────────────────┬──────────────────┘
                                   │
       ┌───────────┬───────────────┼───────────────┬───────────────┐
       ▼           ▼               ▼               ▼               ▼
  ┌─────────┐ ┌─────────┐  ┌──────────────┐ ┌─────────────┐ ┌─────────────┐
  │ Pillar  │ │  Tool   │  │  Governance  │ │  Org Mapper │ │     QA      │
  │Specialist│ │ Mapper │  │  Validator   │ │ + Gap-Analyst│ │  Evaluator │
  │  (1-6)  │ │         │  │              │ │             │ │             │
  └────┬────┘ └────┬────┘  └──────┬───────┘ └──────┬──────┘ └──────┬──────┘
       │           │              │                │               │
       └───────────┴──────────────┴────────────────┴───────────────┘
                                   │
                                   ▼
                  ┌─────────────────────────────────┐
                  │   Conductor synthesizes draft   │
                  └───────────────┬─────────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  │ Parallel fan-out (round 2)    │
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
            ┌───────────┐                   ┌──────────────┐
            │ SOP Author│                   │   Visual     │
            │           │                   │   Renderer   │
            │           │                   │ (Phase 3)    │
            └─────┬─────┘                   └──────┬───────┘
                  │                                │
                  └────────────────┬───────────────┘
                                   ▼
                            output artifact
                       (Markdown + optional HTML/PDF)
```

### Agent roster

| Agent | Type | Responsibility |
|---|---|---|
| **Conductor** | Main | Routes intent, owns conversation, dispatches subagents, synthesizes results |
| **Onboarding** | Subagent (interactive) | First-run interview that builds the overlay |
| **Pillar Specialists** (6) | Subagent (parallel-capable) | One per pillar; loads only its own service-line skills |
| **Tool Mapper** | Subagent | Maps each draft step to a tool from the inventory |
| **Org Mapper** | Subagent | Assigns R/A/C/I per step, runs gap analysis |
| **Governance Validator** | Subagent | Checks every draft against governance principles |
| **QA Evaluator** | Subagent | Scores SOP against rubric — blocks on fail |
| **SOP Author** | Subagent | Renders the human-facing deliverable |
| **Visual Renderer** | Subagent (sandboxed, Phase 3) | Generates Mermaid + screenshots |

Each subagent runs in its own isolated context per the Claude Agent SDK's parallel-execution pattern. They share governance state via filesystem reads; they don't pass large blobs through the Conductor.

## The two SOP formats

There's a critical distinction often missed:

1. **`.sop.md` (Meta-SOPs)** — workflows the agent itself follows. RFC 2119 keywords (`MUST`, `SHOULD`, `MAY`). Format inspired by [strands-agents/agent-sop](https://github.com/strands-agents/agent-sop). Stored in [`agent-sops/`](../agent-sops/).

2. **Generated SOPs** — the human-facing deliverables. Numbered steps, RACI chips, KPIs, screenshots. Rendered from templates in [`templates/`](../templates/).

The meta-SOPs are the *engine*. The generated SOPs are the *product*.

## The overlay precedence

When the framework starts, it resolves the active overlay using this chain (highest wins):

1. `--overlay <path>` CLI flag — explicit, never wrong
2. `$SOP_AGENT_OVERLAY` environment variable — convenient default
3. `~/.sop-agent/overlay/` — auto-discovery for users who set it once and forget
4. **Fallback** — bundled `examples/` directory

The Python implementation lives in [`src/sop_agent/overlay/loader.py`](../src/sop_agent/overlay/loader.py).

## Why each archetype produces different output

The QA Evaluator's rubric is parameterized by archetype. Same Conductor, same Pillar Specialist, same Governance Validator — the Evaluator just enforces different defaults:

| Dimension | Lean | Coordinated | Compliance-Forward |
|---|---|---|---|
| Max step count | 7 | 12 | unlimited |
| RACI required | no | R+A | full R/A/C/I |
| KPIs required | 1 | 3 | comprehensive |
| Risk register | no | optional | required |
| Approval matrix | no | optional | required |
| Changelog format | line | structured | full audit trail |

The agent picks the archetype from `governance/org-profile.md`. When ambiguous, it defaults to **Lean** — the "lowest common denominator" principle.

## Why governance lives in the overlay

Putting governance in the public repo would mean:

- Every fork starts with someone else's opinions baked in
- Atlas's real voice / tools / brand ends up on GitHub
- Updating the framework requires merging across forks

The overlay pattern avoids all three. The public framework knows the *shape* of governance (the schema); the active content is supplied at runtime.

## File hot-paths

When `sop-agent new "..."` runs:

1. `__main__.py` parses args, resolves overlay via `overlay/loader.py`
2. Loads governance files into memory (cheap — they're small)
3. Spawns Conductor agent with governance as system prompt context
4. Conductor classifies request → selects pillar
5. Spawns parallel subagents (each with its own context window)
6. Joins their outputs, validates, synthesizes
7. Spawns SOP Author → writes Markdown to `.sop-output/`
8. (Phase 3) Spawns Visual Renderer in sandbox → writes HTML

Total wall-clock for a typical SOP: 30-90 seconds depending on archetype depth.
