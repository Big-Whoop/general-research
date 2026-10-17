# LANE2-2 — Is the "locally clean but globally incoherent" LLM-code finding backed by RESEARCH?

- **Task:** RESEARCH-clean-code-ai-agents [LANE2-2] (collector in-session verification)
- **Lane scope:** The most counterintuitive wave-1 finding — that LLM coding agents produce code that is *locally* clean (passes linters, has coverage, follows conventions) but *globally* incoherent (no architectural through-line) — was supported ONLY by community/practitioner sources (Reddit, HN). This lane asks whether RESEARCH (papers / named studies) documents the same phenomenon, so the report can elevate it from "practitioner-observed" to "also research-backed" — or document its absence.
- **Source types owned:** research papers (arXiv), named industry studies.
- **Date of research:** 2026-10-17.
- **Tier scheme:** **Verified** (source read whole) / **Plausible** (snippet-level) / **Speculative**.
- **Note:** Executed IN-SESSION by the collector (narrow verification task; the worker context is fenced from creating child cards).

---

## VERDICT (read first)

**YES — the "locally clean but globally incoherent" finding is now RESEARCH-BACKED, not just practitioner-observed.** Three 2025–2026 papers (absent from the wave-1 corpus) document exactly this phenomenon, each with a named concept:

1. **arXiv 2605.02741 — "AI-Generated Smells" (Zhu, Tsantalis, Rigby, Concordia, 4 May 2026):** introduces the **"Modular Mirage"** — "agents achieve superficial structural modularity (file separation) but fail to create semantic cohesion" — and reports the **first longitudinal study of "architectural rot"** in autonomous agents, plus a **"Volume-Quality Inverse Law"** (code volume is a near-perfect predictor of structural degradation). This is the closest research match to the practitioner "meta-code spaghetti" observation.
2. **arXiv 2512.04273 — "Quantitative Analysis of Technical Debt and Pattern Violation in LLM Architectures" (Slater, Georgia Tech, 3 Dec 2025, JSS):** the first empirical framework to measure **"Architectural Erosion"** in AI-synthesized microservices; defines **"Hallucinated Coupling"** (correct class, wrong dependencies violating inversion of control) and **"Silent Accumulation"** of architectural violations.
3. **arXiv 2606.14796 — "Faster Code, Deeper Debt?" (multivocal literature review, 2026):** confirms a "small but growing body of formal literature" on LLMs contributing to technical debt, with "code-level and architectural issues" the most frequently discussed concerns.

Plus, surfaced via the SonarSource blog (see LANE2-1 F-A5): **SlopCodeBench** (scbench.ai) — agent code ends **2.3× more verbose** than human baselines with **structural erosion in 77% of trajectories** over successive iterations.

**Implication for the report:** the wave-1 framing "this is the most counterintuitive *practitioner* finding" should be upgraded to "this is a *convergent* finding — practitioner-observed (LANE-3 F-67, LANE-4 F-05) AND now independently documented in peer-track research (2605.02741, 2512.04273, 2606.14796, SlopCodeBench)." The practitioner intuition and the research literature point the same way.

---

## Findings

### F-C1 — "AI-Generated Smells": the "Modular Mirage" = locally clean, globally incoherent [P2/P6/P10] — STRONGEST match
- Claim: LLM/agent-generated code shows a distinct "machine signature" of technical debt: as models get more capable they generate *more* bloated, coupled code ("Reasoning-Complexity Trade-off"); at scale this becomes "God Class" syndromes and tight module coupling; and agents achieve *superficial* structural modularity (separate files) without *semantic* cohesion — the "Modular Mirage."
- Source: https://arxiv.org/abs/2605.02741 (research paper, arXiv, Concordia University, read in full — abstract + intro + contributions).
- Verbatim: "AI does not eliminate flaws but rather introduces a distinct 'machine signature' of defects." / "a fundamental Reasoning-Complexity Trade-off: as models become more capable, they generate increasingly bloated and coupled code." / "we establish a Volume-Quality Inverse Law, where code volume is a near-perfect predictor of structural degradation." / "we introduce the concept of the 'Modular Mirage,' where agents achieve superficial structural modularity (file separation) but fail to create semantic cohesion." / "running code is just as likely to be structurally flawed as failed code."
- Tier: **Verified** (abstract + intro + contributions read; quote attached to ledger).
- **Mapping:** this is the research name for the practitioner "meta-code made of nicely written pieces that put together form a huge spaghetti" (LANE-4 F-05) and "they think 'Clean Code' means splitting into tiny functions, rather than cohesive functions" (LANE-3 F-67). "Superficial structural modularity without semantic cohesion" = "locally clean, globally incoherent."

