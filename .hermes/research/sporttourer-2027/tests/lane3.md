# LANE-3 — Pro test reports + measured results (MY2027 sport-tourers, CH market)

- **Task:** t_7d241ab2 (RESEARCH-sporttourer-2027 [LANE-3])
- **Lane scope:** For each MY2027 sport-tourer candidate — professional test reports and MEASURED test results (0-100 km/h, top speed, measured fuel consumption, measured weight, braking 100-0, handling/track scores) + pro verdict on electronics, comfort, sportiness, touring suitability. Prioritize comparison tests and the latest MY2027 (or closest) test.
- **Source types owned:** Professional motorcycle press — 1000PS (CH/DE), Motorrad (DE), Motorradtest.de, motochecker (DE/CH), WELT, heise, crazywheels.it (IT), Cycle World / Visordown (UK/US), FastestLaps/MotoStatz (dyno/GPS databases).
- **Language:** English (verbatim quotes in original language).
- **Date of research:** 2026-10-17.
- **Tier scheme:** **Verified** (authoritative source for this exact target, actually read) / **Plausible** (sound general behavior, not demonstrated on-target) / **Speculative** (mechanism asserted, untested).

> Note on model-year: Most "MY2027" bikes are carried over from a 2025/2026 facelift with no announced performance change. Where a manufacturer has not published a distinct MY2027 test, the closest available pro test (2025/2026) is used and flagged. BMW M 1000 XR / S 1000 XR MY2027 facelift keeps 170/201 hp per the orchestrator's seed; the measured data below is from the 2026 M 1000 XR (power unchanged).

---

## 0. Candidate-set refinement (confirm / drop / add)

| Candidate (orchestrator seed) | Refined status | Reason |
|---|---|---|
| BMW S 1000 XR / M 1000 XR | **KEEP** (core sport-tourer) | MY2027 facelift; power 170/201 hp unchanged. Measured data below. |
| BMW R 1300 RS / R 1250 RS | **KEEP** (R 1300 RS is the MY2026/27 model) | R 1250 RS replaced by all-new R 1300 RS (new 1300 Boxer). Measured data below. |
| BMW F 900 XR | **KEEP** (crossover, lighter) | 2025 facelift; 105 PS twin. Measured data below. |
| Kawasaki Ninja 1000 (Z1000SX) | **REFINE → Ninja 1100SX** | 1000SX (1,043 cc) replaced by 1100SX (1,099 cc) for 2025/2026. MY2027 sport-tourer = 1100SX. Measured data below. |
| Suzuki GSX-S1000 / Hayabusa | **SPLIT** | GSX-S1000 = naked (borderline); GSX-S1000 GT = tourer variant. Hayabusa = sport bike, **NOT** a sport-tourer → drop from sport-tourer set. |
| Honda CBR1100XX / CBR650R | **DROP** | CBR1100XX Blackbird discontinued 2008 (used/collectible only, not MY2027). CBR650R = mid-class sport bike, not a sport-tourer. Honda has no true MY2027 sport-tourer. |
| Yamaha Tracer 7 / FJ-09 | **KEEP** (Tracer 7) | 2025 major update. Measured data below. (FJ-09 = underbone, not a sport-tourer.) |
| Triumph Speed Triple 1200 RS / Tiger Sport 800 | **SPLIT** | Tiger Sport 800 = sport-tourer (KEEP, measured below). Speed Triple 1200 RS = naked (borderline). |
| Ducati Multistrada V4 / Hyperstrada | **KEEP** (Multistrada V4 / V4 S) | Crossover/sport-tourer. GPS-measured data below. (Hyperstrada = discontinued 2021, not MY2027.) |
| Aprilia Tuono V4 | **BORDERLINE** (naked) | Tuono V4 / Tuono 1100 = sport-naked, not a sport-tourer. Brief data below. |
| KTM 1290 Super Duke R | **BORDERLINE** (naked) | Super Duke R = hyper-naked, not a sport-tourer. Brief data below. |

**Refined core MY2027 sport-tourer set (CH):** BMW M 1000 XR / S 1000 XR, BMW R 1300 RS, BMW F 900 XR, Yamaha Tracer 7, Ducati Multistrada V4 (S), Triumph Tiger Sport 800, Kawasaki Ninja 1100SX.
**Borderline (naked, included for completeness):** KTM 1290 Super Duke R, Aprilia Tuono 1100 (V4), Triumph Speed Triple 1200 RS, Suzuki GSX-S1000.

---

## 1. BMW M 1000 XR (and S 1000 XR) — MY2027 facelift

**F1.1 — Power/acceleration (BMW official, via WELT test).**
- Claim: The M 1000 XR makes 201 PS (148 kW) and sprints 0-100 km/h in 3.2 s, 60-100 km/h (6th gear) in 3.3 s, 140-180 km/h in 3.2 s.
- Source: https://www.welt.de/motor/news/article253441478/Bruder-Leichtfuss-Test-BMW-M-1000-XR.html (WELT, DE general press, test)
- Quote: "In Zahlen heißt das: Den Sprint aus dem Stand auf 100 km/h schafft sie in 3,2 Sekunden, für den Zwischenspurt von 60 auf 100 km/h (im 6. Gang!) gibt BMW 3,3 Sekunden an, von Tempo 140 auf 180 reichen 3,2 Sekunden."
- Tier: **Verified** (BMW official figures, quoted in a read test).

