# Onboard Organization

## Overview

This meta-SOP guides the SOP Agent through a structured interview with a new user to build their initial governance + org-map overlay. The result is a fully populated overlay directory the framework can load on every subsequent run.

This is the workflow invoked by `sop-agent onboard` and by `/sop-onboard` in Claude Code.

The interview is **archetype-detection-first**: the agent runs a short diagnostic to place the organization on the Directness/Efficiency ↔ Compliance/Thoroughness scale, then asks only the questions appropriate for that archetype. A Lean Operator answers ~12 questions in about 8 minutes; a Compliance-Forward organization answers ~30 questions in about 25 minutes.

The agent MUST favor brevity — every unnecessary question erodes trust and accuracy. "Lowest common denominator" applies to onboarding itself, not just to output.

## Parameters

- **overlay_path** (optional): Where to write the new overlay. If omitted, the agent MUST resolve the destination in this order:
  1. The `--overlay` CLI flag value
  2. The `$SOP_AGENT_OVERLAY` environment variable
  3. `~/.sop-agent/overlay/` (default)
- **mode** (optional, default: `interactive`): One of:
  - `interactive` — full conversation (default)
  - `from_template` — copy a bundled archetype as starting point, skip the interview
  - `from_existing` — read an existing partial overlay and only ask for missing fields
- **template_archetype** (optional): Required if `mode = from_template`. One of `lean`, `coordinated`, `compliance-forward`.
- **resume** (optional, default: `false`): If `true`, the agent MUST resume from the last incomplete checkpoint rather than starting over.

**Constraints for parameter acquisition:**
- If all required parameters are already provided, You MUST proceed to the Steps
- If any required parameters are missing, You MUST ask for them before proceeding
- When asking for parameters, You MUST request all parameters in a single prompt
- When asking for parameters, You MUST use the exact parameter names as defined
- If `mode = from_template` and `template_archetype` is missing, You MUST ask for it before any other questions
- You MUST NOT begin overwriting an existing overlay without explicit confirmation, because the user's prior work could be destroyed

## Steps

### 1. Prepare Destination

Establish the target overlay directory and detect existing content.

**Constraints:**
- You MUST resolve `overlay_path` per the parameter precedence above
- You MUST create the directory if it does not exist
- If the directory exists and contains files, You MUST list them to the user and ask explicitly:
  - "Append to existing overlay" — preserve files, only ask about missing ones (equivalent to setting `mode = from_existing`)
  - "Overwrite existing overlay" — back up to `{overlay_path}.backup-{timestamp}/` first, then start fresh
  - "Cancel" — exit cleanly
- You MUST NOT delete or overwrite any file without first creating the timestamped backup
- You SHOULD create a marker file `{overlay_path}/.onboarding-state.json` so the interview can be resumed if interrupted

### 2. Run Archetype Diagnostic

Ask 5 short questions to place the organization on the archetype scale.

**Constraints:**
- You MUST ask exactly these 5 questions, one at a time, in this order:

  1. **Team size.** "How many people are involved in producing the work your SOPs cover?" — capture an integer or range
  2. **Decision authority.** "When a workflow change needs approval, how many distinct people typically have to sign off?" — capture an integer
  3. **Specialization.** "Do most people on your team wear multiple hats across different service areas, or does each person own one specialty?" — capture `multi-hat`, `mixed`, or `specialist`
  4. **Compliance posture.** "Are you actively maintaining a formal compliance framework like SOC 2, HIPAA, or ISO 27001 — or are your obligations limited to client SLAs and standard business norms?" — capture `none`, `client-sla-only`, or list of frameworks
  5. **New-hire cadence.** "Roughly how often does someone new join your team?" — capture `rare`, `quarterly`, `monthly`, or `weekly+`

- You MUST score the responses using this rubric:

  | Question | Lean score | Coordinated score | Compliance-Forward score |
  |---|---|---|---|
  | Team size | 1-10 | 11-75 | 75+ |
  | Approvers | 1 | 2-3 | 4+ |
  | Specialization | multi-hat | mixed | specialist |
  | Compliance | none | client-sla-only | any framework named |
  | New hires | rare | quarterly | monthly or weekly+ |

- You MUST tally the modal archetype across the 5 dimensions; ties between adjacent archetypes (Lean+Coordinated or Coordinated+Compliance) MUST resolve toward the *less complex* one (Lean over Coordinated, Coordinated over Compliance-Forward)
- You MUST surface the detected archetype to the user with a one-line explanation and ask them to confirm or override before continuing
- You MUST NOT proceed past this step until the archetype is confirmed, because every subsequent question's depth depends on this classification

### 3. Capture Organization Profile

Build `governance/org-profile.md` with the foundational facts.

