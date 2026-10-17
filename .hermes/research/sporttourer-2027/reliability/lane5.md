# Lane 5 — Defects, Recalls, TSBs, Reliability (MY2027 Sport-Tourers, CH market)

Lane: RESEARCH-sporttourer-2027 [LANE-5]
Research date: 2026-10-17
Target market: Switzerland (MY2027 = bikes on sale late 2026 / 2027)
Tier scheme: **Verified** (authoritative/official source read) / **Plausible** (sound general behavior or community-reported, not on-target confirmed) / **Speculative** (mechanism asserted, untested).
Tag per finding: [OFFICIAL RECALL] / [OFFICIAL TSB / SERVICE ACTION] / [COMMUNITY] / [PRO TEST] / [SURVEY].

---

## 0. Candidate-set notes (scope corrections, do-not-invent)

- **Genuine sport-tourers in the set:** BMW S 1000 XR / M 1000 XR, BMW R 1300 RS / R 1250 RS, BMW F 900 XR, Kawasaki Ninja 1100SX (MY2027) / Ninja 1000 (predecessor), Yamaha Tracer 7, Ducati Multistrada V4.
- **Naked / sport bikes in the set (kept for completeness, NOT true sport-tourers):** Suzuki GSX-S1000 (naked) / Hayabusa (hyper-sport), Honda CBR1100XX (hyper-sport) / CBR650R (middleweight sport), Triumph Speed Triple 1200 RS (naked) / Tiger Sport 800 (naked), Aprilia Tuono V4 (naked), KTM 1290 Super Duke R (naked). These are covered below but flagged; the user's core question is sport-touring, so weight conclusions accordingly.
- **Kawasaki MY2027 correction (important):** the MY2027 Kawasaki sport-tourer is the **Ninja 1100SX**, the successor to the Ninja 1000 / Z1000SX. The 1043 cc engine ran 2011–2024; the 1100 naming marks the updated machine. The ZZR1400 / ZX-14 is correctly excluded (ended 2022). See Kawasaki section.
- **MY2027 caveat:** for most models MY2027-specific recall/TSB data does not yet exist (MY2027 not fully on sale / not yet announced). Findings below are the model's documented recall/defect history + platform-level issues that carry into MY2027. Anything not yet confirmed for MY2027 is marked accordingly.

---

## 1. BMW S 1000 XR / M 1000 XR

**F1. [OFFICIAL RECALL] M 1000 XR / M 1000 R steering-damper recall (2024–2025), NHTSA 25V194000.**
- Claim: A defective steering damper with a loose valve pin can cause an unexpected increase in steering effort → loss-of-control / crash risk; 51 units, damper replaced free.
- Source: https://www.rideapart.com/news/755684/bmw-recall-m1000xr-m1000r-steering-damper/ (trade press, NHTSA-sourced)
- Quote: "Some of these models might have a defective steering damper that has a loose valve pin within the housing, which can cause an unexpected increase in steering effort... The safety recall was issued on March 27, 2025, and the NHTSA campaign number is 25V194000."
- Tier: **Verified**. Relevance to MY2027: 2024–2025 units; confirm the MY2027 facelift M 1000 XR is outside the affected build window.

**F2. [OFFICIAL RECALL] S 1000 XR / S 1000 R software recall (2020–2023), NHTSA 23V-051.**
- Claim: A dealer software update could reset the Dynamic Pro wheelie-control (front wheel lift-off assistant) to factory setting with no rider indication → unexpected handling / crash risk; 754 units (484 S 1000 XR).
- Source: https://www.rideapart.com/news/651969/bmw-s-1000-xr-r-recall/ (trade press, NHTSA-sourced)
- Quote: "A software update performed on these bikes may have reset the front wheel lift-off assist (or 'wheelie control') setting without offering any indication of the change in the instrument cluster... NHTSA's campaign number for this recall is 23V-051."
- Tier: **Verified**. Pre-MY2027 (2020–2023); relevant to used-market purchases.

**F3. [OFFICIAL RECALL — EXCLUSION] S 1000 RR ignition-lock recall does NOT affect the XR.**
- Claim: The 2020–2026 S 1000 RR ignition-lock-failure recall explicitly does not extend to S 1000 XR / M 1000 XR.
- Source: https://www.motorcycle.com/bikes/news/2020-2026-bmw-s-1000-rr-recalled-for-ignition-lock-failure-44668897 (trade press)
- Quote: "There have been no reports of crashes or injuries related to the ignition lock issue, and there has been no evidence of it occurring with M 1000 RR, S 1000 R, S 1000 XR, or M 1000 XR models."
- Tier: **Verified** (negative finding — prevents a false-positive).

**F4. [COMMUNITY / WARRANTY] M 1000 RR warranty dispute — $15,000 engine replacement denied.**
- Claim: An M 1000 RR owner had a $15,000 engine replacement refused under warranty after an aftermarket exhaust + 250 rpm over-rev + premature removal of the 600-mile break-in limiter; split opinions on fault.
- Source: https://www.rideapart.com/news/714745/motomillion-bmw-m1000rr-engine-failure/ (referenced in rideapart M 1000 XR recall article)
- Quote: "the Bavarian brand's flagship model, the M 1000 RR was the subject of a video where it suffered a 'massive engine failure' and BMW refused to cover the $15,000 engine replacement bill under warranty."
- Tier: **Plausible** (single documented case, M 1000 RR not XR; signals warranty-enforcement friction on the M platform).

**F5. [OFFICIAL RECALL] 2020 S 1000 XR: two recalls — service brakes + electrical system.**
- Claim: The 2020 S 1000 XR is associated with two recalls affecting service brakes and the electrical system, with failures tending to manifest early.
- Source: https://www.safecarinfo.com/cars/bmw/s-1000-xr/2020 (recall aggregator)
- Quote: "The 2020 BMW S 1000 XR showcases reliability concerns due to two recalls affecting critical systems, including service brakes and the electrical system."
- Tier: **Plausible** (aggregator; underlying NHTSA campaigns not individually re-verified this run — see Gaps).

