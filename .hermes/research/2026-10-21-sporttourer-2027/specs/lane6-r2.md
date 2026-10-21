# Lane 6 — Round 2 — Specs gap (MY2027 sport-tourers, CH)

Research date: 2026-10-21 (round 2). Tier: **V** = Verified (authoritative source read whole) · **P** = Plausible · **S** = Speculative.
Scope: fill round-1 Q2 gaps — official specs for Yamaha Tracer 9 / 9 GT / 9 GT+ / 7, Ducati Multistrada V4 family, MV Agusta TV800; secondary: KTM 1390 GT weight, KTM 1390 GT CH price, BMW M 1000 RS CH presence.
Builds on: specs/lane1.md (round 1), prices/lane2.md (CH prices + hyperdrive API notes).

**Key round-2 access finding (Yamaha):** the round-1 404 was on `yamaha.ch` (wrong domain). The live official CH site is **yamaha-motor.eu/ch/de**, and its product data (including the full technical-spec tables rendered on each PDP) is served by the hyperdrive API: `https://hyperdrive.yamaha-motor.eu/products/yme-prod-ch/slug=<slug>?locale=de-CH` — each product's `variants[n].attributes[techSpecifications]` contains the complete localized spec table (Motor / Fahrwerk / Abmessungen / Screen & Connectivity), the same content as the PDP "Daten" section and the "Datenblatt" PDF. **Tier V** (API read live, cross-checked against rendered PDP tables on yamaha-motor.eu/ch/de, identical values).

## 1. Yamaha Tracer 9 / 9 GT / 9 GT+ / 7 — official specs

### 1.0 CH catalog structure (what "official CH" means for the Tracer line, as of 2026-10-21)
- **Claim:** The current CH sport-touring catalog (official CH importer site) lists 8 Tracer SKUs; the MY2025 generation is the newest published (no MY2027 Tracer exists yet).
- **Source:** https://www.yamaha-motor.eu/ch/de/motorcycles/sport-touring/ (official CH importer, browser-read live)
- **Verbatim (card labels):** "2025 TRACER 9 GT+ CHF 18'990.00" (slug `tracer-9-gt-plus-y-amt`), "2025 TRACER 9 GT CHF 15'690.00" (slug `tracer-9-gt`), "2025 TRACER 9 CHF 12'490.00" (slug `tracer-9`), "2024 TRACER 9 GT CHF 14'490.00" (slug `tracer-9-gt-2024`, run-out), "2025 TRACER 7 CHF 10'490.00", "2025 TRACER 7 GT CHF 11'990.00", "2024 TRACER 7 CHF 9'490.00", "2024 TRACER 7 GT Ab CHF 10'490.00".
- **Tier V**

### 1.1 Yamaha Tracer 9 (MY2025)
- **Claim:** Engine: 890 cc CP3 inline triple, 4-stroke liquid-cooled DOHC 4V, bore×stroke 78×62.1 mm, 11.5:1; 6-speed chain drive.
- **Source:** https://www.yamaha-motor.eu/ch/de/motorcycles/sport-touring/pdp/tracer-9/ + API `hyperdrive.yamaha-motor.eu/products/yme-prod-ch/slug=tracer-9` (official CH, read whole).
- **Verbatim:** "Hubraum = 890 cm³", "Bohrung x Hub = 78 x 62,1 mm", "Verdichtungsverhältnis = 11,5 : 1", "Kraftübertragungssystem = Konstanter Eingriff, 6-Gang".
- **Tier V**
- **Claim:** Power 87.5 kW (119 PS) at 10,000/min; torque 93 Nm at 7,000/min.
- **Source:** same (official CH).
- **Verbatim:** "Maximale Leistung = 87,5 kW (119 PS) bei 10.000/min"; "Maximales Drehmoment = 93 Nm bei 7.000/min". (Confirms round-1 Tier-P figures from moto-data/1000ps — now official.)
- **Tier V**
- **Claim:** Kerb weight (ready to ride, with oil and full tank): 219 kg with standard 6-speed gearbox; 224 kg with Y-AMT. No dry weight published.
- **Source:** same (official CH).
- **Verbatim:** "Gewicht, fahrfertig (mit Öl und vollem Kraftstofftank) = Standard-6-Gang-Schaltgetriebe: 219 kg; Y-AMT: 224 kg".
- **Tier V**
- **Claim:** Tank 19 L; seat 845–860 mm; wheelbase 1,500 mm; ground clearance 135 mm; overall length 2,175 mm; height 1,460–1,505 mm.
- **Source:** same. **Verbatim:** "Kraftstofftank-Volumen = 19 l", "Sitzhöhe = 845 mm – 860 mm", "Radstand = 1.500 mm".
- **Tier V**
- **Claim:** Brakes: front hydraulic twin disc Ø298 mm, rear hydraulic single disc Ø267 mm; tires 120/70ZR17 (58W) / 180/55ZR17 (73W) tubeless.
- **Source:** same. **Verbatim:** "Vorderradbremse = Hydraulische Doppelscheibenbremse, Ø 298 mm", "Hinterradbremse = Hydraulische Einzelscheibenbremse, Ø 267 mm".
- **Tier V**
- **Claim:** Suspension/chassis: diamond frame; USD 41 mm KYB fork fully adjustable + KYB monoshock (official feature text); travel 130/131 mm; rake 24°25', trail 106 mm.
- **Source:** PDP feature text + spec table (official CH). **Verbatim:** "Hochspezialisierte 41-mm-KYB-Telegabel ist voll einstellbar, ebenso wie das KYB-Federbein hinten"; "Federweg vorn = 130 mm / Federweg hinten = 131 mm".
- **Tier V**
- **Claim:** Electronics/equipment (MY2025 base): YRC riding modes (SPORT/STREET/RAIN + 2 user), 7" TFT with USB-C and storage, LED twin headlight with cornering light (from 7° lean), 10-stage windscreen, cruise control + speed limiter (from 3rd gear), emergency stop signal, TPMS (via "Anpassbare Fahrmodi"/feature set), Y-AMT optional.
- **Source:** PDP "Features" section (official CH, read whole). **Verbatim:** "Drei Werkseinstellungen sind vorinstalliert (SPORT, STREET und RAIN), während zwei benutzerdefinierte Einstellungen ... programmiert werden können"; "Der serienmäßige Tempomat ... ab dem dritten Gang"; "Eine neue Funktion ist die Notbremssignalfunktion".
- **Tier V**