**Constraints:**
- You MUST ask for and capture:
  - Organization name
  - Industry or vertical (one short phrase)
  - Services offered — present a checklist derived from the six pillars and let the user multi-select
  - Average number of clients in flight (Coordinated + Compliance-Forward only)
  - Typical engagement length in months (Coordinated + Compliance-Forward only)
- You MUST ask one question per turn and append the answer to a working `org-profile.md` after each response
- You SHOULD pre-fill the `archetype` field with the value confirmed in step 2
- You MAY skip the optional questions for Lean archetypes — they add depth that the agent doesn't need at that scale
- You MUST conclude this step by writing the completed file to `{overlay_path}/governance/org-profile.md`

### 4. Capture Tool Inventory

Build `governance/tool-inventory.md` organized by category.

**Constraints:**
- You MUST present the user with these categories one at a time, asking only about categories relevant to their selected services:
  - Project management
  - Communication
  - Design + asset creation
  - Analytics + measurement
  - Email + marketing automation
  - SEO + search
  - Paid media
  - Social + content distribution
  - AI + automation
  - Storage + documentation
- For each category, You MUST ask "What tool(s) do you use for {category}?" and accept a comma-separated list, "none", or "skip"
- You SHOULD offer common defaults if the user hesitates (e.g., for project management: "Common choices include Asana, ClickUp, Linear, Trello, Monday — what fits?")
- You MUST NOT prompt the user for credentials or login details — the framework never asks for and never stores credentials
- You MUST write the populated inventory to `{overlay_path}/governance/tool-inventory.md`

### 5. Capture Brand Voice

Build `governance/brand-voice.md` from a small set of high-signal prompts.

**Constraints:**
- You MUST ask these prompts in order:
  1. "In three to five adjectives, how do you want your SOPs to sound? (e.g., 'direct, warm, precise, slightly informal')"
  2. "Are there words or phrases your organization explicitly avoids? (e.g., 'we say *client* not *customer*'; or 'no MBA jargon')"
  3. "What reading level should SOPs target? (Lean default: 'Grade 8, no jargon'; Coordinated: 'Grade 10, light terminology defined inline'; Compliance-Forward: 'Grade 12, technical terms acceptable with glossary')"
  4. **Voice sample.** "Paste a paragraph of your existing internal copy — a Slack post, an email to a client, anything that sounds like your team. The agent will use this as a reference for tone." — accept text, file path, or URL
- You MUST use the voice sample to extract concrete style markers (sentence length, formality, use of contractions, etc.) and include them in the written file as observations
- You SHOULD NOT ask for more than 4 brand-voice questions even in Compliance-Forward archetype — voice is captured better through examples than exhaustive enumeration
- You MUST write the populated voice doc to `{overlay_path}/governance/brand-voice.md`

### 6. Capture Design and Measurement Principles

Build `governance/design-principles.md` and `governance/measurement-principles.md`.

**Constraints:**
- You MUST pre-populate both files with archetype defaults from the bundled `examples/{archetype}/governance/` directory
- You MUST then ask the user three confirmation questions:
  1. "Default SOP length for your archetype is `{archetype-default}`. Override?"
  2. "Required sections in every SOP: `Purpose, Definition of Done, Roles, Tools, Process steps, KPIs`. Add or remove any?"
  3. "Quality score threshold (below which the agent blocks): `{archetype-default}`. Override?"
- You MAY skip steps 2 and 3 for Lean archetypes and just accept the defaults
- You MUST write both files to `{overlay_path}/governance/`

### 7. Capture Roles and Build Org Map

Build `org-map/roles.yaml`, `org-map/team-structure.md`, and (Coordinated + Compliance-Forward) `org-map/raci-defaults.md`.

**Constraints:**
- You MUST ask the user to enumerate roles in this format: "title, seniority (junior/mid/senior/lead/principal), department, count"
- You MUST support batch input — let the user paste a list rather than enter one role at a time
- For each role, You MUST then ask "What kinds of work does this role own?" and accept either:
  - Free text (the agent will map to pillar IDs)
  - Explicit pillar IDs from the framework's taxonomy
