# LANE-3 — World-leading AI devs' & vendors' practical experience

Research run: RESEARCH-clean-code-ai-agents (task t_4b380f49)
Lane: LANE-3 — what WORLD-LEADING AI DEVELOPERS and agent vendors say (practically) about clean code in the context of AI coding agents
Scope: vendor engineering blogs/docs (Anthropic Claude Code, OpenAI Codex, Cursor, Cognition/Devin, Aider, GitHub Copilot), the AGENTS.md open standard, prominent AI engineers' posts/talks (Simon Willison), "how I use AI coding agents" posts, and how clean-code rules are encoded for agents (CLAUDE.md, AGENTS.md, .cursor/rules, .github/copilot-instructions.md). Per-principle findings mapped to the shared anchor.
Source types owned: practice — vendor engineering blogs/docs, prominent AI engineers' posts/talks, "how I use AI coding agents" posts, agent-config conventions.
Date of research: 2026-10-17
Tier scheme: **Verified** (authoritative source for this exact target, actually read in full) / **Plausible** (sound general behavior / snippet-level, not yet read in full) / **Speculative** (inferred, unconfirmed)

Anchor principles referenced: [P1] naming, [P2] small functions/SRP, [P3] DRY, [P4] KISS, [P5] YAGNI, [P6] SOLID, [P7] error handling, [P8] unit testing/TDD, [P9] refactoring/Boy Scout Rule, [P10] readability & maintainability.

---

## TL;DR

The practice/vendor literature is **loudly and consistently pro-clean-code for agents**, and it converges on a small set of mechanisms that differ from the papers lane (LANE-2). Three load-bearing, on-target themes:

1. **The #1 practical lever is a machine-runnable check, not a prose rule.** Every major vendor (Anthropic, OpenAI, Cursor, GitHub) and the top practitioner posts converge on: give the agent a deterministic check it can run (test suite, build, linter, type-checker) and gate the work on it — ideally as a **pre-commit hook / CI the agent cannot bypass**, because a rule written in CLAUDE.md/AGENTS.md "is only a suggestion it can skip." This is the practice-world expression of [P7] error handling + [P8] testing. [F-01, F-16, F-24, F-36, F-42, F-58]
2. **Keep the instruction file short, specific, and pruned — "bloat makes the agent ignore you."** Anthropic, OpenAI, Cursor, and Aider all say the same thing: a short, accurate, pruned CLAUDE.md/AGENTS.md/.cursor/rules outperforms a long vague one; add rules only after repeated mistakes; delete what the agent already does. This is [P4] KISS + [P5] YAGNI + [P9] Boy Scout applied to the *config file itself*. [F-03, F-07, F-18, F-25, F-35, F-41]
3. **Clean code is now a *performance* setting, not an aesthetic one — and the agent reads your code many times a day.** The strongest practitioner framing: an agent learns conventions from the code it reads, so codebase quality "sets a ceiling" on its output; clean, well-named, small, well-abstracted code makes the agent land a change in 1–2 tries instead of many. A SonarSource controlled study (660 Claude Code trials) quantifies it: clean codebases → 7–8% fewer tokens, 34% fewer file revisits, **same pass rate**. This is [P10] maintainability + [P1] naming + [P2] small files, now with a measured payoff. [F-55, F-56, F-57, F-62, F-63]

