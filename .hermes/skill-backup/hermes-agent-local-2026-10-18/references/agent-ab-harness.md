# Agent A/B harness — comparing model parameter variants on agentic tasks

Class: "does parameter X change agent behavior?" (temperature, reasoning_effort, …) on a tool-using task. Proven on Qwen3.8-27B via ryzen/llama-swap (2026-10-10, 40 runs). Parameter variants run as cloned profiles (see SKILL.md "Per-instance sampling params"); this file is the harness around them.

## Task design

- Self-gradable: objective success signal (e.g. pytest 6/6), not interpretation.
- Reproducible: identical starting copy per run.
- Agent-shaped: several turns, tool use (read/execute/patch/verify).
- No side effects: runs in a scratch dir, never infrastructure.
- Plant N real bugs + red herrings (unused TODO, misleading docstring note) — the red herrings test whether higher temperature starts "fixing" things that are not broken.
- Require a machine-readable final line, e.g. `RESULT: <changed-lines> <reason>`.

## Harness (load-bearing parts)

- Shared `src/` with the buggy project; per-run `runs/<profile>-r<rep>/` copies.
- **`src/` read-only (0o555 dir / 0o444 files) + SHA256 integrity hash checked after EVERY run**; on violation: restore from in-memory pristine copies + flag `src_violated` in results.
- Runner: copy src → run dir, `hermes -p <profile> chat -q "<task>"` with cwd = run dir, then evaluate: pytest result, `diff -u` size vs src, protected files touched?, src hash, session stats.
- **Prompt names the run dir by ABSOLUTE PATH** ("Im Verzeichnis /abs/path liegt …") — never "aktuelles Arbeitsverzeichnis" (see pitfalls).
- Metrics per run: success (binary), diff size (minimality), protected-file violations, consecutive identical tool calls (loop indicator), in/out/reasoning tokens, wall time.

## Pitfalls (each cost a full re-run)

- **The agent will patch the shared source, not its run copy** — if `src/` is writable, one run silently fixes it and every later run inherits the fixed code ("6 passed" with `diff=+0/-0` is the tell). Read-only + integrity hash is the only reliable guard; the prompt alone is not.
- **"aktuelles Arbeitsverzeichnis" in the prompt is ambiguous** — the profile's config may declare a different cwd than the process actually runs in, and several project copies are visible. Observed failures: agent investigated the harness instead of the task, or patched the PREVIOUS run's dir and claimed success. Absolute path in the prompt eliminated all of it (28/28 success after the fix).
- **`shutil.copytree` inherits the read-only DIRECTORY mode** — chmod the run dir to 0o755 (and files 0o644) after copying, or every patch silently fails and the agent works around it (copies the project elsewhere, or hallucinates success).
- **Verify file state, never the agent's claim.** Observed: agent reported "6 passed, nothing to change" while 3 tests failed; patch tool (temp-file + rename) fails silently in a read-only dir and the agent reports success anyway. The harness's own pytest + diff is the only ground truth.
- **Session stats live in the profile's `state.db`, not JSONL transcripts**: `sessions` table (`started_at` is a UNIX epoch float, `input_tokens`/`output_tokens`/`reasoning_tokens`/`api_call_count`/`tool_call_count`), `messages` table (`tool_calls` JSON per assistant row) — for tool-call sequences and consecutive-repeat (loop) detection. Match the session by `started_at >= run_start_epoch`.
- **n=3 per cell is not enough** — the harness itself was the dominant failure factor at n=3; at n=7+ per cell it was 28/28. Budget ≥7 reps per variant, or report the harness failure rate separately from the parameter effect.
- **Prompt clarity beats parameter tuning**: the biggest quality delta in the whole experiment came from fixing the prompt (absolute path), not from any parameter. If a variant cell fails, check the harness before blaming the parameter.

## Findings worth starting from (Qwen3.8-27B, debugging task, reasoning_effort medium)

- Temperature 0.0/0.3/0.7/1.0: identical success, identical minimal patch, no loops, no verbosity difference (the t=1.0 "verbosity" seen in an earlier run was the directory-ambiguity artifact, not the temperature).
- Conclusion for this model class: in t = 0–1 the parameter is quality-neutral on solvable tasks; pick 0.7 as default, 0.0 only for reproducible benchmarks.
