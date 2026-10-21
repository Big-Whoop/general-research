# RESEARCH-sporttourer-2027-fresh — corpus manifest

**Topic:** Top sport-touring motorcycles for MY2027 (on sale in Switzerland in 2026/2027).
**Research date:** 2026-10-21 · **Market:** Switzerland (CHF, incl. 8.1% VAT) · **Method:** gated multi-round subagent fan-out (round 1: 5 lanes in dispatch batches 3+2).
**Tier scheme (all lanes):** **V** = Verified (authoritative source for this exact target, read whole) · **P** = Plausible (sound general behavior / community-reported, not on-target confirmed) · **S** = Speculative (inferred / unconfirmed).
**Language rule:** lane files, briefs, README in English (AI-facing); REPORT.md in the language the research is produced in.

## Run history (interruptions)

- **2026-10-17:** a prior complete corpus exists at `../sporttourer-2027/` (10 lanes, ~230 findings). Per user decision 2026-10-21 it is IGNORED as evidence (kept for reference only).
- **Fresh run attempt 1 (2026-10-21 ~04:17–05:15):** 5 lanes dispatched; the owner session crashed ~04:56 killing all subagents. Lane 4 (owners) had landed 8/13 bikes on disk. Re-dispatch at ~05:09 was stopped by user abort ("Die Suche funktioniert nicht"); user then ordered deletion ("löschen") of the partial corpus. Deleted ~05:14.
- **Fresh run attempt 2 (this corpus, from ~05:20):** search backend confirmed fixed by user + verified by probe search. Crash mitigations in all lane briefs: (1) incremental file writes (create skeleton first, append per bike, save after each) so an interruption never loses work, (2) reuse of the web cache at /opt/data/cache/web/ (pages fetched 04:17–05:15 today are still on disk and fresh; /opt/data/cache/web/extract-index.json maps hash to url/file/title/fetched_at), (3) spaced queries + timebox, (4) graceful degradation: repeated fetch errors are logged under "searched, found nothing" and the lane continues with cache/other sources instead of retry loops.

## Premise

- Subject: "top sport-tourer motorcycles, MY2027, Switzerland" — **verified as a live, moving category** (probe searches 2026-10-21).
- BMW M 1000 RS: EPA/CARB-certified for MY2027 as a new M-line sport-tourer, not yet officially announced (motorcycle.com, rideapart, bikewale, i-motorbike).
- KTM 1390 Super Duke GT: **confirmed for 2027** (MCN news 2025-09: production push; 188 hp 1350cc LC8 V-twin, new-gen semi-active suspension, radar cruise per jimaimracing/motoplanete 2027 listings) — replaces the 1290 Super Duke GT.
- Dichotomy named up front: **true sport-tourers** (dedicated fairing, touring comfort, ~900cc+) vs. adjacent categories (naked, supersport, adventure, GT-crossover) — lanes must label each candidate.
- Timing note: EICMA 2026 is late November 2026 (not yet held) — MY2027 re-pricing and some new models may legitimately be unpublished in CH; that is a finding, not a gap.

## Step 0 — Source universe checklist

