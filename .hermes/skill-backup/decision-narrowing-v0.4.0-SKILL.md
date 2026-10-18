---
name: decision-narrowing
description: "Constraint-driven loop to pick one implementation path."
version: 0.4.0
author: Peter Fahsel, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [decision-making, constraints, design-space, orchestration, delegate_task, subagent, planning, convergence]
    related_skills: [deep-research, decision-execution, plan, system-engineering-orchestration]
---

# Decision Narrowing Skill

Turn an options-complete research corpus (from `deep-research`) into **one chosen implementation** by iteratively narrowing the design space. The user fixes **CONSTRAINTS** (for or against, at the abstract level) and — once a fork has become small enough — falls **DECISIONS** (for, on a concrete technology). Between user moves, a subagent enumerates the surviving paths, the open axes, and the highest-leverage next move. The loop repeats until exactly one path remains or the remaining choice is trivial. It is the *decision* phase after the *research* phase: `deep-research` maps every feasible path, this skill drives them to a single pick. This skill is stage 2 of the decision pipeline: `deep-research` (stage 1) produces the options-complete corpus, this skill narrows it to one path, and `decision-execution` (stage 3) carries the result into implementation under the same artifact discipline. The three stages share one directory: `.hermes/decision/<topic>/`.

## The core distinction: CONSTRAINT vs DECISION

Two levels, two file types, two kinds of user input. Confusing them is the main failure mode of this skill — check every incoming statement against the table before filing it.

**CONSTRAINT** — a for-or-against statement about an *abstract construct* (a pattern, a principle, an architectural boundary). It carves the design space: eliminates whole regions of paths at once, without committing to any product.
- For: "Wir stellen nur VPN-Verbindungen zwischen Containern her."
- Against: "Wir stellen keine VPN-Verbindungen zwischen Hosts her."
- A statement may combine both: "Keine VPN-Verbindung zwischen Hosts, sondern nur zwischen Containern."
- A concrete product name is allowed **only in the against-direction** (a veto: "kein Produkt X"). A for-statement that names a product is NOT a constraint — it is a DECISION.

**DECISION** — a *for-only* statement about a *specific technology* (a named product, a concrete implementation).
- For: "Wir benutzen die Kxs Gateway Technologie."
- A decision is never "against" — against lives in constraints (abstract) or eliminations (derived).
- Only the user falls decisions. The subagent may *recommend*; it never *falls*.

| | Level | Direction | Names a product? | File |
|---|---|---|---|---|
| CONSTRAINT | abstract construct | for or against | only as veto (against) | `CONSTRAINTS.md` |
| DECISION | concrete technology | for only | yes — that is the point | `DECISIONS.md` |

Interaction: constraints eliminate broad regions; a decision fixes one concrete technology and thereby eliminates every surviving path that does not use it. A decision is valid only against the current constraint set — if it violates a constraint or a veto, stop and surface the conflict (supersede or veto) instead of filing it.

**Soft / indicative statement** — a third input type, distinct from both: the user sketches a preference without committing ("kein harter Constraint, aber so ungefähr", "ich würde ungefähr X machen"). It is **neither** a CONSTRAINT **nor** a DECISION — do not file it as one (that would over-commit and let a casual phrasing eliminate paths). Capture it in `STATE.md` as a *preference/indication* on the relevant open axis: it shapes the recommendation and how you phrase the question, but it eliminates nothing on its own. Promote it to a constraint or decision only if the user later states it as a firm requirement or an explicit pick.

**Environment fact** — a fourth input type: a statement about the current state of the world (hardware, OS, versions, what is already installed and working) that carves the design space but is neither for/against nor a product pick. It is **neither** a CONSTRAINT **nor** a DECISION — filing it as a constraint lets a fact rot into a rule that later mis-eliminates. Persist it as a dated environment-update file in the corpus (`research/<topic>/env-<host>-<date>.md`), add a manifest row, and cross-reference it from any constraint entry that relies on it; the subagent picks it up via the corpus it reads, and it enters the round's `Inputs:` line. When it supersedes an assumption baked into the lane briefs or an earlier lane's premise, say so in the file header — the elimination must override the stale assumption, not average it.

