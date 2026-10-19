---
name: subagent-fanout
description: "Fan out N items via delegate_task; cap output, batch small."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [delegate_task, subagent, fan-out, parallel, web-search, rate-limit, 429, truncation, orchestration]
---

# Parallel subagent fan-out

For tasks that are "do the same thing for each of N items" (headline/price/spec research per city or product, per-URL extraction, per-file summaries), `delegate_task` runs subagents in parallel. They wait on each other and one consolidated result re-enters the conversation when **all** finish. Don't poll — keep working or wait for the batch-complete message.

## Three failure modes that kill large fan-outs (all seen live)

1. **HTTP 429 from simultaneous bursts.** Two flavors, same cure. (a) Web-search: N subagents firing `web_search` at the same instant trips the search-backend QPS limit → abort after 3 retries. (b) Model endpoint: with a custom/self-hosted LLM endpoint, N children starting at once can trip the *provider's* rate limit instead — the child dies on its very first API call (`api_calls=1`, fails in ~5s, "Custom endpoint rate-limited every one of 3 attempts"), while children that already got a slot survive fine. Neither is the agent concurrency cap — raising `max_concurrent_children` does not help and makes both worse.
   - **Fix:** fan out in **small batches** (2–3 at a time) instead of all N at once, and tell each subagent to **space its queries** (1–2 `web_search` calls per iteration, wait between, prefer a few high-quality queries over a parallel burst). A 10-city job → 2 batches of 5, or 3 batches of 3–4, works reliably; for tight LLM endpoints even fewer.
2. **Summary truncation past ~1300 chars.** A subagent's final answer is truncated by the parent if it exceeds ~1300 chars (head+tail windowed, full text saved to a host file the sandbox can't always read). Long, verbose "summary + what I did" answers get cut mid-list → you get 5 of 10 items and can't recover the rest.
   - **Fix:** instruct each subagent in its `goal` that the **final answer must stay under ~1300 characters**: output ONLY a numbered list, one line per item (`N. <headline> — <Source> — <date>`), no URLs, no intro, no "what I did" paragraph. Compact answers never truncate.
3. **Degenerate final answer (repetition loop / stream cut).** A child can fall into a repetition loop while composing the final response — most often while mechanically counting/shortening characters to fit the output cap — and the stream is cut mid-loop, discarding the ENTIRE response even though the actual work (e.g. a research file) is already fully on disk.
   - **Prevention:** instruct the child to write the final answer in ONE pass — no character counting or iterative shortening; if it is too long, drop lines.
   - **Recovery:** on such a failure, first check the on-disk deliverable (section headers + tail); if it is complete, use it and do NOT re-dispatch the whole lane.

## Working recipe (verified)

- **First batch:** dispatch the N items (or first 2–3). Watch the batch-complete message.
- **On 429 / truncation:** re-dispatch the FAILED items only, in **smaller batches** (ideally one at a time, staggered after the main batch ends) and with the **compact-output** instruction above. Don't re-run the ones that succeeded.
- **Re-dispatch as seeded follow-ups, not clones:** the sibling results that arrived first usually confirm facts that shrink the failed task's scope. Re-dispatch with those verified facts in `context` and a *narrowed* goal (only what's still missing) instead of re-asking the original broad question — cheaper, faster, and it can't contradict the siblings.
- **Don't dispatch the follow-up while the batch is still running** unless you're sure the failed child's slot is gone; otherwise you duplicate work when the batch-complete message shows siblings that later succeeded, and you add load to the endpoint that just rate-limited you.
- **On a subagent timing out** (`Non-streaming API call timed out after 90s`): re-dispatch that one alone; it's often transient.
- **Live control:** while children run, `delegate_task(action='list')` shows status + `running_seconds`; `action='steer'` + `subagent_id` to redirect one; `action='stop'` to end early.
- **Verify before trusting a claim:** a subagent reporting "done/10 items" is a self-report. If the consolidated result is missing items or the summary says it was truncated, re-dispatch — don't present a partial set as complete.

