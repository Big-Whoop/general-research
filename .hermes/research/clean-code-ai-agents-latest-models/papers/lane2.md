# Lane 2 — Academic papers dated >= 2026-06-01: code quality x current-gen coding agents

Card: t_18289613 (board general-research). Run date: 2026-10-18.
Note: the full brief file (/opt/data/cache/scratch/research-clean-code-ai-agents-latest-models/lane2.body.md) did not exist at run time; this lane ran from the inline card summary.

Method: arXiv export API (sorted by submittedDate, 6 + 4 abstract queries, filtered to published >= 2026-06-01), web_search, Semantic Scholar citation graph for the six baseline papers, full-text HTML reads (arxiv.org/html) of every load-bearing paper, with a regex scan for the evaluated model names to apply the "current generation" filter.

Date evidence = arXiv `published` (v1) date from the arXiv API. Model evidence = model names found in the paper's own setup section.

Generation filter used. "Current gen (Oct 2026)" = model families visible in post-2026-08 papers: Claude Opus 5 / 5.5, Sonnet 5, GPT-5.6 (Luna/Sol/Terra), DeepSeek V4 / V4.1, GLM-5.x, Qwen3.7, Kimi K2.5, Gemini 3.x. Papers that only test Claude 4.5 Sonnet / GPT-5 / Sonnet 4.6 are flagged OLDER-GEN and capped at Plausible for any claim about today's models.

Tiers: Verified (paper read, claim is in the paper, current-gen models used) / Plausible (paper read, but older-gen models, observational design, or the claim is generalized beyond the setup) / Speculative.

---

## A. Status of the six baseline papers (updates / replications / rebuttals)

A1. arXiv 2605.20049 (SonarSource, "Does Code Cleanliness Affect Coding Agents?") — still v1 only (submitted 2026-05-19); no v2, no replication, no rebuttal found. Only one citing paper in Semantic Scholar (2609.36730, see B4), which cites it as support, not as replication. — Verified (absence)
- URL: https://arxiv.org/abs/2605.20049 (arXiv abs page, submission history) + Semantic Scholar citations API
- Quote: "[v1] Tue, 19 May 2026 16:06:26 UTC (1,094 KB)"
- Date: pre-cutoff; comparison only, not new evidence.

A2. arXiv 2605.02741 ("AI-Generated Smells") — still v1 (2026-05-04); 0 citing papers in Semantic Scholar. — Verified (absence)
- Quote: "[v1] Mon, 4 May 2026 15:41:13 UTC (67 KB)"

A3. arXiv 2512.04273 (Hexagonal architecture erosion, GPT-5.1 / Claude 4.5 Sonnet / Llama 3) — no new version found; now "Under review at the Journal of Systems and Software (Special Issue on Impactful Software Architecture)". 0 citing papers in Semantic Scholar. — Verified (status), no new evidence.

A4. arXiv 2606.14796 (multivocal review on LLM technical debt) — now "Accepted for publication in ACM Transactions on Software Engineering and Methodology (TOSEM), 2026". Venue change only; content is a literature review, not a current-gen measurement. — Verified (status)

A5. arXiv 2603.03823 (SWE-CI) — latest version v4 updated 2026-04-01 (pre-cutoff); no post-cutoff version. But it is the most-cited baseline: 18 citing papers dated >= 2026-06-01 (incl. B1, B2, StaminaBench 2606.19613, SWE-Journey 2610.11559, SWE Refactor Bench 2608.23564, "Needle in the Repo" ASE 2026, WEAVE 2610.22039). These are follow-ups in the same "maintainability over time" paradigm, not replications of SWE-CI numbers. — Verified
- Quote (arXiv API): `<updated>2026-04-01` for 2603.03823v4.

A6. arXiv 2602.07900 ("Rethinking the Value of Agent-Generated Tests") — no new version, 0 citing papers in Semantic Scholar. Closest post-cutoff related work: 2607.12068 (B15) and 2610.14629 (MockBench, 2026-10-10: agent mocks executable but often behavior-unfaithful; not expanded). — Verified (absence)

