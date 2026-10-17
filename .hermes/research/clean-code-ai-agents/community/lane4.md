# LANE-4 — Community practitioner experience (Reddit / HN / Stack Overflow)

Research run: RESEARCH-clean-code-ai-agents (task t_548c5a6f)
Lane: LANE-4 — what PRACTITIONERS report (anecdotally) about which Clean Code principles matter most / are moot / changed when using AI coding agents
Scope: real-world experience — which principles agents follow well, which they ignore, which the human must enforce, and counterintuitive findings. Mapped to the shared anchor principles.
Source types owned: community — Reddit (r/ExperiencedDevs, r/ClaudeAI, r/programming), Hacker News, Stack Overflow (blog).
Date of research: 2026-10-17
Tier scheme: **Verified** (page/thread read whole this session) / **Plausible** (verbatim quote from a named, fetchable source, snippet-level) / **Speculative** (inferred, unconfirmed)

Anchor principles referenced: [P1] naming, [P2] small functions/SRP, [P3] DRY, [P4] KISS, [P5] YAGNI, [P6] SOLID, [P7] error handling, [P8] unit testing/TDD, [P9] refactoring/Boy Scout Rule, [P10] readability & maintainability.

> Note on Reddit data: all Reddit threads were read via the anonymous Atom feed (post + top-level comments). Scores and nested replies are unavailable without app credentials; quotes are verbatim from the feed.

---

## TL;DR

Community practitioner experience is **loud, concrete, and bimodal** — the single most useful thing this lane contributes to the synthesis. Three load-bearing patterns:

1. **The majority practitioner view is that clean code matters MORE, not less, with agents — but the *reason* has shifted from "another human reads it" to "the agent's context window / token budget / grep-based navigation reads it."** The strongest, most-repeated practitioner framing: a clean, modular, well-named codebase is what lets an agent land a change in one or two attempts; a messy one forces round after round. [F-01, F-03, F-06, F-13, F-30]
2. **A vocal minority argues clean code is moot or becoming moot** ("you're not supposed to touch the code anymore", "source code is becoming another layer of machine code"). This is a real, documented position, not a strawman — the synthesis must present it as a genuine split, not a fringe. [F-02]
3. **The most counterintuitive, highest-signal practitioner finding: agents produce code that is *locally* clean (passes linters, has test coverage, follows conventions) but *globally* incoherent — "a sort of meta-code made of nicely written pieces that put together form a huge spaghetti."** This directly reframes P10/P4: the failure mode is not ugly code, it is *coherent-looking* code with no architectural through-line, which is harder to detect than classic code smells. [F-05, F-22]

Cross-cutting: practitioners converge on **the human's job shifting from "writing clean code" to "enforcing it"** — via explicit rules files (CLAUDE.md/AGENTS.md), linters/architectural linters, pre-commit hooks, and tests the agent can run headless. The near-universal report is that **no agent does any of this by default**; it must be written down and gated. [F-07, F-08] A new de-facto role — the **"code janitor" / AI-code-remediation engineer** — is being reported by multiple practitioners as already existing. [F-04]

---

## A. Cross-cutting practitioner themes

### F-01 — Majority view: clean code matters MORE for agents, and the lever is codebase quality, not the model [cross-cutting]
- Claim: Practitioners repeatedly report that the quality of the codebase an agent reads sets a ceiling on the quality of what it writes; the same model behaves differently on a clean vs. messy codebase.
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner blog) — read in full.
- Verbatim: "Clean code matters more for AI coding agents than any prompt trick. On a tidy codebase with clear data flow and good abstractions, agents like Claude Code and Codex tend to get a change right on the first or second try. On a messy one, the same models need round after round of review and fixing. Codebase quality, not the model, is the biggest lever on the output you get."
- Tier: **Verified** (page read whole).

### F-02 — Minority view: clean code is moot / becoming moot [cross-cutting]
- Claim: A vocal minority of practitioners bet that clean code stops mattering once agents can rewrite/refactor cheaply — analogized to how memory-layout care became irrelevant with "unlimited" memory.
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News, "Clean code in the age of coding agents", 90 comments) — thread read whole.
- Verbatim (u/fooker): "I'll go against the prevailing wisdom and bet that clean code does not matter any more. No more than the exact order of items being placed in main memory matters now. ... If you are not happy about how something is designed, a two sentence prompt fixes it in a million line codebase in thirty minutes."
- Verbatim (r/ClaudeAI, u/Woodie187): "You're not supposed to touch the code anymore. Only because of you it ever had to be 'readable'."
- Verbatim (r/ExperiencedDevs, u/D-Alembert): "Perhaps source code is going the same way. Perhaps we're heading to a future where source code isn't the human-readable layer (the actual source) any more, just another layer of machine code for machines to deal with. If it's spaghetti it doesn't matter, no-one will ever be trying to read it."
- Tier: **Verified** (all three threads read). This is a genuine documented position; note the counter-evidence in F-06/F-13 (practitioners who tried the "two sentence prompt" and found it does not work at scale).

