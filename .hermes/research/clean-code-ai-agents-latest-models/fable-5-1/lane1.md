# Lane 1 (Fable 5.1 supplement) — Official / vendor sources only

Run: 2026-10-18 · Sub-question SQ1: "What exactly is Claude Fable 5.1?" (parts a–g)
Scope: official Anthropic only — anthropic.com (announcement, product page, system card), platform.claude.com docs (model overview, prompting guide, API release notes). Docs-first gate honored; no foreign source code used.
Tier scheme: **Verified** = authoritative/primary source actually read · **Plausible** = sound but secondary, vendor self-interest, small n · **Speculative** = asserted, untested.
Date filter: every source below is dated on/after 2026-06-01 (the model itself is 2026-09-01; date evidence per source is given).
Ledger note: the 42 sources in `../ledger.json` are NOT re-cited as new evidence. Where a finding leans on a ledger source it is flagged "already in ledger, source n". New primary sources used here (none in the ledger): `anthropic.com/claude-fable-and-mythos-5-1`, `anthropic.com/claude/fable`, `anthropic.com/claude-fable-5-1-mythos-5-1-system-card`, `platform.claude.com/docs/en/models/fable-5-1/overview`, `platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1`, `platform.claude.com/docs/en/release-notes/api`.

---

## (a) Positioning and capabilities

**F1.** Anthropic positions Fable 5.1 as its most advanced and most capable *generally available* model, aimed at ambitious, long-running, asynchronous work.
- Source: https://www.anthropic.com/claude-fable-and-mythos-5-1 (vendor announcement page; dated 2026-09-01 via the product page and system card) + https://www.anthropic.com/claude/fable (product page FAQ, current)
- Quote: "They're the world's most advanced models for coding and knowledge work—and their research capabilities offer an early glimpse of how AI models will contribute to scientific progress." / "Claude Fable 5.1 is our most capable generally available model. It's best for ambitious, long-running, asynchronous work."
- Tier: Verified

**F2.** Mechanically, "days-long / long-horizon / asynchronous" means Fable 5.1 is built for jobs that run for hours across many applications and continue unattended: it plans, uses tools, recovers from failures, and self-reports without being prompted; for coding it spans whole codebases over multi-day autonomous sessions and writes its own tests.
- Source: https://www.anthropic.com/claude/fable (product page, "Agents" and "Coding" sections)
- Quote: "Claude Fable 5.1 is built for jobs that take hours and span many applications: working through a backlog in Cowork, picking up requests in Slack through Claude Tag (beta), operating a browser, or running unattended as a managed agent on the Claude Platform. It plans the work, uses the tools it needs, recovers when a step fails, and keeps you posted without being asked." / "features that span an entire codebase, code review, performance work, and multi-day autonomous sessions. It can write its own tests to check its work, implement designs with high fidelity, and use vision to check outputs against goals."
- Tier: Verified

**F3.** The long-horizon claim is backed by vendor-published customer anecdotes of multi-hour/multi-day unattended runs (38-hour ML run; ~3-day prototype; self-maintained records across a long stretch).
- Source: https://www.anthropic.com/claude-fable-and-mythos-5-1 (customer quotes: Ramp, MongoDB, Shopify, Jane Street)
- Quote: "One unattended 38-hour run on a machine learning problem diagnosed a prior result as a label artifact, made the correction, kicked off six parallel experiments that ran overnight, and returned with a result and next steps." (Ramp) / "It then ran for hours unattended, with strong verification loops, to implement the entire prototype. I would wake up in the morning to the next phase finished" (MongoDB) / "it keeps its own records, reprioritizes as things change, and picks up where it left off." (Shopify) / "While prior models became hard to follow the longer they worked, Fable 5.1 remains readable over long, multi-step tasks." (Jane Street)
- Tier: Plausible (vendor-published customer anecdotes, small n)

