# Kanban worker incidents & resolutions (2026-09-29, board `llama-swap`)

Session-specific detail for the `hermes-kanban-cli` skill.

## Incident 1 — parallel ROADMAP.md write race (no damage, by luck)
- Cards `t_cd2cdd4b` (finalize skills + update ROADMAP) and `t_cb3cfdf9`
  (sync tooling + update ROADMAP) both had `scratch` workspaces but both
  edited the real repo at `/workspace/dev/repos/ours/llama-swap` via absolute
  paths.
- Both modified `ROADMAP.md` (different sections) and committed at 09:08 and
  09:10 — serialized by timing, not by any guard. A same-hunk conflict would
  have left one worker with a dirty tree and a failed commit.
- **Resolution/convention:** cards with shared touch points get parent→child
  links; parallel code work gets `worktree` workspaces.

## Incident 2 — stale "not pushed" claim
- Worker on `t_cb3cfdf9` blocked with `needs_input`, claiming dev commit
  `a3bf730` was local-only and NOT pushed, awaiting review.
- Reality: the other worker had pushed `9a2cc04` (its own commit), and
  `a3bf730` was its parent — so it WAS on `origin/master`.
- **Lesson:** verify git state (`git rev-parse master origin/master`,
  `git log`) before relaying worker claims; a blocked card's summary is a
  self-report.

## Incident 3 — gateway dispatcher did not auto-tick
- After `assign`ing 4 ready tasks to `default`, nothing was claimed within
  ~20 s. `hermes kanban dispatch --dry-run` showed all 4 spawnable; a manual
  `hermes kanban dispatch` spawned them immediately (4 parallel, each in its
  own scratch workspace).
- Gateway was running (PID 16, manual, not a service). Whether the in-gateway
  tick was disabled, lagging, or waiting for its 60 s interval was not
  diagnosed — the manual dispatch is the reliable fallback.

## Incident 4 — scratch workspace tip
- Dispatcher emitted `tip_scratch_workspace` events on spawn: "scratch
  workspaces are ephemeral — they're deleted when the task completes."
- Worker output that must persist must be written outside the workspace
  (absolute paths) or the card needs `worktree`/`dir:`.

## Gate-card pattern (worked as designed)
- 5 ready cards needed to be held in `todo` for a readiness review.
- No `ready→todo` verb exists; `unblock` only covers blocked/scheduled.
- Created gate card `t_db73278b`, linked all 5 as children → they dropped to
  `todo` automatically. `complete` on the gate promoted the 4 remaining
  children back to `ready` (the 5th was unlinked + archived first).

## Incident 5 — PR-merge watchdog false-positive corrupted the chain (SEVERE)

The most damaging incident of the day. A deterministic "PR merged → complete
card → pull → dispatch" watchdog script was written and **test-run manually
before any cron job existed**.

**Root cause:** the merge test was `git merge-base --is-ancestor
<branch-head> origin/master`. A worktree branch that was just created from
master and has **zero own commits** has HEAD == master HEAD, and a commit is
its own ancestor → the test returns true for a branch with **no PR at all**.
Card A2 (t_3d36e719) was in exactly that state (worker running, worktree
freshly branched at 275116c, 329 lines of *uncommitted* work in progress).

**Cascade of damage:**
1. Watchdog "detected" the merge → `kanban complete t_3d36e719` (falsely done,
   summary "PR merged into master (watchdog auto-complete)").
2. `git pull --ff-only` (no-op, master already current).
3. `kanban dispatch` → A3 (t_4c9a1778) auto-promoted to ready and spawned —
   **on top of A2's unfinished, unmerged work** (A3's worktree branched from
   master which did NOT contain A2's changes → the chain's sequential
   guarantee was silently broken).
4. Recovery required killing BOTH workers (A2 mid-flight with uncommitted
   work; A3 seconds after spawn). A3's respawn then hit the spawn-failure
   circuit breaker (2 failures) with a **transient** "worktree path not inside
   a git repo" error — leftover state from the kill, not a real defect.

**Recovery that worked (step by step):**
1. `ps aux | grep "hermes -p"` to find worker PIDs; `kill` (not -9 first).
2. Save the falsely-completed card's body verbatim from the DB before
   archiving: `SELECT body FROM tasks WHERE id='…'` (read-only sqlite URI).
3. `git -C .worktrees/<id> status` → uncommitted incomplete work → explicit
   discard decision: `git checkout -- .`.
