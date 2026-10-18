---
name: before-reading-source
description: "Load BEFORE opening foreign source code to understand it."
version: 2.0.0
author: Peter Fahsel, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, docs, workflow, method, docs-first]
    related_skills: [deep-research, hermes-agent, grounded-citations, release-notes-search]
---

# Before reading source

The docs-before-code gate as a checklist. Load it the moment you are about to
open a foreign source file to *understand* how or why something works — a
lookup, a bug analysis, a "is this by design?" question. A standing policy
line does not fire at the moment of action; this checklist does.

## When to Use
- You are about to `read_file` / grep a repo you do not own, to understand behavior.
- A question of the form "why does X do Y", "is Y a bug", "what does option Z really do".

## When NOT to use
- Coding/programming tasks (implement, fix, refactor): there the code IS the
  primary source. Docs-first does not apply.

## The gate

Before opening any foreign source file for understanding, state in your reply
which tiers below you already tried and what they gave you. If you cannot,
docs-first has NOT happened yet.

## The sequence (top -> bottom; stop when you have an answer)

1. **Official docs.** Hermes: `https://hermes-agent.nousresearch.com/docs/llms.txt`
   (indexes the whole doc set; find the page, read it; `llms-full.txt` = all in
   one). Config defaults with inline comments (`hermes_cli/config_defaults.py`)
   count as docs. Other tools: official docs site, then `README` / `docs/` in
   the repo (README is docs, not code).
2. **Issue tracker / changelogs / release notes** — quirks, known bugs, "is this
   a bug or by design". `gh issue list --search`, `gh pr list --search`,
   `CHANGELOG.md`, release notes (`release-notes-search`).
3. **Our own records** — the decision topic directory
   (`.hermes/decision/<topic>/research/`, DECISIONS/REVISIONS), `references/`
   of relevant skills, `session_search` for "how did we resolve this before".
4. **Source code — ONLY as the fallback,** minimal read. Say so explicitly:
   "docs say X is unspecified/contradictory, reading the code to confirm."
   Read the smallest slice (a function, not the file), cite it as `path:line`,
   then go back to docs/issues to confirm the code matches intent.

## Rules
- **Never use foreign source code as documentation.** Code shows what IS true
  now, not what was INTENDED. Code vs docs disagreement is a finding to
  surface, not a reason to treat the code as the doc.
- **"Docs gave no answer" must be real.** A search that returned nothing means
  try the next tier, not jump to code.
- **Cite your tier.** Name where each fact came from (doc page / issue # /
  record / `file:line`) so the user can audit the tier you used.
- **Regressions:** when behavior changed "since the last update", tier 2
  includes the merged PRs of that release — find the PR that touched the
  subsystem before reading its code.

## Why this exists
Repeatedly (Aug–Oct 2026) sessions reached for source before docs during an
active problem; the user had to interrupt ("DOKU vor Code. IMMER.").