**F4.** How it differs from Opus 5.5: Anthropic's own routing guidance is to *start* with the cheaper Opus 5.5 and reach for Fable 5.1 only for demanding reasoning / long-horizon agentic work where Opus 5.5 at higher effort still falls short; Opus 5.5 is framed as performing "at the level of Claude Fable 5.1 on most work."
- Source: https://platform.claude.com/docs/en/models/fable-5-1/overview (official model docs) + Opus 5.5 page (already in ledger, source 1)
- Quote: "For most workloads, start with Claude Opus 5.5 … Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still fall short." / (ledger source 1) "It performs at the level of Claude Fable 5.1 on most work and costs 40% less to run than Opus 5."
- Tier: Verified

---

## (b) Fable vs Mythos — what the safeguard difference actually is

**F5.** Fable 5.1 and Mythos 5.1 are the same model with different safeguard levels; Fable 5.1 is generally available, Mythos 5.1 is gated to trusted access programs.
- Source: https://www.anthropic.com/claude-fable-and-mythos-5-1 (vendor announcement)
- Quote: "Claude Fable 5.1 and Claude Mythos 5.1 are the same model, but with different levels of safeguards. Fable 5.1 is generally available, while Mythos 5.1 is available only through our trusted access programs; its safeguards are specifically designed to support work in cybersecurity and the life sciences."
- Tier: Verified

**F6.** Fable 5.1 is the SAFER / more-restricted variant; Mythos 5.1 is the same model with more permissive safeguards in the high-risk domains.
- Source: https://www.anthropic.com/claude-fable-5-1-mythos-5-1-system-card (system card, Executive Summary; dated "September 1, 2026")
- Quote: "Claude Fable 5.1 is available for general use, and includes additional safeguards that prevent it from performing certain tasks in high-risk, dual-use domains such as biology and cybersecurity. Claude Mythos 5.1 is the same model with more permissive safeguards in these domains."
- Tier: Verified

**F7.** What Fable 5.1 is restricted from: it may *discover* software vulnerabilities but not *develop exploits*; flagged cyber/bio/chem queries are blocked or rerouted to less-capable Opus models (Opus 4.8 for cyber, Opus 5 for bio).
- Source: https://www.anthropic.com/claude-fable-and-mythos-5-1 (announcement) + https://www.anthropic.com/claude/fable (product page "Safeguards" + FAQ)
- Quote: "In part, this is because Fable 5.1 can now be used to discover software vulnerabilities—though not to develop exploits for them." / "Many queries in these domains are automatically routed to less capable models if flagged by these safeguards. You won't be charged Fable prices for rerouted requests." / "For most Claude applications, queries flagged by our cybersecurity safeguards automatically route to Opus 4.8 and biology safeguards route to Opus 5."
- Tier: Verified

**F8.** Who gets which variant: Fable 5.1 = GA (Pro/Max/Team/Enterprise + API). Mythos 5.1 = vetted cyberdefenders and life scientists, currently only a set of US organizations, via the Cyber Verification Program / Life Sciences Verification Program; its capabilities also power "Claude Security" for all Claude Enterprise customers.
- Source: https://www.anthropic.com/claude-fable-and-mythos-5-1 (announcement) + https://www.anthropic.com/claude-fable-5-1-mythos-5-1-system-card (system card)
- Quote: "Claude Mythos 5.1 is available to vetted cyberdefenders and life scientists. Currently, it is only available to a set of US organizations, though we're coordinating with the US government to expand access to a broader set of domestic and international partners as quickly as possible." / "Direct access to Mythos 5.1 is limited to vetted individuals and organizations through our trusted access programs. Its capabilities also power Claude Security, available to all Claude Enterprise customers."
- Tier: Verified

