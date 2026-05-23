# Audit SOP

## Overview

This meta-SOP guides the SOP Agent through reviewing an existing SOP and identifying everything that's stale: roles that no longer exist, tools that are no longer in the inventory, language that no longer matches the current brand voice, archetype-fit drift (the SOP was written for a 5-person team and now there are 50), and structural issues.

The output is an **audit report** with severity-classified findings and a clear recommendation: ship as-is, patch the specific issues, or regenerate from scratch.

This is the workflow invoked by `sop-agent audit <path>` and by `/sop-audit` in Claude Code.

Auditing is intentionally lightweight — it does *not* re-run the full subagent fan-out used by `new-sop.sop.md`. It is a comparison pass between an existing artifact and the current overlay. Full regeneration is offered as an explicit follow-up action, not the default.

## Parameters

- **sop_path** (required): Path to the SOP file to audit. Accepts `.md` files (generated SOPs) or `.sop.md` files (meta-SOPs).
- **mode** (optional, default: `report`): One of:
  - `report` — produce findings only, do not modify anything
  - `patch` — produce findings and offer to apply minimal edits in place for fixable findings
  - `regenerate` — produce findings and offer to re-run `new-sop.sop.md` against the original description, replacing the file
- **scope** (optional, default: `all`): Which dimensions to audit. Comma-separated subset of: `structure`, `roles`, `tools`, `voice`, `archetype-fit`, `governance`, `freshness`.
- **threshold** (optional, default: `warn`): Severity at which the audit returns a non-zero exit code. One of `critical`, `high`, `medium`, `low`. Useful for CI use.

**Constraints for parameter acquisition:**
- If all required parameters are already provided, You MUST proceed to the Steps
- If any required parameters are missing, You MUST ask for them before proceeding
- When asking for parameters, You MUST request all parameters in a single prompt
- When asking for parameters, You MUST use the exact parameter names as defined
- If `mode = patch` or `mode = regenerate` and the SOP file is under version control with uncommitted changes, You MUST refuse to proceed and ask the user to commit or stash first, because modifications could overwrite their work

## Steps

### 1. Load the Target SOP

Read the file and parse its structure.

**Constraints:**
- You MUST verify the file exists and is readable; fail clearly if not
- You MUST detect the SOP type from the file extension and content:
  - `.sop.md` → meta-SOP (uses RFC 2119 format)
  - `.md` with the framework's section markers (Purpose, Definition of Done, etc.) → generated SOP
  - Other → ask the user to confirm what kind of SOP this is
- You MUST extract metadata from the SOP if present:
  - Version / changelog
  - Original archetype (if recorded)
  - Last-updated date
  - Original `description` parameter (if recorded in a `<!-- meta: ... -->` comment block)
- You MUST NOT mutate the file at this stage, regardless of `mode`

### 2. Load Active Overlay

Resolve the current overlay so the audit has something to compare against.

**Constraints:**
- You MUST call the overlay loader per the standard precedence (flag → env → auto-discovery → fallback)
- You MUST surface the overlay source to the user, because auditing against the bundled `examples/` fallback will produce misleading findings if the SOP was authored against a real overlay
- You SHOULD warn and offer to abort if the overlay source is `fallback` and the SOP file looks like it was generated against a real overlay (heuristic: contains role names that don't appear in the bundled examples)

### 3. Structural Audit

Verify the SOP has the sections and shape its archetype requires.

**Constraints:**
- You MUST check for the presence of required sections per the active archetype:
  - **Lean**: Purpose, Process steps, KPIs (minimum viable)
  - **Coordinated**: above + Definition of Done, Roles, Tools, Escalation path
  - **Compliance-Forward**: above + Risk register, Approval matrix, Changelog with full audit trail
- You MUST flag missing required sections as `high` severity findings
- You MUST flag extra sections that violate `governance/design-principles.md` declared structure as `medium` severity
- You SHOULD flag steps that exceed any `max_words_per_step` constraint declared in design principles as `low` severity
- For `.sop.md` files only, You MUST also run `agent-sops/validate-sop.sh` against the file and incorporate its output

### 4. Role and RACI Audit

Verify every role assignment in the SOP still maps to an existing role in `org-map/roles.yaml`.

**Constraints:**
- You MUST parse all role references in the SOP (typically in the `## Roles` section and inline RACI chips like `[R: account-strategist]`)
- For each referenced role, You MUST verify:
  - The role ID exists in `roles.yaml`
  - The role's `can_own` array includes the relevant pillar (matching the SOP's classification, if available from metadata)
  - The role's `headcount` is greater than zero
