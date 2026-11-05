#!/usr/bin/env python3
"""board-probe.py — read-only health metrics for one Hermes kanban board.

Usage: python3 board-probe.py <board-slug> [--since YYYY-MM-DD]
Prints a Markdown table: cards/runs, runs per card, run duration, loop/guard
events, created->completed latency. Never writes. sqlite3 CLI is not needed.
"""
import argparse
import datetime as dt
import sqlite3
import statistics as st
import sys
from pathlib import Path

BOARDS = Path("/opt/data/kanban/boards")
EVENTS = ("block_loop_detected", "blocked", "unblocked", "respawn_guarded",
          "crashed", "reclaimed", "gave_up", "timed_out", "review_requested",
          "changes_requested", "completed")


def pct(xs, p):
    if not xs:
        return 0
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("--since", help="only runs/events created on/after this date (UTC)")
    a = ap.parse_args()
    db = BOARDS / a.board / "kanban.db"
    if not db.is_file():
        sys.exit(f"no board db: {db}")
    since = 0
    if a.since:
        since = int(dt.datetime.fromisoformat(a.since).replace(tzinfo=dt.timezone.utc).timestamp())
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)

    runs = c.execute("select task_id, started_at, ended_at from task_runs where coalesce(started_at,0)>=?", (since,)).fetchall()
    per_card = {}
    for tid, _, _ in runs:
        per_card[tid] = per_card.get(tid, 0) + 1
    cnt = list(per_card.values())
    dur = [(e - s) / 60 for _, s, e in runs if s and e and e > s]
    ev = dict(c.execute(
        "select kind, count(*) from task_events where created_at>=? and kind in (%s) group by kind"
        % ",".join("?" * len(EVENTS)), (since, *EVENTS)).fetchall())
    lat = c.execute("""select (select max(e.created_at) from task_events e where e.task_id=t.id and e.kind='completed')
                              - (select min(e.created_at) from task_events e where e.task_id=t.id and e.kind='created')
                       from tasks t where t.status in ('done','archived')""").fetchall()
    lat = [x[0] / 3600 for x in lat if x[0] and x[0] > 0]
    status = dict(c.execute("select status, count(*) from tasks group by status").fetchall())

    print(f"## Board `{a.board}` — probe {dt.date.today()}" + (f" (since {a.since})" if a.since else ""))
    print()
    print("| metric | value |\n|---|---|")
    print(f"| cards by status | {status} |")
    print(f"| cards with runs / runs | {len(per_card)} / {len(runs)} |")
    if cnt:
        print(f"| runs per card median / mean / max | {st.median(cnt)} / {st.mean(cnt):.2f} / {max(cnt)} |")
        print(f"| cards with ≥4 runs | {sum(1 for x in cnt if x >= 4)} |")
    if dur:
        print(f"| run minutes median / mean / p90 | {st.median(dur):.1f} / {st.mean(dur):.1f} / {pct(dur, .9):.1f} |")
    for k in EVENTS:
        print(f"| event `{k}` | {ev.get(k, 0)} |")
    if cnt:
        print(f"| block_loop per 10 cards | {10 * ev.get('block_loop_detected', 0) / max(1, len(per_card)):.2f} |")
    if lat:
        print(f"| created→completed hours median / mean (n={len(lat)}) | {st.median(lat):.1f} / {st.mean(lat):.1f} |")


if __name__ == "__main__":
    main()
