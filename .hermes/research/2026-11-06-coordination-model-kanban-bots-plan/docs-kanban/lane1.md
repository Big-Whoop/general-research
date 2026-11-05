# Lane 1 — Official docs: where the kanban orchestrator/coordinator lives and how it behaves

Date: 2026-11-06. Docs version: live site (hermes-agent.nousresearch.com/docs, fetched today). Local ground truth: Hermes Agent v0.22.7 (`b200f5bc`, install `/opt/hermes`, files dated Nov 3 20:57).

Scope: `kanban.orchestrator_profile`, Auto vs Manual orchestration / decomposer, `hermes kanban specify`, the auto-injected orchestration guidance (`KANBAN_GUIDANCE`), `kanban_block` kinds / `needs_input` / triage / `block_loop_detected`, `max_in_progress_per_profile`, how questions reach a human, the "director decomposes and routes only" pattern, tool split (task-scoped vs orchestrator), profile docs, release notes 0.22.x.

---

## A. The documented model in one paragraph

The official docs describe **two different "orchestrators"** and the reader must keep them apart:

1. **The built-in decomposer** — a *single auxiliary-LLM call* (`auxiliary.kanban_decomposer`) run by the gateway dispatcher (Auto) or on demand (Manual: `hermes kanban decompose`, dashboard ⚗, `/kanban decompose`). It is *not* a profile, has no tools, loads no SOUL/skills, and reads only the task + profile roster descriptions. It writes a child graph, links the root under every child, and sets the root's assignee to `kanban.orchestrator_profile`.
2. **The orchestrator profile** — a normal Hermes profile that (a) becomes the *assignee of the root card* after decomposition and is therefore **spawned as a headless dispatcher worker on that root card** when all children complete ("wakes back up to judge completion"), and/or (b) is an **interactive chat session** with the `kanban` toolset enabled that calls `kanban_create` / `kanban_link` / `kanban_list` / `kanban_unblock` directly and gets woken by `notify+wake` subscriptions on terminal events.

The injected `KANBAN_GUIDANCE` block (incl. its "Orchestrator mode" section) is delivered **only to dispatcher-spawned workers that own a task** — an interactive chat session with the kanban toolset gets the tools but *not* the guidance. The "board-resident coordinator" in the docs is therefore: *a headless worker run of the orchestrator profile on a root/decomposition card, one run per wake, which must end its turn with `kanban_complete`/`kanban_block`*. Questions to humans go through `kanban_block(kind=needs_input)` + `kanban_comment`; `clarify` is explicitly forbidden in workers. Delivery to humans is via gateway subscriptions (Telegram etc.), desktop toasts, and the dashboard's Blocked/Triage columns; `block_loop_detected` routes a repeatedly re-blocked card to `triage` "for orchestration attention".

---

## B. Findings

### F1. `kanban.orchestrator_profile` = owner of the root card after fan-out; nothing else
- **Claim:** `orchestrator_profile` only decides which profile is assigned to the root/orchestration task after decomposition; it does not inject that profile's prompt, skills or logic into the decomposer.
- **Source:** official docs — https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban#auto-vs-manual-orchestration
- **Quote:** "`kanban.orchestrator_profile` does not load that profile's prompt, skills, or custom logic into the decomposition call. It controls who owns the root/orchestration task after fan-out. To change the decomposer's model/provider, configure `auxiliary.kanban_decomposer`. To use a profile's custom task-splitting logic instead of the built-in decomposer, switch to Manual mode and have that profile create or decompose tasks explicitly."
- Config table quote: "| `orchestrator_profile` | `\"\"` | Profile assigned to the root/orchestration task after decomposition. Empty = the root task keeps its own assignee, else the active default profile. |"
- **Local source confirmation:** `/opt/hermes/hermes_cli/kanban_decompose.py:133-140` — "``orchestrator_profile`` owns the root after fan-out; ``default_assignee`` catches children the decomposer can't route. The root's assignee sits before the active profile because the decomposer runs inside whatever profile hosts the dispatcher … and that profile must never silently become the owner of work the card was assigned away from (#114294)." Resolution order in code: config key if it names an existing profile → root task's own assignee → active default profile.
- `/opt/hermes/hermes_cli/kanban_db_graph.py:90-160` `decompose_triage_task`: "Root waits for the whole graph: link it under EVERY child", "Flip the root triage -> todo, assignee -> orchestrator", comment "Decomposed into …. Root will wake when all children complete."
- **Tier:** Verified (docs + local source v0.22.7).

### F2. The root card "wakes" the orchestrator as a *dispatcher-spawned worker*
- **Claim:** After decomposition the root sits in `todo` as a child of every leaf; when the graph completes it is promoted to `ready` and the dispatcher spawns the orchestrator profile as an ordinary headless worker on that card to "judge completion and add more tasks".
- **Source:** official docs — kanban#auto-vs-manual-orchestration; kanban-tutorial.
- **Quote (kanban):** "The original triage task becomes the parent of every leaf in the graph, so it stays alive until the whole graph completes - and then promotes back to `ready` so its assignee (`kanban.orchestrator_profile`, else the assignee the task already had, else the active default profile) can judge completion and add more tasks if the work isn't done. This is the \"drop a one-liner, walk away\" flow."
- **Quote (tutorial):** "The original task is held alive as the parent so its assignee (`kanban.orchestrator_profile`, or the active default profile when unset) wakes back up to judge completion when everything finishes."
- **Implication (verified via F5/F6):** that wake is a normal worker run — the orchestrator profile receives `KANBAN_GUIDANCE`, must `kanban_show()` first and end with `kanban_complete`/`kanban_block`, and is subject to the protocol-violation nudge/retry budget. With local config `orchestrator_profile: default`, the dispatcher spawns a headless `hermes -p default` process on the root card.
- **Tier:** Verified.

