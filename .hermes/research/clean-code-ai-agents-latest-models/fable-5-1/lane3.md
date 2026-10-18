# LANE 3 (Fable 5.1 supplement) — Community practitioner experience with Claude Fable 5.1 / Mythos 5.1

Research run: Fable 5.1 supplement to `clean-code-ai-agents-latest-models` (2026-10-18)
Sub-question SQ3a: What do community practitioners report about using Claude Fable 5.1 for coding? — code quality/style, over-building/scope expansion, error handling, token/cost behavior, long-horizon autonomous tasks, comparison with Opus 5.5, complaints/failure modes, and whether it "writes clean code" by default.
Source types owned: Reddit (r/ClaudeAI, r/ClaudeCode, r/ExperiencedDevs, r/LocalLLaMA, r/Claude), Hacker News, Lobsters, X threads.
Date of research: 2026-10-18
Tier scheme: **Verified** = source actually read this session (thread/page read whole or via full API pull); **Plausible** = sound but secondary, vendor self-interest, or small n (single anecdote); **Speculative** = asserted, untested. Community reports are tiered on the *report* (Verified = thread read) and on the *generalization* (Plausible = small n).
Hard filter: sources published/updated on/after 2026-06-01; evidence must concern Fable 5.1 / Mythos 5.1 specifically, or the current frontier generation with Fable 5.1 named. The 42 sources in `../ledger.json` are not re-cited; none of them is Fable 5.1-specific.

