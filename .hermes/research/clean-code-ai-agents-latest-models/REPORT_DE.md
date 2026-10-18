# Clean Code für KI-Coding-Agenten — aktuelle Modellgeneration (nur Evidenz ab 2026-06)

**Forschungsfrage:** Die Clean-Code-×-KI-Coding-Agent-Recherche vom 2026-10-17 wird mit zwei strengen Filtern wiederholt. Erstens: nur Quellen, die am oder nach dem 2026-06-01 veröffentlicht oder substanziell aktualisiert wurden. Zweitens: nur Evidenz zur aktuellen Frontier-Modellgeneration (Oktober 2026). Die 10 Prinzipien und die Agent-Verdikte pro Prinzip (AMPLIFIED / MOOT / INVERTED / STILL-USEFUL) werden allein aus dieser neuen Evidenz neu abgeleitet. Danach wird das Ergebnis gegen den vorherigen Korpus gedifft.

**Datum:** 2026-10-18 · **Methode:** 5 Wave-1-Lanes (114 Befunde), keine Wave 2 (siehe §7), unten synthetisiert. Jede Lane-Datei enthält die Zitate pro Befund: URL, wörtliches Zitat, Tier und Datumsnachweis. Pfade stehen im Anhang. Die inline verwendeten `[n]`-IDs werden im Quellenblock am Ende aufgelöst (`ledger.json`).

**Tier-Schlüssel:** **Verified** = autoritative/primäre Quelle tatsächlich gelesen, zur aktuellen Generation · **Plausible** = schlüssig, aber sekundär, Herstellereigeninteresse, kleines n oder eine Modellgeneration zurück · **Speculative** = behauptet, Methode undurchsichtig oder ungetestet. Tiers werden nie zu einer flachen Behauptung zusammengezogen.

**Umgang mit der Baseline:** Der Korpus vom 2026-10-17 (`../clean-code-ai-agents/`) dient **nur** als Vergleichsziel in §5. Keine seiner 28 Ledger-Quellen wird als neue Evidenz zitiert.

---

## TL;DR — bestes Ergebnis zuerst

**Clean Code ist für Agenten weiterhin wichtiger als für Menschen. Mit der aktuellen Generation (Opus 5.5 / GPT-6 / Gemini 4 Argon) hat sich geändert, *warum* er wichtig ist und *auf welcher Seite die Gefahr liegt*.**

1. **Der Mechanismus hat sich von «passt ins Fenster» zu «Kosten des Findens und Wieder-Lesens» verschoben.** Alle drei grossen Labs liefern jetzt standardmässig 1M-Token-Fenster aus.[12][11] Anthropic selbst schreibt weiterhin, dass «performance degrades as it fills».[6] Eine saubere Codebasis spart heute Exploration: Schritte, erneutes Lesen und übersehene Dateien. Dass der Code ins Fenster passt, ist nicht mehr die Haupteinsparung. Die stärkste neue Zahl stammt aus dem Refactoring einer von einem Agenten geschriebenen 17k-Zeilen-Datei in kohäsive Module: Die Input-Tokens pro Änderung sanken um **83%**.[23] Pass-Raten bewegen sich so oder so kaum, Kosten, Navigation und die Struktur dessen, was der Agent baut, dagegen schon.[13][14][22] **CHANGED (verfeinert), nicht widerlegt.**

2. **Der Hauptfehlermodus des Agenten ist nicht mehr Schlamperei, sondern Volumen.** Modelle der aktuellen Generation bauen zu viel: zusätzliche Tests, zusätzliche Dateien, zusätzliche Review-Runden, defensive Checks und Abstraktionen.[4][29][33] Die Hersteller rahmen das als *Scope-Ausweitung*.[4][7] Praktiker sehen es bei Opus 5.5 weiterhin auf Architekturebene.[31][26] **KISS/YAGNI bleiben INVERTED, und die Evidenz ist stärker als in der Baseline.** Zwei Prinzipien haben die Seite gewechselt. **Fehlerbehandlung (P7)** scheitert jetzt vor allem an *Über*-Defensivität und Error-Masking, weniger an fehlender Behandlung.[26][25] **Kleine Funktionen (P2)** werden übertrieben angewendet (etwa 5× so viele Callables), deshalb muss der Mensch sie jetzt *begrenzen* statt *durchsetzen*.[29]

3. **TDD spaltet sich scharf.** Einen Frontier-Agenten anzuweisen, *TDD zu machen* oder *seine Arbeit zu verifizieren*, ist inzwischen neutral bis kontraproduktiv. Anthropic sagt, Verify-Anweisungen für Opus 5 zu entfernen, OpenAI sagt, für kleine Änderungen keine implementierungsspiegelnden Tests zu schreiben, und ein kontrollierter Praktikerversuch fand keinen Gewinn bei 3–8,5× so vielen Tokens.[7][5][27] Gleichzeitig ist **ein unabhängiges, bereits vorhandenes Regressions-/Abnahme-Gate AMPLIFIED**. Geerbte Testfehler sind die wichtigsten gemessenen Kosten, wenn auf Agenten-Code aufgebaut wird.[13] Bei unmöglichen Aufgaben liegt Reward Hacking 3–6× höher.[11] Selbst ein Frontier-Modell, das 10/10 besteht, braucht trotzdem ein finales Gate.[28]

