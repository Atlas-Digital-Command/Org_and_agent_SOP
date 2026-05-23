# New SOP

## Overview

This meta-SOP guides the SOP Agent through the canonical workflow for authoring a new Standard Operating Procedure. It loads the active overlay (governance + org-map), classifies the request into a pillar and service line, runs domain specialists in parallel, validates the draft against governance, scores it through the QA evaluator, iterates if needed, and renders the final human-facing deliverable.

This is the workflow invoked by `sop-agent new "<description>"` and by `/sop-new` in Claude Code.

The SOP this workflow produces is *for humans*. This document, by contrast, is for the agent itself — written in the strands-agents `.sop.md` format with RFC 2119 keywords.

## Parameters

- **description** (required): Natural-language description of the SOP to create. Should answer "what does this SOP need to enable a person to do?"
- **pillar** (optional): One of `strategy`, `branding`, `website`, `acquisition`, `retention`, `agentic-ai`. If omitted, You MUST classify automatically from the description.
- **service_line** (optional): A specific service under the pillar (e.g., `seo`, `paid-media`). If omitted, You MUST classify or ask.
- **archetype_override** (optional): Force a specific archetype output: `lean`, `coordinated`, or `compliance-forward`. If omitted, You MUST read it from `governance/org-profile.md`. If that file is missing or ambiguous, You MUST default to `lean`.
- **output_path** (optional, default: `.sop-output/`): Directory to write the generated SOP into.
- **output_format** (optional, default: `markdown`): One of `markdown`, `pdf`, `html`. Additional formats require optional exporter dependencies.
- **visual** (optional, default: `false`): If `true`, also render a Scribe-style HTML walkthrough. Requires `pip install sop-agent[visual]`.

**Constraints for parameter acquisition:**
- If all required parameters are already provided, You MUST proceed to the Steps
- If any required parameters are missing, You MUST ask for them before proceeding
- When asking for parameters, You MUST request all parameters in a single prompt
- When asking for parameters, You MUST use the exact parameter names as defined
- You MUST support multiple input methods for `description`:
  - Direct input: text provided in the conversation
  - File path: a markdown file containing a brief
  - URL: a link to an internal brief or ticket
- You MUST confirm classification (pillar + service_line) with the user before proceeding to step 4 if you inferred them
- You MUST NOT silently substitute a default for `archetype_override` because picking the wrong archetype produces an SOP at the wrong depth, which is the single most user-visible failure mode of this framework

## Steps

### 1. Load Active Overlay

Resolve the active overlay using the loader's precedence chain and load its contents into context.

**Constraints:**
- You MUST call the overlay loader (precedence: `--overlay` flag, then `$SOP_AGENT_OVERLAY` env var, then `~/.sop-agent/overlay/`, then bundled `examples/` fallback)
- You MUST read every file present under `governance/`:
  - `design-principles.md`
  - `measurement-principles.md`
  - `brand-voice.md`
  - `tool-inventory.md`
  - `org-profile.md`
- You MUST read every file present under `org-map/`:
  - `roles.yaml`
  - `team-structure.md`
  - `raci-defaults.md`
  - `hiring-priorities.md`
- You MUST surface to the user which overlay source resolved (so they know whether their private content was loaded or the bundled fallback)
- You SHOULD warn the user if the overlay source is `fallback`, since output will be generic rather than organization-specific
- You MUST NOT proceed if `governance/org-profile.md` exists but lacks an `archetype` field, because the rest of the workflow depends on that classification — instead, ask the user to either supply `archetype_override` or run `sop-agent onboard` first

### 2. Classify the Request

Determine the target pillar and service line from the description.

**Constraints:**
- If `pillar` was provided as a parameter, You MUST use it without re-classification
- If `pillar` was not provided, You MUST classify by mapping the description against the six pillars:
  - `strategy` — marketing strategy, marketing analytics
  - `branding` — branding/creative services, content studio
  - `website` — conversion rate optimization, web design + development
  - `acquisition` — paid media, SEO, social media management, content marketing, cold email
  - `retention` — email marketing, SMS marketing
  - `agentic-ai` — AI audit/fit, ready-built AI systems, enterprise agentic AI, automation, agents for small business
- If the description is ambiguous across multiple pillars, You MUST present the user with the top 2-3 candidates and ask them to choose; You MUST NOT guess
- If `service_line` was not provided, You MUST classify the same way within the chosen pillar
- You MUST confirm the classification with the user in a single sentence (`"I'm treating this as Acquisition → SEO. Proceed?"`) before continuing to step 3
- You MAY suggest that the user invoke `/sop-list` if they want to see the full pillar/service taxonomy

### 3. Determine Active Archetype

Pick the output archetype that determines depth, RACI requirements, and template variant.

