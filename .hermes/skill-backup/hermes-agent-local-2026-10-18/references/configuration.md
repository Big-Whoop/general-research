# Configuration, Toolsets & Voice

Edit with `hermes config edit` or `hermes config set section.key value`.
Full reference: https://hermes-agent.nousresearch.com/docs/user-guide/configuration

### Config Sections (most-used keys)

| Section | Key options |
|---------|-------------|
| `model` | `default`, `provider`, `base_url`, `api_key`, `context_length`, `aliases` |
| `agent` | `max_turns` (90), `tool_use_enforcement`, `service_tier`, `verify_on_stop` |
| `terminal` | `backend` (local/docker/ssh/modal/daytona/singularity), `cwd`, `timeout` (180) |
| `compression` | `enabled`, `threshold` (0.50), `target_ratio` (0.20) |
| `display` | `skin`, `interface` (cli/tui), `language`, `show_reasoning`, `show_cost`, `pet` |
| `approvals` | `mode` (smart/manual/off), `timeout`, `cron_mode` |
| `stt` | `enabled`, `provider` (local/groq/openai/mistral/elevenlabs/deepinfra) |
| `tts` | `provider` (edge/elevenlabs/openai/minimax/mistral/neutts/gemini/piper/kittentts/deepinfra/xai) |
| `memory` | `memory_enabled`, `user_profile_enabled`, `provider`, `write_approval`, `memory_char_limit`, `user_char_limit` |
| `security` | `redact_secrets`, `tirith_enabled`, `website_blocklist` |
| `delegation` | `model`, `provider`, `max_concurrent_children`, `max_iterations` (50), `max_spawn_depth` |
| `checkpoints` | `enabled`, `max_snapshots` (50) |
| `curator` | `enabled`, `consolidate` (false, opt-in aux-model consolidation), `interval_hours`, `stale_after_days` |

`hermes config check` reports sections missing from an older config.

**Raising the memory budget** (the memory tool keeps rejecting adds/patches at the char limit): back up `config.yaml`, change `memory.memory_char_limit` / `memory.user_char_limit` with an anchored single-line `sed` (nested key — `config set` is unsafe here), then confirm with `hermes config get memory`. The running session keeps the old limit; the new budget applies from the next session, so note the pending entry and add it then.

### Toolsets

Enable/disable via `hermes tools` (interactive) or `hermes tools enable/disable NAME`.
Full enumeration: `TOOLSETS` dict in `toolsets.py` (`_HERMES_CORE_TOOLS` is the default bundle most platforms inherit).

| Toolset | What it provides |
|---------|-----------------|
| `web` / `search` | Web search + extraction / search-only subset |
| `browser` | Browser automation (Browserbase, Camofox, or local Chromium) |
| `terminal` | Shell commands and process management |
| `file` | File read/write/search/patch |
| `code_execution` | Sandboxed Python execution |
| `coding` | Code-editing helpers (LSP-backed) |
| `computer_use` | Desktop GUI control (cua-driver) |
| `vision` | Image analysis |
| `image_gen` | Image generation and image-to-image editing |
| `video` / `video_gen` | Video analysis / video generation |
| `x_search` | X (Twitter) search (X OAuth or API key) |
| `tts` | Text-to-speech |
| `skills` | Skill browsing and management |
| `memory` | Persistent cross-session memory |
| `session_search` | Search past conversations |
| `context_engine` | Pluggable context-engine hooks |
| `project` | Named multi-folder workspace tools |
| `delegation` | Subagent task delegation |
| `cronjob` | Scheduled task management |
| `clarify` | Ask user clarifying questions |
| `todo` | In-session task planning |
| `kanban` | Multi-agent work-queue tools (gated to workers) |
| `debugging` | Extra introspection tools (off by default) |
| `safe` | Minimal low-risk toolset for locked-down sessions |
| `spotify`, `homeassistant`, `discord`, `discord_admin`, `feishu_doc`, `feishu_drive`, `yuanbao` | Service integrations (gated on their credentials) |

Tool changes take effect on `/reset` (new session) — never mid-conversation, to preserve prompt caching.

