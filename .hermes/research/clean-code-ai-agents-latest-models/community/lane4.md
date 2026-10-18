# LANE-4 — Community practitioner experience with current-gen models (post-2026-06)

Research run: RESEARCH-clean-code-ai-agents-latest-models (task t_9b6c09bb, parent t_875c7cc1)
Lane: what practitioners report since 2026-06-01 about using current-generation coding models in agents on clean vs messy codebases: which clean-code principles matter more or less, which became moot, which failure modes persist. Dissent is recorded explicitly.
Source types owned: community. Covered: Reddit (r/ClaudeCode, r/ClaudeAI, r/claude, r/codex, r/ExperiencedDevs), Hacker News, Lobsters, plus practitioner blog/benchmark write-ups that those threads discuss.
Date of research: 2026-10-18
Tier scheme (same as the baseline lane 4): **Verified** = page/thread read whole this session; **Plausible** = verbatim quote from a named, fetchable source read at snippet or partial level; **Speculative** = inferred, not confirmed.
Anchor principles: [P1] naming, [P2] small functions/SRP, [P3] DRY, [P4] KISS, [P5] YAGNI, [P6] SOLID, [P7] error handling, [P8] testing/TDD, [P9] refactoring, [P10] readability & maintainability.

> Reddit data was read through the anonymous Atom feed (post plus top-level comments; no scores, no nesting). Quotes are verbatim from the feed.
> Date evidence for Reddit: the search feed returned explicit timestamps for 1v9zg50 (2026-07-29T15:27Z), 1x6nfto (2026-10-15T14:40Z) and 1u1b207 ("Introducing Claude Fable 5", 2026-06-09). Reddit post IDs are base-36 and increase monotonically, so every thread ID cited here (1v6…, 1v9…, 1w…, 1x…) is later than 1u1b207 and therefore after 2026-06-09. Each thread also names a model released after June 2026 (Opus 5, GPT-5.6 Sol, Opus 5.5, GPT-6 Sol/Astra).
> HN date evidence comes from the HN Algolia API `created_at` field (read via `hn.algolia.com/api/v1/items/<id>`).

## Model-generation context (lane 1 owns the authoritative list)

Practitioners in these threads talk about two waves after June 2026:
- **Wave A (Jun–Aug 2026):** Claude Fable 5 (2026-06-09), Claude Opus 5 / Sonnet 5 (around late July 2026; HN SlopCodeBench thread dated 2026-07-27), OpenAI GPT-5.6 Sol/Terra/Luna.
- **Wave B (Sep–Oct 2026, the current frontier):** Claude Opus 5.5 and OpenAI GPT-6 Sol/Luna (both announced 2026-09-22, per paddo.dev, F-14), GPT-6 Astra, Claude Fable 5.1, GPT-6.1 Sol (DevDay, 2026-09-29), Sonnet 5.5, Gemini 4 Argon (paddo.dev, 2026-10-14), Grok 4.7.
Wave A evidence counts as "current generation, previous point release." Where a finding rests only on wave A, it is marked **[wave A]**. The collector should check this against lane 1's model list.

---

## TL;DR

1. **The baseline's main claim (clean code matters MORE for agents) holds up in post-June practice, and now has longitudinal benchmark data from practitioners behind it.** The strongest new artifact is a practitioner-run SlopCodeBench evaluation of Opus 5 vs Opus 4.8 vs Sonnet 5 (HumanLayer, 2026-07-27; HN 405 points). It found that "not a single model made it through all the challenges without increasing complexity across checkpoints", and that the winner cleared only 4 of 17 strict checkpoints. [F-01, F-02]
2. **The dominant new failure mode of the current generation is over-engineering and volume (P4/P5), not sloppiness.** Many practitioners describe Opus 5 and GPT-5.6 Sol adding lookup tables, unnecessary null checks, a "compiler", and roughly 5x more functions. They blame RL post-training that rewards completeness and test coverage. Wave B (Opus 5.5) is reported as clearly better on verbosity and focus, but over-engineering complaints continue (HN, 2026-10-03). **P4 KISS / P5 YAGNI = INVERTED is CONFIRMED and gets stronger with the current generation.** [F-03, F-04, F-05, F-06, F-07]
3. **The "locally clean, globally incoherent" claim is CONFIRMED.** Practitioners now describe it as a compounding, nonlinear process ("decoherence", Lobsters, 2026-10-16; "longitudinal sloppification", HN). Models are also reported never to restructure architecture to fix bugs unless told to. [F-08, F-09, F-10]
4. **Small functions (P2) is now contested within the community, not just amplified.** Opus 5 writes many more small functions, and practitioners disagree on whether that counts as clean code or as slop. [F-02, F-11]
5. **DRY (P3) is still reported as something agents do not do by default.** A "dedupe pass" on a 500k-line, agent-maintained codebase found 2,500 duplicate lines. Agents duplicate because they cannot find existing code, so codebase organization matters more. [F-12, F-13]
6. **Dissent is stronger than in the baseline and has moved.** The "clean code is moot" position now says AI itself writes clean, maintainable code (HN, 2026-10-04) and "real codebases were so far from perfect that AI really isn't much worse" (r/ClaudeAI, 2026-10-15). Other practitioners answer with concrete bug-rate reports (3x customer bugs). [F-15, F-16, F-17]
7. **NEW for this generation: tests become a cost.** The best-performing model's output was 51% tests, and practitioners complain about "tests pinning non-ideal fuzzy behavior" and "a massive pile of unit tests" that make code hard to change. P8 is still AMPLIFIED as a *gate*, but agent-written test volume is now listed as a failure mode. [F-02, F-18]
8. **NEW: instruction/rules files now age with model versions.** Practitioners report that rules written for older models make newer ones over-do things (e.g. verification instructions). The baseline's "short, pruned AGENTS.md" recommendation is CONFIRMED and extended: prune the rules file again at every model upgrade. [F-19, F-20]
9. **Codebase mess shows up in agent cost.** In a 20-run monorepo replay, Opus 5.5 cost 1.6x more than GPT-6 Sol on the tidiest change and 6.1x more on the widest. Both models stalled on the same 26-file change. [F-14]

