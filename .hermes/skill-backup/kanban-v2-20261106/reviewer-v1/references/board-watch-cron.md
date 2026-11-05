# Board watcher via cron (monitor-gated, zero LLM cost when idle)

> **User preference (Peter, 2026-10-11): do NOT set this up by default — he
> dislikes cron watchers for board work.** The board already pings subscribed
> chats on blocked/done/review (cards created by a session are auto-subscribed)
> — never claim the board cannot notify. Protect chain ordering board-natively
> instead: (a) every card body carries "any follow-up card you create:
> kanban_link it BEFORE the next chain card <id>"; (b) PR cards end with
> `request_review` to `reviewer` (2-lane rule), reviewer merges. Use this
> recipe only when the user explicitly asks for a watcher.

Use when a sequential card chain will run for hours while the user is away and
they want to be told about completions, blocks, new follow-up cards and
ordering violations.

## 1. Deterministic snapshot script (the monitor)

`/opt/data/scripts/<board>-board-snapshot.py` — prints one sorted line per
non-done task, no timestamps, stable token on error:

```python
import json, subprocess
try:
    out = subprocess.run(["/opt/hermes/bin/hermes", "kanban", "--board", "<slug>",
                          "list", "--json"], capture_output=True, text=True,
                         timeout=60).stdout
    tasks = json.loads(out[out.find("["):])
    lines = sorted(f"{t['id']} {t['status']}" for t in tasks
                   if t.get("status") not in ("done", "archived"))
    print("\n".join(lines) if lines else "ALL-DONE")
except Exception:
    print("error")
```

CLI facts: `--board` goes BEFORE the subcommand (`hermes kanban --board X list`);
the CLI may print an install warning line before the JSON — slice from the
first `[`; `list --json` rows carry no parent/child fields (use `kanban_show`
in the agent tick for links). Run the script once by hand before wiring it.

## 2. Cron job

`cronjob_manage action=create` with: `schedule="every 10m"` (user prefers
frequent short polls), `monitor="<board>-board-snapshot.py"` (NOT `script` —
script would wake the agent every tick), `continuity=true`,
`enabled_toolsets=["kanban","terminal","cronjob"]`, `workdir=<repo>`.

**Set `deliver` explicitly** (`all` or the user's platform): a job created from
a desktop/CLI session defaults to `local`, which saves output but never
notifies anyone — the watcher would be silent.

## 3. Tick prompt (self-contained, user's language)

- The planned chain with ids + one-line purpose + which cards block on purpose
  for a user decision.
- Report only changes: completed (1 line each), blocked (reason + recommended
  option), crashed/gave_up, new card, ordering violation (two host-sharing
  cards running, or a card running before its predecessor is done).
- Allowed actions: `kanban_link` new not-yet-running cards into the chain,
  `kanban_comment`. Forbidden: kill, unblock, complete, block, touching hosts
  or git — the user decides; an already-parallel run is alert-only.
- `error` monitor output or nothing relevant → reply `.`.
- Lifecycle: when the last chain card is done → 3-line summary, then
  `cronjob_manage list` + `remove` itself.
