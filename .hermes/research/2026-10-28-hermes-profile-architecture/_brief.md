# Deep-Research Lane Brief — Hermes Profile Architecture (shared contract)

Read this WHOLE file first, then execute ONLY your lane (named in your task goal).

## Research question (framing)
We mainly use the Hermes **default** profile for everything (interactive desktop chat,
Telegram, cron, kanban orchestration, personal assistant). Official docs + community
practice: which profiles make sense for our fleet, and what tools/skills should each
carry? A "profile split" must be evaluated against the alternative mechanisms
(Bot Mode, delegate_task subagents, cron jobs, kanban worker profiles).

## Environment context — VERIFIED facts about OUR deployment (do NOT re-search these)
- Hermes runs from a self-built Docker image (`custom-hermes-suite`, Hermes v0.22.2) as
  a SINGLE Kubernetes pod; HERMES_HOME=/opt/data on persistent ext4, UID 10000.
  One desktop app, one Telegram bot, and an api_server connect to this instance.
  Single-user home-lab team (operator: Peter).
- Profiles today (probed 2026-10-28):
  - default (/opt/data): everything interactive — desktop chat, Telegram + api_server
    platforms, gateway with gateway.multiplex_profiles true, kanban ORCHESTRATOR
    (orchestrator_profile default, default_assignee worker, max_in_progress_per_profile 5),
    3 cron jobs (incl. update-report delivered to Telegram), 44 skills, 14 plugins, SOUL.md.
  - worker: kanban worker (dispatch_in_gateway false, no chat tokens), 37 skills, 11 plugins.
  - reviewer: 24 skills, 2 plugins, own LCM plugin config.
  - crew-coordinator / crew-worker / crew-verifier / crew-content: four profiles of the
    "crew" plugin (2 skills each, 15 plugins each, model_overrides; three have slack platforms).
  - /opt/data/profiles/default/ is an empty stub with no config (anomaly).
- Past incident (fleet memory): kanban cards historically ran on default → parallel
  writes to /opt/data next to the interactive desktop session ("two writers on one home").
- Native memory disabled (memory_enabled false); Hindsight configured but frozen pending
  a written concept — per-profile memory design is open, not a blocker.
- Standing user preference: profiles are kept at parity (config drift = known cost).

## Rules for every lane
- DOCS-FIRST gate: official docs (hermes-agent.nousresearch.com/docs), the GitHub repo
  docs/ tree and issues come first. Foreign source code is a last-resort fallback only,
  never used as documentation.
- Search the FEATURE AND ITS WORKAROUNDS: documented surfaces and community hacks under
  alternative vocabulary (e.g. profile bloat, skill dilution, agent-per-role, two writers,
  state.db lock, profile parity drift, cron double-firing).
- Rate limits: make AT MOST 1-2 web_search calls per iteration, pause between; prefer
  web_extract of the starting URLs over search bursts. The model endpoint is shared —
  be frugal.
- Language: write your lane file in ENGLISH (AI-facing).
- Write EXACTLY ONE file: your lane file path given below (use write_file, complete
  findings). Do NOT touch other files, do NOT git add/commit/push anything.
- Never write secrets, never echo env vars values.

## Output contract
(a) LANE FILE — one entry per finding:
    - claim (one sentence)
    - source URL + source type (official-docs / reference / dev-guide / github-issue /
      discussion / reddit / blog / vendor-community-page)
    - supporting quote (verbatim, short)
    - confidence tier: Verified (authoritative source for this exact target) /
      Plausible (sound general behavior, not demonstrated on-target) / Speculative
    Plus a "Searched, found nothing" list (queries + source types) — evidence of absence.
    Plus the LAST line exactly:
    Sub-question status from this lane's view: answered | partial | not found
(b) FINAL ANSWER (what returns to the orchestrator): a compact numbered index, ONE line
    per key finding in the format: N. FINDING TEXT — TIER. Under ~1300 characters.
    No URLs, no intro, no methodology talk. Write it in ONE pass — do NOT count
    characters; if too long, drop lines.

## Lane assignments

