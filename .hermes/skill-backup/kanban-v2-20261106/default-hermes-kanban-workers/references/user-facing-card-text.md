# User-facing text on cards — MANDATORY FORMAT

Applies to: needs_input blocks, completion summaries, PR descriptions, worker
instruction blocks, card templates. The user reads these on the board/GitHub
without the card body or the chat. Previous cards were cryptic or incomplete
(missing URLs, "create it in the usual place"). Every worker instruction block
and every card template MUST carry this rule, and the orchestrator checks
summaries against it before archiving a card:

- First line is one of exactly two headings: `Für Peter zu tun:` (steps the
  user performs) or `Entscheidung nötig:` (a pick) — never mixed; two blocks
  if both apply.
- Steps are numbered. Each step names WHERE (complete URL, or absolute path
  + host, or UI menu path), WHAT exactly (full copy-pasteable one-line
  command or exact value/name — no placeholders except dates), and HOW TO
  VERIFY (the exact command and the expected output).
- Decisions: numbered options, one marked recommended with one sentence why,
  free-text answer explicitly allowed.
- No card ids, PR numbers, or abbreviations without the full term next to
  them; no "as discussed" / references to chat; no "the usual" anything.
- State what happens if the user does nothing (e.g. "until step 1 the
  cluster stays on the pre-merge state — intended").
