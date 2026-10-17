# .hermes — Project Archive

Research archive for the general-research project.

## Layout

- `research/<YYYY-MM-DD>-<topic>/` — one directory per research topic
  - `REPORT-*.md` — processed results (reports)
  - `lane1-<topic>.md`, `lane2-<topic>.md`, ... — per-lane research notes
  - `ledger.json` — source ledger (where each fact came from)
  - screenshots — supporting images

## Rules

- Only PROCESSED results are committed (reports, lane files, ledgers,
  screenshots). Raw dumps (source-code copies, cached doc pages, JSON API
  dumps) are intermediate artifacts and never committed.
- Research results stay in the language they were produced in (usually
  German); this index stays in English.
- Research done directly in chat (no lane files) gets its own note file in
  the same layout, so the archive stays complete.
