---
name: deep-research
description: "Multi-round subagent research into an options report."
version: 0.6.0
author: Peter Fahsel, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, web-search, verification, subagents, epistemics, reddit, sources]
    related_skills: [grounded-citations, subagent-fanout, reddit-reading, decision-narrowing, hermes-project-bootstrap]
---

# Deep Research Skill

Run a research question to a *useful, tiered, options-complete* answer: not a first-look "yes/no + hedge", but "here are all feasible paths, each with mechanism, prerequisites, per-part confidence, and sources." The process rests on three disciplines: **map sources first** (think through where the answer could exist before searching), **fan out in gated rounds** (parallel subagent lanes across source types, repeated only while a mechanical gap assessment says the question is not closed), **tier** (separate verified facts from plausible inference from speculation). Hand off to `grounded-citations` for the final cited write-up; the parallel lanes follow the `subagent-fanout` pattern. When the research feeds a decision pipeline (`decision-narrowing` downstream), it is stage 1 of three stages sharing one directory — `.hermes/decision/<topic>/` — and the corpus is persisted there from the first lane file, per "Pipeline corpora" below.

The orchestrating session (this one) does the framing, the gap assessment between rounds, and the synthesis. Lanes are `delegate_task` subagents. Kanban is NOT used for research.

## When to Use
- The question has a *system* or *capability* at its core ("can X do Y?", "how does X support Y?") where the honest answer is often "not natively, but here are the feasible paths."
- A one-pass search returns a defensible-sounding "no" — that is the exact moment to go deeper: real value usually lives one level below the documented feature.
- The user asked for a fresh, thorough, web-only investigation (no memory/skills/old sessions).
- A previous run exists and the user asks to repeat it under modified constraints (newer sources only, a different model generation, a narrower scope) and to highlight the differences — see "Repeating a previous run".

## When NOT to use
- A single verifiable fact — one `web_search`/`web_extract` is enough; this process is wasted motion.
- When the user only wants the headline, not the mechanism. Confirm depth before fanning out.

## Target repo + project (existence gate — resolve BEFORE the first search)

1. `desktop_project` with `action=list` → `active_id` + all projects with their `primary_path`.
2. The active project's `primary_path` is a git checkout with a remote → that is the target: the research runs in that project context, corpus under that repo.
3. No project is open, or the active project has no repo (e.g. the default Workspace project) → the target is the **General Research** project (repo `/workspace/dev/repos/ours/general-research`): switch the chat into it first — `desktop_project` with `action=switch, name=general-research`. The switch is automatic; do not ask.
4. Verify BOTH exist for the resolved target: the repo (git checkout with a remote) and the project. If either is missing: say exactly what is missing and ABORT. Never create a repo or project as a side effect of a research request (General Research is bootstrapped via `hermes-project-bootstrap`, never by this skill).

Corpus root — always INSIDE the target repo:
- decision pipeline → `<repo>/.hermes/decision/<topic>/research/`
- standalone → `<repo>/.hermes/research/<YYYY-MM-DD>-<topic>/`

Session scratch (`$TMPDIR`) is for throwaway intermediates only. Lane files are written to the ABSOLUTE corpus-root path from the first dispatch and `git add`ed when they land (untracked = nonexistent for the next session). The finished corpus is committed directly to `main` (decision 2026-10-18; no PR/review branch).

## Step 0 — Map the source universe (think before you search)

Before the first query, enumerate every plausible location of the answer *for this specific question*. Write the list down; it is a checklist — at the end every entry is marked **covered**, **skipped (reason)**, or **searched, no results** (a documented absence is itself a finding). A single backend or wording returns the same page cluster; different source types contain different facts.

Generic source taxonomy — for any system/capability question, consider all of:
- **Official:** vendor docs/KB, technical spec sheets, whitepapers, release notes/changelogs, migration guides, official forums/community.
- **Semi-official:** vendor API/CLI references, Terraform/provider/SDK docs (often expose settings GUI docs omit), developer/beta programs.
- **Community:** Reddit (the vendor subreddit *and* the broader-tech subreddits), Stack Exchange, Experts-Exchange, Discourse/forums of related projects, X/Facebook threads. Use the `reddit-reading` skill for the Reddit lane.
- **Code:** GitHub issues/PRs of the vendor's own projects and of wrapper/automation tools around the vendor's products; issues of the open-source engine the product is built on (it often surfaces capability/limitation reports the vendor docs never mention).
- **Practice:** blog posts, homelab write-ups, "how I did X" posts, conference talk articles, video transcripts.
- **Upstream:** the generic technology the product wraps — its docs describe what the underlying engine can do; the gap between upstream capability and product exposure is often the answer itself.

