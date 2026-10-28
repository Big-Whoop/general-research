# LANE L2 — Official best-practice on splitting work off the default profile (SQ2)

Docs-first execution. Every quote verbatim from the cited official page (or issue text).
Confidence tiers: Verified = authoritative source states this exact claim; Plausible = sound
report/behavior, not demonstrated on-target by an authoritative doc; Speculative = inference.

Note: URLs below omit the repeated base `https://hermes-agent.nousresearch.com`.

---

## A. Explicit split recommendations (what official sources actually say)

**L2-1. The single strong "always split" rule: one agent process per profile — never two writers on one Hermes home.**
- Source: /docs/user-guide/profiles — official-docs (callout "Give every agent its own profile")
- Quote: "Never point two agent processes at the same profile (the same Hermes home). Both write memory automatically, and each loads the other's writes into its system prompt at session start — so two writers on one home compound each other's state until it stops being anything you configured. Profiles exist exactly to prevent this; agents that need shared memory should use an external memory provider instead."
- Confidence: Verified
- This is the documented hazard matching our fleet-memory incident (kanban cards writing next to the interactive session on /opt/data).

**L2-2. Same warning restated in the FAQ with the degradation mechanism.**
- Source: /docs/reference/faq ("Do profiles share memory or sessions?") — official-docs
- Quote: "This isolation is also the reason to never run two agents against the _same_ profile or Hermes home: both write memory automatically and each loads the other's writes at session start, so their stored state degrades with every session. One agent per profile."
- Confidence: Verified

**L2-3. Documented purpose of profiles = per-purpose agents without state mixing.**
- Source: /docs/user-guide/profiles ("What are profiles?") — official-docs
- Quote: "Profiles let you run separate agents for different purposes — a coding assistant, a personal bot, a research agent — without mixing up Hermes state."
- Confidence: Verified

**L2-4. The canonical "when you want multiple agents" list lives on the multi-profile-gateways page.**
- Source: /docs/user-guide/multi-profile-gateways ("When to use this") — official-docs
- Quote: "A personal assistant on one Telegram bot and a coding agent on another / One agent per family member or one per Slack workspace / Sandbox + production instances of the same configuration / A research agent + a writing agent + a cron-driven bot — each with isolated memory and skills"
- Confidence: Verified

**L2-5. Profiles are cheap: no hard limit, idle profiles cost nothing.**
- Source: /docs/reference/faq ("How many profiles can I run?") — official-docs
- Quote: "There is no hard limit. ... The practical limit depends on your disk space and how many concurrent gateways your system can handle (each gateway is a lightweight Python process). Running dozens of profiles is fine; each idle profile uses no resources."
- Confidence: Verified

