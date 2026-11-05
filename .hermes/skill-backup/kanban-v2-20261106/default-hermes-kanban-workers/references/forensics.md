# Kanban forensics: who changed a card

Use when a card unexpectedly changed state (started, unblocked, archived, "reactivated") and the CLI view does not explain it. The full audit trail is the board DB, not the CLI. Query with python `sqlite3` (read-only URI `file:<db>?mode=ro`) via execute_code.

## Board DB — `/opt/data/kanban/boards/<board>/kanban.db`

- `task_events(kind, run_id, payload, created_at)` is the complete history per card; `tasks` has NO `updated_at` column — reconstruct state changes from events only.
- A `commented` event payload records only `{author, len}` — the text is in `task_comments` (join by task_id + created_at).
- Audit "all boards" by iterating every `/opt/data/kanban/boards/*/kanban.db`; CLI/board resolution defaults to the active/current board and hides open cards elsewhere.
- Comment/event storms across many cards within seconds = an automation (crew stop flow, coordinator pass), not a person.
- A stop flow stamps `BLOCKED: Owner stop` comments on archived and already-blocked cards too and prints `cannot block …` for those — its listed card set is NOT evidence of live cards; read `task_comments` + events for the true sequence before reporting what was running.

## Dispatcher verbs — transitions without an actor

- `block_loop_detected` routes a card back to `triage` (where the decomposer can feed it again).
- `decomposed` creates `todo` children that auto-promote once parents finish.
- `promoted` = a dependency gate opened (parent done/archived).
- Consequence: a campaign "stopped" via typed/technical blocks can return to a dispatchable state on its own without anyone unblocking. Verify a stop by `status='archived'` — the dispatcher skips archived — NOT by `blocked`, which retries.

## Attribution — events carry no caller

- Join events by timestamp against the `sessions` table in `/opt/data/state.db` and `/opt/data/profiles/*/state.db`: a card's worker session row appears seconds after its `claimed` event (`started_at`, `source='kanban'`, `cwd` = the card workspace).
- Grep `messages.tool_calls` (JSON) for the card id or `kanban_block`/`kanban_unblock`/`kanban_archive` to find the calling session and profile.
- An operator acting via raw CLI or plugin code leaves no kanban-tool call: widen the search to `terminal` tool_calls whose arguments contain the card id.
- `edited`/`unblocked` events with no payload and no matching session tool_call anywhere (terminal grep included) were made by plugin code, not a chat agent: plugin coordinators (crew) rewrite card bodies and unblock cards themselves — correlate the plugin's own log (e.g. `/opt/data/crew/coordinator.log`) with the event timestamps before blaming a human or a session.
- Session ids can display truncated: re-query with `where id like '<prefix>%'` rather than re-running the earlier query with the short id.
- A worker that self-blocked and reports "made no changes": read its session `messages` tool_calls before believing it — it may have written config before blocking.
