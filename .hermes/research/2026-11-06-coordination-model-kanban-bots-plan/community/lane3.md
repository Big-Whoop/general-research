# Lane 3 — Community + GitHub evidence: how Hermes users actually run multi-agent work, and what hurts

Date: 2026-11-06 · Sub-question 3 · Sources: GitHub issues in NousResearch/hermes-agent (via `gh search issues` / `gh issue view`, auth'd), r/hermesagent (reddit-reading skill, anonymous Atom backend → top-level comments only, no scores), dev.to, Substack, macd2/Crew README + ForgeCore launch post, prior local research corpus (`nixos-infra/.hermes/research/2026-10-28-crew-vs-kanban/`). All quotes verbatim. Tier key: **Verified** = authoritative for this exact subject (upstream issue with measurements / primary-source README) · **Plausible** = first-hand practitioner report, not reproduced on our install · **Speculative** = opinion/inference.

Reading note on tiers: community reports can never be "Verified for v0.22.7 on our install"; I mark an item Verified only when it is an upstream issue with log evidence or a primary-source document. Practitioner reports are Plausible even when several independent users confirm them.

---

## A. Where does the coordinator live — chat or board?

**A1. The dominant working pattern is: human talks to ONE coordinator profile in chat (Telegram/Desktop); the coordinator writes a brief + creates chained cards; workers never talk to each other; blocked/done cards ping back.**
- Source: r/hermesagent "Sharing my Hermes fleet setup: one coordinator, six specialists" (u/__smb, 2026-10-28) https://www.reddit.com/r/hermesagent/comments/1xi1oyz/ · Reddit · template repo github.com/SamueleBassoli/hermes-fleet-apps
- Quote: "I only talk to one profile, the coordinator. I reach it over Telegram, mostly from my phone. It doesn't build anything itself: it writes the job briefs, hands them out, checks what comes back, and it's the only one allowed to merge." … "rule is simple: workers never talk to each other. Everything goes through the coordinator and the Kanban board. A worker only sees its own card, and when it finishes, the next chained card starts on its own" … "There's one shared fleet file every profile reads before starting. It says who owns what and where each one's work goes. It's a map, not a status board: the live state of a job is on its Kanban card and in git."
- Tier: **Plausible** (first-hand, detailed, template published; Opus 5.5 on Max sub — same model class as ours).

**A2. Same shape from a second practitioner: default profile = single Telegram contact; a separate Planner profile replaces the built-in decomposer; "everything else lives in Kanban".**
- Source: r/hermesagent "Building a multi-agent AI organisation with Hermes" (u/DaveThe0nly reply, 2026-11-05) https://www.reddit.com/r/hermesagent/comments/1xoem9v/ · Reddit
- Quote: "My 'default' profile is my single point of contact via Telegram, everything else lives in Kanban. Planner Profile - PM/Staff engineer, plans and breaks down tasks instead of the built in decomposer (looks at current tasks at board also, everything is properly connected - related, blocked etc...) … Important is to instruct Hermes, if there are any blocking questions, to send you message where you clear it up and it can unblock the card. If a card gets stuck, let Hermes figure it out automatically first, then ask you - cards can get stuck for no reason sometimes."
- Tier: **Plausible**.

**A3. Community advice to a user who is "the message bus": don't make the coordinator notice completions — encode the chain as parent/child cards so the dispatcher promotes the next step; ownership = card assignee + workspace, not the chat session you typed in.**
- Source: r/hermesagent "How do you make coordinator–worker handoffs reliable" (u/Living-Swimming-2772, 2026-10-28; replies u/wireandshield, u/kaijurules, u/Mean-Loquat-7982) https://www.reddit.com/r/hermesagent/comments/1xhmndq/ · Reddit
- OP quote: "A worker finishes and saves its results, but the coordinator doesn't always pick them up and start the next step. … When I switch between Desktop and Slack, it's unclear which coordinator session should receive the task results … I still find myself acting as the message bus between agents."
- Reply quote (u/wireandshield): "The thing that removes you from the message bus is making the next step a dependent task instead of something the coordinator has to notice. Create the chain up front … it does not matter whether you were in Desktop or Slack when the worker finished, because ownership is the card's assignee plus its workspace, not the session you happened to be typing in." … "needs_input is the only kind that should actually page you … repeated block/unblock on the same card escalates to triage by itself — that escalation is the 'is it still working' signal you are currently producing manually." … "put the shared restrictions in a skill and pin it on the card with the skills field".
- Tier: **Plausible** (matches documented dispatcher semantics; the triage-escalation claim is contradicted in practice by B-section loops).

**A4. The in-chat coordinator that WAITS inside its own turn is the measured anti-pattern: sleep+poll busy-wait, ~2 min latency quantization per hop, context ratchet 92k→133k tokens from repeated `kanban_show` dumps, one routine DM = 1961 s / 56 API calls.**
- Source: GitHub issue #90853 "[Bug]: Bot Mode/Kanban orchestrator busy-waits on delegated tasks (sleep+poll)" (grigoryfeil, 2026-08-20, open, labels type/perf P3) https://github.com/NousResearch/hermes-agent/issues/90853 · GitHub issue
- Quote: "there is no event-driven way for it to be woken when a worker finishes. In practice the model falls back to a busy-wait loop: `terminal` runs `sleep 120`, then `kanban_show`, then an API round-trip decides 'keep waiting', repeat." … "an 11–19 KB `kanban_show` dump appended to the transcript every cycle, so context grows without bound while the orchestrator is just waiting." … "a routine gateway DM that the orchestrator chose to run through Kanban took 1961.6 s and 56 API calls … The same class of request handled solo completes in seconds to a few minutes. Chains (worker → independent review worker) multiply this". Suggested fixes: event-driven wake, a server-side `kanban_wait(task_ids, timeout_s)`, a `summary/delta` mode for `kanban_show`. Zero comments, no PR linked.
- Tier: **Verified** (log-backed upstream measurement; the only quantitative kanban-vs-solo latency/token figure found anywhere).

**A5. Crew's rationale for putting the coordinator ON the board: a model-free loop runs one pass per dispatch tick; mechanical cases never reach a model; the coordinator "decides, does not do"; chat stays untouched except for `/crew` and results.**
- Source: macd2/Crew README https://github.com/macd2/Crew (v0.10.7, 15★/5 forks on 2026-11-06, up from 5★ on 10-28) + ForgeCore launch post https://dev.to/forgecoreai/i-built-an-agentic-workforce-where-done-means-a-command-exited-0-475i + prior lane1 (`crew-docs/lane1.md` F10–F12, quoting crew.forgecoreai.com) · vendor README / vendor blog
- Quotes: README "Why" table: "**One ask** — `/crew <ask>` is the only thing you type. Normal chat stays untouched." "**An owner for every card** — The coordinator heals, retries, rescopes or splits a stuck card, and asks you only when it needs you." "**Hard budgets** — Every card carries a token budget; a run that reaches it stops instead of burning on." Launch post: "a card has one owner - a coordinator that wakes on every card event with the whole record in hand and takes exactly one decision: retry, rescope, split, or ask me. … After that I am out of the loop until the card ends, and it ends either with a verified result in the thread I asked from, or with one concrete question." Website (via lane1): "The mechanical cases never reach a model: a held workspace, a dead model pin, a proof that now passes. Everything else gets one bounded turn: two retries, then one question to you." Honest limits: "It is bad for work where done is a judgement" / "Proofs cost a minute each. On trivial work that is a bad trade."
- Tier: **Verified** (primary source for the rationale; effectiveness claims are vendor-reported → Plausible at best). Note: the launch post explicitly bounds the human's chat involvement to ≤5 questions in one batch before the card opens — i.e. Crew moves planning questions *out* of the open-ended chat loop too. Still no independent public Crew usage report found (re-checked: Reddit search "crew" in r/hermesagent, GitHub issues in macd2/Crew are all contributors/our own #19).

**A6. A fork-maintainer's version of "coordinator on the board": plans become a kanban task set to Manual; worker calls `advance` and waits for dispatcher approval; status changes push-wake the dispatcher; replies go to the exact originating session.**
- Source: u/RPG-Nerd in thread A3 · Reddit
- Quote: "I changed the plan system so that when a plan is dispatched by one agent to another, the dispatcher must review and approve each step. The worker calls advance and then waits for approval. … Instead of plans being a file, its a kanban task set to 'Manual' so everything gets stored with the task … I make status changes send a notification to the dispatcher that instantly wakes the agent. … The fork is too expensive to maintain to keep up with all the changes".
- Tier: **Speculative** for us (private fork, not reproducible); useful as a convergent design signal.

---

## B. Known loops / pitfalls (triage decomposer, needs_input flapping, block_loop_detected, stale/claim)

**B1. `auto_decompose` defaulted to `true` upstream and rewrites+spawns ANY triage card within one tick — including cards parked in triage by `block_loop_detected`; multiple reproductions up to v0.22.6; fix PR #109466 ("make auto-decompose opt-in") in flight.**
- Source: #109453 (airmonitor, 2026-09-12, open, P2) https://github.com/NousResearch/hermes-agent/issues/109453 · GitHub issue
- Quotes: "every card in `triage` - including cards created by automation for a technical purpose - is picked up by `auto_decompose_tick` on the next dispatcher tick, handed to the aux LLM, rewritten (title, body, assignee = orchestrator profile), promoted, and spawned." Comment (percyhendrux123-prog, Oct 20): "A worker card blocked twice with `needs_input`, both times for the same reason: it was waiting on the operator to grant a reviewer permission. … Within one dispatcher tick the auto-decomposer split the already-finished card into 5 child cards and assigned them to a different profile." Comment (rohitxsh, v0.22.6): "`block_loop_detected` is still the event name on main … and `list_triage_ids` still returns every triage card unfiltered."
- Tier: **Verified** upstream; our install has `auto_decompose: false` (context), so we are already on the safe side of this one.

**B2. Infinite block bounce: escalated triage tasks are re-specified/re-dispatched by the decomposer; one production card escalated 13×; same bounce via `kanban specify --all`.**
- Source: #75444 (Zazzles2908, 2026-07-31, open, 11 comments) https://github.com/NousResearch/hermes-agent/issues/75444 · GitHub issue
- Quotes: "The task bounces triage → worker → block → triage indefinitely. … task `t_f4413ea8` was escalated 13 times in this loop before manual intervention." (Marcin-Work, v0.21.5): "The card's title and body were rewritten as a full redo of steps 1–6" after the worker had finished steps 1–6 and blocked on a human approval for step 7. (Ajar9715): "`kanban specify --all` has the same bounce, not only the decomposer."
- Tier: **Verified** upstream (still open).

**B3. needs_input "flapping" root cause: same-cause = same `block_kind` only; every distinct `needs_input` question increments the recurrence counter; counter resets only on completion; limit 2 → the 2nd different question already lands in triage. Fix PR #83645 open.**
- Source: #83624 (DmytroVolodymyrson, 2026-08-11, open, needs-decision) https://github.com/NousResearch/hermes-agent/issues/83624 · GitHub issue
- Quote: "`block_recurrences` is reset only on successful completion, not when a human provides new input or `specify` changes the card. Consequently, any second `needs_input` block—regardless of content—becomes `block_loop_detected` and goes to `triage`." Also mkappl: same with `transient` across different CI heads.
- Tier: **Verified** upstream. Direct explanation of our pitfalls section "needs_input flapping" and of the "one question per turn" rule being incompatible with the kernel's counter.

**B4. The maker→checker→rework loop is structurally broken by `BLOCK_RECURRENCE_LIMIT=2`; one multi-board install measured 148 trips in 7 days, 88/105 triage cards from block loops, 29% of worker runs ending blocked.**
- Source: #74009 (NeoGeoSNK, 2026-07-29, open) https://github.com/NousResearch/hermes-agent/issues/74009 · GitHub issue
- Quote (sycamoregroupltd, kernel as of 2026-10-07): "Scale (7 days, ~10 boards, ~40 worker profiles): 148 `block_loop_detected` trips. 88 of the 105 cards now in `triage` carry a `block_loop_detected` event. 29% of all worker runs ended with the card blocked. The dominant shape … a maker finishes and blocks for an external checker … The maker's second block for the re-check is the second same-kind block, so the card goes to `triage`, where nothing dispatches it." Also: "the CLI has no supported recovery path" (no command targets triage; #149042 confirms "there is no CLI or tool action to move a card to `triage` explicitly").
- Tier: **Verified** upstream.

**B5. Silent token burn: with auto-decompose on, a card parked in triage is re-billed to the aux LLM every tick forever — 4,653 paid calls in ~4 days (≈¥70), 96% of one day's requests, invisible in local `state.db` cost reports.**
- Source: #109566 (Big-David365, 2026-09-13, open, area/billing) + #118872 duplicate https://github.com/NousResearch/hermes-agent/issues/109566 · GitHub issue
- Quote (English summary in issue): "A card parked in triage whose decomposition …" + body: "3 天 23 小时 4,653 次付费调用 ≈ ¥70 … 本地 state.db 记账不记录辅助模型调用" (3d23h, 4,653 paid calls; local state.db does not record auxiliary-model calls). freeformz (v0.21.7): "493 `kanban_decomposer` calls in under a day, a steady ~33 per hour". Related #118595: decomposer produces no `session_model_usage` rows (cost unattributed).
- Tier: **Verified** upstream. Not applicable to us while `auto_decompose: false`, but it is the single largest reported "kanban token burn" and it is in the *orchestration layer*, not the workers.

**B6. Cards that keep running without converging (schedule loops, review ping-pong) trip no diagnostic; "The operator only notices when token usage climbs"; 20+ runs over two days "is not unusual".**
- Source: #149042 (artyficialmind, 2026-11-04, open, feature) https://github.com/NousResearch/hermes-agent/issues/149042 · GitHub issue
- Quote: "A Kanban card can loop for days without any rule in `hermes_cli/kanban_diagnostics.py` firing, as long as each run ends cleanly. … The operator only notices when token usage climbs. A card with 20+ runs over two days is not unusual in this pattern".
- Tier: **Verified** upstream (feature request with code references; 2 days old).

**B7. No per-run token/turn bound for workers; a worker that lost its claim keeps calling the model; stale detection off on daemon/CLI dispatch paths.**
- Sources: #124365 (zanzipanzi, 2026-09-26) https://github.com/NousResearch/hermes-agent/issues/124365 ; #146433 (Adolanium, 2026-10-29, P2) https://github.com/NousResearch/hermes-agent/issues/146433 ; umbrella #35986 (magnus919, 2026-05-31) https://github.com/NousResearch/hermes-agent/issues/35986 · GitHub issues
- Quotes: #124365: "Turn budgets reset every turn, so nothing caps a run's total model calls or tokens. … A worker that has lost its claim keeps calling the model and running tools." #146433: "`kanban.dispatch_stale_timeout_seconds` … is only honoured by the gateway-embedded dispatcher." #35986 comment (donovan-yohan): "cards had otherwise sat blocked for hundreds of hours" until someone ran `diag` by hand.
- Tier: **Verified** upstream. (Our install dispatches inside the gateway, so #146433 does not bite us.)

**B8. Claim/identity leakage family: nested processes (delegate_task children, cron fired beside a worker) inherit `HERMES_KANBAN_TASK` and can complete the parent card; `kanban complete` lets any caller close a claimed card.**
- Sources: #81508, #103883, #87725, #145739 (2026-10-27) https://github.com/NousResearch/hermes-agent/issues/145739 · GitHub issues (titles verified via `gh search`)
- Quote (#103883 title): "cron fired from/beside a kanban worker closes the worker's card — 6 identity gates read raw HERMES_KANBAN_TASK". Docs page confirms the design hole: "a delegate_task child or a cron run fired from inside a worker — which inherit the worker's HERMES_KANBAN_TASK — neither receives the worker protocol nor records a terminal outcome".
- Tier: **Verified** upstream (open). Relevant to "worker uses delegate_task inside a card" patterns (also Reddit: "delegate task inside a card screams errors", u/Euphoric_Piglet_9087, thread C1).

**B9. Notifications drop exactly the events an in-chat coordinator needs: block_loop/review events omitted from Desktop/TUI; `block_loop_detected` transitions silent; blocked wakes to api_server omit the reason.**
- Sources: #141866 (2026-10-20, 8 comments), #82597, #99436, #123563 · GitHub issues (titles from `gh search`)
- Quote (#82597 title): "Kanban: block_loop_detected transitions are silent — repeat blocks never notify, cards vanish into t[riage]". (#141866 title): "Desktop/TUI Kanban notifications omit block-loop and review events (corrected diagnosis)".
- Tier: **Verified** upstream (open). This is the mechanism behind "work stuck, chat lost connection" in our own 2026-10-28 suspension note.

---

## C. Reported token burn / latency: kanban workers vs subagents vs bots

**C1. The only side-by-side comparison found: single agent + delegate_task ≈ kanban orchestrator (no goal loop) in quality AND token usage; auto-decomposition and goal mode added overhead.**
- Source: r/hermesagent "When do we need more agents? Testing Single Agent vs Multi-Agent Workflows" (u/_wanderloots, 2026-09-19, video + summary) https://www.reddit.com/r/hermesagent/comments/1wksx3p/ · Reddit/YouTube creator
- Quote: "The single agent with delegation and the Kanban orchestrator without a goal loop came out pretty similar in quality and token usage. Automatic decomposition and the goal-enabled setup added overhead for this particular task. For me, the appeal of Kanban is being able to come back later, inspect the handoffs, see what's blocked, and continue the work." Also: subagents "keep the main conversation smaller, although it doesn't necessarily reduce total token usage once you count the helpers."
- Tier: **Plausible** (single research task, no numbers published).

**C2. ~1B-token benchmark on a third-party orchestration layer: multi-agent only pays when offloading expensive orchestrator tokens to cheaper builders/verifiers (30–40% avg, up to 70% main-session savings); author abandoned his own kanban layer — "no benefit … outside highly regulated environments that need detailed audit trails and human approval gates"; auto-verify turned off because it "wasn't finding any problems and was just burning extra tokens".**
- Source: u/johnfkngzoidberg reply in C1 thread (github.com/lunarnexus/orchestra, orchestra-bench, cellos) · Reddit
- Quote: "through about 1B tokens worth of testing, I found that agents aren't all that useful unless you're trying to offload expensive tokens from an orchestrator/planner to builders/verifiers/reviewers/appsec roles using cheaper/local tokens … Average savings is around 30%-40% … and only with long running or complicated tasks." "I also wrote a Kanban layer … I've pretty much abandoned that project for now. There's just no benefit to be had outside of highly regulated environments".
- Tier: **Plausible** (self-reported, own tool, not Hermes-kanban-specific). Note: same user wrote "It's terrible." about Hermes kanban in thread D1.

**C3. Subscription-budget reality for a 7-profile Opus 5.5 fleet via kanban: $100 Max plan hit daily limits "quite often"; $200 plan sits at 80–90% weekly quota; mitigations = narrow briefs (≤3 deliverables/card, handoffs ≤3 files), compress at 150k, max 2 compressions then fresh session, max 150 turns/run.**
- Source: u/__smb in A1 thread · Reddit
- Quote: "On the $100 Max plan I was hitting the daily limit quite often. … On the $200 plan I basically never hit the daily or weekly limit, but I do end up at around 80-90% of the weekly quota every week." "Context that never gets loaded is the cheapest kind." "After the second compression, the agent stops and writes a handoff instead of pushing on. By a third summary too much detail is gone."
- Tier: **Plausible** (first-hand numbers, same model class as ours).

**C4. Kanban cost blow-ups users report are from parallelism and retries, not per-card overhead: "started all tasks simultaneously which blew through my OpenAI allowance nearly immediately"; "20 tasks trying to fix my 4 task simple board"; goal-mode-in-chat user: "not even 1/10 of the token usage".**
- Source: r/hermesagent "Do you use Kanban in Hermes? If not, why not?" (u/Jonathan_Rivera, ~2026-08) https://www.reddit.com/r/hermesagent/comments/1vfl4es/ · Reddit
- Quotes: u/GullibleBoat: "I tried it and it immediately started all tasks simultaneously which blew through my OpenAI allowance nearly immediately." u/Euphoric_Piglet_9087: "The tasks started spawning other tasks and immediately I had 20 tasks trying to fix my 4 task simple board. DeepSeek wrote a patch to prevent cards from spawning other cards". u/RobertoVeloso: "using goal mode and asking an agent to deliver was waaaay more effective and not even 1/10 of the token usage". u/Tha_Reaper: "You can tell the orchestrator to do all tasks sequentially, not parallel. That usually works for me."
- Tier: **Plausible**. Our `max_in_progress_per_profile: 5` already caps this.

**C5. Profile-level token argument for bots/profiles: narrow profiles load a fraction of the per-turn tool context; this was the historical reason for role profiles (20–30k tokens of tool schemas) but is now partly moot since tools are no longer front-loaded.**
- Source: r/hermesagent "New Bot feature vs Multiple Profiles vs a Master Profile" (u/SirDomz, 2026-08-17) https://www.reddit.com/r/hermesagent/comments/1vqsnol/ · Reddit
- Quotes: u/Schizophreud: "If you have one profile that does everything, you load all of the tools upfront … 20-30 thousand tokens every time you start a new conversation." u/Elektro121: "Actually they don't load the tool on the context automatically anymore" (links Teknium X post). u/Mean-Loquat-7982: "I'd only reach for separate profiles when roles need different tools or you want smaller per-turn tool loads, which is real, a narrow profile loads a fraction of the context a do-everything one does."
- Tier: **Plausible**.

**C6. Bot-mode group chat has its own token/latency pathology: each thread = fresh 2-message throwaway session with delta-only prompt; 5-bot room lost the task within ~45 min; Hindsight memory "do[es] not compensate"; still reproduces on 0.21.6 canary; fix PR #120762 closed unmerged.**
- Source: #123766 (Aiden181, 2026-09-26, open, P2) https://github.com/NousResearch/hermes-agent/issues/123766 · GitHub issue
- Quote: "In a real multi-bot working session (5 members), bots lost the original task instruction within ~45 minutes of active discussion: they replied to the newest 1-2 lines, repeated questions already answered, and ignored decisions made earlier in the room. Persistent memory providers (Hindsight) do not compensate, because throwaway 2-message sessions retain nothing on their own."
- Tier: **Verified** upstream (open). Directly relevant to "bot army via group chat" as a coordination substrate on our Hindsight-backed install.

**C7. Bot-to-bot transport is a shell hop (`hermes -p <agent> chat … -q`) with no delivery signal, no envelope, and it "doesn't survive sandboxing"; Teknium's own design issue #88061 names reliable pipeline execution (A→B→C must not start C when B failed) as unsolved.**
- Source: #88061 (teknium1, 2026-08-17, design) https://github.com/NousResearch/hermes-agent/issues/88061 ; #89995 (Bot Mode rooms in dashboard/gateway, 21 comments) · GitHub issues
- Quote (MrFluffen): "the transport under every hop today is a shell command … It doesn't survive sandboxing. A profile on `terminal.backend: docker` has no `hermes` binary in its sandbox". (Kavyrocom, production incident): "one member never produced a result in the room. Because group turns are serial, the following members waited and the room appeared silent. The user asked for status and discovered the missing handoff only manually."
- Tier: **Verified** upstream (design status, open).

---

## D. Did anyone move kanban → bots/chat, or the reverse, and why?

**D1. Mass "kanban → back to chat/delegation" testimony in the moderator's survey thread (~40 top-level replies; majority negative): unreliable, stuck cards, babysitting, setup cost; the minority who stayed all say the same thing — it works once the main agent drives it and the human stops managing the board by hand.**
- Source: thread C4 (u/Jonathan_Rivera "Do you use Kanban in Hermes? If not, why not?") · Reddit
- Moved away: u/DanBennett: "It's too unreliable. Things get blocked that can be dealt with but never do. It's easier and better to just do it within a session and delegation". u/yeahbuddyia: "Hermes Kanban takes more than it gives. It's simply unreliable so you have to babysit it AND manage the kanban board. The agents make it worse just patching around it creating other errors." u/Nashtanir: "Tasks get stuck and cannot be continued at all." u/-Davster-: "having the entire Kanban lock up permanently because I swapped to a different model for 10 mins - waiting for a scheduled cron job to fix it … you can't make a Kanban task to clean up the Kanban either - because kanban card workers don't get permissions to do that." u/marvborg: "It is very difficult to track and prevent circular dependencies that cause deadlocks or races. I use it as a list but not to launch agents directly." u/one_two_three_4_5: moved to Linear MCP + a cron that watches "@hermesbot". u/hubertron: "just use projects now". u/XLioncc: "I need a simple method to let my agent to talk to another agent, and not kanban". u/mitchells00: "HITL is broken for Hermes Kanban: the tasks can't surface approval requests, and there's no practical way to stop/intervene in a kanban task session".
- Stayed: u/Even-Breeze: "I use it extensively now but it took a lot to get it functional. I think my biggest mistake was trying to manage it manually. Now I just let my main agent handle things and it works great." u/Ithron_Morn: "I just gave my main agent control to manage it/them for me." u/Lpaydat: "manage up to 20 projects concurrently without the need to monitor it for days … without the proper setup, it's very difficult to use." u/ambassadortim: "It took a lot of tweaking and coaching to get it stable. Now Hermes uses it for projects". u/ivanstackd: "works well for bigger tasks. You can setup multiple rounds of review … I'm mostly running deepseek flash so costs are basically zero". u/Judg3d: "I just use it as bot to bot comms, so i avoid the churn in telegram".
- Tier: **Plausible** (large N, independent, but version-unspecified ~Aug 2026).

**D2. Kanban → disabled → back to kanban with smaller cards: a user who "disabled Kanban because I had so many cards fail" attributes the collapse to oversized cards + unmerged worktrees; the fleet author's fix: "small cards (one stage, one job each) … only the coordinator creates cards. If a card blocks twice it gets split into smaller ones instead of retried."**
- Source: u/Dave-The-Chef + u/__smb in thread A1 · Reddit
- Quote (Dave-The-Chef): "I suspect I was giving each profile too much work per feature and spawning multiple worktress without merging and each profile was responsible for its own ticket. Kind of just led to kanban ticket collapse and I found myself fixing more than I solved for."
- Tier: **Plausible**.

**D3. Bots ≠ a migration target: the community consensus is that Bot Mode is a Desktop UI over profiles ("that capability has always existed"), and the one user who prefers it over kanban prefers *in-session agent-to-agent calls*, not the board.**
- Source: thread C5 · Reddit
- Quotes: u/veganmaister: "The way bot mode was launched is weird. That capability has always existed in Hermes. Seperate profiles for seperate agents. They've just added the front end to Hermes Desktop and called it 'bot mode'". u/covamedia: "It's essentially borrowing the concepts that are in place with the Kanban feature, but without the complexity. I much prefer my agents calling each other in session. I also haven't been a big fan of the Kanban implementation in Hermes." u/shortsteve: "I just have a main profile that is the orchestrator and that profile sends the relevant information to the profile to do it's task. When an output is received the main profile reviews the work and may make changes".
- Tier: **Plausible**. No post found where someone moved a durable workflow *to* group chat; the Bot-vs-Kanban content creators (vivek_shetye dev.to/YouTube, 2026-08-25) recommend "Bot Mode = the team, Kanban = the work" and use bots only as the roster + cron trigger feeding an orchestrator that creates cards.

**D4. Telegram-bot-per-agent fleets hit the same handoff problem as kanban users (LLM "forgets" to call the handoff tool; UI shows work that never got dispatched); the two answers offered were "a skill that pins who does what" and "Kanban".**
- Source: r/hermesagent "Hermes multi-agent Telegram orchestration" (u/CCR_OUTBets123, 2026-08-11) https://www.reddit.com/r/hermesagent/comments/1vllo7l/ · Reddit
- Quote (OP): "what mechanism guarantees that Agent A finishing automatically wakes Agent B without relying on the LLM remembering to call a handoff tool?" u/AvGeekExplorer: "I create a skill for the workflow I'm doing and specify the agents that should perform each task. Then I just instruct my orchestrator to 'follow x skill to do y' and it prevents the orchestrator from deciding on its own who should do what." u/RPG-Nerd: "Kanban". u/jebk (thread "tokenmaxxing"): "The kanban is very reliable for going between profiles" vs u/gabrurdesodio: "Orchestrating between profiles is a pain in the ass tho. It always finds a way of hallucinate and skip the workflow…"
- Tier: **Plausible**.

**D5. Independent blogger (June, v0.15): still uses delegate_task daily, migrating heavy review flows to the board precisely because "when a fork/join run dies, it dies whole, and the context dies with it".**
- Source: Anthony Maio, "Hermes Agent Got Serious" (2026-06-05) https://anthonymaio.substack.com/p/hermes-agent-got-serious · blog
- Quote (search snippet; the full-text extract was truncated before this passage): "I lean on delegate_task every day and I am still migrating my heavier review flows onto the board. The reason I am migrating is exactly the failure mode delegate_task has and Kanban does not. When a fork/join run dies, it dies whole, and the context dies with it." In-text: "delegate_task is a function call, while Kanban is a work queue where every handoff is a row any profile or human can see and edit."
- Tier: **Plausible** (pre-dates most of the B-section bugs; v0.15).

---

## E. Patterns people converge on (synthesis)

1. **One human-facing coordinator in chat (Telegram/Desktop); everything durable on the board.** Nobody successful keeps the *supervision loop* in chat. The coordinator's chat turn ends when the cards are created; results come back via card events (done/blocked ping), not by the coordinator waiting. The one measured counter-example (#90853: coordinator waits in-turn) is the worst latency/token figure in the entire corpus (1961 s, 56 calls, +40k context for a routine DM).
2. **Encode the plan as the dependency graph, up front.** "Link the steps up front", "make each next step a child", "cards are chained, so the next stage starts on its own". The coordinator is not a scheduler; the dispatcher is. This is exactly what Crew mechanises (coordinator = one model-free pass per tick + one bounded decision turn).
3. **Replace the built-in decomposer with a profile or with the chat coordinator.** Multiple practitioners ("instead of the built in decomposer", "I've also read that the decomposer isn't ideal") and the upstream bug cluster (B1/B2/B5) agree: `auto_decompose` on a board that also receives block-loop escalations is the #1 reported loop and the #1 reported silent token sink. Our `auto_decompose: false` is the community default-in-practice.
4. **`needs_input` is the only block kind that should page a human — but the kernel's recurrence counter (same `kind` = same cause, limit 2, no reset on human input) turns a second question into triage.** Practitioner mitigations: ask at most one block per card (Crew: ≤5 questions batched *before* the card opens, then "two retries, then one question"); if a card blocks twice, split it instead of answering again (__smb). This reframes our "one question per turn" rule: it must be "one question per *card lifetime*" to survive `BLOCK_RECURRENCE_LIMIT=2` on v0.22.x.
5. **Small cards, one writer per artifact, one worktree per card, coordinator merges.** Convergent across __smb, Crew ("never two writers on one artifact", ≤6 children), curiousbheja (design-doc + checklist so "fresh sessions" are cheap). Oversized cards are the stated cause of "kanban ticket collapse".
6. **Shared truth lives in the repo / a pinned skill, not in N profiles.** "repo truth in the repo, role truth in the profile" (AGENTS.md / .hermes.md); "put the shared restrictions in a skill and pin it on the card with the skills field"; weekly job promotes lessons seen in ≥2 profiles' lessons files to a shared file (Unusual-Albatross43). Matches our `crew/lessons.md` decision and argues against per-role memory banks for rules.
7. **Context hygiene is the real token lever, not the coordination primitive.** Narrow briefs, ≤3 files per handoff, compress at 150k, hard cap on compressions, HANDOFF comment that is "state, not instructions". The only controlled comparison (C1) found kanban ≈ delegate_task in tokens when the goal loop/decomposer are off; the only large benchmark (C2) found savings come from *cheaper models on worker roles*, not from the board. With Opus everywhere (our setup) the board buys durability and auditability, not tokens.
8. **Bots/group chat are a roster + cron trigger, not a work queue.** No practitioner runs a durable pipeline through group chat; the upstream design issue (#88061) and the room-context bug (#123766) explain why. The pattern that uses bots well is: bot routine (cron) → orchestrator profile → cards.
9. **Hard caps everywhere**: per-profile in-progress cap (ours: 5), per-run turn cap (150), per-card token budget (Crew), "if a card blocks twice, split". Upstream has no per-run token bound (#124365) and no non-convergence diagnostic (#149042), so these caps must be imposed by the orchestrator/plugin.
10. **Expect to babysit until the rules are written down.** Every "it works for me" post includes "it took a lot of tweaking", "write the rule down in that profile's skill, with the reason", "commit every profile change to git so you can roll back". The failure stories are the same setups before that discipline.

**Direct answers to the lane questions**
- *Coordinator in chat or on the board?* Hybrid, with a sharp split: intake/planning in chat (bounded), supervision on the board (event-driven). Nobody keeps a *polling* coordinator in chat and reports it working; Crew moves even the decision turn onto a tick-driven, file-prompted role profile.
- *Token/latency of kanban vs subagents vs bots?* One upstream measurement (A4) for the in-chat-waiting anti-pattern; one informal parity result (C1); one big-benchmark claim that savings come from model tiering (C2); subscription-quota anecdotes (C3). No measurement found of kanban *worker* overhead (skill re-reads, spawn cold start) per card — gap.
- *Known loops?* Decomposer×block_loop (B1/B2/B5), needs_input same-kind counter (B3/B4), non-converging schedule/review loops (B6), claim/identity leakage (B8), silent notifications (B9), bot-room amnesia (C6).
- *Moved kanban→bots or back?* Many moved kanban→"session + delegation" or →external trackers (D1); some returned to kanban with smaller cards (D2); nobody reports moving a pipeline onto bot-mode group chat (D3); Telegram-bot fleets converge back toward the board or a pinned workflow skill (D4).

---

## Searched, found nothing

| Query | Source type | Result |
|---|---|---|
| `gh search issues "kanban needs_input"`, `"needs_input flapping"`, `"kanban slow"`, `"delegate_task cost tokens"`, `"subagent context tokens delegate_task"`, `"kanban latency dispatch"`, `"kanban worker tokens skill"`, `"orchestrator chat poll kanban wake"`, `"kanban notify wake orchestrator session"`, `"kanban orchestrator context growth"` | GitHub issues (repo-scoped) | 0 hits each — the flapping/latency vocabulary is ours, not upstream's; upstream files these as block_loop/auto_decompose/busy-wait |
| GraphQL search type:DISCUSSION "kanban orchestrator chat" | GitHub Discussions | 0 nodes (discussions appear unused/disabled for this topic) |
| `"bot mode" kanban` | GitHub issues | only #90853 (+2 unrelated) |
| site:reddit.com/r/hermesagent "crew" / forgecore / macd2 (re-check) | Reddit search | still no third-party Crew report (consistent with 2026-10-28 lane) |
| hermes agent "bot mode" vs kanban tokens blog | web | only vivek_shetye dev.to/YouTube (no measurements) and the Reddit threads cited |
| Kanban worker per-card overhead measurement (skill prompt size, spawn time) | all | not found anywhere — nobody has published per-card worker cost |
| X/Twitter posts on hermes kanban orchestrator (via web_search) | web | none surfaced beyond a Teknium tool-loading note quoted on Reddit |
| Discord summaries | web | none indexed |
| Reddit nested replies / scores | Reddit | unavailable (anonymous Atom backend returns top-level comments only; counts and vote scores not captured) |
| Local `/opt/data/plugins/crew` | local | not present at that path anymore (crew roles exist as profiles/bootstrap JSON and `/opt/data/kanban/boards/nixos-infra/crew`); rationale taken from upstream README + prior lane1 instead |

Sub-question status from this lane's view: answered