4. `git worktree remove .worktrees/<id>` (frees the branch name).
5. `kanban archive <falsely-done-card>`; recreate with **same body, same
   branch name**, fresh `--idempotency-key` (landed straight in `ready`
   because its parents were done).
6. `kanban unlink <old> <child>`; `kanban link <new> <child>`; `kanban
   unblock <child>` for any card the circuit breaker parked.
7. Reassign + `kanban dispatch` to restart the chain on the correct base.

**Lessons (durable):**
- **Never** use `merge-base --is-ancestor branch origin/master` as a
  "PR was merged" test. Use `git rev-list --count origin/master..HEAD` (>0
  means own commits exist) AND `gh pr view <n> --json mergedAt`, or verify
  the merge commit in `git log origin/master`.
- **Never test a board-mutating script on the live board** — even one manual
  "test run" is a live run. Test the detection logic against a throwaway
  repo/branch first.
- Killing a running worker mid-flight leaves uncommitted work + transient
  worktree spawn errors; the recovery sequence above is the proven path.
- The user's follow-up preference: for unattended chain supervision use a
  **subagent supervisor** (with explicit merge authority + recovery
  procedure in its goal), not a watchdog script.

## Incident 6 — gateway user lacked git `safe.directory` → all gateway-spawned
worktree cards failed to spawn (2026-09-29, evening)

- 5 new worktree research cards (LLM-gate batch) were created with
  `--assignee worker`/`default`. The gateway dispatcher tried to spawn them
  and each failed **twice** with:
  `workspace: task t_… worktree path '/workspace/dev/repos/ours/llama-swap'
  is not inside a git repo and does not point at a git repo root` →
  circuit breaker (failure_limit=2) auto-blocked all 5.
- **Root cause:** the repos are owned by `nobody`; the gateway process runs
  as user `hermes` with `HOME=/opt/data`. Git's dubious-ownership guard
  requires a `safe.directory` entry for cross-user repos. The shell user's
  entries live in `/opt/data/home/.gitconfig`, but the gateway reads
  `/opt/data/.gitconfig` — which **did not exist**. So `git rev-parse
  --show-toplevel` (called by `kanban_db._git_toplevel()`) returned rc≠0 →
  "not a git repo".
