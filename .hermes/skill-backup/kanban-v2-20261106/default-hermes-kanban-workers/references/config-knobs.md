# Kanban Config Knobs (verified 2026-09-29, hermes 2.101-era)

Source: `/opt/hermes/hermes_cli/config.py` `kanban:` block. All keys under the
top-level `kanban:` mapping in `/opt/data/config.yaml`.

| Key | Default | Meaning |
|---|---|---|
| `dispatch_in_gateway` | `true` | Run the dispatcher inside the gateway process (recommended). `false` = run a separate dispatcher. |
| `dispatch_interval_seconds` | `60` | Seconds between dispatcher ticks. Lower = snappier pickup, more SQL. |
| `failure_limit` | `2` | Auto-block a task after N consecutive non-success runs (spawn_failed/timed_out/crashed). Reassignment resets the streak. |
| `max_in_progress_per_profile` | `null` (unlimited) | **The parallelism knob.** Per-profile cap on simultaneous workers. Over-cap `ready` tasks defer to next tick. Set to `2` in this sandbox. |
| `worker_log_rotate_bytes` | `2MiB` | Worker stdout/stderr rotation size. |
| `worker_log_backup_count` | `1` | Rotated worker logs kept. |
| `orchestrator_profile` | `""` | Profile assigned to root/orchestration task after triage decomposition. |
| `default_assignee` | `""` | Fallback assignee when orchestrator can't match a profile. A task never ends up unassigned. |
| `auto_decompose` | `true` | Auto-run decomposer on triage tasks each tick. |
| `auto_decompose_per_tick` | `3` | Max triage tasks decomposed per tick. |
| `stale_timeout_seconds` | `0` | Reclaim running tasks with no heartbeat for N seconds. `0` = disabled. |

## How to edit (IMPORTANT)
`hermes config set kanban.max_in_progress_per_profile 2` is **UNSAFE** for
nested YAML (it can coerce a list→string or truncate). Append/edit the block
directly:
```bash
printf '\nkanban:\n  max_in_progress_per_profile: 2\n' >> /opt/data/config.yaml
```
Then validate the whole file parses before relying on it:
```bash
/opt/hermes/.venv/bin/python -c "import yaml;print(yaml.safe_load(open('/opt/data/config.yaml')).get('kanban'))"
```
(`/opt/hermes/bin/python3` does not exist; the venv python is
`/opt/hermes/.venv/bin/python`.)

## Notes
- The cap is **per profile**, global to the board. To fan out across more
  concurrency, create more profiles and distribute assignees — that also
  isolates model quota / browser pool / sessions per profile.
- `hermes kanban dispatch --max N` caps spawns for a single manual pass only.
- Config changes are read at dispatcher start; a running gateway may need a
  restart to pick up `kanban:` changes (verify, don't assume).
- **Tick cost:** one idle in-process tick ≈ 0.5 s with ~11 boards on iSCSI (≈0.45 s `tick_once` over all boards + ≈0.03 s `ready_nonempty`), run in a worker thread (does not block the gateway event loop). Cost scales with board count — each board's DB is opened, queried, and closed per tick — so the source comment "~300µs per idle tick" is outdated. CPU share of one core ≈ tick/(tick+interval): 10 s ≈ 5 %, 5 s ≈ 9 %, 2 s ≈ 20 %, 1 s ≈ 33 %; floor is 1 s (`max(interval, 1.0)`), 10–5 s is the sweet spot. Never estimate the tick from `hermes kanban dispatch --dry-run` — that CLI path pays a ~10 s gateway-liveness probe the in-process tick never calls; time `tick_once` in-process (venv python) instead.
