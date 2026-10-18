# Hermes Kanban — CLI recipes (normal session)

Consolidated from the former `hermes-kanban`, `hermes-kanban-ops` and
`hermes-kanban-cli` skills. Campaign workflow, input-gate rules (R1–R8),
conflict analysis, config knobs and watchers live in `hermes-kanban-workers`
(+ its `references/`) and are NOT repeated here — only pointed at.

Standing facts: CLI is `/opt/hermes/bin/hermes` (not on PATH). Boards live in
`/opt/data/kanban/boards/<slug>/` (`kanban.db` + `board.json`, `logs/`,
`workspaces/`). Exactly two lanes per board: `default` (worker) and
`reviewer`. Code goes card → worktree → branch → PR; the user reviews/merges
at the PR. Event-driven chains (parent→child links), never cron polling.
Decisions are kanban comments. Never create cards unasked.

## Environment & CLI quick reference

```bash
H=/opt/hermes/bin/hermes            # or inline the path (see Pitfalls: $VAR noise)
$H kanban boards create <slug> --name "…" --description "…" --icon "🔁" --color "#f59e0b" --default-workdir /abs/repo --switch
$H kanban boards list               # all boards + counts;  `boards show` takes NO slug (prints current)
$H kanban boards switch <slug>      # session-global; prefer --board per verb
$H kanban --board <slug> <verb> …   # --board goes AFTER `kanban`, BEFORE the verb
$H kanban create "Title" --body "…" --idempotency-key <key> --json [--parent <id>] [--assignee <p>] [--workspace worktree --branch <b> --completion-contract local-only] [--triage]
$H kanban list [--status blocked] / show <id> [--json] / stats / runs <id> / log <id> / tail <id> / diagnostics
$H kanban link <parent> <child> / unlink <parent> <child>
$H kanban assign <id> <profile|none> / reassign <id> <profile> [--reclaim]
$H kanban dispatch [--dry-run] [--max N]
$H kanban comment <id> '…'
$H kanban complete <id> --summary "…" [--force]     # the done verb; `kanban done` does not exist
$H kanban block <id> --kind {capability,dependency,needs_input,transient} <reason words…>   # reason is POSITIONAL, no --reason
$H kanban unblock <id>              # blocked/scheduled → ready|todo only
$H kanban schedule <id> "reason"    # park (deferred)
$H kanban promote <id> "reason"     # todo/blocked → ready (recovery)
$H kanban specify <id>              # triage → todo (LLM refine, ~60–90 s/card; sanctioned path = kanban-tools gate wrapper)
$H kanban reclaim <id>              # release a running claim → card goes back to READY (not todo)
$H kanban set-model <id> <model> --provider <name>   # per-card override, `none` clears
$H kanban request-review <id> --summary "…" --reviewer reviewer [--force]
$H kanban request-changes <id> <reason…> / reopen-review <id>
$H kanban archive <id>              # no delete verb; idempotency key stays reusable
$H kanban edit <id> --body "…"      # replaces the WHOLE body (older notes said edit cannot set body — verify with `--help`)
```

- Title is positional — there is no `--title` flag.
- `--summary` vs `--result` on `complete`: both appear in older notes; verify with `hermes
  kanban complete --help`.
