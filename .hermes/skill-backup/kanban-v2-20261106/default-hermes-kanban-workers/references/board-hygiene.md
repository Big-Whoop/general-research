# Board Hygiene Pass — audit all boards, archive stale cards

Class of task: "go over all boards and archive outdated cards". Archive is
reversible and the only terminal verb (no delete); `--rm` is the hard purge —
never use it unless explicitly told.

## Procedure

1. **Inventory before deciding anything.** Capture `kanban boards list` output
   (before-counts) per board. Extract slugs carefully: skip the `SLUG` header,
   the `●` current-board marker, and the trailing `Current board:` /
   `Switch boards with...` footer lines — filter to `^[a-z0-9-]+$`.

2. **Dump each board's cards to a FILE, never parse stdout:**
   `$H kanban --board $b list --json --sort updated > $SCRATCH/$b.json`
   then `json.load` the file. A full-board `--json` (hundreds of cards) exceeds
   tool stdout limits and comes back head+tail-truncated, which makes
   `json.loads` fail; the redirect to disk is the stable path.

3. **Classify — age is only decisive for `done`:**
   - `done` with `completed_at` older than ~7 days → archive (user's cleanup
     rule). The last week's done cards stay visible.
   - Open cards (`todo/blocked/ready/review/...`): age alone is NOT a reason.
     Read the last comments (`show --json` → comments), created date, and
     whether a successor card superseded the work.
   - A card parked on an EXTERNAL gate must be verified live before judging:
     upstream PR state via `https://api.github.com/repos/<org>/<repo>/pulls/<n>`
     (read `state`/`merged`, don't trust the card's last-known view), and
     `hermes cron list` to confirm the watcher job still exists — cron jobs are
     per-profile. A parked chain whose watcher vanished has no trigger anymore:
     report it to the user, do not silently archive the chain.
   - Cards stopped by an explicit user STOP or waiting on a manual user step
     (e.g. a desktop checklist) are active backlog, not stale — keep and say so.
   - Blocked card whose blocker is GONE → unblock-with-reason offer per §5c,
     not archive.

4. **Bulk-archive per board:** `$H kanban --board $b archive <id> <id> ...`
   (~60 ids per call). It runs seconds per card, so a fleet-wide pass exceeds
   a 5-min execute_code cell timeout. Recovery after a timeout/interruption:
   re-derive the remaining ids from a FRESH `list --json` (status filter +
   date threshold) — never re-run from a stale plan file; a duplicate
   `archive` prints "cannot archive", which means already-done, not an error
   (confirm via `show <id>` / status grep).

5. **Verify by count diff:** re-run `boards list` and check archived/done
   deltas match the per-board plan exactly before reporting. Report a per-board
   table (archived / remaining open / remaining done) and explicitly list the
   open cards you did NOT archive with the evidence-backed reason for each.
