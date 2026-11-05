# Lane 5 — How should Hindsight memory banks be cut per coordination model?

Date: 2026-11-06. Scope: Hindsight bank semantics (upstream docs), the Hermes hindsight plugin as installed at `/opt/data/plugins/hindsight` (read-only), Hermes core memory-provider contract (v0.22.7, `/opt/hermes`), general multi-agent memory practice, and a derived bank layout for the four coordination models.

Tier legend: **Verified** = authoritative source for this exact subject+version (upstream docs, plugin source as installed, Hermes core as installed). **Plausible** = sound general behaviour, not demonstrated on-target. **Speculative** = derived recommendation.

Local facts respected as given (not re-researched): profile banks `hermes-default` / `hermes-worker` / `hermes-reviewer` + project bank `nixos-infra`; `bank_id_template: "{project}"` falls back to the profile bank in gateway-spawned sessions (core cwd bug); worker/reviewer `auto_retain: false`; crew roles memory-free (lessons in `crew/lessons.md`).

---

## Part A — Hindsight bank semantics (upstream)

### A1. A bank is a hard isolation + recall boundary; there is no cross-bank query server-side.
- Source: https://hindsight.vectorize.io/blog/2026/07/16/bank-strategy-agent-memory (vendor blog, Hindsight team) — **Verified**
- Quote: "A **bank is a recall boundary**. `recall`, `retain`, and `reflect` all operate inside one bank, and there is no cross-bank query. So 'should these two things share a bank?' really means 'should a memory stored by A be recallable by B?'"
- Also: https://hindsight.vectorize.io/developer/api/memory-banks (official docs) — "Banks are completely isolated from each other — memories stored in one bank are not visible to another."
- Consequence for us: any "cross-bank recall" is a *client-side* fan-out (the Hermes plugin does this, see B3); the server never merges banks.

