---
name: hermes-kanban-ops
description: "Operate Hermes kanban boards from a NORMAL session via the hermes kanban CLI: boards, card lifecycle, gate-parent pattern for todo, manual dispatch, workspace modes, parallelism caps, review-blocked cards."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [Hermes, Kanban, Multi-agent, CLI]
    related_skills: [hermes-agent, hermes-kanban, github-code-review]
---

# Hermes Kanban — Board Operations from a Normal Session

Use this when driving a kanban board from a regular chat/CLI session (the `kanban_*`
tools are worker-gated and absent here — the CLI is the interface).

Hook schema for blocking `pre_tool_call` hooks (input-gate enforcement):
`references/hooks.md`. Live-installing/verifying a plugin built on a board:
`references/plugin-live-install.md`.

**Why the CLI (two-surface design, verified in v0.19.0 source + official docs):**
normal sessions have ZERO `kanban_*` tools by design ("zero schema footprint on
normal sessions" — docs). The `kanban` toolset is NOT in `_HERMES_CORE_TOOLS`;
it is opt-in for orchestrator profiles via `hermes tools enable kanban` (writes
`platform_toolsets`). Gotcha: the runtime gate `_profile_has_kanban_toolset()`
in `tools/kanban_tools.py` reads the TOP-LEVEL `toolsets:` key, NOT
`platform_toolsets` — so enabling for a session may require both keys
(`toolsets: ["hermes-cli", "kanban"]`). A session with the toolset enabled gets
board tools (`kanban_list`, `kanban_unblock`, …) directly instead of shelling
out; dispatcher-spawned workers always get task-scoped tools via
`HERMES_KANBAN_TASK` regardless of config. Don't explain the absence of kanban
tools as a bug — it's the documented default.

CLI: `/opt/hermes/bin/hermes kanban …` (not on PATH in the sandbox).

## Core Loop

```bash
H=/opt/hermes/bin/hermes
$H kanban boards create <slug> --name "…" --description "…" --icon "🔁" \
  --default-workdir /abs/repo --switch
$H kanban create "Title" --body "…self-contained spec with ABSOLUTE paths…" \
  --idempotency-key <stable-key> --json     # batch-safe dedup
$H kanban specify <task_id>                 # triage -> todo (LLM refine, SLOW)
$H kanban assign <task_id> <profile>
$H kanban dispatch --dry-run                # ALWAYS preview first
$H kanban dispatch                          # real pass: reclaim/promote/claim/spawn
$H kanban list                              # status: ◻ todo ▶ ready ● running ⊘ blocked ⏱ scheduled ✓ done
$H kanban show <task_id>                    # body + comments + events + runs
$H kanban runs <task_id>                    # attempt history (profile, outcome, elapsed)
```

## Card Lifecycle

`triage → todo → ready → running → done` (+ `blocked`, `scheduled`, `archived`).
- `triage`: parked, not yet specified. **The only `triage → todo` CLI verb is
  `kanban specify <id>`** — `promote` and `unblock` both refuse triage cards.
  **Sanctioned entry in this sandbox:** the gate wrapper
  `/workspace/dev/repos/ours/kanban-tools/kanban_specify_gate.py <id>` (specify +
  deterministic rules check + idempotent rules-block append) — standing user
  rule: raw `kanban specify` bypasses the check and is not allowed
  (`--check <id>` / `--check --all` audit without an LLM call).
  Gotcha: `specify` runs an LLM refine pass that can retitle/reformat the
  card and takes ~60–90 s per card — run multi-card promotion loops in the
  background, not foreground.

**Direct-DB create path (hook + decomposer + refine all bypassed):** when the
body is already a complete, hand-written spec (Quality-Gate rules block +
verifiable Done-Kriterien checklist) and the card must NOT be auto-decomposed,
skip the CLI entirely and call `create_task` from `hermes_cli.kanban_db`
directly against the board DB (`/opt/data/kanban/boards/<slug>/kanban.db`):
`create_task(conn, title=…, body=…, assignee="default", created_by="…",
workspace_kind="worktree", branch_name="feat/…", idempotency_key="…",
board="<slug>")` then `conn.commit()`. With no parents the card lands
`ready` immediately and — because an assignee is set — the gateway
dispatcher claims + spawns it on the next tick (~60 s) without any manual
`dispatch`.
**Gated batch in one script (whole planned chain, nothing dispatches):**
(1) set `conn.row_factory = sqlite3.Row` BEFORE the first `create_task` —
it reads `row["id"]` internally and crashes on tuple rows; (2) create the
gate with `initial_status="blocked"` and NO assignee (`initial_status`
accepts only `blocked`/`running`; to get `todo` you pass `parents=` instead);
(3) create each work card with `parents=[gate, <prior card ids>]` — an open
parent lands it in `todo` atomically, no separate `link` step and no ready
window; (4) one `conn.commit()`; (5) verify one leaf with `kanban show`
(`workspace: worktree @ <repo>`, all parents, `dependency_wait` event).
Release later with `kanban complete <gate>`. Commit+push any spec/decision
files the cards reference before creating them (pitfall 9).
For private repos set `completion_contract="local-only"`; public repos may
use `OWNER/REPO`. This is the cleanest decomposer-proof create path: the hook
(which only sees the raw command string and cannot read a `$(cat …)`/`$BODY`
body, pitfall 18) is never in the path, the card never sits in triage (no
decomposition window, pitfall 15), and there is no LLM refine pass to mangle
the body. Use the CLI path instead when the body is still a draft that needs
the specify wrapper's Judge + rules-block append.
**Amending card bodies of unclaimed cards (`todo`/`ready`) after create:** there is no edit verb, so read and update the board DB directly. Per card, run `SELECT body FROM tasks WHERE id=?`, then `assert old in body`, then `UPDATE tasks SET body=?` with `body.replace(old, new, 1)`. Run all affected cards in one script with one commit. The assert matters because a silent no-op replace leaves the worker on the old spec. Never touch a `running` card this way, because its worker already read the body; comment on it instead.

**Interpreter gotcha (cost a retry):** run this script with the Hermes venv
interpreter — `/opt/hermes/.venv/bin/python3` — NOT bare `python3` (the
sandbox system python at `/usr/local/bin/python3` lacks `ruamel.yaml` and
`import hermes_cli.kanban_db` dies with `ModuleNotFoundError: No module named
'ruamel'` before any board code runs). The venv python is the one the
`/opt/hermes/bin/hermes` shebang resolves to; it has every `hermes_cli` dep.

**Fast path (no LLM, body stays verbatim):** call the pure DB function
  directly instead of the CLI — `specify_triage_task(conn, task_id,
  author="…")` does `triage → todo` in one write txn with NO refine pass
  (title/body/assignee only change if you pass them). Use this when the card
  body is already a complete spec and you want to promote many cards quickly
  without the ~90 s/card LLM cost or risk of the refine mangling a
  hand-written body.
- `todo`: spec complete but waiting (usually on open parents).
- `ready`: all parents done; dispatcher can claim+spawn when an assignee is set.
- `scheduled`: parked by time, not input (use for explicitly deferred items).
- `blocked`: worker or human stopped it; `--kind capability|dependency|needs_input|transient`.

## Pitfalls (proven 2026-09-29)

1. **No ready→todo demote verb exists.** To hold a batch of cards in `todo`,
   create a **gate parent card** and `kanban link <gate> <child>` each child —
   children auto-drop to `todo` while the parent is open. `kanban complete <gate>`
   → dispatcher promotes children back to `ready` on the next tick.
   `unblock` only transitions `blocked`/`scheduled` → ready/todo; it does NOT demote.
2. **The gateway dispatcher may not tick on its own** even when the gateway runs
   (observed: cards sat `ready`+assigned for minutes). Don't wait — run
   `hermes kanban dispatch` manually after assigning. `--dry-run` shows exactly
   what would spawn (count + workspace paths) with zero side effects.
   **Conversely, the gateway MAY auto-claim a `ready`+assigned card within ~60 s
   of `unblock`/`assign`** — before a manual `dispatch`, check `kanban list`: if
   the card already shows `running`, no manual dispatch is needed. A `--dry-run`
   showing `Spawned: 0` on a `ready`+assigned card means the gateway already
   claimed it, NOT that it is stuck.
3. **Workspace modes decide collision safety** (set at `create` time via `--workspace`):
   - `scratch` (default): own dir per task, **EPHEMERAL — deleted on task completion**
     (dispatcher emits a `tip_scratch_workspace` event). Fine for research; worker
     output does not survive. Cards still reach real paths via absolute paths in the body.
   - `worktree`: isolated git worktree + branch per task — the mode for **parallel
     code changes**; results come back as branch/PR.
   - `dir:/abs/path`: the shared directory itself — **sequential work only**;
     parallel workers on the same `dir:` collide on the same checkout.
4. **Parallelism is unbounded by default.** The only cap is
   `kanban.max_in_progress_per_profile: N` in config.yaml (default `null` = unlimited
   per profile; observed 4 parallel spawns). Manual passes: `dispatch --max N`.
   Multi-profile assignment is the intended fan-out lever (cap is per profile).
   The cap is GLOBAL per profile across ALL boards — it is NOT a per-board cap
   (user-confirmed 2026-10-07; lowering it to 1 would also limit `default` to
   1 parallel everywhere, which is why it stays high). Related:
   `dispatch_interval_seconds` (default 60), `failure_limit` (default 2).
5. **`needs_input` blocks are reviews, not failures.** A worker that finished and
   wants human sign-off (e.g. before pushing) blocks with `kind: needs_input` and a
   summary. Do NOT auto-unblock — surface the summary to the user, then either
   `kanban unblock <id>` (user approved) or comment feedback and re-assign.
6. **`boards show` takes no arguments** (prints current board); use `boards list`
   or the global `--board <slug>` flag before the verb.
7. **Card bodies must be self-contained** — workers get no chat context. Include
   absolute paths to repos/files, API endpoints, env var names, and the definition
   of done. Verify every referenced path/env/endpoint exists BEFORE dispatch
   (readiness check) and record the result as a `kanban comment` per card.
8. **Dependent cards (shared files/docs) must be linked parent→child** so they
   run *sequentially*, not in parallel. Two parallel workers editing the same
   file (e.g. both touching ROADMAP.md / the same script) race on the same
   checkout even in `worktree` mode — the worktrees diverge and the merge
   becomes a manual conflict. Link the later card `--parent <earlier-card>` and
   let it promote only after the parent is `done`.
9. **Untracked files in the base repo are INVISIBLE to a worker's worktree.**
   A `worktree` checkout is a fresh git worktree — it sees committed content
   only. If a file was created but never committed (e.g. a freshly written
   `AGENTS.md` showing as `?? AGENTS.md`), a worker's worktree will NOT contain
   it, and any card that must commit/edit it will silently fail. Either commit
   the file to the base repo first, or add an explicit step to the card body:
   `cp /abs/base/repo/<file> .` before the worker commits it.
10. **`kanban complete` refuses `triage` and `todo` cards** — it only accepts
    `running | ready | blocked` (transition `→ done`). Completing a card that
    is still in `triage`/`todo` returns `cannot complete <id> (unknown id or
    terminal state)`. When you do a piece of work yourself (e.g. exempt-doc
    edits the main session makes directly) and need to close the card, the
    sequence is: promote it out of `triage` first (CLI `specify <id>` for one,
    or the pure-DB `specify_triage_task` + `recompute_ready` loop for a batch —
    see the fast path above), then `kanban complete <id> --result "…"`. Do the
    whole promote+complete in one Python script against the board DB so the
    state machine stays consistent: `specify_triage_task(conn, tid)` →
    `recompute_ready(conn)` (promotes parent-free/parent-done todos to `ready`)
    → `complete_task(conn, tid, result=…)`, then `conn.commit()`.
11. **`git merge-base --is-ancestor <branch-head> origin/master` is NOT a
    "PR was merged" test.** A freshly branched worktree with zero own commits
    has HEAD == master HEAD, and a commit is its own ancestor — the check
    returns true for a branch that has no PR at all. A watchdog built on it
    falsely completed a card and spawned the next one mid-flight (2026-09-29
    incident; recovery = kill workers, discard uncommitted worktree work,
    archive + recreate the card with the same body/branch, re-link, unblock).
    Verify merges with `gh pr view <n> --json mergedAt` or the merge commit in
    `git log origin/master`, plus `git rev-list --count origin/master..HEAD`
    (>0 = branch has own commits).
12. **Worktree spawn failure "…already exists" is a dead end — `unblock`
    alone never fixes it.** If a previous spawn died mid-`git worktree add`
    (killed worker, half-created dir), the dir `.worktrees/<id>` survives and
    every later spawn fails `fatal: '…' already exists` until the dir is gone
    (proven 2026-09-29, card t_28301c34). Recovery: check
    `git -C .worktrees/<id> status --porcelain` first — **two cases**:
    (a) **empty** (nothing to salvage) → confirm the checked-out commit is on
    `origin/master` (safe to delete the branch), then `git worktree remove
    .worktrees/<id>` + `git branch -D <branch>`;
    (b) **dirty with real uncommitted work** (the worker finished or nearly
    finished but the dispatcher re-spawned and hit "already exists") → **do NOT
    delete the work first.** `git add -A && git commit -m "wip: …"` +
    `git push origin <branch>` to bank the work on the branch, THEN remove the
    worktree. The next spawn re-checks-out the branch (now with the WIP commit)
    and the worker resumes from there instead of re-doing the work. In both
    cases finish with `kanban unblock <id>` (resets the failure counter) +
    `kanban dispatch`. Distinct from the safe.directory variant (error says
    "not inside a git repo" — fix the gateway user's gitconfig instead).
13. **Worktree git access: every process context needs `safe.directory` on the worktree dir itself — and the wildcard must be in BOTH gitconfigs.** Reviewer dispatch reuses the implementer's worktree; the reuse check runs `git -C <worktree> rev-parse` as the GATEWAY process. If the worktree dir (`.worktrees/<id>`) is not in that process's `safe.directory`, git fails with "dubious ownership", the code falls through to `git worktree add` → `fatal: '…' already exists` → `spawn_failed` ×2 → auto-blocked. Root cause in this sandbox: repos under /workspace/dev/repos are owned `nobody` (uid 65534) while gateway + workers run as `hermes` (uid 10000) — an ownership mismatch, so EVERY git context hits it, not just the reviewer. Each context reads the gitconfig of ITS OWN HOME: gateway `HOME=/opt/data` → `/opt/data/.gitconfig`; main-session profiles `HOME=/opt/data/home` → `/opt/data/home/.gitconfig`; **worker-spawned runs get `HOME=<profile home>` = `/opt/data/profiles/<profile>/home/`** (dispatcher sets `HERMES_HOME` to the profile root; the terminal tool anchors HOME there) → gitconfig `/opt/data/profiles/<profile>/home/.gitconfig`. Add `safe.directory = <repo>/.worktrees/*` (or the whole-workspace `/workspace/*`) to ALL FOUR — git supports `*`, but a bare `.worktrees` entry WITHOUT `/*` does NOT match subdirs, and workers then self-heal by adding per-task paths one run at a time (silent wasted run time; the user flagged this as recurring friction). INI gotcha: appending `directory = …` lines at end-of-file lands them in the LAST section (often `[credential]`) where they are IGNORED — insert inside the `[safe]` section. Worker profile homes also LACK git credentials: a reviewer/worker running `git ls-remote`/`fetch` hits `fatal: could not read Username for 'https://github.com'` (observed 2026-10-01, reviewer run on t_793e294e) — fix by adding `[credential] helper = store --file /opt/data/home/.git-credentials` to the profile-home gitconfig (reuses the main credential store, no token duplication). `gh` works in workers regardless (it resolves hosts.yml via the profile's own `.config/gh` or inherited env). Verify per context: `env HOME=/opt/data/profiles/<profile>/home git -C <worktree> rev-parse --git-dir` and `… git ls-remote https://github.com/Big-Whoop/llama-swap.git HEAD`. **Whole-workspace wildcard (proven 2026-10-01):** `safe.directory = /workspace/*` in BOTH gitconfigs covers every repo, worktree and scratch dir under the NAS share. Git 2.47 wildcard semantics (isolated-verified with empty global config): the pattern is matched against ANCESTOR dirs of the repo path — `/workspace/*` matches, but plain `/workspace`, `/workspace/` and `/workspace/**` do NOT. `chown` is NOT a fix in this sandbox: /workspace is a NAS5 NFS share owned by `nobody` and the container runs as `hermes` without CAP_CHOWN (CapEff 0) — `chown` fails "Operation not permitted" even with sudo (verified 2026-10-01). The safe.directory wildcards are the permanent in-container solution.
14. **After a worker-PR merge, the main checkout's `git pull --ff-only` can
    fail on the main session's own uncommitted exempt-doc edits** (AGENTS.md,
    discussion/, skills/ — the files the main session is allowed to edit
    directly, which tend to be exactly the files merged PRs also touch).
    Recovery: `git diff --stat` to confirm the local changes are yours and
    exempt, `git add` + commit them, then `git merge origin/master` (NOT
    `--ff-only` — the local commit already diverged history), resolve if
    needed, `git push origin master` so GitHub and the local checkout
    re-converge. Verify the merge result with `git log --oneline -3` AND
    `git status --short` (a "Updating X..Y" line in pull output does NOT
    mean HEAD moved — check `git log -1`).
15. **Auto-decompose races the gate: it decomposes triage cards on the ~60 s
    dispatcher tick, so a card you are still reworking in triage can be
    decomposed mid-flight.** Observed: a gate-rejected card was decomposed
    into a 5-card chain (in the LLM's own language, in `scratch`
    workspaces — against the board rules) in the gap between rejection and
    archive, running in parallel with the correctly recreated card → two
    chains editing the same files. Rules: (a) when you must recreate a
    card, `archive` the old one in the SAME command batch as the recreate
    (no tick in between); (b) the moment a card is created in triage and
    you intend to specify it, run the gate wrapper immediately — every tick
    it sits in triage is a decomposition window; (c) if a duplicate chain
    is discovered, stop it surgically: `reclaim` the running child first
    (releases the claim so the dispatcher won't respawn), then `archive`
    every open chain member; `done` members can stay as history (they did
    no harm) — but verify they only did research.
16. **After any auto-decompose, VERIFY the dependency graph against your
    intended sequence before dispatching.** The decomposer LLM builds the
    parent→child edges itself and can get the ORDER wrong (observed: it
    placed PR-REVIEW before the runtime test of the PR, when the intended
    flow was test-first; the review card then sat `ready` permanently
    guarded and blocked the whole downstream chain). Check each child's
    `parents:` with `kanban show`; fix wrong edges with
    `kanban unlink <parent> <child>`. Also: a review-lane card whose PR is
    still open gets `respawn_guarded {'reason': 'active_pr'}` every tick and
    will NEVER dispatch while the PR is open — if it must wait, park it
    explicitly with `kanban schedule <id>` (scheduled cards are not
    respawn-looped) instead of leaving it `ready` and accumulating guarded
    events.
17. **`kanban reclaim <id>` transitions the card to `ready`, not `todo`** —
    it releases the claim but leaves the card dispatchable (it promotes on
    the next tick if all parents are done and an assignee is set). To hold a
    reclaimed card behind a gate: `kanban link <gate> <id>` in the same
    batch — linking an open parent drops it `ready → todo` automatically
    (the CLI prints the transition). Related: `kanban block <id>` takes
    NO `--reason` flag (reason goes via `kanban comment`).
18. **The quality-gate `pre_tool_call` hook parses the RAW command string (shlex) — it cannot see `--body-file`, shell variables (`BODY=$(cat f); … --body "$BODY"`), or script wrappers (`bash create.sh`)** — the
    hook runs at tool-call time and reads only the command string, so
    `kanban create … --body-file x.md` fails with "Body fehlt" even though
    the file exists. And inline `--body` must already contain the full
    rules block + verifiable done-criteria or the hook blocks it too. The
    sanctioned path is the one the hook's error message tells you: create
    with `--triage` and EMPTY body (always allowed), then run
    `kanban_specify_gate.py <id>` (LLM refine + deterministic rules check +
    idempotent rules-block append). The wrapper also runs an LLM Judge that
    REJECTS non-conformant cards (e.g. code-change card anchored to
    `scratch` workspace → reject, card stays triage) — re-create with
    `--workspace worktree` and re-run the wrapper. After the wrapper passes,
    the card lands `ready` but UNASSIGNED — `dispatch` skips unassigned
    cards, so `kanban assign <id> <profile>` is a required final step.
    **Escape hatch — a card that must NOT be auto-decomposed (user: "don't split it") must NOT be created in triage at all.** Triage is the decomposer's input queue (pitfall 15); parking there hands the card to the decomposer LLM on the next tick. Instead create it DIRECTLY in `todo` with a conforming inline body (the hook enforces the rules block + done-criteria at create time, so the specify wrapper is not needed — note in the rules block that the Triage→Todo input gate is bypassed by design). Link its parent in the SAME batch (`kanban link <parent> <id>`) to hold it behind a dependency — linking an open parent drops it `ready → todo` automatically. This is the only create path that is both hook-conformant and decomposer-proof.
19. **Killing a worker does NOT stop the card — the dispatcher re-claims killed running cards on the next tick.** Observed: killing 4 worker PIDs left the cards `running` and the gateway re-spawned 3 of them within one tick. Correct order to stop a card for good: `kanban archive <id>` FIRST (archived cards are unclaimable), THEN kill the worker PID. The reverse order (kill → archive) leaves a tick window in which the dispatcher respawns. Same rule for cancelling: archive is the durable stop, kill is only cleanup.
20. **Cross-board parallel spawn: creating multiple `ready` cards with the same assignee on DIFFERENT boards spawns them in parallel** — the gateway dispatcher ticks every board, and in practice observed parallel spawns across boards even with a low per-profile cap (2026-10-07: 4 cards of one profile across 4 boards → 4 concurrent workers). Do NOT rely on the cap to serialize cross-board work. To run one-at-a-time: create exactly ONE card, dispatch it, wait for its `done`, then create the next. If a parallel spawn did happen: archive the extra cards first, then kill their PIDs (pitfall 19 order).
21. **The quality-gate `pre_tool_call` hook blocks even `kanban create --help`** (it parses every terminal command for the create op and finds no body). To discover create/dispatch flags, read the parser source (`/opt/hermes/hermes_cli/kanban_parser.py`) instead of running `--help` in the terminal tool.
22. **`kanban complete` refuses a card that still holds a LIVE worker claim, even after the run "gave up".** A crashed/loop-stopped worker that hit the failure limit leaves a `gave_up` event but the task can retain its claim (status may even read `ready` after an `unblock`). `kanban_complete` then returns `refused: <id> is running under a live worker claim; pass expected_run_id … or force=True`. This is NOT a state-machine bug — it is the ownership guard. To reconcile such a card (the work actually landed, the crash was in evidence-gathering, not the deploy): close it as an operator override with `hermes kanban complete --force <id> --result "…"`. Do NOT re-run the card to "finish" it — re-dispatching a card whose side effects already landed re-does a deploy/switch. Verify the side effect really landed (generation, unit state, merged PR) BEFORE force-completing, and record that reconciliation in the `--result` text so the audit trail explains why a crashed card closed clean.
23. **Resolve PR merge conflicts in a worktree INSIDE the repo (`.worktrees/<name>`), never in `/tmp`.** A `/tmp` worktree hits `dubious ownership` (repo files owned by a different UID than the session user; `/tmp` is outside any `safe.directory` wildcard like `/workspace/*`, and adding a `/tmp` exception to the gitconfig is more churn than the worktree it protects). Inside the repo the existing wildcards cover it. Recipe: `git worktree add .worktrees/<name> origin/<branch>` → `git checkout -B <branch>` → `git merge origin/master` → resolve → `git add` + `git commit --no-edit` (keep the auto-generated merge message) → `git push origin <branch>`. Add-Add conflicts in docs (two branches appended different sections at the same spot): keep BOTH sections, delete only the three conflict markers. GitHub recomputes `mergeable` a few seconds after the push — poll `gh pr view <n> --json mergeable,mergeStateStatus` (expect `MERGEABLE`/`CLEAN`), and do NOT merge the PR yourself unless the user asked — a card-less branch has no review-lane handoff, so merging is a user/reviewer decision (state it explicitly in the report).
24. **sqlite3 rows are tuples without a row factory — `dict(row)` crashes.** When driving the board DB directly from Python (`create_task`, `specify_triage_task`, `recompute_ready`), a bare `conn.execute(…).fetchone()` returns a plain tuple; `dict(row)` then raises `ValueError: dictionary update sequence element … has length …`. Set `conn.row_factory = sqlite3.Row` first, or `SELECT` the columns you need by explicit name and read them positionally. Verify card state after a direct-DB write with an explicit-column `SELECT` (id, status, assignee, workspace_kind, branch_name, idempotency_key) — a misaligned positional read can look like the card was created with the wrong status/workspace when it was actually created correctly.

25. **A spec/research card does not pause the chain for the user: the reviewer merges it and its children promote on the next tick.** If the user must weigh in on the card's findings (open questions, design answers) before implementation starts, put a SECOND user-closed gate between the spec card and its children at create time. A promise to "report when it reaches review" is not enough, because the whole chain can merge before the user answers. Corrections found after the merge become a new card linked before the e2e card. Do not request changes on a `done` card.
26a. **Never ask the user to approve an infra action you cannot perform from the sandbox (container/pod restart, k8s scale): there is no kubectl and the pod service-account token is unreadable.** Prepare everything else (symlink, config edit with backup + YAML validation), then hand the user the exact one-liner and list the post-restart checks you will run.
26. **Done criteria a worker cannot execute (manual Desktop/GUI checklists, screenshots, anything that needs a user-side app or a gateway restart) belong on the final e2e card, not on each feature card.** Workers have no Desktop, so the feature card blocks `capability` and stalls the chain. At create time, scope feature cards to code + automated checks (pytest, smoke scripts) and collect the manual checklists plus the install prerequisites on the e2e card. If a card is already blocked this way and the user defers the check: comment the waiver on the card, comment    the deferred checklist on the e2e card, then run `unblock` followed by `request-review <id> --force --reviewer reviewer --summary "…"`.
27. **Before creating a fix card, list the board (including `done`) and `gh pr list --state all` for an existing card/PR on the same bug.** Another session working the same board can file and merge the same fix minutes earlier; a second worker then branches from a stale base, conflicts, and its tests contradict the merged design — wasted run plus a user decision. If a duplicate is found after the fact: close the redundant PR with a comment naming the canonical one, comment the card, `archive` it.
28. **Workers cannot write protected context files (`AGENTS.md` and similar) — the protected-file guard needs approval in an interactive session, so the card blocks `needs_input` with a draft path.** Handle it from the main session: read the draft, check it against the code, copy it into the card's worktree (`<repo>/.worktrees/<id>`), commit + push on the card branch, comment the approval on the card, then `unblock` + `request-review <id> --force --reviewer reviewer`. To avoid the stall, state in the card body that the worker should leave such files as a draft for the main session.

29. **`unblock` of a card that already has a PR URL in a comment leaves it `ready` but never spawned (`respawn_guarded {'reason': 'active_pr'}` every tick).** The guard prevents a duplicate PR. It is lifted only by a REAL handoff event after the newest PR comment: `assigned` to a DIFFERENT profile (`from != to`), `changes_requested`, or `review_reopened`. A no-op `assign <id> default` while already `default` does NOT count. To send the implementer back to its own open PR (e.g. after a user decision), bounce the assignee: `kanban assign <id> reviewer` then `kanban assign <id> default`, then `kanban dispatch`. Watch loops that only wait for done/blocked miss this stuck `ready` state — check the card's events too.
30. **A card handed to review after earlier rate-limited runs never gets a reviewer (`respawn_guarded {'reason': 'blocker_auth'}` every tick).** The implementer's earlier `rate_limited` run stamped `tasks.last_failure_error` ("…rate-limited (quota wall)…"). The later successful run ends `review_requested` (not `rate_limited`), so the rate-limit early-return no longer applies and the stale text matches the quota/auth blocker regex — the review lane is held forever although quota is back. Fix: clear the stale field for that card (`UPDATE tasks SET last_failure_error=NULL WHERE id='<id>' AND status='review'`), then `kanban --board <b> dispatch`. Check first that the newest run is NOT itself rate-limited.
31. **"User merges" infra cards: the review lane loops and the auto-specify/decomposer can rewrite the merge rule away.** A reviewer that may not merge ends with `block_loop_detected`; the card falls back to triage, the specify pass rewrites the body (observed: "Peter merges" became "merge is done by Peter or the reviewer") and the decomposer spawned a child "Review and merge … PR". Stop it in this order: `archive` the merge child FIRST, then kill its worker; archive the parent too if it keeps re-entering review (archive also terminates the worker). Then verify the PR is still unmerged. Track the "waiting for user merge" state outside the looping card (comment + main-session follow-up), not by leaving the card in `review`.
32. **A worker blocked on "origin/main moved backwards / force-reset" may be reading a transient state.** Before relaying the question to the user, check the repo's ref history: `gh api repos/<owner>/<repo>/activity -q '.[:8][]|"\(.timestamp) \(.activity_type) \(.ref) \(.before[:7])->\(.after[:7])"'` plus `git merge-base --is-ancestor <expected-sha> origin/main`. If the reset was already reverted, comment the facts on the card, `unblock`, and let the worker do the original rework — no user question needed.
33. **Background watch loops die on a container restart (exit -15/SIGTERM) while the cards keep running.** On such a notice check `ps -o lstart= -p 1` against the time, re-read the board state, and re-arm the watch in the same turn. Watch for every terminal state you care about (`done|blocked|review`), and record per-card start states so a card already in `review` does not fire immediately.

## Board Selection (proven 2026-10-01 — two wasted card recreations)

`kanban create` always lands the card on the **ACTIVE board** (whatever
`boards switch` last set), and a `worktree` workspace anchors to that
board's `default_workdir` — NOT to the repo named in the card body. A card
for repo X created while board Y (workdir = repo Y) is active spawns its
worker in Y's worktrees. There is **no move-verb between boards** (each
board is its own DB). Rules:
- One board per repo/workstream, created with the right
  `--default-workdir <abs repo>`; use `--board <slug>` on EVERY verb
  (create/show/list/dispatch/link) instead of switching the active board
  (switching is session-global and surprises the next command).
- After creating a worktree card, verify the anchor BEFORE dispatch:
  `kanban --board <slug> show <id>` must show `workspace: worktree @
  <expected-repo>`. If it shows the wrong repo, the card is on the wrong
  board — archive it and recreate on the right board (see pull-back recipe
  below) rather than hoping the worker's body paths save it (the worktree
  checkout is the wrong repo's, so the worker edits the wrong tree).

## Pulling Back a Running Card (cancel recipe, proven)

When a card must be cancelled while its worker is live:
1. Find the worker PID: `ps aux | grep <task-id> | grep -v grep` (the spawn
   cmdline contains `work kanban task <id>`). ⚠️ **Kill surgically — this grep
   matches MANY PIDs** (the dispatcher spawn, the worker's bash shell, its child
   processes, and anything else with the id in its argv — observed 10 matches on
   one card, 2026-10-01). Do NOT `xargs kill` over all of them: identify the ONE
   dispatcher-spawned worker process (verify with `ps -o pid,ppid,args -p <pid>`
   that its cmdline is the `hermes … kanban` task spawn and its ppid is the
gateway/dispatcher) and kill only that. A broad `xargs kill` risks taking down
   unrelated supervised services.
2. `kill <pid>` (then `kill -9` if it lingers).
3. `kanban reclaim <id>` — releases the claim so the dispatcher won't
   respawn.
4. `kanban archive <id>` — removes it from the board.
5. Clean the workspace: `git worktree remove .worktrees/<id> --force` in the
   base repo (check `git status --porcelain` first — if the worker banked
   real work, commit+push it to the branch first, same two cases as
   pitfall 12b), then `git branch -D <branch>` if it has no own commits.
Order matters: kill BEFORE reclaim, or the dispatcher re-spawns between the
steps. A reclaimed-but-not-killed PID keeps writing into the worktree.

## Review Workflow (worker → PR → human)

Preferred over local-commit review: worker works in `worktree` workspace, pushes
branch, opens PR (`gh pr create`), blocks the card `needs_input` with the PR number.
Review via the `github-code-review` skill (inline comments + approve/request-changes).
On approval: merge, `kanban complete <id> --summary "…PR #N merged"`.
Caveat: single-account setups (agent and user same GitHub login) get no
platform-enforced author/reviewer separation — the gate is process, not permission.
Repos without a GitHub remote (local-only) can't do PR review; commits stay local.

**The main/orchestrator session does NOT implement a card's code fixes itself
(user correction 2026-09-29: "Du sollst nicht coden. Zurück nach Kanban. mit
Deinen Findings.")** When a review finds a bug — even an obvious one — the main
session's job is to (1) diagnose the root cause, (2) write the finding as a
`kanban comment` on the card with the exact `file:line` + fix direction, (3)
unblock/dispatch so the ASSIGNEE WORKER makes the change in its own
worktree→branch→PR. The main session coding the fix directly breaks the
card→worktree→branch→PR discipline (the change lands outside the card's branch,
the worker's self-report can't be reconciled, and the per-card audit trail is
lost). The ONE exception is *exempt* content the main session is already
sanctioned to edit directly (docs under `discussion/`, `AGENTS.md`, skills) —
that is not "coding the card." If you catch yourself about to `patch` a card's
source file from the main session: stop, write the comment, hand it back.

**Native review lane (RELEASED, verified working 2026-10-01 on v0.21.5):**
`review` is a task status; the dispatcher has a review-column dispatch that
spawns the reviewer profile force-loading the bundled `sdlc-review` skill
(`/opt/data/skills/devops/sdlc-review/`, also cloned into profile skill dirs).
Setup (proven end-to-end, card t_78a63297):
1. `hermes profile create reviewer --clone --description "…"` (clone carries
   skills incl. sdlc-review; optionally repoint the model in the profile's
   config.yaml). Smoke-test with `hermes -p reviewer -z "…" --cli`.
2. Config: `kanban.review_dispatch: true` (default; no config change needed).
3. Worker policy in the assignee profile's MEMORY.md: after push + PR, finish
   with `kanban request-review <task-id> --summary "…" --reviewer reviewer`
   (NOT a needs_input block). The `--reviewer` reassigns the card before
   review dispatch.
4. Verdicts: approve = `kanban_complete` (card → done, PR stays OPEN — the
   user still merges); request changes = `kanban_comment` +
   `kanban_request_changes` (card returns to implementer, re-review routes
   back to the same reviewer via persisted reviewer provenance); escalate =
   `kanban_block`. CLI verbs: `request-review` (also `--force` to move a
   running claimed task), `request-changes <id> <reason…>`, `reopen-review`.
5. **PR verdict comment (user requirement 2026-10-01):** the reviewer must
   post its verdict to the GITHUB PR, not only the kanban card. Single-account
   setups (reviewer + worker share one GitHub login) CANNOT use
   `gh pr review --approve` — GitHub rejects own-PR approvals ("Can not
   approve your own pull request"). Use `gh pr comment <PR#> --body "✅
   Reviewed and approved (Kanban-Review-Lane, Card <id>) + evidence"` (or
   `❌ Request changes …`). Put this in the reviewer profile's MEMORY.md so it
   holds every run; the reviewer shares the main HOME's gh auth.
6. **Reviewer merges approved PRs (user decision 2026-10-01):** after an
   approve verdict the reviewer ITSELF merges (`gh pr merge <PR#> --squash`),
   then `git -C <base-repo> pull --ff-only` so dependent child worktrees
   branch from fresh master, and only then `kanban_complete` (summary must
   carry 'PR #N merged, base repo updated to <sha>'). This closes the race
   where `done` promoted children before the merge (children branched from
   stale master → conflicts). Merge failure (conflict/CI red) → do NOT
   complete: post failure to PR + `kanban_block` needs_input. The human merge
   gate no longer exists for reviewed cards; the user audits on GitHub. Rule
   4 of quality-gate-rules.md ("kein Merge ohne menschliche Freigabe") is
   superseded for the review lane by this decision.
7. **Reviewer-Handoff is MANDATORY for multi-card projects (user decision
   2026-10-07):** a project with more than one card hands EVERY worktree/PR
   card over to the reviewer lane on completion (`kanban_request_review` /
   `kanban request-review … --reviewer reviewer`) — it is the default on all
   boards with a GitHub remote. The only exception is local-only repos
   (no remote → no PR → no review handoff; those end with the worker's own
   block + evidence in the card).

**Recovering a prematurely-completed card into review:** `kanban_request_review`
(tool and CLI) only accepts `running`/`ready` cards — a `done` card is refused
("task is not in running/ready"). If a worker called `kanban_complete` instead
of `kanban_request_review` (the card skipped review), recover it with a direct
DB update:
```python
import sqlite3
db = sqlite3.connect("/opt/data/kanban/boards/<slug>/kanban.db")
db.execute("UPDATE tasks SET status='review', assignee='reviewer' WHERE id='<tid>'")
db.commit()
```
The dispatcher picks up the `review` card on the next tick and spawns the
reviewer profile. Verify with `kanban list` (status should show `review`).
This is the only path — there is no CLI verb for `done → review`.

**Completion contract (released in v0.21.5, verified in installed source):**
`kanban create … --completion-contract OWNER/REPO` (or an exact GitHub PR
URL; default `local-only`) makes completion DETERMINISTIC — the lifecycle
refuses `kanban_complete` until PR head SHA + required status checks + merge
evidence are collected via `gh api graphql` (`hermes_cli/kanban_pr_acceptance
.py`). Use it on every worktree code card: it enforces the PR-must-merge
board rule with no LLM in the path.
**Pitfall — completion contract on private repos without GitHub Pro is a dead end (verified 2026-10-06, card t_4aa2143a):** the gate calls `gh api repos/<repo>/rules/branches/<branch>`, which returns 403 ('Upgrade to GitHub Pro or make this repository public') — classified 'infra', so `kanban_complete` is refused PERMANENTLY; only the other API calls in the chain (graphql, check-runs, statuses, pulls) succeed. For private repos without CI: `--completion-contract local-only`; provide merge evidence manually via `gh pr view <n> --json state,mergedAt,mergeCommit` in the completion summary. **Recovery when a card is already stuck** (contract set at create, reviewer merged the PR, card sits `review`/`blocked` and `kanban complete` refuses even with `--force` — the gate check runs BEFORE the status transition, so no flag bypasses it): (1) flip the contract directly in the board DB — `UPDATE tasks SET completion_contract='local-only' WHERE id='<tid>'` (`prepare_acceptance` short-circuits on `local-only`); (2) `kanban complete <id> --result "…"` with the merge evidence (PR state, mergedAt, mergeCommit, reviewer verdict) in the result text. Note: `unblock` on a `review`-status card does NOT move it to `ready` — it stays `review` (the block_kind lingers cosmetically); only the contract flip + complete closes it.

**Auto-decompose (v0.21.5, verified in installed source):**
NOT an inline pass in `kanban create` — it is a GATEWAY DISPATCHER TICK:
every tick (~60 s) it takes up to 3 `triage` cards per board
(`auto_decompose_per_tick: 3`, default) and runs them through the
decomposer LLM (`auxiliary.kanban_decomposer`). Single-task cards get
promoted `triage → todo` directly (`specify_triage_task`, no gate wrapper);
fanout cards are split into child cards. Consequence: with auto-decompose
ON, `triage` is NOT a holding point — a card parked there is auto-promoted
within ~2 ticks WITHOUT the gate wrapper, so the input gate must enforce
at CREATE-time (rules block + verifiable done-criteria in the body survive
the decompose rewrite) plus a `pre_tool_call` hook that blocks
non-conformant `kanban create` (see `references/hooks.md`); the wrapper's
specify-time check remains the second net. `kanban.auto_decompose: false`
in config.yaml makes triage a true holding point with the wrapper as the
sole triage→todo entry — but the user keeps auto-decompose ON (standing
decision), so the create-time enforcement is the design. The decompose LLM
call goes through the auxiliary pipeline, but `pre_auxiliary_call` hooks
are observer-only/fail-open — they cannot block it; and kanban lifecycle
hooks are observer-only (fire after the DB commit, return ignored). The
The only deterministic block point on the agent path is `pre_tool_call` on the
terminal/kanban tools. The decomposed ROOT card is a short verification pass,
NOT a re-execution: when all children complete it wakes, runs briefly (tens of
seconds) to verify the children's results, and completes without redoing the
work or re-sending their outputs — a root that "flashes" briefly after its
children finish is expected behavior, not a bug (confirmed by user
observation).

**Hook activation & verification (proven 2026-10-01):** `hooks:` entries in
config.yaml are read at PROCESS STARTUP ONLY. If the gateway (and the
webui/API server — separate process, same rule) started before the hook
entry was written, the hook is silently inactive in every session those
processes serve — a correct, installed, allowlisted hook still lets
non-conformant `kanban create` through. After ANY `hooks:` config edit:
(1) restart the gateway/container (user step), (2) verify the hook is
live with a deliberately non-conformant command in a real terminal call of
the session — it must come back blocked; a card that lands `ready` means
the hook did not fire. Quick sanity check without a live test:
`ps -o lstart -p <gateway-pid>` vs `stat -c %y config.yaml` — config newer
than process start = hook not loaded. Also: `pre_tool_call` hooks need
first-use consent per (event, command) — approvals persist in
`/opt/data/shell-hooks-allowlist.json`, but consent is PER PROCESS: an
approval recorded by a worker/CLI process does not cover the gateway
process.

**The hook-owning process must be the one EXECUTING your terminal tool.**
In this deployment the main chat session's `terminal` tool runs under the
**webui `server.py` process, NOT the gateway** (verified 2026-10-01 via
`ps -o pid,ppid,args`: my terminal bash's parent was `/opt/hermes-webui/server.py`,
while the gateway was a separate PID). Observed: a config-registered, allowlisted
`pre_tool_call` hook that showed up in the gateway's "shell hook registered" log
**fired 0 times** for the main session's terminal calls (a deliberate
"log-on-every-fire" probe stayed at 0 across dozens of calls) even after a full
container restart. So "registered" in the gateway log is NOT proof the hook
covers the session you're testing in — confirm the hook-owning process is the
one running your terminal tool (`ps -o pid,ppid,args -p $$` up the chain) before
treating a non-blocking `kanban create` as proof the hook is broken. (Whether the
webui process fires `pre_tool_call` for its terminal tool at all was left
unresolved when the container restarted — verify, don't assume.)

**Retiring a profile:** `hermes profile delete <name>` is interactive (type
the name to confirm — pipe it: `echo <name> | hermes profile delete <name>`).
It warns the gateway will stop; a running gateway kept its PID and stayed up.
Before deleting, check `kanban list` for cards assigned to that profile.

## Lane model: default + reviewer (user decision 2026-10-11)

The 2026-10-07 board-doctor lane (automated repair chain on a weaker model)
is RETIRED — it did not work well. Do not create doctor cards or reintroduce
a repair lane. Broken processes (blocked cards with dead PIDs, half-created
or orphan worktrees, stale claims) are repaired by the main session: kill the
worker + reclaim + re-seed a narrower card (see `hermes-kanban-workers`
pitfalls 12/15).

**2-Lane invariants:**
- **Mandatory for multi-card projects (>1 card):** `default` (work) +
`reviewer` (handoff per PR card via `kanban_request_review`, see native review
lane; the reviewer merges). Single-card work is exempt. Post-merge live
verification (deploy tick, on-target checks) is a separate `default` card
gated behind the PR card — the reviewer only reviews + merges. Full reference
doc: DokuWiki page `concepts/kanban-2-lane-workflow`.
- **Lane invariant (Board-Regel 9):** exactly 2 lanes per board
(default/reviewer), no more, no less; dead lanes (e.g. of a deleted profile)
get their open cards reassigned to `default`; done cards of a retired lane are
archived. Audit per board:
`sqlite3 <board>/kanban.db "SELECT assignee, COUNT(*) FROM tasks GROUP BY
assignee"`.
- **Worktree prevention (multi-card code series):** pre-create the worktrees
BEFORE dispatch (`git worktree add <path> -b feat/<card>` per card) — on NFS
the lazy first-create at spawn time costs tens of seconds of latency and can
burn the dispatch window. One branch per card — no chained-branch design
(branch B on top of branch A); each card branches from fresh master. The
final card merges all branches.

## Multi-Model Fan-Out (proven 2026-09-29)

Spread parallel workers across **different model backends / machines** to
offload the agent's own model. The parallelism cap is per-profile, so a second
profile is the fan-out lever — and it can run a *different model on a different
host*, not just a second seat on the same one.

```bash
# 1. Clone the active profile (carries skills + .env), then repoint the model:
hermes profile create worker --clone --description "Kanban-Worker-Modell: <model> on <host>. Offloads the agent model for parallel workers."
# 2. Edit /opt/data/profiles/worker/config.yaml  (hermes config set is UNSAFE for nested YAML — edit directly):
#      model:
#        default: <model-id>
#        base_url: http://<host>:<port>/v1
# 3. Validate the YAML, then a one-shot functional test (real LLM call, no stub):
#      hermes -p worker -z "Antworte mit genau einem Wort: bereit" --cli
# 4. Assign cards to it:  hermes kanban create "…" --assignee worker --workspace worktree --branch feat/…
```

- The dispatcher spawns the worker per card on that profile; no permanent
  gateway is needed for kanban work (`Gateway: stopped` is fine).
- Quality trade-off: a weaker/secondary model is fine for routine cards
  (docs, cleanup, running tests) but keep critical code/merge work on the
  primary profile. Fan-out = routine on the cheap backend, critical on the strong one.
- A lazy-loaded secondary model costs a ~100 s boot on first use — not worth it
  for very short cards.

## Durable Worker Policy (survives "I forgot to say it")

When the user wants a worker behavior to hold **every run** — not just the
cards you annotated this session — split it into two layers with different
durations:

1. **Isolation is structural (cannot be forgotten).** The dispatcher pins
   `TERMINAL_CWD` to the per-task workspace (`workspaces_root/<task-id>` for
   `scratch`, the worktree dir for `worktree`) and loads context files from
   that dir. A worker physically cannot land in the shared checkout unless the
   card is explicitly `dir:`. You do not need to "remind" it — the code does it.
2. **Policy is an instruction (can be forgotten) → put it in profile
   `MEMORY.md`.** A per-card comment only covers that one card. The durable
   place is the assignee profile's `MEMORY.md`
   (`/opt/data/profiles/<profile>/memories/MEMORY.md`), which is injected into
   **every** worker run on that profile regardless of card or workspace.
   Example policy that belongs there: *"scratch workspace = own isolated dir;
   repo is READ-ONLY for investigation cards — deliver the result as
   card-result, the main session updates exempt docs; code only via
   card→worktree→branch→PR."* Write it declarative (a fact about how this
   profile's workers operate), not as a per-task command. For the default
   profile use the `memory` tool; for a *different* profile's MEMORY.md use a
   direct file edit (cross-profile) — the `memory` tool only writes the
   active profile.

Verify the injection actually reaches workers: kanban spawns run
`hermes -p <profile> chat -q …` **without** `--ignore-rules`, so profile
memory + context files ARE loaded. If you ever see a worker ignore a policy,
check the profile's MEMORY.md first (is the line there? correct profile?)
before suspecting the spawn path.

## Diagnosing What a Worker Run Actually Did

**Live progress while a run is still `running`:** read the worker's streamed
stdout at `/opt/data/kanban/boards/<board>/logs/<task_id>.log`
(`tail -c 3000 …` for the last chunk) — fast and non-blocking. Do NOT use the
`kanban tail <id>` subcommand in the foreground: it is a live-follow that blocks
past the terminal's 180 s timeout. **To get notified when a long card completes
from a normal session** (no Telegram/chat to `notify-subscribe`), run a bounded
background poll that exits when the card leaves `running`, with
`notify_on_complete=true` (a legitimate bounded wait, not a busy-loop):
`for i in $(seq 1 90); do st=$(hermes kanban --board <slug> list 2>/dev/null | grep ' <id> ' | grep -oE '\b(running|done|blocked|crashed|gave_up|timed_out|archived)\b' | head -1); [ -n "$st" ] && [ "$st" != "running" ] && { echo "<id> -> $st"; break; }; sleep 60; done`.

For a FINISHED run, `kanban show` / `kanban runs` truncate summaries; the full
worker transcript is in the session DB. Worker sessions are rows in
`/opt/data/state.db` `sessions` (title = card title, `profile_name` set,
`started_at` near the run). Then query the messages and grep for the friction
that silently ate run time:

```bash
sqlite3 /opt/data/state.db "SELECT id, profile_name, title FROM sessions ORDER BY started_at DESC LIMIT 8"
sqlite3 /opt/data/state.db "SELECT role, substr(content,1,400) FROM messages WHERE session_id='<id>' ORDER BY id"
# grep the output for: permission|denied|dubious|safe.directory|EACCES
```

This is how you tell "the worker finished cleanly" from "it hit a permissions wall, self-healed, and lost 5 minutes" — the card events show neither.

## Pre-Merge Conflict Preview (read-only, no working tree)

Before dispatching a merge card, predict conflicts without touching any
checkout — useful when several worker branches must land and you want the
conflict map up front:

```bash
git merge-tree --write-tree --name-only master <branch>   # lists files that WILL conflict
git merge-tree --write-tree -p master <branch>            # shows the conflict hunks
```

Run it per branch pair (and branch-vs-branch, not just branch-vs-master) to see
which files collide across the whole wave. Classify the result (docs-only vs
code) and put the expected-conflict map + resolution rule into the merge card
body so the worker resolves deliberately instead of hitting it cold. (In a
sandbox where the repo owner ≠ the running user, add
`git config --global --add safe.directory <repo>` first, or every git call
fails with "dubious ownership".)

## Batch Pattern (proven)

0. Planning first, as a spec Q&A. Ask one decision at a time, each with a recommended option and short choices. Record every answer immediately in `<repo>/.hermes/decisions.md` (a table with D-numbers), then commit + push before creating cards (pitfall 9). Present the card plan (table: card / decisions covered / depends on) for confirmation before writing to the board.
1. `boards create` + `--switch`
2. create all cards with `--idempotency-key` (safe re-runs)
3. create gate card, `link` gate → each child (children fall to `todo`)
4. readiness-verify each dependency, `comment` results per card
5. user pulls items out: `unlink` + `archive` the pulled card
6. `complete` the gate → children promote to `ready`
7. `assign` each child to a profile → `dispatch --dry-run` → `dispatch`
8. track via `list` / `show` / `runs`; handle `needs_input` blocks as reviews
