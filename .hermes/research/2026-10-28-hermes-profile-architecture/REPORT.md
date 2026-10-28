# Hermes-Profile für unsere Flotte — Deep-Research-Report

**Datum:** 2026-10-28 · **Frage:** „Wir nutzen das Default-Profil für alles — ist das schlechte
Praxis, welche Profile sind sinnvoll, und womit ausstatten?" · **Basis:** 5 Research-Lanes
(4× offizielle Doku, 1× Community/GitHub) + lokale Inventur unserer Installation.
Alle Belege mit Zitaten: `lane1–5.md` in diesem Verzeichnis.

---

## 1. Kurzfassung

1. **Die Prämisse ist nur halb wahr.** Kein offizielles Dokument sagt, dass „alles auf
   default" schlecht ist — die Tips-Seite enthält *null* Profil-Erwähnungen, die
   Security-Checkliste kein Profil-Item (Verified, L2-7). Was die Doku **verbietet**, ist
   exakt zweierlei: **zwei Agent-Prozesse auf einem Hermes-Home** („two writers on one
   home" — genau unser Kanban-On-Default-Inzidenz-Fall) und **viele Prozesse auf einem
   `state.db`** (Verified, L2-1/2/13 + 5 korrespondierende GitHub-Issues).
2. **Profile sind für getrennte *Agenten*, nicht zum Strukturieren eines Agenten.**
   Rollen, die eigene Identität/Gedächtnis/Kanäle brauchen → Profil. Alles andere
   (billigere Modelle für Teilaufgaben, Personas, wiederkehrende Jobs) löst die Doku
   bewusst mit **Delegation, `/personality`, Cron + `cron.model`** statt mit neuen
   Profilen (Verified, L2-8, L2-23).
3. **Für uns ist der Hebel nicht „mehr Profile", sondern saubere Rollen + Ausstattung.**
   worker/reviewer/crew-* existieren bereits korrekt als getrennte Homes. Die lokale Inventur
   vermutete zunächst „8 Gateway-Prozesse im Pod" — nach Detailprüfung korrigiert (siehe §4.2):
   das Base-Image registriert pro Profil einen s6-Slot (Upstream-Design), alle benannten sind
   down, und genau ein Host-Multiplexer-Gateway bedient bereits alle 7 Profile. Offen blieb nur
   die persistente Desired-State-Normalisierung — 2026-10-28 gesetzt.
4. **Ausstattung folgt dokumentierten Mustern:** headlose Worker ohne Chat-Kanäle,
   `kanban`-Toolset explizit (nicht über `all`), Billig-Modell per `model.default`,
   Skills minimal (`--no-skills`, Curator, per-Plattform-Skills), Cron-Agent mit eigenem
   schmalen `cron`-Plattform-Toolset (Verified, L4).

---

## 2. Prämissen-Check (was die Quellen wirklich sagen)

| Behauptung | Befund | Tier |
|---|---|---|
| „Default für alles ist keine gute Praxis" | **Nirgends offiziell so gesagt.** Einzige Split-Pflichten: ein Agent-Prozess pro Home; Gateway-Topologie-Regel. FAQ rät bei Multi-Persona/Multi-Modell sogar *gegen* Profile (→ `/personality`, Delegation) | Verified (L2-7, L2-8) |
| „Default als Mülleimer ist schlecht" | Offiziell: Begründung existiert für Skill-Overgrowth („dozens of narrow near-duplicates … pollute the catalog and waste tokens", Curator-Seite) und Toolset-Bloat (Cron-Seite: Tool-Schema-Kosten pro Call). Community formuliert es als Warnung („Don't turn the default profile into a giant backpack") | Verified (Begründung) / Plausible (Zitat) |
| „Trennung = Sicherheit" | **Nein:** Profile isolieren Hermes-*State*, kein Sandbox — jeder Profil-Agent kann schreiben, was UID 10000 kann. Echte Isolation = Toolsets/Approval/Infrastruktur | Verified (L2-24, L1-F6) |
| „Profile sind teuer im Unterhalt" | Parity-Drift ist dokumentierter Kostenpunkt (eine kaputte `config.yaml` blockiert `hermes update` für die ganze Installation; per-Profil-`.env`-Drift ohne Sync-Mechanismus). Bundled-Skills bleiben dagegen automatisch synchron | Verified (L2-28) / Plausible (Issue #91572) |

**Fazit der Prämisse:** Nicht „default ist das Problem", sondern: *mehrere Mechanismen
(Interaktion, Kanäle, Orchestrierung, Cron, Karten-Ausführung) teilen sich einen State-Store*,
und die Rollen, die bereits Profile sind, sind nicht minimal ausgestattet.

---

## 3. Mechanik-Grenzen: Wer gehört worhin? (L3, Verified)

| Mechanismus | Zuständigkeit (Doku-Position) | Explizit NICHT |
|---|---|---|
| **Profil** | Dauerhafte Identität: config, memory, skills, Credentials, Sessions | Kein Scheduler, keine Work-Queue |
| **Bot Mode** | Präsentations-Schicht über Profilen: Roster, Bot Chat, Routines, Gruppen — „a Bot **is** a Hermes profile" | Eigener State-Besitz: abgeschaltet bleibt alles unverändert |
| **delegate_task** | Kurzlebige parallele Teilfragen im Elternprozess; nur Summary kehrt zurück | Nicht persistent (Restart tötet Kinder), keine Interaktion, Toolsets nur vererbbar |
| **Cron (LLM)** | Dauerhafte Jobs, profil-lokaler Store + Secret-Scope; eigenes `cron`-Plattform-Toolset + `cron.model` | Kann keine Jobs erzeugen; Hermes selbst damit überwachen → falsch (OS-cron + webhook) |
| **Kanban** | Dauerhafte Cross-Profil-Queue; Worker = vom Dispatcher gespawnte `hermes -p <profil>`-Prozesse | Für In-Kontext-Antworten → delegate_task; Kinder des Workers sterben mit ihm → Kind-Karten |
| **MoA** | Virtueller *Modell*-Provider, intra-session — kein Multi-Agent | Kein Profil-Mechanismus |

Faustregel des Maintainers (PR #122979, Verified): *„A profile isolates the agent;
a [Telegram-]topic only isolates the session."*

---

## 4. Ziel-Architektur für unsere Flotte (SQ6-Synthese)

### 4.1 Beibehalten, aber nachrüsten

**`default` — Interaktion + Kanäle + Orchestrierung** *(Desktop-Chat, Telegram,
api_server, Kanban-Orchestrator, 3 Cron-Jobs, 44 Skills, 14 Plugins)*
- Richtige Rollen-Zuordnung laut Doku: interaktiver Assistent + Dispatcher dürfen auf
  einem Profil leben; der Dispatcher läuft im Default-Gateway ohnehin dort.
- **Nachrüsten (alle Verified-Mechanismen):**
  - `platform_toolsets.telegram` beschneiden + Skills **per Plattform** deaktivieren
    (Doku-Beispiel: „keeping development skills off Telegram") — Telegram erreicht
    heute alle 44 Skills inkl. Terminal-Browser-Stack.
  - **Cron-Toolset statt Cron-Profil:** Das Cron-Plattform-Toolset (`hermes tools` →
    Plattform `cron`) explizit klein halten und `cron.model` auf ein Billig-Modell —
    die Doku warnt ausdrücklich, dass `browser`/`delegation` in jedem „fetch news"-Job
    das Prompt-Schema aufbläht. Ein `automation`-Profil ist *optional*, nicht nötig;
    wenn, dann Delivery-Identität vorziehen prüfen (Issue #144974, Plausible).
  - Curator aktiv lassen (Gegenmittel gegen Skill-Overgrowth; pro Profil).
  - `profile.yaml`-Description pflegen (`hermes profile describe`) — das ist der
    offizielle Routing-Futter-Mechanismus des Kanban-Orchestrators.

**`worker` + `reviewer` — headlose Kanban-Rollen** (37 bzw. 24 Skills)
- Dokumentationsempfehlung für Worker-Profile (L4, L3-F22/F23): **keine Chat-Plattformen**
  (ist so ✓), `kanban`-Toolset explizit listen (`all` grantet es bewusst nicht),
  interaktive Tools per `agent.disabled_toolsets` abklemmen, **billiges Modell** via
  `model.default` (Frontier-Modell nur auf dem Orchestrator — dokumentierter
  „planner/worker cost split"), Skills auf Rollen-Kern reduzieren, Per-Task-Ausnahmen
  über Task-Pins (`--model`, Task-`skills`) statt Profil-Edits.
- reviewer: strukturell read-only wäre wünschenswert, ist aber offiziell *nicht* erzwungen
  (Issue #126923, Plausible) → als Fallback `approvals`-Modus des Profils streng stellen
  (approvals sind pro-Profil, Verified L2-26).
- Worker-Skill-Bestand (37) gegen die tatsächlichen Kartentypen auditieren; Curator läuft
  pro Profil.

**`crew-*` (4 Profile)** — Plugin-eigene Rollen (je 2 Skills, 15 Plugins, eigene
Slack-Plattformen bei coordinator/worker/verifier)
- Wenn Personas/Routinen/Gruppen-Chats gewünscht: als **Bot-Mode-Roster** führen
  (offizielle Präsentations-Schicht; ändert nichts an den Profilen selbst). Wenn nicht:
  lassen wie sie sind — Profiles sind billig, idle Profile kosten nichts (FAQ, Verified).
- Achtung Token-Hygiene: ein Bot-Token gehört an genau ein Profil; Klone transportieren
  keine Channels — Slack-Tokens bleiben 1:1 (Verified, L1-F27/F28).

### 4.2 Gateway-Topologie: Korrektur + Ist-Stand (lokaler Befund, 2026-10-28 nachgeprüft)

Die ursprüngliche Behauptung — „8 Gateway-Prozesse laufen im Pod" — war auf Prozessebene
**falsch** und wird hiermit korrigiert. Verifizierter Stand:
- Das offizielle Base-Image registriert bei jedem Boot pro Profil einen `gateway-<profile>`-s6-Slot
  (`cont-init.d/02-reconcile-profiles` → `container_boot.reconcile_profile_gateways`,
  `docker/stage2-hook.sh`) und startet ihn nur automatisch, wenn `gateway_state.json` des Profils
  zuletzt `running` stand. Registrierung ≠ laufender Prozess; das ist Upstream-Design.
- Prozessebene: genau **ein** Gateway (`hermes gateway run --replace`, pid 380). Der Host-Gateway
  meldet `served_profiles` = default + alle 6 benannten Profile; Telegram + api_server `connected`.
- Die `gateway.lock`-Dateien der benannten Profile referenzieren den **lebenden** pid 380
  (Serve-Eigentümerschaft / Token-Kampf-Schutz des Multiplexers) — keine Stale-Artefakte, bleiben.
- Verursacher der Slots: Base-Reconciler; die `gateway-crew-*`-Registrationen zusätzlich vom
  crew-Installer (`--service`-Pfad, REFERENCE.md dokumentiert `--no-service`). Kein Crew-Workflow
  hängt daran: `crew_card.dispatcher_state()` prüft `base_home()` = Host-Gateway (läuft).
- **Normalisiert (2026-10-28):** `/opt/data/profiles/<p>/gateway_state.json` =
  `{"gateway_state":"stopped","desired_state":"stopped"}` in allen 6 benannten Profilen, damit der
  Reconciler die Slots dauerhaft down lässt. Die Upstream-Wortwahl („Do not build new setups on it",
  L2-10) und Pitfall #88521 betreffen *laufende* Profil-Gateways bzw. das `gateway.standalone`-
  Shim — beides hier nicht im Einsatz.
- **Verzögerte Verifikation:** nach dem nächsten regulären Pod-Neustart `ps`/`s6-svstat` erneut —
  die 6 Slots müssen down bleiben (s6-svstat fehlt übrigens im Image; ps ist der Beweis).

### 4.3 Was wir NICHT tun sollten

- **Keine weiteren Profil-Gateway-Prozesse** — Topologie s. 4.2.
- **Profile nicht als Sandbox missverstehen** — wer harte Isolation braucht (untrusted
  Kanäle, Kunden): dünnes Profil *plus* minimales Toolset *plus* Approval, nicht nur ein
  neues Profil (Verified L2-24; Community-Muster „nine tools, no shell" ist Plausible).
- **Kein Clone von Channels/Cron** für Spezialisten — Doppel-Feuern und Token-Kampf sind
  der dokumentierte Grund, warum Klone beides nie mitnehmen (Verified, L2-17/18).
- **Kein Profil-Boom für Modell-Kosten** — dafür existieren `delegation.model`,
  `cron.model`, Per-Task-`--model`; wiederholtes `/model`-Switchen ist wegen
  Prompt-Cache-Reset sogar anti-optimal (Verified, L2-22/23).

---

## 5. Optionen-Matrix

| | A: Status quo (+ Hausaufgaben) | **B: moderate Trennung (empfohlen)** | C: Community-Vollsplit („Chief of Staff" + Spezialisten) |
|---|---|---|---|
| Profile | default als Alles+Orchestrator; worker/reviewer/crew wie heute | wie heute, aber: default = Interaktion+Kanäle+Orchestrierung+schlankem Cron; worker/reviewer headlos-minimal; crew-* optional als Bots | dazu router-only default + Profil pro Lebensbereich/Domäne (work/home/research/content …) |
| Evidenz | Doku verbietet nichts davon außer Multi-Writer | 1:1 deckungsgleich mit dokumentierten Rollenmustern (orchestrator frontier / worker cheap, headless workers, cron toolset) | Nur Community-Muster (≥3 Reddit-Berichte, Plausible; Maintainer-FAQ stellt klar: Profile = Agent-Grenzen, nicht Themen-Grenzen) |
| Kosten | Skill-/Tool-Bloat auf Telegram; ein .env für alles; Bloat wächst weiter | Einmalige Ausstattungsaufwand; Parity-Drift bleibt Betriebslast (dokumentiert) | Maximaler Drift-Aufwand (pro Profil .env/Modell/Skills), Routing-Fehler, #144974-Klasse bei Cron-Delivery |
| Risiko | state.db-Konkurrenz, falls jemals zweiter Writer | gering | Parity-/Credential-Drift (Issues #91572, #135306) |

**Empfehlung: B.** Es ist das Maximum, was die offizielle Doku deckt; C ist vertretbar,
aber community-belegt, nicht dok-triniert — und unsere Kanban-Flotte bildet Rollen
bereits als Profile ab, sodass C nur private Lebensbereiche nachziehen müsste, wenn wir
die überhaupt trennen wollen.

---

## 6. Bekannte Lücken (unredlich wäre anderes)

- **Keine offizielle „Profile best practices"-Seite** existiert (Verified-Absence); die
  Doku-Empfehlungen sind Seiten-verteilt. Best Practices im engeren Sinn = unsere Synthese
  über Verified-Einzelregeln.
- Community-Muster (F1–F17 L5) sind Einzelberichte = **Plausible**, auf unserem System
  nicht getestet. X-Belege nur via offizielle user-stories-Kacheln (kein X-Suchzugang).
- **Cron-Delivery-Identität unter Multiplex** (#144974) und **Cron-Feuer-Überlappung**
  (#136018) sind ungeprüfte Einzelfall-Reports → vor Cron-Umbau verifizieren.
- **Memory-Design je Profil** (Hindsight-Banks) ist bewusst ausgeklammert — steht seit
  2026-10-23 unter Konzept-Vorbehalt (Fleet-Regel, nicht Rechercheergebnis).
- Gateway-Topologie: die frühere „8 laufende Gateways"-Aussage war ein Irrtum (Registrierung durch
  den Boot-Reconciler ≠ laufender Prozess; siehe §4.2). Restunsicherheit ist nur das
  Reconciler-Verhalten nach dem nächsten Pod-Neustart (verzögerte Verifikation; kein Lasttest).
- `model_overrides` in den crew-Configs ist Plugin-Vokabular, kein dokumentierter
  Core-Konfig-Key (L4 #16).

## 7. Quellen

Lane-Dateien mit allen Zitaten: `docs-profiles/lane1.md` (Profile/Lifecycle),
`docs-bestpractice/lane2.md` (Best Practice + Silence), `docs-boundaries/lane3.md`
(Mechanik-Grenzen), `docs-equipping/lane4.md` (Ausstattung), `community/lane5.md`
(Community/Issues). Hauptseiten: `docs/user-guide/profiles`, `…/multi-profile-gateways`,
`…/faq`, `…/bot-mode`, `…/features/kanban`, `…/features/cron`, `…/features/skills`,
`…/features/curator`, `…/reference/toolsets-reference`, `…/user-stories`;
GitHub: #73411, #110106, #139959, #85858, #88521, #126923, #144974, #91572, #135306,
#22620, PR #122979 (Maintainer-Boundary).
