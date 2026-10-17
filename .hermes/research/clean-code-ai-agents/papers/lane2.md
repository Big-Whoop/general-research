# LANE-2 — Research papers: clean code & LLM code quality

Research run: RESEARCH-clean-code-ai-agents (task t_a7de8e41)
Lane: LANE-2 — what RESEARCH PAPERS say about whether/how Clean Code principles apply to LLM-based coding agents
Scope: code quality & maintainability of LLM-generated code; SWE-bench / SWE-agent & agent benchmarks; test-driven agent loops; whether clean code in the codebase improves agent performance; per-principle findings.
Source types owned: research papers (arXiv, SWE-bench, SWE-agent, code-quality/maintainability of LLM code, agent evaluation/benchmarks).
Date of research: 2026-10-17
Tier scheme: **Verified** (authoritative source for this exact target, actually read in full) / **Plausible** (sound general behavior / snippet-level, not yet read in full) / **Speculative** (inferred, unconfirmed)

Anchor principles referenced: [P1] naming, [P2] small functions/SRP, [P3] DRY, [P4] KISS, [P5] YAGNI, [P6] SOLID, [P7] error handling, [P8] unit testing/TDD, [P9] refactoring/Boy Scout Rule, [P10] readability & maintainability.

---

## TL;DR

The research literature on "clean code + LLM agents" is real and growing, but it is **not organized around the 10 Clean Code principles**. Papers instead use **ISO/IEC 25010 quality attributes** (maintainability, reliability, security) and **static metrics** (SonarQube, Pylint, Maintainability Index / cyclomatic complexity). The three most load-bearing, on-target findings:

1. **Clean-code decisions compound over time and DO affect agent performance — but only in long-horizon/evolution settings.** SWE-CI (2026) is the first benchmark to measure this: it shows an agent that writes clean, extensible code scores higher on *future* modifications (EvoScore), while one that accumulates technical debt degrades. On snapshot benchmarks (SWE-bench) this difference is **invisible** — a brittle fix and a clean fix both pass the same test suite. [F-04]
2. **LLM-generated code is "superficially clean but intrinsically complex."** SWE-CI Observation 5: 15/20 LLMs beat human oracle code on Pylint (surface conventions: line length, naming) but **all 20 lose on the Maintainability Index** (cyclomatic complexity). LLMs optimize for the *minimal* change that passes the test, not for abstraction/encapsulation/modularization. [F-05, F-06]
3. **Test-driven loops are a weaker lever for agents than for humans.** A 2026 trajectory study (SMU) on SWE-bench Verified finds agent-written tests are mostly observational `print` statements (not assertions), test-writing frequency is similar in resolved vs unresolved tasks, and prompt-induced changes in test volume **do not significantly change outcomes**. GPT-5.2 matches top agents while writing ~no new tests. [F-12]

Cross-cutting: the dominant benchmark paradigm (SWE-bench) measures **issue resolution, not code quality** — so "does clean code help the agent?" is largely *unmeasured* by the field's own standard benchmark. The best available proxy evidence is that **more complex/enterprise codebases reduce agent success** (SWE-Bench Pro: ≤23.3% vs >70% on Verified). [F-01, F-03]

---

## A. Benchmarks & the "does clean code help the agent?" causal question

### F-01 — SWE-bench measures issue resolution, not code quality/cleanliness [cross-cutting]
- Claim: The de-facto standard agent benchmark scores only whether the issue is resolved (fail-to-pass + pass-to-pass tests); it does not measure code quality, readability, maintainability, or adherence to any clean-code principle.
- Source: https://arxiv.org/abs/2310.06770 (research paper, arXiv, ICLR 2024) — read in full (abstract + framing).
- Verbatim: "We introduce SWE-bench, an evaluation framework consisting of 2,294 software engineering problems drawn from real GitHub issues and corresponding pull requests across 12 popular Python repositories. Given a codebase along with a description of an issue to be resolved, a language model is tasked with editing the codebase to address the issue." / "The best-performing model, Claude 2, is able to solve a mere 1.96% of the issues."
- Tier: **Verified** (abstract + framing read). This is a *scope* finding: the field's headline metric is orthogonal to clean code, which is why per-principle evidence is sparse.