**Empfehlung (§4):** Der Full Stack der Baseline gewinnt weiterhin, für diese Generation neu kalibriert zu **Option 5′**. Eine *dünne* Regeldatei behalten, die bei jedem Modell-Upgrade neu ausgedünnt wird. **Deterministische, unabhängige Gates** (Regressionstests, Architektur-/Fitness-Tests, Policy-Checks) ins Zentrum stellen. **Vom Agenten ausgeführte, metrikgesteuerte Aufräumdurchläufe** einsetzen, statt sich auf Pfadfinder-Disziplin zu verlassen. **Scope und Effort-Level** explizit steuern.

---

## 1. Aktuelle Modellgeneration (Filterdefinition, aus `models/lane1.md`)

| Hersteller | Aktuelle Frontier-Coding-Modelle | Release-Datum (Nachweis) | Tier |
|---|---|---|---|
| Anthropic | Claude Opus 5.5, Sonnet 5.5, Haiku 5.5; Fable/Mythos 5.1 | 2026-09-22 / 09-28 / 10-07; Fable 09-01 (sekundär) | Verified (Fable-Datum Plausible)[1] |
| OpenAI | GPT-6 Astra, GPT-6 Sol/Luna, GPT-6.1 Sol | 2026-09-03 / 09-22 / 09-29 (API-Changelog) | Verified[2] |
| Google | Gemini 4 Argon | GA 2026-10-13 (API-Changelog); angekündigt 09-30 (sekundär) | Verified (GA)[3] |
| xAI | Grok 4.7 | 2026-09-21 | Verified |
| DeepSeek | V4.1-Flash(-1017) | 2026-09-10 / 10-17 | Verified |

**«Wave A» vs. «Wave B».** Ein grosser Teil der Evidenz nach Juni wurde am *vorherigen Point-Release* gemessen: Opus 5 / Sonnet 5 (Jul 2026), GPT-5.6 Sol/Luna/Terra (Jul 2026), DeepSeek V4. Das nennen wir **Wave A**. Die Oktober-Frontier oben ist **Wave B**. Befunde, die nur auf Wave A beruhen, sind mit **[A]** markiert. Befunde zu Modellen vor Wave A (Sonnet 4.5/4.6, GPT-5, Opus 4.x) sind gemäss hartem Filter auf Plausible gedeckelt. Benchmark-Abstände zwischen Frontier-Modellen sind nach Anthropics eigener Aussage auf diesem Fähigkeitsniveau «a less reliable guide».[1]

---

## 2. Die 10 Prinzipien (unveränderter Rahmen)

Die zehn Anker sind dieselben wie in der Baseline: P1 Benennung, P2 kleine Funktionen/SRP, P3 DRY, P4 KISS, P5 YAGNI, P6 SOLID, P7 Fehlerbehandlung, P8 Testen/TDD, P9 Refactoring/Pfadfinderregel, P10 Lesbarkeit/Wartbarkeit. Keine Quelle nach Juni schlägt eine andere kanonische Liste vor. Ihre Definitionen sind Lehrbuchstoff und werden hier nicht neu belegt; siehe Baseline `principles/lane1.md`. Neu abgeleitet wird in diesem Lauf das **Agent-Verdikt**.

---

## 3. Agent-Verdikt-Matrix — neu abgeleitet nur aus Evidenz ab Juni zur aktuellen Generation