Docs-first gate (standing rule): for technical questions, official docs / issues / KB come first; foreign source code is only a last-resort fallback, never used as documentation — tier sequence and the gate wording in `before-reading-source`.

## Step 1 — Frame the question

- Split into sub-questions; each should map to one lane and/or one option in the final matrix. Write them as the first column of the **coverage table** (Step 2b) in `<corpus-root>/README.md` before dispatching — every sub-question gets a row, and the rows drive every later round decision.
- If a concrete device/model/version was given, identify it FIRST (CPU, arch, feature flags, prerequisites) — a cheap spec lookup anchors the "prereqs satisfied / not satisfied" logic and stops conclusions resting on an assumed hardware base. For research on the user's own system/fleet, the spec lookup is LOCAL and authoritative: the decision topic directory (DECISIONS.md, plans/, research/, env-*.md) and the repo's AGENTS.md — read them before the first web query. They also supply the environment context block for the lane briefs (Step 2). Where local sources disagree, the newer measured value wins; flag the stale source in the report and file an env-update in the topic corpus in the same session.
- If the question is a **procedure / operational workflow** ("how do I build & start X", "how do I set this up"), decompose it beyond the mechanism into three axes and give each its own lane/section: (a) **actor attribution** — which component performs each step (who starts it, who drives it, who reboots it); (b) **addressing / identification** — how the controlling component finds/addresses its target (explicit address vs discovery, and where that resolution happens); (c) **trigger / initiation** — what kicks the flow off and where the operator acts. Naming only the tool/mechanism ("use X") without these three is the most common way a procedural report ships operationally hollow and gets re-asked.
- Name the **dichotomy**: for "can X do Y", find the axis that produces confusion (X as *server* vs X as *client*; GUI option vs underlying-engine capability; supported list vs unsupported list). One unnamed axis produces a confident report about the wrong thing.

### Premise check (before round 1)

Before writing any lane brief, verify the subject noun(s) with ONE cheap in-session lookup (web_search / README / spec page): does the exact tool, product, model, option the user named exist under that name and version? Record the result in `README.md` under `## Premise`: subject · verified as · source. If it cannot be verified, ask the user BEFORE fanning out — one question now beats five lanes about a phantom.

## Step 2 — Fan out (search + collect)

`delegate_task` (see `subagent-fanout`) with parallel lanes. Lane granularity: **source type × sub-question** — e.g. "official docs + whitepapers for facet b", "Reddit + forums for facet c", "GitHub issues for the workaround space".

### Fan-out rounds (iterative, gated)

A research run consists of one or more fan-out ROUNDS. Each round = up to **5 lanes in parallel** (never more at once unless the user says so). Lanes of round N+1 are NOT a repeat of round N: they are narrowed briefs seeded with round N's Verified facts that re-ask ONLY what the gap assessment (Step 2b) marked OPEN.

Round gate — who decides whether another round runs:
- **Round 1:** always.
- **Round 2:** the orchestrator decides autonomously from the Step 2b table. No user question. Bounded as follows:
  1. **Lane count follows the OPEN rows, not the cap.** Dispatch exactly as many lanes as the table has OPEN rows (max 5). Never pad round 2 to 5 lanes "while we're at it".
  2. **Each round-2 brief names the gap it closes.** The brief's first line is the OPEN row it targets, verbatim from the table, plus the Verified facts from round 1 it may build on and must NOT re-search. A lane without a named OPEN row is not dispatched.
  3. **Pre-dispatch log.** Before dispatching, write to `README.md` under `## Round 2 dispatch`: the OPEN rows → lane mapping and one sentence per lane on what evidence it expects to find and where. This is the same text a round-3+ gate question would present — written now so the user can audit afterwards why round 2 ran.
- **Round 3 and every round after it:** the orchestrator MUST ask the user before dispatching — see "Round-3+ gate question" below. The user may approve any number of further rounds; each approval covers ONE round — ask again before the next. Rules 1–3 of round 2 apply to every later round as well.
- A concrete user instruction always wins (explicit lane count, "go deeper", "stop here").
- Within the autonomous rounds, in doubt thoroughness beats resources.
- The round counter resets to 1 after a PREMISE-ERROR restart (Step 2b) — the counter measures insight gained, not lanes spent.