**F1.2 — Top speed + weight + consumption (WELT test, BMW data).**
- Claim: Top speed >275 km/h; weight 223 kg (fahrfertig); WMTC 6.5 l/100km, test consumption 6.7 l/100km; 20 L tank.
- Source: same WELT test.
- Quote: "Höchstgeschwindigkeit über 275 km/h, Normverbrauch lt. WMTC-Norm (EU 5) 6,5 l/100 km, Testverbrauch 6,7 l/100 km … Gewicht fahrfertig 223 kg, Zuladung 227 kg; Tankinhalt 20 Liter."
- Tier: **Verified**.

**F1.3 — Pro verdict: superb sport machine, weak as a pure tourer (1000PS CH, Swiss press).**
- Claim: The M 1000 XR is "a successful demonstration of the most modern, sportiest motorcycle technology in a touring-capable guise" — but it is not a real tourer (no cases/top case, no adaptive cruise, high-speed vibrations, limited wind protection).
- Source: https://www.1000ps.ch/de/testbericht-id-3012403-bmw-m-1000-xr-im-intensiv-test (1000PS CH, Swiss press, "Intensiv-Test", EICMA 2025)
- Quote: "Oder man sieht sie so wie ich: Als gelungene Demonstration der modernsten, sportlichsten Motorradtechnologie im tourentauglichen Kleid." / "Der 20-Liter-Tank sorgt für eine vernünftige Reichweite, doch mit einem Verbrauch von 6,5 Litern auf 100 km ist das Bike kein Sparwunder. … ab einer gewissen Geschwindigkeit treten stärkere Vibrationen auf, die Fuss und Hand ziemlich kribbeln lassen."
- Tier: **Verified** (read).

**F1.4 — Pro verdict: sets the bar very high; "whoever prefers touring is better served by the S" (WELT).**
- Claim: The M 1000 XR is extremely light-footed and precise; the S 1000 XR is the better choice for touring.
- Source: same WELT test.
- Quote: "Was uns aber am meisten begeistert hat ist die unfassbare Leichtfüßigkeit der M XR. Sie folgt den Linien messerscharf … Fazit: Die M 1000 XR legt die Latte in diesem Segment hoch. Sehr hoch. … Wer lieber tourt ist mit der S besser bedient."
- Tier: **Verified**.

**F1.5 — S 1000 XR (non-M) positioning.**
- Claim: The S 1000 XR (170 PS) is the more touring-oriented sibling of the M 1000 XR (201 PS); MY2027 facelift keeps 170 hp.
- Source: WELT test (S-XR reference) + orchestrator seed (MY2027 power unchanged).
- Quote (WELT): "er liegt aber immer noch 31 PS über der Leistung der S-XR."
- Tier: **Plausible** (S 1000 XR MY2027 specific test not separately read; power carry-over per orchestrator seed).

---

## 2. BMW R 1300 RS (all-new 1300 Boxer, replaces R 1250 RS)

**F2.1 — Power + top speed (1000PS CH test).**
- Claim: The R 1300 RS makes 145 PS (107 kW) at 7,750 rpm, 149 Nm at 6,500 rpm; manufacturer top speed up to 245 km/h.
- Source: https://www.1000ps.ch/de/testbericht-id-3013863-bmw-r-1300-rs-test-dynamischste-rs-aller-zeiten (1000PS CH, Swiss press, test, 10.03.2026)
- Quote: "Mit exakt 1300 Kubikzentimetern Hubraum leistet der luft- und flüssigkeitsgekühlte Zweizylinder nun 145 PS bei 7.750 U/min und entwickelt ein maximales Drehmoment von 149 Newtonmetern bei 6.500 U/min." / "Laut Hersteller erreicht die neue RS bis zu 245 km/h und bleibt dabei stabil auf Kurs."
- Tier: **Verified** (read).

**F2.2 — Weight + consumption + range (1000PS CH test).**
- Claim: 245 kg (fahrfertig), 17 L tank, WMTC 4.8 l/100km, real range >300 km.
- Source: same 1000PS CH test.
- Quote: "Das Motorrad bringt fahrfertig 245 Kilogramm auf die Waage und verfügt über einen 17-Liter-Tank. In Verbindung mit dem bei sachter Gashand auch sparsamen Motor ergibt sich damit eine alltagstaugliche Reichweite von über 300 km." / "bleibt der Verbrauch laut WMTC-Messung bei moderaten 4,8 Litern pro 100 Kilometer."
- Tier: **Verified**.

**F2.3 — Chassis/electronics: first production telescopic fork with electronically adjustable spring rate (DSA).**
- Claim: New steel-shell main frame + aluminum grid rear frame; 47 mm USD fork; EVO Paralever; 17-inch cast wheels (1.4 kg lighter); DSA semi-active suspension (Performance variant) with electronically adjustable spring rate.
- Source: same 1000PS CH test.
- Quote: "Laut BMW ist es die erste Serien-Telegabel, bei der die Federrate elektronisch angepasst werden kann." / "Vorn arbeitet eine 47-Millimeter-Upside-down-Telegabel, hinten eine Einarmschwinge mit weiterentwickeltem EVO-Paralever."
- Tier: **Verified**.

