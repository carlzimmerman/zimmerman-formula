# SP3_starting_point: PARTLY as frozen, and only through an on-record fair-share cell that fails tilt, groups and LITTLE THINGS. In the owner's grid (EM1, AM1, E1, C1) no start with the response on reaches Υ's line. Found on the way: UR3's "NFW c 12.95, no response" row used a c over r_vir on R₂₀₀; with the real native shape the weighings want the response on

Criteria: `FROZEN_CRITERIA.md` (b5b6b0a8e5), committed alone first. Briefed as SP1_starting_point; SP1 and SP2 prefixes are taken. `sp3_tables.py`, `sp3_hand.py`, `sp3_hand_tail.py`, `sp3_x.py`, `sp3_native.py`, `sp3_sweep.py`, `sp3_weigh.py`, `sp3_read.py`, `sp3_upsilon.py`, `sp3.out`, `sp3_weigh.out`, `sp3_upsilon.out`, `cells/`. Post-result, no verdict: `sp3_post.py`, `sp3_post.out`. κ = ½ FITTED, unused. No a₀ in the cold sector. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind.** The 0.50-0.80 line is not moved.

## Record check: where each cell was already graded
"Weighing" is DiskMass + Milky Way by UR3's method. Hand core on NR2's η unless stated; native shape reads no η (z = 0 zoom table).

| Cell | SPARC side on record | Weighing on record |
|---|---|---|
| Hand EM1 off | NR2, FG1 C1 | UR3 (NR1 η; same at these masses) |
| Hand EM1 Blumenthal | NR3, FG1 C2 | UR3 |
| Hand E1, C1, off and Blumenthal | RET1 on NR2 | none |
| Hand AM1 off | AM1, older η: rms 0.168 | none |
| Hand AM1 Blumenthal | none | none |
| Native EM1 off | ZN2 A1, OP2: Υ, groups; no tilt, no LITTLE THINGS (OP1 is Local Group) | UR3's c 12.95 stress only, see below |
| Native EM1 measured | OP3: Υ, groups; no tilt, no LITTLE THINGS | UR3's c 12.95 stress only |
| Native AM1 off | ZN2 A1: rms 0.233-0.253 | none |
| Native AM1 measured, E1, C1 both | none | none |

## Grid, canonical, NR2 medians. f_Q 0.872 on native, Blumenthal on hand
Pairs are backgrounds A/B, tilt and LT to A here (both in `sp3.out`). r target 0.90-1.10, n ≥ 27. MW: PRIORS, WIDE, V+K, INF.

| Cell | Υ | rms | tilt | groups | LT | r (n) | MW (cells) | Υ by V_flat, 150-200, 200-250 | Fails |
|---|---|---|---|---|---|---|---|---|---|
| hand EM1 off | 0.75/0.76 | 0.069 | +0.59 | +1.47 | +0.153 | 1.365 (30) | WIDE 1 | 0.57 0.62 | tilt, LT, DM, MW |
| hand EM1 Blum | 0.35/0.36 | 0.067 | +0.17 | +1.50 | +0.116 | 1.071 (28) | V+K 0 | 0.30 0.36 | line, tilt, LT, MW |
| hand E1 off | 0.67/0.68 | 0.090 | +0.49 | +0.42 | −0.030 | 1.370 | V+K 0 | 0.57 0.59 | tilt, DM, MW |
| hand E1 Blum | 0.30/0.30 | 0.103 | +0.01 | +0.46 | −0.123 | 1.051 | INF | 0.30 0.33 | line, LT, MW |
| hand C1 off | 0.67/0.68 | 0.088 | +0.51 | +0.41 | +0.069 | 1.370 | V+K 0 | 0.57 0.59 | tilt, DM, MW |
| hand C1 Blum | 0.30/0.30 | 0.100 | +0.01 | +0.46 | −0.017 | 1.051 | INF | 0.30 0.33 | line, MW |
| hand AM1 off | 0.65/0.68 | **0.196** | +0.47 | **−16.5** | −0.119 | 1.380 | V+K 0 | 0.51 0.59 | line (rms), tilt, groups, DM, MW, LT |
| hand AM1 Blum | 0.30/0.30 | **0.223** | 0 | **−16.5** | −0.186 | 1.033 | INF | 0.30 0.30 | line, groups, LT, MW |
| native tot EM1 off | 0.84/0.81 | 0.083 | +0.55 | +2.08 | +0.304 | 1.282 | V+K 0 | 0.57 0.67 | all |
| **native tot EM1 f_Q** | 0.44/0.41 | 0.073 | +0.29 | +2.08 | +0.236 | **1.080** | **PRIORS 11** | 0.32 0.40 | line, tilt, groups, LT |
| native FC1 EM1 off | 0.75/0.69 | 0.078 | +0.58 | +1.91 | +0.283 | 1.260 | V+K 0 | 0.52 0.62 | tilt, LT, DM, MW |
| **native FC1 EM1 f_Q** | 0.39/0.37 | 0.071 | +0.20 | +1.91 | +0.219 | **1.052** | **PRIORS 9** | 0.30 0.38 | line, tilt, LT |
| native tot E1 off | 0.48/0.48 | 0.065 | −0.24 | +1.13 | +0.005 | 1.238 | WIDE 8 | 0.48 0.58 | line, tilt, DM, MW |
| native tot E1 f_Q | 0.30/0.30 | 0.071 | −0.01 | +1.13 | −0.051 | 1.027 | WIDE 2 | 0.30 0.35 | line, MW |
| native FC1 E1 off | 0.40/0.37 | 0.066 | −0.22 | +0.94 | −0.020 | 1.209 | PRIORS 15 | 0.45 0.56 | line, tilt, DM |
| native FC1 E1 f_Q | 0.30/0.30 | 0.078 | 0 | +0.94 | −0.080 | 1.002 | V+K 0 | 0.30 0.33 | line, MW |
| **native tot C1 off** | **0.54/0.53** | **0.065** | **+0.15/+0.10** | +1.12 | +0.164 | 1.238 | WIDE 8 | 0.48 0.58 | LT, DM, MW |
| native tot C1 f_Q | 0.30/0.30 | 0.069 | −0.01 | +1.12 | +0.073 | 1.027 | WIDE 2 | 0.30 0.35 | line, MW |
| native FC1 C1 off | 0.46/0.45 | 0.064 | −0.02 | +0.92 | +0.135 | 1.209 | PRIORS 15 | 0.45 0.56 | line, LT, DM |
| native FC1 C1 f_Q | 0.30/0.30 | 0.074 | 0 | +0.92 | +0.050 | 1.002 | V+K 0 | 0.30 0.33 | line, MW |
| native AM1, all four | 0.30/0.30 | 0.233-0.284 | ≈0 | −15.6 to −15.8 | −0.17 to −0.22 | n 21-24, under 27 | V+K, INF | 0.30 0.30 | line, groups, LT, DM, MW |