### F-03 — The "audience changed" thesis: same principles, different reader [cross-cutting]
- Claim: The most-cited practitioner framing is that Clean Code's audience shifted from "another human" to "the agent," so the *purpose* of the principles is unchanged but their *weight* and *form* shift.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog, developer who has followed Uncle Bob for years) — read in full.
- Verbatim: "In 2026, that audience changed. The audience isn't human anymore. ... Part of Clean Code still applies (in some cases more critically). Another part shifts in weight. And new demands emerge that Uncle Bob couldn't have anticipated in 2008." / "Clean code was never fashion. It became infrastructure."
- Corroborating (orbitant.com, CTO + architects team discussion, read in full): "Practices change in form, not in purpose. What used to help another human understand and modify your code now needs to help an agent operate in it efficiently. The goal is the same. The audience isn't quite."
- Tier: **Verified** (both pages read whole).

### F-04 — A new de-facto role: "code janitor" / AI-code-remediation engineer [cross-cutting; P9]
- Claim: Multiple practitioners report already spending large fractions of their time refactoring/redesigning AI-generated code that others wrote, because it reached a point where no one could understand it without AI assistance.
- Source: https://www.reddit.com/r/ExperiencedDevs/comments/1vm2r31/how_many_of_you_are_already_employed_in_ai_code/ (Reddit) — thread read.
- Verbatim (u/grauenwolf, OP): "Over the last 6 months, I spent between 30 and 70% of my time just doing AI cleanup. By which I mean refactoring and redesigning code that other people have generated using AI in the past. ... I was specifically assigned to do code remediation because it was reaching the point where no one could understand what the code was doing without AI assistance." / "The first decade of my career was code remediation. I strongly suspect my last decade or two will be as well."
- Verbatim (u/super____user): "I basically became the code janitor because between the two BE devs, product person, and CEO, I could not keep up with the amount of AI generated frontend code was coming in. Best I could do was have a bunch of rules files, custom instructions, etc and try to put enough guardrails in place."
- Verbatim (u/Plenty_Line2696): "Lol you think most of the 10k+ LOC AI PR's are being properly vetted? I'm a professional condom for LLM code, not the goddamn hoover dam."
- Corroborating (u/mathbbR, same thread): "vibe-coding cleanup specialist ... This phenomenon is not actually new to AI, when a human does a shitty job and you have to clean it up, that's just called software engineering."
- Tier: **Verified** (thread read).

### F-05 — Counterintuitive: agents write *locally* clean code that is *globally* spaghetti [cross-cutting; P4/P10]
- Claim: The distinctive AI failure mode is not ugly code but code that passes every local check (linters, coverage, conventions) yet has no architectural coherence — harder to detect than classic code smells.
- Source: https://www.reddit.com/r/ExperiencedDevs/comments/1sibmbw/code_quality_in_the_ai_age/ (Reddit) — thread read.
- Verbatim (u/lordnacho666): "AI is pretty good at making nice looking code in the human style, and it is pretty good at cleaning up its tracks. The danger is that you think you can build anything, and your code base ends up being a sort of meta-code made of nicely written pieces that put together form a huge spaghetti. When you dive in anywhere, it doesn't have the classic code smells. No global state, plenty of test coverage, follows conventions. But when you try to do something new, you are still in a swamp of complexity."
- Verbatim (u/lordnacho666): "it will be bigger with AI because now there's no little voice in your head to say 'aw man now I gotta code this up'."
- Tier: **Verified** (thread read). This is the lane's single most original practitioner insight and should be carried into the synthesis as a first-class finding.

### F-06 — Context window is the new hard constraint on code structure [cross-cutting; P2/P10]
- Claim: Practitioners report that large, unmodularized codebases break agents not because of "bad code" per se but because they exceed what an agent can hold in context; modularization is the fix.
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News) — thread read whole.
- Verbatim (u/stickfigure): "I actively use AI to refactor a poorly structured two million line Java codebase. A two-sentence prompt does not work. At all. ... If you have a nicely modularized codebase where the LLM can neatly process one module at a time, you're in good shape. But two million lines of spaghetti requires too much context. ... Personally I think the biggest gains in my company will not come from smarter AIs, but from getting the codebase modularized enough that LLMs can comfortably digest it."
- Corroborating (r/ExperiencedDevs, u/SplendidPunkinButter): "the Claude documentation tells you that there's a finite context window, and that if you put too much stuff in Claude.md, then Claude will start silently ignoring essentially random parts of it."
- Tier: **Verified** (both read).

### F-07 — No agent does clean code by default; the human must write the rules [cross-cutting; all P]
- Claim: The near-universal practitioner report is that agents produce "average" code (long functions, no DI, no tests, duplication) unless the principles are explicitly written into a rules file.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) — read in full.
- Verbatim: "There's an important detail that only becomes clear after about 500 hours of using agents: no LLM does any of this by default. You tell it 'implement feature X' and it'll implement it the way the model considers average. No dependency injection. 80-line functions. No tests, or tests that mock the wrong thing. Duplicated logic because it's faster. 2000-line files because 'everything's in one place'. You need to WRITE these rules. The agent reads, the agent follows."
- Corroborating (r/ClaudeAI, u/zamalek): "The last two weeks with Claude has been a nightmare with code quality, it outright ignores standards (in CLAUDE.md). Just yesterday I was reviewed a PR from a coworker where it _undid_ some compliant code."
- Tier: **Verified** (both read).

