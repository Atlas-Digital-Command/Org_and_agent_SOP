# SEO Playbook (Deep Reference)

This is the reference loaded on-demand by the Acquisition Pillar Specialist when it needs to actually draft an SEO SOP. It is *not* loaded by `SKILL.md` automatically — progressive disclosure keeps `SKILL.md` short and this file rich.

When you (the Pillar Specialist) load this file, you have access to the full domain framework. Use what's relevant; don't dump everything into the draft.

---

## The four-pillars framing

Every SEO SOP touches one or more of these four pillars. Internalize them:

### 1. Technical SEO — can search engines reach, render, and understand the site?

Concerns:
- **Crawl** — robots.txt, sitemap.xml, internal-link reachability, crawl-budget management, log analysis
- **Render** — JavaScript SEO (CSR vs SSR vs ISR), hydration timing, render-blocking resources
- **Index** — canonicalization, noindex usage, soft-404s, duplicate-content handling, hreflang for i18n
- **Architecture** — URL structure, depth from root, breadcrumb hierarchy, faceted-nav governance
- **Performance** — Core Web Vitals (LCP, INP, CLS), TTFB, total page weight
- **Structured data** — schema.org markup, JSON-LD vs microdata, validation against rich-result requirements
- **Security + hygiene** — HTTPS everywhere, mixed-content elimination, expired-cert monitoring

Owner role typically: Technical SEO Lead, SEO Engineer, or Full-stack Dev with SEO context

### 2. On-page SEO — does each page serve its target query well?

Concerns:
- **Title + meta** — query-relevant titles within length limits, click-worthy meta descriptions
- **Headings** — H1 alignment with target query, H2/H3 covering related queries
- **Content** — query-aligned body content, semantic depth, freshness signals
- **Internal links** — anchor text relevance, link distribution to priority pages, orphan-page elimination
- **Image SEO** — descriptive filenames, alt text, format choice (WebP/AVIF), explicit dimensions
- **Engagement signals** — dwell time, scroll depth (indirect signals, not direct ranking factors but downstream value)

Owner role typically: On-page SEO Specialist, Content Editor, or SEO Generalist

### 3. Off-page SEO — does the broader web vouch for this site?

Concerns:
- **Link earning** — content worth linking to, digital-PR campaigns, statistic / research / data-driven assets
- **Link building** — guest contributions, partnership links, broken-link reclamation, unlinked mentions
- **Brand signals** — branded search volume, brand mentions across the web
- **Toxicity management** — disavow file maintenance, hostile-backlink monitoring
- **Local citations** — NAP consistency across directories (for local SEO)

Owner role typically: Link Building Manager, Digital PR Specialist, or Outreach Coordinator

### 4. Content SEO — does the site cover the topics the audience searches for?

Concerns:
- **Keyword research** — volume, difficulty, intent, SERP-feature analysis
- **Topic clusters** — pillar pages + cluster pages + internal-link topology
- **Content briefs** — query coverage, semantic completeness, length appropriate to intent
- **Refresh cadence** — decaying content identification, refresh prioritization
- **Cannibalization management** — multiple pages competing for the same query

Owner role typically: SEO Content Strategist, Content Marketing Manager, or hybrid SEO/Content role

---

## Workflow shapes — the three patterns

Every SEO SOP fits one of these three workflow shapes. Identify the shape early; it dictates section structure.

### Shape A: Audit workflow

```
Scope → Crawl/Collect → Analyze → Prioritize → Report → Handoff
```

Use when the SOP's purpose is to surface what's wrong (or right) and produce a prioritized fix list. Examples: monthly technical audit, content gap analysis, backlink toxicity audit.

Step-count by archetype:
- Lean: 4-5 steps (collapse Crawl+Analyze, collapse Report+Handoff)
- Coordinated: 6 steps (the canonical shape)
- Compliance-Forward: 7-8 steps (add explicit sign-off gates between Prioritize and Report, and a post-handoff verification step)

### Shape B: Production workflow

```
Brief → Research → Produce → Optimize → Review → Publish → Log
```

Use when the SOP's purpose is to generate a deliverable. Examples: new page brief, blog post production, schema implementation.

Step-count by archetype:
- Lean: 4-5 steps (combine Brief+Research, combine Optimize+Review)
- Coordinated: 6-7 steps
- Compliance-Forward: 8+ steps (add legal/compliance review, brand review, executive sign-off as separate steps)