### F-C2 — "AI-Generated Smells": first longitudinal study of "architectural rot"; prompting does NOT fix it [P10/P9]
- Claim: The paper reports the first longitudinal study of "architectural rot" in autonomous agents — as system complexity scales, functionally correct code degenerates into unmaintainable structures — and finds the decay is NOT mitigated by advanced prompting (few-shot, more specific requirements).
- Source: https://arxiv.org/abs/2605.02741 (research paper, read).
- Verbatim: "We conduct the first longitudinal study of 'architectural rot' in autonomous software agents, demonstrating that as system complexity scales, functionally correct code degenerates into unmaintainable structures. Our statistical analysis confirms that this decay is not mitigated by advanced prompting techniques like few-shot examples." / "neither functional correctness nor detailed prompting mitigates this decay."
- Tier: **Verified** (read; quote attached to ledger).
- **Why it matters:** this directly supports the wave-1 practitioner consensus that prose rules (CLAUDE.md/AGENTS.md) are insufficient — the decay persists even with detailed prompting, so mechanical enforcement (linters/architectural linters/CI) is required (LANE-3 F-59, LANE-4 F-08).

### F-C3 — "Quantitative Analysis of Technical Debt in LLM Architectures": "Architectural Erosion" + "Hallucinated Coupling" [P6/P10]
- Claim: The first empirical framework to measure "Architectural Erosion" and technical-debt accumulation in AI-synthesized microservices. Defines "Hallucinated Coupling" (an LLM correctly implements a class but imports dependencies that violate inversion of control) and "Silent Accumulation" of architectural violations. In a Hexagonal-Architecture "trap," GPT-5.1 had 0% violation rate, Claude 4.5 20%, Llama 3 8B 80% (illegal circular dependencies); open-weights models also showed "Implementation Laziness" (60% fewer logical lines, omitting complex logic).
- Source: https://arxiv.org/abs/2512.04273 (research paper, arXiv, Georgia Tech, Journal of Systems and Software, read in full — abstract + intro + method + results table).
- Verbatim: "this study presents the first empirical framework to measure 'Architectural Erosion' and the accumulation of Technical Debt in AI-synthesized microservices." / "We define a new metric, Hallucinated Coupling, which occurs when an LLM correctly implements a class but incorrectly imports dependencies that violate the inversion of control principle." / "This paper investigates the 'Silent Accumulation' of architectural violations in LLM-generated code." / "without automated architectural linting, utilizing smaller open-weights models for system scaffolding accelerates the accumulation of structural technical debt."
- Tier: **Verified** (read; quotes attached to ledger).
- **Caveat:** this is a **pilot study** (N=5 runs per model, one microservice task) — directional, not statistically robust. The report should note the small-N limitation.
- **Why it matters:** "without automated architectural linting... accelerates the accumulation of structural technical debt" is a research citation for the wave-1 "enforce with architectural linters" recommendation (LANE-4 F-08, u/esilverberg2: "hundreds of architectural lint rules that the AI will violate, read, and correct").

