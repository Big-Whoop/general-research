# Research: Hermes Profile Architecture — Best-Practice Profile Split for Our Fleet

Date: 2026-10-28 · Language: EN (AI-facing corpus; REPORT.md will be DE)
Question: We mainly use the Hermes **default** profile for everything. Which profiles
would be sensible for us per best practices, and with which tools and skills should
they be equipped? Official docs are a first-class source.

## Premise
- Subject **"Hermes profile"** — VERIFIED 2026-10-28: official docs exist
  (`/docs/user-guide/profiles`, `/docs/reference/profile-commands`), local install
  has 7 profile dirs under `/opt/data/profiles/` + `/opt/data` itself.
- User premise "default-for-everything is not good practice" is treated as a
  **hypothesis to verify/nuance against official docs**, not an assumed fact.

## Dichotomy (the axis that produces confusion)
"Run a separate specialist" can mean four different mechanisms with very different
costs: **profile** (fully isolated HERMES_HOME: own config/.env/sessions/skills/
memory/cron/plugins) vs **Bot Mode** (named Bots layered on profiles: own chat,
role, model, memory, skills, avatar) vs **delegate_task subagents** (ephemeral,
in-process) vs **cron jobs / kanban worker profiles** (schedule- vs board-driven).
"Specialist for X" can be any of them; the report must say which mechanism owns
which workload split, not just "make more profiles".

## Environment (verified locally by orchestrator probe, 2026-10-28 — VERBATIM in all lane briefs)
- Deployment: Hermes runs from a self-built Docker image (`custom-hermes-suite`,
  Hermes v0.22.2) as a **single Kubernetes pod**; `HERMES_HOME=/opt/data` on a
  persistent ext4 volume, UID 10000. One desktop app + one Telegram bot + api_server
  connect to this instance. Single-user home-lab team (operator: Peter).
- Profiles today (probed 2026-10-28):
  - **default** (`/opt/data`): everything interactive — desktop chat, Telegram +
    api_server platforms, gateway with `gateway.multiplex_profiles: true`, kanban
    **orchestrator** (`kanban.orchestrator_profile: default`, `default_assignee: worker`,
    `max_in_progress_per_profile: 5`), 3 cron jobs (project-reminder, release-watch,
    update-report→Telegram), 44 skills, 14 plugins, SOUL.md.
  - **worker**: kanban worker (`dispatch_in_gateway: false`, no chat tokens), 37 skills, 11 plugins.
  - **reviewer**: 24 skills, 2 plugins, own LCM plugin config.
  - **crew-coordinator / crew-worker / crew-verifier / crew-content**: four profiles of
    the "crew" plugin (2 skills each, 15 plugins each, `model_overrides`; coordinator/
    worker/verifier have slack platforms).
  - `/opt/data/profiles/default/` is an empty stub (no config) — anomaly to note.
- Past incident (fleet memory): kanban cards historically ran on **default** → parallel
  writes to `/opt/data` next to the interactive desktop session ("two writers on one
  home" hazard); since mitigated by routing cards to worker.
- Memory: native memory disabled (`memory_enabled: false`); Hindsight provider
  configured but bank work frozen pending a written concept — treat per-profile memory
  design as open, not a blocker for the profile question.
- User's own words: "Wir benutzen hauptsächlich das Default-Profil für alles."
  I.e. worker/reviewer/crew-* exist but the interactive + orchestration + channel +
  cron + personal-assistant load all sits on default.
- Standing preference (fleet memory): profiles are kept at **parity** with each other
  (config drift is a known maintenance cost).

## Coverage table (sub-questions)
| # | sub-question | best tier | ≥2 sources | workarounds searched | lane verdicts | status |
|---|---|---|---|---|---|---|
| SQ1 | What a profile isolates/shares + lifecycle (create/clone/export); documented purpose | Verified (official docs, 10 pages) | yes (profiles page + FAQ + configuration + dev-guide multiplexing) | yes (empty stub, home_mode, clone guards) | answered | RESOLVED |
| SQ2 | Official best-practice statements: when to split off default; documented hazards of everything-on-default | Verified (incl. verified silence) | yes (docs + FAQ + 5 corroborating issues) | yes (absence table: tips=0 hits, no best-practices page) | answered | RESOLVED |
| SQ3 | Mechanism boundaries: profile vs Bot Mode vs delegate_task vs cron vs kanban vs MoA | Verified (12 pages whole) | yes (kanban/delegation/cron/bot-mode pages cross-corroborate) | yes (no single comparison page = absence recorded) | answered | RESOLVED |
| SQ4 | Per-profile equipping: toolsets, model, skills, MCP, plugins, SOUL, approvals; minimal per-role surface | Verified (docs + llms-full corpus) | yes (toolsets-reference, skills, cron, kanban, plugins pages) | yes (no "minimal specialist checklist" = absence recorded) | answered | RESOLVED |
| SQ5 | Community/practice: real multi-profile fleets, role splits, pitfalls | Verified (1 maintainer PR) + Plausible (user reports) | yes for patterns (≥3 independent reports per pattern); pitfalls single-issue each (flagged) | yes (registry ecosystem, CLI-delegation workaround; GitHub Discussions 410 = absence) | answered | RESOLVED |
| SQ6 | Target architecture for OUR fleet (orchestrator synthesis from SQ1–5 + local inventory) | synthesis over Verified rows | n/a | n/a | orchestrator | RESOLVED (REPORT.md) |

## Source universe checklist
- [x] Official docs (user-guide + reference + guides) — L1–L4
- [x] Developer-guide internals (multiplexing-gateway, config-backend) — L1
- [x] GitHub issues/discussions (NousResearch/hermes-agent) — L5 (Discussions disabled 410, absence recorded), L2 (issues)
- [x] Community: Reddit / HN / X / blogs — L5 (Reddit via user-stories quotes + search snippets; X via user-stories tiles; native search unavailable, recorded)
- [x] Official user-stories page (community evidence hosted by vendor) — L5
- [x] Source code — NOT needed (docs-first gate held; no lane fell back to code)
- [x] Local config probe of our own deployment — orchestrator, 2026-10-28 (+ addendum below)

## Rounds
Round 1: 5 lanes dispatched 2026-10-28 (docs×4 + community×1) — all completed with full lane files,
status lines, and "Searched, found nothing" sections.
Round 2: **not needed** — Step-2b audit found no OPEN/PARTIAL row; stop rule satisfied.

## Local addendum (orchestrator probe, post-lane, 2026-10-28)
- s6 services in the pod: gateway-default, gateway-worker, gateway-reviewer, and one gateway per
  crew-* profile (8 gateway processes total) — i.e. one-gateway-per-profile inside a single
  container, alongside `gateway.multiplex_profiles: true`. Upstream position: multiplexed host
  gateway is the supported container topology; per-profile gateways are a refused/temporary-shim
  topology (docs bestpractice L2-10) and a documented single-container pitfall (community
  lane5 F28, issue #88521). Crew profiles carry own slack platform sections; worker/reviewer
  gateways are idle (no platforms).
- crew-* configs have no `gateway.standalone` key; kanban.default_assignee=worker present in crew configs.