### A2. Banks are auto-created on first write; an unstable or mistyped bank id silently yields an empty memory.
- Source: same blog — **Verified**
- Quote: "a `bank_id` you have never written to is simply an empty bank, and a typo or an unstable id silently gives you a fresh, blank memory instead of an error. Bank identity is load-bearing."
- Docs add: "Only _writes_ create a bank … **Reads of a bank that does not exist return `404`**" (https://hindsight.vectorize.io/developer/api/memory-banks). The plugin handles that 404 (`_bank_not_written_yet`, `__init__.py:373`).
- Relevance: the local `{project}`→profile-bank fallback is exactly the "unstable id" failure mode: the same worker writes to `nixos-infra` from a CLI session and to `hermes-worker` from a gateway session.

### A3. Vendor guidance for multi-agent: per-agent banks when roles should keep separate experience; one shared bank when they must collaborate; tags for soft partitions, banks for hard ones.
- Source: same blog, strategy table + checklist — **Verified**
- Quote: "**A crew of specialized agents** (a planner, a researcher, a reviewer) that should each keep their own experience: **per-agent**. But the moment you want them to collaborate on shared context, point them at one **shared** bank instead."
- Quote: "**Hard isolation** (a tenant, a customer, an untrusted source, anything where a leak is a bug): **separate bank**. … **Soft partition** (… projects, topics, or users you sometimes want to filter and sometimes want to see together): **one bank, tags**."
- Quote (anti-pattern): "**Over-fragmentation.** … A bank per (user × project × agent × session) feels tidy and starves recall … When in doubt, prefer fewer banks and lean on tags."

### A4. Tags are not a security control: default `tags_match=any` includes untagged memories.
- Source: same blog + https://hindsight.vectorize.io/best-practices — **Verified**
- Quote (blog): "Because `any` includes untagged memories, tags are a _soft_ partition: convenient for organizing, not a security control. If a memory absolutely must never surface in the wrong context, do not rely on a tag filter someone can forget to pass. Put it in its own bank."
- Quote (best-practices anti-patterns): "`tags_match=\"any\"` for multi-tenant banks | Leaks memories across users | Use `any_strict` or `all_strict`".
- Note: the Hermes plugin's `recall_tags_match` defaults to `any` (README "Recall" table), so role-tagging inside one shared bank would leak by default unless `*_strict` is configured.

### A5. Per-bank config can shape what gets stored (retain_mission, observations_mission, directives) and what tools are allowed (`mcp_enabled_tools`), and Memory Defense can redact/block secrets per bank.
- Source: https://hindsight.vectorize.io/developer/api/memory-banks, https://hindsight.vectorize.io/developer/memory-defense — **Verified**
- Quote: "`mcp_enabled_tools` … An allowlist of MCP tool names that are enabled for this bank. When set, only the listed tools can be invoked" (e.g. `["recall","reflect"]` → read-only bank for MCP clients).
- Quote: "Memory Defense is opt-in per bank … `block` — drop any item that contains a match." Caveat: `mcp_enabled_tools` governs the MCP surface only; the Hermes plugin uses the REST client, so a read-only bank for Hermes profiles must be enforced client-side via `recall_additional_banks` (B3).

### A6. Observations are the consolidated layer; `shared` scope merges across sessions, which is what makes a shared project bank useful but also what lets one worker's bad fact be consolidated into a belief others recall.
- Source: plugin README (installed) lines 267-273 + 296; https://hindsight.vectorize.io/best-practices "Observation Scopes" — **Verified**
- Quote (README): "`observation_scopes` | `shared` | … `shared` (one scope for the whole bank, so observations merge across sessions; the `session:`/`parent:` tags stay on the facts for filtering)".
- Quote (best-practices): "**Observations** — Deduplicated, evidence-grounded knowledge consolidated from multiple facts. … Refined — not overwritten — when new evidence supports, contradicts, or extends them."

### A7. "Shared bank, many clients" is a vendor-endorsed pattern (static bankId across tools).
- Source: https://hindsight.vectorize.io/blog/2026/04/07/one-memory-for-every-ai-tool — **Verified** (vendor blog)
- Quote: "The multi-client, single-bank pattern is where Hindsight has a real edge."

---

## Part B — Hermes hindsight plugin semantics (installed copy, `/opt/data/plugins/hindsight`)

### B1. Primary bank precedence: trusted-repo `.hindsight/config.toml` → `bank_id_template` → `HINDSIGHT_BANK_ID`/`bank_id`.
- Source: README.md:234; `__init__.py:1312-1333` — **Verified**
- Quote (README): "The primary bank is chosen in this order: a `.hindsight/config.toml` in a trusted repository, then `bank_id_template`, then `HINDSIGHT_BANK_ID` or `bank_id`."
- Code: `__init__.py:1329-1333` `if cwd_bank: self._bank_id, self._bank_source = cwd_bank, "repository config" else: self._bank_id = self._resolve_template_bank()`.

### B2. `{project}` = git main-repository folder name of the session cwd; empty outside a repo → template collapses → fallback to `bank_id`.
- Source: README.md:224; `settings.py:190-203, 247-254`; `__init__.py:1316-1328` — **Verified**
- Quote (README): "`{project}` is the name of the git repository Hermes runs in; every worktree of a repository resolves to the same name, and it is empty outside a repository or for one rooted at your home directory."
- Code: `_resolve_bank_id_template` → `re.sub(r"([-_])\1+", r"\1", rendered).strip("-_") or fallback` (settings.py:203); `if self._cwd and (trusted_dirs or uses_project): root = _repository_root(self._cwd)` (`__init__.py:1317-1319`) — no `cwd` kwarg ⇒ `root is None` ⇒ `_project == ""`.
- Local confirmation of the cwd bug path (core v0.22.7): `agent/agent_init.py:1200-1201` only passes `kwargs["cwd"] = agent.session_cwd` when set; `gateway/session_execution.py:161-189` constructs `ctx.AIAgent(...)` with no `cwd=`/`session_cwd` argument. Kanban workers go through the gateway owner (`hermes_cli/kanban_worker_client.py:1` "Dispatcher subprocess: submit one claim to its profile owner; never run an agent."), so worker sessions resolve `{project}` = "" → bank `hermes-worker`. Dispatcher sets `TERMINAL_CWD`/`HERMES_KANBAN_WORKSPACE` (`kanban_db_dispatch.py:2812, 2827-2828`) but these do not reach `_memory_provider_init_kwargs`. **Verified** (local file:line).

### B3. Write set and recall set are computed client-side: writes = primary → own `bank_id` (if `mirror_to_own_bank`) → `additional_banks`; recall = write set + `recall_additional_banks` (read-only); reflect = primary only.
- Source: README.md:234; `__init__.py:1215-1229, 1271-1284` — **Verified**
- Quote (README): "Writes go to the primary, then `bank_id` when `mirror_to_own_bank` is on, then each `additional_banks` entry. Recall searches the same banks and then each `recall_additional_banks` entry, all at once … results are merged in that order and deduplicated by text. Reflect uses the primary bank only."
- Code: `_build_recall_bank_ids` docstring: "Recall-only banks are read and never written, so a shared bank can be consulted without this provider's conversations landing in it."
- Consequence: `recall_additional_banks` is the only *read-only* mechanism on the Hermes side; `additional_banks` always writes.

### B4. `mirror_to_own_bank` is dedup-safe: when the template collapses to the own bank, the write set is just `[bank_id]`.
- Source: `__init__.py:1223-1225` — **Verified**
- Code: `ordered = [self._bank_id]; if self._mirror_to_own_bank and self._static_bank_id not in ordered: ordered.append(self._static_bank_id)`.
- Local effect today: worker in gateway session → write set `[hermes-worker]`, recall set `[hermes-worker]`; the project bank `nixos-infra` is neither written nor read by gateway-spawned workers. Only sessions with a real cwd inside the repo (CLI/desktop with workspace) get `[nixos-infra, hermes-<profile>]`.

### B5. `auto_retain` controls automatic transcript retain; the `hindsight_retain` tool still works when it is off; cron runs are skipped unless `retain_cron`; `delegate_task` subagents get no provider at all.
- Source: README.md:290-291; `__init__.py:1380-1384, 1798-1810`; tests `test_provider.py:741-761`; core `agent/agent_init.py:1179-1180`, `tools/delegate_tool.py:296-298`, `agent/memory_provider.py:124-127` — **Verified**
- Quote (README): "`retain_cron` | `false` | Also auto-retain scheduled (cron) runs. Off by default, so job output stays out of the user's memory; the `hindsight_retain` tool still works in cron runs."
- Code: `self._auto_retain = cfg.get("auto_retain", True) and (not is_cron or bool(cfg.get("retain_cron", False)))`; `sync_turn` returns early with "auto_retain disabled".
- Test: `test_cron_runs_are_not_auto_retained` — `cron.handle_tool_call("hindsight_retain", …)` still records one retain.
- Core: `"agent_context": platform if platform in ("cron", "subagent") else "primary"`; `delegate_tool.py:298` builds children with `skip_memory=True` → no memory provider for subagents. Note the plugin only checks `== "cron"`; the `subagent` value is moot because `skip_memory=True` prevents provider init.
- Local: worker/reviewer have `auto_retain: false` (`/opt/data/profiles/{worker,reviewer}/hindsight/config.json`) → their only write channel is the explicit `hindsight_retain` tool (memory_mode `hybrid` default exposes it).

### B6. Auto-retained items carry `session:<id>` / `parent:<id>` lineage tags; no role/profile tag is attached unless `retain_tags` is configured.
- Source: `__init__.py:1758-1762`; README.md:295-297 — **Verified**
- Code: `lineage = (("session", self._session_id), ("parent", parent)); tags = [f"{kind}:{sid}" for kind, sid in lineage if sid] or None`.
- Quote (README): "`retain_tags` | — | Default tags applied to retained memories; merged with per-call tool tags." "`retain_source` | — | Opt-in `metadata.source` … Empty by default — no attribution tag ships unless you set it."
- Consequence: in a shared bank, provenance per role requires each profile to set `retain_tags: ["role:worker"]` (filterable) and/or `retain_source` (metadata, not filterable). Without it, a poisoned fact cannot be traced to the writing role except via `session:` tag → session DB.

### B7. `trusted_project_dirs` is the anti-redirect guard: an untrusted clone cannot choose a bank via `.hindsight/config.toml`.
- Source: README.md:228, 240-246; `settings.py:257-300` — **Verified**
- Quote: "Absolute folders whose git repositories may choose their own bank with a `.hindsight/config.toml`. Empty by default, so a cloned repository cannot redirect your memory."
- Local: all three configs set `trusted_project_dirs: ["/workspace/dev/repos/ours"]`. Risk: any repo under that path (including a worker's worktree, since "a linked worktree is judged by where the worktree is") can carry a `.hindsight/config.toml` that redirects the *primary* bank of every profile that opens it with a real cwd. A card-produced commit adding that file is a bank-redirect vector (mitigated today only by the cwd bug making gateway sessions ignore cwd).

### B8. Profile isolation: one config per profile (`$HERMES_HOME/hindsight/config.json`); shared memory across profiles must go through bank configuration, not shared HERMES_HOME.
- Source: README.md:195-205; https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers "Profile Isolation"; https://hermes-agent.nousresearch.com/docs/user-guide/profiles — **Verified**
- Quote (profiles doc): "Never point two agent processes at the same profile (the same Hermes home). … agents that need shared memory should use an external memory provider instead."
- Quote (README): "A profile has exactly one config. To give one profile different banks per repository, workspace, platform or user, use `bank_id_template` or the multiple banks settings".

### B9. Everything handed to the provider is secret-scrubbed by core first, but shapeless secrets pass.
- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers — **Verified**
- Quote: "Everything Hermes hands a provider (turns, the transcript including tool output, recall queries, … delegation results and the arguments of the provider's own tools) passes through the same secret scrub … Credentials with no recognisable shape (an arbitrary password, an opaque token …) are not detected".

### B10. Recall is rank-only; off-topic queries still return up to `recall_max_tokens`; `recall_min_scores` is the opt-in floor.
- Source: README.md:275-284 — **Verified**
- Quote: "Recall ranks, it does not judge relevance: a question unrelated to anything stored still comes back with up to `recall_max_tokens` of the least-bad memories."
- Relevance: every worker turn with `auto_recall: true` pays ~4 k tokens of injected memory per turn across *all* recall banks; more banks in the recall set = more latency/tokens per card turn.

### B11. Hermes kanban docs position the worker profile's own memory (MEMORY.md / provider bank) as the durable per-role store and the card body/parent links as the per-task hand-off; tenant scoping is by prefix, not by bank.
- Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban — **Verified**
- Quote: "| Child identity | Anonymous subagent | Named profile with persistent memory |"; "Workers receive `$HERMES_TENANT` and namespace their memory writes by prefix. The board, the dispatcher, and the profile definitions are all shared; only the data is scoped."
- Quote: "A worktree or branch alone is not a substitute: repo state tells the follow-up worker _what_ the code looks like, but not _why_ — the decisions, tests run, and files touched live in the parent's structured handoff, not in git."
- Local skill confirms the same split (`/opt/data/skills/autonomous-ai-agents/hermes-kanban-workers/references/cli-recipes.md:400-408`): "The durable place is the assignee profile's `MEMORY.md` … injected into every worker run of that profile" (native memory is disabled locally, so the Hindsight profile bank is the equivalent).

### B12. Bot Mode: a Bot is a profile; memory stays per-profile; each group-chat member keeps its own room session; routines are cron.
- Source: https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode — **Verified**
- Quote: "a Bot **is** a Hermes profile — isolated config, memory, skills, credentials, and chat history under `~/.hermes/profiles/<name>/`." "Each member keeps its own persistent room session". "Routines are plain Hermes cron jobs".
- Consequence: in a bot army every bot auto-retains its own room session into its own bank (`auto_retain` default true); a routine run does not auto-retain unless `retain_cron`.

---

## Part C — General multi-agent memory practice

### C1. Orchestrator–worker systems should externalise plan/phase summaries and pass lightweight references; subagents start context-free and return to the lead.
- Source: https://www.anthropic.com/research/multi-agent-research-system (vendor engineering blog) — **Plausible** (general practice, not Hermes-specific)
- Quote: "We implemented patterns where agents summarize completed work phases and store essential information in external memory before proceeding to new tasks." "Subagents call tools to store their work in external systems, then pass lightweight references back to the coordinator."
- Hermes equivalent: delegate_task children "start with a **completely fresh conversation**" and have no memory provider (B5) — their results flow back only through the parent, which is the sole memory writer. (https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation — Verified for the Hermes part.)

### C2. OpenAI guidance: share memory across cooperating agents by a stable key (conversation/session), not by free-form merge.
- Source: https://developers.openai.com/tracks/building-agents — **Plausible**
- Quote: "Use **agent‑as‑tool** (expose one agent as a callable tool for another) and share memory keyed by `conversation_id`."

### C3. Curated `lessons.md`-style memory: agent writes lessons after mistakes, human curates periodically; it is read at session start and must be pruned or it becomes "a second memory leak".
- Source: https://docs.bswen.com/blog/2026-03-27-what-is-lessons-md-in-claude-code/ (practitioner blog) — **Plausible**
- Quote: "`CLAUDE.md`: You write instructions before Claude works … `lessons.md`: Claude writes lessons after making mistakes". "After a month, my lessons.md was 47KB. … I've been manually reviewing it weekly".
- Local: `crew/lessons.md` is exactly this pattern for the memory-free crew roles (user decision). Hindsight's own README argues the opposite for raw facts ("Pass rich, full-context content … do not pre-summarize"), so the two mechanisms are complementary: a bank for raw experience, a curated file for rules.

### C4. Memory poisoning: shared/externally-hosted memory amplifies blast radius; write channels include auto-retain (compaction/experience writes), not just explicit writes; OWASP lists it as ASI06.
- Sources: https://arxiv.org/abs/2603.20357 (Torra et al., "Memory poisoning and secure multi-agent systems") — **Plausible**; https://www.emergentmind.com/topics/persistent-memory-poisoning (secondary survey of MPBench/ULSP) — **Plausible**; https://hermes-agent.nousresearch.com/docs/plugins/memory-shield (Hermes plugin README) — **Verified** for the Hermes-native-memory part.
- Quote (Torra abstract): "We also emphasize actual risks in relation to interactions between agents, which can cause memory poisoning. These latter risks are not so much studied in the literature and are difficult to formalize and solve."
- Quote (survey): "A systematic taxonomy identifies four memory write channels—explicit instruction-executed write, system prompt-driven write, compaction-driven write, and experience-to-procedure write". "shared indices, common retrieval services, and cross-session stores amplify the blast radius of a single successful write."
- Quote (memory-shield): "In a group, anyone who can address the agent can try to plant or change facts about its owner. OWASP lists this as ASI06, Memory and Context Poisoning." Note: memory-shield guards the *built-in* `memory` tool only (disabled locally); there is no equivalent gate on `hindsight_retain`.
- Mapping to Hindsight: auto_retain = "experience write" channel (every turn, including tool output that may contain web/repo-injected text); `hindsight_retain` = "explicit write" channel; observation consolidation = a compaction-like channel that can promote a single injected fact into a bank-wide belief (A6).

---

## Part D — Derived bank layout per coordination model

Common notation. Banks: `D`=`hermes-default`, `W`=`hermes-worker`, `R`=`hermes-reviewer`, `P`=`nixos-infra` (project), `L`=`crew/lessons.md` (file, not a bank), `B<n>`=`hermes-<bot>` per bot profile. "today" = what the installed configs actually do given the cwd bug (B2/B4); "target" = the recommended cut. All "target" rows are **Speculative** (derived from A1–A4, B3–B7, C1–C4); the "today" rows are **Verified** from local config + code.

### Model 1 — Coordinator in the human chat (default profile) + kanban workers (worker/reviewer)

| Role | Session kind | Write set today | Recall set today | Write set target | Recall set target |
|---|---|---|---|---|---|
| Coordinator (default, chat; desktop/Telegram) | gateway → `{project}`="" | `[D]` (auto_retain on) | `[D]` | `[P, D]` once cwd fix lands, else `[D]` + `additional_banks: [P]` for the duration of a feature | `[P, D]` |
| Worker | gateway-owned kanban session, `auto_retain:false` | `[W]` via tool only | `[W]` | `[W]` (tool only) | `[W]` + `recall_additional_banks: [P]` |
| Reviewer | same | `[R]` via tool only | `[R]` | `[R]` (tool only) | `[R]` + `recall_additional_banks: [P]` |
| delegate_task children of the coordinator | subagent | none (`skip_memory=True`) | none | none | none |

- Who writes `P`: only the coordinator (human-supervised chat) — explicit "lessons" via `hindsight_retain` and its auto-retained chat turns. Workers/reviewer read `P` read-only (B3). This is the "curated lessons by the supervised role, raw experience per role" split from C3/C1.
- Why not `additional_banks: [P]` on workers: that makes every `hindsight_retain` from a card run land in the shared bank with no role tag (B6) and get consolidated into shared observations (A6) — the blast-radius case of C4. If worker writes to `P` are ever wanted, require `retain_tags: ["role:worker"]` + `retain_source: hermes-worker` on the worker profile and a `retain_mission` on `P` that ignores task chatter.
- Risks: (i) today's `{project}` collapse means `P` is **not read** by any gateway session at all — the project bank is effectively dead for this model until the core cwd bug is fixed or `recall_additional_banks` lists it explicitly (B2/B4, Verified). (ii) Coordinator auto-retain stores card bodies and worker comments it reads — repo/web text echoed into the chat becomes memory (C4 experience-write channel); `recall_min_scores` (B10) limits re-injection noise but not poisoning. (iii) `trusted_project_dirs` covers all worktrees under `/workspace/dev/repos/ours`, so a card commit adding `.hindsight/config.toml` could redirect the coordinator's primary bank when it opens that worktree with a real cwd (B7). (iv) Token cost: each extra recall bank adds up to `recall_max_tokens` per turn on every worker turn (B10).

### Model 2 — Board-resident coordinator profile (Crew coordinator) + workers + verifier

| Role | Session kind | Write set today | Recall set today | Write set target | Recall set target |
|---|---|---|---|---|---|
| crew-coordinator | dispatch-tick session (gateway-owned), memory-free by user decision | none (no provider) | none | none; durable rules → `L` (`crew/lessons.md`), state → board rows | reads `L` via repo context files |
| crew-worker / crew-content | same | none | none | none | `L` via context files; optionally `recall_additional_banks: [P]` if a Hindsight config is ever added to these profiles |
| crew-verifier | same | none | none | none (verdicts are proof-command output on the card) | same as worker |
| Human (default profile, `/crew` entry) | chat | `[D]` | `[D]` | `[P, D]` (owner curates `P` after a crew run from the card trail) | `[P, D]` |

- Rationale: with no human in the loop per tick, a board-resident coordinator is the role most exposed to the C4 interaction channel (it reads every worker's output every tick). Keeping it memory-free and putting rules in a human-curated file (`L`) matches C3 and Hindsight's own advice to isolate untrusted contexts by bank rather than tag (A3/A4). Lessons written by the human after reviewing the board are the only path into `P`.
- Risks: (i) `L` is a repo file: a worker card can edit it (code-change-via-cards rule does not stop doc edits — skill rule "Docs, skills, wiki, and memory are not code and may still be edited directly"), so `L` is itself a write channel; protect via CODEOWNERS/review or keep it outside worker worktrees. (ii) No cross-run learning for the coordinator except via `L` — if `L` grows unpruned it becomes the "second memory leak" of C3. (iii) If someone later enables Hindsight on crew-* with the shared config template, they inherit `mirror_to_own_bank: true` + `trusted_project_dirs` → same cwd/redirect caveats as Model 1.

### Model 3 — Bot army (N bot profiles in Bot Chats / group chats)

| Role | Session kind | Write set (default plugin behaviour) | Recall set | Target |
|---|---|---|---|---|
| Each bot `b_i` (its own profile) | canonical Bot Chat + per-room session (gateway, no cwd) | `[B_i]` auto_retain every turn incl. what other bots say in the room | `[B_i]` | keep `[B_i]` private writes; add `recall_additional_banks: [P]` for project facts; one optional `team` bank written **only** by the human-facing lead bot |
| Routines (cron) of `b_i` | cron | none unless `retain_cron` | `[B_i]` | leave `retain_cron: false` |
| Lead/concierge bot (talks to the human) | Bot Chat | `[B_lead]` | `[B_lead]` | `additional_banks: [P]` (the one curated writer) |

- Rationale: in a group chat every member re-reads the others' messages (B12: "an added Bot reads the recent room history on its first turn"), so with a *shared* writable bank each bot's auto-retain would store N copies of the same exchange and consolidate them into observations with N× "proof counts" (A6) — an echo-chamber that both wastes tokens and manufactures false confidence. Per-bot private banks + one read-only shared bank is the vendor's "per-agent, shared only on explicit opt-in" rule (A3) and the "tenancy/untrusted boundary = bank" rule (A4) applied to bots that may receive untrusted chat input.
- Risks: (i) Highest cross-role leak surface of all models: anything said in a room is auto-retained by every member into its own bank and recalled in that bot's *other* chats (B12 + auto_retain default true) — a fact planted in one group reaches every private chat of every member. (ii) No role attribution in stored facts unless each bot sets `retain_tags`/`retain_source` (B6). (iii) `memory-shield`-style gating exists only for the built-in memory tool, not for `hindsight_retain` (C4), so a bot can be talked into retaining arbitrary text. (iv) Token cost scales N× per room turn (auto-recall per member, B10).

### Model 4 — Plan-first single session (default profile), then hand-off to workers

| Phase | Role | Session kind | Write set | Recall set | Target |
|---|---|---|---|---|---|
| Plan | default (chat, cwd = repo if desktop workspace set; otherwise gateway no-cwd) | `[P, D]` with real cwd, else `[D]` | same | `[P, D]`; write the plan to the repo plan file (state), retain only *decisions* to `P` via `hindsight_retain` |
| Hand-off | plan file + contract cards | n/a (board rows / repo file carry state) | n/a | keep the hand-off out of memory: the plan file is the authoritative hand-off (C1 "store work in external systems, pass references") |
| Execute | worker/reviewer | as Model 1 | as Model 1 | `recall_additional_banks: [P]` so workers see the plan-phase decisions |
| Close | default | `[P, D]` | `[P, D]` | human/lead retains the post-mortem lessons to `P`; prune `L` if used |

- Rationale: this model has the cleanest write discipline — exactly one memory writer (the planning session) and a file-based hand-off, which is what both Anthropic (C1) and the Hindsight blog's "stable identity, few banks" guidance (A3) point at. The project bank holds *decisions and rationale* (what the kanban doc says git cannot carry, B11), the plan file holds *state*.
- Risks: (i) Same `{project}` collapse: if the planning session runs in a gateway context without a workspace cwd, decisions land in `D` not `P`, and workers (even with `recall_additional_banks: [P]`) never see them — verify the bank in the `👁️ Hindsight` indicator / debug log line "Hindsight bank %s from %s" (`__init__.py:1186`). (ii) Auto-retain during the long planning chat stores every draft and rejected option; consolidation may keep superseded decisions as observations unless the closing retain explicitly states the final decision (A6 "refined, not overwritten"). (iii) Lowest poisoning surface: workers are read-only on `P`, subagents have no provider, cron does not retain.

### Cross-model configuration recipe (Speculative, derived)
1. Fix or work around `{project}`: until core passes `cwd` for gateway sessions, set on every headless profile `recall_additional_banks: ["nixos-infra"]` so the project bank is at least read; do **not** put it in `additional_banks` for workers.
2. On the sole writer of `P` (default profile / lead bot) keep `bank_id_template: "{project}"` + `mirror_to_own_bank: true`; add `retain_tags: ["role:default"]` and `retain_source: "hermes-default"` so provenance is filterable (B6).
3. On `P` set a `retain_mission` ("extract decisions, conventions, blockers, failed approaches; ignore card chatter, pings, status lines") and enable Memory Defense `redact` (A5) as a second net behind the core scrub (B9).
4. Narrow `trusted_project_dirs` to the canonical checkout, excluding `.worktrees/` and card worktrees (B7).
5. Keep crew roles and delegate_task children memory-free; keep `retain_cron: false` for routines (B5/B12).
6. Treat `crew/lessons.md` as the curated "rules" layer and `P` as the "raw experience" layer; schedule a human prune of `L` (C3).

---

## Searched, found nothing
- `site:hindsight.vectorize.io "team memory"` / explicit "shared vs private banks for multi-agent" page — nothing beyond the 2026-07-16 bank-strategy blog and best-practices "One bank per agent is common" (web_search, vendor docs).
- `hindsight.vectorize.io/developer/memory-banks`, `/developer/concepts` — 404 (URLs moved to `/developer/api/memory-banks`).
- Hermes docs page specifically about Hindsight + kanban workers or + subagents (`site:hermes-agent.nousresearch.com hindsight subagent/kanban`) — none; the only relevant text is the generic provider contract (`agent_context`, "skip automatic writes for the non-primary values") in the developer guide and the kanban doc's `$HERMES_TENANT` prefix note.
- A Hermes-side read-only gate for `hindsight_retain` (equivalent of memory-shield for provider tools) — none found (web_search, plugin catalog).
- Hermes docs describing the gateway `cwd=` omission as a known bug/issue — not searched upstream per brief (local fact taken as given); local code read confirms the omission at `gateway/session_execution.py:161-189`.
- OpenAI first-party guidance on memory for *subagents* beyond "share memory keyed by conversation_id" — nothing more specific (web_search, developers.openai.com).
- A local `crew/lessons.md` file on this host — not present under `/opt/data` or `/workspace` (find); crew-* profile directories are not under `/opt/data/profiles` on this pod (only gateway logs exist), so crew Hindsight config could not be inspected and is assumed absent per the brief.

Sub-question status from this lane's view: answered