### 1.2 Yamaha Tracer 9 GT (MY2025)
- **Claim:** Same CP3 engine: 87.5 kW (119 PS) @ 10,000/min, 93 Nm @ 7,000/min, 890 cc, 11.5:1, 6-speed.
- **Source:** API `slug=tracer-9-gt` (official CH, read whole). **Verbatim:** "Maximale Leistung = 87,5 kW (119 PS) bei 10.000/min", "Maximales Drehmoment = 93 Nm bei 7.000/min".
- **Tier V**
- **Claim:** Kerb weight (ready, full tank): 227 kg standard 6-speed; 231 kg Y-AMT. Tank 19 L; seat 845–860 mm; height 1,440–1,530 mm; wheelbase 1,500 mm.
- **Source:** same (official CH). **Verbatim:** "Gewicht, fahrfertig (mit Öl und vollem Kraftstofftank) = Standard-6-Gang-Schaltgetriebe: 227 kg; Y-AMT: 231 kg". (Confirms round-1 Tier-P "GT ~227 kg" from throttlecraze — now official.)
- **Tier V**
- **Claim:** Brakes/tires identical to base Tracer 9 (front twin Ø298 mm, rear Ø267 mm; 120/70ZR17 / 180/55ZR17); USD fork; travel 130/131 mm.
- **Source:** same. **Tier V**

