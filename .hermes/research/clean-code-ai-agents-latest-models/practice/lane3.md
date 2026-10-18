# LANE-3 — Industry studies + vendor/practitioner engineering blogs (post-2026-06-01)

Research run: RESEARCH-clean-code-ai-agents-latest-models (task t_27d77f31, parent t_875c7cc1)
Date of research: 2026-10-18
Scope: quantified industry studies and vendor/practitioner engineering posts dated on/after 2026-06-01, current frontier model generation (Claude Opus 4.8 / Sonnet 5 / Mythos-class Fable 5; GPT-6 Sol/Luna; Gemini 3.8), on which code-quality practices matter for agents.
Tier scheme: **Verified** (source read in full, on-target for current-gen agents) / **Plausible** (read, but mechanism or model generation not fully on-target, or vendor self-interest/small n) / **Speculative** (inferred).
Anchor: [P1] naming, [P2] small functions/SRP, [P3] DRY, [P4] KISS, [P5] YAGNI, [P6] SOLID, [P7] error handling, [P8] testing/TDD, [P9] refactoring/Boy Scout, [P10] readability/maintainability.
Baseline comparison: ../../clean-code-ai-agents/REPORT.md (2026-10-17). None of its 28 ledger sources are cited here as evidence.

Deviation: the full brief file (/opt/data/cache/scratch/research-clean-code-ai-agents-latest-models/lane3.body.md) did not exist at run time (pruned or never written); this lane worked from the inline brief summary on the kanban card.

---

## TL;DR

1. **Structure (P2/P3/P9/P10) is now quantified in tokens and is the strongest post-June signal.** Thoughtworks/Fowler (30 Jul 2026): refactoring a 17,155-line agent-written Rust file into cohesive modules cut input tokens for an identical change by 83% (159,564 -> 27,360). CodeScene (24 Sep 2026): a 300 kLoC C codebase uplifted to Code Health 10 by Claude Opus agents in 3 weeks for ~$4k, with projected ~70% fewer AI-induced defects and ~45% less token waste. Verdict: AMPLIFIED, and the *reason* is now cost/context, measured. [F-01, F-02, F-03]
2. **Agents still degrade structure by default (P3/P9 INVERTED pressure persists in the current generation).** GitClear 2026 (623M changes): block duplication +81% vs 2023, moved/refactored code down to 3.8% of changed lines, cross-file reuse -35%, error-masking constructs +47%. Fowler: "Claude was not good at refactoring" without human guidance. Anthropic: engineers' main job became telling Claude "no" when it violated system constraints or over-engineered after adversarial review. [F-04, F-05, F-06]
3. **TDD-in-the-loop (P8, process form) is weakening to MOOT/INVERTED; tests-as-sensor is AMPLIFIED.** Böckeler (Jul 2026): agent-internal TDD gave no quality gain, often ranked lower, cost 3-8.5x tokens; she stopped asking agents to do TDD. Jain (13 Oct 2026): a deterministic harness gave GPT-6 Sol no gain (10/10 either way, 7x cost) but turned GPT-6 Luna from 3/10 to 10/10. Independent verification gates remain required for all models. [F-07, F-08, F-09]
4. **KISS/YAGNI (P4/P5) still must be imposed** — even with Mythos-era models; Anthropic reports adversarial review pushing Claude into over-engineering, and Böckeler reports agents overshooting minimal implementation. [F-06, F-07]
5. **Context/navigation beats raw model power** for large codebases: Sourcegraph (16 Jun 2026) Sonnet 4.6 + code search beat Mythos-class Fable 5 on a local checkout (0.698 vs 0.568, half the $/point; 9 tasks only). Supports P1 (searchable names) / P10 indirectly; strongest for tooling, not code style. [F-10]
6. **Delivery-level studies: throughput up, review is the bottleneck, quality gates matter more.** Harvard/Jellyfish (Aug 2026, 718 firms): +30% code, no rise in finished work, review time +49%. Sonar (29 Sep 2026) cites CMU/Cursor study (+30% warnings, +41% cognitive complexity) and argues for independent, in-loop gates. [F-11, F-12]

