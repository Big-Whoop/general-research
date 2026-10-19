---
name: hermes-project-bootstrap
description: "Use when bootstrapping a new Hermes project end to end."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [project, bootstrap, git, github, kanban, desktop]
    related_skills: [sandbox-git-repos, peters-github, hermes-kanban-workers]
---

# Hermes Project Bootstrap

The user's standard ("das Übliche") setup for a new project: local repo
under `/workspace/dev/repos/ours/`, upstream GitHub repo, research archive
under `.hermes/`, 2-lane kanban board, desktop project.

## Standing conventions

- **Language split:** project docs (README, spec, code, commit messages) in
  English; research results stay in the language they were produced in
  (usually German). Never translate research into the repo.
- **Private by default (Peter, 2026-10-17):** the GitHub repo is PRIVATE
  unless Peter explicitly says public. Public is the exception — never
  assume it, never ask preemptively; just create private and report it.
- **MIT license** unless told otherwise; state it in the report so it can
  be changed.
- **No spec at bootstrap:** the project spec happens in a separate session.
  Bootstrap = scaffold + research archive only. The board starts empty.

## Procedure

### 1. Local repo

```bash
mkdir -p /workspace/dev/repos/ours/<name> && cd /workspace/dev/repos/ours/<name>
git init -b main
git config --global --add safe.directory /workspace/dev/repos/ours/<name>
```

Kebab-case name; public Hermes plugins use the ecosystem prefix
`hermes-<name>` (matches hermes-plan-mode, hermes-dynamic-workflows, ...).
safe.directory is required for every new repo (sandbox-git-repos).

### 2. Research archive under `.hermes/`

Layout: `.hermes/README.md` (English index) +
`.hermes/research/<YYYY-MM-DD>-<topic>/` containing `REPORT-*.md`, `lane*.md`
(rename consistently: `lane1-<topic>.md` ...), `ledger.json`, screenshots.

- Commit PROCESSED results only (reports, lane files, ledgers, screenshots).
  NEVER raw dumps — source-code copies, cached doc pages, JSON API dumps are
  intermediate artifacts and bloat the public repo (observed: 4.8M source
  copies + 950K JSON dumps left out of a ~200K results set).
- Copy from the scratch locations (`/opt/data/cache/scratch/...`,
  `/opt/data/research/`) into the repo.
- Research done directly in chat (no lane files) gets its own note file in
  the same layout, so the archive is complete.

### 3. README + LICENSE

Root `README.md` (English): what the project is, status (pre-spec if
pending), pointer to `.hermes/research/`, board name, workflow line
(card → worktree → branch → PR → reviewer merge), key findings in short
form. `LICENSE`: MIT, `Copyright (c) <year> Peter Fahsel`.

### 4. Secret scan BEFORE any public push

Recipe: `references/pre-public-scan.md`. Read every hit — the case-
insensitive `sk-` pattern false-positives on words like "task-Completion".
Only real secrets (keys, tokens, internal IPs/URLs) block the push; internal
names get flagged in the report and the user decides.

### 5. Commit + public repo

```bash
git add -A
git -c user.name="Peter Fahsel" -c user.email="peter.fahsel@gmail.com" commit -m "Initial commit: ..."
gh repo create <name> --private --source . --push
```

Verify with `gh api repos/Big-Whoop/<name> --jq .private` → `true`
(`false` only if Peter explicitly asked for a public repo).
Auth details: peters-github.

### 6. Kanban board (2-lane)

Create per hermes-kanban-workers §1: `boards create <slug> --name ... \
--description ... --icon ... --color ... --default-workdir \
/workspace/dev/repos/ours/<name> --switch`. slug = repo name; the
description carries the repo URL + "2-lane: default/reviewer". Verify the
`default` + `reviewer` profiles exist (`hermes profile list`) before
creating. No cards at bootstrap — the spec session seeds them.

### 7. Desktop project

`desktop_project` tool: `action=create, name=<human name>, path=<repo dir>`.
Creating switches the current chat into the project (intended — the chat
anchors to the repo).

## Report shape

Short, structured: repo (URL + visibility verified), what was committed under
`.hermes/` and what was deliberately left out, board (slug, lanes), desktop
project (id), next step (spec in separate session). Note that `--switch` made the
new board the CLI's current board — the Kanban UI keeps its own board selection,
so the user may see the new board in the UI while looking at a different project
(prevents "where did my other board go" confusion).

## Pitfalls

- **Kanban UI shows board A's label with board B's cards** (observed after a
  bootstrap `--switch`): that is an OLD desktop app build (pre-#20879 fix) whose
  card fetch omits `?board=` and falls through to the CLI `current` pointer —
  NOT data loss. Verify the data read-only first (each board's `kanban.db`, live
  API `GET /api/plugins/kanban/board?board=<slug>`), then update the desktop app
  (fixed in the 2026-10-15+ dev build).
