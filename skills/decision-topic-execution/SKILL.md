---
name: decision-topic-execution
description: "Build or board work under a closed decision topic dir."
version: 1.0.0
author: Peter Fahsel, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [decision-execution, precedence, revisions, implementation, governance, kanban]
    related_skills: [decision-narrowing, hermes-kanban-workers, plan, deep-research]
---

# Decision-topic execution contract

Rules for every session, subagent, or kanban orchestrator that implements, plans a wave, or tidies up under a CLOSED decision topic (`.hermes/decision/<topic>/` with `STATE-final.md`). The topic's artifacts stay the binding rulebook while the chosen path is built. This skill decides nothing new and does not run the narrowing loop — that is `decision-narrowing`; it does not plan — that is `plan`, always invoked with the explicit target path `<topic>/plans/YYYY-MM-DD-<slug>.md` (its default `.hermes/plans/` is outside the topic). Load it once per implementation session; it is short on purpose.

## When to Use
- Starting a session that implements or boards work (kanban wave) under a closed topic.
- Hitting the first conflict between what you are about to build and what the artifacts say.
- A user asks to re-plan, move a phase, tidy up a topic, or revise a decision on-target.

## When NOT to use
- The narrowing loop is still running → `decision-narrowing`.
- Work no decision loop ever governed → nothing to enforce.
- The design space itself must move → back to `decision-narrowing` or the user.

## Contract

**Reading levels — descend only as far as the task needs.**
- **L0 (every session):** topic `README.md` → `CONSTRAINTS.md` → non-superseded `DECISIONS.md` entries → the plan. Completion: you can name, by id, which C#/D# the task at hand sits under.
- **L1 (on conflict or "why"):** `STATE-final.md`, `REVISIONS.md`, and the manifest line in `research/README.md` for the affected file.
- **L2 (only to revise or re-validate):** one research file, the sections the manifest points at. Never bulk-read the corpus — that is drift back into stage 2 and how a STALE line resurrects a dead path.

**Precedence stack:** repo ground rules (`AGENTS.md`) → CONSTRAINTS → DECISIONS → plan. The higher tier always wins and is never edited; the lower artifact is corrected to match. Implementation contradicts plan → fix the plan. Decision contradicts constraint → the decision is retired by a formal revision, never routed around with a flag. Constraint contradicts a ground rule → stop, surface to the user; the constraint was never valid.

**Formal revision (the only way a decision changes after close).** Live evidence (failed test, measurement, on-target conflict) → NEW `D#` continuing the sequence, status "revised during implementation", the superseded id, the evidence, the new rationale, and a per-constraint re-validation written out entry by entry (passes included). The old entry gets a single appended `SUPERSEDED by D#` marker — scoped to the sub-part when the old entry bundles several (**partial supersede**; state what remains in force). If the original Rationale cited a research file, re-open it at L2 and check whether the new decision contradicts the evidence or a misreading. Ids are never reused or renumbered. If the new decision violates a constraint → file nothing, surface to the user: **constraint changes are the user's alone**, filed as a new superseding C# by the user-authorized session.

**On-target decisions and the plan.**
- A deferred live item (parked in the loop) that turns out to change WHAT gets built → `D#` with source "on-target test <name>, <date>" the session it is decided — never only in a commit message, card comment, or chat. A test that merely confirms the paper decision → note in the plan task, no entry.
- The plan is the least stable artifact: reshape it freely within the C#/D# set; every change beyond detail (re-sequenced phase, dropped task, new component) → one line in `REVISIONS.md` (append-only) naming what, why, and which C#/D# it still satisfies.
- A user request "re-plan / move X" is classified out loud before touching anything: re-sequencing → plan + REVISIONS line; a change in what gets built → D# (with a docs-first research note into `research/` first if the component is not in the corpus); anything moving a constraint → user. Then the dependency pass: move coupled phases together and list later-phase text that assumed the old order.
- A user operating policy ("updates never automatic", backup rules, report cadence) is a CONSTRAINT, filed verbatim-in-intent the session it is stated; the HOW stays plan text marked "decision pending".
- `STATE-final.md` is frozen evidence; implementation progress never goes there.

**Kanban-campaign compatibility** (`hermes-kanban-workers` is the delivery pipeline for code work):
- During a campaign, `CONSTRAINTS.md` / `DECISIONS.md` / `REVISIONS.md` / plan edits land through a **docs card** (its PR), not as direct commits on `main` — append-only files conflict on every parallel append, and a worker sees only committed files.
- An answer or revision that cannot be filed yet (open docs PR) is parked the same turn as a `kanban comment` on the card that will file it, or in the body of the queued docs card; tell the user where it is parked. Chat-only answers are lost at compaction.
- A running card whose parameter the user changes: comment on the card at once (worker reads comments on its next kanban call), fix the target repo's own docs directly, and put the plan/REVISIONS correction into the next docs card.
- A design flaw discovered by a card ("does this match best practice?") → answer honestly (matches / deviates on purpose per C# / would change now, from knowledge not research), propose a `deep-research` round that drafts the revision, hold the dependent PR with a card comment, and let the user pick; file the pick as the formal revision in the same docs PR.
- Cards for the next phase are proposed, never created unasked; re-read the plan's current execution order (user re-orders mid-campaign) before proposing.

**Cleanup pass** (user asks to "look around / tidy up"): read L0, `git status`/branches/worktrees, the board; present a numbered PROPOSAL (plan text contradicting a higher tier, README open-items listing finished work, C#/D# range lagging, stale skill references) and execute only what is approved. Verify each claimed-stale item read-only first.

**Execution pitfalls:** the quiet workaround (build and a non-superseded D# diverge — if any live D# does not describe what the build does, file the revision before continuing); the in-place edit ("it was never meant that way"); renumbering superseded ids; last-round-only re-validation; batch-recording deferred answers at phase end; a plan task written from an inferred live-state premise (check `git log -- hosts/<h>` and deploy notes, say which); starting a phase without listing irreversible parameters (CIDRs, disk layout, key identities, cluster names) — conflicting values go to the user as one question before the card runs.

## Verification
- Every non-superseded D# describes what the build actually does (spot-check one against real code/config, not the plan).
- Append-only files show zero edited lines since close: `git log -p --follow .hermes/decision/<topic>/DECISIONS.md` (same for CONSTRAINTS.md).
- Every revision entry carries superseded id, forcing evidence, per-constraint re-validation (failures included), source.
- Plan deferred-items, OQ notes, and filed D# account for each other one-to-one.
- Cold-reader test: L0 files alone state precedence, current architecture, open items; L1 explains each revision.

## References
- `references/agent-host-access.md` — staged sudoers drop-ins for agent access to a user-owned, non-fleet host.
