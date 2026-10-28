# LANE L5 — Community practice: what REAL users do with multiple Hermes profiles (SQ5)

Collected 2026-10-28. Sources tried in docs-first order: official user-stories page
(https://hermes-agent.nousresearch.com/docs/user-stories, 395 community stories, full page
cached), GitHub issue/PR search of NousResearch/hermes-agent via the REST API, HN Algolia,
web search for r/hermesagent threads and blogs, two blog deep-dives. GitHub Discussions are
disabled on the repo (API returns 410). Tier meanings per brief: Verified = authoritative
source for this exact target (incl. maintainer statements); Plausible = sound user-reported
behavior, single instance; Speculative = weak/unofficial sourcing.

## A. Role splits people actually run

F1. Small companies split one Hermes box into role-scoped production profiles.
- Source: https://x.com/lecaj_/status/2100724076188709249 via official user-stories page — source type: official-docs (aggregated user report / X)
- Quote: "1 box, 1 gateway, 3 profiles. All split by role: ops, finance, and an approvals-only (for executive and large approvals). … Everything is in production."
- Tier: Plausible (user report, hosted on official page)

F2. A 17-person startup runs one profile per team on a single machine.
- Source: https://x.com/JacquelineSYC19/status/2100262432413528336 via official user-stories page — source type: official-docs (aggregated X)
- Quote: "It runs on a single physical machine in Germany, has a different personality for each team, and dreams at night. … Hermes BizOps handles the recurring operational work"
- Tier: Plausible

F3. An individual operator separates work, coaching and homelab into three profiles and explicitly recommends the practice.
- Source: https://www.reddit.com/r/hermesagent/comments/1urri8w/ via official user-stories page — source type: reddit
- Quote: "Profiles are a game changer. Use them. My default profile is for work. It's connected to my second brain in Obsidian and synced through Git."
- Tier: Plausible

F4. The dominant multi-profile pattern is a Chief-of-Staff/router profile delegating to specialist profiles whose roles were hand-designed.
- Source: https://www.reddit.com/r/hermesagent/comments/1vyd3wk/ via official user-stories page — source type: reddit
- Quote: "I went with multi profile setup, Nyx … is my Hermes \"Chief of Staff.\" Its whole job is to figure out what I want, delegate to the specialist i spent days working out their roles and rules."
- Tier: Plausible

F5. Community consensus pattern named "orchestrator + specialists"; recommended on-ramp is one extra profile + own SOUL.md + Kanban board.
- Source: https://www.reddit.com/r/hermesagent/comments/1ucmvi8/ (Multi-Agent & Profiles Megathread, June 2026) — source type: reddit
- Quote: "The community is actively graduating from single-agent setups to agent teams: orchestrator + specialists pattern, shared boards with self-management … Start simple: create one extra profile, give it a different SOUL.md, connect it to a Kanban board."
- Tier: Plausible

F6. Persistent-orchestrator pattern: one profile as single point of contact that drives the others per-project.
- Source: https://www.reddit.com/r/hermesagent/comments/1ss20t0/ — source type: reddit
- Quote: "a persistent orchestrator – one Hermes profile that's your single point of contact – that talks to your other Hermes profiles like a conductor talking to musicians. Each specialized agent has its own memory, runs in its own session"
- Tier: Plausible

F7. A community workaround replaces delegate_task with CLI-launched profiles, enforced from the orchestrator's SOUL.md.
- Source: https://www.reddit.com/r/hermesagent/comments/1tla8oi/ — source type: reddit
- Quote: "Add this to your SOUL.md of the main agent - that enforces the use of profiles instead of delegate_task … Delegation is done via: `hermes -p <profile> chat -q \"prompt\"` Do NOT use `delegate_task`."
- Tier: Plausible

F8. Users skip the default profile entirely and create a profile per role/project, using default only as router; shared memory provider bridges profiles.
- Source: https://www.reddit.com/r/hermesagent/comments/1ughn02/ — source type: reddit
- Quote: "the best way is to have the default profile as a router and use multiple primary profiles … I actually dont even use the default hermes profile but instead create profiles for the different types of roles or projects that i am working on … you can use the same hindsight memory"
- Tier: Plausible

