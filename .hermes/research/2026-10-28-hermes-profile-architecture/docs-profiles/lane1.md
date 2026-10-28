# Lane L1 — SQ1: What a Hermes profile officially isolates vs shares; purpose & lifecycle

Read (whole or complete relevant sections, web_extract; base https://hermes-agent.nousresearch.com):
/docs/user-guide/profiles · /docs/reference/profile-commands · /docs/user-guide/which-file-does-what ·
/docs/user-guide/sessions (profile/state.db sections, 84K page) · /docs/user-guide/configuration (profile-relevant
sections, 304K page) · /docs/reference/environment-variables (incl. truncated middle from saved file) ·
/docs/user-guide/remote-config · /docs/user-guide/managed-scope · /docs/developer-guide/multiplexing-gateway ·
/docs/developer-guide/config-backend. All ten starting URLs covered. No web_search needed (docs-first satisfied).

## Findings

### A. Definition & purpose

**F1.** A profile is a separate Hermes home directory with its own config.yaml, .env, SOUL.md, memories, sessions, skills, cron jobs and state database.
- Source: https://hermes-agent.nousresearch.com/docs/user-guide/profiles — official-docs
- Quote: "A profile is a separate Hermes home directory. Each profile gets its own directory containing its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions, skills, cron jobs, and state database."
- Tier: Verified

**F2.** Documented purpose: run separate agents for different purposes on one machine without mixing state.
- Source: /docs/user-guide/profiles — official-docs
- Quote: "Profiles let you run separate agents for different purposes — a coding assistant, a personal bot, a research agent — without mixing up Hermes state."
- Tier: Verified

**F3.** The official docs name the "two writers on one home" hazard as the exact problem profiles exist to prevent (directly relevant to our past kanban-on-default incident).
- Source: /docs/user-guide/profiles — official-docs
- Quote: "Never point two agent processes at the same profile (the same Hermes home). Both write memory automatically, and each loads the other's writes into its system prompt at session start — so two writers on one home compound each other's state ... Profiles exist exactly to prevent this; agents that need shared memory should use an external memory provider instead."
- Tier: Verified

**F4.** Empty-stub pitfall: only directories carrying an identity file count as profiles; bare stubs (e.g. from logging or cron) are ignored — explains our `/opt/data/profiles/default/` empty-stub anomaly as benign, not a profile.
- Source: /docs/user-guide/profiles — official-docs
- Quote: "Hermes recognises a directory under `~/.hermes/profiles/` as a profile only when it carries one of those identity files (`config.yaml`, `.env`, `SOUL.md`, `profile.yaml`, `auth.json`, `state.db`); a bare directory left behind by logging or cron is ignored by `profile list`, gateways and `-p`."
- Tier: Verified

**F5.** Terminology positions profile vs Bot vs subagent: Bots are profile-roster entries; a delegate_task subagent is a fresh conversation, explicitly NOT a profile.
- Source: /docs/user-guide/profiles — official-docs
- Quote: "Every Bot is a profile, but not every profile is a Bot" / "A separate conversation is different from a separate profile."
- Tier: Verified

**F6.** Profiles isolate Hermes state but do NOT sandbox the filesystem; workspace (terminal.cwd) is separate; `cwd: "."` means launch dir, not profile dir.
- Source: /docs/user-guide/profiles — official-docs
- Quote: "A **sandbox** is what limits filesystem access. Profiles do **not** sandbox the agent." / "On the default `local` terminal backend, the agent still has the same filesystem access as your user account."
- Tier: Verified

### B. The HERMES_HOME mechanism

**F7.** Isolation is implemented via HERMES_HOME; the alias wrapper exports it and everything resolves through get_hermes_home().
- Source: /docs/user-guide/profiles ("How it works") — official-docs
- Quote: "When you run `coder chat`, the wrapper script sets `HERMES_HOME=~/.hermes/profiles/coder` before launching hermes. Since 119+ files in the codebase resolve paths via `get_hermes_home()`, Hermes state automatically scopes to the profile's directory — config, sessions, memory, skills, state database, gateway PID, logs, and cron jobs."
- Tier: Verified

**F8.** HERMES_HOME resolution: literal `~`/`$VAR` expanded, defaults `~/.hermes` (POSIX), official Docker image uses `/opt/data`; "Profile/runtime context can select a more specific home." The default profile is simply `~/.hermes` itself.
- Source: /docs/reference/environment-variables + /docs/user-guide/profiles — official-docs
- Quote: "Defaults to `~/.hermes` on POSIX and `%LOCALAPPDATA%\hermes` on Windows; the official Docker image uses `/opt/data`." / "The default profile is simply `~/.hermes` itself. No migration needed."
- Tier: Verified

**F9.** HOME (OS user home) is deliberately NOT the profile boundary: host tool subprocesses keep the real HOME so git/ssh/gh keep working; profile data is isolated by HERMES_HOME only. Strict per-profile CLI config requires `terminal.home_mode: profile` (HOME={HERMES_HOME}/home, HERMES_REAL_HOME exposed).
- Source: /docs/user-guide/profiles + /docs/user-guide/configuration — official-docs
- Quote: "Profile data is isolated by `HERMES_HOME`, not by changing `HOME`." / "In that mode Hermes launches tool subprocesses with `HOME={HERMES_HOME}/home`."
- Tier: Verified
- Fleet note: on our single-pod Docker deploy, containers already use {HERMES_HOME}/home in auto mode; host home_mode is moot.

**F10.** Per-profile TMPDIR: every Hermes process gets TMPDIR/TMP/TEMP at `~/.hermes/cache/scratch` "(per profile)" — even scratch is profile-scoped.
- Source: /docs/user-guide/configuration — official-docs
- Quote: "every Hermes process (CLI, TUI, gateway, Desktop backend, cron) and every child it launches gets `TMPDIR`, `TMP` and `TEMP` pointed at **`~/.hermes/cache/scratch`** (per profile) at startup"
- Tier: Verified

### C. Per-profile files (incl. SOUL.md vs MEMORY.md vs USER.md vs AGENTS.md)

**F11.** Each profile owns its config trio; everything about model/provider/toolsets is per-profile.
- Source: /docs/user-guide/profiles — official-docs
- Quote: "Each profile has its own: **`config.yaml`** — model, provider, toolsets, all settings / **`.env`** — API keys, bot tokens / **`SOUL.md`** — personality and instructions"
- Tier: Verified

**F12.** Personality/memory file map: SOUL.md = agent identity, injected verbatim as prompt slot #1, lives in the profile home ("never the working directory"); USER.md (who you are) and MEMORY.md (what the agent learned) are agent-written into `memories/` of the profile home; AGENTS.md/.hermes.md are project context loaded from the working directory — not profile-scoped.
- Source: /docs/user-guide/which-file-does-what — official-docs
- Quote: SOUL.md: "`~/.hermes/SOUL.md` (or `$HERMES_HOME/SOUL.md` with a custom home) — never the working directory"; USER.md/MEMORY.md live in "`~/.hermes/memories/`"; AGENTS.md lives in "Project working directory + subdirectories". Memory is a "frozen snapshot captured once at session start".
- Tier: Verified
- Fleet note: with multiplexing the home shown is the routed profile's; our default SOUL.md belongs to default only.

**F13.** `profile.yaml` (identity file) carries `display_name` and the kanban routing `description`; `hermes profile describe` sets it (aux LLM auto-gen via `auxiliary.profile_describer`).
- Source: /docs/reference/profile-commands — official-docs
- Quote: "The description is consumed by the kanban orchestrator to route tasks based on what each profile is good at ... Persisted in `<profile_dir>/profile.yaml`"
- Tier: Verified

**F14.** Sessions: one state.db per profile; gateway session keys name the owning profile. Cross-profile state crossing is a known failure with an official repair command.
- Source: /docs/user-guide/sessions — official-docs
- Quote: "Every profile owns one `state.db`, and every gateway session key names the profile that owns the conversation (`agent:main:…` for the default profile, `agent:<name>:…` for a named one)." / "rows sitting in another profile's store | move (with all messages) to the owning profile's store" (`hermes sessions repair-profiles`)
- Tier: Verified

### D. What is SHARED across profiles

**F15.** Code install is shared once for all profiles; `hermes update` syncs bundled skills into every profile automatically (user-modified skills never overwritten).
- Source: /docs/user-guide/profiles — official-docs
- Quote: "`hermes update` pulls code once (shared) and syncs new bundled skills to **all** profiles automatically"
- Tier: Verified

**F16.** Parity hazard at update time: dependency preparation reads EVERY profile's config.yaml to compute the shared plugin set — one unparseable config breaks the whole install (config drift is not just cosmetic).
- Source: /docs/user-guide/profiles — official-docs
- Quote: "Dependency preparation reads every profile's `config.yaml` to compute the plugin set the shared environment must carry. A profile whose `config.yaml` does not parse ... fails that step for the whole install"
- Tier: Verified

**F17.** Plugin Python dependencies live in one shared environment (cloned plugins keep working "at the same revision" without reinstall); machine-scoped local-model runtime trees (`models/`, `runtimes/`, `node/`) are shared and re-fetched on demand.
- Source: /docs/user-guide/profiles — official-docs
- Quote: "Plugin Python dependencies live in the shared environment and are not reinstalled." / "the local-model runtime trees (`models/`, `runtimes/`, `node/` — downloaded weights and managed binaries, re-fetched on demand) are skipped too"
- Tier: Verified

**F18.** OAuth logins are root-shared (single-use refresh tokens make copies harmful); per-profile OAuth is opt-in via `hermes -p <name> auth add`.
- Source: /docs/user-guide/profiles — official-docs
- Quote: "The new profile keeps reading the login from the root `~/.hermes/auth.json`, and a token refresh performed inside any profile is written back to root, so all profiles stay signed in."
- Tier: Verified

**F19.** Under multiplexing, several things stay process-global by design: MCP discovery/tool registration (first profile to build an agent wins), `TERMINAL_*` env, built-in tool registry (plugin tools overlaid per profile), provider/capability registries, one HTTP listener/process lock owned by default.
- Source: /docs/developer-guide/multiplexing-gateway — official-docs (developer-guide)
- Quote: "MCP discovery and tool registration | Process-global; the first profile to build an agent wins the discovery slot." / "Terminal / sandbox env (`TERMINAL_*`) | Global by allowlist" / "Built-ins are process-global; plugin-registered tools are overlaid per profile via `hermes_home_key()`."
- Tier: Verified

**F20.** Multiplexed-gateway isolation contract: per-profile adapters, secrets, sessions, cron ticks; shared event loop, HTTP listener, process lock, status surface; hard constraint "profile A's turns must never observe profile B's state".
- Source: /docs/developer-guide/multiplexing-gateway — official-docs
- Quote: "the default profile plus every served named profile get their own adapters, secrets, sessions, and cron ticks, while sharing one event loop, one HTTP listener, one process lock, and one status surface."
- Tier: Verified

**F21.** Profiles are a configuration boundary, not an identity/authorization boundary.
- Source: /docs/developer-guide/multiplexing-gateway — official-docs
- Quote: "A profile is a configuration, not a person: the gateway trusts its transport and its routing table to decide which profile an event belongs to."
- Tier: Verified

**F22.** Secrets: each profile's `.env` + secret sources form a context-local scope; under multiplexing an unscoped secret read raises rather than leaking another profile's value; `${VAR}` in a profile's config.yaml resolves from that profile's own .env.
- Source: /docs/developer-guide/multiplexing-gateway + /docs/user-guide/configuration — official-docs
- Quote: "multiplexing **on**, no scope installed: **raises `UnscopedSecretError`** rather than silently reading the process environment" / "references in a profile's `config.yaml` resolve against **that profile's** `.env` (its secret scope), not the shared process environment"
- Tier: Verified

**F23.** Kanban is deliberately shared across profiles: board/db anchored at the shared Hermes root (parent of any active profile), with dispatcher-injected HERMES_KANBAN_DB/BOARD/WORKSPACES_ROOT so worker profiles converge on the dispatcher's board.
- Source: /docs/reference/environment-variables — official-docs
- Quote: "`HERMES_KANBAN_HOME` | Override the shared Hermes root that anchors the kanban board (db + workspaces + worker logs). Falls back to `get_default_hermes_root()` (the parent of any active profile)."
- Tier: Verified

**F24.** Docker sandbox containers are per-profile by label (`hermes-profile=<name>`; profile A's container invisible to profile B), with explicit cross-profile sharing only via `docker_shared_container_key`.
- Source: /docs/user-guide/configuration — official-docs
- Quote: "a container labeled `hermes-profile=work` is invisible to a Hermes process running under `hermes-profile=research`"
- Tier: Verified

### E. Lifecycle (create → use → rename → export → delete)

**F25.** Create: blank profile seeded with bundled skills; every profile auto-gets a command alias (`~/.local/bin/<name>` = `hermes -p <name>`); `-p` flag works in any position; `--no-skills` makes a zero-skill profile (`.no-bundled-skills` marker; `hermes skills opt-out` to toggle on existing profiles, incl. default).
- Source: /docs/user-guide/profiles + /docs/reference/profile-commands — official-docs
- Quote: "Creates a fresh profile with bundled skills seeded." / "The alias works with every hermes subcommand — it's just `hermes -p <name>` under the hood." / "`--no-skills` | Create an **empty** profile with zero bundled skills enabled."
- Tier: Verified

**F26.** `--clone` copies config.yaml, .env, SOUL.md, skills, curated memories (MEMORY.md/USER.md) and the active memory-provider's own config; sessions, state.db, cron "start empty". `--clone-all` adds plugins/memories but excludes per-profile history (state.db, backups/, state-snapshots/, checkpoints/) and NEVER cron jobs — a clone inheriting them "would run every job twice (two gateways, same job ids)".
- Source: /docs/user-guide/profiles — official-docs
- Quote: "**Cron jobs are not cloned** either: they are scheduled work bound to the source profile and its delivery channel, and a clone that inherited them would run every job twice"
- Tier: Verified

**F27.** Messaging channels are never cloned (bot tokens, allowlists, platforms sections, profile_routes, pairing stores stripped; opt-in `--clone-channels`, refused while a multiplexer serves the source) — "a bot can only belong to one profile".
- Source: /docs/user-guide/profiles — official-docs
- Quote: "Every clone — `--clone`, `--clone-from`, `--clone-all`, and the dashboard / Desktop / TUI 'clone from profile' option — copies the source **without its messaging channels**"
- Tier: Verified

**F28.** Runtime separation & collision guards: each profile runs its own gateway process with its own token; token locks block a second gateway on the same bot token (Telegram, Discord, Slack, WhatsApp, Signal); in the official Docker image per-profile gateways are s6-supervised (`/run/service/gateway-<name>/`).
- Source: /docs/user-guide/profiles — official-docs
- Quote: "If two profiles accidentally use the same bot token, the second gateway will be blocked with a clear error naming the conflicting profile."
- Tier: Verified

**F29.** Sticky default (`hermes profile use`, kubectl-context style) + safety: if the sticky profile's directory is hand-deleted, ordinary commands are refused rather than silently running on default.
- Source: /docs/user-guide/profiles — official-docs
- Quote: "If the sticky profile's directory is deleted by hand, Hermes refuses to run ordinary commands in the default profile instead, since they would read or write the wrong profile's state."
- Tier: Verified

**F30.** Rename/delete carry identity migration; retries are first-class commands.
- Source: /docs/reference/profile-commands — official-docs
- Quote: "The rename also migrates the profile's persisted session/routing identity — session keys (`agent:<old>:*`), `sessions.profile_name`, heartbeats, and routing/delivery rows — to the new name." / purge-identity: "`delivery_obligations` rows are marked `abandoned` rather than dropped"; delete "removes the profile's own `profiles/<name>/`, its `state.db` included".
- Tier: Verified

**F31.** Delete stops gateway, removes service + alias + all data (type name to confirm); the default profile (`~/.hermes`) cannot be deleted — `hermes uninstall` instead.
- Source: /docs/user-guide/profiles — official-docs
- Quote: "This stops the gateway, removes the systemd/launchd service, removes the command alias, and deletes all profile data." / "You cannot delete the default profile (`~/.hermes`)."
- Tier: Verified

**F32.** Export/import = portable tar.gz with credentials always excluded (`auth.json`, `.env`, other credential stores) and machine-specific `installs/`, `tools/`, `cache/` never portable; full-history backup = `hermes backup` (excludes the same machine-scoped trees).
- Source: /docs/reference/profile-commands + /docs/user-guide/profiles — official-docs
- Quote: "`auth.json`, `.env` and the other credential stores are always excluded" / "Export, import, and distribution install exclude `installs/`, `tools/`, and `cache/` at a profile's root."
- Tier: Verified

**F33.** Distributions = profile as git repo; `auth.json`/`.env` never distributed; user data (memories, sessions, auth, .env edits) preserved across install/update; `distribution_owned` scopes what updates may overwrite.
- Source: /docs/reference/profile-commands — official-docs
- Quote: "`auth.json` and `.env` are never part of a distribution — they stay on the installing user's machine." / "The recipient's user data (memories, sessions, auth, their own edits to `.env`) is always preserved across the initial install and subsequent updates."
- Tier: Verified

**F34.** The dashboard is machine-level and can manage ANY profile (config, keys, skills, MCP, model) via the profile switcher — no per-profile dashboard needed; "Set as active" there is only the sticky default for future CLI/gateway runs.
- Source: /docs/user-guide/profiles — official-docs
- Quote: "The web dashboard is a machine-level surface that can manage **any** profile's config, API keys, skills, MCPs, and model via the profile switcher"
- Tier: Verified

### F. Config layering around profiles

**F35.** Per-profile config selection: `HERMES_CONFIG_BACKEND` (env/.env only, never config.yaml itself) chooses `file` (local `<home>/config.yaml`) vs `remote` (fleet config plane); only `<home>/config.yaml` is "a user layer". Remote mode refuses file-tooling commands (config edit, profile clone/rename, backup/import).
- Source: /docs/developer-guide/config-backend + /docs/user-guide/remote-config — official-docs
- Quote: "Only `<home>/config.yaml` is a user layer." / "Remote config is for fleet deployments, for example Hermes Cloud. A single machine with one user should keep `config.yaml`."
- Tier: Verified

**F36.** Above the user layer sits the admin-managed scope `/etc/hermes` (config.yaml + .env), per-key immutable, wins over the user AND shell env — the fleet-pinning mechanism distinct from profiles.
- Source: /docs/user-guide/managed-scope — official-docs
- Quote: "it injects _specific immutable values_ on a per-key basis rather than locking the whole config" / "the values it specifies win over the user's `~/.hermes/config.yaml`, `~/.hermes/.env`, and even the shell environment — for exactly the keys it pins"
- Tier: Verified

**F37.** Multiplexed serving is a single chokepoint: default + every valid profile dir, optionally allowlisted; excluded profiles keep running their own standalone gateway; a malformed allowlist fails safe to default-only.
- Source: /docs/developer-guide/multiplexing-gateway — official-docs
- Quote: "`profiles_to_serve(multiplex, profile_allowlist)` ... is the single chokepoint for which profiles a multiplexer serves: default plus every valid profile directory, optionally filtered by allowlist. A malformed allowlist fails safe to default-only."
- Tier: Verified

## Searched, found nothing

- No web_search calls were needed for this lane — all ten starting URLs were extracted and read in full (or in complete profile-relevant sections for the two oversized pages). Queries/types listed below record absence within the docs read:
- "profile bloat" / "skill dilution" warning: NOT found on /docs/user-guide/profiles or /docs/reference/profile-commands (closest official affordances: `--no-skills` for "narrow orchestrator profiles or sandbox profiles that should not inherit the full skill catalog" and `--description` for orchestrator routing). Source types: official-docs.
- Dedicated empty-stub troubleshooting page: NOT found — the identity-files sentence in F4 is the only doc text covering it. Source types: official-docs.
- Canonical "profile directory layout" tree diagram: NOT found as such — layout is only enumerated in prose (F1, F7, F11–F14). Source types: official-docs.
- Docs recommendation of how many/which profiles to run ("when to split"): NOT found in any L1 page (recorded as absence; L2 owns this). Source types: official-docs.
- Explicit state.db cross-profile write-lock hazard page: NOT found in L1 pages; closest is `hermes sessions repair-profiles` (F14) and journal-mode docs. Source types: official-docs.

Sub-question status from this lane's view: answered
