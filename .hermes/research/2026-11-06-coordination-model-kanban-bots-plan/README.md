# Research: Coordination model for agent work — Kanban coordinator vs Bots/profiles vs plan-first chat

Date: 2026-11-06 · Language: EN (AI-facing corpus; REPORT.md will be DE)
Question: Our chat (main) session "thinks too much" before handing a feature to the
Kanban board — the orchestration role sits in the chat. Should the coordinator live on
the board instead? Are Bots (direct chat communication) a superior alternative — faster,
fewer tokens? How must Hindsight memory banks be cut for each alternative? Or is
plan-first-in-one-session, then hand off to board / bot army, the superior pattern?
Which roles are decisive?

## Premise
- Subject **Hermes Kanban** — VERIFIED 2026-11-06: `/docs/user-guide/features/kanban`,
  `/docs/user-guide/features/kanban-tutorial`; local install v0.22.7 has 11 boards,
  `kanban.orchestrator_profile: default`, `auto_decompose: false`.
- Subject **Hermes Bot Mode** — VERIFIED (research 2026-10-28, local corpus
  `2026-10-28-hermes-profile-architecture`): "a Bot is a Hermes profile"; roster +
  canonical Bot Chat + routines (cron) + group chats as desktop UI layer.
- Subject **Hindsight memory plugin** — VERIFIED: `/opt/data/plugins/hindsight`, config
  `bank_id_template: "{project}"`, `mirror_to_own_bank: true`, per-profile `bank_id`.
- Subject **Crew plugin** (Coordinator/Worker/Verifier/Content roles on the board) —
  VERIFIED: four `crew-*` profiles exist, Crew 0.10.1.

## Dichotomy (the axis that produces confusion)
"Where does the coordinator live" conflates FOUR separable questions:
1. **Where is the plan made** (chat with the human; a coordinator card; a bot chat)?
2. **Where is the state kept** (board rows; chat transcript; plan file in repo)?
3. **Who talks to the human and how** (chat turn-taking; board `blocked/needs_input`;
   bot group chat; Telegram)?
4. **Who executes** (dispatcher-spawned profile processes; delegate_task subagents;
   bot routines/cron; the chat session itself)?
"Faster / fewer tokens" must be measured per axis: tokens burned by the plan,
by the hand-off contract, by supervision/polling, by re-reads of skill text.
Also: **Bot ≠ new execution primitive** — a Bot is a profile; direct chat with a Bot
is a session; Bot routines are cron. So "bot army" = N profiles talking via chat/
group chat, with no shared queue unless kanban is used.

## Environment (verified locally 2026-11-06 — VERBATIM in all lane briefs)
- Hermes Agent v0.22.7 (docker install, single k8s pod, HERMES_HOME=/opt/data,
  UID 10000). Desktop app + Telegram + api_server attach to one multiplexed gateway.
- Profiles: `default` (interactive, orchestrator), `worker`, `reviewer` (headless
  kanban roles, `auto_retain: false`), `crew-coordinator/-worker/-verifier/-content`
  (Crew plugin). Model everywhere: claude-opus-5-5 via custom provider.
- Kanban config (default): `orchestrator_profile: default`, `default_assignee: worker`,
  `max_in_progress_per_profile: 5`, `auto_decompose: false`, dispatch 5 s. Boards: 11;
  `nixos-infra` has 95 done + 215 archived cards.
- Local orchestrator skill `hermes-kanban-workers` is ~100 KB: ~20 KB pre-card planning
  rules (plan file, dependency graph, wave table, contract cards, one question per turn),
  ~20 KB in-chat orchestration loop (board-watch.py, `--hold`, triage order per wake),
  ~22 KB pitfalls (auto-decomposer on `triage`, needs_input flapping,
  block_loop_detected, active_pr guard). The pre-card rules all run in the main chat.
- Standing user decisions: code changes ONLY via cards; card PRs → `feat/<feature>`,
  one feature PR → main merged by user; no cron polling in kanban workflows; no chat
  watcher inside a wave, blocked cards are the inbox; Kanban temporarily suspended
  2026-10-28 because it was too slow for agent communication (work stuck, chat lost
  connection, ~10 "Ping"s/day); plan-file first, questions one per turn.
- Memory: Hindsight external service (`hindsight-api.memory.svc`), banks
  `hermes-default`, `hermes-worker`, `hermes-reviewer`, `nixos-infra` (project);
  `bank_id_template: {project}` falls back to profile bank in gateway sessions (core
  bug: `gateway/session_execution.py` builds AIAgent without `cwd=`). Crew roles are
  memory-free by user decision (lessons via `crew/lessons.md` only). Native Hermes
  memory disabled everywhere.