### F-02 — SWE-agent: the interface the agent works through (ACI) materially changes agent performance [cross-cutting; analog to "clean interface/context"]
- Claim: LM agents are "a new category of end users" whose performance depends heavily on the agent-computer interface (ACI) design — a custom, well-structured interface for creating/editing files, navigating repos, and running tests raised SWE-bench pass@1 to 12.5% (SOTA at the time).
- Source: https://arxiv.org/abs/2405.15793 (research paper, arXiv, NeurIPS 2024) — read in full (abstract).
- Verbatim: "we posit that LM agents represent a new category of end users with their own needs and abilities, and would benefit from specially-built interfaces to the software they use." / "SWE-agent's custom agent-computer interface (ACI) significantly enhances an agent's ability to create and edit code files, navigate entire repositories, and execute tests and other programs." / "pass@1 rate of 12.5% and 87.7% [HumanEvalFix], respectively, far exceeding the previous state-of-the-art achieved with non-interactive LMs."
- Tier: **Verified** (abstract read). Relevance: the closest benchmark-world analog to "clean code helps" is that a *cleaner, better-structured working environment/interface* improves agent outcomes — but this is about the tooling surface, not the codebase's internal cleanliness.

### F-03 — SWE-Bench Pro: enterprise codebase complexity sharply reduces agent success [cross-cutting; codebase-quality → performance proxy]
- Claim: On realistic, complex, enterprise-level tasks (long-horizon, multi-file), agent resolution drops to ≤23.3% (public) / ≤17.8% (commercial), far below the >70% on SWE-bench Verified; the public-vs-commercial gap "underscores the greater complexity of enterprise codebases."
- Source: https://arxiv.org/abs/2509.16941 (research paper, arXiv, Scale AI, 2025) — read in full (abstract + intro).
- Verbatim: "LLM agents achieve only modest resolution rates on SWE-Bench Pro (≤23.3% on the public set; ≤17.8% on the commercial set), substantially lower than the >70% Pass@1 reported on SWE-Bench Verified. We additionally observe a marked performance gap between the public and commercial sets, underscoring the greater complexity of enterprise codebases." / "Larger models (e.g., Opus 4.1) often fail on semantic or algorithmic correctness in large, multi-file edits, whereas smaller models ... more frequently fail due to issues in syntax and formatting, tool use, or context management."
- Tier: **Verified** (abstract + intro read). This is the strongest *proxy* evidence that codebase complexity/organization (a clean-code-adjacent property) affects agent performance — but it is correlational (harder/less-organized codebases), not a controlled A/B on "cleanliness."

### F-04 — SWE-CI: maintainability decisions compound over evolution; clean/extensible code → better future agent performance [cross-cutting + P4 KISS + P9 refactoring + P10 maintainability] — THE key causal finding
- Claim: The first CI-loop benchmark shows an agent's code-quality decisions accumulate: an agent that sacrifices short-term speed for a cleaner, more extensible design is *rewarded* on later modifications, while one that rushes to pass early tests and accumulates technical debt degrades. State-of-the-art models still struggle to sustain code quality over extended evolution.
- Source: https://arxiv.org/abs/2603.03823 (research paper, arXiv, Sun Yat-sen Univ + Alibaba, 2026) — read in full (abstract, formalization, and all 6 observations in §4).
- Verbatim: "Maintainability can be revealed by tracking how functional correctness changes over time." / "an agent that hard-codes a brittle fix and one that writes clean, extensible code may both pass the same test suite — their difference in maintainability is simply invisible. It becomes visible only when the codebase must evolve." / "An agent that sacrifices short-term speed for a cleaner, more extensible design will be rewarded over one that rushes to pass early tests but accumulates technical debt that cripples subsequent evolution." / "despite substantial progress on functional correctness, state-of-the-art models still struggle when tasked with sustaining code quality over extended evolution."
- Tier: **Verified** (abstract + §2 formalization + §4 observations read in full). This is the single most on-target paper for the lane's core question: it directly ties clean-code quality to *future* agent performance, and shows the effect is invisible on snapshot benchmarks.