Net diff vs 2026-10-17 baseline (for collector): direction of verdicts unchanged for P1-P7, P9, P10; **P8 splits harder** (TDD workflow -> MOOT/INVERTED for frontier agents; regression suites/mutation testing/contract sensors -> AMPLIFIED, with cadence depending on model tier); **P2/P3/P9 move from "argued" to "quantified" (tokens, defects)**; new nuance: harness/gate value is *inversely* related to model capability per run, but an independent final gate stays required.

---

## Findings

### F-01 — Refactoring an agent-written god-file cut per-change input tokens by 83% [P2, P3, P9, P10] — KEY
- Claim: Splitting a 17,155-line agent-written Rust data-access file via strict refactoring (dedupe, extract client/helpers, split into 19 cohesive files) reduced input tokens for an identical representative change from 159,564 to 27,360; the saving comes from the agent reading a smaller relevant subset, not from less total code.
- Source: https://martinfowler.com/articles/exploring-gen-ai/refactoring-economic-benefit.html (practitioner long-form, Thoughtworks CTO EMEA, martinfowler.com "Exploring Gen AI"). Date: "30 July 2026". Models: Claude Code (Sonnet 5 pricing referenced), Cursor. Read in full.
- Verbatim: "Between the base line and the final refactoring, input tokens for the same task reduced from **159,564** to **27,360**. A saving of **132,204** tokens, or **83%**." / "This saving is because the agent has to read less code. But it is not because there is less code to read." / "randomly cutting the file into smaller files is unlikely to help as much: even if each file were smaller, the agent would be forced to read through many files looking for the relevant code."
- Tier: **Verified** (n=1 codebase, one representative change; author flags token counting approximated by chars/4). Verdict evidence: P2 AMPLIFIED with explicit *cohesion* caveat (random splitting does not help); P3 AMPLIFIED (dedupe set up the saving); P9 AMPLIFIED (economic case now measured).

### F-02 — Same source: current agents are poor at choosing and applying refactorings unaided [P9]
- Claim: Claude identified/applied refactorings only when directed; an explicit refactoring step in the harness did not trigger improving the file; mechanical refactoring via grep/sed scripts broke on indentation; the most valuable refactoring was initially skipped.
- Source: as F-01.
- Verbatim: "Claude was not good at refactoring. ... Claude is unable to look at code, look at refactorings in general and work out which are suitable to apply: a human needs to actively guide it." / "The development harness includes an explicit refactoring step. That refactoring step did not prompt Claude into improving this file."
- Tier: **Verified** (single practitioner, current-gen Claude Code). Verdict: P9 STILL-USEFUL/AMPLIFIED but must be human-initiated (INVERTED pressure: agents do not self-apply Boy Scout).

### F-03 — CodeScene: 300 kLoC refactored to Code Health 10 by agents in 3 weeks, ~$4k [P2, P3, P9, P10] — KEY
- Claim: Using Claude Opus (Claude Code) with a Code Health MCP server as objective feedback signal and a replay-trace harness for behavioural equivalence, a 300k-line C codebase (Street Fighter III) went from avg Code Health 5.6 to 10.0 in 3 weeks (2,903 commits, 252,055 lines modified); projected ~70% fewer AI-induced defects and ~45% less token waste for future features. Smaller models (Sonnet, "Terra") plateaued at local optima; Opus beat Codex/"Sol" at capturing refactoring patterns into a playbook. Many attempts did not improve or degraded health — documented failures were fed back.
- Source: https://codescene.com/blog/case-study-refactoring-at-scale-with-agents (vendor engineering blog, Adam Tornhill). Date: "Sep 24, 2026". Read in full.
- Verbatim: "Your existing code is an important part of any AI agent's context. Consequently, poorly structured code and technical debt are considerable barriers to agentic coding." / "The uplift was executed in three weeks at a token cost of roughly 4,000 USD." / "A ~ 70% reduction in AI-induced defects making the code itself AI-ready. A reduction of token waste with ~45% when implementing future features." / "not all refactoring attempts were successful. Many didn't move the quality needle at all, while some attempts even made it worse"
- Tier: **Plausible** for the outcome numbers (vendor projection from its own prior research, not measured on the uplifted codebase yet — the Lund follow-up study is pending); **Verified** for the process facts (current-gen models, metric-gated agent loop). Verdict: P9 AMPLIFIED (economics of debt paydown inverted — cheap now), conditional on an objective gate + behavioural oracle.