### LANE L1 — file docs-profiles/lane1.md — owns SQ1
Sub-question: What does a Hermes profile officially isolate, and what is shared? What is
the documented purpose and lifecycle of profiles?
Cover: profile directory layout (config.yaml, .env, SOUL.md, sessions, state.db, skills/,
cron/, plugins/, memories/); what is shared across profiles (code install, model runtimes,
plugin python deps); lifecycle commands: hermes profile create/clone/--clone-all/
--clone-channels/export/backup/delete; HERMES_HOME resolution; per-profile vs global files
(SOUL.md vs MEMORY.md vs USER.md vs AGENTS.md); what the docs say profiles are FOR;
the empty-stub pitfall.
Starting URLs: /docs/user-guide/profiles ; /docs/reference/profile-commands ;
/docs/user-guide/which-file-does-what ; /docs/user-guide/sessions ;
/docs/user-guide/configuration ; /docs/reference/environment-variables ;
/docs/user-guide/remote-config ; /docs/user-guide/managed-scope ;
/docs/developer-guide/multiplexing-gateway ; /docs/developer-guide/config-backend
(base https://hermes-agent.nousresearch.com). Read pages WHOLE — if web_extract
truncates, read the saved file's omitted middle.

### LANE L2 — file docs-bestpractice/lane2.md — owns SQ2
Sub-question: What do OFFICIAL sources say about when to split work off the default
profile, and what hazards of "everything on default" are documented?
Cover: any explicit recommendation (or absence thereof!) to use multiple profiles; the
tips page profile-related advice; FAQ profile entries; security page (isolation,
approvals, production deployment) and "secure hermes on a work machine";
multi-profile-gateways page (when one multiplexed gateway vs several gateway processes;
routing; secret scope); profile-distributions page (sharing a whole agent); state.db /
SQLite single-writer or concurrency hazards; cron/profile interaction pitfalls
(jobs cloned = double firing); "two writers on one home" hazards; per-profile model
cost control. Quote EVERY profile-split recommendation verbatim. If official docs stay
silent on "default for everything is bad", that absence is itself a finding — record it.
Starting URLs: /docs/guides/tips ; /docs/reference/faq ; /docs/user-guide/security ;
/docs/guides/secure-hermes-on-a-work-machine ; /docs/user-guide/multi-profile-gateways ;
/docs/user-guide/profile-distributions ; /docs/reference/cli-symbols skip ;
/docs/user-guide/session-storage-recovery ; /docs/user-guide/secrets

### LANE L3 — file docs-boundaries/lane3.md — owns SQ3
Sub-question: Where are the documented BOUNDARIES between the specialist mechanisms —
profile vs Bot Mode vs delegate_task subagents vs cron jobs vs kanban worker profiles vs
Mixture of Agents — and which mechanism do the docs position for which workload?
Cover: Bot Mode (it says "turn your Hermes profiles into a roster of named Bots" — what
exactly do Bots add per-profile vs replacing a profile; per-bot model/memory/skills/
avatar; routines; group chats); kanban (explicitly "coordinating multiple Hermes
profiles" — dispatcher model, orchestrator_profile, default_assignee, worker profiles,
kanban-multi-gateway, worker lanes); delegation (delegate_task: when ephemeral children
suffice instead of profiles; delegation-patterns guide); cron (jobs live per profile —
which profile should own scheduled automations; script-only cron); MoA presets; git
worktrees guide (same repo, multiple agents); heartbeats/loops. Produce a crisp
mechanism-ownership table as findings.
Starting URLs: /docs/user-guide/bot-mode ; /docs/user-guide/features/kanban ;
/docs/user-guide/features/kanban-multi-gateway ; /docs/user-guide/features/kanban-worker-lanes ;
/docs/user-guide/features/delegation ; /docs/guides/delegation-patterns ;
/docs/user-guide/features/cron ; /docs/guides/automate-with-cron ;
/docs/guides/cron-script-only ; /docs/user-guide/features/mixture-of-agents ;
/docs/user-guide/git-worktrees ; /docs/user-guide/features/heartbeat

### LANE L4 — file docs-equipping/lane4.md — owns SQ4
Sub-question: How is a profile equipped officially — which settings are per-profile, and
is there documented guidance on a minimal per-role toolset/skill surface?
Cover: toolsets (core/composite/platform/dynamic; platform_toolsets per surface; how to
restrict which tools a profile/platform gets; toolsets-reference; tools-reference);
per-profile model/provider and model_overrides; skills (skills dir per profile? shared?;
Skills Hub install targets; curator per profile; skills guidance on bloat — does the docs
warn about too many skills in the listing); MCP servers per profile (mcp_servers in
config.yaml + filtering semantics); plugins per profile (install --profile, catalog);
SOUL.md / personality per profile; approvals & security per profile; what cloning copies
for equipping new profiles; dashboard/profile builder. Note any docs statement about
minimum viable specialist config (e.g. worker profiles need no chat platforms).
Starting URLs: /docs/user-guide/features/tools ; /docs/reference/toolsets-reference ;
/docs/reference/tools-reference ; /docs/user-guide/features/skills ;
/docs/reference/skills-catalog ; /docs/reference/optional-skills-catalog ;
/docs/guides/work-with-skills ; /docs/user-guide/features/curator ;
/docs/user-guide/features/plugins ; /docs/user-guide/features/plugin-catalog ;
/docs/reference/mcp-config-reference ; /docs/guides/use-mcp-with-hermes ;
/docs/user-guide/features/personality ; /docs/guides/use-soul-with-hermes ;
/docs/user-guide/features/web-dashboard

### LANE L5 — file community/lane5.md — owns SQ5
Sub-question: What do REAL users do with multiple Hermes profiles — role splits, tool/skill
equipping choices, and pitfalls?
Cover: GitHub issues + discussions of NousResearch/hermes-agent mentioning profiles
(search terms: profile per project, multiple profiles, profile vs bot, skill dilution,
profile bloat, multiplex routing, cron cloned, state.db lock, two gateways); the
official user-stories page (community evidence: what setups people run); Reddit
(hermes agent profiles, NousResearch), Hacker News, X, blog posts about multi-agent or
multi-profile Hermes setups. Workaround vocabulary: agent-per-role, separate agent per
persona, profile bloat, skill listing dilution, parity drift, profile routes.
Distinguish maintainer statements (Verified-ish) from user reports (Plausible).
Starting points: github.com/NousResearch/hermes-agent issues + discussions search;
https://hermes-agent.nousresearch.com/docs/user-stories ; reddit search.
If X/Twitter or Reddit search is unavailable, record it under "Searched, found nothing".