---

## 2. BMW R 1300 RS / R 1250 RS (Boxer)

**F6. [OFFICIAL RECALL — PLATFORM] R 1300 boxer starter-relay recall (worldwide), NHTSA 24V-557.**
- Claim: The R 1300 platform's semiconductor starter-relay housing had an insufficient injection-molding process → moisture ingress → contact corrosion → current leakage → heating/scorching → fire risk; ~25,000 units worldwide (1,582 US), built 14 Jul 2023 – 18 Mar 2024. Recurring: Nov 2023 service action → Feb 2024 recall → 18 Jul 2024 new recall. Remedy: replace relay (semiconductor → electromagnetic) + software update.
- Source: https://www.advpulse.com/adv-news/bmw-r1300gs-recall-starter-relay/ (trade press, NHTSA-sourced)
- Quote: "the starter relay is enclosed in a housing which was produced with an insufficient injection molding process... In rare cases, this could increase the risk of a thermal event or a fire... refer to the NHTSA recall #24V-557."
- Tier: **Verified** (recall is officially for the R 1300 **GS**). **On-target caveat:** the R 1300 RS shares the R 1300 boxer platform/engine; the starter relay is a platform component, so this is a platform-level concern for the RS even though the published recall names the GS. Treat as **Plausible-for-RS / Verified-for-platform**.

**F7. [COMMUNITY — PLATFORM] R 1300 platform clutch failures.**
- Claim: Multiple R 1300-platform owners report clutch failures, incl. one 2025 GSA 1300 clutch that "disintegrated after 6000 miles in 4 months" (BMW contributed $1,250 good-faith; owner still out >$3,000 + parts wait), and one clutch failure that caused an accident (bike kept moving with clutch fully depressed).
- Source: https://www.r1300gsforum.com/threads/gs1300-clutch-failure.101/ and https://www.r1300gsforum.com/threads/problems-with-my-new-r-1300gs.11/ (owner forums)
- Quote: "My 2025 GSA 1300 clutch disintegrated after 6000 miles in 4 months. BMW chipped in $1250 in good faith but I'm still out over $3000 and a months wait for parts because the clutch basket needed replacing too." / "I had a clutch failure which caused a small accident, with fully depressed clutch the bike was still going forward."
- Tier: **Plausible** (community, platform-level; the R 1300 RS uses the same boxer + clutch architecture — early-model concern to watch).

**F8. [PRO TEST] R 1300 RS: clunky gearbox in the lower gears (mitigated by ASA option).**
- Claim: The new R 1300 gearbox/quick-shifter is "a blunt instrument" in the first three gears; the ASA (Automatic Shift Assist) clutchless option largely resolves it.
- Source: https://www.mcnews.com.au/bmw-r-1300-r-r-1300-rs-r-1300-rt-ridden-rated/ and https://www.mcnews.com.au/bmw-r-1300-rs-review-sports-tourers-are-back/ (pro reviews)
- Quote: "Shifting between the first three cogs via BMW's quick-shifter (BMW shift assist) isn't exceptionally smooth. Far from it, I found it to be quite a blunt instrument." / "the ASA (Automatic) gearbox option, which pretty much resolves my criticisms of what can be a rather clunky gearshift in the 1300s' lower gears."
- Tier: **Plausible** (pro-reported drivability trait, not a safety defect).

**F9. [COMMUNITY — SPECULATIVE] R 1300 GS electronically-controlled damping / rebound-control complaints.**
- Claim: A forum commenter alleges the new R 1300 GS suffers electronically-controlled rebound/damping-circuit faults (sensors) causing sudden instability/rear slide, "with or without the VAHC option."
- Source: https://www.advpulse.com/adv-news/bmw-r1300gs-recall-starter-relay/ (comment section, Nov 2024)
- Quote: "They will soon recall those new R1300GS because of suspension failures... this bike suffer from dampening circuit control (sensors issues or other element related to the electronically controlled rebound)... the rear slides on slight angle and bounce like pogo sticks."
- Tier: **Speculative** (single unverified forum comment; no official recall/TSB found for it this run).

---

## 3. BMW F 900 XR (parallel-twin)

**F10. [COMMUNITY] F 900 XR shaft final drive: driveline lurch/clunk.**
- Claim: The shaft final drive needs periodic gear-oil changes + seal checks; the recognizable warning sign is a driveline lurch or clunk when transitioning between acceleration and engine braking.
- Source: https://www.motosport.com/blog/2024-bmw-f-900-xr-common-warning-signs-your-motorcycle-needs-service (dealer/service blog)
- Quote: "The most recognizable warning sign is a driveline lurch or clunk when transitioning between acceleration and engine braking."
- Tier: **Plausible**.

**F11. [COMMUNITY] F 900 XR: clunky gearbox, rust/tarnished fasteners, finish quality.**
- Claim: An owner (ex-Suzuki SV1000) reports the F 900 XR gearbox is "horrible & clunky," with rust/tarnished fasteners and a finish below expectation.
- Source: https://www.f900xr.com/index.php?topic=958.0 (owner forum)
- Quote: "finish isn't great (rust and tarnished fasteners) Gearbox is horrible & clunky after the suzuki's smooth as silk box."
- Tier: **Plausible** (single owner, subjective).

**F12. [COMMUNITY] F 900 XR (2025): clutch-cable break at 17,000 km, neutral-shift trouble, oil use.**
- Claim: A 2025 F 900 XR at 22,000 km (since Nov 2024) had a clutch cable break at 17,000 km (owner-paid), ongoing trouble shifting into neutral, and slightly elevated oil consumption.
- Source: https://www.motoplanete.us/bmw/10954/F-900-XR-2025/contact.html (user review)
- Quote: "the clutch cable broke at 17,000 km—at my expense, of course. I still have a little trouble shifting into neutral, and it tends to use a bit of oil!"
- Tier: **Plausible** (single owner).

