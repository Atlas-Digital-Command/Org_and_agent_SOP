---
name: service-acquisition-seo
description: Use when generating, auditing, or refining SOPs for SEO work. Covers technical SEO, on-page, off-page, content SEO, local, programmatic, and e-commerce SEO. Loads the playbook on demand for deeper reference.
version: 0.1.0
tags: [skill, sop, service-line, acquisition, seo, organic-search, technical-seo, content-seo]
---

# SEO (Service Line under Acquisition)

This skill activates for any SOP request whose substance is **earning visibility in search engines**. The Pillar Specialist loads this `SKILL.md` first; if the SOP requires actual drafting, it then loads [`playbook.md`](./playbook.md) from this directory for the deeper reference.

## Sub-disciplines

SEO is not one thing. SOPs in this space typically anchor to one of these sub-disciplines:

| Sub-discipline | What it owns |
|---|---|
| **Technical SEO** | Crawlability, indexability, site architecture, render budget, Core Web Vitals, structured data, internationalization, log analysis |
| **On-page SEO** | Title + meta optimization, heading structure, content optimization for target queries, internal linking, image SEO |
| **Off-page SEO** | Link building, digital PR, partnerships, unlinked-mention reclamation, disavow management |
| **Content SEO** | Keyword research, content gap analysis, topic clusters, content briefs, refresh cadences |
| **Local SEO** | Google Business Profile management, citations, location pages, local link building, review programs |
| **Programmatic SEO** | Template-driven page generation at scale, data-source curation, internal-link orchestration |
| **E-commerce SEO** | Product page optimization, category structure, faceted-navigation governance, schema for products/offers/reviews |

Most real-world SEO SOPs touch two or three of these — a technical audit may surface on-page issues; a content brief includes internal-link recommendations. The Pillar Specialist should classify the *primary* sub-discipline and treat the others as secondary considerations.

## Common SOP categories

These are the canonical SOP types most agencies and in-house teams need. When a user gives a vague request, offer these as a multiple choice:

1. **Audit SOPs** — diagnose current state, surface issues, prioritize fixes
   - Monthly / quarterly technical SEO audit
   - Content audit (gap, decay, cannibalization)
   - Backlink profile audit
   - Local SEO audit
   - E-commerce category-page audit

2. **Optimization SOPs** — execute changes
   - Page-level on-page optimization
   - Internal link sculpting
   - Schema implementation
   - Core Web Vitals remediation
   - Title + meta refresh at scale

3. **Research SOPs** — produce inputs for other work
   - Keyword research for a new cluster
   - Competitor SEO analysis
   - SERP feature analysis for a target query set
   - Content gap analysis

4. **Brief / spec SOPs** — produce written specifications others execute against
   - New page SEO brief
   - Blog post SEO brief
   - Site migration plan
   - Schema spec for product / article / event / how-to types
   - Hreflang implementation spec

5. **Reporting SOPs** — generate the recurring deliverables
   - Weekly rank + traffic snapshot
   - Monthly SEO performance report
   - Quarterly strategic review

6. **Process SOPs** — internal team workflows
   - New-client onboarding (SEO data + tool access)
   - Site migration QA checklist
   - Algorithm-update response playbook
   - Crisis / drop investigation runbook

## Pattern recognition: workflow shapes

Most SEO SOPs follow one of three workflow shapes. Match the request to a shape early; it speeds drafting significantly:

- **Audit shape:** scope → crawl/collect → analyze → prioritize → report → handoff
- **Production shape:** brief → research → produce → optimize → review → publish → log
- **Reporting shape:** define window → pull data → reconcile → narrate → deliver → archive

When in doubt, ask the user which shape best matches their need.

## Tool categories used by SEO SOPs

The Tool Mapper substitutes specific vendors from `governance/tool-inventory.md`. The Pillar Specialist references these *categories* generically:

- **Site crawler** — bulk URL crawling and technical analysis
- **Rank tracker** — keyword position monitoring
- **Backlink analyzer** — link discovery, profile analysis, toxicity scoring
- **Keyword research tool** — search volume, difficulty, intent classification
- **Content optimization tool** — semantic recommendations, query-coverage scoring
- **Web analytics** — organic traffic, conversion, engagement metrics
- **Search console** — direct query/page performance from search engines
- **Schema validator** — structured data testing
- **Core Web Vitals tool** — performance measurement (lab + field)
- **Log analyzer** — crawl-budget and bot-behavior analysis
- **Local SEO platform** — citation management, review monitoring
- **Site speed / performance tool** — image optimization, JS profiling

If a user's overlay has only some of these categories, the Pillar Specialist should still draft the SOP and let the Tool Mapper flag missing categories.

## Common KPIs per SOP category

The QA Evaluator scores SOPs partly on measurability. These are the canonical KPIs by category — every SEO SOP should reference one or more:

| SOP category | KPIs |
|---|---|
| Audit | Issues identified (count + severity), priority-ranked fix list completeness |
| Optimization | Pre/post organic traffic delta, ranking delta for target queries, indexed-pages delta |
| Research | Volume of usable keywords identified, cluster coverage %, intent classification accuracy |
| Brief | Time-to-publish, ranking achieved within 90 days, organic traffic to the page within 90 days |
| Reporting | Stakeholder NPS on report quality, time-to-deliver, decision changes attributed to the report |
| Process | Time-to-completion vs benchmark, error rate, handoff success rate |

When drafting, the Pillar Specialist should propose 2-3 KPIs per SOP (Lean), 3-4 (Coordinated), or 4+ (Compliance-Forward) — and each should be measurable with a tool category the org owns.

## Common gotchas

These are the things SEO SOPs get wrong most often. The Pillar Specialist should proactively avoid them:

1. **Confusing rankings with traffic.** Rankings are a leading indicator; traffic is the outcome. SOPs that measure only rank are common and weak. KPIs should include at least one downstream metric (traffic, clicks, conversions).

2. **No "what to do with the output" handoff.** Audit SOPs that don't define how findings get worked are bookshelf decoration. Every audit SOP should specify what happens to the prioritized fix list (ticketed, scheduled, queued in CMS, handed to a dev team, etc.).

3. **Assuming the user has every tool.** Don't write "use Ahrefs to..." Write "use the rank-tracker category tool to..." and let the Tool Mapper substitute.

4. **Ignoring intent in keyword research.** Volume + difficulty is necessary but not sufficient. Modern keyword research SOPs must include intent classification (informational / navigational / transactional / commercial-investigation) and SERP-feature analysis.

5. **Skipping the "log this" step.** SEO is cumulative; every change should be logged with timestamp, what changed, who changed it, and what the expected impact was. SOPs without a logging step compound debt over time.

6. **Treating Core Web Vitals as a one-time fix.** CWV regresses with deployments. SOPs in this space should have a recurring cadence (monthly minimum), not a one-time audit.

7. **Confusing site migration QA with launch.** SEO migration SOPs should have explicit before / during / after phases with separate checklists. Folding all three into one checklist is a recipe for missed redirects.

## What this skill does not cover

- Paid search (Google Ads, Bing Ads) — that's `paid-media`
- Conversion rate optimization on the page — that's `website/conversion-rate-optimization`
- Email marketing — that's `retention/email-marketing`
- Social platform algorithms (TikTok SEO, Pinterest, YouTube) — these are search-adjacent and currently belong under `social-media-management`; revisit if a "social-seo" service line is proposed

## Next-step pointer

When the Pillar Specialist needs the deep reference — discipline framework details, full tool category mapping, common RACI patterns, archetype-specific step counts — it loads [`playbook.md`](./playbook.md) from this directory.
