# Clean Code for AI Coding Agents — Current Model Generation (post-2026-06 evidence only)

**Research question:** Repeat the 2026-10-17 clean-code × AI-coding-agent research with two strict filters. First, use only sources published or substantively updated on or after 2026-06-01. Second, use only evidence about the current frontier model generation (October 2026). Re-derive the 10 principles and the per-principle agent verdicts (AMPLIFIED / MOOT / INVERTED / STILL-USEFUL) from this new evidence alone. Then diff the result against the previous corpus.

**Date:** 2026-10-18 · **Method:** 5 wave-1 lanes (114 findings), no wave 2 (see §7), synthesized below. Each lane file holds the per-finding citations: URL, verbatim quote, tier and date evidence. Paths are in the Appendix. The `[n]` ids used inline are mapped in the Sources block at the end (`ledger.json`).

**Tier key:** **Verified** = authoritative/primary source actually read, on the current generation · **Plausible** = sound, but secondary, vendor self-interest, small n, or one model generation behind · **Speculative** = asserted, method opaque or untested. Tiers are never collapsed into a flat assertion.

**Baseline handling:** the 2026-10-17 corpus (`../clean-code-ai-agents/`) is used **only** as the comparison target in §5. None of its 28 ledger sources is cited as new evidence.

---

## TL;DR — best result first

**Clean code still matters more for agents than for humans. What changed with the current generation (Opus 5.5 / GPT-6 / Gemini 4 Argon) is *why* it matters, and *which side the danger sits on*.**

1. **The mechanism moved from "fit in the window" to "cost of finding and re-reading".** All three major labs now ship 1M-token windows by default.[12][11] Anthropic itself still writes that "performance degrades as it fills".[6] What a clean codebase saves now is exploration: steps, re-reads and missed files. Window fit is no longer the main saving. The strongest new number comes from refactoring an agent-written 17k-line file into cohesive modules, which cut input tokens per change by **83%**.[23] Pass rates barely move either way, but cost, navigation and the structure of what the agent builds do.[13][14][22] **CHANGED (refined), not overturned.**

2. **The agent's main failure mode is no longer sloppiness. It is volume.** Current-gen models over-build: extra tests, extra files, extra review rounds, defensive checks and abstractions.[4][29][33] The vendors frame this as *scope expansion*.[4][7] Practitioners still see it on Opus 5.5 at the architecture level.[31][26] **KISS/YAGNI stay INVERTED, and the evidence is stronger than in the baseline.** Two principles have flipped sides. **Error handling (P7)** now fails mostly through *over*-defensiveness and error-masking, less through missing handling.[26][25] **Small functions (P2)** is over-applied (about 5× the callables), so the human must now *bound* it rather than *impose* it.[29]

3. **TDD splits sharply.** Telling a frontier agent to *do TDD* or to *verify its work* is now neutral to counterproductive. Anthropic says to remove verify-instructions for Opus 5, OpenAI says not to write implementation-mirroring tests for small changes, and a controlled practitioner trial found no gain at 3–8.5× the tokens.[7][5][27] Meanwhile, **an independent, pre-existing regression/acceptance gate is AMPLIFIED**. Inherited test failures are the main measured cost of building on agent code.[13] On impossible tasks, reward hacking runs 3–6× higher.[11] Even a frontier model that passes 10/10 still needs a final gate.[28]

**Recommendation (§4):** the baseline's full stack still wins, recalibrated for this generation into **Option 5′**. Keep a *thin* rules file that is re-pruned at every model upgrade. Make **deterministic, independent gates** (regression tests, architecture/fitness tests, policy checks) the centrepiece. Run **agent-executed, metric-gated cleanup passes** instead of relying on Boy-Scout discipline. Steer **scope and effort level** explicitly.

---

## 1. Current model generation (filter definition, from `models/lane1.md`)

