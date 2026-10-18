# Removing a Hermes profile and proving nothing references it

Use when the user asks to delete a profile AND "make sure it's used nowhere" / "ensure nothing still references it." Deletion alone is not enough — a profile can still be referenced by kanban assignees, cron jobs, the gateway's `served_profiles`, skills, and docs. Sweep all of them, and separate ACTIVE references (keep the profile "in use") from HISTORICAL ones (logs, transcripts, "retired" notes — do not block deletion).

## 1. Confirm what it is and where it lives

- `hermes profile list` — confirm it's a real profile; note its model/alias.
- Profile home: `$HERMES_HOME/profiles/<name>/` (resolve `$HERMES_HOME`, never hardcode `~/.hermes`).

## 2. Sweep for references BEFORE deleting

Active references (must be cleared / are the blocker):
- **Gateway:** `$HERMES_HOME/gateway_state.json` → `served_profiles` plus any `<name>:<platform>` platform entry. A profile sharing a credential with another shows a `fatal` platform state here.
- **Cron:** `hermes -p <name> cron list`.
- **Kanban assignees:** every board DB — see step 3.
- **Config:** `grep -rn "<name>" $HERMES_HOME/profiles/*/config.yaml $HERMES_HOME/config.yaml`.

Historical references (note them, don't block on them):
- Logs (`$HERMES_HOME/logs/*`), session transcripts (`webui/sessions/**/*.jsonl`), and skills that mention the profile only as "retired"/historical.

## 3. Kanban: check assignees in every board DB

The `sqlite3` CLI is often absent — query with Python's `sqlite3` module (read-only URI) instead:

```python
import sqlite3, glob
home = "$HERMES_HOME"  # resolve first
dbs = glob.glob(f"{home}/kanban/boards/*/kanban.db") + [f"{home}/kanban.db"]
for db in dbs:
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    rows = con.execute("SELECT id,status,title FROM tasks WHERE assignee='<name>'").fetchall()
    con.close()
    # report a status breakdown; OPEN cards (not done/archived) are the blocker
```

Open (non-`done`/`archived`) cards assigned to the profile must be reassigned or closed before deletion. `done`/`archived` cards are fine to leave — they're history.

## 4. Delete

```bash
echo <name> | hermes profile delete <name>   # interactive confirm; pipe the name (no -y flag)
hermes profile purge-identity <name>          # clears session/routing identity settlement
rm -rf $HERMES_HOME/profiles/<name>           # dir reappears empty after the purge
```

`profile delete` already removes the profile dir and its command alias (under `$HERMES_HOME/home/.local/bin/<name>` in this install). The "identity settlement still pending" message is expected — `purge-identity` resolves it. The delete's own inline purge attempt may fail with a benign `FileNotFoundError` (dir already gone); ignore it.

## 5. Verify

- `hermes profile list` — profile gone.
- `grep -c "<name>" $HERMES_HOME/gateway_state.json` → 0. The running gateway rewrites this file on each state write, so a stale `served_profiles` entry clears itself; do NOT hand-edit it.
- Confirm the command alias path is gone.

## Pitfalls

- **Don't hand-edit `gateway_state.json`.** It's live-written by the running gateway; a stale entry self-clears on the next state write.
- **`sqlite3` CLI may be missing.** Use Python's `sqlite3` module with a `file:...?mode=ro` URI — read-only so you never mutate a board while inspecting.
- **Distinguish active from historical references.** Logs, transcripts, and "retired" doc notes are not "in use." Only gateway `served_profiles`, live cron jobs, open kanban cards, and active config/skill routing count.
- **Docs can go stale.** A deleted profile/lane often leaves a reference doc (e.g. a "3-lane workflow" page) that now describes a removed concept. Flag it to the user rather than silently deleting KB content.