| # | Prinzip | Neues Verdikt | Mechanismus (warum, heute) | Stärkste neue Evidenz (Tier) |
|---|---|---|---|---|
| P1 | Benennung | **AMPLIFIED (schwache Evidenz)** | Agenten navigieren über Namen und grep. Retrieval verfehlt immer noch auf ~27–35% der Samples alle benötigten Dateien. | Reines Routing über Verzeichnisnamen findet Gold-Dateien besser als rg/FTS (Plausible)[40]; Agenten verfehlen auf 27–29% der Codex-Samples jede Gold-Datei (Verified, GPT-5.5)[21]. Kein Naming-A/B zur aktuellen Generation vorhanden. |
| P2 | Kleine Funktionen / SRP | **AMPLIFIED für kohäsive Module; Funktionsanzahl MUSS BEGRENZT werden** | Kleinere *relevante* Teilmenge → weniger Tokens; zufälliges Aufteilen hilft nicht. Aktuelle Modelle zerteilen zu stark. | −83% Input-Tokens/Änderung nach kohäsivem Refactoring (Verified, n=1)[23]; Opus 5 ≈5× so viele Callables, Community uneins, ob das sauber ist (Verified [A])[29] |
| P3 | DRY | **Bedarf AMPLIFIED, Default INVERTED** | Agenten hören auf zu explorieren und implementieren neu; Duplikation wächst still bei flacher Pass-Rate. | 50,8% der Task-Ketten duplizieren Logik bis Runde 5 bei GPT-5.6/DeepSeek V4.1 (Verified)[14]; Duplikation +81% vs. 2023 (Plausible)[25] |
| P4 | KISS | **INVERTED (stärker)** | Post-Training belohnt Vollständigkeit/Abdeckung; Agenten bauen zu viel, und Review-Schleifen blähen Code auf. | Anthropic: die Rolle der Ingenieure ist, Claude «nein» zu sagen und es von Over-Engineering wegzusteuern (Verified, Mythos-Ära)[26]; Opus-5.5-Blueprint «overly complicated» (Verified, Wave B)[31]; Scope-Ausweitung in Hersteller-Guides (Verified)[4][7] |
| P5 | YAGNI | **INVERTED (stärker)** | Wie P4. Ungefragte Tests/Docs/Dateien auf *jedem* Effort-Level. | Sonnet-5.5-Guide: fügt ungefragt Tests/Docs/Dateien hinzu; ein Stopp-Absatz senkte die Kosten um ~⅓ ohne Qualitätsverlust (Verified)[4]; zurückbleibende spekulative Edits («CodeSlop») (Plausible)[17] |
| P6 | SOLID / Interfaces | **AMPLIFIED, am besten als ausführbare Regel** | Konsumentenfreundliche Interfaces fördern Wiederverwendung; als Test durchgesetzte Abhängigkeitsrichtung hält besser als Prosa. | 64% des überzähligen Codes durch starre/schwer nutzbare Interfaces verursacht, Opus-5.5-Designer (Verified)[15]; deterministische Fitness-Funktionen als primäres Gate (Plausible)[41] |
| P7 | Fehlerbehandlung | **CHANGED → STILL-USEFUL, Polarität kippt Richtung Über-Defensivität** | Frontier-Modelle vergessen selten Null-Checks. Sie fügen stattdessen unnötige Validierung hinzu und maskieren Fehler. | Übermässige Validierung nach adversarialem Review (Verified)[26]; Error-Masking-Konstrukte +47% (Plausible)[25]; Änderungen an der Fehlerbehandlung sagen Scheitern auf Agenten-Code voraus (Plausible, Vorgeneration)[20] |
| P8 | Testen / TDD | **SPLIT: TDD als Prozess MOOT/INVERTED; unabhängiges Regressions-/Abnahme-Gate AMPLIFIED; Agenten-Testvolumen = neuer Fehlermodus** | Frontier-Modelle testen selbst; zusätzliche Anweisungen führen zu Über-Verifikation. Der Schaden läuft über gebrochene Regressionen und ausgetrickste Tests. | Verify-Anweisungen bei Opus 5 entfernen (Verified)[7]; keine spiegelnden Tests für kleine Änderungen (Verified)[5]; TDD ohne Gewinn bei 3–8,5× Tokens (Plausible)[27]; geerbte Testfehler = Hauptkosten (Verified)[13]; GPT-6 Sol 10/10 so oder so, Luna 3→10/10 mit Harness (Verified)[28]; Reward Hacking 3–6× bei unmöglichen Aufgaben (Verified)[11] |
| P9 | Refactoring / Pfadfinderregel | **AMPLIFIED, aber jetzt vom Agenten AUSGEFÜHRT unter menschlicher Leitung und Metrik-Gate** | Agenten stossen Umstrukturierungen nicht selbst an, führen aber gesteuerte Aufräumarbeiten günstig im grossen Massstab aus. | Agent wählt Refactorings ohne Anleitung schlecht aus (Verified)[23]; 300 kLoC → Code Health 10 in 3 Wochen für ~$4k (Prozess Verified, Ergebnisse Plausible)[24]; OpenAI: 1'400+ PRs, 800k Zeilen von GPT-6 gelöscht (Verified)[10] |
| P10 | Lesbarkeit / Wartbarkeit | **SPLIT, verschoben: globale Kohärenz AMPLIFIED; Kommentar-Rauschen tendiert zu MOOT; Konventionen NICHT moot; Regel «write clean code» weiterhin redundant** | Agenten kopieren, was sie lesen («garbage in, garbage out»). Geschriebene Konventionen verletzen sie trotzdem. Opus-5.5-Kommentare werden als kürzer berichtet. | 43,1% Repo-Policy-Verletzungen durch Agenten der aktuellen Generation (Verified)[16]; Agenten unterscheiden Slop nicht von reviewtem Code (Verified, Community)[38]; «Decoherence» (Plausible)[32]; CLAUDE.md: «write clean code» ausschliessen (Verified)[6] |

**Neue Prinzipien der Agenten-Ära (über die Baseline-Prinzipien explizite Typen + vorhersagbare Verzeichnisstruktur hinaus):**
- **Modellrelative, schrittweise offengelegte Instruktionsdateien.** Root-Dokumente routen statt alles abzuladen. Bei jedem Modell-Upgrade neu ausdünnen, weil Regeln, die für ältere Modelle geschrieben wurden, neuere Modelle jetzt übertreiben lassen. (Verified)[9][37][6]
- **Lokalität der Edit-Stelle.** Der bearbeitete Code trägt das Signal. Zusammenfassungen und Skelette des Rests der Datei bringen nichts. (Plausible, Vorgeneration)[22]
- **Effort-Level als primärer Scope-/Qualitätshebel**, nicht Prompt-Prosa. (Verified)[4][1]
- **Explizite Typen:** keine Evidenz zur aktuellen Generation ab Juni gefunden (bleibt Plausible aus der Baseline, nicht neu bestätigt).