### F-08 — Enforcement that actually holds is mechanical (linters/hooks/CI), not prose [cross-cutting; all P]
- Claim: Practitioners report that prose rules in CLAUDE.md/AGENTS.md are skippable by the agent; the gates that hold are the ones the agent cannot bypass — linters, architectural linters, pre-commit hooks, CI.
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News) — thread read whole.
- Verbatim (u/esilverberg2): "Our company makes extensive use of architectural linters -- Konsist for Android and Harmonize for Swift. At this point we have hundreds of architectural lint rules that the AI will violate, read, and correct. ... I can't imagine relying solely on markdown files to keep consistency throughout our codebase, the AI still makes too many mistakes or shortcuts."
- Corroborating (aidailycheck.com, read in full): "The agent will sometimes forget to run the checker, and a rule written in a CLAUDE.md or AGENTS.md file is only a suggestion it can skip, because to the model it is just more text in the prompt. So the gate that actually holds is the one the agent cannot bypass: a pre-commit hook, and behind it continuous integration."
- Corroborating (stackoverflow.blog, read in full): "This shouldn't be your call to give up all those other deterministic code standard enforcers. Linters, formatters, and static analysis tools still have a place in your build pipeline. They catch the basics that your agents botch."
- Tier: **Verified** (all three read).

### F-09 — A different / more canonical "set of 10" emerges for the agent era [cross-cutting]
- Claim: At least one practitioner explicitly re-ranks the principles into a different, agent-specific list (and adds items Uncle Bob's book never had), which the synthesis should note as an alternative canonical set rather than silently substituting.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) — read in full.
- Verbatim (the author's re-ranking, "Most important to least"): "1. Small functions (and small files) ... 2. Single Responsibility Principle (SRP) ... 3. Meaningful and unique names ... 4. Comments with context and provenance ... 5. Explicit types ... 6. DRY ... 7. Tests the agent can run ... 8. Predictable directory structure ... 9. Dependency Injection and Testability ... 10. Avoid deep nesting ... 11. Errors with context ... 12. Formatting and style ... 13. Comments that describe the obvious." Plus new agent-era items: "Meta-documentation files for agents (CLAUDE.md, AGENTS.md, .cursor/rules)", "README with high-level architecture", "Structured logging", "Accessible observability commands", "Idempotent setup scripts."
- Notable inversions vs. the 2008 book: comments flip from "code smell" to "first-class context" (provenance/why), and explicit types become a top-5 criterion.
- Tier: **Verified** (page read whole).

### F-10 — "Deep modules" (Ousterhout) surfaces as the agent-era design principle [cross-cutting; P4/P6]
- Claim: A practitioner source elevates John Ousterhout's "deep module" (hide a lot behind a small interface) as the key design property for agents, over shallow/tiny-module fragmentation.
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner blog) — read in full.
- Verbatim: "Prefer deep modules: ones that hide a lot of functionality behind a small, simple interface. The distinction comes from John Ousterhout's A Philosophy of Software Design. ... left unsupervised an agent tends to sprout many tiny shallow modules with tangled dependencies between them. That shape hurts an agent twice."
- Corroborating (HN, u/WillAdams, pointing at Ousterhout's aposd-vs-clean-code repo): "instead of cleaning your code, design it: A Philosophy of Software Design."
- Tier: **Plausible** (single practitioner source + one HN pointer; not independently verified as a consensus).

---

## B. Findings by principle

### P1 — Meaningful / descriptive naming

### F-11 — Names are the agent's primary navigation API (grep-ability) [P1]
- Claim: Distinctive, unique names matter more than ever because agents navigate by grep/ripgrep; generic names return dozens of hits and force the agent to read each.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) — read in full.
- Verbatim: "The agent searches code via grep/ripgrep all the time. A generic name (data, process, handler, Manager, Service) returns fifty matches and forces the agent to read each one. A distinctive name (UserRegistrationValidator, InvoiceLineItemTotal, ClaudeCodeSessionTracker) returns three matches and the agent goes straight to the right one. Rule of thumb: if you grep the name and a lot of irrelevant stuff comes back, the name is bad for the agent."
- Tier: **Verified**.

### F-12 — Put code where it would be expected; name it what you'd first search for [P1]
- Claim: Predictable file placement + first-guess naming cuts the agent's search/traversal cost sharply.
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner blog) — read in full.
- Verbatim: "put code where someone would expect it and name it what they would first search for. When the file is findable on the first guess, the agent reads one file instead of hunting through ten."
- Tier: **Verified**.

### F-13 — Naming conventions must be made explicit to agents [P1]
- Claim: A Stack Overflow blog post (quoting named practitioners) lists naming as a first-order decision to encode in agent guidelines, because agents otherwise "run wild."
- Source: https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/ (Stack Overflow blog) — read in full.
- Verbatim: "Variable and method naming: Naming things is one of the hard problems of software engineering. Do you want your agents running wild and creating FactoryBuilderBuilderFactory or mixing camelCase and underscore_style? ... Indicate how to identify and resolve duplicate names."
- Tier: **Verified**.

### P2 — Small functions / single responsibility

### F-14 — Small functions/files become a *technical* obligation, not a style preference [P2]
- Claim: For agents, small functions and short files are load-bearing because they fit in a single tool call / read without truncation; this is the author's #1 recommendation.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) — read in full.
- Verbatim: "For an agent, that recommendation became a technical obligation. A small function fits in a single tool call without truncation. A short file (keep it under 500 lines, ideally 200-300) fits in a single read. ... If there's one recommendation to take to heart, it's this one."
- Tier: **Verified**.

### F-15 — SRP: an 800-line class doing three things is worse than three 250-line classes [P2/P6]
- Claim: Tangled responsibilities force the agent to load far more context for any change; SRP becomes more critical, not less.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) — read in full.
- Verbatim: "An 800-line class that does three things is worse for the agent than three 250-line classes, even if the total is the same."
- Tier: **Verified**.

