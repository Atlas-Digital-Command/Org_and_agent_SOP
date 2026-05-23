# Design Principles

## SOP length preference

**lean** — target ≤ 1 printed page (roughly 400 words / 5-7 steps).

## Tone

Direct, action-first, no hedging. Assume the reader is competent and busy. Skip preambles; lead with the verb. If a step needs context, put the context in a single sentence after the action, not before.

## Required sections

The framework MUST include all of these in every generated SOP:

- Purpose (1 sentence, why this SOP exists)
- Definition of Done (1-2 sentences, what success looks like)
- Process (numbered steps)
- KPIs (1-2 metrics)
- Changelog (line-level; date + brief note)

## Optional sections

The framework MAY include these only if the SOP's subject genuinely needs them:

- Prerequisites — include only when starting state isn't obvious
- Tools — include only when more than one tool is involved
- Escalation path — include only when the step might break in a way the owner can't recover from
- Related SOPs — include only when there's a direct cross-reference

## Sections to omit entirely

The framework MUST NOT include any of these for Lean SOPs:

- Roles + RACI — single owner is implicit
- Risk register — overkill at this archetype
- Approval matrix — founder-as-fallback is sufficient
- Appendices — push detail into linked references instead

## Visual elements

- **Mermaid diagrams:** when-helpful only. Most Lean SOPs are linear and don't need them.
- **Screenshots:** never required. The Visual Renderer should not be invoked for Lean by default.
- **Tables:** encouraged for tool / KPI / handoff sections only.

## Hard constraints

The framework MUST follow these without exception:

- You MUST keep each step under 30 words
- You MUST use the second person ("You") consistently
- You MUST NOT use ellipses (...) in any output
- You MUST NOT use the phrase "as needed" — every cadence must be specific
- You MUST NOT use the words "leverage," "synergies," "unlock," or "robust" (Brightline forbidden vocabulary)
- You MUST NOT include placeholder text like "TBD" or "[insert here]" in delivered SOPs

## Review cadence

Default SOP review cadence: every 180 days. The audit-sop workflow uses this for freshness scoring.

## Specific to this archetype

- Single-step SOPs are allowed. If the workflow really is one action, the SOP is one step plus KPIs.
- Multi-page SOPs are a smell. If the agent produces more than 1 page, it should question whether this SOP should be split into 2 smaller ones.
