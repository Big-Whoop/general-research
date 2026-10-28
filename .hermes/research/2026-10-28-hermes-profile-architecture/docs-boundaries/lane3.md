# LANE L3 — Documented boundaries between profile / Bot Mode / delegate_task / cron / kanban worker profiles / MoA (SQ3)

Method: all 12 lane starting URLs read whole via web_extract (bot-mode, kanban, kanban-multi-gateway,
kanban-worker-lanes, delegation, delegation-patterns, cron, automate-with-cron, cron-script-only,
mixture-of-agents, git-worktrees, heartbeat), plus one extra extract of
`/docs/user-guide/profiles#profiles-agents-and-bots` because bot-mode cross-references it as THE
terminology boundary section. No web_search bursts were needed (docs-first gate satisfied).
Every quote below is verbatim from the fetched official docs page named.

---

## F1. Mechanism-ownership table (the lane's deliverable, assembled from the cited findings)

| Mechanism | What it owns (docs position) | Explicitly NOT / hand-off point |
|---|---|---|
| **Profile** | Persistent identity: config, memory, skills, credentials, sessions (`~/.hermes/profiles/<name>/`) | Not a scheduler, not a work queue; "a separate conversation is different from a separate profile" |
| **Bot Mode** | Desktop presentation + interaction layer over profiles: roster, canonical Bot Chat, routines UI, group chats, bot-to-bot messaging | Adds no new primitive; a Bot *is* a profile; never owns profiles/sessions/cron |
| **delegate_task** | Ephemeral parallel subtasks inside the parent's session/process; only the final summary returns | Not durable (restart strands children), not interactive (no `clarify`), cannot widen toolsets; durable work → cron / background terminal |
| **Cron (LLM job)** | Durable scheduled/event-triggered agent runs, profile-local store and secret scope | Cannot create cron jobs recursively; no in-thread context (use heartbeat); don't monitor Hermes itself with it (OS cron + webhook) |
| **Cron (no-agent)** | Zero-LLM script-on-schedule; stdout *is* the message | No reasoning — if the content needs judgment, use an LLM cron job |
| **/heartbeat** | One recurring instruction bound to *this live session*, full context | Not a durable standing job → cron |
| **Kanban** | Durable cross-profile work queue + state machine; workers are named profiles spawned as OS processes by one dispatcher gateway | Not for in-context RPC answers → delegate_task; worker's children die with the worker → child cards |
| **Kanban worker profile** | Role identity the orchestrator routes to by name/description; per-profile model = cost lever | Task-level `skills`/model pins avoid profile edits; `orchestrator_profile` owns root task only, not decomposition logic |
| **MoA preset** | A virtual *model provider* — reference models advise, aggregator acts inside one agent loop | Not multi-agent orchestration; per-profile model choice, not a profile mechanism |
| **Git worktrees** | Workspace isolation for multiple agents on one repo (branch + checkpoint history per agent) | Solves the directory dimension, not the identity/config dimension |

## F2–F5. Profile vs Bot Mode

- **F2 — A Bot adds no new primitive: a Bot is a profile plus desktop-UI presentation.**
  Source: https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode (official-docs)
  Quote: "There is no new primitive to learn: a Bot **is** a Hermes profile — isolated config, memory, skills, credentials, and chat history under ~/.hermes/profiles/<name>/. Bot Mode is a UI over that primitive"
  Tier: Verified

- **F3 — What Bots add per profile: permanent Bot Chat, roster, inter-bot messaging, group chats, routines beside the chat — nothing moves from the profile layout.**
  Source: /docs/user-guide/bot-mode (official-docs), "Coming from profiles?" table
  Quote: "Profiles never talk to each other → Bots message each other and share group chats … Nothing moves: config, memory, skills, and credentials stay in ~/.hermes/profiles/<name>/"
  Tier: Verified

- **F4 — Bot Mode can be switched off without touching anything: it owns no state.**
  Source: /docs/user-guide/bot-mode (official-docs)
  Quote: "Your profiles, sessions, and cron jobs are untouched either way; Bot Mode never owns y[ou]r…"
  Tier: Verified