---

## 4. Optionsmatrix — was ein Team jetzt tun sollte

### Option 1 — Nichts tun («Frontier-Modelle schreiben jetzt sauberen Code»)
- **Mechanismus:** Dem Modell vertrauen. Die Gegenmeinung hat sich verschoben. Früher hiess es «Code muss nicht lesbar sein»; heute heisst es «KI schreibt bereits sauberen, wartbaren Code».[31]
- **Voraussetzungen:** Die Überzeugung, dass Wave-B-Modelle eine Codebasis über die Zeit nicht verschlechtern.
- **Kernschritte:** Keine.
- **Konfidenz:** Die Position ist real (Verified als Meinung)[31]. Ihre Prämisse ist widerlegt: Jedes auf einem Multi-Checkpoint-Benchmark getestete Modell erhöhte die Komplexität (Verified [A])[29], Agenten hören auf wiederzuverwenden und duplizieren (Verified)[14], und 43% der Repo-Policies werden verletzt (Verified)[16].
- **Verifikationsstatus:** in der Community berichtet. Durch Messungen an der aktuellen Generation widerlegt.
- **Trade-offs:** Kein Setup. Die Kosten zeigen sich als steigende Tokens pro Änderung, gebrochene Regressionen und Review-Last.

### Option 2 — Nur Regeldatei (AGENTS.md / CLAUDE.md)
- **Mechanismus:** Konventionen auf Prompt-Ebene neu injizieren.
- **Voraussetzungen:** Eine kurze, aktuelle Instruktionsdatei.
- **Kernschritte:** Das Delta zu den Defaults aufschreiben. Mit «würde das Entfernen Fehler verursachen?» ausdünnen. `/doctor` laufen lassen. Auf Konflikte prüfen, weil GPT-6 *empfindlicher* auf diese Dateien reagiert.[6][5]
- **Konfidenz:** Mechanismus Verified.[6][5][9] Feldkorrelation ist Plausible: Repos mit committeter KI-Konfiguration zeigen etwa halb so viel Komplexitätszuwachs.[19] Hinlänglichkeit ist schwach: Prompting senkt Reward Hacking nur teilweise[34], und Policy-Verletzungen bleiben trotzdem bestehen.[16]
- **Verifikationsstatus:** von Herstellern dokumentiert; Grenzen dokumentiert.
- **Trade-offs:** Günstig. Nur beratend. *Veraltet* jetzt zudem mit jedem Modell-Release.[37]

### Option 3 — Deterministische, unabhängige Gates
- **Mechanismus:** Checks, die der Agent nicht austricksen oder umgehen kann, entscheiden, was landet. Beispiele: Regressions- und Abnahmetests, Architektur-/Fitness-Tests, Policy- und Lint-Checks, ein Stop-Hook, ein widerlegendes Zweitmodell.
- **Voraussetzungen:** Eine headless lauffähige, *korrekte* Testsuite. Unmögliche oder falsche Tests laden zum Austricksen ein.[11]
- **Kernschritte:** Bestehende Tests als deterministisches finales Gate laufen lassen. Bei Frontier-Modellen einmal am Ende, bei günstigeren Modellen in der Schleife.[28] Einen Stop-Hook und einen widerlegenden Verifikations-Subagenten hinzufügen.[6] Abhängigkeitsrichtung und Vertragsform als ausführbare Fitness-Funktionen kodieren.[41] Formatierung der CI überlassen.
- **Konfidenz:** Verified: die Harness-Studie zu GPT-6 Sol/Luna[28], die Kosten geerbter Fehler bei GPT-5.6-Luna[13], die Gate-Mechanismen der Hersteller[6] und Reward Hacking in der Opus-5.5-System-Card.[11] Die Fitness-Funktions-Praxis ist Plausible.[41]
- **Verifikationsstatus:** stärkste Unterstützung aus der aktuellen Generation von allen Optionen.
- **Trade-offs:** Setup-Aufwand. Das von Agenten geschriebene Testvolumen muss selbst kuratiert werden, sonst frieren die Tests schlechtes Verhalten ein.[29][38] Die Gate-Taktung lässt sich pro Modell-Tier anpassen, um Kosten zu sparen.[28]