---

## A. Longitudinal / quantitative practitioner evidence

### F-01 — Practitioner-run SlopCodeBench: current-gen models still degrade codebases over time [P10, P4, P3]
- Claim: In a practitioner re-run of SlopCodeBench (a multi-checkpoint benchmark where requirements arrive one at a time), Opus 5 led but passed only 4 of 17 checkpoints under the strict criterion. Every model increased complexity across checkpoints.
- Source: https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/benchmarking-opus-5-on-slop-code-bench.md (practitioner benchmark write-up, HumanLayer). HN discussion https://news.ycombinator.com/item?id=49076391 (405 points, posted 2026-07-27).
- Verbatim: "Opus 5 got a **24%** on the small subset of the benchmark that I ran - not much higher than Opus 4.6's 17% strict pass rate in the original paper. All of the tested models showed a pretty significant increase in verbosity, complexity, and a bunch of other code smell metrics over the course of each challenge" / "Not a single model made it through all the challenges without increasing complexity across checkpoints." / "for real-shaped software engineering work, building one issue at a time, today's models can't be relied on to run lights-off without steering."
- Caveat (author's own): small subset (3 problems, 17 checkpoints); the slop rules are "a bit over-aggressive"; the metric's link to maintainability "is not yet established".
- Tier: **Verified** (write-up read through the metrics sections; HN thread read via the API). **[wave A]**. The author announced Fable and 5.6 Sol runs; no wave-B re-run was found.

### F-02 — Opus 5 gains correctness through code volume: about 5x the functions, 51% tests [P2, P8, P4]
- Claim: In the same benchmark, Opus 5 wrote 29,065 source lines against roughly 9,000 for each of the other models (about 1.8x production code, 51% tests) and about 5x the callables, with fewer single-use functions.
- Source: same HumanLayer write-up (F-01).
- Verbatim: "opus 5 wrote 29,065 against roughly 9,000 each for the other two" / "opus 5 is 51% tests, opus 4.8 is 11%, sonnet 5 is 24%" / "single-use functions as a share of all callables — opus 5 at 14.9%, opus 4.8 at 49.1%, sonnet 5 at 71.5%" / "Both sonnet and Opus 4.8 answered the increasing complexity ... by making individual functions bigger ... its single worst function ended at a cyclomatic complexity of 93." / "Duplication ... Opus 4.8 goes from 4.6% to 16.8%, with an inflection at ck3 — ~roughly where new requirements start fighting the initial design."
- Also: "the Opus 5 lights-off-generated solutions have over 11 times more slop triggers per kLOC than our 99%-AI-generated-but-also-carefully-reviewed Typescript monorepo." The author lists heavy caveats for this figure.
- Tier: **Verified**. **[wave A]**

### F-14 — Monorepo replay: Opus 5.5 vs GPT-6 Sol; cost rises with how spread out a change is [P10, cross-cutting]
- Claim: On six real merged changes from a 3,700-file TypeScript monorepo (20 runs per model), Opus 5.5 never broke a passing test (13/20 clean); GPT-6 Sol broke one in 5 runs (8/20 clean). Both stalled on the widest (26-file) change, and the cost gap grew from 1.6x on the tidiest change to 6.1x on the widest.
- Source: https://paddo.dev/blog/opus-5-5-vs-gpt-6-sol/ (practitioner benchmark blog; published 23-SEP-26, "LAST UPDATED: 29-SEP-26").
- Verbatim: "**The gap grows with the mess.** Opus cost 1.6x more on the tidiest change and 6.1x on the widest." / "Change C spread one setting across 26 files. Both models fixed under half its new tests, and both skipped the same part of the codebase, one the ticket named." / "Sol where the tests and review are strong. Every regression Sol made failed a test that already existed." / "**More effort made Opus less careful.** ... Neither model beat its medium score at any level."
- Interpretation: "mess" here means the scope or spread of a change, not a clean/messy pair of codebases, so this is **indirect** evidence for the baseline's token-cost claim (SonarSource minimal pairs). It does support the practical rule that **existing tests are the gate that catches regressions** (P8 AMPLIFIED as a gate).
- Tier: **Verified** (page read whole). **Wave B.**

## B. Over-engineering / KISS / YAGNI (P4, P5)

### F-03 — Opus 5 and GPT-5.6 Sol "over engineer"; practitioners blame RL toward coverage and completeness [P4, P5, P8]
- Claim: Practitioners report that the new models produce large lookup tables with hundreds of tests where a simple rule would do, chase edge cases that cannot happen, and drift from scope. The OP attributes this to post-training that rewards test coverage over parsimony.
- Source: https://www.reddit.com/r/ClaudeCode/comments/1v9zg50/why_opus_5_and_gpt_56_over_engineer_and_are/ (Reddit, 2026-07-29).
- Verbatim (OP u/ZhopaRazzi): "instead of a simple general parsing rule, they might instead produce a gigantic lookup table with hundreds of tests written against it. Same function in the end, but slower, arguably less robust ... models are post-trained for test coverage completeness, robustness, and long-horizon tasks, with likely automated classifiers that reward test coverage growth at the expense of parsimony. Parsimony is much harder to quantify and classify - so it will lose out in an RLAIF setting."
- Verbatim (u/skip_the_tutorial_): "Sometimes edge cases that can't even occur. Half the null checks it adds are completely unnecessary"
- Verbatim (u/somerussianbear): "5.6 Sol and Opus 5 only medium for me. Anything more than that will try to rewrite the thing from scratch."
- Workaround (u/khalon23): "I treat over-engineering as a scoping failure, not an intelligence failure. My default ask is: 'smallest change that fixes the failing test, no new abstractions.' ... cap the diff. 'Touch at most N files' ..." / OP's reply: "this is fine for supervised workflows, but not for autonomous implementation"
- The RL explanation is the practitioner's hypothesis and is not confirmed (**Speculative** as a mechanism). The behavior report itself is **Verified** (thread read). **[wave A]**

### F-04 — GPT-5.6 Sol over-engineered even when steered; GPT-6 Astra used to remove it [P4, P5, P9]
- Claim: A Codex user reports that GPT-5.6 Sol kept finding new ways to over-engineer despite repeated steering, and used GPT-6 (Astra) to delete about 10k lines. The same user says Sol "is ok in well maintained codebase and horrible in start a new blank project". A commenter says half the "saved" lines were comments and line breaks.
- Source: https://www.reddit.com/r/codex/comments/1whq988/when_gpt6_refactoring_sol_56_codebase/ (Reddit, ID series after 2026-06-09; mentions GPT-6 Astra, so after its release).
- Verbatim (OP u/Shoddy-Answer458): "I tried. I steered gpt5.6 many times to not overengineering. But finally, gpt5.6 will find another way to overengineer. Gpt5.6 is ok in well maintained codebase and horrible in start a new blank project" / "Another refactor; gpt5.6 implment a fking compiler in my code!" / method: "list obvious overengineering. then review the findings".
- Dissent (u/34986234986234982346): "5000 saved lines was removing comments, 5000 was by removing line breaks". Dissent (u/adolf_twitchcock): "You did this, not sol". Dissent (u/GM8): "12k useless lines of code ... does not appear over the course of a blink."
- Note: the line "ok in well maintained codebase" is a direct practitioner data point for "a clean codebase constrains the agent".
- Tier: **Verified** (thread read; humorous tone, treat as anecdote).

### F-05 — Automated reviews by multiple agents produce slop through review/fix loops [P4, P8]
- Claim: Teams running automated agent review loops on Opus 5 report that pedantic reviews create fix/feedback spirals that inflate trivial code, e.g. a single CREATE TABLE migration growing to 200 lines.
- Source: https://news.ycombinator.com/item?id=49076391 (HN, comment by patwolf, 2026-07-28).
- Verbatim: "Since switching to Opus 5 I've noticed the reviews are overly pedantic, and that leads to feedback loops where each fix generates more feedback, which requires more fixes, i.e. slop. I had, for example, a simple SQL migration script with a single CREATE TABLE. After a few rounds of review, it ballooned into a complicated 200 line script."
- Corroborating (HN 49079191, cjk, 2026-07-28): "I had what should have been a trivial feature go for 13 rounds of review/fix before I stopped it, where each round was just flip-flopping the same logic back and forth".
- Tier: **Verified** (both threads read via API). **[wave A]**. NEW failure mode compared with the baseline: review gates can themselves inflate code.

### F-06 — Opus 5.5 (wave B) is widely reported as less verbose and more focused [P4, P10]
- Claim: Practitioners moving back from Codex report that Opus 5.5 fixed Opus 5's verbosity, comment noise and drift. The OP cites Anthropic's claim of "about 40% less verbose with shorter code comments".
- Source: https://www.reddit.com/r/claude/comments/1wnwsg7/opus_55_worth_coming_back_from_codex/ (Reddit, after Opus 5.5 launch 2026-09-22).
- Verbatim (OP): "Opus 5 ... drifted off task and overcomplicated everything, even with effort turned down ... it spread that same style into code comments and docs, which left my codebase full of noise. I spent two weeks trying to fix it with output styles, CLAUDE.md rules, effort settings and prompting. Nothing worked." / "Anthropic says 5.5 is about 40% less verbose with shorter code comments".
- Verbatim replies: (u/LittleRoof820) "It definitely needs less handholding but I had one case where I interrupted it and steered it when it went on a useless tangent." / (u/i_maq) "gets more done correctly the first time" / dissent (u/Lynne22) "It's making really really bad mistakes out of nowhere this evening." / (u/rkh4n) "Just wait a week for reality".
- Corroborating (HN 49946567, slaser79, 2026-10-03): "What a jump after the writing slop you got from Opus 5 ... With 5.5 it needs less steering now".
- Tier: **Verified** (thread read; launch-week sentiment, so short-lived). Implication: some of the P4/P5 burden depends on the model version and was eased in wave B, but see F-07.

### F-07 — Over-engineering persists with Opus 5.5 at architecture level [P4, P5, P6]
- Claim: Even on Opus 5.5, an experienced builder found that the model's architecture blueprint was "overly complicated without adding extra value" and contained security risks, and needed days of human review notes.
- Source: https://news.ycombinator.com/item?id=49946567 (HN, "Getting the most out of Opus 5.5 in Claude and Claude Code", comment by tamimio, 2026-10-03).
- Verbatim: "you still need to know what you are doing, not just the goal/s ... after an hour work at Xhigh, it did create the blueprint artifacts that I asked for, then I spent 3 days reading every single thing and writing notes, turned out it made the system overly complicated without adding extra value, plus I can see how some of the architecture design will be potentially a security risk."
- Corroborating (same thread, moltar, 2026-10-04), on agent CI optimizations: "The result was a faster CI, but full of cludges huge inline bash scripts in workflow YAML files, and effectively unmaintainable, unreviewable mess."
- Corroborating (r/ExperiencedDevs 1wu1tzt, u/sn0wquake): the LLM added "hidden form fields (that had security holes), signing algos, temporary storage, and a ton of unnecessary clever complexity" and then admitted: "I missed four explicit instructions: - Simple over clever - Less code is more - YAGNI - Use what exists".
- Tier: **Verified**. **Wave B** (tamimio, moltar). This is the key evidence that P4/P5 INVERTED still holds on the current frontier model.

## C. Global coherence / architecture (P6, P10, P9)

### F-08 — "Decoherence": agents produce locally valid but mutually incompatible models faster than they can be resolved [P10, P6, P3]
- Claim: A widely discussed essay (Lobsters +51) names the baseline's "locally clean, globally incoherent" pattern "decoherence" and argues that it grows faster than linearly.
- Source: https://maevyn.codes/decoherence (practitioner essay) + https://lobste.rs/s/vjmn84/decoherence_trap_when_ai_slop_drowns_out (Lobsters, posted 2026-10-16).
- Verbatim (essay TL;DR): "**decoherence**: the accumulation of locally valid but mutually incompatible or redundant models within a system, such that the cost of change is dominated by translating among those models and preventing unintended side-effects." / "Decoherence grows relative to the rate of change of a system, and it increases faster the more decoherent a system is ... the widespread use of AI is currently producing it at a rate that is unsustainable."
- Verbatim (author on Lobsters, ~maevyn): "the reason they are able to is _because_ we have built up so much coherence in these systems! They are super well defined, super well abstracted, and agents combine the power of those existing abstractions really very well. The issue is, when you try to fill in the space between abstractions ... they can't really handle that complexity, particularly over time."
- Dissent (~shonfeder): "Arguably having 'built up so much coherence' helps reduce the size of available solutions somewhat, but its still the case that quite impressive results are being produced in domains that have massive combinatorial complexity."
- Tier: **Verified** (essay lead and Lobsters thread read). The essay is not tied to a specific model. Its model-generation relevance comes from the date (Oct 2026), so it is **Plausible** as current-gen evidence.

### F-09 — Agents never restructure architecture to fix bugs unless told to [P9, P6]
- Claim: A 13-year developer maintaining a 500k-LOC agent-built game engine reports that the agent "will not ever consider restructuring to solve bugs without intervention". A two-month bug was caused by architecture, and fixing it removed a set of earlier band-aids.
- Source: https://www.reddit.com/r/ClaudeCode/comments/1v6tiod/i_tested_opus_5_full_context_gathering_against_a/ (Reddit, Opus 5 era).
- Verbatim (u/Charming_You_25): "I discovered recently it will not ever consider restructuring to solve bugs without intervention- and instead think from what the current architecture permits as a baseline. Found the root cause of an issue I've had for 2 months today because the architecture was wrong. Fixed it and a bunch of related issues I had slapped bandaids over disappeared. Also tests are great till they pin non ideal fuzzy behavior"
- Same thread, codebase design: "It's a game engine. All modularized, downward dependencies only, no files over 150 lines." / "I architected it as well as I could ... and have been consistent about cleanups and refactors but it's now on the edge where my agents are starting to drift a little".
- Verbatim (u/Street_Attorney_9367): "Ai ... doesn't give any damns about your code quality or implementation unless you explicitly tell it to"
- Tier: **Verified**. **[wave A]**. P9 refactoring stays human-imposed (AMPLIFIED, must be ordered).

### F-10 — Agents cannot tell reviewed code from slop in the codebase they read, so garbage in means garbage out [P10]
- Claim: Experienced devs report that agents treat all existing code as equally authoritative and copy bad patterns. A messy codebase therefore degrades agent output further, which is a feedback loop.
- Source: https://www.reddit.com/r/ExperiencedDevs/comments/1wu1tzt/giving_your_codebase_entirely_to_the_ai/ (Reddit, ID after 2026-06; thread mentions Opus 5.5, so after 2026-09-22).
- Verbatim (u/DavidDavidsonsGhost): "ai can't tell the difference between the slop it generates and any reviewed code, it all looks the same and weighs it the same in consideration ... It's a 'garbage in, garbage out' problem."
- Verbatim (u/jhartikainen): "If you give the AI a bunch of nonsense it will not work as well as with a clean'ish codebase. Since AI generated code generally moves the codebase towards making less sense, doesn't that inevitably lead to a point where the AI stops producing working code, because the source of truth has gotten so bad?"
- Verbatim (u/patient-palanquin): "even the LLM has to understand what's been written before, without the original prompts. And the code has to be architected in a way that is set up for future changes. ... your simple features require bringing the whole damn codebase into context and guzzling tokens by the million."
- Tier: **Verified** (thread read). Wave B (Opus 5.5 named in thread).

### F-21 — Models may never learn "maintainable" because nothing in post-training rewards it [P10]
- Claim: HN practitioners argue that maintainability is not a post-training target and that the labs prioritize flashy one-shots. Some suggest this may be a fundamental limit.
- Source: https://news.ycombinator.com/item?id=49076391 (HN, 2026-07-28/29).
- Verbatim (Vgoose): "I think there's a simple explanation for why the models aren't good at 'maintainable' code: they're not explicitly trained on it in post-training." / (rstuart4133) "'maintainable' has a simple definition: minimising the effort to incrementally grow a software system as its size grows to infinity ... So far models haven't figured the same thing out." / (jerf) "It could be a fundamental architecture problem for LLMs ... The fact they've never so much as mentioned it suggests to me that it's not something they've been able to fix." / (akurilin) "Really hoping that all of the attention you're bringing to the longitudinal sloppification of codebases makes it back to the labs".
- Tier: **Speculative** as a mechanism; **Verified** that practitioners hold the view.

## D. Small functions, DRY, discoverability (P2, P3, P1)

### F-11 — "5x more functions": clean code or slop? The community is split [P2]
- Claim: Practitioners disagree about whether Opus 5's many-small-functions style is good. Some see it as readable and testable; others guard against "excessive function" generation in CLAUDE.md.
- Source: https://news.ycombinator.com/item?id=49076391 (HN, 2026-07-28).
- Verbatim (drcongo): "I have McCabe complexity switched on in Ruff ... Five times as many callables could make for much more readable and testable code." / (piazz): "The excessive function thing has always driven me crazy; I guard against this explicitly in Claude.md." / HumanLayer author (F-01): "FWIW I don't think lots of small functions is bad. I take it with a grain of salt these days, but I used to be a die-hard Clean Code guy."
- Tier: **Verified**. P2 is now **contested** in practice: the agent over-applies it, so the human has to bound it rather than impose it.

### F-12 — DRY still not followed by default; a dedupe pass found 2,500 duplicate lines [P3]
- Claim: On a 500k-LOC carefully curated agent codebase, a dedupe pass found 2,500 duplicate lines. Experienced devs say agents "never seem to want to follow DRY", and apply a DRY rule from CLAUDE.md only when they are fixing bugs.
- Sources: https://www.reddit.com/r/ClaudeCode/comments/1v6tiod/ (u/Charming_You_25: "You're right about the DRY, been a while since I did a dedupe pass. Found 2500 lines."); https://www.reddit.com/r/ExperiencedDevs/comments/1wu1tzt/ (u/ISuckAtJavaScript12: "AI generally produces more verbose code and doesn't ever seem to want to follow the DRY principle. Which means over time each successive change to the codebase would require more tokens"); HN 49076391 (dmrivers, 2026-07-28: "It does seem to find redundancies, but only when I point out bugs, that's when it goes into fixing mode and actually applies my Don't Repeat Yourself preference from the CLAUDE.md").
- Tier: **Verified** (all three read).

### F-13 — Agents duplicate because they cannot find existing code, so organization must be better than for humans [P3, P1, new: directory structure]
- Claim: A practitioner argues that agents read large files poorly and navigate by grep, so they "defensively add functions and modules that were already implemented" unless the codebase is better organized than a human-only one.
- Source: https://www.reddit.com/r/ExperiencedDevs/comments/1wu1tzt/ (u/roger_ducky).
- Verbatim: "Agents can read non-human-readable code. They can't. In fact, even a 1000 line file is a challenge for them. That's why they grep for relevant sections and tries to just edit a specific line range when faced with 'big' files. If you don't make the codebase even better organized than a human-only one, agents will defensively add functions and modules that were already implemented because they can't find out what else is there."
- Tension with vendor claims of 1M-token context windows (Opus 5.5, GPT-6 Sol): no practitioner in this lane reported that long context made organization unnecessary. A 500k-LOC owner reported that full-context gathering cost "about 10% of my current session limit" and still produced confidently wrong answers through subagent discovery (F-09 thread).
- Tier: **Verified** (thread read). The long-context "moot" hypothesis is **not supported** by community evidence (see Searched-found-nothing).

## E. Dissent: "clean code is moot / AI writes clean code"

### F-15 — Dissent: "AI writes clean code ... in a very maintainable way" (wave B) [cross-cutting]
- Source: https://news.ycombinator.com/item?id=49946567 (HN, AnotherGoodName, 2026-10-03; tripleee, 2026-10-04).
- Verbatim (AnotherGoodName): "AI writes clean code and can do so in a very maintainable way honestly." / (tripleee): "One of the last things developers had to offer was being able to guide the AI to write maintainable code. Now that it can do that there's not a whole lot left"
- Direct rebuttal in the same thread (moltar, F-7): "full of cludges ... effectively unmaintainable, unreviewable mess."
- Tier: **Verified**. Compared with the baseline, the dissent has moved from "code no longer needs to be readable" to "the agent already produces clean code".

### F-16 — Dissent: "real codebases were never clean, so AI isn't much worse" [P10]
- Source: https://www.reddit.com/r/ClaudeAI/comments/1x6nfto/the_anti_vibecoding_cult_is_going_to_be_on_wrong/ (Reddit, 2026-10-15; 400+ comments per mod bot).
- Verbatim (u/lucisferre): "AI doesn't write perfect code, but the truth is real codebases were so far from perfect that AI really isn't much worse for most applications. The purists fantasize about a historical time that never was."
- Verbatim (OP): "the idea that a model of Opus 5.5 standard can't write optimised code is disproven by all the hot paths."
- Counter (mod-bot TL;DR of 400 comments): "The community overwhelmingly rejects your 'vibe coder vs. purist' holy war ... the sweet spot is the skilled developer who uses AI as a powerful tool. They know enough to direct the model, review the code, understand the architecture".
- Tier: **Verified** (thread read, top-level). The mod summary is auto-generated, so treat it as **Plausible** as a measure of consensus.

### F-17 — Counter-dissent with numbers: 3x customer bug reports after going heavily agentic [P10, P8]
- Source: https://www.reddit.com/r/ExperiencedDevs/comments/1wu1tzt/ (u/coderstephen).
- Verbatim: "Bug reports from customers have increased like 3x, and every new feature we've launched have been more buggy launches than before. But hey, we've launched them faster than before by maybe 20%... These aren't 'you forgot to check for null' bugs, the AI is good at avoiding that. More like, 'it doesn't do what it is supposed to do and instead does something strange'."
- Also (u/dinosaurkiller): "'You must be using an outdated model', 'you mean Opus 5.5?'. ... it to have poor judgement and it makes bad assumptions even when you give it explicit instructions."
- Tier: **Verified** (single-org anecdote; unaudited numbers).

## F. Tests and rules files (P8, agent-era practice)

### F-18 — Agent-written test volume becomes a maintainability cost [P8]
- Claim: Practitioners report that current models generate test suites so large that they freeze bad behavior and slow change. This is the reverse of the baseline's "tests are the agent's gate".
- Sources: HumanLayer (F-02: Opus 5 output "51% tests"); r/ClaudeCode 1v9zg50 OP ("hundreds of tests written against it"); r/ClaudeCode 1v6tiod ("tests are great till they pin non ideal fuzzy behavior"); r/ExperiencedDevs 1wu1tzt (u/andymaclean19): "I've seen it create a massive pile of unit tests for something which left the code very bogged down and hard to change."
- Tier: **Verified** (all read). Verdict implication: P8 stays AMPLIFIED as an **external, human-owned gate** (F-14: existing tests caught every Sol regression), but **agent-authored test volume** should be listed as a failure mode. This fits the baseline finding that agent tests are mostly observational.

### F-19 — Rules/skills files age with models: instructions written for old models make new ones over-do work [agent-era: AGENTS.md]
- Source: https://dev.to/evbermudez/the-model-didnt-get-dumber-my-agent-skills-got-stale-8cm (practitioner blog, written after Opus 5 / GPT-5.6 launch).
- Verbatim: "The audit found instructions written around the behavior of older models. Some were redundant. Some were no longer necessary. Others pushed the newer models too hard and caused them to overdo tasks." / "Anthropic's Claude Opus 5 documentation says the model now verifies its work without being told. It specifically recommends removing verification instructions carried over from earlier models because they can cause over-verification." / "**The model might be fine. Your prompts may just have technical debt.**"
- Corroborating (r/ClaudeCode 1v6tiod OP): "The slimming of the system prompt means I have to fix my claude.md and agents files before it's usable."
- Vendor claims are second-hand here; lane 1 owns the primary doc. Tier: **Verified** (blog read whole). **[wave A]**

### F-20 — Rules-file size limits and simplicity rules: practitioners' practice [agent-era: AGENTS.md, P4]
- Sources/verbatim:
  - HN 49874728 (rubzah, 2026-09-28, "Prompting Claude Opus 5.5" thread, 207 points): "A CLAUDE.MD larger than about 150 lines will exceed it. That is not a lot of space to describe, for example, a complex code base, development conventions, and all the other important stuff."
  - HN 49874728 (gregwebs, 2026-09-28): "as the frontier models get better there is less need for agents with specialized personas ... I have a generated CODING_STANDARDS.md document and a skill for architecture design and a skill for implementing testing that are referenced by a single reviewer."
  - HN 49076391 (tracker1, 2026-07-28): "I call out specifically in my agent/claude file that I want and prefer simpler solutions over complex enterprise pattern usage and overuse of abstractions. It tends to help a bit, but often I have to give feedback in my review step."
  - HN 49076391 (delbertty, 2026-07-28): "Mostly a harness problem in my experience. Slop accumulates when the agent can touch anything, so constraining it to one seam and having it add alongside rather than edit in place does more than model choice."
  - HN 49076391 (piazz / anentropic): interleaved adversarial "refactor turn" / "periodically run a separate round of whole-codebase code review ... and then rounds of refactoring".
  - HN 49874728 (Prompting Opus 5.5 thread, search snippet): "I keep seeing comments added to code, which reads like reasoning output instead of meaningful words. I see this behavior for both OpenAI and Anthropic models".
- Tier: **Verified** for the comments read via the API; the last item is **Plausible** (search snippet, not found in the keyword-filtered API output).

---

## G. Per-principle community signal (input for the collector)

| Principle | Baseline verdict | Post-2026-06 community signal | Status vs baseline |
|---|---|---|---|
| P1 naming | AMPLIFIED | No new evidence. Indirect: discoverability/grep navigation (F-13); "invents jargon about your project" (HN 49946567, narrator) | CONFIRMED (weak) |
| P2 small functions/SRP | AMPLIFIED | Models now over-apply it (5x callables); community split (F-02, F-11) | CHANGED: still matters, but must be bounded, not imposed |
| P3 DRY | AMPLIFIED | Still not done by default; duplication grows across checkpoints; caused by poor discoverability (F-12, F-13, F-02) | CONFIRMED |
| P4 KISS | INVERTED | Strongest signal: over-engineering is the main current-gen failure (F-03..F-07), partly eased in Opus 5.5 (F-06) | CONFIRMED, stronger |
| P5 YAGNI | INVERTED | Same as P4; explicit YAGNI rules ignored (F-07 sn0wquake) | CONFIRMED, stronger |
| P6 SOLID/architecture | AMPLIFIED | No restructuring without instruction; decoherence (F-08, F-09) | CONFIRMED |
| P7 error handling | AMPLIFIED | Opposite failure: excessive null checks / edge cases (F-03); "AI is good at avoiding" null bugs (F-17) | CHANGED: over-defensive rather than missing |
| P8 testing | AMPLIFIED | Existing tests as gate still decisive (F-14); agent test volume is a new cost (F-18) | SPLIT: gate AMPLIFIED, agent-authored volume a failure mode (NEW) |
| P9 refactoring | AMPLIFIED | Must be scheduled/ordered; "refactor turns", dedupe passes, cleanup models (F-04, F-09, F-20) | CONFIRMED |
| P10 readability | SPLIT | Comment noise was Opus 5's issue, eased in 5.5 (F-06); global coherence is the main concern (F-08, F-10); dissent that AI writes clean code (F-15, F-16) | CONFIRMED; dissent moved |
| NEW | — | Rules files age with model upgrades (F-19); review-loop inflation (F-05); effort level as a quality lever ("medium" best; F-03, F-14) | NEW |

---

## Searched, found nothing (evidence of absence)

- **Long context makes clean code moot:** searched `"Opus 5.5" OR "GPT-6 Sol" legacy messy codebase long context no longer matters clean code` (web) and checked HN Opus 5.5 threads. No practitioner claimed that 1M-token context removes the need for a clean structure; the results were vendor/aggregator context-size comparisons. The closest is F-15/F-16 (a quality claim, not a context claim).
- **Wave-B SlopCodeBench re-run (Opus 5.5 / GPT-6 / Fable 5.1):** the HumanLayer post promised Fable and 5.6 Sol runs; no follow-up with wave-B models was found (web search for SlopCodeBench + Opus 5.5 returned only the Opus 5 post).
- **Controlled clean-vs-messy minimal-pair study on wave-B models (community):** none found. The HN thread cites arXiv 2605.20049 (SonarSource) and arXiv 2601.02200. Both are baseline-era/pre-June sources, so they are **not** cited as new evidence here.
- **Stack Overflow:** not searched directly (low yield in the baseline; search budget went to Reddit/HN). Skipped.
- **X/Twitter:** only reached indirectly (HN 49079191 links a tweet "Opus 5 is a really bad model"). No xurl access was used. Skipped.
- **GitHub Discussions:** no relevant post-June clean-code discussion found. The GitHub hits were "agents-radar" digest issues (secondary summaries, not cited).
- **r/LocalLLaMA, r/cursor, r/programming, r/ChatGPTCoding:** not searched individually because of the anonymous Reddit rate limit (~1 request/min). The site-wide Reddit search "over engineer opus 5" returned no relevant hits from these subs.
- **Reddit r/ExperiencedDevs search "clean code AI agents" (sort new):** no thread specifically about clean code; nearest relevant thread used as F-10/F-13/F-17 (1wu1tzt).
- **Gemini 4 / Grok 4.7 practitioner clean-code reports:** none found beyond a paddo.dev cost post title (Gemini 4 Argon, 2026-10-14, not read) and dismissive remarks about Gemini ("Anything gemini does will just have to be ripped out", r/ClaudeCode 1v6k643, wave A).

## Source index (all dated on or after 2026-06-01)

| # | URL | Type | Date evidence |
|---|---|---|---|
| S1 | https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/benchmarking-opus-5-on-slop-code-bench.md | practitioner benchmark | HN submission 2026-07-27 |
| S2 | https://news.ycombinator.com/item?id=49076391 | HN | 2026-07-27 (Algolia) |
| S3 | https://news.ycombinator.com/item?id=49079191 | HN | 2026-07-28 |
| S4 | https://news.ycombinator.com/item?id=49874728 | HN | 2026-09-28 |
| S5 | https://news.ycombinator.com/item?id=49946567 | HN | 2026-10-03 |
| S6 | https://paddo.dev/blog/opus-5-5-vs-gpt-6-sol/ | practitioner benchmark blog | 23-SEP-26, updated 29-SEP-26 |
| S7 | https://maevyn.codes/decoherence | practitioner essay | Lobsters 2026-10-16 |
| S8 | https://lobste.rs/s/vjmn84/decoherence_trap_when_ai_slop_drowns_out | Lobsters | 2026-10-16 |
| S9 | https://www.reddit.com/r/ClaudeCode/comments/1v9zg50/ | Reddit | 2026-07-29 |
| S10 | https://www.reddit.com/r/ClaudeCode/comments/1v6tiod/ | Reddit | Opus 5 era (ID > 1u1b207 = 2026-06-09) |
| S11 | https://www.reddit.com/r/ClaudeCode/comments/1v6k643/ | Reddit | Opus 5 / GPT-5.6 Sol era |
| S12 | https://www.reddit.com/r/claude/comments/1wnwsg7/ | Reddit | after 2026-09-22 (Opus 5.5 + GPT-6 Sol out) |
| S13 | https://www.reddit.com/r/codex/comments/1whq988/ | Reddit | GPT-6 Astra era |
| S14 | https://www.reddit.com/r/ExperiencedDevs/comments/1wu1tzt/ | Reddit | after Opus 5.5 (named in thread) |
| S15 | https://www.reddit.com/r/ClaudeAI/comments/1x6nfto/ | Reddit | 2026-10-15 |
| S16 | https://dev.to/evbermudez/the-model-didnt-get-dumber-my-agent-skills-got-stale-8cm | practitioner blog | post-Opus 5 / GPT-5.6 (content) |

Also read but not used as a finding: r/ExperiencedDevs 1wzic5u ("my three-year ai honeymoon is over"; mostly well-being, not code quality) and r/codex 1w8uf0g (GPT-6 Astra job anxiety; one remark: "it cannot get an intuition for the product and needs babysitting").