### F3. Auto vs Manual: what the decomposer does, and what Manual does *not* disable
- **Claim:** `auto_decompose: true` makes the gateway dispatcher call the decomposer every tick on up to `auto_decompose_per_tick` (3) triage tasks; `false` leaves triage cards until a human/profile acts; Manual disables *only* the built-in triage decomposer — profiles can still `kanban_create`, and creator wake-ups still fire.
- **Source:** official docs — kanban#auto-vs-manual-orchestration
- **Quote:** "**Auto (default)** — `kanban.auto_decompose: true`. The gateway-embedded dispatcher runs the **decomposer** on each tick, capped by `kanban.auto_decompose_per_tick` (default 3 tasks per tick) … The decomposer uses the built-in decomposition prompt plus the `auxiliary.kanban_decomposer` model path, reads your installed profiles + their descriptions, and asks the LLM to produce a JSON task graph: which tasks to spawn, who they go to, and which depend on which."
- **Quote:** "**Important boundary:** Manual mode disables only the built-in Triage decomposer. It does not prevent a profile from calling `kanban_create`, and it does not disable creator-session wake-ups. With `kanban.auto_subscribe_on_create: true`, a task's terminal event resumes the originating agent with a synthetic status turn so it can inspect the handoff and decide whether genuinely new follow-up work is needed. Set `auto_subscribe_on_create: false` when task completion should remain passive. For provenance, built-in decomposer children use `created_by=auto-decomposer`; tasks created by a resumed profile carry that profile name instead."
- **Quote (routing):** "The decomposer NEVER lands a child task with `assignee=None`: when the LLM picks an unknown profile, the child gets routed to `kanban.default_assignee`, else the root task's assignee (if it names an existing profile), else the active default profile."
- **Local source — the decomposer prompt** (`/opt/hermes/hermes_cli/kanban_decompose.py:37-91`): "You are the Kanban decomposer for the Hermes Agent board. A user dropped a rough idea into the Triage column. Your job is to break it into a small graph of concrete child tasks and route each one to the best-matching profile from the available roster." Rules include "Use 2-6 tasks for normal work.", "Prefer parallelism.", "Pick assignees from the roster by matching the task to the profile's DESCRIPTION (not just the name)", "Each child task body is what a fresh worker will read with no other context". `fanout:false` collapses to specify behaviour. Auto mode re-reads `kanban.auto_decompose` live every tick (`gateway/kanban_watchers_common.py:66-87`: "Auto-decompose is a safety toggle").
- **Local config divergence:** docs default is `true`; this install has `auto_decompose: false` (`/opt/data/config.yaml:52`).
- **Tier:** Verified.

### F4. `hermes kanban specify` = single-task spec rewrite, triage → todo; decompose is a strict superset
- **Claim:** `specify` runs `auxiliary.triage_specifier` to flesh out one triage card (goal, approach, acceptance criteria) and promote it to `todo`, with no fan-out; `decompose` falls back to specify when the LLM decides not to fan out.
- **Source:** official docs — kanban (dashboard drawer section; REST table; collaboration pattern P9) and kanban-tutorial.
- **Quote:** "**⚗ Decompose** fans the task out into a graph of child tasks routed to specialist profiles by description, and **✨ Specify** does a single-task spec rewrite. Decompose falls back to specify-style promotion when the LLM decides the task doesn't benefit from fan-out, so it's a strict superset. Both are reachable from the CLI (`hermes kanban decompose <id>` / `specify <id>` / `--all`), from any gateway platform (`/kanban decompose <id>`), and programmatically via `POST /api/plugins/kanban/tasks/:id/decompose` and `…/specify`."
- **Quote (REST):** "`POST /tasks/:id/specify` — Run the triage specifier — auxiliary LLM fleshes out the task body and promotes it from `triage` to `todo`."
- **Quote (P9):** "**P9 Triage specifier** | rough idea → `triage` → `hermes kanban specify` expands body → `todo` | \"turn this one-liner into a spec'd task\""
- **Local:** `/opt/hermes/hermes_cli/kanban.py:1296-1317` (`_cmd_specify`, `_cmd_decompose`, shared `_run_triage_sweep` — "one task id XOR `--all`", `--tenant` filter).
- **Tier:** Verified.