### Round-3+ gate question (fixed shape)

Ask via `clarify`, single-select, with exactly these choices (recommended option FIRST, with one sentence why):
1. **Synthesize now, list the OPEN rows as known gaps in REPORT.md** — recommended when the pre-dispatch log cannot name a concrete source where the missing evidence should be.
2. **Run round <N>** — recommended when it can. Present the OPEN rows → lane mapping and the expected evidence per lane (from the pre-dispatch log).
3. **Stop, deliver what exists without synthesis** — lane files + README only.

The question body must contain, in this order: the OPEN rows (verbatim from the table) · per-row expected gain + source · the lane list for round N · the recommendation.

**Free-text answer is a first-class option** (user requirement 2026-10-18): `clarify` appends an "Other" free-text row automatically — treat whatever the user types there as the binding instruction (e.g. "round 4 only with a lane for row 2", "add a lane on source type X", "two more rounds without asking"). Narrow the dispatch to exactly what was typed; if the free text is ambiguous, ask once more rather than interpret.

If option 1 is chosen: `REPORT.md` gets a `## Known gaps` section — one entry per OPEN row with its best tier reached and why a further round was not run. That section is part of the deliverable, never dropped.

### Lane briefs

Each lane brief must contain: the question + its sub-question, the source types it owns, the docs-first gate, the output contract, and the instruction to search for **the feature AND its workarounds** — pair the technology with alternative-vocabulary terms (chainload, fallback, netboot, alternative protocol, manual firmware interrupt, config-file hack); workaround names rarely match feature names. If the documented answer is "no", the workaround lane is where the usable answer lives. For research on the user's own system, the brief also carries a **verified environment context block** (hosts, versions, current state, standing constraints, budget rules) built in Step 1 — repeated VERBATIM in every brief: subagents have no conversation context, and on-target findings ("does X fit our 4–6 GB VMs?", "which of our nodes is off-site?") are impossible without it. Language line in every brief: lane files in English (AI-facing text).

Per-lane output contract (one entry per finding):
- claim (one sentence)
- source URL + source type
- supporting quote or excerpt (verbatim)
- confidence tier: **Verified** (authoritative source for this exact target) / **Plausible** (sound general behavior, not demonstrated on-target) / **Speculative** (mechanism asserted with false precision, untested)
- plus a "searched, found nothing" list (queries + source types) — evidence of absence
- plus, as the LAST line of the lane file: `Sub-question status from this lane's view: answered | partial | not found` — the orchestrator uses the independent lane verdicts in Step 2b, not only its own reading.

Cap lane output per `subagent-fanout`; deep sources stay in the lane, not in this context.

Make the cap *mechanical*, not just verbal — otherwise the full detail either floods the parent or gets lost. Give every lane a **fixed on-disk output file** — `<corpus-root>/<axis-dir>/lane<N>.md` (round 2+: `lane<N>-r<round>.md`) — and a two-part output contract in the brief: (a) **write the complete findings** to that file — every finding with its claim, source URL + type, verbatim quote, tier, the searched-found-nothing list and the status line; (b) **return only a compact numbered index** (one line per key finding: `N. <finding> — <tier>`), which stays under the `subagent-fanout` ~1300-char truncation cap and can never lose the tail. Instruct the lane to write the index in ONE pass — no character counting or iterative shortening (mechanical counting is a known repetition-loop trigger); if the index is too long, drop lines rather than counting. The parent then reads each lane file whole with `read_file` (that read is Step 3) before synthesizing — so the parent reasons from the full detail without it having transited the delegation result.

## Step 2b — Gap assessment (mechanical, after every round)

After reading all lane files of the round whole (Step 3 discipline), fill ONE row per sub-question from Step 1 in `<corpus-root>/README.md` under `## Round <N> assessment`:

| sub-question | best tier reached | independent sources for load-bearing claim | workaround space searched | lane verdicts (answered/partial/not found) | status |
|---|---|---|---|---|---|

Status rules (apply in order, no discretion):
- premise signal present (see below) → **PREMISE-ERROR** (restart, not next round)
- best tier < Verified → **OPEN**
- load-bearing claim has < 2 independent sources → **OPEN**
- workaround space not searched → **OPEN**
- otherwise → **CLOSED**

