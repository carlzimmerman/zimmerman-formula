# ND1_native_dwarfs: ARGON'S LINES FAIL on LITTLE THINGS. Native N passes SPARC's line and the gas-rich offset, stays tilted in surface brightness, and on the ceilings the measured cusp clears only the ultra-faints, almost all of them inside 3ε

Criteria: `FROZEN_CRITERIA.md` (9230f53a67), committed alone before any number. Scripts `nd1_ab.py`, `nd1_shapes.py`, `nd1_ceiling.py`. Outputs `nd1_ab.out`, `nd1_shapes.out`, `nd1_ceiling.out`, their JSON, `nd1_systems.csv` (per system, with the 3ε flags), `*_MUTATE.*`. κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

## Frozen verdicts
- **Argon's lines: ARGON'S LINES FAIL: LITTLE THINGS median E.** No noise or background flag. The LITTLE THINGS failure held in all 200 draws of X80's seeds. The lowest draw was +0.129.
- **HS1 slope: TILTED −.** b −0.173 ± 0.064 per dex (−2.70σ) on A, −0.171 ± 0.064 on B. The law's FLAT is on record.
- **Core, free M200:** ultra-faints NO M200 RESCUES (Z_C +5.02), J0946 EXCEEDS at both radii (R 152 / 46), Draco +0.838, above by more than 2 s. Each class held in all 200 draws.
- **Cusp, lg M200 9, M ∝ r² inside 3ε: SOME CLEAR: ultra-faints [INSIDE 3 EPS].** Draco +0.541, J0946 R 80 / 48. J0946 doesn't reach R ≤ 2 at any tag up to 10¹⁴, on any reading.
- **z = 0 was not graded.** ZN2's low-mass runs had 0 of 9 seeds finished at both masses, and hadn't started. Everything in part C is z_f.

## Part A: SPARC
Native N: ρ₁₀ 1.128, ρ₁₁ 0.938, CE1's A4 η. Below, A / B are the backgrounds. The other rules are the record on A; `nd1_ab.out` has them on B.

| Rule | Υ (A/B) | rms free Υ (A/B) | offset gas ≥ 0.5 (81) | offset gas ≥ 0.7 (41) | LITTLE THINGS median E | Argon's three lines |
|---|---|---|---|---|---|---|
| **Native N** | **0.70 / 0.72** | **0.0682 / 0.0694** | **+0.035 / +0.034** | **+0.007 / +0.007** | **+0.138 / +0.132** | **fails LITTLE THINGS** |
| F canonical | 0.51 / 0.50 | 0.0687 / 0.0700 | −0.039 | −0.110 | −0.041 | fails offset |
| F alt | 0.44 / 0.44 | 0.0719 | −0.073 | −0.146 | −0.055 | fails SPARC, offset |
| N0 | 0.71 / 0.73 | 0.0678 / 0.0688 | +0.036 | +0.016 | +0.158 | fails LITTLE THINGS |
| N1 | 0.55 / 0.56 | 0.0670 / 0.0681 | −0.017 | −0.060 | +0.078 | passes |
| N2 | 0.47 / 0.48 | 0.0695 / 0.0706 | −0.056 | −0.114 | −0.026 | fails SPARC, offset |

**68 % from X80's seeds:** Υ [0.61, 0.81] on A; offset gas ≥ 0.7 [−0.016, +0.058]; gas ≥ 0.5 [+0.010, +0.066]; LITTLE THINGS [+0.137, +0.233]. The central LITTLE THINGS value sits at the low edge because η₁₀'s median, 29.26, is near the top of its own bootstrap. Outcomes held: SPARC line 0.83 / 0.79, offset 0.94 / 0.94, LITTLE THINGS 1.00 / 1.00.

**The offset pass is weak.** It's a mean over a split population. On gas ≥ 0.7, 49 % of galaxies pin at the top of the Υ grid and 32 % at the bottom. Scatter is 0.150 at free Υ and 0.171 at Υ 0.50, where the law has 0.125 and 0.156.

