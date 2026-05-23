# Governance

> This folder is **intentionally empty in the public repo**. It defines the *shape* of your organization's private governance overlay. Your actual content belongs in your overlay path (see [SCHEMA.md](./SCHEMA.md)), never here.

## What governance is

Governance is the layer that makes every SOP this framework produces feel like *yours*. It encodes the rules that apply across every department — your design principles, how you measure success, your brand voice, what tools you own. Without governance, the agent has no opinion about what "good" looks like in your organization.

Governance is loaded *first* and applies to every subsequent agent decision.

## How to populate yours

You have three options, in order of preference:

1. **Use the overlay pattern (recommended)** — keep your real governance in a private folder outside this repo, and point the framework at it via the `--overlay <path>` flag, the `$SOP_AGENT_OVERLAY` env var, or `~/.sop-agent/overlay/`. Your content stays private; you can keep it in a private Git repo for versioning.

2. **Use an example as a starting point** — pick whichever of the three archetypes in [`examples/`](../examples/) most resembles your operation, copy it to your overlay path, and edit from there.

3. **Run the onboarding interview** — `sop-agent onboard` walks you through a structured conversation and writes a starter overlay for you.

## What goes in governance

Five files, each with a single, clear purpose:

| File | Purpose |
|---|---|
| `design-principles.md` | How your SOPs should be designed — voice, length, depth, formatting preferences |
| `measurement-principles.md` | How outcomes are measured — what counts as "done well" across every SOP |
| `brand-voice.md` | Tone, terminology, vocabulary your organization uses |
| `tool-inventory.md` | The tools your team actually owns, organized by category |
| `org-profile.md` | High-level snapshot — size, archetype, services, client mix |

See [SCHEMA.md](./SCHEMA.md) for the full structure of each file.

## What does NOT go in governance

- Per-SOP specifics (those belong in the SOP itself)
- Role definitions (those belong in [`org-map/`](../org-map))
- Client-specific information (use `client-context/` in your overlay if you need this)
- Anything secret or credentialed (the framework never asks for credentials)