Also update the Step 0 source-universe checklist (covered / skipped (reason) / searched, no results).

Decision rule: any OPEN row → next round is justified (round 2 autonomous, round 3+ ask). All rows CLOSED → Step 4. No "good enough" override — a Plausible-only row stays OPEN; if the user accepts it as a known gap, that is their call at the round-3 gate, not yours. Rows that stay OPEN because a second independent source most likely does not exist (niche hardware, brand-new feature) are reported to the user as exactly that at the gate — never silently closed.

### Premise signals

Mark PREMISE-ERROR — not OPEN — when any of these appear:
- lanes disagree on what the subject IS (name, version, which component)
- ≥ 2 lanes report "does not exist / no results" for the subject itself (not for a feature)
- a lane finds the user's term is an alias/mis-transcription of something else
- the dichotomy named in Step 1 turns out to be the wrong axis (the answer hinges on a distinction nobody asked about)

PREMISE-ERROR handling: do NOT dispatch another round, do NOT patch the report. Tell the user what the premise error was and its likely origin, propose the corrected framing, and on confirmation restart as a NEW round 1 under a new corpus dir (`...-<topic>-v2`); the old corpus stays for reference. The corrected premise is an assumption about what the user meant — ask, never guess.

## Step 3 — Read sources whole, not half

`web_extract` truncates long pages and the footer points at the full saved text. Before concluding on any load-bearing page, read the omitted middle with `read_file`. A loaded-but-unread source is not a consulted source — that is how a known fact sitting in an already-loaded document gets missed. The same applies to lane files: read each one whole before filling the Step 2b table.

## Step 4 — Synthesize: the options matrix

Consolidate all lanes of all rounds into **all feasible options**, including the native "no". For each option:
- **Mechanism** — how it works (one paragraph).
- **Prerequisites** — hardware/firmware/license/configuration.
- **Key steps** — what the user actually does.
- **Confidence per part** — Verified / Plausible / Speculative.
- **Verification status** — documented / community-reported / inferred from upstream / untested.
- **Trade-offs** — automation suitability, persistence after install, fragility, unsupported status.

Rank the options and recommend one, with the rationale explicit. If the run ended with OPEN rows (gate option 1), add `## Known gaps` as described above.

## Step 5 — Present (cited)

Load `grounded-citations` and present: best result first, the full options matrix, and an explicit statement of what remains untested on the user's exact target (model + version). Never collapse tiers into a flat assertion; never present an inference as a fact.

In a multi-lane run the lane files already carry per-finding citations (URL + verbatim quote + tier) — they are the detailed citation layer. The synthesis report is the second layer: register in the ledger only the primary sources the synthesis cites directly, cite them inline, and reference the lane files by path for the rest. Do not re-register every lane URL into the ledger from memory — the lanes already own those citations, and registering from memory is exactly the failure mode the ledger exists to prevent.

Standing user preference (2026-10-09, applies to ALL report deliverables, not just research): always do **BOTH** — print the FULL report content in the chat reply AND attach the saved file via `MEDIA:`. Never save-only.

## Saving the result (corpus format)

