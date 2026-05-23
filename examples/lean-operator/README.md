# Lean Operator — Example Overlay

This is a reference overlay for a **Lean Operator** archetype organization. Copy this folder to your overlay path and edit to match your own organization.

## The fictional org

**Brightline Studios** — a six-person digital marketing boutique. They serve ~12 active clients across e-commerce and B2B SaaS, ranging from $3K to $12K MRR. The founder is the strategist; the rest of the team is execution-oriented with overlapping skill sets. There is no formal compliance posture, no HR system, and onboarding happens roughly once a year.

This overlay generates SOPs that are:

- **Short** (≤ 1 page typical)
- **Single-owner** (no formal RACI)
- **Direct in voice** (no hedging, no corporate-speak)
- **Light on KPIs** (1-2 per SOP, focused on outcomes)
- **Action-first** (verb-first steps, minimal preamble)

## Files

```
governance/
├── org-profile.md           — Org snapshot + archetype declaration
├── design-principles.md     — SOP shape + length preferences
├── brand-voice.md           — Tone + vocabulary + reading-level target
├── tool-inventory.md        — Tools by category (the Brightline stack)
└── measurement-principles.md — Quality bar + KPI defaults

org-map/
├── roles.yaml               — 6 roles, no formal RACI
└── team-structure.md        — Pod structure + capacity defaults
```

## Use it

```bash
# Use this overlay for one run
sop-agent new "Monthly client newsletter" --overlay ./examples/lean-operator

# Or copy it as your starting overlay and edit
cp -r examples/lean-operator ~/.sop-agent/overlay
$EDITOR ~/.sop-agent/overlay/governance/org-profile.md
```

## What this overlay deliberately omits

To stay true to the Lean archetype:

- No `raci-defaults.md` — Lean SOPs don't carry formal RACI
- No `hiring-priorities.md` — added when an org is actively recruiting
- No risk-register defaults — Lean SOPs don't include risk registers
- No approval-matrix defaults — single-decider model
