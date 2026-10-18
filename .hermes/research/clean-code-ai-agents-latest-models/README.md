# Research corpus — clean-code-ai-agents-latest-models

**Question:** Repeat the 2026-10-17 clean-code × AI-coding-agent research (`../clean-code-ai-agents/`) using only sources dated ≥ 2026-06-01 that concern the current frontier model generation (Oct 2026: Opus 5.5 / GPT-6.x / Gemini 4 Argon). Re-derive the per-principle agent verdicts and diff them against the baseline.

**Status:** COMPLETE (synthesized) · **Date:** 2026-10-18 · **Language:** English (+ German 1:1 translation of the report)

**Tier scheme (all lanes):** **V**erified / **P**lausible / **S**peculative (see REPORT.md). Findings measured only on the previous point release (Opus 5, GPT-5.6) are marked [A]. Older models are capped at Plausible.

## Corpus manifest

| File | Axis / sub-question | One-line claim summary | Tier scheme | Status |
|---|---|---|---|---|
| `REPORT.md` | Synthesis + DIFFERENCES vs 2026-10-17 + Fable 5.1 supplement (§8) | Clean code still matters more. The mechanism moved from window fit to exploration cost. Over-building is the main failure. P2/P7/P8/P10 CHANGED. Recommend recalibrated full stack 5′ (independent gates as the centrepiece). §8: Fable 5.1 confirmed — over-building grows with effort, reward hacking drops 73.5%→11.1%, model-tier routing is the new practice. | V/P/S | CURRENT |
| `REPORT_DE.md` | Synthesis, German 1:1 translation | 1:1-Übersetzung von REPORT.md. | V/P/S | CURRENT |
| `models/lane1.md` | Current model generation (dated) + official vendor guidance | Frontier as of 2026-10-18: Opus 5.5, GPT-6 Astra/6.1 Sol, Gemini 4 Argon. Vendors now restrain scope and over-verification. AGENTS.md is more influential on GPT-6. | V/P/S | CURRENT |
| `papers/lane2.md` | Academic papers ≥ 2026-06-01 + baseline paper status | No replication of baseline anchors. Current-gen: inherited test failures cost −5.6 pp, 50.8% duplication by turn 5, 43.1% policy violations, rigid interfaces drive re-implementation. | V/P/S | CURRENT |
| `practice/lane3.md` | Industry studies + engineering blogs | Cohesive refactor −83% tokens/change. Agent-run uplift 300 kLoC for ~$4k. TDD-in-loop no gain. Frontier needs a final gate only, cheaper models need in-loop sensors. | V/P/S | CURRENT |
| `community/lane4.md` | Reddit / HN / Lobsters practitioners | Baseline confirmed. Over-engineering is the dominant failure, partly eased in Opus 5.5. Agent test volume and stale rules files are new problems. Dissent now says "AI writes clean code". | V/P/S | CURRENT |
| `agent-mechanisms/lane5.md` | Why clean code matters now (capacity / attention / cost), gates, reward hacking | Capacity argument weaker (1M). Attention degradation unchanged. Cost reframed to exploration. Reward hacking 3–6× higher on impossible tasks, so gates are still needed. | V/P/S | CURRENT |
| `fable-5-1/lane1.md` | Fable 5.1 supplement — official/vendor (SQ1) | Fable 5.1 = top-tier GA model (2026-09-01 Verified at 4 primaries); $10/$50, 1M ctx; Fable/Mythos = same model, different safeguards; vendor ships scope + edit guidance. | V/P/S | CURRENT |
| `fable-5-1/lane2.md` | Fable 5.1 supplement — independent measurements (SQ2) | 7 arXiv papers evaluate Fable 5.1; reward hacking 73.5%→11.1%; no independent generated-code-quality study (documented absence). | V/P/S | CURRENT |
| `fable-5-1/lane3.md` | Fable 5.1 supplement — community practitioners (SQ3a) | Opus 5.5 = workhorse for 80–90%, Fable = architect/orchestrator; over-building is the signature failure; usage hog; long-horizon strength; clean code only with standards + review. | V/P/S | CURRENT |
| `fable-5-1/lane4.md` | Fable 5.1 supplement — practice / engineering / GitHub (SQ3b) | Huntress 48%→28/28 with rule + second-model reviewer; Cognition quantifies over-building as an effort-dependent scope penalty; vendor injects a scope clause into the system prompt. | V/P/S | CURRENT |
| `ledger.json` | Source ledger (grounded-citations) | 95 sources cited by REPORT.md / REPORT_DE.md; per-finding quotes live in the lane files. | n/a | CURRENT |

## Reading order