- Missing role → `high` severity finding with suggested fix: either update the SOP to use a current role, or add the missing role to `roles.yaml`
- `headcount: 0` (vacant role) → `medium` severity with suggestion: assign a backup or flag as `[GAP]`
- Role exists but `can_own` mismatch → `medium` severity with suggestion: either update `can_own` or reassign
- If the SOP archetype requires RACI but the SOP is missing R/A/C/I assignments per step, that's a `high` severity finding (separate from missing-role findings)

### 5. Tool Audit

Verify every tool referenced in the SOP still exists in `governance/tool-inventory.md`.

**Constraints:**
- You MUST parse all tool references in the SOP — look in the `## Tools` section and inline mentions in steps
- For each tool, You MUST verify it appears in the current `tool-inventory.md`
- Missing tool → `high` severity finding, because the SOP instructs the user to use a tool the organization doesn't own
- You SHOULD suggest the most plausible replacement from the current inventory based on category match
- Tool exists but in a different category than when the SOP was written → `low` severity informational note only

### 6. Brand Voice Audit

Sample sections of the SOP and compare against the current `brand-voice.md`.

**Constraints:**
- You MUST sample 3-5 representative passages (intro, a process step, the KPI section)
- You MUST evaluate each sample against:
  - Tone descriptors declared in `brand-voice.md`
  - Vocabulary preferences (forbidden words / required phrasings)
  - Reading-level target
- Deviations from declared voice → `medium` severity findings with the specific offending phrase quoted
- This audit is inherently fuzzy; You MUST cap voice findings at the top 5 most impactful issues — long lists of minor voice quibbles are noise

### 7. Archetype-Fit Audit

Determine whether the SOP's depth still matches the current organizational archetype.

**Constraints:**
- You MUST compare the SOP's current depth (length, RACI depth, section count) against what the active archetype expects
- If the SOP is *too thin* for the current archetype (e.g., a Lean SOP at a now-Compliance-Forward org), that's a `high` severity finding with the recommendation "regenerate at current archetype"
- If the SOP is *too deep* for the current archetype (rare but possible if the org has simplified), that's a `medium` severity finding with the recommendation "regenerate or trim"
- If the SOP's recorded archetype matches the current archetype, no archetype-fit finding is generated

### 8. Governance Audit

Run the same checks that `new-sop.sop.md` step 6 runs, scoped to the current SOP.

**Constraints:**
- You MUST invoke the Governance Validator subagent against the loaded SOP
- You MUST include all `critical` and `high` findings from the validator in the audit report
- You MUST NOT block the audit run on validator findings — the audit's job is to report, not to gate; the user decides what to do

### 9. Freshness Audit

Check whether the SOP is overdue for review based on declared cadence.

**Constraints:**
- You MUST check for a `last_updated` date in the SOP metadata
- If absent, You MUST flag as `low` severity with the suggestion to add metadata going forward
- If present, You MUST compare against any `review_cadence_days` declared in `governance/design-principles.md` (default: 180 days if unset)
- Overdue by less than 30 days → `low` severity
- Overdue by 30-90 days → `medium` severity
- Overdue by 90+ days → `high` severity

### 10. Compile the Audit Report

Assemble all findings into a single report and write it out.

**Constraints:**
- You MUST produce a report with this structure:
  - Header (SOP path, audit timestamp, overlay source, archetype, total findings count by severity)
  - Summary verdict — one of:
    - `ship` (no critical or high findings)
    - `patch` (no critical, some high or medium — recommend targeted edits)
    - `regenerate` (critical or many high — recommend full regeneration)
  - Findings table, grouped by dimension (Structure, Roles, Tools, Voice, Archetype-fit, Governance, Freshness)
    - For each finding: severity, location in the SOP (line range), description, suggested fix
  - Recommended next action (if any)
