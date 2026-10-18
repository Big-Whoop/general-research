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

**New workstream in its own repo (user pattern):** bootstrap all three in one
pass — private GitHub repo (`gh repo create <name> --private --source . --push`
with README + AGENTS.md carrying the card→worktree→PR rule and the fixed
stack), the kanban board (same slug as the repo, `--default-workdir` = the
local clone under `/workspace/dev/repos/ours/<slug>`), and a Hermes desktop
project (`desktop_project create` with that path) — then `desktop_project
switch` back to the project the chat belongs to. Ask the user for the slug
before creating anything; renaming later touches all three.

**CLI flag order:** `--board <slug>` goes AFTER `kanban` (`hermes kanban
--board <slug> create …`); `hermes --board …` fails with "'<slug>' is not a
hermes command". The "No gateway is running" warning on create is cosmetic
when the gateway hosts the dispatcher — check `kanban list` instead.

**Comments: single-quote the body.** `kanban comment <id> "…"` with
backticks inside gets shell-expanded (`languageVersion: command not found`
and the token silently disappears from the comment). Use `'…'` or
`--body-file`.

### 2. Tasks — pick the workspace DELIBERATELY
```bash
$H kanban create "Title" --body "..." \
  --idempotency-key <stable-key> --json   # returns the task id
```
⚠️ **Input gate:** non-triage `kanban create` is checked by a `pre_tool_call`
hook that enforces 8 gate rules (workspace, completion-contract, review-handoff,
PR-pflicht, reviewer-assignment, worktree-isolation, dependency-info) + legacy
checks (Rules-Block-Marker, Done-Kriterien). The hook blocks non-conformant
commands and tells the agent what's missing. Override per-rule with
`OVERRIDE: <rule> (reason ≥ 10 chars)` in the body. Full rule table +
override mechanism: `references/input-gate.md`.
`--workspace` options (default `scratch`):
- No `--skills` flag on `kanban create` (the global `hermes --skills` is rejected after the subcommand). Pin skills post-create via the `tasks.skills` column: `sqlite3 <board>/kanban.db "update tasks set skills='a,b' where id='<id>'"` (comma-separated; `kanban show` prints it as `skills:`).
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

### 3b. Seeding a chain of several new cards: link BEFORE the dispatcher sees them
`kanban create` lands a card in `ready` (no parents) and the gateway
dispatcher claims `ready` cards every tick — so creating four chain cards in
one shell loop and linking them afterwards fails for every card that got
spawned in between (`cannot link: child is already running`). Order that
works: create the FIRST card only, create each later card and link it to its
parent in the same command (`ID=$(create …); kanban link <parent> $ID`),
or create every card with an existing open parent (a gate card) and link
them down the chain while they sit in `todo`. Simplest: `kanban create …
--parent <id>` links at create time and the card lands in `todo` directly.
Create long chains from `terminal` in small batches (2–3 creates per call,
each wrapped in `timeout 120`, ids captured with `grep -oE 'Created t_…'`),
not in one `execute_code` loop: each create costs several seconds, so a
chain of ~9 cards can hit the 300 s cell limit and the kernel dies mid-chain
with the id map lost (and `execute_code` also skips the input-gate hook).
After any interrupted batch, list what already exists from the board DB
(`select id,title from tasks where title like '<prefix>%'`) and continue
from there instead of re-creating duplicates. Write the card bodies to
files first so they survive a dead kernel.

**Seeding an execution chain for a plan phase:** create the first card
plain, every later one with `--parent`, and parallel siblings that share
one downstream card get `--parent <first sibling>` plus `kanban link
<other sibling> <child>` for each extra parent. Then list in your reply
the points where the USER must act inside the chain (drop an ISO the
vendor hides behind a form, create a provider token, confirm a login) —
they surface later as `needs_input` and the user wants to know up front
that they are coming, not be surprised card by card. Append the chain ids
to the decision repo's REVISIONS line for the re-sequencing in the same
turn, so the next session can map ids to phases without the board.