### F-04 — GitClear 2026: duplication up 81%, refactoring collapses, error-masking up 47% [P3, P7, P9]
- Claim: Across 623M analyzed changes 2023-2026 as AI authorship rose: block duplication 40.3 -> 73.0 per M changed lines (+81%), moved (refactored) code 3.8% of changed lines YTD 2026 (21% in 2022), copy/paste 15.7% H1 2026, cross-file function connectivity -35%, long-term legacy updates -74%, error-masking constructs +47%, two-week churn +15%.
- Source: https://www.gitclear.com/the_ai_code_quality_maintainability_gap (industry report landing page; full PDF gated behind form — not read). Date evidence: data "year-to-date in 2026" / "first half of 2026" → published ≥ mid-2026; explicit publication date not shown.
- Verbatim: "block duplication climbed from 40.3 in 2023 to 73.0 year-to-date in 2026 — an 81% increase over 2023" / "today's default AI workflow is incentivized to deliver atomic code — a happy-path, a passing test, a closed ticket — while quietly taxing the invisible and the deferred: the reuse, consolidation, and error-surfacing"
- Tier: **Plausible** (summary page only; date inferred; not separated by model generation; correlational). Verdict: P3 AMPLIFIED need / INVERTED default pressure; P7 error-masking is an agent default to gate against; P9 refactoring must be budgeted.

### F-05 — Anthropic: engineers' role is to tell Claude "no"; adversarial review causes over-engineering [P4, P5, P6, P7]
- Claim: In building Scion (in-house VCS) with Claude incl. Mythos Preview, agents sometimes violated core system constraints to satisfy a bad existing pattern; adversarial review made Claude add excessive defensive validation/complexity, requiring human steering; humans now review intent rather than every line. Also: the codebase ended up "among the most well-tested" thanks to agent-written hermetic simulations and fuzzing.
- Source: https://www.anthropic.com/engineering/redesigning-source-control (vendor engineering blog). Date: "Published Oct 13, 2026". Read in full (relevant sections).
- Verbatim: "Very often, we found that the role of the engineers was to tell Claude "no." Agents will sometimes violate core system constraints to satisfy a pattern that should never have been allowed in the first place." / "skilled engineers needed to steer Claude away from over-engineering parts of the system in response to hypothetical concerns. For example, one such review was overly defensive about trusting another internal service, which resulted in Claude adding excessive validation and complexity." / "Scion is among the most well-tested and well-defended codebases we have ever worked on."
- Tier: **Verified** (first-party, current Mythos-class generation). Verdict: P4/P5 INVERTED pressure persists at frontier; P7 over-defensiveness is now a failure mode (not only missing error handling); P10 "pattern that should never have been allowed" = existing bad code is copied (codebase-as-context); P8 AMPLIFIED (cheap, extensive tests).

### F-06 — Anthropic: merges/day 2,500 -> 30,000+; human-scale CI/merge queues break [P8, gates]
- Claim: Agent code volume grew >10x in 4 months; Anthropic moved from global merge-queue locks to post-merge/pre-deploy automated testing.
- Source: as F-05.
- Verbatim: "In May 2026, Anthropic averaged around 2,500 code changes merged per day; as of September, we merged over 30,000 per day." / "A proper merge queue, for example, doesn't make much sense at agent scale. ... we've invested in post-merge and pre-deploy automated tes[ting]"
- Tier: **Verified** (first-party; Anthropic itself says workload is atypical). Verdict: automated gates AMPLIFIED but relocated.