### F-C4 — "Faster Code, Deeper Debt?" — a growing formal literature on LLM technical debt [cross-cutting]
- Claim: A 2026 multivocal literature review confirms "a small but growing body of formal literature examines how LLMs can contribute to technical debt," with "code-level and architectural issues, including code quality and maintainability risks" the most frequently discussed concerns.
- Source: https://arxiv.org/abs/2606.14796 (research paper, arXiv, multivocal literature review, read — abstract).
- Verbatim: "A small but growing body of formal literature examines how LLMs can contribute to technical debt. Across these studies, the most frequently discussed concerns relate to code-level and architectural issues, including code quality and maintainability risks that signal the accumulation of technical [debt]."
- Tier: **Verified** (abstract read).
- **Why it matters:** confirms this is an active, growing research area (not a one-off), which strengthens the report's confidence that the "globally incoherent" finding is a real, studied phenomenon.

### F-C5 — SlopCodeBench (via SonarSource blog): agent code degrades over successive iterations [P10/P9]
- Claim: A companion benchmark tracks code quality as agents extend their own prior work under evolving specs: agent-generated code ended 2.3× more verbose than human-maintained baselines, with structural erosion rising in 77% of trajectories; prompt interventions cut initial verbosity ~⅓ but did not change degradation rates over time.
- Source: https://www.scbench.ai/ (benchmark) + https://www.sonarsource.com/blog/your-ai-bill-is-a-code-quality-problem/ (PRIMARY, read).
- Verbatim (Sonar blog): "Agent-generated code drifted toward more verbose, less structured output, ending 2.3 times more verbose than human-maintained baselines, with structural erosion rising in 77% of trajectories. Prompt-level interventions reduced initial verbosity by roughly a third but didn't change degradation rates over time."
- Tier: **Verified** (Sonar blog read; SlopCodeBench site not independently read — figures as the blog states them).
- **Why it matters:** the *temporal* version of the finding — the incoherence isn't just present, it *accumulates* over iterations, which is why the "code janitor"/remediation role (LANE-4 F-04) is emerging.

---

## Searched, found nothing (evidence of absence)

- **A study measuring a *global* architectural metric (ArchUnit / dependency-cruiser / package coupling) specifically on Claude Code / Cursor / Devin output in a real repo** → The papers found (2605.02741, 2512.04273) use code-smell taxonomies (PyExamine) and AST-based dependency analysis on *generated* microservices/agent systems (MetaGPT), not on a specific commercial agent's output in a real production repo. → The research validates the *phenomenon* but not yet on the exact commercial agents named in the research question.
- **A paper using the exact phrase "locally clean but globally incoherent"** → None uses that exact phrase; the research uses "Modular Mirage," "architectural rot," "Architectural Erosion," "Hallucinated Coupling," "machine signature." → The concept is documented under different (research) names.

---

## Notes for the collector / final report

1. **Upgrade the "globally incoherent" finding from practitioner-only to convergent (practitioner + research).** The research names: "Modular Mirage" (2605.02741), "architectural rot" (2605.02741), "Architectural Erosion" / "Hallucinated Coupling" / "Silent Accumulation" (2512.04273), "machine signature" (2605.02741), and the temporal "structural erosion over iterations" (SlopCodeBench).
2. **The research and the practitioners converge on the same prescription:** prose/prompting does NOT fix it (2605.02741: "neither functional correctness nor detailed prompting mitigates this decay"; 2512.04273: "without automated architectural linting... accelerates the accumulation") → mechanical enforcement (architectural linters, CI, quality gates) is required. This is a strong, doubly-sourced (research + practitioner) recommendation.
3. **Caveats to carry:** 2512.04273 is a small-N pilot (N=5/model); 2605.02741 uses MetaGPT-generated systems + CodeContest tasks (not the commercial agents named in the question); SlopCodeBench figures are as the Sonar blog states them. None of these measured the *exact* commercial agents (Claude Code/Cursor/Devin) in a real production repo — so the report should say the phenomenon is research-validated in general but not yet benchmarked on the specific named agents.
4. **New arXiv IDs to add to the corpus source register:** 2605.02741, 2512.04273, 2606.14796, 2605.20049 (Sonar study), 2510.03178 (Le et al. naming), + scbench.ai (SlopCodeBench).
