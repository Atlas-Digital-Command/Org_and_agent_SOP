# Governance Schema

This document specifies the structure of every file under a governance overlay. The framework reads these files; deviating from the schema means the agent may not pick up your preferences correctly.

Five files are core (`design-principles`, `measurement-principles`, `brand-voice`, `tool-inventory`, `org-profile`). Two are optional but powerful for multi-client organizations: `segmentation-tags.md` and `automation-inventory.md` — both documented at the end of this file.

---

## `design-principles.md`

```markdown
# Design Principles

## SOP length preference
[One of: "lean" | "moderate" | "thorough"]

## Tone
[A few sentences describing how SOPs should read. E.g., "Direct, action-first, no jargon. Assume the reader is smart and busy."]

## Required sections
- [ ] Purpose
- [ ] Definition of Done
- [ ] Prerequisites
- [ ] Roles
- [ ] Tools
- [ ] Process steps
- [ ] KPIs / Quality metrics
- [ ] Escalation path
- [ ] Related SOPs
- [ ] Changelog

## Optional sections
- [ ] Risk register
- [ ] Approval matrix
- [ ] Compliance references
- [ ] Appendices

## Visual elements
- Mermaid diagrams: [always | when-helpful | never]
- Screenshots: [required | when-helpful | never]
- Tables: [encouraged | as-needed]

## Constraints
[Free-form bullets. Anything the agent MUST or MUST NOT do across all SOPs.]
- You MUST keep steps under [N] words each
- You MUST use the second person ("You") consistently
- You MUST NOT use jargon without defining it on first use
```

---

## `measurement-principles.md`

```markdown
# Measurement Principles

## What "done" means
[One paragraph: what's the bar for an SOP that's been executed correctly?]

## Quality dimensions
The framework's QA evaluator scores every generated SOP on these dimensions:

- **Clarity** — would a new hire understand it without asking questions?
- **Completeness** — does it cover the full workflow end-to-end?
- **Measurability** — can the outcome be verified objectively?
- **Role-fit** — does it match the seniority and specialization of the assigned role?
- **Brand alignment** — does it sound like us?

## Score thresholds
- Pass: [score >= N]
- Warn: [N - M]
- Fail: [< M]

## KPI defaults
When an SOP needs KPIs and none are obvious, default to:
- [List preferred KPIs by service pillar]
```

---

## `brand-voice.md`

```markdown
# Brand Voice

## Tone descriptors
[Three to five adjectives. E.g., "Direct, warm, precise, slightly irreverent, never corporate."]

## Vocabulary preferences
- We say "[X]" not "[Y]"
- We say "client" not "customer"
- We say "deliverable" not "output"
- [Add yours]

## Forbidden words / phrases
[Free-form list of words your organization avoids.]

## Reading-level target
[E.g., "Grade 8. No MBA-speak. No filler."]

## Example: how we sound
[A real example paragraph in your voice. The agent will use this as a tone reference.]
```

---

## `tool-inventory.md`

```markdown
# Tool Inventory

Organize by category. Use generic categories so this file remains portable.

## Project management
- [Tool name] — used for [purpose]
- ...

## Communication
- [Tool name] — used for [purpose]
- ...

## Design + asset creation
- ...

## Analytics + measurement
- ...

## Email + marketing automation
- ...

## SEO + search
- ...

## Paid media
- ...

## Social + content distribution
- ...

## AI + automation
- ...

## Storage + documentation
- ...

## Other
- ...
```

---

## `org-profile.md`

```markdown
# Organization Profile

## Identifier
- **Name:** [your org]
- **Archetype:** [lean-operator | coordinated-specialist | compliance-forward]
- **Headcount range:** [e.g., 11-25]
- **Industry / vertical:** [e.g., digital marketing services]

## Services offered
[Bulleted list of services you sell. Used by the org-mapper to know which pillars are active.]

## Client mix
- Average clients in flight: [N]
- Typical engagement length: [months]
- Industries served: [list]

## Operating model
- Where do most decisions get made? [founder | dept lead | tiered]
- How often do new hires come on? [rare | quarterly | monthly]
- What does a "typical" deliverable cycle look like? [free-form]

## Compliance posture
- Frameworks active: [none | SOC2 | HIPAA | ISO | other]
- Client compliance requirements: [free-form]

## Notes for the agent
[Any free-form context the agent should always know about your organization.]
```

---

## `segmentation-tags.md` (optional)

For organizations whose SOPs serve many clients/contexts with different profiles (agencies especially). When present, **every task in every generated SOP carries exactly one tag**, and the Governance Validator treats untagged tasks as `high` severity findings.

```markdown
# Segmentation Tags

## Tag vocabulary

| Tag | Meaning | Applies when |
|-----|---------|--------------|
| `[ALL]` | Every client — no exceptions | [description] |
| `[SEGMENT_NAME]` | [client segment definition] | [when tasks get this tag] |
| `[COND]` | Conditional — apply based on findings | [trigger discipline] |

## Rules for the agent
- Every generated SOP task MUST carry exactly one tag
- `[COND]` tasks MUST name their trigger
- New tags get added here first, never invented inline in an SOP
```

Recommended baseline vocabulary for agencies: `[ALL]`, `[LOCAL]`, `[ECOM]`, `[COND]`, `[INDUST]`, plus platform tags like `[WP/SF]`. Define what fits your client mix.

---

## `automation-inventory.md` (optional)

For organizations with automations that replace manual work. When present, the Pillar Specialist **checks this file before drafting any manual task** — generating a manual task that duplicates a registered automation is a `high` severity governance finding.

```markdown
# Automation Inventory

## Active automations

### [Automation name]
- **What it does:** [description]
- **Replaces:** [the manual work this eliminates]
- **Human checkpoint:** [who verifies it, at what cadence]
- **SOP rule:** [how SOPs should reference this — verification tasks, not execution tasks]

## Rules for the agent
- Check before you draft: manual tasks duplicating an automation are governance findings
- Automations get QA checkpoints in SOPs, not blind trust
- New automations get registered here first; affected SOPs then get flagged for regeneration
```

The core insight: **SOPs for automated work are verification workflows, not execution workflows.** An org with a strong automation stack should see its SOPs shrink, not grow.
