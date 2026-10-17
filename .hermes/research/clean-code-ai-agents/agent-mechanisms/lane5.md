# LANE-5 — Agent-specific mechanisms: clean code × agent architecture

- **Task:** t_500d0b6b (RESEARCH-clean-code-ai-agents [LANE-5])
- **Lane scope:** How the 10 canonical Clean Code principles interact with the SPECIFIC MECHANISMS of LLM coding agents — (1) context window limits, (2) codebase-as-context / RAG, (3) test-driven verification loops, (4) the "agent writes → tests verify" paradigm, (5) encoding principles as explicit rules (CLAUDE.md / AGENTS.md / .cursor/rules / copilot-instructions.md). Classify each principle as AMPLIFIED / MOOT / INVERTED by the agent paradigm and map findings to the shared anchor principles [P1]–[P10].
- **Source types owned:** code (GitHub repos/issues of SWE-agent, Aider, SWE-bench, claude-code, aider) + semi-official (agent docs/CLI references, config-file conventions, agent-skills repos).
- **Language:** English (AI-facing text; verbatim quotes in original language).
- **Date of research:** 2026-10-17.
- **Tier scheme:** **Verified** (authoritative source for this exact target, actually read) / **Plausible** (sound general behavior, not demonstrated on-target) / **Speculative** (mechanism asserted, untested).

> Framing note: this lane does NOT re-derive the 10 principles (that is LANE-1's job). It takes the shared anchor set [P1 naming, P2 small functions/SRP, P3 DRY, P4 KISS, P5 YAGNI, P6 SOLID, P7 error handling, P8 unit testing/TDD, P9 refactoring/Boy Scout, P10 readability/maintainability] as given and asks, for each, what the *agent's own machinery* does to its weight. The single most important structural fact found across sources: **the agent's context window is a fixed, scarce, metered resource, and "distracting context can harm performance"** (SWE-agent, NeurIPS 2024). Nearly every AMPLIFIED/MOOT/INVERTED verdict below reduces to that one constraint.

---

## 1. Mechanism 1 — Context window limits (the foundational constraint)

**F1.1 — The context window is the binding constraint; performance degrades as it fills [cross-cutting].**
- Claim: Every agent best-practice reduces to one constraint: the context window fills fast and the model degrades as it fills, so managing context is the primary engineering task.
- Source: https://code.claude.com/docs/en/best-practices (Claude Code official docs, Anthropic)
- Quote: "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills. … A single debugging session or codebase exploration might generate and consume tens of thousands of tokens. This matters since LLM performance degrades as context fills. When the context window is getting full, Claude may start 'forgetting' earlier instructions or making more mistakes. The context window is the most important resource to manage."
- Tier: **Verified** (read).

**F1.2 — Context is a fixed cost; distracting context actively harms performance (academic grounding) [cross-cutting].**
- Claim: Unlike humans who can ignore irrelevant content, every token an agent sees has a fixed memory/computation cost, and irrelevant content degrades performance — the academic basis for why "less noise, more signal" (clean code) matters.
- Source: https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf (SWE-agent, NeurIPS 2024, academic paper)
- Quote: "humans can flexibly ignore unnecessary information, whereas all content has a fixed cost in memory and computation for LMs and distracting context can harm performance [27]."
- Tier: **Verified** (read).

**F1.3 — File reads are chunked/truncated; a giant file does not fit in one read [P2 small functions/files].**
- Claim: Agent CLIs cap file reads (Claude Code ~2000 lines/chunk by default; Cursor/Codex/Windsurf similar), so a large file cannot be read whole — small files/functions are a technical obligation, not just a readability preference.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog, 500+ hrs agent use)
- Quote: "File truncation. Most agent CLIs limit file reads to small ranges. Claude Code reads 2000 lines per chunk by default. Cursor, Codex, Windsurf, all have similar caps. A giant file simply doesn't fit into the context window in one shot."
- Tier: **Verified** (read).

**F1.4 — Attention/retrieval degrades well before the nominal window limit [cross-cutting].**
- Claim: Even large windows (200k–3M tokens) do not mean usable attention across all of it; needle-in-haystack retrieval quality drops well before the claimed limit, and the window is shared with CLAUDE.md, system prompt, chat history, tool and test output.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Claude Opus has a 200k-token window, Sonnet 1M, Gemini 1M. Sounds like a lot. In practice, 'needle in haystack' tests show retrieval quality drops well before the claimed limit. … The more you stuff into the window, the worse the detail precision. And the agent's context isn't just your code: it holds CLAUDE.md, the system prompt, chat history, tool output, error logs, test output. All competing for the same window."
- Tier: **Plausible** (practitioner report of benchmark behavior; specific model figures not independently re-verified here).

**F1.5 — "Context engineering" is the named discipline of deciding what to keep/remove [cross-cutting].**
- Claim: Power users routinely hit context limits and must manually curate what stays in the window — a new discipline that clean code (compact, low-coupling code) directly reduces the need for.
- Source: https://ivan-rubinson.medium.com/clean-code-is-crucial-in-the-llm-age-392569be8a90 (practitioner blog, first-principles)
- Quote: "LLM power-users often rub against context-window limits, and have to engage in 'context engineering', manually deciding what to keep and what to remove from the LLM's context."
- Tier: **Verified** (read).

**F1.6 — Tool calls and latency are metered costs; short files / small test output / concise logs keep the agent productive [cross-cutting].**
- Claim: Every Read/Edit/Bash burns tokens and adds latency, so compact code and terse output are economic as well as quality wins.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Tool calls cost tokens. Every Read or Edit or Bash burns input and output tokens. Short files, small test output, concise logs — all of that keeps the agent productive and the bill low."
- Tier: **Verified** (read).

**F1.7 — Context management is a named, measured failure mode of agents [cross-cutting].**
- Claim: In long-horizon agent benchmarks, "context management" is an explicitly catalogued failure mode (smaller models fail on it more), confirming it is a first-class engineering concern, not a footnote.
- Source: https://arxiv.org/html/2509.16941v1 (SWE-Bench Pro, arXiv/Scale, benchmark paper)
- Quote: "Larger models (e.g., Opus 4.1) often fail on semantic or algorithmic correctness in large, multi-file edits, whereas smaller models (e.g., Qwen 3 32B) more frequently fail due to issues in syntax and formatting, tool use, or context management."
- Tier: **Plausible** (benchmark diagnostic; specific model/version results not independently reproduced here).

---

