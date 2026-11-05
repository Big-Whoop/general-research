# Umsetzungsplan: Kanban-Koordination auf „Plan-first → Board, Supervision per Event" umstellen

Datum: 2026-11-06 · Status: Vorschlag, nichts umgesetzt · Grundlage: `.hermes/research/2026-11-06-coordination-model-kanban-bots-plan/REPORT.md`

## Ziel

Die Hauptsession plant bounded, schreibt ein Plan-Artefakt, legt verlinkte Karten an und beendet den Turn. Danach läuft die Welle ohne Chat-Beteiligung; der Chat wird nur durch Board-Events geweckt (`blocked/needs_input`, `review_requested`, Wellenende). Kein Watcher-Prozess, kein Poll, kein stehender Koordinator-Prozess. Crew-Mechanik (Budget-Stop, unabhängiger Proof, Retry-dann-Frage) wird als Regelwerk übernommen, nicht als Plugin.

## Was sich NICHT ändert

- Code nur über Karten; Karten-PRs → `feat/<feature>`; Feature-PR → `main` durch Peter; Deploy via Tag.
- `auto_decompose: false`, `orchestrator_profile: default`, `default_assignee: worker`.
- Profile default / worker / reviewer; Hindsight-Banks unberührt (Bank-Arbeit wartet auf das Konzept in `.hermes/decision/agent-memory/`).

## Phasen

### Phase 0 — Messbasis (½ h, read-only)
- `board-probe.py` (neu, unter `hermes-kanban-workers/scripts/`): pro Board Runs/Karte, Run-Dauer, `block_loop_detected`, `respawn_guarded`, created→completed. Heute nixos-infra: 812 Runs/302 Karten, median 2 Runs, 75 block_loop, 200 respawn_guarded, Karte 0,6 h median.
- Erfolgskriterium für den Umbau: nach zwei Features < 1 `block_loop_detected` pro 10 Karten, median ≤ 2 Runs/Karte, null Chat-Watcher-Prozesse.
- Verify: `python3 scripts/board-probe.py nixos-infra` läuft und druckt die Tabelle.

### Phase 1 — Skill-Umbau `hermes-kanban-workers` → v3.0.0 (1 Karte, docs-only, kein PR nötig: Skill liegt in `/opt/data/skills`)
Backup zuerst: `.hermes/skill-backup/hermes-kanban-workers-v2.0.0-SKILL.md` committen (Konvention wie bei der v2-Konsolidierung).

| Block heute | Aktion | Neuer Ort |
|---|---|---|
| Hard rule, Feature-Branch, Waves (113–363) | behalten, kürzen auf Regeln (Bug-Class-Playbooks sind schon in `references/bug-class-playbooks.md`) | SKILL.md §Intake |
| „Plan file first, questions one per turn" | **ändern**: Fragen *gebatcht* in max. zwei `clarify`-Runden vor der ersten Karte (Crew: ≤ 5); Plan-Datei + Decisions committen; danach Karten anlegen; **Turn beendet den Intake** | §Intake, Schritt 0 |
| Monitoring-Abschnitt + „In-session orchestration loop" (859–1149, ~20 KB) | **streichen** aus SKILL.md; `board-watch.py` bleibt als Notfall-Werkzeug in `references/board-watch-cron.md` mit Warnung | `references/board-watch-cron.md` |
| Pitfalls (1149–1445, ~22 KB) | **umschreiben** zu Kartenschnitt-Regeln (siehe unten); Kernel-Forensik nach `references/forensics.md` | §Card rules + references |
| Verification | ergänzen: Verifier-Karte pro Welle mit Proof-Kommando | §Verification |

