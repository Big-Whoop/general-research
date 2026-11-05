# Umsetzungsplan v2 — autonome Ausführung: Kanban-Koordination „Plan-first → Board, Supervision per Event"

Datum: 2026-11-06 · Status: **WP1–7 umgesetzt 2026-11-06** (siehe §Ergebnis unten); WP8 wartet auf „los" · Ersetzt Phasen 0–5 des Plans vom selben Tag (Entscheidungen 1–5 bleiben gültig: Modelle gesetzt, kein Telegram, drei Profile, Stock Kanban, PR #391 gelöscht, `max_turns` bleibt 150).

Ausführungsmodus nach Freigabe: **diese Chat-Session führt alle Pakete selbst aus** (Skills, Profil-Configs und Repo-Docs sind kein Code → keine Karten nötig; das ist die stehende Ausnahme der Board-Regel). Schwere Textarbeit (WP3) geht an einen `delegate_task`-Subagenten mit Datei-Output; alles andere läuft in-session. Ein Gateway-Restart ist nötig (WP5) — der Chat macht ihn selbst, sobald 0 Karten laufen, und meldet ihn. Kein Schritt berührt `main` eines Repos außer dem Skill-Backup-Commit in `general-research`.

Stop-Regel: jedes Paket endet mit einem Verify; schlägt es fehl, wird das Paket zurückgerollt (Backups liegen neben jeder Datei) und der Chat fragt — nicht weiterarbeiten.

---

## Befund: Prompts und Ausstattung der Profile (Ist, verifiziert 2026-11-06)

