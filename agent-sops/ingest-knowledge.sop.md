# Ingest Knowledge

## Overview

This meta-SOP guides the SOP Agent through ingesting new organizational information — a document, a chat export, meeting notes, a new tool announcement, a process change — and propagating it through the overlay and the existing SOP library.

This is the maintenance loop that keeps an SOP library alive. Organizations don't rewrite their SOPs when things change; they accumulate small changes (a new automation, a renamed role, a revised KPI, an extra checklist item) and the library silently rots. Ingest reverses that: **drop information in → the overlay updates → affected SOPs get flagged and refreshed.**

This is the workflow invoked by `sop-agent ingest <source>` and by `/sop-ingest` in Claude Code.

The flow has three stages: **classify** (which overlay files does this touch?), **apply** (diff-and-approve updates to the overlay), and **propagate** (find existing SOPs invalidated by the change and offer to refresh them via the audit workflow).

## Parameters

- **source** (required): The new information. Accepts:
  - A file path (markdown, text, or any readable document)
  - A URL
  - Direct text pasted into the conversation
- **scope_hint** (optional): Which overlay area the user believes this affects: `governance`, `org-map`, `playbooks`, `tools`, `automations`, `roles`, or `unknown` (default). The agent verifies rather than trusts the hint.
- **propagate** (optional, default: `ask`): What to do about affected SOPs after the overlay updates:
  - `ask` — list affected SOPs and let the user choose which to refresh
  - `auto` — automatically run the audit workflow in `patch` mode on every affected SOP
  - `none` — update the overlay only; skip SOP propagation
- **dry_run** (optional, default: `false`): If `true`, produce the classification and proposed diffs but write nothing.

**Constraints for parameter acquisition:**
- If all required parameters are already provided, You MUST proceed to the Steps
- If any required parameters are missing, You MUST ask for them before proceeding
- When asking for parameters, You MUST request all parameters in a single prompt
- When asking for parameters, You MUST use the exact parameter names as defined
- You MUST confirm successful acquisition of the source content (file read, URL fetched, or text received) before classifying, because misread input produces confidently wrong overlay edits

## Steps

### 1. Load Active Overlay

Resolve and load the overlay this ingestion will modify.

**Constraints:**
- You MUST resolve the overlay via the standard precedence chain (flag → env → auto-discovery)
- You MUST NOT proceed against the `fallback` source because ingestion writes to the overlay, and the bundled examples are read-only reference material — instead, tell the user to run onboarding first or pass an explicit `--overlay` path
- You MUST read the overlay's current state: all `governance/` files, all `org-map/` files, any `playbooks/`, and the `sops/` directory listing (filenames + metadata blocks only, not full contents — that comes later)

### 2. Read and Summarize the Source

Acquire the new information and play it back.

**Constraints:**
- You MUST read the full source content
- You MUST produce a 3-6 bullet summary of what the source contains and present it to the user with: "Here's what I read. Is this the information you want ingested?"
- You MUST wait for confirmation before classifying, because users frequently paste the wrong file or an outdated version
- If the source exceeds roughly 2,000 lines, You SHOULD ask the user whether to ingest all of it or a specific section

### 3. Classify Against the Overlay

Determine which overlay files the new information touches, and how.

