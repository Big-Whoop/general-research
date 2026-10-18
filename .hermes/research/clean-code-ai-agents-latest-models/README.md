# Research corpus — clean-code-ai-agents-latest-models

**Question:** Repeat the 2026-10-17 clean-code × AI-coding-agent research (`../clean-code-ai-agents/`) using only sources dated ≥ 2026-06-01 that concern the current frontier model generation (Oct 2026: Opus 5.5 / GPT-6.x / Gemini 4 Argon). Re-derive the per-principle agent verdicts and diff them against the baseline.

**Status:** COMPLETE (synthesized) · **Date:** 2026-10-18 · **Language:** English (+ German 1:1 translation of the report)

**Tier scheme (all lanes):** **V**erified / **P**lausible / **S**peculative (see REPORT.md). Findings measured only on the previous point release (Opus 5, GPT-5.6) are marked [A]. Older models are capped at Plausible.

## Corpus manifest

| File | Axis / sub-question | One-line claim summary | Tier scheme | Status |
|---|---|---|---|---|
| `REPORT.md` | Synthesis + DIFFERENCES vs 2026-10-17 | Clean code still matters more. The mechanism moved from window fit to exploration cost. Over-building is the main failure. P2/P7/P8/P10 CHANGED. Recommend recalibrated full stack 5′ (independent gates as the centrepiece). | V/P/S | CURRENT |
| `REPORT_DE.md` | Synthesis, German 1:1 translation | 1:1-Übersetzung von REPORT.md. | V/P/S | CURRENT |
| `models/lane1.md` | Current model generation (dated) + official vendor guidance | Frontier as of 2026-10-18: Opus 5.5, GPT-6 Astra/6.1 Sol, Gemini 4 Argon. Vendors now restrain scope and over-verification. AGENTS.md is more influential on GPT-6. | V/P/S | CURRENT |
| `papers/lane2.md` | Academic papers ≥ 2026-06-01 + baseline paper status | No replication of baseline anchors. Current-gen: inherited test failures cost −5.6 pp, 50.8% duplication by turn 5, 43.1% policy violations, rigid interfaces drive re-implementation. | V/P/S | CURRENT |
| `practice/lane3.md` | Industry studies + engineering blogs | Cohesive refactor −83% tokens/change. Agent-run uplift 300 kLoC for ~$4k. TDD-in-loop no gain. Frontier needs a final gate only, cheaper models need in-loop sensors. | V/P/S | CURRENT |
| `community/lane4.md` | Reddit / HN / Lobsters practitioners | Baseline confirmed. Over-engineering is the dominant failure, partly eased in Opus 5.5. Agent test volume and stale rules files are new problems. Dissent now says "AI writes clean code". | V/P/S | CURRENT |
| `agent-mechanisms/lane5.md` | Why clean code matters now (capacity / attention / cost), gates, reward hacking | Capacity argument weaker (1M). Attention degradation unchanged. Cost reframed to exploration. Reward hacking 3–6× higher on impossible tasks, so gates are still needed. | V/P/S | CURRENT |
| `ledger.json` | Source ledger (grounded-citations) | 42 sources cited by REPORT.md / REPORT_DE.md; per-finding quotes live in the lane files. | n/a | CURRENT |

## Reading order

1. `REPORT.md` §TL;DR → §3 verdict matrix → §5 DIFFERENCES.
2. `models/lane1.md` (it defines the model filter), then the other lanes for per-finding evidence.

## Conventions

- Lane files hold the per-finding citations (URL + verbatim quote + tier + date evidence). The report cites inline via `ledger.json`.
- The baseline corpus is comparison-only. None of its 28 sources is re-cited as new evidence.
- No wave 2 was run. The remaining gaps are documented absences (see REPORT.md §7).