Cross-cutting: the field has **standardized on a shared instruction file** (AGENTS.md, now stewarded by the Linux Foundation's Agentic AI Foundation) that works across Codex, Claude Code, Cursor, Devin, Aider, Copilot, Jules, Windsurf, etc. — so "clean-code rules for agents" is a portable, version-controlled artifact, not a per-tool hack. [F-10, F-11, F-43]

**Key nuance / tension to carry into the report:** practitioners repeatedly warn that agents **over-apply** some clean-code rules — they over-DRY (merge two call sites a human would leave apart), over-split into "tiny functions" instead of cohesive ones, and are reluctant to delete dead code. So the advice is to pair DRY with YAGNI, and to ask for cohesion over mere smallness. [F-44, F-60, F-64]

---

## A. Anthropic — Claude Code Best Practices (official)

### F-01 — Give the agent a way to verify its work: tests, build, linter, screenshot [P8 testing + P7 error handling] — KEY
- Claim: The single most-emphasized Claude Code best practice is to give the agent a runnable check that returns pass/fail (test suite, build exit code, linter, diff-vs-fixture, screenshot), so the agent can close the loop itself instead of you becoming the verification loop.
- Source: https://www.anthropic.com/engineering/claude-code-best-practices (official Anthropic / Claude Code docs, now at code.claude.com/docs/en/best-practices) — read in full.
- Verbatim: "Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from. ... Give Claude something that produces a pass or fail, and the loop closes on its own. ... The check is anything that returns a signal Claude can read in the conversation: a test suite, a build exit code, a linter, a script that diffs output against a fixture, or a browser screenshot compared against a design."
- Tier: **Verified** (official docs, read in full). Directly encodes [P8] (tests as first-class) and [P7] (never ignore errors — the check is the error signal) for the agent context.

### F-02 — Explore first, then plan, then code (don't jump to coding) [P4 KISS + cross-cutting]
- Claim: Separating exploration/planning from implementation prevents the agent from "solving the wrong problem"; plan mode is recommended when scope is uncertain or the change spans multiple files.
- Source: https://www.anthropic.com/engineering/claude-code-best-practices (official) — read in full.
- Verbatim: "Letting Claude jump straight to coding can produce code that solves the wrong problem. Use plan mode to separate exploration from execution." / "If you could describe the diff in one sentence, skip the plan."
- Tier: **Verified** (official docs). Maps to [P4] (do the simplest correct thing — don't over-build the wrong solution) and to the broader "understand before you edit" discipline.

### F-03 — Write an effective CLAUDE.md: keep it short, prune ruthlessly [P4 KISS + P5 YAGNI + P9 Boy Scout]
- Claim: CLAUDE.md (the persistent agent-instruction file) should be short and human-readable; each line must earn its place; a bloated file causes the agent to ignore your actual instructions; treat it like code and prune it regularly.
- Source: https://www.anthropic.com/engineering/claude-code-best-practices (official) — read in full.
- Verbatim: "keep it short and human-readable. ... For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" / "Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts."
- Tier: **Verified** (official docs). This is [P4]/[P5]/[P9] applied to the *instruction file itself* — the clean-code principle that the config artifact must stay minimal and be continuously refactored.

### F-04 — CLAUDE.md should EXCLUDE self-evident clean-code rules [P10 readability + cross-cutting]
- Claim: Anthropic's own include/exclude table explicitly lists "Self-evident practices like 'write clean code'" as something to EXCLUDE from CLAUDE.md — i.e., you do not need to (and should not) tell the agent to write clean code; encode only the non-obvious, project-specific rules.
- Source: https://www.anthropic.com/engineering/claude-code-best-practices (official) — read in full.
- Verbatim (❌ Exclude column of the "Include/Exclude" table): "Self-evident practices like 'write clean code'." / (✅ Include column): "Code style rules that differ from defaults."
- Tier: **Verified** (official docs). Important nuance: the vendor's position is that clean code is a *default* the model already has; the value of the config file is in the *delta* from defaults, not in restating Clean Code.

### F-05 — Hooks are deterministic; CLAUDE.md is advisory [P7 error handling + P10]
- Claim: For actions that must happen with zero exceptions, use hooks (deterministic scripts) rather than CLAUDE.md instructions (advisory prose) — the reliable gate is the one the agent cannot skip.
- Source: https://www.anthropic.com/engineering/claude-code-best-practices (official) — read in full.
- Verbatim: "Use hooks for actions that must happen every time with zero exceptions. ... Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." / example: "Write a hook that runs eslint after every file edit."
- Tier: **Verified** (official docs). The practice-world version of [P7] "never ignore errors": enforce the invariant mechanically, not by asking nicely.

### F-06 — Adversarial review → warn against over-engineering [P4 KISS + P5 YAGNI]
- Claim: When using a fresh-context reviewer subagent, Anthropic explicitly warns that chasing every reported gap leads to over-engineering (extra abstraction layers, defensive code, tests for impossible cases); tell the reviewer to flag only correctness/requirement gaps.
- Source: https://www.anthropic.com/engineering/claude-code-best-practices (official) — read in full.
- Verbatim: "A reviewer prompted to find gaps will usually report some, even when the work is sound, because that is what it was asked to do. Chasing every finding leads to over-engineering: extra abstraction layers, defensive code, and tests for cases that can't happen. Tell the reviewer to flag only gaps that affect correctness or the stated requirements, and treat the rest as optional."
- Tier: **Verified** (official docs). A rare *vendor* statement that explicitly names over-engineering as the failure mode — direct [P4]/[P5] guidance for agent review loops.

### F-07 — Failure pattern: the over-specified CLAUDE.md; fix = prune [P4 KISS + P5 YAGNI + P9 Boy Scout]
- Claim: One of Anthropic's named "common failure patterns" is an over-specified CLAUDE.md that the agent half-ignores; the fix is to ruthlessly prune and convert standing rules into hooks.
- Source: https://www.anthropic.com/engineering/claude-code-best-practices (official) — read in full.
- Verbatim: "The over-specified CLAUDE.md. If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise. Fix: Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook."
- Tier: **Verified** (official docs). Reinforces F-03; "delete it or convert it to a hook" is [P9] (leave the config cleaner) + [P7] (make it deterministic).

### F-08 — Failure pattern: the trust-then-verify gap [P8 testing + P7 error handling]
- Claim: A named failure pattern is the agent producing a plausible-looking implementation that doesn't handle edge cases; the fix is always to provide verification and "if you can't verify it, don't ship it."
- Source: https://www.anthropic.com/engineering/claude-code-best-practices (official) — read in full.
- Verbatim: "The trust-then-verify gap. Claude produces a plausible-looking implementation that doesn't handle edge cases. Fix: Always provide verification (tests, scripts, screenshots). If you can't verify it, don't ship it."
- Tier: **Verified** (official docs). [P8] (tests catch the edge cases) + [P7] (don't ignore the unhandled cases).

### F-09 — Reference existing patterns; follow the codebase [P10 consistency + P3 DRY]
- Claim: A core prompting technique is to point the agent at existing patterns in the repo and have it follow them ("look at how existing widgets are implemented ... follow the pattern"), rather than inventing new structure.
- Source: https://www.anthropic.com/engineering/claude-code-best-practices (official) — read in full.
- Verbatim: "Reference existing patterns. Point Claude to patterns in your codebase. ... 'look at how existing widgets are implemented on the home page to understand the patterns. HotDogWidget.php is a good example. follow the pattern to implement a new calendar widget ... build from scratch without libraries other than the ones already used in the codebase.'"
- Tier: **Verified** (official docs). [P10] (consistency with the codebase) + [P3] (reuse what exists, don't duplicate/diverge).

### F-10 — Let the agent interview you; write a self-contained spec [P10 + P8]
- Claim: For larger features, have the agent interview you and write a spec (SPEC.md) that names the files/interfaces, states what is out of scope, and ends with an end-to-end verification step; then execute in a fresh session.
- Source: https://www.anthropic.com/engineering/claude-code-best-practices (official) — read in full.
- Verbatim: "The most useful specs are self-contained: they name the files and interfaces involved, state what is out of scope, and end with an end-to-end verification step that proves the feature works. Time spent making the spec precise pays off more than time spent watching the implementation."
- Tier: **Verified** (official docs). [P10] (a readable, self-contained spec) + [P8] (the spec ends with a verification step).

---

## B. AGENTS.md open standard (multi-vendor)

### F-11 — AGENTS.md = a "README for agents," deliberately separate from the human README [P10 + cross-cutting]
- Claim: AGENTS.md is an open format that holds the extra, sometimes detailed context agents need (build steps, tests, conventions) that would clutter a human README; it is intentionally kept separate so READMEs stay concise for humans and agents get precise, agent-focused guidance.
- Source: https://agents.md/ (official AGENTS.md site) — read in full.
- Verbatim: "README.md files are for humans: quick starts, project descriptions, and contribution guidelines. AGENTS.md complements this by containing the extra, sometimes detailed context coding agents need: build steps, tests, and conventions that might clutter a README or aren't relevant to human contributors." / "We intentionally kept it separate to: Give agents a clear, predictable place for instructions. Keep READMEs concise and focused on human contributors. Provide precise, agent-focused guidance that complements existing README and docs."
- Tier: **Verified** (official site). [P10] (readability, split by audience) — the clean-code idea of "right tool / right place for the right reader," now with a second reader (the agent).

### F-12 — One AGENTS.md works across many agents; now stewarded by the Linux Foundation [P10 + cross-cutting]
- Claim: A single AGENTS.md is compatible with a large ecosystem (Codex, Jules, Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin, Amp, Cursor, RooCode, Gemini CLI, Kilo Code, Semgrep, GitHub Copilot, Windsurf, Augment); it is now stewarded by the Agentic AI Foundation under the Linux Foundation.
- Source: https://agents.md/ (official) — read in full.
- Verbatim: "One AGENTS.md works across many agents ... Codex from OpenAI, Jules from Google, Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin from Cognition, ... Amp, Cursor, RooCode, Gemini CLI from Google, Kilo Code, ... Coding agent from GitHub Copilot, Windsurf from Cognition, Augment Code." / "AGENTS.md is now stewarded by the Agentic AI Foundation under the Linux Foundation."
- Tier: **Verified** (official site). Cross-cutting: clean-code rules for agents are a *portable, version-controlled* artifact — a big deal for the report (one file, many tools).

### F-13 — AGENTS.md: list test commands and the agent runs them; "add tests even if nobody asked" [P8 testing + P7]
- Claim: The canonical AGENTS.md example includes "Add or update tests for the code you change, even if nobody asked," and the FAQ confirms the agent will execute listed test commands and fix failures before finishing.
- Source: https://agents.md/ (official) — read in full.
- Verbatim (example AGENTS.md, Testing instructions): "Add or update tests for the code you change, even if nobody asked." / (FAQ) "Will the agent run testing commands found in AGENTS.md automatically? Yes—if you list them. The agent will attempt to execute relevant programmatic checks and fix failures before finishing the task."
- Tier: **Verified** (official site). [P8] (tests as first-class, agent-run) — the standard's own example treats "write the test" as a default agent duty.

### F-14 — Treat AGENTS.md as living documentation; nearest-file-wins [P9 Boy Scout + P10]
- Claim: AGENTS.md is meant to be continuously updated ("living documentation"); in monorepos, nested AGENTS.md files apply with the nearest file to the edited file winning (explicit chat prompts override everything).
- Source: https://agents.md/ (official) — read in full.
- Verbatim: "Can I update it later? Absolutely. Treat AGENTS.md as living documentation." / "What if instructions conflict? The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything." / "Large monorepo? Use nested AGENTS.md files for subprojects ... the closest one takes precedence ... at time of writing the main OpenAI repo has 88 AGENTS.md files."
- Tier: **Verified** (official site). [P9] (continuously improve the config) + [P10] (scoped, readable, per-subproject guidance).

### F-15 — Recommended AGENTS.md sections = the clean-code checklist for agents [P10 + P8 + P1]
- Claim: The recommended sections to cover are project overview, build & test commands, code style guidelines, testing instructions, and security considerations — i.e., the same hygiene a clean codebase needs, packaged for the agent.
- Source: https://agents.md/ (official) — read in full.
- Verbatim: "Add sections that help an agent work effectively with your project. Popular choices: Project overview, Build and test commands, Code style guidelines, Testing instructions, Security considerations."
- Tier: **Verified** (official site). Maps the clean-code checklist onto the agent-instruction file.

---

## C. OpenAI Codex Best Practices (official)

### F-16 — Treat Codex like a teammate you configure and improve over time [cross-cutting + P9]
- Claim: OpenAI's framing is that Codex works best as a durable teammate you configure and improve over time — right context, AGENTS.md for durable guidance, MCP for external systems, skills for repeated work, automation for stable workflows.
- Source: https://developers.openai.com/codex/learn/best-practices (official OpenAI/Codex docs) — read in full.
- Verbatim: "Codex works best when you treat it less like a one-off assistant and more like a teammate you configure and improve over time. A useful way to think about this: start with the right context for the task, use AGENTS.md for durable guidance, configure Codex to match your workflow, connect external systems with MCP, turn repeated work into skills, and automate stable workflows."
- Tier: **Verified** (official docs). [P9] (continuously improve the setup) + cross-cutting "configure once, improve continuously."

### F-17 — Prompt structure: Goal / Context / Constraints / "Done when" [P8 + P10]
- Claim: OpenAI's default prompt template includes a "Done when" criterion — "what should be true before the task is complete, such as tests passing, behavior changing, or a bug no longer reproducing" — making the success check part of the request.
- Source: https://developers.openai.com/codex/learn/best-practices (official) — read in full.
- Verbatim: "A good default is to include four things in your prompt: Goal: What are you trying to change or build? Context: Which files, folders, docs, examples, or errors matter ... Constraints: What standards, architecture, safety requirements, or conventions should Codex follow? Done when: What should be true before the task is complete, such as tests passing, behavior changing, or a bug no longer reproducing?"
- Tier: **Verified** (official docs). [P8] (define done = tests passing) + [P10] (scoped, reviewable work).

### F-18 — AGENTS.md: short & accurate beats long & vague; add rules only after repeated mistakes [P4 KISS + P5 YAGNI + P9]
- Claim: OpenAI's AGENTS.md guidance is to keep it short and practical, start with basics, add new rules only after you notice repeated mistakes, and run a retrospective to update it when the agent errs twice.
- Source: https://developers.openai.com/codex/learn/best-practices (official) — read in full.
- Verbatim: "Keep it practical. A short, accurate AGENTS.md is more useful than a long file full of vague rules. Start with the basics, then add new rules only after you notice repeated mistakes." / "When Codex makes the same mistake twice, ask it for a retrospective and update AGENTS.md. Guidance stays practical and based on real friction."
- Tier: **Verified** (official docs). The exact [P4]/[P5]/[P9] discipline, applied to the config file — identical in spirit to Anthropic's F-03/F-07.

### F-19 — Improve reliability with testing and review; the agent needs to know what "good" looks like [P8 + P7]
- Claim: Don't stop at "make a change" — ask Codex to create tests, run the relevant checks (test suites, lint, formatting, type checks), confirm the result, and review the diff; it can run this loop only if it knows what "good" looks like.
- Source: https://developers.openai.com/codex/learn/best-practices (official) — read in full.
- Verbatim: "Don't stop at asking Codex to make a change. Ask it to create tests when needed, run the relevant checks, confirm the result, and review the work before you accept it. Codex can do this loop for you, but only if it knows what 'good' looks like." / "Writing or updating tests for the change, Running the right test suites, Checking lint, formatting, or type checks, Confirming the final behavior matches the request, Reviewing the diff for bugs, regressions, or risky patterns."
- Tier: **Verified** (official docs). [P8] + [P7] — the full verify loop as a first-class agent duty.

### F-20 — "At OpenAI, Codex reviews 100% of PRs" [P10 code review]
- Claim: OpenAI states that at OpenAI, Codex reviews 100% of PRs (automatic or reactive via @Codex) — code review is a core, automated agent duty.
- Source: https://developers.openai.com/codex/learn/best-practices (official) — read in full.
- Verbatim: "If you use GitHub Cloud, you can set up Codex to run code reviews for your PRs. At OpenAI, Codex reviews 100% of PRs. You can enable automatic reviews or have Codex reactively review when you @Codex."
- Tier: **Verified** (official docs). [P10] (code review as a maintainability practice, now agent-performed at 100% coverage).

### F-21 — MCP: add tools only when they unlock a real workflow [P5 YAGNI + P4 KISS]
- Claim: OpenAI explicitly advises against wiring in every tool: start with one or two that remove a manual loop you already do often, then expand — a YAGNI stance on tooling.
- Source: https://developers.openai.com/codex/learn/best-practices (official) — read in full.
- Verbatim: "Add tools only when they unlock a real workflow. Do not start by wiring in every tool you use. Start with one or two tools that clearly remove a manual loop you already do often, then expand from there."
- Tier: **Verified** (official docs). [P5]/[P4] applied to agent tooling — don't build/integrate before it's needed.

### F-22 — Skills: keep each scoped to one job; don't cover every edge case up front [P2 SRP + P5 YAGNI]
- Claim: OpenAI's skill guidance is to keep each skill scoped to one job with clear inputs/outputs, and to start with one representative task rather than covering every edge case up front.
- Source: https://developers.openai.com/codex/learn/best-practices (official) — read in full.
- Verbatim: "Keep each skill scoped to one job. Start with 2 to 3 concrete use cases, define clear inputs and outputs, and write the description so it says what the skill does and when to use it." / "Don't try to cover every edge case up front. Start with one representative task, get it working well, then turn that workflow into a skill and improve from there."
- Tier: **Verified** (official docs). [P2] (single responsibility per skill) + [P5] (don't pre-build for imagined edge cases).

### F-23 — "If you keep reusing the same prompt or correcting the same workflow, it should probably become a skill" [P3 DRY]
- Claim: OpenAI's rule of thumb is to extract repeated prompts/workflows into reusable skills — the DRY principle applied to agent instructions.
- Source: https://developers.openai.com/codex/learn/best-practices (official) — read in full.
- Verbatim: "A good rule of thumb: if you keep reusing the same prompt or correcting the same workflow, it should probably become a skill."
- Tier: **Verified** (official docs). [P3] (no duplication — factor the repeated instruction into one place).

### F-24 — Use scheduled tasks for reflection and maintenance, not just execution [P9 Boy Scout]
- Claim: OpenAI recommends scheduling Codex for reflection/maintenance — reviewing recent chats, summarizing repeated friction, and improving prompts/instructions/workflow over time — i.e., continuous self-improvement of the setup.
- Source: https://developers.openai.com/codex/learn/best-practices (official) — read in full.
- Verbatim: "Use scheduled tasks for reflection and maintenance, not just execution. Review recent chats, summarize repeated friction, and improve prompts, instructions, or workflow setup over time."
- Tier: **Verified** (official docs). [P9] (leave the system cleaner/better than you found it) — the Boy Scout Rule automated.

### F-25 — Keep one chat per coherent unit of work [P2 SRP + P4 KISS]
- Claim: OpenAI's common-mistakes list warns against using one chat for an entire project (bloated context, worse results); keep one chat per coherent unit of work.
- Source: https://developers.openai.com/codex/learn/best-practices (official) — read in full.
- Verbatim: "Keep one chat per coherent unit of work. If the work is still part of the same problem, staying in the same chat is often better because it preserves the reasoning trail. Fork only when the work truly branches." / (Common mistakes) "Using one chat for an entire project instead of one chat per coherent outcome. This leads to bloated context and worse results over time."
- Tier: **Verified** (official docs). [P2] (one unit of work = one scope) + [P4] (avoid the bloated, hard-to-manage context).

### F-26 — Common mistake: overloading the prompt with durable rules instead of AGENTS.md/skill [P4 KISS + P10]
- Claim: OpenAI lists "overloading the prompt with durable rules instead of moving them into AGENTS.md or a skill" as a common first-time mistake — durable rules belong in the config file, not repeated in every prompt.
- Source: https://developers.openai.com/codex/learn/best-practices (official) — read in full.
- Verbatim: "A few common mistakes to avoid when first using Codex: Overloading the prompt with durable rules instead of moving them into AGENTS.md or a skill. Not letting the agent see its work by not giving details on how to best run build and test commands. Skipping planning on multi-step and complex tasks."
- Tier: **Verified** (official docs). [P4]/[P10] (put durable knowledge in one clean place) + [P8] (the "not letting the agent see its work" item is the testing/verification gap).

---

## D. Cognition (Devin) — "Don't Build Multi-Agents" (Walden Yan, co-founder/CPO)

### F-27 — "At the core of reliability is Context Engineering" [cross-cutting + P10]
- Claim: Cognition's framing is that for long-running, reliable agents, the #1 engineering job is context engineering — managing what the agent sees — which is the agent-world analog of keeping the working context clean and coherent.
- Source: https://cognition.com/blog/dont-build-multi-agents (official Cognition blog, Walden Yan, June 2025) — read in full.
- Verbatim: "When agents have to actually be reliable while running for long periods of time and maintain coherent conversations, there are certain things you must do to contain the potential for compounding errors. ... At the core of reliability is Context Engineering." / "'Context engineering' is the next level of this. It is about doing this automatically in a dynamic system. ... effectively the #1 job of engineers building AI agents."
- Tier: **Verified** (official blog, read in full). Cross-cutting: a clean, well-managed context is the reliability substrate — the agent-context analog of a clean codebase.

### F-28 — Principle 1: share full agent traces, not just messages [P10 + cross-cutting]
- Claim: Cognition's first principle of context engineering is to share full context/traces between collaborating parts, not just individual messages, so decisions don't get lost.
- Source: https://cognition.com/blog/dont-build-multi-agents (official) — read in full.
- Verbatim: "Principle 1: Share context, and share full agent traces, not just individual messages."
- Tier: **Verified** (official blog). [P10] (complete, unambiguous information flow) — the agent-world version of "don't lose the context of a decision."

### F-29 — Principle 2: actions carry implicit decisions; conflicting decisions → bad results [cross-cutting + P10]
- Claim: Cognition's second principle: every action encodes implicit decisions, and when parallel agents make conflicting implicit decisions the result is bad — so architectures must avoid dispersed, conflicting decision-making.
- Source: https://cognition.com/blog/dont-build-multi-agents (official) — read in full.
- Verbatim: "Principle 2: Actions carry implicit decisions, and conflicting decisions carry bad results." / "I would argue that Principles 1 & 2 are so critical, and so rarely worth violating, that you should by default rule out any agent architectures that don't abide by them."
- Tier: **Verified** (official blog). Cross-cutting: consistency of decisions (a clean-code value) is a reliability requirement for agents.

### F-30 — Simplest reliable architecture = single-threaded linear agent [P4 KISS + cross-cutting]
- Claim: Cognition's recommendation is that the simplest way to satisfy the context principles is a single-threaded linear agent with continuous context; multi-agent parallelism is "fragile" today.
- Source: https://cognition.com/blog/dont-build-multi-agents (official) — read in full.
- Verbatim: "The simplest way to follow the principles is to just use a single-threaded linear agent. Here, the context is continuous." / "it is evident that in 2025, running multiple agents in collaboration only results in fragile systems. The decision-making ends up being too dispersed and context isn't able to be shared thoroughly enough between the agents."
- Tier: **Verified** (official blog). [P4] (the simple design is the reliable one) — a vendor's explicit KISS argument for agent architecture.

### F-31 — Claude Code subagents only answer questions, don't write code, because they lack context [P2 SRP + cross-cutting]
- Claim: Cognition notes Claude Code deliberately uses subagents only to answer well-defined questions (not to write code) because a subagent lacks the main agent's context — a single-responsibility constraint driven by context limits.
- Source: https://cognition.com/blog/dont-build-multi-agents (official) — read in full.
- Verbatim: "Claude Code is an example of an agent that spawns subtasks. However, it never does work in parallel with the subtask agent, and the subtask agent is usually only tasked with answering a question, not writing any code. Why? The subtask agent lacks context from the main agent that would otherwise be needed to do anything beyond answering a well-defined question."
- Tier: **Verified** (official blog). [P2] (each subagent does one narrow thing) — a concrete, vendor-observed SRP pattern in a shipping product.

### F-32 — Edit-apply models: a markdown explanation + a small model rewriting the file was more reliable than a big model emitting a diff [P4 KISS + P10]
- Claim: Cognition describes the historical "edit apply model" pattern — having a large model emit a markdown explanation of the change and a small model rewrite the file — as more reliable than a large model emitting a formatted diff; today a single model does both in one action.
- Source: https://cognition.com/blog/dont-build-multi-agents (official) — read in full.
- Verbatim: "The key idea was that it was actually more reliable to get a small model to rewrite your entire file, given a markdown explanation of the changes you wanted, than to get a large model to output a properly formatted diff. ... Today, the edit decision-making and applying are more often done by a single model in one action."
- Tier: **Verified** (official blog). [P4]/[P10] (the simpler, more legible representation — markdown explanation — was more reliable than the clever diff).

---

## E. Cursor — Rules docs (official)

### F-33 — Rules = persistent, reusable context because LLMs don't retain memory between completions [P10 + cross-cutting]
- Claim: Cursor's rules exist because LLMs don't retain memory between completions; rules inject persistent, reusable context at the start of the model context to give the AI consistent guidance for generating code and interpreting edits.
- Source: https://cursor.com/docs/rules (official Cursor docs) — read in full.
- Verbatim: "Large language models don't retain memory between completions. Rules provide persistent, reusable context at the prompt level. When applied, rule contents are included at the start of the model context. This gives the AI consistent guidance for generating code, interpreting edits, or helping with workflows."
- Tier: **Verified** (official docs). [P10] (consistency) — the mechanism by which clean-code conventions persist across an agent's stateless completions.

### F-34 — Best practices: focused, actionable, scoped; under 500 lines; split into composable rules [P4 KISS + P2 SRP + P10]
- Claim: Cursor's rule best practices are to keep rules focused/actionable/scoped, under 500 lines, split large rules into composable ones, provide concrete examples, avoid vague guidance ("write rules like clear internal docs"), and reuse rules when repeating prompts.
- Source: https://cursor.com/docs/rules (official) — read in full.
- Verbatim: "Good rules are focused, actionable, and scoped. Keep rules under 500 lines, Split large rules into multiple, composable rules, Provide concrete examples or referenced files, Avoid vague guidance. Write rules like clear internal docs, Reuse rules when repeating prompts in chat."
- Tier: **Verified** (official docs). [P4] (scoped, not bloated) + [P2] (composable single-purpose rules) + [P10] (clear docs) + [P3] (reuse).

### F-35 — Concrete rule: keep components under 200 lines; extract subcomponents [P2 small functions/SRP]
- Claim: Cursor's own example project rule encodes the small-function/single-responsibility principle directly: keep components under 200 lines and extract subcomponents when a file grows beyond that.
- Source: https://cursor.com/docs/rules (official) — read in full.
- Verbatim (example "Apply to Specific Files" rule): "Keep components under 200 lines. Extract subcomponents into the same directory when a file grows beyond that."
- Tier: **Verified** (official docs). A direct, shipped example of [P2] encoded as an agent rule.

### F-36 — Concrete rules: composition over prop drilling; one service per file [P6 SOLID + P10]
- Claim: Cursor's example rules encode design principles: prefer composition over prop drilling, and define each service in its own file (single-responsibility / predictable architecture).
- Source: https://cursor.com/docs/rules (official) — read in full.
- Verbatim (example rules): "Prefer composition over prop drilling. Pass children or render props instead of threading data through multiple layers." / "Define each service in its own file under `src/services/`."
- Tier: **Verified** (official docs). [P6] (composition, SRP) encoded for the agent.

### F-37 — Concrete rules: validate inputs at the boundary; structured error objects; reversible migrations [P7 error handling]
- Claim: Cursor's example rules encode error-handling discipline: validate inputs at the service boundary, return structured error objects (never raw strings), and make every migration reversible (up + down).
- Source: https://cursor.com/docs/rules (official) — read in full.
- Verbatim (example rules): "Always validate inputs at the service boundary before passing data to internal functions." / "Return structured error objects with a `code` and `message` field, never throw raw strings." / "Every database migration must have both `up` and `down` functions so it can be fully reversed."
- Tier: **Verified** (official docs). [P7] (no raw/ignored errors, defensive boundaries, reversibility) — the cleanest shipped example of error-handling rules for an agent.

### F-38 — Concrete rules: named exports; snake_case columns; read source before proposing changes [P1 naming + P10]
- Claim: Cursor's example rules encode naming/consistency and a "don't guess" discipline: use named exports, snake_case for DB columns, and read the relevant source files before proposing changes when unsure.
- Source: https://cursor.com/docs/rules (official) — read in full.
- Verbatim (example rules): "Use named exports, not default exports." / "Use snake_case for database columns." / "When you are unsure about implementation details, read the relevant source files before proposing changes."
- Tier: **Verified** (official docs). [P1] (consistent, meaningful naming) + [P10] (don't guess — read the code).

### F-39 — AGENTS.md as the simple, readable alternative to structured rules [P10]
- Claim: Cursor supports AGENTS.md as a plain-markdown, "simple, readable instructions" alternative to .cursor/rules, including nested AGENTS.md in subdirectories where more specific instructions take precedence.
- Source: https://cursor.com/docs/rules (official) — read in full.
- Verbatim: "AGENTS.md is a simple markdown file for defining agent instructions. ... It's perfect for projects that need simple, readable instructions without the overhead of structured rules." / (example) "## Code Style - Use TypeScript for all new files - Prefer functional components in React - Use snake_case for database columns ## Architecture - Follow the repository pattern - Keep business logic in service layers."
- Tier: **Verified** (official docs). [P10] (readability) + [P6] (architecture rules) — and confirms the cross-tool AGENTS.md convergence (F-12).

---

## F. Aider — Specifying coding conventions (official)

### F-40 — Conventions file: a small markdown file of coding guidelines loaded into the chat [P1 + P10]
- Claim: Aider's mechanism for clean-code conventions is a small markdown file (e.g. CONVENTIONS.md) listing guidelines (type hints, preferred libraries) that you load into the chat; best loaded read-only and cached.
- Source: https://aider.chat/docs/usage/conventions.html (official Aider docs) — read in full.
- Verbatim: "Sometimes you want GPT to be aware of certain coding guidelines, like whether to provide type hints, which libraries or packages to prefer, etc. The easiest way to do that with aider is to simply create a small markdown file and include it in the chat." / "It's best to load the conventions file with /read CONVENTIONS.md or aider --read CONVENTIONS.md. This way it is marked as read-only, and cached if prompt caching is enabled."
- Tier: **Verified** (official docs). [P1]/[P10] (conventions as a small, readable, reusable file) — the earliest/simplest form of the agent-instruction-file pattern.

### F-41 — Demonstrated: WITH conventions the model uses httpx + type hints; WITHOUT it uses requests and skips types [P1 + P10 + cross-cutting] — KEY
- Claim: Aider's worked example shows the model's default output is *not* clean: without CONVENTIONS.md it used `requests` and skipped type hints ("perhaps more typical in small python scripts"); with the conventions file ("Prefer httpx over requests ... Use types everywhere possible") it correctly used httpx and provided type hints.
- Source: https://aider.chat/docs/usage/conventions.html (official) — read in full.
- Verbatim: "GPT correctly used `httpx` and provided type hints. See below for the transcript of this same coding task conducted _without_ using `CONVENTIONS.md`. In this case, GPT used `requests` and skipped types, which is perhaps more typical in small python scripts."
- Tier: **Verified** (official docs, worked example). A concrete, reproducible demonstration that LLMs do not write clean code by default — you must encode the conventions. This is the practice-world twin of the papers-lane finding that LLMs optimize for the minimal change.

---

## G. GitHub Copilot — custom instructions (official)

### F-42 — Cross-tool convergence: .github/copilot-instructions.md, AGENTS.md, and CLAUDE.md are all supported [P10 + cross-cutting]
- Claim: GitHub's local agent harness accepts project instructions in .github/copilot-instructions.md, AGENTS.md, or CLAUDE.md; the Copilot coding agent supports .github/copilot-instructions.md, .github/instructions/**.instructions.md, plus CLAUDE.md and GEMINI.md — confirming the field is converging on shared instruction files.
- Source: https://code.visualstudio.com/docs/agent-customization/custom-instructions + https://github.blog/changelog/2025-08-28-copilot-coding-agent-now-supports-agents-md-custom-instructions/ (official GitHub/VS Code) — read (search + changelog).
- Verbatim: "For Local harness sessions: Project instructions can use .github/copilot-instructions.md, AGENTS.md, or CLAUDE.md." / "Alongside AGENTS.md, the agent continues to support GitHub's .github/copilot-instructions.md and .github/instructions/**.instructions.md formats, plus CLAUDE.md and GEMINI.md files."
- Tier: **Verified** (official GitHub/VS Code). Cross-cutting: the clean-code-rules artifact is portable across the major agents — a strong, concrete data point for the report.

### F-43 — copilot-instructions.md = "onboard" the repo to a coding agent [P10]
- Claim: GitHub's recommended task for the file is to "onboard" the repository to a coding agent — describe how the agent, seeing the repo for the first time, can work most efficiently.
- Source: https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/ (official GitHub blog) — read (search snippet).
- Verbatim: "Your task is to 'onboard' this repository to a coding agent by adding a .github/copilot-instructions.md file. It should contain information describing how the agent, seeing the repo for the first time, can work most efficiently."
- Tier: **Verified** (official GitHub blog). [P10] (the file is an onboarding doc for a new "teammate" that happens to be an agent).

### F-44 — Code-review custom instructions: async/await, structured try/catch, isolated state [P7 error handling + P10 + P6]
- Claim: GitHub's code-review instruction example encodes concrete clean-code/anti-pattern rules: prefer async/await over .then() chains, wrap every API call in a structured try/catch, and keep React local UI state isolated from global stores.
- Source: https://docs.github.com/en/copilot/tutorials/customize-code-review (official GitHub docs) — read (search snippet).
- Verbatim: "### Code Style & Anti-Patterns Enforce these strict patterns for code inspection: - **Asynchronous Code:** Prefer `async/await` syntax over explicit `.then()` chains. - **Error Handling:** Every API call must be wrapped in a structured `try/catch` block. - **State Management:** React components must keep local UI state completely isolated from global stores."
- Tier: **Verified** (official GitHub docs). [P7] (structured error handling) + [P10] (consistent style) + [P6] (state isolation / SRP).

### F-45 — For large repos, break instructions into multiple focused files [P2 SRP + P10]
- Claim: GitHub recommends, for large repositories with many concerns, splitting instructions into multiple focused files (AGENTS.md for agent-specific, copilot-instructions.md for general standards, and per-language/security/api .instructions.md files).
- Source: https://docs.github.com/en/copilot/tutorials/customize-code-review (official) — read (search snippet).
- Verbatim: "For large repositories with many concerns, break instructions into multiple focused files: AGENTS.md # Agent-specific, .github/copilot-instructions.md # General standards, .github/instructions/python.instructions.md # Python-specific, javascript.instructions.md # JavaScript-specific, security.instructions.md # Security-specific, api.instructions.md # API-specific."
- Tier: **Verified** (official GitHub docs). [P2] (single-responsibility per instruction file) + [P10] (organized, navigable guidance).

### F-46 — Best practice: run the formatter before every commit [P10 + P7]
- Claim: GitHub's Copilot task best-practices example makes "run `make fmt` before committing any changes to ensure proper code formatting" a required, codified step.
- Source: https://docs.github.com/copilot/how-tos/agents/copilot-coding-agent/best-practices-for-using-copilot-to-work-on-tasks (official) — read (search snippet).
- Verbatim: "Please follow these guidelines when contributing: ## Code Standards ### Required Before Each Commit - Run `make fmt` before committing any changes to ensure proper code formatting - This will run gofmt on all Go files to maintain consistent ..."
- Tier: **Verified** (official GitHub docs). [P10] (consistent formatting) + [P7] (a deterministic pre-commit gate).

---

## H. Simon Willison (prominent AI engineer / Datasette author)

### F-47 — "Clean code is the way. Less docs. Linters define the style. Tests define the intent. Code defines the architecture." [P10 + P8 + P1 + P6] — KEY
- Claim: Willison's pithy statement: clean code is the way; you need less docs because linters define the style, tests define the intent, and the code defines the architecture — if you need docs to explain code you can't just ask an LLM about, the code isn't clean enough.
- Source: https://x.com/simonw/status/1982158311739867546 (Simon Willison, X/Twitter, 2025) — read (search snippet of his own post).
- Verbatim: "Clean code is the way. Less docs. Linters define the style. Tests define the intent. Code-defines the architecture. If you need docs for your code, and you can't just ask an LLM what's going on, then your code's not clean enough."
- Tier: **Verified** (direct quote from his X account via search; social-media post, not a long-form doc). A world-leading AI engineer's one-line thesis that maps [P1] (linters→style), [P8] (tests→intent), [P6] (code→architecture), [P10] (readability) onto the agent era.

### F-48 — Keeping code clean means examples (e.g. how to write a test) point in the right direction [P8 + P10]
- Claim: Willison (coding-agents tag) frames clean code as making the right examples discoverable: keeping the code clean means when someone (or an agent) looks for examples of how to write a test, they're pointed in the right direction.
- Source: https://simonwillison.net/tags/coding-agents/ (Simon Willison, blog tag index) — read (search snippet).
- Verbatim: "It's similar to how working on large projects with a team of other developers work - keeping the code clean means when people look for examples of how to write a test they'll be pointed in the right direction."
- Tier: **Plausible** (tag-index snippet; the underlying post not read in full this lane). [P8] (tests as discoverable examples) + [P10] (a clean codebase is a good reference).

### F-49 — "Boring technology": innovate on the unique part, use tried-and-tested for the rest [P4 KISS]
- Claim: Willison applies "boring technology" to LLM coding: stick with stable, popular libraries (well-represented in training data) and innovate only on the project's unique selling points.
- Source: https://simonw.substack.com/p/how-i-use-llms-to-help-me-write-code (Simon Willison's Newsletter, 2025-03-11) — read in full.
- Verbatim: "I like applying the principles of boring technology - innovate on your project's unique selling points, stick with tried and tested solutions for everything else."
- Tier: **Verified** (long-form post, read in full). [P4] (KISS / boring technology) applied to agent-era library choice.

### F-50 — "You have to test what it writes!" + use tools that can run the code [P8 testing]
- Claim: Willison's how-I-use-LLMs post has an explicit section "You have to test what it writes!" and "Use tools that can run the code for you" — testing/running the code is non-negotiable.
- Source: https://simonw.substack.com/p/how-i-use-llms-to-help-me-write-code (Simon Willison's Newsletter, 2025-03-11) — read in full.
- Verbatim (section headings + body): "You have to test what it writes!" / "Use tools that can run the code for you." / "I feel like programmers have it easy ... they can tether their A.I.s to reality, because they can demand the agents test the code to see if it runs correctly." (Pragmatic Summit fireside chat)
- Tier: **Verified** (long-form post + talk, read). [P8] (tests/running code as the reality tether) — a prominent engineer's emphasis that the test loop is what makes agent coding safe.

### F-51 — "Context is king" + LLM coding is "difficult and unintuitive" [cross-cutting + P10]
- Claim: Willison's core craft is managing the model's context ("Context is king"), and he stresses that using LLMs to write code is "difficult and unintuitive" with "precious little guidance" — the sharp/soft edges must be learned.
- Source: https://simonw.substack.com/p/how-i-use-llms-to-help-me-write-code (Simon Willison's Newsletter, 2025-03-11) — read in full.
- Verbatim: "Context is king. Most of the craft of getting good results out of an LLM comes down to managing its context - the text that is part of your current conversation." / "Using LLMs to write code is difficult and unintuitive. It takes significant effort to figure out the sharp and soft edges of using them in this way, and there's precious little guidance to help people figure out how best to apply them."
- Tier: **Verified** (long-form post, read in full). Cross-cutting: context management (a clean-code-adjacent discipline) is the central skill; [P10] (a clean, navigable codebase is what makes context manageable).

---

## I. SWE-agent (Princeton / PLI) — the agent-computer interface (academic, world-leading)

> Note: LANE-2 (papers) covers SWE-agent in depth as F-02. Included here (lightly) because it is a world-leading *system* whose design decisions are a direct, citable practice statement about making the working environment "agent-ready."

### F-52 — A custom agent-computer interface (ACI) beats the human Linux shell for agents [cross-cutting + P4 KISS]
- Claim: SWE-agent (Princeton, NeurIPS 2024) shows a custom-built agent-computer interface — simple, efficient commands plus carefully crafted feedback — substantially outperforms the human-oriented Linux shell (12.5% vs baseline; +10.7 points over the shell-only agent).
- Source: https://arxiv.org/abs/2405.15793 (research paper, arXiv, Princeton PLI, NeurIPS 2024) — read (abstract + intro).
- Verbatim: "We find that custom ACIs tailored to LMs can outperform existing user interfaces (UIs), such as the Linux shell, designed for human users." / "SWE-agent solves 10.7 percentage points more issues than the baseline agent that uses just the default Linux shell."
- Tier: **Verified** (abstract + intro read). Cross-cutting: the "clean, well-structured working surface" improves agent outcomes — the tooling-side twin of clean code.

### F-53 — The ACI integrates a code linter into the edit action and returns informative error feedback [P7 error handling + P10]
- Claim: SWE-agent's ACI integrates a code linter into the edit function to alert the agent of mistakes it introduces, and returns informative error messages for edits with syntax errors — i.e., the environment gives the agent immediate, actionable error feedback.
- Source: https://arxiv.org/abs/2405.15793 (research paper, arXiv, Princeton PLI) — read (abstract + intro + design section).
- Verbatim: "we integrate a code linter into the edit function to alert the agent of mistakes it may have introduced when editing a file. Select errors from the linter are shown to the agent along with a snippet of the file contents before/after the error was introduced." / "it does not provide any feedback when invalid edits are made ... This leads us to construct a novel agent-computer interface ... including informative error messages for edits that contain syntax errors."
- Tier: **Verified** (read). [P7] (never ignore errors — the interface surfaces them) + [P10] (legible, actionable feedback). This is the academic anchor for the "give the agent a runnable check" theme (F-01/F-19).

### F-54 — ACI design principle: actions should be simple and efficient [P4 KISS + P2]
- Claim: SWE-agent's effective-ACI principles are that actions should be simple (few options, concise docs) and efficient (consolidate important operations into as few actions as possible) — a KISS/SRP argument for the agent's tool surface.
- Source: https://arxiv.org/abs/2405.15793 (research paper, arXiv, Princeton PLI) — read (design section).
- Verbatim: "Actions should be simple and easy to understand. Many bash commands have documentation that includes dozens of options. Simple commands with a few options and concise documentation are easier for agents to use." / "Actions should be efficient. Important operations (e.g., file navigation, editing) should be consolidated into as few actions as possible."
- Tier: **Verified** (read). [P4] (simple) + [P2] (consolidated, single-purpose actions).

---

## J. "Clean code for AI agents" / "agent-ready codebase" practitioner posts

### F-55 — "A coding agent learns your conventions from the code it reads; code quality sets a ceiling on its output" [P10 + cross-cutting] — KEY
- Claim: The central practitioner claim: an agent learns the project's conventions from the code it reads, so the quality of that code sets a ceiling on the quality of what it writes; clean code is "now a performance setting, not just an aesthetic preference," and "every property that helps a new teammate onboard also helps the agent, except the agent reads your code many times a day."
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner guide, "Clean Code for AI Agents: Make Your Codebase Agent-Ready") — read in full.
- Verbatim: "A coding agent learns your project's conventions from the code it reads, so the quality of that code sets a ceiling on the quality of what it writes." / "That is why clean code is now a performance setting, not just an aesthetic preference. Every property that helps a new teammate onboard also helps the agent, except the agent reads your code many times a day."
- Tier: **Verified** (read in full). The single best practitioner statement of [P10] (code is read more than written — now by an agent that reads it many times a day).

### F-56 — The agent-friendly codebase checklist = the clean-code checklist [P6 + P2 + P1 + P8 + P3 + P9]
- Claim: The agent-friendly checklist is literally the clean-code checklist: good abstractions that hide the layer below, reasonably sized methods/functions, clear honest names, principled service architecture, unit tests that pin behavior, and no dead code / duplicated logic / unreachable fallbacks.
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner guide) — read in full.
- Verbatim: "Good abstractions, where each layer hides the one below it instead of leaking it. Reasonably sized methods and functions, small enough to hold in view at once. Clear, honest names that say what a thing actually does. Principled service architecture ... Unit tests that pin behavior, so an agent can change code and immediately see whether it broke something. No dead code, no duplicated logic, and no fallbacks that can never run."
- Tier: **Verified** (read in full). A direct, itemized mapping of [P6]/[P2]/[P1]/[P8]/[P3]/[P9] onto "what makes a codebase agent-ready."

### F-57 — Naming + small files cut the agent's search/traversal cost [P1 + P2]
- Claim: Because an agent can't hold the whole codebase in context, it explores like a new teammate; putting code where it's expected and naming it what you'd first search for means "the agent reads one file instead of hunting through ten," and small well-named files beat one 2000-line file.
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner guide) — read in full.
- Verbatim: "put code where someone would expect it and name it what they would first search for. When the file is findable on the first guess, the agent reads one file instead of hunting through ten." / "keep files small. A single file of several thousand lines forces the agent to read chunk after chunk to locate the relevant part, while a set of well-named smaller files lets the filename itself point the way."
- Tier: **Verified** (read in full). [P1] (naming = findability) + [P2] (small files) with a concrete cost mechanism (token/latency of traversal).

### F-58 — Prefer deep modules (Ousterhout); shallow modules break agent testing [P6 SOLID + P8]
- Claim: The guide recommends deep modules (hide a lot behind a small interface, per Ousterhout's "A Philosophy of Software Design"); left unsupervised an agent sprouts many tiny shallow modules with tangled dependencies, which both costs traversal and makes testing unclear (no obvious test boundary → trivial per-function tests that never check the pieces work together).
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner guide) — read in full.
- Verbatim: "Prefer deep modules: ones that hide a lot of functionality behind a small, simple interface. The distinction comes from John Ousterhout's A Philosophy of Software Design. ... with dozens of thin pieces there is no obvious place to draw a test boundary or decide what to mock, so the agent falls back on wrapping each function in its own trivial test, which never checks that the pieces work together."
- Tier: **Verified** (read in full). [P6] (module depth / good design) + [P8] (testability) — a sophisticated, named-theory (Ousterhout) grounding for why design quality matters to agents.

### F-59 — Enforce with ONE script run by the agent AND as a pre-commit hook; prose rules can be skipped [P7 error handling + P10] — KEY
- Claim: The highest-leverage practice: write one script (linters + dead-code detector + complexity/method-size check + test suite, exit non-zero on failure), give the agent the command to run it, and install the same script as a pre-commit hook — because "a rule written in a CLAUDE.md or AGENTS.md file is only a suggestion it can skip, because to the model it is just more text in the prompt," so the gate that holds is the one the agent cannot bypass.
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner guide) — read in full.
- Verbatim: "Write one script that runs your linters, a dead-code detector, a complexity or method-size check, and your test suite, and exits non-zero on any failure. ... Give the agent the command to run that script. ... Install the same script as a pre-commit hook. Now nothing that fails the checks can enter the repository, whether a human or an agent wrote it." / "The agent will sometimes forget to run the checker, and a rule written in a CLAUDE.md or AGENTS.md file is only a suggestion it can skip, because to the model it is just more text in the prompt. So the gate that actually holds is the one the agent cannot bypass: a pre-commit hook."
- Tier: **Verified** (read in full). The strongest practice-world statement of [P7] (deterministic enforcement over advisory prose) — and the key reason the "machine-runnable check" theme dominates this lane.

### F-60 — Agents are reluctant to delete dead code and over-apply DRY; pair DRY with YAGNI [P9 + P3 + P5] — KEY nuance
- Claim: Two default agent behaviors to correct during cleanup: agents are reluctant to delete (they keep old code and add wiring so it stays callable), and they over-apply DRY (merging two similar call sites a human would leave apart, which turns brittle when they need to differ) — so explicitly tell the agent to remove what it replaces and ask for YAGNI alongside DRY.
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner guide) — read in full.
- Verbatim: "Agents are reluctant to delete: left alone they keep old code, add wiring so it stays callable, and leave dead code that confuses the next change, so tell the agent explicitly to remove what it replaces rather than assuming a cleanup pass subtracts anything. They also over-apply the DRY principle, pulling two similar call sites into one shared helper that a human would have left apart, which turns brittle the moment the two need to differ. Ask for the YAGNI principle alongside the cleanup."
- Tier: **Verified** (read in full). A crucial *tension* finding: [P3] DRY and [P5] YAGNI are not automatically balanced by agents — the human must enforce the balance. Directly relevant to the report's "does the principle transfer?" question.

### F-61 — Claude Code ships an official code-simplifier plugin (refine for clarity, preserve behavior) [P9 Boy Scout]
- Claim: Claude Code ships an official `code-simplifier` plugin — an agent that refines recent changes for clarity and consistency while preserving behavior — the packaged form of a focused cleanup/Boy-Scout pass.
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner guide) — read in full.
- Verbatim: "Claude Code ships an official `code-simplifier` plugin built for exactly this: an agent that refines recent changes for clarity and consistency while preserving behavior. It is the packaged form of spending one focused session on cleanup."
- Tier: **Verified** (read in full; the plugin's existence is a vendor fact, the description is the guide's). [P9] (refactor/leave it cleaner, behavior-preserving) — a shipping product feature for the Boy Scout Rule.

