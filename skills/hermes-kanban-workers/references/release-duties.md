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

Then write the chosen scope as ONE comment on EVERY open card of the campaign
(and on every card created later). Workers and reviewers act only on
authority inside the card. The comment MUST say explicitly which of the two
the reviewer does — "reviewer: approve only, orchestrator merges + tags" or
"reviewer may merge + tag" — because a comment that only names the
orthestrator's duties is read both ways: one reviewer leaves the PR open,
the next one merges and tags itself, and the version number you promised
another card is gone. Never write a concrete next version into a card body;
write "next free `v*` tag (`git tag --list`) at merge time".

## 2. Per feature: merge -> tag -> pin -> deploy tag -> live check
1. **Merge** when the reviewer's summary says APPROVE and
   `gh pr view <n> --json mergeStateStatus,statusCheckRollup` shows `CLEAN`
   and no non-SUCCESS/SKIPPED check:
   `gh pr merge <n> --squash --delete-branch=false`. If a tag already exists
   when you arrive, check who merged — a removed cron tick or the user may
   have been faster; never re-tag.
2. **Version tag** (annotated, on origin/main after fetch):
   `git tag -a vX.Y.Z origin/main -m '...' && git push origin vX.Y.Z`.
   Feature = minor bump, mid-campaign bugfix = patch bump. CI publishes the
   image on `v*` with BOTH `:vX.Y.Z` and `:<sha>`; the infra pin uses the
   SHA tag (existing convention), so the pin card must wait for
   `gh run list --branch vX.Y.Z` to show success.
3. **Pin card** on the infra board (through the input gate, terminal
   `--body-file`, title prefix `<campaign>: pin <app> vX.Y.Z`; start from
   `templates/infra-pin-card.md` and fill the placeholders): bump
   `images[].newTag` to the merged SHA, re-sync the vendored manifests from
   the app's `deploy/` at that SHA keeping the documented local deltas,
   README line. Body says: the deploy tag is the orchestrator's step, not
   the card's. Diff the app's `deploy/` between the old pin and the new SHA
   FIRST and name the delta (new RBAC verbs, renamed env vars) in the body —
   otherwise the worker bumps only the tag and the pod fails at runtime.
4. **Deploy tag** after the pin PR is merged (annotated, per the infra
   repo's release decision):
   `git tag -a deploy-$(date +%Y%m%d)-N origin/main -m '...' && git push origin deploy-$(date +%Y%m%d)-N && git tag -fa deploy-current origin/main -m '...' && git push -f origin deploy-current`.
   N = next running number for today (`git tag --list 'deploy-<date>-*'`).
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

## 3. Mid-campaign side findings
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
- Several single-card fixes in flight at once (a consumer's bug report, a
  UI nit, a perf change): merge each as its reviewer approves, tag ONCE when
  the last one lands, one pin, one deploy. After every merge to `main`,
  comment the new SHA on each still-running sibling card that touches the
  same files ("rebase onto origin/main, keep both") — the worker reads it
  at its next kanban call, the reviewer always.
- A bug report from another session/consumer: confirm the mechanism
  read-only in the code first (grep the auth/config path it names) and put
  the confirmed cause + the exact fix into the card body; a card that says
  "investigate the 502" re-opens the design space (pitfall 12).
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

## 4. Final message to the user
One message when the last live check passes: a 2-column table (app version +
SHA, infra PRs + deploy tags, live probes, rebuilt artefacts), any incident a
worker reported in a card comment (with its status and the follow-up you
propose), then "Für Peter zu tun" numbered: his end-to-end test with the
concrete client steps first, then secret-store cleanups, then low-priority
disk cleanups with the exact one-liner, then anything you refused to touch
(changed host keys). Kill the watchers in the same turn.