A7. Venue update for a pre-cutoff paper: "Needle in the Repo" (arXiv 2603.27745, v1 2026-03-29) now appears in the Proceedings of ASE 2026 (doi 10.1145/3832783.3834401). Its models include Claude Opus 4.6, GPT-5.3/5.4, Gemini 3.1 Pro. arXiv date is pre-cutoff, so it is listed for context only, not as new evidence. — Plausible (borderline date; ACM page blocked by cookie wall, venue taken from search snippet)
- Quote (arXiv HTML): "64/483 outcomes (13.3%) pass all functional tests yet fail the structural oracle. Under our harness, agent-mode configurations improve average performance from 28.2% to 45.0%, but does not eliminate the architectural failures."

---

## B. New papers (published >= 2026-06-01)

### Agent-written code as the substrate for later agent work (P9 refactoring, P10 maintainability, P8 tests)

B1. Building on an agent's own earlier changes lowers later-task resolution by 5.6 points on average (14.0 points if earlier tests must also pass). The cost comes mostly from inherited test failures: when the inherited code still passes earlier tests, the disadvantage goes away. — Verified (current gen: GPT-5.6-Luna, DeepSeek-V4-Flash; 5 coding systems incl. Claude Code)
- URL: https://arxiv.org/abs/2610.14768 (arXiv preprint, SWE-Maintain), published 2026-10-10
- Quote: "Across five coding systems, two backbone models, and 1,996 paired later events, Agent-History reduces later-task resolution by 5.6 percentage points on average. When success additionally requires all earlier tests to pass, the gap reaches 14.0 points. ... When the inherited code passes earlier tests and the next task is not already solved, the disadvantage disappears (+2.7 points; 95% CI [-0.5, +6.1]). These findings suggest that the main downstream cost of agent-written changes lies in inherited test failures rather than a measurable maintenance disadvantage in code that preserves earlier tested behavior."
- Model quote: "We evaluate all applicable approaches with two backbone models, GPT-5.6-Luna and DeepSeek-V4-Flash-0731"
- Bearing: P8 (a regression suite you can run is the main protection), and a nuance for P10: once behavior is preserved, no extra structural maintainability penalty was measurable.

B2. CodeThread: agents resolve up to 13.1% fewer tasks when they build on agent-written code than on human-written code. Traditional maintainability metrics do NOT explain the gap. The clearest predictors are input-validation and error-handling changes, plus code size. — Plausible (OLDER-GEN: Claude 4.5 Sonnet, GPT-5, GLM 4.7, MiniMax M2.5; date fits)
- URL: https://arxiv.org/abs/2606.21804 (arXiv preprint), published 2026-06-19
- Quote: "agents are less effective at resolving tasks when building on agent code compared to human code, with task resolve rate drops of up to 13.1%. Regression analysis reveals that many traditional software engineering maintainability metrics do not explain this difference. Instead, the clearest signals are subtler behavioral differences in agent code, such as changes to input validation and error handling, along with differences in downstream code size and task difficulty."
- Model quote: "we evaluate four frontier models: Claude 4.5 Sonnet, GPT-5, GLM 4.7 and MiniMax M2.5"
- Bearing: P7 error handling (strengthened as a causal signal), and a caution on P10 metric-based "cleanliness".

B3. RepoReuse: over multiple turns, agents gradually stop exploring existing repository code and reuse their own earlier work less. By turn 5, 50.8% of task chains contain duplicated logic, while pass rates barely change. — Verified (current gen: GPT-5.6 Terra, DeepSeek-v4.1-flash, Qwen3.7-plus, GLM-5.3; mini-SWE-agent + OpenCode)
- URL: https://arxiv.org/abs/2609.35357 (arXiv preprint, "Work In Progress"), published 2026-09-28
- Quote: "agents progressively stop exploring relevant repository code, reuse their own history less even when it is fully in the workspace, and leave duplicated logic in 50.8% of task chains by turn 5—all while pass rates barely move."
- Model quote: "four backbone models: GPT-5.6 Terra ..., DeepSeek-v4.1-flash ..., Qwen3.7-plus ..., and GLM-5.3"
- Bearing: P3 DRY is AMPLIFIED, and the agent's default is to duplicate. That makes it an agent-violated principle that has to be enforced from outside.