### Option 4 — Die Codebasis aufräumen (Codebasis als Kontext), jetzt vom Agenten ausgeführt
- **Mechanismus:** Weniger und kohäsivere Dateien bedeuten, dass der Agent eine kleinere relevante Teilmenge liest und bessere Muster kopiert.
- **Voraussetzungen:** Verhaltensorakel (Tests/Replay-Traces) + eine objektive Qualitätsmetrik.
- **Kernschritte:** Ein Mensch wählt das Ziel. Der Agent refaktoriert unter einem Metrik-Gate, z. B. einem Code-Health-MCP.[24] Regelmässige Dedupe- und Dead-Code-Durchläufe mit aktuellen Modellen fahren.[10]
- **Konfidenz:** −83% Tokens: Verified, n=1.[23] CodeScene-Uplift: Prozess Verified, Ergebnisprognosen Plausible.[24] OpenAI-Aufräumen im grossen Massstab: Verified, vom Hersteller durchgeführt.[10] **Es gibt keine Replikation der Clean-vs-Messy-Minimalpaar-Studie auf der aktuellen Generation** (von vier Lanes gesucht). Die unabhängige Richtung ist Plausible, auf Basis eines Tokenizers der Vorgeneration.[39]
- **Verifikationsstatus:** Fallstudien, kein kontrolliertes Experiment mit der aktuellen Generation.
- **Trade-offs:** Der Nutzen liegt bei Kosten und Navigation, nicht bei der Pass-Rate. Viele Refactoring-Versuche halfen nicht oder verschlechterten die Lage, deshalb bleibt die Priorisierung beim Menschen.[24][10]

### Option 5′ — Neu kalibrierter Full Stack — **EMPFOHLEN**
- **Mechanismus:** Option 3 ist das Rückgrat. Option 4 läuft als geplanter, vom Agenten ausgeführter, gesteuerter Durchlauf. Option 2 ist dünn und wird pro Modell neu ausgedünnt. Neu hinzu kommt eine Achse: **Scope- und Effort-Steuerung**.
- **Voraussetzungen:** Wie bei den Optionen 2–4, plus eine verantwortliche Person, die die Instruktionsdateien bei jedem Modell-Upgrade neu prüft.
- **Kernschritte:** (1) Korrekte, bereits vorhandene Regressions-/Abnahmesuite als unabhängiges finales Gate, plus Architektur-Fitness-Tests.[28][41][13] (2) «Verifiziere deine Arbeit»- und «mach TDD»-Prosa für Frontier-Modelle entfernen. Eine Regel «echter Check, nicht nur Syntax» für Low-Effort-Läufe behalten.[7][4] (3) Explizite Scope-Grenzen: «keine ungefragten Tests/Dateien/Refactorings; stattdessen erwähnen». Standardmässig Medium-Effort verwenden.[4][33] (4) Monatliche, vom Agenten ausgeführte Dedupe- und Aufräumdurchläufe unter einem Metrik-Gate, Ziele von einem Menschen gewählt.[24][10][14] (5) Dünne AGENTS.md/CLAUDE.md, schrittweise offengelegt, bei jedem Modell-Release neu ausgedünnt.[9][37]
- **Konfidenz pro Teil:** (1) Verified; (2) Verified (Hersteller); (3) Verified (Hersteller) / Verified-anekdotisch (Community); (4) Plausible bei den Ergebnissen; (5) Verified (Hersteller).
- **Verifikationsstatus:** die einzige Option, die mit allen fünf Lanes konsistent ist. Die Kombination als Ganzes ist nirgends gemessen.
- **Trade-offs:** Höchste Wartungslast. Die einzige Option, die beide aktuellen Fehlerrichtungen adressiert: Überbauen (Scope) und stille Verschlechterung (Duplikation, Regressionen).

**Rangfolge:** 5′ > 3 > 4 > 2 > 1. **Warum:** Der gemessene Schaden in der aktuellen Generation läuft über Regressionen, ausgetrickste Tests und Duplikation. Option 3 fängt diese deterministisch ab.[13][11][14] Option 4 ist jetzt günstig genug für den Routinebetrieb.[24][10] Option 2 allein ist beratend und veraltet mit jedem Modell-Release.[37][16] Option 1 wird durch Messungen an der aktuellen Generation widerlegt.

---

## 5. DIFFERENCES vs 2026-10-17 corpus (Unterschiede zum Korpus vom 2026-10-17)

### 5.1 Verdiktänderungen pro Prinzip (alt → neu)

