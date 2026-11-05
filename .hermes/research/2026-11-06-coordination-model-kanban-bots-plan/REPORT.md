# Koordinationsmodell für Agentenarbeit: Koordinator im Chat, auf dem Board, als Bot-Armee — oder Plan zuerst?

**Datum:** 2026-11-06 · **Frage:** Die Hauptsession „denkt zu viel", bevor ein Feature aufs Board geht; gehört der Koordinator aufs Board? Sind Bots (direkter Chat) überlegen — schneller, weniger Tokens? Wie sind die Hindsight-Banks je Modell zu schneiden? Oder ist „Plan in einer Session, dann Übergabe" das überlegene Muster, und welche Rollen sind entscheidend?
**Basis:** 5 Research-Lanes (Hermes-Doku Kanban · Hermes-Doku Bots/Delegation · Community/GitHub/Crew · Industrie-Muster und Papers · Hindsight-Banks) + lokale Board- und Token-Probe. Belege mit Zitaten: `docs-kanban/lane1.md`, `docs-bots-delegation/lane2.md`, `community/lane3.md`, `industry-patterns/lane4.md`, `memory-banks/lane5.md`. Tier: **Verified** = autoritative Quelle für genau dieses Subjekt · **Plausible** = belastbar, nicht auf unserem Ziel gezeigt · **Speculative** = Ableitung.

---

## 1. Kurzfassung