B4. LibraryDesignBench: current-gen designers (Opus 5.5 scores highest) reproduce the production-library abstractions in 11 of 15 tasks. But downstream agents still reimplement features the library already provides, mostly because the interfaces are "rigid or hard to use" (64% of audited excess-code cases), not because features are missing (14%). Agent-first design guidance plus subagent testing improves reuse. — Verified (current gen: Opus 5.5, GPT-5.6, DeepSeek V4.x, GLM-5)
- URL: https://arxiv.org/abs/2609.36730 (arXiv preprint, code at github.com/SprocketLab/librarydesignbench), published 2026-09-29
- Quote: "Opus 5.5 scores highest (48.9), 2.3 points above the production library. In eleven of fifteen tasks, designers reproduce production-library abstractions. Our audit classifies 64% of sampled excess-code cases under rigid or hard-to-use interfaces, and only 14% under missing capabilities."
- Quote: "downstream agents write extra code mainly because agent-written libraries are rigid or hard to use, not because capabilities are missing."
- Also the only post-cutoff paper citing 2605.20049, as support: "agents spend more tokens and revisit more files on code that scores high on it and violates more static-analysis rules (Trivedi & Schmitt, 2026)".
- Bearing: P6 SOLID / interface design is AMPLIFIED (consumer-friendly interfaces drive reuse). Supports the baseline's "agents are weak at interface design" with current-gen data, while frontier designers now match production abstractions.

B5. TRIM: agent code is more verbose than human code because speculative and abandoned edits from the search process stay in the final patch ("CodeSlop"). Trajectory minimization cuts CodeSlop by 17.9–32.9% with negligible performance regression. — Plausible (mixed gen: Gemini-3-Flash/Pro, Claude Sonnet 4.6, Opus 4.5; not Opus 5 / GPT-5.6)
- URL: https://arxiv.org/abs/2607.18161 (arXiv preprint), published 2026-07-20
- Quote: "while iterating toward a passing solution, an agent accumulates speculative edits, abandoned hypotheses, and temporary changes that persist into the final patch. ... a codebase that was once minimal and well-maintained slowly accumulates redundancy faster than it can be cleaned up ... TRIM cuts CodeSlop by 17.9%-32.9% across agentic scaffolds, with negligible performance regression."
- Bearing: P4 KISS / P5 YAGNI INVERTED pressure (bloat is the default), and P9 (a separate cleanup pass is needed and can be automated).

### Codebase quality as an input to the agent (P1, P2, P10)

B6. CodeScene CodeHealth is a "weak but consistent" signal of how effective LLM-generated tests are, and is negatively correlated with input-token count (healthier code means fewer tokens). — Plausible (peer-reviewed, SCAM 2026 Engineering Track; models: Claude Sonnet 4.6 tokenizer, Qwen3-Coder-30B, GPT-4o, so older/mid-gen; test generation, not full agent tasks)
- URL: https://arxiv.org/abs/2608.18645 (arXiv + SCAM 2026 acceptance), published 2026-08-19
- Quote: "Our results suggest that CH provides a weak but consistent signal of LLM-generated test effectiveness and is negatively correlated with input-token count. These findings provide further evidence for a relationship between maintainability and LLM-based software development."
- Bearing: replicates, from an independent vendor (CodeScene vs SonarSource), the direction of 2605.20049: clean code saves tokens, with a small effect on outcome.

B7. Name-only directory routing (an LM follows directory and file names) recovers 0.465 of gold files within 8 candidates, vs 0.352 for FTS5 and 0.245 for an `rg` query. The authors say this cannot be attributed to hierarchy and is not shown to improve resolution. — Plausible (model not named in text; observational retrieval study)
- URL: https://arxiv.org/abs/2609.35918 (arXiv preprint), published 2026-09-28
- Quote: "name-only directory routing recovered 0.465 of gold files within eight candidates, compared with 0.352 for FTS5 and 0.245 for a fixed full-issue rg query. ... the study cannot attribute the gain to hierarchy or show that it improves issue resolution."
- Bearing: P1 naming (descriptive file/directory names are a navigation signal), consistent with the baseline's AMPLIFIED verdict.