- For Lean archetypes, You MAY skip `raci-defaults.md` entirely (Lean SOPs typically don't include formal RACI)
- For Coordinated and Compliance-Forward archetypes, You MUST ask:
  - "When a step needs review-before-proceeding, which role is the default Accountable?"
  - "When a step has compliance implications, which role must always be Consulted?"
- You MUST write valid YAML to `org-map/roles.yaml` (validate before writing)
- You MUST NOT include any specific person's name or email — capture roles, not people

### 8. (Optional) Capture Hiring Priorities

Build `org-map/hiring-priorities.md` if the user opts in.

**Constraints:**
- You MUST ask: "Are there roles you're actively hiring for, or planning to hire in the next 6 months? (You can skip this and add it later.)"
- If the user provides any priorities, You MUST write them to `org-map/hiring-priorities.md` in the schema-defined format
- You MUST NOT block the workflow if the user skips this — it is genuinely optional

### 9. Validate the Overlay

Run a sanity-check pass on the written files before declaring onboarding complete.

**Constraints:**
- You MUST verify every file declared in the schema is present and non-empty
- You MUST run `agent-sops/validate-sop.sh` against any `.sop.md` files in the overlay (if the user supplied custom meta-SOPs in the overlay — rare but supported)
- You MUST validate `roles.yaml` parses as valid YAML
- You MUST validate that any pillar IDs referenced in `roles.yaml.can_own` exist in the framework's taxonomy
- If validation fails, You MUST report the specific file and field, and offer to re-ask the relevant questions

### 10. Summarize and Suggest Next Step

Close the loop with a clean handoff.

**Constraints:**
- You MUST display a summary table:
  - Overlay path
  - Detected archetype (and whether the user confirmed or overrode)
  - Number of services activated
  - Number of tools captured
  - Number of roles captured
  - Files written (with paths)
- You MUST suggest the user run a real SOP next: `sop-agent new "<a SOP they actually need>"`
- You SHOULD remind the user that they can re-run `sop-agent onboard --resume` if anything was incomplete, or edit the overlay files directly at any time
- You MUST NOT mark `.onboarding-state.json` complete until every required file has been written and validated

## Examples

### Example 1: Lean operator — fast path

**Input:**
- (no parameters; user just ran `sop-agent onboard`)

**Expected agent behavior:**
1. Detects no existing overlay at `~/.sop-agent/overlay/`; proceeds to create
2. Asks 5 archetype-diagnostic questions; detects `lean` (5 people, 1 approver, multi-hat, no compliance, rare hires)
3. Asks ~7 follow-up questions: org name, services (multi-select), tools across 4-5 relevant categories, voice sample, role list
4. Writes ~6 files; skips `raci-defaults.md` and `hiring-priorities.md`
5. Total elapsed: ~8 minutes
6. Summarizes and suggests: "Try: `sop-agent new 'Weekly client status email'`"

### Example 2: Compliance-forward organization — full path

**Input:**
- `overlay_path: "~/atlas-overlay"`

**Expected agent behavior:**
1. Detects existing partial overlay (governance/ is empty, org-map/roles.yaml exists from a manual draft)
2. Offers append vs overwrite vs cancel; user picks append
3. Diagnostic detects `compliance-forward` (120 people, 4+ approvers, specialist, SOC 2 active, monthly hires)
4. Asks ~25 follow-up questions across all categories including RACI defaults
5. Validates and writes ~9 files; preserves the existing `roles.yaml`
6. Total elapsed: ~22 minutes
7. Summarizes and suggests: "Try: `sop-agent new 'Quarterly vendor access review'`"

### Example 3: From-template mode for someone in a hurry

**Input:**
- `mode: "from_template"`
- `template_archetype: "coordinated"`
- `overlay_path: "./my-overlay"`

**Expected agent behavior:**
1. Skips the interview entirely
2. Copies `examples/coordinated-specialist/` to `./my-overlay/`
3. Prints a summary listing every file the user should edit before running `sop-agent new`
4. Total elapsed: ~3 seconds

## Troubleshooting

### User abandons mid-interview
The `.onboarding-state.json` marker preserves all answered questions. On the next `sop-agent onboard --resume`, the agent picks up at the next unanswered question. If the user starts a fresh `sop-agent onboard` without `--resume`, the agent MUST detect the partial state and offer to resume vs restart.

### Archetype diagnostic gives a tied result
The constraint in step 2 resolves ties toward the *less complex* archetype. If the user disagrees, they can override at the confirmation prompt — that override is captured and the agent proceeds with their choice.

### Voice sample is missing or thin
The agent SHOULD NOT block onboarding on a missing voice sample. Write `brand-voice.md` with whatever was captured plus a note that the user can add a sample later via `sop-agent overlay --edit brand-voice`. Quality of generated SOPs will improve once a sample is added.

### User provides a person's name in a role definition
Strip it. Roles, not people. If the user objects ("but Sarah is the only one who does this"), explain that role-based mapping makes the overlay portable across staff changes; suggest they capture the actual person separately in their HR system, not in the framework.

### `roles.yaml` doesn't validate
The agent MUST surface the specific YAML error (line + column if available) and offer to walk through the malformed role's fields one at a time to repair it.

### User's industry has compliance terms the framework doesn't know
Capture the framework names verbatim in the compliance question. The framework treats unknown frameworks as "compliance posture: active" for archetype detection without needing built-in knowledge of every regulation.