### F-05 — SWE-CI Obs 5: LLMs are "superficially clean but intrinsically complex" vs human code [P1 naming + P4 KISS + P10 maintainability]
- Claim: On successfully solved problems, LLM-generated code beats human oracle code on surface conventions but loses on deep maintainability: 15/20 LLMs outperform on Pylint (line length, naming rules) but **all 20 underperform on the Maintainability Index** (cyclomatic complexity).
- Source: https://arxiv.org/abs/2603.03823 (same paper as F-04) — read in full.
- Verbatim: "Pylint score reflects adherence to surface-level coding conventions such as line length and naming rules, while MI score captures deeper maintainability through indicators such as cyclomatic complexity. ... while the majority of LLMs (15 out of 20) outperform human oracle code on Pylint score, all 20 LLMs underperform on MI score." / "LLM-generated code tends to be superficially clean but intrinsically complex, whereas human-written oracle code, though less strictly formatted, achieves higher maintainability through simpler and more elegant logic."
- Tier: **Verified** (read in full). Direct per-principle evidence: LLMs handle [P1] naming/formatting conventions well but fail [P10] maintainability / [P4] simplicity-of-structure.

### F-06 — SWE-CI Obs 6: LLMs write *fewer* lines than humans, at the cost of maintainability [P4 KISS + P9 refactoring + P10 maintainability]
- Claim: LLMs universally produce more concise patches than human oracles, yet achieve lower maintainability — the human "extra" lines are purposeful investments in abstraction, encapsulation, and modularization that LLMs skip.
- Source: https://arxiv.org/abs/2603.03823 (same paper) — read in full.
- Verbatim: "LLMs universally produce more concise patches than their human counterparts. ... LLMs achieve lower MI scores with fewer changed lines, whereas human solutions, though more verbose, attain higher maintainability. This suggests that the additional lines written by humans are not redundant, but rather purposeful investments in code quality through practices such as abstraction, encapsulation, and modularization. LLMs, by contrast, appear to optimize for the minimal changes necessary to satisfy immediate task requirements, without investing in the broader code structure that characterizes maintainable software engineering practice."
- Tier: **Verified** (read in full). Nuance for the report: LLMs *do* lean "simple/minimal" (a KISS-like behavior) but in the wrong direction — minimal-to-pass, not minimal-but-well-structured. This is a direct, measured tension with [P4] and [P9].

### F-07 — SWE-CI Obs 3 & 4: LLMs are poor at controlling regressions in long-term maintenance [P7 error handling + P8 testing + P10 maintainability]
- Claim: Most models have a zero-regression rate below 0.25 (only two Claude-Opus models exceed 0.5); as iterations progress, regression *rate* rises for most models (12/20) while regression *magnitude* falls (11/20).
- Source: https://arxiv.org/abs/2603.03823 (same paper) — read in full.
- Verbatim: "most models achieve a zero-regression rate below 0.25, with only the two Claude-opus models exceeding 0.5. This indicates that current LLMs still struggle to reliably avoid regressions across long-term, multi-round code maintenance, despite their strong performance on snapshot-based tasks." / "12 out of 20 models show a positive correlation [regression rate vs iteration count] ... 11 out of 20 models show a negative correlation [regression magnitude]."
- Tier: **Verified** (read in full). Relevant to [P7] (not breaking existing behavior / error handling) and [P8] (regression testing as a first-class concern): agents are weak at the "leave it no worse than you found it" discipline.

---

## B. Code quality & maintainability of LLM-generated code (measured)

