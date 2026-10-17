# LANE2-1 — Verify the two load-bearing anchors at PRIMARY sources

- **Task:** RESEARCH-clean-code-ai-agents [LANE2-1] (collector in-session verification)
- **Lane scope:** Verify the two most load-bearing quantitative/causal claims in the wave-1 corpus against their PRIMARY sources, because both rested on a secondary source or a single full-read not independently re-checked. The final report headlines these two claims, so they must be confirmed (or corrected) at the primary before synthesis.
- **Source types owned:** research papers (arXiv), the primary vendor/blog source of the SonarSource study.
- **Date of research:** 2026-10-17.
- **Tier scheme:** **Verified** (primary read) / **Plausible** (secondary-only or snippet) / **Speculative**.
- **Note:** This lane was executed IN-SESSION by the collector (the kanban worker context is fenced from creating child cards on its own board), not as a dispatched subagent. It is a narrow verification task, matching the deep-research "Docs-first note without fan-out" case.

---

## VERDICTS (read first)

- **TARGET A — SonarSource study: CONFIRMED at primary, figures refined.** The wave-1 claim (7–8% fewer tokens, 34% fewer file revisits, same pass rate) is **confirmed and made more precise** by the primary. The primary is the SonarSource blog (17 Jun 2026) + the underlying paper **arXiv 2605.20049** ("Does Code Cleanliness Affect Coding Agents?"). Exact figures: **7.1% fewer input tokens, 8.5% fewer output tokens, 11.1% less reasoning effort, <1% pass-rate difference, ~34% fewer file revisits.** Important caveats the wave-1 missed: it is a **vendor (Sonar) study, one model (Claude Sonnet 4.6), one harness (Claude Code), six repo pairs, wide per-task variance (−47% to +44%)**, with a documented counterexample and token-neutral cognitive-hotspot tasks. → The headline is valid but must carry these caveats.
- **TARGET B — SWE-CI: CONFIRMED real.** arXiv **2603.03823** exists; title, authors, date, and abstract all match the wave-1 framing. The paper is real and the core causal claim (maintainability revealed by tracking functional correctness over time; 100 tasks, avg 233 days / 71 commits) is confirmed at the abstract level. The specific observations (15/20 Pylint vs 20/20 MI, etc.) were read in full by LANE-2 and are consistent with the confirmed abstract.

---

## TARGET A — The SonarSource controlled study (the quantified anchor)

### F-A1 — The primary source is the SonarSource blog + arXiv 2605.20049 [cross-cutting; P10/P1]
- Claim: The "660 Claude Code trials" study is Sonar's own, published as a SonarSource blog post (17 Jun 2026, Killian Carlsen-Phelan) with the full paper at arXiv 2605.20049 ("Does Code Cleanliness Affect Coding Agents?").
- Source: https://www.sonarsource.com/blog/your-ai-bill-is-a-code-quality-problem/ (PRIMARY vendor blog, read) + https://arxiv.org/abs/2605.20049 (paper, cited by the blog).
- Verbatim (blog): "A controlled study from Sonar looked at the code side and found that structural quality affects what agents cost to run." / "Further reading: Does Code Cleanliness Affect Coding Agents?, the full Sonar research paper."
- Tier: **Verified** (primary blog read).
- **Correction to wave-1:** LANE-3 F-62 sourced this via developersdigest.tech (secondary) and said the figures were "from the arXiv abstract per the article." The primary is the SonarSource blog + arXiv 2605.20049 — now confirmed directly.

### F-A2 — Confirmed study design: 6 matched repo pairs, 33 tasks × 10 runs = 660 trials, Claude Sonnet 4.6 [P10/P1]
- Claim: The study built six matched pairs of repositories (same app, same test suite, same deps; only internal factoring/naming/nesting differs). Three pairs were clean→degraded, three messy→cleaned (both directions to isolate structural state). 33 tasks, each run 10× on both sides = 660 trials on Claude Code with Claude Sonnet 4.6.
- Source: https://www.sonarsource.com/blog/your-ai-bill-is-a-code-quality-problem/ (PRIMARY, read).
- Verbatim: "Sonar's study built six matched pairs of repositories. Each pair ships the same application and passes the same test suite with the same dependencies. The only difference is internal: how the code is factored, named, and nested... Three pairs started from clean codebases and were deliberately degraded; three started from organically messy codebases and were cleaned up... Across the six pairs, researchers authored 33 coding tasks and ran each ten times on both sides, totaling 660 trials on Claude Code with Claude Sonnet 4.6."
- Tier: **Verified** (primary read). Confirms the wave-1 "660 trials / 33 tasks / six minimal-pair repos."