**By V_flat, `sel`'s bins, Υ 0.50 (A; B within about 0.03 in Υ and 0.7 km/s):**
| V_flat | n | lg M200 | S_rule | ET1 [95 %] | Υ | ΔV km/s |
|---|---|---|---|---|---|---|
| 20–60 | 13 | 9.97 | 53 | 69 [52, 85] | 1.20 | −4.3 |
| 60–100 | 35 | 10.59 | 69 | 103 [81, 124] | 1.14 | −6.6 |
| 100–150 | 23 | 11.13 | 90 | 143 [118, 200] | 0.86 | −12.1 |
| 150–200 | 25 | 11.76 | 134 | 150 [98, 190] | 0.54 | −4.2 |
| 200–250 | 18 | 12.11 | 162 | 215 [137, 272] | 0.58 | −13.9 |
| 250–400 | 10 | 12.27 | 175 | 412 [182, 596] | 0.74 | −54.7 |

**Offset at Υ 0.50, all galaxies in the bin (A / B):** 20–60 +0.038 / +0.040; 60–100 +0.054 / +0.056; 100–150 +0.082 / +0.081; 150–200 +0.012 / +0.014; 200–250 +0.048 / +0.048; 250–400 +0.123 / +0.124.

**HS1:** same as N0's −0.173 within rounding, against N1's −0.227 and the law's −0.016. 68 % from the seeds [−0.203, −0.141], tilted at the central σ in 91 % of draws. A higher native S doesn't help: N1 and F tilt more.

## Part B: LITTLE THINGS (RT1's recipe, 20 galaxies; negative E is over-predicted)
| | Native N, A | Native N, B | N0 | N1 | F canonical | law canonical |
|---|---|---|---|---|---|---|
| median E | **+0.138** | +0.132 | +0.158 | +0.078 | −0.041 | −0.025 |
| 16–84 % | −0.043, +0.467 | −0.048, +0.466 | −0.035, +0.495 | −0.098, +0.370 | −0.253, +0.260 | −0.176, +0.321 |
| rms | 0.396 | 0.396 | 0.408 | 0.365 | 0.353 | 0.345 |
| IC 1613, E (Z) | −0.474 (−6.3) | −0.477 (−6.4) | −0.449 (−6.0) | −0.553 (−7.4) | −0.644 (−8.6) | −0.593 (−7.9) |
| WLM | +0.191 (+2.5) | +0.187 (+2.5) | +0.214 (+2.9) | +0.118 (+1.6) | +0.035 (+0.5) | +0.079 (+1.0) |
| DDO 210 | +0.325 (+4.3) | +0.333 (+4.4) | +0.359 (+4.8) | +0.106 (+1.4) | −0.182 (−2.4) | −0.077 (−1.0) |
| DDO 216 | +0.036 (+0.5) | +0.039 (+0.5) | +0.069 (+0.9) | −0.098 (−1.3) | −0.256 (−3.4) | −0.178 (−2.4) |

So native N stays close to N0, short of this sample, and IC 1613 still fails on it, by over-prediction. N1 passes the line, but its S at lg M200 9 is 48.6 against the measured rule's 29.4, 1.66 times higher. 16 of the 20 galaxies are below X80's lowest zoom, where ρ is held at ρ₁₀.

## Part C: ceilings
**A correction first.** The rule's halo is the smooth core, whose own bound is M₃D(<r) ≤ 2.1907 S r². The 1.599 in PC1, in the brief and in the earlier Argon check is Burkert's. So:
- The earlier check's gain, +0.36 to +0.43 dex, is against Burkert's bound. Against the smooth core's own it's +0.22 to +0.29 dex, on exact NFW.
- PC1 stands as frozen for Burkert. With the floor's S on the smooth core's bound, Draco falls from +0.148 to +0.015 canonical (−0.066 alt), no longer above by 2 s, and J0946's R from 31.2 to 22.8 (18.8 alt), still EXCEEDS.

