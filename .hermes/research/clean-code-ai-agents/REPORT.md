# Clean Code for AI Coding Agents — Research Report

**Research question:** Identify the 10 most important principles of Clean Code (software engineering) and how each of them works. Then, for each, determine whether it is also useful for programming AI agents (LLM-based coding agents that autonomously write, edit, and test code — e.g. Claude Code, OpenAI Codex, Cursor, Devin, SWE-agent, Aider). Focus on research papers and practical experience from world-leading developers in the AI field.

**Date:** 2026-10-17 · **Method:** 5 wave-1 lanes (242 findings) + 2 in-session verification lanes, synthesized below. Full per-finding citations live in the lane files (paths in the Appendix); the Sources block at the end maps the `[n]` ids used inline.

**Tier key used throughout:** **Verified** = authoritative/primary source actually read · **Plausible** = sound general behavior or snippet-level, not demonstrated on-target · **Speculative** = mechanism asserted, untested. Tiers are never collapsed into a flat assertion.

---

## TL;DR — best result first

**Clean code is MORE useful for AI coding agents, not less — but the *reason* has shifted and the *form* of some principles has flipped.** The 2008 argument was "another human will read this code." The 2026 argument is "an agent's context window, token budget, and grep-based navigation will read this code — many times a day — and every token of noise has a fixed cost."[15][12]

Three findings carry the whole report:

1. **The single load-bearing fact is the context window.** The agent's context window is a fixed, scarce, metered resource, and *distracting context actively harms performance* (unlike a human, the model cannot just ignore irrelevant content).[12][15] Every Clean Code principle that **shrinks the context the agent must hold to do one job correctly** is **AMPLIFIED**; things that **don't change that budget** (formatting minutiae, "write clean code" as a stated rule) are **MOOT**; and places where the **agent's default runs opposite to the human instinct** (comments, defensive code, over-engineering) are **INVERTED** and must be corrected by explicit rules + mechanical enforcement.[22][15]

2. **The most counterintuitive finding — agents write code that is *locally* clean but *globally* incoherent — is now RESEARCH-BACKED, not just practitioner-observed.** Practitioners call it "a sort of meta-code made of nicely written pieces that put together form a huge spaghetti"[27] and "they think 'Clean Code' means splitting into tiny functions, rather than cohesive functions."[26] The research literature independently names the same phenomenon: the **"Modular Mirage"** (superficial file-separation without semantic cohesion) and **"architectural rot"**[6], **"Architectural Erosion"** / **"Hallucinated Coupling"**[7], and a growing formal literature on LLM technical debt[8]. The convergence of practitioner intuition and peer-track research is the report's strongest signal.

3. **The quantified anchor (primary-verified):** a controlled Sonar study (660 Claude Code trials, six matched repo pairs) found clean codebases use **7.1% fewer input tokens, 8.5% fewer output tokens, 11.1% less reasoning effort, and ~34% fewer file revisits — with no change in pass rate**[5][4]. The payoff is **efficiency, not success rate** — and it is largest at module boundaries (10.7% / 50.8%).[5]

**The bottom line for the "is it useful?" question:** all 10 principles transfer to the agent context, but with a non-uniform verdict — most are **AMPLIFIED** (naming, small units/SRP, DRY, SOLID, error handling, TDD, refactoring, maintainability), two carry an **INVERTED pressure** that must be actively imposed (KISS, YAGNI), and readability/maintainability is a **split** (comments invert, formatting goes moot, "write clean code" as a rule is redundant). The human's role shifts from *writing* clean code to *enforcing* it — because **no agent does it by default**[22][23] and **prompting alone does not fix the global incoherence**[6].

---

## 1. The 10 principles (Facet A — the backbone)