F9. Platform-per-profile split: one Discord server per profile.
- Source: https://www.reddit.com/r/hermesagent/comments/1solv8v/ — source type: reddit
- Quote: "I use multiple discord servers with different channels and topics to connect with, each discord server gets it own Hermes profile."
- Tier: Plausible

F10. Per-person isolation inside a family: a purpose-built profile for a child instead of sharing the operator's agent.
- Source: https://x.com/trevin/status/2090598635029598224 via official user-stories page — source type: official-docs (aggregated X)
- Quote: "I didn't want to hand her the same general-purpose agent I use. … So I built her a separate Hermes profile from scratch."
- Tier: Plausible

F11. Agency model: one fully isolated profile per client (own SOUL.md, memory, cron) sold as recurring service.
- Source: https://x.com/IBuzovskyi/status/2060773706574479754 via official user-stories page — source type: official-docs (aggregated X)
- Quote: "one Hermes profile per client, fully isolated — each gets their own SOUL.md, memory, cron. Charge $497/month per client"
- Tier: Plausible

F12. Team-shared gateway with per-role capability scoping instead of separate profiles for everyone.
- Source: https://x.com/MichaelVersluis/status/2100811955309084978 via official user-stories page — source type: official-docs (aggregated X)
- Quote: "One Hermes gateway runs 24/7 on dedicated hardware connected to Telegram. … Sales/Retention: Scoped strictly to their own leads, CRM deals, and tasks (no financial/commissions or infrastructure access)."
- Tier: Plausible

F13. Project-per-sub-profile operating system: main agent = Chief of Staff, every project channel gets its own sub-profile with own memory.
- Source: https://github.com/teknium1/nous-discord-archive/blob/main/archives/community-projects-showcase/1496117910287024159-Running-Hermes-as-a-Hardcore-Project-Operating-System.txt via user-stories page — source type: blog (Discord archive)
- Quote: "My 'main agent' is my 'Chief of Staff' who has his own memory cross-project/workflow. Every 'project' (1 project = 1 Slack channel) has its own agent sub-profile with its own memory."
- Tier: Plausible

F14. Company-brain setup runs on a dedicated profile of one instance (low cost).
- Source: https://indiehackers.com/post/i-built-a-company-brain-for-my-startup-free-template-included-cd50ee8ef1 via official user-stories page — source type: blog (Indie Hackers)
- Quote: "The stack: a Hermes Agent instance with a dedicated profile"
- Tier: Plausible

F15. Enterprise-scale answer is infrastructure isolation, not profile isolation: one always-on agent per employee in its own k8s namespace.
- Source: https://engineering.razorpay.com/running-hermes-at-razorpay-a-network-isolated-self-improving-second-brain-for-every-employee-f91d56bea3f1 — source type: blog (vendor engineering blog)
- Quote: "Every one runs in its own isolated Kubernetes namespace, with its own encrypted storage, its own cloud identity, and its own network policy. … Isolation is a property of the infrastructure, not the application."
- Tier: Plausible (single-company report; relevant contrast: profile = app-level isolation, they chose infra-level)

## B. Equipping choices (tools/skills per profile), community view

F16. Security-motivated thin specialist profile: public-facing bot gets its own profile + gateway + number with a minimal MCP tool surface.
- Source: https://blog.technodrone.cloud/2026/09/family-budget-whatsapp-bot.html — source type: blog
- Quote: "The budget bot got its own Hermes profile, its own gateway and its own WhatsApp number. Its WhatsApp side has exactly nine budget tools, exposed over MCP. No shell. No files. No browser. No memory."
- Tier: Plausible

