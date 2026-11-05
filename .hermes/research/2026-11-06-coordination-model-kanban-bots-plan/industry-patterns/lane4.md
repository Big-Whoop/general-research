# Lane 4 — Industry patterns for coordinating LLM agent teams (A: plan-first → queue; B: coordinator on the board; C: chat-swarm)

Date: 2026-11-06. Scope: sources OUTSIDE Hermes Agent. Every quote below was fetched and verified verbatim against the saved page text (ledger: `lane4-ledger` in scratch; quote list rendered in `## Sources` at the end). Tier legend: **Verified** = authoritative source on this exact subject; **Plausible** = sound general evidence, not demonstrated on our exact setting; **Speculative** = inference.

Mapping used throughout (from the shared brief):
- **A = plan-first in one human-facing session, hand the plan to a queue/board of workers.** Industry equivalents: Claude Code plan mode → subagents/teammates with shared task list; spec-kit `spec.md → plan.md → tasks.md`; CrewAI `planning=True` + sequential process; Codex cloud tasks (human writes task, worker runs in sandbox, human reviews PR).
- **B = persistent coordinator agent living on the queue/board, talks to the human only when blocked.** Industry equivalents: Anthropic orchestrator-workers / lead researcher; Magentic-One Orchestrator with task ledger + progress ledger + stall counter; CrewAI hierarchical `manager_agent`; OpenAI "manager pattern"; LangChain "subagents" pattern; Claude Code agent-team lead.
- **C = swarm of chat-bots messaging each other (group-chat / conversational orchestration).** Industry equivalents: AutoGen `SelectorGroupChat` / `RoundRobinGroupChat`; OpenAI "decentralized/handoffs"; LangChain "handoffs"/swarm; ChatDev/CAMEL-style role chats; Claude Code teammates messaging each other via mailbox.

---

## 1. Findings (claim · source · quote · tier)

### F1. Orchestrator-workers is the industry-default topology for coding-style work whose subtasks are not known up front; the orchestrator *decomposes, delegates and synthesizes* — it is not described as an executor.
- Source: Anthropic, "Building effective agents" (vendor engineering guide).[1]
- Quote: "In the orchestrator-workers workflow, a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results."[1] "This workflow is well-suited for complex tasks where you can’t predict the subtasks needed"[1]
- Tier: **Verified** (pattern definition). Note: the post is prefaced with a Dec-2024 → "Managed Agents" update banner, but the pattern taxonomy is unchanged.

### F2. Multi-agent costs ~15× the tokens of a chat (agents ~4×); it is only economic when task value justifies it, and coding is explicitly called out as *less* parallelizable than research.
- Source: Anthropic, "How we built our multi-agent research system" (vendor engineering post).[2]
- Quote: "agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats."[2] "most coding tasks involve fewer truly parallelizable tasks than research, and LLM agents are not yet great at coordinating and delegating to other agents in real time."[2]
- Tier: **Verified** (first-party production data for pattern B in research; **Plausible** when transferred to coding/kanban).

### F3. The plan is made by the lead, then *persisted outside the context window* (memory/file) before workers are spawned; subagents write artifacts to a filesystem and pass back references, to avoid the "game of telephone".
- Source: Anthropic multi-agent research post.[2]
- Quote: "The LeadResearcher begins by thinking through the approach and saving its plan to Memory to persist the context, since if the context window exceeds 200,000 tokens it will be truncated and it is important to retain the plan."[2] "Subagents call tools to store their work in external systems, then pass lightweight references back to the coordinator."[2]
- Tier: **Verified** for "where should the plan be persisted" (answer: outside the chat transcript, in durable memory/files, with artifacts not relayed through the coordinator).

### F4. The hand-off contract per worker must contain objective, output format, tool/source guidance and boundaries; vague one-liners cause duplicate work and gaps. Effort must be scaled by explicit rules, otherwise the lead over-spawns.
- Source: Anthropic multi-agent research post.[2]
- Quote: "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries. Without detailed task descriptions, agents duplicate work, leave gaps, or fail to find necessary information."[2] "Early agents made errors like spawning 50 subagents for simple queries, scouring the web endlessly for nonexistent sources, and distracting each other with excessive updates."[2]
- Tier: **Verified** (directly supports "contract cards" and "scale rules" in the pre-card planning phase).

