# llama-swap Kanban Board

Project board for `/workspace/dev/repos/ours/llama-swap` (GitHub: `Big-Whoop/llama-swap`, private).

- **Slug:** `llama-swap` — **DB:** `/opt/data/kanban/boards/llama-swap/kanban.db`
- Icon 🔁, color `#f59e0b`, board default-workdir `/workspace/dev/repos/ours/llama-swap`
  (note: cards still resolved to `scratch` — see SKILL.md workspace gotcha)
- **The board is the source of truth for open items.** `ROADMAP.md` was removed
  2026-09-29 (card `t_9d85444f`); do not recreate it.

## Card inventory (idempotency keys stable — reuse when re-seeding)

Original ROADMAP-seeded cards (all done/archived by 2026-09-29):

| Task ID | Key | Status | Card |
|---|---|---|---|
| `t_db73278b` | `ls-gate-readiness` | done | GATE: Readiness-Prüfung |
| `t_89e7b292` | `ls-offen-1` | done | L2/L3-Gates im Skript implementieren |
| `t_8355bdb0` | `ls-offen-2` | done | Proxy-Port zur Verifikationszeit auflösen (Protokoll B) |
| `t_092ab10c` | `ls-offen-3` | archived | Live-E2E-Test Protokoll A (user: manually later) |
| `t_cd2cdd4b` | `ls-offen-4` | done | Safe-Reboot-Skills finalisieren |
| `t_cb3cfdf9` | `ls-offen-5` | done | Dev→Produktion-Sync (`scripts/sync_to_prod.sh`) |
| `t_e1a63f2c` | `ls-perspektivisch-1` | scheduled | [Perspektivisch] Session-Handoff nach Reboot |
| `t_9d85444f` | — | done | ROADMAP.md löschen, Board als Source of Truth |
| `t_4ab6cd8d` | — | done | Harte Regel in AGENTS.md: Code nur via Kanban |
| `t_69a97ac7` | — | done | Doku-Drift-Analyse → `discussion/DRIFT.md` |
| `t_5e4fd97d` | — | done | Q2–Q7 in `discussion/QUESTIONS.md` dokumentieren |

## Triage backlog from DRIFT.md / QUESTIONS.md (created 2026-09-29, parked `triage`, assignee `default`)

15 cards, dependency-linked (parent→child) by a dedicated wiring subagent. Groups:

- **A — Safe-Reboot-Trigger-Protokoll (Code, worktree/PR):**
  `t_3701b55f` Inflight-Warten (D1/D38) · `t_3d36e719` /upstream/health-Polling + Fallback-Snapshot (D3/Q4) · `t_4c9a1778` Post-Reboot-Ping + report.json (D4/D8/Q3)
- **B — Gates + Tests (Code):**
  `t_cff235cf` L1-Rollup-Check + 10s-Schwelle (D9) · `t_73eedc82` L3-Drain-Semantik (D10/C1) · `t_b9c15ded` Test-Coverage (C5/Rec-8)
- **D — Doku (exempt, direct to master):**
  `t_a23bcb56` no-unload auf B scopen (D2/D5) · `t_552525e3` delay_seconds entfernen (D6/D11) · `t_b0d38487` Crash-Detection + Hygiene (D7/C2-C7) · `t_b4815965` Target-Design-Banner (Rec-1b)
- **Q — offene Fragen (Investigation/Entscheidung):**
  `t_af15338d` Q1a SSE-Delete-Semantik · `t_164b5036` Q2a last_activity_at BLOCKER · `t_a39f35b9` Q3 Ping-Mechanismus · `t_913e6ed6` Q4a Retry-Limit/Livelock · `t_c9168fe9` Q6a Unload bei Protokoll A

Key dependency edges: Q1a+Q2a→A1 (blockers), Q4a→A2, Q3→A3, Q6a→D1,
D1+D4-Banner→A1, A1→A2→A3 sequential (same script file), B1→B2,
A3+B2→B3 (test coverage last).

## Change process (hard rule 2026-09-29, in repo AGENTS.md)

- **No code changes outside the kanban board** — code goes card → worktree →
  feature branch → PR → user merges on GitHub. Not by the main session, not
  by workers, no direct edits to master.
- **Exempt:** documentation (AGENTS.md, README.md, discussion/QUESTIONS.md,
  skills/, wiki), memory, and the repo folder `discussion/` — editable
  directly without a card.
- **Feature branches sprout in a worktree, never in the main checkout.**
  `dir:` is read-only-only (shares tree/index/HEAD with the main session —
  see SKILL.md workspace gotcha).
- Workers must not push to GitHub; ship as branch + PR, human merges.

## Readiness checks (all done 2026-09-29, commented on each card)

All access targets verified: API `:8080` HTTP 200, `GET /running` exposes a
per-model `proxy` field, gate DBs `/opt/data/state.db` + `/opt/data/lcm.db`
exist, `/opt/data/skills` writable, dev/prod script copies identical,
`llama-swap-infra` has NO git remote (sync = copy + local commit).

## Dispatch notes

- Manual `hermes kanban dispatch` after creating cards (gateway dispatcher
  may not tick quickly); always `--dry-run` first.
- Concurrency: `kanban.max_in_progress_per_profile: 2` in
  `/opt/data/config.yaml` (edit the file directly, not `hermes config set`).
- Check outcomes: `hermes kanban list`, `kanban show <id>`, `kanban runs <id>`.

## Collision history (2026-09-29)

- Cards 4 & 5 both edited `ROADMAP.md` in the same checkout in parallel
  (scratch workers reached the real repo by absolute path). No conflict only
  by luck. Dependent cards (shared docs/files) must be linked parent→child.
- Push-state lie: card 5's block summary claimed its commit was "local, not
  pushed" — it was already on `origin/master`. Verify git state directly,
  never the card text (see SKILL.md "Verifying worker output").
- `dir:` near-miss: a `dir:` worker wrote `discussion/DRIFT.md` while the
  main session committed `AGENTS.md` in the same checkout — no damage only
  because the worker's index was still empty. `dir:` = read-only-only now.

Task IDs are stable but only meaningful while the board DB lives; the
idempotency keys are the durable handle for re-seeding/dedup.