- **F5 — Official terminology separates profile / agent / Bot Mode bot / messaging bot / subagent; becoming-a-Bot is only roster metadata + pinned Bot Chat.**
  Source: https://hermes-agent.nousresearch.com/docs/user-guide/profiles#profiles-agents-and-bots (official-docs)
  Quote: "Every Bot is a profile, but not every profile is a Bot … A separate conversation is different from a separate profile."
  Tier: Verified

## F6–F9. Bot Mode vs cron (routines) and Bot creation

- **F6 — Bot "routines" are ordinary per-profile cron jobs; Bot Mode is a cron UX, not a scheduler.**
  Source: /docs/user-guide/bot-mode (official-docs)
  Quote: "Routines are plain Hermes cron jobs namespaced [bot:<name>] <routine> — they also show up in hermes cron list and the core Cron page."
  Tier: Verified

- **F7 — Bot creation is a profile-equipping wizard: per-Bot model pin, custom SOUL.md, per-skill/toolset/MCP enablement, or a minimal empty profile.**
  Source: /docs/user-guide/bot-mode (official-docs)
  Quote: "Model & provider pin — give the Bot its own model … Per-skill, per-toolset, and per-MCP-server enablement — tick exactly the capabilities this specialist needs."
  Tier: Verified

- **F8 — Cron→Bot hand-off: the `bot-chat` delivery target exists exactly so a scheduled job's output becomes a message a bot profile acts on.**
  Source: /docs/guides/automate-with-cron (official-docs)
  Quote: "This is the target to use when you want a bot to see and react to scheduled output instead of just having it archived in Run history." (Caveats listed: "Machine-local." / "Costs a bot turn.")
  Tier: Verified

- **F9 — Group chats are gateway-owned durable sessions over member profiles, independent of Desktop.**
  Source: /docs/user-guide/bot-mode (official-docs)
  Quote: "When every member of a room lives on the same gateway, that gateway owns turn scheduling through a durable driver: closing Hermes Desktop … does not stop a room mid-discussion"
  Tier: Verified

## F10–F19. Kanban vs delegate_task vs profiles (the core boundary)

- **F10 — Kanban is the officially positioned cross-profile coordination mechanism, explicitly contrasted with in-process subagents.**
  Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban (official-docs)
  Quote: "a durable task board, shared across all your Hermes profiles, that lets multiple named agents collaborate on work without fragile in-process subagent swarms … every worker is a full OS process with its own identity"
  Tier: Verified

- **F11 — The docs publish an explicit kanban-vs-delegate_task table: RPC vs durable queue, anonymous vs named child.**
  Source: /docs/user-guide/features/kanban (official-docs)
  Quote: "Shape | RPC call (fork → join) | Durable message queue + state machine … Child identity | Anonymous subagent | Named profile with persistent memory"
  Tier: Verified

- **F12 — One-sentence official distinction.**
  Source: /docs/user-guide/features/kanban (official-docs)
  Quote: "delegate_task is a function call; Kanban is a work queue where every handoff is a row any profile (or human) can see and edit."
  Tier: Verified

- **F13 — Workload assignment rules, verbatim.**
  Source: /docs/user-guide/features/kanban (official-docs)
  Quote: "Use delegate_task when the parent agent needs a short reasoning answer before continuing, no humans involved, result goes back into the parent's context. … Use Kanban when work crosses agent boundaries, needs to survive restarts, might need human input, might be picked up by a different role, or needs to be discoverable after the fact."
  Tier: Verified

