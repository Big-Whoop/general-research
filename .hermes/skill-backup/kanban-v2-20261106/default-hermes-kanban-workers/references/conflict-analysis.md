# Read-only Conflict Pre-Analysis for Worker Branches

Determine what would conflict when merging kanban worker branches **without
touching any working tree** — so you can present a safe merge order to the
user before committing to anything.

## Why not a scratch clone?
In this sandbox repos are owned by a different uid than the agent, so
`git clone <repo>` into /tmp fails with `fatal: detected dubious ownership`.
Instead operate **in-place in the base repo** using object-level git commands.

## Setup (once)
```bash
git config --global --add safe.directory /workspace/dev/repos/ours/<repo>
git config --global --add safe.directory /opt/data/kanban/boards/<board>/workspaces/<task-id>/repo
```

## Commands (all read-only)
```bash
cd <base-repo>

# Which files conflict when merging A into B (B's tree is the "theirs"):
git merge-tree --write-tree --name-only <A> <B>
#   -> prints a tree oid, then each conflicting file, then
#      "Auto-merging X / CONFLICT (content): Merge conflict in X"

# Full conflict hunks (the actual <<<<<<< markers):
git merge-tree --write-tree -p <A> <B> | grep -A12 '<<<<<<<'

# Common ancestor of two branches:
git merge-base <A> <B>

# What each side actually changed vs the base (to judge severity):
git diff <base> <branchA> -- <file>
git diff <base> <branchB> -- <file>

# Hunk positions per side (do the edits overlap?):
git diff <base> <branch> -- <file> | grep -E '^@@'
```

## Interpreting the result — severity ladder
1. **Only docs conflict** (`README.md`, `ROADMAP.md`, `*.md`): trivial
   editorial merge — both sides' content is kept, renumber lists. Low risk.
2. **Core script conflicts** (`scripts/*.py` etc.): manual merge required.
   Check `git diff` on both sides — if the changes are *functionally
   orthogonal* (e.g. one adds gate logic, the other adds a verify function)
   and only touch the same `main()`/helper region, it's a clean manual merge.
   If they rewrite the same logic, escalate.
3. **Incompatible-content, no text conflict**: two branches add *different*
   lines to the *same* doc section. Git auto-merges them, but the result may
   be semantically wrong (e.g. two different "drain semantics" statements).
   Read the merged output, don't trust the auto-merge.

## Worked example (originating session, 2026-09-29)
Two worker branches off an old base, `master` had moved on:
- `task/t_89e7b292-l2l3-gates` (off `d75c8b8`, 2 commits behind master)
- `task/t_8355bdb0-proxy-resolve` (off `a3bf730`, 1 commit behind master)

Findings:
- `master` × L2/L3 branch → conflicts in `README.md` + `ROADMAP.md` only
  (script auto-merged clean).
- `master` × Proxy branch → conflict in `ROADMAP.md` only.
- L2/L3 × Proxy (the two code branches against each other) → conflict in
  `README.md`, `ROADMAP.md`, **and** `scripts/reboot_llamaswap.py`.
  The script conflict was in `main()`/`ping()` — orthogonal functions,
  manual merge feasible.
- Secondary: `protocol.md` had *incompatible content* (L2/L3 added drain
  semantics, Proxy added sync docs) — no text conflict but must be read.

Recommended merge order produced: merge the larger branch first (L2/L3,
+687 lines, 39 tests green), rebase+merge the smaller (Proxy) onto the new
master, re-sync global skills from merged state, then `sync_to_prod.sh --push`.
Nothing pushed/merged until the user approved.

## Reporting to the user
Present: per-file conflict table (file | conflict? | severity), the
recommended merge order with one-line rationale, and the explicit statement
that nothing was merged/pushed. Then wait for the go-ahead (see SKILL.md §6).