### F5. Synchronous lead→worker execution is a known bottleneck (lead can't steer, workers can't coordinate, whole system blocks on one slow worker) — i.e. the "coordinator waits in chat" model is the documented weakness of pattern B-in-a-session.
- Source: Anthropic multi-agent research post.[2]
- Quote: "Currently, our lead agents execute subagents synchronously, waiting for each set of subagents to complete before proceeding. This simplifies coordination, but creates bottlenecks in the information flow between agents."[2]
- Tier: **Verified** (motivates an asynchronous board as the state carrier rather than a blocking chat session).

### F6. Claude Code's lighter primitive (subagent) returns *only a summary* to the caller; its heavier primitive (agent team) shares a task list + mailbox and costs "significantly more tokens" (~7× in plan mode), and is explicitly *not* recommended for sequential, same-file, or dependency-heavy work.
- Source: Claude Code docs, "Subagents" and "Agent teams"; "Costs".[3][4][27]
- Quote: "Use one when a side task would flood your main conversation with search results, logs, or file contents you won’t reference again: the subagent does that work in its own context and returns only the summary."[3] "Agent teams add coordination overhead and use significantly more tokens than a single session. They work best when teammates can operate independently. For sequential tasks, same-file edits, or work with many dependencies, a single session or subagents are more effective."[4] "Agent teams use approximately 7x more tokens than standard sessions when teammates run in plan mode, because each teammate maintains its own context window and runs as a separate Claude instance."[27]
- Tier: **Verified** (official docs; the agent-teams feature is marked experimental).

### F7. In Claude Code agent teams the shared task list IS the board: lead creates tasks, tasks have pending/in-progress/completed + dependencies, workers self-claim via file locking; documented failure: "task status can lag" (workers forget to mark done → dependents block).
- Source: Claude Code "Agent teams" docs.[4]
- Quote: "Task claiming uses file locking to prevent race conditions when multiple teammates try to claim the same task simultaneously."[4] "Task status can lag: teammates sometimes fail to mark tasks as completed, which blocks dependent tasks."[4]
- Tier: **Verified** (independent vendor evidence that board-state drift is a generic failure, not a Hermes-only bug).

### F8. "The orchestrator should not execute" is documented as a *drift to be corrected*, not as an automatic property: the lead sometimes starts implementing itself; the documented fix is to tell it to wait.
- Source: Claude Code "Agent teams" troubleshooting.[4]
- Quote: "Sometimes the lead starts implementing tasks itself instead of waiting for teammates."[4]
- Tier: **Verified**. Corroborated by AutoGen's canonical planner prompt (F14): "You only plan and delegate tasks - you do not execute them yourself."[13] and by Magentic-One's analogy (F12) where the Orchestrator "cannot directly act".[17]

### F9. Vendor sizing guidance for pattern B: 3–5 workers, 5–6 tasks per worker, each worker owns disjoint files, human keeps monitoring; permission requests bubble to the lead and are the main friction.
- Source: Claude Code "Agent teams" best practices.[4]
- Quote: "Start with 3-5 teammates for most workflows."[4] "Two teammates editing the same file leads to overwrites. Break the work so each teammate owns a different set of files."[4] "Letting a team run unattended for too long increases the risk of wasted effort."[4] "Teammate permission requests bubble up to the lead, which can create friction."[4]
- Tier: **Verified**.

### F10. Plan mode = research-and-propose with edits blocked until human approval; the plan is a human-editable artifact (Ctrl+G opens it in an editor) — i.e. the plan is made in the human-facing session and approved there (pattern A's first half).
- Source: Claude Code "Permission modes".[6]
- Quote: "Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source."[6] "Press Ctrl+G to open the proposed plan in your default text editor and edit it directly before Claude proceeds."[6]
- Tier: **Verified**. Also: a teammate spawned while the lead is in plan mode plans first and sends a plan-approval request to the lead (lead-gated, not human-gated by default).[4]