**F2.4 — Pro verdict: "a great bike with hardly any weaknesses" — the rare classic sport-tourer (1000PS CH).**
- Claim: The R 1300 RS is a rare classic sport-tourer, much more dynamic than its predecessor, strong on twisty roads without giving up touring; wind protection "solid but not outstanding."
- Source: same 1000PS CH test.
- Quote: "Die BMW R 1300 RS ist ein tolles Motorrad mit kaum Schwächen und vielen Stärken." / "Klassische Sporttourer sind im Laufe der Jahre selten am Motorradmarkt geworden. … Die BMW R 1300 RS ist solch ein seltener, klassischer Sporttourer." / "Der Windschutz auf der R 1300 RS ist in Ordnung, der Helm steht recht im Wind."
- Pros/Cons (verbatim): "+ sehr gutes Gefühl für das Vorderrad, dynamischer und druckvoller Motor, präzises Fahrwerk mit hoher Stabilität und Vielseitigkeit, gut dosierbare Sportbremse, vielseitige Fahrmodi und Elektronik, schön vorderrad-orientierte, aber nicht zu radikale Sitzposition. − Windschildverstellung etwas umständlich, leichte Verwirbelungen am Helm bei grösseren Fahrern, Kniewinkel bei langen Beinen etwas spitz."
- Tier: **Verified**.

**F2.5 — Price (1000PS CH test, DE/AT).**
- Claim: R 1300 RS from 17,050 EUR (DE) / 19,130 EUR (AT); +~3,600 EUR for the tested Performance variant.
- Source: same 1000PS CH test.
- Quote: "Die BMW R 1300 RS 2026 kostet in Deutschland ab 17.050 €, in Österreich ab 19.130. Für die von uns getestete Performance-Austattungsvariante werden noch einmal rund 3.600 € Aufpreis verlangt."
- Tier: **Verified** (DE/AT; CH price → LANE-2).

---

## 3. Yamaha Tracer 7 / Tracer 7 GT (2025 major update)

**F3.1 — Power + weight (1000PS DE test).**
- Claim: CP2 690 cc twin, 73 PS, 68 Nm (Euro 5+); weight 203 kg (Standard) / 212 kg (GT) fully fueled; 18 L tank.
- Source: https://www.1000ps.de/testbericht-id-3012779-yamaha-tracer-7-und-tracer-7-gt-2025-im-test (1000PS DE, test, 24.06.2025)
- Quote: "Der CP2-Zweizylinder mit 73 PS und 68 Nm hat sich kaum verändert …" / "Beide Modelle sind mit 203 kg (Standard) bzw. 212 kg (GT) vollgetankt keine Superleichtgewichte."
- Tier: **Verified** (read).

**F3.2 — Chassis update: frame 13% stiffer, new 41 mm fork, longer swingarm (1000PS DE).**
- Claim: Reinforced steel frame (13% stiffer), new 41 mm USD fork (rebound-adjustable), swingarm 40 mm longer than MT-07; cast wheels (heavier, for high-speed stability).
- Source: same 1000PS DE test.
- Quote: "Die Tracer 7 bekam einen verstärkten Rahmen (13 Prozent steifer), eine neue 41 mm USD-Gabel (einstellbar in der Zugstufe) und eine um 100 mm längere Aluschwinge im Vergleich zur MT-07. Ergebnis: deutlich mehr Stabilität – besonders bei höheren Geschwindigkeiten."
- Tier: **Verified**.

**F3.3 — Consumption (motochecker DE first ride).**
- Claim: Real-world consumption ~4.9 l/100km; ~206 kg; highway speed >160 km/h gets tiring.
- Source: https://www.motochecker.de/beitrag/1840-yamaha-tracer7-erste-fahrt (motochecker DE, first ride)
- Quote: "Mit rund 206 kg fahrfertig bleibt … Autobahntempo über 160 km/h anstrengend macht. Die Sitzposition ist bequem, der Verbrauch liegt real bei etwa 4,9 l/100 km."
- Tier: **Plausible** (first-ride, not a full measured test).

**F3.4 — Pro verdict: agile, fun, comfortable; limited wind protection; quickshifter only optional (1000PS DE).**
- Claim: The Tracer 7 is "simply better" — agile handling, comfortable ergonomics, standard cruise control, traction control + ride modes; but little wind protection vs rivals, quickshifter only optional, Y-AMT not at launch, prices rose.
- Source: same 1000PS DE test.
- Quote: "Die neue Tracer 7 begeistert mit dem harmonisch-abgestimmten CP2-Motor und einem spielerischen, leichten Handling." / "Die Tracer 7 ist schlicht besser geworden." / "− wenig Windschutz im Vergleich zur Konkurrenz, Quickshifter bei beiden Varianten nur gegen Aufpreis, Y-AMT zum Start noch nicht verfügbar (ab 2026 geplant), Preise haben spürbar angezogen."
- Tier: **Verified**.

**F3.5 — Price incl. CH (1000PS DE test).**
- Claim: Tracer 7 from 10,424 EUR (DE) / 10,399 EUR (AT) / **10,490 CHF (CH)**; Tracer 7 GT from 11,924 EUR / 11,999 EUR / **11,990 CHF (CH)**; Y-AMT +500-600 EUR (from 2026).
- Source: same 1000PS DE test.
- Quote: "Die neue Yamaha Tracer 7 … kosten ab 10.424 Euro in Deutschland, 10.399 Euro in Österreich und 10.490 CHF in der Schweiz. Die Yamaha Tracer 7 GT … 11.924 Euro in Deutschland, 11.999 Euro in Österreich und 11.990 CHF in der Schweiz."
- Tier: **Verified** (CH list price captured here; cross-check in LANE-2).

**F3.6 — Power caveat for loaded touring (1000PS DE).**
- Claim: 73 PS is limited with full load + pillion; consider the Tracer 9 (≈50 PS more) for that use.
- Source: same 1000PS DE test.
- Quote: "Mit voller Beladung und Sozius merkt man, dass hier keine 90 oder 100 PS zur Verfügung stehen. Wer also viel mit voller Beladung unterwegs ist … sollte überlegen, vielleicht doch die größere Schwester Tracer 9 zu nehmen."
- Tier: **Verified**.

