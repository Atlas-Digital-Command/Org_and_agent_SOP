<!--
Thanks for opening a PR! A few quick things to help us merge it cleanly.
Delete sections that don't apply.
-->

## Summary

<!-- One or two sentences. What does this PR change and why? -->

## Type of change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature / enhancement (non-breaking change that adds functionality)
- [ ] New service line (under an existing pillar)
- [ ] New pillar (top-level — see new-pillar checklist below)
- [ ] New archetype refinement
- [ ] New exporter (Markdown, PDF, Notion, Confluence, etc.)
- [ ] Documentation
- [ ] Refactor / cleanup
- [ ] Breaking change

## Linked issues

<!-- e.g. Closes #123 -->

## What I changed

<!-- Bulleted list of concrete changes. File names + brief reason are ideal. -->

-
-

## Testing

- [ ] `pytest` passes locally
- [ ] `ruff check` passes
- [ ] `ruff format` was applied
- [ ] If I added/changed an SOP or skill, `validate-sop.sh` passes
- [ ] I added tests for the new behavior (or explained why not)

## New-pillar checklist (only if applicable)

- [ ] Non-overlapping with existing pillars (`strategy`, `branding`, `website`, `acquisition`, `retention`, `agentic-ai`)
- [ ] Includes at least 2 concrete service lines
- [ ] Each service line ships a `SKILL.md` with progressive-disclosure references
- [ ] At least one example SOP per service line, in all three archetypes (Lean / Coordinated / Compliance-Forward)
- [ ] No hardcoded vendor names — references generic categories instead
- [ ] No organization-specific branding anywhere except in `examples/<org>-public/`
- [ ] Example SOPs cover RACI vocabulary clearly
- [ ] Tests added for new skill loader paths

## New service-line checklist (only if applicable)

- [ ] Service-line name in kebab-case
- [ ] Lives under the correct pillar's `skills/` folder
- [ ] At least one example SOP shipped in `examples/*/`
- [ ] Doesn't duplicate an existing service line under another pillar

## Breaking changes

<!-- If this is a breaking change, describe the impact and migration path. -->

## Additional notes

<!-- Anything else reviewers should know. Screenshots, design decisions, links, etc. -->