### F11. OpenAI's guide: maximize a single agent first; the **manager pattern** is for when exactly one agent should control execution *and* own the user channel; the **decentralized/handoff pattern** is for when each agent may take over the user conversation; human escalation is triggered by retry thresholds and high-risk actions.
- Source: OpenAI, "A practical guide to building agents" (vendor guide) + Agents SDK docs.[16][8]
- Quote: "Our general recommendation is to maximize a single agent’s capabilities first. More agents can provide intuitive separation of concepts, but can introduce additional complexity and overhead, so often a single agent with tools is sufficient."[16] Manager: "This pattern is ideal for workflows where you only want one agent to control workflow execution and have access to the user."[16] Decentralized: "This is optimal when you don’t need a single agent maintaining central control or synthesis—instead allowing each agent to take over execution and interact with the user as needed."[16] "Exceeding failure thresholds: Set limits on agent retries or actions. If the agent exceeds these limits (e.g., fails to understand customer intent after multiple attempts), escalate to human intervention."[16] SDK: "Use agents as tools when a specialist should help with a bounded subtask but should not take over the user-facing conversation. Use handoffs when routing itself is part of the workflow and you want the chosen specialist to own the remainder of the current turn."[8] "orchestrating via code makes tasks more deterministic and predictable, in terms of speed, cost and performance."[8]
- Tier: **Verified**. Interpretation: handoffs (pattern C) are a *customer-service* routing idiom where the human is in the loop every turn; for engineering work, OpenAI's own product (Codex cloud, F18) uses pattern A.

### F12. Magentic-One is the reference implementation of pattern B: orchestrator keeps a **Task Ledger** (facts, guesses, plan; outer loop) and a **Progress Ledger** (5 questions per step; inner loop), with a stall counter (≤2) that triggers re-planning; the orchestrator relays instructions and does not act directly.
- Source: Microsoft Research blog + arXiv 2411.04468.[9][17]
- Quote: "The Orchestrator begins by creating a plan to tackle the task, gathering needed facts and educated guesses in a Task Ledger that is maintained. At each step of its plan, the Orchestrator creates a Progress Ledger where it self-reflects on task progress and checks whether the task is completed."[9] "The Orchestrator also maintains a counter for how long the team has been stuck or stalled. If a loop is detected, or there is a lack of forward progress, the counter is incremented."[17] "this configuration resembles a telephone technical support scenario where the Orchestrator knows what to do, but cannot directly act on the web page. Instead it relays instructions, and relies on the WebSurfer to carry out actions and report observations."[17]
- Tier: **Verified** (paper + vendor blog).

### F13. Direct ablation of B vs C: replacing the ledger orchestrator with AutoGen's plain GroupChat speaker-selection (pattern C) removes planning/progress/loop-detection and costs 31% on GAIA.
- Source: arXiv 2411.04468 §5.3.[17]
- Quote: "This baseline orchestrator simply decides which agent should speak next during task execution, eliminating both ledgers, planning, progress tracking, loop detection, and explicit instructions to other agents."[17] "We find that the Orchestrator’s ledgers are important to Magentic-One’s performance: without the full ledgers, performance drops by 31%."[17]
- Tier: **Verified** (the only controlled head-to-head of ledger-orchestrator vs group-chat found; reliability axis, not token axis).

### F14. AutoGen group chat = every message broadcast to all participants, LLM picks next speaker from shared context; the docs' own planner prompt forbids the planner from executing; without a termination condition the chat runs forever (docs cap at 25 messages "to avoid infinite loop").
- Source: AutoGen SelectorGroupChat guide + teams API reference.[13][25]
- Quote: "implements a team where participants take turns broadcasting messages to all other members. A generative model (e.g., an LLM) selects the next speaker based on the shared context"[13] "You only plan and delegate tasks - you do not execute them yourself."[13] "Without a termination condition, the group chat will run indefinitely."[25]
- Tier: **Verified**. Cost implication (Speculative but structural): broadcast means every agent re-reads the whole transcript each turn — token cost grows ~quadratically with message count, which is exactly the "~10 Pings/day, chat lost connection" symptom class.

### F15. MAST taxonomy (1,600+ traces, 7 frameworks): 14 failure modes in 3 classes — system design/spec, inter-agent misalignment, task verification. Fixing role spec alone gave +9.4%; verifier presence helps but shallow verifiers are common; "fail to ask for clarification" and "task derailment" are mid-frequency conversational failures.
- Source: Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" arXiv 2503.13657 v3 (paper).[12]
- Quote: "This process identifies 14 unique modes, clustered into 3 categories: (i) system design issues, (ii) inter-agent misalignment, and (iii) task verification."[12] "We demonstrate that a straightforward system workflow adjustment ensuring the CEO had the final say contributed to a +9.4% increase in overall task success rate."[12] "Multi-Level Verification is Needed. Current verifier implementations are often insufficient; sole reliance on final-stage, low-level checks is inadequate."[12] "Systems with explicit verifiers like MetaGPT and ChatDev generally show fewer total failures"[12] "proceeding with wrong assumptions instead of seeking clarification (FM-2.2, 6.80%), task derailment (FM-2.3, 7.40%)"[12]
- Tier: **Verified** (paper). Reading for our question: a single final authority (CEO/coordinator "has the final say") and an explicit multi-level verifier are the two interventions with measured effect; both are structural properties of B, absent by default in C.