### F-62 — SonarSource controlled study: clean codebases → 7–8% fewer tokens, 34% fewer file revisits, SAME pass rate [P10 + P1 + cross-cutting] — KEY (quantified)
- Claim: A SonarSource controlled study of 660 Claude Code trials (33 tasks across six "minimal-pair" repo pairs identical in architecture but differing in cleanliness) finds clean code does not change whether the agent succeeds, but reduces token usage by 7–8% and file revisitations by 34%.
- Source: https://www.developersdigest.tech/blog/code-cleanliness-affects-ai-coding-agents (secondary coverage of the SonarSource study; figures re-checked against the arXiv abstract per the article) — read in full.
- Verbatim: "A controlled study of 660 Claude Code trials shows clean codebases reduce token usage by 7-8% and file revisitations by 34%, while pass rates stay the same." / "clean code does not change whether agents succeed at tasks, but it dramatically changes how efficiently they work." / "The key innovation was using 'minimal pairs' - repositories identical in architecture but differing in code cleanliness. This isolates code quality as the variable being measured."
- Tier: **Verified** (study exists and is described in detail; the 7–8%/34% figures are from the arXiv abstract per the article). The quantified, controlled anchor for [P10]/[P1] — and the important nuance that the payoff is *efficiency*, not *success rate*. (Cross-checks LANE-2's F-03/F-04 correlational/evolution evidence.)

### F-63 — SonarSource study HN: the most effective lever is strict linters + pre-commit hooks + automated checks [P7 + P10]
- Claim: In the Hacker News discussion of the SonarSource study, the most upvoted practical insight was that strict linters, pre-commit hooks, and automated code-quality checks are the most effective way to improve agent performance — and that you can use agents to clean the code first.
- Source: https://www.developersdigest.tech/blog/code-cleanliness-affects-ai-coding-agents (secondary coverage summarizing the HN thread, https://news.ycombinator.com/item?id=48798815) — read in full.
- Verbatim: "The most upvoted practical insight was around linting and deterministic guardrails. Multiple commenters shared that setting up strict linters, pre-commit hooks, and automated code quality checks has been the most effective way to improve agent performance in their workflows." / "if agents work more efficiently on clean code, you can use agents to clean the code first. Prompts like 'Refactor the Python code to make it more Pythonic' ... appear to both improve code quality and agent performance on subsequent tasks."
- Tier: **Verified** (HN thread summarized in the read article). [P7] (deterministic guardrails) + [P9] (use agents to clean first) — community consensus converging on the same "machine-runnable check" theme.

### F-64 — SonarSource study: clear naming + logical file structure help agents navigate [P1 + P10]
- Claim: The study's file-revisitation reduction suggests clear naming conventions and logical file structures help agents navigate codebases more efficiently; the article also flags that loose, permissive rules erode over long sessions (constraint decay), so explicit guardrails hold up better than soft conventions.
- Source: https://www.developersdigest.tech/blog/code-cleanliness-affects-ai-coding-agents (secondary coverage) — read in full.
- Verbatim: "File organization matters. The reduction in file revisitations suggests that clear naming conventions and logical file structures help agents navigate codebases more efficiently. Loose, permissive rules tend to erode over long sessions too."
- Tier: **Verified** (read in full). [P1] (naming) + [P10] (organization) with a measured mechanism (fewer revisits).

### F-65 — "No LLM does any of this by default ... You need to WRITE these rules. The agent reads, the agent follows." [P6 + P2 + P8 + P3 + P10]
- Claim: A practitioner's ~500-hours-of-agents summary: no LLM writes clean code by default — left alone it produces "average" code (no dependency injection, 80-line functions, no/wrong tests, duplicated logic, 2000-line files); you must explicitly write the rules, and the agent reads and follows them.
- Source: https://akitaonrails.com/en/2026-04-20/clean-code-for-ai-agents/ (practitioner blog, "Clean Code for AI Agents") — search snippet (live page returned 404 at research time).
- Verbatim (search-index snippet): "There's an important detail that only becomes clear after about 500 hours of using agents: no LLM does any of this by default. You tell it 'implement feature X' and it'll implement it the way the model considers average. No dependency injection. 80-line functions. No tests, or tests that mock the wrong thing. Duplicated logic because it's faster. 2000-line files because 'everything's in one place'. You need to WRITE these rules. The agent reads, the agent follows."
- Tier: **Plausible** (strong, specific, on-point quote from the search index, but the live page 404'd at research time so the full text could not be verified). Corroborated by F-41 (Aider's worked example) and F-55/F-56 — the "agents don't do clean code by default" claim is well-supported even if this single URL is unstable.

### F-66 — "Explain how the code should be organized — not only value, but also structure"; LLMs pick up repo style [P10 + P2]
- Claim: A practitioner's advice: when you give the agent a task, also explain how the code should be organized (not just the value, but the structure); if the code is properly organized, a feature might need the model to read just a couple of small files instead of dozens; LLMs are good at picking up the style in your repo.
- Source: https://www.yanist.com/clean-code-in-the-age-of-coding-agents/ (practitioner blog, "Clean code in the age of coding agents") — search snippet (not read in full).
- Verbatim (search-index snippet): "If your code is properly organized, implementing a feature might require a model to read just a couple of small files, and make changes, instead of having to read dozens going around in circles. ... When you give a task to your agent, make sure you also explain how the code should be organized. Not only value, but also structure. LLMs are pretty good at picking up the style in your repo."
- Tier: **Plausible** (search-snippet level; not read in full). [P10] (structure/organization) + [P2] (small files) — consistent with F-57.

### F-67 — HN: agents imitate visual style but hide coupling; they think "clean code" = tiny functions, not cohesive ones [P2 + P10] — KEY nuance
- Claim: A Hacker News commenter (on the "clean code in the age of coding agents" thread) warns that agents are good at imitating a visually similar style but hide coupling that's easy to miss (they don't understand the concepts they imitate), and that they tend to think "Clean Code" means splitting into tiny functions rather than cohesive functions.
- Source: https://news.ycombinator.com/item?id=47704285 (Hacker News comment, community) — search snippet.
- Verbatim (search-index snippet): "At least in my experience, they are good at imitating a 'visually' similar style, but they'll hide a lot of coupling that is easy to miss, since they don't understand the concepts they're imitating. They think 'Clean Code' means splitting into tiny functions, rather than cohesive functions."
- Tier: **Plausible** (community comment, snippet-level). A key *nuance* for the report: [P2] "small functions" is not the same as "cohesive" — agents can satisfy the letter (small) while violating the spirit (cohesion/low coupling). Pairs with F-60 (over-DRY).

