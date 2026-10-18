# Troubleshooting

### Browser tool: `browser_exec` fails with `BU_CDP_URL=... unreachable`
`browser.cdp_url` in `config.yaml` forces the tool to *connect* to that CDP endpoint instead of launching the bundled local Chromium. If it points at a dead external host (e.g. `http://192.168.10.10:9223`), every `browser_exec` fails with `fatal: BU_CDP_URL=... unreachable ... Connection refused`. **Fix:** delete the `cdp_url` line (keep `backend: browser-use`, `cloud_provider: local`) — with no `cdp_url` the tool auto-spawns the bundled Chromium at `/opt/hermes/.playwright/chromium-*/`. Code path: `browser_tool_cdp.py::_get_cdp_override` (env `BROWSER_CDP_URL` wins over config) → `browser_tool_session.py::_create_local_session` when the override is empty. Note: `/opt/data` is a persistent volume (not part of the image), so a config edit survives container restarts AND image A/B-swaps; for a true in-image fix, seed the config in the suite repo. Verify after: `browser_exec` → `new_tab("https://example.com")` + `page_info()`.

### Desktop file browser: 403 "Path is outside the managed read boundary"
The dashboard file browser (`/api/files`) enforces a "managed read boundary". When `HERMES_HOME` resolves to `/opt/data` (hosted/container layout), `_managed_files_policy()` (in `hermes_cli/web_server_files.py`) auto-locks the root to `/opt/data`, so any path outside it (e.g. `/workspace` repos) is refused with 403 "Path is outside the managed read boundary". **Fix:** set `HERMES_DASHBOARD_FILES_ROOT` to a single root that contains ALL the paths you want browsable (e.g. `/` to cover both `/opt/data` and `/workspace` — it takes one root, not a colon-separated list). The value is read at request time, so it takes effect as soon as it's in the process env; in a container the env comes from the deployment (ConfigMap), so a pod rollout is needed to apply it.

### Voice not working
1. Check `stt.enabled: true` in config.yaml
2. Verify provider: `pip install faster-whisper` or set API key
3. In gateway: `/restart`. In CLI: exit and relaunch.

### Tool not available
1. `hermes tools` — check if toolset is enabled for your platform
2. Some tools need env vars (check `.env`)
3. `/reset` after enabling tools

### Model/provider issues
1. `hermes doctor` — check config and dependencies
2. `hermes auth` — re-authenticate OAuth providers (or `hermes auth add <provider>`)
3. Check `.env` has the right API key
4. **Copilot 403**: `gh auth login` tokens do NOT work for Copilot API. You must use the Copilot-specific OAuth device code flow via `hermes model` → GitHub Copilot.

### Changes not taking effect
- **Tools/skills:** `/reset` starts a new session with updated toolset
- **Config changes:** In gateway: `/restart`. In CLI: exit and relaunch.
- **Code changes:** Restart the CLI or gateway process

### web_extract shows a stale page (result caching)
`web_search`/`web_extract` cache results for 20 minutes (PR #94618) — a
repeat fetch of the same URL within the TTL is served from cache, which
can look like "my website changes aren't showing up."

Automatic carveouts (always fetched live, never cached):
- localhost / 127.0.0.1 / `*.local` / `*.localhost` / single-label LAN
  hostnames / private + link-local IP ranges (dev servers, hot-reload
  builds, chat-GUI artifact previews)
- URLs matched by `security.website_blocklist`
- failed responses and keyless-rescue-served responses

Developing a site tested over the PUBLIC internet (Vercel/Netlify
preview, ngrok/cloudflared tunnel, staging domain)? Public DNS isn't
auto-carved-out — list the host in config.yaml:

```yaml
web:
  cache_exempt_hosts:      # always fetched live; effective immediately
    - mysite.vercel.app
    - "*.ngrok-free.app"
    - mysite.dev           # suffix match: also covers preview.mysite.dev
```

Blunt instruments: `web.cache_ttl_minutes: 1` (min) or
`web.cache_enabled: false` disables both caches entirely.

### Skills not showing
1. `hermes skills list` — verify installed
2. `hermes skills config` — check platform enablement
3. Load explicitly: `hermes -s name` (or the skill's own `/<name>` slash command)

### Gateway issues
Check logs first:
```bash
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
```

Common gateway problems:
- **Gateway dies on SSH logout**: Enable linger: `sudo loginctl enable-linger $USER`
- **Gateway dies on WSL2 close**: WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
- **Gateway crash loop**: Reset the failed state: `systemctl --user reset-failed hermes-gateway`

### Platform-specific issues
- **Discord bot silent**: Must enable **Message Content Intent** in Bot → Privileged Gateway Intents.
- **Slack bot only works in DMs**: Must subscribe to `message.channels` event. Without it, the bot ignores public channels.
- **Windows-specific issues** (`Alt+Enter` newline, WinError 10106, UTF-8 BOM config, line endings): see `references/windows-quirks.md`.

### Auxiliary models not working
If `auxiliary` tasks (vision, compression, session_search) fail silently, the `auto` provider can't find a backend. Either set `OPENROUTER_API_KEY` or `GOOGLE_API_KEY`, or explicitly configure each auxiliary task's provider:
```bash
hermes config set auxiliary.vision.provider <your_provider>
hermes config set auxiliary.vision.model <model_name>
```

### "Reset permissions" / auto-approving everything
See `references/security-privacy.md` — wipe the "Always allow" stores, don't touch yolo mode.