**What the zooms measure (z_f, ng 64, cold share; rule's S at that M_t):**
| Tag | 3ε (pc) | n(<3ε) | c_nfw | ρ_s r_s / S | M/r² at 3ε | limit 2πρ_s r_s | rule S | over 2.19 S: at 3ε, limit | slope 3–6ε (NFW) |
|---|---|---|---|---|---|---|---|---|---|
| 10¹⁰ | 714 | 244 | 8.55 | 0.612 | 118 | 177 | 51.8 | 1.03, 1.56 | 1.65 (1.64) |
| 10¹¹ | 1674 | 247 | 7.35 | 0.596 | 216 | 319 | 78.4 | 1.26, 1.86 | 1.63 (1.68) |
| 10¹² | 3964 | 217 | 7.75 | 0.601 | 339 | 568 | 149 | 1.04, 1.74 | 1.78 (1.66) |
| 10¹³ | 9483 | 204 | 7.15 | 0.593 | 558 | 868 | 236 | 1.08, 1.68 | 1.74 (1.68) |
| 10¹⁴ | 22905 | 207 | 6.80 | 0.590 | 968 | 1293 | 380 | 1.16, 1.55 | 1.79 (1.67) |

So what's measured at 3ε barely exceeds the smooth core's bound at that S. Only continuing NFW to r = 0 gives up to × 1.9. And M/r² at fixed r rose at every step with mass, on every reading, so a cusp has no ceiling over M200. It has one only at a stated mass, which is why a reference mass is used.

**E_C (Z_C) by class, Draco, J0946's R at 0.3 / 0.6 kpc:**
| Reading | MW ultra-faint (31) | bright M31 (25) | M31 others (5) | MW classical (8) | LG field (13) | Draco | J0946 R |
|---|---|---|---|---|---|---|---|
| Floor, Burkert (PC1), canonical | −0.275 (−2.49) | −0.390 (−2.58) | +0.001 (0.00) | −0.036 (−0.42) | −0.149 (−2.12) | +0.148 | 31.2 / 15.6 |
| Floor, Burkert (PC1), alt | −0.357 (−3.24) | −0.471 (−3.11) | −0.081 (−0.25) | −0.109 (−1.26) | −0.230 (−3.21) | +0.068 | 25.8 / 12.9 |
| Floor, smooth bound, canonical | −0.411 (−3.73) | −0.526 (−3.46) | −0.136 (−0.42) | −0.158 (−1.82) | −0.284 (−3.94) | +0.015 | 22.8 / 11.4 |
| N1, lg 9, Burkert bound (brief's) | +0.065 (+0.59) | −0.052 (−0.35) | +0.342 (+1.06) | +0.251 (+2.79) | +0.150 (+2.30) | +0.477 | 68.6 / 34.3 |
| Native, lg 9, smooth bound | +0.147 (+1.33) | +0.028 (+0.19) | +0.423 (+1.31) | +0.307 (+3.33) | +0.224 (+3.48) | +0.555 | 82.9 / 41.5 |
| Native, lg 9, the halo's own r₀ (992 pc) | +0.845 (+6.20) | +0.183 (+1.19) | +0.811 (+2.43) | +0.470 (+3.25) | +0.278 (+3.44) | +0.853 | 155 / 47.7 |
| **Native core, free M200 (PRIMARY)** | **+0.554 (+5.02)** | **+0.167 (+0.97)** | **+0.784 (+2.43)** | **+0.465 (+3.14)** | **+0.274 (+2.76)** | **+0.838** | **152 / 46.0** |
| Native core, free M200, background B | +0.569 (+5.17) | +0.187 (+1.09) | +0.806 (+2.51) | +0.476 (+3.20) | +0.284 (+2.86) | +0.857 | 160 / 48.2 |
| **Cusp, lg 9, M ∝ r² (PRIMARY)** | **+0.132 (+1.20)** | **+0.014 (+0.11)** | **+0.409 (+1.27)** | **+0.297 (+4.23)** | **+0.237 (+3.03)** | **+0.541** | **80.1 / 48.2** |
| Cusp, lg 9, NFW fit at r | −0.020 (−0.18) | −0.015 (−0.12) | +0.336 (+1.05) | +0.271 (+4.40) | +0.179 (+2.30) | +0.487 | 73.3 / 48.2 |
| Cusp, lg 9, limit | −0.045 (−0.40) | −0.161 (−1.07) | +0.232 (+0.72) | +0.162 (+1.84) | +0.052 (+0.77) | +0.372 | 53.2 / 26.6 |
| Cusp at the 10¹⁰ tag, M ∝ r² | −0.113 (−1.03) | −0.229 (−1.61) | +0.163 (+0.50) | +0.104 (+1.27) | +0.002 (+0.02) | +0.306 | 45.4 / 22.7 |
| Cusp at the 10¹¹ tag, M ∝ r² | −0.377 (−3.42) | −0.492 (−3.25) | −0.101 (−0.31) | −0.128 (−1.47) | −0.250 (−3.42) | +0.048 | 24.6 / 12.3 |
| Cusp at the 10¹⁴ tag, limit | −1.153 (−10.44) | −1.265 (−8.28) | −0.877 (−2.71) | −0.866 (−9.61) | −1.021 (−13.32) | −0.721 | 4.1 / 2.1 |

N has no a₀, so its E_C has no footing; alt's row differs only in the Monte Carlo s (`nd1_ceiling.out`). The frozen labels name Draco, J0946 and the ultra-faints, but the classical dwarfs and LG field are above the primary cusp at lg 9 too.

**Where the half-light radius lies below 3ε (a continuation, not a measurement):**
| Mass used | 3ε | ultra-faint | bright M31 | M31 others | classical | LG field | Draco | J0946 0.3 / 0.6 |
|---|---|---|---|---|---|---|---|---|
| lg M200 9, scaled | 327 pc | 30/31 | 7/25 | 5/5 | 4/8 | 4/13 | yes | yes / no |
| 10¹⁰ tag | 714 pc | 31/31 | 17/25 | 5/5 | 7/8 | 8/13 | yes | yes / yes |
| 10¹¹ tag | 1674 pc | 31/31 | 24/25 | 5/5 | 8/8 | 11/13 | yes | yes / yes |

Even "lg 9, measured" rests on scaling the 10¹⁰ zoom down self-similarly. No zoom exists there.

**M200 needed by the cusp (lg, median; × over EM1's relation):**
| Reading | ultra-faint | bright M31 | M31 others | classical | LG field | Draco | J0946 |
|---|---|---|---|---|---|---|---|
| M ∝ r² | 9.50, ×3087 | 9.06, ×25 | 10.54, ×15760 | 10.37, ×222 | 9.94, ×23 | 11.18, ×6347 | not reached at 10¹⁴ |
| NFW fit | 8.94, ×1022 | 9.00, ×25 | 10.06, ×5219 | 9.97, ×107 | 9.68, ×23 | 10.62, ×1748 | not reached |
| limit | 8.84, ×707 | 8.40, ×5 | 9.88, ×3448 | 9.71, ×46 | 9.28, ×5 | 10.46, ×1209 | not reached |

Most of these lie inside 3ε at that mass, and Draco's do on all three. The core on the rule can't reach most at any M200: 3 of 31 ultra-faints, 10 of 25 bright M31, 0 of 5, 0 of 8, 2 of 13, Draco not.

## Argon's cusp claim, rechecked
**Draco on N1 (S 48.6, lg M200 9):**
| Reading | E |
|---|---|
| Brief's Burkert bound (by hand +0.49) | +0.477 |
| Smooth core's own bound | +0.347 |
| Argon's form, 2π S r² (it said −0.104) | −0.099 |
| Earlier check's c 15, ratio 0.660 (it said +0.076) | +0.079 |
| c equivalent to N1's η, 12.5, ratio 0.645 | +0.088 |
| **Measured ratio at 10¹⁰, 0.612 (score's basis)** | **+0.111** |
| c equivalent, at Draco's actual radius (y 0.296, × 0.705) | +0.236 |

**J0946 at 0.3 kpc:** Argon's form at the floor's S gives 7.9, as it said. With the measured ratio, 13.0 (score's basis). The earlier check's c 15 recomputes to 12.0. But R 31 and these all use the floor's S, which version N doesn't have: N1's S gives 28.5, native N's 47.2, and the measured primary reading 80.1.

**What changed from the earlier check.** Its arithmetic holds, and three of its inputs don't: the zooms give c 8.55 at 10¹⁰, not 15; the limit overstates the mass at Draco's real radius; and the gain was quoted against Burkert's bound. Draco is not marginal on N1 once the radius is used. It's +0.11 to +0.24.

## Argon's lines scored
| Line | Set | Measured | Result |
|---|---|---|---|
| ρ₁₀ window | pass 1.15–1.85, fail below 1.10 or above 1.90 | 1.128 [0.967, 1.301] | neither |
| SPARC line, both backgrounds | rms ≤ 0.110, Υ 0.50–0.80 | Υ 0.70 / 0.72, rms 0.0682 / 0.0694 | pass |
| Gas ≥ 0.7 offset, Υ 0.50 | \|Δ\| ≤ 0.07 | +0.007 / +0.007 | pass |
| LITTLE THINGS median | \|E\| ≤ 0.10 | +0.138 / +0.132 | **FAIL** |
| Draco, native cusp on N1 | −0.104 ± 0.05 | +0.111 | **MISS** |
| J0946, R 31 falls to | 7.9 ± 15 % | 13.0 | **MISS** |

Its diagnosis is half right: the floor does fail the offset line (−0.110) and version N doesn't. N1 passes all three of its lines, but N1's slope isn't what the zooms measured.

**My expectation on record:** offset near 0, hit. LITTLE THINGS near +0.13 and narrow, hit in value, wrong to think it might be noise-limited. HS1 near −0.18, hit. S near 29, hit. Ultra-faints NO M200 RESCUES, J0946 EXCEEDS, ultra-faints admitted mostly inside 3ε, all hit. Draco around +0.3 on the cusp: miss, +0.541. I'd used the limit and not the measured mass.

## How this reads
The measured collapse S at dwarf masses is short in two separate places. LITTLE THINGS wants more acceleration at R_max. The dwarfs' central masses want far more inside r₁₂ than a core on this S can hold, and a cusp only reaches them at M200 hundreds to thousands of times above EM1's relation. J0946's dark solution fails under every reading here, so route E still needs its luminous solution. This doesn't decide version N against the floor: the floor fails the gas-rich offset and passes LITTLE THINGS, the reverse. a₀ out of the cold sector stays the owner's call.

## Checks
All pass.
- **K1** ρ = 1, pre-A4 table, against N0's record in four files: |d| 0.
- **K2** N1's slope against N1's record: |d| 0.
- **K3** native N against `nf1_native_read.json`: bins 0, grader-path rms 2.6e-6, Υ 0.
- **K4** floor's S with Burkert against PC1: 0; Draco 0.0005. **K4b** (added) S at lg 9 against NF1: 3.6e-15.
- **K5** zoom path against X80's c_nfw and η: 0, 18 runs; ZN1's sampled NFW passes; r_f 0.
- **K6** free-M200 path returns 1.599 S r²: 5.5e-5. **K7** exact NFW against `argon_check.out`: 4.4e-3.
- **MUTATE** S × 0.5, r × 1.5: Υ 0.70 / 0.72 → 1.20 / 1.20, offset +0.177, LITTLE THINGS +0.158, bound halves exactly, ultra-faint Z_C +5.02 → +8.34, cusp median E +0.340. BITES.
- **Side effects:** no file changed in the lanes this reads, checked by modification time. The loader's X74 by-products landed here and were removed.

Added after the criteria, reported only, no verdict depends on them: K4b, the NFW-fit row at the tags, `nd1_systems.csv`, the normalisation diagnostics below. The scripts' `--nodraws` flag was used for a first run of the checks.

## Limits
1. **Nothing below 10¹⁰ is measured.** ρ is held there: 13 of 41 gas ≥ 0.7 galaxies, 16 of 20 LITTLE THINGS on A, and every dwarf's own EM1 mass. The shape is scaled from one zoom mass.
2. **The radii that matter aren't resolved.** See the 3ε table. M(<3ε) also lies 3–16 % below each seed's own NFW fit, depending on tag.
3. **Primary is the low reading.** M ∝ r² is below NFW's continuation. The limit is an upper reading, and it depends on the fit: at 10¹² it's 395 at z = 0 and 568 at z_f, on nearly the same inner mass (320, 339).
4. **Normalisation.** The zoom's own η 3M_vir/(4πr_vir²) f_c is 0.89 of the rule's S at 10¹⁰, 1.05 at 10¹¹. That's why rule-based and measured readings differ, such as J0946's 47.2 and 53.2.
5. **Σ_coll is held below lg M_t 7.301,** where its table ends. This favours the rule. The free-M200 peak falls there for 25 systems. No SPARC or LITTLE THINGS galaxy reaches it.
6. **Ratios are noise-limited.** η₁₀ and η₁₁ come from nine seeds each, and their bootstrap is lumpy.
7. **No baryons in the zooms,** so no stripping, heating or contraction. LC1 measures contraction. Stripping and heating would lower these masses. Contraction would raise them, and N is on the collapse branch for every galaxy.
8. **Data.** EM1's M200 is an extrapolated fit with no scatter. LITTLE THINGS is one point per galaxy, with all baryons inside R_max. Lens masses depend on assumed profiles, perturbers may be on the line of sight, and dwarfs are taken as in equilibrium. B1938 wasn't regraded.
9. **HS1 has 47 galaxies.** The tilt is −2.7σ, and 91 % of draws stay tilted.
