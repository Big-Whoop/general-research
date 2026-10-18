# Model cost strategy: mixing cheap and expensive models

Load when: cost concerns in long projects, "which model for which task", model switching, prefill/prompt-cache cost, pinning models for delegation/kanban/auxiliary slots.

## Core rule: one model per chat for its lifetime

A mid-session `/model` switch rebuilds the system prompt (model name + model-gated guidance blocks sit in the cached prefix) → prefix bytes change → 100% prompt-cache loss → the next turn re-prefills the ENTIRE history at full input price. Measured on a ~300k-token session: ~220 s cold after a switch vs 8–25 s warm; maintainers treat this as inherent, not a bug. Route work to the right model via FRESH contexts instead of switching the chat.

Cost shape (Anthropic list prices — verify against anthropic.com/pricing before quoting):
- One-time re-prefill of a 100k-token chat on switch: Sonnet-class $0.20–0.40, Opus-class $0.40–0.80, Haiku-class $0.50–1.00 (the >100k tier can make a downgrade cost MORE than an upgrade).
- Staying on the expensive model with a warm 1h cache: ~$0.02 per turn per 100k read.
- Fresh session + 5–10k handover on the expensive model: $0.04–0.08 — 5–20× cheaper than re-prefilling 100k.
- Break-even for an Opus→Sonnet switch: 20–40 turns.

## Native mechanisms (ranked by fit for "expensive only where needed")

1. **`delegation.model` / `delegation.provider` / `delegation.base_url`** (config.yaml) — profile-wide pin; ALL `delegate_task` children run on the pinned model with a FRESH context (goal+context only, no parent history). The docs' sanctioned "frontier planner, inexpensive workers" pattern. Resolution: base_url > provider > inherit; empty model = inherit parent. There is NO per-task model parameter on `delegate_task` (verified in the tool schema; per-task selection is an open feature request, not shipped). Child cache TTL is clamped 1h→5m.
2. **Kanban per-task model override** — the ONLY native per-task pin: `hermes kanban create "task" --assignee P --model M --provider P` or later `hermes kanban set-model <id> M --provider P` (`none` clears). Workers spawn as `hermes -p <assignee>` and read their own profile's model config; the dashboard's per-task dropdown drives the same field.
3. **Auxiliary slots** — ~11 side-job slots (compression, vision, web_extract, approval, title_generation, kanban_decomposer, triage_specifier, review, …), each independently overridable via `auxiliary.<task>.provider/model`. Zero impact on the chat's model/cache. Pin compression to a cheap model (summarizing on a frontier model is the classic waste); keep `review` on the strong model; do NOT put approvals on a different model (community-reported breakage).
4. **New chat on the right model + handover** — the desktop composer picker is per-chat and never writes the profile default; hand context via a handover file, @-references (CLI), or `session_search`. The docs' own advice: on a long chat, a fresh chat on the new model is often cheaper than bouncing.
5. **Profiles** — per-profile `config.yaml` model; `hermes -p <name> chat -q "…"` one-shots; durable separation with own memory/skills.
6. **`/model <name> --once`** — one-turn escalation with auto-restore; breaks the cache prefix TWICE (out and back) and has a known stale-identity-note wart; only for short sessions or deliberate cheap→expensive escalation.
7. **MoA presets** — mix providers/models per turn (references advise, aggregator acts); `/moa` one-shot restores the previous model; cache-safe but pays extra model calls per turn.
8. **`channel_overrides`** (gateway) — per-channel model/system-prompt from one gateway; priority: session `/model` > channel > global.

## Workflow pattern for long projects

- Expensive model only where judgment counts: planning, architecture, review, hard debugging (its own chat, or kanban cards with the per-task pin).
- Volume work on the cheap/local model: execution, research, file scans, summaries — via pinned delegation + auxiliary slots.
- Context transfer between model tiers: handover files (markdown), kanban parent links (carry the parent's completion summary), @-references, session_search.
- `reasoning_effort` is a cache-safer lever than model switching: effort-only changes are reported to preserve the cache on current-gen models (verify per model — vendor invalidation tables list effort as a message-block invalidator).

## Pitfalls

- **Bare-name `/model` with local/custom providers is a billing hazard**: when a configured provider declares a model id that also matches the bare part of a metered provider's slug, the switch can be silently routed to the metered provider. Always use explicit `provider:model` syntax.
- **Aux slots default to `auto` = main model**: after switching the main model to an expensive one, compression/titles/etc. silently follow it. Audit `auxiliary.*` whenever the main model changes.
- **Orchestrators trust subagent reports blindly** — a frontier model will believe a false report from a cheap subagent. Verify load-bearing claims; keep `/review` on the strong model.
- **`context_length` pins can follow the wrong model across switches** (known bug family); the supported per-model declaration is `custom_providers[].models.<id>.context_length`.
- **Local-model window overflow** (e.g. 256k local vs 1M API): over-limit requests 400, no silent truncation; Hermes preflight-compresses when compression is enabled — so keep compression on the cheap model.
- **Cache visibility through OpenAI-compatible proxies**: some proxies (e.g. CLIProxyAPI) inject `cache_control` server-side but do not translate `cached_tokens` back into OpenAI usage — verify cache hits on the provider side, not in the client's usage stats.