### F16. Controlled scaling study (260 configs, 6 benchmarks): token overhead vs single agent — independent 58%, decentralized 263%, centralized 285%, hybrid 515% (1.6–6.2×); centralized verification reduces error propagation; on SWE-bench Verified *all* multi-agent variants are slightly worse than single-agent; centralized orchestrator is a bottleneck.
- Source: Kim et al., "Towards a Science of Scaling Agent Systems", arXiv 2512.08296 v3 (paper).[21]
- Quote: "Multi-agent architectures incur substantial overhead: independent (58%), centralized (285%), decentralized (263%), and hybrid (515%)"[21] "architectures without centralized verification tend to propagate errors more than those with centralized coordination."[21] "SWE-bench Verified shows slight degradation across all MAS architectures (from -15% to -2%), consistent with high single-agent baselines"[21] "This design stabilizes reasoning but creates a bottleneck at the orchestrator."[21] "they incur an unavoidable coordination tax in which the global context must be compressed into inter-agent messages."[21] "Independent MAS shows no error correction (+4.6%"[21]
- Tier: **Verified** as a paper result; **Plausible** transfer (their "decentralized" = debate rounds, not a kanban; their "centralized" = orchestrator re-reads all sub-agent output). Key numbers for the table: B ≈ C in raw token overhead (285% vs 263%), but B wins on error containment; both lose to a single strong agent on SWE-bench-class coding.

### F17. LangChain's own call-count accounting: handoffs (swarm) run sequentially and accumulate conversation history; subagents (orchestrator) cost one extra call per hop but isolate context and processed 67% fewer tokens in the multi-domain case.
- Source: LangChain multi-agent docs.[15]
- Quote: "Handoffs executes sequentially—can’t research all three languages in parallel. Growing conversation history adds overhead."[15] "Subagents adds one extra call because results flow back through the main agent—this overhead provides centralized control."[15] "Subagents processes 67% fewer tokens overall due to context isolation."[15]
- Tier: **Verified** (vendor doc micro-benchmark, toy scale). Their selection table: subagents ⭐⭐⭐⭐⭐ for parallelization but ⭐ for direct user interaction; handoffs the inverse.

### F18. Codex cloud = pattern A operationalized: human writes the task, each task runs in its own sandboxed workspace asynchronously, human reviews diff/test results and opens the PR. No coordinator agent; the human is the board.
- Source: OpenAI Codex Cloud docs.[24]
- Quote: "Each task has its own workspace and can keep working while your computer is asleep."[24] "Inspect changed files and check results, request follow-up changes, and commit or open a pull request when you're ready."[24]
- Tier: **Verified**.

### F19. spec-kit: the spec and plan are versioned repo files; `/speckit.tasks` derives `tasks.md` from `plan.md`, marks parallel-safe tasks `[P]`, and the file is "ready for execution by a Task agent" — the plan file *is* the hand-off artifact and is team-reviewed via branches.
- Source: GitHub spec-kit `spec-driven.md`.[14]
- Quote: "Specifications don't serve code—code serves specifications."[14] "Marks independent tasks [P] and outlines safe parallel groups"[14] "Writes tasks.md in the feature directory, ready for execution by a Task agent"[14] "This is supportive of a team process, where team-reviewed specifications are expressed and versioned, created in branches, and merged."[14]
- Tier: **Verified**.

### F20. CrewAI: default is sequential (pattern A, pre-ordered task list, output of one task feeds the next); hierarchical adds a manager that delegates *and validates*; a separate `CrewPlanner` writes the plan for every task before the run; agent-to-agent delegation is off by default.
- Source: CrewAI docs (processes, hierarchical, planning).[10][18][19]
- Quote: "adopting a hierarchical approach allows for a clear hierarchy in task management, where a ‘manager’ agent coordinates the workflow, delegates tasks, and validates outcomes for streamlined and effective execution."[10] "Delegation Control: Delegation is now disabled by default to give users explicit control."[10] "before the crew runs, a CrewPlanner writes a plan for every task and adds it to each task description."[18]
- Tier: **Verified**.