**F13. [OFFICIAL RECALL — VERIFY SCOPE] 2020 F 900 XR listed under brake-light recall 20V146000.**
- Claim: A 2020 F 900 XR appears under NHTSA campaign 20V146000 (exterior lighting / brake lights — brake light may flash instead of remain steady during emergency braking); the campaign text also names 2019–2020 S 1000 R and R nineT models.
- Source: https://auto-recalls.justia.com/bmw/f-900-xr/2020/20v146000/ (recall aggregator)
- Quote: "2019-2020 S1000R motorcycles. The brake light may flash instead of remain steady during emergency braking."
- Tier: **Plausible** (aggregator; exact model scope of 20V146000 not re-verified against the NHTSA PDF this run — see Gaps).

**F14. [COMMUNITY — LIKELY INACCURATE] F 900 XR engine "made by Loncin" claim.**
- Claim: A forum post (citing "the web AI") asserts the F 900 XR engine is manufactured by Loncin (China) based on the F 850 GS engine, with bikes assembled in Berlin.
- Source: https://www.bayarearidersforum.com/forums/threads/bmw-f900-xr-reliability.566041/ (owner forum)
- Quote: "That's what the web AI says, 'The engine for the BMW F900 XR is manufactured by Loncin, a Chinese company, and is based on the engine used in the F850GS.'"
- Tier: **Speculative / likely inaccurate** (the F 900 parallel-twin is a BMW-designed engine; the Loncin attribution is an unverified AI-generated claim — do not carry into the report as fact).

---

## 4. Kawasaki — MY2027 Ninja 1100SX (successor to Ninja 1000 / Z1000SX)

**F15. [OFFICIAL / MY2027 CHANGE] MY2027 Kawasaki sport-tourer is the Ninja 1100SX (new for Europe).**
- Claim: Kawasaki announced the return of the Ninja 1100SX for the 2027 model year (for now Europe-only); the 2026 Ninja 1100SX SE adds an Öhlins S46 rear shock + Brembo front brake package. The 1043 cc engine ran 2011–2024; the 1100 marks the updated machine.
- Source: https://www.autoevolution.com/news/2027-kawasaki-ninja-1100sx-brings-back-the-bad-boy-looks-to-the-sports-touring-segment-274707.html ; https://www.kawasaki.com/en-us/motorcycle/ninja/sport/ninja-1100sx/2026-ninja-1100sx-se-abs ; https://motofomo.com/kawasaki-ninja-1000-sx-buyers-guide/
- Quote: "Kawasaki announced the return of the Ninja 1100SX for the 2027 model year, for now only in Europe." / "The 2026 Ninja 1100SX SE ABS features an Öhlins S46 rear shock and Brembo front brake package." / "From the first model released in 2011 until 2024, the Ninja 1000 had the same engine: a 1043cc inline four-cylinder."
- Tier: **Verified** (MY2027 model identity + change). Reliability of the new 1100SX: too new for a track record — see F16 for the predecessor's history.

**F16. [COMMUNITY — PREDECESSOR] Ninja 1000 / Z1000SX recurring issues: electrical, gasket oil leak, sticky clutch, stalling.**
- Claim: Documented recurring issues on the Ninja 1000 (predecessor): intermittent electrical problems (no-start, battery drain), oil/water-pump gasket oil leaks (esp. 2016), sticky clutch (2011–2013), and intermittent stalling.
- Source: https://motorandwheels.com/problems-kawasaki-ninja-650-1000/ (problems roundup, NHTSA/forums-sourced)
- Quote: "Some of these include: 1. Bike refuses to start... 2. Bike battery doesn't hold charge." / "Oil leaks... most common with the 2016 model year bikes and is likely caused by a faulty oil/water pump seal." / "you may experience what's called a 'sticky clutch'."
- Tier: **Plausible** (predecessor model; MY2027 1100SX may or may not carry these over — unconfirmed).

**F17. [OFFICIAL RECALL — OLD] Z1000 front brake-hose recall (2010).**
- Claim: A 2010 factory recall replaced the front brake hose after it could curl toward the brake disc under extreme front-suspension compression; fixed with a grommet.
- Source: https://www.visordown.com/reviews/used-bike/buyers-guide-kawasaki-z1000 (buyer's guide)
- Quote: "Kawasaki issued a factory recall in 2010 to replace the front brake hose, following a potential issue where under extreme front suspension compression, the front brake line may curl towards the brake disc and make contact with it."
- Tier: **Verified** (old, pre-MY2027; used-market relevance only).

**F18. [COMMUNITY — POSITIVE] Ninja 1000 high-mileage durability report.**
- Claim: A Ninja 1000SX owner reportedly reached 120,000 miles without ever checking valve clearance — a positive durability signal for the inline-four.
- Source: https://www.reddit.com/r/Kawasaki/comments/1dosw29/z1000_reliability/ (owner forum)
- Quote: "there was someone on a ninja 1000sx who got to 120k miles without ever checking valve clearance lol."
- Tier: **Plausible** (anecdotal, single report).

---

## 5. Suzuki GSX-S1000 / Hayabusa