Three durable artifacts in the repo are the state:
- **`CONSTRAINTS.md`** — the user's constraints (abstract for/against + product vetoes). Append-only.
- **`DECISIONS.md`** — the user's decisions (concrete, for). Append-only. The loop ALWAYS ends with an entry here (the user's explicit pick, or the user's confirmation of the sole survivor).
- **`STATE.md`** — the subagent's per-round analysis: surviving paths, eliminated paths (each with the exact constraint/veto/decision that killed it), open axes, recommended next move. Rewritten every round.

Loop state must always be reconstructable from these three files plus the corpus — never from chat memory.

## When to Use

- You have a handful to a dozen `deep-research` reports on the same topic and now must **choose** which concrete implementation to build.
- The design space is large (tens to hundreds of paths / decisions) and the user wants to shrink it by fixing constraints rather than enumerate-and-compare by hand.
- Decisions are coupled (one choice forces or forbids others), so an input added in round N changes what is open in round N+1.

**Don't use for:**
- No research corpus yet — run `deep-research` first; this skill can only narrow options the corpus already contains.
- A single obvious choice — just pick it.
- Trying candidate fixes hands-on on a live system — that is `system-engineering-orchestration` (this skill decides on paper; it does not run the implementation).

## Preconditions (Step 0)

- **Locate the corpus.** `search_files` / `terminal` ls for the existing `deep-research` reports on this topic (project research dir, session scratch, or wiki). List the files to the user and **confirm they are all the same topic** before starting — the subagent can only work with what is listed.
  - When the user names the corpus by a vague time/recency window ("today", "recent", "all the research I kicked off"), do not take the word literally — verify the actual mtime range (`find -newermt`) and widen per the user. Multi-session research commonly spans an evening into the next day; a literal "today" silently drops half the corpus and leaves the survivor set incomplete.
- **Fix the topic directory — always.** Create `.hermes/decision/<topic>/` (short kebab-case topic name, decided with the user in Step 0) and put `CONSTRAINTS.md`, `DECISIONS.md`, and `STATE.md` **there, from the first write** — never in the repo root. If a topic directory already exists for a *different* topic, create a new one; two topics never share a directory.
- **Persist the corpus before round 1.** If the corpus lives in session scratch (24 h pruning) or outside the repo, `git mv`/copy it into `.hermes/decision/<topic>/research/` and `git add` it **before** the first dispatch — a loop whose corpus is pruned mid-run or after the session ends cannot be reconstructed, and the stage-3 agent that must re-open a decision's sources will find nothing. The corpus README/manifest goes with it.
- **Collect the seed constraints.** Take the user's initial few statements and classify EACH one against the table: abstract for/against or veto → `CONSTRAINTS.md`; concrete for ("wir benutzen X") → file as the first `DECISIONS.md` entry and tell the user the reclassification. Statements that are environment facts (hardware/OS/current state) go to the corpus environment-update file instead — see the fourth input type above.

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
- Source: <user / research file # / test> — <date>
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
- Re-validation: <one line per existing constraint/veto/decision — satisfied / not touched / conflict. Catches a pick that silently violates an earlier input.>
- Open/unverified: <implementation-phase items this decision defers (live checks, version pins, on-target tests).>
```

`STATE.md` — rewritten each round, headed by round number:
```markdown
# STATE — round N (<date>)
Inputs: CONSTRAINTS.md (C1..Ck); DECISIONS.md (D1..Dm); corpus: <files>; prior: round N-1.

## Surviving paths (ranked)
### P1 — <concrete implementation / technology>
- What: one line
- Survives because: satisfies C1..Ck, not vetoed, not excluded by a decision (name them)
- Still leaves open: <axis ids>
- Effort / risk / tradeoffs
- Confidence: carries the corpus tier (Verified/Plausible/Speculative) per load-bearing part
- Recommendation: <prefer? why>

## Eliminated paths
- <path> — out by C# (<abstract reason>) / veto C# / decision D# (<technology>)

## Open axes
- A1 (ABSTRACT): <pattern / principle axis> — <options> → resolvable by a CONSTRAINT
- A2 (CONCRETE): <technology axis> — <candidates> → resolvable by a DECISION