## 2. Mechanism 2 — Codebase-as-context / RAG (how the agent retrieves and navigates)

**F2.1 — Aider ships a "repo map": a ranked, token-budgeted structural overview of the whole repo [P1 naming, P3 DRY].**
- Claim: Aider sends the LLM a concise map of the entire git repo (key classes/functions + signatures), selected by a graph-ranking algorithm over file dependencies, so the agent sees the whole codebase's structure within a fixed token budget without loading every file.
- Source: https://aider.chat/docs/repomap.html (Aider official docs)
- Quote: "Aider uses a concise map of your whole git repository that includes the most important classes and functions along with their types and call signatures. … for large repositories even just the repo map might be too large for the LLM's context window. Aider solves this problem by sending just the most relevant portions of the repo map. It does this by analyzing the full repo map using a graph ranking algorithm, computed on a graph where each source file is a node and edges connect files which have dependencies. … The token budget is influenced by the --map-tokens switch, which defaults to 1k tokens."
- Tier: **Verified** (read).

**F2.2 — The repo map selects the *most-referenced* symbols → naming and coupling determine what the agent actually sees [P1 naming, P3 DRY, P6 coupling].**
- Claim: The map includes "the most important identifiers, the ones which are most often referenced by other portions of the code" — so distinctive, well-referenced names and low duplication are what get surfaced to the agent; poorly-named or duplicated code is under-represented in the agent's view.
- Source: https://aider.chat/docs/repomap.html (Aider official docs)
- Quote: "The sample map shown above doesn't contain every class, method and function from those files. It only includes the most important identifiers, the ones which are most often referenced by other portions of the code. These are the key pieces of context that the LLM needs to know to understand the overall codebase."
- Tier: **Verified** (read).

**F2.3 — The map's purpose is to make the agent *reuse* existing abstractions (DRY/consistency as a retrieval property) [P3 DRY, P10 consistency].**
- Claim: The repo map exists specifically so the agent writes new code that "respects and utilizes existing libraries, modules and abstractions found elsewhere in the codebase" — i.e., DRY/consistency is enforced by the retrieval mechanism, not by the agent's goodwill.
- Source: https://aider.chat/docs/repomap.html (Aider official docs)
- Quote: "The repo map also helps aider write new code that respects and utilizes existing libraries, modules and abstractions found elsewhere in the codebase."
- Tier: **Verified** (read).

**F2.4 — Grep/lexical search is the agent's primary navigation API; distinctive names are the interface [P1 naming].**
- Claim: Agents prefer `rg "name"` over loading whole files (cheaper, faster, on-target), so a name's value is measured by how few irrelevant hits it returns — "searchable" becomes the dominant property of a good name, over "pronounceable."
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Grep is cheaper than read. The agent knows this. It prefers rg 'funcName' over loading a whole file. It's faster, uses fewer tokens, hits the target. Unique, distinctive names make that much more effective. … greppable names aren't just 'nice for humans', they're the agent's primary navigation API."
- Tier: **Verified** (read).

**F2.5 — SWE-agent's ACI exposes find_file / search_file / search_dir with suppressed (≤50) results [P1 naming, cross-cutting].**
- Claim: The research-grade agent interface provides dedicated search commands that deliberately suppress verbose output, reinforcing that navigation is search-driven and that terse, targeted results are what the agent can use.
- Source: https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf (SWE-agent, NeurIPS 2024)
- Quote: "We introduce the special commands find_file, search_file, and search_dir, which output a summary of search results when searching for filenames and strings within files or directories. … Our interface encourages efficient searches by suppressing verbose results. The search commands return at most 50 [results]."
- Tier: **Verified** (read).

**F2.6 — Consistent formatting/indentation reduces the tokens the agent spends "internalizing the mess" [P10 consistency].**
- Claim: Inconsistent indentation / mixed tabs-spaces / varied brace style forces the agent to burn tokens normalizing the code before it can reason; consistency is a retrieval/navigation efficiency, not just aesthetics.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Grepping by visual pattern is hard. If you used inconsistent indentation, mixed tabs and spaces, varied brace style between files, the agent spends tokens internalizing the mess. Consistency helps."
- Tier: **Verified** (read).

**F2.7 — Predictable directory structure lets the agent anticipate paths without exploring [P10 structure / cross-cutting].**
- Claim: Framework conventions (controller/model/view, src/lib/test) let the agent predict where code lives; idiosyncratic layouts cost the agent tokens in `find`/exploration.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "If src/controllers/users.rb implies src/models/user.rb and src/views/users/, the agent can anticipate paths without listing directories. If the project uses idiosyncratic naming (random files, unpatterned names, everything flat in one folder), the agent loses time with find."
- Tier: **Verified** (read).

**F2.8 — Steering context: point the agent at the files that show the pattern you want [P3 DRY, P10 consistency].**
- Claim: For legacy code you can't rewrite, the practical lever is to steer the agent's retrieval — point it at the good-pattern files/directories and keep new work in cleanly separated modules so old habits don't propagate.
- Source: https://aidailycheck.com/learn/clean-code-for-ai-agents (practitioner blog, "Make Your Codebase Agent-Ready")
- Quote: "You cannot always rewrite the legacy, but you can steer context: point the agent at the files and directories that show the pattern you want, keep new work in cleanly separated modules, and let the checker stop old habits from spreading into new code."
- Tier: **Plausible** (practitioner guidance; not a measured result).

---

## 3. Mechanism 3 — Test-driven verification loops ("agent writes → tests verify")

**F3.1 — The core loop is gather-context → take-action → verify-results; verification is a first-class phase [P8 TDD, cross-cutting].**
- Claim: The agentic loop is explicitly three phases — gather context, take action, verify results — and "fix the failing tests" is the canonical worked example (run suite → read error → find files → edit → re-run).
- Source: https://code.claude.com/docs/en/how-claude-code-works (Claude Code official docs)
- Quote: "When you give Claude a task, it works through three phases: gather context, take action, and verify results. … When you say 'fix the failing tests,' Claude might: 1. Run the test suite to see what's failing 2. Read the error output 3. Search for the relevant source files 4. Read those files to understand the code 5. Edit the files to fix the issue 6. Run the tests again to verify."
- Tier: **Verified** (read).