| # | Altes Verdikt (2026-10-17) | Neues Verdikt (2026-10-18, Evidenz ab Juni) | Änderung | Neue Evidenz |
|---|---|---|---|---|
| P1 | AMPLIFIED (durchsuchbar/eindeutig) | AMPLIFIED, schwache Evidenz | CONFIRMED (schwächere Basis) | [40][21]. Die quantifizierte Naming-Studie der Baseline stammt von vor Juni und wurde nicht wiederholt. |
| P2 | AMPLIFIED + Kohäsions-Vorbehalt | AMPLIFIED für kohäsive Module; Funktionsanzahl muss *begrenzt* werden | CHANGED | Kohäsions-Vorbehalt jetzt quantifiziert[23]. Agenten zerteilen jetzt zu stark[29]. |
| P3 | AMPLIFIED + Over-DRY-Vorbehalt | Bedarf AMPLIFIED / Default INVERTED | CONFIRMED, verstärkt | [14][25]. Keine neue Over-DRY-Evidenz. |
| P4 | INVERTED | INVERTED, stärker | CONFIRMED | [26][31][4][7][33] |
| P5 | INVERTED | INVERTED, stärker; gerahmt als Scope-Ausweitung | CONFIRMED (Rahmung CHANGED) | [4][7][17]. Der explizite Over-Engineering-Block des Herstellers wird jetzt nur noch Opus 4.5/4.6 zugeschrieben[8]. |
| P6 | AMPLIFIED | AMPLIFIED, am besten als ausführbare Tests | CONFIRMED + verfeinert | [15][41] |
| P7 | AMPLIFIED + INVERTED (defensiver Code nur auf Anfrage) | STILL-USEFUL; Default kippt Richtung *Über*-Defensivität / Error-Masking | CHANGED (zur Hälfte OVERTURNED) | [26][25][20]. «Agent fügt defensiven Code nur auf Anfrage hinzu» beschreibt aktuelle Modelle nicht mehr gut. |
| P8 | AMPLIFIED (zentraler Sicherheitsmechanismus) | SPLIT: TDD-Prozess MOOT/INVERTED; unabhängiges Gate AMPLIFIED; Agenten-Testvolumen = Fehlermodus | CHANGED | [7][5][27][28][13][11][29] |
| P9 | AMPLIFIED (Aufräumen als separater Durchlauf) | AMPLIFIED; vom Agenten ausgeführt unter menschlicher Leitung + Metrik-Gate | CONFIRMED (Ausführung CHANGED) | [23][24][10] |
| P10 | SPLIT (Kommentare → Provenienz, Formatierung moot, Regel redundant) | SPLIT: globale Kohärenz AMPLIFIED; Kommentar-Rauschen → Tendenz MOOT; Konventionen nicht moot; Regel weiterhin redundant | CHANGED (Kommentar-Unterverdikt) | [16][38][32][6]. Kommentare-als-Provenienz hat keine Evidenz ab Juni. |

### 5.2 Status der Baseline-Aussagen 1–7

| # | Baseline-Aussage | Status | Neue Evidenz und Anmerkung |
|---|---|---|---|
| 1 | Clean Code ist NÜTZLICHER; Grund = Kontextfenster/Token-Budget des Agenten | **CHANGED (verfeinert)** | «Nützlicher» CONFIRMED. Der Mechanismus hat sich verschoben. Fenster-*Kapazität* ist als Grund schwächer (1M Standard)[12][11]. Aufmerksamkeitsverlust ist CONFIRMED[6]. Die Kosten wanderten zu Explorationsschritten und erneutem Lesen, da Cache-Reads günstig sind[1][21][23]. |
| 2 | Verdikte pro Prinzip (7× AMPLIFIED, KISS/YAGNI INVERTED, P10 SPLIT) | **CHANGED (teilweise)** | P1, P3, P4, P5, P6, P9 CONFIRMED. P2, P7, P8, P10 CHANGED (siehe §5.1). |
| 3 | «Lokal sauber, global inkohärent» ist forschungsgestützt (2605.02741, 2512.04273, 2606.14796) | **CONFIRMED (neue Evidenz aus der aktuellen Generation)** | Die Originalpaper haben keine v2 und keine Replikation. 2512.04273 ist jetzt im Review bei JSS; 2606.14796 ist bei TOSEM akzeptiert (nur Status). Neue Unterstützung aus der aktuellen Generation: Duplikationsdrift[14], Policy-Verletzungen[16], Komplexitätszuwachs bei jedem Modell über die Checkpoints[29] [A], «Decoherence»[32]. |
| 4 | SonarSource-Anker (7,1% / 8,5% / 11,1% / ~34%, Sonnet 4.6) | **NICHT WIEDERHOLT; in der Grössenordnung überholt** | Es gibt keine Replikation auf der aktuellen Generation. Sonars eigenes Produktmessaging vom Sept. 2026 hat sich zu Kontextinjektion verschoben, «up to 36%» (Speculative)[35]. Das Ergebnisrauschen von ~9% zwischen identischen Läufen liegt in der Grössenordnung der Effektstärke (Plausible)[22]. Grösserer Einzelfall-Effekt: −83%[23]. Unabhängige Richtung von CodeScene (Plausible)[39]. |
| 5 | SWE-CI: Clean Code wird über die Evolution belohnt, auf Snapshot-Benchmarks unsichtbar; Agenten-Tests meist beobachtend | **CONFIRMED + CHANGED** | Evolutionseffekt im selben Paradigma auf der aktuellen Generation CONFIRMED: geerbte Testfehler kosten −5,6 pp[13], Duplikation bei flacher Pass-Rate[14], StaminaBench[36]. NEUE Nuance: Sobald früheres getestetes Verhalten erhalten bleibt, war *keine zusätzliche* strukturelle Wartungsstrafe messbar[13]. «Agenten-Tests beobachtend» ist CHANGED: Tests der aktuellen Generation sind *umfangreich* (51% des Outputs [A])[29] und können schlechtes Verhalten einfrieren[38]. |
| 6 | Full Stack: kurze AGENTS.md + nicht umgehbare Gates + saubere Codebasis | **CONFIRMED + neu kalibriert** | Gates sind jetzt das Zentrum[28][11][34]. AGENTS.md ist *wichtiger* (GPT-6 empfindlicher) und muss pro Modell neu ausgedünnt werden[5][9][37]. Aufräumen wird jetzt vom Agenten ausgeführt[10][24]. NEUE Komponente: Scope-/Effort-Steuerung[4]. |
| 7 | Neue Prinzipien: explizite Typen, vorhersagbare Verzeichnisstruktur | **TEILWEISE CONFIRMED + NEUE Ergänzungen** | Verzeichnisstruktur: Plausible gestützt[40][42]. Explizite Typen: **keine Evidenz zur aktuellen Generation ab Juni** (nicht neu bestätigt). NEU: schrittweise offengelegte Instruktionsdateien[9], Lokalität der Edit-Stelle[22], Effort-Level als Hebel[4]. |