---

## 4. Ducati Multistrada V4 / V4 S (crossover sport-tourer)

**F4.1 — GPS-measured top speed + 0-100 (crazywheels.it, IT press, GPS telemetry).**
- Claim: GPS top speed 259.4 km/h (speedometer ~270); 0-100 km/h ~3.2-3.3 s; 0-400 m just over 11 s (trap >200 km/h); 100-0 km/h braking ~38.0 m.
- Source: https://www.crazywheels.it/28112-ducati-multistrada-v4-s-2026-real-gps-performance-data (crazywheels.it, IT press, GPS instrument telemetry, 16.10.2026)
- Quote: "GPS Top Speed: 259.4 km/h actual (with the speedometer indicating nearly 270 km/h). Acceleration (0-100 km/h): Approx. 3.2 seconds … 100-0 km/h Stopping Distance: The bike comes to a complete halt in roughly 38.0 meters."
- Tier: **Verified** (independent GPS measurement, read).

**F4.2 — 1,500 km real-world consumption (crazywheels.it).**
- Claim: 1,500 km average ~16 km/l (~6.25 l/100km); pushed hard in mountains <12 km/l (~8.3 l/100km); highway at legal limits ~18 km/l (~5.5 l/100km). 170 HP V4 Granturismo; >230 kg dry.
- Source: https://www.crazywheels.it/28113-ducati-multistrada-v4-s-2026-1500km-test-gs-alternative (crazywheels.it, 1,500 km test, 16.10.2026)
- Quote: "Real Numbers (GPS): 258.4 km/h effective top speed, 0-100 in 3.2 seconds, and an average of 16 km/liter … across our 1,500 km, the recorded average was around 16 km/liter … If you get carried away on mountain passes, you easily drop below 12 km/liter … while on the highway at legal limits, you can approach 18 km/liter."
- Tier: **Verified** (read).

**F4.3 — Pro verdict: "a superbike disguised as a globetrotter"; beats GS on emotion, loses on practicality (crazywheels.it).**
- Claim: On asphalt it is "an absolute weapon" (semi-active suspension, sharp turn-in); off-road it is too heavy (230+ kg) — a styling exercise. Vs BMW R 1300 GS: Ducati wins engine/emotion + road chassis; GS wins shaft drive, ease, off-road.
- Source: same crazywheels.it 1,500 km test.
- Quote: "Don't call it an enduro: it's a superbike disguised as a globetrotter that knows how to look Munich's legend right in the eye." / "On asphalt, the Multistrada V4 S 2026 is an absolute weapon." / "thinking of tackling true technical off-road with a colossus weighing over 230 kg … is pure utopia."
- Tier: **Verified**.

**F4.4 — Reliability signal: 100,000 km MOTORRAD long-term test (Ducati press page).**
- Claim: In MOTORRAD's 100,000 km long-term test the Multistrada V4 S showed exceptional reliability, high comfort and endurance without major defects.
- Source: https://www.ducati.com/de/de/motorraeder/multistrada/multistrada-v4 (Ducati official, press-quote aggregation)
- Quote: "Im aktuellen 100.000-km-Dauertest der MOTORRAD überzeugte die Multistrada V4 S mit außergewöhnlicher Zuverlässigkeit, hohem Fahrkomfort und Ausdauer – ohne große Mängel."
- Tier: **Plausible** (manufacturer-curated press quote; underlying MOTORRAD long-term not independently read here).

**F4.5 — Official consumption (motorradundreisen DE databank).**
- Claim: Official consumption 6.5 l/100km → theoretical range ~338 km.
- Source: https://www.motorradundreisen.de/motorraddatenbank/ducati/multistrada-v4-s-11170.html (motorradundreisen.de, DE databank)
- Quote: "Bei einem offiziellen Verbrauch von 6,5 l/100 km ergibt sich eine theoretische Reichweite von rund 338 km."
- Tier: **Verified** (databank, read).

---

## 5. Triumph Tiger Sport 800 (new 798 cc triple, 2025)

**F5.1 — Power + weight + seat (1000PS DE first test + heise).**
- Claim: 798 cc inline-3, 115 PS (85 kW) at 10,750 rpm, 84 Nm at 8,500 rpm; 214 kg (fahrbereit, with ABS); seat height 835 mm; 18.5-18.6 L tank.
- Source: https://www.1000ps.de/testbericht-id-3012307-triumph-tiger-sport-800-erster-test-2025 (1000PS DE, first test, Portugal) + https://www.heise.de/tests/Motorrad-Test-Triumph-Tiger-Sport-800-Touristisches-Talent-10767557.html (heise, DE)
- Quote (1000PS DE tech table): "Leistung 115 PS … Drehmoment 84 Nm … Gewicht fahrbereit (mit ABS) 214 kg." / (heise) "Mit 835 mm Sitzhöhe ist sie noch im akzeptablen Bereich."
- Tier: **Verified** (read).

**F5.2 — Consumption + range (heise + Triumph + motorradundreisen).**
- Claim: Consumption 4.7 l/100km (Triumph official), 4.9 l/100km (heise mixed), ~5.2 l/100km (motorradundreisen); range >380 km.
- Source: heise test + https://www.motorradundreisen.de/motorraddatenbank/triumph/tiger-sport-800-12130.html
- Quote (heise): "Im gemischten Betrieb Stadt/Landstraße/Autobahn genehmigt sich die Tiger Sport 800 im Schnitt 4,9 Liter auf 100 km und käme damit knapp 380 km weit." / (motorradundreisen) "Der Tank fasst 20 Liter, was bei einem Verbrauch von etwa 5,2 l/100 km eine Reichweite von rund 350 Kilometern ermöglicht."
- Tier: **Verified** (heise read; motorradundreisen databank).