> **Provenance caveat (Verified):** there is **no single primary source that lists exactly "the 10 Clean Code principles."** The canonical set is a **cross-source synthesis**: the core of Robert C. Martin's *Clean Code* (2008) — whose Part I is organized into ~14 principle *chapters*, not a numbered "10"[1] — folded with **DRY, KISS, YAGNI** (from *The Pragmatic Programmer* / Extreme Programming) and **SOLID** (from Martin's 2000 paper / *Agile Software Development* 2003 / *Clean Architecture* 2017). Three of the ten (KISS, YAGNI, SOLID) are **not chapters in *Clean Code*** at all.[1][2] If a defensible "canonical 10" is needed, cite *Clean Code* (2008) Part I as the backbone and note the cross-source additions.

| # | Principle | One-line definition | How it works in practice (concrete) | Canonical source (tier) |
|---|---|---|---|---|
| P1 | **Meaningful naming** | Names reveal intent; unambiguous, distinguishable, searchable | Rename `d` → `daysBetweenCreationAndModification`; one word per concept; make it `grep`-able | *Clean Code* Ch 2 (Verified TOC) |
| P2 | **Small functions / SRP** | Functions do one thing, short, one abstraction level; one reason for a class to change | Extract Method; split a 200-line function; keep each class single-purpose | *Clean Code* Ch 3 + SOLID-SRP (Verified) |
| P3 | **DRY** | Every piece of knowledge has a single, unambiguous representation | Extract repeated logic into one function; single source of truth | *Pragmatic Programmer* Topic 9 (Verified, text read) |
| P4 | **KISS** | Prefer the simplest solution that works | Pick a plain function over a heavyweight pattern when the simple one works | *Pragmatic Programmer* / US-Navy origin (Plausible) |
| P5 | **YAGNI** | Don't build until actually needed | Ship minimal; add capability only on concrete demand | XP / *Pragmatic Programmer* (Plausible) |
| P6 | **SOLID** | 5 OOP design principles (SRP/OCP/LSP/ISP/DIP) for flexible, maintainable code | Split god class; extend via interface; depend on abstractions (DI) | Martin 2000 / PPP 2003 / *Clean Architecture* (Verified) |
| P7 | **Error handling** | Complete, deliberate; exceptions over codes; no nulls | Throw `UserNotFoundException`; never return null; never swallow | *Clean Code* Ch 7 (Verified TOC) |
| P8 | **Unit testing / TDD** | Tests are first-class; drive development; F.I.R.S.T. | Red–green–refactor; one assert per test; fast/independent/deterministic | *Clean Code* Ch 9 (Verified TOC) |
| P9 | **Refactoring / Boy Scout Rule** | Improve design without changing behavior; leave it cleaner | Small behavior-preserving cleanup on every touch | *Clean Code* Ch 1 + Fowler *Refactoring* (Verified) |
| P10 | **Readability & maintainability** | Code is read ≫ written; write to be read | Team style guide; code reads like prose; peer review | *Clean Code* Ch 1 "We Are Authors" (Verified, text read) |

*Two structural notes from the backbone lane:* (a) anchor #2 fuses a function-level rule (*Clean Code* Ch 3 "Do One Thing") with a class-level SOLID rule (SRP) — related but distinct; (b) SOLID is a **meta-principle** (5 sub-principles under one mnemonic), structurally different from the other nine.[1]

---

## 2. The agent-paradigm verdict matrix (Facet B — the core answer)