1. `REPORT.md` §TL;DR → §3 verdict matrix → §5 DIFFERENCES → §8 Fable 5.1 supplement.
2. `models/lane1.md` (it defines the model filter), then the other lanes for per-finding evidence.
3. `fable-5-1/lane1.md` … `lane4.md` for the per-finding evidence behind §8.

## Conventions

- Lane files hold the per-finding citations (URL + verbatim quote + tier + date evidence). The report cites inline via `ledger.json`.
- The baseline corpus is comparison-only. None of its 28 sources is re-cited as new evidence.
- No wave 2 was run. The remaining gaps are documented absences (see REPORT.md §7).

## Fable 5.1 supplement (2026-10-18)

**Trigger:** user finding — Fable 5.1 is named in the model table (M4) but not investigated; it is Anthropic's top-tier model, and the report's de-facto frontier (Opus 5.5) is the cheaper model that "performs at the level of Claude Fable 5.1 on most work." Run with the revised deep-research skill v0.6.0 (subagent lanes, no kanban).

### Premise

| Subject | Verified as | Source |
|---|---|---|
| Claude Fable 5.1 | Anthropic's top-tier model, "the world's most advanced models for coding and knowledge work"; Fable 5.1 = Mythos 5.1 (same model, different safeguards); released 2026-09-01 (date: Plausible, secondary — lane 1 verifies at primary); available to Pro/Max/Team/Enterprise | anthropic.com/claude-fable-and-mythos-5-1 (read in main run, M4); anthropic.com/claude/fable; The Hindu 2026-09-01; MacRumors 2026-09-01 |

### Source universe (Step 0)

| Source type | Plan |
|---|---|
| Official: Anthropic announcement, Fable product page, system card, API changelog, pricing, prompting guides | lane 1 |
| Papers / independent benchmarks: arXiv ≥ 2026-06-01, third-party evals of Fable 5.1 | lane 2 |
| Community: Reddit (r/ClaudeAI, r/ClaudeCode, r/ExperiencedDevs, r/LocalLLaMA), HN, Lobsters | lane 3 |
| Practice: engineering blogs, hands-on write-ups, GitHub issues/PRs mentioning Fable 5.1 | lane 4 |
| Upstream: n/a (the subject is a model, not a wrapped engine) | skipped (reason) |

### Coverage table (Step 1)

| Sub-question | Lane |
|---|---|
| SQ1: What exactly is Fable 5.1 — positioning, capabilities (days-long async tasks), Fable vs Mythos safeguards, availability, pricing, primary release date, vendor benchmarks, Fable-specific vendor guidance? | lane 1 (official) |
| SQ2: What do independent measurements (papers, third-party benchmarks) say about Fable 5.1's coding performance and code quality? | lane 2 (papers/benchmarks) |
| SQ3a: What do community practitioners report about Fable 5.1 (code quality, over-building, cost, long-horizon tasks)? | lane 3 (community) |
| SQ3b: What do hands-on write-ups / engineering blogs / GitHub issues report about Fable 5.1 in real coding work? | lane 4 (practice) |
| SQ4: Does Fable 5.1 change the report's per-principle verdicts or the Option 5′ recommendation? | synthesis (from all lanes) |

### Round 1 assessment

| Sub-question | Highest tier reached | Independent sources for the load-bearing claim | Workaround space searched | Lane verdict | Status |
|---|---|---|---|---|---|
| SQ1: What exactly is Fable 5.1 | Verified | 6 primary Anthropic sources (announcement, product page, system card, model docs, API changelog, prompting guide); release date Verified at 4 primaries | n/a (codenames checked: Project Glasswing) | answered | CLOSED |
| SQ2: Independent measurements | Verified | 7 arXiv papers + CodeRabbit primary; AA/Vals/ARC/Snorkel via secondary (Plausible); code-quality gap = documented absence | searched (5 arXiv phrase queries, third-party evals, other labs) | partial | CLOSED (absence is a finding — no concrete source where the missing evidence should exist; see REPORT.md §8.5) |
| SQ3a: Community experience | Verified | 37 sources; ~10 independent threads on the load-bearing claims | searched (all model-name variants + alternative vocabulary; Lobsters 0; X access-limited) | answered | CLOSED |
| SQ3b: Practice / GitHub | Verified | Huntress, CodeRabbit, Cognition/Devin, Every, 10 GitHub issues | searched (UA-spoof, model-ID quirks; Aider/SWE-agent 0 results) | partial | CLOSED (documented absences: per-day long-run cost, conference talks — see REPORT.md §8.5) |

No round 2: every row is CLOSED (highest tier Verified; load-bearing claims carry 2+ independent sources; the remaining gaps are documented absences that a second wave would only re-search). Synthesis landed in REPORT.md / REPORT_DE.md §8.