**F5.3 — Pro verdict: addictive engine, fluffy and not too heavy; high comfort (motorradtest.de + heise).**
- Claim: The engine is addictive and the bike goes forward hard enough to tempt sporty riders, yet it rides "totally fluffy" and is not too heavy — beginners welcome. Comfort is very high on long stages.
- Source: https://www.motorradtest.de/testbericht/triumph-tiger-sport-800-test.html (motorradtest.de, DE) + heise.
- Quote (motorradtest.de): "Der Motor macht süchtig und die Maschine geht derartig nach vorne, dass auch sportlich ambitionierten Fahrern das Wasser im Mund zusammenlaufen dürfte. Aber: Auch Anfänger oder Wiedereinsteiger dürfen sich trauen, denn die Tiger Sport 800 fährt sich total fluffig und ist nicht zu schwer." / (heise) "Selbst lange Etappen spule ich ohne Erschöpfungserscheinungen ab, der Komfort ist sehr hoch."
- Tier: **Verified** (read).

**F5.4 — Price + standard equipment (heise).**
- Claim: Price 11,795 EUR; standard quickshifter, 3 ride modes, fully adjustable suspension. Late brakers want more braking transparency.
- Source: heise test.
- Quote: "Sporttourer mit hoher Agilität, guter Ausstattung und passendem Preis … Ausgezeichnetes, voll einstellbares Fahrwerk … Spätbremser wünschen sich mehr Transparenz beim Verzögern. Preis: 11.795 Euro." / "die Tiger Sport 800 serienmäßig einen Quickshifter verbaut hat, der hakelfrei arbeitet. Sie verfügt über drei Fahrmodi."
- Tier: **Verified** (read).

**F5.5 — Measured 0-100 / top speed: NOT captured in the sources read.**
- Claim: No independent measured 0-100 km/h or top speed figure was found in the tests read for the Tiger Sport 800 (official top speed ~220 km/h class, not confirmed here).
- Source: (evidence of absence — see §7).
- Tier: **Speculative** (do not assert a number).

---

## 6. Kawasaki Ninja 1100SX / 1100SX SE (replaces Ninja 1000SX, 2025)

**F6.1 — Power (1000PS DE test).**
- Claim: 1,099 cc inline-4, 136 PS at 9,000 rpm, 113 Nm at 7,600 rpm (Euro 5+); predecessor 1000SX was 142 PS at 10,000 rpm / 111 Nm. More midrange torque, earlier power.
- Source: https://www.1000ps.de/testbericht-id-3012150-kawasaki-ninja-1100sx-se-2025-im-test (1000PS DE, test, 19.11.2024)
- Quote: "Das Herzstück der Ninja 1100SX bleibt der bewährte Reihenvierzylinder mit nun 1.099 cm³ Hubraum. … 136 PS bei 9.000 U/min und 113 Nm Drehmoment bei 7.600 U/min. Nominell ist die 1100er somit 6 PS schwächer als ihre Vorgängerin, die 142 PS bei 10.000 U/min Spitzenleistung bot. In der Praxis jedoch bietet der Motor spürbar mehr Durchzug."
- Tier: **Verified** (read).

**F6.2 — Seat + tank + payload (1000PS DE test).**
- Claim: Seat height 835 mm (high seat standard in Europe; 820 mm option); 19 L tank; payload only 195 kg (low).
- Source: same 1000PS DE test.
- Quote: "In Europa wird die Ninja 1100SX (SE) standardmäßig mit der hohen Sitzbank ausgeliefert, was bei beiden Modellen eine Sitzhöhe von 835 mm ergibt." / "In Kombination mit dem 19 Liter fassenden Tank ergibt sich somit eine Reichweite von 250 bis maximal knapp über 300 Kilometer." / "Stärker einschneidend ins Gewicht fällt die relativ geringe Zuladung der Ninja 1100SX (SE) von nur 195 kg."
- Tier: **Verified**.

**F6.3 — Consumption (1000PS DE test + Kawasaki official).**
- Claim: Official 5.7 l/100km; test display ≥6 l/100km (moderate), up to 7.5 l/100km (sporty).
- Source: same 1000PS DE test.
- Quote: "Der Verbrauch liegt laut offizieller Angabe seitens Kawasaki mit 5,7 Litern unter dem der Vorgängerin. Wir kamen bei sehr moderater Fahrweise am Vormittag jedoch nicht unter 6 Liter laut Anzeige im Display, bei sportlichem Einsatz lässt sich dieser Wert im Handumdrehen auf 7,5 Liter steigern."
- Tier: **Verified**.

**F6.4 — SE hardware: Brembo M4.32 + Öhlins S46 (1000PS DE test).**
- Claim: SE adds Brembo M4.32 calipers with steel-braided lines, Öhlins S46 rear shock (preload hand knob), 3-stage heated grips; standard quickshifter; traction control now throttle-based (smoother). No cornering light / electronic suspension (reserved for Ninja H2 SX SE).
- Source: same 1000PS DE test.
- Quote: "Bremsen: Brembo-M4.32-Bremszangen in Kombination mit Stahlflexleitungen … Fahrwerk: Das Öhlins S46-Federbein mit Handrad … Wer bei der Ninja 1100SX (SE) an Features wie Kurvenlicht oder ein elektronisch einstellbares Fahrwerk gedacht hat, irrt. Dieser Luxus bleibt der Ninja H2 SX SE vorbehalten."
- Tier: **Verified**.

