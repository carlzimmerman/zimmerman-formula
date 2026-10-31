# SR1_r2_on_sluggs: SR1 OVER; LITERAL R2: EXCLUDED [SCALE-DEPENDENT] [TRACER-DEPENDENT]. Inside r₁/₂ SLUGGS's dynamics won't hold R2 as stars on the catalogue's scale, while its GC window wants a lift of about +0.17 dex in both models

Criteria: `FROZEN_CRITERIA.md` (1d0fea100e), committed alone before any script or number from this comparison. No amendment. Script `sr1_grade.py`, outputs `sr1.out`, `sr1_results.json`, twin `sr1_MUTATE.*`. Post-result, reporting only: `sr1_post.py`, `sr1_post.out`.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. The theory stays open. No preference between frameworks is claimed here.

## Verdict (frozen, the same on both footings)

- **R2 as carried to SLUGGS (+0.172): SR1 OVER.** Stars alone at +0.172 exceed the JAM mass inside r₁/₂ by a median 0.134 ± 0.035 dex (Z_stat −3.8). Z_sys is −1.3 with the catalogue's 0.10 dex taken as fully shared, so it is over the ceiling and not excluded.
- **Literal R2 (+0.295): EXCLUDED.** Stars alone exceed M_JAM inside r₁/₂ by a median 0.257 dex (Z_stat −7.3, Z_sys −2.4), in 15 of 16 galaxies, 7 of them by more than 2σᵢ. No model enters this line.
- **[SCALE-DEPENDENT] fired.** On ATLAS3D's own population scale the r₁/₂ classes are AT for +0.172 and OVER for +0.295.
- **[TRACER-DEPENDENT] fired,** but it does not touch the verdict. Stars' GC window class at +0.295 moves from AT to BELOW at β = +0.5. The rung's class is set at r₁/₂, which has no tracer in it.
- **[RADIUS-CONVENTION-DEPENDENT] and [CENTRALS-DEPENDENT] did not fire.**

## How R2's two parts were treated

- **SLUGGS's scale:** Spitzer 3.6 μm light, age-corrected M/L, Kroupa IMF (Forbes+17 by the catalogue's ReadMe; Alabi+17's text on disk), typical uncertainty 0.1 dex.
- **+0.172 carries over.** It is an IMF statement relative to Chabrier. It is the graded rung, I. The recalled Kroupa to Chabrier offset of at most 0.05 dex was not applied; at its largest it would put this median at about −0.084 (Z_stat −2.4), still OVER.
- **+0.123 does not carry over.** It is an OLD minus YOUNG difference between two optical estimators inside KiDS's photometry. On near-IR light the same difference is +0.026 (CFG669).
- **+0.295 is kept** as an upper bracket and for Argon's lines. It would need SLUGGS's catalogue to share the lens catalogue's deficit, which nothing on disk supports or excludes.

## Table 1: stars alone, no halo, no law, no footing

M_dyn(< r₁/₂) = M_JAM/2. M★(< r₁/₂) = f_H M★, Hernquist at SLUGGS's R_e. In the 1–5 R_e columns d lg M = 2⟨log₁₀ σ_obs/σ_pred⟩ on h50's bins, γ = 3, isotropic, hot gas omitted, as CFG55. Negative means stars above M_dyn. Bold means over by more than 2σᵢ.