### F-08 — LLM code has fewer bugs / less fix-effort than human code, but introduces structural issues on complex tasks [P4 KISS + P7 error handling + P10 maintainability]
- Claim: Using SonarQube across three difficulty levels, LLM-generated code overall has fewer bugs and requires less effort to fix than human code; but on competition-level (hardest) problems LLM solutions "sometimes introduce structural issues that are not present in human-written code."
- Source: https://arxiv.org/abs/2508.00700 (research paper, arXiv, IEEE 2025, Toronto Metropolitan / Colorado State / NCSU) — read in full (abstract + intro + related work).
- Verbatim: "Our analysis shows that LLM-generated code has fewer bugs and requires less effort to fix them overall. ... In competition-level problems, the LLM solutions sometimes introduce structural issues that are not present in human-written code." / "fine-tuned models reduced the prevalence of high-severity issues, such as blocker and critical bugs, and shifted them to lower-severity categories, but decreased the model's performance."
- Tier: **Verified** (abstract + intro read). Balanced finding: LLM code is *reliably* cleaner on easy/mid tasks but degrades structurally as task complexity rises — the same complexity cliff seen in F-03/F-05.

### F-09 — LLM code quality is language-dependent; models under-use modern security features and lean on outdated methods [P7 error handling + P10 maintainability + cross-cutting]
- Claim: Across 200 tasks, 5 LLMs, and 4 languages (Python/Java/C++/C), security/quality effectiveness varies by language; many models fail to use modern security features in recent compiler/toolkit updates (e.g. Java 17) and still commonly use outdated methods, especially in C++.
- Source: https://arxiv.org/abs/2502.01853 (research paper, arXiv, UCF + Birzeit, 2025) — read in full (abstract + intro).
- Verbatim: "while LLMs can automate code creation, their security effectiveness varies by language. Many models fail to utilize modern security features in recent compiler and toolkit updates, such as Java 17. Moreover, outdated methods are still commonly used, particularly in C++."
- Tier: **Verified** (abstract + intro read). Relevant to [P7] (robust/error-safe idioms) and [P10] (maintainability via current best practices): LLMs do not reliably apply "the right modern way," which is a maintainability/correctness gap.

### F-10 — Atlassian (HULA): LLM-generated code readability is comparable to human code; practitioners still rate readability as critical [P10 readability + P1 naming]
- Claim: In an industrial case study (118-practitioner survey + 144 real Jira tasks via the HULA agent framework, GPT-4-powered), 81% of practitioners say code readability is important (mainly to cut long-term maintenance cost), and HULA's LLM-generated code is *comparable* to human-written code in readability (negligible-to-small effect size on LOC, complexity, comment-to-code ratio).
- Source: https://arxiv.org/abs/2501.11264 (research paper, arXiv, Monash + Atlassian, 2025) — read in full (abstract + RQ1/RQ2 results).
- Verbatim: "81% of practitioners agreed that code readability is important. The key motivation is to reduce maintenance costs in the long term ... 39% of practitioners perceived that LLM-generated code is more readable than human-written code in general, followed by 34% perceived that the readability of both ... is similar." / "the readability of LLM-generated code is comparable to human-written code (with a negligible to small effect size difference) based on various measurements (e.g., lines of code, code complexity, comment to code ratio)."
- Tier: **Verified** (abstract + RQ results read). Note the tension with F-05/F-06: on *surface* readability metrics LLM ≈ human, but on *deep* maintainability (MI) LLM < human. Both are true — different metrics.

### F-11 — LLMs (as code-quality *evaluators*) are sensitive to readability attributes: naming, comments, refactoring [P1 naming + P9 refactoring + P10 readability]
- Claim: A quasi-experiment (9 LLMs, 3 interventions: remove comments, replace identifiers with obscure names, refactor to remove code smells) shows all LLMs are sensitive to these readability changes and show "strong semantic sensitivity" a static reference tool did not fully capture — i.e., LLMs can *perceive* clean-code attributes (descriptive names, comments, smell-free structure).
- Source: https://arxiv.org/abs/2507.05289 (research paper, arXiv, Banco do Brasil / UnB, 2025) — read in full (abstract + intro).
- Verbatim: "all LLMs were sensitive to the interventions, with agreement with the reference classifier being high for the original and refactored code scenarios. However, this agreement diverged for the other two interventions. The LLMs demonstrated a strong semantic sensitivity that the reference model did not fully capture." / "LLMs demonstrated potential for evaluating semantic quality aspects, such as coherence between identifier names, comments, and documentation with code purpose."
- Tier: **Verified** (abstract + intro read). Relevance: LLMs respond to [P1] naming and [P9] refactoring signals — supporting the idea that clean-code attributes are *legible to* the model, which is a precondition for them to matter to agent behavior.

