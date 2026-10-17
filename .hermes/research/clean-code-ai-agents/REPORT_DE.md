# Clean Code für KI-Coding-Agenten — Research-Report

**Forschungsfrage:** Bestimme die 10 wichtigsten Prinzipien von Clean Code (Software-Engineering) und wie jedes von ihnen funktioniert. Bestimme dann für jedes, ob es auch für das Programmieren von KI-Agenten nützlich ist (LLM-basierte Coding-Agenten, die autonom Code schreiben, bearbeiten und testen — z. B. Claude Code, OpenAI Codex, Cursor, Devin, SWE-agent, Aider). Fokus auf Research Papers und praktische Erfahrungen (z. B. Blog Posts) von weltweit führenden Entwicklern im KI-Bereich.

**Datum:** 2026-10-17 · **Methode:** 5 Wave-1-Lanes (242 Findings) + 2 In-Session-Verifikations-Lanes, unten synthetisiert. Vollständige Zitate pro Finding stehen in den Lane-Dateien (Pfade im Anhang); der Sources-Block am Ende ordnet die inline verwendeten `[n]`-IDs zu.

**Verwendete Tier-Skala:** **Verifiziert (Verified)** = autoritative/Primärquelle tatsächlich gelesen · **Plausibel (Plausible)** = solides allgemeines Verhalten oder Snippet-Ebene, nicht am Ziel demonstriert · **Spekulativ (Speculative)** = Mechanismus behauptet, ungetestet. Tiers werden nie zu einer flachen Aussage zusammengefasst.

---

## TL;DR — bestes Ergebnis zuerst

**Clean Code ist für KI-Coding-Agenten NÜTZLICHER, nicht weniger — aber der *Grund* hat sich verschoben und die *Form* einiger Prinzipien ist umgekippt.** Das Argument 2008 lautete: „Ein anderer Mensch wird diesen Code lesen." Das Argument 2026 lautet: „Der Context Window, das Token-Budget und die grep-basierte Navigation eines Agenten werden diesen Code lesen — mehrmals täglich — und jedes Token Rauschen hat einen festen Preis."[15][12]

Drei Erkenntnisse tragen den ganzen Report:

1. **Die einzige tragende Tatsache ist der Context Window.** Der Context Window des Agenten ist eine feste, knappe, abgerechnete Ressource, und *ablenkender Kontext schadet der Leistung aktiv* (im Gegensatz zu einem Menschen kann das Modell irrelevante Inhalte nicht einfach ignorieren).[12][15] Jedes Clean-Code-Prinzip, das **den Kontext verkleinert, den der Agent halten muss, um eine Aufgabe korrekt zu erledigen**, wird **VERSTÄRKT (AMPLIFIED)**; Dinge, die **dieses Budget nicht verändern** (Formatierungs-Finessen, „schreibe sauberen Code" als formulierte Regel), sind **BEDEUTUNGSLOS (MOOT)**; und an den Stellen, an denen die **Voreinstellung des Agenten dem menschlichen Instinkt entgegenläuft** (Kommentare, defensiver Code, Over-Engineering), ist die Polarisität **UMGEKEHRT (INVERTED)** und muss durch explizite Regeln + mechanische Durchsetzung korrigiert werden.[22][15]

2. **Die kontraintuitivste Erkenntnis — Agenten schreiben Code, der *lokal* sauber, aber *global* inkohärent ist — ist jetzt RESEARCH-BESTÄTIGT, nicht mehr nur von Praktikern beobachtet.** Praktiker nennen es „eine Art Meta-Code aus schön geschriebenen Stücken, die zusammen eine riesige Spaghetti bilden"[27] und „sie denken, 'Clean Code' bedeutet, in winzige Funktionen aufzuteilen, statt in kohärente Funktionen."[26] Die Research-Literatur benennt unabhängig dasselbe Phänomen: die **„Modular Mirage"** (oberflächliche Dateitrennung ohne semantische Kohärenz) und **„architectural rot"**[6], **„Architectural Erosion"** / **„Hallucinated Coupling"**[7] sowie eine wachsende formale Literatur zu technischer Schuld in LLM-Systemen[8]. Die Konvergenz von Praktiker-Intuition und peer-reviewter Research ist das stärkste Signal des Reports.

3. **Der quantifizierte Anker (Primärquelle verifiziert):** eine kontrollierte Sonar-Studie (660 Claude-Code-Versuche, sechs abgestimmte Repo-Paare) fand: saubere Codebases verbrauchen **7,1 % weniger Input-Tokens, 8,5 % weniger Output-Tokens, 11,1 % weniger Reasoning-Aufwand und ~34 % weniger Datei-Neubesuche — bei unveränderter Pass-Rate**[5][4]. Der Nutzen ist **Effizienz, nicht Erfolgsrate** — und am größten an Modul-Grenzen (10,7 % / 50,8 %).[5]

**Das Fazit zur Frage „Ist es nützlich?":** Alle 10 Prinzipien übertragen sich in den Agenten-Kontext, aber mit einem nicht-einheitlichen Urteil — die meisten werden **VERSTÄRKT** (Namensgebung, kleine Einheiten/SRP, DRY, SOLID, Fehlerbehandlung, TDD, Refactoring, Wartbarkeit), zwei haben einen **UMGEKEHRTEN Druck**, der aktiv aufgezwungen werden muss (KISS, YAGNI), und Lesbarkeit/Wartbarkeit ist **GESPLITTET** (Kommentare kehren um, Formatierung wird bedeutungslos, „schreibe sauberen Code" als Regel ist redundant). Die Rolle des Menschen verschiebt sich vom *Schreiben* von Clean Code zum *Durchsetzen* — weil **kein Agent es von sich aus tut**[22][23] und **Prompting allein die globale Inkohärenz nicht behebt**[6].

