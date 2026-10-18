# Hermes Shell Hooks (v0.21.5, verified in installed source)

Schema facts for writing a blocking hook (e.g. the input-gate
`pre_tool_call` guard). Source: `agent/shell_hooks.py`.

- Config: top-level `hooks:` map in `config.yaml`, e.g.
  `pre_tool_call: [{matcher: "terminal", command: "/abs/path/script.py",
  timeout: 10, fail_closed: false}]`. Edit the file directly (never
  `hermes config set` for nested YAML), validate the YAML, keep the edit
  idempotent (check the entry exists first).
- **Startup reload pitfall (proven 2026-10-01):** hooks are registered from
  config at PROCESS STARTUP ONLY. A gateway/webui process that started
  before the `hooks:` entry was written never loads it — the hook is
  silently inactive in every session that process serves, even though the
  script is installed, correct, and allowlisted. After any `hooks:` edit:
  restart the process (user step), then verify with a live test (see
  Testing). Sanity check: `ps -o lstart -p <pid>` vs
  `stat -c %y config.yaml` — config newer than process start = hook not
  loaded.
- Invocation: Hermes runs the script with the event payload as JSON on
  **stdin**. For `pre_tool_call` the payload carries `tool_name` and the
  arguments under the key **`tool_input`** (exact field name — a script
  probing for `arguments`/`args` instead finds nothing and fails open);
  for `terminal` the command string is `tool_input.command`.
- Verdict: script **stdout** JSON. `{"action": "block", "message": "…"}`
  (key is `message`, not `reason`) blocks the tool call and feeds the
  message back to the agent; empty stdout + exit 0 = allow. A `modify`
  action rewrites the arguments for some tools — prefer block+message for
  gate hooks.
- `fail_closed: true` = a broken/timeout hook blocks the call; default is
  fail-open. For a quality gate: fail-open + log every decision (a broken
  hook must not wedge the board), and document `fail_closed` as the strict
  alternative.
- Consent: `pre_tool_call` hooks need first-use approval per
  (event, command); approvals persist in
  `/opt/data/shell-hooks-allowlist.json`. Consent is per process — an
  approval recorded by a worker/CLI process does NOT cover the gateway
  process.
- `pre_auxiliary_call` hooks exist but are OBSERVER-ONLY (fail-open, return
  ignored) — they cannot block auxiliary LLM calls (auto-decompose, etc.).
- Kanban lifecycle hooks are observer-only (fire after the DB commit).
- Testing: feed the exact stdin JSON (with `tool_input`, not `arguments`)
  via a pipe and check stdout/exit code per case — but a pipe test only
  proves the SCRIPT is correct, not that it is ACTIVE. The real check is
  one live non-conformant command through an actual agent terminal call
  after the process restart: it must come back blocked (spawned workers
  inherit the same config, so the hook covers them too).
