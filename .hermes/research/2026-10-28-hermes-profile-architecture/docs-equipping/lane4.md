# Lane L4 — How a profile is officially equipped (SQ4)

Sub-question: which settings are per-profile, and is there documented guidance on a minimal per-role toolset/skill surface?
Method: docs-first (official docs pages whole; llms-full.txt grep for exact vocabulary). All URLs under `https://hermes-agent.nousresearch.com`.

## A. Toolsets — the per-platform/per-profile tool surface

1. **Claim:** Toolsets are the official primary mechanism for restricting which tools an agent gets, at platform, session, or task granularity.
   **Source:** /docs/reference/toolsets-reference (official-docs)
   **Quote:** "Toolsets are named bundles of tools that control what the agent can do. They're the primary mechanism for configuring tool availability per platform, per session, or per task."
   **Tier:** Verified

2. **Claim:** Toolsets come in exactly three kinds — core, composite, platform (MCP/plugin/custom are dynamic additions, see #10–11).
   **Source:** /docs/reference/toolsets-reference (official-docs)
   **Quote:** "Core — A single logical group of related tools … Composite — Combines multiple core toolsets for a common scenario … Platform — A complete tool configuration for a specific deployment context"
   **Tier:** Verified

3. **Claim:** Per-platform tool selection is saved per profile in its `config.yaml` (`platform_toolsets.<platform>`), and `agent.disabled_toolsets` overrides everything.
   **Source:** /docs/user-guide/features/kanban via llms-full.txt (official-docs)
   **Quote:** "Each platform has its own selection under `platform_toolsets.<platform>` in `config.yaml`; the toolset is also a checkbox in `hermes tools` and the dashboard. … `agent.disabled_toolsets` remains authoritative."
   **Tier:** Verified

4. **Claim:** `agent.disabled_toolsets` is the documented single switch to strip a toolset everywhere in one profile, applied after per-platform config.
   **Source:** /docs/user-guide/configuration (official-docs)
   **Quote:** "This applies after per-platform tool config (`platform_toolsets` written by `hermes tools`), so a toolset listed here is always removed — even if a platform's saved config still lists it."
   **Tier:** Verified

5. **Claim:** `hermes tools` toggles individual tools per platform (finer than toolsets) and the selection persists to the profile's config.yaml.
   **Source:** /docs/reference/toolsets-reference (official-docs)
   **Quote:** "This operates at the tool level (finer than toolsets) and persists to `config.yaml`. Disabled tools are filtered out even if their toolset is enabled."
   **Tier:** Verified

6. **Claim:** Built-in platform toolsets are already documented minimal specialist surfaces: the API-server preset drops interactive tools, and webhook runs get only a read-only safe subset.
   **Source:** /docs/reference/toolsets-reference (official-docs)
   **Quote:** "hermes-api-server | Drops `clarify`, `text_to_speech`, `computer_use`, and the kanban tools. Keeps everything else — suitable for programmatic access where user interaction isn't possible." / "hermes-webhook | Restricted safe subset — only `web_search`, `web_extract`, `vision_analyze`, and `clarify`. Webhook-triggered runs get no terminal, file, or browser access."
   **Tier:** Verified

7. **Claim:** The kanban toolset is deliberately opt-in per profile/platform and is not granted by the `all` wildcard — a role-safety rule for worker vs orchestrator equipping.
   **Source:** /docs/reference/toolsets-reference (official-docs)
   **Quote:** "`all`/`*` does **not** enable kanban; you must list `kanban` explicitly (or be a dispatcher-spawned worker with `HERMES_KANBAN_TASK` set). Kanban tools mutate shared board state, so they stay off by default even under `all`."
   **Tier:** Verified

8. **Claim:** Docs encode a role convention: worker profiles don't route, orchestrator profiles don't implement.
   **Source:** /docs/user-guide/features/kanban via llms-full.txt (official-docs)
   **Quote:** "the convention (encoded in the auto-injected kanban guidance) is that worker profiles don't fan out or route unrelated work, and orchestrator profiles don't execute implementation work."
   **Tier:** Verified

9. **Claim:** Custom toolsets let a profile define its own named bundles in config.yaml.
   **Source:** /docs/reference/toolsets-reference (official-docs)
   **Quote:** "Define custom toolsets in `config.yaml` to create project-specific bundles"
   **Tier:** Verified

10. **Claim:** Every configured MCP server and every plugin generates a referenceable toolset (`mcp-<server>`, plugin toolsets), equip-able like built-ins.
    **Source:** /docs/reference/toolsets-reference (official-docs)
    **Quote:** "Each configured MCP server generates a `mcp-<server>` toolset at runtime." / "Plugins can register their own toolsets via `ctx.register_tool()` during plugin initialization. These appear alongside built-in toolsets and can be enabled/disabled the same way."
    **Tier:** Verified

11. **Claim:** Blank Slate is the docs' explicit minimal-agent baseline — the documented model for a minimal per-role surface.
    **Source:** /docs/quickstart (llms-full.txt "Hermes Agent Quickstart") (official-docs)
    **Quote:** "everything starts **off** except the bare minimum needed to run an agent: **provider & model, the File Operations toolset, and the Terminal toolset**. No web, browser, code execution, vision, memory, delegation, cron, skills, plugins, or MCP servers" + "Blank Slate writes an explicit `platform_toolsets.cli` list plus `agent.disabled_toolsets`, so nothing you didn't choose ever loads — not even after `hermes update`."
    **Tier:** Verified

12. **Claim:** The docs justify narrow per-task toolsets on cost grounds — minimal toolsets are official guidance for cron specialists, which run with no chat platform.
    **Source:** /docs/user-guide/features/cron via llms-full.txt (official-docs)
    **Quote:** "Cron runs each job in a fresh agent session with no chat platform attached. By default the cron agent gets the toolset you configured for the `cron` platform in `hermes tools` — not the CLI default, not everything under the sun." + "This matters for cost control: carrying `browser`, `delegation` into every tiny 'fetch news' job bloats the tool-schema prompt on every LLM call."
    **Tier:** Verified

13. **Claim:** Webhook routes can carry their own per-route toolsets, editable only by hand so agents cannot self-grant tools.
    **Source:** /docs/user-guide/features/webhooks via llms-full.txt (official-docs)
    **Quote:** "List of toolset keys … that **replaces** the platform-level webhook toolset for runs triggered by this route only. Manual config edit only — not settable via `hermes webhook subscribe`, so agent-created subscriptions cannot self-grant elevated tools."
    **Tier:** Verified

## B. Model / provider per profile

14. **Claim:** Model and provider are per-profile settings in the profile's own config.yaml, and the docs actively recommend splitting expensive vs cheap models across orchestrator and worker profiles.
    **Source:** /docs/user-guide/features/kanban (official-docs)
    **Quote:** "Run your orchestrator/dispatcher profile on a frontier model and point worker profiles at inexpensive models. Each profile has its own `config.yaml` under `~/.hermes/profiles/<name>/`, and the dispatcher injects the profile-scoped `HERMES_HOME` when it spawns `hermes -p <assignee>`, so each worker reads its own profile's model settings"
    **Tier:** Verified

15. **Claim:** Individual kanban tasks can override the worker profile's model without editing the profile.
    **Source:** /docs/user-guide/features/kanban (official-docs)
    **Quote:** "pin just that task back to a stronger model with the per-task model override (`--model`/`--provider` at create time, `hermes kanban set-model` later, or the dashboard's model dropdown) — no profile edits needed."
    **Tier:** Verified

16. **Claim:** `model_overrides` in the official docs is per-config (hence per-profile) model *metadata* correction (context window, vision/reasoning flags, output limit) under a provider, not a per-role model switch; aux tasks have their own per-profile model slots (`auxiliary.<task>`).
    **Source:** /docs/integrations/providers + /docs/user-guide/configuration (official-docs)
    **Quote:** "A `model_overrides` entry that only corrects metadata (for example `context_window`) for a model the catalog does not know leaves vision and reasoning capability and the output-token limit **unknown**" / "override the slot to pin a specific provider + model for the review pass instead" (auxiliary.curator)
    **Tier:** Verified for what the docs define; our crew profiles' `model_overrides` usage is plugin-level behavior, not core documented vocabulary (Plausible as a mapping).

17. **Claim:** In a multiplexed gateway, a profile's config.yaml `${VAR}` references (model keys, MCP tokens) resolve against that profile's own `.env` — secret scope is per profile.
    **Source:** /docs/user-guide/configuration (official-docs)
    **Quote:** "references in a profile's `config.yaml` resolve against **that profile's** `.env` (its secret scope), not the shared process environment — a `${MATRIX_ACCESS_TOKEN}` in profile B stays unresolved … unless B defines the variable itself."
    **Tier:** Verified

## C. Skills per profile

18. **Claim:** Skills are profile-local: each profile is seeded with the bundled catalog and keeps its own manifest/reset state.
    **Source:** /docs/user-guide/features/skills (official-docs)
    **Quote:** "By default every profile is seeded with the bundled skill catalog, and each `hermes update` adds any newly bundled skills." / "Each profile has its own `.bundled_manifest` under its own `HERMES_HOME`, so `hermes -p coder skills reset <name>` only affects that profile."
    **Tier:** Verified

19. **Claim:** A profile can be created and kept skill-free (minimal specialist skill surface) via `--no-skills` / opt-out marker.
    **Source:** /docs/user-guide/features/skills (official-docs)
    **Quote:** "**At profile-create time** (named profiles): hermes profile create research --no-skills" + "All of these paths write a `.no-bundled-skills` marker into the profile directory. While the marker is present, the installer, `hermes update`, and any skill sync all skip bundled-skill seeding for that profile."
    **Tier:** Verified

20. **Claim:** Hub/catalog installs land in one chosen profile ("Install to"), not machine-wide.
    **Source:** /docs/reference/toolsets-reference + /docs/user-guide/features/plugin-catalog (official-docs)
    **Quote:** "Search the plugin catalog and skills hub, and install items through the approval card into this chat's profile." / "Each row installs into your `default` profile only when you click Install, at the same reviewed commit this page describes."
    **Tier:** Verified

21. **Claim:** The docs explicitly warn that an unmaintained, overgrown skill listing pollutes the catalog and wastes tokens — the documented bloat rationale (curator is the countermeasure, run per profile).
    **Source:** /docs/user-guide/features/curator (official-docs)
    **Quote:** "Without maintenance, you end up with dozens of narrow near-duplicates that pollute the catalog and waste tokens." + "The timer services its backend's profile." + "For one profile only: edit `~/.hermes/config.yaml` (or the active profile's config) and set `curator.enabled: false`."
    **Tier:** Verified

22. **Claim:** The skill listing cost is bounded by progressive disclosure (~3k tokens for the whole list), which softens but does not remove per-profile listing bloat.
    **Source:** /docs/user-guide/features/skills (official-docs)
    **Quote:** "Level 0: skills_list() → [{name, description, category}, ...] (~3k tokens) … The agent only loads the full skill content when it actually needs it."
    **Tier:** Verified

23. **Claim:** Skills can additionally be restricted per platform (not just per profile), e.g. keeping dev skills off Telegram.
    **Source:** /docs/guides/work-with-skills (official-docs)
    **Quote:** "This opens an interactive TUI where you can enable or disable skills per platform (CLI, Telegram, Discord, etc.). Useful when you want certain skills only available in specific contexts — for example, keeping development skills off Telegram."
    **Tier:** Verified

24. **Claim:** Agent-created skills default to the profile-local dir; `skills.create_dir` (plus external_dirs, highest-precedence project skills) is the documented way to share or redirect skill storage across a fleet.
    **Source:** /docs/user-guide/features/skills (official-docs)
    **Quote:** "By default the agent writes new skills to the profile-local `~/.hermes/skills/`. If you want agent-created skills to land somewhere else — a shared 'brain' directory, a git-tracked repo, or a fleet-wide skills volume — set `create_dir` under the `skills` section"
    **Tier:** Verified

## D. MCP servers per profile

25. **Claim:** MCP servers are configured in the profile's own config.yaml `mcp_servers:` block with per-server tool include/exclude filtering (include wins over exclude, exact-name/glob semantics on original tool names).
    **Source:** /docs/reference/mcp-config-reference (official-docs)
    **Quote:** "If `include` is set, only those server-native MCP tools are registered." / "If both are set, `include` wins."
    **Tier:** Verified

26. **Claim:** MCP equipping has per-server security knobs that gate writes and spend: `trust: untrusted` forces approval per write-capable call; costed tools have a per-chat spend limit that hard-refuses where nobody can answer (cron, chat -q).
    **Source:** /docs/reference/mcp-config-reference (official-docs)
    **Quote:** "On an `untrusted` server, every write-capable tool call (any tool without a `readOnlyHint: true` annotation) requires user approval through the standard approval surface before it runs." / "A costed call that would take the chat past it asks first, even on a `trust: full` server, and is refused where nobody can answer (cron, `chat -q`)."
    **Tier:** Verified

## E. Plugins per profile

27. **Claim:** Plugin enable/disable state lives in each profile's config.yaml (`plugins.enabled`/`plugins.disabled`) and toggling a plugin also syncs its toolset in and out of the saved platform_toolsets lists.
    **Source:** /docs/user-guide/features/plugins (official-docs)
    **Quote:** "If you saved a tool selection (`hermes tools`, so `platform_toolsets` lists toolsets explicitly), disabling a plugin also takes its toolset out of those saved lists, and enabling it puts the toolset back."
    **Tier:** Verified

28. **Claim:** Plugin installs (catalog, git, hand-installed) are recorded per profile, including pinned revisions.
    **Source:** /docs/user-guide/features/plugins (official-docs)
    **Quote:** "Hermes checks out the commit detached, verifies that `HEAD` exactly matches the requested SHA, and records the canonical source, installed revision, and pin status in the current profile."
    **Tier:** Verified

29. **Claim:** Plugin Python dependencies are shared-environment and computed as the union across all profiles (parity cost is real at the dependency layer); plugin *code* isolation is per profile (plugin host = one process per profile).
    **Source:** /docs/user-guide/features/plugins + /docs/reference/package-management (official-docs)
    **Quote:** "The enabled set is the union over the default home **and every profile** under `profiles/`, read from each `config.yaml`" / "one separate Python process per profile, started on demand, that imports the profile's user-installed plugins and talks to Hermes over a private pipe."
    **Tier:** Verified

## F. Personality / SOUL per profile

30. **Claim:** SOUL.md is loaded only from the instance's HERMES_HOME — since each profile is its own HERMES_HOME, personality is per-profile identity, not shared.
    **Source:** /docs/user-guide/features/personality (official-docs)
    **Quote:** "Hermes loads `SOUL.md` only from `HERMES_HOME` … That makes `SOUL.md` a true per-user or per-instance identity, not just an additive layer."
    **Tier:** Verified

31. **Claim:** Custom personality presets are per-profile config (`agent.personalities`), and `/personality` is only a session overlay — a per-profile persona lives in SOUL.md.
    **Source:** /docs/user-guide/features/personality (official-docs)
    **Quote:** "You can add your own — or override a built-in by reusing its name — in `~/.hermes/config.yaml` under `agent.personalities`" + "`SOUL.md` = baseline voice / `/personality` = temporary mode switch"
    **Tier:** Verified

## G. Approvals & security per profile

32. **Claim:** Approval mode and the smart-approval classifier are ordinary config.yaml settings, hence per profile (dashboard exposes them as form fields per profile switcher).
    **Source:** /docs/user-guide/features/web-dashboard + /docs/user-guide/configuration (official-docs)
    **Quote:** "**approvals** — dangerous command approval mode (smart/manual/off)" + "And more — every section of config.yaml has corresponding form fields"
    **Tier:** Verified

33. **Claim:** Self-modification gates are per-profile config: `skills.write_approval` / `memory.write_approval` stage agent writes for human review in that profile.
    **Source:** /docs/user-guide/features/skills (official-docs)
    **Quote:** "skills: write_approval: false # false = write freely (default) | true = require approval"
    **Tier:** Verified

34. **Claim:** Settings that must be identical across profiles (e.g. plugin isolation) are pinned via root-owned managed scope instead of per-profile config.
    **Source:** /docs/user-guide/features/plugins (official-docs)
    **Quote:** "When the profiles belong to people you are isolating from each other, pin it in the managed scope instead; the managed value wins over every profile's own config and `hermes config set` refuses to change it"
    **Tier:** Verified

## H. Cloning as the equipping path

35. **Claim:** `--clone` is the documented "equip a new profile from an equipped source" path: config.yaml, .env, SOUL.md, skills, curated memories and installed plugins (with install records) travel.
    **Source:** /docs/user-guide/profiles (official-docs)
    **Quote:** "Copies your current profile's `config.yaml`, `.env`, `SOUL.md`, skills, and the curated memory files … Installed plugins travel too: `plugins/` (catalog, Git and hand-installed plugins, plus their install records) is copied … Sessions, `state.db`, cron jobs and everything else start empty."
    **Tier:** Verified

36. **Claim:** Clones never carry messaging channels (bot tokens, platform sections, multiplex routes) or cron jobs unless explicitly opted in — channel-less clones are the documented default for specialist profiles.
    **Source:** /docs/user-guide/profiles (official-docs)
    **Quote:** "Every clone — `--clone`, `--clone-from`, `--clone-all`, and the dashboard / Desktop / TUI 'clone from profile' option — copies the source **without its messaging channels**" + "**Cron jobs are not cloned** either: … a clone that inherited them would run every job twice (two gateways, same job ids)."
    **Tier:** Verified

37. **Claim:** A kanban-role profile is equipped for routing at create time with `--description "<role>"` so the orchestrator knows what it's good at.
    **Source:** /docs/user-guide/profiles (official-docs)
    **Quote:** "If you plan to use this profile as a kanban worker (or want the kanban orchestrator to route work to it), pass `--description \"<role>\"` at create time so the orchestrator knows what it's good at"
    **Tier:** Verified

## I. Dashboard / profile builder

38. **Claim:** The web dashboard is the GUI equipping surface: profile cards show model/skills/gateway state; creation flow offers clone-from-default, clone-everything, no-bundled-skills, description and model, with a dedicated Profile Builder page for model, MCPs and skills.
    **Source:** /docs/user-guide/features/web-dashboard (official-docs)
    **Quote:** "**Create** — name + optional clone-from-default / clone-everything / no-bundled-skills, description, and model; the dedicated Profile Builder page (`/profiles/new`) offers the full flow (model, MCPs, skills)" + "**Profile cards** — each shows its model/provider, skill count, gateway state, description, and badges"
    **Tier:** Verified

39. **Claim:** The dashboard can run a dedicated per-profile server for a worker profile.
    **Source:** /docs/user-guide/features/web-dashboard (official-docs)
    **Quote:** "`--isolated` | off | When launched from a named profile (`worker dashboard`), run a dedicated per-profile server instead of routing to the machine dashboard"
    **Tier:** Verified

## Minimal-per-role guidance — synthesis

- The docs never publish a single checklist titled "minimal specialist profile," but the minimal baseline is documented in three concrete places: **Blank Slate** (provider+model, file, terminal only — #11), **cron** (no chat platform; per-platform/per-job toolsets; explicit bloat warning — #12), and the **kanban worker cost split** (cheap model, own config — #14). Cloning without channels (#36) plus `--no-skills` (#19) plus `agent.disabled_toolsets` (#4) is the documented composition for a headless worker.

## Searched, found nothing (evidence of absence)

- `model_overrides` as a *core per-role model switch* key — searched llms-full.txt (official docs, 6 MB corpus) and /docs/llms.txt index; all hits are provider-model *metadata* overrides (context_window, supports_vision/reasoning, max_output_tokens) and plugin `llm.model_override` capability. No core profile-level "model_overrides" documented → crew-plugin usage is plugin-internal. (source types: official-docs)
- Query "worker profiles need no chat platforms" (variants: "needs no chat", "no chat platform", "don't need a gateway") — no explicit kanban statement found in llms-full.txt; closest documented facts are cron-runs-with-no-chat-platform and channel-less clones. (official-docs)
- "skill listing dilution" / "too many skills" / "profile bloat" as documented terms — zero hits in official docs; nearest documented rationale is the curator's "pollute the catalog and waste tokens" (#21). (official-docs)
- `skills.disabled` config key — mentioned once on the curator page ("skills in `skills.disabled` (which `skill_view` refuses)") but not documented on the skills page; no further spec found. (official-docs)
- GitHub issues / community practice for per-role equipping — deliberately not covered (lane L5 scope).

Sub-question status from this lane's view: answered