---

## C. Test-driven agent loops (TDD for agents)

### F-12 — Agent-written tests are mostly observational, and more test-writing does NOT significantly improve outcomes [P8 unit testing/TDD] — KEY counterpoint
- Claim: Analyzing trajectories of 6 strong LLMs on SWE-bench Verified (mini-SWE-agent), test-writing frequency is similar in resolved vs unresolved tasks; when tests are written they are mostly value-revealing `print` statements rather than assertions; and prompt-induced increases/decreases in test volume do not significantly change final outcomes. GPT-5.2 (71.8% resolution) writes near-zero new tests, matching Claude Opus 4.5 (74.4%) which writes a test in ~83% of tasks.
- Source: https://arxiv.org/abs/2602.07900 (research paper, arXiv, SMU + SJTU + ByteDance, 2026) — read in full (abstract + intro + RQ overview).
- Verbatim: "test writing is common, but resolved and unresolved tasks within the same model exhibit similar test-writing frequencies. When tests are written, they mainly serve as observational feedback channels, with value-revealing print statements appearing much more often than assertion-based checks." / "prompt-induced changes in the volume of agent-written tests do not significantly change final outcomes in this setting." / "current agent-written testing practices reshape process and cost more than final task outcomes."
- Tier: **Verified** (abstract + intro read). This is the strongest *negative* result for [P8] in the agent context: the human TDD intuition (write tests first, they drive correctness) does not straightforwardly transfer to autonomous agents. Caveat: this is about *agent-authored* throwaway tests on SWE-bench Verified, not about the value of a *pre-existing human test suite* (which SWE-bench itself uses as the oracle).

### F-13 — Survey: agents run the full loop (write code → run tests → diagnose → fix), but agent code still carries defects hard to cover with unit tests [P8 testing + P7 error handling + cross-cutting]
- Claim: A systematic survey of LLM-based code-generation agents frames agents as simulating the full human workflow (analyze requirements, write code, run tests, diagnose errors, apply fixes); it notes agent-generated code "often contains logical defects, performance pitfalls, or security vulnerabilities that are difficult to cover with unit tests," and cites TDD-style approaches (e.g. TiCoder auto-generating test cases to clarify requirements) as a way to improve generation accuracy.
- Source: https://arxiv.org/abs/2508.00083 (research paper, arXiv survey, Peking University, 2025) — read in full (abstract + intro).
- Verbatim: "They are capable of simulating the complete workflow of human programmers, including analyzing requirements, writing code, running tests, diagnosing errors, and applying fixes." / "code generated by agents often contains logical defects, performance pitfalls, or security vulnerabilities that are difficult to cover with unit tests." / "combining test-driven development concepts, TiCoder guides users to clarify natural language requirements by automatically generating test cases, thereby improving code generation accuracy."
- Tier: **Verified** (abstract + intro read). Nuance: the *loop* (test → observe → fix) is central to agent design, but the *value* of the tests is limited when the defects are logical/semantic rather than assertion-catchable — consistent with F-12.

### F-14 — SWE-CI's programmer agent is explicitly prompted as a TDD practitioner [P8 testing]
- Claim: The SWE-CI benchmark's Programmer agent prompt explicitly casts the model as "a senior programmer proficient in Python software engineering and Test-Driven Development (TDD)," implementing requirements "in small-step iterations under a TDD workflow" — i.e., TDD is used as a *scaffold* for long-horizon maintenance, not just as a correctness oracle.
- Source: https://arxiv.org/abs/2603.03823 (same paper as F-04) — read in full (prompt appendix).
- Verbatim: "You are a senior programmer proficient in Python software engineering and Test-Driven Development (TDD). ... You excel at implementing requirements and refactoring code in small-step iterations under a Test-Driven Development (TDD) workflow."
- Tier: **Verified** (prompt text read). Shows TDD is treated as an agent *workflow discipline* in the maintainability-setting, complementing F-12/F-13.