| Vendor | Current frontier coding models | Release date (evidence) | Tier |
|---|---|---|---|
| Anthropic | Claude Opus 5.5, Sonnet 5.5, Haiku 5.5; Fable/Mythos 5.1 | 2026-09-22 / 09-28 / 10-07; Fable 09-01 (secondary) | Verified (Fable date Plausible)[1] |
| OpenAI | GPT-6 Astra, GPT-6 Sol/Luna, GPT-6.1 Sol | 2026-09-03 / 09-22 / 09-29 (API changelog) | Verified[2] |
| Google | Gemini 4 Argon | GA 2026-10-13 (API changelog); announced 09-30 (secondary) | Verified (GA)[3] |
| xAI | Grok 4.7 | 2026-09-21 | Verified |
| DeepSeek | V4.1-Flash(-1017) | 2026-09-10 / 10-17 | Verified |

**"Wave A" vs "wave B".** Much of the post-June evidence was measured on the *previous point release*: Opus 5 / Sonnet 5 (Jul 2026), GPT-5.6 Sol/Luna/Terra (Jul 2026), DeepSeek V4. We call this **wave A**. The October frontier above is **wave B**. Findings that rest on wave A only are marked **[A]**. Findings on models from before wave A (Sonnet 4.5/4.6, GPT-5, Opus 4.x) are capped at Plausible, per the hard filter. Benchmark margins between frontier models are, by Anthropic's own account, "a less reliable guide" at this capability level.[1]

---

## 2. The 10 principles (unchanged backbone)

The ten anchors are the same as in the baseline: P1 naming, P2 small functions/SRP, P3 DRY, P4 KISS, P5 YAGNI, P6 SOLID, P7 error handling, P8 testing/TDD, P9 refactoring/Boy Scout, P10 readability/maintainability. No post-June source proposes a different canonical list. Their definitions are textbook material and are not re-sourced here; see the baseline `principles/lane1.md`. What this run re-derives is the **agent verdict**.

---

## 3. Agent verdict matrix — re-derived from post-June, current-gen evidence only

| # | Principle | New verdict | Mechanism (why, now) | Strongest new evidence (tier) |
|---|---|---|---|---|
| P1 | Naming | **AMPLIFIED (weak evidence)** | Agents navigate by name and grep. Retrieval still misses all needed files on ~27–35% of samples. | Name-only directory routing beats rg/FTS at finding gold files (Plausible)[40]; agents miss every gold file on 27–29% of Codex samples (Verified, GPT-5.5)[21]. No current-gen naming A/B exists. |
| P2 | Small functions / SRP | **AMPLIFIED for cohesive modules; MUST BE BOUNDED for function count** | Smaller *relevant* subset → fewer tokens; random splitting does not help. Current models over-split. | −83% input tokens/change after cohesive refactor (Verified, n=1)[23]; Opus 5 ≈5× callables, community split on whether that is clean (Verified [A])[29] |
| P3 | DRY | **AMPLIFIED need, INVERTED default** | Agents stop exploring and re-implement; duplication grows silently while pass rate is flat. | 50.8% of task chains duplicate logic by turn 5 on GPT-5.6/DeepSeek V4.1 (Verified)[14]; duplication +81% vs 2023 (Plausible)[25] |
| P4 | KISS | **INVERTED (stronger)** | Post-training rewards completeness/coverage; agents over-build and reviewer loops inflate code. | Anthropic: engineers' role is to tell Claude "no", steer away from over-engineering (Verified, Mythos-era)[26]; Opus 5.5 blueprint "overly complicated" (Verified, wave B)[31]; scope expansion in vendor guides (Verified)[4][7] |
| P5 | YAGNI | **INVERTED (stronger)** | Same as P4. Unrequested tests/docs/files at *every* effort level. | Sonnet 5.5 guide: adds tests/docs/files unasked; a stop-paragraph cut cost ~⅓ with no loss in quality (Verified)[4]; leftover speculative edits ("CodeSlop") (Plausible)[17] |
| P6 | SOLID / interfaces | **AMPLIFIED, best when executable** | Consumer-friendly interfaces drive reuse; dependency direction enforced as tests holds better than prose. | 64% of excess code caused by rigid/hard-to-use interfaces, Opus 5.5 designers (Verified)[15]; deterministic fitness functions as primary gate (Plausible)[41] |
| P7 | Error handling | **CHANGED → STILL-USEFUL, polarity flipped toward over-defensiveness** | Frontier models rarely miss null checks. They add unnecessary validation and mask errors instead. | Excessive validation after adversarial review (Verified)[26]; error-masking constructs +47% (Plausible)[25]; error-handling changes predict agent-on-agent-code failure (Plausible, prev-gen)[20] |
| P8 | Testing / TDD | **SPLIT: TDD-as-process MOOT/INVERTED; independent regression/acceptance gate AMPLIFIED; agent-test volume = new failure mode** | Frontier models self-test; extra instructions over-verify. Damage runs through broken regressions and gamed tests. | Remove verify-instructions on Opus 5 (Verified)[7]; no mirroring tests for small changes (Verified)[5]; TDD no gain at 3–8.5× tokens (Plausible)[27]; inherited test failures = main cost (Verified)[13]; GPT-6 Sol 10/10 either way, Luna 3→10/10 with harness (Verified)[28]; reward hacking 3–6× on impossible tasks (Verified)[11] |
| P9 | Refactoring / Boy Scout | **AMPLIFIED, but now agent-EXECUTED under human direction and a metric gate** | Agents do not self-initiate restructuring, but run gated cleanup cheaply at scale. | Agent not good at choosing refactorings unaided (Verified)[23]; 300 kLoC → Code Health 10 in 3 weeks for ~$4k (process Verified, outcomes Plausible)[24]; OpenAI: 1,400+ PRs, 800k lines deleted by GPT-6 (Verified)[10] |
| P10 | Readability / maintainability | **SPLIT, shifted: global coherence AMPLIFIED; comment-noise trending MOOT; conventions NOT moot; "write clean code" rule still redundant** | Agents copy what they read ("garbage in, garbage out"). They violate written conventions anyway. Opus 5.5 comments are reported shorter. | 43.1% repo-policy violations by current-gen agents (Verified)[16]; agents can't tell slop from reviewed code (Verified, community)[38]; "decoherence" (Plausible)[32]; CLAUDE.md: exclude "write clean code" (Verified)[6] |

