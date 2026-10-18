# Session spawning & multi-session orchestration (surface map)

Verified against official docs + main-branch source during a 5-lane deep research. This surface is evolving (open roadmap work on cross-session messaging) — re-verify specifics against current docs/source before building on them.

## Target pattern: "spawn with report"

Agent in session A creates session B with task + context; B runs independently; B's result reports back into A. (Claude Desktop analog: "nested sessions" / task chips — agent-spawned visible session with parent link + own worktree.)

## Verified negatives (do not re-research from scratch)

- No built-in agent tool creates a session. The core tool registry was scanned; the agent's only spawn surfaces are `delegate_task` (subagent) and, for plugins, `ctx.subagent_lifecycle.launch`.
- No desktop UI for "new session with initial prompt" or fork-from-session. Cmd/Ctrl+T/N create empty sessions only. Fork exists only at gateway level: `session.branch` RPC, `POST /api/sessions/{id}/fork`, CLI `/branch`.
- Subagent sessions are hidden from session pickers by default (`_delegate_from` marker set at creation). Profile config `sessions.show_subagents` re-admits them to the session list.

## Mechanism map

| Mechanism | Agent-initiated | New session | Visible in session list | Context transfer | Report-back to A |
|---|---|---|---|---|---|
| `delegate_task` / async_delegation | ✅ model tool | ✅ (source `subagent`) | ❌ Subagents frame; ✅ with `sessions.show_subagents` | ✅ goal+context | ✅ result re-enters A as a message |
| `/bg` | ❌ user command | ✅ (`bg_*`) | ❌ own task ID | ❌ prompt only | ✅ same chat/terminal |
| Kanban card | ✅ `kanban_create` or user | ✅ worker per card (source `kanban`) | ❌ hidden (board UI) | ✅ card body + parent-link handoff | ✅ `notify+wake` synthetic turn |
| Bot Mode `message_agent` / @mention | ✅ tool or user | ❌ targets existing Bot Chat | ❌ hidden | ✅ message | ✅ reply attributed |
| api_server Sessions API | ❌ external HTTP | ✅ (source `api_server`) | ✅ dashboard/history | ✅ via `/chat` turn | n/a (poll/SSE) |
| tui_gateway `session.create` | ❌ external client | ✅ | ✅ (or `hidden`) | ✅ seed messages | n/a (events) |
| Compression split | ❌ internal | ✅ continuation | ✅ numbered title | summary | n/a |

Key per-mechanism facts:

- **`/bg`**: three surfaces — CLI, messaging gateway, desktop/TUI (via `prompt.background` RPC; result arrives as a `background.complete` event on the parent session). One-shot amnesiac: no history, no reply channel.
- **Kanban**: each card = full OS process with its own profile/model; worker session hidden from pickers, titled with the card name; `notify+wake` forges a synthetic inbound message so the originating agent takes a real turn with the worker's summary.
- **api_server**: `POST /api/sessions` (title, model/provider) → `POST /api/sessions/{id}/chat[/stream]` (sync turn) or `POST /v1/runs` (async + SSE). **409 boundary:** API sessions cannot bind to sessions owned by other surfaces (CLI/TUI/Desktop/messaging) — you cannot drive another surface's transcript this way.
- **`session.create` (tui_gateway JSON-RPC)**: params include seed `messages`, `model`/`provider`/`reasoning_effort`, `cwd`, `title`, `parent_session_id`, `hidden`, `idempotency_key`. Callable by any authenticated gateway client (desktop WS, TUI stdio, remote desktop) and by the server itself — but by no agent tool.

## Plugin seams (zero core edits)

- **`ctx.subagent_lifecycle.launch`** — the public plugin API for spawn+supervise: `SubagentLaunchRequest(goal, context, role, model, provider, allowed_toolsets, working_directory, parent_session_id, correlation_id, timeout_seconds)` + `wait`/`result`/`steer`/`cancel`. Same host path as `delegate_task`; per-spawn `model` overrides the `delegation` config; terminal result ≤32k chars; in-process 1h only (no reconnect across restarts); fail-closed outside an active agent turn. Known bug: `launch` bypasses delegation safety checks (pause, max_spawn_depth, one-shot child budget) — check upstream before building on it.
- **Slash command**: `ctx.register_command("spawn", h)` + `ctx.dispatch_tool("delegate_task", {goal, context})` is the documented pattern for a /spawn-style command (works in CLI + gateway).
- **`ctx.inject_message(origin=…)`** — starts a new gateway session in a chat with a fresh prompt; reply delivered to that chat; the session lives in the plugin's own profile.
- **Desktop plugin SDK**: `host.newChat()` + `host.composer.submit('new', text)` ("send as if the user typed + pressed Enter") is the ONLY documented path to a visible top-level session tab. Monitor via `host.state.busyBySession` / `host.onEvent('message.complete')`; report back via `host.composer.insertText(A_session, …)` or toast. Optional `plugin_api.py` backend runs inside the gateway process (can import hermes internals) for agent-level report-back. Desktop plugins are NOT sandboxed.
- **Precedent**: the A2A plugin (merged, zero core edits) is the maintainer-endorsed pattern for agent-to-agent features; the sessions_spawn feature request was closed in its favor.

## Decision guide

- Agent-initiated spawn + report-back, visibility not required → `delegate_task` (or a `subagent_lifecycle`-based tool for per-spawn model).
- Want subagent sessions visible in the sidebar → `sessions.show_subagents: true` in profile config.
- Durable, human-in-loop work → kanban card with `notify+wake`.
- Visible top-level tab is a hard requirement → desktop plugin (`host.newChat` + `composer.submit`), optionally paired with a subagent_lifecycle tool for agent-initiation.
- External/scripted spawn → api_server endpoints (mind the 409 boundary).