### 1.3 Yamaha Tracer 9 GT+ (MY2025, Y-AMT — the current top model, CHF 18'990)
- **Claim:** Engine: 87.5 kW (119 PS) @ 10,000/min; 93 Nm @ 7,000/min; 890 cc CP3, 11.5:1, 6-speed Y-AMT (clutchless).
- **Source:** API `slug=tracer-9-gt-plus-y-amt` (official CH, read whole). **Verbatim:** "Maximale Leistung = 87,5 kW (119 PS) bei 10.000/min", "Maximales Drehmoment = 93 Nm bei 7.000/min".
- **Tier V**
- **Claim:** Kerb weight (ready, full tank): **232 kg** (single figure — GT+ is Y-AMT only). Tank 19 L; seat 845–860 mm; wheelbase 1,500 mm; height 1,440–1,530 mm.
- **Source:** same (official CH). **Verbatim:** "Gewicht, fahrfertig (mit Öl und vollem Kraftstofftank) = 232 kg". (Confirms round-1 Tier-P "GT+ Y-AMT ~232 kg".)
- **Tier V**
- **Claim:** Brakes: front hydraulic twin disc Ø298 mm, rear Ø267 mm; tires 120/70ZR17 / 180/55ZR17; USD fork; travel 130/131 mm.
- **Source:** same. **Tier V**
- **Claim:** Electronics (MY2025 GT+): **radar with adaptive cruise control AND blind-spot detection; semi-active electronic suspension; matrix LED headlight; 7" TFT with navigation via free Garmin Motorize app; electric windscreen; Smart Key with central locking; intelligent brake system with hill-hold; TPMS; adaptive riding modes (YRC); Y-AMT.**
- **Source:** PDP `pdp/tracer-9-gt-plus-y-amt/` feature list (official CH, read whole) + spec table. **Verbatim headings:** "Radar mit adaptiver Geschwindigkeitsregelanlage und Toter-Winkel-Erkennung", "Einstellbares, semiaktives elektronisches Fahrwerk", "Völlig neuer Matrix LED-Scheinwerfer", "7 Zoll großes TFT-Farbdisplay mit Kartennavigation durch die kostenlose Garmin Motorize App", "Intelligentes Bremssystem mit Fahrzeughaltefunktion", "Smart Key-Technologie mit Zentralverriegelung". Spec table adds: "Screen & Connectivity :: Adaptive Cruise Control = Ja" (base Tracer 7 spec table shows ACC = Nein — the table field is model-specific).
- **Tier V** (closes round-1 Tier-P electronics gap from 1000ps test)
- **Note (run-out MY2024 GT+):** slug `tracer-9-gt-plus` (PDP `/pdp/tracer-9-gt-plus/`) = "TRACER 9 GT+ Icon Performance CHF 16'490.00" — the MY2024 run-out (different geometry: rake 25°00', trail 108 mm, seat 820–835 mm, kerb 223 kg). **Tier V**

### 1.4 Yamaha Tracer 7 (MY2025)
- **Claim:** Engine: 689 cc CP2 parallel twin, 4-stroke liquid-cooled DOHC 4V, bore×stroke 80.0×68.6 mm, 11.5:1, 6-speed. Power **54 kW** (≈73.5 PS) at 8,750/min; A2-limited version 35 kW at 7,750/min; torque 68 Nm (6.83 kg·m) at 6,500/min.
- **Source:** API `slug=tracer-7` (official CH, read whole). **Verbatim:** "Hubraum = 689 cm³", "Maximale Leistung = 54 kW bei 8 750 U/min", "Limited power version = 35 kW bei 7 750 U/min", "Maximales Drehmoment = 68 Nm (6,83 kg-m) bei 6 500 U/min". (Official kW figure; round-1 "73–75 PS" was secondary — 54 kW = 73.5 metric PS, consistent.)
- **Tier V**
- **Claim:** Kerb weight (ready, full tank): 203 kg standard 6-speed; 206 kg Y-AMT. Tank 18 L; seat 830–850 mm; wheelbase 1,495 mm; ground clearance 140 mm.
- **Source:** same (official CH). **Verbatim:** "Gewicht, fahrfertig (mit Öl und vollem Kraftstofftank) = Standard-6-Gang-Schaltgetriebe: 203 kg; Y-AMT: 206 kg". (Closes round-1 Tier-P "~212 kg wet" — that figure was actually the GT's; base is 203 kg.)
- **Tier V**
- **Claim:** Brakes: front twin disc Ø298 mm, rear single Ø245 mm; 41 mm USD fork; travel 130/139 mm; tires 120/70ZR17 / 180/55ZR17. Connectivity: MyRide app, Garmin StreetCross on-screen navigation option, ACC = Nein (not fitted).
- **Source:** same (official CH). **Verbatim:** "Vorderradbremse = Hydraulische Doppel-Bremsscheiben, Ø 298 mm", "Hinterradbremse = Hydraulische Scheibenbremse, Ø 245 mm", "Screen & Connectivity :: Smartphone Connectivity = MyRide", "Adaptive Cruise Control = Nein", "On-screen Navigation = Garmin StreetCross".
- **Tier V** (closes round-1 "full brake/tire spec not captured" gap)

### 1.5 Yamaha Tracer 7 GT (MY2025)
- **Claim:** Same engine (689 cc, 54 kW @ 8,750/min, 35 kW A2 version, 68 Nm @ 6,500/min). Kerb weight (ready, full tank): 212 kg standard; 214 kg Y-AMT. Tank 18 L; seat 845 mm (865 mm); wheelbase 1,495 mm.
- **Source:** API `slug=tracer-7-gt` (official CH, read whole). **Verbatim:** "Gewicht, fahrfertig (mit Öl und vollem Kraftstofftank) = Standard-6-Gang-Schaltgetriebe: 212 kg; Y-AMT: 214 kg", "Sitzhöhe = 845 mm (865mm)".
- **Tier V**
- **Claim:** Brakes/tires/fork identical to Tracer 7 base (front Ø298 mm twin, rear Ø245 mm, 41 mm USD, 130/139 mm travel); GT adds taller fairing/seat ergonomics (height 1,425–1,480 mm vs 1,330–1,390 mm).
- **Source:** same (official CH). **Tier V**

### 1.6 Yamaha status finding
- **Claim:** No MY2027 Tracer model or MY2027 price/spec delta is published on the official CH site as of 2026-10-21 — newest published generation is MY2025 (with 2024 SKUs in run-out). Any MY2027 changes remain EICMA-2026-pending (unpublished finding, not a gap).
- **Source:** yamaha-motor.eu/ch/de sport-touring catalog (official CH, read whole); consistent with lane2 price findings (all SKUs "valid from 2026-01-21", 2025-gen prefixes).
- **Tier V** (absence verified on official catalog)

## 2. Ducati Multistrada V4 / V4 S (family) — official specs

### 2.0 CH lineup + access finding
- **Claim:** ducati.com/ch (CH official) is browser-readable and publishes a full side-by-side "Technische Daten" table for Multistrada V4 and V4 S on the model page; the CH lineup (per nav/prices) is: Multistrada V4 (ab CHF 19'990), V4 S (ab CHF 25'290), V4 S Grand Tour (ab CHF 28'490), V4 Rally (ab CHF 29'290), V4 Pikes Peak (ab CHF 33'190), V4 RS (ab CHF 39'990). **There is no model called "Multistrada V4 GT"** — the touring top-trim is the "V4 S Grand Tour". (Confirms lane2 price nav; no MY2026/2027 label — copy still refers to "Modelljahr 2025".)
- **Source:** https://www.ducati.com/ch/de/motorrader/multistrada/multistrada-v4 (official CH, browser-read live, full spec table read whole) + nav cards (browser).
- **Tier V**

### 2.1 Multistrada V4 (base) — official CH
- **Claim:** Engine: V4 Granturismo — liquid-cooled 90° V4, counter-rotating crank, 4V/cyl, Twin Pulse ignition, semi-dry sump; 1,158 cm³, bore×stroke 83×53.5 mm, compression 14:1.
- **Source:** ducati.com/ch Technische Daten (official CH, read whole).
- **Verbatim:** "TYP :: V4 Granturismo: flüssigkeitsgekühlter 90-Grad-V4-Motor mit gegenläufiger Kurbelwelle, 4 Ventile pro Zylinder, Twin Pulse Zündfolge, Semi-Trockensumpfsystem"; "BOHRUNG X HUB :: 83 x 53,5 mm"; "VERDICHTUNG :: 14:1".
- **Tier V**
- **Claim:** Power 170 PS (125 kW) at 10,750 U/min; torque **124 Nm at 9,000 U/min**. (Note: round-1 secondary source 1000ps quoted "125 Nm at 8,750/min" — the official CH table differs slightly in Nm/rpm; official values prevail here.)
- **Source:** same. **Verbatim:** "LEISTUNG :: 170 PS (125 kW) bei 10.750 U/min", "DREHMOMENT :: 124 Nm bei 9.000 U/min".
- **Tier V**
- **Claim:** Weight: **229 kg "fahrfertig ohne Kraftstoff"** (ready to ride, WITHOUT fuel). Tank 22 L. (Closes round-1 gap where only a 2020 secondary "~243 kg wet" existed.)
- **Source:** same. **Verbatim:** "GEWICHT FAHRFERTIG OHNE KRAFTSTOFF :: 229 kg", "TANKINHALT :: 22 l".
- **Tier V**
- **Claim:** Chassis/suspension: aluminium monocoque frame; fully adjustable 50 mm USD fork (mechanical compression/rebound) + fully adjustable monoshock w/ remote preload, aluminium twin-spar swingarm; travel 170/180 mm; wheelbase 1,566 mm; rake 24.2°; trail 100.6 mm; seat 840–860 mm adjustable (accessory seats 795–890 mm).
- **Source:** same. **Verbatim:** "RAHMEN :: Monocoque-Rahmen aus Aluminium", "VORDERE FEDERUNG :: Voll einstellbare Upside-Down-Federgabel mit Ø 50 mm ...", "FEDERWEG (VORN/HINTEN) :: 170 mm / 180 mm", "RADSTAND :: 1.566 mm".
- **Tier V**
- **Claim:** Brakes: front 2×320 mm floating discs, radial-mounted Brembo monoblock 4-piston calipers, cornering ABS; rear 280 mm disc, Brembo 2-piston floating, cornering ABS. Tires: 19" front / 17" rear — Pirelli Scorpion Trail II 120/70 ZR19 front, 170/60 ZR17 rear.
- **Source:** same. **Verbatim:** "VORDERRADBREMSE :: 2 x Ø 320 mm halbschwimmend gelagerte Bremsscheiben, radial verschraubte Brembo Monoblock 4-Kolben-Bremszangen ... Kurven-ABS", "VORDERREIFEN :: Pirelli Scorpion Trail II 120/70 ZR 19", "HINTERREIFEN :: Pirelli Scorpion Trail II 170/60 ZR 17".
- **Tier V**
- **Claim:** Transmission/electronics (base V4): 6-speed with Ducati Quick Shift up/down, hydraulic anti-hopping clutch; 5" TFT; safety package = Riding Modes, Power Modes, cornering ABS, Ducati Traction Control, Ducati Wheelie Control, DRL, Cornering Light, Brake Light EVO; standard: DQS, cruise control, full-LED headlight.
- **Source:** same. **Verbatim:** "GETRIEBE :: 6-Gang-Getriebe mit Ducati Quick Shift (DQS) Up/Down", "SICHERHEITSAUSSTATTUNG :: Riding Modes, Power Modes, Kurven-ABS, Ducati Traction Control, Ducati Wheelie Control, Daytime Running Light, Ducati Cornering Light, Ducati Brake Light EVO".
- **Tier V**
- **Claim:** Emissions/service: Euro 5+, CO2 152 g/km, 6.6 L/100 km; warranty 48 months unlimited km; oil interval 15,000 km/24 months.
- **Source:** same. **Tier V**

### 2.2 Multistrada V4 S — official CH
- **Claim:** Same engine (1,158 cm³, 170 PS (125 kW) @ 10,750, 124 Nm @ 9,000); weight **231 kg fahrfertig ohne Kraftstoff**; tank 22 L; 19"/17" Scorpion Trail II.
- **Source:** same comparison table (V4 S column, official CH). **Verbatim:** "GEWICHT FAHRFERTIG OHNE KRAFTSTOFF :: 229 kg / 231 kg" (V4 / V4 S).
- **Tier V**
- **Claim:** Suspension upgrade: **Ducati Skyhook semi-active** front + rear — "Zug-/Druckstufendämpfung elektronisch einstellbar über die Ducati Skyhook Suspension, integrierter Federwegsmesser" (front); rear "elektronisch einstellbar über die Ducati Skyhook Suspension, Absenkautomatik zwischen 10km/h und 50km/h".
- **Source:** same (V4 S column). **Tier V**
- **Claim:** Brakes upgrade: front **2×330 mm Brembo Stylema** monoblock 4-piston (cornering ABS); rear 280 mm Brembo 2-piston.
- **Source:** same (V4 S column). **Verbatim:** "2 x Ø 330 mm halbschwimmend gelagerte Bremsscheiben, radial verschraubte Brembo Stylema Monoblock 4-Kolben-Bremszangen ... Kurven-ABS".
- **Tier V**
- **Claim:** Electronics/equipment (V4 S): 6.5" TFT with Ducati Connect + map navigation; safety adds Engine Brake Control (EBC), Bosch cornering ABS, Ducati Vehicle Observer (DVO) with automatic tire calibration, Vehicle hold control; standard adds DQS up/down 2.0, Coming-Home, **Extended Cylinder Deactivation (ECD)**, Hands-Free, automatic turn-signalling, USB + 12V, automatic lowering device.
- **Source:** same (V4 S column). **Verbatim:** "SICHERHEITSAUSSTATTUNG :: ... Ducati Vehicle Observer (DVO), Ducati Wheelie Control (DWC) DVO, automatische Reifenkalibirierung, Vehicle hold control", "SERIENAUSSTATTUNG :: Ducati Quick Shift (DQS) up/down 2.0, Ducati Skyhook Suspension, Coming-Home-Funktion, TFT-Farbdisplay, Extended Cylinder Deactivation (ECD), Hands-Free, Voll-LED-Scheinwerfer mit Daytime Running Light (DRL), automatische Blinkerrückstellung, Karten-Navigation, USB-Anschluss, 12V-Steckdose ... Automatic Lowering device".
- **Tier V**
- **Claim:** V4 S marketing/tech section states: **front and rear radar with adaptive cruise control and 3-level Forward Collision Warning** (part of the 2025+ V4 S tech).
- **Source:** same page, tech callout (official CH). **Verbatim:** "RADARTECHNOLOGIE UND VERBESSERTE SICHERHEIT MIT DER FUNKTION FORWARD COLLISION WARNING :: Die Multistrada V4 ist mit modernster Ducati Elektronik ausgestattet. Das Front- und Heckradar und der adaptive Tempomat erhöhen den Fahrspaß, während die neue, in drei Stufen einstellbare Funktion Forward Collision Warning ...".
- **Tier V**
- **Claim (variant note):** V4 S Grand Tour (ab CHF 28'490) is a V4 S-based touring variant in the CH lineup (pannier-ready); no separate spec page was opened this round — treat its specs as V4 S + touring accessories pending its own data page.
- **Source:** ducati.com/ch nav/price cards (official CH, browser).
- **Tier P** (variant identification V; full spec table not read)

## 3. MV Agusta Turismo Veloce 800 — official specs

### 3.0 CH access finding
- **Claim:** mvagusta.com/ch product pages DO work in the browser (round-1 404s were stale/cached fetches); each product page carries a full official spec sheet in the "Tech Specs" modal (`#product-tech-specs-modal`) plus a "Download .PDF" spec reference. CH lineup: Turismo Veloce R (from 13'900 CHF), Lusso SCS (from 18'700 CHF), RC (no CH price card seen).
- **Source:** https://www.mvagusta.com/ch/en/product/turismo-veloce/r and .../lusso-scs (official CH, browser-read live, spec modals read whole).
- **Tier V**

### 3.1 Turismo Veloce R — official spec sheet (CH)
- **Claim:** Engine: 798 cm³ (48.7 cu.in.) inline 3-cylinder, 4-stroke, 12 valves, DOHC w/ mechanical chain tensioner + DLC tappets; bore×stroke 79×54.3 mm; compression 12.3:1.
- **Source:** mvagusta.com/ch R Tech Specs modal (official, read whole).
- **Verbatim:** "Total displacement 798 cm3 (48.7 cu. in.) Compression ratio 12.3:1 ... Bore x stroke 79 mm x 54.3 mm".
- **Tier V**
- **Claim:** Power **81 kW (110 hp) at 11,000 rpm** (at crankshaft); torque **84 Nm (8.57 kgm) at 8,500 rpm**. (Closes round-1 torque gap; confirms round-1 headline "110 HP".)
- **Source:** same. **Verbatim:** "Max. power - rpm (at the crankshaft) 81 kW (110 hp) at 11.000 rpm", "Max. torque - rpm 84 Nm (8.57 kgm) at 8.500 r.p.m".
- **Tier V**
- **Claim:** Weight: **213 kg "in running order (without fuel)"**. Tank **21.5 L**. (Closes round-1 weight + tank gaps.)
- **Source:** same. **Verbatim:** "Mass in running order (without fuel) 213 Kg (469.58 lbs.)", "Fuel tank capacity 21.5 l (5.68 U.S. gal.)".
- **Tier V**
- **Claim:** Performance: max speed 230 km/h (closed course); 0–100 km/h 3.95 s; 0–200 km/h 16.40 s.
- **Source:** same. **Verbatim:** "Maximum speed * 230 km/h (143 mph) ... 0-100 km/h in 3.95 s; 0-200 km/h in 16.40 s".
- **Tier V**
- **Claim:** Chassis: ALS steel tubular trellis frame (MAG welded); front **Marzocchi 43 mm USD** fully adjustable (external rebound/compression + preload), travel 160 mm; rear **Sachs progressive monoshock** fully adjustable, travel 165 mm; wheelbase 1,445 mm; seat 830 mm; trail 108 mm; ground clearance 140 mm.
- **Source:** same. **Verbatim:** "Frame type ALS Steel tubular trellis (MAG welded)", "Front suspension type Marzocchi "UPSIDE DOWN" ... 43 mm ... 160 mm", "Rear suspension type Progressive, Sachs single shock absorber ... 165 mm", "Wheelbase 1.445 mm (56.89 in.)".
- **Tier V**
- **Claim:** Brakes: front double floating Ø320 mm discs, **Brembo radial 4-piston** calipers (Ø32 mm); rear single Ø220 mm disc, **Brembo 2-piston**; **ABS Continental MK100 with RLM (Rear Wheel Lift-up Mitigation) + cornering function**. Tires: 120/70 ZR17 (58W) / 190/55 ZR17 (75W) on 17" alu.
- **Source:** same. **Verbatim:** "Front brake Double floating disc with Ø 320 mm ... Brembo radial-type, with 4 pistons", "ABS System Continental MK100 with RLM (Rear Wheel) Lift-up Mitigation) and with cornering function", "Front tyre 120/70 - ZR 17 M/C (58 W) Rear tyre 190/55 - ZR 17 M/C (75 W)".
- **Tier V**
- **Claim:** Electronics: MVICS 2.1 integrated ignition-injection, Eldor Nemo 2.1 ECU, 47 mm full ride-by-wire Mikuni throttle body w/ pencil coil + ion sensing; torque control (4 maps); **traction control 8 levels with lean-angle sensor (IMU — e-Novia platform per page text)**; **electronic quickshift MV EAS 4.0 up/down**; optional Garmin nav, heated grips, 34 L bags, center stand; exclusive: Bluetooth, cruise control, GPS, adjustable windshield, MV Ride App.
- **Source:** same + page feature text (official CH). **Verbatim:** "Traction Control with eight levels of intervention with lean angle sensor", "Electronic quick-shift MV EAS 4.0 (Electronically Assisted Shift Up & Down)", "The introduction of the IMU inertial platform, developed by e-Novia exclusively for MV Agusta...".
- **Tier V**
- **Claim:** Emissions: Euro 5, combined 5.5 L/100 km, CO2 128 g/km.
- **Source:** same. **Tier V**

### 3.2 Turismo Veloce Lusso SCS — official spec sheet (CH)
- **Claim:** Same 798 cm³ 3-cylinder (81 kW (110 hp) per spec table; hero card on page shows "@ 10.150 R.P.M." — spec table's 11,000 rpm value taken as authoritative); 84 Nm @ 8,500 rpm; **clutch: S.C.S. 3.0 (Smart Clutch System — official definition of "SCS")**; 0–100 3.75 s, 0–200 15.00 s.
- **Source:** mvagusta.com/ch Lusso SCS Tech Specs modal (official, read whole). **Verbatim:** "Clutch S.C.S. 3.0 (Smart Clutch System) Radius CX", "The SCS (Smart Clutch System) significantly improves the riding feeling... the SCS automatically manages the clutch".
- **Tier V** (rpm discrepancy between hero card and spec table noted)
- **Claim:** Suspension: **Sachs 43 mm USD SEMI-ACTIVE fork with MVCSC (MV Agusta Chassis Stability Control)** + **Sachs semi-active monoshock w/ hydraulic preload adjustment, MVCSC**; travel 160/165 mm.
- **Source:** same. **Verbatim:** "Front suspension type Sachs "UPSIDE DOWN" semi-active telescopic hydraulic fork MVCSC (MV Agusta Chassis Stability Control)", "Rear suspension type Progressive, Sachs semi-active single shock absorber ... MVCSC".
- **Tier V**
- **Claim:** Weight: **226 kg "in running order (without fuel)" — 217 kg without side bags** (both figures official). Tank 21.5 L; seat 830 mm; wheelbase 1,445 mm.
- **Source:** same. **Verbatim:** "Mass in running order (without fuel) 226 Kg (498.24 lbs.) - 217 kg (478.40 lbs.) weight without side bags".
- **Tier V**
- **Claim:** Brakes: identical to R (2×320 mm Brembo radial 4-piston front, 220 mm Brembo 2-piston rear, Continental MK100 ABS w/ RLM + cornering). Tires 120/70 ZR17 / 190/55 ZR17.
- **Source:** same. **Tier V**
- **Claim:** Exclusive standard content (Lusso SCS): heated grips, Bluetooth, cruise control, GPS sensor, **center stand**, adjustable windshield, **34 L hard panniers (each)**, MV Ride App, **Mobisat anti-theft system with geolocation**; parking brake integrated in rear hydraulic system; Euro 5, 5.5 L/100 km, 128 g/km.
- **Source:** same. **Verbatim:** "Exclusive content Heated Grips - Bluetooth - Cruise control - GPS sensor - Central stand - Adjustable windshield - Bags 34 l ... - Mobisat anti-theft system with geolocation", "Parking brake Integrated in the rear hydraulic brake system".
- **Tier V**

## 4. Secondary items

### 4a. KTM 1390 Super Duke GT — weight (official confirmation)
- **Claim:** **No official ktm.com spec page with a weight figure exists for the 1390 GT as of 2026-10-21.** Verified absences: (a) ktm.com/de-ch sports-tourer model tree lists only "2026 KTM 890 SMT" and "2024 KTM 1290 Super Duke GT" — no 1390 GT card; (b) ktm.com/de-ch/models/sports-tourer/2025-ktm-1390-superdukegt.html redirects to that segment listing (no model page); (c) ktm.com/en-ch/.../2025-ktm-1390-superdukegt/technical-specifications.html → 404 "We ran out of fuel"; (d) ktm.com/en-us and /en-sg sports-tourer listings likewise show only the 1290 GT + 890 SMT (no 1390 GT); (e) the official MY25 press kit PDF (read whole, ktm.com CH press area) and the international press release (press.ktm.com, read whole) contain **no weight figure**; (f) the CH press page (ktm.com/1390-super-duke-gt-press, round 1, read whole) also has none.
- **Source:** ktm.com/de-ch, /en-us, /en-sg sports-tourer segment pages (official, fetched live) + MY25 press kit PDF + press.ktm.com release (official, read whole).
- **Verbatim:** KTM CH segment listing shows only: "### 2026 KTM 890 SMT — The Long-range Supermoto Weapon" and "### 2024 KTM 1290 Super Duke GT — THE LONG DISTANCE BEAST". 404 page: "OOPS! We ran out of fuel. The page you're looking for is beyond our reach."
- **Consequence:** the **~228 kg (kerb) figure remains Tier P** (secondary: moto-data.net et al. per round 1) — it could NOT be upgraded to V from any official source found.
- **Tier V (the absence is verified); weight value itself stays P**

### 4b. KTM 1390 Super Duke GT — CH price
- **Claim:** **No CH price found as of 2026-10-21.** CH importer portal ktmbikes.ch still down (maintenance, per lane2 live check); CH dealer portal mototech.ch has no 1390 GT page (404, per lane2); CH trade media moto.ch launch article (05.11.2024) states prices were never communicated: "Zu Lieferterminen und Preisen wurde noch nichts kommuniziert." Web search for CH dealer quotes returned only used 1290 GT listings and 1390 Super Duke R (naked) offers — no 1390 GT CH price quote.
- **Source:** moto.ch/neue-ktm-1390-super-duke-gt (CH trade media, read whole) + ktmbikes.ch/mototech.ch status (lane2, live) + web_search (2 queries, no CH price results).
- **Verbatim:** moto.ch: "Zu Lieferterminen und Preisen wurde noch nichts kommuniziert."
- **Tier V (absence verified across the official CH channels + CH media); any specific CHF price = none found**

### 4c. BMW M 1000 RS — CH presence (bmw-motorrad.ch)
- **Claim:** **The M 1000 RS is NOT in the current bmw-motorrad.ch range as of round 2 (2026-10-21).** Verified live: (a) https://www.bmw-motorrad.ch/de/models/m/m1000rs.html returns the 404 "Sackgasse" page; (b) the full live model overview contains the M models **M 1000 RR, M 1000 R, M 1000 XR only** — zero occurrences of "M 1000 RS" in the entire page text. No CH price/announcement exists.
- **Source:** bmw-motorrad.ch/de/models/modeloverview.html + /de/models/m/m1000rs.html (official CH, fetched live in round 2, read whole).
- **Verbatim:** M 1000 variants present in overview: M 1000 RR, M 1000 R, M 1000 XR; "M 1000 RS": 0 matches. Model URL 404: "404 - Sackgasse — Die eingegebene Seite existiert leider nicht".
- **Tier V (absence verified)** — consistent with lane2 (price lane) and the BMW MY2027 press release that does not list an M 1000 RS.

## Searched, found nothing

- **KTM 1390 GT official spec page (weight):** ktm.com/de-ch model tree + /de-ch model URL (redirects to segment), ktm.com/en-ch technical-specifications (404), ktm.com/en-us + /en-sg sports-tourer listings (no 1390 GT), MY25 press kit PDF + international press release + CH press page (read whole; no weight). (source type: official spec pages/press — absent)
- **KTM 1390 GT CH price:** ktmbikes.ch (down/maintenance), mototech.ch (404), web_search "KTM 1390 Super Duke GT Schweiz Preis CHF" and ""1390 Super Duke GT" 2027 Schweiz "ab CHF" OR Preis" (no CH dealer price; only 1290 GT used listings, 1390 R offers, DE spec DBs). (source type: CH importer/dealer portals, web search)
- **BMW M 1000 RS CH page/price:** bmw-motorrad.ch model URL (404), model overview (0 mentions), MY2027 press release (no M 1000 RS — round 1/lane2). (source type: official CH + press)
- **MV Agusta Turismo Veloce "RC" CH price card:** RC appears in the lineup but its CH product page/price was not opened this round (R and Lusso SCS fully sourced). (source type: official CH product page)
- **Ducati V4 S Grand Tour / Rally / Pikes Peak / RS individual spec tables:** only the V4 vs V4 S comparison table was read; other variants share the V4 S platform (Grand Tour = V4 S + touring content) but their own data pages were not opened. (source type: official CH spec pages)
- **Yamaha Tracer 7 GT Y-AMT separate spec:** slug `tracer-7-gt` spec lists both "Standard-6-Gang" (212 kg) and "Y-AMT" (214 kg) weights, so the Y-AMT variant is covered within the same official table. (no gap)

## Completeness summary (this lane)
- **Yamaha Tracer 9 / 9 GT / 9 GT+ (MY2025) / 7 / 7 GT:** full official CH specs (power, torque, kerb weights, tank, brakes, tires, suspension, electronics highlights) — all **Tier V** from the official CH product API + PDPs. Closes round-1 gap (yamaha.ch 404 was a wrong-domain issue; yamaha-motor.eu/ch works).
- **Ducati Multistrada V4 / V4 S:** full official CH spec tables (both columns) — **Tier V**. Closes round-1 gap (no official ducati CH page in round 1). "V4 GT" does not exist as a model.
- **MV Agusta TV 800 (R + Lusso SCS):** full official CH spec sheets (power, torque, weights, tank, brakes, ABS, electronics) — **Tier V**. Closes round-1 gap (subpage 404s resolved via browser).
- **KTM 1390 GT weight:** NOT confirmable from any official source found (verified absence; ~228 kg stays P). **KTM CH price:** none published (verified absence). **BMW M 1000 RS CH:** absent from range (verified absence — a finding in itself).

Sub-question status from this lane's view: answered