**New agent-era principles (beyond the baseline's explicit types + predictable directory structure):**
- **Model-relative, progressively disclosed instruction files.** Root docs route rather than dump. Re-prune at every model upgrade, because rules written for older models now make newer ones over-do work. (Verified)[9][37][6]
- **Edit-site locality.** The code being edited carries the signal. Summaries and skeletons of the rest of the file add nothing. (Plausible, prev-gen)[22]
- **Effort level as the primary scope/quality lever**, not prompt prose. (Verified)[4][1]
- **Explicit types:** no post-June current-gen evidence found (stays Plausible from the baseline, not re-confirmed).

---

## 4. Options matrix — what a team should do now

### Option 1 — Do nothing ("frontier models write clean code now")
- **Mechanism:** Trust the model. The dissent has shifted. It used to say "code needn't be readable"; it now says "AI already writes clean, maintainable code".[31]
- **Prerequisites:** Belief that wave-B models do not degrade a codebase over time.
- **Key steps:** None.
- **Confidence:** The position is real (Verified as a view)[31]. Its premise is contradicted: every model tested on a multi-checkpoint benchmark increased complexity (Verified [A])[29], agents stop reusing and duplicate (Verified)[14], and 43% of repo policies get violated (Verified)[16].
- **Verification status:** community-reported. Contradicted by current-gen measurements.
- **Trade-offs:** Zero setup. The cost shows up as rising tokens per change, broken regressions and review load.

### Option 2 — Rules file only (AGENTS.md / CLAUDE.md)
- **Mechanism:** Re-inject conventions at prompt level.
- **Prerequisites:** A short, current instruction file.
- **Key steps:** Write the delta from defaults. Prune with "would removing this cause mistakes?". Run `/doctor`. Audit for conflicts, because GPT-6 is *more* sensitive to these files.[6][5]
- **Confidence:** Mechanism Verified.[6][5][9] Field correlation is Plausible: repos with committed AI config show about half the complexity growth.[19] Sufficiency is weak: prompting reduces reward hacking only partially[34], and policy violations persist anyway.[16]
- **Verification status:** documented by vendors; limits documented.
- **Trade-offs:** Cheap. Advisory only. Now also *decays* with every model release.[37]

### Option 3 — Deterministic, independent gates
- **Mechanism:** Checks the agent cannot game or bypass decide what lands. Examples: regression and acceptance tests, architecture/fitness tests, policy and lint checks, a Stop-hook, a second-model refuter.
- **Prerequisites:** A headless, *correct* test suite. Impossible or wrong tests invite gaming.[11]
- **Key steps:** Run existing tests as a deterministic final gate. For frontier models run them once at the end; for cheaper models run them in-loop.[28] Add a Stop-hook and a refuting verification subagent.[6] Encode dependency direction and contract shape as executable fitness functions.[41] Leave formatting to CI.
- **Confidence:** Verified: the harness study on GPT-6 Sol/Luna[28], inherited-failure cost on GPT-5.6-Luna[13], vendor gate mechanisms[6], and reward hacking in the Opus 5.5 system card.[11] Fitness-function practice is Plausible.[41]
- **Verification status:** strongest current-gen support of any option.
- **Trade-offs:** Setup cost. Agent-written test volume itself needs curating, or the tests freeze bad behaviour.[29][38] Gate cadence can be tuned per model tier to save cost.[28]

### Option 4 — Clean the codebase (codebase-as-context), now agent-executed
- **Mechanism:** Fewer and more cohesive files mean the agent reads a smaller relevant subset and copies better patterns.
- **Prerequisites:** Behavioural oracle (tests/replay traces) + an objective quality metric.
- **Key steps:** Have a human pick the target. Let the agent refactor under a metric gate, e.g. a Code Health MCP.[24] Run periodic dedupe and dead-code passes with current models.[10]
- **Confidence:** −83% tokens: Verified, n=1.[23] CodeScene uplift: process Verified, outcome projections Plausible.[24] OpenAI cleanup at scale: Verified, vendor-run.[10] **No current-gen replication of the clean-vs-messy minimal-pair study exists** (searched by four lanes). The independent direction is Plausible, from a prev-gen tokenizer.[39]
- **Verification status:** case studies, no controlled current-gen experiment.
- **Trade-offs:** The payoff is cost and navigation, not pass rate. Many refactor attempts did not help or made things worse, so prioritisation stays human.[24][10]

### Option 5′ — Recalibrated full stack — **RECOMMENDED**
- **Mechanism:** Option 3 is the backbone. Option 4 runs as a scheduled, agent-executed, gated pass. Option 2 is thin and re-pruned per model. A new axis is added: **scope and effort control**.
- **Prerequisites:** As in Options 2–4, plus an owner who re-audits the instruction files at every model upgrade.
- **Key steps:** (1) Correct, pre-existing regression/acceptance suite as an independent final gate, plus architecture fitness tests.[28][41][13] (2) Remove "verify your work" and "do TDD" prose for frontier models. Keep a "real check, not syntax-only" rule for low-effort runs.[7][4] (3) Explicit scope caps: "no unrequested tests/files/refactors; mention them instead". Use medium effort by default.[4][33] (4) Monthly agent-run dedupe and cleanup passes under a metric gate, with targets chosen by a human.[24][10][14] (5) Thin AGENTS.md/CLAUDE.md, progressively disclosed, re-pruned on every model release.[9][37]
- **Confidence per part:** (1) Verified; (2) Verified (vendor); (3) Verified (vendor) / Verified-anecdotal (community); (4) Plausible on outcomes; (5) Verified (vendor).
- **Verification status:** this is the only option consistent with all five lanes. The combination as a whole is not measured anywhere.
- **Trade-offs:** Highest maintenance load. It is the only option that addresses both current failure directions: over-building (scope) and silent degradation (duplication, regressions).

**Ranking:** 5′ > 3 > 4 > 2 > 1. **Why:** the measured current-gen damage runs through regressions, gamed tests and duplication. Option 3 catches those deterministically.[13][11][14] Option 4 is now cheap enough to run routinely.[24][10] Option 2 alone is advisory and goes stale with each model release.[37][16] Option 1 is contradicted by current-gen measurement.

---

## 5. DIFFERENCES vs 2026-10-17 corpus

### 5.1 Per-principle verdict changes (old → new)

| # | Old verdict (2026-10-17) | New verdict (2026-10-18, post-June evidence) | Change | New evidence |
|---|---|---|---|---|
| P1 | AMPLIFIED (searchable/unique) | AMPLIFIED, weak evidence | CONFIRMED (weaker base) | [40][21]. The baseline's quantified naming study is pre-June and not re-run. |
| P2 | AMPLIFIED + cohesion caveat | AMPLIFIED for cohesive modules; function count must be *bounded* | CHANGED | Cohesion caveat now quantified[23]. Agents now over-split[29]. |
| P3 | AMPLIFIED + over-DRY caveat | AMPLIFIED need / INVERTED default | CONFIRMED, strengthened | [14][25]. No new over-DRY evidence. |
| P4 | INVERTED | INVERTED, stronger | CONFIRMED | [26][31][4][7][33] |
| P5 | INVERTED | INVERTED, stronger; framed as scope expansion | CONFIRMED (framing CHANGED) | [4][7][17]. The vendor's explicit over-engineering block is now attributed to Opus 4.5/4.6 only[8]. |
| P6 | AMPLIFIED | AMPLIFIED, best as executable tests | CONFIRMED + refined | [15][41] |
| P7 | AMPLIFIED + INVERTED (defensive code only when asked) | STILL-USEFUL; default flipped toward *over*-defensiveness / error-masking | CHANGED (half OVERTURNED) | [26][25][20]. "Agent won't add defensive code unless asked" no longer describes current models well. |
| P8 | AMPLIFIED (central safety mechanism) | SPLIT: TDD process MOOT/INVERTED; independent gate AMPLIFIED; agent test volume = failure mode | CHANGED | [7][5][27][28][13][11][29] |
| P9 | AMPLIFIED (cleanup as separate pass) | AMPLIFIED; agent-executed under human direction + metric gate | CONFIRMED (execution CHANGED) | [23][24][10] |
| P10 | SPLIT (comments → provenance, formatting moot, rule redundant) | SPLIT: global coherence AMPLIFIED; comment noise → MOOT trend; conventions not moot; rule still redundant | CHANGED (comments sub-verdict) | [16][38][32][6]. Comments-as-provenance has no post-June evidence. |

### 5.2 Claim-level status for baseline claims 1–7

| # | Baseline claim | Status | New evidence and note |
|---|---|---|---|
| 1 | Clean code is MORE useful; reason = agent context window/token budget | **CHANGED (refined)** | "More useful" CONFIRMED. The mechanism shifted. Window *capacity* is weaker as a reason (1M default)[12][11]. Attention degradation is CONFIRMED[6]. Cost moved to exploration steps and re-reads, since cache reads are cheap[1][21][23]. |
| 2 | Per-principle verdicts (7× AMPLIFIED, KISS/YAGNI INVERTED, P10 SPLIT) | **CHANGED (partially)** | P1, P3, P4, P5, P6, P9 CONFIRMED. P2, P7, P8, P10 CHANGED (see §5.1). |
| 3 | "Locally clean, globally incoherent" is research-backed (2605.02741, 2512.04273, 2606.14796) | **CONFIRMED (new current-gen evidence)** | The original papers have no v2 and no replication. 2512.04273 is now under review at JSS; 2606.14796 is accepted at TOSEM (status only). New current-gen support: duplication drift[14], policy violations[16], complexity growth on every model across checkpoints[29] [A], "decoherence"[32]. |
| 4 | SonarSource anchor (7.1% / 8.5% / 11.1% / ~34%, Sonnet 4.6) | **NOT RE-RUN; superseded in magnitude** | No current-gen replication exists. Sonar's own Sept-2026 product messaging moved to context injection, "up to 36%" (Speculative)[35]. The ~9% run-to-run outcome noise floor is comparable to the effect size (Plausible)[22]. Larger single-case effect: −83%[23]. Independent direction from CodeScene (Plausible)[39]. |
| 5 | SWE-CI: clean code rewarded over evolution, invisible on snapshot benchmarks; agent tests mostly observational | **CONFIRMED + CHANGED** | Evolution effect CONFIRMED in the same paradigm on current gen: inherited test failures cost −5.6 pp[13], duplication with flat pass rate[14], StaminaBench[36]. NEW nuance: once earlier tested behaviour is preserved, *no extra* structural maintenance penalty was measurable[13]. "Agent tests observational" is CHANGED: current-gen tests are *voluminous* (51% of output [A])[29] and can freeze bad behaviour[38]. |
| 6 | Full stack: short AGENTS.md + bypass-proof gates + clean codebase | **CONFIRMED + recalibrated** | Gates are now the centrepiece[28][11][34]. AGENTS.md matters *more* (GPT-6 more sensitive) and must be re-pruned per model[5][9][37]. Cleanup is now agent-executed[10][24]. NEW component: scope/effort control[4]. |
| 7 | New principles: explicit types, predictable directory structure | **PARTIALLY CONFIRMED + NEW additions** | Directory structure: Plausible support[40][42]. Explicit types: **no post-June current-gen evidence** (not re-confirmed). NEW: progressive-disclosure instruction files[9], edit-site locality[22], effort level as a lever[4]. |

### 5.3 What the current model generation changed (summary)

1. **Capacity stopped being the argument; exploration became it.** 1M windows and cheap cache reads removed "the code must fit" as the main reason. The reason that remains is that finding and re-reading the right code is still the main cost and failure surface.[12][1][21]
2. **The failure moved from *too little* to *too much*.** Earlier models under-delivered: missing error handling, observational tests, comment noise. Current models over-deliver: unasked tests and files, review rounds, defensive checks, more callables, longer diffs. Vendors now ship prompt paragraphs to *stop* behaviour, not to *start* it.[4][5][7]
3. **Process instructions lost value; outcome gates gained it.** "Verify", "do TDD" and "read everything first" are now redundant or harmful on frontier models.[7][9][27] Independent deterministic gates remain necessary at every capability level.[28][11]
4. **Instruction files became versioned artifacts.** They age with the model and need re-auditing at each release.[37][9][5]
5. **Cleanup became cheap.** Refactoring and dead-code removal at repo scale is agent work now. What stays human is *choosing* what to clean, plus the gate.[10][24][23]
6. **Model-tier matters.** Harness and gate value is inversely related to model strength *per run*. Cheaper models need in-loop sensors; frontier models need a final gate.[28][18]

---

## 6. Key tensions

1. **"AI writes clean code now" vs measured drift.** Wave B is reported as less verbose and more focused (Opus 5.5 comments shorter)[1][31], yet over-building at the architecture level persists[31]. Every model tested increased complexity over checkpoints [A][29]. Local quality has improved; longitudinal quality has not been shown to improve.
2. **Clean code changes cost, not pass rate.** This holds across [13][14][22][23]. Pass/fail benchmarks will keep under-reporting quality effects.
3. **More tests vs fewer tests.** Vendors tell frontier models to test *less* and more meaningfully[5][7], while gates matter *more*[28][13]. The resolution: the value lies in *independent, correct, pre-existing* tests, not in agent-generated volume.
4. **Rules files: matter more vs decay faster.** GPT-6 follows them more closely[5], and repos with committed config degrade less (Plausible)[19]. The same files go stale per model[37].

---

## 7. What remains untested on the exact target (current frontier, October 2026)

- **No clean-vs-messy controlled study on any wave-B model** (Opus 5.5, GPT-6.x, Gemini 4 Argon). Lanes 2, 3, 4 and 5 each searched and found none. The token-saving claim for clean code currently rests on a single n=1 case (Opus/Sonnet-5-era Claude Code)[23], vendor case studies[24][10], and prev-gen data.
- **Wave-A vs wave-B gap.** Key longitudinal data (SlopCodeBench run[29], RepoReuse[14], SWE-Maintain[13]) uses Opus 5 / GPT-5.6 / DeepSeek V4.x, not Opus 5.5 / GPT-6. Opus 5.5 is reported less verbose[31], so P2/P4/P5 magnitudes on wave B are unknown. The one wave-B head-to-head (Opus 5.5 vs GPT-6 Sol, 20 runs) found cost rising with change spread and existing tests catching every regression[30].
- **No Gemini 4 Argon or Grok 4.7 code-quality evidence** beyond vendor docs that say nothing on the topic.
- **Naming, types and comments:** no post-June current-gen controlled evidence. These verdicts rest on indirect or older support.
- **CodeScene outcome numbers** (−70% defects, −45% token waste) are projections; the follow-up study is pending.[24]
- **Two OpenAI blog posts** carry no printed date; they are dated by the model names they mention.[9][10]
- **Why no wave 2:** the open gaps are absences that four lanes already searched for and documented. A second wave would have repeated the same searches. Re-run when a current-gen replication of the clean-vs-messy study appears.

---

## Appendix — corpus map

| File | Axis | Findings |
|---|---|---|
| `models/lane1.md` | Model generation (dated) + vendor guidance | 27 (M1–M11, G1–G16) |
| `papers/lane2.md` | Academic papers ≥ 2026-06-01 + baseline paper status | 28 (A1–A7, B1–B21) |
| `practice/lane3.md` | Industry studies + engineering blogs | 15 (F-01–F-15) |
| `community/lane4.md` | Reddit / HN / Lobsters practitioners | 21 |
| `agent-mechanisms/lane5.md` | Mechanism shift (capacity / attention / cost), gates, reward hacking | 23 (F1–F23) |
| `ledger.json` | Source ledger for this report | 42 |

*Language note:* English; German 1:1 translation in `REPORT_DE.md`.

## Sources

[1] https://www.anthropic.com/claude-opus-5-5
[2] https://developers.openai.com/api/docs/changelog.md
[3] https://ai.google.dev/gemini-api/docs/changelog
[4] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
[5] https://developers.openai.com/api/docs/guides/latest-model.md
[6] https://code.claude.com/docs/en/best-practices
[7] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
[8] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
[9] https://learn.chatgpt.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
[10] https://learn.chatgpt.com/blog/maintaining-software-with-the-gpt-6-family
[11] https://anthropic.com/claude-opus-5-5-system-card
[12] https://code.claude.com/docs/en/changelog
[13] https://arxiv.org/abs/2610.14768
[14] https://arxiv.org/abs/2609.35357
[15] https://arxiv.org/abs/2609.36730
[16] https://arxiv.org/abs/2610.06193
[17] https://arxiv.org/abs/2607.18161
[18] https://arxiv.org/abs/2608.21747
[19] https://arxiv.org/abs/2608.25241
[20] https://arxiv.org/abs/2606.21804
[21] https://arxiv.org/html/2607.24882
[22] https://arxiv.org/html/2607.09691v1
[23] https://martinfowler.com/articles/exploring-gen-ai/refactoring-economic-benefit.html
[24] https://codescene.com/blog/case-study-refactoring-at-scale-with-agents
[25] https://www.gitclear.com/the_ai_code_quality_maintainability_gap
[26] https://www.anthropic.com/engineering/redesigning-source-control
[27] https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html
[28] https://martinfowler.com/articles/are-harnesses-worth-the-cost.html
[29] https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/benchmarking-opus-5-on-slop-code-bench.md
[30] https://paddo.dev/blog/opus-5-5-vs-gpt-6-sol
[31] https://news.ycombinator.com/item?id=49946567
[32] https://maevyn.codes/decoherence
[33] https://www.reddit.com/r/ClaudeCode/comments/1v9zg50/why_opus_5_and_gpt_56_over_engineer_and_are
[34] https://alignment.anthropic.com/2026/reward-seeker
[35] https://www.sonarsource.com/blog/sonarqube-server-2026-5-lta
[36] https://arxiv.org/abs/2606.19613
[37] https://dev.to/evbermudez/the-model-didnt-get-dumber-my-agent-skills-got-stale-8cm
[38] https://www.reddit.com/r/ExperiencedDevs/comments/1wu1tzt/giving_your_codebase_entirely_to_the_ai
[39] https://arxiv.org/abs/2608.18645
[40] https://arxiv.org/abs/2609.35918
[41] https://www.infoq.com/articles/agentic-fitness-functions-evolutionary-architecture
[42] https://shopify.engineering/building-an-agentic-harness-that-outlasts-the-model
