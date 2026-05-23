# Org Map

> Like [`governance/`](../governance), this folder is **intentionally empty in the public repo**. It defines the *shape* of your organization's role and accountability overlay.

## What org-map is

The org map tells the agent who actually works at your organization and what they're accountable for. It's how the framework knows whether your proposed SOP can be staffed today — or whether you need to hire someone first.

The Org Mapper subagent reads these files to:

- Assign owners (Responsible / Accountable) to each SOP step
- Flag steps that don't map to any existing role (**gap analysis**)
- Suggest hires or contractor engagements when gaps appear
- Build a RACI matrix automatically based on your role definitions

## Files in this folder

| File | Purpose |
|---|---|
| `roles.yaml` | Authoritative list of roles in your organization with responsibilities, seniority, and reporting lines |
| `team-structure.md` | How roles are organized — departments, pods, reporting chains |
| `raci-defaults.md` | When the agent needs to assign R/A/C/I and the SOP doesn't specify, these defaults apply |
| `hiring-priorities.md` | Optional: roles you're actively hiring for. Gap analysis prefers suggesting these first. |

See [SCHEMA.md](./SCHEMA.md) for the precise structure.

## How gap analysis works

When the agent drafts an SOP, the Org Mapper looks at each step and asks:

1. Is there a role in `roles.yaml` that can credibly own this step?
2. Is that role available (not over-allocated according to `team-structure.md`)?

If either answer is no, the agent annotates the SOP with:

- A `[GAP]` marker on the affected step
- A suggested role definition (title, responsibilities, seniority) you'd need to add to staff this SOP
- A suggestion of whether the gap is best filled by a hire, a contractor, or a tool

You then decide whether to staff up, accept the gap with workarounds, or skip the SOP.

## How RACI gets assigned

For each step, the agent picks:

- **Responsible** — the role that does the work
- **Accountable** — the role that owns the outcome (often the same as Responsible in lean orgs, separate in larger orgs)
- **Consulted** — roles whose input is required before proceeding
- **Informed** — roles that are kept in the loop but don't gate progress

The depth of RACI assignment scales with your archetype:

- **Lean Operator** — usually just R (whoever's available). RACI may be skipped entirely.
- **Coordinated Specialist** — R + A always, C/I when relevant
- **Compliance-Forward** — full R/A/C/I per step, with approval thresholds