**F19. [OFFICIAL RECALL] Hayabusa (GSX1300R) front brake master-cylinder recall, 2022–2024, NHTSA 24V769 / Suzuki 3A04.**
- Claim: The front brake master-cylinder reservoir-cap diaphragm contains an additive that can swell rubber parts in the master cylinder → greater-than-normal brake-lever travel → extended stopping distances; 2022–2024 Hayabusa (GSX1300RM2–M4). 3A04 supersedes the earlier 2A99 campaign. Remedy: replace master-cylinder body + reservoir-cap diaphragm with updated material (~1 h, free).
- Source: https://suzukicycles.com/recalls/hayabusa (official manufacturer recall letter)
- Quote: "The front brake master cylinder reservoir cap diaphragm contains an additive that can affect the brake fluid and cause rubber parts inside the master cylinder to swell... Recall campaign 3A04 supersedes the previous 2A99 campaign."
- Tier: **Verified** (official). Note: a second, related 2022–2024 brake master-cylinder recall (6,338 units) and a 2023 993-unit braking recall are also documented (thebrakereport, autoevolution) — the Hayabusa has had **repeated** brake-system recalls.

**F20. [OFFICIAL RECALL] 2016 GSX-S1000 A/FA front brake caliper recall.**
- Claim: A 2016 GSX-S1000 front brake caliper recall is listed on Suzuki's official recalls page.
- Source: https://suzukicycles.com/recalls (official manufacturer recalls index)
- Quote: "2016 GSX-S1000 A FA Front Brake Caliper Recall Notice."
- Tier: **Verified** (official; old, used-market relevance).

**F21. [SURVEY / POSITIVE] GSX-R1000: very low complaint count.**
- Claim: The Suzuki GSX-R1000 has only 3 complaints on record across 10 model years — a low complaint signal.
- Source: https://vinspectorai.com/vehicle-stats/reliability/suzuki/gsx-r1000 (complaints aggregator)
- Quote: "The Suzuki GSX R1000 has 3 complaints on record across 10 model years."
- Tier: **Plausible** (aggregator; low-N, and GSX-R1000 ≠ GSX-S1000 exactly).

---

## 6. Honda CBR1100XX / CBR650R

**F22. [COMMUNITY — POSITIVE / NEW] CBR1100XX: too new for a track record; early reports favorable.**
- Claim: The CBR1100XX (2024+ Fireblade) is recent, so long-term reliability data is thin; early owner sentiment is favorable with no widely-reported critical defects yet.
- Source: https://www.cbrxx.com/threads/reliability-for-the-cbr-1100-xx.19798/ ; https://www.reddit.com/r/cbr/comments/1siyuua/new_fireblade_reliability/ (owner forums)
- Quote: "everything I have read about the bike online seems very favorable." (cbrxx)
- Tier: **Plausible** (early, low-N; MY2027-specific defects not yet documented).

**F23. [OFFICIAL RECALL — PREDECESSOR] CBR1000RR-R Fireblade SP: exhaust-overheat / oil-cooler-pipe recall.**
- Claim: The CBR1000RR-R Fireblade SP exhaust could overheat, melting/rupturing the oil-cooler pipe → oil leak (onto rear tire) → fire risk; ~331 US units (Apr 2020–Oct 2021).
- Source: https://www.bikesrepublic.com/english/archive/honda-issue-recall-for-cbr1000rr-r-fireblade-sp-due-to-overheat-exhaust/ ; https://www.newsbytesapp.com/news/auto/honda-cbr1000rr-r-fireblade-sp-recalled-in-the-us/story (trade press)
- Quote: "the exhaust pipe on the Fireblade SP could overheat, which could lead to the oil cooler pipe melting and rupturing." / "An issue with the oil cooler pipe is plaguing 331 units."
- Tier: **Verified** (predecessor platform; the CBR1100XX carries the Fireblade SP lineage — check whether the MY2027 CBR1100XX is affected/updated).

**F24. [OFFICIAL RECALL — PREDECESSOR] CBR1000RR-R Fireblade SP: connecting-rod failures at sustained high rpm (Honda Europe).**
- Claim: Honda Europe recalled the CBR1000RR-R Fireblade SP over connecting-rod failures experienced at sustained high-rpm operation during internal testing.
- Source: https://www.roadracingworld.com/news/honda-europe-recalling-cbr1000rr-r-fireblade-sp/ (trade press)
- Quote: "The recall is related to connecting rod failures experienced at sustained high rpm operation during internal testing, according to American Honda Motorcycle Press Relations."
- Tier: **Verified** (predecessor; a significant top-end durability signal for the high-rev Fireblade engine family).

**F25. [OFFICIAL RECALL — PREDECESSOR] CBR1000RR-R Fireblade SP: rear cushion / connecting-plates recall (2021).**
- Claim: A 2021 recall addressed incorrectly installed rear cushion connecting plates that could let the bike suddenly drop height.
- Source: https://www.rideapart.com/news/501515/honda-cbr1000rrr-fireblade-sp-recall/ (trade press)
- Quote: "due to the possibility of incorrectly installed rear cushion connecting plates."
- Tier: **Verified** (predecessor).

**F26. [PRO TEST] Fireblade SP: runs hot, high oil consumption under hard use.**
- Claim: The Fireblade SP is a high-revving race-derived bike that runs hot and consumes more oil than typical, especially when pushed.
- Source: https://enginepatrol.com/honda-cbr-1000rr-r-fireblade-sp-common-problems/ (problems roundup)
- Quote: "the Fireblade SP is a race bike, which means it revs high, runs hot, and consumes more oil than other motorcycles, especially when pushed hard."
- Tier: **Plausible** (expected trait, not a defect).

---

## 7. Yamaha Tracer 7 (Tracer 700, CP2 689 cc)

**F27. [SURVEY / POSITIVE] Tracer 7: no widely-reported critical reliability issues (4 minor documented).**
- Claim: The Tracer 700 has no widely-reported critical reliability issues; only ~4 minor issues are documented.
- Source: https://motoryk.com/bikes/yamaha/tracer-700 (review/reliability summary)
- Quote: "The Yamaha Tracer 700 has no widely-reported critical reliability issues. 4 minor issues are documented."
- Tier: **Plausible**.