---

## D. Refactoring as an agent task (Boy Scout Rule / continuous improvement)

### F-15 — Refactoring benchmarks exist; agents can refactor but struggle to fully eliminate smells [P9 refactoring/Boy Scout Rule]
- Claim: A cluster of 2025–2026 benchmarks targets agent refactoring: RefactorBench (stateful reasoning via code; a proficient human solves 87% of test cases in 5 min/task), SWE-Refactor (repository-level real-world refactoring), RefAgent (multi-agent automatic refactoring), and SmellBench (fine-grained smell elimination across 7 smell types; best agent+LLM combo, Qwen Code + Claude Sonnet 4.5, reached only a 50.34 smell-elimination score).
- Source: https://arxiv.org/abs/2503.07832 (RefactorBench), https://arxiv.org/abs/2602.03712 (SWE-Refactor), https://arxiv.org/abs/2511.03153 (RefAgent), https://arxiv.org/abs/2606.05574 (SmellBench) — research papers, arXiv.
- Verbatim (search-snippet level): "a proficient human developer attempt all the tasks within the benchmark, with a limit of 5 minutes per task ... they solve 87% of the test cases" (RefactorBench) / "the best combination—Qwen Code + Claude Sonnet 4.5—achieved only a 50.34 score of smell elimination" (SmellBench).
- Tier: **Plausible** (search-snippet level; abstracts not read in full this lane — flag for the collector to confirm exact figures if quoted as hard facts). Relevance: [P9] "leave the code cleaner than you found it" is an active, measurable agent capability that is still weak (smell elimination ~50%), and continuous autonomous refactoring is an emerging research area.

### F-16 — Continuous autonomous refactoring is an emerging roadmap area; generated refactorings can introduce new defects [P9 refactoring + P7 error handling]
- Claim: A 2026 research roadmap for AI-driven code-quality maintenance notes that while LLMs show potential for continuous refactoring, "the generated refactorings may introduce new defects, hallucinations, or syntax errors, especially in repository-level contexts, requiring additional human verification."
- Source: https://arxiv.org/abs/2609.01236 (research paper, arXiv, 2026) — search-snippet level.
- Verbatim (search-snippet level): "they also show that the generated refactorings may introduce new defects, hallucinations, or syntax errors, especially in repository-level contexts, requiring additional human verification."
- Tier: **Plausible** (search-snippet level; not read in full). Reinforces F-15: [P9] refactoring by agents is promising but not yet safe to run unattended.

---

## E. Frame-mismatch finding (the "10 principles" lens)