**Chain contracts: name the shared artefacts verbatim in BOTH cards.** When
a later card consumes something an earlier card produces (a golden image the
API resolves by template name, a ConfigMap a deployment mounts, a label a
selector matches), write the exact resource name into the producer's body
AND the consumer's body, taken from the consumer's config/docs (e.g. the
app's `application.yaml` default) — not from the plan's prose. Why: each
worker is correct in isolation ("ubuntu-26.04" vs template "ubuntu";
"provided by Track B" with nobody assigned), and the mismatch only surfaces
in the final e2e card as a failed verify + fix card + re-run card.

**Cross-board chains (app repo → infra repo):** `kanban link` cannot cross boards. Seed the infra card (pin bump, manifest change) with `initial_status: blocked` and a body gate "first action: read the latest orchestrator comment for the merged <app> SHA; if absent, block needs_input"; when the app PR merges, comment the full SHA and `kanban unblock`. Gate the downstream verify card behind the infra card normally. Why: a ready infra card otherwise runs before the artefact exists and blocks on a guess.

**Failed verify → fix → re-run loops are normal, not failures of the plan.** Each round: archive the failed verify card (its evidence PR is docs-only — merge it yourself, no reviewer needed), one fix card per layer that is wrong (app repo vs infra repo; decide A/B with the user only when the fix location changes the design), a fresh re-run card gated behind the fix with "do not fix here, do not decompose" and the prior rounds' PASSED checks listed as "re-run briefly, do not re-investigate". Expect 2–3 rounds for a chain with a new app + new host contracts; say so up front.

**User-held downloads behind a vendor form (eval ISOs):** before writing
"Peter downloads it" into a card, resolve the vendor's `fwlink`/download
button with `curl -sIL` — it usually 301s to a CDN object that answers 200
without the form. Then the agent fetches it on the target host itself
(`nohup curl -sL -o <file>.part …`, poll size, `mv` when complete, pin the
sha256 in the card comment since such vendors publish no hash) and the user
step disappears from the chain.

**User does a manual step ahead of the plan** (e.g. enables provider
firewall ports before the card that asks for them): comment "precondition
met, do not block for it" on EVERY downstream card that would otherwise
block needs_input for that step. Why: the card body still says "ask the
user", and the chain stalls on a question that is already answered.

**Inserting a card INTO a running chain ("so it doesn't get in the way"):**
link BOTH ways. Parent = the card currently touching the same files/repo
(`--parent <running-id>`); then `kanban link <new> <child>` for every
next-phase card that was waiting on that parent. Keep the children's existing
parent links. Confirm with `kanban show <new>` (parents + children). Use this
for orchestrator leftovers too: uncommitted docs in the main checkout
(handover, notes) go on a docs-PR card queued after the open docs/code PR.
The card body must also say to clean the main checkout after the merge.
Why: a direct commit on main while a worker PR is open causes merge conflicts. If a card did get spawned early:
kill the worker PID, `kanban reclaim`, `kanban block --kind dependency`,
`kanban link <parent> <id>`, then confirm via `task_links` (Pitfall 20) —
`kanban unblock` may answer "not blocked" because the link already parked it
in `todo`.

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
**Lane model binding (where a card's model comes from):** boards have NO
per-board or per-lane model setting. A card runs on its assignee profile's
`model:` block (`/opt/data/profiles/<profile>/config.yaml`; `default` =
`/opt/data/config.yaml`) unless the card has a per-card `model_override` /
`provider_override` column in `tasks` (query the board DB with python3
sqlite3: `select id,assignee,model_override,provider_override from tasks`).
So switching a lane's model = edit that profile's `model:` block; it applies
to every card WITHOUT an override at its next spawn (todo/ready cards and
future review handoffs), but NOT to an already-running worker. Before
switching, list open cards for that assignee across all boards and report
any `running` ones; ask whether to restart them.

Switching a profile to a cpa (CLIProxyAPI) model: list real models live via
`GET <cpa base_url>/models` with the cpa key from the main config; replace
the whole `model:` block (default/provider: custom/base_url/api_key — copy
the key from the main config in a script, never print it) and drop
llama-swap-only keys (`extra_body`, temperature); back up the file first,
validate with `yaml.safe_load`, then smoke-test with `hermes -p <profile>
-z ...`. Expiring quota (e.g. a model whose allowance ends) -> offer a
reminder to switch back, or reviews will fail.

**Lane config is a copy, not a link:** each profile carries its OWN
`config.yaml`/`.env`. When the infrastructure under the main profile moves
(LLM proxy URL, tool endpoints, API-key env names), apply the same edit to
every `/opt/data/profiles/<name>/` — a lane still pointing at a retired
endpoint shows up only as reviews that never finish. Then kill + reclaim the
lane's running workers so they restart on the new config.

**Reviewer strength:** never recommend a reviewer model WEAKER than the
worker's model — the reviewer is the last gate before main and must catch
what the coder missed; review costs few tokens, so cost is not a valid
argument for downgrading. Recommend equal-or-stronger (a different model
family is a plus when available). Check the worker lane's actual model first.

Rules:
- **Never assume the second host is up** — it is an offload, not a safety net.
  Critical work (merge-conflict resolution, protocol logic) stays on the
  strong model; routine cards (docs, cleanup, running tests) go to the offload.
- The offload model may be a different variant (e.g. VL) — quality is not
  identical; weight card difficulty accordingly.
- First turn on a lazy-loaded model costs ~100 s boot — short cards don't
  amortize it.

### 5c. Triage blocked cards / unattended chain runs
- **Find blocked cards on ALL boards** — `kanban list` only shows the current
  board: `for b in $($H kanban boards list | awk 'NR>1{print $1}'); do $H kanban --board $b list --status blocked; done`
  (skip header/marker tokens). Then `kanban --board <b> show <id>` for the
  block reason and evidence.
- **Before unblocking a card whose blocker got fixed on main:** check the fix
  commit (`git show --stat <sha>`) really covers the reported site, then
  comment on the card "sync <target checkout> to origin/main (must contain
  <sha>) before rerun". Why: the worker reruns against its stale remote
  checkout and reproduces the old failure.
- **Overnight / "keep it moving" requests:** (1) map the full chain
  (`show` each card for parents/children); (2) if any card changes running
  infra, ask the user for Gate-2 sign-off ONCE, up front, with a
  recommendation; (3) record the sign-off as a comment on every affected card
  (scope = the plan; out-of-plan → block needs_input); (4) only then create a
  bounded watcher cron (`references/board-watch-cron.md`: repeat-limited,
  `continuity: true`, [SILENT] when unchanged, reports only decisions).
  An explicit "stay on it" request counts as the explicit ask for a watcher.
  **Never say "I'll let you know" / "ich melde mich" unless a watcher job
  exists**. Without a watcher nothing ever reports back, and the user waits
  on a promise. Pick one: an in-session watcher (desktop chat; see "In-session
  orchestration loop"), a cron watcher (Telegram delivery), or say explicitly
  "you ask, I check". When the user later asks
  to "create the watcher", run `cronjob_manage list` first and answer with
  the existing job id + its last tick status instead of creating a second
  one; remove stale paused watchers from earlier phases in the same pass.
  When the chain is re-planned mid-run (cards inserted or re-gated), update
  the watcher's prompt (`cronjob_manage update`) in the same turn — a
  watcher still describing the old chain reports the new cards as
  "ungated" noise.
  When the user wants the chain to finish unattended ("I'm going to sleep"),
  get the sign-off scope as a BLANKET up front: in-plan one-time ops on the
  target hosts, reviewer merges, and in-plan operational needs_input
  questions decided by the watcher using the worker's recommended option
  (recorded as a card comment). List the exclusions explicitly:
  architecture/decision changes, other hosts, reinstalls, data deletion. Put
  the scope in the watcher prompt. Why: a narrow "deploy approved" sign-off
  still stalls the chain on the first bootstrap step nobody planned for. The
  user then asks why the card didn't just do it.
  For a "something hangs" complaint, tighten the watcher interval (5 min) and
  first check whether the card is really stuck or waits on needs_input. A
  needs_input card is not moved by any tick frequency. When the user asks
  "why didn't it progress at <time>", answer from `kanban show` timestamps
  (started/completed/blocked events) — usually a verify card was waiting
  on the deploy timer, or the chain had already moved to the next card.
- **No long-lived `blocked` cards.** The user dislikes cards sitting in
  blocked forever. When re-seeding a parked card, ARCHIVE the old one in the
  same turn (`kanban archive <id>`; the CLI has no delete verb). Do not keep
  it parked with a "superseded by" comment, because two cards for one task
  just confuse. On every board review, check each blocked card's reason. If
  the reason is gone (e.g. a STOP/freeze that has since lifted), explain in
  one or two lines what the card tests and why it is still needed, then
  offer to unblock it with a short reason comment.
- **Self-rollout cards (the update replaces the pod the worker runs in)**
  park themselves as `scheduled` until the rollout settles. Confirm the new
  version from the running instance (`hermes --version`), then comment +
  `kanban unblock` so the post-merge checks run. Such a card then often sits
  `ready` with `respawn_guarded {'reason': 'active_pr'}` every tick, because
  its comments quote the already-merged PR. Confirm the merge
  (`gh pr view <n> --json state`), age the PR-URL comments (recipe in
  `hermes-kanban`), then `kanban dispatch`.
- **Re-gating an already-blocked verify card behind a new prerequisite
  card:** comment the answer to its blocker + the new expectation, then
  `kanban link <new-card> <verify-card>` and `kanban unblock` — it lands
  in `todo` gated and resumes against the new state (e.g. a renamed
  hostname) instead of re-failing on the old one.
- **Write ops steps into infra-card bodies when the plan implies them.**
  First-deploy bootstraps (e.g. nix trusted-users on an already-running
  host), key placement, and similar one-time host changes need explicit
  scope plus the sign-off reference in the body. Otherwise a correct worker
  or reviewer blocks needs_input instead of acting, because the change is
  outside its card's stated scope.
- **Verify the host address yourself before seeding a host card.** Resolve
  it from the record that serves the host (e.g. the service A record), not
  from a placeholder FQDN or the domain apex, and run the login line once
  read-only. When the user says you set the host up earlier, find the
  address, user and key with `session_search` (search the IP or the host
  role) instead of asking. Why: a wrong-but-reachable IP makes the worker
  block with a misleading "port closed / firewall" diagnosis.
  Also check whether the host is still in the state the plan assumes (e.g. a
  plan saying "Debian -> takeover" for a host that already runs the target
  OS). If not, rewrite the card's goal in the unblock comment before it runs.
- **After a reviewer merge, check the main checkout for unpushed commits**
  (`git log origin/main..HEAD --oneline`). A reviewer that reconciles
  local main keeps a user's unpushed commit only locally. Worker worktrees
  branch from origin and miss it, so tell the user and offer a PR card.
- **Headless workers cannot overwrite system files over ssh.** The
  tool harness classifies `ssh … sudo tee /etc/<x>` as a dangerous command
  and blocks it with no approver present, so a card whose live step is
  "write the config and restart the service" ends in `needs_input` with the
  read-only findings done. Either let the card ship the change inside an
  idempotent repo script (`sudo bash scripts/<host>-setup.sh` is one
  command, not a file overwrite) or, after the user's GO, run the handful
  of live commands from the main session yourself and comment the evidence
  on the card — the worker keeps the follow-up PR.
- **Put the exact host login line in every card that touches a host**
  (`ssh -i ~/.ssh/<key> -o IdentitiesOnly=yes <admin-user>@<fqdn>`, sudo
  note). A worker without it guesses user names (hermes/root/peter), gets
  `Permission denied (publickey)` and blocks "SSH denied" — which the
  card body then forbids retrying. Before accepting such a block, run the
  correct line yourself; if it works, comment the line and unblock.

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

**Recovery when a worker self-completed (skipped review):** if a worker
called `kanban_complete` instead of `kanban_request_review`, the card is
`done` and `kanban request-review <id>` REFUSES it (it requires
`running`/`ready` status) — you cannot pull a `done` card back into review.
Recovery = create a SEPARATE reviewer card (assignee=`reviewer`) whose body
says: review the PR diff, merge it (`gh pr merge <n> --squash`), plus any
post-merge deploy the PR needs. This is the standard 2-lane pattern for a PR
that is already open but never got a review handoff.

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

### 9b. Resume-note comments on half-finished cards (comments only)
To prepare a stalled card's worker for a rebase, add ONE comment per card (`kanban --board <b> comment <id> "..."`; no status/body edits, never touch the worktree): (1) `git -C <wt> log --oneline origin/main..HEAD` + `status --short`; (2) `git merge-tree --write-tree --name-only origin/main HEAD` for conflicts vs main; (3) the same `merge-tree` between SIBLING branches that create the same files (add/add conflicts only appear once one merges); (4) state the keep-both rule for shared files and the merge order. A card without a branch gets "branch from main only after <parent> merged". Do not pipe `kanban show` into `head` (BrokenPipe traceback).

### 10. Campaign cleanup (retire a feature: card + branches + cron + wrappers)
When a feature/workstream is retired (user decision), tear down ALL its
artifacts, not just the obvious ones:
1. **Cron jobs** referencing it: `hermes cron list` (full path), `hermes cron remove <id>`.
2. **Wrapper scripts + report/state dirs** the jobs created (e.g. under
   `/opt/data/scripts/`, `/opt/data/<feature>/`) — remove with `rm`/`rm -rf`.
3. **Branches**: verify the PR is merged FIRST (`gh pr list --state all
   --search <term> --json number,state`), then `git branch -D <branch>` and
   `git push origin --delete <branch>` from the base repo. Use `-D` (force),
   not `-d`: a squash merge creates a NEW commit on main, so git does not
   consider the feature branch merged and `-d` refuses. If the worktree is
   already gone, the branches are the only leftovers. Also `rmdir .worktrees`
   if the kanban worktree left an empty directory behind.
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

## In-session orchestration loop (desktop chat, not Telegram)
Use when the user wants the orchestrator to keep driving the board in THIS
chat ("don't make me nudge you", "keep running, no fixed end"). A cron job is
the wrong tool here: it runs in an isolated session and can only report.
1. Start `python3 <skill_dir>/scripts/board-watch.py <board> 120` via the
   terminal tool with `background=true, notify=true`. The script takes ONE
   board slug — with two active boards (infra repo + its separate code
   repo) start one watcher per board and restart only the one that fired. The script exits on
   block/review/scheduled/done/new card/board idle, and the exit notification
   arrives as a new turn. It diffs against the last REPORTED snapshot (state
   file per board), so a gap between runs loses nothing, and it auto-fixes
   the `active_pr` respawn guard on `ready` cards (see (b)).
   `pkill -f board-watch.py` kills the watchers of EVERY board — after it,
   restart one per active board, or the other board goes silent.
   **Run the `pkill` as its OWN terminal call**, never chained with other
   commands (`pkill -f board-watch.py; hermes kanban comment …`): the
   pattern matches the shell running the combined command line itself, so
   the whole call dies with SIGTERM and the chained commands silently never
   run. Same trap for `pgrep -af <pattern>` inside a one-liner — exclude
   yourself (`| grep -v pgrep`) or you read your own command as the process.
   A watcher that exits with only an `unguarded active_pr` line plus a
   `tcsetattr: Inappropriate ioctl` error reported nothing: it fixed the
   guard and died on the TTY-less pod; restart it and treat the silence as
   "no event", not as "board idle".
   **"no heartbeat" on a running card** is usually a reviewer run that
   stalled on a quota wall; the dispatcher reclaims it as stale after ~20 min
   and respawns. Check `kanban runs <id>` (a `reclaimed` row followed by a
   fresh `(running)` row) and the PR state before intervening — the work is
   often already merged by the respawned run.
   **Do not run a watcher on a board that is idle BY DESIGN** (only
   `todo`/`blocked` cards waiting on a cross-board SHA or a user step):
   it exits with `IDLE … propose next` on every tick and each exit is a
   wake turn with nothing to say. Keep the watcher on the board where work
   actually runs; restart the idle board's watcher in the turn where you
   unblock its first card.
   **Strict turn-taking (user rule):** if your turn ends with a question to
   the user, start it with `--hold` instead: no reports, only the guard
   fix. When the user answers, kill the hold process and start a normal
   run; it reports everything since your last report in ONE message.
   Why: event messages arriving while a question is open stack up
   (you -> user -> you -> you -> you) and the user loses track of what to
   answer.
   **Sign-off cards loop:** a card that ends in `needs_input` ("plan ready,
   Peter decides") gets re-specified + promoted by the auto-decomposer and
   re-run by the reviewer every few minutes (seen 17x in 30 min, card
   flapping running <-> triage/review). `kanban schedule`/`block` refuse a
   card in `review`. Fix: once the PR exists, `kanban archive` the card (the
   PR is the artefact; the user's answers go into a fresh execution card).
   Better: write plan/research cards so they finish with the PR URL instead of
   blocking for the user.
   **"Peter-only merge" cards: archive at approve time.** A card whose
   only remaining step is the user's merge (live commit, rollout of the
   agents' own pod) must be archived as soon as the reviewer posts APPROVE
   and the PR is CLEAN; the PR is the artefact. Left in `review`/`blocked`
   it loops needs_input, hits `block_loop_detected`, and the decomposer
   spawns a child "Review and merge" card in the reviewer lane whose body
   says "if approved, merge it" — bypassing the user-only gate. Kill that
   child's worker before it merges, then archive child and root.
   **Auto-decomposer trigger = status `triage`.** Never move a card to triage
   and never leave one there: a needs_input block can land a card in triage
   by itself, and the decomposer then re-specifies it or splits it into
   sub-cards gated as its parents. On every wake, check for `triage` cards
   first and get them out at once (comment + `kanban unblock` -> ready).
   To re-run a blocked card use comment + `kanban unblock` (-> ready), not a
   triage round-trip. If it already split: `unlink` each sub-card from the
   parent, `archive` the sub-cards, then the parent promotes/claims again.
2. On each wake, triage in this order:
   (a) self-inflicted blockers (wrong ssh user, stale stop): comment + unblock;
   (b) `ready`/`review` cards that do not spawn: `kanban dispatch --dry-run`.
       `Guarded (blocker_auth)` after a pod restart or reclaim: the card's
       `last_failure_error` still carries the "exited rate-limited (quota
       wall)" stamp from an earlier run, but the LATEST run is now
       `reclaimed`, so the rate-limit exemption no longer applies and the
       quota regex parks the card forever. Fix: `UPDATE tasks SET
       last_failure_error=NULL WHERE id IN (...)` on the board DB (python3
       sqlite3), then `kanban dispatch`. The other
       usual cause is `Guarded (active_pr)`: it fires after EVERY unblock of
       a card whose comments quote its own (merged) PR, including
       PETER-GO gates and self-rollout cards. The watcher script ages those
       comments automatically; by hand: recipe in `hermes-kanban`, then
       `kanban dispatch`;
   (b2) restart the watcher in EVERY wake turn, also when the turn only
       answers the user. A forgotten restart silently drops a whole
       phase of events (merges nobody reported). A wake that only reports
       cards you just created yourself gets a one-line reply, no recap;
   (c) auto-decomposed sub-cards (`created {'by': 'auto-decomposer'}`):
       accept them only if they match the parent's body AND the current
       non-superseded decisions. The decomposer copies the parent body
       verbatim, so a stale design choice in an old card is carried into a
       fresh implementation card. Also read the parent's latest worker
       comments; a resume/rebase note often names that conflict. On a
       conflict, comment a STOP-POINT on the running sub-card ("do not push
       X; prepare the rest, then block needs_input"). `kanban block` on a
       running card can refuse. Then take an A/B question to the user, with
       the option that matches the current decision recommended first;
   (c2) a reviewer `done` on a deploy PR means merged and render-checked,
       not live. Report it as "merged, live not yet verified" and propose a
       read-only live verify card right away (Flux/HelmRelease Ready, PVs
       mounted, pods Running, endpoints answer, secrets synced). Why:
       render checks miss live-only gaps such as a missing volume login on
       the node or secret keys absent from the secret store. A failed
       verify becomes ONE ops fix card that repairs state and re-runs the
       same checks; archive the failed verify card;
   (c3) a verify card FAILS because of the test fixture, not the system
       under test (e.g. the test host config misses a fleet-wide pin):
       propose a fix-PR card plus a re-run verify card gated behind it
       (`--parent <fix>`). Put "do not fix here, do not decompose" in the
       re-run body, and archive the failed verify tree in the same turn.
       Why: a blocked verify card cannot be re-run against new code. Its
       decomposed sub-cards stay blocked forever.
   (c3a) a reviewer escalates `needs_input` for a STALE BASE (a sibling PR
       merged mid-review, the PR is now CONFLICTING) or for a mechanical
       contract mismatch between parallel layers: that is the
       orchestrator's call, not the user's. Comment the fix (rebase onto
       main, keep both sides; thin adapter so nothing on main is a stub)
       and `kanban unblock`. A card blocked FROM review returns to
       `review`, not `ready` — the reviewer re-runs with your comment and
       hands it to the implementer itself. Bring to the user only what
       changes what gets built;
   (c3b) the user changes a parameter of a RUNNING card (stack version,
       library, name): (1) `kanban comment` the change on the card at once
       — the worker reads comments on its next kanban call, the reviewer
       always; (2) fix the docs that state the old value in the target
       repo's own README/AGENTS.md directly (docs are exempt from the card
       rule); (3) put the plan/REVISIONS correction in the decision repo as
       a comment on the next open docs card, not as a one-line commit on
       main (it would conflict with that card's PR). Report where each
       piece landed. Users of this board prefer "latest stable GA" for
       frameworks and the newest LTS for runtimes unless the decision set
       pins otherwise — ask once, then write the preference into the
       repo's AGENTS.md.
   (c4) a parameter you chose yourself that is costly to change later
       (volume size, retention) goes into the card body AND your reply as
       "say now if you want different". Ask before the card runs.
       Soak / waiting periods (24 h stable, 7-day soak, evidence on two
       different days) are NOT defaults for this user: he fixes forward and
       accepts a hard reset / re-takeover as the fallback. Do not write them
       into card bodies; when a plan contains them, strike them in the cut
       cards and say so.
   (c4a) a chain card changes the network/netfilter state of a host the
       user actively works on (joining his desktop to k3s, adding a CNI):
       say in the seeding reply that his own services on that host
       (LLM proxy, podman port maps) can break and ask him to report it.
       When he does ("X is broken"), check the host read-only in the SAME
       turn (process start times vs the card's timeline, `curl` the
       backend on 127.0.0.1 and on the LAN IP, the proxy's state endpoint)
       and answer "yes/no it is us" with the mechanism, then put the
       next live-apply card on HOLD with a comment ("merge the PR, then
       block needs_input waiting for orchestrator GO") until the host
       is confirmed healthy. Why: a second host change on top of an
       undiagnosed breakage makes the bisect impossible;
   (c4b) the user asks for a dated reminder ("remind me in 7 days on
       Telegram"): `cronjob_manage create` with `schedule: "in 7d"`,
       `deliver: telegram`, `no_agent: true` and a tiny script under
       `/opt/data/scripts/` that prints the fixed text. Put the precondition
       into the text ("only if X has happened; otherwise the period starts
       then"), because the date is fixed while the plan step can slip.
   (c5) the user authorizes a blocked card to "investigate and fix it
       yourself" on shared infra (NAS, cluster): write the scope into the
       unblock comment. Read-only first, then a list of allowed changes,
       then a list of forbidden ones (existing volumes and targets, other
       datasets, pool export/import, key unlocks). Add "block again with
       the exact finding if more is needed". Why: an open-ended "fix it"
       on storage reaches objects the user still depends on. If the fix
       needs access the worker lacks (e.g. a NAS shell), it comes back to
       the user as one copy-paste one-liner; do not widen the access;
   (c6) a NEW card or PR you did not create appears (priority card from another
       session or the user): read its body, report what it gates and which
       host it shares with running cards, and ask the user once whether it
       is theirs. Do not stop it on suspicion. If it rolls out the instance
       you run in, say up front that the watcher will die and ask to be
       nudged after the rollout. When the user confirms a parallel session
       on the same repo, read it with `session_search(session_id=...)`, note
       its own board/watcher and the decision IDs it already used, and from
       then on check for its open docs PRs before opening one that appends to
       the shared decision files (append-only files conflict on every
       parallel append);
   (d) board idle or a phase finished: propose the next plan cards. If the
       repo has a closed decision topic (`.hermes/decision/<topic>/` with
       `STATE-final.md`), load `decision-topic-execution` first — it owns
       the precedence stack, the docs-card rule for artifact edits, and the
       revision mechanism every wave must respect. Flow:
       proposal -> user approval -> create + link cards. Never create
       unasked. Re-read the plan's current execution order first: the user
       re-orders phases mid-campaign, and that order (recorded in the plan
       via a docs card) beats the section numbering. When the user re-orders,
       ask where unmentioned phases go only if it matters now; otherwise keep
       them after the named ones and say so. A plan step with live downtime or data migration starts as
       a read-only PLAN card (measure, size, card cut, numbered open
       questions with recommendations, PR, then FINISH with the PR URL — not
       block needs_input, which triggers the sign-off loop above). After
       sign-off, record the answers in the new execution card and create the execution
       chain with `--parent` links. Cards that restart a control plane or
       touch the secret store get a GATE section: the first action is
       `kanban_block needs_input` unless a comment contains the user's GO
       word. The worker may prepare the PR before the GO.
   (d2) a plan or decision draft that comes back with N open questions:
       ask them ONE per turn, each with the recommendation first (watcher
       on `--hold` between). The user may answer "take all
       recommendations" or give a blanket "go through to X, no further
       asking". Then write that scope into the card body as the Gate-2
       sign-off ("this body = sign-off, no further GO needed"). Keep only
       genuine safety stops as needs_input, e.g. "host unreachable after
       reboot -> user hard reset". Why: a card that still says "wait for GO"
       after a blanket go stalls the chain, and a card without any safety
       stop can lock out a host that has no console.
       Re-check every worker recommendation against the mechanism BEFORE
       presenting it: the user accepts recommendations in bulk, so a wrong one
       (e.g. "drop the outer firewall rule" when the tool only opens the inner
       one) becomes a signed-off plan step. If one slips through, say so
       plainly when caught, and put the correction (old text marked
       superseded + reason) into the next docs card, not a silent edit.
   (d3) a secret only the user holds (API token, bot token): propose the
       secret store's own UI as the entry point (e.g. Infisical path +
       name), not a file drop on a build host and never the chat. The card
       then reads it from there. A host outside the trust zone (edge VPS)
       must not pull from the LAN secret store; the card copies the value
       on the build host into the OS-plane store (sops) without printing
       it. If the user cannot log in to the store, diagnose read-only
       (pod health, auth log lines, then the users table via a read-only
       SQL query through `kubectl exec` with a heredoc, names and flags only)
       before proposing a DB-level reset card behind a GO. Typical finding:
       the account exists and is not locked, and the password manager picked
       the wrong entry for a deep subdomain;
   (d4) a user conceptual question in the middle of a sign-off round ("is
       this part of Kubernetes?", "is this best practice?"): answer it
       directly first, then repeat the pending question. If the answer
       reveals a design flaw, follow the "design flaw discovered by a card" rule in `decision-topic-execution` instead of
       continuing the question round;
   (e) a needs_input that is a mechanical gap of the current decision
       (missing re-discovery, a hand-applied setting) -> create the fix
       card yourself, gated behind running migrations on the same host,
       and say "say if you want it differently". Only design choices go to
       the user as questions.
3. Restart the watcher in the SAME turn, every time. No fixed end unless the
   user sets one.
4. The watcher dies with the pod (rollout of the instance itself), so restart
   it in the next turn after a self-update.
Keep wake replies short: what changed, what was done, and at most one open
question with a recommendation.

**Answering "why is card X not claimed?":** run `kanban dispatch --dry-run`
(Spawned: 0 = nothing eligible) and build a table of each waiting card and its
open parents. Print `parents:` labelled per card
(`echo "$t: $(... show $t | grep parents:)"`). Why: grepping `parents`/
`children` from several unlabelled `show` calls interleaves the lines, which
looks like a dependency cycle that does not exist.

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
3. **Always pass `--board <slug>` to `kanban show/list/link/unblock`.** Without
   it the CLI uses the current board and reports `no such task` for a card on a
   project board; check `hermes kanban boards list` (slug usually = repo name)
   before concluding a card is missing.
   **Dispatcher may not auto-claim.** Run `hermes kanban dispatch` manually
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
    `kill -9`; (b) `kanban reclaim <id>`; (c) `kanban block <id> --kind <kind> <reason words...>`
 (the reason is POSITIONAL — a `--reason` flag prints usage and does
 nothing, leaving the card `ready` for the next tick) + reason. Verify with `kanban list` that no
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
    After a `kill -9`, `kanban reclaim` can return "not running or unknown id"
    (the kill already released the claim) and the card may sit in `blocked`
    with an EMPTY reason — skip reclaim and use `kanban_unblock <id>` to
    re-gate it into `todo` (it lands gated behind its open parents).
    **Kill, reclaim and block in ONE terminal command** — the dispatcher
    ticks every minute and re-spawns a reclaimed card before a block issued
    in a later tool call lands; check `tasks.worker_pid` afterwards and kill
    again if a new PID appeared. A card with no open parent blocks as
    `needs_input` regardless of `--kind dependency`; link the parent first
    if you want it to park in `todo`.
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
    **The input gate hook now enforces this** (R3 `review-handoff`, R4
    `no-self-complete`, R5 `pr-pflicht`, R6 `reviewer-assignment`) — a card
    body missing any of these keywords is blocked at create time — **but only when the card is created via the
    `terminal` tool.** A card created via `execute_code`/`subprocess` bypasses
    the hook entirely (it matches only terminal tools), so the gate will NOT
    catch a missing keyword on that path. The Review-Handoff block in the body
    is the real protection; the gate is a backstop for terminal creates only.
    The template below is the minimal body text that satisfies all four rules.
    **Concrete template — paste this section into EVERY PR card body** (the
    worker has no other context; without it the worker calls `kanban_complete`
    and the card skips review):
    ```
    Quality-Gate (Board-Regeln): Verteilungsregel, PR-Pflicht, Kein-Push-master, Input-Gate apply.
    ## Review-Handoff (2-Lane)
    Arbeite in deinem isolierten Worktree. Nie in dir: schreiben.
    Am Ende: PR auf GitHub öffnen (gh pr create), dann kanban_request_review
    (reviewer=reviewer) aufrufen. NICHT kanban_complete — das überspringt
    die Review-Lane.
    ```
    Keep these phrases free of backticks (the gate matches plain substrings).
    The Quality-Gate line is required too. Without it the legacy check blocks
    the create with "fehlende Regel-Kworte". Copy both blocks from a gate-passing
    sibling card (`kanban show <id>`) rather than writing them from memory.
    The hook also blocks `kanban create --help` (no body). Read flags from
    `references/input-gate.md` instead.
    Full first-try body + flags: `references/input-gate.md`.
    If the card also contains deploy/verify steps, those belong to a separate
    post-merge card, not to the PR card.
    ⚠️ **The gate is only as strong as its `terminal`-tool matcher.** The
    `pre_tool_call` hook matches only `TERMINAL_TOOL_NAMES = {terminal, shell,
    run_command, bash}` and returns 0 (pass) for any other `tool_name`. Driving
    `kanban create` from `execute_code` / `subprocess.run([...])` — the
    documented "clean way to avoid shell-quoting" for long bodies — therefore
    **bypasses the R1–R8 enforcement entirely**: a non-conformant body (missing
    the Review-Handoff section, `reviewer=reviewer`, etc.) sails through, the
    worker calls `kanban_complete`, and the card skips review (observed
    2026-10-13, kanban-tools t_b179f21b: PR #12 opened but never reviewed).
    The Rules-Block marker does NOT save you — it only skips the legacy L1/L2
    checks, not R1–R8 (which run unconditionally). Mitigation: always include
    the Review-Handoff template regardless of create path, and/or add a
    create-path-agnostic (DB-based) R1–R8 validation so the create path doesn't
    matter.
17b. **Fan-out of parallel layer cards on one codebase: fix the shared
    contracts BEFORE the fan-out, not in the layers.** When several cards
    each own one package (client layer, storage service, transport layer,
    janitor) and must talk through interfaces, put the port interfaces
    (names, methods, package) into the scaffold card or a tiny contracts card
    that is the parent of all layers. Why: two parallel workers otherwise
    each define their own `XPort`, both PRs are correct in isolation, and the
    reviewer blocks the second one needs_input asking "which contract" —
    while on main the consumer binds to its no-op stub (silent production
    no-op). If it already happened: decide it yourself (it is port
    reconciliation, not a design move), order a thin adapter in the open PR
    so nothing on main is a stub, put the unification (one interface in the
    shared package, delete the duplicate + adapter) into the integration card
    that is gated behind all layers, and tell the reviewer. Expect
    `docs/architecture.md`-style shared docs to conflict on every second
    layer merge — say "keep both" in the card bodies up front. Card bodies
    for parallel layers must name the sibling packages they must not touch.

17. **Serialize cards that share a host resource by dependency links, not by
    comments.** Cards that each run `nix build` of the same flake or use the
    same VM disk image on one host must be parent→child linked; a "check
    pgrep and wait" comment is advisory and racy. Gate the next phase's first
    card behind the last such card too. This also covers a **data dependency**
    with no shared host resource: a card that TESTS or CONSUMES an artifact
    (script, config, image) must be gated behind the card that MODIFIES it —
    otherwise the test runs against the pre-fix version and its result is
    meaningless. Link the producer as the parent.
    **Cross-session chains on one board:** a parallel session (other
    workstream) can seed cards that build on the same host while your chain
    runs, and `kanban link` refuses once its card is running. When such cards
    appear (c6), link its first host-touching card behind your running one
    at once; if it already runs, check the host (`pgrep -fa 'nix build'`),
    comment the collision window on its card (e.g. a nightly unattended build
    at a fixed time), and tell the user to relay it to the other session.
19. **A "worker crashed (pid gone)" / "gave up after repeated spawn failures"
    ping can be a STALE replay of a worker you already stopped.** When the
    named PID is one you already killed, do NOT assume the card auto-blocked
    or is looping — verify the real state first: `sqlite3 <board>/kanban.db
    "SELECT status, consecutive_failures FROM tasks WHERE id='<id>'"` +
    `ps -eo pid,cmd | grep <id>`. A kill + reclaim + link + unblock sequence
    resets `consecutive_failures` to 0 and parks the card in `todo` (gated),
    so the "gave up" never actually fires. Reacting to the ping (re-blocking,
    re-seeding) on a card that is already correctly gated just churns it.
20. **The `parents` field in `kanban show --json` / `kanban list --json` can
    read `None` for every card even when links exist — it is not a reliable
    source of dependency edges.** To confirm a `kanban link` landed (or audit
    a chain), query the board DB directly: `sqlite3 <board>/kanban.db "SELECT
    parent_id, child_id FROM task_links WHERE child_id='<id>'"`. Trust the
    `task_links` table, not the JSON `parents` field, when deciding whether a
    card is gated.

22. **Cards created before the input gate (or via a bypass path) are NOT
    gate-conformant — audit the chain before an unattended run.** Typical
    gaps: no Rules-Block marker / Done-Kriterien, "do NOT merge yourself"
    instead of the R4 phrase, `reviewer=`reviewer`` with backticks (R6 misses
    it), no Dependencies line, `scratch` workspace with a hand-made worktree.
    Fix by editing bodies (content and links unchanged); for verify-only /
    test cards with no code change add per-rule `OVERRIDE:` lines with a
    reason instead of forcing PR/reviewer text. Don't edit the body of a
    `running` card — comment instead. Propose the fix list to the user first.
    Verify retrofitted bodies against the REAL hook, not by eye: feed
    `{"tool_name":"terminal","tool_input":{"command":"hermes kanban create 'x' --workspace scratch --body <quoted body>"}}`
    on stdin to the hook script (path in config.yaml `hooks.pre_tool_call`).
    No output means pass; a `{"action":"block"...}` names the missing rule.
    Verify-only cards on `scratch` also need `OVERRIDE: workspace-worktree`
    (R1 fires whenever `--workspace` is passed). Ops-only cards are handled
    the same way: a live action with an already-merged script and no code
    change (e.g. NAS volume provisioning) gets the four OVERRIDE lines
    (workspace-worktree, pr-pflicht, review-handoff, reviewer-assignment),
    each with an "ops-only card" reason. Mirror an existing documented run
    of the script (README block) in the body with the names swapped.
    Read bodies via `kanban show <id> --json`, but stdout can carry trailing
    non-JSON warning text, so parse with `json.JSONDecoder().raw_decode` from
    the first `{`, not `json.loads`. Edit with `kanban edit <id> --body`, which
    replaces the whole body, so append to the fetched body.

21. **Completion contract on private repos without GitHub Pro: use `local-only` (the default), not `OWNER/REPO`.** An `OWNER/REPO` (or exact-PR-URL) contract triggers the PR-acceptance gate (`hermes_cli/kanban_pr_acceptance.py`), which calls the `rules/branches` API to discover required CI checks. On a private repo without Pro that API 403s ('Upgrade to GitHub Pro or make this repository public'); the gate treats it as a permanent failure and refuses `kanban_complete` forever — even on a no-CI repo where the correct answer would be 'no required checks → OK'. Workaround (per `sdlc-review` skill): set the contract to `local-only` and let the reviewer verify the merge via `gh pr view --json state,mergedAt,mergeCommit`. But `hermes kanban edit` has NO `--completion-contract` flag, so changing it after the fact needs a raw `sqlite3 UPDATE tasks SET completion_contract='local-only' WHERE id=...` on the board DB. Simplest: for boards whose repo is private without Pro, pass `--completion-contract local-only` explicitly at create time (the input gate requires the flag for `--workspace worktree`). The gate is hermes core (foreign); a 'proper' fix (treat the Pro-403 as 'no discoverable required checks') is an upstream hermes-agent contribution, not a kanban-tools change.

## Verification (definition of done)
- `kanban list` shows expected statuses; no unexpected `running`.
- Merged: `git rev-parse master origin/master` match (if pushed), no conflict
  markers, tests pass.
- Global skills (if touched) `diff -r` clean against in-repo reference.