### Shape C: Reporting workflow

```
Define window → Pull data → Reconcile → Narrate → Deliver → Archive
```

Use when the SOP's purpose is recurring reporting. Examples: weekly snapshot, monthly performance report, quarterly review.

Step-count by archetype:
- Lean: 3-4 steps (combine Reconcile+Narrate)
- Coordinated: 5-6 steps
- Compliance-Forward: 6-7 steps (add data-quality sign-off, stakeholder review window before Deliver)

---

## Tool category reference

The Pillar Specialist references categories generically; the Tool Mapper substitutes actual vendors from `governance/tool-inventory.md`. Below is the canonical category list with example vendors *only as illustration* — never hardcode these into a draft.

| Category | What it does | Example vendors (illustration only) |
|---|---|---|
| **Site crawler** | Bulk URL crawling, status codes, redirect chains, internal-link discovery | Screaming Frog, Sitebulb, OnCrawl, JetOctopus |
| **Rank tracker** | Daily/weekly keyword position monitoring | Ahrefs, SEMrush, Moz, AccuRanker, SE Ranking |
| **Backlink analyzer** | Discovers backlinks, scores authority, flags toxicity | Ahrefs, Majestic, SEMrush, Moz |
| **Keyword research tool** | Search volume, difficulty, SERP overview | Ahrefs, SEMrush, Moz, Keywords Everywhere |
| **Content optimization tool** | Semantic recommendations, query-coverage scoring | Clearscope, SurferSEO, MarketMuse, Frase |
| **Web analytics** | Traffic, conversions, engagement | GA4, Adobe Analytics, Matomo, Plausible |
| **Search console (engine-side)** | Direct query/page performance from search engines | Google Search Console, Bing Webmaster Tools |
| **Schema / structured-data validator** | Tests structured-data markup | Google Rich Results Test, Schema.org Validator |
| **Core Web Vitals tool** | Lab + field performance measurement | PageSpeed Insights, Lighthouse, CrUX, WebPageTest |
| **Log analyzer** | Crawl-budget and bot-behavior analysis | Screaming Frog Log Analyzer, Splunk, Logz.io |
| **Local SEO platform** | Citation management, GBP optimization, review monitoring | BrightLocal, Whitespark, Moz Local, Yext |
| **Site speed / performance tool** | Image optimization, JS profiling, asset analysis | WebPageTest, Lighthouse, Cloudflare Speed |

When drafting, you may say: "use a `rank-tracker` category tool" or "open the org's `keyword-research` tool" — never name a specific vendor unless `governance/tool-inventory.md` declares one for that category.

If the org's inventory lacks a category needed by the SOP, the Tool Mapper will flag the gap. Do not block drafting on missing tools.

---

## KPI library

These are the canonical KPIs per SOP category. Pick 2-3 for Lean, 3-4 for Coordinated, 4+ for Compliance-Forward.

### Audit SOPs
- Issues identified by severity (count)
- Priority-ranked fix list completeness (binary: yes/no)
- Critical issues resolved within SLA (% of total critical)
- Audit-to-implementation time (median days)

### Optimization SOPs
- Pre/post organic traffic delta to affected URLs (% over 30 days)
- Pre/post ranking delta for target queries (positions)
- Indexed-pages delta (count, from search console)
- Pages with target structured data deployed (count)

### Research SOPs
- Usable keywords identified (count after dedup + intent filter)
- Cluster coverage (% of intent-relevant queries covered)
- Time-to-deliver (days from kickoff)
- Stakeholder NPS on usefulness (1-10)

### Brief / spec SOPs
- Briefs accepted without rework (% of total)
- Time-to-publish from brief delivery (days)
- Ranking achieved within 90 days (target position)
- Organic traffic to the page within 90 days (sessions/users)

### Reporting SOPs
- Stakeholder NPS on report quality (1-10)
- Time-to-deliver vs SLA (hours)
- Decisions changed based on report (count, qualitative tracking)
- Reports delivered on schedule (% of total)

### Process SOPs
- Time-to-completion vs benchmark (% of SLA met)
- Error rate per execution (defects per 100 executions)
- Handoff success rate (% completed without rework)

---

## RACI patterns by archetype

How role assignment scales:

### Lean Operator
- Single Owner per SOP (no formal RACI). The "owner" is whoever's available on the SEO team.
- Approver = Founder (rarely invoked; most SOPs are owner-discretion)
- Example: "Owner: SEO Generalist. Sign-off: Founder if budget impact > $X."