---

## Searched, found nothing (evidence of absence)

- **A single vendor that publishes a formal, numbered "10 clean-code principles for agents" list** → None found. Vendors/practitioners all express the same underlying principles (short config files, runnable checks, small cohesive units, tests, deep modules, naming) but none frames them as "the 10 Clean Code principles applied to agents." The 10-principle frame is the report's lens, not a vendor's. (Anthropic, OpenAI, Cursor, GitHub, Aider docs + practitioner posts)
- **A vendor blog post explicitly titled "Clean Code for AI Agents" from Anthropic/OpenAI/Cursor/Cognition** → None found from the vendors themselves; the "Clean Code for AI Agents" / "agent-ready codebase" framing comes from *practitioner* blogs (aidailycheck, akitaonrails, yanist, dev.to), not the vendor engineering blogs. (Vendor blogs vs practitioner blogs)
- **Boris Cherny (Claude Code creator) or Andrej Karpathy publishing a dedicated "clean code for agents" post** → No dedicated post found in this lane's searches; their relevant statements (e.g. "agentic engineering," "Software 2.0") are about workflow/paradigm, not a clean-code-principles mapping. (web)
- **A vendor that recommends telling the agent to "write clean code" as a standing rule** → The opposite is the documented norm: Anthropic explicitly lists "Self-evident practices like 'write clean code'" as something to EXCLUDE from CLAUDE.md (F-04). No vendor found recommending it. (Anthropic docs)
- **Devin/Cognition publishing a "clean code" best-practices doc (beyond the multi-agent/context-engineering post)** → Cognition's public engineering content found here is the "Don't Build Multi-Agents" context-engineering post (F-27–F-32); no separate Cognition "clean code for agents" doc surfaced. (Cognition blog)
- **A measured study of the effect of *naming* [P1] or *DRY* [P3] specifically on agent *generation* correctness (vs efficiency)** → The SonarSource study (F-62) measures efficiency (tokens/revisits), not per-principle generation correctness; no practice source found isolating naming or DRY as the variable. (practitioner posts + web)