### F21. MetaGPT: SOP-encoded assembly line with role-typed structured artifacts (PRD → design → tasks → code) outperforms "chat-based multi-agent systems" by letting roles verify intermediate results — the paper's own framing is anti-pattern-C.
- Source: arXiv 2308.00352 abstract.[22]
- Quote: "MetaGPT encodes Standardized Operating Procedures (SOPs) into prompt sequences for more streamlined workflows, thus allowing agents with human-like domain expertise to verify intermediate results and reduce errors."[22] "MetaGPT generates more coherent solutions than previous chat-based multi-agent systems."[22]
- Tier: **Verified** (claim as stated by authors; benchmark details not re-checked here).

### F22. SWE-agent / OpenHands are single-agent loops (one agent, one sandbox, one ACI); they are the *worker* primitive, not a coordination model; SWE-agent is now maintenance-only in favour of mini-swe-agent.
- Source: swe-agent.com architecture page.[26] (OpenHands backend page fetched but body is image-only — nothing quotable.)
- Tier: **Verified** for "single-agent loop"; nothing on multi-agent coordination found in these docs.

---

## 2. Pattern comparison table (A / B / C)

| Axis | **A. Plan-first in human chat → queue/board of workers** | **B. Persistent coordinator ON the board, talks to human only when blocked** | **C. Chat-swarm / group chat** |
|---|---|---|---|
| **Token cost** | Lowest marginal: plan once in chat; each worker = isolated context + summary back (subagent model[3]); Codex cloud = one sandbox per task.[24] LangChain: isolation → 67% fewer tokens than accumulating-history patterns.[15] No standing coordinator burn. | Orchestrator re-reads every result: Kim et al. 285% overhead vs single agent[21]; Anthropic ~15× chat[2]; Claude agent teams ~7×.[27] Coordinator context is the bottleneck ("creates a bottleneck at the orchestrator"[21]). | Broadcast to all participants each turn[13]; "growing conversation history adds overhead"[15]; Kim: decentralized 263%, hybrid (orchestrator + peer chat) 515%.[21] Runs forever without a termination rule.[25] |
| **Speed / latency** | Workers run async in parallel ("can keep working while your computer is asleep"[24]); human review is the only serialization point. | Fast when async; documented slow mode is the synchronous lead that "waits for each set of subagents to complete before proceeding"[2]. Dispatch-tick polling adds latency per hop. | Sequential by construction ("Handoffs executes sequentially—can’t research all three languages in parallel"[15]); speaker-selection LLM call per turn. |
| **Reliability** | Plan is a reviewed, versioned artifact (spec-kit tasks.md[14]; plan mode approval[6]); failure surface = per-card worker. No in-flight re-planning unless human re-plans. | Best error containment: "architectures without centralized verification tend to propagate errors more than those with centralized coordination"[21]; ledgers + stall counter = +31% vs group chat.[17] Known drifts: lead starts implementing itself[4]; task status lags[4]. | Worst measured: GroupChat baseline −31% vs ledger orchestrator[17]; MAST FC2 failures (wrong assumptions, derailment, withholding) are conversational[12]; MetaGPT/ChatDev authors moved to SOP pipelines *because* chat-based MAS were incoherent.[22] Needs an authority with "the final say" (+9.4%).[12] |
| **Human-interaction fit** | Highest: human is the planner and the reviewer; one approval gate before work, one PR review after.[6][24] Questions are answered during planning, not mid-flight. | Medium: human sees only blocked/needs-input escalations (OpenAI: "Exceeding failure thresholds … escalate to human intervention"[16]); permission prompts "bubble up to the lead"[4]; must keep monitoring ("Letting a team run unattended for too long increases the risk of wasted effort"[4]). | High for *customer-service routing* (each agent "interact[s] with the user as needed"[16]), low for engineering: human is one voice in a broadcast channel; no single owner of the answer. |
| **Where the plan lives** | Repo file (`plan.md`/`tasks.md`[14]) or approved plan-mode plan[6]; board rows are derived from it. | Coordinator's Task Ledger / memory ("saving its plan to Memory to persist the context"[2]; Magentic-One task ledger[9]) — must be externalized or it dies with the context. | In the transcript (shared context[13]) — lossy, grows, not reviewable. |
| **Who executes** | Workers only; human never executes; no coordinator process. | Workers; orchestrator "cannot directly act … relays instructions"[17]; must be explicitly told not to implement.[4][13] | Whoever is selected next speaker — role boundaries erode (MAST FM-1.2 "disobey role specification").[12] |
| **When recommended (per sources)** | Default for coding: "maximize a single agent’s capabilities first"[16]; "For sequential tasks, same-file edits, or work with many dependencies, a single session or subagents are more effective"[4]; SWE-bench: every MAS variant ≤ single agent.[21] Use when subtasks can be enumerated up front and the human wants a review gate. | When subtasks "can’t [be] predict[ed]" up front[1] and work is breadth-first/parallel with high task value (research, parallel review, independent modules[4]); when re-planning on stall is needed (Magentic-One[17]). | "Complex work requiring discussion and collaboration" (debate, competing hypotheses)[4]; customer-service triage where a specialist should own the user turn.[16][8] Not recommended by any source for executing a dependent coding plan. |