### F-07 — TDD inside the agent loop: no quality gain, 3-8.5x tokens [P8, P5] — KEY
- Claim: In an exploratory eval (Sonnet 4.6 generating, Opus 4.8 judging blind, mutation testing), agent-internal TDD produced no better design/test quality or mutation scores than non-TDD; non-TDD often ranked higher because it designed up front; TDD cost 2.96x-8.5x tokens; minimal-implementation instructions did not stop over-building; author stopped instructing agents to do TDD, keeps regression tests + mutation testing + static analysis.
- Source: https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html (practitioner long-form, Birgitta Böckeler, Thoughtworks). Date evidence: experiment artefacts "sol-2026-07-10_..."; references Opus 4.8; page lists "latest article (Oct 13)". Read in full.
- Verbatim: "Based on Opus's judgment of the quality of the outcomes, there was no clearly discernable difference based on TDD workflow versus no TDD workflow. On the contrary, more than once Opus ranked the non-TDD workflow solutions slightly higher in design and test quality." / "I personally have stopped telling my coding agents to write tests first, let alone do TDD" / "minimal-implementation instructions didn't reliably stop them from building more" / "I think at this point there is generally more and more evidence that being overly specific about _how_ we want a model to do something is not a sustainable approach. Instead, we should find as many ways as we can to monitor the outcomes and give feedback."
- Tier: **Plausible** (small n, greenfield tasks, generator Sonnet 4.6 is one generation behind the judge). Verdict: P8-as-TDD-process MOOT/INVERTED for agents; P8-as-regression-suite STILL-USEFUL/AMPLIFIED; P5 via small steps does not transfer.

### F-08 — Behavioural harness: no gain for GPT-6 Sol, 3/10 -> 10/10 for GPT-6 Luna [P8, gates, types/contracts] — KEY
- Claim: Building one API service from a detailed brief, 10 paired runs each: GPT-6 Sol passed all 178 acceptance tests 10/10 with or without harness (harness = 10.5x tokens, ~7x cost); GPT-6 Luna went 3/10 -> 10/10 with harness, harnessed Luna 33% cheaper than unharnessed Sol. Unharnessed misses clustered on contract details (HTTP codes, null vs array, config names) — "attention lapses". Conclusion: model capability changes *when* sensors run, not whether an independent gate is needed.
- Source: https://martinfowler.com/articles/are-harnesses-worth-the-cost.html (practitioner long-form, Naresh Jain). Date: "13 October 2026". Read in full (setup through conclusions).
- Verbatim: "Using Codex with GPT-6 Sol at low reasoning effort, the agent produced an application that passed all 178 automated acceptance tests in each of the 10 runs, both with and without the harness." / "Without a harness, it succeeded in 3 of 10 runs. With the harness, it succeeded in all 10." / "Model capability changes when and how often sensors run, not whether an independent verification gate is needed." / "For frontier models: Retain an independent acceptance check even when a model passes consistently on the first attempt. Instead of running continuous checks during development, run the automated tests once as a deterministic final verification gate"
- Tier: **Verified** (current-gen models, controlled, n=10 per arm; one greenfield service, unusually complete brief). Verdict: P8 STILL-USEFUL as final gate for frontier, AMPLIFIED in-loop for cheaper models; machine-readable contracts (OpenAPI/AsyncAPI) act as types-at-the-boundary (P7/P6 interface discipline).

### F-09 — Sonar: first-pass quality; agents cannot be their own reviewer; independent in-loop gates [P8, P10, gates]
- Claim: Agent PRs grew from ~300 to ~3,000 lines; rework/review churn erase gains. Cites LinearB 2026 (8.1M PRs: agent PRs wait 4.6x longer for review), Faros (AI-heavy teams +98% PRs merged, review time +91%), CMU study of 806 Cursor-adopting projects (+30% static-analysis warnings, +41% cognitive complexity persisting after velocity spike faded). Prescribes Guide -> Verify -> Solve: give architecture patterns/standards/constraints up front, run quality gates before human review, feed findings back to the agent.
- Source: https://www.sonarsource.com/blog/how-to-achieve-first-pass-quality-with-ai-coding-agents/ (vendor blog). Date: "September 29, 2026". Read in full.
- Verbatim: "Pull requests that used to be 300 lines are now 3,000" / "studying 806 open-source projects that adopted Cursor, found a velocity spike that dissipated within two months while the added complexity persisted: +30% code analysis warnings and +41% cognitive complexity" / "An agent cannot be its own reviewer; verification has to be independent of generation to be trustworthy."
- Tier: **Plausible** (vendor marketing; secondary citations not read at origin; model generation of cited studies mixed). Verdict: P10 AMPLIFIED (complexity accrues), gates AMPLIFIED, "rules in the instruction file" STILL-USEFUL as guide layer.