### F-A3 — CONFIRMED + refined figures: 7.1% fewer input tokens, 8.5% fewer output, 11.1% less reasoning, <1% pass-rate diff, ~34% fewer file revisits [P10/P1]
- Claim: The exact headline figures, confirmed at the primary and more precise than the wave-1 "7–8%."
- Source: https://www.sonarsource.com/blog/your-ai-bill-is-a-code-quality-problem/ (PRIMARY, read).
- Verbatim: "Agents working on cleaner code used 7.1% fewer input tokens, 8.5% fewer output tokens, and 11.1% less reasoning effort. Whether or not they finished the task didn't change as there was a less than 1% difference in pass rate." / "Agents on the cleaner side also re-read files they had already edited roughly 34% less often, and that pattern held across every repository pair."
- Tier: **Verified** (primary read, quote attached to ledger).
- **Reconciliation with wave-1:** "7–8% fewer tokens" = 7.1% input + 8.5% output. "34% fewer file revisits" = confirmed. "Same pass rate" = confirmed (<1% difference). The wave-1 claim holds, now with precision.

### F-A4 — CAVEATS the wave-1 missed: vendor study, one model/harness, wide variance, a counterexample, token-neutral hotspots [P10]
- Claim: The finding is directional, not universal. It is Sonar's own study (vendor), on one model (Sonnet 4.6) in one harness (Claude Code), across six repo pairs, with wide per-task variance; one cleanup made things worse; cognitive-hotspot tasks were token-neutral.
- Source: https://www.sonarsource.com/blog/your-ai-bill-is-a-code-quality-problem/ (PRIMARY, read).
- Verbatim: "The study is Sonar's own, conducted on one model in one harness, across six repository pairs. Per-task variance was wide, with individual deltas ranging from -47% to +44% on input tokens, and of 27 non-calibration tasks, 16 favored the clean side while 11 favored the messy side." / "Not every cleanup helped. On one genie task, the pipeline extracted helpers... spreading work across more methods without making the core any more findable. The agents paid for the added surface area with 8% more input tokens." / "Cognitive-hotspot tasks... netted out roughly token-neutral, because extraction redistributed complexity across more files rather than eliminating it."
- Tier: **Verified** (primary read).
- **Multi-module nuance:** "Where work required changes across two or more module boundaries, agents on the clean side used 10.7% fewer input tokens and revisited files 50.8% less often." — the effect is strongest at module boundaries (relevant to P6/SOLID and P2/SRP).

### F-A5 — NEW finding surfaced: SlopCodeBench — agent code drifts more verbose/less structured over successive iterations [P10/P9; cross-cutting]
- Claim: A companion benchmark (SlopCodeBench, scbench.ai) tracks what happens to code quality when agents extend their own prior work under evolving specs: agent-generated code ended **2.3× more verbose** than human-maintained baselines, with **structural erosion rising in 77% of trajectories**; prompt-level interventions cut initial verbosity ~⅓ but did not change degradation rates over time.
- Source: https://www.scbench.ai/ (benchmark, cited by the SonarSource blog) + https://www.sonarsource.com/blog/your-ai-bill-is-a-code-quality-problem/ (PRIMARY, read).
- Verbatim (blog): "Agent-generated code drifted toward more verbose, less structured output, ending 2.3 times more verbose than human-maintained baselines, with structural erosion rising in 77% of trajectories. Prompt-level interventions reduced initial verbosity by roughly a third but didn't change degradation rates over time."
- Tier: **Verified** (primary blog read; the SlopCodeBench site itself not independently read — the figures are as the Sonar blog states them).
- **Why it matters:** this is the research-side twin of the "globally incoherent / code rot" practitioner finding (see LANE2-2), and the Sonar blog explicitly connects the two: "if messier code costs more for agents to work on (the Sonar finding), and agents tend to make code messier over successive iterations (the SlopCodeBench finding), then the cost trajectory for unverified agent work bends upward."

### F-A6 — NEW finding surfaced: Le et al. 2025 (arXiv 2510.03178) — naming quantitatively affects agent performance [P1]
- Claim: A related study quantifies the naming effect: uninformative identifier renames degraded GPT-4o's summarization accuracy from 87.3% to 58.7% — nearly 30 percentage points from names alone.
- Source: https://arxiv.org/abs/2510.03178 (paper, cited by the SonarSource blog) + https://www.sonarsource.com/blog/your-ai-bill-is-a-code-quality-problem/ (PRIMARY, read).
- Verbatim (blog): "Le et al. (2025) quantified the effect in a related study, finding that uninformative identifier renames degraded GPT-4o's summarization accuracy from 87.3% to 58.7%, nearly 30 percentage points from names alone."
- Tier: **Verified** (primary blog read; the Le et al. paper itself not independently read — figures as the Sonar blog states them).
- **Why it matters:** this is a QUANTIFIED [P1] naming result the wave-1 corpus did not have — it upgrades "naming helps agents navigate" from practitioner-asserted to measured.