**Framing.** For each principle, the agent paradigm does one of four things: **AMPLIFIED** (matters more, with a new mechanism), **MOOT** (de-emphasized to noise), **INVERTED** (polarity flipped — the agent's default runs opposite to the human instinct), or **STILL-USEFUL** (transfers unchanged). The dominant mechanism behind nearly every verdict is the **context window**: a fixed, scarce, metered resource where distracting context harms performance.[12][15]

| # | Principle | Verdict | Mechanism (why) | Strongest evidence (tier) | Practical implication for agents |
|---|---|---|---|---|---|
| P1 | Naming | **AMPLIFIED** (emphasis → *searchable/unique*) | Agents navigate by `grep`/repo-map; a distinctive name returns few hits → the agent goes straight to the target | Le et al. 2025: uninformative renames dropped GPT-4o summarization 87.3%→58.7% (Verified, quantified)[9]; Aider repo map surfaces most-referenced symbols (Verified)[17] | Prefer unique, specific names over `data`/`handler`/`Manager`; "if you `grep` the name and a lot of irrelevant stuff comes back, the name is bad"[22] |
| P2 | Small functions / SRP | **AMPLIFIED** (→ *technical obligation*) — with a *cohesion* caveat | A small unit fits in one read/tool-call without truncation → full attention; an 800-line 3-thing class is worse than three 250-line classes | Agent CLIs cap file reads (~2000 lines/chunk) (Verified)[22]; Cursor rule "keep components under 200 lines" (Verified)[18] | Keep functions/files small **and cohesive** — agents satisfy the *letter* (small) while violating the *spirit* (cohesion)[26] |
| P3 | DRY | **AMPLIFIED** (duplication breaks edit consistency) — with an *over-DRY* caveat | When changing replicated logic the agent updates one copy and misses the others (no "two more copies" gravity) | akitaonrails field report (Verified)[22]; Aider repo map rewards shared abstractions (Verified)[17] | Factor shared logic **and** pair DRY with YAGNI — agents over-DRY into brittle premature abstractions[22][23] |
| P4 | KISS | **INVERTED pressure** (must be imposed) | An unfettered reviewer/agent over-abstracts; deep abstraction stacks cost the agent more tokens than a direct implementation | Claude Code docs warn chasing every finding → over-engineering (Verified)[15]; orbitant: 20 abstraction layers cost more than a KISS impl (Verified)[24]; Cognition: the single-threaded linear agent is the reliable KISS design (Verified)[20] | Explicitly tell the agent/reviewer to flag only correctness gaps, not every possible abstraction[15] |
| P5 | YAGNI | **INVERTED pressure** (same mechanism as P4) | Chasing imagined edge cases builds features/tests that can't happen | Claude Code docs (Verified)[15]; OpenAI: "add tools only when they unlock a real workflow" (Verified)[19] | Add rules/tools/abstractions only after real, repeated friction[19][15] |
| P6 | SOLID | **AMPLIFIED** (each principle saves context window) | SRP (fewer things to track), OCP (write new code to plug in, don't edit existing), DIP (abstractions more concise than concretions), DI = isolation scope for tests | First-principles argument (Plausible)[22]; DI "isolation scope" field example (Verified)[22]; Cursor composition rules (Verified)[18] | Encode SRP/composition/DI as rules; agents are weak at interface design (design APIs from the storage view, not the consumer's)[26] |
| P7 | Error handling | **AMPLIFIED** (rich messages = debug signal) **+ INVERTED** (defensive code only when asked) | The agent uses the stack trace as its primary debug signal — a vague message costs an extra reasoning round; but on its own it implements the happy path and won't propose retries/breakers | akitaonrails (Verified)[22]; SWE-agent integrates a linter into the edit action for error feedback (Verified)[12]; Cursor structured-error rules (Verified)[18] | Make exception messages carry the offending value + expected shape; **enumerate** defensive cases in the rules file — don't expect the agent to invent them[22] |
| P8 | TDD / testing | **AMPLIFIED** (→ central safety mechanism) — with a key distinction | Without a runnable check the *human* is the verification loop; headless tests or the agent "goes blind" | Claude Code "give it a check it can run" (Verified)[15]; akitaonrails: 274 commits / 1,323 tests, CI caught 50+ bugs (Verified)[22]; AGENTS.md auto-runs listed test commands (Verified)[16] | **Value of a pre-existing/runnable suite ≠ agent-authored throwaway tests** — the latter are mostly observational and don't move outcomes (Verified)[14] |
| P9 | Refactoring / Boy Scout | **AMPLIFIED** (tests make refactoring safe) | "Factoring… is automated-refactor safety"; continuous agent edits need a regression net | akitaonrails (Verified)[22]; Claude Code ships a `code-simplifier` plugin (Verified)[23]; SWE-CI: quality decisions compound over evolution (Verified)[3] | Run cleanup as an explicit, separate pass (agents are reluctant to delete); use agents to clean first, then gate[23][27] |
| P10 | Readability / maintainability | **SPLIT: INVERTED + MOOT + AMPLIFIED** | Code is read ≫ written — now by an agent that reads it many times a day; but comments flip to *provenance context*, formatting goes to *noise*, and "write clean code" as a rule is *redundant* | Comments-as-provenance (Verified)[22]; README/AGENTS.md two-audience split (Verified)[16]; "write clean code" is in the EXCLUDE list (Verified)[15] | Keep WHY/provenance comments (don't prune the agent's own); adopt the default formatter and stop debating style; don't restate clean code in the rules file[22][15] |

**Two NEW agent-era principles surfaced (not in the canonical 10):** **explicit types** (typed code is an "answer key" that saves the agent's inference — Plausible)[22] and **predictable directory structure** (framework conventions let the agent anticipate paths without exploring — Verified)[22].

**Cross-cutting headline:** the AMPLIFIED verdicts are all ways to *shrink the context the agent must hold to do one job correctly*; the MOOT verdicts are things that *don't change that budget*; the INVERTED verdicts are where the agent's *default* runs opposite to the human instinct and must be corrected by explicit rules.[22][15]

---

## 3. Three convergent lines of evidence

The five lanes attack the question from independent angles; they converge, which is what makes the answer robust.

**Line 1 — Research papers (LANE-2 + verification LANE2-1/2).** The field does *not* organize around "the 10 principles"; it uses ISO/IEC 25010 attributes + static metrics (SonarQube, Pylint, Maintainability Index). The load-bearing results: **SWE-CI** shows clean/extensible code is *rewarded* on future modifications while technical debt degrades — and this is **invisible on snapshot benchmarks** like SWE-bench, which measure issue resolution, not quality[3][11], and enterprise codebase complexity sharply reduces agent success[13]. LLM code is **"superficially clean but intrinsically complex"** — better on Pylint (surface), worse on the Maintainability Index (deep)[3]. **Agent-authored tests are mostly observational and don't move outcomes**[14]. And the "locally clean, globally incoherent" phenomenon is documented as the **Modular Mirage / architectural rot**[6], **Architectural Erosion / Hallucinated Coupling**[7], and a growing literature[8].

**Line 2 — World-leading AI developers & vendors (LANE-3).** Overwhelmingly pro-clean-code, converging on **three mechanisms**: (a) **a machine-runnable check** (tests/build/linter) gated by a **pre-commit hook / CI the agent cannot bypass** — because a rule in CLAUDE.md/AGENTS.md "is only a suggestion it can skip"[15][23]; (b) **keep the instruction file short, specific, and pruned** — bloat makes the agent ignore it[15][19]; (c) **treat the codebase itself as the agent's context** — its quality "sets a ceiling" on output[23]. The field has **standardized on a shared instruction file** (AGENTS.md, now Linux-Foundation-stewarded) that works across Codex, Claude Code, Cursor, Devin, Aider, Copilot, etc.[16] Simon Willison's one-line thesis: *"Clean code is the way. Less docs. Linters define the style. Tests define the intent. Code defines the architecture."*[21]

**Line 3 — Community practitioners (LANE-4).** **Bimodal.** The **majority** view: clean code matters *more*, with the reason shifted from "another human reads it" to "the agent's context/token budget reads it"[27][26]. A **vocal minority** argues it's moot ("you're not supposed to touch the code anymore") — a genuine, documented position, not a strawman[26][27]. The **counterintuitive** finding: locally-clean-but-globally-incoherent "meta-code" spaghetti[27]. And a new de-facto role — the **"code janitor" / AI-code-remediation engineer** — is already reported by multiple practitioners[28], and code review is becoming the engineer's first look at the code[25].

**How they converge:** the papers' "quality decisions compound over evolution"[3] + the practitioners' "meta-code spaghetti"[27] + the research's "architectural rot / Modular Mirage"[6] are the *same phenomenon* seen from three directions. The papers' "give the agent a runnable check / clean interface helps"[12] + the vendors' "pre-commit hook the agent can't bypass"[15][23] + the practitioners' "linters/hooks/CI are what hold"[26] are the *same prescription*. Two independent lines of evidence (measured + observed) point the same way.

---

## 4. Options matrix — how to make Clean Code work for AI agents

The research question reduces, operationally, to: *given that clean code transfers (with the verdicts above), what should a team actually DO?* There are five feasible options, from doing nothing to the full stack. Each is assessed on mechanism, prerequisites, key steps, confidence per part, verification status, and trade-offs.

### Option 1 — Do nothing: "clean code is moot for agents"
- **Mechanism:** Bet that agents will rewrite/refactor cheaply enough that code quality stops mattering — analogized to how memory-layout care became irrelevant with "unlimited" memory.[26]
- **Prerequisites:** Belief that agent comprehension is unbounded and free; acceptance of "garbage code only the AI can make sense of."[27]
- **Key steps:** None — let the agent generate and merge.
- **Confidence per part:** The *position* is documented (Verified as a real minority view)[26]; its *premises* are **Speculative** — practitioners who tried "a two-sentence prompt fixes a million-line codebase" found it does not work at scale[26], and the research shows incoherence *accumulates* over iterations[6][10].
- **Verification status:** community-reported minority position; **contradicted** by the measured Sonar efficiency result[5] and the architectural-rot research[6].
- **Trade-offs:** Zero upfront cost; high long-term cost (comprehension debt, rising token bills, unreviewable code). The "code janitor" role is what this option produces.[28]

### Option 2 — Encode clean-code rules in the instruction file (AGENTS.md / CLAUDE.md / .cursor/rules)
- **Mechanism:** Because LLMs have no persistent memory between completions, persistent context must be re-injected at the prompt level; a short, pruned rules file tells the agent the project's non-obvious conventions.[18][16]
- **Prerequisites:** A shared, version-controlled instruction file (AGENTS.md is the cross-agent standard)[16]; discipline to keep it short.
- **Key steps:** Write short, imperative rules for the *delta* from defaults (naming, structure, error-handling, test command); prune ruthlessly — "for each line, would removing this cause a mistake? If not, cut it"; add rules only after repeated mistakes.[15][19]
- **Confidence per part:** The mechanism is **Verified** — all major vendors document it[15][16][18]. Its *sufficiency* is **Plausible-to-weak**: it is advisory prose the agent can skip[23], and the research shows detailed prompting does **not** mitigate architectural decay[6].
- **Verification status:** documented by every major vendor (Verified); its limits are documented too ("write clean code" is in the EXCLUDE list; bloated files get ignored)[15].
- **Trade-offs:** Cheap, portable, fast to start; but **advisory** — the agent half-ignores long files and skips rules under load. Necessary but not sufficient.

### Option 3 — Enforce with machine-runnable checks (linters, tests, pre-commit hooks, CI, architectural linters)
- **Mechanism:** A rule written in a markdown file "is only a suggestion it can skip, because to the model it is just more text in the prompt"; the gate that holds is the one the agent **cannot bypass** — a pre-commit hook / CI that exits non-zero on failure.[23][15]
- **Prerequisites:** A deterministic check (test suite, build, linter, type-checker, dead-code detector, complexity check) the agent can run headless; a hook/CI wiring it to block bad commits.
- **Key steps:** Write one script (linters + dead-code + complexity + tests, exit non-zero on failure); give the agent the command; install the same script as a pre-commit hook; optionally a Stop-hook that blocks the turn from ending until the check passes.[23][15] Add **architectural** linters (Konsist, Harmonize, ArchUnit-style) to catch the *global* incoherence that per-file linters miss.[26][7]
- **Confidence per part:** **Verified** across vendors and practitioners — Claude Code hooks are "deterministic and guarantee the action happens"[15]; practitioners report "hundreds of architectural lint rules that the AI will violate, read, and correct"[26]; the research concludes "without automated architectural linting… accelerates the accumulation of structural technical debt"[7].
- **Verification status:** the most strongly-supported option (Verified, multi-source, and the only one the research says actually holds).
- **Trade-offs:** Higher setup cost; requires the checks to be headless and fast; but it is the **only** option that closes the loop the agent can't close itself, and it catches the global-incoherence failure mode that prompting can't.

### Option 4 — Treat the codebase itself as the agent's context (clean the codebase)
- **Mechanism:** "A coding agent learns your project's conventions from the code it reads, so the quality of that code sets a ceiling on the quality of what it writes"[23]; clean, well-named, small, well-abstracted code makes the agent land a change in 1–2 tries instead of many.
- **Prerequisites:** A codebase that can be modularized/cleaned (the 2M-line spaghetti case needs modularization first, not a smarter model)[26].
- **Key steps:** Modularize so the agent can process one unit at a time; name things for `grep`; keep files small; prefer deep modules (hide a lot behind a small interface) over shallow fragmentation; use the agent to clean first, then gate the result.[23][22]
- **Confidence per part:** **Verified** and **quantified** — the Sonar study: clean codebases → 7.1% fewer input tokens, 8.5% fewer output, 11.1% less reasoning, ~34% fewer file revisits, same pass rate[5][4]; naming effect quantified at 87.3%→58.7%[9].
- **Verification status:** the only option with a controlled, primary-verified measurement — but it is a **vendor** study, one model (Sonnet 4.6), one harness (Claude Code), six pairs, wide per-task variance (−47% to +44%), with a counterexample and token-neutral hotspots[5].
- **Trade-offs:** Pays off in *efficiency* (tokens, latency, revisits), **not** in pass rate[5]; one-time + ongoing investment; the effect is directional, not universal.

### Option 5 — The full stack (2 + 3 + 4, applied together) — **RECOMMENDED**
- **Mechanism:** Use the instruction file for the *delta* (Option 2), enforce invariants mechanically (Option 3), and raise the codebase's own quality so the agent starts from a good context (Option 4). Each layer covers the others' blind spots: prose is advisory (→ hooks), hooks catch local smells (→ architectural linters catch global incoherence), a clean codebase reduces the context the agent must hold (→ all of the above get cheaper).
- **Prerequisites:** All of the above; a team willing to maintain the rules file and the gates.
- **Key steps:** (1) Modularize/clean the codebase and use the agent to help[23]. (2) Write a short AGENTS.md with the non-obvious rules + the test command[16][15]. (3) Wire linters + tests + **architectural** linters into a pre-commit hook / CI the agent can't bypass[23][26][7]. (4) Pair DRY with YAGNI and impose KISS on the review loop to stop over-engineering[15][22]. (5) Keep WHY/provenance comments, prune the rules file regularly, and schedule maintenance/reflection passes[22][19].
- **Confidence per part:** Each component is **Verified** (see Options 2–4); the *combination* is the practitioners' and vendors' de-facto consensus (Verified as a convergent practice)[15][23][26][21].
- **Verification status:** the only option consistent with **all three** evidence lines (papers, vendors, community) and the one the research says actually holds against the global-incoherence failure mode[6][7].
- **Trade-offs:** Highest upfront cost; but it is the only option that addresses the *global* (not just local) failure mode, and it compounds — a cleaner codebase makes every subsequent agent run cheaper[5][10].

**Ranking & recommendation.** **Option 5 (the full stack)** is recommended, then Option 3, then Option 4, then Option 2; **Option 1 is not recommended** (its premises are contradicted by the measured and research evidence). **Rationale:** the single most dangerous failure mode is *global* incoherence that local checks and prompting both miss[6][7][27] — only **Option 3's architectural linters + CI** catch it, and only **Option 4's clean codebase** makes the agent affordable to run repeatedly[5]. Option 2 alone is advisory and skippable[23]; Option 1 produces the "code janitor" end-state[28]. The full stack is the only configuration that is consistent with all three independent evidence lines.

---

## 5. Key tensions (presented as tensions, not contradictions)

1. **"Agents don't write clean code by default" vs "LLMs pick up the style in your repo."** Both are true: the *default* output is "average" (80-line functions, no DI, duplication, 2000-line files)[22][23], but a *clean, well-organized* repo is picked up and rewarded[23][5]. The default is the floor; the codebase is the ceiling.
2. **"Small functions" (the letter) vs "cohesive" (the spirit).** Agents satisfy "small" while violating cohesion — "they think 'Clean Code' means splitting into tiny functions, rather than cohesive functions"[26] and over-DRY into brittle premature abstractions[22]. The research names this the **Modular Mirage**[6].
3. **DRY vs over-DRY / duplication-as-context.** The agent's failure is *missing* duplicate copies on edit (favors DRY)[22], but it also *over*-applies DRY[22]; a minority argues repetition may be cheaper for an agent than a leaky abstraction[26]. The literature resolves toward DRY + YAGNI, not intentional duplication.
4. **Surface readability ≈ human vs deep maintainability < human.** Atlassian (HULA) finds LLM code *comparable* to human on surface readability metrics, while SWE-CI finds LLM code *worse* on the Maintainability Index — both true, different metrics (surface vs deep).[3]
5. **Clean code helps efficiency vs clean code doesn't change pass rate.** The Sonar study shows a real token/revisit reduction **and** no pass-rate change — the payoff is *efficiency*, not *success*.[5]

---

## 6. What remains untested on the exact target

The research question names specific agents (Claude Code, OpenAI Codex, Cursor, Devin, SWE-agent, Aider). The evidence is strong but has these on-target gaps, stated plainly:

- **The commercial agents are not directly benchmarked for the global-incoherence phenomenon.** The research that documents it (AI-Generated Smells[6], Technical Debt in LLM Architectures[7]) used **MetaGPT-generated systems** and **generated microservices**, not the specific named commercial agents in a real production repo. The phenomenon is research-validated *in general* but not yet measured on Claude Code / Cursor / Devin output specifically.
- **The quantified efficiency anchor is single-source and narrow.** The Sonar study is a **vendor** study, **one model** (Claude Sonnet 4.6), **one harness** (Claude Code), **six repo pairs**, with wide per-task variance (−47% to +44%) and a documented counterexample[5]. No independent lab has replicated the 7.1%/8.5%/34% figures.
- **No controlled A/B isolates a single principle.** There is no study that varies *only* naming, or *only* DRY, or *only* SOLID, and measures the effect on agent generation *correctness* (as opposed to efficiency). Per-principle effect sizes are inferred from the metric-based papers, not isolated experiments.[3]
- **The "globally incoherent" research is small-N or off-target.** Technical Debt in LLM Architectures is a **pilot** (N=5 runs/model, one task)[7]; AI-Generated Smells uses CodeContest + MetaGPT, not the named agents[6].
- **SWE-CI's specific body observations** (15/20 Pylint vs 20/20 MI, zero-regression rate) rest on LANE-2's full read; this run independently confirmed the paper's existence and abstract at the primary[3] but did not re-read the body.
- **Devin-specific and Copilot-instructions first-party clean-code guidance** was not located (covered only via the AGENTS.md compatibility list).

---

## Appendix — corpus map (per-finding citations live here)

| File | Axis / sub-question | Findings |
|---|---|---|
| `principles/lane1.md` | Facet A — the canonical 10 principles + how each works | 51 |
| `papers/lane2.md` | Facet B — research papers on clean code & LLM code quality | 17 |
| `practice/lane3.md` | Facet B — world-leading AI devs' & vendors' practical experience | 67 |
| `community/lane4.md` | Facet B — community practitioner experience (Reddit/HN/SO) | 46 |
| `agent-mechanisms/lane5.md` | Facet B — clean code × agent architecture (AMPLIFIED/MOOT/INVERTED) | 61 |
| `verification/lane2-1.md` | Verify the two load-bearing anchors (SonarSource, SWE-CI) at primary | in-session |
| `papers/lane2-2.md` | Is "locally clean but globally incoherent" backed by research? | in-session |

*Language note:* this report and all lane files are in English — the language the research was produced in (per the project archive convention that research results stay in the language they were produced in).

## Sources

[1] https://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884 — Clean Code (2008) — publisher TOC
[2] https://en.wikipedia.org/wiki/SOLID — Wikipedia: SOLID
[3] https://arxiv.org/abs/2603.03823 — SWE-CI (Chen et al. 2026)
[4] https://arxiv.org/abs/2605.20049 — Does Code Cleanliness Affect Coding Agents? (Sonar study)
[5] https://www.sonarsource.com/blog/your-ai-bill-is-a-code-quality-problem — SonarSource: Your AI bill is a code quality problem
[6] https://arxiv.org/abs/2605.02741 — AI-Generated Smells (Zhu, Tsantalis, Rigby 2026)
[7] https://arxiv.org/abs/2512.04273 — Quantitative Analysis of Technical Debt in LLM Architectures (Slater 2025)
[8] https://arxiv.org/abs/2606.14796 — Faster Code, Deeper Debt? (multivocal review 2026)
[9] https://arxiv.org/abs/2510.03178 — Le et al. 2025 — identifier naming effect
[10] https://www.scbench.ai — SlopCodeBench
[11] https://arxiv.org/abs/2310.06770 — SWE-bench (2023)
[12] https://arxiv.org/abs/2405.15793 — SWE-agent (Princeton, NeurIPS 2024)
[13] https://arxiv.org/abs/2509.16941 — SWE-Bench Pro (Scale, 2025)
[14] https://arxiv.org/abs/2602.07900 — Rethinking Agent-Generated Tests (2026)
[15] https://code.claude.com/docs/en/best-practices — Claude Code best practices (Anthropic)
[16] https://agents.md — AGENTS.md open standard
[17] https://aider.chat/docs/repomap.html — Aider repo map
[18] https://cursor.com/docs/rules — Cursor rules docs
[19] https://developers.openai.com/codex/learn/best-practices — OpenAI Codex best practices
[20] https://cognition.com/blog/dont-build-multi-agents — Cognition: Don't Build Multi-Agents
[21] https://simonw.substack.com/p/how-i-use-llms-to-help-me-write-code — Simon Willison: How I use LLMs to write code
[22] https://akitaonrails.com/en/2026-04-20/clean-code-for-ai-agents — AkitaOnRails: Clean Code for AI Agents
[23] https://aidailycheck.com/learn/clean-code-for-ai-agents — AI Daily Check: Clean Code for AI Agents
[24] https://orbitant.com/en/clean-code-with-ai-agents-best-practices — Orbitant: Clean Code with AI Agents
[25] https://stackoverflow.blog/2026-03-26/coding-guidelines-for-ai-agents-and-people-too — Stack Overflow blog: coding guidelines for AI agents
[26] https://news.ycombinator.com/item?id=47704285 — HN: Clean code in the age of coding agents
[27] https://www.reddit.com/r/ExperiencedDevs/comments/1sibmbw/code_quality_in_the_ai_age — r/ExperiencedDevs: Code quality in the AI age
[28] https://www.reddit.com/r/ExperiencedDevs/comments/1vm2r31/how_many_of_you_are_already_employed_in_ai_code — r/ExperiencedDevs: AI code remediation