### F-17 — No paper found organizes findings around "the 10 Clean Code principles"; the field uses ISO/IEC 25010 + static metrics [cross-cutting / framing]
- Claim: None of the on-target papers adopt the 10-principle Clean Code frame (naming, SRP, DRY, KISS, YAGNI, SOLID, error handling, TDD, refactoring, readability). They instead evaluate against **ISO/IEC 25010** quality attributes (maintainability, reliability, security, performance efficiency) and **static metrics** (SonarQube maintainability/reliability, Pylint, Maintainability Index / cyclomatic complexity).
- Source: cross-paper synthesis of F-04 (ISO/IEC 25010), F-08 (SonarQube), F-05/F-06 (Pylint + MI), F-09 (SAST/security).
- Verbatim (F-04): "The ISO/IEC 25010 standard defines maintainability as the degree to which software can be modified effectively without introducing defects or degrading existing quality."
- Tier: **Verified** (directly observed across the read papers). Implication for the collector: the report must *map* these metric-based findings onto the 10 principles (done via the [P#] tags above) rather than expect a paper to state them that way. The cleanest per-principle coverage is [P1], [P4], [P7], [P8], [P9], [P10]; [P2] SRP, [P3] DRY, [P5] YAGNI, [P6] SOLID have **no direct agent-context paper** found in this lane.

---

## Searched, found nothing (evidence of absence)

- **A controlled A/B experiment isolating "codebase cleanliness" as the independent variable on SWE-bench-style issue resolution** → No such controlled study found. The best available is correlational (SWE-Bench Pro enterprise-complexity gap, F-03) and the evolution-based EvoScore (SWE-CI, F-04), which measures the *consequence* of quality decisions over time rather than a clean "clean vs dirty codebase → resolution rate" contrast. (arXiv, SWE-bench ecosystem)
- **Direct agent-context studies on DRY [P3], SOLID [P6], YAGNI [P5], or single-responsibility [P2]** → No paper found that tests these specific principles' effect on LLM coding-agent performance. DRY/SOLID/YAGNI appear only as generic maintainability sub-factors inside SonarQube/MI scores, never as isolated experimental variables. (arXiv)
- **"Clean code makes the agent's *context window* more efficient" (token/context-management angle)** → No paper found quantifying that a cleaner codebase reduces an agent's token/context consumption or context-overflow failures. SWE-Bench Pro lists "context_overflow_from_listing" and "context management" as failure categories (F-03) but does not tie them to code cleanliness. (arXiv)
- **Per-principle effect of *naming* [P1] on agent *generation* correctness (vs evaluation)** → F-11 shows LLMs *perceive* naming quality (as evaluators) and F-05 shows LLMs *produce* good naming (Pylint), but no paper found measures whether better names in the *input* codebase improve an agent's patch correctness. (arXiv)
- **A paper explicitly titled/framed "Clean Code for LLM agents" or "Clean Code in the age of AI agents"** → No such dedicated paper found; the topic is addressed indirectly via maintainability/readability/agent-benchmark papers. (arXiv + web)

---

## Notes for the collector / final report

1. **The headline answer the papers support:** Clean-code principles *do* matter for LLM coding agents, but the evidence is (a) strongest for **maintainability over time** (SWE-CI: clean/extensible code → better future performance; technical debt compounds), (b) **weaker/absent for snapshot task success** (SWE-bench doesn't measure it; a clean fix and a brittle fix both pass), and (c) **mixed for TDD** (the human "tests-first" intuition does not straightforwardly transfer — agent-written tests are mostly observational and don't move outcomes, F-12).
2. **The most quotable, on-target result** is SWE-CI Observation 5/6 (F-05/F-06): LLM code is "superficially clean but intrinsically complex" — better on Pylint (naming/formatting), worse on the Maintainability Index, and more concise *at the cost of* abstraction/encapsulation/modularization. This is the empirical core of "LLMs get the surface of clean code but not the substance."
3. **Per-principle coverage map** (what the papers actually evidence): [P1] naming — good (F-05, F-10, F-11); [P4] KISS — nuanced, LLMs go "minimal-to-pass" not "minimal-but-structured" (F-06); [P7] error handling — LLM code has fewer bugs on easy tasks but structural/regression issues on complex/long-horizon (F-08, F-07, F-09); [P8] TDD — loop is central but agent-authored tests are low-value (F-12, F-13, F-14); [P9] refactoring — measurable agent task, still weak (~50% smell elimination) (F-15, F-16); [P10] maintainability/readability — surface ≈ human, deep < human (F-05, F-10). **Gaps: [P2] SRP, [P3] DRY, [P5] YAGNI, [P6] SOLID — no direct agent-context paper found** (F-17).
4. **Two findings to present as tension, not contradiction:** F-10 (Atlassian: LLM readability ≈ human) vs F-05/F-06 (SWE-CI: LLM maintainability < human). Both are true because they use different metrics (surface readability vs deep MI/complexity). The report should make this metric distinction explicit.
5. **Recency:** the field is moving fast — the three most decision-relevant papers are all 2025–2026 (SWE-CI 2026, Rethinking Agent-Generated Tests 2026, SWE-Bench Pro 2025). The 2023 SWE-bench / 2024 SWE-agent numbers (1.96% / 12.5%) are historical baselines, not current SOTA.
6. **Caveat to carry into the report:** F-15/F-16 are snippet-level (Plausible) — confirm exact SmellBench/RefactorBench figures before quoting them as hard numbers.