F17. Community principle behind thin specialists: minimize blast radius; the main (power-user) profile must not be exposed to untrusted channels.
- Source: https://blog.technodrone.cloud/2026/09/family-budget-whatsapp-bot.html — source type: blog
- Quote: "My main Hermes assistant is a power user. It has a terminal, it can run code, it has a browser. Do I want anyone's WhatsApp messages going to an agent that can run shell commands on my Mac? Hell no! … The smallest blast radius is a tool that doesn't exist."
- Tier: Plausible

F18. Role authority should be enforced structurally (toolsets), not by prompt — praised in the community's flagship role-team installer.
- Source: https://www.reddit.com/r/hermesagent/comments/1uxnr3u/ via official user-stories page — source type: reddit
- Quote: "You run it on a fresh Hermes install and you get 8 specialist profiles plus the default profile acting as CTO … authority is enforced by toolset restrictions, not just system prompt instructions."
- Tier: Plausible

F19. Community explicitly warns against accumulating everything on the default profile.
- Source: https://www.reddit.com/r/hermesagent/comments/1t29ogw/ via official user-stories page — source type: reddit
- Quote: "Don't turn the default profile into a giant backpack full of every skill, every tool, every instruction."
- Tier: Plausible

F20. Skill-list size on a profile is a real context cost; users file FRs for lazy loading/routing.
- Source: https://github.com/NousResearch/hermes-agent/issues/22620 — source type: github-issue
- Quote: "Skill list bloat causes massive context window inflation — need vector-based skill routing or lazy loading"
- Tier: Plausible

F21. Profile-parity mechanics can multiply skill payload storage: bundled skill sync copies skill-local .venv dirs into every profile.
- Source: https://github.com/NousResearch/hermes-agent/issues/137905 — source type: github-issue
- Quote: "A skill that creates its own venv … gets that venv copied into every profile at sync — 8 profiles × ~600 MB ≈ 5.4 GB, and it re-syncs after each update."
- Tier: Plausible

F22. Kanban worker/reviewer profiles want per-profile structural tool exclusions; today fences are advisory or global.
- Source: https://github.com/NousResearch/hermes-agent/issues/126923 — source type: github-issue
- Quote: "a reviewer profile must be read-only on the board; today the only fences are advisory (write-check after the fact) or global."
- Tier: Plausible

## C. Maintainer statements (Verified-ish per brief)

F23. Maintainer (teknium1, COLLABORATOR) codified the profile-vs-topic boundary in a docs FAQ PR, responding to repeated community confusion ("Confused about bots, profiles and telegram" on r/hermesagent): a profile isolates the agent, a topic only isolates the session.
- Source: https://github.com/NousResearch/hermes-agent/pull/122979 (PR body; open, docs FAQ) — source type: github-issue (maintainer PR)
- Quote: "a Telegram topic … is its own **session**; memory, skills, `SOUL.md`, cron, credentials, model and bot token stay shared. A profile isolates the **agent** (own memory, skills, SOUL, cron, model/credentials) and needs its own bot token."
- Tier: Verified (maintainer statement of intended semantics)

F24. Community reviewer of that FAQ asks for precision: profile "heaviness" (skill/memory context riding along) is not guaranteed — focused profiles reduce context "can", not "do".
- Source: https://github.com/NousResearch/hermes-agent/pull/122979 (comment by kvnloo) — source type: github-issue
- Quote: "a broad profile can carry more skill/memory context into its chats, so focused profiles can reduce unrelated context and keep memory boundaries clearer."
- Tier: Plausible

F25. Maintainer-side framing of Bot Mode economics (no maintainer reply yet, but the issue frames current behavior): one Bot = one profile = a full Hermes home.
- Source: https://github.com/NousResearch/hermes-agent/issues/138415 — source type: github-issue (user report of product behavior)
- Quote: "Bot Mode currently treats one Bot = one profile = a full Hermes home (`SOUL.md`, `memories/`, skills, `.env`, `state.db`, cron). … Mapping each catalog role onto a Hermes profile would mean hundreds of full homes."
- Tier: Plausible

## D. Multi-profile pitfalls reported by users (GitHub issues)