- You MUST write the report to `{sop_dir}/{sop_filename}.audit-{timestamp}.md`
- You MUST also print a one-screen summary to the terminal

### 11. Execute the Mode-Specific Action

Take the action the user requested via the `mode` parameter.

**Constraints:**
- If `mode = report`, You MUST stop after writing the audit report; do not modify the SOP
- If `mode = patch`, You MUST present each `high` and `medium` finding's suggested fix to the user one at a time and ask for approval before applying it; You MUST update the SOP's changelog with an entry per applied patch
- If `mode = regenerate`, You MUST:
  - Verify the SOP file's metadata contains the original `description` parameter
  - If absent, ask the user to supply it
  - Invoke `new-sop.sop.md` with the captured description and the current overlay
  - Write the new SOP to a `.regenerated.md` filename adjacent to the original
  - Show the user a diff and ask whether to replace or keep both
- You MUST NOT replace the original SOP file without explicit user confirmation, regardless of mode

## Examples

### Example 1: Quick CI audit, report-only

**Input:**
- `sop_path: "docs/sops/monthly-seo-audit.md"`
- `mode: "report"`
- `threshold: "high"`

**Expected agent behavior:**
1. Loads SOP and overlay
2. Runs all audit dimensions
3. Writes `docs/sops/monthly-seo-audit.md.audit-2026-05-22T14-32-08.md`
4. Returns exit code 0 (no `high` or `critical` findings) → CI passes

### Example 2: Stale SOP discovered, patch mode

**Input:**
- `sop_path: "docs/sops/quarterly-content-review.md"`
- `mode: "patch"`

**Expected agent behavior:**
1. Loads SOP; detects it references role `content-writer` which has been renamed to `content-strategist`
2. Flags 1 high finding (role rename), 2 medium findings (voice drift, archetype upgrade since SOP was written)
3. Asks user about each: "Replace `content-writer` with `content-strategist` throughout? [y/n]"
4. On approval, applies the rename and adds a changelog entry
5. Skips the voice drift fix (asks user explicitly; user declines for now)
6. Writes the audit report alongside the patched SOP

### Example 3: Severely outdated SOP, regenerate mode

**Input:**
- `sop_path: "old-sops/website-launch-checklist.md"`
- `mode: "regenerate"`

**Expected agent behavior:**
1. Loads SOP; detects metadata `description: "End-to-end checklist for launching a new client website"` and `archetype: lean`
2. Detects active archetype is now `coordinated-specialist`; flags as critical archetype-fit issue
3. Confirms with user: "Regenerate using description '{captured}' at current archetype 'coordinated'? [y/n]"
4. On approval, invokes `new-sop.sop.md` with the captured description
5. Writes `old-sops/website-launch-checklist.regenerated.md`
6. Shows side-by-side summary; asks user whether to replace the original

## Troubleshooting

### SOP has no metadata
Older or hand-authored SOPs may not have a metadata block. Run audit with `mode: report` to surface what's auditable; for `mode: regenerate`, the agent will prompt the user for the original description.

### Audit produces too many findings to act on
That usually means the overlay has drifted significantly since the SOP was written. Recommend running `sop-agent onboard --resume` first to refresh the overlay, then re-running the audit. Cap finding count in the terminal summary at 20; the full set lives in the audit report file.

### Patch mode loops on the same finding
If a suggested fix doesn't fully resolve a finding (e.g., a voice rephrase introduces a different voice issue), the agent MUST stop applying that category of patch and surface the conflict for human resolution rather than iterating mechanically.

### Audit report file collision
The timestamp in the report filename should prevent collisions, but if two audits run within the same second, append a counter (`.audit-{timestamp}-2.md`) rather than overwriting.

### Voice audit hallucinates issues
This dimension is the most error-prone. If the user reports false positives, the agent SHOULD lower its sensitivity by sampling fewer passages and using stricter exact-match rules from `brand-voice.md` rather than semantic similarity. Open an issue with the false-positive example so the framework can improve.