---

## Notes for the collector / final report

1. **The practice lane's headline answer:** World-leading AI developers and agent vendors are *overwhelmingly* pro-clean-code for agents, and they converge on **three mechanisms** that differ from the papers lane: (a) **a machine-runnable check** (tests/build/linter) gated by a **pre-commit hook / CI the agent cannot bypass** — because prose rules in CLAUDE.md/AGENTS.md "are only a suggestion it can skip"; (b) **keep the instruction file short, specific, and pruned** (bloat makes the agent ignore it); (c) **treat the codebase itself as the agent's training data** — its quality "sets a ceiling" on output, and clean/well-named/small/well-abstracted code makes the agent land changes in 1–2 tries. [F-01, F-03, F-16, F-18, F-34, F-55, F-59]
2. **The single most quotable practitioner thesis** is Simon Willison's: "Clean code is the way. Less docs. Linters define the style. Tests define the intent. Code defines the architecture." [F-47] — and the most quotable *quantified* result is the SonarSource study: clean codebases → 7–8% fewer tokens, 34% fewer file revisits, **same pass rate** (efficiency, not success). [F-62]
3. **Per-principle coverage map (what the practice/vendor sources actually evidence):**
   - [P1] naming — strong (F-38, F-40, F-41, F-57, F-64): naming = findability; linters define style.
   - [P2] small functions/SRP — strong but with a *cohesion* caveat (F-35, F-36, F-22, F-45, F-67): keep units small AND cohesive; agents over-split.
   - [P3] DRY — present but with an *over-application* caveat (F-23, F-56, F-60, F-65): agents over-DRY; pair with YAGNI.
   - [P4] KISS — strong (F-02, F-06, F-18, F-21, F-22, F-30, F-49, F-52, F-54): simple config, simple architecture, boring technology, simple ACI.
   - [P5] YAGNI — strong (F-06, F-18, F-21, F-22, F-60): don't over-engineer, don't pre-build, add rules/tools only after real friction.
   - [P6] SOLID — moderate (F-36, F-44, F-58, F-65): composition, SRP, deep modules (Ousterhout), DI — but mostly as *rules to encode*, less as measured agent behavior.
   - [P7] error handling — strong (F-01, F-05, F-08, F-19, F-37, F-44, F-46, F-53, F-59): deterministic checks, structured errors, linter-in-the-loop, pre-commit gates.
   - [P8] testing/TDD — strong (F-01, F-13, F-17, F-19, F-20, F-41, F-50, F-56): give the agent a runnable test; "add tests even if nobody asked"; "you have to test what it writes." (Note: this is the *value of a pre-existing/runnable suite*, distinct from LANE-2's finding that *agent-authored* throwaway tests are low-value.)
   - [P9] refactoring/Boy Scout — strong (F-03, F-07, F-14, F-16, F-24, F-61, F-63): prune the config, scheduled maintenance, code-simplifier plugin, "use agents to clean first."
   - [P10] readability/maintainability — the *dominant* theme across every source (F-11, F-33, F-42, F-43, F-47, F-51, F-55, F-56, F-62, F-66): code is read more than written, now by an agent that reads it many times a day.
4. **Two tensions to present, not contradictions:** (a) "Agents don't write clean code by default" (F-41, F-65) vs "LLMs pick up the style in your repo" (F-66) — both true: the *default* is average, but a *clean, well-organized* repo is picked up and rewarded. (b) "Small functions" (F-35) vs "cohesive, not tiny" (F-67) — the letter vs the spirit of [P2].
5. **The config-file convergence is a concrete, report-worthy fact:** CLAUDE.md (Anthropic), AGENTS.md (now Linux Foundation / Agentic AI Foundation), .cursor/rules (Cursor), .github/copilot-instructions.md (GitHub) are all supported, and several tools accept multiple (F-12, F-39, F-42). Clean-code rules for agents are a portable, version-controlled artifact.
6. **Cross-lane consistency:** this lane's "give the agent a runnable check" (F-01/F-19/F-59) and "clean codebase → better agent" (F-55/F-62) themes are the *practice* expression of LANE-2's *papers* findings (SWE-CI maintainability-over-time, SWE-agent ACI, SWE-Bench Pro complexity gap). The report should present them as two independent lines of evidence converging.
7. **Caveats to carry:** F-65 (akitaonrails) and F-66 (yanist) and F-67 (HN) are snippet-level (Plausible) — the akitaonrails live page 404'd at research time; confirm before quoting as a hard citation. F-62's exact 7–8%/34% figures are from the arXiv abstract via the secondary article — confirm against the primary SonarSource paper if quoted as hard numbers.