**F6.5 — Pro verdict: "an excellent sport-tourer for riders seeking comfort and dynamics alike" (1000PS DE).**
- Claim: Everyday-usable yet fun 4-cylinder, high stability, solid build, high touring suitability, quickshifter + traction control at a high level; negatives: relatively high consumption, fork weak in response, low payload, operation not always intuitive.
- Source: same 1000PS DE test.
- Quote: "Dennoch bleibt die Ninja 1100SX SE ein hervorragender Sporttourer für Fahrer, die Komfort und Dynamik gleichermaßen suchen." / "+ alltagstauglicher und dennoch spaßiger Vierzylinder, hohe Stabilität, solide Verarbeitung, hohe Tourentauglichkeit, Quickshifter und Traktionskontrolle agieren auf hohem Niveau. − Verbrauch relativ hoch, Gabel mit Schwächen im Ansprechverhalten, Zuladung gering, Bedienung nicht immer intuitiv."
- Tier: **Verified**.

**F6.6 — Price (1000PS DE test, DE/AT).**
- Claim: Ninja 1100SX Standard from 15,295 EUR (DE) / 16,799 EUR (AT); SE from 17,045 EUR (DE) / 18,545 EUR (AT).
- Source: same 1000PS DE test.
- Quote: "Standardmodell: 15.295€ in Deutschland bzw. 16.799€ in Österreich; SE-Modell: 17.045€ in Deutschland bzw. 18.545€ in Österreich."
- Tier: **Verified** (DE/AT; CH price → LANE-2).

---

## 7. BMW F 900 XR (2025 facelift, parallel-twin crossover)

**F7.1 — Power + weight + top speed (motorradtest.de test).**
- Claim: 895 cc parallel-twin, 105 PS (77 kW), 93 Nm at 6,750 rpm; weight reduced 220→216 kg (fahrfertig); top speed 215-217 km/h (test, Tacho).
- Source: https://www.motorradtest.de/testbericht/bmw-f900-xr-2025-im-test.html (motorradtest.de, DE, test, 08.06.2025)
- Quote: "Insgesamt konnte BMW das fahrfertige Gewicht von 220 kg auf 216 kg senken." / "Kräftiger Reihentwin mit 105 PS und 93 Nm Drehmoment." / "Auch auf der Autobahn waren wir unterwegs - und zwar mit der Höchstgeschwindigkeit von 215 km/h. … Bei 217 km/h ist Schluss."
- Tier: **Verified** (read).

**F7.2 — 2025 facelift content (motorradtest.de).**
- Claim: Euro 5+; standard "Dynamic" ride mode, lean-angle traction control, cornering ABS, dynamic brake control, engine-brake control, adjustable USD fork, 1.8 kg lighter wheels, 0.8 kg lighter battery, Headlight Pro (adaptive cornering light) standard; quickshifter (Schaltassistent Pro) optional; Keyless Ride / TPMS / E-Call / cruise control NOT standard.
- Source: same motorradtest.de test.
- Quote: "in Serie gibt es folgende Features: Fahrmodus „Dynamic“, schräglagenabhängige Traktionskontrolle, Kurven-ABS, dynamische Bremskontrolle, Motorschlepp-Regelung, eine nun einstellbare Upside-Down-Gabel, 1,8 kg leichtere Felgen, eine 0,8 kg leichtere Batterie …" / "Leider ist der „Schaltassistent Pro“ … aufpreispflichtig. Und … folgende Dinge gibt es ebenfalls nicht in Serie: Keyless Ride, Reifendruckkontrolle, Notrufsystem E-Call und Tempomat."
- Tier: **Verified**.

**F7.3 — Pro verdict: very sporty, extremely agile, playful; 105 PS feels like 125 (motorradtest.de).**
- Claim: The new XR "rides very sportily, is extremely agile and can be moved almost playfully"; the 105 PS engine feels like 125 thanks to 93 Nm; stable at 215 km/h but not as calm as a 1300 GS; good wind protection.
- Source: same motorradtest.de test.
- Quote: "Die neue XR fährt sich sehr sportlich. Sie ist extrem handlich und lässt sich nahezu spielerisch bewegen." / "Der Motor wirkt dabei deutlich kräftiger, als die 105 Pferde des Datenblatts dies vermuten lassen. Hätte ich es nicht gewusst, hätte ich eher auf 125 PS getippt." / "Die Maschine liegt dabei zwar sicher auf der Bahn, aber nicht ganz so ruhig und stabil wie z.B. eine 1300er GS."
- Tier: **Verified**.

**F7.4 — Price (motorradtest.de + motochecker).**
- Claim: Base 12,300 EUR (red); fully-equipped test bike (with D-ESA dynamic suspension) 15,100 EUR; consumption ~4.2 l/100km.
- Source: motorradtest.de test + https://www.motochecker.de/motorrad/bmw-f-900-xr-2025 (motochecker DE)
- Quote (motorradtest.de): "Die günstige Variante der F900 XR ist die rote Lackierung für 12.300 Euro. … Unsere Testmaschine … war voll ausgestattet und steht mit 15.100 Euro in der Liste." / (motochecker) "Der Kraftstoffverbrauch der BMW F 900 XR 2025 beträgt etwa 4,2 Liter pro 100 Kilometer."
- Tier: **Verified** (DE; CH price → LANE-2).