**F9.** The Fable/Mythos performance gap is attributed to safeguard intervention, not capability: on Terminal-Bench 4.0 Fable 5.1 scores 55.8% vs Mythos 5.1 60.9%, and Anthropic says the gap "reflects the tasks on which our earlier, less precise cyber safeguards intervened."
- Source: https://www.anthropic.com/claude-fable-and-mythos-5-1 (announcement, benchmark table + caption)
- Quote: "Claude Fable 5.1 and Claude Mythos 5.1 are the same underlying model; the gap between them reflects the tasks on which our earlier, less precise cyber safeguards intervened. With the improvements we're making to these safeguards today, we expect the difference between the models to be much smaller."
- Tier: Verified

---

## (c) Availability — API access, model ID, clouds, plans, restrictions

**F10.** Model IDs per platform: Claude API `claude-fable-5-1`; Amazon Bedrock `anthropic.claude-fable-5-1`; Google Cloud `claude-fable-5-1`; Microsoft Foundry `claude-fable-5-1`; Claude Platform on AWS `claude-fable-5-1`. (Mythos 5.1's API ID is `claude-mythos-5-1`.)
- Source: https://platform.claude.com/docs/en/models/fable-5-1/overview (official model docs, "Model IDs") + https://platform.claude.com/docs/en/release-notes/api (API changelog, Sep 1 2026 entry)
- Quote: "Claude API — claude-fable-5-1 / Amazon Bedrock — anthropic.claude-fable-5-1 / Google Cloud — claude-fable-5-1 / Microsoft Foundry — claude-fable-5-1 / Claude Platform on AWS — claude-fable-5-1" / "We've launched Claude Fable 5.1 (`claude-fable-5-1`) … alongside Claude Mythos 5.1 (`claude-mythos-5-1`) for Project Glasswing participants."
- Tier: Verified

**F11.** Clouds/platforms: Claude API, Amazon Bedrock, Claude Platform on AWS, Google Cloud, Microsoft Foundry (product page adds "through available marketplaces").
- Source: https://platform.claude.com/docs/en/models/fable-5-1/overview + https://www.anthropic.com/claude/fable
- Quote: "Claude Fable 5.1 is available on the Claude Platform natively, through available marketplaces, and in Amazon Web Services, Google Cloud, and Microsoft Foundry."
- Tier: Verified

**F12.** Consumer plans: Fable 5.1 is available to Pro, Max, Team, and Enterprise users.
- Source: https://www.anthropic.com/claude/fable (product page, "Availability and pricing")
- Quote: "For individuals and organizations taking on their hardest knowledge and coding work, Claude Fable 5.1 is available to Pro, Max, Team, and Enterprise users."
- Tier: Verified

**F13.** Specs: 1M-token context, 128K max output, adaptive (always-on) thinking, default effort `high`, knowledge/training cutoff Jun 2026, status "Active (latest)", retirement not sooner than 2026-09-01+1yr.
- Source: https://platform.claude.com/docs/en/models/fable-5-1/overview (official model docs)
- Quote: "Claude Fable 5.1 … 1M | 128K | $10 / $50 | Slower | Adaptive (always on) | `high` | Jun 2026" / "Status — Active (latest) / Released — September 1, 2026 / Retirement — Not sooner than September 1, 2027"
- Tier: Verified

**F14.** Data retention / usage restriction: 30-day retention by default for safety monitoring; eligible Enterprise customers can use Enterprise Frontier Safeguards (EFS) to store data on their own cloud with customer-side human review, and until EFS ships, eligible customers can run Fable 5.1 with zero data retention.
- Source: https://www.anthropic.com/claude/fable (product page "Data retention") + https://www.anthropic.com/claude-fable-and-mythos-5-1 (announcement)
- Quote: "Using Fable requires 30-day data retention for safety monitoring by default. Enterprise customers eligible for Enterprise Frontier Safeguards can store data on their own cloud infrastructure and any human review is by default done by the customer themselves, rather than Anthropic. Until EFS is available, eligible customers can use Fable 5.1 with zero data retention."
- Tier: Verified

**F15.** US-only inference is available at 1.1× input/output pricing.
- Source: https://www.anthropic.com/claude/fable (product page)
- Quote: "For workloads that need to run in the US, US-only inference is available at 1.1x pricing for input and output tokens."
- Tier: Verified

**F16.** Breaking API changes vs Fable 5 (relevant to agent harnesses): forced tool use (`tool_choice` `any`/`tool`) returns a 400; thinking blocks are tied to the model+conversation that produced them (replay after a prefix change → 400 or dropped); editing earlier turns invalidates thinking blocks. Additive: per-message effort (beta), turn-scoped system messages (beta), readable progress updates (`display:"updates"`, beta), lower cache-read price, content provenance.
- Source: https://platform.claude.com/docs/en/models/fable-5-1/overview + https://platform.claude.com/docs/en/release-notes/api (Sep 1 2026 entry)
- Quote: "three changes are breaking: forced tool use returns an error, only Claude Fable 5.1 and Claude Mythos 5.1 can read Claude Fable 5.1's thinking blocks, and editing earlier turns invalidates thinking blocks" / "On Claude Fable 5.1 and Claude Mythos 5.1, `tool_choice` types `any` and `tool` aren't supported and return a 400 error."
- Tier: Verified

---

## (d) Pricing vs Opus 5.5 and Opus 5

**F17.** Fable 5.1 token pricing: $10/M input, $50/M output; cache read $0.25/M (0.025× base input, vs 0.1× on other models); 5-min cache write $12.50/M; 1-hour cache write $20/M; Batch API 50% discount.
- Source: https://platform.claude.com/docs/en/models/fable-5-1/overview (official model docs, "Pricing") + https://platform.claude.com/docs/en/release-notes/api
- Quote: "Input $10 / MTok / Output $50 / MTok / 5m cache write $12.50 / MTok / 1h cache write $20 / MTok / Cache read $0.25 / MTok / Batch API 50% discount" / "Prompt cache reads on Claude Fable 5.1 and Claude Mythos 5.1 cost $0.25 USD per million tokens: 0.025x the base input price, compared with 0.1x on other models."
- Tier: Verified

**F18.** vs Fable 5: same $10/$50, but cache reads cut to $0.25/M (75% cheaper than Fable 5), which Anthropic says lowers typical-workload cost ~25% and highly-agentic workloads up to ~45%.
- Source: https://www.anthropic.com/claude-fable-and-mythos-5-1 (announcement) + https://www.anthropic.com/claude/fable (product page)
- Quote: "Fable 5.1 will cost an estimated 25% less than Fable 5 for typical workloads, wherever usage is billed by token. This is because we're reducing our pricing on cache reads … For highly agentic work, the savings will often be much larger—up to approximately 45%." / "Cache reads now cost $0.25 per million tokens, 75% less than Fable 5."
- Tier: Verified

**F19.** vs Opus 5.5 / Opus 5: Fable 5.1 is the premium-priced model at $10/$50; Opus 5.5 is $4/$20 (2.5× cheaper per token) and Opus 5 is $5/$25. Anthropic's net-cost framing is that Opus 5.5 "costs 40% less to run than Opus 5" — i.e., Opus 5.5 is the cheaper "most work" alternative to Fable 5.1, not the other way around.
- Source: https://platform.claude.com/docs/en/models/fable-5-1/overview (comparison table) + https://platform.claude.com/docs/en/release-notes/api (Opus 5.5 $4/$20, Opus 5 $5/$25) + Opus 5.5 page (already in ledger, source 1)
- Quote: "Claude Fable 5.1 … $10 / $50 … Claude Opus 5.5 … $4 / $20 … Claude Sonnet 5.5 … $2 / $10" / "at $4 / $20 USD per MTok (Claude Opus 5 is $5 / $25)" / (ledger source 1) "costs 40% less to run than Opus 5."
- Tier: Verified

---

## (e) PRIMARY release date

**F20.** The primary release date is **2026-09-01**, confirmed at four independent primary sources (this upgrades the previously Plausible secondary-source date to Verified).
- Source: https://platform.claude.com/docs/en/release-notes/api (API changelog) + https://www.anthropic.com/claude/fable (product page announcement list) + https://www.anthropic.com/claude-fable-5-1-mythos-5-1-system-card (system card) + https://platform.claude.com/docs/en/models/fable-5-1/overview (model docs)
- Quote: "### September 1, 2026 — We've launched Claude Fable 5.1 (`claude-fable-5-1`), the successor to Claude Fable 5 for long-running agentic coding, knowledge work, and research" / "Introducing Claude Fable 5.1 — Sep 1, 2026" / "September 1, 2026" (system card masthead) / "Released — September 1, 2026"
- Tier: Verified

---

## (f) Vendor-reported benchmarks for Fable 5.1

**F21.** Anthropic's Fable 5.1 announcement table (columns: Fable 5.1 | Fable 5 | Opus 5 | GPT-5.6 Sol): Terminal-Bench-Science 0.1 = 52.6% / 24.7% / 29.0% / 22.4%; Terminal-Bench 4.0 = 55.8% (60.9% Mythos 5.1) / 42.0% / 52.3% / 37.3%; GDPval-AA v2 = 1853 / 1723 / 1824 / 1711; OSWorld 2.0 = 77.9% partial (41.7% strict) / 72.9% (36.1%) / 75.4% (39.6%) / —; Humanity's Last Exam = 60.9% no-tools (65.0% with-tools) / 57.8% (63.8%) / 56.6% (63.6%) / —; AutomationBench = 31.4% / 17.1% / 26.9% / 19.6%; CursorBench 3.2.0 = 73.4% / 70.5% / 70.0% / 67.2%.
- Source: https://www.anthropic.com/claude-fable-and-mythos-5-1 (vendor announcement, benchmark table)
- Quote: "Terminal-Bench 4.0 | 55.8% 60.9% (Mythos 5.1) | 42.0% | 52.3% | 37.3%" / "Agentic scientific research Terminal-Bench-Science 0.1 | 52.6% | 24.7% | 29.0% | 22.4%" / "Agentic coding CursorBench 3.2.0 | 73.4% | 70.5% | 70.0% | 67.2%"
- Tier: Verified (vendor-reported; primary source read)
- Note: the Fable 5.1 page reports **CursorBench 3.2.0** (73.4%), not CursorBench 4.0. The CursorBench 4.0 = 51.8%, FrontierCode v1.1 = 50.3% and DeepSWE v1.1 = 70.0% figures for Fable 5.1 in the existing corpus come from the Opus 5.5 page (already in ledger, source 1) and x.ai's table — not from the Fable 5.1 page, which does not report FrontierCode or DeepSWE.

**F22.** Anthropic frames Fable 5.1 as more cost-efficient than its predecessor: "matching or exceeding Fable 5 at roughly half the cost per task on agentic coding benchmarks."
- Source: https://www.anthropic.com/claude-fable-5-1-mythos-5-1-system-card (system card, Executive Summary)
- Quote: "It is also more cost-efficient than its predecessors on many evaluations, matching or exceeding Fable 5 at roughly half the cost per task on agentic coding benchmarks."
- Tier: Verified (vendor self-report)

**F23.** Benchmark caveat: Fable 5.1 was evaluated with production safeguards enabled, and on safeguard-intervened tasks it (and Fable 5) scored zero on OSWorld 2.0 / AutomationBench, so the numbers likely understate raw capability.
- Source: https://www.anthropic.com/claude-fable-and-mythos-5-1 (announcement, table footnote)
- Quote: "Fable 5.1 was evaluated with its production safeguards enabled. On tasks where these safeguards intervened, Fable 5.1 and Fable 5 scored a zero on OSWorld 2.0, and Fable 5 scored a zero on AutomationBench. … This likely reduces the performance of Fable 5.1 and Fable 5 on these benchmarks."
- Tier: Verified

---

## (g) Fable-5.1-specific vendor prompting / usage guidance

**F24.** There IS a Fable 5.1-specific prompting guide, analogous to the Opus 5.5 / Sonnet 5.5 guides, scoped to "long-horizon and agentic work."
- Source: https://platform.claude.com/docs/en/models/fable-5-1/overview (Resources) + https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 (the guide itself)
- Quote: "Prompting Claude Fable 5.1 — Model-specific prompting guidance for long-horizon and agentic work." / "Your existing Claude Fable 5 prompts should perform well on Claude Fable 5.1 without changes, but a handful of behavioral differences are worth knowing about."
- Tier: Verified (documented existence + content)

**F25.** Effort-level guidance: start at default `high`, then sweep `low/medium/xhigh/max` on your own evals; effort is "the primary control for trading off intelligence, latency, and cost." Gains over Fable 5 are largest at higher effort; at `medium` it roughly matches Fable 5 at lower cost; at `low` it is often competitive with Opus/Sonnet on cost-per-task while scoring higher.
- Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 ("Consider all effort levels")
- Quote: "Start at the default effort level, `high`, then test the other levels (`low`, `medium`, `xhigh`, and `max`) against your own evals. Effort is the primary control for trading off intelligence, latency, and cost on Claude Fable 5.1." / "At `medium`, results roughly match Claude Fable 5 at lower cost … At `low`, Claude Fable 5.1 is often competitive with Claude Opus and Claude Sonnet models on cost per task while scoring higher."
- Tier: Verified

**F26. [P4 KISS / P5 YAGNI scope, P8 tests]** Fable 5.1 over-delivers on open-ended features (fixes nearby code, extends unmentioned behavior, commits extra test files); the vendor's stop-paragraph drops unrequested additions and committed test code "with no measurable change in task success," and sizes tests at "roughly one focused test per stated behavior."
- Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 ("Keep changes and tests to what the task asks for")
- Quote: "When asked to implement an open-ended feature, Claude Fable 5.1 delivers what's asked for and sometimes more: it may fix nearby code, extend behavior the task didn't mention, or commit more test files than the change warrants. It responds well to explicit instructions about what to leave out. With the following instruction, unrequested additions and committed test code drop substantially with no measurable change in task success." / "Commit tests only where the task asks for them or this repository already keeps tests for this kind of change, sized like the neighboring test files — roughly one focused test per stated behavior — and don't turn scratch checks into additional permanent test files."
- Tier: Verified
- Note: this is the Fable 5.1-generation analogue of the Sonnet 5.5 scope paragraph (already in ledger, source 4); it confirms the scope-expansion failure mode persists into Fable 5.1 and adds the "one focused test per stated behavior" sizing rule.

**F27. [P2 / edit-site locality]** Fable 5.1 REGRESSED vs Fable 5 on edit granularity: it is more likely to rewrite whole files for small changes, costing more output tokens and time; the vendor ships a "surgically edit" instruction to bring it back in line.
- Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 ("Prefer targeted edits over whole-file rewrites")
- Quote: "Claude Fable 5.1 is more likely than Claude Fable 5 to rewrite an entire text file rather than make a targeted edit. The resulting file is usually the same, but unless the file is short or most of it is changing, a rewrite costs more output tokens and time." / "try to surgically edit a file rather than rewrite the entire thing."
- Tier: Verified

**F28. [P10 writing / formatting]** Fable 5.1's prose is denser than Fable 5's (longer sentences, fewer paragraph breaks) with few stock phrases; and it leans the *opposite* way on chat formatting from earlier models (less bold, fewer headers/lists/quotes), so anti-formatting rules written for older models should be removed.
- Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 ("Writing density", "Formatting in chat")
- Quote: "its prose is denser than Claude Fable 5's: sentences run longer and there are fewer paragraph breaks." / "Earlier models overused bullets and bold in chat … Claude Fable 5.1 leans the other way: it uses bold less and is less likely to reach for headers, lists, or quotation marks. If your prompt contains anti-formatting language, remove it."
- Tier: Verified

**F29. [long-horizon autonomy / scope]** "Finish the whole task": Fable 5.1 can run very long tasks with little methodology guidance, but on complex asynchronous workloads it can end its turn early ("Next, I'll …" / "Shall I …?"); the vendor's two-paragraph nudge defines the user's request as the scope of the deliverable ("don't quietly narrow, widen, or swap it").
- Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 ("Finish the whole task")
- Quote: "Claude Fable 5.1 can execute very long tasks without much guidance on methodology, especially when the goal is clear. On complex asynchronous workloads, though, nudge it not to end its turn before the work is done." / "The user's request — or the plan they approved — sets the scope, and the scope is the deliverable: don't quietly narrow, widen, or swap it."
- Tier: Verified

**F30. [safeguard false positives]** Fable 5.1's classifiers produce fewer false positives than Fable 5 at launch, and vulnerability discovery in source code is permitted; three triggers remain (compile-check phrasing, lesser-known languages, base64 in tool output).
- Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 ("Reduce safeguard false positives")
- Quote: "Claude Fable 5.1's safety classifiers produce fewer false positives than Claude Fable 5's did at launch, and finding vulnerabilities in source code is permitted."
- Tier: Verified

**F31. [P10 / long-horizon context]** Fable 5.1 responds well to being told exactly what to preserve in compaction summaries, and its thinking blocks are conversation-bound (keep history append-only; editing earlier turns invalidates them).
- Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 ("Tell the model what to preserve in compaction summaries", "Keep the conversation history append-only")
- Quote: "Claude Fable 5.1 responds well to being told explicitly what its summary must retain when a long conversation is compacted." / "Claude Fable 5.1's thinking blocks are valid only in the exact conversation that produced them."
- Tier: Verified

---

## Searched, found nothing (evidence of absence)

- **No Fable 5.1 vendor guidance on naming, abstractions, SOLID, refactoring, or "clean code" as such.** The Fable 5.1 prompting guide (read in full) covers effort, progress updates, tool-call batching, append-only history, writing density, chat formatting, quoting sources, finish-the-task/scope, compaction, scope-of-tests, low-effort search, safeguard false positives, targeted edits, long-output headroom, subagent concurrency, and vision crop tools — but has NO section on naming, abstractions, SOLID, refactoring, or a "write clean code" rule. Source type: official prompting guide. (Mirrors the documented absence for the Opus 5.5 guide, G10.)
- **No FrontierCode or DeepSWE score on the Fable 5.1's own announcement page.** The Fable 5.1 page reports Terminal-Bench-Science 0.1, Terminal-Bench 4.0, GDPval-AA v2, OSWorld 2.0, Humanity's Last Exam, AutomationBench, and CursorBench 3.2.0 only. Source type: vendor announcement.
- **No single Fable 5.1-page table that includes Opus 5.5 as a column.** The Fable 5.1 announcement compares Fable 5.1 vs Fable 5 / Opus 5 / GPT-5.6 Sol; the head-to-head Fable 5.1 vs Opus 5.5 lives on the Opus 5.5 page (already in ledger, source 1). Source type: vendor announcement.
- **No separate Fable 5.1-only system card.** The system card is a combined "Claude Fable 5.1 & Claude Mythos 5.1" document. Source type: system card.
- Queries used (web_search): "Claude Fable 5.1 prompting guide platform.claude.com effort level" (→ found the guide + model overview + system-prompt page). Discovery of the announcement/product/system-card/changelog pages was by direct URL extraction from the premise facts and cross-links, not search. No alternate-name / codename / pre-release-leak search was needed: all primary sources were directly accessible and self-consistent; the only codename surfaced was "Project Glasswing" (the Mythos 5.1 access program) in the API changelog.

Sub-question status from this lane's view: answered