Neue §Card rules (aus Lanes 1/3/4 + Crew-Probelauf abgeleitet):
1. **Eine Karte = eine Stufe, ein Writer, ein Worktree, ≤ 3 Deliverables, ≤ ~10 Dateien.** 27-Dateien-Karten sind der Kollaps-Fall.
2. **Eine `needs_input`-Frage pro Karten-Lebenszeit.** `BLOCK_RECURRENCE_LIMIT=2` ist Konstante, Zähler resettet nicht bei Antwort. Blockt eine Karte zum zweiten Mal → splitten, nicht antworten.
3. **„Nach jedem Schritt committen + pushen" steht in jedem Body.** Crew-Run 1: 54 min ohne Commit, beim Budget-Stop weg.
4. **Design-Entscheidungen stehen im Plan, nicht in der Karte.** Jeder Body zitiert die D#-Nummern aus `.hermes/plans/<date>_<slug>.md`; Worker entscheiden nichts, was zwei Karten betrifft.
5. **Reviewer als vorangelegtes Kind, nie `kanban_block` für Review.** Review-Zyklen zählen nicht gegen den Loop-Breaker.
6. **Verifier-Karte pro Welle** mit maschinellem Proof-Kommando im Body (`kustomize build | kubeconform`, `kubectl auth can-i --as=…`, Testlauf) — nicht „PR offen + CI grün". Modell ≠ Worker-Modell (Vier-Augen).
7. **Budget-Zeilen**: `agent.max_turns` pro Profil (heute 150) bleibt der Stop; Body nennt erwartete Größe („≤ 40 Turns"), Reviewer meldet Überschreitung als Finding.
8. **Wake-Turn-Protokoll**: beim Wecken erst `kanban_show`, dann genau eine Aktion (comment+unblock / assign-flip / split / Frage an Peter), Turn beenden. Nie `sleep`, nie Poll.

Verify: `skill_view` zeigt v3.0.0; SKILL.md < 40 KB; `grep -c board-watch SKILL.md` = 0 außerhalb der Notfall-Referenz.

### Phase 2 — Wake-Kanal statt Watcher (1 Karte, config + Probe)
- Prüfen, dass `kanban.auto_subscribe_on_create: true` (Default) greift: Desktop-Session, die `kanban_create` ruft, bekommt `notify+wake`.
- Telegram als Zweitkanal: `/kanban create` aus dem Telegram-Chat oder `kanban_notify-subscribe` auf die Feature-Root-Karte, damit Events auch bei geschlossenem Desktop ankommen (Toasts werden nicht nachgeliefert).
- Live-Probe mit einer Dummy-Karte: `blocked(needs_input)` → kommt der Wake im Chat an? `review_requested` → ja/nein? `block_loop_detected` → bekannt still (Upstream #82597) → als Known gap akzeptieren, Reviewer-Karte deckt es ab.
- Verify: drei Events, drei Wakes im Desktop-Chat, mindestens `blocked` + `completed` auf Telegram.

### Phase 3 — Profil-Ausstattung (1 Karte, config)
- **worker**: Modell bleibt Opus (User-Entscheidung Qualität); `platform_toolsets.cli` um `clarify`, `cronjob`, `delegation`, `memory` kürzen (Doku: Worker darf nicht fragen, nicht planen, nicht delegieren; Delegation-Kinder erben `HERMES_KANBAN_TASK`, Upstream #103883). `agent.max_turns` 150 → 100.
- **reviewer**: anderes Modell als worker (Vier-Augen; Kandidaten aus CPA: `claude-fable-5-1` oder `gpt-6.1-sol`); `platform_toolsets.cli` ohne `cronjob`, `delegation`, `clarify`; Terminal bleibt (Tests laufen).
- **Verifier**: kein neues Profil — Verifier-Karten laufen als `reviewer` mit Proof-Kommando im Body. Ein viertes Profil erst, wenn Proof-Laufzeiten den Reviewer blockieren.
- **default**: `kanban`-Toolset bleibt explizit; keine Änderung.
- Verify: `hermes -p worker tools list` zeigt die Kürzung; Smoke-Karte auf jedem Profil läuft durch.

### Phase 4 — Probelauf an einem echten Feature (die Karte, die Crew nicht geschafft hat)
PR #391 (service-toggle) als Vorlage neu schneiden, nicht mergen:
- Intake im Chat: Plan-Datei `.hermes/plans/2026-11-xx_service-toggle.md` mit den fünf offenen Punkten aus dem Crew-Review (abhängige Dienste, verwaiste llmp-Pods, cpl-IP in NetworkPolicy, zweistufiger Release, Schema-Check) als D#-Entscheidungen; eine `clarify`-Runde.
- Welle 1 (parallel, disjunkte Dateien): Flux-Replica-Ignore + Label; `apps.json` + Warntexte. Welle 2: UI + RBAC + NetworkPolicy. Welle 3: Verifier-Karte (`kustomize build | kubeconform`, `kubectl auth can-i`), dann Feature-PR-Karte.
- Phase-0-Probe danach erneut; Vergleich mit Crew: 88 min / 5 Runs / 1,5 M Budget.
- Verify: Feature-PR offen, Verifier PASS mit Funktionsnachweis, Board-Zahlen im Zielkorridor.

### Phase 5 — Aufräumen
- `local-skill-addenda/references/crew.md` → Historie-Hinweis bleibt; Crew-Lessons-Mechanik ersetzt durch `hindsight_retain` aus der Intake-Session (einziger Schreiber der Projekt-Bank, sobald das Bank-Konzept steht).
- Memory-Einträge aktualisieren: Crew entfernt, Koordinationsmodell A + B-Mechanik, Kartenschnitt-Regeln.
- PR #391: Worktree `.worktrees/t_e4e351e5`, Branch, `.crew/` entfernen, PR schließen mit Verweis auf den Neuschnitt (offene Frage aus Session 20261104_232522).

## Reihenfolge und Aufwand

| Phase | Abhängigkeit | Aufwand | Wer |
|---|---|---|---|
| 0 Probe-Skript | — | ½ h | Chat (docs/skills sind kein Code) |
| 1 Skill v3 | 0 | 2–3 h | Chat |
| 2 Wake-Kanal | 1 | 1 h + Live-Probe | Chat + Peter (Telegram-Test) |
| 3 Profile | 1 | 1 h | Chat, Gateway-Restart durch Peter |
| 4 Probelauf | 1–3 | 1 Feature | Board |
| 5 Aufräumen | 4 | ½ h | Chat |

## Offene Entscheidungen für Peter

1. Reviewer-Modell: `claude-fable-5-1` (günstig, im Crew-Lauf als Verifier solide) oder `gpt-6.1-sol` (anderer Hersteller, stärkeres Vier-Augen)?
2. Telegram als Zweitkanal für Board-Events ja/nein?
3. PR #391 schließen und neu schneiden (Phase 4) oder als Feature-Branch behalten und nur die fünf Punkte als Karten nachziehen?
4. `worker.agent.max_turns` 150 → 100?

## Risiken

- `notify+wake` ist „not exactly-once"; stille `block_loop`-Events bleiben (Upstream). Mitigation: Reviewer-Karte + Phase-0-Probe nach jeder Welle als manueller Check durch den Chat auf Zuruf.
- Toolset-Kürzung am worker kann Karten brechen, die `delegation` nutzten. Mitigation: Smoke-Karte in Phase 3.
- Der Skill-Umbau ist groß; Backup + Commit vor dem Schnitt.
