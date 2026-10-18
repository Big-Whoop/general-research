# Input Gate Hook — Gate Rules & Override Mechanism

The `pre_tool_call` hook (`hooks/block_nonconform_kanban_create.py` in the
kanban-tools repo) blocks `kanban create` / `kanban swarm` commands whose
body or command flags are not gate-conformant. It runs as a subprocess on
every terminal tool call — **no gateway restart needed for script changes**
(the config only holds the path; the script is re-executed per invocation).

Hook mechanism (stdin/stdout schema, fail-open, consent, testing): see
`hermes-kanban-ops` → `references/hooks.md`.

## Legacy checks (L1, L2)

Reused from `kanban_specify_gate.py`:
- **L1:** Body contains the Rules-Block-Marker (`Quality-Gate (Board-Regeln`)
  OR all rule keywords from `RULE_CHECKS`.
- **L2:** Body contains verifiable Done-Kriterien (checklist).

## Gate rules R1–R8

| Rule | Type | Condition | Keywords / Flag |
|---|---|---|---|
| R1 `workspace-worktree` | command_flag | Only when `--workspace` is present | `--workspace` must equal `worktree` (not `dir:`, not `scratch`) |
| R2 `completion-contract` | command_flag | Only when R1 satisfied (`--workspace worktree`) | `--completion-contract` must be present: `local-only`, `OWNER/REPO`, or a GitHub PR URL (`local-only` is accepted and is the right choice for private repos without Pro) |
| R3 `review-handoff` | body_text | Always (non-triage) | `kanban_request_review` |
| R4 `no-self-complete` | body_text | Always | `nicht kanban_complete` / `nie kanban_complete` / `never kanban_complete` |
| R5 `pr-pflicht` | body_text | Always | `gh pr create` / `pr auf github` / `pull request` / `pr öffnen` |
| R6 `reviewer-assignment` | body_text | Always | `reviewer=reviewer` / `--reviewer reviewer` / `reviewer: reviewer` |
| R7 `worktree-isolation` | body_text | Always | `isoliert` / `eigener worktree` / `worktree isolation` |
| R8 `dependency-info` | body_text | Always | `parent:` / `dependencies:` / `keine dependencies` / `abhängigkeiten` |

### Design decisions

- **R1/R2 are conditional, not absolute.** R1 only fires when `--workspace`
  is present in the command. Not every card is a code card — research and
  documentation cards don't need a worktree. R2 only fires when R1 is
  satisfied (workspace=worktree). If R1 is overridden, R2 is also skipped
  (the `requires` dependency in the rule definition).
- **Body-text rules use case-insensitive substring matching.** Each rule has
  one or more keyword groups; at least one keyword per group must appear in
  the body. Groups are OR'd, groups within a rule are AND'd.
- **The hook is fail-open.** Any internal error → exit 0 + log line to
  `/tmp/kanban-gate-hook.log`. A broken hook must not wedge the board.

## Override mechanism

Format (in the card body):
```
OVERRIDE: <rule-name> (Begründung min. 10 Zeichen)
```

- `<rule-name>` must be one of the 8 gate rule keys (e.g. `pr-pflicht`,
  `review-handoff`). Unknown names are silently ignored (no effect).
- The reason in parentheses must be ≥ 10 characters. Shorter reasons are
  not parsed as overrides (the regex requires `[^)]{10,}`).
- `OVERRIDE: ALL` or `OVERRIDE: *` is NOT supported — overrides are
  per-rule only.
- Multiple overrides can coexist in one body (one line each).
- The override is permanent in the card body → audit trail.
- When R1 (`workspace-worktree`) is overridden, R2
  (`completion-contract`) is also skipped (dependency chain).

## First-try conformant body (copy, then fill in)