| galaxy | r₁/₂ kpc | lg M_dyn(<r₁/₂) | lg M★(<r₁/₂) R0 / +0.172 / +0.295 | d lg M R0 | +0.172 | +0.295 | 1–5 R_e R0 | +0.172 | +0.295 |
|---|---|---|---|---|---|---|---|---|---|
| NGC 1023 | 2.34 | 10.52 | 10.58 / 10.75 / 10.87 | −0.060 | −0.232 | **−0.355** | +0.343 | +0.171 | +0.048 |
| NGC 2768 | 10.00 | 11.23 | 10.95 / 11.12 / 11.24 | +0.284 | +0.112 | −0.011 | +0.535 | +0.363 | +0.240 |
| NGC 3377 | 3.08 | 10.17 | 10.19 / 10.36 / 10.49 | −0.023 | −0.195 | **−0.318** | +0.355 | +0.183 | +0.060 |
| NGC 3607 | 6.38 | 11.04 | 11.07 / 11.24 / 11.36 | −0.028 | −0.200 | **−0.323** | +0.249 | +0.077 | −0.046 |
| NGC 4278 | 3.55 | 10.77 | 10.70 / 10.87 / 11.00 | +0.074 | −0.098 | −0.221 | +0.557 | +0.385 | +0.262 |
| NGC 4365 | 9.87 | 11.22 | 11.17 / 11.34 / 11.46 | +0.055 | −0.117 | −0.240 | +0.672 | +0.500 | +0.377 |
| NGC 4374 | 7.60 | 11.28 | 10.95 / 11.12 / 11.25 | +0.333 | +0.161 | +0.038 | +0.835 | +0.663 | +0.540 |
| NGC 4459 | 4.17 | 10.62 | 10.63 / 10.80 / 10.93 | −0.015 | −0.187 | **−0.310** | +0.154 | −0.018 | −0.141 |
| NGC 4473 | 3.31 | 10.62 | 10.69 / 10.86 / 10.98 | −0.062 | −0.234 | **−0.357** | +0.249 | +0.077 | −0.046 |
| NGC 4486 | 8.94 | 11.41 | 11.31 / 11.48 / 11.60 | +0.105 | −0.067 | −0.190 | +0.852 | +0.680 | +0.557 |
| NGC 4494 | 5.23 | 10.69 | 10.70 / 10.87 / 11.00 | −0.008 | −0.180 | **−0.303** | +0.084 | −0.088 | −0.211 |
| NGC 4526 | 4.38 | 10.94 | 11.02 / 11.19 / 11.31 | −0.074 | −0.246 | **−0.369** | +0.261 | +0.089 | −0.034 |
| NGC 4649 | 7.76 | 11.40 | 11.28 / 11.45 / 11.57 | +0.120 | −0.052 | −0.175 | +0.553 | +0.381 | +0.258 |
| NGC 4697 | 5.92 | 10.81 | 10.77 / 10.95 / 11.07 | +0.032 | −0.140 | −0.263 | +0.418 | +0.246 | +0.123 |
| NGC 5846 | 9.74 | 11.27 | 11.05 / 11.23 / 11.35 | +0.218 | +0.046 | −0.077 | +0.908 | +0.736 | +0.613 |
| NGC 7457 | 3.41 | 9.92 | 9.87 / 10.04 / 10.17 | +0.044 | −0.128 | −0.251 | +0.598 | +0.426 | +0.303 |

**Sample level** (median over 16, bootstrap error):

| rung | r₁/₂ | Z_stat, Z_sys | over, by 2σᵢ | class | 1–5 R_e | Z_stat, Z_sys | over, by 2σᵢ | class | rung class |
|---|---|---|---|---|---|---|---|---|---|
| R0 | +0.038 ± 0.035 | +1.1, +0.4 | 7, 0 | AT | +0.476 ± 0.098 | +4.9, +3.2 | 0, 0 | BELOW | **AT** |
| +0.172 | −0.134 ± 0.035 | −3.8, −1.3 | 13, 0 | OVER | +0.304 ± 0.098 | +3.1, +2.0 | 2, 0 | BELOW | **OVER** |
| +0.295 | −0.257 ± 0.035 | −7.3, −2.4 | 15, 7 | EXCLUDED | +0.181 ± 0.098 | +1.9, +1.2 | 5, 0 | AT | **EXCLUDED** |