**Net reading for a kanban + bots setting:** A for the plan and the human gate; B's *mechanics* (ledger = board, stall counter = retry-then-ask, verifier card) for the run; C only as the *human-facing escalation channel*, never as the state carrier.

---

## 3. Roles most sources agree on

| Role | Who names it | Decisive? |
|---|---|---|
| **Planner / spec author** (produces plan + task list before execution) | Claude plan mode[6]; Anthropic lead "saving its plan"[2]; Magentic-One outer loop / task ledger[9]; CrewAI `CrewPlanner`[18]; spec-kit `/speckit.plan`, `/speckit.tasks`[14]; AutoGen PlanningAgent[13]; MetaGPT PM/Architect[22] | **Yes** — every source. In A it is the human-facing session; in B it is the orchestrator's outer loop. |
| **Coordinator / router** (assigns, tracks progress, re-plans on stall; does not execute) | Anthropic orchestrator[1]; Magentic-One Orchestrator + progress ledger + stall counter[17]; OpenAI manager[16]; CrewAI manager[10]; LangChain subagents main agent[15]; Claude team lead[4] | Yes for B; in A the *board dispatcher + human* replace it. All sources: must **not** execute.[4][13][17] |
| **Worker** (isolated context, one task, returns result/artifact reference) | Subagents[3]; teammates[4]; Codex task sandbox[24]; SWE-agent/OpenHands loop[26]; Magentic-One Coder/WebSurfer[9] | Yes — universal. Contract: objective, output format, tools, boundaries.[2] Own disjoint files.[4] |
| **Reviewer / verifier** (explicit, multi-level, not just "does it compile") | MAST Insight 3[12]; Kim "centralized verification"[21]; CrewAI manager "validates outcomes"[10]; MetaGPT role verification[22]; Claude `TaskCompleted` hook gate[4]; OpenAI evaluator loop[8] | **Yes** — the one role whose *absence* is measured as a failure class (FC3, 23.5% of failures across 3 modes).[12] |
| **Human gate** (approve plan; receive escalations on retry-threshold/high-risk; review PR) | Plan-mode approval[6]; Codex PR review[24]; OpenAI human-intervention triggers[16]; Claude "monitor and steer"[4]; spec-kit team-reviewed specs[14] | Yes — placed at **plan approval** and **merge**, plus **blocked** escalations; no source puts the human inside the worker loop. |
| **Final authority** (one agent/human "has the final say" on done) | MAST ChatDev intervention (+9.4%)[12]; OpenAI manager "control workflow execution"[16] | Yes — a corollary: exactly one owner of "complete". |

Roles that appear in only one or two sources and are *not* consensus: memory/ledger agent (Magentic-One folds it into the orchestrator), devil's-advocate / debate agents (Claude teams, Kim "decentralized"), separate "router" node (LangChain).

---

## 4. Direct answers to the lane questions