## Highest-leverage next move
- CONSTRAINT proposed: <abstract for/against statement> — resolves A#, K -> K'
- or: DECIDE NOW — A2 is trivial: <candidates>, one-line why this is not an architectural fork
- (Suggestion only: it counts only once the user accepts it.)

## Termination
- Surviving paths: K
- ONE_PATH: Y/N   TRIVIAL_CHOICE: Y/N + one-line why
```

## Roles (strict)

**Orchestrator (this session):** owns `CONSTRAINTS.md`, `DECISIONS.md`, `STATE.md`, the round counter, the termination check, the definition check on every incoming statement, and all user communication. Never does the elimination itself. May read the subagent's compact return and, only when a decision needs it, one specific section of `STATE.md`.

**Decision subagent (`delegate_task`):** reads the full corpus + `CONSTRAINTS.md` + `DECISIONS.md` (+ prior `STATE.md`), does the elimination, writes `STATE.md`, returns the compact index. It builds on the corpus's existing option matrix — it does **not** invent new paths, re-research, or fall decisions.

## Output contract (in every subagent goal)

Write `STATE.md` fully to disk. Return **only** (under ~1000 chars):
1. `ROUND:` N
2. `SURVIVORS:` K — one line each: `P#: <name> — open: A#`
3. `ELIMINATED_THIS_ROUND:` <path> — by C# / veto C# / D# (one line each)
4. `NEXT_MOVE:` `CONSTRAINT: <statement> (resolves A#)` or `DECIDE_NOW: A# trivial (<candidates>)`
5. `TERMINATION:` ONE_PATH / TRIVIAL_CHOICE / CONTINUE
6. `FILE:` absolute path to `STATE.md`

## Procedure

