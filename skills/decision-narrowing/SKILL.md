---
name: decision-narrowing
description: "Narrow a deep-research corpus to one path (user loop)."
version: 0.5.0
author: Peter Fahsel, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [decision-making, constraints, design-space, orchestration, delegate_task, subagent, planning, convergence]
    related_skills: [deep-research, decision-topic-execution, feature-spec-qa, plan, hermes-kanban-workers, system-engineering-orchestration]
---

# Decision Narrowing Skill

Turn an options-complete research corpus (from `deep-research`) into **one chosen implementation** by iteratively narrowing the design space. The user fixes **CONSTRAINTS** (for or against, at the abstract level) and — once a fork has become small enough — falls **DECISIONS** (for, on a concrete technology). Between user moves, a subagent enumerates the surviving paths, the open axes, and the highest-leverage next move. The loop repeats until exactly one path remains or the remaining choice is trivial — **there is no round budget: it is done when it is done** (decision 2026-10-18). It is the *decision* phase after the *research* phase: `deep-research` (stage 1) produces the options-complete corpus, this skill (stage 2) narrows it to one path, and `decision-topic-execution` (stage 3) governs implementation under the same artifacts. The three stages share one directory: `.hermes/decision/<topic>/`.

No corpus to narrow, just a feature design to settle question by question → `feature-spec-qa` instead.

## The core distinction: CONSTRAINT vs DECISION

Two levels, two file types, two kinds of user input. Confusing them is the main failure mode of this skill — check every incoming statement against the table before filing it.

**CONSTRAINT** — a for-or-against statement about an *abstract construct* (a pattern, a principle, an architectural boundary). It carves the design space: eliminates whole regions of paths at once, without committing to any product.
- For: "Wir stellen nur VPN-Verbindungen zwischen Containern her."
- Against: "Wir stellen keine VPN-Verbindungen zwischen Hosts her."
- A statement may combine both: "Keine VPN-Verbindung zwischen Hosts, sondern nur zwischen Containern."
- A concrete product name is allowed **only in the against-direction** (a veto: "kein Produkt X"). A for-statement that names a product is NOT a constraint — it is a DECISION.
- Edge case: a requirement that names a product as the MECHANISM ("soll per QEMU laufen", "k8s-basiert") is a constraint on the mechanism, not a pick among candidate implementations — file it as a constraint with an explicit note that the concrete implementation within that mechanism remains a DECISION.

**DECISION** — a *for-only* statement about a *specific technology* (a named product, a concrete implementation).
- For: "Wir benutzen die Kxs Gateway Technologie."
- A decision is never "against" — against lives in constraints (abstract) or eliminations (derived).
- Only the user falls decisions. The subagent may *recommend*; it never *falls*.

| | Level | Direction | Names a product? | File |
|---|---|---|---|---|
| CONSTRAINT | abstract construct | for or against | only as veto (against) | `CONSTRAINTS.md` |
| DECISION | concrete technology | for only | yes — that is the point | `DECISIONS.md` |

Interaction: constraints eliminate broad regions; a decision fixes one concrete technology and thereby eliminates every surviving path that does not use it. A decision is valid only against the current constraint set — if it violates a constraint or a veto, stop and surface the conflict (supersede or veto) instead of filing it.

**Soft / indicative statement** — a third input type: the user sketches a preference without committing ("kein harter Constraint, aber so ungefähr", "ich würde ungefähr X machen"). It is **neither** a CONSTRAINT **nor** a DECISION — filing it as one over-commits and lets a casual phrasing eliminate paths. It goes to `PENDING.md` as an `S#` entry (see Artifact formats): it shapes the recommendation and how you phrase the question, but eliminates nothing. Promote it to a constraint or decision only if the user later states it as a firm requirement or an explicit pick.

**Environment fact** — a fourth input type: a statement about the current state of the world (hardware, OS, versions, what is already installed and working) that carves the design space but is neither for/against nor a product pick. Filing it as a constraint lets a fact rot into a rule that later mis-eliminates. Persist it as a dated environment-update file in the corpus (`research/env-<host>-<date>.md`), add a manifest row, and cross-reference it from any constraint entry that relies on it; the subagent picks it up via the corpus, and it enters the round's `Inputs:` line. When it supersedes an assumption baked into the lane briefs or an earlier lane's premise, say so in the file header — the elimination must override the stale assumption, not average it.