**Constraints:**
- If `archetype_override` was supplied, You MUST use it
- Otherwise, You MUST read `archetype` from `governance/org-profile.md`
- If both are missing or the value is invalid, You MUST default to `lean` and surface this to the user with a one-line explanation
- You MUST log the resolved archetype to the conversation so the user can see what depth-of-output to expect
- You SHOULD remind the user that they can override per-run with `--archetype <value>`

### 4. Spawn Domain Specialists in Parallel

Fan out three subagents concurrently against the loaded context. Each runs in its own isolated thread per the Claude Agent SDK pattern.

**Constraints:**
- You MUST dispatch the following three subagents *in parallel*, not sequentially:
  1. **Pillar Specialist** (`agents/pillar-{pillar}.md`) — drafts the substantive process steps for the chosen service line
  2. **Tool Mapper** (`agents/tool-mapper.md`) — matches each draft step to a tool from `governance/tool-inventory.md`
  3. **Org Mapper** (`agents/org-mapper.md`) — assigns RACI per step from `org-map/roles.yaml` and runs gap analysis
- Each subagent MUST receive:
  - The user's `description`
  - The resolved `pillar` and `service_line`
  - The resolved `archetype`
  - Read access to the full overlay
- You MUST wait for all three subagents to complete before proceeding to step 5
- You MUST NOT pass any subagent's draft as input to another subagent in this round, because they operate on independent dimensions; cross-pollination at this stage muddies the contributions and makes failure attribution harder
- If a subagent returns an error or empty output, You MUST surface the specific failure and retry that subagent only — do not regenerate the whole workflow

### 5. Synthesize Draft

Merge the three subagent outputs into a single coherent draft SOP.