### F-10 — Sourcegraph: cheaper model + code search beats Mythos-class model on local checkout [P1, P10, context]
- Claim: On 9 discovery-heavy CodeScaleBench tasks, Claude Sonnet 4.6 + Sourcegraph MCP (no code on disk) scored 0.698 vs Fable 5 with full local checkout 0.568, at $1.02 vs $1.83 per quality point; gap concentrated in cross-repo symbol/reference discovery.
- Source: https://sourcegraph.com/blog/sourcegraph-mcp-and-a-cheaper-model-beat-a-mythos-class-model-alone (vendor engineering blog; read via browser — web_extract failed). Date: "June 16, 2026".
- Verbatim: "Claude Sonnet 4.6 with the Sourcegraph MCP server and no source code on disk scored 0.698. Claude Fable 5, working from the whole repository checked out locally with no retrieval at all, scored 0.568" / "Treat the result as an early signal, not a settled benchmark."
- Tier: **Plausible** (vendor benchmark, 9 tasks, self-flagged early signal). Verdict: navigation/findability is the bottleneck even for the strongest model → P1 (searchable, unique names) and directory/module structure AMPLIFIED indirectly (Speculative link — the study measures tooling, not naming).

### F-11 — Harvard/Jellyfish (718 firms): +30% code, no rise in finished work, review +49% [P10, gates]
- Claim: Staggered DiD over 725,938 workers / 718 firms (Jan 2021-Mar 2026): AI coding agent adoption → ~30% more code, no detectable increase in finished work, code review time +49%.
- Source: https://complexdiscovery.com/harvard-researchers-find-ai-coding-agents-shifted-the-bottleneck-to-code-review/ (secondary news analysis of Chen & Stratton working paper, version dated Aug 4, 2026). Article date: Oct 13, 2026. Paper itself not read.
- Verbatim: "Engineers at firms that adopted AI coding agents added about 30 percent more code, yet finished work did not measurably rise and getting code through review took 49 percent longer" / "The current version of the paper is dated Aug. 4, 2026"
- Tier: **Plausible** (secondary report; not peer-reviewed; sample ends Mar 2026 so mostly pre-current-gen models). Verdict: readability for *human reviewers* (P10) remains a bottleneck — not MOOT.

### F-12 — Shopify AppSec harness (Jul 2026): tests are the oracle; partition by domain to 20-30% of context [P8, P2/structure, P4]
- Claim: Shopify's agentic vulnerability harness over 80+ apps (incl. the Core Rails monolith) depends on a test-bootstrap stage, a shared architecture-documentation artifact, and partitioning files by domain to ~20-30% of the context window; partitioning improved accuracy and recall in benchmarks; deterministic scripts for structured outputs; better models produce more confident noise, so the harness (not the model) is the durable asset.
- Source: https://shopify.engineering/building-an-agentic-harness-that-outlasts-the-model (vendor engineering blog). Date: "Published on Jul 29, 2026". Read in full.
- Verbatim: "Tests are the oracle" / "Aim for token counts of roughly 20-30% of the context window of the model in use" / "Group files by related domain, purpose, or feature." / "When using partitions, we observed improved accuracy and recall while keeping costs reasonably low." / "a better hunter also produces more confident-sounding noise"
- Tier: **Verified** for practice (first-party, current frontier models); outcome numbers not separated by code-quality factors. Verdict: P8 AMPLIFIED (existing test pipelines enabled the oracle); domain-cohesive directory structure AMPLIFIED (Plausible link to code layout — partitioning is done by the harness, but easier when code is grouped by domain).