**F3.2 — Without a runnable check, the human becomes the verification loop [P8 TDD].**
- Claim: The single highest-leverage practice is giving the agent a check it can run (tests/build/linter/screenshot); without one, "looks done" is the only signal and the human is the loop.
- Source: https://code.claude.com/docs/en/best-practices (Claude Code official docs)
- Quote: "Give Claude a way to verify its work. Give Claude a check it can run: tests, a build, a screenshot to compare. It's the difference between a session you watch and one you walk away from. … Claude stops when the work looks done. Without a check it can run, 'looks done' is the only signal available, and you become the verification loop: every mistake waits for you to notice it. Give Claude something that produces a pass or fail, and the loop closes on its own."
- Tier: **Verified** (read).

**F3.3 — The check must be headless / runnable without human setup, or the agent "goes blind" [P8 TDD].**
- Claim: TDD's F.I.R.S.T properties still apply, with an agent-specific addendum: the test command must be discoverable (README/CLAUDE.md/Makefile/package.json), output must be parseable, and it must not depend on manual DB seeding or out-of-repo secrets.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "the test has to be executable by the agent without human setup. Meaning: the command to run the test is in the README or CLAUDE.md, in the Makefile, in the package.json. Output has a predictable format the agent parses. It doesn't depend on manually seeding the database, on a config file that isn't in the repo, on a secret credential. The agent writes code, runs tests, reads output, adjusts, runs again. That cycle is the foundation. If the tests don't run headless, the agent goes blind."
- Tier: **Verified** (read).

**F3.4 — TDD becomes a "technical obligation, not a philosophy"; field data on the virtuous loop [P8 TDD, P9 refactoring].**
- Claim: In a real 274-commit/8-day agent project, CI caught 50+ real bugs the agent would have shipped; tests are what turn the agent from a guesser into a multiplier.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog, field report)
- Quote: "274 commits in 8 days, 4 integrated applications, 1,323 automated tests by the end. … CI caught real bugs more than 50 times, bugs that would have gone straight to production if I had blindly trusted the agent. Without tests, the agent hands you plausible code that silently breaks something that worked yesterday. … TDD became a technical obligation, not a philosophy."
- Tier: **Plausible** (self-reported field data, not independently audited).

**F3.5 — AGENTS.md: the agent will auto-run listed test commands and fix failures before finishing [P8 TDD, P10].**
- Claim: The open AGENTS.md standard documents that if you list test commands, the agent executes them and iterates to green — the verification loop is now an expected, documented behavior of conforming agents.
- Source: https://agents.md/ (AGENTS.md open standard, stewarded by Agentic AI Foundation / Linux Foundation)
- Quote: "Will the agent run testing commands found in AGENTS.md automatically? Yes—if you list them. The agent will attempt to execute relevant programmatic checks and fix failures before finishing the task."
- Tier: **Verified** (read).

**F3.6 — SWE-agent's ACI is built to let the agent "execute tests and other programs" as a core capability [P8 TDD].**
- Claim: The research agent interface explicitly enhances the agent's ability to "execute tests and other programs" — the write→run→verify loop is a designed-in capability, not an afterthought.
- Source: https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf (SWE-agent, NeurIPS 2024)
- Quote: "SWE-agent's custom agent-computer interface (ACI) significantly enhances an agent's ability to create and edit code files, navigate entire repositories, and execute tests and other programs."
- Tier: **Verified** (read).

