# general-research

General research workspace.

## Status

Pre-spec — the project spec is defined in a separate session. This repo is the
scaffold: research archive under `.hermes/research/` plus the kanban board for
work tracking.

## Layout

- `.hermes/research/` — research archive (see `.hermes/README.md`)
- Kanban board: `general-research` (2-lane: default/reviewer)

## Workflow

card → worktree → branch → PR → reviewer merge

## License

MIT — see [LICENSE](LICENSE).

## skills/

Shareable Hermes skills maintained in this repo (source of truth for versioning; the live copies live under `/opt/data/skills`). Each `SKILL.md` carries its own `version:` — bump it on every change and sync both directions deliberately.

| Skill | Purpose |
|---|---|
| `deep-research` | Multi-round subagent research into an options report |
| `decision-narrowing` | Narrow a research corpus to one path (user-driven loop) |
| `feature-spec-qa` | Settle a feature design one question per turn, no corpus |
| `decision-topic-execution` | Build/board work under a closed decision topic |
| `hermes-kanban-workers` | Kanban campaigns: waves, feature branches, review lane |
| `before-reading-source` | Docs-first gate before opening foreign source code |
| `subagent-fanout` | Fan out N items via delegate_task with capped output |
| `merge-reconciler` | Neutral resolution of agent merge conflicts |
| `plan` | Write a markdown plan, no execution (adapted from obra/superpowers, MIT) |
| `reddit-reading` | Read Reddit without a browser (from Hermes optional-skills by Teknium, MIT; local changes in `scripts/reddit.py`) |
