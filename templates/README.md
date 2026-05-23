# Templates

Jinja2 templates the SOP Author and Visual Renderer use to produce the final human-facing artifact.

**Coming in Phase 1:**
- `sop-employee.md.j2` — primary Markdown SOP template
- `checklist.md.j2` — quick-checklist variant (Lean archetype default)
- `mermaid-flow.j2` — process diagram for SOPs with sequential steps

**Coming in Phase 3:**
- `visual-render.html.j2` — Scribe-style HTML walkthrough

Templates are archetype-aware via Jinja conditionals — the same template renders differently for Lean vs Compliance-Forward based on the active org profile.
