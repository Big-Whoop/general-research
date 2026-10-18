# Unattended multi-stage kanban campaigns (driver cron)

When the user wants a multi-stage campaign to run with no chat present and only
Telegram reports (e.g. "run this, I'll decide at the end"), drive it with a
recurring cron job instead of a live session. Pattern:

1. Build the stage cards + a gate card (Gate Pattern). Link stage cards under
   the gate so they stay `todo` until released. Do NOT link the first/entry
   stage card under the gate unless you want it held too — link only the cards
   that must wait.
2. Raise `kanban.max_in_progress_per_profile` (edit config.yaml directly —
   `hermes config set` is unsafe for nested YAML) to the fan-out width the user
   wants. Takes effect next dispatcher tick, no restart.
3. Create a recurring cron job (`cronjob_manage action=create`,
   `schedule: "every 20m"`, **`deliver: "local"`** = silent, no chat noise).
   Its prompt is a SHORT pointer: "read <driver-file> and execute its
   idempotent steps". The driver file (e.g. under the board's artifacts dir)
   holds the full pipeline logic + per-card body templates.
4. Workers notify the user via `hermes send -t telegram -s "<subject>" -f
   <file>` (or stdin) — NOT via the cron deliver (keep that local). Test
   `hermes send` once before wiring it into cards.
5. The driver self-removes its own cron job on completion and sends a final
   Telegram line.

## Pitfalls
- **Don't inline a huge multi-paragraph prompt into `cronjob_manage` via
  tool_call** — it fails with a JSON parse error. Write the prompt + card
  templates to files and have the cron prompt point at them.
- **The driver must be idempotent**: check board state each tick, create only
  missing cards (by `--idempotency-key`), complete the gate only once, and
  never re-notify. A cron fires on a fixed cadence whether or not anything
  changed.
- **`deliver: local` for the driver, `hermes send` for user-facing reports.**
  The cron deliver is the driver's OWN output channel — point it at telegram
  and you get one message per tick. Workers do their own `hermes send`.
- The driver must VERIFY stage artifacts before releasing the gate (e.g.
  `json.load` a produced file, cross-check a count against the source DB) — a
  worker's completion summary is a self-report, not proof the artifact landed.
- The driver works ONLY because workers carry the profile's full CLI toolset
  (see Worker/dispatcher model) — they can read DBs, write artifacts, and run
  `hermes send`.
