# RESEARCH-sporttourer-2027 — corpus manifest

**Topic:** Top sport-touring motorcycles for MY2027 (on sale in Switzerland in 2026/2027).
**Research date:** 2026-10-17 · **Market:** Switzerland (CHF, incl. 8.1% VAT) · **Method:** 2-wave fan-out (5 wave-1 single-axis lanes + 5 wave-2 gap-fill lanes).
**Tier scheme (all lanes):** **V** = Verified (authoritative source for this exact target, read whole) · **P** = Plausible (sound general behavior / community-reported, not on-target confirmed) · **S** = Speculative (inferred / unconfirmed).
**Status:** all files **CURRENT** (researched 2026-10-17).

## Corpus files

| File | Axis / sub-question | One-line claim summary | Tier scheme | Status |
|---|---|---|---|---|
| `REPORT.md` | Synthesis (all 6 axes) | Best result first (BMW R 1300 RS = benchmark; GSX-S1000GT = value+reliability), full options matrix over 13 core sport-tourers, ranked recommendation, explicit untested list. | V/P/S | CURRENT |
| `specs/lane1.md` | Axis 1 — performance/specs + candidate set + MY2027 changes | Refined candidate set (drops discontinued, adds M 1000 RS / CB 1000 GT / Ninja 1100SX / Tracer 9); official power/torque/weight/electronics per bike; MY2026→MY2027 change table. | V/P/S | CURRENT |
| `prices/lane2.md` | Axis 3 — CH prices (CHF incl. 8.1% VAT) + importer availability | Official CH list price per candidate (all VAT-inclusive); candidate-set refinements (Ninja 1100SX replaces 1000SX, R 1300 RS replaces R 1250 RS); MY2027 re-pricing gaps. | V/P/S | CURRENT |
| `tests/lane3.md` | Axis 2 — pro tests + measured results | Pro verdicts + measured data (0-100, top speed, consumption, weight, braking) per core bike; 3 comparison tests flagged as teasers (read in full in wave2/lane25). | V/P/S | CURRENT |
| `owners/lane4.md` | Axis 4 — owner experiences + long-term reports | Per-bike owner sentiment, long-ride comfort, running costs, recurring complaints; Swiss/DACH-specific reports (toeff-forum.ch S 1000 XR, motor-talk.de R 1300 RS). | V/P/S | CURRENT |
| `reliability/lane5.md` | Axis 5 — defects, recalls, TSBs, reliability | Per-bike recall/TSB history (NHTSA campaign numbers) + platform-level concerns; brand-level survey context; MY2026→MY2027 reliability-relevant changes. | V/P/S | CURRENT |
| `wave2/lane21.md` | Gap: BMW M 1000 RS (specs) | M 1000 RS is EPA/CARB-certified for 2027 (sport-touring M 1000 RR, ~205 hp US / ~218 PS EU expected, EIM 280 kg) but **not yet officially announced** — no CH price/spec/tests/owners. | V/P/S | CURRENT |
| `wave2/lane22.md` | Gap: Honda CB 1000 GT + Yamaha Tracer 9 (full deep-dive) | CB 1000 GT (CHF 13'690, 149.7 PS) carries the **Hornet oil-consumption platform recall** (GT fix unconfirmed); Tracer 9 (CHF 12'490–18'990, 119 PS CP3) has a **recurring electronic TPS/ECU recall** history. | V/P/S | CURRENT |
| `wave2/lane23.md` | Gap: KTM 1290 Super Duke GT (the actual sport-tourer) | The 1290 Super Duke GT (CHF 22'790, action 18'790) is KTM's true sport-tourer and is **end-of-line** — replaced by the all-new 1390 Super Duke GT for MY2027; GT is NOT in the wiring-harness recall scope. | V/P/S | CURRENT |
| `wave2/lane24.md` | Gap: Suzuki GSX-S1000GT (tests/owners/reliability) | GSX-S1000GT (CHF 16'495, 152 PS): MCN 5/5 "a hell of a sports tourer for the money," 4.2/5 owner reliability, **no MY2022–27 recalls** (only 2016 caliper); confirmed for MY2027. | V/P/S | CURRENT |
| `wave2/lane25.md` | Gap: head-to-head comparison tests + MY2027 re-pricing | The 3 1000PS DE comparison tests are 2025 tests of MY2024/25 bikes (only the Tiger Sport 800 is a core-set bike directly tested); **only BMW has published a distinct MY2027 CH price** (R 1300 RS ab 16'700). | V/P/S | CURRENT |

## Reading order

1. `REPORT.md` — the synthesis (start here).
2. `wave2/lane25.md` — the re-pricing + comparison-test findings that shape the recommendation.
3. The wave-1 axis lanes (`specs` → `prices` → `tests` → `owners` → `reliability`) for the per-bike detail.
4. The wave-2 gap lanes (`lane21`–`lane24`) for the deep-dives on the new/missing bikes.

## Known gaps / open items (carried into REPORT.md §9)

- BMW M 1000 RS: unannounced — re-probe after the EICMA reveal.
- MY2027 re-pricing: unpublished for 9 of 10 core-set bikes — re-probe after importers advance their model-year labels (expected Q4 2026 / Q1 2027).
- S 1000 XR MY2027 facelift: homologation-based (Plausible), not an official BMW presentation.
- CB 1000 GT oil-consumption fix + Tracer 9 MY2025 CH ECU/TPS fix: not independently confirmed.
- No single head-to-head comparison test covers the full MY2027 core set; no Swiss-specific (SECO/BAFU) recall database query was possible.