| Source type | Plan | Status after round 1 |
|---|---|---|
| Official: manufacturer spec/press pages (BMW, Ducati, Kawasaki, Honda, Yamaha, KTM, Triumph, Suzuki, MV Agusta) | lane 1 | covered (9/13 core bikes V-tier; Yamaha/Ducati/MV-Agusta spec gaps → round 2 lane 6) |
| Semi-official: EPA/CARB filings, CH importer pages (bmw-motorrad.ch, ducati.ch, kawasaki.ch, honda.ch, yamaha.ch, ktmbikes.ch, triumph.ch, suzki.ch) | lanes 1+2 | covered (M 1000 RS EPA/CARB via 4 media reading the same primary docs; CH importer pages read per brand; ktmbikes.ch down — V absence) |
| Swiss price lists: mybikes.ch, CH dealer/importer price pages, bike24/motorrad.ch | lane 2 | covered (27 price findings; mybikes.ch = DEAD domain at GoDaddy auction — documented absence) |
| Pro tests: 1000PS.ch/.de, Motorrad.com, MC (Motor-Cycle), ADAC, MCN, visordown, motorcycle.com, Motorcyclist | lane 3 | covered (round 2 lane 7 adds second sources + measured data for single-source bikes) |
| Community: Reddit (r/SportBikes, r/motorcycles, brand subs), forums (bmw-motorrad-forum.de, motor-talk.de, motocommunity, toeff-forum.ch, honda-crosstourer.de) | lane 4 | covered (181 V / 61 P / 15 S findings; motor-talk.de, honda-crosstourer.de, r/bmwmotorrad, r/multistrada, r/Kawasaki, revtothelimit, gsxs1000.org, fjrowners) |
| Recalls/defects: NHTSA, EU Safety Gate, manufacturer recall/TSB pages, BASMA (CH), forum complaint threads | lane 5 | covered (NHTSA relay via ridertoolkit full per-make lists + EU Safety Gate 2023–2026 feed + KTM global recall page; BASMA has no central public list — documented) |
| Practice: vlogs/long-term video tests (secondary, corroboration only) | lanes 3+4 | covered (roaddirt.tv Tracer 9 GT 2-month long-term + owner comments; dancingthepolka.com GSX-S1000GX+ 2-month long-term) |
| Code/issue trackers | skipped (not a software system) | n/a |

## Step 1 — Sub-questions (coverage table)

| # | Sub-question | Owning lane(s) |
|---|---|---|
| Q1 | Candidate set: which MY2027 bikes are the top TRUE sport-tourers on sale in CH 2026/27 (and which are adjacent-category)? | lane 1 (+ refinements from all lanes) |
| Q2 | Performance data per candidate: power, torque, weight, 0–100, top speed, electronics, brakes | lane 1 (official) + lane 3 (measured) |
| Q3 | MY2026→MY2027 model-year changes + new MY2027 models (incl. end-of-line) | lane 1 |
| Q4 | Pro test reports: independent reviews, comparison tests, verdicts | lane 3 |
| Q5 | CH prices: CHF incl. VAT per equipment level; MY2027 re-pricing status per bike | lane 2 |
| Q6 | Owner/user experiences: long-ride comfort, running costs, recurring complaints, DACH/CH-specific reports | lane 4 |
| Q7 | Known defects: recalls, TSBs, platform-level reliability concerns, brand survey context | lane 5 |
| Q8 | Cross-cutting Swiss purchase context: importers, availability/lead times, homologation, financing quirks | lane 2 |

## Round 1 dispatch (attempt 2, 2026-10-21 ~05:20)

| Lane | Axis dir | Brief focus |
|---|---|---|
| lane 1 | `specs/` | Candidate set + official MY2027 specs + MY changes (official sources first) |
| lane 2 | `prices/` | CH prices (CHF incl. VAT) + cross-cutting CH purchase context |
| lane 3 | `tests/` | Pro tests + measured results + comparison tests |
| lane 4 | `owners/` | Owner experiences (Reddit, DACH forums, long-term reports) |
| lane 5 | `reliability/` | Defects, recalls, TSBs, reliability |

## Discrepancy log

- **KTM 1390 Super Duke GT "new MY2027 188 hp" (seed) vs "MY2025 190 PS" (KTM press):** RESOLVED — same bike, same engine. 190 PS (KTM CH press, V) = 140 kW = 187.7 hp ≈ "188 hp" (jimaimracing 2027 listing). The 1390 GT is the **MY2025 design delayed to 2027 market arrival by KTM insolvency** (MCN 2025-09, V; probe search: motoplanete, jimaimracing, MCN). It is "new to market MY2027", NOT a new MY2027 design. Lane 3's flag is answered; no round-2 action needed on the engine. Remaining: no CH price (ktmbikes.ch down — V absence), no pro test (never reached market yet — V absence), weight ~228 kg (P, secondary only).

## Round 1 assessment (complete — all 5 lanes read whole)