| same r₁/₂ test, other reading | R0 | +0.172 | +0.295 | classes |
|---|---|---|---|---|
| half convention (the record's), SLUGGS catalogue | −0.003 ± 0.045 | −0.175 ± 0.045 | −0.298 ± 0.045 | AT, OVER, EXCLUDED |
| ATLAS3D's own population Chabrier, half the same light | +0.204 ± 0.029 | +0.032 ± 0.029 | −0.091 ± 0.029 | BELOW, AT, OVER |

## The law and route E on top

Median d lg M with bootstrap error. FC1's rule, smooth core, EM1's M200 at the rung's stars. No hot gas. State: LEVEL within ±0.07; OVER or SHORT beyond it at 2σ.

| model, footing | rung | r₁/₂ | state | 1–5 R_e | state | 1–3 R_e |
|---|---|---|---|---|---|---|
| law, canonical | R0 | −0.090 ± 0.040 | OVER | +0.112 ± 0.062 | WITHIN 2σ | +0.135 |
| law, canonical | +0.172 | −0.238 ± 0.041 | OVER | −0.007 ± 0.065 | LEVEL | +0.016 |
| law, canonical | +0.295 | −0.346 ± 0.041 | OVER | −0.095 ± 0.067 | WITHIN 2σ | −0.073 |
| route E, canonical | R0 | −0.028 ± 0.039 | LEVEL | +0.115 ± 0.057 | SHORT | +0.149 |
| route E, canonical | +0.172 | −0.181 ± 0.037 | OVER | −0.004 ± 0.060 | LEVEL | +0.046 |
| route E, canonical | +0.295 | −0.292 ± 0.036 | OVER | −0.089 ± 0.062 | WITHIN 2σ | −0.042 |
| native z = 0 (reported, no footing) | R0 | −0.065 ± 0.038 | LEVEL | +0.144 ± 0.061 | SHORT | +0.205 |
| native z = 0 | +0.172 | −0.217 ± 0.038 | OVER | +0.017 ± 0.064 | LEVEL | +0.073 |
| native z = 0 | +0.295 | −0.324 ± 0.036 | OVER | −0.077 ± 0.066 | WITHIN 2σ | −0.024 |
| law, alt | R0 | −0.102 ± 0.040 | OVER | +0.081 ± 0.062 | WITHIN 2σ | +0.108 |
| law, alt | +0.172 | −0.250 ± 0.040 | OVER | −0.032 ± 0.064 | LEVEL | −0.009 |
| law, alt | +0.295 | −0.356 ± 0.041 | OVER | −0.118 ± 0.066 | WITHIN 2σ | −0.095 |
| route E, alt | R0 | −0.028 ± 0.039 | LEVEL | +0.094 ± 0.059 | WITHIN 2σ | +0.128 |
| route E, alt | +0.172 | −0.186 ± 0.038 | OVER | −0.013 ± 0.059 | LEVEL | +0.032 |
| route E, alt | +0.295 | −0.294 ± 0.036 | OVER | −0.089 ± 0.061 | WITHIN 2σ | −0.049 |

**No model is LEVEL at both radii at any of the three rungs.**

**The rung each radius asks for** (per-galaxy roots, reported, in dex above the catalogue):

| model | rung at the r₁/₂ ceiling | rung that zeroes 1–5 R_e | gap |
|---|---|---|---|
| stars | +0.038 ± 0.035 | +0.476 ± 0.098 | +0.394 ± 0.050 |
| law, canonical | −0.105 ± 0.047 | +0.163 ± 0.089 | +0.244 ± 0.059 |
| law, alt | −0.121 ± 0.048 | +0.126 ± 0.090 | +0.229 ± 0.059 |
| route E, canonical | −0.031 ± 0.042 | +0.168 ± 0.091 | +0.240 ± 0.059 |
| route E, alt | −0.031 ± 0.043 | +0.156 ± 0.090 | +0.240 ± 0.059 |
| native | −0.076 ± 0.043 | +0.194 ± 0.084 | +0.255 ± 0.049 |

## What the numbers say

1. **The catalogue is already at the ceiling inside r₁/₂.** At R0, 7 of 16 galaxies are at or above M_JAM. There is about +0.04 ± 0.035 dex of room for stars, before any halo or law.
2. **The GC window wants about the size of R2's IMF part, in both models.** The rung that zeroes 1–5 R_e is +0.16 to +0.17 canonical. So +0.172 brings the law and route E level there, at −0.007 and −0.004.
3. **The inner dynamics refuse that lift as stars.** The ceiling rung is −0.03 for route E and −0.105 for the law. The gap is +0.24 ± 0.06 on both, so no uniform stellar scale fits both radii in the median galaxy, in either model.
4. **The scale matters as much as the rung.** Inside r₁/₂ the catalogue sits a median +0.13 dex above ATLAS3D's Chabrier (`sr1_post.out`, range −0.11 to +0.30). In absolute terms the ceiling reads catalogue +0.04 ± 0.035, or ATLAS3D's Chabrier +0.20 ± 0.03. On ATLAS3D's scale +0.172 is at the ceiling with nothing to spare, almost by construction because CFG926 fits its relation there, and +0.295 is over by 0.09 dex (Z_stat −3.1, Z_sys −0.9).
5. **The non-centrals, nearer R2's lenses, leave less room and need less.** On the 12 non-centrals route E reads −0.052 / +0.072 at R0 (r₁/₂ / 1–5 R_e) and −0.205 / −0.033 at +0.172. The law reads −0.104 / +0.079 and −0.257 / −0.047. Their rungs are ceiling −0.06, null +0.115 for route E, and ceiling −0.12, null +0.11 for the law. The 4 centrals carry the outer excess: route E +0.340 at R0 and still +0.187 at +0.295, with host halos omitted as in GR1.
6. **SLUGGS doesn't separate route E from the law here.** Route E overshoots M_JAM by 0.05 to 0.06 dex less at each rung, and their gaps match.

**How this bears on SI2 and SI3.** R2 on the lenses is LePhare + 0.445 dex. This lane cannot tie that to SLUGGS's scale, so the lens result stays conditional as it was. It now has a check, and R2 read as stellar mass does not pass it at face value on the catalogue's scale. A lift of that size at GC radii is what SLUGGS shows; stars inside r₁/₂ are what it refuses. The lens window, beyond about 30 kpc, can't tell stars from other mass. This lane has no model of a non-stellar lift and does not claim one.

## Argon's lines, frozen as stated

Its text names no model, so each line is scored on three rows. R2 = +0.295. Canonical, alt in brackets.

| line | stars | law | route E |
|---|---|---|---|
| A1 PASS, \|median\| ≤ 0.07, 1–5 R_e | +0.181 MISS | −0.095 (−0.118) MISS | −0.089 (−0.089) MISS |
| A1, JAM column, r₁/₂ | −0.257 MISS | −0.346 (−0.356) MISS | −0.292 (−0.294) MISS |
| A2, \|median\| ≤ 0.05, 1–3 R_e | +0.101 MISS | −0.073 (−0.095) MISS | **−0.042 (−0.049) HIT** |
| A2 as PREDICTIONS_ON_RECORD writes it, median \|Δ\| ≤ 0.05 | 0.190 MISS | 0.207 (0.203) MISS | 0.167 (0.167) MISS |
| A3, R0 under-predicted by 0.18–0.25, 1–3 R_e | +0.396 MISS | +0.135 (+0.108) MISS | +0.149 (+0.128) MISS |
| A4 FAIL, rejected by more than 2σ, r₁/₂ | **FIRES**, Z −7.3, sys −2.4 | **FIRES**, −8.5 (−8.7), sys −3.2 (−3.3) | **FIRES**, −8.1 (−8.1), sys −2.7 (−2.8) |
| A4 FAIL, 1–5 R_e | no, Z +1.9 | no, −1.4 (−1.8) | no, −1.4 (−1.4) |

**Score: one HIT at R2, route E on A2's |median| form only. Its FAIL line fires at r₁/₂ on every row and at 1–5 R_e on none.** Its PASS line is not met.

Reported, at the carried +0.172: A1 and A2 both HIT for the law (−0.007, +0.016; alt −0.032, −0.009) and route E (−0.004, +0.046; alt −0.013, +0.032). So its numbers describe the GC window at +0.172 better than at +0.295. A3's band holds only on the native line (+0.205), which is not one of the frozen rows. A4 still fires at r₁/₂ at +0.172 on Z_stat, with Z_sys −1.3 (stars), −2.2 (law), −1.7 (route E).

## Reported rows

| row | result |
|---|---|
| Rung T = +0.091, tie through CFG505 (recalled Bell+03 IMF offset) | r₁/₂ / 1–5 R_e: stars −0.053 ± 0.035 (AT) / +0.385; law −0.169 / +0.050 (alt −0.180 / +0.024); route E −0.110 / +0.057 (alt −0.111 / +0.038) |
| Rung Iσ, CFG926's relation at own σ_e (0.133–0.188) | stars −0.131 / +0.305; law −0.234 / −0.006; route E −0.163 / −0.003 |
| CFG111's γ, 1–5 R_e, R0 / +0.172 / +0.295 | stars +0.459 / +0.287 / +0.164; law +0.087 / −0.031 / −0.118; route E +0.108 / −0.018 / −0.109 |
| β = +0.5 | stars +0.541 / +0.369 / +0.246; law +0.120 / +0.012 / −0.073; route E +0.121 / +0.010 / −0.078 |
| β = −0.5 | stars +0.443 / +0.271 / +0.148; law +0.104 / −0.017 / −0.107; route E +0.114 / −0.010 / −0.094 |
| Route E, M200's argument held at the catalogue | +0.172: −0.185 / +0.009; +0.295: −0.296 / −0.067 |
| Route E on CE1's A4 η (25.94, 23.54, 22.10) | R0 −0.033 / +0.113; +0.172 −0.184 / −0.012; +0.295 −0.294 / −0.108 |
| h50's 19, 1–5 R_e | stars +0.423 / +0.251 / +0.128; law +0.112 / +0.001 / −0.081; route E +0.120 / +0.016 / −0.075 |
| N = 17, NGC 821 restored, r₁/₂ | stars +0.044 / −0.128 / −0.251; law −0.083 / −0.226 / −0.332; route E −0.014 / −0.168 / −0.282 |
| Alabi+17's published M_tot(<5 R_e) and f_DM column, β = 0 | stars +0.538 ± 0.107 / +0.366 / +0.243; over 0, 1, 4 of 16, none by 2σ. It agrees with the Jeans window to 0.06 dex |
| GC estimator against JAM: stars at R0, innermost window bin minus r₁/₂ | median +0.314, SD 0.237 |
| M★/M_JAM, totals, R0 / +0.172 / +0.295 (SG1's JAM analogue 0.87–0.95) | NGC 4365 0.97 / 1.45 / 1.92; NGC 4374 0.84 / 1.25 / 1.66; NGC 4486 0.81 / 1.20 / 1.59; NGC 5846 0.77 / 1.15 / 1.52 |

**Four centrals on CFG528b's measured GC profiles and anisotropy, catalogue masses, 1–5 R_e** (NGC 4486, 4365, 4374, 5846):

| | R0 | +0.172 | +0.295 |
|---|---|---|---|
| stars | +0.767 +0.624 +0.781 +0.897 | +0.595 +0.452 +0.609 +0.725 | +0.472 +0.329 +0.486 +0.602 |
| law, canonical | +0.406 +0.236 +0.257 +0.388 | +0.291 +0.124 +0.153 +0.284 | +0.205 +0.041 +0.077 +0.207 |
| route E, canonical | +0.370 +0.184 +0.194 +0.306 | +0.266 +0.088 +0.101 +0.214 | +0.189 +0.018 +0.035 +0.148 |
| route E, canonical, measured gas to the X-ray edge | +0.332 +0.183 +0.194 +0.302 | +0.236 +0.087 +0.101 +0.210 | +0.163 +0.017 +0.034 +0.145 |

Inside 1–5 R_e the measured gas only moves M87.

## My expectation, scored

Stars at +0.295 beyond 2σ: right. Stars at +0.172 at or over the ceiling: right. The GC window not binding stars: right. The law over at r₁/₂ and level in the GC window at +0.172: right. Route E close to the inner ceiling at +0.172: **wrong**, it is over by 0.181 dex (Z_stat −4.9). Route E short for the centrals: right.

## Checks

| check | result |
|---|---|
| K1 (a) CFG55's committed law offsets and log M★ | \|d\| 0.0, both footings |
| K1 (b) stars path equals h50's `off_newt` | \|d\| 0.0 |
| K1 (c) CFG55's kernel through this path equals its SLUGGS-mass law mean | \|d\| 0.0 |
| K1 (d) CFG528b row M K0 | \|d\| 0.0 |
| K2 raw TSV equals machinery for r₁/₂ and M_JAM | 0.0 |
| K2 median lg(r₁/₂/R_e) | 0.137 against lg 1.33 = 0.124 |
| K2 f_H(1.33 R_e); f_H range | 0.5000; 0.28–0.57, as CFG55 printed |
| K2 windows | all 16 have bins at 1–5 and 1–3 R_e, inside h50's outer bins |
| K3 FC1's S/Σ_coll nodes; M_h(R200) = M200; native m(1) | 5.9e-4; 3.7e-15, 0 saturated; 3.3e-4 |
| K4 stars' linearity in the rung | 1.2e-15 |
| K5 peak RSS | 0.45 to 0.46 GB across runs |
| Rerun | results JSON byte-identical (sha256 72ed60c4…) |
| **MUTATE** (M_JAM × 0.5, σ_obs × 0.8, halos × 0.5) | stars' median shifts −0.30103 at r₁/₂ and −0.19382 in the window, route E's gap shrinks in every galaxy, K1 fails, no verdict, exit 1: **BITES** |

**Post-result check on the decisive column:** `sr1_post.py` recomputes r₁/₂ from the raw TSVs with no machinery. Max |d| per galaxy is 3.9e-7 dex (the arcsec-per-radian rounding), and the medians are the same.

## Disclosures

- Not blind. §0 of the criteria lists what I read, a hand estimate from AUDIT_SLUGGS's table and a machinery probe, all before freezing.
- Criteria §3 cites §5 for the measured gas row. It is §8 row 9. A typo, no rule affected.
- `sr1_post.py` was written after the result. Its subset rungs and scale comparison move no class.
- h50's name-key artefact stays in the main sample, as CFG55's. The N = 17 row shows its size.

## Limits

1. **The tie between lens masses and SLUGGS masses is not measured.** +0.172, +0.295 and +0.091 are three readings of it. No galaxy is in both catalogues. Read any other tie off the ceiling rung above.
2. **+0.172 is not independent of ATLAS3D at r₁/₂.** CFG926 fits its relation to ATLAS3D's JAM-based M/L, itself built with NFW halos. CFG926's native check gives +0.168 / +0.154. The GC window is independent of ATLAS3D, but it does not bind stars.
3. **SLUGGS isn't the lens sample.** These are local, massive, mostly group and cluster galaxies. R2's lenses are isolated, red, at z ≈ 0.25, with σ about 186 km/s. A uniform shift across them is an assumption.
4. **The rung is uniform at all radii.** A measured IMF gradient would put less of it at GC radii.
5. **The two M_dyn estimators don't meet.** Near the same radius the GC estimator reads a median 0.31 dex above JAM, SD 0.24. Part may be mass rising with radius, part may be γ = 3 and isotropy, which AUDIT_SLUGGS, CFG323 and CFG466 name as the soft side. This lane can't separate them, so the gap's size leans on the tracer. The r₁/₂ classes do not.
6. **M_JAM carries its own assumptions:** mass follows light inside r₁/₂. Its 0.05 dex per-galaxy error is recalled. It enters only the 2σᵢ flags.
7. **Distance:** d lg M at r₁/₂ runs as −lg D, so a shared 10 % distance error moves it by 0.04 dex.
8. **The Hernquist profile stands in for the 3.6 μm light.** The half convention gives the same classes.
9. **Route E's inputs are taken as given:** EM1's M200 extrapolated to these masses, FC1's rule (COLD-SHARE FAIL at A4 on its own grader), and the isolated reading with host halos omitted for M87 and NGC 5846. The halo-argument and η-table rows move it by about 0.02 dex at most.
10. **The law here is algebraic and spherical,** with no external field. AUDIT_SLUGGS finds an external field can only widen its shortfall.
11. **N = 16.** A bootstrap of a median over 16 galaxies is coarse.
12. **This checks a stellar-mass scale.** It does not derive κ, and it does not choose between route E and the law.

## Next (not done here)

- A direct tie between KiDS-bright masses and a near-IR scale on common galaxies would replace the three readings. It isn't on disk.
- Per-galaxy GC density slopes and anisotropy for the 12 non-centrals would narrow limit 5.

## Compute

One thread, `nice -n 15`, one process at a time, about 30 s per run, peak RSS at most 0.46 GB. Nothing downloaded. No other lane's file changed; the machinery ran through a read-only `open`.

```
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 -B sr1_grade.py            # exit 0
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 -B sr1_grade.py --mutate   # exit 1 = bites
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 nice -n 15 python3 -B sr1_post.py             # post-result, reporting only
```