F26. Multiplex-routing pitfall: satellite profile's cron output is delivered by the root profile's bot — identity leak for multi-brand setups.
- Source: https://github.com/NousResearch/hermes-agent/issues/144974 — source type: github-issue
- Quote: "the satellite profile's private scheduled output is posted under another persona's bot, and the satellite profile's own bot never sends it. … For multi-tenant / multi-brand setups this is an identity leak"
- Tier: Plausible

F27. Cron double-firing pitfall across profiles: a standalone profile's gateway cron ticker also fires the HOST profile's jobs when the host gateway is down (fix PR open).
- Source: https://github.com/NousResearch/hermes-agent/pull/136018 — source type: github-issue (PR by community user)
- Quote: "fires the host's jobs (the stopped host's cron keeps firing), … races the other standalone gateways for each store's `cron/.tick.lock`."
- Tier: Plausible

F28. One-container, one-gateway-per-profile pitfall (directly relevant to single-pod fleets): profile gateways fight over token/webhook port and SIGTERM each other's children, killing cron mid-run.
- Source: https://github.com/NousResearch/hermes-agent/issues/88521 — source type: github-issue
- Quote: "These gateways constantly compete for the Telegram bot token and webhook port (8644), restarting each other in an endless loop … ~50% of daily cron runs are killed."
- Tier: Plausible

F29. Desktop profile-switch kills user-managed per-profile gateways; users want parallel per-profile gateways as first-class.
- Source: https://github.com/NousResearch/hermes-agent/issues/125394 — source type: github-issue
- Quote: "Users who run one gateway per profile … cannot switch profiles in the desktop app without their profile gateways being killed."
- Tier: Plausible

F30. Shared-home concurrency hazard: multiple Hermes processes writing the same SQLite stores surface as user-visible turn aborts and cron failures; sessions split confusingly between root and per-profile state.db.
- Source: https://github.com/NousResearch/hermes-agent/issues/140622 and https://github.com/NousResearch/hermes-agent/issues/81888 — source type: github-issue
- Quote: "`database is locked` — 67 occurrences … 4 user-visible turn aborts with the \"session storage was busy\" message"; "sessions live in both root `state.db` (29 sessions) and per-profile `profiles/<name>/state.db` (14 sessions) … No visible hierarchy"
- Tier: Plausible

F31. Profile-parity drift is a documented operational cost: provider capability silently diverges per profile (profile-local .env wins), and there is no supported "share providers across profiles" mechanism.
- Source: https://github.com/NousResearch/hermes-agent/issues/91572 — source type: github-issue
- Quote: "Stale per-profile key shadows the good one — `reviewer` profile had an old invalid `DEEPSEEK_API_KEY` in its own `.env`; every DeepSeek call 401'd while `default` worked. … There is currently no supported way to say \"all my profiles share the same model providers\" — only point-in-time copying."
- Tier: Plausible

F32. Same plugin installed in multiple profile homes breaks `hermes update` (uv workspace rejects duplicate members).
- Source: https://github.com/NousResearch/hermes-agent/issues/135306 (also #125252) — source type: github-issue
- Quote: "error: Two workspace members are both named `hermes-telemetry`"
- Tier: Plausible

F33. Concurrent multi-profile use has cross-profile locking gaps: tool updater re-prompts installs (no cross-profile install lock).
- Source: https://github.com/NousResearch/hermes-agent/issues/144784 — source type: github-issue
- Quote: "10+ download prompts for the same package (ripgrep 15.2.0) within a few minutes" (when multiple agent profiles run concurrently)
- Tier: Plausible

F34. Profiles share almost nothing by design; users request a shared workspace tier for skills/memory/files across profiles.
- Source: https://github.com/NousResearch/hermes-agent/issues/56701 — source type: github-issue
- Quote: "Multiple Hermes profiles on the same machine are fully isolated. There's no way to share data, skills, or memory between them without `cross_profile=True` guards or manually copying files."
- Tier: Plausible