**Constraints:**
- You MUST classify every distinct fact or change in the source into one of:
  - **`governance/org-profile.md`** — org facts: size, services, clients, operating model
  - **`governance/tool-inventory.md`** — new, changed, or retired tools
  - **`governance/automation-inventory.md`** — new, changed, or retired automations
  - **`governance/segmentation-tags.md`** — new or changed segment tags
  - **`governance/design-principles.md`** — new rules about how SOPs should be built
  - **`governance/brand-voice.md`** — voice, vocabulary, tone changes
  - **`governance/measurement-principles.md`** — KPI or quality-bar changes
  - **`org-map/roles.yaml`** — role additions, removals, responsibility or reporting changes
  - **`org-map/team-structure.md`** — structure, capacity, or gap-resolution changes
  - **`org-map/hiring-priorities.md`** — hiring plan changes
  - **`playbooks/*`** — domain process changes (new steps, changed standards, new phases)
  - **`no-op`** — information already reflected in the overlay (note it, don't re-write it)
  - **`out-of-scope`** — information that doesn't belong in the overlay (client-specific data, credentials, one-off tasks); name where it should live instead
- You MUST present the classification as a table: fact → target file → change type (add / modify / remove / no-op)
- You MUST flag any fact that *contradicts* the current overlay separately and prominently, because contradictions are either real strategy changes (important) or source errors (dangerous) — the user decides which
- You MUST NOT classify credentials, API keys, or login details into any overlay file because the framework never stores credentials; flag them as out-of-scope

### 4. Generate Diffs

For each overlay file with changes, produce a concrete before/after diff.

**Constraints:**
- You MUST show the user a unified-style diff (or clear before → after excerpt) for every file you propose to change
- You MUST keep edits surgical — modify the specific lines the new information affects; do not rewrite whole files because wholesale rewrites destroy provenance and invite regressions
- You MUST preserve each file's existing structure and schema
- If `dry_run` is `true`, You MUST stop after presenting the diffs and write nothing

### 5. Apply Approved Changes

Get approval and write.

**Constraints:**
- You MUST ask for approval before writing — either per-file or "approve all," at the user's preference
- You MUST apply only approved diffs
- You MUST append an ingest log entry to `{overlay}/INGEST-LOG.md` (create it if missing) recording: timestamp, source description, files changed, one-line summary per change — because the overlay's evolution history is what makes future contradictions debuggable
- If the overlay is a git repository, You SHOULD offer to commit the changes with a descriptive message
- You MUST NOT modify `source/` reference documents in the overlay because they are immutable historical records; the structured files are the living layer

### 6. Identify Affected SOPs

Find existing SOPs that the overlay changes may have invalidated.

**Constraints:**
- You MUST scan every SOP in `{overlay}/sops/` (and any user-registered SOP output directories) for references to the changed content:
  - Changed/removed roles → SOPs whose `owner_role` or task assignments reference them
  - Changed/removed tools → SOPs referencing those tools
  - New/changed automations → SOPs containing manual tasks the automation now covers (these are now governance violations)
  - Changed playbook standards → SOPs generated from the affected phases or sections
  - Changed tags → SOPs using the affected tag vocabulary
- You MUST present the affected-SOP list with, per SOP: filename, what changed that affects it, and estimated impact (`low` — cosmetic; `medium` — content updates needed; `high` — workflow is now wrong)
- If no SOPs are affected, You MUST say so explicitly and finish at step 8

### 7. Propagate (per the propagate parameter)

Refresh the affected SOPs.

**Constraints:**
- If `propagate: none`, You MUST skip to step 8
- If `propagate: ask`, You MUST let the user select which affected SOPs to refresh
- If `propagate: auto`, You MUST queue all `medium` and `high` impact SOPs
- For each selected SOP, You MUST invoke the audit workflow (`audit-sop.sop.md`) in `patch` mode, passing the specific overlay changes as context so the audit focuses on the deltas rather than re-checking everything
- For SOPs the audit verdict marks `regenerate`, You MUST surface that recommendation and let the user decide — regeneration is a bigger step than ingestion implies
- You MUST NOT modify any SOP without the audit workflow's diff-and-approve loop, because silent SOP edits break the trust that makes the library authoritative

### 8. Summarize

Close the loop.

**Constraints:**
- You MUST report: source ingested, overlay files changed (with counts), SOPs affected / refreshed / deferred, and any out-of-scope or contradictory items that need human follow-up
- You MUST remind the user of deferred items ("3 SOPs flagged but not refreshed — run `/sop-audit` on them when ready")
- You SHOULD suggest updating the overlay's source documents folder if the ingested material is a substantial reference document worth archiving

## Examples

### Example 1: New automation announced

**Input:**
- `source`: "We built a new automation: the Schema Validator Bot. It runs nightly and validates structured data on all newly published articles, posting failures to the #seo-alerts channel. Justin gets the escalations."

**Expected behavior:**
1. Summary played back; user confirms
2. Classification: add to `automation-inventory.md` (add); no contradictions
3. Diff shown: new automation entry with what-it-does / replaces / human checkpoint / SOP rule
4. Applied; INGEST-LOG.md entry written
5. Affected SOPs: any SOP with a manual "validate schema on new articles" task → flagged `high` (now duplicates an automation)
6. User approves propagation → audit-patch converts those tasks to verification tasks
7. Summary: 1 overlay file changed, 2 SOPs refreshed

### Example 2: Role responsibility change

**Input:**
- `source`: meeting notes — "Moving GBP photo updates from the Off-Page Specialist to the Content Writers since they're already producing the visual assets."

**Expected behavior:**
1. Confirmed; classified: `roles.yaml` (modify two roles' responsibilities)
2. Contradiction flag: current `roles.yaml` says writers never publish directly — does GBP photo posting violate that? Surfaced to user for decision
3. User clarifies (writers upload to a queue; Content Lead approves) → diff reflects the nuance
4. Applied; affected SOPs: the local-SEO maintenance SOP reassigns the photo-update task
5. Audit-patch run; owner changed; changelog entries added

### Example 3: Dry run of a big strategy doc

**Input:**
- `source`: "strategy-update-q3.md" (large doc)
- `dry_run`: true

**Expected behavior:**
1. Doc read; 6-bullet summary confirmed
2. Classification table: 14 facts → 5 overlay files; 2 contradictions flagged; 1 out-of-scope (client pricing — doesn't belong in overlay)
3. Diffs presented for all 5 files
4. Nothing written; user reviews and re-runs without `dry_run` when ready

## Troubleshooting

### The source contradicts the overlay in many places
That usually means the overlay is stale, not the source. Offer two paths: ingest the source as the new truth (bulk-apply), or walk contradictions one at a time. For more than ~10 contradictions, recommend re-running onboarding against the new document instead of incremental ingestion.

### Classification puts everything in `playbooks/`
Domain-heavy sources (process docs) legitimately concentrate there. But check whether facts about roles, tools, or automations are embedded in the process prose — pull those out into their structured homes too. The playbook holds *process*; everything else has a dedicated file.

### The user pastes credentials in the source
Stop. Flag them, exclude them from all writes, and recommend the credentials go into the org's password manager. The overlay never stores secrets — it's designed to be shareable with the team.

### An affected SOP is mid-edit by a human
If the SOP file has uncommitted changes (when under git), the audit workflow will refuse to patch it. Defer that SOP and note it in the summary rather than blocking the whole ingestion.

### Ingestion is requested but no overlay exists
Don't improvise an overlay from the ingested document alone. Route to onboarding (`onboard-org.sop.md`) with the document as a pre-supplied input — onboarding asks the structured questions ingestion can't infer.