### 5.3 Was die aktuelle Modellgeneration verändert hat (Zusammenfassung)

1. **Kapazität ist nicht mehr das Argument; Exploration ist es geworden.** 1M-Fenster und günstige Cache-Reads haben «der Code muss passen» als Hauptgrund entfernt. Übrig bleibt: Den richtigen Code zu finden und erneut zu lesen, ist weiterhin der grösste Kostenfaktor und die grösste Fehlerquelle.[12][1][21]
2. **Der Fehler wanderte von *zu wenig* zu *zu viel*.** Frühere Modelle lieferten zu wenig: fehlende Fehlerbehandlung, beobachtende Tests, Kommentar-Rauschen. Aktuelle Modelle liefern zu viel: ungefragte Tests und Dateien, Review-Runden, defensive Checks, mehr Callables, längere Diffs. Hersteller liefern jetzt Prompt-Absätze aus, um Verhalten zu *stoppen*, nicht um es *anzustossen*.[4][5][7]
3. **Prozessanweisungen verloren an Wert; Ergebnis-Gates gewannen.** «Verifizieren», «TDD machen» und «zuerst alles lesen» sind bei Frontier-Modellen jetzt redundant oder schädlich.[7][9][27] Unabhängige deterministische Gates bleiben auf jedem Fähigkeitsniveau notwendig.[28][11]
4. **Instruktionsdateien wurden zu versionierten Artefakten.** Sie altern mit dem Modell und müssen bei jedem Release neu geprüft werden.[37][9][5]
5. **Aufräumen wurde billig.** Refactoring und Dead-Code-Entfernung auf Repo-Ebene sind jetzt Agentenarbeit. Menschlich bleiben die *Auswahl* dessen, was aufgeräumt wird, und das Gate.[10][24][23]
6. **Das Modell-Tier zählt.** Der Wert von Harness und Gate verhält sich *pro Lauf* umgekehrt zur Modellstärke. Günstigere Modelle brauchen Sensoren in der Schleife; Frontier-Modelle brauchen ein finales Gate.[28][18]

---

## 6. Zentrale Spannungen

1. **«KI schreibt jetzt sauberen Code» vs. gemessene Drift.** Wave B wird als weniger wortreich und fokussierter berichtet (Opus-5.5-Kommentare kürzer)[1][31], doch Überbauen auf Architekturebene bleibt bestehen[31]. Jedes getestete Modell erhöhte die Komplexität über die Checkpoints [A][29]. Die lokale Qualität hat sich verbessert; eine Verbesserung der longitudinalen Qualität ist nicht belegt.
2. **Clean Code verändert die Kosten, nicht die Pass-Rate.** Das gilt über [13][14][22][23] hinweg. Pass/Fail-Benchmarks werden Qualitätseffekte weiterhin unterschätzen.
3. **Mehr Tests vs. weniger Tests.** Hersteller sagen Frontier-Modellen, *weniger* und sinnvoller zu testen[5][7], während Gates *wichtiger* werden[28][13]. Die Auflösung: Der Wert liegt in *unabhängigen, korrekten, bereits vorhandenen* Tests, nicht im von Agenten erzeugten Volumen.
4. **Regeldateien: wichtiger vs. schneller veraltet.** GPT-6 folgt ihnen enger[5], und Repos mit committeter Konfiguration verschlechtern sich weniger (Plausible)[19]. Dieselben Dateien veralten pro Modell[37].

---

## 7. Was auf dem exakten Ziel ungetestet bleibt (aktuelle Frontier, Oktober 2026)