- **`--json` parsing:** stdout can carry a warning line before/after the JSON ("No gateway
  is running" is cosmetic). Parse with `json.JSONDecoder().raw_decode(out[out.find('{'):])`
  (or `[` for `list`), not `json.loads`. `list --json` rows carry no parent/child fields.
- **Body text:** on gate-enabled boards write long bodies to a scratch file under
  `/opt/data` or `/workspace` (`write_file` to `/tmp` is denied) and pass `--body-file
  <path>` (the current hook reads the file; older notes claimed it is blocked — if it is,
  inline the body as a single-quoted literal). Never `--body "$(cat file)"`: the hook
  `shlex`-parses the raw command and sees the literal `$(cat …)`, and `$(…)` substitution
  can trip the unconditional blocklist. Confirm a staged file is visible to the shell (`wc
  -l`) before `create`; a lagging `write_file` yields an empty-body card (`"body": ""` in
  the JSON).
- **Comments: single-quote the body.** Backticks in `"…"` get shell-expanded and the token
  silently disappears.
- `create --help` is blocked by the input-gate hook (no body). Read flags from
  `hermes-kanban-workers/references/input-gate.md` or
  `/opt/hermes/hermes_cli/kanban_parser.py`.
- Do not pipe `kanban show` into `head` (BrokenPipe traceback). `kanban tail` is a live
  follow that blocks past the 180 s terminal timeout — use `log` or the log file.
- Kanban tools in a normal session: none by design (two-surface model). `kanban_*` tools
  exist only in dispatcher-spawned workers (`HERMES_KANBAN_TASK`) or when `kanban` is in the
  TOP-LEVEL `toolsets:` list of config.yaml (`platform_toolsets` is the wrong key). The CLI
  is the sanctioned interface.
- Direct DB access: the `sqlite3` CLI may be absent — use Python stdlib `sqlite3`; use the
  venv interpreter `/opt/hermes/.venv/bin/python3` for anything importing `hermes_cli.*`
  (system python lacks `ruamel`). Tables are `tasks`, `task_events` (column `kind`),
  `task_runs`, `task_links`, `task_comments`; `archived` is a status value, not a column.
  Set `conn.row_factory = sqlite3.Row` before `dict(row)` or `create_task`.

## Card lifecycle & workspace modes

`triage → todo → ready → running → done`, plus `blocked`, `scheduled`, `review`, `archived`.
List glyphs: ◻ todo ▶ ready ● running ⊘ blocked ⏱ scheduled ✓ done.

- `triage`: raw, unspecified — and the auto-decomposer's INPUT QUEUE (up to 3 per tick).
  Never park a card there; a card you intend to specify gets the gate wrapper immediately.
  Only `specify` leaves triage (`promote`/`unblock` refuse). `specify` with no args still
  runs an LLM refine that can retitle/reformat; run multi-card loops in the background.
  Pure-DB fast path: `specify_triage_task(conn, id, author=…)` then `recompute_ready(conn)`
  (no LLM, body verbatim).
- `todo`: spec done, waiting on open parents. `ready`: parents done; claimable only with an
  assignee.
- `scheduled`: parked by time/resource (e.g. a host the user is using manually). `blocked
  --kind needs_input` = a review/decision request, not a failure — surface it, never
  auto-unblock.
- `complete` accepts only `running|ready|blocked`; `triage`/`todo` cards must be promoted
  first. `complete` on a done card → "unknown id or terminal state" (harmless).
  `request-review` accepts only `running|ready`.
- `reclaim` → `ready` (dispatchable). `unblock` on a `review` card leaves it in `review`.

Workspace (per card, `--workspace`, default `scratch`):

| Mode | Worker gets | Use for |
|---|---|---|
| `scratch` | own dir `<board>/workspaces/<id>/`, **deleted on completion** | research/read-only; results must go into the card result or a repo |
| `worktree` (+`--branch`) | isolated worktree `<repo>/.worktrees/<id>` + branch | any parallel code change (the only PR path) |
| `dir:/abs/path` | the shared checkout itself | read-only sequential work ONLY |

- Board `--default-workdir` does NOT give cards repo access; a `worktree` card anchors to
  the ACTIVE board's workdir. Verify with `kanban show <id>` → `workspace:` line before
  dispatch.
- Isolation is of the starting cwd only (dispatcher pins `TERMINAL_CWD`); a scratch worker
  editing the repo by absolute path writes into the real checkout. Collision rules:
  `hermes-kanban-workers` §3 / Pitfall 1.
- Unassigned `ready` cards are skipped forever (`skipped_unassigned`) unless
  `kanban.default_assignee` is set; a non-profile assignee is `skipped_nonspawnable`. One
  card = one assignee; "all workers" is not a mode.
- Worker = `hermes -p <assignee> chat -q …` with the profile's full CLI toolset +
  task-scoped `kanban_*` tools; memory and context files ARE loaded. Heartbeats ~60 s;
  circuit breaker after `failure_limit` (2) failed runs.

## Board selection & creation

- `board.json` holds name/description/`default_workdir`; its mtime + the oldest `created`
  event are the creation markers (DB mtime is not — WAL checkpoints touch it). Active
  pointer: `/opt/data/kanban/current`.
- One board per repo/workstream with the right `--default-workdir`. `create` always lands on
  the ACTIVE board, there is no move-between-boards verb, and a worktree card for repo X
  created while board Y is active spawns in Y's worktrees — the "two wasted recreations"
  lesson. Use `--board <slug>` on every verb instead of `boards switch`.
- "Missing cards" is almost always the UI's own persisted board selection (it follows
  neither the CLI `current` pointer nor the active project). Check the DB first
  (`keep-board-forensics.md`), then tell the user to pick the board in the dropdown /
  hard-reload.
