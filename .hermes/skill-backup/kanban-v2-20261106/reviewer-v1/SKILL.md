---
name: hermes-kanban-workers
description: "Use when running Hermes Kanban worker campaigns. Board setup, dependency chains, stopping workers, watchers, review/merge."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [kanban, worker, dispatcher, multi-agent, git, review]
    related_skills: [merge-reconciler, subagent-fanout, github-pr-workflow, peters-github]
---

# Hermes Kanban — Multi-Worker Code Campaigns

Operate the durable SQLite kanban board to fan out work to named worker
profiles, keep parallel workers from clobbering each other, and review/merge
their output safely. This is the *operational* workflow (distinct from
`hermes-agent`'s high-level feature overview and from `merge-reconciler`, which
is only the conflict-resolution sub-task).

## When to use
- User wants work fanned out to kanban workers ("let the worker do it", "run
  these in parallel", "assign to a profile").
- Setting up a project board, linking dependent cards, or capping concurrency.
- A worker finished and you must review / merge / reconcile its output.
- Diagnosing why a card is `blocked` / stuck / not spawning.

## Hard rule: code changes go through the board ONLY (2026-09-29)

The user set a standing rule: **no code change happens outside the kanban
board.** Every code change — even a one-line fix, even when the user asks for
it mid-conversation — goes:

**kanban card → worktree → feature branch → PR → user merges on GitHub.**

- Not by the main session, not by a worker, not as a direct commit to
  `master` (or any branch). If you catch yourself about to `git commit` code
  on `master` in the main session, stop — that is exactly the path this rule
  forbids. Route it as a card instead (or get the user's explicit
  per-instance OK to bypass, and say so).
- **"Code" = source, scripts, configs that run.** Docs, skills, wiki, and
  memory are **not** code and may still be edited directly (that is how this
  very rule got recorded). When in doubt whether a file is "code", treat it
  as code and use the board.
- **Exempt folders:** the llama-swap repo additionally designates
  `discussion/` as exempt — files there (e.g. `discussion/QUESTIONS.md`) may
  be edited/created/moved directly without a card, per its `AGENTS.md`.
- This is the user's stated preference for *reliability*: it lives in
  MEMORY.md (injected every session) and in the repo `AGENTS.md` (injected to
  every worker in the repo) as well. If those two and this skill ever
  disagree, the user's most recent statement wins — re-confirm.
- **2-lane model (user decision 2026-10-11, replaces the 2026-10-07 3-lane
  model — the board-doctor lane was retired as not working well):** boards
  run exactly 2 lanes — `default` (work) and `reviewer`. >1 card ⇒ every PR
  card ends with `kanban_request_review` (reviewer=`reviewer`) and the
  reviewer merges; the worker never merges itself. Code only via
  card→worktree→branch→PR (repos under `/workspace/dev/repos/ours/<repo>`):
  main does plan/docs, reviewer merges PRs (reviewer lane default on all
  remote boards; local-only repos exempt). Stuck/broken cards are repaired
  by the main session (kill + reclaim + re-seed), not by a doctor lane.
  Post-merge live checks (deploy tick etc.) go into a separate verify card
  gated behind the PR card. Details: `hermes-kanban-ops`, DokuWiki
  `concepts/kanban-2-lane-workflow`.

## Environment (this sandbox)
- CLI: `/opt/hermes/bin/hermes` (NOT on PATH — always full path).
- Boards live under `/opt/data/kanban/boards/<slug>/` — `kanban.db`,
  `workspaces/<task-id>/` (scratch) or `workspaces/<task-id>/repo` (worktree).
- Dispatcher runs inside the **gateway** (`kanban.dispatch_in_gateway: true`).
- Config: `/opt/data/config.yaml`, `kanban:` block. `hermes config set` is
  UNSAFE for nested YAML — append/edit the block by hand (see
  `references/config-knobs.md`).
- Git repos are often owned by a different uid than the agent → you may need
  `git config --global --add safe.directory <repo>` before git works (see
  Pitfalls).

## Core workflow

### 1. Board (one per project/workstream)
```bash
H=/opt/hermes/bin/hermes
$H kanban boards create <slug> --name "Name" --description "..." \
  --icon "🔁" --color "#f59e0b" \
  --default-workdir /abs/path/to/repo --switch
```
`--default-workdir` is only a fallback; the per-task `--workspace` wins.

### 2. Tasks — pick the workspace DELIBERATELY
```bash
$H kanban create "Title" --body "..." \
  --idempotency-key <stable-key> --json   # returns the task id
```
`--workspace` options (default `scratch`):
- `scratch` — **ephemeral per-task dir, deleted on done.** Good for research.
  ⚠️ Does NOT isolate file writes (see Pitfall #1).
- `worktree` (+ `--branch feat/<id>-…`) — **isolated git worktree + branch.**
  Use for any parallel code change.
- `dir:/abs/path` — the shared existing dir. **Read-only-only.** It shares the
  working tree, index, and HEAD with the main session, so a `dir:` worker
  writing while the main session commits/pulls the same checkout can clobber
  each other's staged files, commits and pulls (see Pitfall #10). Use `dir:`
  for read-only analysis; for ANY write — even to an exempt folder like
  `discussion/` — prefer a worktree, or make sure the main session is idle on
  that checkout first.

### 3. Dependency control (the part people get wrong)
- `todo` = task is waiting on open **parent** links; `ready` = all parents done.
  There is **no direct `ready→todo` demote verb**.
- **Gate-card pattern** to hold a batch in `todo` until you say go:
  ```bash
  GATE=$($H kanban create "GATE: <reason>" --body "..." --json | jq -r .id)
  for T in <child-ids>; do $H kanban link $GATE $T; done
  # children now sit in 'todo'. When ready:
  $H kanban complete $GATE --summary "..."   # dispatcher promotes children → ready
  ```
- **Dependent cards (shared files/docs) MUST be linked parent→child so they
  run sequentially.** Running two cards that both edit `ROADMAP.md` / the same
  script in parallel is a write race. (This is the #1 user correction from
  the originating session: "Skills hinzufügen und dokumentieren hätte
  nacheinander laufen müssen.")

### 4. Assign + dispatch
```bash
$H kanban assign <task> <profile>        # profile = a Hermes profile name
$H kanban dispatch --dry-run             # see what WOULD spawn
$H kanban dispatch                        # actually claim + spawn workers
```
⚠️ The gateway dispatcher ticks every `dispatch_interval_seconds` (60s) but in
the originating session it did **not** auto-claim — a manual `hermes kanban
dispatch` was required. Always run a manual dispatch (or verify the tick fired)
after assigning; don't assume the gateway picked it up.

### 5. Concurrency
Set a per-profile cap in `config.yaml` so one profile can't saturate the shared
model/quota (default `null` = unlimited — that's why 4 workers can blast away
at once):
```yaml
kanban:
  max_in_progress_per_profile: 2
```
Over-cap `ready` tasks defer to the next tick. See `references/config-knobs.md`.

### 5b. Multi-profile fan-out (offload routine work to a second LLM host)
The cap is **per profile** — a second worker profile on a different model/host
doubles real throughput AND keeps the main profile's model free for the user's
own session (a saturated shared GPU slows the interactive session down).
Pattern (proven 2026-09-29 with a `worker` profile on the `llm` host — that
profile was RETIRED 2026-10-01; cards now run on `default` + `reviewer`;
always check `hermes profile list` before assigning):
```bash
# 1. Clone a profile (skills + .env come along)
/opt/hermes/bin/hermes profile create worker --clone --description "..."
# 2. Point it at the other host's model — edit the profile's config.yaml
#    model block directly (sed/patch); `hermes config set` is UNSAFE for
#    nested YAML. Set `default: <model-id>` + `base_url: http://<host>:8080/v1`.
# 3. Smoke-test BEFORE dispatching cards:
/opt/hermes/bin/hermes -p worker -z "Antworte mit genau einem Wort: bereit" --cli
# 4. Assign cards to it:
$H kanban create "..." --assignee worker --workspace worktree --branch feat/...
```
Rules:
- **Never assume the second host is up** — it is an offload, not a safety net.
  Critical work (merge-conflict resolution, protocol logic) stays on the
  strong model; routine cards (docs, cleanup, running tests) go to the offload.
- The offload model may be a different variant (e.g. VL) — quality is not
  identical; weight card difficulty accordingly.
- First turn on a lazy-loaded model costs ~100 s boot — short cards don't
  amortize it.

### 6. Review the finished work (worker → human gate)
A well-behaved worker blocks its own card with `kind=needs_input` and a
"review-required" summary instead of pushing/merging. Inspect:
```bash
$H kanban show <task>      # status, summary, comments, events
$H kanban runs <task>      # per-run outcome/elapsed/summary
```
**User working style (originating session, recurring):** for anything
irreversible (git push, merge, deploy) the agent REPORTS first and the user
decides. "Nur Report, noch nicht schieben." Do the read-only analysis, present
findings + a recommended merge order, and wait for the go-ahead before
pushing/merging.

### 7. Post-merge conflict resolution (user merges, you fix the other PR)
Recurring user workflow: the user merges the PRs **themselves** on GitHub,
then asks you to resolve the conflict on the remaining open PR and re-push.
Recipe (from the base repo, working tree stays clean):
```bash
cd <base-repo>
git fetch -q origin
git checkout feat/<branch>            # the PR's head branch
git merge origin/master               # expected: CONFLICT in the shared file(s)
# resolve: keep BOTH sides' changes (both PRs are user-approved intent),
# then:
git add <file>
git commit -m "Merge origin/master into feat/<branch> (resolve <file>: keep both)"
git push origin feat/<branch>
```
- **GitHub's `mergeable` status lags 15–40 s after the push** — it reports
  `CONFLICTING` immediately, then `UNKNOWN` while recomputing, then
  `MERGEABLE/CLEAN`. Poll `gh pr view <n> --json mergeable,mergeStateStatus`
  with a short sleep between checks; do NOT report "still conflicting" from
  the first read.
- Verify after the merge that both PRs' changes coexist (grep for each side's
  markers) — a "keep both" resolution that silently dropped a hunk is the
  classic failure.

### 9. Read-only conflict pre-analysis (do NOT touch the working tree)
To see what would conflict when merging worker branches, use `git merge-tree`
(object-level, no working-tree mutation) from the base repo:
```bash
cd <base-repo>
git merge-tree --write-tree --name-only <A> <B>     # lists conflicting files
git merge-tree --write-tree -p <A> <B>              # full conflict hunks
git merge-base <A> <B>                              # common ancestor
git diff <base> <branch> -- <file>                  # what each side changed
```
This is how you tell "only docs conflict (trivial)" from "the core script
conflicts (manual merge needed)" before committing to a merge order. Full
recipe + worked example in `references/conflict-analysis.md`.

### 10. Campaign cleanup (retire a feature: card + branches + cron + wrappers)
When a feature/workstream is retired (user decision), tear down ALL its
artifacts, not just the obvious ones:
1. **Cron jobs** referencing it: `hermes cron list` (full path), `hermes cron remove <id>`.
2. **Wrapper scripts + report/state dirs** the jobs created (e.g. under
   `/opt/data/scripts/`, `/opt/data/<feature>/`) — remove with `rm`/`rm -rf`.
3. **Branches**: verify the PR is merged FIRST (`gh pr list --state all
   --search <term> --json number,state`), then `git branch -d <branch>` and
   `git push origin --delete <branch>` from the base repo. If the worktree is
   already gone, the branches are the only leftovers.
   Bulk local cleanup of stale card branches/worktrees: `git branch
   --no-merged` is useless after squash merges — per branch check
   `git rev-list --count origin/main..<b>` + `gh pr list --state all --head <b>
   --json number,state` + `git ls-remote --heads origin <b>`. Delete only if
   the PR is MERGED, its content is verifiably in main, or a remote copy
   exists; a branch with none of these (e.g. a recon report never PR'd) holds
   the only copy — rescue its files into the repo first. Check worktrees are
   clean (`git -C <wt> status --short`) before `git worktree remove`.
4. **Memory entries** that describe the retired state (e.g. "db corrupt,
   backups in …") — replace with the current state in the same pass.
5. Verify each removal (job absent from `cron list`, paths gone, branch gone
   on both sides).

## Pitfalls (learned the hard way)
1. **Workspace isolation is illusory for file writes.** A worker in a
   `scratch` workspace still edits the REAL repo at its absolute path if the
   task body names that path. The workspace only sets the starting cwd. Two
   parallel scratch workers on the same checkout WILL race on shared files
   (observed: two workers both rewrote `ROADMAP.md`; no damage only by luck).
   → Parallel code work = `worktree` per card. `dir:` = read-only-only
   (Pitfall #10).
2. **`todo` has no demote verb.** To park `ready` cards, use the gate-card
   parent-link pattern (§3), not a status flag.
3. **Dispatcher may not auto-claim.** Run `hermes kanban dispatch` manually
   after assigning; verify with `kanban list` (status flips `ready→running`).
4. **`safe.directory` ownership mismatch.** Repos owned by another uid than the
   agent trigger `fatal: detected dubious ownership`. Fix:
   `git config --global --add safe.directory <repo>` (and each worktree path).
   `git clone` of such a repo fails the same way — operate in-place instead.
   The full story — which gitconfig EACH process context reads (gateway vs
   session vs worker-spawn), wildcard semantics, credential helper for
   profile homes — is in `hermes-kanban-ops` Pitfall 13. Fix ALL contexts,
   not just the one that errored, or the next run self-heals and burns time.
5. **`gh` is not in plain apt.** Install from the official GitHub apt repo
   (`cli.github.com/packages`, key → `/etc/apt/keyrings/`); see `peters-github`.
6. **A worker's "not pushed" claim can be stale.** A *second* worker pushing a
   child commit can carry a sibling commit along. Re-verify `git rev-parse
   master origin/master` before trusting a card's "local, not pushed" note.
7. **Skills copied to global before a dependent edit** go stale. If card A
   finalizes skills to `/opt/data/skills/` and card B later edits the in-repo
   reference, the global copy lags. Re-sync global from the merged state.
8. **Untracked files are invisible to worktrees.** A file that exists in the
   base repo only as `?? untracked` (e.g. a freshly written `AGENTS.md` that
   was never committed) does NOT appear in a worker's worktree checkout. If a
   card needs it, either commit it first or copy it into the worktree
   (`cp <base-repo>/FILE <worktree>/FILE`) before dispatching, and note it in
   the card body. Observed 2026-09-29: worker card expected `AGENTS.md` in its
   worktree; it was only untracked in the base repo.
9. **Master drifting while a worker runs** invalidates the worker's branch.
   If you commit to `master` while a worktree worker is mid-flight on a
   branch that edits the same file, its PR will conflict. Two mitigations:
   (a) link your doc work as a parent so it runs sequentially, or (b) after
   the drift, comment on the blocked card with the exact conflict-resolution
   instruction (merge `origin/master` into the branch, keep BOTH sides'
   changes) — but a `blocked` card won't read the comment on its own; the
   user must re-trigger or you do the small merge yourself. Observed
   2026-09-29: post-mortem doc commit to `AGENTS.md` on master vs. worker
   branch `feat/remove-roadmap` editing the same file.
10. **`dir:` (main checkout) is a write race with the main session.** A `dir:`
    worker and the main session share ONE working tree, index and HEAD. If the
    worker writes a file while the main session is committing/pulling the same
    checkout, they can clobber each other's staged files, commits and pulls.
    Observed 2026-09-29 (near-miss): a `dir:` worker wrote `discussion/DRIFT.md`
    to the main checkout while the main session committed `AGENTS.md` +
    `discussion/QUESTIONS.md` to that same checkout — no clobbering ONLY because
    the worker's index was still empty (luck, not safety). Rule: `dir:` is for
    READ-ONLY tasks. For any write — even to an exempt folder — use a worktree,
    or confirm the main session is idle on that checkout before dispatching.
    (Also recorded in the llama-swap repo `AGENTS.md` "Change process".)
    Corollary: a `dir:` card that points at a WORKTREE path outlives that
    worktree — when the worktree is deleted, every terminal command in the
    next session fails at startup with `cd: <worktree>: No such file or
    directory` (the shell restores the deleted cwd). Pass an explicit valid
    `workdir` to terminal calls until the session cwd is reset.
11. **Merged code stays in the repo — cleanup ≠ deletion.** Retiring a
    feature removes its branches, worktrees, cron jobs and wrappers; the
    merged code in `master` is NOT deleted as part of cleanup (that would be
    a new commit/PR). State explicitly that the code remains and offer a
    separate PR if the user wants it stripped — the user decides.
12. **A worker that crashes on "Response dominated by repeated text" (the
    🔁 marker) is a CARD-DESIGN problem, not a flaky model — re-seed a
    narrower execute-only card, do NOT just re-dispatch the same card.** The
    repetition loop fires when the card body asks the worker to *design or
    decide* an open-ended mechanism (e.g. "pick FIFO vs QMP vs sendkey for
    serial input") rather than *execute* a fixed one: the model ruminates over
    the design space, the stream self-terminates mid-loop, the run exits rc=1,
    and at `failure_limit` (default 2) the card auto-blocks. Recovery:
    (a) confirm the signature in `kanban runs` / the worker log ("Response
    dominated by repeated text — stopping the stream mid-loop");
    (b) rewrite the card as execute-only — remove the design decision, ship a
    complete ready-to-run script skeleton + exact commands, and where possible
    ELIMINATE the hard sub-problem entirely (e.g. a Default-Y timeout made the
    serial-input mechanism unnecessary, so the card just reads the log);
    (c) put an explicit "AUSFÜHREN, NICHT DESIGNEN" / "execute, don't design"
    rule at the TOP of the body so the worker does not re-open the design
    space. Re-dispatching the same design-heavy card re-crashes it identically.
    After a crash, do a bounded READ-ONLY diagnosis yourself (Gate 8 allows
    recon to verify a claim / seed ≤4 facts) and seed the next card with the
    root cause + exact fix so the worker EXECUTES a known fix instead of
    re-diagnosing — a card that says "diagnose and fix" re-opens the design
    space and re-loops. If the loop is a known model-backend issue, switching
    the backend (user decision) clears it without any card change — verify
    the retry run is loop-free before trusting it.
14. **Completing a parent AUTO-PROMOTES gated children to `ready` — the
    dispatcher then spawns them on the next tick.** A destructive card gated
    on a fix card (e.g. a hardware E2E that wipes a disk and needs the
    user's explicit GO + physical action) will be auto-started the moment
    its last parent completes — the worker cannot perform the user's part
    and the card burns a run (or worse, acts). Pre-block such cards with
    `kind=needs_input` ("wants user GO") BEFORE the parents complete; if the
    promotion already happened, kill the spawned worker + reclaim + re-block
    immediately (see #15).
15. **Stopping a running worker = kill + reclaim + block — reclaim alone
    respawns it.** `kanban reclaim <id>` releases the claim and returns the
    card to `ready`; the dispatcher re-spawns it on the next tick. Full
    stop: (a) find the worker PID (`ps aux | grep "kanban task <id>"`),
    `kill -9`; (b) `kanban reclaim <id>`; (c) `kanban block <id>` with
    `kind=needs_input` + reason. Verify with `kanban list` that no
    `running`/`ready` state remains for the id. To stop a batch of cards
    (e.g. to free a machine for a reboot): stop each, and if they share a
    host resource (QEMU/VMs, nix builds), also stop the host-side processes
    (`pkill` the VMs) — the cards being blocked does not stop what the
    workers already launched. When stopping several cards that will later
    resume on the same shared resource, link them parent→child so they run
    sequentially, not in parallel (store-lock / write-lock races).
    The `kanban_block` TOOL on a running card behaves the same: it records
    `blocked` but the worker process keeps running and keeps acting on the
    target. Always follow a block with `ps -eo pid,cmd | grep "kanban task
    <id>"` → kill, and check the target host for processes the worker
    started (test harnesses, VMs, builds). A killed worker showing `Zs` is a
    zombie awaiting dispatcher reap — already dead, no further action.
    To park a blocked card behind another card: `kanban_block` → `kanban_link
    parent child` → `kanban_unblock` (lands in `todo`, gated); `kind=dependency`
    only parks in `todo` when an open parent already exists.
16. **Workers spawn follow-up cards that bypass your planned order.** A
    completing worker can `kanban_create` a follow-up whose only parent is
    itself; the moment it completes, that follow-up AND your next planned card
    both become `ready` and run in parallel on the same host. Also another
    actor (user/other session) may complete a card concurrently — a
    `kanban_complete` returning "already terminal" means re-read state, not
    retry. After any completion in a sequential chain: `kanban_list` for new
    ids and link them into the chain BEFORE they dispatch — `kanban_link`
    refuses a child that is already `running`, so linking late fails. For a
    long chain, put the link rule into every card body ("follow-up cards you
    create: kanban_link them before <next chain id>"); the user rejects cron
    watchers by default (`references/board-watch-cron.md` only on explicit ask).
18. **Every PR card on a multi-card board must hand off to the reviewer lane.**
    Write the body so the worker ends with `kanban_request_review`
    (reviewer=`reviewer`) instead of merging itself; the reviewer merges. Check
    this BEFORE creating the cards — it is the user's 2-lane (default + reviewer) rule and is easy
    to forget when a card also contains deploy/verify steps (post-merge deploy
    then belongs to the timer or the next card).
17. **Serialize cards that share a host resource by dependency links, not by
    comments.** Cards that each run `nix build` of the same flake or use the
    same VM disk image on one host must be parent→child linked; a "check
    pgrep and wait" comment is advisory and racy. Gate the next phase's first
    card behind the last such card too.

## Verification (definition of done)
- `kanban list` shows expected statuses; no unexpected `running`.
- Merged: `git rev-parse master origin/master` match (if pushed), no conflict
  markers, tests pass.
- Global skills (if touched) `diff -r` clean against in-repo reference.