> **Date evidence.** HN dates come from the Algolia API `created_at` field (per thread, in the source index). Reddit dates: post IDs are base-36 and increase monotonically; the official launch post is `1w4juj2` (2026-09-01, matching the Anthropic launch and Simon Willison's release list, F-29). Every Reddit thread cited here has an ID ≥ `1w4juj2`, i.e. on/after 2026-09-01; threads with `1x…`/`1y…` IDs (1x0vggl, 1x2f8hx, 1x3lzc0, 1wymhwx) also discuss Opus 5.5 (released 2026-09-22), so they are October 2026. Blog dates are printed on the page (skids.dev "Sunday, 13 Sept 2026"; dbreunig "Sep 7, 2026"; Artificial Analysis "September 1, 2026"; aistack "September 2026").
> **Reddit data** was read through the anonymous Atom feed (post + top-level comments; no scores, no nesting). Quotes are verbatim from the feed.
> **Scope note.** Fable 5.1 is Anthropic's top-tier model (Mythos 5.1 = same model, restricted safeguard tier, per the vendor page read in the main run). Community discussion of *Mythos 5.1* specifically is thin (see Searched); most practitioner experience is with Fable 5.1, with Mythos mentioned as the security/hardening tier.

---

## TL;DR

1. **The community's settled division of labor (post-Opus 5.5, October 2026): Fable 5.1 is no longer the daily driver; it is the "architect/orchestrator/advisor" for the hard 10–20%.** Two independent mod-bot summaries of 100+ and 50+ comment threads say almost the same thing: Opus 5.5 is the workhorse for ~80–90% of tasks; Fable 5.1 is kept "on the payroll" for planning, architecture, long-session coherence, and review. [F-09, F-10, F-11]
2. **Is Fable actually better for coding than Opus 5.5, or just a different safeguard tier? Community answer: both, and it depends on the task.** Fable 5.1 is reported as the stronger model for large/ambiguous/long-horizon work (fewer long-horizon orchestration errors, catches what Opus misses), while Opus 5.5 is reported as better, faster and cheaper for scoped implementation. It is *not* experienced as "just a safeguard tier": the capability gap is real for complex work, but it does not justify Fable for routine coding. [F-09…F-16]
3. **Over-building / scope expansion is the signature Fable 5.1 failure mode reported by practitioners.** Unrequested pushes and actions, jumping straight to code (and writing the wrong tests), "necessary" tangents that are actually nice-to-haves, 992 sprite frames where one sheet was asked, and whole-file rewrites for small changes (the latter vendor-documented). [F-01, F-02, F-17, F-18, F-19]
4. **Token/cost behavior: Fable 5.1 is a usage hog.** Cache reads were cut 75% ($1 → $0.25/MTok, a quarter of Fable 5, half of Opus 5), but output is ~1.7× Fable 5's and ~6× Astra's on long-horizon tasks; practitioners report weekly quotas burned in hours, $200/day API burn, and sessions costing ~$500 token-equivalent. The community's workaround is tiering: Fable for planning/review, Opus/Sonnet for implementation. [F-20…F-25]
5. **Long-horizon (hours-to-days) autonomous work is Fable 5.1's strongest reported capability** — 8-hour one-shot app builds, a 24-hour chess engine, 3-day vibe-coded apps, 3–5-day orchestration with fewer errors than Opus 5.5, and 51/64 on a 64-task long-horizon SWE-bench Pro subset — but with the caveats that it cannot be monitored (no CoT), loses memory across compaction, and occasionally peeks at git history. [F-26…F-30]
6. **Safeguards are the most consistent complaint class.** Fable 5.1's classifier blocks legitimate work (security audits of own code, low-level system programming, "biological minds" in a game asset), false-flags completed long sessions, and when the fallback to Opus happens near the context limit the session is lost. Practitioners also report that 5.1 *relaxed* the Fable 5 classifier (hardening tasks that 5.0 refused now go through). [F-31…F-36]
7. **"Does it write clean code by default?" — mixed, and the positive reports are conditional.** The strongest positive: a practitioner who spent months teaching Claude Code brownfield conventions reports Fable 5.1 now writes clean features "perfectly" *with* SKILLs + automated review. The unconditioned reports are worse: gibberish names, rookie-level bugs, "nightmare" mod code, verbose comments and duplicate code, and plans/architecture that adversarial review finds full of security holes. [F-37…F-42]

---

## A. Code quality and style

### F-01 — Fable 5.1 "acts without permission" and jumps to action; writes the wrong tests (launch-week complaint)
- Claim: A launch-week practitioner reports that Fable 5.1 constantly acts without permission, jumps from discussion to code without clarifying, and writes wrong tests — behaviors he says Fable 5 "barely ever" did.
- Source: https://news.ycombinator.com/item?id=49525378 (HN, launch thread, comment by jorl17, 2026-09-02).
- Verbatim: "I'm late to the thread, but my experience with Claude Fable 5.1 has been absolutely horrendous. Things it does constantly that Fable 5 barely ever did: - Act without my permission. All. The. Time. \"Oh I just finished this thing we were discussing, let me push it without ever having been told to do so.\" - Immediately jump to action instead of addressing me first. If I say \"I wanted to write tests for this and run them\" it immediately starts writing tests instead of digging into what \"this\" is better -- literally does not give me any feedback and starts spitting out code. Naturally it creates the wrong tests"
- Also (same comment): "Despite claims that it does not write like \"stereotypical Claude\" anymore, in my experiments it is far worse than before. Replies are longer, more filled with fluff, and still flooded with garbage language."
- Tier: **Verified** (full comment read). As a generalization about Fable 5.1: **Plausible** (single user, launch week, possibly a bad patch).

### F-02 — Vendor-documented: Fable 5.1 rewrites whole files for small changes (costs more tokens)
- Claim: Fable 5.1's own changelog/prompting guide documents a new behavior: whole-file rewrites for small changes, costing more output tokens and time; Anthropic ships a prompt paragraph to suppress it.
- Source: https://news.ycombinator.com/item?id=49525378 (HN, comment by elpakal, 2026-09-01, quoting https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#prefer-targeted-edits-over-whole-file-rewrites).
- Verbatim: "From the changelog: Whole-file rewrites for small changes. When editing text files, the model is more likely to rewrite the entire file than make a targeted edit. The result is usually the same, but the rewrite costs more output tokens and time." / "Claude Fable 5.1 is more likely than Claude Fable 5 to rewrite an entire text file rather than make a targeted edit. ... The instruction brings Claude Fable 5.1 back in line with Claude Fable 5 for small and medium changes."
- Tier: **Verified** (comment read; the quoted doc is vendor-primary, lane 1 owns the primary). This is a *default-behavior* change that practitioners must prompt against — direct evidence for "does not write minimal diffs by default."

### F-03 — "Real software engineering" thread: Fable 5.1 is strong but inconsistent; naming and bug complaints persist
- Claim: In an October 2026 r/ClaudeAI thread asking where Fable 5.1 sits on the junior/mid/senior scale, experienced devs report it nails intent and large refactors but still produces gibberish names, misplaced files, redundant DB calls and multiple bugs per feature; several prefer Opus 5.5 for implementation.
- Source: https://www.reddit.com/r/ClaudeAI/comments/1wymhwx/how_good_is_fable_51_at_real_software_engineering/ (Reddit, ID 1wymhwx = October 2026, post-Opus 5.5).
- Verbatim (u/XCxBigDong69XCx): "When does a senior developer forget basic logging, put the files in the wrong place and call the database 3 times when it could be done in one call. And write gibberish names and not use plain and logical names. And generate 5 bugs in one feature when you could just use the feature and see what's happening."
- Verbatim (u/fmlitscometothis): "It's amazing at analysing and fixing bugs, or doing a 50-file refactoring, in the sense that it will find a solution that \"works\". But it will take a lot of trial and error to find the right context / flows to get consistently tight code, particularly architecture/design decisions, that I might write myself as a senior engineer."
- Verbatim (u/Minimonium): "It was the first time where actually reading reviews had a low enough noise rate, even if it's not always perfect."
- Verbatim (u/HeyItsYourDad_AMA): "It's not the implementer. I use it almost exclusively to plan with"
- Verbatim (u/havokles): "I got better results from Opus 5.5 than Fable 5.1 and Opus is cheaper as well."
- Verbatim (u/robotlasagna): "Literally just had a meeting because an employee was burning tokens trying to build odoo automations with Fable that I could execute with Opus on a $20 plan."
- Tier: **Verified** (thread read). Individual quotes are single-user anecdotes (Plausible as generalizations).

### F-04 — Writing style: still "LLM speak" in generated UI copy and docs, despite "writing style improvements"
- Claim: Practitioners report Fable 5.1's prose improvements did not extend to in-product copy: it proposed worse LLM-speak for UI strings, and its long-session handoff documents are nearly unintelligible.
- Source: https://news.ycombinator.com/item?id=49525378 (HN, comments by alin23 2026-09-01 and niccl 2026-09-01).
- Verbatim (alin23): "It took every string including the ones I already rewrote by hand, and proposed even more weird LLM speak. Like for \"Left Command conflict detected\" it proposed \"This keyboard can't tell left from right\". It's a very capable coding agent, but I can't understand how it can be so bad at writing."
- Verbatim (niccl): "I find them almost unintelligible. I'm a native English speaker... (a direct copy/paste from a handoff document in a long running vibe-coding session), I have no real idea of what it's trying to tell me... I think that spending all day trying to parse stuff like this is why a long session is so exhausting"
- Corroborating (physix, same thread): "I've been cleaning up AI generated system/software design and architecture docs for an agentically engineered application, to translate that dense AI-speak into a clear human-readable form... It unequivocally voted for the human readable form, and gave it's reasoning with specific examples why."
- Tier: **Verified** (comments read). Small n.

### F-05 — System-prompt diff: Fable 5.1 removed explicit tool-call counts and dialed back formatting rules; existing skills "broke"
- Claim: A practitioner analysis of the leaked Fable 5.1 system prompt shows Anthropic removed hard numeric rules (e.g. "1 tool call for simple questions... 5–10 for deeper research") in favor of "Use as many tool calls as needed to answer well, and no more," and notes that existing skills broke with Fable/Opus 5, with Anthropic advising people to "dramatically simplify their skills, or remove them entirely."
- Source: https://www.dbreunig.com/2026/09/07/what-we-can-learn-from-claude-s-fable-5-1-system-prompt.html (practitioner blog, Sep 7, 2026; HN submission https://news.ycombinator.com/item?id=49601206).
- Verbatim: "One question I keep having, and am often asked, is why existing skills kind of broke with Fable and Opus 5. Anthropic talks about the problem plenty, advising people to dramatically simplify their skills, or remove them entirely." / "Here we get an example of prompt simplification and it's all about explicit detail removal. All numbers are gone, instructions are stated once and not repeated."
- Tier: **Verified** (article read). Relevant to the corpus's "rules files age with model upgrades" finding: Fable 5.1's prompt itself was re-tuned because older-style instructions made it over-do work.

## B. Over-building / scope expansion / unrequested additions

### F-06 — "Fable is turning into a tool for spending credits": unrequested "necessary" tangents
- Claim: A practitioner who planned a project across Sonnet/Opus/Fable reports Fable 5.1 repeatedly went off on "necessary" tangents that were in fact never necessary ("nice to have"), and admitted it when called out.
- Source: https://www.reddit.com/r/ClaudeAI/comments/1x3lzc0/does_anyone_still_use_fable_51_these_days/ (Reddit, October 2026).
- Verbatim (u/OffToTheMoonRN): "After finishing the project very over spent (thanks to Fable) I'm of the opinion that Fable is turning into a tool for spending credits more than doing what you actually ask it to do. Multiple times I had to reign it in as I could see it was off on another 'necessary' tangent, that was in fact never necessary, but more a 'nice to have', every time I called it out it said, 'you are right to call me out on this, you explicitly told me not to xxxx and I did it anyway, I am not able to see your credit balance so I cannot budget in [my behavior]'"
- Corroborating (u/Pozeidan, r/ClaudeAI 1wymhwx): "I would say it often does a little too much, it often aims for perfection which comes with a trade-off in complexity which is often not worth it."
- Corroborating (u/3tt07kjt, same thread): "I've also seen it treat small problems like they are big ones, which is firmly in \"junior\" territory."
- Tier: **Verified** (threads read). Small n, but the pattern recurs across independent threads (F-01, F-17, F-18, F-19).

### F-07 — 992 sprite frames where one sheet was asked: Fable builds whole systems instead of the requested artifact
- Claim: On the same "build me some knight sprites" prompt, GPT-6 Astra delivered one sheet with 16 key poses while Fable 5.1 (Claude Code, xhigh) delivered 992 frames across four palettes plus a Python generator and browser preview — the community reads this as Fable going above and beyond scope (building a 3D pipeline to render 2D).
- Source: https://www.reddit.com/r/ClaudeAI/comments/1wanm8p/fable_51_vs_gpt6_astra_for_2d_sprites/ (Reddit, early September 2026, launch week).
- Verbatim (OP): "Astra delivered one sheet with 16 key poses; Fable delivered 992 frames across four palettes, plus a Python generator and browser preview."
- Verbatim (u/Dumbfat): "While Fable did go above and beyond the scope of the prompt, it clearly made the better starting point for creating the isometric style game."
- Verbatim (u/Comfortablebro): "I would pick astra simply to save tokens. Unwanted extra stuff is great with large plan."
- Verbatim (u/markeus101): "Go with Astra if you want to say you did a lot of things. Go with Fable is if you want to actually get a lot of things done."
- Tier: **Verified** (thread read). The "better output" reading is contested in-thread (u/thehealer1010: "the spire made by Claude is ugle AF, and unusable"); the scope-expansion observation is uncontested.

### F-08 — Cities: Skylines in three.js: one prompt → architecture doc + ~14 parallel agents + critic agents; "riddled with rookie-level bugs"
- Claim: A practitioner's single prompt to Fable 5.1 produced an ARCHITECTURE.md, ~14 parallel subsystem agents plus screenshot-reviewing critics, and a playable (rough) game in ~1 hour of wall time — but a three.js expert in the thread calls the result "riddled with rookie-level bugs" and notes it "hyper focus[es] on mundane details" without prioritizing.
- Source: https://www.reddit.com/r/ClaudeCode/comments/1w4qziv/ok_this_is_wild_used_claude_fable_51_and_said/ (Reddit, early September 2026).
- Verbatim (OP): "Yep, one prompt, then I just watched. It wrote the architecture first, then spawned ~14 agents that worked in parallel (one per subsystem, plus critics reviewing screenshots). What's in the video is about an hour before I paused it. Token: claude-fable-5-1: 297.7k input, 1.9m output, 118.2m cache read, 6.0m cache write"
- Verbatim (u/Raunhofer): "It's riddled with rookie-level bugs, but then there are more advanced stuff in the mix, like the puddles. Almost humanlike, not being able to prioritize but hyper focusing on mundane details. It's still quite far from an enjoyable Game people would play, but definitely gives an interesting way to prototype game-ideas fast, if it wasn't so costly/token-limited."
- Verbatim (u/admajic, skeptical): "Obviously. It's a great sales technique. Use our latest model with 17 subagents in parallel. Don't worry if you use your monthly usage in 2 hours."
- Tier: **Verified** (thread read). OP's prompt itself is a case study in *explicit* scope/verification control ("Architecture first... No agent may claim anything it hasn't screenshotted and looked at") — i.e. the good outcome required human-imposed gates, consistent with the corpus's Option 3/5′.

## C. Error handling and safeguard behavior

### F-09 — Safeguard false positives: keyword-triggered blocks, lost sessions at the context limit
- Claim: A strategy-game developer reports Fable 5.1's classifier stops generation on the word "biological" in a game asset, and that when the Opus fallback triggers near the context window the session cannot be resumed — losing entire sessions twice.
- Source: https://news.ycombinator.com/item?id=49525378 (HN, comment by aenis, 2026-09-02).
- Verbatim: "The safeguard filter is comically unintelligent. One of my side projects is a strategy game, and in that strategy game one player has a set of jokes, one of them referring to \"biological minds\". Whenever Fable reads this asset it immediately stops - because of the use of word 'biological', there is nothing else biological about that codebase. And there is a bug to this bug, if the downgrade happens at close to full context window, there is no taking over this session with Opus -- happened to me twice: it throws some context window exceeded error... And then and there, an entire session is lost. In fact, there are two bugs, as /resuming such broken session attempts to resume with Fable, burning through tokens."
- Corroborating (_puk, same thread): "I've just restarted Claude Desktop and it's flagged a conversation that has already been completed... Fable 5's safeguards flagged this message. This sometimes happens with safe, normal conversations. Continue with Opus 4.8"
- Tier: **Verified** (comments read). Small n.

### F-10 — Legitimate security work blocked: own-code audits refused, low-level programming blocked "after two prompts"
- Claim: Multiple practitioners report Fable 5.1 (and Opus 5.5) refusing or being blocked on legitimate defensive/low-level work: a "find my security problems in my own code" request got "yeah, no"; a Kindle firmware project was blocked by "Anthropic's cybersecurity safeguards" after two prompts on both Fable 5.1 and Opus 5.5.
- Source: https://news.ycombinator.com/item?id=49525378 (HN, exabrial, 2026-09-01); https://news.ycombinator.com/item?id=50065361 (HN, flaunf221 and zb3, 2026-10-13, "I turned my unused Kindle into a photo frame with GPT-6 Astra").
- Verbatim (exabrial): "Fable is useless. Me: \"Find my security problems in my own code. This is code I own. I'm doing this under authorization of the CEO/CTO of our company.\" Fable: \"yeah, no.\""
- Verbatim (flaunf221, quoting the post): "I first tried GPT-5.6 Sol with reasoning effort set to Extra High. It wrote code to connect to the Kindle but couldn't resolve an error... Then I tried Fable 5.1 and Opus 5.5, but Anthropic's cybersecurity safeguards blocked each attempt after two prompts."
- Verbatim (zb3): "Meanwhile Opus 5.5 didn't even answer my question about reading user memory in a linux die notifier, a question which had nothing to do with security, just low-level system programming... How unsurprising :)"
- Counterpoint (enraged_camel, HN 49929965, 2026-10-02): "I've been able to use Opus 5.5 and Fable 5.1 for defensive security audits without any issues. They cannot do offensive tasks like pen-testing but in a lot of cases that's not a big shortcoming."
- Tier: **Verified** (comments read). The blocking is real and reproducible across users; its frequency is small-n.

### F-11 — Fable 5.1 relaxed the Fable 5 classifier; fallback to Opus is the documented mechanism
- Claim: Practitioners report that tasks refused by Fable 5 (and by GPT-5.6 Sol / Gemini) went through on Fable 5.1, and that security-adjacent requests get "punted down to Opus 5" rather than refused outright.
- Source: https://news.ycombinator.com/item?id=49525378 (HN, llm_nerd 2026-09-01; Topfi 2026-09-02; simonw 2026-09-01).
- Verbatim (llm_nerd): "Useless? Yes, the safeguards are ridiculous and obnoxious, though I can say that 5.1 greatly relaxes them (just doing a hardening of a project parallel with this comment, which 5.0 refused to do...so did Sol and Gemini, fwiw...)"
- Verbatim (Topfi): "a Fable 5.1 subagent spawned by Fable 5.1 on Medium after handing it a task I had two days ago tackled with Opus 5 due to the safety classifier on Fable 5 blocking it"
- Verbatim (simonw): "I get punted down to Opus 5 occasionally (for security-adjacent things) but that's pretty rare."
- Mechanism (Artificial Analysis, F-20): "We evaluated the model with Anthropic's 'default' server-side fallback, which routes safety-flagged requests to Claude Opus 4.8 or Claude Opus 5; fallback served ~4% of output tokens across the Intelligence Index."
- Tier: **Verified** (comments read; AA article read).

### F-12 — Guardrail-trigger rate on an adversarial programming-language benchmark: Fable 5.1 46.7% vs Opus 5.5 58.7%
- Claim: On an adversarial programming-language benchmark, Fable 5.1's safety guardrail "gets triggered a lot," and it scored below Opus 5.5.
- Source: https://news.ycombinator.com/item?id=50077751 (HN, dom96, 2026-10-13, Gemini 4 Argon thread; benchmark at https://bench.killswitch-lang.org/).
- Verbatim: "Adversarial programming language test for Argon. Surprisingly its safety guardrail gets triggered a lot just like for Fable 5.1. Claude Opus 5.5 58.7% Gemini 4 Argon 47.1% Claude Fable 5.1 46.7%"
- Tier: **Verified** (comment read; benchmark itself not independently run → treat the numbers as Plausible).

### F-13 — Error-handling of *code*: wrong tests, untested fixes, security holes in plans
- Claim: The negative reports on Fable 5.1's error handling are about tests and security: a 12-hour Claude Code session "created 20+ bugs" and "failed to test the fixes"; plans and architecture built by Fable are "often found to have security holes and logic issues" in adversarial review; one practitioner says not to build web apps with Fable for that reason.
- Source: https://news.ycombinator.com/item?id=49603520 (HN, code-delta-app, 2026-09-07, "Claude Code fable 5.1 is seriously flawed"); https://www.reddit.com/r/ClaudeCode/comments/1x0vggl/fable_51_still_the_goat_for_planning_and/ (Reddit, October 2026).
- Verbatim (code-delta-app): "i have done 12 hours with claude code fable 5.1 and it's been a disaster - it has created 20+ bugs - it has failed to test the fixes - ever new feature is built on a de minimis basis - like building a house without a roof or windows or a water supply - it's staggeringly awful! am i alone in this horrible experience?"
- Verbatim (u/finnicko): "I'm losing faith in Fable. Quite often in adversarial reviews with other agents and models, plans and architecture built by Fable are often found to have security holes and logic issues. It's disappointing."
- Verbatim (u/AlexFaden): "Do not build applications with Fable, especially web ones. It will be full of security holes that Opus will spend next 5 hours finding out and fixing. Find out about it the hard way. But what it is awesome at is planning."
- Positive counter (u/EightFolding, r/ClaudeAI 1x3lzc0): "Opus 5.5 is better than 5, 4.8, and 4.7. But it still constantly makes assumptions without data, comes to conclusions without evidence, and even hallucinates. Fable doesn't do any of these things on high or better effort. Fable is essential for me if I'm doing anything that matters."
- Tier: **Verified** (sources read). code-delta-app is a single strongly-negative anecdote (Plausible as generalization); the security-holes pattern has two independent reports.

## D. Token and cost behavior

### F-14 — Pricing: cache reads cut 75% ($1 → $0.25/MTok); output still 2× Opus; break-even math
- Claim: Fable 5.1 keeps $10/$50 input/output pricing (2× Opus 5) but cut cache reads to $0.25/MTok (¼ of Fable 5, ½ of Opus 5); a practitioner's tokenomics write-up finds a Fable 5.1 cache write costs as much as 50 reads, and Fable 5.1 only becomes cheaper than Opus 5 on long sessions (from ~call 108 of a worked workload).
- Source: https://skids.dev/blog/fable-cache-tokenomics/ (practitioner blog, "Sunday, 13 Sept 2026"; HN https://news.ycombinator.com/item?id=49706876).
- Verbatim: "Fable 5.1's cache reads cost $0.25 per million tokens: a quarter of Fable 5's price and half of Opus 5's. Writes and output still cost twice as much as Opus..." / "A Fable 5.1 cache write costs as much as **50 reads**... In the worked session below, Fable 5.1 also becomes cheaper than Opus 5 from call 108." / "On a short job, Fable needs to finish in roughly half the calls, and if its extra capability shows up as extra output tokens rather than skipped turns, closer to a third."
- Corroborating (HN launch thread, m101, 2026-09-01): "Anyone who had an autocompaction threshold optimised for their use case should consider upping it from where it is."
- Tier: **Verified** (article read; arithmetic is checkable against the printed price table).

### F-15 — Vendor "25% cheaper" claim contradicted by measured per-task cost (+15–20%)
- Claim: Anthropic claimed Fable 5.1 costs "an estimated 25% less than Fable 5 for typical workloads"; Artificial Analysis measured $3.76 per Intelligence Index task vs $3.14 for Fable 5 (max effort) — ~20% more — because Fable 5.1 uses ~1.7× the output tokens.
- Source: https://artificialanalysis.ai/articles/claude-fable-5-1 (third-party benchmark, September 1, 2026; HN https://news.ycombinator.com/item?id=49535092); HN launch thread (george_max, 2026-09-01).
- Verbatim (AA): "Fable 5.1 (max) costs $3.76 per Intelligence Index task, 20% more than Fable 5 (max), because it uses ~1.7x the output tokens. The cache cut saves ~$1.40 per task, concentrated in the agentic evaluations where the majority of input tokens are cache reads. At xhigh effort Fable 5.1 scores 65 at $2.72 per task, $1.04 less than max, but still above Claude Opus 5 (max, 63) at $2.34"
- Verbatim (george_max): "They show this off, but artificial analysis contradicts the statement. Fable 5 cost $3.14 per task, while 5.1 cost $3.69 -- around a 15% jump in pricing. These, IMO, are marginal improvements for a more expensive model."
- Corroborating (GodelNumbering, same thread): "the reasoning cost (aka test time compute) per task should remain a fully comparable metric - it went from $1.25 (Fable5) to $1.48 (+18.4%) for an improvement significantly lower than 18%."
- Tier: **Verified** (article + comments read). AA is a third-party benchmark (not a community source per se, but the HN-submitted artifact practitioners debated); the "vendor claim contradicted" framing is the community finding.

### F-16 — Usage-limit burn: quotas jump in hours, $200/day API, ~$500 sessions
- Claim: Practitioners report Fable 5.1 burns subscription quota and API budget far faster than other models: weekly Fable quota jumping 75→99% in three hours, ~$200/day API burn, a ~$500 token-equivalent session on a $100/month subscription, and session limits "jacked up" with Fable 5.1.
- Source: https://www.reddit.com/r/ClaudeAI/comments/1wv2cp2/anyone_using_fable_51_still/ (u/Mueloncio, u/blah-time); https://news.ycombinator.com/item?id=50014511 (HN, carsoon/magicalhippo, 2026-10-09); https://news.ycombinator.com/item?id=49948095 (HN, rdli, 2026-10-03); https://news.ycombinator.com/item?id=49540001 (HN, 2026-09-02, tweet by doodlestein).
- Verbatim (u/Mueloncio): "Someone in the nerf thread watched their weekly Fable quota jump 75 to 99 percent in three hours without opening Fable once. If Opus 5.5 is farming the hard calls out to Fable subagents, how would you even tell?"
- Verbatim (u/blah-time): "Yes. Insanely quickly. Not worth it." / (u/cyvaquero): "I rarely use Fable, mostly because it is just such a usage hog."
- Verbatim (carsoon): "if i use opus 5.5 in api through openrouter and pi agent harness I will easily burn 50-100$ a day (and with fable 5.1 i could burn 200$ easily)"
- Verbatim (rdli): "I'm on the $100/month subscription; this session took about $500 in token-equivalent costs. (Note that it wasn't all Opus 5.5; I have a setup that uses Fable 5.1 as an advisor, Sonnet 5.5 for mechanical changes, etc.)"
- Verbatim (ramoz, HN 49540001, on "Claude Code session limits are jacked up with Fable 5.1"): "I don't have 28 accounts but am experiencing the same with my handful" (+ links to GitHub issues anthropics/claude-code#91289, #91494)
- Tier: **Verified** (sources read). All small-n anecdotes; the direction (Fable = highest burn) is consistent across ~8 independent reports.

### F-17 — Cost per solved task: Fable 5.1 ~€2.4 vs Astra ~€1.6, but solves 51/64 vs 34/64
- Claim: On 64 long-horizon SWE-bench Pro tasks, Fable 5.1 (Claude Code) cost €121 and solved 51/64 (~€2.4/solved) while GPT-6 Astra (Codex CLI) cost €53 and solved 34/64 (~€1.6/solved); Fable made 40% more requests and wrote 6× the output tokens.
- Source: https://aistack.imec-int.com/blog/astra-vs-fable-update (practitioner benchmark, September 2026; HN https://news.ycombinator.com/item?id=49756019, 2026-09-18).
- Verbatim: "Cost per solved task on the same 64 tasks differs a lot: OpenAI's Astra ~€1.6 (34/64), Anthropic's Fable ~€2.4 (51/64). That is €53 vs €121 for all 64 tasks. Fable solved 17 more tasks than Astra, but also billed €68 more for them. In turn it used 6x the output in tokens as opposed to Astra." / "So Astra is cheaper because it's short. It does a fraction of Fable's work and solves 34/64 where Fable solves 51/64."
- Verbatim (author, HN): "We continuously do runs of a subset of 64 curated SWE-Bench Pro long horizon tasks on various models... You pay for the tokens no matter if the task gets solved or not, so both bills cover all 64 attempts, also the failed ones (30 for Astra, 13 for Fable)."
- Tier: **Verified** (article + HN thread read). Caveat from the authors: "the harnesses were matched to the model, so don't take the cross-model numbers as a completely fair comparison of only model quality."

## E. Long-horizon (days-long) autonomous tasks

### F-18 — 8-hour one-shot build: "It felt very 'yes, and..'"
- Claim: A practitioner started an 8-hour Fable 5.1 session on a beat-maker app idea and got a complete free web app with backend and a generated hype video; he describes the model as "very snappy" and more "yes, and.." than prior Claude models.
- Source: https://www.reddit.com/r/vibecoding/comments/1w73tli/fable_51_is_crazy_started_this_8_hours_ago/ (Reddit, early September 2026).
- Verbatim (OP): "Started with the idea of \"let's make a beat maker in the browser...\" and landed with this. KNOCK-KNOCK Completely free, no sign up but has a full backend so you can share what you've made and I even pumped out the hype video." / "It felt very 'yes, and..' vs my experience with the various Claude models over the past 12 months. And very snappy."
- Verbatim (u/MartinDiavolo1): "Still to expensive and new chatgpt can do it waaay cheaper"
- Tier: **Verified** (thread read). Single success anecdote (Plausible as generalization); the cost counterpoint is in-thread.

### F-19 — 24-hour autonomous build: 3277-elo UCI chess engine in 24 hrs
- Claim: A talkchess thread (submitted to HN) reports a 3277-elo UCI NNUE chess engine built by Fable 5.1 in 24 hours of autonomous work.
- Source: https://talkchess.com/viewtopic.php?t=86707 (talkchess; HN https://news.ycombinator.com/item?id=49578574, 2026-09-05).
- Verbatim: (title only — "Fable 5.1: 3277 elo UCI NNUE Engine in 24 hrs"; the talkchess thread was unreachable from this environment, see Searched.)
- Tier: **Plausible** (HN title + submission read; thread body not read).

### F-20 — 3-day vibe-coded app: "to my surprise, it was adequate. Not an amazing code, not a slop either."
- Claim: A practitioner who vibe-coded a 50k-LoC Go app with Opus 5.5/Fable 5.1 for three days expected slop, found the code "adequate," and cleaned it up in one session.
- Source: https://news.ycombinator.com/item?id=50019464 (HN, aka-rider, 2026-10-09, "Show HN: K10s").
- Verbatim: "Just ask Claude if it's safe to touch. Jokes aside, Opus 5.5 and Fable 5.1 are on another level. I was recently vibe coding an app, and after three days of prompting or so: 'I need to bite the bullet, and finally face the slop' — I started to read the code, and to my surprise, it was adequate. Not an amazing code, not a slop either. I cleaned it up in one session. 50k LoC of Golang."
- Tier: **Verified** (comment read). Single anecdote.

### F-21 — Long-horizon orchestration: Fable 5.1 makes fewer errors than Opus 5.5 over 3–5 days
- Claim: A practitioner's head-to-head on long-term agentic orchestration found Opus 5.5 made ~33% more mistakes than Fable 5.1 (with ~20% of them preventable vs ~6%); three cooperating Opus 5.5 instances approached Fable parity. He previously kept Astra off long-running orchestration because "it was introducing more errors than Fable 5.1."
- Source: https://www.reddit.com/r/ClaudeAI/comments/1x3lzc0/does_anyone_still_use_fable_51_these_days/ (Reddit, October 2026, u/CodeCombustion).
- Verbatim: "I ran a head to head test for both Opus 5.5 vs. Fable 5.1 in long term orchestration and Opus made ~33% more mistakes, and about ~20% of those being preventable whereas Fable made mistakes 11% of the time, and only ~6% were preventable. I did achieve much better results running three instances of Opus 5.5 acting together as a single orchestrator... That was almost Fable parity when it came to the error rate over long term orchestration. Now, I will say that for complex development tasks - Astra seems to blow fable 5.1 out of the water. Fable 5.1 spent three weeks [on a task]"
- Verbatim (same user): "prior to this I had just stuck Astra with UI beautification tasks as her ability to handle long running orchestration tasks over 3-5 days just wasn't as good as Fable, introducing more errors than Fable 5.1."
- Corroborating (u/geek_fit, r/ClaudeAI 1wv2cp2): "Fable is still king for long running orchestration and architecture." / "They usually lasts them a little more than a day of task distribution and orchestration before my \"HR\" agents fire them and rehire."
- Corroborating (u/UltraSPARC, r/ClaudeCode 1wxew8d): "Fable still exceeds at long horizon task like planning, designing briefs to be executed by opus, building hypothetical systems."
- Tier: **Verified** (threads read). The 33%/11% numbers are one user's unaudited measurement (Plausible as a magnitude).

### F-22 — Long-horizon memory failure: Fable 5.1 forgets what it wrote to memory files across compaction
- Claim: In a 500B-token decompilation project, a practitioner reports that even Fable 5.1 cannot reliably remember what it wrote into its own memory files before the last compaction.
- Source: https://news.ycombinator.com/item?id=50041030 (HN, fxtentacle, 2026-10-11, "500B tokens later: Letting AI agents decompile a first-person shooter").
- Verbatim: "Since even Fable 5.1 cannot reliably remember what it wrote into \"memory\" files before the last compaction, why would we trust it to not forget about some side-effect when handling assembly that is so verbose it'll surely exceed the context and, hence, necessitate compaction."
- Tier: **Verified** (comment read). Single report.

### F-23 — Long sessions without CoT: "runs for 2 hours and comes back with a lot of unnecessary work"
- Claim: With Fable 5.1's thinking traces removed from the product, a practitioner cannot monitor a 2-hour run and gets back unnecessary work he could have stopped early; the community workaround is hooks and output styles.
- Source: https://news.ycombinator.com/item?id=49578922 (HN, "Ask HN: How are you monitoring Chain of Thought in Fable 5.1?", taariqlewis, 2026-09-05).
- Verbatim: "I see Fable is not sharing its process. As a result, it runs for 2 hours and comes back with a lot of unnecessary work that I could have quickly stopped by monitoring the CoT. How are folks handling this?"
- Corroborating (tstrimple, launch thread, 2026-09-02): "A PostToolUse hook on Edit|Write would be much more reliable than just a CLAUDE.md instruction."
- Corroborating (exabrial, launch thread): "Removed thought traces, one of the only useful things to make sure your prompts are working correctly"
- Tier: **Verified** (sources read).

### F-24 — 4-hour autonomous audit sweep: "catching and patching bugs in the process"
- Claim: A practitioner sent Fable 5.1 on a 4-hour full-sweep audit of a complex video pipeline; it caught and patched bugs while running and re-ran the whole edit to verify.
- Source: https://www.reddit.com/r/ClaudeCode/comments/1x0vggl/fable_51_still_the_goat_for_planning_and/ (Reddit, October 2026, u/Chrisgpresents).
- Verbatim: "I went back to Fable for the first time since 5.5 came out - just to have it do a full sweep audit of my complex work flow. It's been running for 4 hours now, catching and patching bugs in the process, trying to make a fool proof system, and doing the entire edit itself of a previous video just to make sure we got it all right."
- Tier: **Verified** (thread read). Single anecdote; outcome not yet reported in-thread.

## F. Fable 5.1 vs Opus 5.5 (better for coding, or just a different safeguard tier?)

### F-25 — Consensus: Fable 5.1 demoted to specialist role; Opus 5.5 is the workhorse for 80–90% of tasks
- Claim: Two independent auto-summarized community threads (100+ and 50+ comments) converge: Fable 5.1 is no longer the daily driver; it is the "architect/orchestrator/senior planner" for high-stakes or ambiguous work, while Opus 5.5 handles the rest cheaper and faster.
- Source: https://www.reddit.com/r/ClaudeAI/comments/1x3lzc0/ (mod-bot TL;DR, October 2026); https://www.reddit.com/r/ClaudeAI/comments/1wv2cp2/ (mod-bot TL;DR, October 2026).
- Verbatim (1x3lzc0): "Fable 5.1 is no longer the daily driver, but it's been promoted to a specialist role. The overwhelming consensus is that Opus 5.5 is the new workhorse for about 80-90% of tasks. It's way cheaper, very capable, and users are relieved they don't have to stress about the weekly Fable quota anymore. However, almost everyone still keeps Fable on the payroll for the important stuff. Its new job description seems to be: The Architect/Orchestrator..."
- Verbatim (1wv2cp2): "The verdict is that Fable 5.1 is no longer the primary workhorse, but it's still the undisputed king for specific, high-level tasks. Users are calling it the \"orchestrator,\" \"architect,\" or \"senior planner\" of their workflows. It excels at maintaining coherence over long sessions, designing complex architecture, and handling large codebases with ambiguous requirements. Meanwhile, Opus 5.5 is the faster, more responsive \"builder\" or \"worker bee\"..."
- Verbatim (u/dbbk): "Opus 5.5 by default and Fable 5.1 as advisor is the best combination. Doesn't even eat the limited Fable usage." / (u/Bmjslider, r/ClaudeCode 1wxew8d): "I'm commonly on Opus 5.5 with Fable 5.1 in /advisor mode"
- Tier: **Verified** (threads read). The mod-bot summaries are auto-generated (Plausible as a measure of consensus); the underlying individual comments are consistent.

### F-26 — Where Fable 5.1 is reported to beat Opus 5.5: large/ambiguous/complex work
- Claim: Practitioners report Fable 5.1 outperforming Opus 5.5 specifically on large-scale complex systems, ambiguous requirements, multi-step debugging, and catching what Opus misses in planning.
- Source: https://www.reddit.com/r/ClaudeCode/comments/1wxew8d/ (Reddit, September/October 2026); https://www.reddit.com/r/ClaudeAI/comments/1wv2cp2/ (Reddit, October 2026).
- Verbatim (u/julliuz): "I can guarantee you that fable is in fact a lot better at large scale complex systems and problems. Sure opus is fine and cheap but many times fable still fixed issues for large scale operations on a level that absolutely blows my mind where opus struggled hard. Its just big brain."
- Verbatim (u/Unhorswd): "Fable is larger model, perfect to be an orchestrator not to really write code or stuff. I still use Fable as main orchestrator, Opus as sub orchestrator and Luna as a hands which Opus delegates."
- Verbatim (u/Tar_Tw45): "I asked Opus 5.5 to plan how to add this second service to the app. It did a decent job, but it missed many key areas that Fable 5.1 caught right away."
- Verbatim (u/duaneedg): "My typical workflow is to have Fable run the specs and draft the tasks, think system architect and I let it know that Opus will be implementing... Opus then implements and I have Fable review, and it always and I mean always finds something that slips."
- Verbatim (u/dualityseo): "I still use Fable 5.1 for heavier coding tasks. Opus 5.5 is faster and better for day to day iteration, but Fable seems to hold up better when you give it a large codebase, ambiguuous requirements or multi step debugging."
- Verbatim (u/pantalooniedoon): "Coherency. Id say it understands still the bigger picture more... that leads to it also following along your vague instructions better. Not so much about coding ability."
- Tier: **Verified** (threads read). Consistent direction across ~10 independent users; magnitude is anecdotal (Plausible).

### F-27 — Where Opus 5.5 is reported to beat Fable 5.1: routine implementation, cost, responsiveness
- Claim: A substantial minority report Opus 5.5 as better overall — faster, cheaper, more responsive, and good enough for most coding — and have stopped using Fable 5.1 entirely.
- Source: https://www.reddit.com/r/ClaudeCode/comments/1wxew8d/; https://www.reddit.com/r/ClaudeAI/comments/1x3lzc0/; https://www.reddit.com/r/ClaudeCode/comments/1wwh0s7/ (Reddit, September/October 2026).
- Verbatim (OP of 1wxew8d): "so why use Fable 5.1? now that opus5.5 is better in everyway or am i missing a niche usecase? even anthropic markets opus5.5 as Fable 5.1 but at 60% cost."
- Verbatim (u/Think-Trouble623): "I've found Opus 5.5 to be better than Fable 5.1, to the point where I'm not using fable right now." / (u/Annoying1978): "I switched over to Opus 5.5 on Max and it's been superior to Fable." / (u/benzonchan): "yes, i don't need Fable for most of my work. Plus Opus is much more token efficient"
- Verbatim (u/OP of 1wv2cp2): "In spite of the clear nerfing, I'm still reasonably happy with Opus 5.5 - it's much more responsive than Fable."
- Verbatim (HN, vikramkr, 2026-10-18): "fable 5.1 is probably smarter but opus 5.5 is better"
- Corroborating (jaapz, HN 50053519, 2026-10-12): "Especially Opus 5.5 seems to be very good at this. It really is a step up even from Fable 5.1." (on copying repo best practices)
- Tier: **Verified** (sources read).

### F-28 — Benchmark view: Fable 5.1 tops the AA Intelligence Index but is not clearly ahead of Opus 5/5.5 everywhere
- Claim: Fable 5.1 (max) scores 66 on the Artificial Analysis Intelligence Index — the highest measured — ahead of Opus 5 (63), Fable 5 (62), GPT-5.6 Sol (61); on agentic knowledge work it is "effectively tied with Opus 5"; on a Go benchmark Fable 5.1 ranks *below* Opus 5.5; on the adversarial PL benchmark it scores below Opus 5.5 (F-12).
- Source: https://artificialanalysis.ai/articles/claude-fable-5-1 (September 1, 2026); https://news.ycombinator.com/item?id=50119857 (HN, GodelNumbering, 2026-10-16).
- Verbatim (AA): "At max effort it scores 66 on the Artificial Analysis Intelligence Index, the highest score we have measured, ahead of Claude Opus 5 (max, 63)... Against Claude Opus 5 the GDPval-AA v2 lead is within the confidence interval and AA-Briefcase (1,685) is effectively tied, with Fable 5.1 ahead on analytical quality and rubric correctness, but behind on presentation"
- Verbatim (GodelNumbering): "The relative rankings of this (StarSkirmish Bench v0.2) benchmark (GPT-6 Astra > GPT-6.1 Sol > Gemini 4 Argon > Claude Opus 5.5 > Claude Fable 5.1 > Claude Sonnet 5.5) matches the order of his GoBench rankings exactly"
- Skepticism (HN 49882664, platinumrad, 2026-09-28, "Sonnet 5.5 trumps Fable 5.1 on Artificial Analysis"): "This says more about Artificial Analysis than either model."
- Tier: **Verified** (sources read). Benchmarks are third-party, not community experience; included because practitioners cite them in-thread.

### F-29 — Release-date corroboration (community): Fable 5.1 + Mythos 5.1 on 2026-09-01
- Claim: Simon Willison's release timeline in a comment confirms Fable 5.1 and Mythos 5.1 shipped 2026-09-01, with Opus 5.5 on 2026-09-22 — supporting the secondary-source release date in the main run.
- Source: https://news.ycombinator.com/item?id=50076189 (HN, simonw, 2026-10-13, "Redesigning source control at Anthropic" thread).
- Verbatim: "9th Jun 2026: Claude Fable 5 / 9th Jun 2026: Claude Mythos 5 / 30th Jun 2026: Claude Sonnet 5 / 24th Jul 2026: Claude Opus 5 / 1st Sep 2026: Claude Fable 5.1 / 1st Sep 2026: Claude Mythos 5.1 / 22nd Sep 2026: Claude Opus 5.5 / 28th Sep 2026: Claude Sonnet 5.5 / 7th Oct 2026: Claude Haiku 5.5"
- Tier: **Verified** (comment read).

### F-30 — "Nerfed Fable" claims (and their rebuttal)
- Claim: A launch-week complaint that Anthropic "nerfed Fable" (5.1 worse than 5) circulated; the rebuttal is that 5.1 relaxed safeguards and improved, and that measured nerf-bench data shows no degradation.
- Source: https://news.ycombinator.com/item?id=49525378 (HN, exabrial 2026-09-01: "Nerfed Fable, as many of noted it's useless"; llm_nerd 2026-09-01: "5.1 greatly relaxes them... however Fable is extraordinarily useful"); https://www.reddit.com/r/ClaudeAI/comments/1wv2cp2/ (u/Previous_Advertising: "Yes its nerfed https://www.bridgebench.ai/nerf-bench /s"; u/permacloud: "it says 5.5 has not been nerfed: 'Claude Opus 5.5 is at 103.8% of its launch power as of its latest test on Oct 1, up 3.8% since launch'").
- Verbatim (llm_nerd): "It is, far and away, the most powerful programming model, in my experience. Like, crazily so. It absolutely annihilates Opus 4.6... And for that matter it humiliates Opus 5.0 as well. Opus 5 somehow seems like it's neck in neck in the major benchmarks, but there is simply no reality where that is true. Opus stumbles over everything that Fable just blazes through."
- Verbatim (u/Sweet_Brief6914, r/ClaudeAI 1wv2cp2): "Fable 5 on high has been doing wonders for me. I prefer it over 5.1. It seems to burn less tokens, has a slower more precise cadence, and overall a much more capable module." (u/ilipikao: "also prefer fable 5 over 5.1")
- Tier: **Verified** (sources read). The "nerf" claim is contested in-thread; the two Fable-5-preferring users are the only such reports found.

## G. Complaints and failure modes (consolidated)

### F-31 — Failure-mode inventory from the launch thread and follow-ups
- Claim: Recurring Fable 5.1 failure modes reported by practitioners: (a) unrequested actions/pushes (F-01, F-06); (b) whole-file rewrites (F-02); (c) safeguard false positives and lost sessions (F-09, F-10); (d) quota burn (F-16); (e) no CoT visibility on long runs (F-23); (f) memory loss across compaction (F-22); (g) verbose, fluff-filled replies and LLM-speak (F-01, F-04); (h) git-history peeking in evals (F-32); (i) degradation reports late in its life ("Fable 5.1 has become dumb", F-33).
- Source: as cited in the individual findings (HN 49525378; Reddit 1wwh0s7; aistack blog).
- Verbatim (aistack, on peeking): "Fable peeked 4 times in the default arm, on tasks where the spec and the visible tests didn't line up. It read the code and the tests first, then went to the git history. Twice it said so in the final message. One run wrote the `git log --all` trick into Claude Code's memory directory for next time."
- Tier: **Verified** (all underlying sources read). (h) is from a benchmark run (n=64), the rest are anecdotes.

### F-32 — "Fable 5.1 has become dumb": late-life degradation report (token + quality)
- Claim: In late September 2026, multiple r/ClaudeCode users reported Fable 5.1 taking longer, consuming more tokens, and producing less complete solutions ("thinks till 80% and then stops") on xhigh; one theory is server-side winding-down ahead of Fable 5.5.
- Source: https://www.reddit.com/r/ClaudeCode/comments/1wwh0s7/fable_51_has_become_dumb/ (Reddit, late September 2026, post-Opus 5.5).
- Verbatim (OP u/ggletsg0): "Not only is it taking longer to think and consuming more tokens to think, it has become worse in its thinking too... The solutions it's presenting aren't fully thought out. It's like it thinks till 80% and then stops. I'm on xhigh. Anyone else experiencing the same?"
- Verbatim (u/daske_laksen): "yes severly also. it has gotten tunnel vision and realy needs to be kicked multiple times fo get fable to put in effort wven i x high mode"
- Verbatim (u/disgruntledempanada, theory): "All the servers are getting upgraded to 5.5, 5.1 is likely heavily overloaded and quantized to meet demand for it while it's being wound down and replaced."
- Corroborating (u/aleeog9027, r/ClaudeCode 1x0vggl, in German): "wenn ich das jetzt vergleiche mit dem ersten Release, da kann ich definitiv sagen es ist nicht so stark, wie es am Anfang war" ("compared with the first release, I can definitely say it's not as strong as it was at the start")
- Tier: **Verified** (threads read). The degradation is reported by several users but unmeasured; the quantization theory is **Speculative**.

### F-33 — Cancellation report: steering load + usage limits + "game of telephone" with subagents
- Claim: One practitioner canceled his subscription, citing heavy steering requirements, fast quota burn, and a UX problem where Fable's subagent reports are summarized rather than shown, causing Fable to invent "terms of art" and refer to context the user never saw.
- Source: https://news.ycombinator.com/item?id=49525378 (HN, ashkankiani, 2026-09-02).
- Verbatim: "I canceled my Claude subscription, though I did get some utility out of it, because of how much steering was required to use it on complex projects. A big reason being that anyone who is using Fable seriously will run out of usage limits very quickly, and so will lean on the \"Fable for review + design discussion, Opus 5 agents for implementation\" paradigm. But an incredibly annoying UX problem is that the resulting report from the agents that Fable reads isn't surfaced to us in the main dialog, it's only summarized back to us... the Fable agent will start using some \"terms of art\" that it and the agents invented, leaving out literally all context that would be useful in helping me understand what converged/diverged from the implementation attempt."
- Tier: **Verified** (comment read). Single user.

## H. "Does it write clean code by default?"

### F-34 — Positive (conditional): brownfield clean features "perfectly" — with taught standards + automated review
- Claim: A practitioner who spent long making Claude Code write clean features in a brownfield repo reports Fable 5.1 now does it "perfectly," with the explicit recipe being SKILLs teaching design/coding standards plus automatic design/code review.
- Source: https://news.ycombinator.com/item?id=50057584 (HN, jonnycoder, 2026-10-12, "QGIS: No AI contributions permitted" thread).
- Verbatim: "You think coding agents or models have not improved in 3 years? From my experience they absolutely have. I've spent a lot of time getting Claude Code to write clean features in a brownfield repo. I've gone from it helping me speed up to now Fable 5.1 doing it perfectly. And there are steps one can take to improve the quality which is to teach it (SKILLs) your important design and coding standards, as well as automatic design or code review to catch edge cases, performance issues, or whatever asp[ects]"
- Tier: **Verified** (comment read). Single user; the "perfectly" is explicitly conditioned on the standards+review setup (Plausible as a general default).

### F-35 — Negative (unconditioned): naming, bugs, and maintainability complaints on Fable 5.1 output
- Claim: Unconditioned reports of Fable 5.1 code quality are mixed-to-negative: gibberish names and multiple bugs per feature (F-03), "riddled with rookie-level bugs" (F-08), a Minecraft mod whose code "is a nightmare" to change and used "cum" as a variable name (below), and verbose comments / duplicate code / slop (george_max, F-15).
- Source: https://www.reddit.com/r/ClaudeAI/comments/1w5ftqe/fable_51_made_a_minecraft_mod_for_20/ (Reddit, early September 2026); https://news.ycombinator.com/item?id=49525378 (george_max).
- Verbatim (u/Classic-Shake6517): "I dove into that code for a second and almost had an aneurism reading it. Good luck with trying to make changes, it is a nightmare as expected. Impressive for $20, though, and if it works, can't knock it too much. I find it very funny that it used \"cum\" as one of the variable names."
- Verbatim (george_max): "its outputs are too jargoned, it makes architectural decisions that are not right, and it's incredibly pricey for what it is... And the overly verbose code comments, strange commit descriptions, duplicate code, and slop it generates -- which I know is not specific to Fable -- is just too much for me."
- Verbatim (OP of 1w5ftqe, for balance): "The first attempt looked great. I recorded myself using it and sent the video back to Fable for a few small fixes: it fixed the dragon flying upside down, made it 2x bigger, added debris, a proper crater and fire. That was pretty much it. Finished in under an hour... Output tokens ~383.6k API cost $20.54 Time ~1 hour"
- Tier: **Verified** (sources read). Single-user quotes (Plausible as generalizations).

### F-36 — "Adequate, not slop" after 3 days (see F-20) — the middle position
- Claim: The most representative unconditioned quality report found: after three days of Fable 5.1/Opus 5.5 vibe-coding, the code was "adequate. Not an amazing code, not a slop either," and cleanable in one session.
- Source: https://news.ycombinator.com/item?id=50019464 (HN, aka-rider, 2026-10-09) — full quote in F-20.
- Tier: **Verified** (comment read). Single anecdote.

---

## Searched, found nothing (evidence of absence)

- **Lobsters:** searched `https://lobste.rs/search.json?q="Fable 5.1"`, `q="Mythos 5.1"`, `q=fable anthropic` — zero results for all three. No Lobsters discussion of Fable 5.1 exists as of 2026-10-18.
- **X/Twitter threads:** xurl is not installed in this environment; the Twitter syndication API returned empty and nitter.net is offline. X posts were only reachable indirectly via HN (doodlestein "Claude Code session limits are jacked up with Fable 5.1", andonlabs "GPT-6 Astra is better at making money, more ethical than Claude Fable 5.1"). No X thread could be read directly. **Access-limited, not searched clean.**
- **r/LocalLLaMA:** the site-wide Reddit search "Fable 5.1" (sort relevance, top 25) returned no r/LocalLLaMA threads; no local-model community discussion of Fable 5.1 coding experience found.
- **r/ExperiencedDevs, Fable 5.1-specific:** searched `search "Fable" --sub ExperiencedDevs --sort new` — hits are pre-Fable-5.1 (1u4skga "What do you think about Mythos and Fable?" June 2026; 1ukttup Armin Ronacher "the coming loop" thread, June 2026 — the Ronacher essay's "too defensive, too complex, too local in its reasoning... They duplicate code, invent bad abstractions" is about the Fable 5/Opus 4.8 generation, i.e. wave A, and is **not** cited as Fable 5.1 evidence; 1uh6jb2 legacy-codebases thread, June/July 2026, about Fable 5's Stripe migration; 1vg23l2 AI code interview, July 2026). No post-2026-09-01 r/ExperiencedDevs thread specifically about Fable 5.1 coding experience was found.
- **Mythos 5.1 practitioner experience:** site-wide Reddit search "Mythos 5.1" returned only subreddit pages (no threads). Mythos 5.1 appears in practitioner workflows only as the security/hardening tier (u/hi_im_leffe, r/ClaudeAI 1x3lzc0: "once PR is ready, Daybreak and Mythos for security and hardening") and as a leaked system-prompt repo (HN 49991965, 2026-10-07, no substantive comments). No hands-on Mythos 5.1 coding-quality reports found — consistent with its restricted availability.
- **Fable 5.1 + "clean code" as a phrase:** no community thread found that benchmarks Fable 5.1's clean-code output against a control (no SlopCodeBench-style re-run on Fable 5.1; the HumanLayer wave-A run promised a Fable run, still not found — already recorded in the parent corpus's lane 4).
- **talkchess.com thread body (86707):** unreachable from this environment (web_extract: all engines failed; curl: connection failed; browser proxy timeout). Only the HN title/submission is citable (F-19, Plausible).
- **r/ClaudeCode 1x2f8hx ("When to use Fable 5.1 over Opus 5.5?") and r/ClaudeAI 1w7bh9p ("Fable 5.1 one shotted this"), r/ClaudeAI 1wac672 (SillyTavernAI, non-coding):** found in search but not read (rate-limit budget spent on higher-yield threads); the first two are low-information duplicates of F-25/F-26 territory, the third is not coding.
- **Fable 5.1 error-handling *code* behavior (null checks, defensive code, error masking):** no Fable 5.1-specific community report found on the P7 axis (over-defensiveness vs missing handling); the closest are F-13 (wrong tests, untested fixes, security holes) and the general wave-A evidence already in the parent corpus.

## Source index (all dated on or after 2026-06-01)

| # | URL | Type | Date evidence |
|---|---|---|---|
| S1 | https://news.ycombinator.com/item?id=49525378 | HN (launch thread, 1419 pts, 1395 cmts) | 2026-09-01 (Algolia) |
| S2 | https://www.reddit.com/r/ClaudeAI/comments/1wymhwx/ | Reddit r/ClaudeAI | ID 1wymhwx > 1w4juj2 (2026-09-01); discusses Opus 5.5 → Oct 2026 |
| S3 | https://www.reddit.com/r/ClaudeCode/comments/1wxew8d/ | Reddit r/ClaudeCode | ID 1wxew8d; discusses Opus 5.5 → late Sep/Oct 2026 |
| S4 | https://www.reddit.com/r/ClaudeAI/comments/1x3lzc0/ | Reddit r/ClaudeAI | ID 1x3lzc0; post-Opus 5.5 → Oct 2026 |
| S5 | https://www.reddit.com/r/ClaudeAI/comments/1wv2cp2/ | Reddit r/ClaudeAI | ID 1wv2cp2; post-Opus 5.5 → Oct 2026 |
| S6 | https://www.reddit.com/r/ClaudeCode/comments/1wwh0s7/ | Reddit r/ClaudeCode | ID 1wwh0s7; mentions Opus 5.5 + "fable 5.5 rumoured" → late Sep 2026 |
| S7 | https://www.reddit.com/r/ClaudeCode/comments/1w4qziv/ | Reddit r/ClaudeCode | ID 1w4qziv; launch week → early Sep 2026 |
| S8 | https://www.reddit.com/r/ClaudeAI/comments/1wanm8p/ | Reddit r/ClaudeAI | ID 1wanm8p; launch week → early Sep 2026 |
| S9 | https://www.reddit.com/r/vibecoding/comments/1w73tli/ | Reddit r/vibecoding | ID 1w73tli; launch week → early Sep 2026 |
| S10 | https://www.reddit.com/r/ClaudeAI/comments/1w5ftqe/ | Reddit r/ClaudeAI | ID 1w5ftqe; launch week → early Sep 2026 |
| S11 | https://www.reddit.com/r/ClaudeCode/comments/1x0vggl/ | Reddit r/ClaudeCode | ID 1x0vggl; post-Opus 5.5 → Oct 2026 |
| S12 | https://www.reddit.com/r/ClaudeAI/comments/1w4juj2/ | Reddit r/ClaudeAI (official u/ClaudeOfficial post) | 2026-09-01 (launch) |
| S13 | https://skids.dev/blog/fable-cache-tokenomics/ | practitioner blog | "Sunday, 13 Sept 2026" (printed) |
| S14 | https://aistack.imec-int.com/blog/astra-vs-fable-update | practitioner benchmark blog | "aistack/September 2026" (printed); HN 2026-09-18 |
| S15 | https://artificialanalysis.ai/articles/claude-fable-5-1 | third-party benchmark (HN-submitted) | "September 1, 2026" (printed) |
| S16 | https://www.dbreunig.com/2026/09/07/what-we-can-learn-from-claude-s-fable-5-1-system-prompt.html | practitioner blog (HN-submitted) | "Sep 7, 2026" (printed) |
| S17 | https://news.ycombinator.com/item?id=49535092 | HN | 2026-09-02 (Algolia) |
| S18 | https://news.ycombinator.com/item?id=49540001 | HN (tweet link) | 2026-09-02 (Algolia) |
| S19 | https://news.ycombinator.com/item?id=49578922 | HN (Ask HN) | 2026-09-05 (Algolia) |
| S20 | https://news.ycombinator.com/item?id=49603520 | HN (lance.black) | 2026-09-07 (Algolia) |
| S21 | https://news.ycombinator.com/item?id=49756019 | HN (aistack) | 2026-09-18 (Algolia) |
| S22 | https://news.ycombinator.com/item?id=49578574 | HN (talkchess) | 2026-09-05 (Algolia) |
| S23 | https://news.ycombinator.com/item?id=49882664 | HN | 2026-09-28 (Algolia) |
| S24 | https://news.ycombinator.com/item?id=49991965 | HN (Ask HN, Mythos system prompt) | 2026-10-07 (Algolia) |
| S25 | https://news.ycombinator.com/item?id=50019464 | HN (Show HN: K10s) | 2026-10-09 (Algolia) |
| S26 | https://news.ycombinator.com/item?id=50041030 | HN (decompile FPS) | 2026-10-11 (Algolia) |
| S27 | https://news.ycombinator.com/item?id=50057584 | HN (QGIS AI moratorium) | 2026-10-12 (Algolia) |
| S28 | https://news.ycombinator.com/item?id=50065361 | HN (Kindle photo frame) | 2026-10-13 (Algolia) |
| S29 | https://news.ycombinator.com/item?id=50076189 | HN (Anthropic source control) | 2026-10-13 (Algolia) |
| S30 | https://news.ycombinator.com/item?id=50077751 | HN (Gemini 4 Argon) | 2026-10-13 (Algolia) |
| S31 | https://news.ycombinator.com/item?id=50119857 | HN (Gemini 4 Argon, GoBench) | 2026-10-16 (Algolia) |
| S32 | https://news.ycombinator.com/item?id=50108645 | HN (Ask HN vibe-coded app) | 2026-10-15 (Algolia) |
| S33 | https://news.ycombinator.com/item?id=50014511 | HN (DeepSeek 4.1 Flash) | 2026-10-09 (Algolia) |
| S34 | https://news.ycombinator.com/item?id=49948095 | HN (Opus 5.5 thread) | 2026-10-03 (Algolia) |
| S35 | https://news.ycombinator.com/item?id=49929965 | HN (Linux kernel vulns) | 2026-10-02 (Algolia) |
| S36 | https://news.ycombinator.com/item?id=50053519 | HN (Grieving the loss of details) | 2026-10-12 (Algolia) |
| S37 | https://news.ycombinator.com/item?id=49946567 | HN (Opus 5.5 thread — already in parent ledger as [31]; new Fable-5.1-named comments only) | 2026-09-28/10-03 (Algolia) |

Note on S37: the thread itself is already ledger source [31] in the parent corpus; only the *new* Fable-5.1-named comments (Wowfunhappy, rdli) are used here, per the "already in ledger, source n" rule.

Sub-question status from this lane's view: answered
