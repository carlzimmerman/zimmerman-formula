# LF1_lensing_gas_fraction: DEPLETED [ENOUGH FOR ZN3] [FLAT] as frozen. Measured gas plus stars is short of the cosmic share on the heaviest lensing clusters, log Y −0.12 to −0.135. This doesn't reconcile the clusters: it's the same shear as the keys, and X-COP's hydrostatic share sits 0.12 dex higher

Criteria: `FROZEN_CRITERIA.md` (72548de349, committed alone). `lf1.py`, `lf1.out`, `lf1_results.json`, `lf1_MUTATE_gas.out`, `lf1_MUTATE_shuffle.out`, `lf1_xcop.py`, `lf1_xcop.out`. κ = ½ FITTED; cold dark energy, never a particle; not theory closed. Nothing here says the data favour the framework.

**Not independent.** This is the KiDS shear that graded G-OUT-M3. It removes ZN3's shape from the comparison and shows the size and radial form of the miss. It can't confirm the miss.

## Result: M3 (109 clusters), compensated cylinder, Rmax 3 Mpc
Γ = ζ_b/ζ_shear; log Y = log₁₀(Γ/0.15945). R₂₀₀ edge 1.42 Mpc (median fair-share R₂₀₀ 1.25), R₅₀₀ edge 0.98.

| h | f★ | Γ at R₂₀₀ | log Y ± SE | at R₅₀₀ | Δ (radial) |
|---|---|---|---|---|---|
| 0.672 | 0.034 | 0.1168 | −0.135 ± 0.040 | −0.115 ± 0.054 | +0.020 ± 0.026 |
| 0.672 | 0.0615 | 0.1199 | −0.124 ± 0.039 | −0.104 ± 0.054 | +0.020 ± 0.026 |
| 0.686 | 0.034 | 0.1188 | −0.128 ± 0.037 | −0.124 ± 0.053 | +0.004 ± 0.028 |
| 0.686 | 0.0615 | 0.1220 | −0.116 ± 0.037 | −0.112 ± 0.054 | +0.004 ± 0.028 |

About 3 SE below the share in each cell, and the 2 SE band covers −0.093 in each. In mass terms: gas plus stars about 25 % short of fair share, or about 35 % more mass than fair share gives. Fair reference with a compact cold profile: Γ_ref 0.164–0.168, log Y −0.131 to −0.152, same class, so no [SHAPE-DEPENDENT].

Others, h 0.672, f★ 0.034: M2 −0.153 ± 0.053 at 0.98 Mpc; all 326 −0.124 ± 0.061 at 0.98 Mpc (over the 0.06 power line); M1 −0.213 ± 0.166 at 0.46 Mpc (not powered). M2 and all have the same edge for R₂₀₀ and R₅₀₀.

Γ by edge, M3: 0.32 Mpc 0.105; 0.46 0.113; 0.67 0.1225; 0.98 0.1224; 1.42 0.117; 2.06 0.101.

## What it does and doesn't say
1. **Not a rescue of ZN3.** Lowering the baryon share so the keys pass raises M₂₀₀ for the same gas by about 0.12 dex. X-COP's hydrostatic masses don't allow that: its share is log Y −0.042 at R₅₀₀ and −0.011 at 1.5 R₅₀₀ (f★ 0.034), −0.031 and 0.000 (f★ 0.0615). So shear on eRASS1 clusters and hydrostatic masses on X-COP differ by about 0.12 dex at fixed gas. This lane can't say which is off. Hydrostatic bias, X-COP's selection, a difference between the samples, and a shear bias all remain open. No lensing mass here is on X-COP's own clusters; RF3 has one, A2142, which agrees with hydrostatic.
2. **[FLAT] doesn't rule out extra outer mass.** R₅₀₀'s and R₂₀₀'s apertures share the same annulus, to 3 Mpc. Rmax 2.06 Mpc moves log Y from −0.135 to −0.086, a post-result read on one bin and noisy, so roughly a third of the deficit depends on the last bin. RF4 found the two-halo term unseparable on this shear. So line-of-sight or infall mass isn't excluded, and "missing gas" isn't established. A deficit at 0.67–0.98 Mpc is present at about the same size, on the same annulus.
3. **No mechanism.** A share 25 % short inside R₂₀₀ isn't what gravity-only collapse gives, and CL5 found black-hole gas cycles NOT REACHED at this scale (8 % at ceiling, 15–19 % needed). Adding a depletion factor would add a free parameter.
4. **eRASS1's own catalogue, bracket only (ΛCDM count fit, WL-calibrated):** Mgas500/M500 median 0.084 M3, 0.066 M2, 0.041 M1. Same direction, not independent, not graded.

## Sizes reported, not graded
Gas tail s 2.676 → −0.133; 3.071 → −0.141. Miscentred gas −0.136. Reduced shear f_r − 1 about 0.025, which could shift log Y by about +0.01. Mgas500 catalogue error 0.069 dex: M3 is cut on gas, so scatter biases Γ high, which works against this deficit. GS4's ±0.017 on eRASS1's gas isn't in the SE; adding it moves SE from 0.040 to 0.043.

## Checks
K1 own line-of-sight integral 3.9e-3, PASS. K2 SIS 5.8e-3, PASS. K3 0, PASS, **weaker than frozen:** X30 stores no n, so this is a replay of the data and the formula, not a read of the grader's value. K4 injection 0.10 → 0.1002, PASS. MUTATE gas × 2: +0.301, EXCESS, BITES. MUTATE shuffle: −0.135 → +0.170 ± 0.203, NOT POWERED, BITES. Rerun identical.

## Deviations and errors, all disclosed
Before any verdict: numpy call; R₂₀₀ mass units and first-crossing bug, found by K1 and K4; F1's `project` holds the last density through a truncation, so X2's `project_floor` replaced it (K1). After the first verdict, no graded number changed: the f_r unit, the shuffle wiring (first MUTATE ran unshuffled), and K3 under shuffle. Frozen text says trapezoid and Rmax 2.18; the code sums bins, exact on the bin edges (K2's 0.6 %), and the nearest edge is 2.06. Gas truncated at 3 R₂₀₀ (the criteria left this open); edges use R₂₀₀ at f★ 0.034; ρ_c(z) uses native Ω_m, radius choice only. Frozen same-cylinder X-COP read wasn't possible without mass outside its profile, so it's a 3D share, labelled. Stars take gas's shape, the grader's convention, which is why Γ falls inside 0.5 Mpc: that part isn't a depletion read.