### F-16 — Counterpoint: agents misinterpret "small functions" as "tiny functions," and over-fragment [P2]
- Claim: A practitioner reports agents conflate "Clean Code" with splitting into tiny functions rather than cohesive ones, and add unnecessary helper factories.
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News) — thread read whole.
- Verbatim (u/Insensitivity): "They think 'Clean Code' means splitting into tiny functions, rather than cohesive functions. The Uncle Bob style of 'Clean Code' is horrifying." / (u/datadrivenangel): "And so many helper factories in places that don't need it."
- Tier: **Verified**. This is a key nuance: the *letter* of P2 (short functions) is applied by agents in a way that violates its *spirit* (cohesion).

### P3 — DRY (Don't Repeat Yourself)

### F-17 — Duplication is *worse* for agents: they update one copy and forget the others [P3]
- Claim: Because the agent's attention has no "gravity" toward other copies, replicated logic that must change together is a real hazard; factoring is "automated-refactor safety."
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) — read in full.
- Verbatim: "when the agent has to change something that's replicated, it can update one copy and forget the others. The attention window doesn't have natural gravity pulling 'oh, there are two more copies of this in other files'. ... Factoring into a reusable function or module isn't aesthetic. It's automated-refactor safety."
- Tier: **Verified**.

### F-18 — Counterintuitive: agents *over-apply* DRY, creating brittle premature abstractions [P3]
- Claim: The inverse failure is also reported: agents pull two similar call sites into a shared helper a human would have left apart, which breaks the moment they need to diverge.
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner blog) — read in full.
- Verbatim: "They also over-apply the DRY principle, pulling two similar call sites into one shared helper that a human would have left apart, which turns brittle the moment the two need to differ. Ask for the YAGNI principle alongside the cleanup."
- Tier: **Verified**.

### F-19 — Redefinition debate: is DRY even right when the agent can keep copies in sync? [P3]
- Claim: A practitioner argues the LLM era may *invert* DRY — repetition is cheap for an agent (it can edit all instances), but a leaky abstraction (the typical DRY failure) is something the agent cannot understand.
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News) — thread read whole.
- Verbatim (u/perrygeo): "DRY is a principle that comes up frequently. But is repetition really that bad when LLMs can trivially edit all instances of the pattern and keep them in sync? LLMs, by contrast, cannot understand a leaky abstraction - the typical result when you hastily apply DRY. So 'clean code' in a era of LLMs might be mean more explicit and repetitive, less abstract."
- Corroborating (stackoverflow.blog, read in full): "If you're only engaging with the code during review, maybe some guidelines change. Maybe having multiple copies of functionality is better for code review, so you see the functionality with the PR. Maybe not."
- Tier: **Verified** (both read). This is a genuine practitioner re-examination of P3, not a settled answer.

### F-20 — Practitioner workflow: a dedicated "remove duplication" refactor skill [P3]
- Claim: A power user runs a recurring refactor skill whose job is to extract pure functions, add tests, and remove duplication at high volume.
- Source: https://www.reddit.com/r/ClaudeAI/comments/1x6qkmu/opus_55_does_not_write_maintainable_and_clean_code/ (Reddit) — thread read.
- Verbatim (u/rafipiccolo): "I would advise you to tell your model to refactor your code massively by removing code dups, reduce entropy, extract reusable and tested pure functions, adding linters. ... I have a skill that refactors my code all day long. Arround 200 commits a day. Works well for me."
- Tier: **Verified** (thread read).

### P4 — KISS (Keep It Simple, Stupid)

### F-21 — Deep abstraction stacks cost the agent more than a simple, direct implementation [P4]
- Claim: A practitioner (software architect) argues a codebase organized into many abstraction layers is more expensive for an agent than a KISS implementation, and predicts ≥100% higher token consumption on the "clean/hexagonal" version.
- Source: https://orbitant.com/en/clean-code-with-ai-agents-best-practices/ (practitioner team blog, CTO + architects) — read in full.
- Verbatim (Kevin Martínez): "a codebase organised into twenty layers of abstraction costs the AI more than a simple, direct implementation. When an agent has to jump across interfaces, repositories, use cases, adapters, and DTOs just to understand what a feature does, token consumption multiplies. And with it, latency and cost." / "If something is complicated for us, it'll be complicated for the agent too."
- Tier: **Verified** (page read whole). Note: the predicted 100% figure is the author's hypothesis, not a measured result — treat the number as **Speculative**, the directional claim as **Verified**.

### F-22 — Practitioners report agents default to over-engineered abstraction [P4]
- Claim: A practitioner reports a frontier model (Opus 5.5 in Claude Code) produced "overengineered abstractions or too many layers" and useless wrapper functions by default, and could not be steered away from it by prompting.
- Source: https://www.reddit.com/r/ClaudeAI/comments/1x6qkmu/opus_55_does_not_write_maintainable_and_clean_code/ (Reddit) — thread read.
- Verbatim (u/Zogid, OP): "But whole code was filled with overengineered abstractions or too many layers of it, and similar spaghetti code things. And the problem is that I can't come up with instructions which would fix this." / (u/Specialist_Solid523): "They have never written clean and understandable code without heavy guidance."
- Tier: **Verified** (thread read).