---

## 1. Die 10 Prinzipien (Facet A — das Rückgrat)

> **Provenance-Hinweis (Verifiziert):** Es gibt **keine einzelne Primärquelle, die genau „die 10 Clean-Code-Prinzipien" auflistet.** Der kanonische Satz ist eine **quellenübergreifende Synthese**: der Kern von Robert C. Martins *Clean Code* (2008) — dessen Teil I in ~14 Prinzip-*Kapitel* gegliedert ist, nicht in eine nummerierte „10"[1] — ergänzt um **DRY, KISS, YAGNI** (aus *The Pragmatic Programmer* / Extreme Programming) und **SOLID** (aus Martins Paper 2000 / *Agile Software Development* 2003 / *Clean Architecture* 2017). Drei der zehn (KISS, YAGNI, SOLID) sind **überhaupt keine Kapitel in *Clean Code***.[1][2] Wenn ein verteidigbarer „kanonischer 10er" benötigt wird, zitiere *Clean Code* (2008) Teil I als Rückgrat und vermerke die quellenübergreifenden Ergänzungen.

| # | Prinzip | Einzeilige Definition | Wie es in der Praxis funktioniert (konkret) | Kanonische Quelle (Tier) |
|---|---|---|---|---|
| P1 | **Sinnvolle Namensgebung** | Namen offenbaren Absicht; eindeutig, unterscheidbar, durchsuchbar | `d` → `daysBetweenCreationAndModification` umbenennen; ein Wort pro Konzept; `grep`-bar machen | *Clean Code* Kap. 2 (TOC verifiziert) |
| P2 | **Kleine Funktionen / SRP** | Funktionen tun eine Sache, kurz, eine Abstraktionsebene; ein Grund, warum sich eine Klasse ändert | Extract Method; 200-Zeilen-Funktion aufteilen; jede Klasse einzweckig halten | *Clean Code* Kap. 3 + SOLID-SRP (verifiziert) |
| P3 | **DRY** | Jedes Stück Wissen hat eine einzige, unmissverständliche Darstellung | Wiederholte Logik in eine Funktion extrahieren; Single Source of Truth | *Pragmatic Programmer* Topic 9 (verifiziert, Text gelesen) |
| P4 | **KISS** | Bevorzuge die einfachste Lösung, die funktioniert | Wenn die einfache funktioniert, eine schlichte Funktion statt einem schweren Pattern wählen | *Pragmatic Programmer* / US-Navy-Ursprung (plausibel) |
| P5 | **YAGNI** | Nicht bauen, bis es tatsächlich benötigt wird | Minimal liefern; Fähigkeit nur bei konkretem Bedarf hinzufügen | XP / *Pragmatic Programmer* (plausibel) |
| P6 | **SOLID** | 5 OOP-Designprinzipien (SRP/OCP/LSP/ISP/DIP) für flexiblen, wartbaren Code | God Class aufteilen; über Interface erweitern; von Abstraktionen abhängen (DI) | Martin 2000 / PPP 2003 / *Clean Architecture* (verifiziert) |
| P7 | **Fehlerbehandlung** | Komplett, bewusst; Exceptions statt Codes; keine Nulls | `UserNotFoundException` werfen; nie null zurückgeben; nie schlucken | *Clean Code* Kap. 7 (TOC verifiziert) |
| P8 | **Unit-Testing / TDD** | Tests sind First-Class; treiben die Entwicklung; F.I.R.S.T. | Red–Green–Refactor; ein Assert pro Test; schnell/unabhängig/deterministisch | *Clean Code* Kap. 9 (TOC verifiziert) |
| P9 | **Refactoring / Boy-Scout-Regel** | Design verbessern, ohne Verhalten zu ändern; hinterlasse es sauberer | Kleine verhaltenserhaltende Aufräumarbeiten bei jedem Touch | *Clean Code* Kap. 1 + Fowler *Refactoring* (verifiziert) |
| P10 | **Lesbarkeit & Wartbarkeit** | Code wird ≫ öfter gelesen als geschrieben; schreibe zum Lesen | Team-Style-Guide; Code liest sich wie Prosa; Peer Review | *Clean Code* Kap. 1 „We Are Authors" (verifiziert, Text gelesen) |

*Zwei strukturelle Anmerkungen aus der Backbone-Lane:* (a) Anker #2 verschmilzt eine funktionslevel-Regel (*Clean Code* Kap. 3 „Do One Thing") mit einer klassenlevel-SOLID-Regel (SRP) — verwandt, aber unterschiedlich; (b) SOLID ist ein **Meta-Prinzip** (5 Unterprinzipien unter einem Mnemonik), strukturell anders als die anderen neun.[1]

---

## 2. Die Agenten-Paradigma-Urteilsmatrix (Facet B — die Kernantwort)

**Framing.** Für jedes Prinzip tut das Agenten-Paradigma eines von vier Dingen: **VERSTÄRKT (AMPLIFIED)** (wichtiger, mit neuem Mechanismus), **BEDEUTUNGSLOS (MOOT)** (abgewertet zu Rauschen), **UMGEKEHRT (INVERTED)** (Polarität umgekehrt — die Voreinstellung des Agenten läuft dem menschlichen Instinkt entgegen) oder **WEITER NÜTZLICH (STILL-USEFUL)** (überträgt sich unverändert). Der dominierende Mechanismus hinter fast jedem Urteil ist der **Context Window**: eine feste, knappe, abgerechnete Ressource, in der ablenkender Kontext die Leistung schadet.[12][15]