B8. "Architecture as Capability Equalizer": on the strongest models tested (Sonnet 4.6, GPT-5), the format of the architecture spec "barely matters". On weaker models, code-proximate formats (OpenAPI, TypeScript contracts plus ArchUnit-style rules) recover most of the capability gap. — Plausible (models one generation behind; 90 trials, small sample)
- URL: https://arxiv.org/abs/2608.21747 (arXiv preprint), published 2026-08-22
- Quote: "On the strongest models (Sonnet 4.6, GPT-5), format barely matters (quality spread 0.17-0.92). On weaker models, format produces spreads of 0.83-2.42 points ... Structured architecture specifications serve as a capability equalizer, with value inversely proportional to model strength and the largest returns for cost-optimized deployments."
- Bearing: a possible MOOT trend for frontier models on explicit architecture formatting. The value of structure goes down as model strength goes up. This is a candidate verdict shift; check it against the other lanes.

B9. Code-of-Theseus: giving a coding agent recovered requirements and architecture does not change the held-out pass rate (33.7% vs 35.8%), but brings the rebuilt module structure significantly closer to the original (module F1 0.54 → 0.63). — Plausible (model: Qwen3.5-122B generator; agent model not current-frontier)
- URL: https://arxiv.org/abs/2610.20068 (arXiv preprint), published 2026-10-14
- Quote: "The artefacts do not significantly change the held-out pass rate (33.7% vs. 35.8%), but bring the rebuilt module structure significantly closer to the original (module F1 from 0.54 to 0.63)"
- Bearing: same pattern as 2605.20049 and B6: structure and design inputs shape how the code is built, not pass/fail. Tests cannot see it.

B10. Architecture lever experiment: an agent implements 60 accumulating change requests under a mutative (Spring controller) vs an additive (OfficeFloor pipeline) architecture. The amount of complexity is roughly conserved; where it lands depends on the architecture. Prompts move only the mutative architecture; an AI reviewer is the only lever that moves the additive one. — Plausible (model fixed but not named in the extracted text; single endpoint, single model)
- URL: https://arxiv.org/abs/2610.14130 (arXiv preprint, Zenodo archive), published 2026-10-09
- Quote: "Across all ten cells the finished complexity varies by 7% to 20% over four operationalisations ... Under the four external controls the plasticity ratio between the architectures is near 1 on six amount metrics ... against 2.7 to 10.0 on eleven placement metrics ... The AI reviewer is the one lever that moves the additive arm ... Strict correctness fell in most comparisons"
- Bearing: P6/P2 (architecture choice decides where agent-added complexity lands). Agent review as a lever matches the baseline's "enforce, don't prompt".

### Agent-written code quality in the wild (MSR studies)

B11. Committed AI configuration (rules files, coding standards) correlates with a smaller quality decline after agent adoption. Agent-first repos without it show roughly twice the cognitive-complexity increase (+53% vs +27%) and 1.7x the static-warning increase. The authors call this hypothesis-generating. — Plausible (observational, 441 repos, model-agnostic)
- URL: https://arxiv.org/abs/2608.25241 (arXiv preprint, v2 2026-09-14), published 2026-08-26
- Quote: "agents accelerate development regardless of maturity (28-38% more commits), but quality diverges: among agent-first repositories ... those without committed AI configuration show roughly twice the increase in cognitive complexity (+53% versus +27%) and 1.7x the increase in static-analysis warnings. Because maturity is observational, correlated engineering discipline or model capability may explain part of the gap"
- Bearing: supports the baseline's Option 2 (encode rules in an instruction file) with field data. Contrast with baseline [15] "don't restate write-clean-code".

B12. Post-merge fate, 182 repos: agentic contributions need significantly more corrective maintenance and bring in more security and dependency weaknesses. A 10-point rise in a project's no-review rate is associated with ~6% more agentic maintenance burden. — Plausible (observational; agent-tool mix, model generation not controlled)
- URL: https://arxiv.org/abs/2607.09902 (arXiv preprint), published 2026-07-10
- Quote: "While the overall maintenance rates are similar, agentic contributions require significantly higher rates of corrective maintenance ... each 10 percentage-point increase in a project's no-review rate is associated with roughly a 6% increase in agentic maintenance burden on average."

B13. Merged agent PRs get verified fixes at 1.62x the odds of human PRs in the same repos; 69.6% of those fixes come from the same agent. — Plausible (AIDev-pop data; PRs date from older generations)
- URL: https://arxiv.org/abs/2609.26847 (arXiv preprint), published 2026-09-22
- Quote: "merged agent PRs attract verified fixes at 1.62 times the odds of merged human PRs ... 69.6% of verified fixes in agent merges come from the same agent"