1. **Seed.** Write the initial `CONSTRAINTS.md` (Step 0's seed constraints, classified) and an empty `DECISIONS.md`. Completion: every seed statement is filed according to the definition table; any reclassified concrete-for is noted to the user.
2. **Dispatch.** `delegate_task` one decision subagent. Goal = corpus file paths + `CONSTRAINTS.md` path + `DECISIONS.md` path + prior `STATE.md` path (rounds >1) + the output contract + "build on the corpus option matrix; eliminate by constraints/vetoes/decisions; do not re-research; do not fall decisions; be explicit about which input kills which path." Completion: a `STATE.md` for round N exists on disk.
3. **Integrate.** Read the compact return. Append one line to the round ledger: `round N -> K survivors -> next: <move>`. Do not open the full `STATE.md` unless a decision needs a detail (then pull that section only).
4. **Terminate check.**
   - `ONE_PATH` → before accepting, verify the sole survivor against **every** constraint, veto, and decision (full re-validation, not just the last round) and that every corpus option is either that survivor or in "eliminated." Then propose the DECISION for that path's technology — the user confirms, the entry is recorded in `DECISIONS.md`, finish.
   - `TRIVIAL_CHOICE` → present the concrete fork (candidates, what differs, why it is not an architectural fork). The user falls a DECISION, it is recorded in `DECISIONS.md`, finish.
   - `CONTINUE` → step 5.
   - If an open sub-decision can only be resolved by a **live test the corpus itself defers to its verification plan** (e.g. an interaction or a discovery mechanism the corpus marks unverified), do NOT force it into the paper loop: park it as a named verification-phase item, carry it into the final "untested on-target" list, and converge on the paper-decidable axes. A live-test question is an implementation artifact, not a design fork.
5. **Ask.** Show the user, compact: the K survivors (one line each), the open axes (each labeled ABSTRACT or CONCRETE), and the `NEXT_MOVE` suggestion. Ask for one or more new CONSTRAINTS — and, if a concrete axis is flagged trivial, invite a DECISION. **One question per turn**: 2–3 numbered options, one marked recommended with a one-to-two-sentence justification, ordered by dependency (architecture/visibility first) — the user answers with a bare number or word, so options must be self-contained. When the user explicitly asks to be asked iteratively and the highest-leverage question is already obvious from the seed input, ask it BEFORE the first subagent dispatch and dispatch round 1 with the complete seed — do not burn a loop round to have the subagent propose a question you already knew to ask.
6. **Append.** New constraints → `CONSTRAINTS.md` (definition check first: concrete-for → reclassify to `DECISIONS.md` and say so). New decisions → `DECISIONS.md` (conflict check first: violates a constraint/veto → stop, let the user resolve — supersede or veto, do not file). Surface conflicts explicitly; never silently overwrite.
7. **Loop.** Back to step 2 (round N+1). A mid-loop DECISION is not automatically terminal — it excludes competing technologies, but more than one path may still survive inside the chosen one; re-run the loop. Before re-dispatching, re-annotate the current `STATE.md` for the new decision: move every path it excludes into Eliminated ("out by D# (<technology>)"), update the Termination count, append one Round Ledger line, and note in the header that D# was applied retroactively — otherwise the next subagent re-derives from the stale file and resurrects already-killed paths.
   - **Loop budget: 6 rounds.** If not converged by then, stop, present the full state (constraints, decisions, survivors, and why it will not shrink further — usually the remaining axis is a genuine preference), and let the user make the call. Never auto-pick.
8. **Close — formal stage-3 handoff.** The loop is done; the topic is handed to `decision-execution` in a state a cold session can enter without chat. Do, in order, and commit per the repo's small-commit convention:
   1. **Freeze the state:** rename `STATE.md` → `STATE-final.md`. It is never rewritten after this; implementation progress belongs in `REVISIONS.md` and the plan, not here.
   2. **Seed the revision log:** create `REVISIONS.md` with a header (append-only; stage-3 plan changes and decision revisions land here, one line each) and one line: "loop closed round N → path X".
   3. **Write the topic `README.md`** (< one screen): terminating decision set (ids, one line each), deferred live items (the loop's untested/on-target list) and where they are tracked (the plan), the precedence stack in exact order (repo ground rules → CONSTRAINTS → DECISIONS → plan), and a **Provenance** block naming all three pipeline skills with versions and dates (`deep-research` <version> <dates> → `decision-narrowing` <version> rounds 1–N → `decision-execution` <version> from <date>).
   4. **Complete the research manifest:** in `research/README.md`, fill the C#/D# column for every corpus file (which constraints/decisions each file's claims fed, including "none — context only"). This is elimination analysis, so per the Orchestrator-drift rule it goes to a decision subagent (`delegate_task` with goal = manifest path + `CONSTRAINTS.md` + `DECISIONS.md` paths + output contract "return the completed table, <1000 chars"); the orchestrator applies the returned table to `research/README.md` and spot-checks at least three rows against the C#/D# entries. The chain raw source → C#/D# → code must be traceable from the directory alone.
   5. **State the hand-off:** the chosen path, the constraint + decision set that produced it, what remains untested on-target, and — load `decision-execution` for the implementation phase (or hand its rules to the next session); offer `plan` for the implementation plan, which lives in `<topic>/plans/`.
   Completion: all five artifacts (README, CONSTRAINTS, DECISIONS, STATE-final, REVISIONS) + `research/` manifest exist in the topic directory, are git-tracked, and a session reading only the directory can state what was decided, what is open, and how it was derived.

## Lightweight variant: feature-spec Q&A

Use this variant when no multi-report corpus has to be narrowed. The typical case is a new project with research already done, where the user wants to settle the feature design "iteratively, question by question". In that case, skip the subagent loop and the three-file scheme:

1. **Read in first.** Read the repo, the research reports, and any UI screenshots of the reference product. Then give a short status (goal, what exists, build options, known gaps) and ask Q1 in the same reply.
2. **One question per turn.** Offer 2–3 numbered options, mark one as recommended, and justify the recommendation in one or two sentences. The user answers with a bare number or word, so the options must be self-contained. Order the questions by dependency: visibility/architecture first, then initiation, consent flow, completion/report-back, persistence, model/cost, cwd/context, edge cases (busy/closed target), UI, limits/recursion.
3. **Persist early.** Offer a decisions file in the repo after about 6 questions at the latest, then write it as `.hermes/decisions.md`: a table with D#, topic, decision, and a one-clause rationale, in English. After that, patch in each new answer *before* asking the next question, so that a session switch loses nothing.
4. **Merge user additions.** If an answer adds something the options did not cover (e.g. "also carry the Desktop project, repo and board"), merge it into that D# and do not open a new question for it. If the addition depends on a capability the research did not verify, add a parenthetical "Open: … verify docs-first in spec phase" to the D#. Mention that gap in one line when you confirm the answer, and do not answer it from memory.
5. **Carry cost and safety guards into the recommendations.** Typical guards: confirmation before more expensive models, explicit `provider:model`, depth and concurrency caps, and agent-initiated actions as a proposal card unless the user explicitly asked.

6. **Hand off to the board.** When the user asks to turn the decisions into work, first propose a card table: one row per card, with the D#s it covers and its parents. Put a spec card first that turns every "Open: verify" item into a docs-first question. Order the rest backend → UI → live e2e. Get confirmation, then commit and push the decisions file (worktrees see only committed files), then create the chain behind a gate card. The gated-batch recipe is in `hermes-kanban-ops`. Any questions still open go into a final "planning complete?" question before the user closes the gate.
7. **Late decisions after the cards exist.** Keep asking one question per turn and patch each D# into the decisions file as usual. Do not commit after every answer. When the question round ends, do one consolidated pass: patch every affected card body in the board DB (the recipe is in `hermes-kanban-ops`), then commit and push the decisions file. A worker sees only committed files and the card text it was created with, so a decision that is in neither never reaches it. Report which card gained which D#, as a table.
8. **Custom answers spawn follow-ups.** If the user answers with their own variant instead of a number (e.g. "also allow X" or "keep A but add prefix B"), file it, then ask the one or two sub-questions it opens before moving on. Example: a new state such as "detached" raises whether existing restrictions still apply and whether the state is reversible. Do not silently decide the dependent points.
9. **Close the gate only on the user's explicit "done".** Then release it (`unblock` if it is blocked, then `complete`), check `list` to see whether the dispatcher already started the first card, and offer a bounded background status poll on the first card, with notify on exit.

Each confirmation turn has a fixed shape: "Notiert: <one line>", then the next question. No recap of earlier answers. **When the user's answer also asks a confirmation question** (validating their understanding of the consequence of the pick), answer it clearly FIRST — confirm or correct their understanding in 1–3 lines — before the 'Notiert' line and the next question. The confirmation question often surfaces a load-bearing interpretation (e.g. OS-plane vs k8s-object-plane, runtime-state vs Git-declared) that needs explicit ratification; answering it is itself part of closing the axis, and a vague or wrong confirmation silently mis-files the next decision.

### Extending an existing topic's decision log

A topic directory may already hold a closed or in-progress loop (CONSTRAINTS.md C1..Ck, DECISIONS.md D1..Dm, possibly a frozen STATE-final.md). Adding a new sub-axis (a new feature/concern, e.g. a 'C19: QEMU VMs' axis to an established infra topic) that needs its own decisions is NOT a new topic — do not create a second directory or renumber. Instead:
- Append new constraints as C(k+1)… to the existing `CONSTRAINTS.md` and new decisions as D(m+1)… to the existing `DECISIONS.md`; keep all ids stable and sequential.
- Run the definition check and the **re-validation against the FULL existing set** (every C1..Ck and D1..Dm, not just the new sub-axis's inputs) — a new decision can silently violate a constraint from a prior sub-axis. The `Re-validation` field in each new D# is what makes this auditable.
- New sub-axis research files go under the same `research/` (a new subdirectory is fine); add manifest rows. The sub-axis's env facts go in a new `env-<host>-<date>.md`.

## Expanding the scope mid-loop

The loop is not only for narrowing — the user can **widen** the problem mid-loop by adding an input that brings in a dimension the current corpus does not cover (a new plane, layer, or concern of the same architecture). Widening is legitimate; handle it, don't refuse it.

- **File the input first, then run a scope-expansion round (N+1).** Run the normal definition check on the new statement (constraint / decision / soft-indication), append it, then re-dispatch the subagent with the **widened corpus** — now including the new axis's research files — and instruct it to (a) carry every existing axis's survivor state forward **unchanged**, (b) enumerate the new axis as its own survivor set, and (c) re-validate the whole against the full input set.
- **Model independent planes as separate axes, not one flat P# list.** When the problem spans several largely-independent planes (different deployment planes / layers), do NOT enumerate the full Cartesian product as individual P# paths — it explodes. Give each axis its own survivor set with its own id prefix (P# gateway, G# gitops, B# build-server…) and report the composite count as the **product** (e.g. 2×1×3 = 6). Group `STATE.md`'s "Surviving paths" section by axis in this case. Have the subagent check whether the axes are truly independent or **coupled** (one plane's pick forcing/forbidding another's) and note couplings explicitly — a coupling changes the product.
- **Termination = every axis at one survivor.** ONE_PATH for a multi-axis problem means **1×1×…×1**, not a single P# list of length 1. Confirm each axis is independently at 1 before declaring termination.
- **Keep ids stable across the expansion.** New axes take the next free axis ids (A5, A6…); never renumber existing ones.
- **Re-baseline the round budget.** A scope expansion is itself a round (N+1). The 6-round cap applies to the widened problem; if the problem genuinely grew, converging it may legitimately take a few more rounds — but still stop and present when it stops shrinking, per the cap rule.

## Pitfalls

- **A decision dressed as a constraint.** "Wir benutzen die Kxs Gateway" in `CONSTRAINTS.md` is wrong: for + concrete = DECISION → `DECISIONS.md`. And the mirror: "keine VPN zwischen Hosts" in `DECISIONS.md` is wrong: against + abstract = CONSTRAINT → `CONSTRAINTS.md`. Run the definition table on every incoming statement, including the seed. Edge case: a requirement that names a product as the MECHANISM ("soll per QEMU laufen", "k8s-basiert") is a constraint on the mechanism, not a pick among candidate implementations — file it as a constraint with an explicit note that the concrete implementation within that mechanism remains a DECISION to be fallen in the loop.
- **The subagent falling decisions.** It recommends; the user decides. A `DECISIONS.md` entry without an explicit user move (or user-confirmed sole survivor) is a process violation.
- **Undefined load-bearing jargon.** When a decision fork rests on a technical term the user may not be fluent in (e.g. 'EL kernel' = Enterprise-Linux kernel in the KubeVirt context, 'nested KVM', 'COW snapshot', 'IaR'), define it in one line on first use in the question — or flag it explicitly ('EL = Enterprise Linux; the risk is…'). An undefined load-bearing term forces a clarification round-trip that stalls the loop. The user is a domain expert but not necessarily fluent in every sub-domain's jargon; a term that carries decision weight must be self-contained in the question.
- **Unexpanded template markers in the subagent goal.** Pasting the `STATE.md` format template into the `delegate_task` goal verbatim — with its `<name>` / `<files>` angle-bracket placeholders — gets the whole dispatch rejected by the validator. In the goal text describe the required fields in prose or quoted labels ("a section 'Surviving paths' with one subsection per path"); literal angle brackets stay in the artifact template, not in the goal.
- **Artifact-scheme upgrade mid-loop.** If the skill is re-sharpened while the loop has live files (new/renamed artifact, refined CONSTRAINT-vs-DECISION rule), migrate in place before the next round: reclassify mis-filed entries via a SUPERSEDED cross-reference in the old file (append-only still applies — never silently delete), move subagent analysis into the subagent's own file, and keep the C#/D#/A# ids stable so cross-references stay valid. Tell the user what moved where and why.
- **Treating a mid-loop decision as terminal.** It shrinks the space but may leave several surviving paths inside the chosen technology. Re-run; only ONE_PATH or TRIVIAL_CHOICE ends the loop.
- **No corpus, or mixed-topic corpus.** The subagent can only narrow what is listed. Confirm the corpus is complete and single-topic in Step 0, or the survivor set is quietly incomplete (missing paths never get eliminated).
- **Subagent re-researching / inventing paths.** It narrows the corpus's option matrix; "options" not in the corpus are hallucinated space. If the corpus is genuinely missing a path, say so and run `deep-research` for that gap — do not let the subagent fill it.
- **Stale / contradicting files inside the corpus.** A multi-file research corpus often contains earlier WIP drafts that predate a later decision on the same topic (a draft host-role table, a stale "disable X" line) that flatly contradict the more researched files. The subagent must reconcile EVERY corpus file against the authoritative one during re-validation and mark stale lines explicitly (WIP/STALE) in `STATE.md` — otherwise a stale draft line resurrects an already-eliminated path. When a draft conflicts with a more specific/researched file AND a constraint, the researched file + constraint wins; the conflict is an inconsistency to annotate, not a new survivor to keep.
- **Convergence by ratifying an interpretation, not just adding input.** When an abstract constraint has a scoping ambiguity (does the hard rule apply only to one side of the boundary, or host-wide?) and that interpretation is what *carries* the survivor set, the load-bearing move is the user **ratifying the interpretation** — framed as the decision to close — not adding a brand-new constraint. Make the interpretation explicit in `STATE.md` and flag it as an *interpretation, not a verification*. Do not present it as settled; a load-bearing interpretation the user has not ratified is a live fork, not a given.
- **Forcing ONE_PATH when TRIVIAL_CHOICE is real.** The second exit is a feature. A remaining config-value / naming / equivalent-vendor fork is decided, not looped.
- **Editing old entries.** Both append-only files: a changed constraint or retracted decision is a new entry that supersedes (mark the old: SUPERSEDED by C#/D#); otherwise the elimination history is unauditable.
- **Counting a suggested move as accepted.** `NEXT_MOVE` only enters the files when the user says so. The subagent proposes; the user decides. **Id-collision variant:** if a round's *proposed-but-unaccepted* next-move constraint already consumed a `C#` number, and the user's next *real* constraint then reuses that number, the two collide. Disambiguate in the file (a short note that the earlier proposal was not accepted and is not what C# refers to) and give the pending proposal a fresh id — otherwise the next subagent conflate the accepted constraint with the stale proposal and mis-eliminate.
- **Last-round-only validation.** On `ONE_PATH`, re-check the survivor against the *entire* input set — an input added two rounds ago can be the one the survivor violates.
- **Speculative sole survivor.** If the only survivor leans on a Speculative corpus tier, flag it as untested-on-target before closing — do not let a guess become the decision.
- **Orchestrator drift.** If this session is drafting the elimination logic or reading big corpus files, hand it back to a subagent. The orchestrator owns the input sets + loop state, not the analysis.
- **Loop over-run.** Six rounds is the cap. Past it, the remaining axis is almost always a preference; present it and stop rather than burn rounds.
- **Corpus not persisted before round 1.** A corpus in session scratch is pruned after 24 h: the loop may finish, but every elimination becomes unverifiable and the stage-3 revision path ("re-open the source this decision was based on") is dead. Persist into `<topic>/research/` and git-add it before the first dispatch (Step 0), not at Close.
- **Closing in the repo root / leaving the hand-off to chance.** Artifacts left in the root (or one in the root, one in `.hermes/`) mean the next session re-derives the topic by archaeology. The topic directory is the unit of continuity: if anything the stage-3 agent needs is outside it, the close is incomplete.

## Verification

- Every entry in `CONSTRAINTS.md` is an abstract for/against statement or a product veto (against-direction); every entry in `DECISIONS.md` is a concrete for with a named technology.
- `CONSTRAINTS.md` and `DECISIONS.md` are append-only; every entry has a rationale + source.
- The final `STATE.md` lists exactly one survivor, or marks the remainder `TRIVIAL_CHOICE` with a one-line why.
- The final survivor is re-validated against **every** input, and every corpus option is accounted for (survivor or eliminated-with-reason).
- The loop ended with a `DECISIONS.md` entry — the user's explicit pick or the user-confirmed sole survivor — not just in chat.
- State reconstructable: corpus + the three files fully determine the decision with no chat context.
- Topic directory complete and git-tracked: README, CONSTRAINTS.md, DECISIONS.md, STATE-final.md, REVISIONS.md, plans/, research/ (with manifest C#/D# column filled).
- Provenance block names all three pipeline skills with versions and dates; the manifest lets a cold reader follow any D# to the corpus file(s) that fed it.

## Relationship to neighbors

- **Upstream:** `deep-research` produces the options-complete corpus this skill narrows.
- **Same pattern:** `system-engineering-orchestration` (orchestrator + hands-on subagents) — but that skill *tries* fixes on a live system; this one *decides* on paper from a corpus.
- **Downstream:** on ONE_PATH / TRIVIAL_CHOICE, the decision is recorded and the Close step hands the topic to `decision-execution` (implementation under the artifacts, with the precedence stack and the revision mechanism); `plan` supplies the implementation plan that `decision-execution` treats as the least-stable artifact.