| # | Prinzip | Urteil | Mechanismus (warum) | Stärkste Evidenz (Tier) | Praktische Implikation für Agenten |
|---|---|---|---|---|---|
| P1 | Namensgebung | **VERSTÄRKT** (Fokus → *durchsuchbar/eindeutig*) | Agenten navigieren per `grep`/Repo-Map; ein unterscheidbarer Name liefert wenige Treffer → der Agent geht direkt zum Ziel | Le et al. 2025: uninformativ umbenannte Identifier senkten GPT-4o-Zusammenfassung 87,3 %→58,7 % (verifiziert, quantifiziert)[9]; Aider-Repo-Map zeigt am meisten referenzierte Symbole (verifiziert)[17] | Eindeutige, spezifische Namen bevorzugen statt `data`/`handler`/`Manager`; „wenn du den Namen greppst und viel Unrelevantes zurückkommt, ist der Name schlecht"[22] |
| P2 | Kleine Funktionen / SRP | **VERSTÄRKT** (→ *technische Pflicht*) — mit *Kohärenz*-Einschränkung | Eine kleine Einheit passt in einen Read/Tool-Call ohne Truncation → volle Aufmerksamkeit; eine 800-Zeilen-3-Sachen-Klasse ist schlechter als drei 250-Zeilen-Klassen | Agenten-CLIs begrenzen Datei-Reads (~2000 Zeilen/Chunk) (verifiziert)[22]; Cursor-Regel „Komponenten unter 200 Zeilen halten" (verifiziert)[18] | Funktionen/Dateien klein **und kohärent** halten — Agenten erfüllen den *Buchstaben* (klein), verletzen aber den *Geist* (Kohärenz)[26] |
| P3 | DRY | **VERSTÄRKT** (Duplikation bricht Edit-Konsistenz) — mit *Over-DRY*-Einschränkung | Wenn sich replizierte Logik ändert, aktualisiert der Agent eine Kopie und verpasst die anderen (keine „zwei weitere Kopien"-Schwerkraft) | akitaonrails-Feldbericht (verifiziert)[22]; Aider-Repo-Map belohnt geteilte Abstraktionen (verifiziert)[17] | Geteilte Logik extrahieren **und** DRY mit YAGNI paaren — Agenten über-DRYen in brüchige vorzeitige Abstraktionen[22][23] |
| P4 | KISS | **UMGEKEHRTER Druck** (muss aufgezwungen werden) | Ein ungebundener Reviewer/Agent über-abstrahiert; tiefe Abstraktionsstapel kosten den Agenten mehr Tokens als eine direkte Implementierung | Claude-Code-Docs warnen: jedem Befund nachzujagen → Over-Engineering (verifiziert)[15]; orbitant: 20 Abstraktionsschichten kosten mehr als eine KISS-Impl (verifiziert)[24]; Cognition: der single-threaded lineare Agent ist das zuverlässige KISS-Design (verifiziert)[20] | Sag dem Agenten/Reviewer explizit, nur Korrektheitslücken zu markieren, nicht jede mögliche Abstraktion[15] |
| P5 | YAGNI | **UMGEKEHRTER Druck** (gleicher Mechanismus wie P4) | Eingebildeten Edge Cases nachzujagen baut Features/Tests, die nicht eintreten können | Claude-Code-Docs (verifiziert)[15]; OpenAI: „Tools nur hinzufügen, wenn sie einen echten Workflow freischalten" (verifiziert)[19] | Regeln/Tools/Abstraktionen nur nach echtem, wiederholtem Reibungsverlust hinzufügen[19][15] |
| P6 | SOLID | **VERSTÄRKT** (jedes Prinzip spart Context Window) | SRP (weniger Dinge zu tracken), OCP (neuen Code zum Einstecken schreiben, nicht Bestehendes editieren), DIP (Abstraktionen sind konziser als Konkrete), DI = Isolationsscope für Tests | First-Principles-Argument (plausibel)[22]; DI-„Isolationsscope"-Feldbeispiel (verifiziert)[22]; Cursor-Kompositionsregeln (verifiziert)[18] | SRP/Komposition/DI als Regeln codieren; Agenten sind schwach im Interface-Design (designen APIs aus der Storage-Sicht, nicht der Konsumenten-Sicht)[26] |
| P7 | Fehlerbehandlung | **VERSTÄRKT** (reiche Meldungen = Debug-Signal) **+ UMGEKEHRT** (defensiver Code nur auf Nachfrage) | Der Agent nutzt den Stack Trace als primäres Debug-Signal — eine vage Meldung kostet eine zusätzliche Reasoning-Runde; aber von sich aus implementiert er den Happy Path und schlägt keine Retries/Breaker vor | akitaonrails (verifiziert)[22]; SWE-agent integriert einen Linter in die Edit-Aktion für Fehlerfeedback (verifiziert)[12]; Cursor-Strukturierte-Fehler-Regeln (verifiziert)[18] | Exception-Meldungen sollen den fehlerhaften Wert + erwartete Form tragen; defensive Fälle in der Rules-Datei **aufzählen** — nicht erwarten, dass der Agent sie erfindet[22] |
| P8 | TDD / Testing | **VERSTÄRKT** (→ zentraler Sicherheitsmechanismus) — mit wichtiger Unterscheidung | Ohne ausführbaren Check ist der *Mensch* der Verifikations-Loop; ohne Headless-Tests wird der Agent „blind" | Claude Code „gib ihm einen Check, den er ausführen kann" (verifiziert)[15]; akitaonrails: 274 Commits / 1.323 Tests, CI fing 50+ Bugs (verifiziert)[22]; AGENTS.md führt aufgeführte Test-Kommandos automatisch aus (verifiziert)[16] | **Wert einer vorhandenen/ausführbaren Suite ≠ vom Agenten verfasste Wegwerf-Tests** — letztere sind meist observativ und bewegen keine Outcomes (verifiziert)[14] |
| P9 | Refactoring / Boy Scout | **VERSTÄRKT** (Tests machen Refactoring sicher) | „Factoring… ist automatisierte-Refactor-Sicherheit"; kontinuierliche Agenten-Edits brauchen ein Regressionsnetz | akitaonrails (verifiziert)[22]; Claude Code liefert ein `code-simplifier`-Plugin (verifiziert)[23]; SWE-CI: Qualitätsentscheidungen kumulieren über die Evolution (verifiziert)[3] | Aufräumen als expliziten, separaten Pass ausführen (Agenten sind zögerlich beim Löschen); Agenten zuerst zum Aufräumen nutzen, dann gaten[23][27] |
| P10 | Lesbarkeit / Wartbarkeit | **GESPLITTET: UMGEKEHRT + BEDEUTUNGSLOS + VERSTÄRKT** | Code wird ≫ öfter gelesen als geschrieben — jetzt von einem Agenten, der ihn mehrmals täglich liest; aber Kommentare kippen zu *Provenance-Kontext*, Formatierung wird zu *Rauschen*, und „schreibe sauberen Code" als Regel ist *redundant* | Kommentare-als-Provenance (verifiziert)[22]; README/AGENTS.md-Zwei-Zielgruppen-Split (verifiziert)[16]; „schreibe sauberen Code" steht auf der EXCLUDE-Liste (verifiziert)[15] | WHY/Provenance-Kommentare behalten (nicht die eigenen des Agenten kürzen); den Default-Formatter annehmen und Stildiskussionen stoppen; Clean Code nicht in der Rules-Datei wiederholen[22][15] |

**Zwei NEUE Agenten-Ära-Prinzipien aufgetaucht (nicht in den kanonischen 10):** **explizite Typen** (getypter Code ist ein „Lösungsschlüssel", der die Inferenz des Agenten spart — plausibel)[22] und **vorhersehbare Verzeichnisstruktur** (Framework-Konventionen lassen den Agenten Pfade antizipieren, ohne zu explorieren — verifiziert)[22].

**Querschnitts-Headline:** Die VERSTÄRKT-Urteile sind alle Wege, *den Kontext zu verkleinern, den der Agent halten muss, um eine Aufgabe korrekt zu erledigen*; die BEDEUTUNGSLOS-Urteile sind Dinge, die *dieses Budget nicht verändern*; die UMGEKEHRT-Urteile sind die Stellen, an denen die *Voreinstellung* des Agenten dem menschlichen Instinkt entgegenläuft und durch explizite Regeln korrigiert werden muss.[22][15]

---

## 3. Drei konvergente Evidenzlinien

Die fünf Lanes greifen die Frage aus unabhängigen Winkeln an; sie konvergieren, und das macht die Antwort robust.

**Linie 1 — Research Papers (LANE-2 + Verifikations-LANE2-1/2).** Das Feld organisiert sich *nicht* um „die 10 Prinzipien"; es verwendet ISO/IEC 25010-Attribute + statische Metriken (SonarQube, Pylint, Maintainability Index). Die tragenden Ergebnisse: **SWE-CI** zeigt, dass sauberer/erweiterbarer Code bei zukünftigen Modifikationen *belohnt* wird, während technische Schuld degradiert — und das ist **auf Snapshot-Benchmarks** wie SWE-bench **unsichtbar**, die Issue-Resolution messen, nicht Qualität[3][11], und die Komplexität von Enterprise-Codebases reduziert den Agenten-Erfolg drastisch[13]. LLM-Code ist **„oberflächlich sauber, aber intrinsisch komplex"** — besser bei Pylint (Oberfläche), schlechter beim Maintainability Index (Tiefe)[3]. **Vom Agenten verfasste Tests sind meist observativ und bewegen keine Outcomes**[14]. Und das Phänomen „lokal sauber, global inkohärent" ist dokumentiert als **Modular Mirage / architectural rot**[6], **Architectural Erosion / Hallucinated Coupling**[7] und eine wachsende Literatur[8].

**Linie 2 — Weltführende KI-Entwickler & Vendors (LANE-3).** Überwältigend pro Clean Code, konvergierend auf **drei Mechanismen**: (a) **ein maschinell ausführbarer Check** (Tests/Build/Linter), gater durch einen **Pre-Commit-Hook / CI, den der Agent nicht umgehen kann** — weil eine Regel in CLAUDE.md/AGENTS.md „nur ein Vorschlag ist, den er überspringen kann"[15][23]; (b) **die Instruktionsdatei kurz, spezifisch und gekürzt halten** — Bloat lässt den Agenten sie ignorieren[15][19]; (c) **die Codebase selbst als Kontext des Agenten behandeln** — ihre Qualität „setzt eine Obergrenze" für die Ausgabe[23]. Das Feld hat sich auf eine **gemeinsame Instruktionsdatei** standardisiert (AGENTS.md, jetzt unter Linux-Foundation-Versorgung), die über Codex, Claude Code, Cursor, Devin, Aider, Copilot etc. funktioniert[16]. Simon Willisons einzeilige These: *„Clean code is the way. Less docs. Linters define the style. Tests define the intent. Code defines the architecture."*[21]

**Linie 3 — Community-Praktiker (LANE-4).** **Bimodal.** Die **Mehrheits**-Auffassung: Clean Code ist *wichtiger*, mit dem Grund verschoben von „ein anderer Mensch liest es" zu „das Context/Token-Budget des Agenten liest es"[27][26]. Eine **lautstarke Minderheit** argumentiert, es sei bedeutungslos („du sollst den Code ja nicht mehr anfassen") — eine echte, dokumentierte Position, kein Strohmann[26][27]. Die **kontraintuitive** Erkenntnis: lokal-sauber-aber-global-inkohärente „Meta-Code"-Spaghetti[27]. Und eine neue de-facto-Rolle — der **„Code-Janitor" / KI-Code-Remediation-Ingenieur** — wird bereits von mehreren Praktikern berichtet[28], und Code Review wird der erste Blick des Ingenieurs auf den Code[25].

**Wie sie konvergieren:** Die Papiere „Qualitätsentscheidungen kumulieren über die Evolution"[3] + die Praktiker „Meta-Code-Spaghetti"[27] + die Research „architectural rot / Modular Mirage"[6] sind *derselbe* Phänomen aus drei Richtungen gesehen. Die Papiere „gib dem Agenten einen ausführbaren Check / eine saubere Interface hilft"[12] + die Vendors „Pre-Commit-Hook, den der Agent nicht umgehen kann"[15][23] + die Praktiker „Linter/Hooks/CI sind es, was hält"[26] sind *dieselbe* Preskription. Zwei unabhängige Evidenzlinien (gemessen + beobachtet) zeigen in dieselbe Richtung.

---

## 4. Options-Matrix — wie man Clean Code für KI-Agenten funktionieren lässt

Die Forschungsfrage reduziert sich operationell auf: *Angenommen, Clean Code überträgt sich (mit den Urteilen oben) — was sollte ein Team TATSÄCHLICH TUN?* Es gibt fünf machbare Optionen, von Nichtstun bis zum Full Stack. Jede wird bewertet nach Mechanismus, Voraussetzungen, Hauptschritten, Konfidenz pro Teil, Verifikationsstatus und Trade-offs.

### Option 1 — Nichts tun: „Clean Code ist für Agenten bedeutungslos"
- **Mechanismus:** Wette, dass Agenten günstig genug neu schreiben/refaktorisieren, dass Code-Qualität aufhört zu zählen — analog dazu, wie die Sorge um Memory-Layout irrelevant wurde mit „unbegrenztem" Speicher.[26]
- **Voraussetzungen:** Glaube, dass Agenten-Verständnis unbegrenzt und kostenlos ist; Akzeptanz von „Müll-Code, den nur die KI noch verstehen kann."[27]
- **Hauptschritte:** Keine — den Agenten generieren und mergen lassen.
- **Konfidenz pro Teil:** Die *Position* ist dokumentiert (als echte Minderheitsansicht verifiziert)[26]; ihre *Prämissen* sind **spekulativ** — Praktiker, die „ein zweisätziger Prompt repariert eine Millionen-Zeilen-Codebase" versuchten, fanden, dass es in der Skalierung nicht funktioniert[26], und die Research zeigt, dass Inkohärenz über Iterationen *akkumuliert*[6][10].
- **Verifikationsstatus:** community-berichtete Minderheitsposition; **widerlegt** durch das gemessene Sonar-Effizienz-Ergebnis[5] und die architectural-rot-Research[6].
- **Trade-offs:** Null Vorabkosten; hohe Langzeitkosten (Verständnisschuld, steigende Token-Rechnungen, unreviewbarer Code). Die „Code-Janitor"-Rolle ist das, was diese Option produziert.[28]

### Option 2 — Clean-Code-Regeln in der Instruktionsdatei codieren (AGENTS.md / CLAUDE.md / .cursor/rules)
- **Mechanismus:** Weil LLMs kein persistentes Gedächtnis zwischen Completion haben, muss persistenter Kontext auf Prompt-Ebene erneut injiziert werden; eine kurze, gekürzte Rules-Datei sagt dem Agenten die nicht-offensichtlichen Konventionen des Projekts.[18][16]
- **Voraussetzungen:** Eine gemeinsame, versionierte Instruktionsdatei (AGENTS.md ist der Cross-Agent-Standard)[16]; Disziplin, sie kurz zu halten.
- **Hauptschritte:** Kurze, imperativische Regeln für das *Delta* zu den Defaults schreiben (Namensgebung, Struktur, Fehlerbehandlung, Test-Kommando); radikal kürzen — „für jede Zeile: würde das Entfernen dieser Zeile einen Fehler verursachen? Wenn nicht, streichen"; Regeln nur nach wiederholten Fehlern hinzufügen.[15][19]
- **Konfidenz pro Teil:** Der Mechanismus ist **verifiziert** — alle großen Vendors dokumentieren ihn[15][16][18]. Seine *Ausreichendheit* ist **plausibel-bis-schwach**: es ist beratende Prosa, die der Agent überspringen kann[23], und die Research zeigt, dass detailliertes Prompting den architektonischen Verfall **nicht** mildert[6].
- **Verifikationsstatus:** von jedem großen Vendor dokumentiert (verifiziert); seine Grenzen sind auch dokumentiert („schreibe sauberen Code" steht auf der EXCLUDE-Liste; aufgeblähte Dateien werden ignoriert)[15].
- **Trade-offs:** Günstig, portabel, schnell startklar; aber **beratend** — der Agent ignoriert lange Dateien halbherzig und springt Regeln unter Last über. Notwendig, aber nicht ausreichend.

### Option 3 — Mit maschinell ausführbaren Checks durchsetzen (Linter, Tests, Pre-Commit-Hooks, CI, architektonische Linter)
- **Mechanismus:** Eine in eine Markdown-Datei geschriebene Regel „ist nur ein Vorschlag, den er überspringen kann, denn für das Modell ist es nur mehr Text im Prompt"; das Gate, das hält, ist das, das der Agent **nicht umgehen kann** — ein Pre-Commit-Hook / CI, der bei Fehler non-zero exit.[23][15]
- **Voraussetzungen:** Ein deterministischer Check (Test-Suite, Build, Linter, Type-Checker, Dead-Code-Detektor, Komplexitäts-Check), den der Agent headless ausführen kann; ein Hook/CI, der ihn auf schlechte Commits blockiert.
- **Hauptschritte:** Ein Skript schreiben (Linter + Dead-Code + Komplexität + Tests, bei Fehler non-zero exit); dem Agenten das Kommando geben; dasselbe Skript als Pre-Commit-Hook installieren; optional einen Stop-Hook, der den Turn nicht beenden lässt, bis der Check besteht.[23][15] **Architektonische** Linter (Konsist, Harmonize, ArchUnit-artig) hinzufügen, um die *globale* Inkohärenz zu fangen, die per-File-Linter verpassen.[26][7]
- **Konfidenz pro Teil:** **Verifiziert** über Vendors und Praktiker — Claude-Code-Hooks sind „deterministisch und garantieren, dass die Aktion passiert"[15]; Praktiker berichten „hundert architektonische Lint-Regeln, die die KI verletzt, liest und korrigiert"[26]; die Research schließt „ohne automatisiertes architektonisches Linting… beschleunigt die Akkumulation von struktureller technischer Schuld"[7].
- **Verifikationsstatus:** die am stärksten unterstützte Option (verifiziert, multi-source, und die einzige, die die Research als tatsächlich haltend benennt).
- **Trade-offs:** Höhere Setup-Kosten; erfordert, dass die Checks headless und schnell sind; aber es ist die **einzige** Option, die den Loop schließt, den der Agent nicht selbst schließen kann, und sie fängt den global-inkohärenten Failure-Modus, den Prompting nicht kann.

### Option 4 — Die Codebase selbst als Kontext des Agenten behandeln (die Codebase säubern)
- **Mechanismus:** „Ein Coding-Agent lernt die Konventionen deines Projekts aus dem Code, den er liest, also setzt die Qualität dieses Codes eine Obergrenze für die Qualität dessen, was er schreibt"[23]; sauberer, gut benannter, kleiner, gut abstrahierter Code lässt den Agenten eine Änderung in 1–2 Versuchen landen statt in vielen.
- **Voraussetzungen:** Eine Codebase, die modularisiert/gesäubert werden kann (der 2M-Zeilen-Spaghetti-Fall braucht erst Modularisierung, nicht ein smarteres Modell)[26].
- **Hauptschritte:** Modularisieren, damit der Agent eine Einheit zur Zeit verarbeiten kann; Dinge für `grep` benennen; Dateien klein halten; tiefe Module bevorzugen (viel hinter einer kleinen Interface verstecken) statt flacher Fragmentierung; den Agenten zuerst zum Aufräumen nutzen, dann das Ergebnis gaten.[23][22]
- **Konfidenz pro Teil:** **Verifiziert** und **quantifiziert** — die Sonar-Studie: saubere Codebases → 7,1 % weniger Input-Tokens, 8,5 % weniger Output, 11,1 % weniger Reasoning, ~34 % weniger Datei-Neubesuche, gleiche Pass-Rate[5][4]; Namensgebungseffekt quantifiziert bei 87,3 %→58,7 %[9].
- **Verifikationsstatus:** die einzige Option mit einer kontrollierten, primärquelle-verifizierten Messung — aber es ist eine **Vendor**-Studie, **ein Modell** (Sonnet 4.6), **ein Harness** (Claude Code), **sechs Paare**, weite pro-Aufgaben-Varianz (−47 % bis +44 %), mit einem Gegenbeispiel und token-neutralen Hotspots[5].
- **Trade-offs:** Zahlt sich in *Effizienz* (Tokens, Latenz, Neubesuche) aus, **nicht** in der Pass-Rate[5]; einmalige + laufende Investition; der Effekt ist richtungsweisend, nicht universell.

### Option 5 — Der Full Stack (2 + 3 + 4, zusammen angewendet) — **EMPFOHLEN**
- **Mechanismus:** Die Instruktionsdatei für das *Delta* verwenden (Option 2), Invarianten mechanisch durchsetzen (Option 3) und die Qualität der Codebase selbst heben, damit der Agent von einem guten Kontext startet (Option 4). Jede Schicht deckt die Blindstellen der anderen ab: Prosa ist beratend (→ Hooks), Hooks fangen lokale Smells (→ architektonische Linter fangen globale Inkohärenz), eine saubere Codebase reduziert den Kontext, den der Agent halten muss (→ alles oben wird günstiger).
- **Voraussetzungen:** Alles oben; ein Team, das bereit ist, die Rules-Datei und die Gates zu pflegen.
- **Hauptschritte:** (1) Codebase modularisieren/säubern und den Agenten helfen lassen[23]. (2) Eine kurze AGENTS.md mit den nicht-offensichtlichen Regeln + dem Test-Kommando schreiben[16][15]. (3) Linter + Tests + **architektonische** Linter in einen Pre-Commit-Hook / CI verdrahten, den der Agent nicht umgehen kann[23][26][7]. (4) DRY mit YAGNI paaren und KISS im Review-Loop aufzwingen, um Over-Engineering zu stoppen[15][22]. (5) WHY/Provenance-Kommentare behalten, die Rules-Datei regelmäßig kürzen und Wartungs-/Reflexions-Pässe einplanen[22][19].
- **Konfidenz pro Teil:** Jede Komponente ist **verifiziert** (siehe Optionen 2–4); die *Kombination* ist der de-facto-Konsens von Praktikern und Vendors (als konvergente Praxis verifiziert)[15][23][26][21].
- **Verifikationsstatus:** die einzige Option, die mit **allen drei** Evidenzlinien (Papiere, Vendors, Community) konsistent ist und die, die die Research als tatsächlich haltend gegen den global-inkohärenten Failure-Modus benennt[6][7].
- **Trade-offs:** Höchste Vorabkosten; aber es ist die einzige Option, die den *globalen* (nicht nur lokalen) Failure-Modus adressiert, und sie kumuliert — eine sauberere Codebase macht jeden folgenden Agenten-Lauf günstiger[5][10].

**Ranking & Empfehlung.** **Option 5 (der Full Stack)** wird empfohlen, dann Option 3, dann Option 4, dann Option 2; **Option 1 wird nicht empfohlen** (ihre Prämissen werden durch die gemessene und research-Evidenz widerlegt). **Begründung:** Der gefährlichste Failure-Modus ist *globale* Inkohärenz, die sowohl lokale Checks als auch Prompting verpassen[6][7][27] — nur die **architektonischen Linter + CI von Option 3** fangen sie, und nur die **saubere Codebase von Option 4** macht den Agenten bezahlbar für wiederholte Ausführung[5]. Option 2 allein ist beratend und überspringbar[23]; Option 1 produziert den „Code-Janitor"-Endzustand[28]. Der Full Stack ist die einzige Konfiguration, die mit allen drei unabhängigen Evidenzlinien konsistent ist.

---

## 5. Wichtige Spannungen (als Spannungen präsentiert, nicht als Widersprüche)

1. **„Agenten schreiben nicht von sich aus Clean Code" vs. „LLMs übernehmen den Stil in deinem Repo."** Beide sind wahr: die *Default*-Ausgabe ist „durchschnittlich" (80-Zeilen-Funktionen, kein DI, Duplikation, 2000-Zeilen-Dateien)[22][23], aber ein *sauberes, gut organisiertes* Repo wird übernommen und belohnt[23][5]. Der Default ist der Boden; die Codebase ist die Decke.
2. **„Kleine Funktionen" (der Buchstabe) vs. „kohärent" (der Geist).** Agenten erfüllen „klein", verletzen aber Kohärenz — „sie denken, 'Clean Code' bedeutet, in winzige Funktionen aufzuteilen, statt in kohärente Funktionen"[26] und über-DRYen in brüchige vorzeitige Abstraktionen[22]. Die Research benennt dies als **Modular Mirage**[6].
3. **DRY vs. Over-DRY / Duplikation-als-Kontext.** Der Agent-Fehler ist *verpasste* Duplikat-Kopien beim Edit (begünstigt DRY)[22], aber er *über*-wendet auch DRY[22]; eine Minderheit argumentiert, Wiederholung sei für einen Agenten vielleicht günstiger als eine undichte Abstraktion[26]. Die Literatur löst sich Richtung DRY + YAGNI, nicht intentionale Duplikation.
4. **Oberflächliche Lesbarkeit ≈ menschlich vs. tiefe Wartbarkeit < menschlich.** Atlassian (HULA) findet LLM-Code *vergleichbar* mit menschlichem bei oberflächlichen Lesbarkeitsmetriken, während SWE-CI LLM-Code *schlechter* beim Maintainability Index findet — beide wahr, verschiedene Metriken (Oberfläche vs. Tiefe).[3]
5. **Clean Code hilft Effizienz vs. Clean Code ändert nicht die Pass-Rate.** Die Sonar-Studie zeigt eine echte Token/Neubesuch-Reduktion **und** keine Pass-Rate-Änderung — der Nutzen ist *Effizienz*, nicht *Erfolg*.[5]

---

## 6. Was auf dem exakten Ziel ungetestet bleibt

Die Forschungsfrage benennt spezifische Agenten (Claude Code, OpenAI Codex, Cursor, Devin, SWE-agent, Aider). Die Evidenz ist stark, hat aber diese auf-Ziel-Lücken, offen benannt:

- **Die kommerziellen Agenten sind nicht direkt für das global-inkohärente Phänomen benchmarked.** Die Research, die es dokumentiert (AI-Generated Smells[6], Technical Debt in LLM Architectures[7]) verwendete **MetaGPT-generierte Systeme** und **generierte Microservices**, nicht die spezifisch benannten kommerziellen Agenten in einem echten Produktions-Repo. Das Phänomen ist research-validiert *im Allgemeinen*, aber noch nicht auf Claude Code / Cursor / Devin-Ausgabe spezifisch gemessen.
- **Der quantifizierte Effizienz-Anker ist single-source und schmal.** Die Sonar-Studie ist eine **Vendor**-Studie, **ein Modell** (Claude Sonnet 4.6), **ein Harness** (Claude Code), **sechs Repo-Paare**, mit weiter pro-Aufgaben-Varianz (−47 % bis +44 %) und einem dokumentierten Gegenbeispiel[5]. Kein unabhängiges Labor hat die 7,1 %/8,5 %/34 %-Zahlen repliziert.
- **Kein kontrolliertes A/B isoliert ein einzelnes Prinzip.** Es gibt keine Studie, die *nur* Namensgebung, oder *nur* DRY, oder *nur* SOLID variiert und den Effekt auf die Agenten-Generations-*Korrektheit* (im Gegensatz zu Effizienz) misst. Pro-Prinzip-Effektgrößen sind aus den metrikbasierten Papieren inferiert, nicht aus isolierten Experimenten.[3]
- **Die „global inkohärent"-Research ist small-N oder off-target.** Technical Debt in LLM Architectures ist ein **Pilot** (N=5 Runs/Modell, eine Aufgabe)[7]; AI-Generated Smells verwendet CodeContest + MetaGPT, nicht die benannten Agenten[6].
- **SWE-CIs spezifische Körper-Beobachtungen** (15/20 Pylint vs. 20/20 MI, Null-Regressionsrate) beruhen auf LANE-2s Voll-Lektüre; dieser Lauf bestätigte unabhängig das Dasein und das Abstract des Papiers an der Primärquelle[3], las aber den Körper nicht erneut.
- **Devin-spezifische und Copilot-instructions First-Party-Clean-Code-Guidance** wurde nicht gefunden (nur über die AGENTS.md-Kompatibilitätsliste abgedeckt).

---

## Anhang — Corpus-Map (pro-Finding-Zitate stehen hier)

| Datei | Achse / Teilfrage | Findings |
|---|---|---|
| `principles/lane1.md` | Facet A — der kanonische 10er + wie jedes funktioniert | 51 |
| `papers/lane2.md` | Facet B — Research Papers zu Clean Code & LLM-Code-Qualität | 17 |
| `practice/lane3.md` | Facet B — praktische Erfahrung weltführender KI-Entwickler & Vendors | 67 |
| `community/lane4.md` | Facet B — Community-Praktiker-Erfahrung (Reddit/HN/SO) | 46 |
| `agent-mechanisms/lane5.md` | Facet B — Clean Code × Agenten-Architektur (AMPLIFIED/MOOT/INVERTED) | 61 |
| `verification/lane2-1.md` | Die zwei tragenden Anker (SonarSource, SWE-CI) an der Primärquelle verifizieren | in-session |
| `papers/lane2-2.md` | Ist „lokal sauber, aber global inkohärent" research-bestätigt? | in-session |

*Sprachhinweis:* Der englische Original-Report und alle Lane-Dateien sind auf Englisch — die Sprache, in der die Research produziert wurde (gemäß der Projekt-Archiv-Konvention, dass Research-Results in der Sprache bleiben, in der sie produziert wurden). Diese Datei ist die 1:1-Übersetzung des Hauptberichts ins Deutsche.

## Quellen

[1] https://www.informit.com/store/clean-code-a-handbook-of-agile-software-craftsmanship-9780132350884 — Clean Code (2008) — publisher TOC
[2] https://en.wikipedia.org/wiki/SOLID — Wikipedia: SOLID
[3] https://arxiv.org/abs/2603.03823 — SWE-CI (Chen et al. 2026)
[4] https://arxiv.org/abs/2605.20049 — Does Code Cleanliness Affect Coding Agents? (Sonar study)
[5] https://www.sonarsource.com/blog/your-ai-bill-is-a-code-quality-problem — SonarSource: Your AI bill is a code quality problem
[6] https://arxiv.org/abs/2605.02741 — AI-Generated Smells (Zhu, Tsantalis, Rigby 2026)
[7] https://arxiv.org/abs/2512.04273 — Quantitative Analysis of Technical Debt in LLM Architectures (Slater 2025)
[8] https://arxiv.org/abs/2606.14796 — Faster Code, Deeper Debt? (multivocal review 2026)
[9] https://arxiv.org/abs/2510.03178 — Le et al. 2025 — identifier naming effect
[10] https://www.scbench.ai — SlopCodeBench
[11] https://arxiv.org/abs/2310.06770 — SWE-bench (2023)
[12] https://arxiv.org/abs/2405.15793 — SWE-agent (Princeton, NeurIPS 2024)
[13] https://arxiv.org/abs/2509.16941 — SWE-Bench Pro (Scale, 2025)
[14] https://arxiv.org/abs/2602.07900 — Rethinking Agent-Generated Tests (2026)
[15] https://code.claude.com/docs/en/best-practices — Claude Code best practices (Anthropic)
[16] https://agents.md — AGENTS.md open standard
[17] https://aider.chat/docs/repomap.html — Aider repo map
[18] https://cursor.com/docs/rules — Cursor rules docs
[19] https://developers.openai.com/codex/learn/best-practices — OpenAI Codex best practices
[20] https://cognition.com/blog/dont-build-multi-agents — Cognition: Don't Build Multi-Agents
[21] https://simonw.substack.com/p/how-i-use-llms-to-help-me-write-code — Simon Willison: How I use LLMs to write code
[22] https://akitaonrails.com/en/2026-04-20/clean-code-for-ai-agents — AkitaOnRails: Clean Code for AI Agents
[23] https://aidailycheck.com/learn/clean-code-for-ai-agents — AI Daily Check: Clean Code for AI Agents
[24] https://orbitant.com/en/clean-code-with-ai-agents-best-practices — Orbitant: Clean Code with AI Agents
[25] https://stackoverflow.blog/2026-03-26/coding-guidelines-for-ai-agents-and-people-too — Stack Overflow blog: coding guidelines for AI agents
[26] https://news.ycombinator.com/item?id=47704285 — HN: Clean code in the age of coding agents
[27] https://www.reddit.com/r/ExperiencedDevs/comments/1sibmbw/code_quality_in_the_ai_age — r/ExperiencedDevs: Code quality in the AI age
[28] https://www.reddit.com/r/ExperiencedDevs/comments/1vm2r31/how_many_of_you_are_already_employed_in_ai_code — r/ExperiencedDevs: AI code remediation
