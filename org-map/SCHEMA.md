# Org Map Schema

Reference structure for every file in an org-map overlay.

---

## `roles.yaml`

```yaml
# Each role is an entry under `roles:`. Use kebab-case IDs.
roles:
  founder:
    title: "Founder / CEO"
    seniority: principal
    department: leadership
    headcount: 1
    reports_to: null
    responsibilities:
      - "Final approval on new service offerings"
      - "Client relationship for top-tier accounts"
      - "Strategic direction"
    can_own:
      - strategy
      - any  # special token meaning this role is willing to own any SOP step
    cannot_own:
      - production-execution  # explicit no-go zones

  account-strategist:
    title: "Account Strategist"
    seniority: senior
    department: strategy
    headcount: 2
    reports_to: founder
    responsibilities:
      - "Quarterly strategy reviews with clients"
      - "Performance reporting"
      - "Channel mix recommendations"
    can_own:
      - strategy
      - acquisition.seo
      - acquisition.paid-media
      - retention.email-marketing

  # ... additional roles
```

### Field reference

| Field | Required | Description |
|---|---|---|
| `title` | yes | Human-readable role title |
| `seniority` | yes | One of: `junior`, `mid`, `senior`, `lead`, `principal` |
| `department` | yes | Top-level grouping; need not match pillar names |
| `headcount` | yes | How many people currently hold this role (0 = vacant) |
| `reports_to` | yes | Role ID this role reports to, or `null` |
| `responsibilities` | yes | Bulleted list of what this role owns day-to-day |
| `can_own` | yes | List of pillar / pillar.service IDs this role is willing to own SOP steps for. Use `any` to mean "any step the agent suggests" |
| `cannot_own` | no | Explicit exclusions, overrides `can_own` |

---

## `team-structure.md`

```markdown
# Team Structure

## Departments
- **Leadership** — Founder, COO
- **Strategy** — Account Strategists
- **Acquisition** — SEO Lead, Paid Lead, Content Lead
- **Delivery** — Designers, Developers, Writers
- **Operations** — PM, HR

## Pods or working groups
[If your org organizes into cross-functional pods, document them here.]

## Capacity defaults
For gap analysis:
- A `senior` role can own ~2 concurrent SOP-driven workflows
- A `mid` role can own ~3
- A `junior` role can own ~4

Adjust above based on your reality. The agent uses these for over-allocation warnings.
```

---

## `raci-defaults.md`

```markdown
# RACI Defaults

When the agent assigns RACI and an SOP doesn't specify, use these defaults.

## By SOP step type

| Step type | Responsible (default) | Accountable (default) | Consulted | Informed |
|---|---|---|---|---|
| Strategy / planning | Account Strategist | Department Lead | Founder | Team |
| Execution / production | Pillar specialist | Department Lead | Account Strategist | Client owner |
| Review / approval | Department Lead | Founder | — | Team |
| Client-facing delivery | Account Strategist | Founder | Pillar specialist | — |

## Approval thresholds

- Any step touching $X+ in client spend: requires `founder` in Accountable
- Any step affecting client-facing brand: requires `account-strategist` in Consulted
- Anything labeled `compliance-sensitive`: requires explicit sign-off documented in the SOP changelog
```

---

## `hiring-priorities.md`

```markdown
# Hiring Priorities

Open or planned positions. The Org Mapper prefers these when suggesting hires from gap analysis.

## Active openings
1. **Senior SEO Strategist** — gap created by SEO service growth; want to hire by Q2
2. **Content Production Lead** — gap created by content studio expansion

## On the horizon
- Junior PM (when client load > 15)
- Dedicated Compliance Lead (when SOC2 work materializes)

## Won't hire
- [Roles you've explicitly decided not to hire. Helpful to prevent the agent from suggesting them.]
```