### F5. The auto-injected guidance (`KANBAN_GUIDANCE`) — exact text, and who receives it
- **Claim:** The "orchestration guidance auto-injected into every kanban worker's system prompt" is the `KANBAN_GUIDANCE` constant; it is injected only when the process is a dispatcher-owned worker that owns `HERMES_KANBAN_TASK` and has `kanban_show` in its tool names — not for an interactive session that merely enabled the toolset, not for `delegate_task` children, not for cron runs inside a worker.
- **Source (docs):** kanban#the-worker-lifecycle and #why-tools-instead-of-shelling-to-hermes-kanban.
- **Quote:** "Every profile that works kanban tasks automatically gets the worker lifecycle — it's injected into the worker's system prompt at spawn (the `KANBAN_GUIDANCE` block), so there is **nothing to install or configure**."
- **Quote:** "The auto-injected kanban guidance teaches the model which tool to call when and in what order. It is injected only for the dispatcher-spawned worker that owns the task: an interactive session that merely has the `kanban` toolset enabled keeps the tools but is not told it \"has been assigned ONE task\", and a `delegate_task` child or a cron run fired from inside a worker — which inherit the worker's `HERMES_KANBAN_TASK` — neither receives the worker protocol nor records a terminal outcome against the worker's card when its own turn budget runs out."
- **Source (local):** `/opt/hermes/agent/prompt_builder.py:263-342` (text), `/opt/hermes/agent/system_prompt.py:287-296` and `/opt/hermes/agent/agent_init.py:1043-1045` (gate: `KANBAN_GUIDANCE if owned_kanban_task() and "kanban_show" in agent.valid_tool_names else ""`).
- **Verbatim text of the orchestration-relevant sections (prompt_builder.py:263-342):**
  - Header: "# Kanban task execution protocol — You have been assigned ONE task from the shared board at `~/.hermes/kanban.db`. Your task id is in `$HERMES_KANBAN_TASK`; your workspace is `$HERMES_KANBAN_WORKSPACE`. The `kanban_*` tools in your schema are your primary coordination surface…"
  - Lifecycle step 4: "**Block on genuine ambiguity.** If you need a human decision you cannot infer (missing credentials, UX choice, paywalled source, peer output you need first), call `kanban_block(reason=\"...\")` and stop. Don't guess. The user will unblock with context and the dispatcher will respawn you."
  - Step 5 (review model): "If `kanban_show()` lists child IDs, inspect those cards with `kanban_show(task_id=...)` before choosing the terminal action. When any pre-created review, QA, or release child depends on your task, call `kanban_complete` … Never sticky-block that parent for `review-required` and never request same-card review as well … Review is not a block, so repeated review cycles do not trip unblock-loop detection."
  - Step 6: "**If follow-up work appears, create it; don't do it.** Use `kanban_create(title=..., assignee=<right-profile>, parents=[your-task-id])` to spawn a child task for the appropriate specialist profile instead of scope-creeping into the next thing."
  - Step 7: hotspot flagging — "leave a `kanban_comment` starting with `hotspot: <path> — <one-line reason>` … so the orchestrator can decompose that file before more work lands on it."
  - "## Orchestrator mode — If your task is itself a decomposition task (e.g. a planner profile given a high-level goal), use `kanban_create` to fan out into child tasks — one per specialist, each with an explicit `assignee` and `parents=[...]` to express dependencies. Then `kanban_complete` your own task with a summary of the decomposition. Do NOT execute the work yourself; your job is routing, not implementation."
  - "**Decision ownership.** Design decisions belong to you, the orchestrator, not to workers — settle naming schemes, schemas, file formats, and API shapes before fanning out. Never let two subtree cards decide the same question: if two tasks would each pick one, decide it yourself and write the decision into BOTH card bodies. Every child card body must carry the decisions it depends on, because workers cannot see sibling context."
  - Reference: "**Orchestrating: discover profiles first.** The dispatcher SILENTLY drops a card with an unknown assignee (it sits in `ready` forever). Ground every assignee in a real profile (`hermes profile list`, or ask the user), and express dependencies via `parents=[...]` on `kanban_create`, not prose."
  - "## Do NOT — Do not shell out to `hermes kanban <verb>` … Do not complete a task you didn't actually finish. Block it. — Do not call `clarify` to ask questions. You are running headless — there is no live user to answer. The call will time out and the task will sit silently in `running` with no signal to the operator. Instead: `kanban_comment` the context, then `kanban_block(reason=...)` so the task surfaces on the board as needing input. — Do not assign follow-up work to yourself. Assign it to the right specialist profile. — Do not call `delegate_task` as a board substitute."
- **Note:** `/opt/hermes/tools/kanban_toolset_context.py` (named in the brief) does *not* contain the guidance; it is a 28-line ContextVar helper recording whether `kanban` was explicitly named in a platform's toolset selection ("An all/default selection is not an explicit workflow opt-in."). The guidance lives in `agent/prompt_builder.py`.
- **Tier:** Verified (docs + local source v0.22.7).

### F6. "How the orchestrator behaves": decompose, link, assign, step back; restrict its toolsets
- **Claim:** Docs prescribe that a well-behaved orchestrator never does the work, decides design questions before fan-out, and should run in a profile whose toolsets are restricted to board operations.
- **Source:** official docs — https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban#how-the-orchestrator-behaves
- **Quote:** "A **well-behaved orchestrator does not do the work itself.** It decomposes the user's goal into tasks, links them, assigns each to one of the profiles you've set up, and steps back. The orchestrator guidance — anti-temptation rules, a Step-0 profile-discovery prompt (the dispatcher silently fails on unknown assignee names, so the orchestrator must ground every card in profiles that actually exist on your machine), and a decomposition playbook keyed on `kanban_create` / `kanban_link` / `kanban_comment` — is injected into the worker's system prompt automatically; there is nothing to install."
- **Quote:** "**Decide before you fan out.** Design decisions belong to the orchestrator, not to the workers. … Workers cannot see sibling cards, so every child card body must carry every decision it depends on."
- **Quote:** "For best results, pair it with a profile whose toolsets are restricted to board operations (`kanban`, `gateway`, `memory`) so the orchestrator literally cannot execute implementation tasks even if it tries."
- **Canonical orchestrator turn (docs code block):** `kanban_create(... assignee="researcher-a")` ×2 → `kanban_create(... assignee="writer", parents=["t_r1","t_r2"])` → optional `kanban_link` → `kanban_complete(summary="decomposed into 2 parallel research tasks → 1 synthesis task; …")`.
- **Tier:** Verified.