B14. Vendor-specific, not uniform: Codex PRs were reverted about half as often as human PRs (6.1% vs 11.5%), Devin PRs more often (14.5%). Pooled agent code was less likely to contain a security smell (OR 0.63). — Plausible (data Dec 2024–Jul 2025, so OLDER-GEN agents; published 2026-09-12)
- URL: https://arxiv.org/abs/2609.17598 (arXiv preprint)
- Quote: "Codex-authored PRs were reverted about half as often as human PRs (6.1% vs. 11.5%, odds ratio 0.50), while Devin PRs were reverted more often (14.5%, odds ratio 1.31). Second, agent code pooled across vendors was less likely than human code to contain a security smell (odds ratio 0.63)"
- Bearing: a counterpoint to the "agent code is uniformly worse" framing. The dataset predates the current generation.

### Tests and conventions (P8, P10)

B15. Agent-generated tests (179,732 files, AIDev) cover more edge cases than human tests (variety 0.62 vs 0.32) but have slightly weaker assertions (85.37% vs 88.1% strong) and a higher flakiness risk (0.41 vs 0.30). — Plausible (observational; mixed/older-gen agents)
- URL: https://arxiv.org/abs/2607.12068 (arXiv preprint), published 2026-07-13
- Quote: "AI agents performed better than humans in Edge-Case Coverage, with almost twice the variety of boundary checks (Variety Score: 0.62 vs 0.32) ... human developers had a slight advantage in Assertion Strength (88.1% strong assertions vs. 85.37% for agents) ... agent-generated tests exhibited a higher risk of flakiness (Candidate Rate: 0.41 vs. 0.30)."
- Bearing: refines baseline 2602.07900 ("agent tests mostly observational"). In committed PR tests, agents are thorough on edge cases but weaker on hermeticity.

B16. SWE-CC: even when their patches are functionally correct, current-gen agents violate 43.1% of applicable repository policies (style, git, testing workflow). Nearly half of the violations happen during intermediate steps. — Verified (current gen: GPT-5.6 Luna, Gemini 3.7 Flash, DeepSeek V4 Flash, Kimi K2.5; 500 tasks)
- URL: https://arxiv.org/abs/2610.06193 (arXiv preprint, benchmark at github.com/dangtruong01/swe-cc-arxiv), published 2026-10-05
- Quote: "although agents produce functionally correct patches, they still violate 43.1% of applicable project policies, with nearly half of all violations occurring during intermediate execution steps."
- Bearing: P10 conventions are NOT moot, because current-gen agents do not follow written repository conventions by themselves. Supports mechanical enforcement (Option 3).

B17. RepoNorm: mining repository norms (including implicit ones, from Git history) and passing them to agents raises the norm-compliance rate by 7.4–10.8% relative overall and 31.6–45.4% for contribution norms. Functional gains (+5.8–9.1 pp) are not significant. — Plausible (models include GPT-5.6, DeepSeek V4.x, Gemini 3.1 Flash; tool paper by the authors)
- URL: https://arxiv.org/abs/2610.07757 (arXiv preprint), published 2026-10-06
- Quote: "relative improvements are 7.42-10.77% for Overall Norm Compliance Rate (NCR), 31.64-45.44% for Contribution NCR ... Functional success rates show observed gains of 5.79-9.09 percentage points over Raw; the paired comparisons do not reach the significance threshold."

B18. SmellBench: the best agent+model pair (Qwen Code + Claude Sonnet 4.5) reaches only 50.34 on smell elimination. The weakness is cross-file understanding: agents handle local smells and miss non-local ones. — Plausible (OLDER-GEN)
- URL: https://arxiv.org/abs/2606.05574 (arXiv preprint), published 2026-06-04
- Quote: "the best combination - Qwen Code + Claude Sonnet 4.5 - achieved only a 50.34 score of smell elimination. Further analysis reveals that this gap arises from a focus on local code smells and a lack of cross-file understanding"
- Bearing: matches the SWE-CI baseline observation ("local conventions yes, global quality no").

### Harness / tooling vs code (context for the dichotomy)