**Interpretation** — produced by the subagent, not the user: a reading of an ambiguous constraint that the survivor set depends on (does the hard rule apply to one side of the boundary or host-wide?). It is NOT an input until the user ratifies it. It goes to `PENDING.md` as an `I#` entry and is surfaced in the next Ask (see Procedure step 5).

Durable artifacts in the topic directory are the state:
- **`CONSTRAINTS.md`** — the user's constraints (abstract for/against + product vetoes). Append-only.
- **`DECISIONS.md`** — the user's decisions (concrete, for). Append-only. The loop ALWAYS ends with an entry here (the user's explicit pick, or the user's confirmation of the sole survivor).
- **`INVENTORY.md`** — the complete option set of the corpus, written once in round 1, append-only afterwards. The frozen ground set that STATE.md partitions.
- **`PENDING.md`** — soft preferences (S#) and unratified interpretations (I#). Append-only; status fields are updated in place.
- **`STATE.md`** — the subagent's per-round analysis: surviving paths, eliminated paths (each with the exact constraint/veto/decision that killed it), open axes, recommended next move. Rewritten every round.

Loop state must always be reconstructable from these files plus the corpus — never from chat memory.

## When to Use

- You have a handful to a dozen `deep-research` reports on the same topic and now must **choose** which concrete implementation to build.
- The design space is large (tens to hundreds of paths / decisions) and the user wants to shrink it by fixing constraints rather than enumerate-and-compare by hand.
- Decisions are coupled (one choice forces or forbids others), so an input added in round N changes what is open in round N+1.

**Don't use for:**
- No research corpus yet — run `deep-research` first; this skill can only narrow options the corpus already contains.
- A single obvious choice — just pick it.
- Feature design Q&A without a corpus — `feature-spec-qa`.
- Trying candidate fixes hands-on on a live system — that is `system-engineering-orchestration` (this skill decides on paper; it does not run the implementation).

## Question shape (every user question in this skill)

One question per turn: 2–3 numbered, self-contained options, one marked recommended with a one-to-two-sentence justification, ordered by dependency (architecture/visibility first). The user answers with a bare number or word. **When asking via `clarify`, the free-text row is ALWAYS present and binding** (user rule 2026-10-18): a typed variant is filed exactly as typed — run the definition table on it — never mapped onto the nearest option. A load-bearing technical term (e.g. 'EL kernel', 'nested KVM', 'COW snapshot') is defined in one line on first use inside the question; an undefined term forces a clarification round-trip that stalls the loop. When the user's answer also asks a confirmation question, answer it clearly FIRST (1–3 lines), then "Notiert: <one line>", then the next question.

## Preconditions (Step 0)

- **Locate the corpus.** `search_files` / `terminal` ls for the existing `deep-research` reports on this topic (project research dir, session scratch, or wiki). List the files to the user and **confirm they are all the same topic** before starting — the subagent can only work with what is listed.
  - When the user names the corpus by a vague time/recency window ("today", "recent", "all the research I kicked off"), do not take the word literally — verify the actual mtime range (`find -newermt`) and widen per the user. Multi-session research commonly spans an evening into the next day; a literal "today" silently drops half the corpus.
- **Fix the topic directory — always.** Create `.hermes/decision/<topic>/` (short kebab-case topic name, decided with the user in Step 0) and put all artifact files **there, from the first write** — never in the repo root. If a topic directory already exists for a *different* topic, create a new one; two topics never share a directory.
- **Persist the corpus before round 1.** If the corpus lives in session scratch (24 h pruning) or outside the repo, `git mv`/copy it into `.hermes/decision/<topic>/research/` and `git add` it **before** the first dispatch. The corpus README/manifest goes with it.
- **Collect the seed constraints.** Take the user's initial few statements and classify EACH one against the table: abstract for/against or veto → `CONSTRAINTS.md`; concrete for ("wir benutzen X") → first `DECISIONS.md` entry, tell the user the reclassification; soft → `PENDING.md` S#; environment fact → corpus env file.

## Artifact formats

All artifacts live in `.hermes/decision/<topic>/`; the research corpus lives in `<topic>/research/` with its manifest (`research/README.md` — file → axis/sub-question → C#/D# mapping). The manifest's C#/D# column is completed at Close (step 8), not during the loop.

`CONSTRAINTS.md` — append-only, one section per constraint:
```markdown
# CONSTRAINTS
Abstract for/against constructs + product vetoes. Append-only: to change a
constraint add a new one that supersedes it (mark the old one: SUPERSEDED by C#).
A for-statement naming a specific product is NOT a constraint — it is a
DECISION and belongs in DECISIONS.md.

## C1 — <short label>
- Constraint: <exact, testable statement — abstract, for or against>
- Rationale: <requirement / user statement / research finding>
- Source: <user / research file # / test / ratified I#> — <date>
- Eliminates: <which paths this rules out>
```

`DECISIONS.md` — append-only, one section per decision:
```markdown
# DECISIONS
Concrete, for-only technology picks. Append-only. The loop ends when the
last decision leaves exactly one path (or confirms the sole survivor).

## D1 — <short label>
- Decision: <the concrete technology chosen, named>
- Rationale: <why this one / which open axis it resolves>
- Source: <user / user-confirmed sole survivor> — <date>
- Eliminates: <surviving paths / candidates excluded by this pick>
- Re-validation: <one line per existing constraint/veto/decision — satisfied / not touched / conflict>
- Open/unverified: <implementation-phase items this decision defers (live checks, version pins, on-target tests)>
```

`INVENTORY.md` — written by the round-1 subagent BEFORE eliminating, append-only afterwards:
```markdown
# INVENTORY — corpus option set (frozen after round 1; scope expansions append)
One row per option the corpus names — from REPORT.md's matrix AND from every
lane file (lane-only options count: they were researched, not just mentioned).

| O# | option (concrete path) | corpus file(s) | tier | round-1 fate |
|---|---|---|---|---|
| O1 | ... | ... | Verified | P1 |
| O2 | ... | ... | Plausible | eliminated by C2 |
| O3 | ... | ... | Speculative | out of scope: <one-line reason> — confirmed by user round 1 |
```
Rules: every O# appears in round-1 STATE.md as a P# or under Eliminated; "out of scope" needs a reason and the orchestrator confirms it with the user in the round-1 Ask (otherwise it is a silent elimination). Nothing is renumbered or removed; a scope expansion appends rows.

`PENDING.md` — items that shape the loop but are NOT inputs yet:
```markdown
# PENDING — soft preferences (S#, orchestrator writes) and interpretations (I#, subagent appends)

## S1 — <soft preference label>
- Statement: <the user's indicative phrasing, verbatim>
- Affects axis: A#
- Status: OPEN | PROMOTED to C#/D# (round N) | DROPPED (user, round N)

## I1 — <interpretation label>
- Constraint interpreted: C#
- Reading: <the reading the subagent applied>
- Alternative reading: <what it did not apply>
- Load-bearing for: <P# that survive only under this reading>
- Status: OPEN | RATIFIED (round N → recorded as C# clarification) | REJECTED (round N → round re-run)
```
Rules: the subagent READS it every round and may APPEND I# entries; it never edits or drops one. S# entries are written by the orchestrator only. Status fields are the only in-place edits.

`STATE.md` — rewritten each round, headed by round number:
```markdown
# STATE — round N (<date>)
Inputs: CONSTRAINTS.md (C1..Ck); DECISIONS.md (D1..Dm); PENDING.md (S1..Sn, I1..Im); INVENTORY.md (O1..Oj); corpus: <files>; prior: round N-1.
Inventory check: j options — K surviving, j-K eliminated — all accounted: Y/N
Stale corpus lines reconciled: <file:line — why stale, which file wins> (or: none)

## Surviving paths (ranked)
### P1 — <concrete implementation / technology>   (O#)
- What: one line
- Survives because: satisfies C1..Ck, not vetoed, not excluded by a decision (name them)
- Depends on interpretation: I# (or none)
- Still leaves open: <axis ids>
- Effort / risk / tradeoffs
- Confidence: carries the corpus tier (Verified/Plausible/Speculative) per load-bearing part
- Recommendation: <prefer? why; S# considered>

## Eliminated paths
- <path> (O#) — out by C# (<abstract reason>) / veto C# / decision D# (<technology>)

## Open axes
- A1 (ABSTRACT): <pattern / principle axis> — <options> → resolvable by a CONSTRAINT
- A2 (CONCRETE): <technology axis> — <candidates> → resolvable by a DECISION

## Highest-leverage next move
- RATIFY I#: <reading> — load-bearing for P#   (takes precedence over a new constraint)
- or CONSTRAINT proposed (id PC-N, not yet a C#): <abstract for/against statement> — resolves A#, K -> K'
- or DECIDE NOW — A2 is trivial: <candidates>, one-line why this is not an architectural fork
- (Suggestion only: it counts only once the user accepts it.)

## Termination
- Surviving paths: K
- ONE_PATH: Y/N   TRIVIAL_CHOICE: Y/N + one-line why
- Open load-bearing I#: <list or none>
```

## Roles (strict)

**Orchestrator (this session):** owns `CONSTRAINTS.md`, `DECISIONS.md`, `PENDING.md` S# entries and all status fields, the round counter, the termination check, the definition check on every incoming statement, and all user communication. Never does the elimination itself. May read the subagent's compact return and, only when a decision needs it, one specific section of `STATE.md`.

**Decision subagent (`delegate_task`):** reads the full corpus + `CONSTRAINTS.md` + `DECISIONS.md` + `PENDING.md` + `INVENTORY.md` (+ prior `STATE.md`), does the elimination, writes `STATE.md` (round 1: `INVENTORY.md` first), appends I# entries, returns the compact index. It builds on the corpus's existing option matrix — it does **not** invent new paths, re-research, or fall decisions.

## Output contract (in every subagent goal)

Write `STATE.md` fully to disk. Return **only** (under ~1000 chars):
1. `ROUND:` N
2. `INVENTORY:` j options, all accounted Y/N (round 1: also the out-of-scope O# list)
3. `SURVIVORS:` K — one line each: `P#: <name> — open: A# — depends on: I#/none`
4. `ELIMINATED_THIS_ROUND:` <path> — by C# / veto C# / D# (one line each)
5. `NEW_PENDING:` I# appended this round (one line each) or none
6. `NEXT_MOVE:` `RATIFY: I#` / `CONSTRAINT PC-N: <statement> (resolves A#)` / `DECIDE_NOW: A# trivial (<candidates>)`
7. `TERMINATION:` ONE_PATH / TRIVIAL_CHOICE / CONTINUE
8. `FILE:` absolute path to `STATE.md`

## Procedure

1. **Seed.** Write the initial `CONSTRAINTS.md` (Step 0's seed statements, classified), an empty `DECISIONS.md`, and `PENDING.md` with any seed S#. When the user explicitly asks to be asked iteratively and the highest-leverage question is already obvious from the seed input, ask it BEFORE the first dispatch and dispatch round 1 with the complete seed. Completion: every seed statement is filed per the definition table; reclassifications told to the user.
2. **Dispatch.** `delegate_task` one decision subagent. Goal = corpus file paths + artifact file paths + prior `STATE.md` path (rounds >1) + the output contract + these instructions verbatim:
   - "Round 1: write INVENTORY.md first — one row per option named anywhere in the corpus (REPORT.md and every lane file); every O# must end as a P# or an Eliminated entry or an out-of-scope row with a reason."
   - "Build on the corpus option matrix; eliminate by constraints/vetoes/decisions; do not re-research; do not fall decisions; be explicit about which input kills which path."
   - "Reconcile every corpus file against the most researched one: a WIP draft or stale line that contradicts a researched file AND a constraint is marked STALE in STATE.md, not kept as a survivor."
   - "Read PENDING.md. Consider OPEN S# in the recommendation. When a survivor depends on a reading of an ambiguous constraint, append an I# entry and name it in the survivor's 'Depends on interpretation'. Never edit or drop existing entries."
   - "Make the inventory sum close (surviving + eliminated = total) before returning."
   Describe the STATE.md fields in prose or quoted labels — literal `<…>` placeholders in the goal get the dispatch rejected by the validator. Completion: a `STATE.md` for round N exists on disk (round 1: plus `INVENTORY.md`).
3. **Integrate.** Read the compact return. Append one line to the round ledger: `round N -> K survivors -> next: <move>`. Transfer `NEW_PENDING` I# into your view of open items. Do not open the full `STATE.md` unless a decision needs a detail (then pull that section only).
4. **Terminate check.**
   - Any OPEN load-bearing I# → not terminal regardless of K; go to step 5 and ratify first.
   - `ONE_PATH` → before accepting: (a) verify the sole survivor against **every** constraint, veto, and decision (full re-validation, not just the last round); (b) verify every O# in `INVENTORY.md` is that survivor or in Eliminated; (c) if the survivor leans on a Speculative corpus tier, flag it as untested-on-target in the proposal. Then propose the DECISION for that path's technology — the user confirms, the entry is recorded in `DECISIONS.md`, finish.
   - `TRIVIAL_CHOICE` → present the concrete fork (candidates, what differs, why it is not an architectural fork). The user falls a DECISION, recorded in `DECISIONS.md`, finish.
   - `CONTINUE` → step 5.
   - If an open sub-decision can only be resolved by a **live test the corpus itself defers** (an interaction or discovery mechanism marked unverified), do NOT force it into the paper loop: park it as a named verification-phase item, carry it into the final "untested on-target" list, and converge on the paper-decidable axes.
5. **Ask** (Question shape above). Order of precedence within the turn:
   1. Round 1: confirm the out-of-scope O# list from INVENTORY.md (one question; a rejected out-of-scope row becomes a survivor in round 2).
   2. Every OPEN load-bearing I#: one ratification question each — reading A vs reading B, recommendation, free text. Ratifying an interpretation is the higher-leverage move; it comes before any new constraint. Flag it as an *interpretation, not a verification*.
   3. Then, compact: the K survivors (one line each), the open axes (ABSTRACT/CONCRETE), the `NEXT_MOVE` suggestion — ask for one new CONSTRAINT, or invite a DECISION if a concrete axis is trivial.
6. **Append.** Run the definition table on every answer (including free text). New constraints → `CONSTRAINTS.md` (concrete-for → reclassify to `DECISIONS.md` and say so). New decisions → `DECISIONS.md` (conflict check first: violates a constraint/veto → stop, let the user resolve — supersede or veto, do not file). Ratified I# → new `C#` entry "clarifies C#, source: ratified I#", I# status RATIFIED; rejected I# → status REJECTED, the round is re-dispatched with the rejected reading excluded. Soft answers → `PENDING.md` S#. A proposed-but-not-accepted next-move constraint keeps its `PC-N` id and never consumes a `C#` number. Surface conflicts explicitly; never silently overwrite.
7. **Loop.** Back to step 2 (round N+1). A mid-loop DECISION is not automatically terminal — it excludes competing technologies, but more than one path may still survive inside the chosen one; re-run. Before re-dispatching, re-annotate the current `STATE.md` for the new decision: move every path it excludes into Eliminated ("out by D#"), update the Termination count and inventory check, append one Round Ledger line, and note in the header that D# was applied retroactively — otherwise the next subagent re-derives from the stale file and resurrects killed paths.
   - **No round budget.** The loop runs until ONE_PATH or TRIVIAL_CHOICE. If a round produces no change in K and no new input is forthcoming (the remaining axis is a genuine preference), say so and ask the user to decide — never auto-pick, never stop silently.
8. **Close — formal stage-3 handoff.** The topic is handed to `decision-topic-execution` in a state a cold session can enter without chat. In order, committed per the repo's small-commit convention:
   1. **Freeze the state:** rename `STATE.md` → `STATE-final.md`. Never rewritten afterwards; implementation progress belongs in `REVISIONS.md` and the plan.
   2. **Seed the revision log:** `REVISIONS.md` with a header (append-only; stage-3 plan changes and decision revisions, one line each) and one line: "loop closed round N → path X".
   3. **Write the topic `README.md`** (< one screen): terminating decision set (ids, one line each), deferred live items and where they are tracked (the plan), OPEN S# as "preferences not promoted", the precedence stack in exact order (repo ground rules → CONSTRAINTS → DECISIONS → plan), and a **Provenance** block naming the pipeline skills with versions and dates (`deep-research` <version> <dates> → `decision-narrowing` <version> rounds 1–N → `decision-topic-execution` <version> from <date>).
   4. **Complete the research manifest** via a decision subagent (goal = manifest + CONSTRAINTS + DECISIONS + INVENTORY paths; output contract "return the completed table, <1000 chars"). Two directions, both mandatory: (a) per corpus file, which C#/D# its claims fed (or "none — context only"); (b) **per D#, at least one corpus file that carried it** — a D# with no source file is a finding to surface, not to paper over. The orchestrator applies the table and checks direction (b) for every D# (mechanical), plus three spot-checks in direction (a).
   5. **State the hand-off:** the chosen path, the constraint + decision set that produced it, what remains untested on-target, and the pointer to `decision-topic-execution` (the rules every implementation session reads); offer `plan` for the implementation plan — invoke it with the explicit target path `<topic>/plans/YYYY-MM-DD-<slug>.md` (`plan` writes to `.hermes/plans/` unless given a path; a plan outside the topic directory is invisible to stage 3).
   Completion: README, CONSTRAINTS, DECISIONS, INVENTORY, PENDING, STATE-final, REVISIONS + `research/` manifest exist in the topic directory, are git-tracked, and a session reading only the directory can state what was decided, what is open, and how it was derived.

## After close: execution contract (stage 3)

Implementation under the closed topic runs under `decision-topic-execution` (reading levels, precedence stack, formal revision, kanban-campaign rules). Load that skill — not this one — in every implementation, wave-planning, or cleanup session; this skill's only remaining job after Close is "Extending an existing topic's decision log" below.

## Extending an existing topic's decision log

A topic directory may already hold a closed or in-progress loop. Adding a new sub-axis (a new feature/concern, e.g. a 'QEMU VMs' axis to an established infra topic) that needs its own decisions is NOT a new topic — do not create a second directory or renumber. Instead:
- Append new constraints as C(k+1)… and new decisions as D(m+1)… to the existing files; keep all ids stable and sequential. New options append to `INVENTORY.md` as O(j+1)….
- Run the definition check and the **re-validation against the FULL existing set** (every C1..Ck and D1..Dm) — a new decision can silently violate a constraint from a prior sub-axis. The `Re-validation` field in each new D# makes this auditable.
- New sub-axis research files go under the same `research/` (a new subdirectory is fine); add manifest rows. Env facts go in a new `env-<host>-<date>.md`.

## Expanding the scope mid-loop

The user can **widen** the problem mid-loop by adding an input that brings in a dimension the current corpus does not cover (a new plane, layer, or concern of the same architecture). Widening is legitimate; handle it, don't refuse it.

- **File the input first, then run a scope-expansion round (N+1).** Definition check, append, then re-dispatch with the **widened corpus** — the new axis's research files included — and instruct the subagent to (a) append the new options to `INVENTORY.md`, (b) carry every existing axis's survivor state forward **unchanged**, (c) enumerate the new axis as its own survivor set, (d) re-validate the whole against the full input set.
- **Model independent planes as separate axes, not one flat P# list.** Do NOT enumerate the full Cartesian product — it explodes. Give each axis its own survivor set with its own id prefix (P# gateway, G# gitops, B# build-server…) and report the composite count as the **product** (e.g. 2×1×3 = 6). Group `STATE.md`'s "Surviving paths" by axis. Have the subagent check whether the axes are truly independent or **coupled** and note couplings explicitly — a coupling changes the product.
- **Termination = every axis at one survivor.** ONE_PATH for a multi-axis problem means **1×1×…×1**. Confirm each axis is independently at 1 before declaring termination.
- **Keep ids stable across the expansion.** New axes take the next free ids (A5, A6…); never renumber.

## Pitfalls

- **A decision dressed as a constraint.** "Wir benutzen die Kxs Gateway" in `CONSTRAINTS.md` is wrong: for + concrete = DECISION. Mirror: "keine VPN zwischen Hosts" in `DECISIONS.md` is wrong: against + abstract = CONSTRAINT. Run the definition table on every incoming statement, including the seed and free-text answers.
- **The subagent falling decisions.** It recommends; the user decides. A `DECISIONS.md` entry without an explicit user move (or user-confirmed sole survivor) is a process violation.
- **An interpretation treated as settled.** A reading that carries the survivor set and sits OPEN in `PENDING.md` is a live fork, not a given — it is ratified by the user before any new constraint is requested, and never terminal while OPEN.
- **Silent elimination via inventory.** An option that never made it into `INVENTORY.md` is never eliminated and never noticed. Round 1 inventories lane files too, not only REPORT.md; out-of-scope rows are confirmed by the user.
- **Counting a suggested move as accepted.** `NEXT_MOVE` only enters the files when the user says so. Proposals carry `PC-N` ids, never a `C#`.
- **Treating a mid-loop decision as terminal.** It shrinks the space but may leave several surviving paths inside the chosen technology. Re-run; only ONE_PATH or TRIVIAL_CHOICE ends the loop.
- **Forcing ONE_PATH when TRIVIAL_CHOICE is real.** The second exit is a feature. A remaining config-value / naming / equivalent-vendor fork is decided, not looped.
- **Editing old entries.** All append-only files: a changed constraint or retracted decision is a new entry that supersedes (mark the old: SUPERSEDED by C#/D#); otherwise the elimination history is unauditable.
- **No corpus, or mixed-topic corpus.** The subagent can only narrow what is listed. Confirm the corpus is complete and single-topic in Step 0.
- **Subagent re-researching / inventing paths.** "Options" not in the corpus are hallucinated space. If the corpus is genuinely missing a path, say so and run `deep-research` for that gap.
- **Orchestrator drift.** If this session is drafting the elimination logic or reading big corpus files, hand it back to a subagent. The orchestrator owns the input sets + loop state, not the analysis.
- **Artifact-scheme upgrade mid-loop.** If the skill is re-sharpened while a loop has live files (new artifact such as INVENTORY/PENDING, refined rule), migrate in place before the next round: reclassify via SUPERSEDED cross-references (never delete), create missing artifacts from the current STATE.md, keep C#/D#/A#/O# ids stable. Tell the user what moved where and why.
- **Corpus not persisted before round 1.** A corpus in session scratch is pruned after 24 h; every elimination becomes unverifiable and the stage-3 revision path is dead. Persist and git-add in Step 0.
- **Closing in the repo root / leaving the hand-off to chance.** The topic directory is the unit of continuity: if anything the stage-3 agent needs is outside it, the close is incomplete.

## Verification

- Every entry in `CONSTRAINTS.md` is an abstract for/against statement or a product veto; every entry in `DECISIONS.md` is a concrete for with a named technology.
- `CONSTRAINTS.md`, `DECISIONS.md`, `INVENTORY.md`, `PENDING.md` are append-only; every entry has a rationale + source.
- `INVENTORY.md` covers every option named in REPORT.md and every lane file; the final STATE partitions it completely (survivor + eliminated = total).
- No OPEN load-bearing I# at termination; every RATIFIED I# has a corresponding C# clarification entry.
- The final `STATE-final.md` lists exactly one survivor (per axis), or marks the remainder `TRIVIAL_CHOICE` with a one-line why.
- The final survivor is re-validated against **every** input.
- The loop ended with a `DECISIONS.md` entry — the user's explicit pick or the user-confirmed sole survivor — not just in chat.
- State reconstructable: corpus + the artifact files fully determine the decision with no chat context.
- Topic directory complete and git-tracked: README, CONSTRAINTS, DECISIONS, INVENTORY, PENDING, STATE-final, REVISIONS, plans/, research/ (manifest C#/D# column filled in both directions).
- Provenance block names all three pipeline skills with versions and dates.

## Relationship to neighbors

- **Upstream:** `deep-research` produces the options-complete corpus this skill narrows.
- **Sibling:** `feature-spec-qa` — same question shape, no corpus, no loop; decisions file + kanban handoff.
- **Same pattern:** `system-engineering-orchestration` (orchestrator + hands-on subagents) — but that skill *tries* fixes on a live system; this one *decides* on paper from a corpus.
- **Downstream:** on ONE_PATH / TRIVIAL_CHOICE, the decision is recorded and the Close step hands the topic to `decision-topic-execution`; `plan` supplies the implementation plan; `hermes-kanban-workers` delivers the code work.
