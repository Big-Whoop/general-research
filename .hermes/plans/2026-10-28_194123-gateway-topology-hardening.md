# Plan: Gateway-Topologie härten + Report-Korrektur (kein Deploy)

## Summary
Die 7 `gateway-<profil>`-s6-Slots sind Upstream-Design (Boot-Reconciler des Base-Images registriert sie für jedes Profil; Autostart nur bei letztem Zustand `running`, Quelle: `docker/stage2-hook.sh`). Der multiplexte Host-Gateway bedient bereits alle 7 Profile. Der Plan (a) beweist den Ist-Zustand prozessgenau, (b) stellt dauerhaft sicher, dass kein benanntes Profil-Gateway jemals wieder hochkommt, (c) korrigiert die falsche „8 laufende Gateways"-Aussage im Research-Corpus. Kein Image-Wechsel, kein Flux-Deploy, kein Pod-Restart — die laufende Session bleibt unberührt, `gateway-default` wird nicht angefasst.

## Faktenlage (read-only verifiziert)
- Host-Gateway pid 380, `served_profiles` = default + alle 6 benannten; Telegram + api_server `connected` (`/opt/data/gateway_state.json`).
- `gateway-worker/-reviewer/-crew-verifier/-crew-content` tragen `down`-Marker in `/run/service/…`; keine `gateway_state.json` in den Profil-Homes; keine Log-„state"-Inhalte → keine laufenden Profil-Gateways.
- `crew-*`: `platforms.slack.enabled: false`; worker/reviewer: keine Plattformen. Kanban funktioniert, seit worker/reviewer-Gateways down sind → Worker benötigen kein eigenes Gateway.
- Rest-Artefakte: `gateway.lock`-Dateien in crew-*/worker (Staleness ungeprüft).

## Crew-Plugin-Anforderungen (geprüft, Quelle: plugins/crew README/REFERENCE/Skripte)
- Der Plugin-Dispatcher-Check (`crew_card.dispatcher_state()`) prüft `base_home()` — bei einem Profil-Home
  der Parent von `profiles/`, also `/opt/data` (Host-Gateway). Läuft. Ein laufendes Profil-Gateway ist
  für crew nirgends erforderlich.
- `hermes gateway install` im Plugin ist nur Hint-Text für den Fall, dass der HOST-Gateway down ist
  (assertiert in tests/test_crew_gateway_down.py) — kein Bedarf an Profil-Gateways.
- Chat-Plattformen sind optional und bei uns aus: `--chat-kanban` off-by-default,
  `platforms.slack.enabled: false` in allen crew-Profilen, `--proofs-deliver` Default `local`,
  kein per-Profil-Cron in den crew-Profilen (jobs.json leer).
- Verursacher der `gateway-crew-*`-Services: der crew-Installer (`--service`-Pfad, REFERENCE.md
  Windows-Abschnitt dokumentiert `--no-service --no-cron`). Sie sind heute down-markiert; kein Crew-
  Workflow hängt daran.
- Falls crew später Chat braucht (Slack an/`--chat-kanban`): der Host-Multiplexer bedient die
  Profil-Plattformen inklusive `kanban`-Toolset-Zusaltung — weiterhin kein Profil-Gateway-Prozess nötig.

## Änderungen

### 1. Live-Beweis (read-only, vor jeder Änderung)
- `s6-svstat /run/service/gateway-*` und `ps -eo pid,args | grep 'gateway run'` — Erwartung: genau ein laufendes Gateway (default), alle anderen `down`.
- Ergebnis in die Corpus-Dateien dokumentieren (Abschnitt B/Beweislage).
- **Abzweigung:** Falls doch ein benanntes Gateway läuft (widerspräche der Dateilage): es mit `hermes -p <name> gateway stop` stoppen (perspektivisch via desired-state, nicht `s6-svc`), dann erneut prüfen.

### 2. Dauerhafte Normalisierung (Volume-Zustand, überlebt Pod-Neustarts)
- Für jedes der 6 benannten Profile: `/opt/data/profiles/<p>/gateway_state.json` existieren lassen/erstellen mit `{"gateway_state":"stopped"}`, damit der Boot-Reconciler (`02-reconcile-profiles`) die Slots dauerhaft down lässt (Autostart nur bei `"running"`).
- `gateway.lock` der benannten Profile: nur entfernen, wenn die darin referenzierte PID nicht existiert (Staleness-Check vor Löschen, pid-Referenz wird ausgelesen und verifiziert).
- Kein Löschen der `/run/service/gateway-*`-Registrierungen (Reconciler erzeugt sie bei jedem Boot neu; down-Slots kosten nichts). Kein Eingriff in `/opt/data/gateway_state.json` oder `gateway-default`.

### 3. Report-Korrektur (Corpus `2026-10-28-hermes-profile-architecture`)
- `REPORT.md` §4.2 + Kurzfassung-Punkt 3 + §6: „8 Gateway-Prozesse laufen" → korrigiert auf: „Base-Image registriert pro Profil einen s6-Slot (Upstream-Design); alle benannten sind down, der Host-Multiplexer bedient bereits alle Profile. Offener Punkt ist nur die Persistenz + Beweisführung, nicht laufende Konkurrenz." Issue #88521 bleibt als Pitfall nur für den Fall tatsächlich laufender Profil-Gateways stehen.
- `README.md` Local-Addendum: gleiche Korrektur + Verweis auf `stage2-hook.sh`-Mechanik (Reconciler, `gateway_state.json`-Semantik) und den Live-Beweis aus Schritt 1.
- Hindsight-Memory-Eintrag von heute korrigieren (Topologie-Fix „ausstehend" → „verifiziert; Persistenz normalisiert").

## Testplan
```
# Topologie nachher (Erwartung: 1 Gateway-Prozess, Rest down):
s6-svstat /run/service/gateway-default            # up
for p in worker reviewer crew-coordinator crew-worker crew-verifier crew-content; do s6-svstat /run/service/gateway-$p; done   # down
ps -eo pid,args | grep 'gateway run' | grep -v grep | wc -l   # 1
grep -o '"gateway_state":"[^"]*"' /opt/data/profiles/worker/gateway_state.json  # stopped (für alle 6)
grep -c served_profiles /opt/data/gateway_state.json   # 1, Host unverändert
hermes cron status                                       # Scheduler host = default, heartbeat ok
```
- Telegram-Stichprobe: `hermes gateway status` → telegram `connected`; einmalige Testnachricht via Telegram-Echo-Kanal (nur falls für Beweislage gewünscht).
- **Verzögerte Verifikation:** Beim nächsten ohnehin geplanten Pod-Neustart (Deploy) erneut `s6-svstat` — die 6 Slots müssen down bleiben. Wird als Notiz ins Corpus geschrieben, kein erzwungener Neustart.

## Annahmen
- `crew-*` bleiben ohne eigene Slack-Bots (`enabled: false`); falls später gewünscht, übernimmt der Host-Multiplexer die Adapter mit profil-eigenem `.env`-Secret-Scope — kein Profil-Gateway-Prozess nötig (offizielles Multiplex-Design).
- Die Pod-Restart-Verifikation wird bewusst nicht jetzt erzwungen (würde diese Session + alle Worker killen); sie hängt am nächsten regulären Deploy.
- Corpus-Edits laufen auf dem bestehenden Research-Worktree/Branch und werden wie gehabt auf `main` gepusht.