**F28. [COMMUNITY] Tracer 7: clutch rattle (worn clutch-bolt rubber dampers).**
- Claim: A common Tracer complaint is clutch rattle, often from worn rubber dampers on the clutch bolts (vibration at high rpm); can also trace to flywheel/release-bearing faults; frequently a maintenance issue.
- Source: https://motorandwheels.com/common-problems-yamaha-tracer/ (problems roundup)
- Quote: "As the rubber wears out, the bolts' snug space starts to open up, which causes the bolts to vibrate... causing the Tracer's clutch-rattle... a common complaint on Yamaha Tracers, often resulting from a lack of upkeep."
- Tier: **Plausible**.

**F29. [COMMUNITY] Tracer 700 (2020): vibration + cyclic scrub at ~4,000 km.**
- Claim: A new 2020 Tracer 700 developed increased handgrip/seat vibration and a cyclic scrub sound at ~4,000 km; the dealer's test found nothing wrong.
- Source: https://www.motorcycleforum.com/threads/tracer-700-2020-vibration-issue.245401/ (owner forum)
- Quote: "I am having issues with a lot more vibrations felt on handgrips and seat. Furthermore there is a noticeable sound of a cyclic scrub... Yamaha shop, they've tested it and said it's fine but it definitely doesn't feel so."
- Tier: **Plausible** (single owner).

**F30. [COMMUNITY / WARRANTY] MT07/XSR700/Tracer700 engine failures attributed to non-approved aftermarket exhausts.**
- Claim: Yamaha observed increasing MT07/XSR700/Tracer700 engine failures (incl. total engine damage) within warranty, attributed to non-Yamaha-approved exhausts (notably SC Project and Arrow).
- Source: https://www.xsr700forums.com/threads/mt07-xsr-700-tracer-700-engine-failure.9028/ (owner forum, quoting Yamaha)
- Quote: "YAMAHA has observed an increasing number of failures on vehicles of their brand, including important engine damage on MT07/XSR700/Tracer700 due to the use of non Yamaha-approved exhaust lines, most notably SC Project and Arrow."
- Tier: **Plausible** (aftermarket-induced; relevant to warranty posture, not a base-bike defect).

**F31. [COMMUNITY] Tracer 7: paint/cosmetic problems (2023).**
- Claim: A 2023 Tracer 7 owner reported paint problems; another noted 80,000 km all-weather with no such issue.
- Source: https://www.reddit.com/r/Yamaha/comments/1azvpx8/2023_yamaha_tracer_7_paint_problems/ (owner forum)
- Quote: "Is it a major concern with future issues or should I just forget about it?... Mine has 80.000km in all weather and doesn't look like that."
- Tier: **Plausible** (cosmetic, mixed).

**F32. [EXCLUSION] Tracer 900 battery-drain issues are a DIFFERENT model.**
- Claim: Reported battery-drain/electrical issues belong to the Tracer 900, not the Tracer 7 — do not conflate.
- Source: https://wrasse.plymouth.ac.uk/ac-news/yamaha-tracer-900-common-problems-and-how-to-fix-them-1767648584 (Tracer 900-specific)
- Quote: "The Yamaha Tracer 900 is packed with modern technology... One of the most common issues is battery problems."
- Tier: **Verified** (negative/exclusion finding — keeps the Tracer 7 record clean).

---

## 8. Triumph Speed Triple 1200 RS / Tiger Sport 800

**F33. [OFFICIAL RECALL] Speed Triple 1200 RR/RS: radiator-fan-motor recall (2022–2023), 1,351 units.**
- Claim: A faulty radiator fan motor on 2022–2023 Speed Triple 1200 RS/RR could cause overheating; 1,351 units recalled.
- Source: https://www.rideapart.com/news/632726/triumph-speed-triple-fan-recall/ (trade press)
- Quote: "Triumph recalls 1,351 Speed Triple 1200 RS and RR units produced for the 2022 and 2023 model years due to a faulty radiator fan motor."
- Tier: **Verified**.

**F34. [OFFICIAL RECALL] Speed Triple 1200 RS/RR: engine-overheat recall (2022–2024).**
- Claim: A safety recall on 2022–2024 Speed Triple RR/RS addresses a potential engine-overheating issue.
- Source: https://www.rideapart.com/news/712154/triumph-speed-triple-safety-recall/ (trade press)
- Quote: "Triumph Motorcycles America is issuing a safety recall on certain 2022-2024 Speed Triple RR and RS bikes due to a potential engine overheating issue."
- Tier: **Verified**.

**F35. [OFFICIAL RECALL] Speed Triple 1200: rear brake-rotor bolt recall.**
- Claim: A recall addressed rear brake-rotor bolts that could allow the rotor to come loose.
- Source: https://www.reddit.com/r/Triumph/comments/1av17mh/speed_triple_1200_recalls/ ; https://www.triumphrat.net/threads/speed-1200rs-reliability-poll.992727/ (owner forums, recall-confirmed)
- Quote: "one is that the rear brake rotor might come loose, so the bolts…" / "recall for the rear brake rotor bolts."
- Tier: **Plausible** (community-confirmed official recall; NHTSA campaign number not captured this run).

**F36. [COMMUNITY] Speed Triple 1200 RS owner-reported issues (fuel leak, exhaust-bracket recall, fuel gauge, heated grips).**
- Claim: A 2021–2024 Speed Triple 1200 RS owner lists: a major fuel leak (warranty), a recall for exhaust-bracket malfunction (warranty), a faulty fuel gauge, and failed heated grips (warranty); another reports limp mode at 1,700 miles.
- Source: https://www.motorcyclenews.com/bike-reviews/triumph/speed-triple-1200-rs/2021/ (review comments) ; https://www.triumphrat.net/threads/speed-1200rs-reliability-poll.992727/ (owner forum)
- Quote: "1) Major fuel leak bumped half the tank on the road until I stopped it (warranty issue) 2) Recall for exhaust bracket malfunction (warranty) 3) Fuel gauge playing up 4) Heated grips failed (warranty)." / "Bike went into the 'limp mode' at 1700 miles."
- Tier: **Plausible** (community, mixed severity).

