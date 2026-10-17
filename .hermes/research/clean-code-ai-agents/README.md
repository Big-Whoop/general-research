# Research corpus — clean-code-ai-agents

**Question:** Identify the 10 most important principles of Clean Code and how each works; then determine whether each is also useful for programming AI coding agents (Claude Code, Codex, Cursor, Devin, SWE-agent, Aider). Focus: research papers + practical experience from world-leading AI developers.

**Status:** COMPLETE (synthesized) · **Date:** 2026-10-17 · **Language:** English (the language the research was produced in)

**Tier scheme (all lanes):** **V**erified (authoritative/primary source actually read) · **P**lausible (sound general behavior / snippet-level, not demonstrated on-target) · **S**peculative (mechanism asserted, untested). Tiers are never collapsed into a flat assertion.

## Corpus manifest

| File | Axis / sub-question | One-line claim summary | Tier scheme | Status |
|---|---|---|---|---|
| `REPORT.md` | Synthesis (all axes) | Clean code is MORE useful for agents (reason shifted to the context window); most principles AMPLIFIED, KISS/YAGNI INVERTED, readability SPLIT; "locally clean but globally incoherent" is research-backed; recommend the full stack (rules file + mechanical gates + clean codebase). | V/P/S | CURRENT |
| `REPORT_DE.md` | Synthesis (all axes) — German 1:1 translation of `REPORT.md` | 1:1-Übersetzung des Hauptberichts ins Deutsche (gleiche Struktur, Zitate und Tiers). | V/P/S | CURRENT |
| `principles/lane1.md` | Facet A — the canonical 10 principles + how each works | No single source lists exactly "the 10"; it is a cross-source synthesis (Clean Code 2008 Part I + DRY/KISS/YAGNI + SOLID); KISS/YAGNI/SOLID are not Clean Code chapters. | V/P/S | CURRENT |
| `papers/lane2.md` | Facet B — research papers on clean code & LLM code quality | SWE-CI: clean/extensible code is rewarded over evolution but invisible on snapshot benchmarks; LLM code is "superficially clean but intrinsically complex"; agent-authored tests are mostly observational. | V/P/S | CURRENT |
| `papers/lane2-2.md` | Facet B (wave-2) — is "locally clean but globally incoherent" research-backed? | YES — Modular Mirage / architectural rot (2605.02741), Architectural Erosion / Hallucinated Coupling (2512.04273), growing LLM-technical-debt literature (2606.14796). | V/P/S | CURRENT |
| `practice/lane3.md` | Facet B — world-leading AI devs' & vendors' practical experience | Overwhelmingly pro-clean-code; converges on 3 mechanisms: a machine-runnable check the agent can't bypass, a short pruned instruction file, and the codebase-as-context ("sets a ceiling"). | V/P/S | CURRENT |
| `community/lane4.md` | Facet B — community practitioner experience (Reddit/HN/SO) | Bimodal: majority = clean code matters more (agent context/token budget); minority = moot; counterintuitive = locally-clean/globally-incoherent "meta-code"; a "code janitor" role is emerging. | V/P/S | CURRENT |
| `agent-mechanisms/lane5.md` | Facet B — clean code × agent architecture | Maps all 5 agent mechanisms to P1–P10 with AMPLIFIED/MOOT/INVERTED verdicts; the context window is the binding constraint behind nearly every verdict. | V/P/S | CURRENT |
| `verification/lane2-1.md` | Wave-2 — verify the two load-bearing anchors at primary | SonarSource study + SWE-CI confirmed at primary (arXiv 2605.20049 / 2603.03823); refined figures + caveats (vendor, one model/harness, wide per-task variance). | V/P/S | CURRENT |
| `ledger.json` | Source ledger (grounded-citations) | 28 sources, idempotent url→[n] mapping; 4 load-bearing anchors carry verbatim evidence quotes ([3] SWE-CI, [5] SonarSource, [6] AI-Generated Smells, [7] Technical Debt). | n/a | CURRENT |

## Reading order

1. `REPORT.md` — the answer (TL;DR → 10 principles → agent-paradigm verdict matrix → options matrix → tensions → untested-on-target → Sources).
2. `verification/lane2-1.md` + `papers/lane2-2.md` — the two wave-2 confirmations that upgrade the report's two load-bearing claims from community-only to primary/research-backed.
3. The five wave-1 lanes — the per-finding detail (claim + source URL + verbatim quote + tier) behind every synthesis claim.

## Conventions

- Per-finding citations (URL + verbatim quote + tier) live in the lane files; `REPORT.md` cites inline and references the lanes by path. `ledger.json` owns the `url → [n]` mapping.
- Only processed results are committed (report, lanes, ledger). Raw dumps / cached pages are never committed.
