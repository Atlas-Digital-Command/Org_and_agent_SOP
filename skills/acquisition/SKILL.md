---
name: pillar-acquisition
description: Use when generating, auditing, or refining SOPs for customer/lead acquisition work. Covers paid media, SEO, social media management, content marketing, and cold email. Loads service-line knowledge on demand rather than all at once.
version: 0.1.0
tags: [skill, sop, pillar, acquisition, seo, paid-media, social, content-marketing, cold-email]
---

# Acquisition (Pillar)

This skill activates when an SOP request is about **attracting new customers, leads, or audience** through any acquisition channel. It does not load deep service-line knowledge by itself — it routes the request to the appropriate service-line skill via progressive disclosure.

## When this skill loads

The Conductor loads this skill when an SOP request matches any of:

- Mentions of search-engine optimization, organic traffic, keyword research, technical audits, content briefs, link building, local SEO, programmatic SEO
- Mentions of paid advertising on any platform — Google Ads, Meta, LinkedIn, TikTok, programmatic display, retargeting
- Mentions of social media content production, community management, organic social distribution, influencer programs
- Mentions of content marketing, top-of-funnel content, content cluster strategy, blog programs, gated content
- Mentions of outbound prospecting, cold email sequences, lead lists, sales-marketing handoffs at the acquisition stage

When the request is clearly *retention-focused* (existing customer lifecycle, transactional email, SMS to opted-in subscribers, churn reduction), load the **retention** pillar instead. When ambiguous, route to the most specific match and confirm classification with the user.

## Service-line taxonomy

| Service line | Skill path | What it covers |
|---|---|---|
| `seo` | `skills/acquisition/seo/SKILL.md` | Organic search visibility — technical, on-page, off-page, content, local, programmatic |
| `paid-media` | `skills/acquisition/paid-media/SKILL.md` *(Phase 2)* | Search ads, social ads, display, programmatic, performance creative |
| `social-media-management` | `skills/acquisition/social-media-management/SKILL.md` *(Phase 2)* | Organic content production, community engagement, channel strategy |
| `content-marketing` | `skills/acquisition/content-marketing/SKILL.md` *(Phase 2)* | Editorial strategy, content clusters, top-of-funnel programs |
| `cold-email` | `skills/acquisition/cold-email/SKILL.md` *(Phase 2)* | Outbound list building, sequence design, deliverability hygiene |

Each service-line skill follows the same shape: a short `SKILL.md` that describes when to load it, plus one or more reference files (`playbook.md`, `templates.md`, etc.) loaded on demand by the Pillar Specialist subagent.

## Cross-cutting concerns for Acquisition SOPs

These apply across every Acquisition service line and should be respected in every SOP generated under this pillar:

1. **Channel attribution is contested.** SOPs that touch reporting should either declare the attribution model (last-click, position-based, data-driven, MTA, MMM) or note that attribution methodology is a separate decision upstream.

2. **Measurement windows matter.** Distinguish weekly tactical metrics (rank tracking, ad CPMs) from monthly/quarterly outcome metrics (organic traffic, qualified leads, CAC). Lean SOPs may use only one window; coordinated and compliance-forward SOPs should declare both.

3. **Compliance touches more than you'd think.** Cold email runs into CAN-SPAM, CASL, GDPR. Paid media has platform-specific content policies (alcohol, gambling, health). SEO has Google's spam policies. SOPs in regulated verticals (health, finance, gambling) must reference the relevant constraints.

4. **Owner role varies by org size.** A Lean org's "SEO Lead" may also write the content. A Coordinated org separates strategy from execution. A Compliance-Forward org adds a reviewer between every step. The Pillar Specialist should not assume role separation — that comes from the org-map.

5. **Tool categories matter; specific tools don't.** SOPs should reference *categories* (crawler, rank tracker, content optimization tool) and let the Tool Mapper substitute in the org's actual stack from `governance/tool-inventory.md`.

## Common SOP types per service line

When the user gives only a vague description like "create an SOP for SEO," ask which of these they want:

**SEO:**
- Audits (technical, on-page, content, backlink, local, e-commerce)
- Optimization workflows (page-level, site-level, cluster-level)
- Research (keyword research, content gap, competitor analysis)
- Briefs (new page, blog post, schema implementation)
- Migration / launch checklists
- Reporting cadences (weekly, monthly, quarterly)

**Paid Media:**
- Campaign builds (per platform)
- Creative production workflows
- Budget pacing reviews
- Account audits
- Conversion tracking setup
- Reporting and optimization cadences

**Social Media Management:**
- Content calendar production
- Channel-specific posting workflows
- Community engagement protocols
- Influencer partnership runbooks
- Social listening + response workflows

**Content Marketing:**
- Editorial calendar production
- Brief-to-publish workflows
- Content cluster strategy
- Distribution and amplification
- Performance review cadences

**Cold Email:**
- List building and enrichment workflows
- Sequence design and approval
- Deliverability monitoring
- Reply triage and handoff
- Compliance review cadences

## How the Pillar Specialist uses this skill

The Pillar Specialist subagent ([`agents/pillar-acquisition.md`](../../agents/pillar-acquisition.md)) reads this file first, then loads the relevant service-line `SKILL.md`, then loads the service-line's `playbook.md` only when actually drafting steps. This three-level progressive disclosure keeps context lean for simple requests and deep for complex ones.