- Crew: coordinator runs one pass per dispatch tick; two retries then a question to the
  owner; proof-command verdicts; `/crew` is the only entry point. Research 2026-10-28:
  Crew replaces orchestration/completion layer, not the kanban kernel.

## Coverage table (sub-questions → lanes)

| # | sub-question | lane(s) |
|---|---|---|
| 1 | What do official docs say about WHERE the kanban orchestrator/coordinator should live (chat session vs `orchestrator_profile` vs card), and what Auto/Manual orchestration + `kanban specify`/decompose actually do? | L1 docs-kanban |
| 2 | Bot Mode + delegation + spawn_session as an alternative coordination model: what do docs say about bots talking to each other, group chats, routines, token/latency costs, and limits? | L2 docs-bots-delegation |
| 3 | Community/GitHub: how do Hermes users actually run multi-agent work — kanban vs bots vs subagents; reported pains (slow board, polling, needs_input loops, token burn); any token/latency numbers? | L3 community |
| 4 | Industry patterns (Claude Code/Codex/OpenHands/CrewAI/LangGraph/AutoGen, Anthropic/OpenAI guidance): plan-first vs orchestrator-on-queue vs chat-swarm; which roles are decisive; token-economy evidence | L4 industry-patterns |
| 5 | Hindsight bank cut per alternative: docs on bank templates, per-profile/per-project banks, recall sets, retain policy; what each coordination model needs | L5 memory-banks |

## Round 1 dispatch
5 lanes, 3+2 delegate_task calls. Lane files: `<axis-dir>/lane<N>.md`. All five returned `answered`.

## Orchestrator probe (local, read-only, 2026-11-06)
- `nixos-infra` board (`kanban.db`): 302 cards with runs, 812 runs; runs/card median 2, mean 2.69, max 19; 55 cards with ≥4 runs. Run duration median 4.3 min, mean 10.9, p90 23.8. Events: `block_loop_detected` 75, `blocked` 114, `unblocked` 100, `respawn_guarded` 200, `crashed` 42, `reclaimed` 30, `gave_up` 14. Card created→completed median 0.6 h, mean 3.2 h (n=268).
- Token usage (`session_model_usage`): worker 23 sessions, median 11 API calls, median ~392 k input tokens incl. cache per session; reviewer 486 sessions, median 11 calls, ~595 k; default 2 784 sessions, median 11 calls, mean 2.46 M input per session (orchestrator chat sessions are the heaviest by far; 6.85 G input total).
- Profiles on this pod today: default, worker, reviewer only — the four `crew-*` profiles named in the environment block are NOT present under `/opt/data/profiles` (lane 5 confirmed; corpus environment block was stale on that point).

## Round 1 assessment

| sub-question | best tier reached | independent sources for load-bearing claim | workaround space searched | lane verdicts | status |
|---|---|---|---|---|---|
| 1 docs: where the coordinator lives | Verified (docs + local source) | ≥2 (docs pages + prompt_builder.py + kanban_db.py) | yes (Manual mode, director profile, swarm helper) | answered | CLOSED |
| 2 docs: bots / delegation / spawn_session | Verified | ≥2 (bot-mode, delegation, kanban, api-server pages) | yes (message_agent, hermes peer, spawn-session plugin) | answered | CLOSED |
| 3 community: practice + pains | Verified for upstream issues; Plausible for practice | ≥2 (GitHub issues + 6 Reddit threads + Crew README) | yes (external trackers, pinned workflow skill, smaller cards) | answered | CLOSED |
| 4 industry patterns + roles | Verified | ≥2 (Anthropic, OpenAI, Magentic-One, MAST, Kim et al.) | yes (spec-kit, CrewAI, LangGraph, AutoGen) | answered | CLOSED |
| 5 Hindsight bank cut | Verified (semantics); Speculative (derived layouts) | ≥2 (vendor blog + docs + plugin source) | yes (recall_additional_banks, retain_tags, memory-defense) | answered | CLOSED — layouts are derivations by construction, not researchable facts |
| (cross-cutting) token/latency numbers kanban vs bots vs subagents | Plausible (one upstream measurement #90853; Kim et al. topology overheads) | 1 on-target | yes | partial | OPEN → accepted as Known gap: no public measurement of an async board vs chat exists; local probe above substitutes on-install numbers |

No round 2: the only OPEN row has no plausible source location (lane 3 + lane 4 both report "not found anywhere"); recorded under `## Known gaps` in REPORT.md.