- Prefer the terminal path for creates (the input gate only sees terminal calls). Create
  long chains in small terminal batches (2–3 per call, `timeout 120`), not one
  `execute_code` loop — see `hermes-kanban-workers` §3b.

## Gating & batches

- **Gate-card pattern (ready → todo demotion):** no verb demotes `ready`. Create `GATE: …`
  (lands `ready`), `link <gate> <child>` each card (child drops to `todo` immediately), do
  the readiness work, `complete <gate>` → children auto-promote next tick. Pull a card out:
  `unlink <gate> <id>` THEN `archive <id>` (or it re-promotes). Linking an open parent also
  parks a reclaimed card.
- Link BEFORE the dispatcher sees a card: `--parent <id>` at create time, or create under an
  existing open gate. `link` refuses a child that is already `running`.
- Direct-DB gated batch (whole chain, nothing dispatches): `create_task(conn, …,
  parents=[gate, …])` from `hermes_cli.kanban_db`; gate with `initial_status="blocked"` and
  NO assignee (`initial_status` accepts only `blocked|running`); one `conn.commit()`; verify
  one leaf with `show` (`workspace: worktree @ <repo>`, `dependency_wait` event). Bypasses
  hook, decomposer and refine — the body must be fully conformant on its own.
- Amending `todo`/`ready` bodies in bulk: `SELECT body` → `assert old in body` → `UPDATE
  tasks SET body=?` with `body.replace(old,new,1)`; never on a `running` card (comment
  instead).
- **Parked/deferred cards:** `--triage` + full body + unassigned + a comment with the
  decision and resume path = double-parked (no spawn) — but only safe with auto-decompose
  OFF; with it ON, triage is not a holding point. Safer: `schedule <id> "reason"` (scheduled
  cards are not respawn-looped) or a gate link.
- A spec/research card does not pause the chain for the user: if the user must weigh in
  before implementation, put a second user-closed gate between it and its children at create
  time.
- **Idempotency keys:** always `--idempotency-key <board>-<item>`; re-runs return the
  existing id. Archiving frees the key; an empty-body card is archived and recreated.
- **Readiness check before releasing a gate:** per card verify every path, env var (check
  in-script defaults), endpoint (curl a cheap read), writable target dir and sibling repo
  (remote present?), then `comment <id> 'Readiness-Check: …'`. Only then complete the gate /
  assign.
- Batch order: boards create → create cards with keys → gate + links → readiness comments →
  user pulls items (`unlink` + `archive`) → `complete` gate → assign → `dispatch --dry-run`
  → dispatch → track with `list/show/runs`. Plan first as a one-question-at-a-time spec Q&A;
  record answers in `<repo>/.hermes/decisions.md`, commit + push BEFORE creating cards
  (worktrees see committed content only).
