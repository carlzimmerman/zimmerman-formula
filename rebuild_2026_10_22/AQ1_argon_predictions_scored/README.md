# AQ1_argon_predictions_scored: Argon's frozen predictions for the live runs, scored on landing. ZN4: 6 of 7 lines MISS (η and c_f FALL at ng 80, Argon had them rising; X-COP passes as at ng 64); the one HIT is G-OUT-M3 staying over +2.5 on the measured gas scale. 1e12 ng 80: η_conv 21.5, ratio 0.83 [0.55, 1.12] against 1.035 ± 0.025, MISS (noise-limited). VB1: outer number inside the range, inner mass and the key MISS

Scripts here read other lanes' snapshots and outputs only: `aq1_eta_1e12_ng80.py` (X80's converged-cusp estimator on X48's nine 1e12 ng 80 seeds; `aq1_eta_1e12_ng80.out/.json`), `aq1_cf_zn4.py` (X48's c_f estimator on ZN4's and ZN3's collapses; `aq1_cf_zn4.out/.json`). ZN4's grades are the other session's (`../ZN4_cluster_resolution/zn4.out`, `zn4_c200.out`, `zn4_boot.out`, `zn4_readouts.out`), quoted not re-derived. Predictions as frozen in `../ARGON_REPLY_2026-10-31_EVENING_SCORED.md` §3 and `../ARGON_REPLY_2026-11-01_SEAL_AND_D2.md`. κ = ½ FITTED; footings never pooled; cold dark energy is a gravitating field component, never a particle; not theory closed. Nothing here says the data favour the framework.

## ZN4 (ng 80 at 1e14 and 1e15, six seeds each)

| Argon's line | measured | score |
|---|---|---|
| η(ng 80)/η(ng 64) at 1e14: 1.09 ± 0.05 | z = 0 smooth-core η 29.99 / 34.06 (ZN4 / ZN1 readouts) = **0.88** | MISS, wrong sign |
| c_f(1e14, ng 80) 10.8 ± 0.4 | **6.12** (seeds 2.5–12.6; ng 64 10.07) | MISS, wrong sign |
| c_f(1e15, ng 80) 11.6 ± 0.6; η ratio 1.11 ± 0.05 | **6.54** (ng 64 ZN3 8.02); η 23.06 / 23.80 = **0.97** | MISS, MISS |
| X-COP at ng 80 survives barely on rms 0.088–0.098 or fails on mean −0.055 to −0.085; c₂₀₀(1e15) 12–13 | mean +0.013, rms 0.075 (f★ 0.034); +0.005, 0.074 (0.0615): PASS as at ng 64; c₂₀₀ 5.42 / 4.09 at 1e14 / 1e15, **down 9 %** from ng 64 | MISS, MISS |
| G-OUT-M3 at ng 80 stays UNDER, Z > +2.5 | measured gas +0.005: **+4.41 / +4.13**; X-COP's gas +0.111: +1.53 | HIT on the measured scale (the class scale); not on X-COP's |

ZN4's own reading (other session's grader): Z0 PROFILE PASSES BOTH on X-COP's gas, X-COP ONLY at the measured +0.005, c₂₀₀ within 10 % at both masses, headline class holds in 92 % of bootstrap draws. Argon's mechanism (two-body relaxation inflating the inner profile, saturating at ng 80) predicted concentration rising with resolution; it falls, at both masses, in c_f, c₂₀₀ and η. Noted, not graded here: X48's c_f at 1e14 moves from 10.07 (ng 64) to 6.12 (ng 80), still above A4's window [3.3, 4.6]; the resolution dependence A4 flagged at 1e14 continues.

## 1e12 at ng 80 (A5's nine seeds)

| Argon's line | measured | score |
|---|---|---|
| η_conv(1e12, ng 80)/η_conv(ng 64): 1.035 ± 0.025 | **0.830 [0.553, 1.115]** (21.53 [14.55, 24.89] against 25.94 [23.89, 26.53]; per-seed 12–34 at both resolutions) | MISS on the centre; the 68 % band covers 1.035, so noise-limited |
| c_f(1e12, ng 80) 7.95 ± 0.20 | 7.43 (A5, `../X48_native_cf_zoom/x48_A5_x74_read.out`) | MISS |
| η 25.5–26.3 | 21.5 | MISS |
| native N SPARC Υ after that: 0.69 / 0.71, survives | not read here; a lower η(1e12) anchor moves Υ up from 0.70 / 0.72, not down, so the 0.50 floor is not approached | direction consistent, number not read |

## VB1 (Argon's D2; `../VB1_vacuum_boundary/README.md`)

| Argon's line (at 2.25 q_M; run at 2.0, disclosed) | measured | score |
|---|---|---|
| ΔΣ(2.18–3.17 R500) +18 to +24 %, later +16 to +26 % | **+21.3 ± 1.2 %** | number inside both ranges |
| ΔM(< 0.7 R500) +1.8 ± 1.2 % | **+23.0 %** | MISS by 18σ |
| ΔM(< R200) +5.5 ± 2.0 % | +22.9 % | MISS |
| G-OUT-M3 on the measured scale from about +3.8 to about +2.4 | +4.36 → **+4.41** | MISS |
| class: inner gate passes, outer partial relief | MIXED by the gate; MUTATE does not bite, lane stops; shape unchanged | the mechanism (outskirts fed, inner held) is not what happened |

## Argon's revised stop seal, read against these numbers (recorded, not adjudicated: "and" against "or" is Argon's to state)
- Cluster half: ZN4 passes X-COP; G-IN-Mall > −2; G-OUT-M3 **+4.41 > +2.0 on the measured gas scale** and stays after VB1 → fires on the measured scale, does not on X-COP's (+1.53).
- Galaxy half, branch 1: armed only once η_conv(1e12, ng 80) ≥ 25.0; measured 21.5 → **not armed** by its own clause (ND1's +0.138 and the three missed ET1 bins stand regardless). Branch 2: Υ 0.50 not approached; "2 of 3 ET1 bins outside at 95 % CI" undefined (three central values, no tolerance), and at face value all three are outside on every what-if row on record (NF1, AE1).

## Score card
ZN4 1 of 7; 1e12 0 of 3 (one noise-limited); VB1 1 of 5 (the one hit is the outer number, whose predicted mechanism the inner number contradicts). Across today's doors Argon's structural calls were right twice (the template moves the keys about 2 Z; ρ₁₁ flat) and wrong on direction in every resolution line. The record's own lines were also wrong on VB1 (f_out 1.05–1.15, f_in within 2 %).

κ = ½ FITTED; c_f EXTERNAL where used; not theory closed; nothing here says the data favour the framework.