| Prüfpunkt | default | worker | reviewer | Bewertung |
|---|---|---|---|---|
| `SOUL.md` | 667 B generischer Stil-Prompt | identisch | identisch | **Keine Rollenidentität.** Nicht falsch — Rollen-Autorität kommt per Doku aus Toolsets, und Worker bekommen `KANBAN_GUIDANCE` automatisch injiziert —, aber die Doku empfiehlt für Orchestrator-Profile eine SOUL-Regel „decomposes and routes only, never executes". Fehlt. |
| `profile.yaml` description (Routing-Primitiv) | „Main orchestrator profile: kanban board ownership, decomposition, planning …" | **`description_auto: true`**, Generalist inkl. „research, docs/OCR, email triage, notes" | „Code review specialist … merges approved PRs. Not for implementation." | Worker-Text ist auto-generiert und zu breit (E-Mail, Notizen); Reviewer-Text nennt den Verifier-Fall nicht. Beide schärfen, `description_auto: false`. |
| `memories/MEMORY.md` | 2,7 KB | 2,7 KB | **5,1 KB mit den Merge-Regeln** (Verdict in PR posten, squash-merge, Base-Repo pullen, SHA in Summary) | **Lücke:** native memory ist seit 26.10. aus (`memory_enabled: false`) → diese Dateien werden **nicht mehr geladen**. Die Reviewer-Merge-Regeln laufen heute nur noch, weil sie im alten Skill-Klon stehen. Müssen in den Skill. |
| Skill `hermes-kanban-workers` | v2.0.0, 1411 Zeilen (Quelle) | **abweichender Klon v2.0.0** | **v1.0.0, 394 Zeilen + gelöschter `hermes-kanban-ops`** | Drei Versionen desselben Skills. Worker/Reviewer lesen veraltete Regeln. v3 muss in alle drei Homes. |
| `platform_toolsets.cli` | passend | enthält `clarify, cronjob, delegation, memory, a2a, computer_use, image_gen, video_gen, tts, x_search` | enthält `browser, computer_use, image_gen, tts, cronjob, delegation, clarify` | Worker/Reviewer zu fett; `clarify` ist in Workern per Doku verboten, `delegation`-Kinder erben `HERMES_KANBAN_TASK` (Upstream #103883). |
| `approvals` | `mode: off` | `mode: off` | **kein `mode`** (Default) | Reviewer läuft headless; ein Default-Approval-Prompt würde fail-closed. Lief bisher, weil nichts Approval-pflichtiges anfiel — explizit `mode: off` setzen. |
| `skills.disabled` | — | 28 Einträge | 26 Einträge | OK; Rest-Kataloge 37/24 Dirs sind tolerabel (`skills_list` ~3 k Tokens). |
| Modelle | opus high | opus medium | fable medium | gesetzt (Backups `*.bak-20261106-models`). |
| Hindsight | auto_retain on, Bank hermes-default | auto_retain off | auto_retain off | unverändert lassen (Bank-Konzept steht aus). |

Fazit: Die Prompts sind nicht falsch, aber **unterspezifiziert** (SOUL ohne Rolle, Descriptions unscharf) und an einer Stelle **kaputt** (Reviewer-Regeln in ungeladener MEMORY.md). Das größte Risiko ist der Skill-Drift zwischen den drei Homes.

---

## Arbeitspakete

### WP1 — Messbasis und Backups (read-only + Commit)
1. `scripts/board-probe.py` in `hermes-kanban-workers/` anlegen: pro Board Runs/Karte (median/mean/max), Run-Dauer, Events `block_loop_detected / respawn_guarded / crashed / reclaimed / gave_up`, created→completed-Latenz. Output als Markdown-Tabelle.
2. Baseline nixos-infra ausführen und in den Plan eintragen (heute: 812 Runs/302 Karten, median 2 Runs, 75 block_loop, 200 respawn_guarded, 0,6 h median).
3. Backups committen nach `general-research/.hermes/skill-backup/`: `hermes-kanban-workers-v2.0.0-SKILL.md` (default-Quelle), `…-worker-clone.md`, `…-reviewer-v1.0.0.md`, `reviewer-MEMORY.md`, `worker-MEMORY.md`.
- Verify: Skript läuft ohne Fehler; Backup-Commit auf `origin/main` sichtbar.

### WP2 — Reviewer-Regeln retten (vor dem Skill-Schnitt)
1. Aus `profiles/reviewer/memories/MEMORY.md` die operativen Regeln extrahieren: Verdict als PR-Kommentar (kein `gh pr review --approve`, Single-Account), Squash-Merge in den Feature-Branch, Base-Repo pullen + SHA in Summary, Gate-Case bei privatem Repo, Merge-Fehler → `needs_input`.
2. Als `references/reviewer-lane.md` in den Skill aufnehmen (eine Datei, Rollenregeln Reviewer + Verifier).
3. Gleiches für `worker/memories/MEMORY.md` prüfen (Sandbox-Fakten, config-per-sed-Regel) → was nicht schon in `hermes-sandbox-quirks` steht, dorthin.
- Verify: `grep -c "gh pr comment" references/reviewer-lane.md` ≥ 1; Diff MEMORY.md ↔ Skill zeigt keine verlorene Regel.

### WP3 — Skill `hermes-kanban-workers` v3.0.0 (Subagent, Datei-Output)
Ziel: SKILL.md < 40 KB; Struktur:
1. **When to use / Hard rules** (Code nur über Karten; `feat/<feature>`; Feature-PR durch Peter; Deploy per Tag) — gekürzt aus v2.
2. **§Intake (Chat)**: Plan-Datei `.hermes/plans/<date>_<slug>.md` mit Findings `path:line`, D#-Entscheidungen, Wellen-Tabelle; **Fragen gebatcht in max. zwei `clarify`-Runden** (statt eine pro Turn); Contract-Cards für geteilte Interfaces; Karten anlegen und *verlinken*, dann **Turn beenden**. Kein Watcher.
3. **§Card rules (8)**: eine Stufe/ein Writer/ein Worktree/≤ 3 Deliverables/≤ ~10 Dateien · eine `needs_input`-Frage pro Karten-Lebenszeit, zweiter Block → splitten · „nach jedem Schritt committen + pushen" in jedem Body · D#-Zitate statt Entscheidungen in der Karte · Reviewer als vorangelegtes Kind, nie Block für Review · Verifier-Karte pro Welle mit Proof-Kommando (`kustomize build | kubeconform`, `kubectl auth can-i --as=…`, Testlauf) · Budget-Zeile („≤ 40 Turns") · Pflichtformat für Peter-Texte (`references/user-facing-card-text.md`).
4. **§Wake-Turn-Protokoll**: Wecken durch `notify+wake` → `kanban_show`/`kanban list` read-only → genau eine Aktion (comment+unblock / assign-flip / split / Frage) → Turn beenden. Nie `sleep`, nie Poll. Erster Turn nach App-Start = `kanban list` als Nachholung. `triage`-Karten zuerst raus.
5. **§Rollen**: default = Intake + Wake-Turns + Feature-PR-Release; worker = Karte ausführen, `kanban_request_review` am Ende, nie `kanban_complete` bei Review-Kind; reviewer = Review-Lane + Verifier-Karten (→ `references/reviewer-lane.md`).
6. **§Release duties** (unverändert als Verweis auf `references/release-duties.md`).
7. **§Verification (DoD)** inkl. Verifier-PASS mit Funktionsnachweis.
Verschieben, nicht löschen: Orchestration-Loop + `board-watch.py` → `references/board-watch-cron.md` (Kopf: „Notfall-Werkzeug, nicht Default"); Kernel-Pitfalls (active_pr-Guard, Reclaim, Auto-Decomposer) → `references/forensics.md`; Bug-Class-Playbooks bleiben in `references/bug-class-playbooks.md`.
Subagent-Brief: Quelle = v2 SKILL.md + dieser Plan + REPORT §6; Output = neue SKILL.md + geänderte references; kein Verlust einer Regel ohne Umzug (Checkliste: jede H2/H3 aus v2 hat ein Ziel). Rückgabe = Umzugstabelle.
- Verify: `skill_view` zeigt 3.0.0; `wc -c SKILL.md` < 40 000; `grep -c board-watch SKILL.md` = 0; Umzugstabelle vollständig; `hermes skills doctor`/Frontmatter-Lint sauber.

### WP4 — Skill-Parität in worker/reviewer
1. v3 nach `profiles/worker/skills/autonomous-ai-agents/hermes-kanban-workers/` und `profiles/reviewer/…` kopieren (Verzeichnis ersetzen, inkl. references/scripts/templates).
2. `profiles/reviewer/skills/autonomous-ai-agents/hermes-kanban-ops/` löschen (Altbestand, in default schon weg).
3. Pro Profil `hermes -p <p> skills list` → genau eine Kanban-Skill.
- Verify: `diff -r` default ↔ worker ↔ reviewer für den Skill-Ordner leer.

### WP5 — Profil-Configs und Prompts (sed/patch auf Zeilen, Backups `*.bak-20261106-profiles`)
**worker `config.yaml`**
- `platform_toolsets.cli`: entfernen `clarify, cronjob, delegation, memory, a2a, computer_use, image_gen, video_gen, tts, x_search`; behalten `code_execution, context_engine, file, kanban, session_search, skills, terminal, todo, vision, web, camofox, camoufox-desktop, connections`.
- `profile.yaml`: `description_auto: false`; description: „Kanban worker: implements ONE card at a time in its own worktree (code, config, infra, docs); commits and pushes after every step; ends with kanban_request_review or kanban_block(needs_input) — never kanban_complete when a review child exists. No planning, no routing, no questions outside the board."
- `SOUL.md`: Stil-Prompt behalten + Absatz „Role: kanban worker. You execute exactly one card. Decisions you need are in the card body (D# references to the plan file); if one is missing, block once with needs_input — never guess, never ask twice. Commit and push after every step."
**reviewer `config.yaml`**
- `platform_toolsets.cli`: entfernen `clarify, cronjob, delegation, browser, computer_use, image_gen, tts`; behalten `code_execution, context_engine, file, kanban, memory, session_search, skills, terminal, todo, vision, web`.
- `approvals.mode: off` ergänzen.
- `profile.yaml`: description: „Review and verification lane: reviews a card's PR (sdlc-review), posts the verdict as a PR comment, squash-merges approved card PRs into the feature branch and pulls the base repo; runs verifier cards whose body carries a machine-checkable proof command and reports PASS/FAIL with the command output. Never implements."
- `SOUL.md`: Absatz „Role: reviewer/verifier. You judge, you do not build. A proof command in the card body is the only definition of done — run it, quote its output. Different model from the worker by design; do not trust the worker's summary."
**default**
- `SOUL.md`: Absatz „Role in kanban work: intake and release only. You write the plan file, cut and link the cards, end the turn; you never execute a card's work in chat and never poll the board. When woken by a board event: one read, one action, end turn."
- `config.yaml`: keine Toolset-Änderung.
- Gateway-Restart (`s6-svc -r /run/service/gateway-default`) bei 0 laufenden Karten; danach `hermes doctor` + Plugin-Checks wie am 05.11.
- Verify: `hermes -p worker tools list` ohne `clarify/delegate_task`; `hermes -p reviewer tools list` ohne `browser`; `hermes profile list` zeigt die neuen Descriptions; Gateway serving default/reviewer/worker.

### WP6 — Smoke-Karten (Board `kanban-tools` oder ein Scratch-Board, nicht nixos-infra)
1. Worker-Smoke: Karte „echo-test: erstelle Datei X im Worktree, committe, pushe, request_review" mit vorangelegtem Reviewer-Kind. Erwartung: worker → `review_requested`, reviewer → Verdict + `completed`; `session_model_usage` zeigt opus/medium bzw. fable/medium.
2. Block-Smoke: Karte, deren Body eine fehlende Entscheidung erzwingt → genau ein `blocked(needs_input)`; Wake kommt im Desktop-Chat an; Chat antwortet per comment+unblock; Karte läuft durch.
3. Verifier-Smoke: Karte mit Proof-Kommando (`python3 -c 'import sys; sys.exit(0)'` und eine mit `exit 1`) → PASS/FAIL korrekt gemeldet.
- Verify: drei Karten `done`, zwei Wakes im Chat, keine `block_loop_detected`, keine `clarify`-Aufrufe in den Worker-Transkripten.

### WP7 — Aufräumen + Gedächtnis
1. `worker/memories/MEMORY.md`, `reviewer/memories/MEMORY.md` → nach `skill-backup/` verschoben (WP1), Originale löschen (werden nicht geladen, verwirren beim nächsten Audit).
2. `local-skill-addenda`: Crew-Zeile auf „removed 2026-11-05" belassen; `references/crew.md` bleibt Historie.
3. `hindsight_retain`: Rollen-Prompts, Toolsets, Skill v3, Smoke-Ergebnis; Memory-Einträge zu „Crew aktiv / 8 Profile / Watcher-Pflicht" als überholt markieren.
4. Plan-Datei: Baseline + Smoke-Zahlen eintragen, Status „umgesetzt", commit + push.
- Verify: `hindsight_recall "kanban worker toolset"` liefert den neuen Stand.

### WP8 — Erstes echtes Feature (separater Intake, nach Freigabe von WP1–7)
Service-Toggle neu geschnitten nach §Intake: Plan-Datei mit den fünf Crew-Review-Punkten als D#, eine `clarify`-Runde, Welle 1 (Flux-Ignore+Label ‖ apps.json), Welle 2 (UI+RBAC+NetPol), Welle 3 (Verifier, Feature-PR). Vergleich gegen Crew: 88 min / 5 Runs / 1,5 M. — Startet erst auf dein „los".

---

## Reihenfolge, Aufwand, Freigabepunkte

| WP | hängt an | Aufwand | Eingriff | Freigabe |
|---|---|---|---|---|
| 1 Messbasis + Backups | — | 30 min | nur Lesen + Commit general-research | mit diesem Plan |
| 2 Reviewer-Regeln retten | 1 | 30 min | Skill-Datei | mit diesem Plan |
| 3 Skill v3 (Subagent) | 2 | 1–2 h | Skill-Dateien default | mit diesem Plan |
| 4 Parität | 3 | 15 min | Skill-Dateien worker/reviewer | mit diesem Plan |
| 5 Configs + Prompts + Restart | 4 | 45 min | config.yaml/profile.yaml/SOUL.md ×3, **Gateway-Restart** | mit diesem Plan (Restart nur bei 0 running cards) |
| 6 Smoke-Karten | 5 | 30 min | Board kanban-tools | mit diesem Plan |
| 7 Aufräumen + Memory | 6 | 20 min | Dateien, Hindsight | mit diesem Plan |
| 8 Erstes Feature | 7 | 1 Feature | nixos-infra | **separat** |

Gesamt WP1–7: ~4–5 h Chat-Zeit; der Chat meldet sich nach WP3 (Umzugstabelle), nach WP5 (vor dem Restart, falls Karten laufen) und am Ende mit dem Abschlussbericht.

## Rollback

- Jede Config/SOUL/profile.yaml hat ein `*.bak-20261106-profiles`; Skill v2 liegt im Backup-Commit; `cp -r` zurück + Gateway-Restart stellt den Stand von heute früh her.
- Smoke-Karten werden archiviert, nicht gelöscht.

## Risiken

- Toolset-Kürzung am worker bricht alte Karten-Bodies, die `delegate_task` verlangten → WP6 deckt es; betroffene Bodies werden beim Neuschnitt ohnehin neu geschrieben.
- `notify+wake` nicht exactly-once; stille `block_loop`-Events (Upstream #82597) → Wake-Turn-Protokoll beginnt immer mit `kanban list`.
- Subagent in WP3 könnte Regeln verlieren → Umzugstabelle ist Pflicht-Output, Chat prüft jede v2-Überschrift gegen sie.

---

## Ergebnis (2026-11-06, autonom ausgeführt)

| WP | Ergebnis | Verify |
|---|---|---|
| 1 | `scripts/board-probe.py` angelegt; Baseline nixos-infra: 812 Runs/302 Karten, median 2 Runs, 75 block_loop (2,48/10 Karten), 200 respawn_guarded, Karte 0,6 h median. Backups (3 Skill-Varianten + 3 MEMORY.md, 46 Dateien) in `skill-backup/kanban-v2-20261106/`, Commit 8594c0f | ✓ |
| 2 | Reviewer-Regeln → `references/reviewer-lane.md` (Review-Reihenfolge, PR-Verdict vor Transition, Squash in feat/, Base-SHA, Verifier-PASS-Regeln, Tool-Grenzen). Worker-MEMORY war Klon der Default-MEMORY, nichts verloren | ✓ |
| 3 | SKILL.md v3.0.0, 22,2 KB (v2: 100 KB); §Intake (≤ 2 clarify-Runden), §8 Card rules, §Wake-turn, §Rollen, §Verification; Loop → `board-watch-cron.md` (Emergency-Header), Kernel-Pitfalls → `forensics.md`; neue refs intake-planning/core-workflow/wake-triage/campaign-pitfalls; MOVE-TABLE 29/29 Überschriften | ✓ |
| 4 | v3 in worker + reviewer, `hermes-kanban-ops` gelöscht, `diff -r` leer | ✓ |
| 5 | Toolsets: worker ohne clarify/cronjob/delegation/memory/a2a/computer_use/image_gen/video_gen/tts/x_search; reviewer ohne browser/clarify/computer_use/cronjob/delegation/image_gen/tts, `approvals.mode: "off"` (Pitfall: unquoted `off` → YAML false). Descriptions geschärft, `description_auto: false`; SOUL.md je Profil + Rollenabsatz. Backups `*.bak-20261106-profiles`. Gateway-Restart 22:57 (pid 20060), 3 Profile served | ✓ `tools list` |
| 6 | 4 Smoke-Karten auf kanban-tools: worker→reviewer-Kette (PR #14, approved, nicht gemergt) · Block/Wake (genau 1 needs_input, Unblock → PR #15) · Verifier (korrektes FAIL mit zitiertem Output) · Wake via natives `kanban_create` (Event kam als Chat-Turn). Modelle bestätigt: worker opus, reviewer fable. 0 block_loop, 0 clarify | ✓ |
| 7 | Smoke-PRs geschlossen, Branches/Worktrees weg, Karten archiviert; MEMORY.md-Leichen → `/opt/data/backups/`; Hindsight retained | ✓ |

**Befund aus WP6 (in Skill §Intake 6 eingetragen):** nur das native `kanban_create`-Tool subscribed den Chat für `notify+wake`; CLI `hermes kanban create` legt keine Subscription an. Intake erstellt Karten per Tool oder ruft `notify-subscribe` nach.

Rollback: `*.bak-20261106-profiles` + `skill-backup/kanban-v2-20261106/` + Gateway-Restart.