### Coordinated Specialist
- R + A always declared per step
- C invoked for cross-functional steps (e.g., dev work, content production)
- I list includes Account Strategist + Client Owner
- Example: "Step 3 (Crawl): R = SEO Specialist, A = SEO Lead, C = DevOps Lead, I = Account Strategist"

### Compliance-Forward
- Full R/A/C/I per step
- Tiered approval gates explicit (analyst → lead → director thresholds documented)
- Sign-off documented in changelog with name + date for compliance-sensitive steps
- Example: "Step 5 (Prioritize fixes affecting customer-facing pages): R = SEO Analyst, A = SEO Director, C = Legal + Compliance Lead, I = CMO. Director sign-off required before Step 6."

The Org Mapper subagent owns the actual assignment from `org-map/roles.yaml`. The Pillar Specialist drafts the *step structure* and indicates which steps need RACI depth.

---

## Cross-archetype defaults

These principles apply regardless of archetype:

1. **Every SOP has a "what happens to the output" step.** Audits produce fix lists → fix lists go *somewhere* (ticketed, scheduled, queued). Reports produce insights → insights go *somewhere* (decision, action, archive). Don't ship bookshelf decoration.

2. **Every SOP logs its execution.** A minimum entry: who ran it, when, what was the outcome, what's the next-due date. SEO is cumulative; missing logs = compounding technical debt.

3. **Every SOP has at least one KPI tied to a downstream outcome.** Internal metrics (issues identified, briefs written) are necessary but not sufficient. Connect to traffic, conversions, or revenue at least once.

4. **Every SOP names the SLA / cadence.** Weekly, monthly, quarterly, ad-hoc — be explicit. Vague "as needed" cadences become "never."

5. **Every SOP names an escalation path.** When the SOP breaks (tool fails, finding requires authority above the owner), who does the owner go to?

---

## Common-gotcha checklist

Before returning a draft, mentally verify the SOP avoids each of these:

- [ ] KPIs include at least one downstream metric (not just rank/issues-count)
- [ ] Audit SOPs have a defined handoff for the prioritized fix list
- [ ] No specific vendor names hardcoded (use tool categories)
- [ ] Keyword research SOPs include intent classification, not just volume+difficulty
- [ ] Every SOP has a logging step
- [ ] Core Web Vitals SOPs declare a recurring cadence (not one-time)
- [ ] Migration SOPs have explicit before / during / after phases
- [ ] Cross-functional steps have RACI depth appropriate to archetype
- [ ] Compliance-sensitive sub-domains (health, finance, gambling) reference the relevant constraints

---

## Section template for the draft

When you produce a draft for the Conductor to synthesize, structure your output like this:

```markdown
## Process steps (draft)

### 1. <Verb-first step name>

<One-sentence description of what this step accomplishes>

**Inputs:** <what the executor needs before starting>
**Output:** <what the step produces>
**Tool category:** <category name from the reference above>
**Suggested role seniority:** <junior | mid | senior | lead>
**Estimated time:** <minutes / hours>

**Constraints:**
- <RFC 2119-style constraint specific to this step>
- ...

### 2. ...
```

Keep step descriptions tight. The SOP Author will reformat to the human-facing template; you produce structured content, not polished prose.

Return the draft as a JSON wrapper for the Conductor:

```json
{
  "service_line": "seo",
  "sub_discipline_primary": "technical-seo",
  "sub_disciplines_secondary": ["on-page-seo"],
  "workflow_shape": "audit",
  "step_count": 6,
  "draft_markdown": "<the markdown above as a string>",
  "kpi_suggestions": [
    {"kpi": "Critical issues resolved within 30 days", "measurement": "%"},
    {"kpi": "Pre/post indexed-pages delta", "measurement": "count from search console"}
  ],
  "tool_categories_used": ["site-crawler", "search-console", "log-analyzer"],
  "notes": [
    "Recommended cadence: monthly",
    "Recommended owner seniority: mid-to-senior"
  ]
}
```

The Conductor merges this with the Tool Mapper and Org Mapper outputs per the synthesis precedence rules in `agents/conductor.md`.

---

## When this playbook isn't enough

If a request hits a corner of SEO this playbook doesn't cover (e.g., voice search, AI Overviews / SGE optimization, app-store SEO), do the best you can with the patterns above and flag the gap in your `notes` field. We'll fold new patterns into this file as they prove out.
