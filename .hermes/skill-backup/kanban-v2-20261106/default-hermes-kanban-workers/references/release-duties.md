# Release duties under a blanket sign-off (delegated campaign runs)

Use when the user hands a multi-feature campaign over ("übernimm die
Überwachung, Ziel: beide Features deployt") and leaves. Everything here runs
in the in-session orchestration loop's wake turns, never from cron.

## 0. Watcher hygiene during a delegated run
- One `board-watch.py` per board that currently has running cards; the
  infra board gets its watcher the moment you seed the first pin card and
  loses it (`--hold`) when the pin is merged and nothing else runs there.
- A watcher exit that lists only cards YOU just created or archived is
  self-inflicted noise: restart and answer in one line.
- Watchers die with the session; the user accepts that and restarts by
  saying "weiter" — state that limit once when you take over, not every turn.
- A watcher can also vanish with NO exit notification (seen more than once:
  a whole campaign — card merges, both feature PRs approved, the ops card
  blocked — went unreported for ~2 h until the user pinged). A bare user
  "ping" means exactly that: run the catch-up of §6 FIRST, then report. On
  every user nudge and before claiming "the watcher runs", check `pgrep -af
  board-watch.py | grep -v pgrep`; if gone, catch up per §6. Make the
  release chain script itself `kanban comment` + `unblock` the gated verify
  card on LIVE OK, so the verify never depends on a watcher. Also check it
  at the START of every turn that answers a side question ("how much does
  DISM save?", a screenshot): long Q&A stretches are exactly when it dies
  unnoticed, and an approved feature PR then waits for nobody.
- When a verify card is gated behind a MEASURE card (both load the same
  disks), the release chain must only comment on it, not unblock it; you
  release it when the measurement finishes.
- Before taking over, scan EVERY board for cards blocked since before the
  campaign: their findings are often already fixed by the campaign or are a
  bug the user's end-to-end test will hit (section 3).

## 1. Get the scope once, as a 2-option question
Recommend the blanket option first; the narrow one only lands the features
"merge-ready", which is not what "deployed" means.

1. **Blanket to deploy**: orchestrator merges feature PRs to `main` after
   reviewer APPROVE + green CI, creates `v*` tags, seeds the infra pin card,
   creates the deploy tags, decides in-plan needs_input with the recommended
   option. Exclusions stated verbatim: architecture/design changes, hosts
   outside the plan, deleting previous artefacts (old golden images), secret
   store changes, anything outside the plan files.
2. **To feature PR only**: card PRs merged by the reviewer; main merges, tags
   and infra bumps stay with the user.

The user may answer with a third shape via free text: "run unattended, but
ping me in chat when the feature PR is due — I check first that it does not
disturb other running processes". That is option 2 plus a chat duty. Wire it
as follows:
- Bake the scope into EVERY card body at create time (not only a comment):
  the reviewer merges card PRs into `feat/<feature>` only; nobody merges to
  `main` and nobody creates deploy tags.
- The feature-PR card opens the PR to `main` and hands it to the reviewer
  for APPROVE ONLY.
- Seed a deploy-gated verify card (and ANY ops card that needs the feature
  on `main` — a golden rebuild, a host script run) with `--initial-status
  blocked` (or behind a gate card the orchestrator completes after the
  merge/deploy), not just `--parent <feature-pr card>`: the feature-PR card
  completes when the PR is OPEN, so the link releases the child while the
  PR is still unmerged; it runs its precondition grep against the old
  `main`, blocks, and you pay a reclaim + `assign default` + comment +
  `unblock` round after the merge. This applies under the blanket sign-off
  too — the merge happens in YOUR wake turn, minutes after the link fires.
  Worse when the released ops card then hits a real host fault and blocks
  `needs_input` from `ready`: the auto-decomposer re-specifies and
  re-promotes it every ~2 min (observed 9 runs in 20 min, title and body
  rewritten) — `link`/`block` refuse, the only exit is the DB-park recipe
  in `cli-recipes.md` ("Park a card that is flapping through the
  decomposer"). Seeding it `blocked` from the start avoids the whole class.
- Card PRs into `feat/*` get no CI when the required gate triggers only
  on PRs to `main`; the reviewer's offline checks (e.g. `kustomize build`)
  are the only gate until the feature PR. Wait for the full gate on the
  feature PR (`gh run watch <id> --exit-status`) before merging it.
- The live-verify card is gated behind it. Its first action is
  `kanban_block needs_input` unless a comment carries a fixed GO word that
  you post after the user has merged and tagged (e.g. `PETER-GO-DEPLOYED`).
- When the watcher shows the feature PR approved, report in chat: the PR
  URL, what goes live, any control-plane restart, and the rollback (re-tag).
  Then stop. After the user confirms the merge and tag, post the GO comment
  and unblock the verify card.
- Why: the user times the deploy around other live work, and a deploy
  that is merely scheduled for a moment he did not pick is still a surprise
  outage.

A fourth shape, given once the feature PR is approved: "do the pre-tag
steps 1–N yourself, then stop and tell me". Take the numbered "Für Peter zu
tun" list from the PR body as the contract: execute exactly the steps up to
the named number (secret-store entries on bld, live IdP clients, DNS
records), run each step's own VERIFY line, and stop BEFORE the merge/tag
step even when it would be trivial. Report per step what was done and
which PR steps became obsolete because you did them differently (e.g. the
secret already matches, no copy step), then hand the remaining numbered
steps back verbatim. When a step surfaces a decision (CAA will stop renewal
of certificates issued elsewhere), stop AT that step with options +
recommendation and do not continue to the later steps until answered.
When the user then says "do all of it now", the fourth shape upgrades to
the blanket: merge every approved PR, tag once, seed the read-only verify
card and restart the watcher in the SAME turn — and warn that the pod
rollout kills this session before it happens.

A fifth shape: "I am away, you are me now" ("Du bist jetzt ich"). That is the blanket PLUS every step previously listed as the user's own (one-time host mkdir, merging a foreign-repo PR that blocks the campaign, building/pushing a test image on the build host, triggering cluster Jobs, the live enablement at the end). Comment a SIGN-OFF UPDATE on every open card naming those duties explicitly ("workers: never block needs_input for a Peter step listed here"), then execute them yourself in the same turn. When the agent's own trigger token is unreadable, do the cluster step over ssh on the control-plane host instead of waiting for the token fix. Keep the standing exclusions (no deploy tag that restarts the pod while workers run; design/decision changes still ask).

A sixth shape: the user lifts the merge gate for ONE campaign ("unattended bis zum Deployment"). Comment the exception verbatim on every open card of that campaign AND into the campaign's docs card, so the reviewer may merge reviewed, exact-head-green PRs to `main` and the release card tags without a user step. Scope it to that campaign; the repo's general user-only merge rule stays. Seed the cards so the feature-PR card never blocks for a manual merge.

Before seeding host cards from a plan, read each target host's `hosts/<h>/README.md` (or `/etc/os-release` over ssh). A plan can call a host NixOS when it actually runs another OS managed by a setup script. A wrong host-config path in a card body sends the worker into an unapplied placeholder.

When a spec card blocks with decisions for the user, relay them via clarify in plain words. Expand every product or acronym name in the question ("Synology Virtual Machine Manager, the VM app on the DiskStation"). Describe virtual devices as virtual ("the internal VM bridge", not "vSwitch"). This user answers jargon with a counter-question or a correction, which costs a full clarify round each time. A terse free-text answer ("Kubernetes") is an intent, not an option: map it to concrete variants and confirm in one follow-up question before commenting it on the card.

At seeding time under any unattended shape, also bake in: (a) **foreign unreleased commits** — the release card checks `git log deploy-current..origin/main` and, if a parallel session's merges are there, asks THAT session's orchestrator (card comment) instead of blocking for the user; the owning orchestrator's written OK is sufficient; (b) **integration-branch-only card PRs** get `completion_contract: local-only`, because a PR-URL contract demands required checks the `feat/*` base never runs and the card blocks at completion after the work is verified; (c) **runtime prerequisites discovered mid-campaign** (e.g. the deployed runner pod lacks a writable volume the next card needs) are decided by the orchestrator as a separate small manifest PR + release BEFORE the dependent card — keeps one rollback boundary per PR and avoids a PR that can only prove itself after merge.

The user also expects, in the same message that reports the approved PR,
the concrete client-side steps of his end-to-end test (which app, which
menu, what the browser will do) BEFORE anything is installed — he asked for
this explicitly; "see the PR body" is not enough, restate the numbered list
in chat.

Then write the chosen scope as ONE comment on EVERY open card of the campaign
(and on every card created later). Workers and reviewers act only on
authority inside the card. The comment MUST say explicitly which of the two
the reviewer does — "reviewer: approve only, orchestrator merges + tags" or
"reviewer may merge + tag" — because a comment that only names the
orthestrator's duties is read both ways: one reviewer leaves the PR open,
the next one merges and tags itself, and the version number you promised
another card is gone. Never write a concrete next version into a card body or the seeding reply;
write "next free `v*` tag (`git tag --list`) at merge time". A parallel
session on the same repo (or the user) tags in between — a version promised
at seeding time is often taken by the merge; if you already wrote one,
comment a correction on every card at once.

## 2. Per feature: merge -> tag -> pin -> deploy tag -> live check
1. **Merge** when the reviewer's summary says APPROVE and
   `gh pr view <n> --json mergeStateStatus,statusCheckRollup` shows `CLEAN`
   and no non-SUCCESS/SKIPPED check:
   `gh pr merge <n> --squash --delete-branch=false`. If a tag already exists
   when you arrive, check who merged — a removed cron tick or the user may
   have been faster; never re-tag.
1b. **Preflight the release path BEFORE the version tag.** Read the tag-only
   job in the app's CI (`runs-on`, builder) and every OPEN/blocked card on
   the board that names the image or release path. A tag whose image job
   cannot run (hosted runner refused, no daemon on the self-hosted pod) is
   a half-release that blocks the whole chain. When the repo already has a
   self-hosted runner for build/e2e, a parked "choose a builder" card is
   NOT a reason to wait: propose moving the image job onto that runner
   (daemonless builder such as Jib/buildah) as a card in the same turn —
   the user treats "we have a local runner" as already decided.
   A `v*` tag that already went out WITHOUT an image and without a pin may
   be moved onto the fixed `main` (delete remote tag, re-tag annotated,
   push) instead of burning a patch version — nothing references it; say so
   in one line. Never move a tag that has an image or a pin.
   **Private base image on ghcr + daemonless builder (Jib):** the release
   job's `GITHUB_TOKEN` cannot read a private package of a user account
   until the repo is added under the package's "Manage Actions access"
   (Read) — and ghcr then answers `manifest unknown`, not 401/403, so it
   looks like a wrong digest. Verify the digest yourself with a registry
   token (`/token?scope=repository:<o>/<name>:pull` → GET
   `/v2/<o>/<name>/manifests/<digest>` = 200) and put the UI step into the
   Peter step BEFORE the first tag test; there is no REST API for it.
2. **Version tag** (annotated, on origin/main after fetch):
   `git tag -a vX.Y.Z origin/main -m '...' && git push origin vX.Y.Z`.
   Feature = minor bump, mid-campaign bugfix = patch bump. CI publishes the
   image on `v*` with BOTH `:vX.Y.Z` and `:<sha>`; the infra pin uses the
   SHA tag (existing convention), so the pin card must wait for
   `gh run list --branch vX.Y.Z` to show success.
   The app repo may have ONE self-hosted runner: a tag run sits `queued`
   behind other sessions' branch runs for 10+ min. Check `gh api
   repos/<o>/<r>/actions/runners` (busy=true) and `gh run list --limit 5`
   before assuming a stuck run, then wait in a `background=true,
   notify=true` poll (bounded, e.g. 120 × 30 s) instead of foreground loops
   that hit the terminal timeout and lose their output; tell the user the
   queue position and the expected delay.
3. **Pin card** on the infra board (through the input gate, terminal
   `--body-file`, title prefix `<campaign>: pin <app> vX.Y.Z`; start from
   `templates/infra-pin-card.md` and fill the placeholders): bump
   `images[].newTag` to the merged SHA, re-sync the vendored manifests from
   the app's `deploy/` at that SHA keeping the documented local deltas,
   README line. Body says: the deploy tag is the orchestrator's step, not
   the card's. Diff the app's `deploy/` between the old pin and the new SHA
   FIRST and name the delta (new RBAC verbs, renamed env vars) in the body —
   otherwise the worker bumps only the tag and the pod fails at runtime.
3b. **Before the deploy tag of a feature that touches the agent's own
   Deployment**, decide "does the live pod restart?" from the FINAL
   feature diff (`git diff deploy-current origin/main -- <live
   deployment.yaml>`), never from an earlier card's diff — a later card can
   add a mount/env and turn a comment-only change into a rollout. If it
   restarts: scan EVERY board for `running`/`review` cards (read-only SQL
   over `/opt/data/kanban/boards/*/kanban.db`); their workers die with the
   pod and come back only after reclaim. With any running, stop and ask:
   (1) wait until those cards finish, then tag (recommended), (2) tag now
   and reclaim after. List the post-restart steps (token copies, live IdP
   client, service re-render, reclaims, release of the verify card) in
   the same message — the user must say "weiter" after the restart.
   For "wait until those cards finish", run ONE background poll script
   (notify on exit, bounded e.g. 4 h) that counts `running`/`review`/
   `ready` cards over ALL boards via read-only SQL, excluding the
   deploy-gated verify card, and exits on 0 — not a per-board watcher.
   A count that stays flat for 30+ min is a parked card, not work in
   progress. Cause seen: a reviewer `changes_requested` hands the card back
   to `ready`, but `last_failure_error` still carries the "exited
   rate-limited (quota wall)" stamp from an earlier review run; since the
   LATEST run is no longer rate-limited the exemption lapses and the quota
   guard parks the card forever — and a hand-back produces no board event,
   so the watcher stays silent. Fix: `UPDATE tasks SET
   last_failure_error=NULL, consecutive_failures=0 WHERE id IN (...)` on
   the board DB, `kanban dispatch`, relaunch the poll. Check this FIRST
   for any `ready` card older than one dispatch tick.
   Re-use the same script after the restart to time a second
   live-interrupting step (e.g. a shared LLM proxy re-render that drops
   live calls for seconds): a restarted worker counts as running.
   After the restart, before anything else: the agent pod's optional
   token Secrets are copies (`kubectl get secret <sa>-token -o
   jsonpath='{.data.token}' | base64 -d` into a 700 tmpdir, `kubectl create
   secret generic … --from-file --dry-run=client -o yaml | kubectl apply
   -f -`; cpl has no jq), and a namespace move re-creates the SA token, so
   re-copy every token whose source namespace changed; verify by byte
   count, never print the value.
4. **Deploy tag** after the pin PR is merged (annotated, per the infra
   repo's release decision):
   `git tag -a deploy-$(date +%Y%m%d)-N origin/main -m '...' && git push origin deploy-$(date +%Y%m%d)-N && git tag -fa deploy-current origin/main -m '...' && git push -f origin deploy-current`.
   N = next running number for today (`git tag --list 'deploy-<date>-*'`).
   When today's list is not empty, a parallel session tagged already:
   print each tag's commit + subject and `git diff --stat deploy-current
   origin/main` first — your feature may already be in `deploy-current`,
   and the new tag then carries only the remainder (say so in the report).
   **Two approved, independent PRs merged back-to-back** (feature PR + a
   pin PR that touches the same README/deployment lines) conflict after the
   first merge even though both were CLEAN: resolve on the SECOND PR's
   branch yourself (`git checkout -B <branch> origin/<branch> && git merge
   origin/main`, keep the first PR's rows and apply the second PR's value —
   here the image tag), push, wait ~25 s for `mergeStateStatus` to recompute,
   then merge. No re-review for a 4-line pin conflict.
   **Runtime-config retirement rides the same restart:** when the release
   replaces a login/auth mechanism, delete the old block from the pod's
   runtime `config.yaml` (backup first, YAML-validate) in the same turn as
   the tag — the rollout re-reads it; leaving it costs a second restart.
4b. **Live-verify cards that call the app API as an agent need the
   agent's credential in the WORKER environment.** Before seeding such a
   card, check it the way the worker will: `test -n "$<TOKEN_VAR>"` and one
   authenticated `curl -o /dev/null -w '%{http_code}'` (expect 200, not 401).
   If missing, look for the token in the APP's own Secret first (the
   app's ExternalSecret usually already carries the agent client's token).
   Run-without-rollout path the user prefers: every API call over ssh ON
   the control-plane host, the token read from the app Secret inside the
   remote shell (`T=$(kubectl get secret … | base64 -d | …); curl -H
   "Authorization: Bearer $T" …`), never echoed; verify one call returns
   200 yourself before handing the recipe to the card. The permanent fix
   (ExternalSecret + env in the agent's own deployment) is a rollout of the
   pod you run in — offer it as a user-timed maintenance step, never let
   the card discover the gap after the deploy.
   When the user tests the same feature by hand in parallel, comment a
   scope limit on the verify card: only its own name-prefixed artefacts
   (`e2e-*`), final check "no e2e-* left", never "only built-ins".
5. **Live check** a few minutes later, read-only: HTTP health endpoint plus a
   feature-specific probe that needs no credentials (public OpenAPI JSON no
   longer lists a removed path; a login page answers 200). Flux rollout
   takes ~3–4 minutes after the deploy tag: poll every 30 s up to ~6 min
   before calling it unhealthy. **A 200 on a page is not a pass for a
   login/session feature** — also exercise the first user action the way a
   browser does and read the response headers: `curl -s -c jar -o /dev/null
   <login-url>` then POST with the CSRF cookie and a WRONG token, and check
   that the `Set-Cookie` attributes fit the scheme the user reaches the
   service on (plain http => no `Secure`, else the browser drops the cookie
   and every login silently lands on the login page again). Two probe
   details that otherwise waste a round: (a) Spring's CSRF form value is
   the XOR-masked `_csrf` hidden input from the page HTML, NOT the raw
   `XSRF-TOKEN` cookie value — posting the cookie value gives 403 and
   looks like a broken deploy; (b) without a valid token, POST the logout
   endpoint: its clearing `Set-Cookie` runs through the same attribute code
   path as login and proves the flag set live. Keep each poll loop inside
   one terminal call under the tool timeout (≤ 6 × 30 s; split longer waits
   across calls) — a timed-out call loses the loop's output. kubectl via the
   control-plane host only when its host key is known; a CHANGED host key is
   reported to the user and never auto-accepted.
   **Pick the live probe BEFORE tagging a UI-only release.** `/ui/**` routes
   are not in the OpenAPI JSON, a Thymeleaf button adds no static artefact,
   and `app.css` only gains rules for Tailwind utilities (not for custom
   class names) — so an 8-minute poll for a signal that cannot appear
   wastes the turn. Usable signals: an API path or schema field the tag
   adds (`grep -c '"busy"' /v3/api-docs`), a new utility in `app.css`, a
   new symbol id in `icons.svg`, or a new string literal in a served JS
   file such as `/ui/ui.js` (take it from the merged diff, e.g. a notice
   text; curl the asset once before tagging to confirm it is served).
   **The signal must be ABSENT live before the deploy** — grep the live
   endpoint for it before launching the chain. A field name that already
   exists in another schema (e.g. `diskUsedBytes` on VMs when the release
   adds it to templates) matches the old pod and yields a false "LIVE OK".
   Scope the probe to the new location (parse the schema: `'x' in
   components.schemas.<New>.properties`) and, when cluster access exists,
   add the hard check: the running pod's image tag equals the new `v*`.
   Read that tag with `-o jsonpath='{.items[*].spec.containers[*].image}{"\n"}'`
   and `2>/dev/null`, never `2>&1 | grep -v kuberc`: kubectl's kuberc
   warning and a newline-less jsonpath land on ONE line, the grep drops the
   image too, and the check reads an empty tag forever. Run the probe once
   before launching the chain and confirm it prints the OLD tag.
   **A browser-facing WebSocket feature (console, terminal) needs a probe
   that replays the browser's handshake**, not a 200 on a page: log in like
   the browser (GET login page -> first `name="_csrf"` hidden input ->
   POST with the agent token read on the control-plane host), then `curl
   --http1.1` the upgrade with the session cookie, `Origin`, AND the exact
   `Sec-WebSocket-Protocol` the JS client sends, and require `101` plus the
   echoed subprotocol header. A 101 without it still fails in the browser
   (1006). User report "console does not work" + empty server log = check
   this handshake first.
   **Do not alarm on `DependencyNotReady` right after the deploy tag:**
   Flux reconciles Kustomizations in dependency order, and dependents show
   `dependency '<x>' is not ready` for a minute or two. Re-read `kubectl
   get kustomizations` + flux events after ~2 min before telling the user
   anything is broken. If
   the release has none, say so and ask the
   user for the one click; when two releases are close, verify the pair
   with the later one's signal.

### 2a. One background chain per release (no deploy/ delta)
When the feature PR is merged and `git diff --stat vOLD vNEW -- deploy/` is
empty, run steps 2–5 as ONE `terminal(background=true, notify=true)` chain
instead of a wake turn per step: poll the `v*` image run to `completed
success` (`exit 1` otherwise so a red build never gets tagged) → scratch
worktree from `origin/main`, `sed` the `newTag` line, branch
`pin/<app>-vX.Y.Z`, push, `gh pr create` → `PR=$(gh pr list --head
<branch> --json number --jq '.[0].number')` (`gh pr create` has NO `--json`
flag — it prints usage and exits 1, which under `set -e` kills the chain
right after the push) → poll
`mergeStateStatus` to `CLEAN` → `gh pr merge --squash --delete-branch` →
remove the worktree → `deploy-<date>-N` + `deploy-current` tags → poll the
live signal chosen beforehand. One notification carries the whole result
and the user sees a single running process in chat. Keep each poll bounded
(≤ 24 × 30 s). With a deploy/ delta (e.g. one new RBAC rule), keep the
single chain: put the vendoring into a small idempotent helper script the
chain calls inside the pin worktree right after the `newTag` sed — it
asserts an anchor line exists and the rule is not yet present, inserts the
rule, bumps the vendored file's `@ <sha>` header — and name the delta in the
pin PR body. Write the helper as its own file; Python with triple quotes
nested inside a shell heredoc inside another Python string breaks quoting.
**Pin PR merged by the user (infra repos: never by an agent).** Keep the
single chain, but replace the `CLEAN`→`gh pr merge` phase with a bounded
wait for `gh pr view <n> --json state` = `MERGED` (≤ 4 h at 60 s; exit on
`CLOSED`). Run the chain with `notify` = a pattern list covering EVERY
terminal line, not just the hand-off: `pin PR #` (tell the user to merge)
plus the success line (`LIVE-OK`) and every failure line (`BUILD-FAILED`,
`STOP`, `LIVE-SIGNAL-MISSING`, timeouts) — or `notify=true` for the exit.
A pattern list without the final lines leaves the deploy result unreported
and the user waits for a report that never comes.
Before launching: (1) wait for `main` CI of the last merge to be green, then
tag; (2) run the deploy-current diff check (§5) yourself and name any
foreign remainder in the launch reply (e.g. golden-build scripts that only
run on a manual rebuild are harmless to ship and say so); (3) write the
chain to a scratch script file (`set -euo pipefail`, each phase echoing a
status line, distinct exit codes for build-fail vs live-signal-missing)
and run `bash <file>` in the background, so a failure says where it
stopped. Give every terminal line a UNIQUE token (`STOP-FOREIGN`, not a
bare `STOP` that also occurs in prose) so a notify pattern cannot fire on
the wrong line. Scratch is pruned after ~24 h idle: when a release stalls
across days (waiting on a builder), comment the chain's phases on the
blocking card so it can be rewritten if the file is gone. Make every phase idempotent so the SAME script is simply relaunched
after a mid-chain failure: build poll accepts an already-green run, the pin
phase skips the worktree/push when `git ls-remote --heads origin pin/…`
exists and skips `gh pr create` when `gh pr list --head …` finds the PR,
the tag phase computes the next free `deploy-<date>-N`. A chain that dies
after the push leaves the branch; a non-idempotent rerun then fails on
`worktree add` or opens a duplicate PR. Inside the chain `cd` out of the
pin worktree before `git worktree remove` (removing the cwd's own worktree fails and leaves the branch).
Re-run the foreign-commit check INSIDE the chain right before `git tag`
(`git log deploy-current..origin/main` after a fresh fetch, abort if it
lists more than the pin): a parallel session can merge and tag while the
image builds (~5 min), and a launch-time check misses it. Write the filter
as `R=$(git log --format=%s deploy-current..origin/main | grep -v -E
'<pin subject>|<known PR>' || true); [ -n "$R" ] && { echo STOP; exit 5; }`:
under `set -o pipefail` a bare `grep -v` that filters EVERYTHING exits 1,
so the chain dies exactly in the clean case, right after the pin merge and
before the deploy tag. Call a live-check
helper that exits non-zero for "not yet" as `out=$(helper || true)` — under
`set -e` a bare `$(helper)` kills the chain on the first poll after the
tag, and the user sees an exit code instead of the live result.
**Tag image build red while `main` CI on the same SHA was green:** read
`gh run view <id> --log-failed | grep -E 'FAILED|Exception'` first. Test
timeouts only (no assertion failure) = runner flake: `gh run rerun <id>
--failed`, then relaunch the same chain script (its build poll picks up the
rerun). Say so in one line; build the rerun into the chain script (one automatic
`--failed` rerun before failing).
**`main` CI red right after a merge whose PR check was green, failing a test
the PR did not touch:** compare `git show <merge> --stat` with the failing
test's file; an assertion on state that production code releases
asynchronously (`doFinally`, a detached subscribe) read right after the
call returns is a test race, not the merge. Rerun `--failed` before
tagging (never tag a red `main`), then seed a test-only fix card that
awaits the release instead of asserting immediately; it rides in the next
tag. A second red tag run of the same test
class becomes a single-card fix on `main`, never a re-tag. The card body
lists every failing test + line from the logs and forbids "just raise the
timeout" (a request that hangs 30 s hangs 60 s too): reproduce in a loop,
fix the cause, else isolate client connections per context and label the
hypothesis unproven; require 3 green CI runs.

## 2b. "The infra card hangs" — check the required check before the card
A card whose worker finished in minutes but whose reviewer run shows only
heartbeats is usually waiting for a required status check, not stuck. Read
`gh pr view <n> --json statusCheckRollup` and then the JOB STEPS
(`gh api repos/<o>/<r>/actions/jobs/<id> --jq '.steps[]'`): a build whose
real steps are green but whose `Post <cache action>` step is `in_progress`
is the cache upload hanging (seen 10–25 min, normally 1 s). Give it a bounded
wait in ONE background poll (≤ 15 min) with cancel + rerun as the fallback,
tell the user it is CI, and leave the card alone. A job that sits `queued`, or `in_progress` with zero steps, and ignores cancel/force-cancel is a different case: a runner or GitHub incident. Re-trigger it with `gh pr close/reopen`, and comment on the card that only the new run counts. Recipe: `github-pr-workflow` → `references/ci-troubleshooting.md` § "Run stuck". Since `main` is
ruleset-protected the check must finish anyway; propose an upload timeout
on the cache action only after the second occurrence.
A required check that is RED for a runner reason (`No space left on device`
while building an unrelated host closure, cache rate limit) on a PR whose
diff touches only scripts: compare with the last `main` runs of the same
workflow (green = runner, not diff), `gh run rerun <id> --failed`, and hand
the card back to the reviewer for the merge once green. Never `--admin`
merge past a red required check without the user's explicit OK; a second
identical red is its own CI card (free disk before the build), not a
reason to bypass the gate. Proven fix shape for hosted-runner ENOSPC on Nix builds: a step before the Nix install that deletes only a fixed allowlist of preinstalled toolchains documented in the actions/runner-images README for that image, refuses `/nix`, the workspace and `/home`, logs `df` before/after and fails below a free-space floor (e.g. 20G) — no host skipped, no `continue-on-error`. Under an unattended campaign do this card yourself instead of asking for an admin merge. Before proposing that card, read the workflow's
path classifier: a rule like "everything outside hosts/ clusters/ docs =
shared input -> build ALL hosts" makes a scripts-only PR build every host
closure (the GPU host's nvidia build fills the runner). Offer the user:
(1) admin-merge this PR now (he runs/permits `gh pr merge <n> --squash
--admin`), then (2) a card that classifies host-side scripts not imported
by the flake (grep `flake.nix`/`modules/` first) as non-Nix paths. With
his OK, do the admin merge yourself, comment it on the card, `assign
default` + `unblock` so the implementer runs its post-merge steps.

## 2d. Host-only change (NixOS module, no app image): merge -> deploy tag -> host watch
When the user says "merge and deploy, watch it yourself" for a single-card
infra PR: (1) `gh pr merge <n> --squash` and confirm MERGED + SHA; (2)
`git fetch -f origin 'refs/tags/*:refs/tags/*'`, `git log --oneline
<deploy-current>..<merge-sha>` must list only your commit, then tag
`deploy-<date>-N` (next free N) + move `deploy-current`, verify both with
`git ls-remote origin 'refs/tags/<tag>^{}'`; (3) ONE background poll over
SSH (notify=true, ≤ 40 × 60 s) for the new unit to turn active, then dump
unit status, `systemctl --failed`, the port, the app log and the deploy
unit's journal in the same call. The host's deploy timer ticks within ~5
min; no card is needed for the verify. Kill any leftover PR-merge poller
you started earlier — it fires a redundant wake turn.
The watch must prove ACTIVATION, not just a green tick line. In the same loop, grep the deploy unit's journal for `Activation failed` and stop at once with the error lines. Compare `readlink /run/current-system` with `readlink -f /nix/var/nix/profiles/system`. A tick that logs "no-op: already at <tag>" after a failed switch has deployed nothing. A follow-up PR that fixes the deploy script itself may then be unable to roll itself out (bootstrap trap: `nixos-management` → `references/appliance-gui-on-server.md`). Check for that before merging, and put the one hand step into the GO question. Never stop a user-visible service as a retry trick unless the running script is known to retry.
When the user reports a symptom during the watch ("still no X", "it restarted"), read the background log and the host state (`uptime`, journal) before you answer. The user's view and the agent's chain often disagree about what actually happened.

## 2c. Sandbox load during parallel Java cards
Three Gradle builds at once (two worker cards + the reviewer's checkout) on
the 4-core sandbox mean >10 JVMs and load ~18; it is transient (2–3 min per
build). When the user asks what causes it, answer with `ps --sort=-pcpu`
mapped to worktree ids, offer `max_in_progress_per_profile` and a
`gradle.properties` cap as the two levers, and accept "leave it" — he
prefers throughput over a quiet sandbox.

## 3. Mid-campaign side findings
- **Secrets a new component needs are created by YOU via the provisioner
  path (C25), never handed to the user as a UI step**: on the build host
  `sudo /etc/opt/nixos-infra-deploy/infisical-provision.sh ensure-folder
  /<folder> && … ensure-secret /<folder> <KEY> --random <bytes>` (16 bytes
  = 32 hex for an AES-128 key; `--password` for human logins), then
  `verify /<folder>` (names only). Comment on the infra card that the key
  exists so its PR body does not list a Peter step; the value never appears
  anywhere. The user corrected a plan that asked him to type it.
- **Do a "Peter step" yourself when you have the access** (SSH to the build
  host works, only a token scope is missing). Never hand the user a
  build/push one-liner for a host you can reach. Missing GitHub scope:
  `gh auth refresh -h github.com -s <scopes>` in a background PTY, answer
  the git-credential prompt `n`, give the user the device code +
  https://github.com/login/device, verify with `gh auth status`. Registry
  push from the build host: pipe `gh auth token |` over ssh into
  `podman login --password-stdin` with `REGISTRY_AUTH_FILE` in a mktemp
  build dir, build + `push --digestfile`, then `podman logout`, delete the
  dir and confirm the auth file is gone — no credential stays on the host,
  nothing is echoed. ghcr packages of a USER account live under
  `/user/packages/container/<name>` and
  `https://github.com/users/<u>/packages/container/<name>/settings`, not
  `/orgs/...` (404); check `gh api /users/<owner> -q .type` before writing
  a URL into a card or Peter step.
- **A card waiting only on a user UI step gets re-queued by the
  auto-decomposer and split into children.** Block the first child with a
  "PARKED until <word>" reason, and once the user acts: `kanban edit <root>
  --body` (restore the original body — the decomposer rewrote it — plus a
  binding "Progress" section with what is done and what remains), then
  `unlink <child> <root>` + `archive <child>` for every child. The root
  dispatches by itself.
- **An ops card whose last step is "block needs_input with Peter's steps" loops through the decomposer** (re-promoted every ~2 min, body rewritten and truncated, worker ends up blocking "cannot read my own steps"). Split the duty instead: the ops card only verifies and COMPLETES with evidence; the orchestrator relays the user steps in chat and seeds or unblocks the post-user verify itself. If a card is already looping: `kanban block` it with an orchestrator-hold reason, read the real proposal from the board DB read-only (python `sqlite3` with `?mode=ro`, `task_events` rows `kind='worker_result'` of the early runs — `kanban show` only has the rewritten body), run the verify yourself and hand the steps over in chat.
- **User steps relayed in chat follow the same copy-paste rule:** each command alone in a fenced block, the expected result as a sentence below it, and the session/host it runs in named first ("second SSH session on ryzen"). A step that is "run this command" must say so — "I can't find step 3" means it read like a setting to look up. When the user reports a step done, verify it yourself where you have access before trusting the next one (a `uci add` without the reload leaves the route absent).
- **Hold an app feature release that needs host-side user steps** (bridge on the VM host, router route): the approved feature PR waits unmerged until those prerequisites are verified live; otherwise new resources are created against a missing host object (a bridge CNI silently creates an empty bridge) and collide with the user's later step. Say so when reporting the approval.
- **When the user says "do it directly in the repo, I merge" for a live hotfix:** skip the card, branch from `origin/main`, fix every root cause found live in ONE PR, fold any decision text the user just added (constraint addendum + REVISIONS line) into the same PR, prove render on the cluster host (`tar czf - <dirs> | ssh <cp> 'kubectl kustomize …'` when the sandbox lacks kustomize), body via `--body-file` or printf, then STOP — no self-merge, no tag until he reports the merge.
- **A deploy-tag rollback must be followed by reverting the pin on `main`.** Re-pointing `deploy-current` at the old commit leaves the broken pin on `main`; the next deploy tag (for any unrelated infra fix) rolls the broken release out again. Open the hold-pin PR in the same turn and get it merged before the next tag.
- **Prove a wrapper release against the live cluster before its pin PR** when the feature depends on new cluster objects (NADs, webhooks, device plugins): apply a hand-written throw-away resource that mirrors the release's spec (probe VM), read pod events, delete it. A release that fails only live costs tag + pin + deploy + verify + rollback. KubeVirt NIC recipe + probe template: skill `kubevirt-vm-networking`.
- **Wait for PR checks with the exit code, never by parsing the rollup**: `sleep 20; for i in $(seq 1 36); do gh pr checks <n> >/dev/null 2>&1; rc=$?; [ $rc -ne 8 ] && break; sleep 15; done` (0 = green, 8 = pending, else red), then merge only on 0. The initial sleep matters: right after `gh pr create` no checks are registered yet and `gh pr checks` exits non-zero/non-8, which reads as "red". A `statusCheckRollup` join breaks out on an empty/partial list and the merge is refused by the ruleset ("base branch policy prohibits the merge"). Address the PR by number, not by branch name.
- **The user's "merged" beats a stale GitHub read.** `gh pr view` right after his merge can still say OPEN; re-query once after ~30 s before contradicting him, and check `git log origin/main` after a fetch.
- **When the campaign merge exception ends, say so on every new card** ("reviewer APPROVES, does not merge; Peter merges; orchestrator tags after his merge") and batch the user's merges: present all approved PRs in one message with the merge order and why.
- **Under a blanket sign-off, a worker's fix-forward option for a live failure is the orchestrator's call**: seed a small single-card hotfix on `main` per root cause (paste the live evidence — exit codes, network-status, error line — into the body), merge-on-approve, next deploy tag, check live yourself, repeat. Do not hand each round to the user; report the chain once.
- **Same rule for iSCSI LUNs / zvols a new stateful component needs**: the
  orchestrator provisions them via the build host's `truenas-iscsi.sh`
  (`--dry-run` first; `ensure-zvol … --size NG --volblocksize 16K`,
  `ensure-target <n> --initiator <node> --chap-user <existing node cred>
  --chap-secret-file …`, `ensure-extent`, `ensure-targetextent … --lun 0`,
  `show`; recipe in the infra repo's `hosts/bld/README.md`), confirms the
  node's sendtargets discovery lists the IQN, and comments the target id +
  NAA on the card. Never write "Peter creates the LUN on TrueNAS" into a
  card body or a plan risk row — he corrected exactly that.
- **Text you pass to `gh pr create --body`/`kanban comment` goes through the
  terminal blocklist**: a bare filesystem-format verb in prose blocks the
  whole call ("hardline"). Write PR bodies to a file (`--body-file`) and
  describe the step as "ext4 formatting of the empty LUN" instead of the
  command name.
- **Deploy tag: record the rollback target first, point the moving tag at the peeled commit.**
  Before moving it, save `OLD=$(git rev-parse deploy-current^{commit})` and quote THAT
  SHA (plus the release tag that carries it) as the rollback target in the GO comment —
  `git log`/`origin/main` is not what is live, and the `Updated tag (was <x>)` line
  prints the old TAG OBJECT, not a commit. Then `git tag -fa deploy-current
  deploy-<date>-N^{} -m current` (no "nested tag" hint) and verify both with
  `git ls-remote origin 'refs/tags/<tag>^{}' 'refs/tags/deploy-current^{}'`.
- **Feature PR shows `CONFLICTING`/`DIRTY` with no CI run at all**: the
  branch is behind `main` on an append-only log file (REVISIONS.md). Merge
  `origin/main` into the feature branch, resolve by keeping BOTH sides
  (theirs first, then ours; dedupe identical bullets), push — CI starts only
  after the branch is mergeable. If a card merged into the feature branch
  meanwhile, your push is rejected: fetch, reset to the new tip, redo the
  merge; do not force-push.
- **A required check stuck `IN_PROGRESS` in the PR rollup while
  `gh run list` shows that run `completed/success`** is a stale rollup of
  the `changes` classifier job; when the required `test-gate` check is
  SUCCESS, merge — do not wait for the rollup to recompute.
- **A new node class in a placement decision (a workload moved to a node
  that never ran a private-registry image) needs the node's containerd
  registry config checked before the first rollout**: compare
  `/etc/rancher/k3s/registries.yaml` on the target node with the node that
  already pulls the image; a missing http:// mirror shows up only as
  `ImagePullBackOff` in the verify card. Put that check into the spec card.
  Host-setup scripts with a path-bound sudo whitelist need the new file
  added to the whitelist too — that is a root step for the user.
- **Layout/design revision while the implementing card runs**: do three
  things in one turn — a `DESIGN CHANGE … supersedes the card body` comment
  on the running card (numbered, with done-criteria), edit the bodies of
  the still-`todo` siblings that inherit the old wording (`kanban edit <id>
  --body` takes the whole body; read it via `show --json` → `.task.body`,
  no `--body-file`), and a superseding bullet in the plan's follow-up
  section. Verify at the merge event that the PR follows the new layout
  (grep the template for the new element names) before moving on.
  A spec/docs card often reaches review before its worker reads the
  comment, and the reviewer merges the old scope. At its done event, grep
  the merged artefact for the new requirement (`git show
  origin/<branch>:<file> | grep -c <keyword>`). If it is missing, do not
  reopen the card. Seed an addendum card that reuses the original body with
  the goal narrowed to the missing section, `kanban link` it before the
  first consumer card, and comment a gate on every card that needs the
  missing part ("wait for section X on origin/<branch>"). Leave the cards
  that only need the merged part running. Record a new requirement as a
  decision-file revision through a docs PR in the same turn, then quote the
  same binding paragraph on every affected card.
  Also gate a running implementation card that depends on the missing part:
  it must block needs_input instead of guessing when the section is absent.
- **A cookie `Secure`-only-on-https fix becomes dead code once TLS lands**
  (gateway 301s http→https); say so when the TLS change shows up in a
  diff, do not file a card to remove it.
- **Post-merge steps in a PR card's body (copy a script to a host, then
  block for the user's root run) are not executed by the reviewer lane**:
  the reviewer merges and blocks/completes, the implementer never resumes.
  Plan to do such a step yourself right after the merge event (copy, print
  the sha256 of the file from `origin/main`, compare host vs local, comment
  on the card) and hand the user the one-liner in chat; or seed it as its
  own ops card gated behind the PR card. When announcing a user step whose
  script a card has yet to write, say where it WILL land and that nothing
  is due yet.
- **Another session's watcher may already run on a shared board**
  (`pgrep -af board-watch.py`): do not start a second one there (the state
  file is per board, two watchers race on it); check that board by hand on
  each of your own wake turns instead. **Kill watchers only by pid (`kill
  <pid>` from the process handle), never `pkill -f board-watch.py` — not even
  with the board slug appended, and never chained after other commands in the
  same terminal call (the pattern also matches the tool's own shell line, so
  the call dies with SIGTERM)** — the
  pattern matches every session's watcher on every board, and the other
  orchestrator sees an unexplained SIGTERM exit. Conversely, when YOUR
  watcher dies with SIGTERM you did not send, run the pgrep first: a
  parallel session has probably cleaned up and started its own; if it now
  watches your board, do not restart yours — ask the user which session owns
  the campaign and hand over, instead of two sessions reporting the same
  events.
  **Taking over a campaign from a parent session (delegated monitor):** run
  the pgrep BEFORE your first watcher start, not after your watcher dies.
  The parent's watcher is usually still alive and the two race: the parent's
  cleanup SIGTERMs yours a few minutes in. If one is found, ask ONE clarify
  question ("kill theirs and watch alone" recommended vs "leave it, check on
  ping"); the user's standing answer is that the delegated session watches
  alone — kill the foreign pid, start yours, state it in one line.
- **A reviewer summary "approved, not merged, per card" on a `main` single-card fix means the merge is yours**: merge + patch tag in the wake turn where you read it (the card is already archived, no further event will remind you).
- **User nits that arrive while the campaign runs** (a button label whose `+` suggests addition where the value is set, a dock idea, "merken für den nächsten Schwung"): append them to the plan file's follow-up section with the mechanism already resolved (which widget, which fallback, what the component supports) and reply in one line; do not touch running cards and do not seed cards until the user asks. A "can X also go there?" question gets the mechanism answered first, then the same plan-file entry.
- **Post-deploy tweak requests** ("noch eine Kleinigkeit … wieder von A–Z
  überwachen": form defaults, labels, a flag): same pipeline, no new
  sign-off question — single-card fix on `main`, patch tag, pin card,
  deploy tag, live probe, watcher restarted in the same turn. Write the
  layer boundary into the card body (e.g. "UI form defaults only; API
  defaults for agents unchanged") so the worker does not widen a cosmetic
  request into a contract change. A feature's own bug found by the user's
  first click (login loop) is handled the same way; distinguish it from
  pre-existing infra gaps (no TLS listener => https 404) and say which is
  which.
- An old verify card whose failures the campaign fixes partly: archive it
  with a comment mapping each FAIL to its fix, and seed a single-card fix on
  `main` for the remainder (patch tag, rides in the next pin). Do not leave
  the old card blocked.
- **A live verify that passes one half and fails the other** (Linux PASS,
  Windows FAIL): keep the SAME card. Delete its failed artefacts yourself
  (VM + FAILED template) in the decision turn, seed the fix card, `kanban
  link <fix> <verify>`, comment "half X passed — do not re-run it; re-run
  only half Y with new names after tag vX.Y.Z+1; gate: tag exists", then
  unblock (it parks in `todo`). Warn the user if his own in-flight use of
  the feature will hit the same bug before the fix deploys, and what to do.
- **A user troubleshooting in the guest by hand while a fix card runs**
  (pasting log lines turn by turn): answer each line with the documented
  cause, and in the SAME turn comment the finding as a numbered "LIVE
  FINDING" on the running fix card (mechanism + exact change + pre-check),
  correcting an earlier finding in place when the user disproves it ("I
  used the classic installer"). Before telling the user a remedy, check it
  is actually available to him — a "reinstall it differently" advice that
  the vendor's own installer cannot satisfy costs him another broken VM.
  Recommend stopping hand repairs after the second failed round (fresh
  clone after the fix deploys).
- Several single-card fixes in flight at once (a consumer's bug report, a
  UI nit, a perf change): merge each as its reviewer approves, tag ONCE when
  the last one lands, one pin, one deploy. After every merge to `main`,
  comment the new SHA on each still-running sibling card that touches the
  same files ("rebase onto origin/main, keep both") — the worker reads it
  at its next kanban call, the reviewer always.
- A bug report from another session/consumer: confirm the mechanism
  read-only in the code first (grep the auth/config path it names) and put
  the confirmed cause + the exact fix into the card body; a card that says
  "investigate the 502" re-opens the design space (pitfall 12). Give the
  card the fix that ships regardless of the deeper cause (e.g. offer the
  credential the API already owns as a second auth method) PLUS a bounded
  read-only investigation of the deeper cause (max 30 min, "document the
  finding; apply only if it is X") — a guest-side provisioning hook that
  never ran (no AutoLogon => FirstLogonCommands never fire) is the typical
  second layer.
- **Two user bugs in one message share one tag**: seed them as separate
  cards (disjoint files), gate the one touching the same templates as a
  running card behind it, and tell the user both land in the next tag.
- **Orchestrator commits in a shared main checkout: stage explicit paths,
  never `git add -A`.** Repos that host `.worktrees/` carry embedded git
  dirs (they become gitlinks) and untracked plan files; both ride into the
  commit and the PR silently. Add `.worktrees/` to `.gitignore` when it is
  missing, and read `git show --stat HEAD` before pushing.
- **"It is one line, do it yourself"** (user's explicit per-instance OK to
  skip the card): branch from origin/main, make the fix + a regression test,
  prove RED without the fix (stash the main-code change, run the one test,
  read the failure from `build/test-results`), then GREEN + full build, then
  a PR (main is ruleset-protected), merge on green CI, patch tag, normal
  release chain. Say in the reply that the card rule was bypassed on his OK.
  If the next small fix is bigger than one line (say 60-100 lines + tests),
  state the size and offer "I do it myself the same way" (recommended) vs
  "card"; he picks self-implementation for contained single-file fixes.
  The live check for such a fix proves the symptom path (e.g. served JS
  contains the new table + pod image tag), never a pre-existing field.
- Test-only or flake fixes merged mid-campaign get NO tag of their own;
  they ride in the next feature's version tag. A behaviour fix the user's
  end-to-end test depends on gets a patch tag at once, but still no separate
  pin/deploy when the next feature pin is less than a few hours away.
- A dependent second feature whose first card gates on "feature 1 on
  main": after the merge, comment the SHA on that card and `unblock` if it
  already blocked; if it is still `todo` the link releases it.
- Report to the user only: merges/tags/deploy tags done (one line each),
  decisions taken, out-of-scope blocks with options + recommendation,
  failures (CI red twice, live check not healthy). Collect every "Für Peter
  zu tun" leftover from card summaries for the final message (secret store
  cleanups, manual client checks, his end-to-end test).

- **A single-card fix merged to `main` while the feature PR is open**
  usually conflicts with the feature branch on the shared JS/template file
  (`git merge-tree --write-tree --name-only origin/main origin/feat/<x>`
  shows it). Do not resolve it on the main checkout: seed a small
  reconcile card on the feature branch ("merge origin/main, keep both,
  re-review PR #n") and merge the feature PR only after its re-approval.
  Tell the feature-pr worker in advance (comment) to wait for a fix that is
  about to land so the version tag contains it.

## 5. Replacing the manual pin card: Flux Image Automation as PROPOSAL only
When the user asks "can Flux pull the latest release itself?" and the infra
repo has a no-automatic-updates constraint plus tag-pinned deploys, the
answer is Flux Image Automation in proposal mode — never auto-deploy:
- `image-reflector-controller` + `image-automation-controller` added to the
  declarative Flux install (`flux install --export
  --components-extra=image-reflector-controller,image-automation-controller
  --version=<version already in gotk-components.yaml>`, diff = additions only).
- `ImageRepository` next to the app's pull secret (same namespace),
  `ImagePolicy` semver on the `v*` tags only (`filterTags.pattern:
  '^v(?P<ver>\d+\.\d+\.\d+)$'`, `extract: 'v$ver'`), so SHA tags never
  match. Keep the `v` in `extract`: the extracted string REPLACES the tag
  and is what the Setter writes into `newTag`; `'$ver'` would pin a bare
  `0.3.3` that no image carries (a reviewer caught exactly this).
- `ImageUpdateAutomation` checks out `main` and PUSHES TO A DIFFERENT BRANCH
  (`git.push.branch: flux/image-updates`) with a SEPARATE write deploy key
  (own GitHub deploy key, private half in the secret store -> ExternalSecret).
  The read-only key and the `deploy-current` GitRepository stay untouched.
  Humans/orchestrator merge that branch's commit to `main` and create the
  deploy tag as before; the pin card disappears, the release boundary stays.
- Setter marker on the existing `newTag` line
  (`# {"$imagepolicy": "<ns>:<policy>:tag"}`); the pin value changes from
  SHA to `vX.Y.Z` — record that as a REVISIONS entry against the SHA-pin
  convention, and state in the card body that nothing deploys automatically.
- Rejected alternative, say why if asked: a second GitRepository on `main`
  only for the app path takes the app out of the release tag (constraint
  change); Flux has no image-update path that bypasses git.
- Gate this card behind any still-running pin card (same `newTag` line).
- Verify after the deploy tag: `git ls-remote --heads origin flux/image-updates`
  appears within ~10 min (controller interval) and `git diff origin/main
  origin/flux/image-updates` is the one `newTag` line (SHA -> `vX.Y.Z`,
  same image) — that no-op-looking commit IS the proof the loop works. Poll
  with `sleep 60` x 6 inside ONE terminal call (under the tool timeout);
  do not wait for a kubectl view of the controllers when the branch already
  proves the loop.
- **Release flow once automation is live (replaces step 2.3):** push the
  app's `v*` tag -> wait for the proposal commit on the branch -> open the
  PR yourself (`gh pr create --base main --head flux/image-updates`, body in
  the Für-Peter format) -> seed a REVIEW-ONLY card for it on the infra board
  (assignee `reviewer`, `--workspace scratch`, body: verify diff is the one
  `newTag` line, the `v*` tag derefs to a main commit, the image CI run
  succeeded, `kustomize build` renders the new image; merge if green, never
  tag deploy). Such a card needs SIX override lines or the input gate
  blocks it twice: workspace-worktree, pr-pflicht, review-handoff,
  reviewer-assignment, worktree-isolation AND no-self-complete (the card
  completes itself after the merge). -> deploy tag -> live check. No pin
  card any more; the app's `deploy/` re-sync (RBAC, env renames) is the one
  thing automation cannot do — diff it per release and seed a card only
  when it changed.
- **The proposal branch is NOT rebased by Flux** (full recipe in SKILL.md "Flux image-automation proposal PRs"): check `merge-base --is-ancestor` first; when behind, re-apply the one `newTag` line on a `pin/<app>-vX.Y.Z` branch from `origin/main` in a scratch worktree, never force-push Flux's branch. A `git cherry-pick` of the proposal conflicts on that very line — `--quit` it before switching branches. After several proposals were squash-merged, the branch additionally carries those merged-but-non-ancestor commits: it looks *ahead* of main and `git diff origin/main origin/flux/image-updates` is full of unrelated stale-file noise. Never review the branch diff — validate the NEWEST proposal commit itself (`git show <sha>` must be exactly the one `newTag` line with the setter marker intact, one file) and re-apply that line on a fresh `pin/` branch from `origin/main`; `gh pr create --head flux/image-updates` on such a branch would ship the noise.
- **The proposal PR must still carry the app's `deploy/` delta.** Before merging a Flux proposal (or your re-applied `pin/` branch), `git diff --stat <old-tag> <new-tag> -- deploy/` in the app repo; a changed `rbac.yaml` (new verb such as `patch` for a label-editing endpoint) or an env rename goes into the SAME pin PR (edit the vendored file, bump its `@ <sha>` header comment). Automation bumps only the tag; the pod then answers 403 or crashes on the first use of the new feature.
- **Before every deploy tag on a shared infra `main`:** run `git fetch origin main` FIRST — a tag-only fetch (`git fetch origin 'refs/tags/*:refs/tags/*'`) updates `deploy-current` but leaves `origin/main` stale, and the "what rides along" diff then reads misleadingly EMPTY. Then `git diff --stat deploy-current origin/main | grep -v '\.hermes/\|\.md '`
  and tag only if the remainder is your own change. A parallel campaign
  (another session's feature on the same repo) may have merged manifests
  that are not meant to go live yet; docs/research commits are harmless,
  manifests are not — report them to the user instead of tagging.

## 5b. Protecting `main` (user asked "nur per PR schreibbar?")
Private repos without GitHub Pro have no classic branch protection — use a
**ruleset** (`gh api -X POST repos/<o>/<r>/rulesets --input rs.json`):
target `refs/heads/main`, rules `deletion`, `non_fast_forward`,
`pull_request` with `required_approving_review_count: 0` (the reviewer lane
is our process; GitHub approvals would need a second account and block every
merge), `required_status_checks` = the checks that run on PRs (not the
tag-only image job; for the infra repo only the gate job, conditional jobs
block forever), `bypass_actors: []`. Then
`gh api -X PATCH repos/<o>/<r> -f allow_auto_merge=true` so docs PRs can
`gh pr merge --squash --auto`. Prove it with a throw-away push to `main`
(expect `GH013`), then `git reset --hard origin/main`. Update AGENTS.md:
docs still need no card/review but go through a self-merged `docs:` PR —
plan files pushed straight to `main` stop working.

## 6. Resuming after a Hermes backend restart ("Backend neu gestartet, Watcher anwerfen")
The watchers died with the pod; the board kept moving (reviewer merges, archives). Do in ONE turn, before restarting any watcher:
1. `pgrep -af board-watch.py | grep -v pgrep` (expect none) and a liveness table of `running` cards: `select id,worker_pid,status from tasks` + `ps -p <pid>`; reclaim only the dead ones (pitfall 0).
2. Catch up on releases the watcher never reported: `gh pr list --state merged --limit 6` per app repo and `gh pr list --state open` — an APPROVED-but-unmerged single-card PR whose card is already archived is yours to merge + patch-tag now (the reviewer leaves the main merge to the orchestrator under the sign-off).
3. Restart one watcher per board with running cards. Report the gap in a few lines: what merged meanwhile, what you merged/tagged, what still runs.
Several patch tags close to a feature tag: pin/deploy ONCE with the feature version, not per patch.

## 4. Final message to the user
One message when the last live check passes: a 2-column table (app version +
SHA, infra PRs + deploy tags, live probes, rebuilt artefacts), any incident a
worker reported in a card comment (with its status and the follow-up you
propose), then "Für Peter zu tun" numbered: his end-to-end test with the
concrete client steps first, then secret-store cleanups, then low-priority
disk cleanups with the exact one-liner, then anything you refused to touch
(changed host keys). Kill the watchers in the same turn.