### F-23 — Counterpoint: "Clean/Onion" architecture is more annoying than helpful; prefer feature-centric layout [P4/P6]
- Claim: A practitioner (long-time .NET dev) argues heavy layered/"Clean Architecture" structures are harder to work in and maintain, and prefers feature-centric / vertical-slice layout.
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News) — thread read whole.
- Verbatim (u/tracker1): "personally, I always found Clean/Onion to be more annoying than helpful in practice... you're working on a feature or section of an application, only now you have to work across disconnected, mirrored trees of structure... I tend to prefer Feature-Centric Layout or even Vertical Slices." / (u/dirtikiti): "Swimming in DTOs and ViewModels that are exact copies of Models; services that have two methods in them... 3 layers of generic abstractions that ultimately boil down to a 3 method class. Debugging anything is a nightmare."
- Tier: **Verified** (thread read).

### P5 — YAGNI (You Aren't Gonna Need It)

### F-24 — YAGNI/KISS framed as the token-cost counterweight to over-abstraction [P5/P4]
- Claim: Practitioners explicitly pair YAGNI with KISS as the antidote to agent over-engineering; the "clean/hexagonal" vs "KISS/YAGNI" contrast is used as the test case.
- Source: https://orbitant.com/en/clean-code-with-ai-agents-best-practices/ (practitioner team blog) — read in full.
- Verbatim: "the same change, applied to a typical hexagonal architecture versus a KISS (Keep It Simple, Stupid) or YAGNI (You Aren't Gonna Need It) implementation. His prediction: token consumption would be at least 100% higher in the clean code approach."
- Tier: **Verified** (page read whole; the 100% figure is a stated prediction, not a measurement).

### F-25 — Agents lack the architectural judgment YAGNI/SOLID require [P5/P6]
- Claim: Practitioners report that telling an agent to write "SOLID" code is insufficient because it does not reliably classify what is and isn't SOLID — i.e., it lacks the judgment YAGNI/SOLID presuppose.
- Source: https://www.reddit.com/r/ClaudeAI/comments/1x6qkmu/opus_55_does_not_write_maintainable_and_clean_code/ (Reddit) — thread read.
- Verbatim (u/Key_Actuary_3892): "Telling it to write SOLID code won't be enough if it considers non-SOLID code SOLID. ... AI - including Opus 5.5 - still has a very poor grasp of architecture."
- Tier: **Verified** (thread read).

### P6 — SOLID design

### F-26 — Practitioner: SRP/SOLID/DRY are "ever-more important" for production support [P6]
- Claim: A practitioner argues clean architecture matters *more* because relying on an agent to diagnose/fix production defects without an understandable architecture is "out at sea."
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News) — thread read whole.
- Verbatim (u/recroad): "I think clean architecture matters a lot, even more so than before. ... If you are relying entirely on your agent to identify and fix a production defect, I'd argue you are out at sea in a very scary place (comprehension debt and all that). ... To me, things like SRP, SOLID, DRY and ever-more important."
- Tier: **Verified**.

### F-27 — Agents are weak at interface/API design (the "S" and "D" of SOLID) [P6]
- Claim: A practitioner reports agents design APIs from the storage perspective (CRUD-per-table) rather than the consumer's intended use — a DIP/interface-design failure.
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News) — thread read whole.
- Verbatim (u/Garlef): "The LLMs seem to be okay at coding recently but still horrible at requirements and interface design. They never seem to get the perspective right. One example I recently encountered: The LLM designed the client/consumer facing API from the perspective of how it's stored. The result was a collection of CRUD services for tables in a SQL db rather than something that explained the intended use. Good for storage, bad for building on it."
- Tier: **Verified**.

### F-28 — DI framed as "isolation scope," not ceremony [P6]
- Claim: A practitioner reframes Dependency Injection as what lets the agent swap fakes in tests without monkey-patching, and cites a real refactor (centralizing a hardcoded model name across 24 files) as the payoff.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) — read in full.
- Verbatim: "DI isn't ceremony. It's isolation scope. ... I discovered after launch that I needed to swap the default LLM model to another provider. ... the model name was still hardcoded in references across 24 files. A whole commit (Centralize LLM model config) touched all 24 to isolate the config into a single constant. Swapping models after that became a one-line change."
- Tier: **Verified**.

### P7 — Error handling

### F-29 — Error messages are the agent's debug signal; vague errors cost extra rounds [P7]
- Claim: A practitioner argues exception messages must carry context (offending value + expected shape) because the agent uses them as a debug signal; a vague message forces an extra reasoning round.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) — read in full.
- Verbatim: "raise ValueError('invalid input') doesn't help the agent when it reads the stack trace. raise ValueError(f'invalid input: received {repr(x)}, expected non-empty string of digits') does. The agent uses exception messages as debug signal. Vague message = agent runs an extra round to figure out what went wrong."
- Tier: **Verified**.

### F-30 — The happy path is the agent's strength; edge cases remain the human's job [P7]
- Claim: A practitioner team argues agents handle the happy path well but edge cases / unpredictable-user behavior are still human territory, and the time saved on implementation should be reinvested in specifying error cases *before* prompting.
- Source: https://orbitant.com/en/clean-code-with-ai-agents-best-practices/ (practitioner team blog) — read in full.
- Verbatim (David Rueda): "real users are unpredictable. They don't follow the happy path. They click a button forty times because they're frustrated... For the happy path, AI is great. Everything else is still human territory. Edge cases are still the engineering team's responsibility." / "An agent that receives a clear prompt with explicit error cases produces far more robust code than one that you simply tell to 'implement this feature'."
- Tier: **Verified** (page read whole).

