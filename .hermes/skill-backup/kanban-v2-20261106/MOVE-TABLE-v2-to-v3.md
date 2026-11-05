# MOVE TABLE — hermes-kanban-workers v2.0.0 → v3.0.0

One row per H2/H3 heading of v2 SKILL.md (29 headings, in file order). "verbatim" = text block copied unchanged (apart from the noted watcher→end-turn wording); "condensed" = rule restated shorter in SKILL.md with the long form in the named reference. No heading was dropped as a duplicate.

| # | v2 line | v2 heading | Destination |
|---|---|---|---|
| 1 | 22 | ## When to use | SKILL.md §When to use (rewritten, shorter) |
| 2 | 29 | ## Hard rule: code changes go through the board ONLY (2026-09-29) | SKILL.md §Hard rules 1–2 (condensed, meaning kept); CLI-recipe pointer → references/core-workflow.md intro |
| 3 | 66 | ### Machine secrets: the agent creates them (C25) — never a "Peter creates it" step | references/release-duties.md §8 (verbatim) + SKILL.md §Hard rules 5 (pointer) |
| 4 | 78 | ### Flux image-automation proposal PRs (Peter, 2026-10-18) | references/release-duties.md §7 (verbatim) + SKILL.md §Hard rules 5 (pointer) |
| 5 | 114 | ## Feature branch, waves, and the user's inbox (user decisions 2026-10-18) | references/intake-planning.md (intro, verbatim); SKILL.md §Hard rules 3–7, 9 (condensed) |
| 6 | 121 | ### Feature integration branch: one CI run per feature | references/intake-planning.md §Feature integration branch (verbatim); SKILL.md §Hard rules 3–6, 9 (condensed) |
| 7 | 184 | ### Wave planning replaces chain building | references/intake-planning.md §Wave planning (verbatim incl. 0a–0d, 2b–2d, 1–5); SKILL.md §Intake steps 1–5 (condensed); 'questions one per turn' CHANGED to ≤2 clarify rounds in both |
| 8 | 325 | ### Coordination model (user decision 2026-11) — plan-first, supervise by event | SKILL.md §Intake, §Card rules (8), §Wake-turn protocol, §Roles, Models line (expanded; this was the v2 seed of v3) |
| 9 | 364 | ### User-facing text on cards — MANDATORY FORMAT | SKILL.md §Hard rules 8 + §Card rules 8 (pointer); full rule already verbatim in references/user-facing-card-text.md (unchanged) |
| 10 | 372 | ## Environment (this sandbox) | references/core-workflow.md §Environment (verbatim) |
| 11 | 384 | ## Core workflow | references/core-workflow.md (whole file) |
| 12 | 386 | ### 0. Answering architecture questions about a workstream's code | references/core-workflow.md §0 (verbatim; 'keep the watcher running' → 'end the turn') |
| 13 | 395 | ### 1. Board (one per project/workstream) | references/core-workflow.md §1 (verbatim) |
| 14 | 423 | ### 2. Tasks — pick the workspace DELIBERATELY | references/core-workflow.md §2 (verbatim); SKILL.md §Card rules workspace paragraph (condensed) |
| 15 | 449 | ### 3. Dependency control (the part people get wrong) | references/core-workflow.md §3 (verbatim) |
| 16 | 465 | ### 3b. Seeding a chain of several new cards: link BEFORE the dispatcher sees them | references/intake-planning.md §Seeding a chain + §Chain contracts, cross-board chains, verify→fix→re-run (verbatim); SKILL.md §Intake step 6 (condensed) |
| 17 | 546 | ### 4. Assign + dispatch | references/core-workflow.md §4 (verbatim) |
| 18 | 557 | ### 5. Concurrency | references/core-workflow.md §5 (verbatim) |
| 19 | 567 | ### 5b. Multi-profile fan-out (offload routine work to a second LLM host) | references/core-workflow.md §5b (verbatim incl. lane model binding, cpa switch, 301 trap, archive-from-blocked, reviewer strength) |
| 20 | 646 | ### 5c. Triage blocked cards / unattended chain runs | references/core-workflow.md §5c (all-boards listing, pre-unblock check, no long-lived blocked); overnight/watcher part → references/board-watch-cron.md §Overnight (emergency); sign-off steps already in references/release-duties.md §1 + unattended-delivery.md |
| 21 | 687 | ### 5d. Periodic board hygiene ("archive the stale cards across all boards") | references/core-workflow.md §5d (verbatim) |
| 22 | 746 | ### 6. Review the finished work (worker → human gate) | references/core-workflow.md §6 (verbatim); SKILL.md §Roles/default 'report first' (condensed) |
| 23 | 768 | ### 7. Post-merge conflict resolution (user merges, you fix the other PR) | references/core-workflow.md §7 (verbatim) |
| 24 | 792 | ### 9. Read-only conflict pre-analysis (do NOT touch the working tree) | references/core-workflow.md §9 (verbatim; long form was already in references/conflict-analysis.md) |
| 25 | 806 | ### 9b. Resume-note comments on half-finished cards (comments only) | references/core-workflow.md §9b (verbatim) |
| 26 | 809 | ### 10. Campaign cleanup (retire a feature: card + branches + cron + wrappers) | references/core-workflow.md §10 (verbatim) |
| 27 | 835 | ## In-session orchestration loop (desktop chat, not Telegram) | references/board-watch-cron.md §In-session orchestration loop (watcher mechanics, step 1, 2(b2), 3–4, emergency-only header); step 2 triage cases (a)–(e) + 'why is card X not claimed' → references/wake-triage.md; sign-off loop / Peter-only merge / auto-decomposer / review re-block / respawn guards (step 1 sub-paragraphs, 2(b)) → references/forensics.md §Kernel pitfalls; SKILL.md §Wake-turn protocol (condensed replacement) |
| 28 | 1125 | ## Pitfalls (learned the hard way) | Kernel pitfalls 0, 2, 3, 14, 15, 16, 18, 19, 20, 21, 22 → references/forensics.md §Kernel pitfalls (verbatim); workspace/git/card-design pitfalls 1, 4–12, 17, 17b → references/campaign-pitfalls.md (verbatim); SKILL.md §Card rules 2, 5, 8 and §Wake-turn 2–3 (condensed mechanics) |
| 29 | 1421 | ## Verification (definition of done) | SKILL.md §Verification (rewritten + extended with intake DoD; v2 three bullets kept in the 'wave is done' paragraph and references/core-workflow.md §10 step 5) |

## New / changed files

| File | Status |
|---|---|
| SKILL.md | rewritten, v3.0.0, 21.7 KB |
| references/intake-planning.md | NEW (moved from v2) |
| references/core-workflow.md | NEW (moved from v2) |
| references/wake-triage.md | NEW (moved from v2) |
| references/campaign-pitfalls.md | NEW (moved from v2) |
| references/forensics.md | existing content kept, kernel pitfalls appended |
| references/board-watch-cron.md | rewritten: emergency-only header, v2 loop prepended, old cron recipe kept |
| references/release-duties.md | existing content kept, §7 Flux proposals + §8 machine secrets appended |
| all other references/, scripts/, templates/ | unchanged (not copied) |
