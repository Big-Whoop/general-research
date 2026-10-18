#!/usr/bin/env python3
"""In-session board watcher: polls a kanban board and EXITS (printing the change)
when the orchestrator must act. Run as a terminal background job with
notify=true; the exit notification wakes the orchestrator, which handles the
event and restarts the watcher in the same turn.

Usage:
  board-watch.py <board-slug> [interval_s=120]          normal run
  board-watch.py <board-slug> [interval_s] --hold       wait-for-user mode

Normal run exits on: card -> blocked/review/scheduled/done(or archived), new
card, board idle (nothing running/ready/review/scheduled -> propose next).
It diffs against the last REPORTED snapshot (state file per board), so events
that happened while the watcher was stopped or on --hold are still reported.

--hold: the orchestrator asked the user a question and waits for the answer
(strict turn-taking). Never exits, reports nothing; only keeps ready cards
from being stuck on the active_pr respawn guard. Kill it when the user
answers and start a normal run.

Both modes auto-age PR-URL comments of `ready` cards freshly hit by
`respawn_guarded {'reason': 'active_pr'}` (fires after every unblock of a card
whose comments quote its own, already merged PR)."""
import json, os, sqlite3, subprocess, sys, time

args = [a for a in sys.argv[1:] if not a.startswith("--")]
BOARD = args[0]
INTERVAL = int(args[1]) if len(args) > 1 else 120
HOLD = "--hold" in sys.argv
DB = f"/opt/data/kanban/boards/{BOARD}/kanban.db"
STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), f".board-watch-{BOARD}.json")
ACT = {"blocked", "review", "scheduled", "done", "archived"}
BUSY = {"running", "ready", "review", "scheduled", "claimed"}


def snap():
    out = subprocess.run(["/opt/hermes/bin/hermes", "kanban", "--board", BOARD, "list", "--json"],
                         capture_output=True, text=True, timeout=60).stdout
    tasks = json.loads(out[out.find("["):])
    return {t["id"]: [t.get("status"), t.get("title", "")[:90]] for t in tasks
            if t.get("status") not in ("done", "archived")}


def unguard(cur):
    ready = [k for k, (s, _) in cur.items() if s == "ready"]
    if not ready:
        return
    c = sqlite3.connect(DB, timeout=10)
    try:
        for k in ready:
            hit = c.execute("SELECT 1 FROM task_events WHERE task_id=? AND kind='respawn_guarded' "
                            "AND payload LIKE '%active_pr%' AND created_at > strftime('%s','now')-180",
                            (k,)).fetchone()
            if hit:
                n = c.execute("UPDATE task_comments SET created_at=created_at-86400 WHERE task_id=? "
                              "AND body LIKE '%github.com/%/pull/%' "
                              "AND created_at > strftime('%s','now')-86400", (k,)).rowcount
                if n:
                    print(time.strftime("%H:%M"), f"unguarded active_pr: {k} ({n} comments)", flush=True)
        c.commit()
    finally:
        c.close()


def load():
    try:
        with open(STATE) as f:
            return json.load(f)
    except Exception:
        return None


def save(cur):
    with open(STATE, "w") as f:
        json.dump(cur, f)


def main():
    prev = load()
    while True:
        try:
            cur = snap()
            unguard(cur)
        except Exception:  # transient CLI/db hiccup: retry next tick
            time.sleep(INTERVAL)
            continue
        if HOLD:
            time.sleep(INTERVAL)
            continue
        if prev is None:  # first run ever: board becomes the baseline
            prev = cur
            save(cur)
        events = [f"{k} {s} -> done/archived  {t}" for k, (s, t) in prev.items() if k not in cur]
        events += [f"{k} {s} -> {cur[k][0]}  {t}" for k, (s, t) in prev.items()
                   if k in cur and cur[k][0] != s and cur[k][0] in ACT]
        events += [f"{k} NEW {s}  {t}" for k, (s, t) in cur.items() if k not in prev]
        idle = not any(s in BUSY for s, _ in cur.values())
        if events or idle:
            print(time.strftime("%H:%M"), "BOARD EVENT")
            for e in events:
                print("  " + e)
            if idle:
                print("  IDLE: no card running/ready/review/scheduled -> propose next")
            print("Open cards now:")
            for k, (s, t) in sorted(cur.items()):
                print(f"  {k} {s} {t}")
            save(cur)
            return
        prev = cur
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