1. **Die These „der Koordinator muss aufs Board" ist halb richtig.** Richtig ist: die *Überwachung* (warten, pollen, Karten nachtreten) darf nicht im Chat leben — das ist der einzige quantifizierte Anti-Pattern im ganzen Korpus (Upstream #90853: ein Routine-Auftrag über Kanban = 1 961 s, 56 API-Calls, Kontext 92 k→133 k; Verified, L3-A4). Falsch ist: die *Planung* aufs Board zu schieben. Jede Quelle — Hermes-Doku, Anthropic, Claude Code, spec-kit, Magentic-One, die Community-Fleets — legt die Planung in die menschennahe Session und persistiert den Plan außerhalb jedes Kontextfensters (L4-F3/F10/F19, L1-F6/F7).
2. **Das lokale Problem ist nicht Nachdenken, sondern wo das Ergebnis des Nachdenkens hingeht.** Unsere Pre-Card-Regeln (~20 KB Skill) sind inhaltlich das, was die Doku „Decide before you fan out" nennt (Verified, L1-F6). Was fehlt, ist eine harte Grenze: *Intake endet mit einem Plan-Artefakt und den Karten — danach schweigt der Chat bis zu einem Board-Event.* Die Hermes-Doku kennt genau diesen Schnitt: „interactive session gets the tools but not the guidance" — der Chat ist Ersteller, nicht Besitzer (L1-F5/F13).
3. **Bots sind kein schnelleres oder billigeres Koordinationsmodell.** Ein Bot *ist* ein Profil; Bot-zu-Bot ist eine fire-and-forget-DM mit einem vollen Agent-Turn pro Zustellung, Hop-Cap 4, Antwort nur als Notification (Verified, L2-2/3/4). Gruppenchats verlieren in ~45 min die Aufgabe (Upstream #123766, Verified, L3-C6). In der Industrie ist das Chat-Schwarm-Muster das *schlechteste* gemessene: −31 % gegen einen Ledger-Orchestrator (Magentic-One-Ablation, Verified, L4-F13); Token-Overhead ≈ gleich wie Orchestrator-Worker, aber ohne Fehlereindämmung (Kim et al. 263 % vs 285 %, Verified, L4-F16). Niemand in der Community hat eine Pipeline *auf* Gruppenchat migriert (L3-D3). Bots eignen sich als Roster + Routine-Trigger + Eskalationskanal — nicht als Zustandsträger.
4. **Token-Realität bei uns:** Die Doku und das einzige Side-by-Side (Reddit, Plausible, L3-C1) sagen: Kanban ≈ delegate_task in Tokens, sobald Auto-Decomposer und Goal-Loop aus sind; Einsparung kommt aus *billigeren Modellen auf Worker-Rollen*, nicht aus dem Koordinationsprimitiv (L1-F14, L3-C2). Wir fahren Opus überall — das Board kauft bei uns Dauerhaftigkeit und Audit, keine Tokens. Lokale Probe: Default-Chat-Sessions sind mit im Mittel 2,46 M Input-Tokens die teuersten Sessions des Systems (Worker ~0,9 M, Reviewer ~0,96 M).
5. **Die entscheidenden Rollen** (Konsens über alle Lanes): **Planer/Spec** (im Chat, mit Mensch), **Worker** (isolierter Kontext, eine Karte, disjunkte Dateien), **Verifier** (die Rolle, deren *Fehlen* als Fehlerklasse gemessen ist: 23,5 % aller MAS-Fehler; L4-F15), **Human Gate** an genau zwei Stellen (Plan-Freigabe, Merge) plus blockierte Eskalation, **eine finale Autorität** über „fertig" (+9,4 %, MAST). Ein *stehender* Koordinator ist nur in Modell B entscheidend; in Modell A ersetzen ihn Dispatcher + Plan-Datei (L4 §3).
6. **Empfehlung: Hybrid A + B-Mechanik** — Plan im Chat (bounded, ≤ N Fragen, Plan-Datei im Repo), Karten mit Abhängigkeitsgraph *vor* dem Dispatch verlinkt, Supervision ausschließlich event-getrieben auf dem Board, Verifier-Karte pro Welle, Chat meldet sich nur bei `blocked/needs_input` und Wellenende. Crew ist genau diese B-Mechanik (Coordinator = ein modellfreier Pass pro Tick + „zwei Retries, eine Frage"), ohne unabhängige Nutzungsberichte (L3-A5). Ob wir Crew nehmen oder die Mechanik im eigenen Skill nachbauen, ist eine Folgeentscheidung; der Schnitt Intake/Supervision ist in beiden Fällen derselbe.

---

## 2. Prämissen-Check: was die Quellen wirklich sagen

| Behauptung | Befund | Tier |
|---|---|---|
| „Die Hauptsession denkt zu viel vor der Übergabe" | Die Doku *verlangt* das Denken vor der Übergabe: „Design decisions belong to the orchestrator, not to the workers — settle naming schemes, schemas … before fanning out. Every child card body must carry the decisions it depends on" (L1-F5/F6). Anthropic: ohne detaillierte Task-Beschreibungen „agents duplicate work, leave gaps" (L4-F4). Das Problem ist nicht Menge, sondern dass dasselbe Denken bei uns *im Chat-Transkript* statt in einem Artefakt landet und der Chat danach im Supervisions-Loop bleibt. | Verified |
| „Der Koordinator muss aufs Board" | Doku-Modell: der Orchestrator-*Profil* wacht nur *einmal* auf — als headless Worker auf der Root-Karte, nachdem der ganze Graph fertig ist. Es gibt **keinen dokumentierten stehenden Supervisor-Loop** auf dem Board (L1-F2/F20). Was aufs Board gehört, ist die Zustandsmaschine (Dispatcher promotet Kinder), nicht ein Koordinator, der pollt. Crew fügt diesen Loop hinzu (ein Pass pro Tick). | Verified (Doku) / Plausible (Crew-Wirksamkeit) |
| „Bots: direkte Kommunikation = schneller, weniger Tokens" | Bot-DM = ein voller Turn pro Zustellung, per-invocation, „live interrupt … is future work" (L2-3). Gruppenchat: 3 serielle Runden, 200-Nachrichten/32 k-Zeichen-Fenster pro Member-Turn; jeder Member liest das Zimmer neu → Kosten wachsen pro Runde (L2-6, L4-F14). Kein Doku-Benchmark existiert (L2 §C). | Verified |
| „Plan in einer Session, dann Übergabe ist überlegen" | Industrie-Default für Coding (Claude Code Plan Mode, Codex Cloud, spec-kit `tasks.md`, CrewAI Planner); auf SWE-bench ist *jede* Multi-Agent-Variante ≤ Single-Agent (L4-F16); Anthropic: „most coding tasks involve fewer truly parallelizable tasks than research" (L4-F2). | Verified (Papers/Doku), Plausible (Transfer auf uns) |

---

## 3. Die vier Achsen, sauber getrennt

Die Frage „wo lebt der Koordinator" bündelt vier Entscheidungen. Für jede gibt es eine klare Quellenlage:

| Achse | Befund | Quellen |
|---|---|---|
| **Wo wird geplant** | In der menschennahen Session, bounded. Claude Code: Plan Mode blockiert Edits bis zur Freigabe, Plan ist menschen-editierbar. Crew: ≤ 5 Intake-Fragen *vor* der ersten Karte. Fleet-Praxis: „the coordinator writes the job briefs". | L4-F10, L3-A5, L3-A1 |
| **Wo liegt der Zustand** | Plan-Datei im Repo (Design + Entscheidungen) **und** Board-Zeilen (Lauf-Zustand). Nie im Chat-Transkript: „saving its plan to Memory to persist the context" (Anthropic); spec-kit `tasks.md` mit `[P]`-Markern. | L4-F3/F19, L1-F16 |
| **Wer spricht mit dem Menschen** | Nur `kanban_block(kind=needs_input)` + Comment, geliefert über Gateway-Subscription (`notify+wake`) oder Desktop-Toast; `clarify` ist in Workern verboten. Chat-Koordinator darf wach werden, aber nicht warten. | L1-F12/F13, L3-A4 |
| **Wer führt aus** | Worker-Profile als eigene OS-Prozesse (Kanban); delegate_task-Kinder sterben mit der Session; Bots laufen als Sessions im einen Gateway, pro Ziel-Bot serialisiert. | L2 §A, L1-F16 |

---

## 4. Optionsmatrix

### Option A — Plan-first im Chat, dann Board (Dispatcher statt Koordinator)
- **Mechanik:** Intake-Session (default) erstellt Plan-Datei + Wellen-Tabelle + Contract-Cards, verlinkt den Abhängigkeitsgraphen *vor* dem ersten Dispatch, endet den Turn. Dispatcher promotet Kinder. Chat erhält nur `blocked`/`completed`-Wakes; Reviewer-Karte pro Welle; Feature-PR-Karte am Ende.
- **Voraussetzungen:** `auto_decompose: false` (haben wir); `auto_subscribe_on_create: true` für Wakes; Karten klein (eine Stufe, ein Writer, ein Worktree); höchstens *eine* `needs_input`-Frage pro Karten-Lebenszeit (BLOCK_RECURRENCE_LIMIT=2, Zähler resettet nicht auf Human-Input — L3-B3).
- **Kosten/Tempo:** Niedrigste Grenzkosten (Plan einmal; Worker isoliert; kein stehender Koordinator). Latenz = Dispatch-Tick (5 s lokal) + Worker-Laufzeit (lokal median 4,3 min/Run, created→completed median 0,6 h).
- **Confidence:** Mechanik Verified (L1, L4); Transfer auf unser Board Plausible (Board-Probe: 75 `block_loop_detected`, 200 `respawn_guarded` auf 812 Runs — die Loops sind real und müssen durch Kartenschnitt, nicht durch Chat-Babysitting gelöst werden).
- **Trade-offs:** Kein In-Flight-Re-Planning — bei Stall plant der Mensch (oder eine Fix-Karte). Das ist für unsere Merge/Deploy-Hoheit eher Feature als Mangel.

### Option B — Stehender Koordinator auf dem Board (Crew-Modell oder eigener Director)
- **Mechanik:** Koordinator-Profil wacht pro Karten-Event (Crew: pro Dispatch-Tick, modellfrei für mechanische Fälle), entscheidet *retry / rescope / split / ask*, führt nie aus. Magentic-One-Vorbild: Task Ledger + Progress Ledger + Stall-Zähler ≤ 2 → Re-Plan (L4-F12).
- **Voraussetzungen:** Eigenes Profil mit Toolsets auf `kanban, gateway, memory` beschränkt („literally cannot execute", L1-F6); Pitfall-Wissen (unsere 22 KB) als Rollen-Skill oder `lessons.md`; Rückkanal zum Menschen (Telegram-Subscription) — sonst steckt der Koordinator in `needs_input`.
- **Kosten/Tempo:** Orchestrator liest jedes Ergebnis → 285 % Overhead vs Single-Agent (Kim, Verified als Paper); Crew mitigiert durch modellfreie Pässe (Plausible). Beste Fehlereindämmung aller Topologien (zentrale Verifikation).
- **Confidence:** Doku-Mechanik Verified; Crew-Wirksamkeit Plausible (null unabhängige Berichte, 15 ★); unser Research 2026-10-28: Crew erbt die Kernel-Bugs (Claim-Lock, Loops), fixt sie nicht.
- **Trade-offs:** Zweite Koordinator-Instanz neben dem Chat; Rollen-Gedächtnis-Frage (Crew-Rollen memory-free per Entscheidung); mehr Profile = mehr Parity-Drift.

### Option C — Bot-Armee (N Bot-Profile, DM/Gruppenchat)
- **Mechanik:** Lead-Bot spricht mit dem Menschen, `message_agent` an Spezialisten; Gruppenraum für Deliberation; Routinen = Cron.
- **Was fehlt (dokumentiert):** keine Queue, kein Claim/Ack/Retry, kein Status; Bot-zu-Bot ist Shell-Hop ohne Zustellsignal (#88061, Verified); Zimmer verliert Aufgabe in ~45 min; Hindsight kompensiert nicht (#123766).
- **Kosten/Tempo:** Ein voller Turn pro Zustellung; 3 serielle Runden pro Nachricht; N× Auto-Recall pro Raumrunde (L5-Modell 3). Sequentiell per Konstruktion.
- **Confidence:** Verified (Doku + Upstream-Issues). Keine Quelle empfiehlt Chat-Schwarm zum Ausführen eines abhängigen Coding-Plans (L4-Tabelle).
- **Verwendbar als:** Roster + Routine-Trigger + `@user`-Eskalation („needs you"-Badge ist der reichste Human-Surface, L2 §D). Nicht als Arbeitsqueue.

### Option D — Alles in der Session + delegate_task (die „Suspendierungs"-Lösung seit 2026-10-28)
- **Mechanik:** Hauptsession plant und delegiert; Kinder liefern Summary zurück.
- **Kosten:** ≈ Kanban in Tokens (L3-C1); Kontext bleibt kleiner, Gesamt nicht. Kein Mensch-im-Loop für Kinder, stirbt mit Session/Restart, kein Audit nach Compression (L1-F16).
- **Confidence:** Verified (Doku). Für Features mit Merge-Gate und Deploy-Tags fehlt die Dauerhaftigkeit — genau der Grund, warum die Community-Blogger „heavier review flows" aufs Board migrieren (L3-D5).

**Ranking für unseren Fall (Code-Features mit Review, Merge-Hoheit, Deploy-Tag):** **A** als Grundmodell, **B-Mechanik** (Stall-Zähler, Verifier-Karte, „zwei Retries, eine Frage") als Regelwerk darin; **C** nur als Eskalations-/Trigger-Schicht; **D** für Research und kleine Einzelaufgaben.

---

## 5. Hindsight-Bankschnitt je Modell (L5, Verified für Semantik, Speculative für Layout)

Grundregeln aus Vendor-Doku und Plugin-Code:
- Bank = harte Recall-Grenze; kein server-seitiges Cross-Bank; `recall_additional_banks` ist der **einzige read-only-Mechanismus** auf Hermes-Seite, `additional_banks` schreibt immer (L5-A1/B3).
- Tags sind kein Security-Control (`tags_match=any` schließt untaggte Memories ein) — Rollen-Trennung braucht Banks (L5-A4).
- Auto-Retain ist der „experience write"-Kanal; Observation-Konsolidierung (`shared`) kann eine einzelne injizierte Tatsache zur bankweiten Überzeugung befördern; kein Hermes-Gate für `hindsight_retain` (memory-shield deckt nur das Built-in-Tool) (L5-A6/C4).
- Heute: `{project}` kollabiert in allen Gateway-Sessions (`session_execution.py:161-189` ohne `cwd=`) → Worker/Reviewer schreiben und lesen nur `hermes-<profile>`; **`nixos-infra` wird von keiner Gateway-Session gelesen** (L5-B2/B4, Verified).

| Modell | Schreiber von `nixos-infra` (P) | Leser von P | Rollen-Banks | Risiko-Schwerpunkt |
|---|---|---|---|---|
| **A** Plan-first → Board | nur die Intake-Session (default): Entscheidungen per `hindsight_retain`; Plan-Datei trägt den Zustand | worker/reviewer via `recall_additional_banks: [nixos-infra]` | D, W, R bleiben privat | `{project}`-Kollaps: Entscheidungen landen in D statt P → Bank im `👁️`-Indikator prüfen; Draft-Optionen im Plan-Chat werden mit-retained (Abschluss-Retain muss finale Entscheidung explizit nennen) |
| **B** Board-Koordinator | Mensch nach dem Lauf (kuratiert aus Karten-Trail); Koordinator memory-free, Regeln in `crew/lessons.md` | wie A | Koordinator ohne Bank (höchste Exposition gegen Worker-Output pro Tick) | `lessons.md` ist Repo-Datei → von Worker-Karten editierbar → CODEOWNERS/Review oder außerhalb der Worktrees |
| **C** Bot-Armee | nur der Lead-Bot (`additional_banks: [P]`) | jeder Bot read-only | `hermes-<bot>` privat pro Bot | Höchste Leak-Fläche: jeder Member auto-retained das Zimmer in seine Bank und recallt es in *allen* seinen Chats; N× Echo-Retains → falsche Konfidenz in Observations |
| **D** Session + delegate_task | Session | — (Kinder haben `skip_memory=True`) | D | geringste Poisoning-Fläche, aber nichts für Worker nachlesbar |

Querschnitts-Rezept (Speculative, abgeleitet): (1) `recall_additional_banks: ["nixos-infra"]` auf worker/reviewer, **nicht** `additional_banks`; (2) auf dem einzigen P-Schreiber `retain_tags: ["role:default"]` + `retain_source`; (3) `retain_mission` auf P („Entscheidungen, Konventionen, Blocker, gescheiterte Ansätze; keine Karten-Chatter"), Memory-Defense `redact`; (4) `trusted_project_dirs` auf den kanonischen Checkout einengen (Worktrees raus — ein Karten-Commit mit `.hindsight/config.toml` könnte sonst die Primär-Bank umleiten); (5) Crew-Rollen, Subagenten, Cron bleiben memory-free; (6) `lessons.md` = kuratierte Regeln, P = Rohererfahrung; Prune-Termin für `lessons.md`.

Stehende Constraint des Users bleibt: keine Bank-Arbeit vor dem schriftlichen Konzept in `.hermes/decision/agent-memory/`. Diese Tabelle ist Input dafür, keine Umsetzung.

---

## 6. Was das für den Skill `hermes-kanban-workers` bedeutet

Konkreter Schnitt (Vorschlag, noch nicht umgesetzt):

| Block (heute im Skill) | Gehört zu | Was sich ändert |
|---|---|---|
| Pre-Card-Planung (~20 KB: Plan-Datei, Dependency-Graph, Contract-Cards, Wellen-Tabelle, Fragen eine pro Turn) | **Intake (Chat)** | Bleibt — aber mit hartem Ende: Plan-Datei committed, Karten verlinkt, Turn beendet. Fragen *vor* der ersten Karte batchen (Crew: ≤ 5), nicht über Karten-Lebenszeiten verteilen. |
| Orchestration-Loop (~20 KB: board-watch.py, `--hold`, Triage-Reihenfolge) | **Streichen / durch Events ersetzen** | `notify+wake`-Subscription (Telegram + Desktop) statt Watcher-Prozess; Wake-Turn = read-only Triage + eine Aktion; nie `sleep`/Poll. User-Regel „kein Watcher in der Welle" wird Default. |
| Pitfalls (~22 KB: Auto-Decomposer, needs_input-Flapping, block_loop, active_pr-Guard) | **Rollen-Skill des Koordinators** (B) oder **Kartenschnitt-Regeln** (A) | Umformulieren von „so rettest du die Karte" zu „so schneidest du die Karte, dass es nicht passiert": eine Frage pro Karten-Lebenszeit; blockt sie zweimal → splitten statt antworten; Reviewer als vorangelegtes Kind, nie Block für Review. |
| Verifier | **Neu als Pflicht-Rolle** | Pro Welle eine Verifier-Karte mit maschinellem Proof (Crew-Prinzip) — die am stärksten gemessene Fehlerklasse (MAST). |

Vier-Augen-Prinzip (User-Präferenz: verschiedene Modelle je Rolle) passt in A und B gleich: Reviewer/Verifier-Profil auf anderes Modell; Doku-Kostenstrategie „frontier orchestrator, cheap workers" ist bei uns die einzige echte Token-Hebelwirkung (L1-F14, L3-C2).

---

## 6b. Crew-Probelauf 2026-11-04/05 (lokale Evidenz, Verified aus Session-Transkripten)

Ein Auftrag (k8s-Service-Toggle-UI in nixos-infra, Karte `t_e4e351e5`), Worker Opus, Verifier Fable. Ergebnis PR #391 (27 Dateien, +1360/−9, 5 Commits, CI grün) — fachlich gut, vom Owner aber als Fehlschlag gewertet; Plugin + 4 Rollenprofile am 2026-11-05 entfernt.

| Befund | Zahl | Was es über das Modell sagt |
|---|---|---|
| Laufzeit bis PR | 88 min, 5 Runs | Zwei Runs am Iterationslimit (60), einer am Token-Budget (1,51 M/1,5 M) — Budgets haben gestoppt, nicht gesteuert |
| Erster Run | 54 min, **null Commits**, nur untracked Draft | Ohne „nach jedem Schritt pushen" im Vertrag verschwindet Arbeit beim Budget-Stop; der Board-Koordinator hat das erst nach dem Stall nachgeschoben |
| Koordinator-Entscheidung | „replicas aus Git streichen" — falsch; Worker hat mit richtiger Begründung (Flux-SSA-Ownership) abgelehnt | Design-Entscheidungen *im Tick* ohne Mensch sind fehleranfällig; das Ergebnis stimmte wegen des Workers, nicht des Systems |
| Verifier | 4 min, ~14 k Output, Proof prüfte nur Form (PR offen, CI grün, Design-Doc da) | „Done when" ohne Funktionsnachweis macht den Verifier wertlos — ein Intake-Fehler, kein Rollen-Fehler |
| Worker-Kosten | ~420 k Output, ~17 M Cache-Reads | Eine Karte für ein 27-Dateien-Feature ist genau die Kartengröße, die Community (D2) und Claude-Code-Doku als Kollaps-Ursache nennen |

**Einordnung gegen die Optionsmatrix:** Der Probelauf ist ein Datenpunkt für **Modell B ohne Plan-Phase**: Intake ≤ 5 Fragen, dann eine große Karte, Entscheidungen im Tick. Genau die drei Schwächen, die die Industrie-Lanes für B voraussagen (Koordinator-Kontext als Flaschenhals, Design-Drift, flacher Verifier), sind eingetreten. Die Stärken von B (Budget-Stop, unabhängiger Proof, Owner nur bei Fragen) haben funktioniert, waren aber ohne Plan-Artefakt und Kartenschnitt zu wenig. Das bestätigt die Empfehlung A + B-Mechanik — und schließt Crew als Produkt aus, nicht seine Mechanik.

## 7. Known gaps

- **Kein veröffentlichter Messwert „asynchrones Board vs. Chat"** — weder in der Hermes-Doku (nur qualitativ, L2 §C) noch in Papers (Kim et al. messen Debatte/Orchestrator, kein Board). Der einzige On-Target-Wert ist #90853 (Chat-Koordinator, der wartet). Unsere lokale Probe liefert Board-Zahlen (Run 4,3 min median, Karte 0,6 h median), aber keinen kontrollierten Vergleich mit derselben Aufgabe im Chat.
- **Crew-Wirksamkeit** bleibt vendor-reported (keine unabhängigen Berichte, Stand 2026-11-06).
- **Pro-Karte-Overhead eines Kanban-Workers** (Skill-Re-Reads, Spawn-Cold-Start) hat niemand gemessen (L3 „not found"); lokal: Worker median 11 API-Calls, ~392 k Input-Tokens (inkl. Cache) pro Session.
- Umgebungsblock der Lane-Briefs nannte vier `crew-*`-Profile; auf dem Pod existieren heute nur default/worker/reviewer. Betrifft keine Schlussfolgerung, ist aber ein veralteter Memory-Eintrag.

---

## 8. Ungetestet auf unserem Ziel

- Ob `notify+wake` auf unserer Telegram/Desktop-Kombination zuverlässig ankommt (Doku: „not exactly-once", Toasts nur bei offener App — L1-F12; Upstream-Issues zu stillen block_loop-Events #82597/#141866).
- Ob `recall_additional_banks` in Gateway-Sessions ohne cwd den Rest der Konfiguration unberührt lässt (Code-Lesung sagt ja, L5-B3/B4; nicht live geprobt).
- Crew v0.10.x auf Hermes v0.22.7 mit `auto_decompose: false` und unseren Hooks (Integrations-Lücken aus Research 2026-10-28 offen).