**F37. [COMMUNITY] Tiger 800 / Tiger Sport 800: frequent engine oil leaks.**
- Claim: The Tiger 800 platform has a common problem with frequent engine oil leaks; a RevZilla long-term found ~1 quart low before the 5,000-mile change, and 2 of 3 other post-2015 Tigers showed the same.
- Source: https://motorandwheels.com/triumph-tiger-800-issues/ ; https://www.revzilla.com/common-tread/triumph-tiger-800-xcx-a-year-of-abuse-in-review (problems roundup + pro long-term)
- Quote: "The Triumph Tiger 800 has a common problem with frequent engine oil leaks." / "I first discovered I was about a quart low shortly before I changed the oil around 5,000 miles... I am not the only one."
- Tier: **Plausible** (recurring community + pro observation).

**F38. [COMMUNITY] Tiger 800 / Tiger Sport 800: low-speed surging/hunting; heat-stall.**
- Claim: Owners report low-speed surging/hunting (one "resolved, but with a bizarre dealer experience") and a heat-related stall where the bike wouldn't restart until moved.
- Source: https://www.reddit.com/r/Triumph/comments/q212hy/tiger_800_are_different_gens_more_problematic/ ; https://www.reddit.com/r/Triumph/comments/1oxwih2/how_reliable_is_the_tiger_800/ (owner forums)
- Quote: "Low-speed surging/hunting on the Tiger Sport 800 (Resolved, but with a bizarre dealer experience)." / "Just had the heat issue. Stalled and it wouldn't turn on."
- Tier: **Plausible**.

**F39. [COMMUNITY — POSITIVE] Tiger 800: "bulletproof" / perfect-reliability reports.**
- Claim: Counterweight: multiple owners report the Tiger 800 as effectively problem-free ("bulletproof," "reliability was perfect," 10k miles with only a minor oil leak).
- Source: https://www.reddit.com/r/motorcycles/comments/2l0wkv/triumph_tiger_800_experiences_hows_the_reliability/ ; https://www.reddit.com/r/Triumph/comments/1oxwih2/how_reliable_is_the_tiger_800/ (owner forums)
- Quote: "Apparently the 800s are bulletproof anyways." / "Otherwise the reliability was perfect for me."
- Tier: **Plausible** (positive community signal; the triple is a mature, well-proven engine).

---

## 9. Ducati Multistrada V4

**F40. [OFFICIAL RECALL] Multistrada V4: valve-guide recall (2021), NHTSA 21V212000, 129 units.**
- Claim: One of two valve-guide suppliers had longevity defects → excessive engine wear → power loss → valve-head failure; 129 units (small batch); affected engines replaced free. The V4 Granturismo had just switched from Desmodromic to conventional valve springs (valve-check interval extended to 36,000 mi).
- Source: https://www.rideapart.com/news/498563/ducati-multistrada-v4-valve-guides-recall/ (trade press, NHTSA-sourced)
- Quote: "Ducati contracted two suppliers for the engine components and one was found to experience longevity issues. If left unaddressed, the valve guides could cause excessive engine wear, which could lead to loss of power and a failure at the valve head."
- Tier: **Verified**.