**Constraints:**
- You MUST produce a draft with these sections (sized to the active archetype):
  - Title
  - Purpose
  - Definition of Done
  - Prerequisites
  - Roles + RACI (per `archetype` requirements — see step 7's rubric)
  - Tools
  - Process steps (numbered, verb-first per `governance/design-principles.md`)
  - KPIs / Quality metrics
  - Escalation path
  - Related SOPs
  - Changelog (initial entry only)
- You MUST resolve conflicts between subagent outputs deterministically:
  - Tool Mapper's tool selection takes precedence over Pillar Specialist's tool suggestions when they disagree
  - Org Mapper's role assignment takes precedence over Pillar Specialist's implicit assignments
  - Pillar Specialist's step ordering is authoritative
- You MUST insert a `[GAP]` marker on any step where Org Mapper flagged a missing role, with the suggested hire/contractor recommendation appended
- You MUST save the draft to a scratch path under `.sop-output/.drafts/{slug}-draft-v1.md` for the validation round to inspect

### 6. Validate Against Governance (parallel)

Run the Governance Validator and QA Evaluator concurrently against the draft.

**Constraints:**
- You MUST dispatch the following two subagents *in parallel*:
  1. **Governance Validator** (`agents/governance-validator.md`) — checks the draft against every constraint declared in `governance/design-principles.md`, `governance/brand-voice.md`, and `governance/measurement-principles.md`; returns a list of violations with severity (`critical`, `high`, `medium`, `low`)
  2. **QA Evaluator** (`agents/qa-evaluator.md`) — scores the draft against the rubric for the active archetype; returns a score per dimension and an aggregate
- You MUST wait for both to complete before deciding next step

### 7. Score Against Rubric and Decide

Interpret the validation results and decide whether to ship, revise, or block.

**Constraints:**
- The QA Evaluator's rubric scales by archetype:

  | Dimension | Lean threshold | Coordinated threshold | Compliance-Forward threshold |
  |---|---|---|---|
  | Clarity | 7/10 | 7/10 | 8/10 |
  | Completeness | 6/10 | 8/10 | 9/10 |
  | Measurability | 6/10 | 7/10 | 9/10 |
  | Role-fit | 6/10 | 8/10 | 9/10 |
  | Brand alignment | 7/10 | 7/10 | 7/10 |

- You MUST block delivery if *any* Governance Validator finding has severity `critical`
- You MUST block delivery if the aggregate QA score falls below the active archetype's minimum (Lean: 32, Coordinated: 37, Compliance-Forward: 42)
- If blocked, You MUST loop back to step 5 with the specific findings as feedback, but You MUST NOT exceed 3 revision cycles per run — after the third attempt, You MUST surface the remaining issues to the user and ask whether to ship anyway or abandon
- If not blocked but `high` findings exist, You MUST proceed but include the findings in the user-facing summary
- You SHOULD log each revision cycle's score progression so the user can see whether iteration is converging

### 8. Render Final Artifacts in Parallel

Once the draft passes validation, spawn the renderers concurrently.

**Constraints:**
- You MUST dispatch the following subagents *in parallel*:
  1. **SOP Author** (`agents/sop-author.md`) — renders the Markdown deliverable from the appropriate template at `templates/sop-employee.md.j2` (or `templates/checklist.md.j2` for Lean), applying brand voice, tone, and vocabulary preferences from `governance/brand-voice.md`
  2. **Visual Renderer** (`agents/visual-renderer.md`) — *only if* `visual: true` and the `[visual]` extra is installed; otherwise skipped silently
- The SOP Author MUST honor any reading-level target declared in `governance/brand-voice.md`
- The SOP Author MUST NOT introduce content that didn't appear in the validated draft; rendering is a transformation, not an authoring step
- You MUST write the final Markdown to `{output_path}/{slug}.md`
- If `output_format` is `pdf` or `html`, You MUST invoke the corresponding exporter after the Markdown is written
- You MUST clean up the `.sop-output/.drafts/` directory for this slug after successful render

### 9. Summarize for the User

Report what was created, what was found, and what to do next.

**Constraints:**
- You MUST return a concise summary that includes:
  - The output file path(s)
  - The resolved pillar, service line, and archetype
  - The final QA score breakdown
  - Any `[GAP]` markers flagged by Org Mapper, with the suggested resolution
  - Any non-blocking governance findings, grouped by severity
  - The number of revision cycles needed
- You MUST NOT include the full SOP content in the summary; reference the file instead
- You SHOULD suggest the next logical action — typically reviewing the SOP, running `/sop-audit` on a related existing SOP, or invoking the publisher

## Examples

### Example 1: Lean operator requests a quick checklist

**Input:**
- `description: "Monthly client newsletter send"`
- (no other parameters)

**Expected agent behavior:**
1. Loads overlay; detects archetype = `lean` from `org-profile.md`
2. Classifies as `retention → email-marketing`; confirms with user
3. Dispatches Pillar Specialist (retention), Tool Mapper, Org Mapper in parallel
4. Synthesizes a 5-step checklist, ~1 page, single role assigned (no formal RACI)
5. Validates; QA score = 38/50; no critical findings
6. Renders Markdown to `.sop-output/monthly-client-newsletter-send.md`
7. Summarizes: "Created Lean-format SOP, single owner (Marketing Lead), 1 [GAP] flagged at step 3 (no copywriter on staff — recommend contractor or AI-assist)"

### Example 2: Compliance-forward organization requests a regulated workflow

**Input:**
- `description: "Quarterly access review for PHI-handling systems"`
- `archetype_override: "compliance-forward"`

**Expected agent behavior:**
1. Loads overlay; uses override
2. Classifies as `agentic-ai → enterprise-agentic-ai` (or escalates if no fit; may need new pillar)
3. Dispatches subagents; Org Mapper detects multi-tier approval requirements from `raci-defaults.md`
4. Synthesizes a draft with full R/A/C/I per step, risk register, change-management protocol, and SOC 2 references
5. First validation finds 2 `high` findings on missing audit-trail language; iterates
6. Second validation passes; QA = 43/50
7. Renders ~5-page Markdown plus PDF export
8. Summarizes including the approval matrix and the 2 governance findings that were resolved

### Example 3: User provides a URL brief

**Input:**
- `description: "https://notion.so/atlas/seo-monthly-audit-brief"`

**Expected agent behavior:**
1. Detects URL input, fetches the brief content
2. Confirms successful retrieval with the user before proceeding
3. Continues normally from step 1

## Troubleshooting

### Classification keeps cycling between two pillars
If the agent can't decide between (e.g.) `acquisition → content-marketing` and `branding → content-studio`, ask the user to disambiguate by intent: "Is this about *attracting new leads* (acquisition) or *producing brand assets* (branding)?" Save the chosen classification as a hint for future similar requests by appending to `governance/classification-hints.md`.

### Subagent times out or returns empty
Retry that subagent once with a slightly rephrased prompt. If it fails twice, fall back to having the Conductor itself perform that subagent's job, and flag this as a meta-issue worth filing as a bug.

### QA score never converges across 3 cycles
This usually means a governance constraint contradicts the archetype's depth requirements (e.g., `design-principles.md` demands sub-1-page output but `org-profile.md` says `compliance-forward`). Surface the contradiction to the user and ask whether to relax governance or change archetype for this run.

### Overlay loader returns `fallback`
The user hasn't run `sop-agent onboard` yet, or their overlay path is missing. Generate the SOP using the bundled `examples/lean-operator/` defaults but prefix the output with a warning that the SOP is not tailored to their organization.

### `[GAP]` markers in unexpected places
If gap analysis flags a step that's obviously someone's job at the org, the issue is that `roles.yaml` either lacks the role or its `can_own` array doesn't include the relevant pillar. Suggest the user run `sop-agent audit-overlay` (Phase 2) or edit `roles.yaml` directly.