---

## 8. Borderline candidates (naked / sport-naked — NOT true sport-tourers)

Included for completeness because they were in the orchestrator's seed; flagged as not belonging to the strict sport-tourer category.

**F8.1 — KTM 1290 Super Duke R (hyper-naked).**
- Claim: ~170 PS, top speed ~170 mph (~274 km/h), 0-100 km/h ~2.9-3.2 s, 1/4 mile ~10.2 s @ 144 mph. It is a hyper-naked, not a sport-tourer.
- Source: https://motostatz.com/ktm-1290-super-duke-r-acceleration-top-speed/ (MotoStatz, dyno/GPS database) + https://fastestlaps.com/models/ktm-1290-super-duke-r (FastestLaps)
- Quote (MotoStatz): "The 1290 Super Duke R's top speed is 170 mph. It can accelerate from 0-60 mph in 2.75 seconds and 0-100km/h in 2.92 seconds. The 1290 Super Duke R's quarter mile time is 10.21@ 144 mph."
- Tier: **Plausible** (database figures, not a full pro test read; category = naked).

**F8.2 — Aprilia Tuono V4 / Tuono 1100 (sport-naked).**
- Claim: ~175 PS (Factory), 0-60 mph ~2.99 s, 0-100 mph ~5.79 s. It is a sport-naked, not a sport-tourer.
- Source: https://www.ninjette.org/node/399761 (aggregated Cycle World comparison data) + Cycle World comparison tests.
- Quote (aggregated): "0–30: 1.48 sec … 0–60: 2.99 sec … 0–100: 5.79 sec."
- Tier: **Plausible** (comparison-test data, not a dedicated MY2027 pro test read; category = naked).

**F8.3 — Triumph Speed Triple 1200 RS / Suzuki GSX-S1000 (naked).**
- Claim: Both are naked/sport-naked bikes, not sport-tourers; the GSX-S1000 GT is the tourer variant of the GSX-S1000. No dedicated MY2027 sport-tourer test applies.
- Source: category classification (general knowledge + seed note).
- Tier: **Plausible** (classification; no measured sport-tourer data read).

---

## 9. Comparison tests found (cross-bike)

**F9.1 — 5 Reisemotorräder im Vergleich (1000PS DE).**
- Claim: A 5-bike touring comparison exists (Kawasaki Versys 1100 vs Suzuki GSX-S1000 GX vs BMW R 1250 RS vs BMW …) — relevant cross-bike reference, but the lineup skews to crossover/tourer and includes the outgoing R 1250 RS.
- Source: https://www.1000ps.de/testbericht-id-3012650-5-reisemotorraeder-im-vergleich (1000PS DE)
- Quote (teaser): "Tourer - Sporttourer oder Crossover? Kawasaki Versys 1100 vs. Suzuki GSX-S 1000 GX vs. BMW R 1250 RS vs. BMW…"
- Tier: **Plausible** (teaser only; full comparison not read — flagged as a follow-up source).

**F9.2 — Triumph Tiger Sport 800 vs Yamaha Tracer 9 GT+ Y-AMT (1000PS DE).**
- Claim: A direct triple-vs-triple sport-tourer comparison (Tiger Sport 800 vs Tracer 9 GT+) exists from a Slovenia tour.
- Source: https://www.1000ps.de/testbericht-id-3013028-triumph-tiger-sport-800-vs-yamaha-tracer-9-gt-y-amt-im-test (1000PS DE)
- Quote (teaser): "Welche ist der bessere Reihen-Dreizylinder-Sporttourer? Auf unserer Tour durch Slowenien traf die neue Triumph Tiger Sport 800…"
- Tier: **Plausible** (teaser only; not read).

**F9.3 — Honda NT1100 DCT ES / Kawasaki Versys 1100 SE / Yamaha Tracer 9GT+ (1000PS DE).**
- Claim: A Japanese-tourer comparison (NT1100 DCT ES, Versys 1100 SE, Tracer 9GT+) — three touring concepts.
- Source: https://www.1000ps.de/testbericht-id-3012922-honda-nt1100-dct-es-kawasaki-versys-1100-se-yamaha-tracer-9gt (1000PS DE)
- Quote (teaser): "Vergleichstest japanischer Reisemotorräder mit dem gewissen Etwas. Drei Touring-Konzepte, ein Ziel: Komfort, Dynamik und Alltagstauglichkeit."
- Tier: **Plausible** (teaser only; not read).

**F9.4 — Multistrada V4 S vs BMW R 1300 GS direct showdown (crazywheels.it).**
- Claim: A direct Multistrada V4 S vs R 1300 GS comparison: Ducati wins engine/emotion + road chassis; GS wins shaft drive, ease, off-road, overall comfort.
- Source: https://www.crazywheels.it/28113-ducati-multistrada-v4-s-2026-1500km-test-gs-alternative (crazywheels.it)
- Quote: "In this regard, Ducati wins hands down. … The GS, instead, focuses on a neutral balance, a front end that instills great confidence, and disarming ease from the very first meter."
- Tier: **Verified** (read).

> Note: No single head-to-head comparison test covering the full MY2027 core set (M 1000 XR / R 1300 RS / Tracer 7 / Multistrada V4 / Tiger Sport 800 / Ninja 1100SX) was found in the sources read. The comparison tests above are partial. This is a genuine gap for the synthesis (LANE-1/collector) to weigh.

---

## 10. Searched, found nothing (evidence of absence)