**Per-client selection:** `platform_toolsets.<platform>` lists the enabled toolsets per platform (CLI/TUI/Desktop → `cli`; each messaging platform its own key). The **Desktop app uses `platform_toolsets.cli`** — it is the same agent core as the CLI with no messaging platform, so there is NO separate `desktop` key. `agent.disabled_toolsets` is a global subtractive list applied on top of the platform selection (live selection = `platform_toolsets.<platform>` minus `agent.disabled_toolsets`). `known_builtin_toolsets` / `known_plugin_toolsets` record what was offered per platform.

### Tool Search (progressive disclosure) — hide tools but keep them reachable

When many MCP/plugin tools (or explicitly-named built-ins) would bloat the context, `tools.tool_search` swaps them out of the model-visible tools array for three bridge tools; the model loads each full schema on demand:
- `tool_search(queries)` — search the deferred catalog (BM25 + stemming) → names + short descriptions.
- `tool_describe(names)` — load the full schemas.
- `tool_call(calls)` — invoke; Hermes unwraps the bridge so hooks/guardrails/approval run against the real tool name.

The system prompt carries a one-line-per-tool catalog manifest, so deferred capabilities stay discoverable by name (the model can skip straight to `tool_describe`). Tiered disclosure: Tier 0 = no deferred tools (all eager); Tier 1 = bridge + manifest; Tier 2 = bare bridge + one line per server. Listing budget = `min(threshold_pct% of context, listing_max_tokens)`, re-evaluated every assembly.

Config (`tools.tool_search`):

| Key | Default | Meaning |
|-----|---------|---------|
| `enabled` | `auto` | `auto`/`on` activate when ≥1 deferred tool exists; `off` = everything eager |
| `threshold_pct` | `5` | listing budget as % of context |
| `listing` | `auto` | embed the name+description manifest (degrades to names-only, then per-server summary) |
| `listing_max_tokens` | `4000` | absolute cap on the manifest |
| `defer` | curated list | tool NAMES to defer; an explicit list REPLACES the curated default, `[]` = everything eager |

- `defer` takes individual tool NAMES, not toolsets — you can defer any deferrable built-in (e.g. all `kanban_*` / `browser_*`) to move it from the eager array into the on-demand catalog. This is the main lever for cutting tool-schema payload (tools are typically ~70% of an agent request).
- **Never defer `clarify`** — deferring it collapses structured-clarify usage (A/B: 18/18 → 7/18).
- Core tools (`_HERMES_CORE_TOOLS`) stay eager by default; only cold/event-triggered built-ins + MCP/plugin tools defer.
- Trade-offs (inherent to progressive disclosure): one extra round trip on a cold tool (describe→call); no prompt-cache benefit on deferred schemas; no provider-native validation (Hermes validates locally); model-quality dependent (smaller models write weaker search queries); toolset edits invalidate the cache.
- Tool changes (including `defer`) take effect on `/reset`, never mid-conversation.

## Voice

### STT (Voice → Text)

Voice messages from messaging platforms are auto-transcribed.

```yaml
stt:
  enabled: true
  provider: local   # local (faster-whisper, free) | groq | openai | mistral | elevenlabs | deepinfra
  local:
    model: base     # tiny, base, small, medium, large-v3
```

Auto-detect priority: local faster-whisper (`pip install faster-whisper`) → Groq (`GROQ_API_KEY`, free tier) → OpenAI (`VOICE_TOOLS_OPENAI_KEY`) → Mistral Voxtral (`MISTRAL_API_KEY`).

### TTS (Text → Voice)

| Provider | Env var | Free? |
|----------|---------|-------|
| Edge TTS (default) | None | Yes |
| ElevenLabs | `ELEVENLABS_API_KEY` | Free tier |
| OpenAI | `VOICE_TOOLS_OPENAI_KEY` | Paid |
| MiniMax | `MINIMAX_API_KEY` | Paid |
| Mistral | `MISTRAL_API_KEY` | Paid |
| Gemini | `GOOGLE_API_KEY` | Free tier |
| NeuTTS / Piper / KittenTTS (local) | None | Free |

Voice commands: `/voice on` (voice-to-voice), `/voice tts` (always voice), `/voice off`.