- **F14 — Workloads docs say delegate_task *cannot* cover (kanban's niche): triage, scheduled ops, digital twins, pipelines, fleets.**
  Source: /docs/user-guide/features/kanban (official-docs)
  Quote: "This is the shape that covers the workloads delegate_task can't: … Digital twins — persistent named assistants (inbox-triage, ops-review) that accumulate memory over time."
  Tier: Verified

- **F15 — Coexistence rule: kanban-worker children end with the worker; longer-lived work becomes child cards.**
  Source: /docs/user-guide/features/kanban (official-docs)
  Quote: "each child … returns its result inside the card's turn, and ends with the worker. If the gateway goes down mid-child, the child is retired, never resumed. Work that must outlive the gateway, or needs its own reviewer, still belongs in child cards (kanban_create with parents)."
  Tier: Verified

- **F16 — Dispatcher model: workers are profiles spawned by the dispatcher running inside the gateway.**
  Source: /docs/user-guide/features/kanban + /docs/user-guide/features/kanban-worker-lanes (official-docs)
  Quote: "Runs inside the gateway by default (kanban.dispatch_in_gateway: true) … the assignee is a profile name, the dispatcher spawns hermes -p <profile>"
  Tier: Verified

- **F17 — Multi-gateway posture: many gateway processes (one per profile), exactly one owns the kanban dispatcher.**
  Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-multi-gateway (official-docs)
  Quote: "Hermes supports multiple gateway processes running concurrently — one per profile (default, writer, admin, coder, researcher). … Only one gateway owns the kanban dispatcher."
  Tier: Verified

- **F18 — orchestrator_profile is an ownership knob, not a role loader; custom orchestrator logic requires Manual mode.**
  Source: /docs/user-guide/features/kanban (official-docs)
  Quote: "kanban.orchestrator_profile does not load that profile's prompt, skills, or custom logic into the decomposition call. It controls who owns the root/orchestration task after fan-out. … To use a profile's custom task-splitting logic instead of the built-in decomposer, switch to Manual mode and have that profile create or decompose tasks explicitly."
  Tier: Verified

- **F19 — Routing between profiles is naming + description, not a fixed roster; unknown routes fall to default_assignee.**
  Source: /docs/user-guide/features/kanban-worker-lanes + /docs/user-guide/features/kanban (official-docs)
  Quote: "choose names that match the role you want the orchestrator to route to. The orchestrator … discovers your profile names via hermes profile list — there's no fixed roster the system assumes" / "when the LLM picks an unknown profile, the child gets routed to kanban.default_assignee, else the root task's assignee (if it names an existing profile), else the active default profile"
  Tier: Verified

## F20–F24. Kanban-internal boundaries (task-level knobs vs profile edits, worker lanes, goal loop)

- **F20 — Per-task skill pins exist precisely to avoid profile edits for one-off capability needs (but skills must already exist on the assignee).**
  Source: /docs/user-guide/features/kanban (official-docs)
  Quote: "Rather than editing the assignee's profile every time, attach the skills directly to the task. … The skill names must match skills that are actually installed on the assignee's profile … there's no runtime install."
  Tier: Verified

- **F21 — Per-task model override without profile edits.**
  Source: /docs/user-guide/features/kanban (official-docs)
  Quote: "Pin a task's worker to a specific model (and optionally provider), independent of the assignee profile's default … — no profile edits needed."
  Tier: Verified

- **F22 — Cost strategy: profiles split the planner/worker cost boundary.**
  Source: /docs/user-guide/features/kanban (official-docs)
  Quote: "Kanban's per-profile configs make the planner/worker cost split natural. … Run your orchestrator/dispatcher profile on a frontier model and point worker profiles at inexpensive models."
  Tier: Verified

- **F23 — Orchestrator worker-lane shape = profile with kanban tools but no implementation tools; external CLI lanes are not a paved path.**
  Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-worker-lanes (official-docs)
  Quote: "an orchestrator is a Hermes profile whose toolset includes kanban but excludes terminal / file / code / web for implementation. … Wiring a non-Hermes CLI tool … as a kanban worker lane is not yet a paved path."
  Tier: Verified

- **F24 — Goal-mode cards for open-ended work, one-shot cards otherwise.**
  Source: /docs/user-guide/features/kanban (official-docs)
  Quote: "Use it for open-ended, multi-step, or 'keep going until X is true' cards. Skip it for cheap one-shot work — the per-turn judge overhead isn't worth it"
  Tier: Verified

## F25–F31. delegate_task boundaries (ephemeral, process-local, toolset-inheriting)

- **F25 — Children are ephemeral, context-isolated, summary-only.**
  Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation (official-docs)
  Quote: "The delegate_task tool spawns child AIAgent instances with isolated context, inherited tool access, and their own terminal sessions … only its final summary enters the parent's context."
  Tier: Verified

- **F26 — Subagents know nothing of the parent conversation (the context contract of the mechanism).**
  Source: /docs/user-guide/features/delegation (official-docs)
  Quote: "Subagents start with a completely fresh conversation. They have zero knowledge of the parent's conversation history"
  Tier: Verified

- **F27 — Delegation is not durable; docs redirect durable work to cron / background terminal.**
  Source: /docs/guides/delegation-patterns + /docs/user-guide/features/delegation (official-docs)
  Quote: "Top-level delegation is asynchronous but still process-local." / "For durable execution that must survive session closure or process restart, use: cronjob (action=create) … terminal(background=True, notify_on_complete=True)"
  Tier: Verified

- **F28 — Docs give an explicit anti-delegation list (single tool call, mechanical work, interactive tasks).**
  Source: /docs/guides/delegation-patterns (official-docs)
  Quote: "Mechanical multi-step work with logic between steps → execute_code … Tasks needing user interaction → subagents can't use clarify … Quick file edits → do them directly"
  Tier: Verified

- **F29 — Delegation vs execute_code rule of thumb (reasoning vs mechanical).**
  Source: /docs/user-guide/features/delegation (official-docs)
  Quote: "Use delegate_task when the subtask requires reasoning, judgment, or multi-step problem solving. Use execute_code when you need mechanical data processing or scripted workflows."
  Tier: Verified

- **F30 — Children inherit and cannot widen the parent's tool surface; leaf children lose memory/scheduling/messaging tools (profile equipping ≠ delegation).**
  Source: /docs/user-guide/features/delegation (official-docs)
  Quote: "Subagents inherit the parent's enabled toolsets; the model cannot select or widen them per call … Leaf subagents cannot call: delegate_task, clarify, memory, send_message, cronjob."
  Tier: Verified

- **F31 — Parallel-children repo collisions are solved inside delegation by opt-in worktree isolation (same knob family as the git-worktrees page).**
  Source: /docs/user-guide/features/delegation + /docs/user-guide/git-worktrees (official-docs)
  Quote: "Set delegation.worktree_isolation: true to give each child its own git worktree" / "If you run multiple agents in the same checkout, their changes can interfere with each other … With worktrees, each agent gets: Its own branch and working directory"
  Tier: Verified

## F32–F38. Cron boundaries (per-profile ownership, no-agent, heartbeat, self-monitoring)

- **F32 — Cron jobs are profile-local artifacts: own store, own executions.db, owning profile's secret scope.**
  Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/cron (official-docs)
  Quote: "the cron store (~/.hermes/cron/, or the profile's own cron/ directory)" / "the profile-local ~/.hermes/cron/executions.db" / "resolved through that profile's secret scope, never the launch profile's process environment"
  Tier: Verified

- **F33 — A named profile's cron is served by its scheduler host (multiplexer) with its own heartbeat health.**
  Source: /docs/user-guide/features/cron (official-docs)
  Quote: "For a named profile served by the default-profile multiplexer, hermes cron status names that scheduler host and reports the named profile's own heartbeat health."
  Tier: Verified

- **F34 — Per-profile/Job model cost control is a documented cron feature: per-job pin → cron.model → main model.**
  Source: /docs/user-guide/features/cron (official-docs)
  Quote: "Resolution at fire time is: per-job pin → cron.model in config.yaml → the main agent model from hermes model." (plus: "a cron-fleet default: every unpinned job runs on this model, independent of your chat model")
  Tier: Verified

- **F35 — Cron jobs cannot self-replicate.**
  Source: /docs/user-guide/features/cron (official-docs)
  Quote: "Hermes disables cron management tools inside cron executions to prevent runaway scheduling loops."
  Tier: Verified

- **F36 — no-agent vs LLM cron boundary: reasoning-free stdout-as-message → script job; anything decided → LLM job.**
  Source: https://hermes-agent.nousresearch.com/docs/guides/cron-script-only (official-docs)
  Quote: "Use a normal (LLM-driven) cron job when you need the agent to decide what to say … The no-agent path is for cases where the script's stdout already IS the message."
  Tier: Verified

- **F37 — Self-monitoring boundary: cron inside Hermes must not monitor Hermes itself; use OS cron + webhook.**
  Source: /docs/guides/cron-script-only (official-docs)
  Quote: "OS cron + curl to a webhook subscription | Your script on the OS schedule | When Hermes might be unhealthy (the thing you're monitoring)"
  Tier: Verified

- **F38 — Heartbeat vs cron: in-thread context recurrence vs standalone durable jobs.**
  Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/heartbeat (official-docs)
  Quote: "Rule of thumb: if the recurring prompt needs the conversation's context, use /heartbeat. If it's a self-contained job, use cron." (table: heartbeat "Runs in This conversation — full context"; cron "A fresh isolated session per tick")
  Tier: Verified

## F39–F41. MoA boundary

- **F39 — MoA is positioned as a model-level mechanism (virtual provider), not an agent/profile mechanism.**
  Source: https://hermes-agent.nousresearch.com/docs/user-guide/features/mixture-of-agents (official-docs)
  Quote: "Mixture of Agents is a virtual model provider. Each named MoA preset appears as a selectable model under the moa provider."
  Tier: Verified

- **F40 — MoA's workload: hard single-session tasks that still need the normal agent loop (vs multi-agent fan-out elsewhere).**
  Source: /docs/user-guide/features/mixture-of-agents (official-docs)
  Quote: "Use MoA when a hard task benefits from multiple model perspectives but still needs Hermes' normal agent loop: tool calls, follow-up iterations, interrupts, transcript persistence, and the same session context as any other message."
  Tier: Verified

- **F41 — MoA billing sits on the aggregator's provider (a per-profile model-selection cost consideration, like profile model settings).**
  Source: /docs/user-guide/features/mixture-of-agents (official-docs)
  Quote: "The aggregator is billed for the whole run: it runs every step of the tool loop, so almost all of a preset's cost lands on the aggregator's provider."
  Tier: Verified

## F42. Spawned-process vs delegate_task (adjacent boundary, weaker source)

- **F42 — The official hermes-agent skill positions spawned `hermes` processes for long/interactive missions and delegate_task for quick parallel subtasks (quick subtasks → delegate; hours/days + interactivity → separate process; for scheduled work use cron instead of spawning). No page among the 12 lane URLs carries this comparison.**
  Source: skill `autonomous-ai-agents/hermes-agent` "Spawning Additional Hermes Instances" (reference — shipped skill, not a docs page)
  Quote: "Prefer delegate_task for quick subtasks — less overhead than spawning a full process … For scheduled tasks, use the cronjob tool instead of spawning"
  Tier: Plausible

## Searched, found nothing (evidence of absence)

- No web_search bursts were run; the 12 starting URLs + the profiles terminology anchor answered SQ3 (docs-first gate). Queries held in reserve and NOT needed: "hermes bot mode vs profile reddit", "hermes profile vs subagent vs cron which to use blog", "hermes mixture of agents vs kanban".
- **No single official "choose your mechanism" comparison page** covering all six mechanisms; the boundaries exist only as four pairwise vs-tables (kanban↔delegate_task, delegation↔execute_code, heartbeat↔cron, no-agent↔LLM↔OS cron) plus the profiles#profiles-agents-and-bots terminology list. Source types checked: the 12 official-docs pages.
- **MoA page says nothing about when NOT to use MoA vs multi-agent mechanisms** — its positioning is purely intra-session model choice; absence recorded (official-docs).
- **No normative statement on which profile should own scheduled automations** — docs establish only that jobs are profile-local artifacts (store, executions.db, secret scope, scheduler host). "Run automations on the profile whose identity/credentials/target they use" is our inference, tier Plausible.
- **No official table comparing spawned `hermes` processes vs delegate_task vs profiles** among the lane pages (only the shipped skill; see F42).
- **Heartbeat is session-scoped, not profile-scoped; docs never tie heartbeats to profile strategy** — absence noted (official-docs, heartbeat page).

Sub-question status from this lane's view: answered
