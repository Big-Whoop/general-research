# Board Forensics (read-only)

Use when the user reports a board's cards missing/changed, or when you must verify
what actually happened on a board (which board a run used, whether cards were deleted,
what touched it in a time window). Always read-only: open the DB with the `mode=ro`
URI, never write during an investigation.

## Where state lives

- Active board pointer: `/opt/data/kanban/current` — one line, the slug. Set by
  `boards switch` / `boards create --switch`.
- Per board: `/opt/data/kanban/boards/<slug>/kanban.db` (SQLite) + `board.json`
  (metadata: name, description, default_workdir, archived; its mtime is the board's
  creation marker). Worker logs: `boards/<slug>/logs/`, workspaces:
  `boards/<slug>/workspaces/<task-id>/`.

## Querying the DB

The `sqlite3` CLI is not in the sandbox — use Python's stdlib module:

```python
import sqlite3
con = sqlite3.connect("file:/opt/data/kanban/boards/<slug>/kanban.db?mode=ro", uri=True)
```

Schema essentials:
- `tasks`: id, title, body, status, assignee, created_at, completed_at,
  workspace_kind, branch_name, idempotency_key, model_override, provider_override
- `task_events`: id, task_id, run_id, **kind**, payload, created_at — the column is
  `kind`, not `event_type`
- `task_runs`: one row per attempt (status, outcome, summary, error)
- `task_links`: parent_id, child_id
- `task_comments`: id, task_id, author, body, created_at

## Deletion check (the "board content was deleted" claim)

1. List all tasks (id, title, status, created_at) and compare count/titles with what
   the user expects.
2. `SELECT kind, COUNT(*) FROM task_events GROUP BY kind` — a healthy board shows one
   `created` event per card; a real wipe shows missing `created` events or explicit
   delete/reset kinds.
3. `archived` events are normal operations (pulling a card back), not data loss —
   check the timestamp and which card.
4. Window check: `SELECT task_id, kind, created_at FROM task_events WHERE created_at
   BETWEEN ? AND ?` — if the suspected actor (e.g. a research run) left no events in
   the window, it never touched the board.
5. File mtimes are NOT evidence of a reset: WAL checkpoints touch the main `kanban.db`
   on ordinary reads. `board.json` mtime + the oldest `created` event are the real
   creation markers.

## Live API verification (separating backend from client)

The DB check proves the data is on disk; the live API check proves the backend serves
it correctly — which localizes a wrong UI display to the client.

- The dashboard serves the kanban API at `http://127.0.0.1:<port>/api/plugins/kanban/*`
  (port from the process list: `ps -eo pid,cmd | grep dashboard`).
- `curl -u admin:<pw>` does NOT work — the auth gate wants a session cookie (401
  "no_cookie"). Log in first, then reuse the cookie jar:
  ```bash
  curl -c /tmp/cj -X POST -H "Content-Type: application/json" \
    -d '{"provider":"basic","username":"admin","password":"<pw>"}' \
    http://127.0.0.1:<port>/auth/password-login
  curl -b /tmp/cj http://127.0.0.1:<port>/api/plugins/kanban/boards
  ```
  The password is the dashboard process's env var
  `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD` (`tr '\0' '\n' < /proc/<pid>/environ`) —
  never write it into a report or a skill.
- Endpoints: `GET /boards` → all boards with live card counts + the server's
  `current` board; `GET /board?board=<slug>` → cards for exactly that board;
  `GET /board` (no param) → the ACTIVE board (env `HERMES_KANBAN_BOARD` → `current`
  file → `default`) — the fallback a client hits when it omits the param.
- Decision rule: if `/board?board=<slug>` returns the expected cards, the backend is
  innocent — the wrong display is a client bug (stale UI build or cache), not data
  loss. If it returns the wrong board's cards, the bug is server-side: check the
  dashboard process env for `HERMES_KANBAN_BOARD` / a foreign `HERMES_HOME`, and its
  start time (`ps -eo pid,lstart,cmd`) against the incident window — a restart inside
  the window resets in-memory state and is a common "something changed" trigger even
  when all data is intact.

## Why "missing cards" is usually a display issue

The Kanban UI (dashboard AND desktop app) keeps its OWN board selection, persisted
locally (browser localStorage / local persistence) — it does NOT follow the CLI
`current` pointer and does NOT follow the active project (official kanban docs).
A user looking at the Kanban page in project A can be shown board B (whatever the UI
selection holds) and conclude "board A's content was deleted". Before reporting data
loss: run the deletion check above, then tell the user to pick the intended board in
the UI's board dropdown. Note: project slug and board slug need not match — the UI
has no project→board resolution at all.

Known client failure mode: an OLD kanban UI build omits `?board=` on the card fetch,
so the grid silently falls back to the CLI `current` board while the switcher still
shows the user's selected board — label and data disagree, and the board list can be
a stale cache (a board created later is missing from the dropdown). Signature: the
grid's cards belong to a different board than the switcher label. Forensic trick: the
switcher's count badge reveals the age of the cached board list — compare it with the
card-creation timeline (a count matching the board state from days ago proves the
list is stale). Fix: restart the desktop app / hard-reload the Kanban page so the
current UI build (which always sends `?board=<slug>`) loads; if it persists on the
latest version, report upstream.

## Tracing what a session did to a board

- Session transcripts: `session_search` tool with `session_id` (ids look like
  `YYYYMMDD_HHMMSS_xxxxxx`). The webui session files under `/opt/data/webui/sessions/`
  are NOT named after that id — don't hunt for them on disk; the tool resolves the id.
- Card bodies record the board explicitly (`Board: <slug>` line, `--board <slug>` in
  the commands) — the DB the card lives in is ground truth for which board a run used.
- Cross-check the repo: `git log --all` + `gh pr list --state all` on the target repo
  — a research run's PR lands in the repo its collector card anchored to.

## Report shape

When the user asks for an investigation report first, do the whole investigation
read-only and present findings before touching anything: timeline (CEST), evidence
per claim (card lists, event counts, PR state), root cause, open items,
recommendations.