- Lane files: `<corpus-root>/<axis-dir>/lane<N>.md` (round 2+: `lane<N>-r<round>.md`) — every finding with claim, source URL + type, verbatim quote, tier, searched-found-nothing list, status line.
- Synthesis: `<corpus-root>/REPORT.md` — options matrix, ranked recommendation, explicit untested-on-target statement, `## Known gaps` when applicable.
- Manifest: `<corpus-root>/README.md` — `## Premise`, one row per corpus file (file · axis · claim summary · tier scheme · status · C#/D# column left empty for pipeline corpora), plus the per-round assessment tables and round-2+ dispatch logs (with the quoted user approval for rounds ≥ 3).
- Language: lane files, briefs and README in English (AI-facing); `REPORT.md` stays in the language the research was produced in (standing rule 2026-10-16).
- Commit: all corpus files committed directly to `main` of the target repo in the same session, one commit per research run (`research: <topic> <date>`), then pushed.
- Delivery: copy `REPORT.md` to the session scratch dir (`/opt/data/cache/scratch`, the desktop app's managed read boundary — not `/workspace`) and deliver BOTH the full content in chat AND `MEDIA:<scratch-path>`.

## Pipeline corpora (research that feeds `decision-narrowing`)

When the user says the research is for a decision ("damit ich mich entscheiden kann", "für die Decision-Phase"), or a topic directory `.hermes/decision/<topic>/` already exists for this subject:

- **Corpus root is the topic directory:** all lane files, per-axis directories, and the manifest land in `.hermes/decision/<topic>/research/` from the **first** lane dispatch — never in session scratch. The 24 h scratch pruning is then irrelevant, and stage 2/3 agents find the exact files by path. `git add` the files when they land.
- **Manifest at synthesis:** `research/README.md` with the table from "Saving the result"; C#/D# column **left empty** (stage 2's Close step completes it). If the corpus already has a README (house conventions, see "Appending to an existing corpus"), extend it with the missing columns instead of replacing it.

## Docs-first note without fan-out (bounded, ≤250-line research file)

When a handover asks for ONE research file on a narrow, well-documented topic (tool options, API limits, manager support), skip the subagent fan-out and do it in-session with `execute_code` (`web_search` → `web_extract` → regex/grep on the saved text):
- NixOS module options: fetch the per-option MyNixOS pages (`mynixos.com/nixpkgs/option/<path>.<opt>`); the index page lists names only, the per-option page has type/default/description. They render unstable/master, so list "not diffed against the pinned release" under Open/unverified.
- Long docs pages: `web_extract` truncates; write the content to scratch and regex for the keywords (`re.finditer`) or `grep -n` the saved cache file instead of re-reading whole pages.
- JS-heavy / SPA doc hubs (vendor doc sites that return a scrape error or a `Loading…` shell to `web_extract`, not truncation): fall back to `browser_navigate`, which renders them — retry once on a transient 502, then read the full snapshot. Versioned API-reference paths (e.g. `/vX.Y/…`) often 404 after a vendor version bump; take the method/option names from search and mark the exact schema "verify against the live version" under Open/unverified.
- Prefer the vendor's own page for each limit/expiry claim (e.g. the OAuth "refresh token expiration" section) over forum posts; cite third-party samples as third-party.
- Tag claims you confirmed with a read-only public HTTP call as **[live]** and everything else by its doc URL; never claim host/cluster facts you did not read.
- Check the topic's research manifest (`research/README.md`) first and add a row/table in the existing style; commit only the research files + manifest.

## Verification (definition of done)
- Every **Verified** claim maps to a named, fetchable source that was actually read (not just seen in a search snippet).
- Every **Plausible** claim names the mechanism it rests on and why it is not yet on-target confirmed.
- The load-bearing negative/positive is cross-checked against at least one second independent source — or listed under `## Known gaps`.
- The source-universe checklist is complete: every source type marked covered / skipped (reason) / no results.
- `README.md` carries the premise record, one assessment table per round, and a dispatch log for every round ≥ 2.
- No round ≥ 3 ran without a recorded user approval (the `clarify` answer, quoted in the dispatch log).
- The corpus is committed and pushed on `main`; the report was delivered BOTH in chat and as `MEDIA:`.

## Appending to an existing corpus

When the user asks to file findings "im Format der anderen Rechercheergebnisse" / "to the other findings": this is NOT a fresh report. First `ls` for the existing research corpus (project research dir, session scratch, or wiki), read ONE existing lane/report file, and copy its exact house conventions — tier letters (A/B/C vs Verified/Plausible/Speculative), source numbering style, TL;DR placement, gaps section — into the new file, and write the new lane next to its siblings in the same directory, not in a fresh dir with the skill's default format. The corpus's house format wins over this skill's defaults; the user is checking format consistency. A corpus that lives under `$TMPDIR` (session scratch) is pruned after 24 h — persist it into the target repo (pipeline: `.hermes/decision/<topic>/research/`) and git-track it in the same session; a pruned pipeline corpus is an unreconstructable elimination history.

## Repeating a previous run (repeat + diff)

When the user asks to repeat an existing research run under modified constraints (newer sources only, a different model generation, a narrower scope) and to highlight the differences: this is a NEW run with a baseline — not an append (above) and not a fresh start.

1. **Read the baseline before the first search:** the old corpus's `REPORT.md` (synthesis + verdicts) and `ledger.json` (source list). Extract the key claims and the per-item verdicts. The old corpus's sources are the comparison baseline, never new evidence — the new run's filter applies to every new citation.
2. **New corpus root, sibling of the old one** (dated convention); never overwrite or extend the old corpus in place.
3. **The baseline goes into every lane brief** (context block, repeated verbatim): the old corpus's absolute path, a compact numbered list of the baseline's key claims, and the instruction "comparison baseline, never new evidence". The new run's hard filters (date cutoff, model generation, scope) go in the same block.
4. **Pin the filter's referent first.** If a filter references a moving target ("the latest model generation", "the current version"), one lane's job is to establish exactly what that is, with dated evidence, before the other lanes apply the filter — do not prejudge the names in the briefs.
5. **Mandate a DIFFERENCES section in REPORT.md:** per-item verdict change (old → new, with the new evidence), claim-level status for each baseline claim (CONFIRMED / CHANGED / OVERTURNED / NEW), and a "what the new constraint changed" summary.
6. **Match the previous run's deliverable format** — if the baseline delivered e.g. EN + DE reports, deliver both.

## Pitfalls
- **Stopping at a defensible "no"** — the core failure this skill exists to prevent. "No + here's an alternative feature" is a first-look answer; "not natively, but here are all feasible options, tiered" is a deep answer.
- **Round 3 dispatched without asking** — the autonomous budget is exactly two rounds; a third without `clarify` violates the gate even if "in doubt, thoroughness beats resources".
- **Round N+1 re-asks round N** — unnarrowed briefs burn lanes on known facts; seed with Verified facts and re-ask only the OPEN rows.
- **"Good enough" closing of a Plausible row** — the status rules have no discretion; a Plausible-only row is OPEN until the user accepts it as a known gap.
- **Rounds inherit a wrong premise** — more rounds cannot fix a wrong subject; premise signals mean restart with the user's confirmation, not another round and not a correction section in the report.
- **Corpus outside the target repo** — scratch is pruned after 24 h; lane files go to the absolute corpus-root path from the first dispatch and are git-added when they land.
- **Searching the feature but not the workaround** — feature queries return the documented surface; feasible paths hide under different vocabulary.
- **Trusting truncated `web_extract` output** — unread middle = missed fact.
- **Conflating two meanings of one term** (server vs client, host vs guest, supported vs possible) — one axis unnamed produces a wrong-but-confident report.
- **Inference sold as fact** — sound general behavior of an upstream engine is not proof it works on this product version; label which it is.
- **Dead candidates carried into the recommendation.** When a matrix entry carries "production readiness: verify" (single-maintainer repo, old image), resolve it with a direct liveness probe before the decision phase consumes it: GitHub API on the repo (404? archived? `pushed_at`), the container registry's last-build date + pull count, plus a scan for active alternatives. A deleted repo plus a multi-year-old final build is a hard disqualifier — record it in the lane file as a Verified finding (with the probe date). Never let an unverified tool survive into a recommendation as if alive.
- **Assuming the hardware base** — a concrete model was given, so run the spec lookup before reasoning about prerequisites.
- **One source type, one wording** — the same page cluster comes back; facts that only exist in Reddit/issue trackers/practice posts are missed.
- **Deliverable file outside the app's read boundary** — attaching `MEDIA:/workspace/...` on the Hermes desktop app fails with "Path is outside the managed read boundary". Copy the report to `/opt/data/cache/scratch` before attaching.
- **Procedural question left operationally hollow.** When the ask is a *procedure* (who does what, how is the target located, what triggers it), "which tool/mechanism" is only half the answer. Decompose into actor / addressing / trigger and make each an explicit lane or section; check the first draft against those three axes before delivering.
- **Documented ≠ complete — existing skills are a starting point, not the answer.** When the research subject is a system you already have skills or knowledge about, the existing documentation tells you what is *supposed* to work, not what *actually* works, what is *broken*, or what is *planned*. The fan-out MUST include a "GitHub issues/PRs" lane and a "source code" lane for the system in question, even when you already have a skill for it. A report that only synthesizes existing skills is a first-look answer.
- **Lane "failed" but the file is complete.** Subagents can die with a degenerate-output error (repetition loop, stream cut mid-loop) while composing the final index — AFTER the lane file has already been fully written to disk. On a lane failure, first check the on-disk file (section headers + tail); if it is complete, read it and continue — re-dispatching the whole lane wastes work that already landed. If it is incomplete, re-dispatch that lane alone, seeded with the siblings' Verified facts.
- **429s on a shared/self-hosted model endpoint.** 5 parallel lanes can trip its rate limit; briefs mandate spaced queries (1–2 `web_search` per iteration, pauses between), and a failed lane is re-dispatched alone (staggered).