```
Quality-Gate (Board-Regeln): Verteilungsregel, PR-Pflicht, Kein-Push-master, Input-Gate apply.
## Goal / Sites / Fix (execute, don't design)
## Done-Kriterien
- <verifiable checks>
Dependencies: keine
## Review-Handoff (2-Lane)
Arbeite in deinem isolierten Worktree. Nie in dir: schreiben.
Am Ende: PR auf GitHub öffnen (gh pr create), dann kanban_request_review (reviewer=reviewer) aufrufen. NICHT kanban_complete — das überspringt die Review-Lane.
```
Flags: `--workspace worktree --branch <b> --completion-contract local-only --assignee default`.

Write long bodies to a scratch file and pass `--body-file <path>`, because the hook reads the file. A plain `create` without a body (even `--help` piped through the terminal) is blocked as "body missing". Ops-only cards that change a host without a PR (e.g. a one-time bootstrap) use the verification-only OVERRIDE set below with an "ops-only, no repository change" reason, and their body carries the user's Gate-2 sign-off.

## Retrofitting existing cards (created before the gate)

1. Append, don't rewrite: `hermes kanban edit <id> --body "<old body + gate block>"` (`--body` replaces the whole body, so read it first via `show <id> --json`; the JSON can be followed by CLI warning text, so parse with `json.JSONDecoder().raw_decode`).
2. Code/PR cards: append the first-try block above. If they legitimately run in `scratch` (e.g. recon first, worktree created inside the card), add `OVERRIDE: workspace-worktree (...)`.
3. Verification-only cards (no code, no PR, they complete themselves): add the marker, Done-Kriterien, a Dependencies line, plus one OVERRIDE line with a reason for each of review-handoff, no-self-complete, pr-pflicht, reviewer-assignment, worktree-isolation, workspace-worktree. Missing the workspace-worktree override is the common miss when the card runs in scratch.
4. Leave running cards' bodies alone and add a comment instead.
5. Verify each edited body against the real hook: feed `{"tool_name":"terminal","tool_input":{"command":"hermes kanban create 'x' --workspace <ws> --body <quoted body>"}}` to the hook script on stdin. No output means pass, `{"action":"block",...}` lists the failing rules.

## Pitfalls

- **Keep keywords free of markdown backticks.** Matching is plain substring, so
  a backticked `kanban_complete` after NICHT does NOT match `nicht kanban_complete`
  (R4 fails); write the keyword phrases as plain text.

- **Keyword overlap with the rules block.** The full
  `quality-gate-rules.md` content contains many of the same words the gate
  rules check for ("worktree", "PR", "reviewer"). When testing individual
  gate rules in isolation, use a **minimal body** (just the
  Rules-Block-Marker string + Done-Kriterien, NOT the full rules block)
  so the rules block doesn't accidentally satisfy the gate keywords.
  In production this is not a problem — a conformant card SHOULD contain
  the full rules block AND the gate sections.
- **Keyword specificity matters.** Use the most specific keyword that
  uniquely identifies the instruction. E.g. R3 checks for
  `kanban_request_review` (the function name), NOT `request-review` or
  `review-handoff` (which can appear in unrelated contexts, including the
  override line itself: `OVERRIDE: review-handoff (...)` contains the
  string `review-handoff`).
- **The hook only covers the terminal tool path.** Cards created via the
  `kanban_create` native tool, direct DB access, or the dashboard bypass
  the hook entirely.
- **The hook checks at CREATE time, not at runtime.** It ensures the card
  is created with the right flags and instructions, but cannot prevent the
  worker from ignoring the instructions at runtime. The `completion_contract`
  (structural, at completion time) and the reviewer lane (structural, at
  dispatch time) are the backstops.

## Test file

`tests/test_hook_block_nonconform.py` in the kanban-tools repo — 38 cases
covering legacy checks, all 8 gate rules individually and combined, and
the override mechanism. Run: `python3 tests/test_hook_block_nonconform.py`.

## Config wiring

Already wired in `/opt/data/config.yaml` under `hooks.pre_tool_call`.
The entry points to the script path; no config change is needed when the
script content changes.
