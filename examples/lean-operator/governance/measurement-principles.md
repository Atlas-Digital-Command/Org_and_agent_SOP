# Measurement Principles

## What "done" means

An SOP execution is "done" when the deliverable exists, the outcome is logged, and the next-due date is set. Not when the document is written — when the work is shipped.

## Quality dimensions

The QA Evaluator scores Brightline SOPs on the standard five dimensions: clarity, completeness, measurability, role-fit, brand alignment.

### Brightline-specific weighting

The framework's default thresholds for Lean are:

- Aggregate ≥ 32 (out of 50) to pass
- Per-dimension minimums: clarity ≥ 7, brand ≥ 7; others ≥ 6

Brightline uses the framework defaults without override.

## Score thresholds

- **Pass:** aggregate ≥ 32
- **Pass with warnings:** aggregate ≥ 32 but at least one per-dimension minimum missed
- **Fail:** aggregate < 32

The Conductor blocks delivery on `fail` and surfaces but ships on `pass-with-warnings`.

## KPI defaults

When an SOP needs KPIs and none are obvious from the request, default to one of these by service line:

**SEO**
- Organic traffic delta (30-day pre/post) to affected URLs
- Critical issues resolved within 30 days (% of total)

**Paid Media**
- Cost per qualified lead / cost per acquisition (depending on goal)
- Return on ad spend (ROAS) — minimum window 14 days post-launch

**Email Marketing**
- Open rate against the client's 90-day baseline
- Click-through-rate or revenue-per-recipient (e-commerce)

**Content Marketing**
- Organic sessions to the page (90-day window)
- Time-on-page or scroll depth (engagement signal)

**Conversion Rate Optimization**
- Conversion rate delta vs control (statistical significance noted)
- Revenue per visitor delta

## Definition of "measurable"

A KPI is measurable if all three are true:

1. The metric is a number, not an adjective
2. The org owns or has access to the tool that measures it
3. There is a defined window over which to measure it

Examples that pass:
- "Lift organic traffic to /pricing by 10% within 60 days of publishing"
- "Reduce CPL by 15% within 30 days of new creative launch"
- "Open rate within 5 points of the 90-day baseline"

Examples that fail:
- "Improve SEO" (not a number)
- "Achieve world-class deliverability" (not a number AND forbidden vocabulary)
- "Strong engagement" (not a number)

## Outcome bias

Brightline weights outcome metrics over process metrics. Whenever possible, an SOP's KPIs should include at least one downstream business metric (traffic, leads, revenue, retention) — not just process metrics (briefs written, audits completed). The framework enforces this by requiring ≥ 1 downstream KPI per SOP via the playbook's cross-archetype defaults.

## Anti-vanity-metric stance

The framework MUST NOT default to any of these as primary KPIs (they may be referenced as secondary signals):

- Total impressions / reach (without engagement context)
- Follower counts
- "Engagement rate" without defining the formula
- Bounce rate (deprecated in GA4; use engagement rate or session-based metrics instead)

If the user specifically requests a vanity metric, generate the SOP but flag the metric choice in the summary.