- Fan-out research: one card per source, one target file each, own worktree/branch, plus a
  synthesis card linked under all N whose body says `git fetch origin && git merge
  origin/<base>` first.
- Done criteria a worker cannot execute (GUI checklists, restarts of its own pod) go on the
  final e2e card, not on feature cards — else they block `capability`.

## Dispatch, parallelism & model pinning

- The gateway dispatcher ticks every `dispatch_interval_seconds` (60) and normally
  auto-claims `ready`+assigned cards. Manual `dispatch` is the fallback: card stays `ready`
  well past a tick, a respawn guard holds it, or the gateway is down. `--dry-run` first;
  `Spawned: 0` on a `ready` card often means the gateway already claimed it — check `list`.
  Read `Guarded (<reason>)` output (`active_pr`, `blocker_auth`, `recent_success`,
  `rate_limited`, per-profile cap, `skipped_locked`) instead of re-dispatching blindly.
- `kanban.max_in_progress_per_profile` (config knobs:
  `hermes-kanban-workers/references/config-knobs.md`) is ONE global int applied identically
  to every profile and counts ACROSS ALL BOARDS — not per board, not a per-profile mapping.
  Lowering it to 1 serializes `default` everywhere; campaigns on one profile share it (a new
  campaign's first card defers until a slot frees — normal). Cross-board parallel spawns of
  one profile have been observed even with a low cap; to run strictly one-at-a-time, create
  one card, wait for `done`, create the next.
- Fan-out lever = more profiles, each with its own `model:` block
  (`/opt/data/profiles/<p>/config.yaml`). The worker PROCESS runs locally; only the LLM call
  goes to the profile's `base_url` ("thinking on host X", not "running on X"). Clone a
  profile with `hermes profile create <p> --clone --description "…"`, edit `model.default` +
  `model.base_url` by hand, smoke-test `hermes -p <p> -z "Antworte mit genau einem Wort:
  bereit" --cli`. Lazy-loaded models cost ~100 s on the first turn. Retire with `echo <name>
  | hermes profile delete <name>` after checking `list` for its cards. Today's lanes are
  `default` + `reviewer` only — `hermes profile list` before assigning.
- **Per-card override (model-level crash recovery):** diagnose the crash class first (`show`
  → `last_failure_error`): repetition/timeout in the stream = model-level;
  worktree/safe.directory = spawn-level. Then: register the host under `custom_providers:`
  in config.yaml (edit via terminal python — the file tools refuse config.yaml;
  `yaml.safe_load` afterwards), smoke-test the exact spawn (`hermes -p default -m <model>
  --provider <name> -z … --cli`), `unblock <id>` (resets the failure counter) → `set-model
  <id> <model> --provider <name>` → `dispatch`. The override persists on the row
  (`model_override`/`provider_override`) for every respawn; `set-model <id> none` clears. A
  repetition crash is usually a card-design problem (design-heavy body) — see
  `hermes-kanban-workers` Pitfall 12 before pinning a model.
- Switching a lane's model applies at next spawn to cards without override, not to running
  workers; list running cards for that assignee across boards first.

## Review lane & merge

- Flow: worker in worktree → push → `gh pr create` → `kanban request-review <id> --summary
  "…" --reviewer reviewer` (worker-side tool `kanban_request_review`; NOT a `needs_input`
  block, NOT `kanban_complete`) → reviewer verdict (`kanban_complete` = approve,
  `kanban_comment` + `kanban_request_changes` = back to implementer, `kanban_block` =
  escalate) → the reviewer merges the card PR into the feature branch `feat/<feature>`;
  **the user merges the feature PR into `main`** (single-card fixes against `main`: user merges). Single-card work is exempt from the handoff;
  local-only repos have no PR and end with the worker's evidence block. Post-merge live
  checks are a separate `default` card gated behind the PR card.
- Reviewer requirements: post the verdict on the GitHub PR too. Same-account setups cannot
  `gh pr review --approve` (own PR) — use `gh pr comment <n> --body '✅ Reviewed and approved
  (Kanban-Review-Lane, Card <id>) …'`. Reviewer model never weaker than the worker's.
- The orchestrator does NOT code a card's fix itself: diagnose, `comment` the finding
  (`file:line` + direction), unblock/dispatch so the assignee fixes it in its branch. Exempt
  docs (`AGENTS.md`, `discussion/`, skills) may be edited directly — markdown only, code in
  an exempt folder is still code.
- A worker that self-completed (skipped review): `request-review` refuses `done`. Create a
  separate reviewer card for the open PR (SKILL.md §6), or as last resort
  `UPDATE tasks SET status='review', assignee='reviewer'` in the board DB.
- A review-lane card whose PR is still open is `respawn_guarded active_pr` every tick — park
  it with `schedule` rather than leaving it `ready`.
- "User merges" cards loop: the reviewer ends `block_loop_detected`, the card falls to
  triage, the decomposer spawns a "Review and merge" child. Archive at approve time (the PR
  is the artefact); if the child already exists, archive it FIRST, then kill its worker,
  then archive the root; verify the PR is still unmerged.
- Completion contract: `--completion-contract local-only` (default, required by the input
  gate on worktree cards) unless the repo has required status checks configured;
  `OWNER/REPO` demands a receipt per required check and returns `missing` forever on repos
  without them (and 403s on private repos without Pro). Stuck card: `UPDATE tasks SET
  completion_contract='local-only'` then `complete <id>` with merge evidence (`gh pr view
  <n> --json state,mergedAt,mergeCommit`) in the summary. No flag bypasses the gate; `edit`
  has no `--completion-contract`.
- **Pre-merge conflict preview (read-only):** from the base repo `git merge-tree
  --write-tree --name-only <A> <B>` (files), `-p` (hunks), pairwise across the wave, not
  only vs the base branch. Put the expected-conflict map + "keep both" rule into the merge
  card body. Full ladder: `conflict-analysis.md`. A child
  PR whose base was an intermediate feature-branch state must be diffed against the MERGED
  feature; prefer a single-commit rebase onto the merged base over a conflicted merge, and
  run parity checks on the full file (comments included).
- **Post-merge chain flow:** verify the merge yourself (`git fetch && git log --oneline -3
  origin/<base>`, `gh pr view <n> --json mergedAt`), fast-forward the local checkout (`git
  pull --ff-only`), then let the next child promote. If the pull aborts on the main
  session's uncommitted exempt-doc edits: commit them, `git merge origin/<base>` (not ff),
  push, verify with `git log -1` + `git status --short` ("Updating X..Y" does not prove HEAD
  moved). `git merge-base --is-ancestor <branch> origin/<base>` is NOT a merged test (a
  fresh branch with zero commits passes) — use `git rev-list --count origin/<base>..HEAD`
  plus the PR state.
- **Unpushed-commits check** after any merge/reconcile: `git log origin/<base>..HEAD
  --oneline` in the main checkout — worktrees branch from the committed state and miss a
  local-only commit.
- Resolve PR conflicts in a worktree INSIDE the repo (`git worktree add .worktrees/<name>
  origin/<branch>` → `git merge origin/<base>` → resolve, keep both sides → `git commit
  --no-edit` → push), never in `/tmp` (dubious ownership). GitHub's `mergeable` lags 15–40 s
  — poll `gh pr view <n> --json mergeable,mergeStateStatus`. Do not merge unless the user
  asked.
- Before filing a fix card, check the board (incl. `done`) and `gh pr list --state all` for
  an existing PR on the same bug; close duplicates with a comment naming the canonical one.
- Worktree hygiene for multi-card series: pre-create worktrees before dispatch on slow (NFS)
  storage; one branch per card from the fresh base, no chained branches; after a merge `git
  worktree remove .worktrees/<id>` + `git branch -D <b>` (squash merges defeat `-d`).

## Pulling back / cancelling / re-dispatching a card

**Cancel a running card (order matters):**
1. Find the ONE dispatcher-spawned worker: `ps -o pid,ppid,args` filtered on `kanban task
   <id>` — the grep matches many PIDs (shells, children); never `xargs kill` all of them.
2. `kanban archive <id>` FIRST if the card is being retired (archived cards are
   unclaimable), then `kill <pid>` (`-9` if it lingers). Kill → archive leaves a tick window
   for a respawn. Kill, reclaim and block in ONE terminal command when the card must
   survive: `kill <pid>; kanban reclaim <id>; kanban block <id> --kind <kind> <reason>` —
   reclaim alone returns the card to `ready` and it respawns next tick. After `kill -9`,
   `reclaim` may answer "not running" (claim already released) — skip it and `unblock` to
   re-gate into `todo`. Check `tasks.worker_pid` afterwards.
3. Clean the workspace: `git -C <repo>/.worktrees/<id> status --porcelain`; dirty with real
   work → `git add -A && git commit -m "wip: …" && git push origin <branch>` to bank it;
   then `git worktree remove .worktrees/<id> [--force]` and `git branch -D <branch>` if it
   has no own commits.
4. Also stop what the worker launched on target hosts (VMs, builds) — blocking the card does
   not.

**Pull a card out of a gate:** `unlink <gate> <id>` then `archive <id>`.

**Re-dispatch after a spawn failure:** `unblock <id>` resets the counter; a worktree `…
already exists` error is a dead end until the stale dir is removed (step 3), and "not inside
a git repo" means the spawner's gitconfig lacks `safe.directory` (see Hooks/Pitfalls). Then
`dispatch`.

**Failed run, but the side effect landed** (deploy done, PR merged; crash was in
evidence-gathering): do NOT re-run — it re-does the deploy. Verify the effect, then
`complete --force <id> --summary "reconciled: …"` (the card keeps a live claim after
`gave_up`; `--force` is the operator override). Record why in the summary.

**Pull a hung card to another profile:** `reassign <id> <profile> --reclaim` (plain
`reassign` refuses while running), then `dispatch`.

**Recreate a card with the same spec:** save the body first (`SELECT body FROM tasks WHERE
id=…`), archive and recreate in the SAME command batch (no tick in between — the decomposer
races), same branch name, fresh key, re-link children (`unlink` old, `link` new), `unblock`
children the breaker parked.

## Diagnosing a worker run

- `runs <id>` (attempts, outcome, elapsed), `show <id>` (events, comments,
  `last_failure_error`), `diagnostics`, `dispatch --dry-run` for "why not claimed" (then
  table each waiting card's `parents:` — `task_links` in the DB is the truth; `--json`
  `parents` can read `None`).
- Live log: `tail -c 3000 /opt/data/kanban/boards/<slug>/logs/<id>.log` — never `kanban
  tail` in the foreground. A bounded background wait that exits when the card leaves
  `running` (`notify_on_complete=true`) is fine; a sleep loop in the foreground is not.
- Scratch dirs are deleted on completion — anything to inspect must be in the card result, a
  comment, or a repo.
- Full transcript of a finished run: profile session DB (`/opt/data/state.db` for `default`,
  `/opt/data/profiles/<p>/state.db`), `sessions` row with the card title, then `messages`;
  grep for `permission|denied|dubious|safe.directory|EACCES` to find friction that silently
  ate run time.
- "running + fresh heartbeats" ≠ progress: heartbeats are process-level. For a card older
  than ~1 h check worktree mtimes (`find . -newermt …`), the session DB's last message time,
  and the LLM host's inflight view (`curl -sN <host>/api/events` → `elapsed_ms`,
  `resp_bytes` in the MB = degenerate stream). Recovery: kill the request host-side,
  `reassign --reclaim`, dispatch.