Extra row, fair share (no fitted number, no SN input); hand rows on record in Υ:
| Cell | Υ | rms | tilt | groups | LT | r | MW | Fails |
|---|---|---|---|---|---|---|---|---|
| hand FAIR200 Blum | 0.74/0.74 | 0.093 | +0.75 | +3.79 | +0.427 | 1.106 | PRIORS 5 | tilt, groups, LT, DM |
| native tot, FC1 FAIR200 f_Q | 0.92/0.91, 0.87/0.86 | 0.119, 0.115 | +0.65, +0.67 | +4.27, +4.13 | +0.517, +0.504 | 1.160, 1.144 | V+K | everything |

**Verdict, frozen rule: PARTLY.** Its only trigger is hand FAIR200 + Blumenthal, an on-record cell, reaching Υ's line by putting dwarfs at the cap (1.20) and failing tilt, groups, LITTLE THINGS. Inside the owner's four mass rules, **no cell with the response on reaches the line, and no cell at all clears all galaxy gates.** I'd read that as NOT THE START for what the owner asked; the frozen label stands as written, and my clause was too loose. No cell triggered the cluster addendum. Keys on measured gas stay failed: EM1 line 14 of 15 at best (OP2), E1 and C1 tend to fair share at clusters (RET1), native + response on clusters is still ungraded. RET1's blue lensing still counts against E1, C1: +0.27 against blue's upper +0.14.

My expectation: NOT THE START 70 %, PARTLY 25 %. PARTLY came by the route I named, and it's a technicality.

## What the start does and doesn't do
- **Υ:** a heavier or cuspier start lowers it with the response on, as UR2's arithmetic says. Every no-fit rule but fair share is heavier than EM1. So no start in reach takes the response's Υ back up.
- **Tilt: this is new.** With the native shape and C1, off, frozen map, Υ 0.54/0.53, tilt +0.15/+0.10, rms 0.065, groups +1.12. NR3 and RM1 had every Υ ≥ 0.50 cell at tilt ≥ +0.32, so this is the first row on record clearing line and tilt with no η and no fitted efficiency. It's not a pass: LT +0.164, DiskMass 1.238, MW wide priors only, tilt sits on the line, it's [MAP-DEPENDENT] (FC1 map Υ 0.46), its response is off, C1's ε = 1 ceiling isn't physical and it runs above blue lensing.
- **With the response on, C1 and E1 native clear everything but Υ and MW:** tilt ≈ 0, groups about +1, LT inside line on C1, DiskMass 1.00-1.03. But Υ is at the grid floor 0.30 in almost every bin, so it's censored, dwarfs included. That isn't "near" the line.