**F41. [OFFICIAL RECALL — RECURRING] New Multistrada V4 S: valve-guide recall again.**
- Claim: A newly released Multistrada V4 S was recalled within months of its debut for the same valve-guide issue (one supplier's batch), indicating the valve-guide problem recurred on the updated V4.
- Source: https://www.advpulse.com/adv-news/ducati-issues-recall-on-newly-released-multistrada-v4-s/ (trade press)
- Quote: "Just a few months after its debut, Ducati of North America is recalling several units of the Multistrada V4 S for an issue with the engine's valve guides... the issue was only identified within one supplier's batch."
- Tier: **Verified** (recurring engine-top-end concern — the single most important reliability flag for the Multistrada V4 line; confirm MY2027 build is clear).

**F42. [PRO TEST / DESIGN] V4 Granturismo: conventional-spring valvetrain, 36,000-mile valve interval.**
- Claim: The V4 Granturismo's move from Desmodromic to conventional valve springs was intended to increase longevity and extend valve-check intervals to 36,000 miles.
- Source: https://www.rideapart.com/news/498563/ducati-multistrada-v4-valve-guides-recall/ (trade press)
- Quote: "the decision increased longevity and extended valve check intervals to 36,000 miles."
- Tier: **Verified** (design intent; the valve-guide recalls F40/F41 are the counterweight to that intent).

---

## 10. Aprilia Tuono V4 (V4 1100)

**F43. [COMMUNITY] Earlier V4 1000 (2015 and earlier): exhaust valve-guide + cam-lobe pitting.**
- Claim: Earlier 1000 cc V4 Tuonos/RSV4s (2015 and earlier) were known for exhaust valve-guide and cam-lobe pitting; owners do not believe the 1100 cc engines share these issues.
- Source: https://www.reddit.com/r/Aprilia/comments/1gqbhx5/how_is_tuono_v4_reliability/ (owner forum)
- Quote: "I'd stay away from earlier (say, 2015 and earlier) 1000cc V4 Tuonos and RSV4s as they were definitely known to have exhaust valve guide and cam lobe pitting problems. I don't believe the 1100s have the same issues in this regard."
- Tier: **Plausible** (predecessor; the 1100 is the current/relevant engine).

**F44. [COMMUNITY / WARRANTY] V4 1100: valve-shim warranty problem.**
- Claim: A V4 1100 Factory owner had valve shims replaced under warranty, calling it "a fairly major warranty problem" (left side uses gasket compound, not a gasket).
- Source: https://aprilia.me/t/v4-1100-factory-4-reliability.12558/ (owner forum)
- Quote: "I know because I had mine off to replace the valve shims which turned out to be a fairly major warranty problem."
- Tier: **Plausible** (single owner).

**F45. [COMMUNITY — POSITIVE] Tuono V4 1100: strong reliability reputation, clean owner reports.**
- Claim: The Tuono V4 1100 is regarded as "the Honda of European bikes" for reliability; multiple owners report 10k–15k+ miles with no issues.
- Source: https://www.reddit.com/r/Aprilia/comments/1cdnitw/reliability_of_a_2023_tuono_v4_1100_nonfactory/ (owner forum)
- Quote: "Aprilia is known to be the Honda of European bikes as far as reliability... My 2020 Tuono is at 10k miles and never had an issue... My 18 Tuono has 15K, and no issue ever."
- Tier: **Plausible** (positive community signal).

**F46. [COMMUNITY — PREDECESSOR] Earlier V4 1000: piston/valve + connecting-rod failures (poor-quality supplier).**
- Claim: Earlier V4 (1000) engines, attributed to a low-quality Italian supplier, saw piston-hit-valve and connecting-rod/piston failures; a 2018 engine failure is one cited case.
- Source: https://www.reddit.com/r/Aprilia/comments/1g5z0s5/tuono_v4_1100_engine_failure/ (owner forum)
- Quote: "previous v4 Engines where supplied by a very poor quality manifacturer in Italy hence the problems... piston hit the valve... piston went out of the Engine block due to breakage of the connecting rods."
- Tier: **Plausible** (predecessor 1000; not confirmed for the 1100).

---

## 11. KTM 1290 Super Duke R

**F47. [OFFICIAL RECALL] 1290 Super Duke R: main wiring-harness recall (MY2020–2022), all markets.**
- Claim: A misrouted main wiring harness could be damaged → short circuit and stalling; KTM recalls MY2020–2022 1290 Super Duke R / R EVO to authorized dealers to improve the harness ("Valid for all markets" → applies to CH).
- Source: https://www.ktm.com/language-masters/en/service/recall-pdfs/2022/Recall%20of%20KTM%201290%20SUPER%20DUKE%20R%20MY%2020-22_EN.pdf (official KTM recall PDF) ; https://www.autoevolution.com/news/ktm-recalls-1290-super-duke-r-and-1290-super-duke-r-evo-due-to-misrouted-wiring-harness-206417.html
- Quote: "KTM recalls KTM 1290 SUPER DUKE R models of model year 2020 - 2022 to the workshops of authorized KTM dealers in order to improve the main wiring harness." / "a misrouted wiring harness that may be damaged, thus resulting in a short circuit and stalling."
- Tier: **Verified** (official, all-markets).

**F48. [OFFICIAL RECALL] 1290 Super Duke R: tail-end lower part + main wiring-harness rework (MY2020).**
- Claim: A separate MY2020 recall reworked the tail-end lower part and checked the main wiring harness in that area.
- Source: https://www.ktm.com/content/dam/websites/ktm-com/language-masters/en/service/recall-pdfs/2021/Recall%20of%20KTM%201290%20SUPER%20DUKE%20R%20MY20%2010.02.2020.pdf (official KTM recall PDF)
- Quote: "RECALL OF KTM 1290 SUPER DUKE R MODEL YEAR 2020: REWORK OF THE TAIL END LOWER PART AND MAIN WIRING HARNESS... to check the main wiring harness in the area of..."
- Tier: **Verified** (official).

**F49. [COMMUNITY] 1290 Super Duke R: brake recall + radiator leak (warranty).**
- Claim: Owners reference a brake recall on the 1290 SDR and a radiator that leaked at a mounting bracket (replaced under warranty).
- Source: https://www.pistonheads.com/gassing/topic.asp?h=0&f=74&t=1791225 ; https://www.reddit.com/r/KTM/comments/1ccq3bx/reliability_of_1290/ (owner forums)
- Quote: "i still need to get my mk2 in for its brake recall and 2nd service." / "they replaced my tank on a recall or something, and the radiator under warranty because it started leaking at one of the mounting brackets."
- Tier: **Plausible** (community; specific brake-recall campaign number not captured this run).

**F50. [COMMUNITY — POSITIVE] 1290 Super Duke R: "faultless" owner reports.**
- Claim: Counterweight: multiple owners report the 1290 SDR (mk1 and mk2) as faultless.
- Source: https://www.pistonheads.com/gassing/topic.asp?h=0&f=74&t=1791225 (owner forum)
- Quote: "Both mk1 and mk2 have been faultless... Both my 1290 sdr have been faultless."
- Tier: **Plausible** (positive community signal).

---

## 12. Reliability surveys (brand-level context)

**F51. [SURVEY] Consumer Reports: Japanese brands out-reliability European; Yamaha/Suzuki/Honda/Kawasaki lead.**
- Claim: CR's subscriber survey (11,000+ then 12,300+ bikes) found Japanese brands significantly more reliable than most European bikes; predicted 4-year failure rates: Yamaha 11%, Suzuki 12%, Honda 12%, Kawasaki 15%.
- Source: https://www.consumerreports.org/cro/news/2015/04/who-makes-the-most-reliable-motorcycle/index.htm ; https://www.consumerreports.org/cro/magazine/2015/05/motorcycle-reliability-and-owner-satisfaction/index.htm
- Quote: "the Japanese brands are significantly more reliable than most bikes from other regions—led in order by Yamaha, Suzuki, Honda, and Kawasaki." / "predicted failure rates for four-year-old motorcycles ranged from 11 to 15 percent in this group."
- Tier: **Verified** (but **2015-era and brand-level**, not MY2027 model-level — use as directional context only).

**F52. [SURVEY] 2025: Japanese bikes consistently outperform European in reliability rankings.**
- Claim: 2025 brand-reliability roundups continue to rank the Japanese brands (Honda, Yamaha, Suzuki, Kawasaki) above the European makers.
- Source: https://drmotorides.com/the-most-reliable-and-unreliable-motorcycle-brands-of-2025/ (roundup)
- Quote: "Japanese motorcycles (Honda, Yamaha, Suzuki, Kawasaki) consistently outperform European bikes in reliability rankings."
- Tier: **Plausible** (secondary roundup, brand-level).

**F53. [SURVEY] BMW: 68% of owners would buy a BMW again (high satisfaction despite reliability ranking).**
- Claim: BMW ranks lower on raw reliability than the Japanese brands but has a high repurchase/satisfaction rate (~68% would buy again).
- Source: https://funtransport.com/blog/most-reliable-motorcycle-brands-motorcycle-reliability-by-brand-the-most-dependable-motorcycles-ever (roundup)
- Quote: "68% of owners would buy a BMW again. That's a higher customer satisfaction rate than Yamaha, ranked the most reliable."
- Tier: **Plausible** (secondary roundup, brand-level).

---

## 13. MY2026 → MY2027 reliability-relevant changes / fixes

- **Kawasaki:** Ninja 1000 / Z1000SX → **Ninja 1100SX** (new engine/chassis, MY2027 Europe). Predecessor's electrical/gasket/clutch/stall history (F16) may or may not carry over — unconfirmed for the 1100SX.
- **BMW S 1000 XR / M 1000 XR:** MY2027 facelift (new front design, radar). The 2024–2025 M 1000 XR steering-damper recall (F1) and 2020–2023 software recall (F2) predate MY2027; confirm the MY2027 build is outside affected windows.
- **Ducati Multistrada V4 S:** recurring valve-guide recalls (F40, F41) — the key thing to verify for MY2027 is whether the current build/supplier batch is clear.
- **BMW R 1300 platform:** starter-relay recall (F6) and early clutch-failure reports (F7) are MY2024–2025 platform items; the MY2027 R 1300 RS is the 3rd model year — watch whether clutch/gearbox complaints (F7, F8) persist.
- **Honda CBR1100XX:** MY2027 is only ~3rd year; predecessor Fireblade SP top-end (connecting rod, F24) and exhaust-overheat (F23) history is the main thing to confirm as resolved/updated.

---

## 14. Searched, found nothing / evidence of absence

- **Swiss-specific recall database (SECO / BAFU / Swiss-Moto recall notices):** searched for CH-specific recall/TSB entries for these models — **no Swiss-specific recall database entries surfaced** via web search. Swiss recalls generally mirror the EU/manufacturer campaigns already captured (KTM's "valid for all markets" recall F47/F48 explicitly covers CH). A direct SECO/BAFU database query was not possible in this run (see Gaps).
- **J.D. Power model-level moto reliability for MY2027:** searched — **no J.D. Power motorcycle model-level reliability index found**; only brand-level Consumer Reports (F51) and secondary roundups (F52/F53) exist. No MY2027-specific survey data (too early).
- **MY2027-specific recall/TSB for most candidates:** searched per model — **no MY2027-dated recall or TSB found** for BMW S 1000 XR / R 1300 RS / F 900 XR, Yamaha Tracer 7, Triumph, Aprilia, KTM, or the new Kawasaki Ninja 1100SX (MY2027 not yet fully on sale / not yet announced in most markets).
- **CBR1100XX MY2027-specific defects:** searched — **none documented yet** (model too new); only predecessor CBR1000RR-R recall history (F23–F25).
- **F 900 XR owner-forum deep dive (f900xr.com "Concerns and Longevity" thread):** attempted to read the full thread — **scrape failed (server error)**; only the search snippet was captured. Individual F 900 XR complaints were instead sourced from motoplanete/motosport/bayareariders (F10–F13).
- **Triumph Speed Triple 1200 rear-brake-rotor-bolt recall NHTSA campaign number:** community-confirmed (F35) but the **official NHTSA campaign number was not captured** this run.
- **KTM 1290 SDR brake-recall campaign number:** community-referenced (F49) but the **specific official campaign number was not captured** this run.
- **BMW 2020 S 1000 XR "two recalls" (brakes + electrical) underlying NHTSA campaign numbers:** aggregator-sourced (F5) but the **individual NHTSA PDFs were not re-verified** this run.

---

## 15. Source-universe checklist (coverage)

- **Official manufacturer recall notices / TSBs:** COVERED (Suzuki 3A04/2A99, KTM MY2020-22 wiring harness, BMW NHTSA campaigns, Ducati valve-guide, Triumph fan/overheat, Honda Fireblade SP).
- **NHTSA recall database:** COVERED (campaign numbers captured for BMW 25V194000 / 23V-051 / 24V-557, Suzuki 24V769, Ducati 21V212000; several others referenced via NHTSA-sourced trade press).
- **EU/Swiss recall databases:** PARTIAL — no direct SECO/BAFU query possible this run; relied on "all markets" manufacturer recalls (KTM) + EU-sourced trade press (Honda Europe, Ducati Bologna).
- **Owner forums (reliability/defect threads):** COVERED (r/motorcycles, r/bmwmotorrad, r1300gsforum, f900xr.com, r/Kawasaki, r/Yamaha, r/Triumph, r/Aprilia, r/KTM, triumphrat, xsr700forums, pistonheads, bayareariders, cbrxx, motoplanete).
- **Pro long-term test findings:** COVERED (MCNews, MCN, RevZilla, Cycle News, bike review AU, enginepatrol, motofomo).
- **Reliability surveys (J.D. Power / owner-satisfaction):** PARTIAL — Consumer Reports brand-level (2015) + 2025 roundups; no model-level MY2027 index exists.
- **Code / GitHub:** N/A (not applicable to motorcycle hardware).