B19. Tool architecture, with capabilities held equal, changes agent behavior a lot: CodeAct-style interfaces reach similar task performance with 41.6% fewer steps and 56.3% fewer tokens. — Plausible (Qwen3Coder-30B, Kimi-K2.5, Sonnet-4.5; harness-side, not code-side)
- URL: https://arxiv.org/abs/2608.11386 (arXiv preprint), published 2026-08-11
- Quote: "Python CodeAct-style interfaces achieve similar task performance with 41.6% fewer steps and 56.3% lower token usage."
- Bearing: the effect sizes for harness efficiency are larger than 2605.20049's 7–8% token saving from clean code. Clean code is one cost factor among several.

B20. StaminaBench: in 100-turn change-request sessions, every tested open model fails within 5–6 turns without test feedback. Passing test feedback back to the agent improves the passed-turn count by up to 12x. — Plausible (open models GLM-5, Kimi K2.5, Qwen3.5; no closed frontier models in main runs)
- URL: https://arxiv.org/abs/2606.19613 (arXiv preprint, Amazon Science), published 2026-06-17
- Quote: "all the tested models fail within 5-6 turns, confirming that vibe-coding-style programming without thorough testing produces bugs; (2) passing test feedback back to the agent and allowing it to retry improves passed turn count by up to 12x"
- Bearing: P8 AMPLIFIED (runnable tests are the central safety mechanism). Same direction as B1.

### Registered / announced, no results yet

B21. ESEM 2026 registered report (2609.04208): a planned comparison of agent implementations vs real commits over 628k issues (technical debt, evolution across releases). No results yet. — Speculative (protocol only)
- URL: https://arxiv.org/abs/2609.04208, published 2026-06-06; comment "ACCEPTED REGISTERED REPORT AT ESEM (CORE A*) 2026"

---

## C. Cross-cutting synthesis for the collector (lane-level, not final)

- Convergent post-cutoff pattern (B1, B6, B9, B10, plus baseline 2605.20049): code quality and structure change cost, navigation, and the structure of what the agent builds, much more than they change pass rates. Pass/fail benchmarks systematically underestimate quality effects (B3, B16, NITR A7).
- New current-gen evidence for agent-default violations: DRY (B3, 50.8% duplication by turn 5), conventions (B16, 43.1% policy violations), bloat (B5). These strengthen the baseline's "INVERTED pressure / must be enforced" framing.
- New nuance: once earlier tested behavior is preserved, building on agent code showed no measurable extra maintenance penalty (B1). The damage runs through broken regressions, so P8 carries more weight than metric-level cleanliness (also B2: traditional maintainability metrics do not explain the gap).
- Possible MOOT drift for frontier models: the format and structure of explicit architecture specs matters less as models get stronger (B8, older-gen frontier). Treat this as a hypothesis; there is no Opus 5 / GPT-5.6 replication.
- No paper found that replicates 2605.20049 on Opus 5.x / GPT-5.6. The core "clean code → fewer tokens, same pass rate" claim rests on Claude Code (May 2026) plus the independent direction from CodeScene (B6, Sonnet 4.6 tokenizer).

## D. Searched, found nothing (evidence of absence)

- arXiv: v2+ of 2605.20049, 2605.02741, 2602.07900 → none (abs pages show v1 only).
- Semantic Scholar citations: 2605.02741, 2512.04273, 2606.14796, 2602.07900 → 0 citing papers each; 2605.20049 → 1 (supportive, B4).
- arXiv abs queries (published >= 2026-06-01): "coding agent" AND identifier/naming/type annotations/static typing → no paper isolating naming or typing effects on current-gen agents (only B7 for directory names).
- arXiv: "over-engineering" AND LLM; "cognitive complexity" AND agent → no current-gen controlled study beyond B11 (observational).
- web_search: SonarSource follow-up / replication of code cleanliness on Opus 5 / GPT-5.6 → only blog coverage of the original (developersdigest, HN), no new study.
- No controlled study found that varies comment density or comment quality for current-gen agents (P10 comments sub-verdict stays without post-cutoff evidence).
- Not covered: Google Scholar and the Papers with Code UI (arXiv API + Semantic Scholar were used instead); ICSE/FSE 2027 proceedings are not yet published. ACM DL page for ASE 2026 was blocked by a cookie wall (A7 venue unconfirmed directly).