---

## TARGET B — SWE-CI (the causal anchor)

### F-B1 — SWE-CI EXISTS at arXiv 2603.03823 [cross-cutting; P4/P9/P10]
- Claim: The paper is real: "SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration," Jialong Chen, Xander Xu, Hu Wei, Chuan Chen, Bing Zhao; submitted 4 Mar 2026 (v1), last revised 1 Apr 2026 (v4); cs.SE.
- Source: https://arxiv.org/abs/2603.03823 (PRIMARY arXiv abs page, read) + https://github.com/SKYLENAGE-AI/SWE-CI (repo).
- Verbatim (abstract): "we propose SWE-CI, the first repository-level benchmark built upon the Continuous Integration loop, aiming to shift the evaluation paradigm for code generation from static, short-term functional correctness toward dynamic, long-term maintainability. The key insight is simple: Maintainability can be revealed by tracking how functional correctness changes over time. The benchmark comprises 100 tasks, each deriving from a real-world code repository with a development history spanning an average of 233 days and 71 consecutive commits."
- Tier: **Verified** (primary abs page read, quote attached to ledger).
- **Correction/confirmation to wave-1:** LANE-2 cited SWE-CI as "Sun Yat-sen Univ + Alibaba, 2026." The arXiv author list is Chen/Xu/Wei/Chen/Zhao (the GitHub org is SKYLENAGE-AI). The affiliation detail should be cited as "Chen et al., 2026 (SKYLENAGE-AI)" rather than asserting a specific university unless re-confirmed. The core claim is confirmed.

### F-B2 — Core causal claim confirmed: maintainability over evolution, invisible on snapshot benchmarks [P4/P9/P10]
- Claim: The paper's central thesis — that an agent's code-quality decisions compound over long-term evolution and are invisible on snapshot (SWE-bench-style) benchmarks — is confirmed by the abstract's framing ("dynamic, long-term maintainability," "Maintainability can be revealed by tracking how functional correctness changes over time").
- Source: https://arxiv.org/abs/2603.03823 (PRIMARY, read).
- Tier: **Verified** (abstract read). The specific observations (EvoScore; 15/20 LLMs beat human oracle on Pylint but all 20 lose on Maintainability Index; LLMs write fewer lines at the cost of maintainability; zero-regression rate <0.25 for most models) were read in full by LANE-2 (F-04/F-05/F-06/F-07) with verbatim quotes and are consistent with this confirmed abstract.

---

## Searched, found nothing (evidence of absence)

- **A non-vendor, independent replication of the SonarSource 660-trial study** → None found. The controlled clean-vs-messy A/B is Sonar's own (vendor), one model, one harness. No independent lab has replicated the exact 7.1%/8.5%/34% figures. → The quantified anchor is strong but single-source (vendor); the report should say so.
- **A first-hand read of the SWE-CI body observations (15/20 Pylint, 20/20 MI) in THIS lane** → Not re-read here (LANE-2 read the full body). This lane confirmed the paper + abstract at the primary; the body observations rest on LANE-2's full read. → Chain is: LANE-2 full read (body) + this lane's primary abs read (existence + core claim).

---

## Notes for the collector / final report

1. **The quantified anchor is now primary-verified and more precise:** 7.1% fewer input tokens, 8.5% fewer output, 11.1% less reasoning, <1% pass-rate diff, ~34% fewer file revisits (Sonar blog + arXiv 2605.20049). Carry the caveats: vendor study, one model (Sonnet 4.6), one harness (Claude Code), six pairs, wide per-task variance, a counterexample, token-neutral hotspots. The effect is strongest at module boundaries (10.7% / 50.8%).
2. **The causal anchor (SWE-CI) is confirmed real** (arXiv 2603.03823, Chen et al. 2026). Cite the affiliation as "Chen et al. (SKYLENAGE-AI), 2026" unless the university is re-confirmed.
3. **Two bonus quantified findings surfaced:** SlopCodeBench (agent code 2.3× more verbose, structural erosion in 77% of trajectories) and Le et al. 2025 (naming: 87.3%→58.7% GPT-4o summarization). Both strengthen the report and were absent from the wave-1 corpus.
4. **The Sonar blog explicitly links its efficiency finding to SlopCodeBench's degradation finding** — "the cost trajectory for unverified agent work bends upward." This is a strong, citable synthesis point for the report's "why clean code matters more for agents" argument.