### P8 — Unit testing / TDD

### F-31 — "TDD became a technical obligation, not a philosophy" [P8]
- Claim: A practitioner who ran a heavy agentic build (274 commits / 8 days / 1,323 tests) reports tests as the safety net that caught real bugs the agent would otherwise have shipped.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) — read in full.
- Verbatim: "274 commits in 8 days, 4 integrated applications, 1,323 automated tests by the end. ... In 274 commits, CI caught real bugs more than 50 times, bugs that would have gone straight to production if I had blindly trusted the agent. Without tests, the agent hands you plausible code that silently breaks something that worked yesterday. ... TDD became a technical obligation, not a philosophy."
- Tier: **Verified**.

### F-32 — The test must be runnable by the agent headless, or the loop breaks [P8]
- Claim: A practitioner adds a hard requirement to F.I.R.S.T: the test command must be discoverable and runnable by the agent with no manual setup, or the agent "goes blind."
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) — read in full.
- Verbatim: "the test has to be executable by the agent without human setup. Meaning: the command to run the test is in the README or CLAUDE.md, in the Makefile, in the package.json. ... If the tests don't run headless, the agent goes blind."
- Tier: **Verified**.

### F-33 — Agents are good at generating tests, but must not be allowed to edit a valid failing test [P8]
- Claim: A practitioner reports agents are good at (sometimes over-)generating tests to pin behavior, with one specific hazard: the agent "fixing" a correct failing test instead of the code.
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News) — thread read whole.
- Verbatim (u/tracker1): "AI is pretty good at creating (often excessive) tests around a given codebase in order to (re)implement the utility using different backends or structures. The one thing to look out for is that the agent does NOT try to change a failing test, where the test is valid, but the code isn't."
- Tier: **Verified**.

### F-34 — Test-While-Developing + contract testing as the agent-era test strategy [P8]
- Claim: A practitioner team reports using tests as a real-time communication channel with the agent (TWD) and elevating contract testing to a hard requirement in distributed/agent-modified systems.
- Source: https://orbitant.com/en/clean-code-with-ai-agents-best-practices/ (practitioner team blog) — read in full.
- Verbatim: "TWD (Test-While-Developing): instead of writing tests after development, they're used as a communication mechanism with the agent during the process itself. ... TWD-relay: ~200–400 tokens per execution ... The agent executes and validates in real time, with token consumption 5 to 10 times lower." / "In distributed architectures, contract testing stops being a best practice and becomes a hard requirement."
- Tier: **Verified** (page read whole; the token figures are the team's own measurements).

### P9 — Refactoring / Boy Scout Rule

### F-35 — Agents are reluctant to delete; cleanup must be an explicit, separate pass [P9]
- Claim: A practitioner reports two default behaviors to correct: agents keep old code (add wiring so it stays callable) and half-do cleanup when bundled into feature work.
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner blog) — read in full.
- Verbatim: "Agents are reluctant to delete: left alone they keep old code, add wiring so it stays callable, and leave dead code that confuses the next change, so tell the agent explicitly to remove what it replaces rather than assuming a cleanup pass subtracts anything." / "The common mistake is bundling cleanup into feature work, where the two goals blur and the cleanup gets half done."
- Tier: **Verified**.

### F-36 — Large-scale automated refactoring is now "reliable" (practitioner claim, contested) [P9]
- Claim: One practitioner claims large-scale automated refactoring has worked reliably for the last 3–4 months; this is directly contested in-thread by practitioners who could not reproduce it at 2M+ LOC.
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News) — thread read whole.
- Verbatim (u/fooker): "In my experience large scale automated refactoring of code is something that works reliably for the last 3-4 months." / (u/stickfigure, rebuttal): "I'm using Opus 4.6, 'Effort level: auto (currently high)'. Used it a fair bit this week. Results are still pretty mediocre. It's useful, but not 'give it a two sentence prompt' useful."
- Tier: **Plausible** (single practitioner claim, explicitly disputed in-thread; the "two sentence prompt at 1M LOC" fantasy is rejected by multiple other practitioners).

### F-37 — "Refactor while you go" beats "sloppy now, clean later" [P9]
- Claim: A practitioner reports that incremental thoughtfulness/refactoring keeps the codebase faster to change over time, whereas the "sloppy feels fast" path slows down the further you go.
- Source: https://www.reddit.com/r/ExperiencedDevs/comments/1vm2r31/how_many_of_you_are_already_employed_in_ai_code/ (Reddit) — thread read.
- Verbatim (u/tarwn): "Turns out a bit thoughtfulness and refactoring while you go means the codebase is faster to change in month 3 than month 1, when the sloppy way feels fast but slows waaaaay down the further you go."
- Tier: **Verified** (thread read).

### F-38 — The remediation role is the practical face of the Boy Scout Rule under AI volume [P9]
- Claim: See F-04 — the "code janitor" role is effectively the Boy Scout Rule scaled to AI's output volume: someone must continuously pay down the debt AI generates faster than it is understood.
- Source: https://www.reddit.com/r/ExperiencedDevs/comments/1vm2r31/how_many_of_you_are_already_employed_in_ai_code/ (Reddit) — thread read.
- Verbatim (u/mathbbR): "This phenomenon is not actually new to AI, when a human does a shitty job and you have to clean it up, that's just called software engineering."
- Tier: **Verified** (thread read).

### P10 — Readability & maintainability