### F-13 — InfoQ: deterministic fitness functions remain primary; agentic fitness functions as advisory layer [P6, architecture gates]
- Claim: For AI-generated code, deterministic fitness functions (dependency direction, contract shape, latency budgets) should remain the enforcement mechanism; LLM-based "agentic fitness functions" add judgment for boundary fidelity / semantic drift, kept advisory, with escalation to humans; recurring patterns get converted into deterministic guardrails.
- Source: https://www.infoq.com/articles/agentic-fitness-functions-evolutionary-architecture/ (practitioner long-form, InfoQ Certified Architect cohort). Date: "Aug 17, 2026". Read key takeaways + opening sections.
- Verbatim: "Deterministic fitness functions should remain the primary enforcement mechanism for measurable invariants such as dependency direction, contract shape, latency budgets, security posture, and policy checks." / "A production-ready implementation separates deterministic gates from agentic advisory signals"
- Tier: **Plausible** (framework article, no quantified outcome; not model-specific). Verdict: P6 (dependency direction/DIP, boundaries) STILL-USEFUL → AMPLIFIED when encoded as executable architecture tests.

### F-14 — Monorepo context engineering: directory-scoped instruction files, delegated search [AGENTS.md practice, structure]
- Claim: In a monorepo the cost driver is everything read staying in context; mechanisms: root vs package-level CLAUDE.md (package file loads only when that package is read), glob-activated skills, subagent-delegated search; "name the files, not the module".
- Source: https://www.matthewswong.com/en/blog/context-engineering-monorepo-ai-agents/ (practitioner blog). Date: "September 2026". Read opening sections.
- Verbatim: "Claude Code loads a root CLAUDE.md at launch and a package CLAUDE.md only when it reads that package, and a subagent's file reads never enter the main window." / "A wrong file opened in minute three is therefore still being paid for in minute forty"
- Tier: **Plausible** (single practitioner, mechanism from vendor docs, no measurement). Verdict: package/directory structure with scoped instructions = context hygiene; P10 rules files should be hierarchical and short (consistent with baseline).

### F-15 — Adoption context (scale of the shift) [context only]
- Claim: JetBrains DevEco 2026 (15k+ devs, May-Jul 2026): 90% use AI coding agents weekly, 68% daily; ~47% of code reported fully agent-written; Claude Code 39% at work. Stack Overflow 2026 survey (30k+, results 6 Oct 2026): agents of choice Claude Code 66%, Copilot 59%.
- Sources: https://blog.jetbrains.com/research/2026/08/ai-coding-agent-adoption-2026/ ("August 18, 2026"); https://blog.jetbrains.com/research/2026/08/how-much-code-do-developers-really-let-agents-write/ ("August 26, 2026"); https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/ (2026-10-06). Survey blog posts read.
- Verbatim: "As of May–July 2026, **90% of professional developers were using AI coding agents at work at least weekly** ... with **68% using them daily**." / "**~47% of their code is fully written by agents**." / "The agents of choice are Claude Code (66%) and GitHub Copilot (59%)."
- Tier: **Verified** (survey facts). Verdict relevance: raises stakes for all principles (agents are now the dominant reader/writer); not direct evidence for any verdict.

---

## Per-principle evidence summary (this lane only)