- **Why it was invisible until then:** earlier worktree cards had been
  dispatched by *manual* `hermes kanban dispatch` from the shell session
  (shell user's gitconfig had the entries). Only the in-gateway tick exposed
  the missing config.
- **Diagnosis that confirmed it:**
  `env -i HOME=/opt/data PATH=/usr/bin:/bin git -C <repo> rev-parse
  --show-toplevel` → `fatal: detected dubious ownership` (rc=128), while the
  same command in the normal shell → rc=0.
- **Fix:** created `/opt/data/.gitconfig` with ONLY `[safe] directory = …`
  lines for the known repos (NO credentials — those stay in the shell
  user's config). Re-verified with the `env -i` command (rc=0), then
  `kanban unblock <id>` + `kanban dispatch` for the 5 blocked cards.
- **Lesson:** when worktree cards fail to spawn with the "not inside a git
  repo" error *and* the path clearly is a repo, suspect the *spawner's*
  git environment (user + HOME + gitconfig), not the repo. Reproduce the
  spawner's env with `env -i HOME=<spawner-home> …` before touching the
  board.

## Incident 7 — kanban.db index corruption mid-batch (2026-09-29, evening)

- While unblocking the 5 cards from Incident 6, `kanban unblock`/`dispatch`
  started aborting with: `could not initialize database: Refusing to open
  corrupt kanban.db at … integrity_check returned 'wrong # of entries in
  index idx_events_run'`. Hermes preserved the original as
  `kanban.db.corrupt.<hash>.bak`.
- **Diagnosis:** `PRAGMA integrity_check` showed `wrong # of entries in index
  idx_events_run`, `wrong # of entries in index idx_events_task`, and
  `row 40 missing from index idx_tasks_status` — index drift, **not** data
  loss. Row counts were intact (`tasks`=43, `task_events`=656).
- **Fix:** `python3 -c "import sqlite3; c=sqlite3.connect('<db>');
  c.execute('REINDEX'); c.commit();
  print(c.execute('PRAGMA integrity_check').fetchall())"` → `('ok',)`.
- **Gotchas:** (a) the event/run tables are named `task_events` /
  `task_runs` (NOT `events`/`runs`) — a `SELECT COUNT(*) FROM events` gives
  "no such table"; (b) the corruption was hit *mid-batch*, so some cards in
  the unblock loop had already been unblocked and others not — re-run
  `kanban list` after the REINDEX to see the real state before continuing.
- **Lesson:** on "corrupt kanban.db", try `REINDEX` + `integrity_check`
  before restoring from the `.bak` — the data is usually fine and REINDEX is
  lossless.

## Incident 8 — worker hung in a degenerative LLM stream, heartbeats intact
(2026-09-29, evening, card t_28301c34 on `worker` profile)

- Card `running` since 17:56 (run 59, PID 102628), heartbeats every ~60 s
  through 19:21 — the dispatcher saw a perfectly healthy worker.
- Reality: the worker's LLM request (qwen38vl-27B on `llm.lan.fahsel.ch:8080`)
  started at **18:50:31 and never finished** — by 19:24 it had streamed
  **1,169,085 bytes** (1.17 MB) over **2,014,836 ms (33.6 min)**. A normal
  worker answer is a few KB in seconds-to-minutes. The model had entered a
  degenerate generation loop.
- **Why it was invisible:** (a) heartbeats are auto-emitted by the worker
  process independent of LLM progress, so stale-reclaim never fired;
  (b) the worktree had 0 commits and a clean status (the worker had not yet
  shipped any work — last file change 18:41), so there was no visible
  progress to notice; (c) the profile's `state.db` showed the last session
  message at 18:50:30 — the tell that "last tool result is 40 min old while
  heartbeats continue".
- **Diagnosis path that found it:**
  1. `kanban show` events → heartbeats current (looked healthy).
  2. Worktree: `git status --porcelain` empty + `find . -newermt 18:45`
     → no file changes in 40 min (suspicious).
  3. Profile session DB `/opt/data/profiles/worker/state.db`: latest message
     per session → 18:50:30 (stale). NOTE: that DB's `sessions` table has no
     `last_activity_at` column (older schema) — use `started_at` + latest
     `messages.timestamp`.
  4. LLM host inflight view: `curl -sN http://<llm-host>:8080/api/events` →
     SSE `inflight` snapshot with `elapsed_ms` / `resp_bytes` per request →
     the 33-min/1.17-MB request was the smoking gun.
- **Resolution:** user killed the hung request(s) on the llm host (both
  workers' requests were reset; the other worker, t_b9c15ded, simply
  re-requested and continued fine). Then
  `kanban reassign t_28301c34 default --reclaim` (reclaim releases the
  running claim; reassign moves the card to the stronger local model) +
  `kanban dispatch` → run 63 spawned on `default` (PID 110514), clean.
  Worktree untouched → zero work lost, fresh run from scratch.
- **Lessons (durable):**
  - "running + fresh heartbeats" ≠ "making progress" for workers on a
    second LLM host. For cards older than ~1 h: check worktree mtime, the
    profile session DB's last message timestamp, and the host's inflight
    snapshot (`elapsed_ms`/`resp_bytes`).
  - `kanban reassign <id> <profile> --reclaim` is the clean way to pull a
    live (possibly hung) card to a different profile — it releases the claim
    atomically; a plain `reassign` refuses while running ("still running —
    pass --reclaim").
  - A hung request costs nothing to kill when the worktree is clean — the
    fresh respawn is strictly better than waiting for a degenerate stream to
    finish (it may never finish).

## Board state at end of session (2026-09-29, late)
- A-Kette: A1 (inflight-wait) done via PR #6 (275116c); A2' (t_96a82d91,
  health-poll + fallback, retry after incident 5) done via PR #9; A3
  (t_4c9a1778, ping + report.json) done via PR #8.
- B-Kette: B1 (L1 rollup, t_cff235cf) done; B2 (L3 drain, t_73eedc82) done
  via PR #11 (Option B — full 600 s veto, early-drain removed; reviewed by a
  background subagent with delegated merge authority); B3 (test coverage,
  t_b9c15ded, worker) running.
- Handoff-Kette: t_226f0f46 (basis + follow-up agent) done via PR #10;
  t_28301c34 (telegram interaction) re-assigned worker → default after
  incident 8, running on default.
- LLM-Gate-Recherche: 5 research cards + synthesis all done, committed to
  `discussion/llm-gate-*.md` on master (synthesis commit 7adf50a).
- User decisions recorded as `USER DECISION` comments on the cards: L1
  rollup-in-code, L3 full 600 s veto (no early drain), SSE-only inflight,
  fallback 1× target + 2× fallback/20 s backoff + exit code 4, handoff
  split.
- Open: t_17974a36 (Reboot-Tool als Plugin, default, behind 6 parents —
  4 done, 2 running).
