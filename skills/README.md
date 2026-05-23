# Skills

Progressive-disclosure knowledge packs, one per pillar and service line. Each skill loads only when the Conductor decides it's relevant — keeping the agent's working context lean.

## Structure

```
skills/
├── strategy/
│   ├── SKILL.md
│   ├── marketing-strategy/
│   │   ├── SKILL.md
│   │   └── playbook.md
│   └── marketing-analytics/
│       └── ...
├── branding/
├── website/
├── acquisition/
│   ├── SKILL.md
│   ├── seo/                ← Phase 1 proof slice
│   ├── paid-media/
│   ├── social-media-management/
│   ├── content-marketing/
│   └── cold-email/
├── retention/
└── agentic-ai/
```

Each `SKILL.md` includes frontmatter (`name`, `description`) so Claude can decide whether to load it. Reference files in subdirectories are loaded only when the active skill needs them.

See [strands-agents/agent-sop's SKILL.md](https://github.com/strands-agents/agent-sop/blob/main/skills/agent-sop-author/SKILL.md) for the format we mirror.
