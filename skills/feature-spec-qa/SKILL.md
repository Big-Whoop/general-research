---
name: feature-spec-qa
description: "Use when asked for a feature plan (Planungsvorschlag). One question per turn, then cards."
version: 1.0.0
author: Peter Fahsel, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [decision-making, feature-design, planning, kanban, q-and-a]
    related_skills: [decision-narrowing, hermes-kanban-workers, plan]
---

# Feature-spec Q&A

Lightweight sibling of `decision-narrowing`: settle the design of a new feature/project **iteratively, one question per turn**, when there is no multi-report corpus to narrow. Typical case: a new project where research is done and the user wants to fix the feature design question by question, then turn the decisions into kanban cards. No subagent loop, no CONSTRAINTS/DECISIONS/STATE scheme — one decisions file.

## When to Use
- The user asks for a "Planungsvorschlag" / plan for a new feature in an existing repo (even a short bullet list of requirements) — load this skill together with `plan`; the plan file carries the findings, this skill carries the question round.
- Research is done, the feature/project design is open, and the user wants it settled question by question.
- The result should become kanban cards (code work pipeline).

Use `decision-narrowing` instead when a `deep-research` corpus with many candidate paths must be eliminated down to one.

## Question shape (shared with `decision-narrowing`)

One question per turn: 2–3 numbered, self-contained options, one marked recommended with a one-to-two-sentence justification. The user answers with a bare number or word. When asking via `clarify`, the free-text row is ALWAYS present and binding — a typed variant is filed exactly as typed, never mapped onto the nearest option. Define any load-bearing jargon in one line on first use.

Each confirmation turn has a fixed shape: "Notiert: <one line>", then the next question. No recap of earlier answers. **When the user's answer also asks a confirmation question** (validating their understanding of a consequence), answer it clearly FIRST — confirm or correct in 1–3 lines — before the 'Notiert' line; a vague confirmation silently mis-files the next decision.

## Procedure

1. **Read in first.** Read the repo, the research reports, and any UI screenshots of the reference product. Give a short status (goal, what exists, build options, known gaps) and ask Q1 in the same reply.
1b. **Verify the mechanism behind each requirement before asking about it.** When a requirement names a concrete artefact or client behaviour ("a file that opens the connection without a password prompt", "the token grants X"), check docs/web for whether that is physically possible with the user's actual clients BEFORE forming options; if it is not, lead with the finding and offer what the mechanism allows. Why: a question round built on an impossible premise produces decisions a card cannot implement. Also ask which client/tool the user actually uses when the answer depends on it (he often has two: Linux desktop + Windows laptop).
1c. **"Already true" requirements.** When a listed requirement is already satisfied by the code, say so with the `path:line` evidence and turn it into a docs-only step, not a card.
2. **Order by dependency.** Visibility/architecture first, then initiation, consent flow, completion/report-back, persistence, model/cost, cwd/context, edge cases (busy/closed target), UI, limits/recursion.
3. **Persist early.** Offer a decisions file after about 6 questions at the latest, then write it as `.hermes/decisions.md`: a table with D#, topic, decision, one-clause rationale, in English. After that, patch in each new answer *before* asking the next question, so a session switch loses nothing.
4. **Merge user additions.** If an answer adds something the options did not cover, merge it into that D# — do not open a new question for it. If the addition depends on a capability the research did not verify, add "Open: … verify docs-first in spec phase" to the D#, mention the gap in one line, and do not answer it from memory.
5. **Custom answers spawn follow-ups.** A user variant ("also allow X", "keep A but add prefix B") is filed, then the one or two sub-questions it opens are asked before moving on (e.g. a new state raises whether existing restrictions still apply and whether it is reversible). Never silently decide the dependent points.
6. **Carry cost and safety guards into the recommendations.** Confirmation before more expensive models, explicit `provider:model`, depth and concurrency caps, agent-initiated actions as a proposal card unless the user explicitly asked.
7. **Hand off to the board.** When the user asks to turn the decisions into work, first propose a card table: one row per card, the D#s it covers, its parents. Spec card first, turning every "Open: verify" item into a docs-first question; then backend → UI → live e2e. Get confirmation, commit and push the decisions file (worktrees see only committed files), then create the chain behind a gate card — recipe in `hermes-kanban-workers` (gating & batches, `references/cli-recipes.md`). Open questions go into a final "planning complete?" question before the user closes the gate.
8. **Late decisions after the cards exist.** Keep one question per turn, patch each D# as usual, do not commit after every answer. When the round ends, one consolidated pass: patch every affected card body in the board DB (recipe in `hermes-kanban-workers`, `references/cli-recipes.md`), then commit and push. A worker sees only committed files and the card text it was created with. Report which card gained which D#, as a table.
9. **Close the gate only on the user's explicit "done".** Release it (`unblock` if blocked, then `complete`), check `list` whether the dispatcher already started the first card, and offer a bounded background status poll on the first card with notify on exit.

## Extending an existing decision topic

If the feature belongs to a topic that already has a `decision-narrowing` directory (`.hermes/decision/<topic>/` with CONSTRAINTS/DECISIONS), do NOT start a separate `.hermes/decisions.md`: append to that topic's `DECISIONS.md` per the "Extending an existing topic's decision log" rules in `decision-narrowing` (stable sequential ids, re-validation against the full existing set).

## Pitfalls
- **Promising a credential format the client cannot honour.** Decision table for RDP/SSH "no prompt" delivery and generated guest passwords: `references/remote-access-credentials.md`.
- **Answering a gap from memory.** "Open: verify" items stay open until the spec card resolves them docs-first.
- **Decision in chat only.** A D# that is not in the committed file never reaches a worker.
- **Mapping free text onto an option.** The typed variant is the decision; the options were suggestions.
- **Committing after every late answer.** Batch late decisions into one consolidated card-body + commit pass.