F35. Multiple kanban boards assigning different worker profiles to one single-model local provider livelock (models unload each other forever).
- Source: https://github.com/NousResearch/hermes-agent/issues/141445 — source type: github-issue
- Quote: "the other board retries, sends load model, nothing gets done, just flip flops endlessly."
- Tier: Plausible

F36. Per-profile secrets scoping has holes under shared routing: non-default-profile desktop chats miss that profile's 1Password env.
- Source: https://github.com/NousResearch/hermes-agent/issues/140173 — source type: github-issue
- Quote: "chats for non-default profiles routed via `primary-shared` don't get that profile's `secrets.onepassword.env`"
- Tier: Plausible

F37. Community-built profile-sharing ecosystem exists because there is no official profile registry: ClusterMob registry with security scanning.
- Source: https://news.ycombinator.com/item?id=50197497 (Show HN by -k_sze) — source type: blog (HN submission text)
- Quote: "there is no official registry, no central mechanism for profile discovery. So I set out to build ClusterMob, a community registry of Hermes profiles and profile packs."
- Tier: Plausible

F38. Third-party (unofficial) guides echo the split-by-trust-level advice; treat as market echo, not authority.
- Source: https://hermes-agent.ai/blog/hermes-agent-profiles-guide — source type: vendor-community-page (unofficial third-party site, NOT Nous; domain mimics official)
- Quote: "A separate profile lets each bot have its own token, memory, skills, allowed tools, and gateway configuration, which is safer than sharing one profile across multiple trust levels."
- Tier: Speculative (unofficial site; consistent with F16/F23)

## E. Cross-cutting observations

F39. Users reuse profiles as named personas wired to boards: the Kanban board pulls identity from each profile's SOUL.md.
- Source: https://www.reddit.com/r/hermesagent/comments/1ubz5h6/ via official user-stories page — source type: reddit
- Quote: "Built a Kanban board instead. … The board reads `SOUL.md` from each profile and pulls the name + description."
- Tier: Plausible

F40. Community tooling is emerging around per-profile observability (one usage DB per profile), implying profiles are treated as separate cost/security domains.
- Source: via official user-stories page (plugin tile) — source type: official-docs (aggregated community post)
- Quote: "records every tool call and every LLM API call into a local SQLite database (one DB per profile), with five ready-to-go Grafana dashboards bundled."
- Tier: Plausible

## Searched, found nothing (evidence of absence)

- GitHub Discussions of NousResearch/hermes-agent: channel does not exist — REST API returns 410 "Discussions are disabled for this repo" (github source type). No discussion-format evidence available.
- Exact phrase "skill dilution": no GitHub issue titled/named that; adjacent evidence is "context window inflation" (#22620) and SKILL.md bloat issues (#130532, #67582). (GitHub search, github-issue)
- Exact phrase "two writers" / "two writers on one home": no GitHub issue with that framing; nearest are the state.db lock-contention issues (#140622, #139959). (GitHub search, github-issue)
- Exact phrase "profile bloat": no issue under that name; bloat evidence instead found under skill-sync duplication (#137905). (GitHub search, github-issue)
- "cron cloned = double firing": no issue describing cron jobs double-firing from cloned profiles; found the adjacent standalone-ticker cross-firing bug (#136018) and manual-run concurrency bug (#145530). (GitHub search, github-issue)
- Direct Reddit thread bodies: fetch blocked (old.reddit login wall; .json endpoint returns non-JSON). Quotes above come from search-result snippets and the official user-stories page, both of which quote the same threads. (reddit source type, unavailable)
- X/Twitter native search: no tool available; all X evidence routed through the 85 X tiles curated on the official user-stories page. (x/twitter source type, unavailable)
- HN: story search for "hermes agent profile" found no Ask HN/Show HN dedicated to multi-profile practice beyond ClusterMob (F37) and the Kanban launch post; no profile-specific comments in the Kanban HN thread. (hn source type)

Sub-question status from this lane's view: answered