## UR3's c 12.95 row is a definition error, and it changes the lead
UR3's stress applied LC1's c_nfw 12.95 as c on R₂₀₀. X48's c_nfw is over r_vir. ZN1's table has both on the same halos: c₂₀₀ 5.94 against c_nfw 10.35 at 10¹⁴, 6.47 against 12.20 at 10¹³, ratio 1.74-1.89. ZN2's z = 0 table at 10¹² fits c₂₀₀ 7.8, and 12.95/1.8 is 7.2. M(<R₀) for the Milky Way on EM1: **2.07-2.26e10 native, not 3.84e10.** The smooth core is 1.47e10, so the "× 2.7" in UR3, TP1, MH1 is about × 1.5. Post-result rows (`sp3_post.out`):

| EM1, NFW on R₂₀₀ | r (n) | MW |
|---|---|---|
| c 12.95 off (UR3's row, reproduced) | 1.090 (26) | PRIORS 16 |
| c 12.95 f_Q | 1.003 (23) | INFEASIBLE |
| **c 7.8 off** | **1.266 (29)** | **V+K 0** |
| **c 7.8 f_Q** | **1.053 (28)** | **PRIORS 10** |
| c 6.9 off | 1.291 (30) | V+K 0 |
| c 6.9 f_Q | 1.088 (28) | PRIORS 12 |
| hand core, f_Q 0.872 | 1.088 (29) | PRIORS 5 |

So UR3's readings 1 and 2 reverse on the native start. "NFW + none passes, zoom + measured response overshoots" isn't what the zoom's shape does. **Zoom shape with no response fails both weighings. Zoom shape + LC1's measured response passes both, with no fitted number but EM1's line.** On EM1 the weighings want the response, whichever start. Holds under stress: f_Q 0.54 to 1.07, M_b in the response × 0.7 to 1.15, all in priors but FC1 f_Q 1.07 (wide). In-prior cells at R_d 2.6, M★ 4.9-5.7e10. Hand core at f_Q 0.872 passes too, so **it's the response's amount more than the start.** UR3's Blumenthal missing MW was f = 1 against 0.872.

**Same fragility as UR3:** CFG577's Jeans integral raises r 5-7 %, so 1.080 → about 1.14, 1.052 → about 1.11, outside. A young-tracer σ_z systematic pulls the other way. Two of 30 unfittable. EM1 is still fitted, and matched to the law. It isn't a pass of G5: McMillan's own row misses, V_c 243, K_z 79.

## The refit, FITTED, not a pass
EM1 + δ, native, f_Q 0.872, Υ 0.50 on both: **frozen map δ −0.094, inside blue's (−0.10, +0.14) at its edge; FC1 map δ −0.150, PINCHED.** UR2 had −0.30 on the hand core, so the native shape cuts the pinch by half to two thirds. [MAP-DEPENDENT]. And it costs the rest: tilt +0.55, groups +2.93, +3.28 ABOVE LAW, LT +0.27, rms 0.081. Trough still 0.39, 0.44. **It also loses both weighings:** r 1.109, 1.102, MW wide priors 1 cell, V+K 0. BL1's range was measured on FC1's core, so it's read across, and BL1's shape misfit stands.

## Is the trough about halos at all?
- **Inclination (S4, TP1 hadn't tested it):** partial ρ +0.069 (p 0.55) off, −0.001 (p 0.995) Blumenthal, n 76. e_i moves V² by a median 5 %, coherent 1σ. No.
- **Stellar population (S2):** Υ_W1 at i ≥ 45°, about 15,500 ALFALFA-SDSS galaxies, SPARC-independent:

| V km/s | 60-100 | 100-150 | 150-200 | 200-250 | 250-400 |
|---|---|---|---|---|---|
| GSWLC SED | 0.277 | 0.304 | 0.374 | 0.460 | 0.505 |
| Taylor g-i | 0.231 | 0.231 | 0.247 | 0.277 | 0.326 |

  **Both rise monotonically: no trough.** So stars don't make one at 150-250, on these estimators. That trend is the opposite sense to the off rows' fitted 1.20 → 0.57, and would read as tilt about −0.1 to −0.2 on the record's statistic. ET3, ET4 tested S_need's low-mass rise, not this, and don't address the trough.
- **Reading, judgment:** the trough is not explained by Υ's population trend or inclination. TP1 has no predictor. It remains a feature of fits at fixed halo rule, or of distance, gas, non-circular motion or bars, with bars untested on the full sample. No test here isolates halo as the cause.

## Does 0.30-0.40 break anything independently of the line?
**S2's frozen reading at 150-250: NOT BROKEN.** Medians 0.401 GSWLC [0.284, 0.529], 0.259 Taylor [0.196, 0.334]. By bin GSWLC reads 0.374, 0.460, so 0.30-0.36 at 150-250 is low on GSWLC and high on Taylor. Those two differ by 0.2 dex, so population modelling does not pin this to better than that. These are models with an IMF, W1 stands in for 3.6 μm, not corrected, and the W1 luminosity's own calibration is not independently checked.
- DiskMass, read from h120: Υ_K 0.31 ± 0.07 against populations 0.6 ± 0.1. With h120's bracket K/3.6 of 1.0-1.3, 0.24-0.31 at 3.6 μm. UR3's own fit here Υ_K 0.26-0.29. Young-tracer σ_z systematic open.
- Milky Way: in-prior cells at star-count M★ about 5e10; no 3.6 μm luminosity on disk, so it isn't a Υ_3.6.
- Nothing on disk that I found breaks 0.30-0.40 at 150-250 km/s. Grid floor stands: below 0.30 is censored, and the 0.30 readings there may be lower, which would break it on GSWLC.
- **S3 (same galaxies) FAILS its sanity, no read:** McGaugh-column Υ on SPARC's L is 0.05-0.28, when it should be near 0.45: unWISE photometry on nearby extended UGC galaxies comes up short by × 2-4. n 5 at 150-250 anyway.

## Where the 0.50 line comes from
- First stated in `campaign_fresh_gravity/CFG4_galaxy_law.py`, H2 "[HEADLINE] THE LAW FITS", 2026-09-27 (3409d12da0): rms ≤ 0.110 at Υ_disk inside 0.50-0.80, "EXPECT TRUE", on the a₀ law. The law's fit there is 0.57-0.70. Later lanes inherit it as "CFG4 H2 C2", then route E gets graded on it.
- **The lower edge is the population central value, not a limit below it:** CFG4's README calls Υ = 0.50 the 3.6 μm prior, AG4b traces it to Schombert & McGaugh 2014 and Lelli+ 2016's convention. The record's own anchors carry widths: 0.5 ± 0.1 (h120), 0.10 dex (CFG4, per-galaxy, so not directly a width on a sample median). I found no derivation of 0.80 and no statement of why 0.50 has no margin below.
- **So it isn't a measurement.** It's a one-sided band, centred upward from a model prior, written for the law. The law on the alt footing fails it too (0.44).
- **Evidence the line is part of the problem, not all of it:** on-disk stellar masses and DiskMass allow 0.25-0.46 at these V_flat, and Milky Way and DiskMass both accept a response that requires Υ near 0.3-0.4. **Against it being the whole problem:** no cell fails on the line alone. Native EM1 f_Q keeps tilt +0.20 to +0.29, LT +0.22, and C1, E1 native sit at the floor and miss MW. The line isn't moved here, and no verdict uses a changed line. Changing it is the owner's decision.

## Judgments, mine, not measurements
- A start from what's measured with no fitted number removes the response's Υ problem while clearing all galaxy gates: under 5 %.
- MH1's "the ask comes from the start", about 50 %: I'd lower it to about 15 %. The start can move tilt, and it can't raise Υ with the response on. Its correct half: UR3's reading rested on the mis-set c.
- The response should stay on near f_Q 0.87 at L★ and SPARC's 0.50 lower edge is too high for a sample median: about 45 %, held down by DiskMass's open σ_z, by CFG577's 5-7 %, and by SPS's own 0.50.
- A real process undoing contraction at L★ is still missing: about 25 %, down from MH1's implied 50 %, on the weighings' reversal.

## Not done or weak
EM1 is fitted in every EM1 row. Clusters aren't graded under native + response. KiDS and Local Group not run on new cells. E1 and C1 carried to native with V_esc from the hand core. LITTLE THINGS on native clamps shapes below 10¹⁰ (self-similar per OP1). Native table is ng 64 at 10¹², not ng 80, and η's NR2 medians don't enter it. Seeds not bootstrapped here. UR3, TP1, MH1 aren't edited; they carry the c error until someone with those lanes fixes it forward.

## Checks
K1 EM1 off vs NR2 MEDIAN 0, Blumenthal vs NR3 MEDIAN 0. K2 native EM1 vs OP3 0. K3 interpolated E1, C1 vs RET1: dΥ 0, d rms 0.0003. K4 UR3's own 1.365, 1.071, 1.090 asserted. K5 AM1 native off rms 0.233, 0.253, ZN2's range. K6 η(10¹²) 21.531. MUTATE M_b × 2 in native response ΔΥ 0.11; halo × 2 r 1.282 → 1.235. All pass. **My code error, fixed before reading:** K5 was written with a stray `or True` in the reader, removed; it passes strict. Generated logs dropped from the commit.

κ = ½ FITTED. Not theory closed.