1. **Which roles are decisive?** Planner, worker, verifier, human gate (plan-approval + merge). Coordinator is decisive only in B; in A it is replaced by a dispatcher + the plan file. Verifier is the most under-implemented and the most measured (F15, F16).
2. **Where should the plan be made and persisted?** Made in the human-facing session (plan mode / spec dialogue — F10, F19) or by the orchestrator's outer loop (F12); persisted **outside any context window** as a file or ledger (F3, F19). Nobody recommends the chat transcript as the plan store.
3. **Chat-swarm vs orchestrator-worker evidence?** Reliability: ledger-orchestrator beats group chat by 31% (F13); centralized verification contains errors (F16); SOP pipelines beat chat MAS (F21); MAST conversational failure modes (F15). Cost: roughly equal raw overhead (285% vs 263%) but swarm history grows per turn and runs sequentially (F16, F17); hybrid (orchestrator **plus** peer chat) is worst at 515%. Speed: swarm is sequential by construction (F17); orchestrator is slow only if synchronous (F5). Against both: on SWE-bench-class coding, single agent ≥ any MAS (F16), and Anthropic says coding is poorly parallelizable (F2).
4. **"The orchestrator should not execute"?** Stated as prompt rule (AutoGen F14), as architecture (Magentic-One F12), and as a *drift to correct* (Claude teams F8). The reason given is role-specification failure (MAST FM-1.2) and lead-context bloat (F6/F16 bottleneck).
5. **Plan files / specs as the hand-off artifact?** Yes: spec-kit `tasks.md` with `[P]` parallel markers (F19), Anthropic plan-in-memory + artifact references (F3), CrewAI per-task plan injected into task description (F20), Claude plan editable before approval (F10). Consensus: the artifact must carry per-task objective/output/boundaries (F4), and workers return references to artifacts, not prose through the coordinator (F3).

---

## 5. Searched, found nothing

- `OpenAI "A practical guide to building agents" PDF` — the CDN PDF failed to scrape (HTTP 500 from extractor); used the HTML version on openai.com instead (same text). Source type: vendor guide.
- `doi.org/10.3390/fi18060326` (Future Internet survey "LLM-Based Multi-Agent Orchestration … token-cost profiles") — fetch failed (extractor error); not cited. Source type: journal survey.
- `OpenHands docs multi-agent delegation / orchestrator` — backend architecture page is image-only; no textual coordination guidance found. Source type: official docs.
- `Codex cloud docs "parallel" "delegate"` — page does not describe agent-to-agent coordination at all; only human→task→review. Source type: official docs.
- `AutoGen docs "known failure modes" group chat` — official docs only document the infinite-loop/termination hazard; no vendor-published failure taxonomy for GroupChat beyond that. Magentic-One ablation is the only quantitative B-vs-C evidence found. Source type: official docs + paper.
- `token/latency comparison orchestrator-worker vs conversational on coding tasks specifically` — only Kim et al. (SWE-bench Verified: all MAS ≤ single agent, overhead by topology) and LangChain's toy call counts; no study measuring a kanban-style asynchronous board vs chat. Source type: paper/vendor docs.
- `Claude Code "delegate mode"` (lead-only-coordinates toggle) — not present in the fetched agent-teams page text; the page instead documents correcting the lead with a prompt (F8). Source type: official docs.
- `MetaGPT full paper SOP figures` — only the abstract was fetched; the "more coherent than chat-based MAS" claim is quoted from the abstract, not re-verified against the result tables. Source type: paper.

---

## Sources
[1] https://www.anthropic.com/engineering/building-effective-agents
[2] https://www.anthropic.com/engineering/multi-agent-research-system
[3] https://code.claude.com/docs/en/sub-agents
[4] https://code.claude.com/docs/en/agent-teams
[6] https://code.claude.com/docs/en/permission-modes
[8] https://openai.github.io/openai-agents-python/multi_agent
[9] https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks
[10] https://docs.crewai.com/en/learn/hierarchical-process
[12] https://arxiv.org/html/2503.13657v3
[13] https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/selector-group-chat.html
[14] https://github.com/github/spec-kit/blob/main/spec-driven.md
[15] https://docs.langchain.com/oss/python/langchain/multi-agent
[16] https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents
[17] https://arxiv.org/html/2411.04468v1
[18] https://docs.crewai.com/en/concepts/planning
[19] https://docs.crewai.com/en/concepts/processes
[21] https://arxiv.org/html/2512.08296v3
[22] https://arxiv.org/abs/2308.00352
[24] https://developers.openai.com/codex/cloud
[25] https://microsoft.github.io/autogen/stable//reference/python/autogen_agentchat.teams.html
[26] https://swe-agent.com/latest/background/architecture
[27] https://code.claude.com/docs/en/costs

Sub-question status from this lane's view: answered
