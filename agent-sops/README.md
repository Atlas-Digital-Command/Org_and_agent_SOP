# Agent SOPs (Meta-SOPs)

Workflows the **agent itself** follows. These are `.sop.md` files using the RFC 2119 format (`MUST` / `SHOULD` / `MAY`), inspired by the [strands-agents/agent-sop](https://github.com/strands-agents/agent-sop) project.

These are *not* the SOPs your team executes — those are the *output* the agent produces. These are the recipes the agent uses internally.

**Coming in Phase 1:**
- `new-sop.sop.md` — canonical "create an SOP" workflow
- `onboard-org.sop.md` — onboarding interview
- `audit-sop.sop.md` — review and refresh an existing SOP
- `publish-sop.sop.md` — distribute to exporters

See [`../docs/architecture.md`](../docs/architecture.md) for how meta-SOPs fit into the agent flow.