| P | Verdict from post-June evidence | Key findings | Change vs 2026-10-17 baseline |
|---|---|---|---|
| P1 Naming | AMPLIFIED (indirect) | F-10 (findability is the bottleneck even for Mythos-class) | No direct post-June naming study found; unchanged |
| P2 Small functions/SRP | AMPLIFIED, cohesion caveat confirmed | F-01 (83% tokens, random split doesn't help), F-03, F-12 | Now quantified |
| P3 DRY | AMPLIFIED need, INVERTED default behaviour | F-01, F-04 (+81% duplication) | Now quantified; over-DRY caveat: no new evidence |
| P4 KISS | INVERTED pressure (must be imposed) | F-05 (over-engineering after adversarial review, Mythos era), F-07 | Confirmed for current gen |
| P5 YAGNI | INVERTED pressure | F-05, F-07 (overshoot past minimal impl) | Confirmed; small-steps-YAGNI does not transfer |
| P6 SOLID | STILL-USEFUL → AMPLIFIED when executable | F-13 (dependency-direction fitness functions), F-08 (contracts) | New angle: enforce as architecture tests |
| P7 Error handling | AMPLIFIED + split | F-04 (error-masking +47%), F-05 (over-defensive validation), F-08 (contract-level error codes missed by cheaper model) | New: over-defensiveness is a frontier failure mode |
| P8 Testing/TDD | SPLIT: TDD process MOOT/INVERTED; regression/contract sensors AMPLIFIED; cadence by model tier | F-07, F-08, F-12, F-05 | Sharper than baseline |
| P9 Refactoring | AMPLIFIED, must be human-initiated + metric-gated | F-01, F-02, F-03, F-04 | Economics flipped: agent refactoring cheap when gated |
| P10 Readability | AMPLIFIED (agents copy existing patterns; humans still review) | F-05, F-09, F-11 | Review bottleneck quantified |

---

## Source-universe checklist

- Vendor engineering blogs: Anthropic — covered (F-05/06); OpenAI — searched; Harness engineering post is Feb 11 2026 → excluded (pre-cutoff); Google — searched, nothing on-topic found; GitHub blog — listing fetched, no on-topic post ≥ June found in listing (not exhaustive); Cursor agent-best-practices — undated → excluded; Sourcegraph — covered (F-10); SonarSource — covered (F-09); CodeScene — covered (F-03); JetBrains — covered (F-15); Stripe Minions — Feb/Mar 2026 → excluded; Shopify — covered (F-12).
- Industry reports: GitClear 2026 — covered (summary only, F-04); DORA ROI of AI 2026 — 2026.01 (InfoQ May 2026) → excluded pre-cutoff; Sonar State of Code survey — Jan 2026 → excluded; Stack Overflow 2026 — covered (F-15); JetBrains DevEco 2026 — covered.
- Practitioner long-form: martinfowler.com series — covered (F-01/02/07/08); InfoQ — covered (F-13); monorepo blog — covered (F-14).
- Academic-adjacent (secondary): Harvard/Jellyfish — covered via secondary (F-11).

## Excluded for date (< 2026-06-01) — noted so the collector does not re-add them
- CodeScene "Unhealthy Code is Burning Your Token Usage" (May 28, 2026; 35-45% more tokens on unhealthy code; Qwen3-Coder-30B) — just before cutoff and non-frontier model.
- martinfowler.com "Maintainability sensors for coding agents" (19-27 May 2026).
- Shopify "Under the River" (May 28, 2026).
- OpenAI "Harness engineering" (Feb 11, 2026); Stripe Minions parts 1-2 (Feb-Mar 2026); DORA ROI report (2026.01); Sonar State of Code (Jan 8, 2026); AGENTS.md efficiency/value papers (arXiv 2601.20404, InfoQ Mar 2026); CodeScene AI-Ready Code whitepaper (Jan/Mar 2026); Anthropic engineering posts up to May 25, 2026.

## Searched, found nothing (≥ 2026-06-01, on-target)
- "AI coding agents types TypeScript strict typing study 2026" — only pre-cutoff/blog opinion; no quantified current-gen study on types.
- "AI coding agent code comments documentation provenance study 2026" — provenance *tooling* posts only; no study on comments-as-provenance for agents.
- "Google engineering blog 2026 Jules Gemini agent code health" — product announcements only.
- "GitHub Octoverse 2026 typed languages" — only Octoverse 2025 (pre-cutoff).
- AGENTS.md effectiveness — no post-June primary study found (the ICSE JAWs and ETH studies are early 2026).
- Naming/identifier studies post-June — none found in this lane's source types (belongs to papers lane).

## Open / unverified
- GitClear full PDF (gated) and exact publication date.
- Harvard paper read only via secondary report.
- CodeScene defect/token reductions for the uplifted codebase are projections; Lund follow-up pending.
- Sonar's secondary citations (LinearB, Faros, CMU, New Relic) not read at origin.