- A "worker crashed (pid gone)" ping for a PID you already killed is a stale replay — read
  `status, consecutive_failures` from `tasks` before reacting.
- "timed out (max_runtime=0s)" can be the 150-iteration budget; long remote-build cards must
  push intermediate commits and leave a checkpoint comment so a retry resumes from git.
- Board-level forensics (deletion claims, which board a run used, UI vs backend):
  `keep-board-forensics.md`.
- Never trust a self-report: "not pushed" (`git rev-parse <b> origin/<b>`), "PR merged" (`gh
  pr list --state all --limit 5`, `git log <base>..origin/<base>`), files landed (`ls`, `git
  status`). Read the full `show` for `needs_input` cards — the summary line truncates.

## Durable worker policy

Two layers: isolation is structural (the dispatcher pins `TERMINAL_CWD` to the task
workspace — cannot be forgotten); policy is an instruction and must live where every run
reads it. A per-card comment covers one card only. The durable place is the assignee
profile's `MEMORY.md` (`/opt/data/profiles/<p>/memories/MEMORY.md`; active profile via the
`memory` tool, other profiles by direct file edit with `cross_profile: true`), injected into
every worker run of that profile (workers run without `--ignore-rules`). Write it
declarative ("investigation cards: repo read-only, deliver the result as card result; code
only via card→worktree→branch→PR"), keep it under the char budget by consolidating, and
never anchor transient state (open cards, SHAs) there. Repo-wide rules go into the repo's
`AGENTS.md` (injected to every worker in that repo). If a worker ignores a policy, check the
profile's MEMORY.md first, then the spawn path.

## Hooks

The input gate is a `pre_tool_call` hook that blocks non-conformant `kanban create`/`swarm`
from the terminal tool (rules R1–R8, overrides, template, retrofit:
`hermes-kanban-workers/references/input-gate.md`; hook schema, consent, testing:
`keep-hooks.md`). What those two do not say: the hook matches only terminal-type tools
(`terminal, shell, run_command, bash`) — `execute_code`/`subprocess` creates bypass R1–R8
entirely, so the body must be conformant on its own; the Rules-Block marker only skips the
legacy L1/L2 checks. The hook-owning process must be the one executing YOUR terminal tool
(in this deployment the chat terminal may run under the webui `server.py`, not the gateway)
— "registered" in the gateway log is not proof it fires for your session; test with one
deliberately non-conformant command. `pre_auxiliary_call` and kanban lifecycle hooks are
observer-only; the only deterministic block point is `pre_tool_call`. A gate wrapper
(`kanban_specify_gate.py`: specify + deterministic rules check + idempotent rules-block
append; `--check --all` audits the board) remains the second net at triage→todo.

## Pitfalls (deduplicated)

- `$H`/`$VAR` indirection and `$(…)` substitution in terminal commands trip the security
  scanner (noise, sometimes a hard block). Inline the binary path; use
  `read_file`/`search_files` instead of `sed -n "$(grep …)p"`.
- Card bodies are the worker's only context: absolute paths, env facts, host login line,
  done criteria, dependency info. The WHAT, not the HOW (goal, access, decision pointers,
  success criteria) — but a design-heavy "diagnose and decide" body makes the model loop;
  ship execute-only cards with the fix known.
- Shared files across two cards → link parent→child; parallel code → worktree per card.
  Separate workspaces do not protect a shared repo.
- Untracked files in the base repo are invisible to worktrees — commit first or `cp` into
  the worktree and say so in the body.
- Committing to the base branch while a worktree worker edits the same file makes its PR
  conflict; link the doc work as a parent or hand the worker the exact merge instruction via
  comment.
- `dir:` cards share tree/index/HEAD with the main session: read-only only; after a `dir:`
  worker, `git status` the checkout for edits it left uncommitted. A `dir:` card pointing at
  a deleted worktree breaks every later terminal call (`cd: No such file`) — pass an
  explicit `workdir`.
- `safe.directory`: repos owned by another uid fail with "dubious ownership" in EVERY git
  context — gateway (`HOME=/opt/data` → `/opt/data/.gitconfig`), session
  (`/opt/data/home/.gitconfig`), each worker profile home
  (`/opt/data/profiles/<p>/home/.gitconfig`). Add `directory = <repo>/.worktrees/*` (bare
  `.worktrees` does not match subdirs) INSIDE the `[safe]` section of all of them, plus
  `[credential] helper = store --file /opt/data/home/.git-credentials` in profile homes.
  Diagnose as the spawner: `env -i HOME=/opt/data PATH=/usr/bin:/bin git -C <repo> rev-parse
  --show-toplevel`. Symptom of the gap: worktree cards auto-block after 2× `spawn_failed`
  "not inside a git repo" or "already exists".
- Respawn guard `active_pr` holds a `ready` card 24 h after any comment quoting a PR URL;
  `unblock` does not clear it. Lifters: a real handoff event after the newest PR comment
  (`assign` to a DIFFERENT profile — bounce `assign <id> reviewer` then `assign <id>
  default` — `changes_requested`, `review_reopened`) or ageing the rows: `UPDATE
  task_comments SET created_at = created_at - 86400 WHERE task_id='…' AND body LIKE
  '%github.com/%/pull/%'` (the guard scans `task_comments`, not `task_events`), then
  `dispatch`.
- Respawn guard `blocker_auth`: a stale `tasks.last_failure_error` ("rate-limited (quota
  wall)") from an earlier run parks a later review handoff forever. `UPDATE tasks SET
  last_failure_error=NULL WHERE id='…'`, then `dispatch` (check the newest run is not itself
  rate-limited).
- Auto-decompose rewrites bodies and builds its own parent→child edges, sometimes in the
  wrong order (review before test). After any decompose, verify each child's parents and fix
  with `unlink`; accept auto-created sub-cards only if they match the parent's body and
  current decisions. A duplicate chain: `reclaim` the running child, then `archive` every
  open member.
- Workers can `kanban_create` follow-ups whose only parent is themselves; link them into the
  chain before they dispatch (put the link rule in every card body).
- Completing a parent auto-promotes children and can respawn a root/verify card whose work
  already happened out-of-band — pre-block destructive cards `needs_input` before the last
  parent completes.
- `request-review` with a body that says "no push" conflicts with a "PR merged" done
  criterion — the worker stops at a local commit.
- Workers cannot write protected context files (`AGENTS.md`) or run `ssh … sudo tee /etc/…`
  headless; the card blocks `needs_input`. Let the worker leave a draft / ship an idempotent
  repo script, finish from the main session, comment the evidence, `unblock` +
  `request-review --force`.
- A board-mutating script must never be test-run on a live board; a watchdog false-positive
  once completed a running card and spawned its child on an unmerged base.
- Corrupt `kanban.db` ("wrong # of entries in index"): `REINDEX` + `PRAGMA integrity_check`
  via Python before restoring the `.bak` — data is usually intact. Mid-batch corruption
  leaves half the batch unblocked; re-`list` afterwards. (Skill: `kanban-db-repair`.)
- `sessions` in profile `state.db` has no `last_activity_at` — use `started_at` + latest
  `messages` timestamp.
- Reference cards to the user as column + title, not `t_<hex>`; the status line under a card
  in the UI is the last event, not the state.
- Two parallel workers on a low-VRAM host produce degenerate streams: a resource problem,
  not a model-quality problem — serialize via links or route to the stronger host.
- Never ask the user to approve an infra action you cannot perform from the sandbox (no
  kubectl, SA token unreadable); hand over the exact one-liner and list the checks you will
  run afterwards.