## Single long-running workstream (not a fan-out — user preference)

`delegate_task` is not only for N-item fan-outs. When ONE workstream contains blocking commands that run for minutes — SSH deploys, container start + readiness polling, large builds, bulk migrations — run it in a **background subagent** instead of the main session's terminal: a long foreground `terminal` call holds the WebUI/CLI turn open and the UI appears frozen. The user has asked for this explicitly ("long scripts block the WebUI — offload them to subagents"); treat it as a standing preference. The subagent gets its own terminal session; the parent ends its turn with a one-line status and picks up the completion message. Before dispatching, verify the actual partial state yourself with quick bounded commands (the subagent has no conversation history), then dump that verified state + exact commands + done-criteria into its `goal`; tell it to capture real verification output and to report blockers honestly instead of guessing. Never put secrets in the goal — point at a credentials file and instruct it not to print the values.

## Pitfalls

- **Hard concurrency cap: `max_concurrent_children` (observed value: 3).** `delegate_task` rejects a batch with "Too many tasks: N provided, but max_concurrent_children is 3". For N>3 items, split into multiple `delegate_task` calls (batches of ≤3, sequential or overlapping) — the cap is per call, not per session.
- **Two-phase kanban triage fan-out (create in parallel, wire once at the end):** N subagents each create a small set of kanban cards (CLI `hermes kanban create`, parked in `triage`, NOT dispatched), each returns only its `ID | Titel` list. Then a FINAL single subagent derives and enters the parent→child dependency links across ALL created cards (it reads the card bodies to verify each hypothesized edge). Wiring needs the complete ID set, so it can't be parallel — it runs after both create batches finish.
- **Subagents can't `write_file` to `/tmp`** — the write-safe root is typically `/opt/data:/workspace`. Card bodies and temp docs must go under `/workspace/...` (e.g. `/workspace/tmp-kanban/`, cleaned up afterwards). On `/tmp` they hit "Write denied: outside HERMES_WRITE_SAFE_ROOT" and waste calls.
- **write_file → terminal sync delay:** a file just written via `write_file` may not be visible to a subsequent `terminal` call in the same step (observed: a subagent's `$(cat body.md)` picked up an empty file and created kanban cards with empty bodies). Verify the file exists and has content (`wc -c` / `head`) BEFORE passing it to a command. If a card was created with an empty body: `kanban edit` does NOT set the body of a live card — archive the card and recreate it (the idempotency key stays reusable).
- **Don't raise agent concurrency to fix 429s.** The bottleneck is the search backend's rate limit, not agent slots. More parallel agents = more simultaneous queries = more 429s.
- **Batching beats everything.** 2–3 staggered subagents with spaced queries reliably avoids 429; N-at-once does not, no matter the concurrency cap.
- **Always cap output size in the goal** for fan-outs — verbose subagent summaries truncate and you lose the tail items with no way to recover from the sandbox.
- Each subagent sees **only its own `context`/`goal`** — pass the shared constraints (date, "no invented data", language) into every task entry; they don't share the main conversation.
- **No template-marker-looking tokens in `goal`/`context` — angle brackets AND curly braces.** `delegate_task` rejects any text that looks like an unexpanded template marker with "unexpanded template marker" and the whole spawn call fails. This catches `<la la la>`-style example tokens AND shell formatting strings with curly braces — e.g. curl's `-w '%{http_code}'` write-out syntax triggered the rejection on a spawn whose goal quoted the curl command. Phrase such tokens in plain words ("use curl's `-w` flag with the http_code variable") or quote the whole command as an opaque string the subagent may adapt.
- **Deep-research fan-outs: give every child a fixed output contract** (report language, per-claim source URLs, evidence-strength ranking like strong/anecdotal/unverified, a `output_schema` with findings+recommendations). It makes the consolidated result directly mergeable into one report without re-reading transcripts.