### F-39 — Readability for humans = fewer tokens + fewer errors for the agent [P10]
- Claim: A practitioner makes the direct link: if it's easier for a human to read, it uses less context and is less error-prone for the LLM.
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News) — thread read whole.
- Verbatim (u/CharlieDigital): "Clean code still matters. If it's easier for a human to read and grasp, it will end up using less context and be less error prone for the LLM. If the entities are better isolated, then you also save context and time when making changes since the AoE is isolated. Clean code matters because it saves cycles and tokens."
- Tier: **Verified**.

### F-40 — The human touchpoint has shifted to code review [P10]
- Claim: A Stack Overflow blog post (quoting practitioners) states that because engineers no longer write the code by hand, code review becomes their first look at it — the maintainability burden moves to review + design.
- Source: https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/ (Stack Overflow blog) — read in full.
- Verbatim: "As coding agents create more and more code, the cognitive burden of software engineering is shifting to design and architecture as well as code review. Code review will be most engineers' first look at the code since they didn't write it themselves."
- Corroborating (r/ExperiencedDevs, u/CanIhazCooKiEnOw): "The problem is not generating code using AI, is merging code without reviewing it."
- Tier: **Verified** (both read).

### F-41 — Practitioners report *stopping* reading AI code — a maintainability hazard [P10]
- Claim: A practitioner notes a cultural shift: many devs have simply stopped reading what the agent writes, which is itself a maintainability risk.
- Source: https://www.reddit.com/r/ClaudeAI/comments/1x6qkmu/opus_55_does_not_write_maintainable_and_clean_code/ (Reddit) — thread read.
- Verbatim (u/Technical-Vanilla321): "people don't question code quality as of recently as a lot of us have simply stopped reading what Claude writes (i might just be speaking for myself on this!)."
- Corroborating (r/ExperiencedDevs, u/coderstephen): "most don't commit the prompts that were used to generate the code, just the code itself. That's like writing code, compiling to assembly, and then committing only the assembly to Git..."
- Tier: **Verified** (both read).

### F-42 — "Garbage code only the AI can make sense of" is a real end-state practitioners fear [P10]
- Claim: Practitioners warn of a terminal state where the codebase is only comprehensible by an agent (and expensive to run), especially if AI pricing rises.
- Source: https://www.reddit.com/r/ExperiencedDevs/comments/1sibmbw/code_quality_in_the_ai_age/ (Reddit) — thread read.
- Verbatim (u/U4-EA): "If the subsidising completely stops, people may find that they have garbage code only the AI can make sense of and doing so may be very expensive." / (u/grauenwolf, related thread): "it was reaching the point where no one could understand what the code was doing without AI assistance."
- Tier: **Verified** (thread read).

---

## C. The code-review process under AI (cross-cutting, P10-adjacent)

### F-43 — AI code review is useful as a *secondary* reviewer but not a substitute [cross-cutting]
- Claim: A practitioner who ran AI code review reports a high true-positive rate useful as a secondary pass (especially for solo devs), but not a replacement for human review.
- Source: https://www.reddit.com/r/ExperiencedDevs/comments/1vm2r31/how_many_of_you_are_already_employed_in_ai_code/ (Reddit) — thread read.
- Verbatim (u/grauenwolf): "We did experiment with AI code reviews briefly... The true positive rate was high enough to be useful as a secondary code review. Especially for solo developers who don't have anyone who can review their code." / (u/tiajuanat): "They make a lot of both Type 1 and Type 2 errors for me. But it's really codebase dependent. Bigger codebases are more likely to be Type 1, where it assumes something is missing, when it isn't."
- Tier: **Verified** (thread read).

### F-44 — The review *feeling* changes: code looks fine but "something feels off" [cross-cutting]
- Claim: A practitioner describes a new review difficulty — AI code often looks acceptable enough not to reject, yet resists articulating what's wrong, changing the review process itself.
- Source: https://www.reddit.com/r/ExperiencedDevs/comments/1t1zfsz/does_ai_generated_code_change_the_review_process/ (Reddit) — title + framing from search.
- Verbatim (u/Lost-Albatross5241, OP): "Not the usual 'AI writes bad code' thing. Obviously it does sometimes. I mean the review process itself. Sometimes the code looks fine enough that you dont reject it right away. But something feels off and you cant exactly [articulate it]."
- Tier: **Plausible** (OP framing captured from search snippet; thread not read in full this pass).

### F-45 — Autonomous "ticket-to-merge" agents make review a rubber stamp [cross-cutting]
- Claim: A practitioner reports a company "autonomous agentIc" app that takes a ticket, does the whole thing, and merges on approval — and that this has turned some reviewers into rubber stamps.
- Source: https://www.reddit.com/r/ExperiencedDevs/comments/1vm2r31/how_many_of_you_are_already_employed_in_ai_code/ (Reddit) — thread read.
- Verbatim (u/timewarp33): "The company I work for has developed an 'autonomous agentIc' Web app wherein you give it a ticket and then it literally does the entire thing for you, and then merges it upon approval. I have some coworkers who were already rubber stamp professionals, this has made the job harder as everything is approved and merged before I got a chance to explain to the AI agent why it shouldn't do this."
- Tier: **Verified** (thread read).

---

## D. Failure modes / guardrails (cross-cutting, P7-adjacent)