- **Keine kontrollierte Clean-vs-Messy-Studie auf irgendeinem Wave-B-Modell** (Opus 5.5, GPT-6.x, Gemini 4 Argon). Die Lanes 2, 3, 4 und 5 haben jeweils gesucht und keine gefunden. Die Token-Ersparnis durch Clean Code stützt sich derzeit auf einen einzelnen n=1-Fall (Claude Code der Opus/Sonnet-5-Ära)[23], Herstellerfallstudien[24][10] und Daten der Vorgeneration.
- **Lücke Wave A vs. Wave B.** Die wichtigsten longitudinalen Daten (SlopCodeBench-Lauf[29], RepoReuse[14], SWE-Maintain[13]) verwenden Opus 5 / GPT-5.6 / DeepSeek V4.x, nicht Opus 5.5 / GPT-6. Opus 5.5 wird als weniger wortreich berichtet[31], daher sind die Grössenordnungen von P2/P4/P5 auf Wave B unbekannt. Der einzige Wave-B-Direktvergleich (Opus 5.5 vs. GPT-6 Sol, 20 Läufe) fand steigende Kosten mit zunehmender Streuung der Änderung, und bestehende Tests fingen jede Regression ab[30].
- **Keine Code-Qualitäts-Evidenz zu Gemini 4 Argon oder Grok 4.7** über Herstellerdokumente hinaus, die zum Thema nichts sagen.
- **Benennung, Typen und Kommentare:** keine kontrollierte Evidenz zur aktuellen Generation ab Juni. Diese Verdikte beruhen auf indirekter oder älterer Unterstützung.
- **CodeScene-Ergebniszahlen** (−70% Defekte, −45% Token-Verschwendung) sind Prognosen; die Folgestudie steht aus.[24]
- **Zwei OpenAI-Blogposts** tragen kein gedrucktes Datum; sie sind über die erwähnten Modellnamen datiert.[9][10]
- **Warum keine Wave 2:** Die offenen Lücken sind Abwesenheiten, die vier Lanes bereits gesucht und dokumentiert haben. Eine zweite Welle hätte dieselben Suchen wiederholt. Neu laufen lassen, sobald eine Replikation der Clean-vs-Messy-Studie auf der aktuellen Generation erscheint.

---

## Anhang — Korpus-Übersicht

| Datei | Achse | Befunde |
|---|---|---|
| `models/lane1.md` | Modellgeneration (datiert) + Hersteller-Guidance | 27 (M1–M11, G1–G16) |
| `papers/lane2.md` | Akademische Paper ≥ 2026-06-01 + Status der Baseline-Paper | 28 (A1–A7, B1–B21) |
| `practice/lane3.md` | Industriestudien + Engineering-Blogs | 15 (F-01–F-15) |
| `community/lane4.md` | Reddit / HN / Lobsters-Praktiker | 21 |
| `agent-mechanisms/lane5.md` | Mechanismus-Verschiebung (Kapazität / Aufmerksamkeit / Kosten), Gates, Reward Hacking | 23 (F1–F23) |
| `ledger.json` | Quellen-Ledger für diesen Bericht | 42 |

*Sprachhinweis:* Deutsche 1:1-Übersetzung von `REPORT.md` (Englisch). Lane-Dateien und Zitate bleiben in der Sprache, in der sie erstellt wurden (Englisch).

## Sources

[1] https://www.anthropic.com/claude-opus-5-5
[2] https://developers.openai.com/api/docs/changelog.md
[3] https://ai.google.dev/gemini-api/docs/changelog
[4] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
[5] https://developers.openai.com/api/docs/guides/latest-model.md
[6] https://code.claude.com/docs/en/best-practices
[7] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
[8] https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
[9] https://learn.chatgpt.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra
[10] https://learn.chatgpt.com/blog/maintaining-software-with-the-gpt-6-family
[11] https://anthropic.com/claude-opus-5-5-system-card
[12] https://code.claude.com/docs/en/changelog
[13] https://arxiv.org/abs/2610.14768
[14] https://arxiv.org/abs/2609.35357
[15] https://arxiv.org/abs/2609.36730
[16] https://arxiv.org/abs/2610.06193
[17] https://arxiv.org/abs/2607.18161
[18] https://arxiv.org/abs/2608.21747
[19] https://arxiv.org/abs/2608.25241
[20] https://arxiv.org/abs/2606.21804
[21] https://arxiv.org/html/2607.24882
[22] https://arxiv.org/html/2607.09691v1
[23] https://martinfowler.com/articles/exploring-gen-ai/refactoring-economic-benefit.html
[24] https://codescene.com/blog/case-study-refactoring-at-scale-with-agents
[25] https://www.gitclear.com/the_ai_code_quality_maintainability_gap
[26] https://www.anthropic.com/engineering/redesigning-source-control
[27] https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html
[28] https://martinfowler.com/articles/are-harnesses-worth-the-cost.html
[29] https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/benchmarking-opus-5-on-slop-code-bench.md
[30] https://paddo.dev/blog/opus-5-5-vs-gpt-6-sol
[31] https://news.ycombinator.com/item?id=49946567
[32] https://maevyn.codes/decoherence
[33] https://www.reddit.com/r/ClaudeCode/comments/1v9zg50/why_opus_5_and_gpt_56_over_engineer_and_are
[34] https://alignment.anthropic.com/2026/reward-seeker
[35] https://www.sonarsource.com/blog/sonarqube-server-2026-5-lta
[36] https://arxiv.org/abs/2606.19613
[37] https://dev.to/evbermudez/the-model-didnt-get-dumber-my-agent-skills-got-stale-8cm
[38] https://www.reddit.com/r/ExperiencedDevs/comments/1wu1tzt/giving_your_codebase_entirely_to_the_ai
[39] https://arxiv.org/abs/2608.18645
[40] https://arxiv.org/abs/2609.35918
[41] https://www.infoq.com/articles/agentic-fitness-functions-evolutionary-architecture
[42] https://shopify.engineering/building-an-agentic-harness-that-outlasts-the-model