### F7. Director profile pattern (creative-kanban-video-orchestrator skill page)
- **Claim:** The documented example of a coordinator profile is a *board-resident "director" profile*: the human-facing chat session runs discovery/brief/team design and a setup script, fires one initial card assigned to the director, and the director profile (a dispatcher-spawned worker on that card) decomposes via the kanban toolset and "never executes".
- **Source:** official docs — https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/creative/creative-kanban-video-orchestrator
- **Quote:** "7. Fires the initial `hermes kanban create` task assigned to the director" … "The director profile takes over from here, decomposing the work and routing tasks to specialist profiles via the kanban toolset."
- **Quote (rule 6):** "**The director never executes.** Even with the full `kanban + terminal + file` toolset, the director's `SOUL.md` rules forbid it from executing work itself. It decomposes and routes only — every concrete task becomes a `hermes kanban create` call to a specialist profile. The kanban orchestration guidance auto-injected into every kanban worker's system prompt spells this out further."
- **Quote (monitoring is human/chat-side):** "Stay engaged — the kanban runs autonomously but a stuck task or bad output needs human (or AI) judgment. Monitoring patterns: poll `kanban list` periodically, inspect any RUNNING task that exceeds its expected duration with `kanban show <id>`, and check heartbeats. When a worker's output fails review, the standard interventions are: 1. Comment on the worker's task with specific feedback (`kanban_comment`) 2. Create a re-run task with the original as parent 3. Adjust the brief's scope and let the director re-decompose".
- **Quote (rule 7):** "**Don't over-decompose.** A 30-second product video does NOT need 20 tasks. Aim for the smallest task graph that still parallelizes well and exposes the right human-review gates."
- **Observation:** the skill splits the four axes cleanly — plan made in chat (brief.md is "the contract"), state on the board + shared `dir:` workspace, human talks via comments/re-run cards, execution by specialist profiles; the director is a *worker run*, not a standing process.
- **Tier:** Verified (docs page is the skill's full SKILL.md).

### F8. Tool split: task-scoped lifecycle tools vs orchestrator-only routing tools
- **Claim:** All 14 `kanban_*` tools are registered for dispatcher workers and for profiles that explicitly enable `kanban`; `kanban_list` and `kanban_unblock` are orchestrator-only and hidden from dispatcher-spawned workers; `all`/`*` never enables kanban; `delegate_task` children can never mutate the board.
- **Source:** official docs — https://hermes-agent.nousresearch.com/docs/reference/tools-reference#kanban-toolset ; https://hermes-agent.nousresearch.com/docs/reference/toolsets-reference ; kanban#enabling-tools-for-a-chat-profile
- **Quote (tools-reference):** "Registered when the agent is either (a) spawned by the kanban dispatcher (`HERMES_KANBAN_TASK` env set) or (b) running in a profile that explicitly enables the `kanban` toolset. Task-scoped workers use lifecycle tools for their assigned task; orchestrator profiles additionally get board-routing tools like `kanban_list` and `kanban_unblock`."
- **Quote (tools-reference, kanban_block row):** "Block the current task on a question for the user — the dispatcher pauses, surfaces the question, and resumes once a human replies."
- **Quote (toolsets-reference):** "**Workflow-gated** tools — the `kanban` toolset — are deliberately opt-in. `all`/`*` does **not** enable kanban; you must list `kanban` explicitly (or be a dispatcher-spawned worker with `HERMES_KANBAN_TASK` set)."
- **Quote (kanban):** "`hermes -p planner tools enable kanban` … A gateway agent that has it can `kanban_create` from a chat and is auto-subscribed to that task's completion/block notifications in the same thread. Start a new chat after changing this setting; existing conversations retain their tool schemas and prompt cache." and "Dispatcher-owned workers receive their task lifecycle tools automatically. `delegate_task` children do not gain permission to mutate the board."
- **Quote (kanban):** "The \"(Orchestrators)\" tools — `kanban_list`, `kanban_create`, `kanban_link`, `kanban_unblock`, and `kanban_comment` on foreign tasks — are available through the same toolset; the convention (encoded in the auto-injected kanban guidance) is that worker profiles don't fan out or route unrelated work, and orchestrator profiles don't execute implementation work. Dispatcher-spawned workers are still task-scoped for destructive lifecycle operations and cannot mutate unrelated tasks."
- **Local:** `/opt/hermes/tools/kanban_tools.py:1294` `_ORCHESTRATOR_TOOLS = frozenset({"kanban_list", "kanban_unblock"})`; `:100-103` `_check_kanban_orchestrator_mode` "Board-routing tools (kanban_list, kanban_unblock): hidden from task workers."; `:301-308` `_require_orchestrator_tool` rejects with "is orchestrator-only; dispatcher-spawned workers must use kanban_complete, kanban_request_review, kanban_request_changes, kanban_block, kanban_heartbeat, or kanban_comment for their assigned task." Also the 15th tool `kanban_schedule` exists locally (not in the docs' 14-tool list): "Park your task as 'scheduled' … non-dispatchable until an orchestrator unblocks it; it does not create a timer." (`kanban_tools_schemas.py:202-218`).
- **Tier:** Verified.

### F9. `kanban_block` kinds, `needs_input` re-kinding, dependency waits
- **Claim:** `kanban_block(kind=...)` routes by cause: `dependency` → `todo` (auto-resumes, no human, no recurrence count) but is re-kinded to `needs_input` (sticky) when no parent is open; `needs_input` / `capability` / `transient` → `blocked` (surface to a human) and count toward the loop breaker.
- **Source:** official docs — kanban tool table + event reference.
- **Quote:** "`kanban_block` | Stop work and route by why: `kind=dependency` (waits in `todo`, auto-resumes when an incomplete parent finishes; with no open parent it is recorded as `needs_input` instead, since the wait could never be satisfied), `needs_input`/`capability`/`transient` (surface to a human). Repeated same-kind re-blocks auto-escalate to `triage`."
- **Quote (event `blocked`):** "`kind` is the typed block reason (`needs_input`, `capability`, `transient`, or `null` for a generic block); `recurrences` is the unblock-loop counter. A `kind=dependency` block with no incomplete parent lands here as `needs_input` (payload adds `requested_kind: dependency`, `rekind_reason: no_open_parent`) because `todo` would only get it re-promoted and respawned on the next dispatch tick."
- **Quote (event `dependency_wait`):** "Worker blocked with `kind=dependency` while at least one parent is still open — the task is only waiting on another task, so it routes to `todo` (parent-gated, auto-promoted) instead of `blocked` and no recurrence is counted. No human needed."
- **Local:** `/opt/hermes/hermes_cli/kanban_db.py:111` `VALID_BLOCK_KINDS = {"dependency", "needs_input", "capability", "transient"}`; `:3178-3182` re-kind; `:3211-3240` `_route_block`. Tool schema (`kanban_tools_schemas.py:167-199`): "'needs_input' (you need a human decision/answer), 'capability' (a hard wall: no access, missing credentials, an action no agent can do), or 'transient' (a flaky failure that may clear). ``reason`` is shown to the human on the board. … Use for genuine blockers only — don't block on things you can resolve yourself." Reason guidance: "Don't paste the whole conversation; the human has the board and can ask follow-ups via comments." Goal-mode cards may only block with `dependency`/`needs_input` (`kanban_tools.py:451`).
- **Tier:** Verified.

### F10. `block_loop_detected` / triage escalation is a deterministic DB guard with a hard-coded limit
- **Claim:** After a card is blocked → unblocked → re-blocked for the same kind `BLOCK_RECURRENCE_LIMIT` (2) times it is routed to `triage` (event `block_loop_detected`) instead of `blocked`; the counter survives unblock and resets only on successful `complete`; the limit is a module constant, not a config key.
- **Source:** official docs — kanban#bulk-cli-verbs ("Where an unblocked task lands") + event reference.
- **Quote:** "after a task is blocked → unblocked → re-blocked for the same cause `BLOCK_RECURRENCE_LIMIT` times (default `2`), the unblock-loop breaker stops sending it back to `blocked` — where a cron would just keep unblocking it — and routes it to `triage` for orchestration attention. This is a deterministic DB guard, not an LLM judgment call, and a task's body text cannot opt out of it: the recurrence counter deliberately survives each unblock (it resets only on a successful `complete`). To keep an unblocked task in the work pool, resolve _why it keeps re-blocking_ (unfinished parent, missing input, unmet capability) before unblocking, or raise `BLOCK_RECURRENCE_LIMIT` if the loop is expected."
- **Quote (event):** "`block_loop_detected` | `{reason, kind, recurrences, limit}` | A task was unblocked and re-blocked for the same reason `BLOCK_RECURRENCE_LIMIT` times (default 2). Instead of landing in `blocked` again — where a cron would keep unblocking it — it routes to `triage` for orchestration attention, breaking the unblock↔re-block loop."
- **Quote (unblock):** "`unblock` never routes directly to `triage`." and "Resets the dispatcher's `consecutive_failures` but deliberately preserves `block_recurrences` so the loop breaker keeps its memory."
- **Local:** `/opt/hermes/hermes_cli/kanban_db.py:115` `BLOCK_RECURRENCE_LIMIT = 2` (constant; no `kanban.*` config key found — the docs' "raise `BLOCK_RECURRENCE_LIMIT`" implies a source edit). CLI message (`kanban.py:997-1001`): "`{tid} → triage (unblock loop detected — needs a human decision)`" when kind is `needs_input`, else "orchestration attention needed".
- **Consequence for a coordinator:** in Auto mode a card landing in `triage` via the breaker is *picked up by the decomposer* (`list_triage_ids` = all status=`triage` tasks, `kanban_specify.py:237-241`; `decompose_triage_task` refuses only roots that already carry a `decomposed` event). In Manual mode it waits for a human/orchestrator. The docs do not state this interaction explicitly; it follows from the code. **Tier for this consequence: Plausible (code-derived, not demonstrated).**
- **Tier (main claim):** Verified.

### F11. `max_in_progress_per_profile`
- **Claim:** Caps how many tasks one assignee profile may run concurrently; applies alongside board-wide `max_in_progress`; both must allow a spawn.
- **Source:** official docs — kanban#concurrency-scheduling-and-child-promotion-config
- **Quote:** "`kanban.max_in_progress_per_profile` | unset (unlimited) | Per-profile variant of `max_in_progress` — caps how many tasks any single assignee profile may run concurrently. Useful when one profile is slow or rate-limited but others should keep flowing. Applies alongside the board-wide `max_in_progress`; both must allow a spawn for it to proceed."
- **Local:** `/opt/hermes/hermes_cli/kanban_db_dispatch.py:94,127,2394-2400` (skipped tasks surfaced as "assignee is at ``kanban.max_in_progress_per_profile``… Picked up on a later" tick). Local value: 5 (`/opt/data/config.yaml:49`). Note: with `orchestrator_profile: default` the orchestrator's own root-card wake runs count against `default`'s cap too (code-derived — Plausible).
- **Tier:** Verified.

### F12. How a question reaches a human — the documented channels
- **Claim:** The only documented worker-side primitive for asking a human is `kanban_comment` + `kanban_block(kind=needs_input)`; delivery is via (a) the dashboard/Desktop Blocked column and toasts, (b) gateway subscriptions (Telegram/Discord/…) that deliver one message per terminal event, optionally waking the originating chat agent (`notify+wake`), (c) `/kanban comment` + `/kanban unblock` from any chat, which bypass the running-agent guard.
- **Source:** official docs — kanban#gateway-notifications, #delivery-modes, #desktop-notifications, #mid-run-usage-kanban-bypasses-the-running-agent-guard, #auto-subscribe-on-kanban-create-gateway-only; tools-reference.
- **Quote (gateway):** "When you run `/kanban create …` from the gateway (Telegram, Discord, Slack, etc.), the originating chat is automatically subscribed to the new task. The gateway's background notifier polls `task_events` every few seconds and delivers one message per terminal event (`completed`, `blocked`, `gave_up`, `crashed`, `timed_out`) to that chat."
- **Quote (which events wake):** "The ones that return a task outcome or require orchestration attention: `completed`, `blocked`, `gave_up`, `crashed`, `timed_out`, `review_requested` … and `block_loop_detected` (the task was routed to `triage` after repeated blocks). `status`, `archived` and `unblocked` are delivered but never wake".
- **Quote (wake semantics):** "A \"wake\" forges a synthetic inbound message to the destination gateway agent so it takes a normal turn (reads the comment + result, reasons, replies) instead of getting a one-line passive notification. It only fires when the notifier runs inside a live gateway process".  "Admission is not a guarantee of model execution or a successful reply … This is not exactly-once delivery".
- **Quote (desktop):** "each `completed`, `blocked`, `gave_up`, `crashed`, `timed_out`, or routed-to-triage (`block_loop_detected`) event raises an in-app toast … Events that land while the app is closed are not replayed as notifications on next launch — use a gateway subscription (below) for delivery that must survive the app being closed."
- **Quote (phone loop):** "A worker blocks waiting on a peer → you send `/kanban unblock t_abcd` from your phone and the dispatcher picks the peer up on its next tick. … You spot a card that needs human context → `/kanban comment t_xyz \"use the 2026 schema, not 2025\"` lands on the task thread and the _next_ run of that task will read it in `kanban_show()`."
- **Quote (worker-created cards inherit subscriptions):** "Dispatcher workers creating tasks through `kanban_create` or `hermes kanban create` copy the owning task's durable notification subscriptions even without `parents` dependency links."
- **Quote (plugin hooks):** "`kanban_task_blocked` … register the hook in the dispatcher profile to observe every transition centrally."
- **Local:** `gateway/kanban_watchers_notifier.py:50` `_WAKE_KINDS = ("completed","gave_up","crashed","timed_out","blocked","review_requested","changes_requested","block_loop_detected")`; `:520-521` "Worker handoff carried into the synthetic wake turn so the woken creator doesn't re-decompose work already on the board."
- **Not documented:** any "kanban-mode plugin" as a question channel. The local `/opt/data/plugins/kanban-mode` is a third-party plugin by "Big-Whoop (kanban-tools)" (v1.0.0, `pre_llm_call` hook that batch-loads the toolset); it is not in the official docs.
- **Tier:** Verified (channels); "no kanban-mode plugin in docs" — Verified by absence in the pages read.

### F13. Interactive orchestrator session: wake-on-event, but limited board authority
- **Claim:** A chat session with the kanban toolset (`auto_subscribe_on_create: true`) is resumed with a synthetic status turn on terminal events of cards it created, but it is *not* a run owner: it cannot `kanban_complete` a card whose worker holds a live claim, and the auto-subscribe is skipped for `--json` scripted creates.
- **Source:** official docs — kanban#auto-vs-manual-orchestration config table; #runs--one-row-per-attempt ("Live-claim guard on complete").
- **Quote:** "`auto_subscribe_on_create` | `true` | When `kanban_create` runs inside a persistent gateway/TUI session, terminal events resume that originating agent with a synthetic status turn. Set to `false` for passive completion or to require explicit `kanban_notify-subscribe` calls. Independent of `auto_decompose`."
- **Quote:** "A claim-less `hermes kanban complete <id>` or an orchestrator session's `kanban_complete` is refused with a pointer to `--force` / `hermes kanban reclaim`, so a second session can no longer close a live worker's run underneath it."
- **Quote (kanban_create lineage):** "For `kanban_create`, session lineage resolves in this order: explicit `session_id`, the owning worker task's durable session, request-scoped API origin, then the current session. … Built-in decomposition also inherits its root's durable session."
- **Tier:** Verified.

### F14. Cost split: frontier orchestrator, cheap workers
- **Claim:** Docs recommend running the orchestrator/dispatcher profile on a frontier model and workers on inexpensive models, because tokens are spent mostly in workers.
- **Source:** kanban#cost-strategy-frontier-orchestrator-inexpensive-workers
- **Quote:** "Decomposing a project into well-scoped cards takes frontier-level judgment; executing a card that already carries a clear goal, context, and handoff evidence usually doesn't — and the workers are where the vast majority of tokens are spent, so the worker model is where the cost lives. Run your orchestrator/dispatcher profile on a frontier model and point worker profiles at inexpensive models."
- **Tier:** Verified.

### F15. Profile descriptions are the routing primitive (profiles / profile-commands docs)
- **Claim:** `hermes profile create --description` / `hermes profile describe` is what the decomposer ("kanban orchestrator") uses for routing; `--no-skills` is suggested for narrow orchestrator profiles.
- **Source:** https://hermes-agent.nousresearch.com/docs/reference/profile-commands ; https://hermes-agent.nousresearch.com/docs/user-guide/profiles
- **Quote:** "`--description \"<text>\"` | One- or two-sentence description of what this profile is good at. Used by the kanban orchestrator to route tasks based on role instead of profile name alone." ; "`--no-skills` … Useful for narrow orchestrator profiles or sandbox profiles that should not inherit the full skill catalog."
- **Quote (profiles):** "If you plan to use this profile as a kanban worker (or want the kanban orchestrator to route work to it), pass `--description \"<role>\"` at create time so the orchestrator knows what it's good at".
- **Tier:** Verified.

### F16. Kanban vs delegate_task: coordination is peer, not hierarchical
- **Claim:** Docs position the board as a peer work queue ("any profile reads/writes any task") and `delegate_task` as an RPC; delegate children inside a worker die with the worker and cannot touch the board.
- **Source:** kanban#kanban-vs-delegate_task
- **Quote:** "| Coordination | Hierarchical (caller → callee) | Peer — any profile reads/writes any task |" ; "**Use Kanban when** work crosses agent boundaries, needs to survive restarts, might need human input, might be picked up by a different role, or needs to be discoverable after the fact." ; "If the gateway goes down mid-child, the child is retired, never resumed. Work that must outlive the gateway, or needs its own reviewer, still belongs in child cards".
- **Tier:** Verified.

### F17. Kanban Swarm helper — a documented one-shot coordinator topology without an orchestrator profile
- **Claim:** `hermes kanban swarm` creates a complete root(blackboard)+workers+verifier+synthesizer graph atomically; shared context lives as JSON comments on the root card.
- **Source:** kanban#kanban-swarm-topology-helper
- **Quote:** "`hermes kanban swarm` creates a durable **Kanban Swarm v1** graph in one shot: a completed root/blackboard card, N parallel worker cards, a verifier card gated on all workers, and a synthesizer card gated on the verifier. Shared swarm context (the \"blackboard\") is stored as structured JSON comments on the root card so any worker can read it."
- **Tier:** Verified.

### F18. Review handoffs are not blocks; `kanban_block` reserved for external escalation
- **Claim:** The tutorial and guidance say review feedback goes through `kanban_request_review` / `kanban_request_changes`, never `kanban_block`; with a pre-created reviewer child the implementer must `kanban_complete`.
- **Source:** kanban-tutorial Story 3; kanban-multi-gateway.
- **Quote:** "`kanban_block` is reserved for a real external escalation (missing access, a product decision, unavailable infrastructure), not normal review feedback." ; "Never block the implementation parent merely to ask for review."
- **Quote (multi-gateway):** "A `changes_requested` review event is delivered as an actionable review-BLOCK notification. … Review feedback never creates, unblocks, requeues, or otherwise mutates a task."
- **Tier:** Verified.

### F19. Release notes 0.22.x–0.22.7: no orchestrator/decomposer behaviour change is called out
- **Claim:** The GitHub release notes for v0.22.0 (Threshold) through v0.22.7 mention Kanban only for worker retry-in-place, board explainability, workflow/`kanban_schedule`/`--body-file`, pinned boards as Desktop tabs, and "see and clear Kanban blocks" in the Desktop; nothing on orchestrator_profile / decomposer semantics. v0.22.5–0.22.7 are roll-ups whose "full curated notes ship with v0.23.0" (not yet published as of 2026-11-06).
- **Source:** https://github.com/NousResearch/hermes-agent/releases (page 1) and https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.0
- **Quote (v0.22.0 ### Kanban):** "**Workers ride out provider trouble** — Failed turns retry in place with context; rate limits or 5xx requeue instead of burning retries. (#112318, #112500)" ; "**A board that explains itself** — Cards show the worker's last output on failure; dispatch says why a card is held. (#112618)" ; "**Workflow and tooling** — One workflow definition drives columns; workers get `kanban_schedule`; `kanban create --body-file`; Desktop follows gateway switches. (#134340, #130455, #116791, #119054)"
- **Quote (v0.22.0 Desktop):** "Browse SSH workspaces, drag sessions onto projects, search logs, see and clear Kanban blocks. (#128428)"
- **Quote (v0.22.7):** "Patch release. This tag rolls up the ~174 PRs merged since v0.22.6 … Full curated notes for this window ship with v0.23.0." ; "pinned Kanban boards as quick-switch tabs".
- **Origin of the decomposer:** PR #27572 "feat(kanban): orchestrator-driven auto-decomposition on triage" (teknium1) — predates 0.22 (search result; PR body not read).
- **Tier:** Verified (release pages read); PR #27572 attribution — Plausible (search snippet only).

### F20. Documented limits of the board-resident coordinator (consolidated)
All quotes above; listed here as the "documented limits" deliverable:
1. The decomposer is prompt-only: no profile SOUL/skills/tools, 2–6 children, routes by description, never leaves `assignee=None` (F1, F3).
2. The orchestrator profile only "wakes" as a *headless worker on the root card after the whole graph is done* — there is no standing supervisor loop; mid-graph supervision is the human's (dashboard, `/kanban`, subscriptions) or an interactive session's wake turns (F2, F12, F13).
3. The injected orchestration guidance reaches only dispatcher-owned workers; an interactive orchestrator session gets tools but no protocol (F5).
4. Workers cannot see sibling cards; every decision must be written into each child body by the orchestrator (F5, F6).
5. Unknown assignee → card sits in `ready` forever / `skipped_nonspawnable`; orchestrator must discover profiles first (F5, F6).
6. Questions to humans only via comment + `kanban_block(kind=needs_input)`; `clarify` is forbidden in workers; a blocked card waits for a human `unblock`; two same-kind re-blocks → `triage` (hard-coded limit 2) (F9, F10, F12).
7. In Auto mode `triage` is also the decomposer's input queue; Manual mode is the documented way to keep control ("useful when you want full control over what runs when") (F3, F10).
8. Interactive orchestrator sessions cannot complete a live worker's run; `delegate_task` children and cron runs inside workers cannot mutate the board (F8, F13).
9. Notifications: desktop toasts only while the app is open; gateway wake is "not exactly-once", admission ≠ execution (F12).
10. Single host only; no cross-board links; per-profile concurrency caps also constrain the orchestrator profile's own root-card runs (F11, kanban#out-of-scope: "Kanban is deliberately single-host.").
11. Governance is user-space: "Auto-assignment, budgets, governance gates, and org-chart views remain user-space — a router profile, another plugin, or a reuse of `tools/approval.py`" (kanban#scope-boundary).

---

## C. Notes on this install vs the docs
- `kanban.auto_decompose: false`, `orchestrator_profile: default`, `default_assignee: worker`, `max_in_progress_per_profile: 5`, `dispatch_interval_seconds: 5` (`/opt/data/config.yaml:47-52`). Docs' default `auto_decompose` is `true`.
- `auxiliary.kanban_decomposer` / `triage_specifier` / `profile_describer` are `provider: auto, model: ''` locally (fall back to main chat model).
- The `kanban` toolset is explicitly listed on platform selections (`config.yaml:225,329`), so the interactive `default` session has orchestrator tools; per F5 it does not get `KANBAN_GUIDANCE`.
- Local extra tool `kanban_schedule` (15 tools) vs docs' 14.
- Docs reference `skills/devops/kanban-orchestrator` in a search result (GitHub tree URL), but the raw SKILL.md returned 404 and the skill is not present under `/opt/hermes/skills/devops/` (only `sdlc-review`) — not verifiable here.

---

## Searched, found nothing
- Official docs page `/docs/reference/cli` — HTTP 404 (no standalone CLI kanban reference page; the CLI reference lives inside `/docs/user-guide/features/kanban#cli-command-reference`).
- `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/CHANGELOG.md` — 404 (no top-level CHANGELOG; release notes only on GitHub Releases).
- `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/skills/devops/kanban-orchestrator/SKILL.md` — 404; not installed locally either.
- Web search `site:github.com NousResearch/hermes-agent kanban orchestrator decomposer changelog 0.23` — no v0.23.0 notes exist yet; only roll-up release stubs.
- Web search `hermes-agent docs "kanban-mode" plugin orchestrator questions human needs_input` — no official doc on a "kanban-mode" plugin; only Reddit threads (not read in depth; one snippet claims the default profile "can't use the kanban tools" — outdated relative to current docs §Enabling tools for a chat profile).
- Local source grep for a `kanban.block_recurrence_limit`-style config key — none; `BLOCK_RECURRENCE_LIMIT` is a constant in `hermes_cli/kanban_db.py:115`.
- Docs text of a dedicated "orchestrator guidance" separate from `KANBAN_GUIDANCE` — none; the "orchestrator guidance" the docs mention is the "## Orchestrator mode" + "Decision ownership" + "discover profiles first" sections of the same block.
- Docs statement on whether the orchestrator's root-card wake counts against `max_in_progress_per_profile` — not stated (code-derived only).

Sub-question status from this lane's view: answered