**L2-6. Bot Mode roster is the official presentation layer on top of profiles ("Every Bot is a profile").**
- Source: /docs/user-guide/profiles ("Profiles, agents, and bots") — official-docs
- Quote: "Every Bot is a profile, but not every profile is a Bot: a profile becomes a Bot when Bot Mode stores its roster presentation (title, avatar, section, hidden state) in the profile's metadata and pins its canonical Bot Chat."
- Confidence: Verified
- (Boundary mechanics are L3's lane; recorded here because it is an official reason to create profiles.)

## B. Documented silence — the absence is a finding

**L2-7. NO official page says "everything on the default profile is bad" or recommends splitting the default profile for load/hygiene. The only split mandates are (a) one-agent-per-home (L2-1/2) and (b) the gateway topology rule (L2-10).**
- Source: reviewed WHOLE pages /docs/guides/tips, /docs/reference/faq, /docs/user-guide/security, /docs/guides/secure-hermes-on-a-work-machine, /docs/user-guide/profiles, /docs/user-guide/multi-profile-gateways — official-docs
- Evidence of absence: the tips page contains zero profile mentions (full-text search for "profile" returns no tips-page hits; its Performance & Cost section recommends delegation and model choice, not profiles). The security page's eight-layer model is not profile-based and its Gateway Deployment Checklist (10 items: allowlists, container backend, resource limits, secrets, pairing, command allowlist review, terminal.cwd, non-root, logs, updates) contains no profile item.
- Confidence: Verified (absence confirmed by whole-page review)

**L2-8. Where a split WOULD be the obvious answer, the FAQ instead steers to non-profile mechanisms.**
- Source: /docs/reference/faq ("Running multiple agents on one WhatsApp number"; "Using different models for different tasks") — official-docs
- Quote: "Use a single profile with personality switching. Create different `AGENTS.md` context files or use the `/personality` command to change behavior per chat." and "Use cron jobs for specialized tasks. ... no separate agent needed."
- Confidence: Verified
- For multi-model cost the FAQ prescribes delegation config + `/model`, not per-profile models: "prefer delegation (subagents get their own fresh context) or a new session over repeated back-and-forth switching."

## C. Gateway topology: multiplexed host vs per-profile gateways

**L2-9. Multiplexing is on by default and is the supported topology; one host gateway serves every profile with per-profile credentials.**
- Source: /docs/user-guide/multi-profile-gateways — official-docs
- Quote: "Multiplexing is **on by default** (`gateway.multiplex_profiles` defaults to `true`) ... Each turn resolves the routed profile's config, skills, memory, SOUL, **and provider keys** — credentials are never shared across profiles."
- Confidence: Verified
- Matches our deployment (default gateway multiplexes; single pod).

**L2-10. New per-profile gateway processes are refused; per-profile `gateway.standalone: true` is only a temporary shim.**
- Source: /docs/user-guide/multi-profile-gateways ("No new per-profile gateways"; "Temporary: gateway.standalone: true") — official-docs
- Quote: "One-process-per-profile is no longer a topology to _choose_ implicitly: a named profile's `gateway install` / `gateway start` refuses without `--force`" and "Do not build new setups on it: if you are starting fresh, run the host multiplexer."
- Confidence: Verified
- Implication for us: extra profiles should ride the existing multiplexed default gateway, not add processes to the pod.

**L2-11. When to prefer the single multiplexing gateway (explicitly framed for container deployments).**
- Source: /docs/user-guide/multi-profile-gateways ("When to prefer multiplexing") — official-docs
- Quote: "A container/VPS deployment where N supervisor units, N ports, and N PID files are a burden. / Many low-traffic profiles that don't each justify a full process. / You want a single thing to start, monitor, and restart."
- Confidence: Verified

**L2-12. Bot tokens are exclusive per profile; duplicates are refused/parked (token locks).**
- Source: /docs/reference/faq + /docs/user-guide/multi-profile-gateways ("Token-conflict safety") — official-docs
- Quote: "No. Each messaging platform (Telegram, Discord, etc.) requires exclusive access to a bot token. If two profiles try to use the same token simultaneously, the second gateway will fail to connect." / "If two profiles configure the same `(platform, token)`, the gateway logs an error naming both profiles and parks the **duplicate** adapter"
- Confidence: Verified
- Note for our fleet: our crew profiles use Slack platforms — each needs its own token; `--clone-channels` is refused while the multiplexer serves the source (profiles page).

## D. state.db / SQLite concurrency ("two writers on one home", single-writer hazards)

**L2-13. Official position: many processes MAY share one profile's state.db through SQLite locking; what is forbidden is rewriting the store under a live writer.**
- Source: /docs/user-guide/session-storage-recovery — official-docs
- Quote: "Several Hermes processes can share that file safely — the gateway, the Desktop app, the dashboard, cron, and CLI commands all write through SQLite's own locking. One thing is not safe: **rewriting the store while another process is writing to it**."
- Confidence: Verified

**L2-14. Maintenance commands now refuse under a live writer; the refusal protects against exactly the multi-writer fleet failure.**
- Source: /docs/user-guide/session-storage-recovery ("Maintenance commands refuse while someone is writing") — official-docs
- Quote: "Running one of them under a live gateway is how a fleet of agents ends up in the refusal above, so they now check first and refuse while another process holds the database"
- Confidence: Verified

**L2-15. Real-world corroboration (user reports): multiple processes on ONE profile's state.db corrupt it or starve each other — including kanban workers on a single profile.**
- Sources: github.com/NousResearch/hermes-agent issues #73411, #110106, #103339, #139959 — github-issue
- Quotes: #73411: "state.db corruption from concurrent `hermes serve` + `gateway run` writers on the same default profile"; remedy applied: "leaving the gateway as the sole state.db writer". #110106: "When more than one tui_gateway.entry process is attached to the same Hermes profile, they repeatedly retire each other's state.db WAL generation ... the session dies silently mid-turn". #139959: "On a host where several Hermes processes share one state.db, a busy writer stops the session turn-lease refresher from renewing ... 8–12 concurrent dispatcher-spawned kanban workers per profile state.db".
- Confidence: Plausible (user-reported; consistent with the Verified docs guidance). #139959 is the closest documented analogue of our kanban-on-default incident.

**L2-16. MEMORY.md loss under concurrent instances sharing one profile (last-writer-wins) — the concrete failure mode behind L2-1/2.**
- Source: github.com/NousResearch/hermes-agent issue #85858 — github-issue
- Quote: "MEMORY.md lost under concurrent Hermes instances sharing one profile (frozen-snapshot + full-file rewrite = last-writer-wins)"
- Confidence: Plausible

## E. Cron / profile interaction pitfalls

**L2-17. Cloned cron jobs = double firing; Hermes therefore never clones cron jobs.**
- Source: /docs/user-guide/profiles ("Clone everything (`--clone-all`)") — official-docs
- Quote: "**Cron jobs are not cloned** either: they are scheduled work bound to the source profile and its delivery channel, and a clone that inherited them would run every job twice (two gateways, same job ids). The new profile starts with an empty `cron/`."
- Confidence: Verified

**L2-18. Messaging channels are never cloned either (token fight prevention), `--clone-channels` only with a warning.**
- Source: /docs/user-guide/profiles — official-docs
- Quote: "Every clone — `--clone`, `--clone-from`, `--clone-all`, and the dashboard / Desktop / TUI 'clone from profile' option — copies the source **without its messaging channels**: bot tokens and allowlists ..."
- Confidence: Verified

**L2-19. Cron is per-profile state with anti-double-fire machinery.**
- Source: /docs/user-guide/features/cron — official-docs
- Quote: "A file lock at `~/.hermes/cron/.tick.lock` prevents overlapping scheduler ticks from double-running the same job batch." Also: when the cron store "can't be written ... the scheduler does not run a job whose run it can't record. That prevents double fires after recovery."
- Confidence: Verified
- Related user report (Plausible): issue #145530 "Manual 'cron run' starts a second concurrent instance of a job that is already running".

**L2-20. Under the multiplexer, a named profile's cron ticks on the default gateway's scheduler (heartbeat diagnostics).**
- Source: /docs/user-guide/features/cron — official-docs
- Quote: "For a named profile served by the default-profile multiplexer, `hermes cron status` names that scheduler host and reports the named profile's own heartbeat health. Missing or stale heartbeats point to `hermes --profile default gateway restart`."
- Confidence: Verified
- Operational note: killing/restarting the default gateway affects every profile's cron fleet.

## F. Per-profile cost control

**L2-21. Model is per-profile config — the documented cost knob.**
- Source: /docs/user-guide/profiles ("Configuring profiles") — official-docs
- Quote: "**`config.yaml`** — model, provider, toolsets, all settings" ... `coder config set model.default anthropic/claude-sonnet-4`
- Confidence: Verified

**L2-22. Cron fleet gets its own model ladder, independent of the chat model: per-job pin → `cron.model` → main agent model.**
- Source: /docs/user-guide/features/cron — official-docs
- Quote: "**`cron.model` / `cron.model_provider`** — a cron-fleet default: every unpinned job runs on this model, independent of your chat model."
- Confidence: Verified

**L2-23. For cheap-model tasks the docs prefer delegation config over profile splits; model switches reset the prompt cache.**
- Source: /docs/reference/faq ("Using different models for different tasks") — official-docs
- Quote: "Hermes can route subagents to a different model automatically. Set this in `~/.hermes/config.yaml`: `delegation: model: ... provider: ...`" and warning: "Each `/model` switch resets the prompt cache ... prefer delegation (subagents get their own fresh context) or a new session over repeated back-and-forth switching."
- Confidence: Verified

## G. Security / isolation boundary of a profile split (hazards)

**L2-24. Profiles isolate STATE, not the filesystem — a split does NOT sandbox anything.**
- Source: /docs/user-guide/profiles ("Profiles vs workspaces vs sandboxing") — official-docs
- Quote: "A **sandbox** is what limits filesystem access. Profiles do **not** sandbox the agent. On the default `local` terminal backend, the agent still has the same filesystem access as your user account. A profile does not stop it from accessing folders outside the profile directory."
- Confidence: Verified
- Critical for our single-pod fleet: profile separation reduces state collisions, but any profile's agent can still write anywhere UID 10000 can.

**L2-25. Cross-profile write guards cover only four areas; reads across profiles are unguarded (user-verified).**
- Source: github.com/NousResearch/hermes-agent issue #10376 — github-issue
- Quote: "PROFILE_SCOPED_AREAS = (skills, plugins, cron, memories); classify_cross_profile_target() only classifies writes landing in those 4 areas of another profile." (Title: "Profile isolation is incomplete: --clone copies memory, and agents can read across profile boundaries")
- Confidence: Plausible

**L2-26. Security scope is per-profile: approvals, allow-all switches and credentials resolve in the routed profile's scope.**
- Source: /docs/user-guide/security + /docs/user-guide/multi-profile-gateways — official-docs
- Quotes: "`approvals.mode: off` covers every chat and cron job of that profile" / "In a multi-profile gateway a secondary profile sets `GATEWAY_ALLOW_ALL_USERS` in its own `.env`" / secret scope table: "stdio MCP child environment | Safe baseline + the profile's scoped values ... A name the profile lacks is absent from the child — no default-profile fallthrough"
- Confidence: Verified

**L2-27. The profile home is a code-execution trust boundary: gateway hooks load in-process from `<profile home>/hooks/` with the gateway's privileges; treat it like config.yaml.**
- Source: /docs/user-guide/security ("Trusted-by-placement extension points") — official-docs
- Quote: "the profile home is operator-owned configuration, and anyone who can write into it can already run code as you through `config.yaml` shell hooks or by editing `plugins.enabled`"
- Confidence: Verified

**L2-28. Many-profiles coupling hazard: ONE unparseable profile config.yaml fails the shared dependency-prep step of `hermes update` for the whole install; updates themselves are once-for-all-profiles with automatic skill sync (the official parity mechanism).**
- Source: /docs/user-guide/profiles ("Updating") + /docs/reference/faq — official-docs
- Quote: "A profile whose `config.yaml` does not parse (or whose `plugins` / `memory` sections have the wrong shape) fails that step for the whole install" and "`hermes update` pulls the latest code and reinstalls dependencies **once** (not per-profile). It then syncs updated skills to all profiles automatically."
- Confidence: Verified
- Speaks to our parity-drift cost: bundled skills stay in sync automatically; per-profile config/model drift is on the operator.

## H. Sharing a whole agent (profile distributions)

**L2-29. Distributions package a complete specialist agent as a git repo; credentials and user data are deliberately excluded.**
- Source: /docs/user-guide/profile-distributions — official-docs
- Quote: "A **profile distribution** packages a complete Hermes agent — personality, skills, cron jobs, MCP connections, config — as a git repository." / "**You want to share API keys alongside the agent.** `auth.json`, `.env` and the other credential stores ... are deliberately excluded from distributions."
- Confidence: Verified
- Fit note (Plausible inference): distributions target sharing an agent across people/machines — not our single-pod, single-operator split decision.

## I. Searched, found nothing (evidence of absence)

| Query / probe | Source types searched | Result |
|---|---|---|
| Full-page search "profile" on /docs/guides/tips | official-docs | 0 hits — tips page has no profile advice at all |
| "production deployment"/"checklist"/"least privilege" on /docs/user-guide/security | official-docs | No profile-related checklist item; 8 security layers are not profile-based |
| FAQ probe for "when should I create a profile" recommendation | official-docs | No such FAQ entry; closest is "How many profiles can I run?" (feasibility, not desirability) |
| web_search: `NousResearch hermes-agent github issue state.db WAL "another Hermes process" OR "two writers" OR concurrent write profile` | github-issue | Results found (used above) — but no official maintainer *best-practice doc* on multi-writer avoidance found; guidance exists only as page-level warnings |
| web_search: `NousResearch hermes-agent issue OR discussion "cron" duplicate firing cloned profile double` | github-issue, official-docs | No issue reporting cloned-job double firing after the "cron not cloned" guard; hits were per-job concurrency + UI aggregation issues (#145530, #51721) |
| Dedicated "profile best practices" page (any site search) | official-docs | Does not exist; best-practice material is scattered across tips/FAQ/security/multi-profile-gateways |
| Reddit/HN/X for multi-profile practice | reddit, blog | Not searched in this lane (deliberately L5's scope) |

## J. Lane verdict

Official docs DO document hazards of "everything on default" — but only two, both narrow and specific:
(1) two agent processes on one home corrupt memory/state (profiles page + FAQ, Verified, plus 4 corroborating issues),
(2) N processes hammering one profile's state.db under kanban/serve load (docs page + issues).
Everything else the docs recommend for work on one profile is mechanism choice (delegation, cron, personality switching), and the docs never tell a single-user operator to split the default profile by role. A profile split is officially FOR distinct agents (different purpose / different bot / different memory), not for organizing workload on one agent. Cost control is officially per-profile-config + cron model ladder + delegation, not profile proliferation. The strongest operational guidance for our fleet: keep profiles as separate homes with their own state.db (kills the two-writers and state-contention hazards), ride the single multiplexed default gateway (per-profile gateway processes are refused), and remember a profile split buys ZERO filesystem sandboxing.

Sub-question status from this lane's view: answered
