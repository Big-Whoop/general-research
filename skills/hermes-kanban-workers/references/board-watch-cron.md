# Board watcher via cron — RETIRED for this user

> **Peter (standing): never a cron watcher for board work, not even for
> hours-long unattended runs** — a cron job runs in a session he cannot see,
> so he has no sign that anything is still running. Use the in-session
> background watcher (`scripts/board-watch.py`, terminal background=true,
> notify=true) in the chat he delegated from; release duties live in
> `references/release-duties.md`. If a cron watcher exists from an earlier
> session, `cronjob_manage list` + `remove` it and start the in-chat watcher.
> The board already pings subscribed chats on blocked/done/review — never
> claim the board cannot notify.
>
> The recipe below is kept only for a context with no chat session at all
> (e.g. a Telegram-only profile) and only on explicit ask.

Use when a sequential card chain will run for hours while the user is away and
they want to be told about completions, blocks, new follow-up cards and
ordering violations.

## Variant: overnight autonomous orchestrator (user asleep, wants the chain to finish)

When the user explicitly wants a chain to run through unattended ("finish it
tonight, I'm going to sleep"), a report-only watcher is not enough. The chain
then stalls at the first `needs_input` card. Set it up like this:

1. **Get the sign-off once, scoped, before the user leaves.** Ask a single
   question: "Do you approve all in-plan steps on <hosts> without further
   confirmation?" Write the answer as a comment on every chain card AND into
   the tick prompt. Workers block on Gate-2 questions unless the card itself
   carries the authority.
2. **Write explicit fences into the prompt and the cards.** Allowed: in-plan
   ops, one-time bootstrap ops, reviewer-lane merges, deciding in-plan
   operational `needs_input` questions with the worker's/reviewer's recommended
   option (comment "decided by orchestrator under blanket sign-off"). Still
   forbidden: constraint changes, other hosts, data deletion, pushing to main
   without a PR. If the user calls a host expendable, allow reinstall and
   alternatives. Any deviation from a recorded decision still needs a
   REVISIONS entry in the PR, so it never happens silently.
3. **The orchestrator still never does the work itself (Gate 8).** A blocked
   card gets a seeded ops/fix card linked BEFORE it, then gets unblocked.
   Spell out the unblock chain in the prompt ("when X is done, unblock Y").
4. **Tick every 5m with `continuity=true`, and reply `[SILENT]` when nothing
   changed.** The user asked for this cadence when the chain was hanging.
   Set `deliver` to origin + the user's channels, and cap `repeat`.
5. **Every card the tick creates goes through the input gate** (terminal
   `hermes kanban create --body-file`, never the native tool) and gets
   `kanban link`ed into the chain.
6. **Morning review:** look for out-of-band fixes that workers made on hosts
   (e.g. a hand-edited git remote). Each one gets a follow-up code card that
   codifies it, because a wipe/reinstall silently loses it. Then remove the
   job.

A worker or reviewer that hits a Gate-2 question it was not authorized for
blocks with `needs_input`. That is correct behaviour, not a hang. Report the
concrete decision with options and a recommendation, and don't just reclaim.

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

**Set `deliver` explicitly** (`telegram` or the user's platform): a job created from
a desktop/CLI/TUI session defaults to `local`/origin, which saves output but never
notifies anyone — the watcher would be silent. In the TUI, cron output is NOT
delivered back into the session at all; only a messaging platform target reaches
the user. Cap `repeat` to the expected chain duration (e.g. 200 × 5 min) and
make the prompt remove the job itself when the last chain card is done.

**When the chain is re-sequenced, `update` the job's prompt** (new card ids,
new order, which cards block on purpose) — a watcher reporting against a stale
chain either stays silent on the cards that matter or flags the new ones as
"ungated". Remove superseded paused watchers in the same pass (`list` first).

**Before telling the user the watcher failed, read `cronjob_manage list`:** `last_status ok`
with an unchanged monitor hash means the board did not change — the user got
nothing because there was nothing, not because delivery broke.

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