**F3.7 — SWE-bench operationalizes "agent writes → tests verify" as the scoring mechanism [P8 TDD, cross-cutting].**
- Claim: The canonical benchmark scores an agent by whether its patch makes the repo's (hidden) tests pass — the entire evaluation paradigm IS the write→tests-verify loop.
- Source: https://www.swebench.com/verified.html (SWE-bench Verified, official)
- Quote: "A human-validated subset of 500 SWE-bench instances for reliable evaluation of coding agents and language models."
- Tier: **Verified** (read; the pass@1/test-pass scoring model is the benchmark's defining property).

**F3.8 — A fresh-context "second opinion" so the implementer isn't grading its own work [P8 TDD, P10 review].**
- Claim: A verification subagent with a fresh context (seeing only the diff + criteria, not the reasoning) refutes the result — the agent doing the work is not the one grading it.
- Source: https://code.claude.com/docs/en/best-practices (Claude Code official docs)
- Quote: "a verification subagent or a dynamic workflow that checks its own findings has a fresh model try to refute the result, so the agent doing the work isn't the one grading it. … context sees only the diff and the criteria you give it, not the reasoning that produced the change, so it evaluates the result on its own terms."
- Tier: **Verified** (read).

**F3.9 — Deterministic gates (Stop hooks) can block the turn from ending until the check passes [P8 TDD].**
- Claim: The verification loop can be hardened from "ask the agent to run tests" to a deterministic gate that blocks completion until the check passes — the strongest form of the write→verify paradigm.
- Source: https://code.claude.com/docs/en/best-practices (Claude Code official docs)
- Quote: "As a deterministic gate: a Stop hook runs your check as a script and blocks the turn from ending until it passes."
- Tier: **Verified** (read).

---

## 4. Mechanism 4 — Encoding principles as explicit rules (CLAUDE.md / AGENTS.md / .cursor/rules / copilot-instructions.md)

**F4.1 — Rules files exist because LLMs have no persistent memory between completions [cross-cutting, P10].**
- Claim: The reason for CLAUDE.md/AGENTS.md/rules is architectural: the model does not retain memory across completions, so persistent context must be re-injected at the prompt level every time.
- Source: https://cursor.com/docs/rules (Cursor official docs)
- Quote: "Large language models don't retain memory between completions. Rules provide persistent, reusable context at the prompt level. When applied, rule contents are included at the start of the model context. This gives the AI consistent guidance for generating code, interpreting edits, or helping with workflows."
- Tier: **Verified** (read).

**F4.2 — CLAUDE.md is read at the start of every conversation; keep it short or it gets ignored [P10, cross-cutting].**
- Claim: CLAUDE.md is loaded every session; the discipline is to prune ruthlessly because a bloated file causes the agent to ignore the rules that matter.
- Source: https://code.claude.com/docs/en/best-practices (Claude Code official docs)
- Quote: "CLAUDE.md is a special file that Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules. … For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"
- Tier: **Verified** (read).

**F4.3 — "Write clean code" is MOOT as an explicit rule — the agent already knows it [P10, cross-cutting] (INVERTED).**
- Claim: The official guidance explicitly lists "Self-evident practices like 'write clean code'" as something to EXCLUDE from CLAUDE.md — the meta-principle "write clean code" is redundant because the model is already trained on it; only project-specific deviations belong in the rules file.
- Source: https://code.claude.com/docs/en/best-practices (Claude Code official docs, INCLUDE/EXCLUDE table)
- Quote: "❌ Exclude: … Standard language conventions Claude already knows … Self-evident practices like 'write clean code'."
- Tier: **Verified** (read).

**F4.4 — AGENTS.md is the cross-agent open standard; one file works across 30+ agents [P10, cross-cutting].**
- Claim: AGENTS.md is a vendor-neutral, Linux-Foundation-stewarded format (Codex, Jules, Factory, Aider, goose, opencode, Zed, Warp, VS Code, Devin, Cursor, Copilot, …) that deliberately complements the human README with agent-specific build/test/convention context.
- Source: https://agents.md/ (AGENTS.md open standard)
- Quote: "README.md files are for humans: quick starts, project descriptions, and contribution guidelines. AGENTS.md complements this by containing the extra, sometimes detailed context coding agents need: build steps, tests, and conventions that might clutter a README or aren't relevant to human contributors. … AGENTS.md is now stewarded by the Agentic AI Foundation under the Linux Foundation."
- Tier: **Verified** (read).

**F4.5 — The README/AGENTS.md split is an INVERSION of "code is read by humans" [P10] (INVERTED).**
- Claim: The clean-code axiom "code is written to be read (by humans)" is being extended to a two-audience model: humans read the README, agents read AGENTS.md — the reader of the codebase is now explicitly non-human and gets its own instruction surface.
- Source: https://agents.md/ (AGENTS.md open standard) + https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote (agents.md): "Keep READMEs concise and focused on human contributors. Provide precise, agent-focused guidance that complements existing README and docs." / (akitaonrails): "In 2008, that audience [of Clean Code] changed. … The audience isn't human anymore. … It's for the agent that'll read, edit, and extend it. And an agent is not human."
- Tier: **Verified** (read).

**F4.6 — Nested AGENTS.md: closest-to-edited-file wins; chat prompt overrides all [P10, cross-cutting].**
- Claim: In monorepos, nested AGENTS.md files are combined with the nearest one taking precedence (OpenAI's main repo has 88), and explicit user chat prompts override everything — a context-scoping mechanism that mirrors "scope the instruction to where it applies."
- Source: https://agents.md/ (AGENTS.md open standard)
- Quote: "Large monorepo? Use nested AGENTS.md files for subprojects. Place another AGENTS.md inside each package. Agents automatically read the nearest file in the directory tree, so the closest one takes precedence and every subproject can ship tailored instructions. For example, at time of writing the main OpenAI repo has 88 AGENTS.md files." / "The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything."
- Tier: **Verified** (read).

**F4.7 — Cursor rules: .mdc files with frontmatter (description/globs/alwaysApply), scoped by path or relevance [P10, cross-cutting].**
- Claim: Cursor's project rules are version-controlled .mdc files whose frontmatter decides when they load (path globs, manual, or relevance-based) — a concrete "progressive disclosure" mechanism where rules are injected only when relevant, not all at once.
- Source: https://cursor.com/docs/rules (Cursor official docs)
- Quote: "Project rules live in .cursor/rules as .mdc files and are version-controlled. They are scoped using path patterns, invoked manually, or included based on relevance. … Each rule is a markdown file with frontmatter metadata and content. Control how rules are applied from the type dropdown which changes properties description, globs, alwaysApply."
- Tier: **Verified** (read).

**F4.8 — Rules can @-reference files that are read on demand, not inlined (progressive disclosure) [P10, cross-cutting].**
- Claim: A rule can point at a file by path; the agent reads it with its tools only when the rule applies and it needs the content — keeping the always-on context small and pulling detail in on demand.
- Source: https://cursor.com/docs/rules (Cursor official docs)
- Quote: "Mention a file by path, for example @service-template.ts, and Agent reads it with its tools when the rule applies and it needs the content. The file is not inlined into the prompt, so if something must always be in context, paste it into the rule body."
- Tier: **Verified** (read).

**F4.9 — Skills = on-demand context to avoid bloating every conversation [P10, cross-cutting].**
- Claim: Claude Code steers "sometimes-relevant" knowledge into skills that load on demand "without bloating every conversation" — the same progressive-disclosure pattern as Cursor's relevance-scoped rules.
- Source: https://code.claude.com/docs/en/best-practices (Claude Code official docs)
- Quote: "For domain knowledge or workflows that are only relevant sometimes, use skills instead. Claude loads them on demand without bloating every conversation."
- Tier: **Verified** (read).

**F4.10 — The rules file must be short/imperative because every line burns tokens every iteration [P10, cross-cutting].**
- Claim: Because the rules file is re-read on every iteration, its format must be dense and imperative — a new writing skill, and a direct token-cost constraint on how many principles you can encode.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Where to write: CLAUDE.md, AGENTS.md, .cursor/rules, .github/copilot-instructions.md, depending on the CLI. Format: short, imperative, action-oriented. The agent reads these files on every iteration (Claude Code re-reads CLAUDE.md on every query), so each line burns context tokens — density matters."
- Tier: **Verified** (read).

**F4.11 — Some principles the agent does by default; others only when explicitly encoded [P6 SOLID, P3 DRY, P1 naming] (KEY).**
- Claim: The agent will attempt SRP/small-functions/tests on its own, but DI, strict DRY, explicit types everywhere, and aggressively unique names only happen when written as rules — and "don't strip the comments you wrote on a refactor" is so counter to its default training that without the instruction it WILL prune them.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Some items (SRP, small functions, tests) the agent will try to do on its own. Others (DI, strict DRY, explicit types EVERYWHERE, aggressively unique names) it only does when you say so explicitly. And some (like 'don't strip the comments you wrote yourself on a refactor') are so counterintuitive to its default training that without the instruction it WILL prune them."
- Tier: **Plausible** (practitioner generalization from experience; not a controlled measurement).

**F4.12 — A concrete CLAUDE.md template encodes the 10 principles as agent rules [P1–P10, cross-cutting].**
- Claim: A working rules file encodes the canonical principles in agent-consumable form: functions 4–20 lines, files <500 lines, SRP, unique names returning <5 grep hits, explicit types, no duplication, early returns (max 2 indent), exception messages with the offending value, keep own comments (WHY not WHAT), single-command F.I.R.S.T. tests, DI via constructor, follow framework convention, default formatter, structured JSON logging.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog, template)
- Quote: "Functions: 4-20 lines. Split if longer. Files: under 500 lines. … One thing per function, one responsibility per module (SRP). Names: specific and unique. Avoid data, handler, Manager. Prefer names that return <5 grep hits in the codebase. Types: explicit. … No code duplication. … Early returns over nested ifs. Max 2 levels of indentation. Exception messages must include the offending value and expected shape. … Tests must be F.I.R.S.T: fast, independent, repeatable, self-validating, timely."
- Tier: **Verified** (read; it is a proposed template, not a measured best config).

---

## 5. AMPLIFIED by the agent paradigm (weight increased)

**F5.1 — Small functions / small files [P2] — AMPLIFIED to a technical obligation.**
- Claim: "Small function" shifts from a human-readability preference to a hard constraint: a small unit fits in one tool call / one read without truncation, so the agent reasons about it with full attention.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "For an agent, that recommendation became a technical obligation. A small function fits in a single tool call without truncation. A short file (keep it under 500 lines, ideally 200-300) fits in a single read. If the agent can grab the whole unit of meaning in one call, it reasons about it with full attention. If it has to paginate, it builds a fragmented mental model."
- Tier: **Verified** (read).

**F5.2 — SRP [P2/P6] — AMPLIFIED (isolation = less context to load).**
- Claim: Single Responsibility matters more because the agent can isolate one unit to understand without loading the rest of the system; an 800-line class doing three things is worse than three 250-line classes even at equal total size.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "The agent can isolate the unit to understand without loading the rest of the system … An 800-line class that does three things is worse for the agent than three 250-line classes, even if the total is the same."
- Tier: **Verified** (read).

**F5.3 — DRY [P3] — AMPLIFIED (duplication breaks the agent's edit consistency).**
- Claim: Duplication is worse for an agent than a human because, when changing replicated logic, the agent can update one copy and miss the others — the attention window has no "there are two more copies" gravity, and subtle variation between copies yields inconsistent results.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "For an agent, duplication is worse than a human for one specific reason: when the agent has to change something that's replicated, it can update one copy and forget the others. The attention window doesn't have natural gravity pulling 'oh, there are two more copies of this in other files'. … Factoring into a reusable function or module isn't aesthetic. It's automated-refactor safety."
- Tier: **Verified** (read).

**F5.4 — SOLID [P6] — AMPLIFIED (each principle saves context window; agent is better at writing new code than changing existing).**
- Claim: From LLM first-principles, each SOLID principle reduces context-window usage: SRP (fewer things to track), OCP (agent writes new code to plug in rather than editing existing), LSP/ISP (less coupling = less context + fewer regressions to test), DIP (abstractions are more concise than concretions).
- Source: https://ivan-rubinson.medium.com/clean-code-is-crucial-in-the-llm-age-392569be8a90 (practitioner blog, first-principles)
- Quote: "Open-closed principle lets LLMs shine, since it minimizes how much existing code needs to change, instead letting it mostly write new code to plug in. … Dependency Inversion — Abstractions are much more concise than concretions, so they use less space in context-windows. … Interface Segregation — The more details code touches, the more context-window it uses. It also minimizes the impact of changes, reducing regression testing time and cost, which is especially noticeable in agentic workflows."
- Tier: **Plausible** (first-principles argument, not a measured A/B).

**F5.5 — Naming [P1] — AMPLIFIED, with the emphasis INVERTED toward "searchable/unique."**
- Claim: Good names work for both humans and machines, but for the agent the dominant property is searchability/uniqueness: a distinctive name returns few grep hits and the agent goes straight to the right place.
- Source: https://ivan-rubinson.medium.com/clean-code-is-crucial-in-the-llm-age-392569be8a90 (practitioner blog) + https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote (rubinson): "other Clean Code details (like good names for functions/variables) work for both people and machines. If a good name lets me skip reading an implementation … so can an LLM (which was built exactly for that.)" / (akitaonrails): "A distinctive name (UserRegistrationValidator, InvoiceLineItemTotal, ClaudeCodeSessionTracker) returns three matches and the agent goes straight to the right one."
- Tier: **Verified** (read).

**F5.6 — Unit testing / TDD [P8] — AMPLIFIED to the central safety mechanism.**
- Claim: Tests are the agent's ground truth and its only reliable feedback; without them the agent "keeps guessing" and ships plausible-but-broken code. TDD/XP practices become "exactly the right way to work with an agent."
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Good tests with good coverage became the difference between a productive agent and an agent that keeps flailing. … XP practices (pair programming, CI, tests first, continuous refactoring, short feedback) didn't become obsolete. They became exactly the right way to work with an agent."
- Tier: **Verified** (read).

**F5.7 — Error handling with context [P7] — AMPLIFIED (exception messages are the agent's debug signal).**
- Claim: Rich exception messages (include the offending value + expected shape) matter more because the agent uses the stack trace as its primary debug signal; a vague message costs an extra reasoning round.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "raise ValueError(f'invalid input: received {repr(x)}, expected non-empty string of digits') does. The agent uses exception messages as debug signal. Vague message = agent runs an extra round to figure out what went wrong."
- Tier: **Verified** (read).

**F5.8 — DI / testability [P6-DIP] — AMPLIFIED (isolation scope for the agent's tests).**
- Claim: Injected (not hardcoded) dependencies let the agent swap a real collaborator for a named fake in a test without touching logic; internal instantiation forces fragile monkey-patch hacks that pollute the session.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Code with injected dependencies (not hardcoded) is easier to test in isolation. The agent benefits from this. It can swap the real EmailSender for a FakeEmailSender in a test without touching the logic. … DI isn't ceremony. It's isolation scope."
- Tier: **Verified** (read).

**F5.9 — Shallow nesting / single level of abstraction [P2] — AMPLIFIED (each indent level costs attention).**
- Claim: Deep nesting is more cognitively expensive for the model than for a human, measurably so, because each indentation level is more attention the model must spend tracking state; early returns/guard clauses reduce it.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Every indentation level is more attention the model has to spend tracking state. Four levels of indentation is MUCH more cognitively expensive for the agent than two levels with early return."
- Tier: **Plausible** (practitioner claim of "measurably so" without a cited measurement).

**F5.10 — Explicit types [NEW — not in the 10] — AMPLIFIED (types are an "answer key" that saves inference).**
- Claim: A new agent-era principle: explicit type annotations give the agent an immediate answer key (what goes in / comes out / valid states), whereas dynamic code forces costly, error-prone type inference.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "This isn't in 2008's Clean Code because the industry hadn't converted yet. But in 2026 it's a fundamental criterion. … Dynamic code without annotations forces the agent to infer types from usage, which costs reasoning and gets it wrong frequently. Typed code gives an immediate answer key."
- Tier: **Plausible** (practitioner claim; not in the canonical 10 — flagged as an emerging principle).

---

## 6. MOOT / de-emphasized by the agent paradigm (weight decreased)

**F6.1 — Formatting / style minutiae [P10] — MOOT (de-emphasized to "noise").**
- Claim: Tab-vs-space, 80-vs-100 columns, brace style became noise: the agent handles any *consistent* style fine, so the human should just adopt the language's default formatter and stop debating style.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Don't waste time on this. Use the default or most popular formatter for your language: cargo fmt for Rust, gofmt for Go, prettier for JS/TS, black or ruff for Python, rubocop -A for Ruby. … The agent handles any consistent style just fine … Tab vs space, 80 vs 100 columns, brace style, all of that became noise."
- Tier: **Verified** (read).

**F6.2 — "Write clean code" as a stated rule [P10 / cross-cutting] — MOOT (redundant with the model's training).**
- Claim: Stating the meta-principle "write clean code" to the agent is redundant — the official guidance lists it under what to EXCLUDE from the rules file because the model already knows standard conventions.
- Source: https://code.claude.com/docs/en/best-practices (Claude Code official docs)
- Quote: "❌ Exclude: … Standard language conventions Claude already knows … Self-evident practices like 'write clean code'."
- Tier: **Verified** (read).

**F6.3 — Human-oriented code-review ceremony [P10] — partially MOOT (replaced by fresh-context agent review).**
- Claim: The human code-review ritual is partly displaced by a fresh-context verification subagent that reviews only the diff against stated criteria — review still happens, but the actor and the input (diff, not full reasoning) change.
- Source: https://code.claude.com/docs/en/best-practices (Claude Code official docs)
- Quote: "To check the diff against your plan instead, write the review prompt yourself. Name the work to check, the plan to check it against, and what counts as a finding: … Report gaps, not style preferences."
- Tier: **Verified** (read).

---

## 7. INVERTED by the agent paradigm (polarity flipped)

**F7.1 — Comments [P10] — INVERTED: from "code smell / debt" to "first-class context / provenance."**
- Claim: The 2008 axiom "excessive comments are a code smell, well-named code needs no comments" flips: the agent reads and *likes* comments, and the valuable comment is the one carrying provenance (why this approach, which bug/issue motivated it) — information that exists nowhere else the agent can reach.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "This is where the inversion is most jarring. For Uncle Bob in 2008, the axiom was: 'good code explains itself, excessive comments are a code smell, every comment is debt that gets stale' … Now flip it. The agent reads comments. And likes them. Comments become first-class context. … What it DOESN'T know is why you chose this approach over the obvious one, what production bug motivated this weird logic, what business constraint forces this specific order … That kind of information is provenance: the why of the decision."
- Tier: **Verified** (read).

**F7.2 — Don't prune the agent's own comments [P10] — INVERTED (the human reviewer's "remove verbose comment" reflex is now wrong).**
- Claim: The inherited human reflex "verbose comment = noise, delete it" is now actively harmful: the agent wrote the comment because it judged the information worth preserving for future edits, and stripping it removes context the agent will want next time.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "don't prune the comments the agent writes. If you have the reflex 'verbose comment is noise' inherited from the original Clean Code era, that rule flipped. The agent wrote that comment because, in the act of generating the code, it decided that information was worth preserving for future edits. Removing the comment in code review strips context that the agent itself will want to read on the next interaction."
- Tier: **Verified** (read).

**F7.3 — Obvious comments [P10] — INVERTED in cost, not in kind (still bad, now for a different reason).**
- Claim: The "no obvious comments" rule survives but its *reason* flips: in 2008 obvious comments were bad because they polluted visual space; in 2026 they are bad because they cost real money in tokens the agent must process.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Comments like // increment i by 1 above i++ waste the agent's tokens the same way they wasted the human's patience. … In 2008 it was bad because it polluted visual space. In 2026 it's bad because it costs real money in tokens."
- Tier: **Verified** (read).

**F7.4 — Defensive programming / error handling [P7] — INVERTED: agent defaults to the happy path and will NOT propose defenses unprompted.**
- Claim: The agent implements circuit breakers, retries, timeouts, graceful degradation "nicely — when you ask," but on its own it implements the happy path and waits, because it doesn't know your system's operational failure points; defensive code must be enumerated in the rules file.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "the agent implements circuit breaker, retry with backoff, aggressive timeout, graceful degradation, all of it nicely — when you ask. But on its own it won't propose them. The agent doesn't know what your system's operational failure points are, so it implements the happy path and waits for instruction."
- Tier: **Plausible** (practitioner generalization).

**F7.5 — The agent's default output is "average/fast," i.e. INVERTED toward monolithic/dirty unless constrained [P2, P3, P6, P10, cross-cutting].**
- Claim: No LLM produces clean code by default — told "implement feature X" it produces 80-line functions, no DI, duplicated logic, 2000-line files, "the way the model considers average"; clean structure only appears when the rules file forces it. (Corroborated independently by a second source.)
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) + https://dev.to/doogal/prompting-ai-coding-agents-to-write-clean-code-1jfn (practitioner blog)
- Quote (akitaonrails): "no LLM does any of this by default. You tell it 'implement feature X' and it'll implement it the way the model considers average. No dependency injection. 80-line functions. No tests, or tests that mock the wrong thing. Duplicated logic because it's faster. 2000-line files because 'everything's in one place'. You need to WRITE these rules." / (dev.to): "By default, an LLM treats your prompt like a one-off task. It doesn't automatically understand your project's separation of concerns, your naming conventions, or how you manage state. It just wants to get the feature working as fast as possible. If you don't explicitly ask for well-structured code, you are going to get a dense, monolithic script."
- Tier: **Plausible** (two independent practitioner reports; consistent, not a controlled measurement).

**F7.6 — Over-engineering risk from an unfettered reviewer [P4 KISS, P5 YAGNI] — INVERTED pressure (agent can over-abstract).**
- Claim: A reviewer prompted to "find gaps" will report findings even when the work is sound, and chasing every finding drives over-engineering (extra abstraction, defensive code, tests for impossible cases) — so the KISS/YAGNI discipline must be explicitly imposed on the agent's review loop.
- Source: https://code.claude.com/docs/en/best-practices (Claude Code official docs)
- Quote: "A reviewer prompted to find gaps will usually report some, even when the work is sound, because that is what it was asked to do. Chasing every finding leads to over-engineering: extra abstraction layers, defensive code, and tests for cases that can't happen. Tell the reviewer to flag only gaps that affect correctness or the stated requirements, and treat the rest as optional."
- Tier: **Verified** (read).

**F7.7 — DRY vs. duplication-as-context [P3] — a documented tension (partial inversion).**
- Claim: The lane's posed "DRY vs. duplication-as-context" tension is real but the sources resolve it toward DRY: the agent's failure mode is *missing* duplicate copies on edit (F5.3), and the repo map rewards well-referenced shared code (F2.2/F2.3). No authoritative source found that recommends *intentional* duplication to feed agent context; the consistent guidance is to factor shared logic and point the agent at it.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog) + https://aider.chat/docs/repomap.html (Aider official docs)
- Quote (akitaonrails): "No code duplication. Extract shared logic into a function/module." / (Aider): "The repo map also helps aider write new code that respects and utilizes existing libraries, modules and abstractions found elsewhere in the codebase."
- Tier: **Plausible** (synthesis; the "duplication-as-context" pro side is NOT found in the sources read — see §9).

---

## 8. Cross-cutting / new mechanisms not in the canonical 10

**F8.1 — The agent-computer interface (ACI) is itself a clean-design target [cross-cutting].**
- Claim: The research contribution is that the *interface* the agent uses (commands + feedback format) must be designed for the LM, not reused from human UIs; a well-designed ACI "helps the LM agent understand the state … manage history to avoid unnecessary context … and provide actions that models can use efficiently and reliably."
- Source: https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf (SWE-agent, NeurIPS 2024)
- Quote: "we posit that LM agents represent a new category of end users with their own needs and abilities, and would benefit from specially-built interfaces to the software they use. … A well-designed ACI should help the LM agent understand the state of the application given previous changes, manage history to avoid unnecessary context from prior observations, and provide actions that models can use efficiently and reliably."
- Tier: **Verified** (read).

**F8.2 — ACI design principles mirror clean-code values (simple, compact, concise feedback, guardrails) [cross-cutting].**
- Claim: The four ACI design principles — simple actions, compact/efficient actions, informative-but-concise feedback, and guardrails that catch errors — are the agent-architecture analogues of KISS, DRY, terse output, and error handling.
- Source: https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf (SWE-agent, NeurIPS 2024)
- Quote: "1. Actions should be simple and easy to understand for agents. … 2. Actions should be compact and efficient. … 3. Environment feedback should be informative but concise. … 4. Guardrails mitigate error propagation and hasten recovery. … Building in guardrails, such as a code syntax checker that automatically detects mistakes, can help agents recognize and quickly correct errors."
- Tier: **Verified** (read).

**F8.3 — ACI design measurably changes agent performance (clean interface = better outcomes) [cross-cutting].**
- Claim: A purpose-built ACI outperforms the default Linux shell by 10.7 percentage points on SWE-bench Lite — evidence that "clean, LM-appropriate structure" (here of the interface) has a measurable effect, paralleling the clean-code claim.
- Source: https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf (SWE-agent, NeurIPS 2024)
- Quote: "The results show that SWE-agent solves 10.7 percentage points more instances than the baseline agent, which uses only the default Linux shell. … We show that crafting LM-centric interactive components has meaningful effects on downstream task performance."
- Tier: **Verified** (read).

**F8.4 — New agent-era artifacts: meta-doc files, architecture README, structured logging, observable commands, idempotent setup [cross-cutting, P10].**
- Claim: Beyond re-ranking the book, the agent era adds new "clean" artifacts: CLAUDE.md/AGENTS.md/.cursor/rules, a high-level-architecture README, structured (JSON) logging, predictable observability commands (pnpm test / make lint / cargo check), and idempotent setup scripts the agent can run on a clean machine.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "Meta-documentation files for agents. CLAUDE.md, AGENTS.md, .cursor/rules, and so on. … README with high-level architecture. … Structured logging. JSON logs with named fields are much more useful for the agent than prose logs. … Accessible observability commands. pnpm test, make lint, cargo check, python -m mypy — the more the project exposes predictable commands the agent can invoke to validate changes, the better. … Idempotent setup scripts."
- Tier: **Verified** (read).

**F8.5 — The measurable metric that changed: token cost, tool-call latency, output quality [cross-cutting].**
- Claim: The agent paradigm converts old "opinions" (a file should have N lines) into "technical constraints" (a file with X lines makes the agent perform worse) because there is now a metric: token cost, tool-call latency, output quality.
- Source: https://akitaonrails.com/en/2026/04/20/clean-code-for-ai-agents/ (practitioner blog)
- Quote: "some things that were opinions ('a file should have N lines') became technical constraints ('a file with X lines makes the agent perform worse'). The difference is that now there's a metric: token cost, tool-call latency, output quality. … Clean code was never fashion. It became infrastructure."
- Tier: **Verified** (read).

---

## 9. Searched, found nothing (evidence of absence)

- **"Duplication-as-context" as a *recommended* practice (the pro side of the DRY tension).** Searched for sources arguing that *intentional* code duplication is beneficial because it gives the agent more in-context examples. No authoritative source found recommending it; all sources read resolve the tension toward DRY (factor + point the agent at the shared code). The "duplication helps the agent" framing appears only as a *hypothesis* in the lane brief, not as a documented practice. → The tension is real but one-sided in the literature read.
- **A peer-reviewed (non-practitioner) measurement that a specific clean-code metric (e.g., function length, cyclomatic complexity) causally improves LLM-agent pass rates.** The SWE-agent paper measures *interface* design effects, not *code-style* effects; the clean-code-for-agents claims (akitaonrails, ivan-rubinson) are practitioner/first-principles, not controlled experiments. → No controlled causal study of "clean code → agent performance" found in the sources read.
- **Aider's own documentation on *test-driven* verification loops.** Aider's docs (repomap, conventions) document context/repo-map and convention-loading, but a dedicated Aider "how it runs tests to verify" page was not located in the sources read (the test-loop mechanism is instead well-documented by Claude Code, AGENTS.md, and SWE-agent). → Aider test-loop specifics: not captured.
- **GitHub Copilot `copilot-instructions.md` first-party documentation.** The file is named in the lane brief and referenced by akitaonrails, but a first-party Copilot docs page on `copilot-instructions.md` was not extracted in this lane (it is covered indirectly via the AGENTS.md compatibility list, which includes "Coding agent from GitHub Copilot"). → Copilot-instructions specifics: not directly sourced.
- **Devin-specific clean-code guidance.** Devin appears in the AGENTS.md compatibility list but no Devin-specific documentation on how it consumes clean-code conventions was located. → Not captured.
- **Aider `.aider.conf.yml read: AGENTS.md` convention-loading behavior in depth.** The AGENTS.md FAQ confirms Aider can be configured to read AGENTS.md (`read: AGENTS.md`), but Aider's dedicated "always-load-conventions" page was not extracted. → Confirmed by reference only.

---

## 10. Source-universe checklist

| Source type | Status |
|---|---|
| Official agent docs (Claude Code, Aider, Cursor) | **Covered** — code.claude.com (best-practices + how-it-works), aider.chat/docs/repomap, cursor.com/docs/rules — all read. |
| Semi-official / open standard (config-file conventions) | **Covered** — agents.md (AGENTS.md, Linux Foundation) read; .cursor/rules frontmatter read; copilot-instructions.md referenced (not first-party extracted). |
| Code (GitHub repos/issues: SWE-agent, Aider, SWE-bench, claude-code, aider) | **Covered (paper + docs)** — SWE-agent NeurIPS 2024 paper read (the repo's canonical artifact); Aider via official docs; SWE-bench via swebench.com. Direct source-code reading was NOT needed (docs-first gate satisfied; no foreign source code used as documentation). |
| Academic / research papers | **Covered** — SWE-agent (NeurIPS 2024), SWE-Bench Pro (arXiv/Scale) read. |
| Practice (blogs by AI-field developers) | **Covered** — akitaonrails "Clean Code for AI Agents" (read whole), ivan-rubinson "Clean Code is crucial in the LLM age" (read), dev.to "Prompting AI Coding Agents to Write Clean Code" + "Skills, Not Vibes" (search-snippet level), aidailycheck "Make Your Codebase Agent-Ready" (search-snippet level). |
| Community (Reddit/forums) | **Skipped (reason)** — not a source type this lane owns (lane owns code + semi-official); Reddit is another lane's scope. |
| Upstream (the wrapped engine) | **N/A** — the "upstream" here is the LLM itself; covered via the SWE-agent paper's first-principles (context = fixed cost) rather than a separate engine. |

---

## 11. Synthesis table — principle × agent mechanism → verdict (for the collector)

| # | Principle | Dominant agent mechanism | Verdict | One-line why (source) |
|---|---|---|---|---|
| P1 | Meaningful/descriptive naming | Codebase-as-context / grep-as-navigation | **AMPLIFIED** (emphasis → "searchable/unique") | Distinctive names = few grep hits = agent's primary navigation API (akitaonrails); repo map surfaces most-referenced symbols (Aider). |
| P2 | Small functions / SRP | Context window limits (file truncation) | **AMPLIFIED** (→ technical obligation) | Small unit fits one read/tool call without truncation → full attention (akitaonrails); 800-line 3-thing class worse than three 250-line (akitaonrails). |
| P3 | DRY | Edit-consistency + repo-map retrieval | **AMPLIFIED** (tension with "duplication-as-context" resolves toward DRY) | Agent updates one copy, misses others; no "two more copies" gravity (akitaonrails); map rewards shared abstractions (Aider). |
| P4 | KISS | Review-loop over-engineering | **INVERTED pressure** (must be imposed) | Unfettered reviewer → over-abstraction/defensive code/tests-for-impossible-cases (Claude Code docs). |
| P5 | YAGNI | Review-loop over-engineering | **INVERTED pressure** (must be imposed) | Same mechanism as P4: chasing every finding builds features/tests that can't happen (Claude Code docs). |
| P6 | SOLID | Context window (coupling = context) | **AMPLIFIED** | Each principle saves context window; agent better at writing new code than editing existing (ivan-rubinson); DI = isolation scope for tests (akitaonrails). |
| P7 | Error handling | Exception messages as debug signal; happy-path default | **AMPLIFIED** (rich messages) + **INVERTED** (defensive code only when asked) | Vague message = extra reasoning round (akitaonrails); agent implements happy path, won't propose retry/breaker unprompted (akitaonrails). |
| P8 | Unit testing / TDD | "agent writes → tests verify" loop | **AMPLIFIED** (→ central safety mechanism / technical obligation) | Without a runnable check the human is the loop (Claude Code); headless tests or agent "goes blind" (akitaonrails); SWE-bench scores by test-pass. |
| P9 | Refactoring / Boy Scout | Continuous agent edits + regression net | **AMPLIFIED** (tests make refactoring safe) | "Factoring … is automated-refactor safety" (akitaonrails); CI caught 50+ bugs in 274 commits (akitaonrails field data). |
| P10 | Readability / maintainability | Two-audience (human README + agent AGENTS.md); comments; formatting | **SPLIT: INVERTED (comments=provenance context; don't prune agent comments) + MOOT (formatting minutiae; "write clean code" as a rule)** | Comments become first-class context (akitaonrails); README/AGENTS.md split (agents.md); style "became noise" (akitaonrails); "write clean code" excluded from rules (Claude Code). |
| — | Explicit types (NEW) | Type inference cost | **AMPLIFIED (new principle)** | Typed code = "answer key"; dynamic code forces error-prone inference (akitaonrails). Not in the canonical 10. |
| — | Predictable directory structure (NEW) | Path anticipation / less exploration | **AMPLIFIED (new principle)** | Framework conventions let agent predict paths (akitaonrails). Not in the canonical 10. |

**Cross-cutting headline (for the report):** the single load-bearing fact is that **the agent's context window is a fixed, scarce, metered resource and distracting context harms performance** (SWE-agent, NeurIPS 2024; Claude Code docs). Every AMPLIFIED verdict (small units, SRP, DRY, SOLID, tests, rich errors, unique names) is a way to *shrink the context the agent must hold to do one job correctly*; the MOOT verdicts (formatting minutiae, "write clean code" as a rule) are things that *don't change that context budget*; and the INVERTED verdicts (comments-as-provenance, happy-path default, over-engineering pressure) are places where the agent's *default behavior* runs opposite to the human clean-code instinct and must be corrected by explicit rules (CLAUDE.md / AGENTS.md / .cursor/rules). The rules files exist precisely because **LLMs have no persistent memory between completions** (Cursor docs) — clean code's "written to be read" principle is now read by a non-human reader that must be re-briefed every turn.