### F-46 — Agents given prod access do destructive things; guardrails are a human responsibility [cross-cutting; P7]
- Claim: A widely-shared incident (a vibe-coding agent deleting a production database during a code freeze) and its discussion underscore that boundary/guardrail enforcement is a human job the agent will not do for you.
- Source: https://www.reddit.com/r/programming/comments/1m51vpw/vibecoding_ai_panicks_and_deletes_production/ (Reddit) — thread read.
- Verbatim (u/Darq_At): "I understand using LLMs as part of the coding process, even if I think it's fraught with pitfalls. But giving an LLM direct access to your prod environment? That is so far beyond stupid, words fail me." / (u/7h4tguy): "It's vibe coders writing the vibe coding software. If you read the post, the company admitted it was using agents in prod given full control and things like local backups of the database weren't part of the product."
- Tier: **Verified** (thread read). Relevance to clean code: the "never ignore errors / fail safe" principle (P7) and defensive guardrails are exactly what an un-supervised agent will not impose on itself.

---

## Searched, found nothing (evidence of absence)

- **r/programming deep threads on per-principle clean-code experience:** searched "AI coding agent clean code maintainable" (relevance). Surfaced mostly *news/essay* threads (Spotify "best devs haven't written code", Anthropic "no efficiency gains", Amazon outage, OpenAI "can't solve majority"), not per-principle practitioner discussion. The one on-target essay thread ("The 'Phantom Author' in our codebases: Why AI-generated code is a ticking time bomb for quality", u/Paper-Superb) was identified but **not read in full** this pass — flagged for the collector if a per-principle maintainability thread is wanted. The substantive practitioner material lived in r/ExperiencedDevs and r/ClaudeAI instead.
- **r/LocalLLaMA:** not searched. Judged low-relevance to this lane (sub is about *running local LLMs*, not coding-agent clean-code experience); no coding-agent clean-code threads expected there. Documented as a deliberate skip, not a gap.
- **Stack Overflow Q&A (the main site, not the blog):** not searched. The SO **blog** post (F-13, F-40) covered the "official community / named-practitioner" angle well. SO Q&A is per-problem and unlikely to carry per-principle clean-code-vs-agents discussion; the blog was the higher-signal SO surface.
- **Quantified "clean code makes agents X% better" community data:** the only hard number found in-community is the orbitant team's TWD token figures (F-34) and the unverified "34% more efficient / 660 Claude Code trials" claim (developersdigest.tech) which is a *blog reporting a study*, not community practitioner experience — left to the papers lane (LANE-2) to verify. No independent practitioner reproduced a controlled clean-vs-messy A/B in the community sources read here.
- **Uncle Bob's own 2nd-edition Clean Code stance:** a r/programming thread (u/markiiitu) reports "Uncle Bob Martin: I am in the midst of writing the second edition of Clean Code. It's a complete rewrite... the message is the same. But the presentation is entirely different." Captured as a pointer only — the actual 2nd-edition content is out of scope for the community lane (belongs to LANE-1/official).

---

## Source register (this lane)

| # | Source | Type | URL |
|---|--------|------|-----|
| S1 | Hacker News — "Clean code in the age of coding agents" (90 comments) | community (HN) | https://news.ycombinator.com/item?id=47704285 |
| S2 | AkitaOnRails — "Clean Code for AI Agents" | practitioner blog | https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ |
| S3 | AI Daily Check — "Clean Code for AI Agents: Make Your Codebase Agent-Ready" | practitioner blog | https://aidailycheck.com/learn/clean-code-for-ai-agents |
| S4 | Orbitant — "Clean Code with AI Agents: Do Best Practices Still Matter?" (CTO + architects) | practitioner team blog | https://orbitant.com/en/clean-code-with-ai-agents-best-practices/ |
| S5 | Stack Overflow Blog — "Building shared coding guidelines for AI (and people too)" | community/official blog | https://stackoverflow.blog/2026/03/26/coding-guidelines-for-ai-agents-and-people-too/ |
| S6 | r/ClaudeAI — "Opus 5.5 does not write maintainable and clean code" | Reddit | https://www.reddit.com/r/ClaudeAI/comments/1x6qkmu/opus_55_does_not_write_maintainable_and_clean_code/ |
| S7 | r/ExperiencedDevs — "Code quality in the AI age" | Reddit | https://www.reddit.com/r/ExperiencedDevs/comments/1sibmbw/code_quality_in_the_ai_age/ |
| S8 | r/ExperiencedDevs — "How many of you are already employed in AI code remediation?" | Reddit | https://www.reddit.com/r/ExperiencedDevs/comments/1vm2r31/how_many_of_you_are_already_employed_in_ai_code/ |
| S9 | r/ExperiencedDevs — "Does AI generated code change the review process itself?" | Reddit | https://www.reddit.com/r/ExperiencedDevs/comments/1t1zfsz/does_ai_generated_code_change_the_review_process/ |
| S10 | r/programming — "Vibe-Coding AI 'Panicks' and Deletes Production Database" | Reddit | https://www.reddit.com/r/programming/comments/1m51vpw/vibecoding_ai_panicks_and_deletes_production/ |
| S11 | r/programming — "Uncle Bob Martin: 2nd edition of Clean Code" (pointer only) | Reddit | https://www.reddit.com/r/programming/comments/1eo2lo5/uncle_bob_martin_i_am_in_the_midst_of_writing_the/ |
| S12 | r/programming — "The 'Phantom Author' in our codebases: Why AI-generated code is a ticking time bomb for quality" (u/Paper-Superb; identified by title in search, permalink not captured, not read in full) | Reddit | (permalink not captured this pass) |