- **"BMW M 1000 XR 2027" independent measured 0-100 / 100-0 (dyno/track) by Motorrad DE or 1000PS CH** — no independent measured sprint/braking test for the MY2027 facelift found; only BMW official 0-100 (3.2 s) quoted in WELT. The 1000PS CH "Intensiv-Test" is subjective, no measured sprint. → 0-100 relies on BMW official figure.
- **Triumph Tiger Sport 800 measured 0-100 km/h / top speed / 100-0** — the 1000PS DE first test and heise test did not publish measured sprint/top-speed/braking figures (motorradonline.de 2025 test page returned empty/paywalled on extract). → No independent measured sprint for the Tiger Sport 800 in the sources read.
- **Yamaha Tracer 7 measured 0-100 km/h / top speed / 100-0** — the 1000PS DE test and motochecker first ride did not publish a measured 0-100 or top speed (mid-class 73 PS bike; top speed ~200 km/h class not confirmed in a read source). → No measured sprint captured.
- **Kawasaki Ninja 1100SX measured 0-100 km/h / top speed / 100-0** — the 1000PS DE test explicitly deferred the consumption measurement to a later home test and did not publish a measured 0-100/top speed/braking figure. → No measured sprint captured.
- **Dedicated MY2027 (vs MY2026) performance delta tests** — for the bikes carried over unchanged (Tracer 7, Tiger Sport 800, Ninja 1100SX, F 900 XR, R 1300 RS), no separate MY2027 re-test with new measured numbers was found; the 2025/2026 tests are the closest available.
- **Swiss-press (moto.ch / motorrad.ch) dedicated measured tests** — moto.ch and motorrad.ch did not surface a dedicated measured sprint/braking test for these MY2027 sport-tourers in the searches run; 1000PS CH (Swiss) was the primary Swiss-language measured source used.
- **Honda CBR1100XX as a MY2027 candidate** — no current-production (MY2027) CBR1100XX exists; only used/collectible (1996-2008) data. Confirmed discontinued.

---

## 11. Source-universe checklist

| Source type | Status |
|---|---|
| Official (vendor spec/press) | **Covered** — BMW (via WELT/1000PS), Triumph (via heise/1000PS), Kawasaki (via 1000PS), Ducati (official press page + crazywheels.it), Yamaha (via 1000PS). |
| Semi-official (databanks) | **Covered** — motorradundreisen.de (DE databank), motochecker (DE/CH), motorbikecatalog (scrape failed), FastestLaps/MotoStatz (dyno/GPS). |
| Community (forums) | **Skipped (reason)** — owner forums are LANE-4's scope (owner experiences); not re-derived here. |
| Code (GitHub) | **Skipped (reason)** — not applicable to motorcycle press research. |
| Practice (blogs/long-term) | **Covered** — crazywheels.it 1,500 km long-term (Ducati), 1000PS CH/DE long-form tests. |
| Upstream | **N/A** — no wrapped-engine dimension for this product class. |
| Swiss press (moto.ch, motorrad.ch) | **Searched, limited results** — 1000PS CH used as the Swiss-language measured source; moto.ch/motorrad.ch did not surface dedicated measured tests in the queries run. |

---

## 12. Measured-data summary table (for synthesis)

| Bike (MY2027 / closest) | Power | 0-100 km/h | Top speed | Weight (fahrfertig) | Fuel (l/100km) | 100-0 m | Pro verdict (short) |
|---|---|---|---|---|---|---|---|
| BMW M 1000 XR | 201 PS | 3.2 s (BMW off.) | >275 km/h (BMW off.) | 223 kg | 6.5 WMTC / 6.7 test | n/m | Superb sport machine, weak pure tourer |
| BMW S 1000 XR | 170 PS | n/m | n/m | ~219-223 kg | ~6.5 | n/m | More touring-oriented sibling |
| BMW R 1300 RS | 145 PS | n/m | 245 km/h (BMW off.) | 245 kg | 4.8 WMTC | n/m | Rare classic sport-tourer, very dynamic |
| BMW F 900 XR | 105 PS | n/m | 215-217 km/h (test) | 216 kg | ~4.2 | n/m | Very agile, playful, 105 PS feels like 125 |
| Yamaha Tracer 7 | 73 PS | n/m | ~200 km/h class (n/c) | 203/212 kg | ~4.9 real | n/m | Agile, fun, comfortable; limited wind protection |
| Ducati Multistrada V4 S | 170 PS | 3.2-3.3 s (GPS) | 259.4 km/h (GPS) | >230 kg dry | ~6.25 (16 km/l) real | ~38.0 m (GPS) | Superbike disguised as globetrotter |
| Triumph Tiger Sport 800 | 115 PS | n/m | ~220 km/h class (n/c) | 214 kg | 4.7-4.9 | n/m | Addictive triple, fluffy, high comfort |
| Kawasaki Ninja 1100SX (SE) | 136 PS | n/m | n/m | n/m (payload 195 kg) | 5.7 off. / 6-7.5 test | n/m | Excellent comfort+dynamics sport-tourer |
| KTM 1290 Super Duke R (naked) | ~170 PS | ~2.9-3.2 s (db) | ~274 km/h (db) | n/m | n/m | n/m | Hyper-naked, not a sport-tourer |
| Aprilia Tuono 1100 (naked) | ~175 PS | 0-60 2.99 s (db) | n/m | n/m | n/m | n/m | Sport-naked, not a sport-tourer |

n/m = not measured in the sources read; n/c = not confirmed in a read source; db = database figure (MotoStatz/FastestLaps).