| sub-question | best tier reached | independent sources for load-bearing claim | workaround space searched | lane verdicts (answered/partial/not found) | status |
|---|---|---|---|---|---|
| Q1 candidate set | V | 9 brand CH importer ranges checked (BMW, Honda, Suzuki, Triumph, Yamaha API, Ducati, Kawasaki, KTM, MV Agusta) | n/a (not a feature question) | lane1: partial | **CLOSED** (exclusions = "not found in CH sources checked", flagged) |
| Q2 performance data | V for 9/13 core bikes (official CH/manufacturer); P for Yamaha Tracer 9/7, Ducati V4 (official CH 404/not cached); MV Agusta headline-only (subpages 404) | per-bike official page (lane1) + CH price page (lane2) | n/a | lane1: partial, lane3: partial | **OPEN** → round-2 lane 6: official specs via browser/product-API |
| Q3 MY changes | V (BMW press 2026-07-02 primary; KTM 2027 arrival MCN V; 1100SX MY2027 kawasaki.eu V; carryovers = official absences) | M 1000 RS existence: ≥4 independent media reading the same EPA/CARB primary docs (motorcycle.com, rideapart, bikewale, motorcycles.news) | n/a | lane1: partial | **CLOSED** (M 1000 RS CH availability + EICMA-dependent deltas = legitimate unpublished findings, not gaps) |
| Q4 pro tests | V for R 1300 RS (1000PS 2026-03 + MCN), CB 1000 GT (1000PS CH 2026-08, V); P for most others — **single-source** for S 1000 XR, M 1000 XR, GSX-S1000GX, Ninja 1100SX, Tracer 9, Tiger 800, F 900 XR, Multistrada (1000PS+visordown=2 for V4 S); no measured 0–100/100–0/fuel-consumption in any lane-3 test | 1–2 per bike | n/a | lane3: partial | **OPEN** → round-2 lane 7: second independent test source per single-source bike + measured data where published |
| Q5 CH prices | V (verbatim price strings; MY-label check complete) | per-brand official CH page (lane2, 27 findings) | mybikes.ch = DEAD domain (GoDaddy auction) — documented | lane2: partial | **CLOSED** (9/10 bikes without MY2027 price = importer/EICMA timing finding; BMW already re-priced: R 1300 RS ab 16'700–16'800) |
| Q6 owner experiences | V (first-hand owner reports read whole: F 900 XR 100'000 km, Swiss Tracer 9 GT 12'000 km, Multistrada V4S 15'000 mi, KTM 1290 GT 7 y) | ≥2 per bike (reddit + forum-DACH + long-term vlog reports; 181 V findings total) | yes (seat upgrades Sargent/Wunderlich, screens MRA/Ermax, MCC cruise retrofit, exhaust/tuning) | lane4: partial (no owners exist yet for M 1000 RS / KTM 1390 GT / CB 1000 GT — documented absences, bikes not on the road; thin: M 1000 XR long-term, Tiger Sport 800 multi-month, R 1300 RS real-world consumption) | **CLOSED** (thin spots carried as caveats in REPORT.md) |
| Q7 defects/recalls | V (official campaign numbers, all 13 candidates; NHTSA relay + EU Safety Gate 2023–2026 feed + KTM global page) | ≥2 per candidate (NHTSA + EU Safety Gate; KTM global page for KTM) | n/a (not a feature question) | lane5: partial (TSB portals dealer-only, no current 2025/26 brand reliability survey exists, no central BASMA list — all documented unreachable) | **CLOSED** (documented absences are findings, not gaps) |
| Q8 CH purchase context | V (importer map, VAT verbatim BMW+Suzuki, financing/leasing, availability signals) | official CH pages (lane2) | ktmbikes.ch down (V) | lane2: partial | **CLOSED** |

## Round 2 dispatch (2026-10-21, autonomous per round gate — 2 OPEN rows → 2 lanes)

| OPEN row | Lane | Expected evidence + where |
|---|---|---|
| Q2 performance data — Yamaha Tracer 9 / 9 GT / 7, Ducati Multistrada V4, MV Agusta TV800 official specs at P-tier (official CH pages 404 / not cached); KTM 1390 GT weight only P (~228 kg secondary); BMW M 1000 RS CH presence unconfirmed | lane 6 → `specs/lane6-r2.md` | Manufacturer official spec pages via browser: yamaha.eu / yamaha-motor.com (yamaha.ch 404'd in r1), ducati.com/ch (browser-readable in r1), mvagusta.com (subpages 404'd in r1 — retry). Secondary: KTM 1390 GT weight (ktm.com global spec), KTM 1390 GT CH price (ktmbikes.ch down — CH dealer alternates via search), bmw-motorrad.ch M 1000 RS range listing check |
| Q4 pro tests — 8 bikes single-source (S 1000 XR, M 1000 XR, GSX-S1000GT/GX, Ninja 1100SX, Tracer 9/GT, Tiger Sport 800, F 900 XR, Multistrada V4); no measured 0–100 km/h / 100–0 m / fuel consumption found in lane 3 | lane 7 → `tests/lane7-r2.md` | Second independent test per bike from a DIFFERENT publisher than lane 3 used (ADAC, motorradonline.de, 1000PS.de archive, MC, motorcycle.com, visordown, mcn.co.uk); ADAC-style measured data (0–100, 100–0, consumption) where published |

## Round 2 assessment (complete — both lanes read whole)

| sub-question (residual) | best tier reached | independent sources for load-bearing claim | workaround space searched | lane verdicts | status |
|---|---|---|---|---|---|
| Q2 performance data (residual) | V for ALL 13 candidates, except KTM 1390 GT weight = P (~228 kg secondary; NO official figure exists — verified absence across ktm.com CH/US/SG model trees, /en-ch spec 404, MY25 press kit PDF, press.ktm.com release, CH press page). Yamaha Tracer 9/9 GT/9 GT+/7/7 GT now official CH (yamaha-motor.eu/ch API + PDPs — round-1 404 was the wrong domain yamaha.ch); Ducati V4/V4 S official CH spec tables (170 PS/125 kW, 124 Nm @9'000, 229/231 kg fahrfertig ohne Kraftstoff — official Nm/rpm supersedes round-1 secondary "125 Nm @8'750"); MV TV800 R + Lusso SCS official CH spec sheets (81 kW/110 hp, 84 Nm, 213 kg / 226 kg in running order w/o fuel, 21.5 L). M 1000 RS: NOT in bmw-motorrad.ch range (verified absence, V — a finding) | official CH spec source per bike (Yamaha hyperdrive API + PDP cross-check, ducati.com/ch, mvagusta.com/ch) + round-1 secondary cross-checks | n/a (not a feature question) | lane6: answered | **OPEN** (single P cell: KTM 1390 GT weight — no source can plausibly contain an official figure; absence verified 2026-10-21 → round-3 gate, reported as such, not silently closed) |
| Q4 pro tests (residual) | V — second independent publisher found for ALL 8 single-source bikes (WELT/SP-X, MCN, ADAC, Visordown, motorradonline.de — every one a different publisher than lane 3's 1000PS); measured data now: 0–100 km/h for S 1000 XR (3.2 s, WELT, P) + M 1000 XR (3.2 s, aggregator S); consumption for S 1000 XR (6.0/6.2), F 900 XR (4.2, real ~5), M 1000 XR (6.5), GX (~5.2 official), Tiger Sport 800 (5.2), Multistrada V4/V4 S (6.6) + V4 Rally MY2026 (5–6); top speed S 1000 XR 250 / F 900 XR 201; measured power = spec in all cases | ≥2 different publishers per bike (round 1 + round 2) | n/a | lane7: partial | **CLOSED** (100–0 m braking: NOT published for any bike in ADAC/WELT/MCN/visordown/motorradonline — genuine gap, documented, carried to REPORT.md known gaps) |

## Round 3 gate (pending user decision 2026-10-21)

- OPEN row (verbatim): Q2 — "KTM 1390 GT weight = P (~228 kg secondary; NO official figure exists — verified absence)".
- Expected gain + source for a round-3 lane: ≈ 0. No source plausibly exists that contains an official KTM 1390 GT weight figure — all official channels (ktm.com CH/US/SG, press kit, press release) were verified absent on 2026-10-21; a lane could only re-confirm the absence. The 100–0 m braking gap is in the same boat (no publisher publishes it for these models).
- Lane list for a hypothetical round 3: 1 lane (KTM 1390 GT weight re-confirmation via any not-yet-tried official channel, e.g. KTM dealer config tools).
- Recommendation: **synthesize now**, list both items as known gaps in REPORT.md.
