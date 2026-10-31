# GS5_gas_offset_sz_independent: NO OFFSET [Y-PRODUCT-DEPENDENT], conditional on AMENDMENT_A1. The SZ route doesn't reach ZN3's +0.093 overall, but its low-z half does come close, and it reaches only the massive end

Criteria: `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (c8ef57d5f0, committed alone), `AMENDMENT_A1.md`. `gs5.py`, `gs5.out`, `gs5_results.json`, `gs5_MUTATE.out`, `gs5_shear.py`, `gs5_shear.out`, `gs5_shear_results.json`. κ = ½ FITTED; not theory closed. Nothing here says the data favour the framework. Clusters only.

d = how much eRASS1's Mgas500 must be raised, at its own R500. Line: +0.093.

| Route | d | SE | class | floor (unmatched Y = 0) |
|---|---|---|---|---|
| **(d) T dropped, Y5R500, headline** | **+0.029** | **0.026** | **NO OFFSET** | +0.020 |
| (d) T dropped, Y(MSZ) | +0.049 | 0.017 | BELOW | +0.040 |
| (b) relative to X-COP, with T scale | +0.013 | 0.092 | NOT POWERED | +0.000 |
| (a) absolute constant, with T scale | +0.016 | 0.096 | NOT POWERED | +0.004 |

Raw eRASS1 KT, no T scale: (a) +0.096, (b) +0.093. These sit on the line, by the T term alone: T_X/KT over the five same clusters runs −0.14 to +0.23 dex, median +0.08. That scatter is why (a), (b) can't decide.

Both (d) readings lie below the line by about 2.5 SE. Precision: the question needs about 0.02; (d) has 0.026, MSZ's 0.017 leans on Planck's Y–θ prior.

## By mass and redshift
| Set | N | median M500 | (d) Y5R500 | (d) Y(MSZ) |
|---|---|---|---|---|
| lg Mg 13.6–13.9, z 0.03–0.10 | 21 | 6.1e14 | +0.076 ± 0.046 | +0.073 ± 0.041 |
| lg Mg 13.9–14.3 | 28 | 8.7e14 | +0.013 ± 0.026 | +0.041 ± 0.018 |
| z ≤ 0.15, θ500 ≥ 10′ (same 26 clusters) | 26 | | +0.070 ± 0.025 | +0.075 ± 0.015 |
| z > 0.15, θ500 < 10′ (same 23) | 23 | | +0.003 ± 0.025 | +0.033 ± 0.013 |
| lg Mg ≥ 13.9, z ≤ 0.15 | 5 | | +0.059 ± 0.035 | +0.077 ± 0.014 |
| lg Mg ≥ 13.9, z > 0.15 | 23 | | +0.003 ± 0.025 | +0.033 ± 0.013 |

Top two rows: full SE. Others: bootstrap only, and post-result reads where marked in `gs5.out`.

**The split is the main thing to read.** The clusters most like X-COP in z and size on the sky give about +0.07, one SE or so from the line. The more distant half gives about 0 to +0.03. z and θ500 are the same split here, and mass partly follows, so this can't say which matters. A size-flux bias, Planck's beam, evolution past E^(2/3), or a z trend in eRASS1's gas would each do it. E's exponent moves the whole-sample d by only 0.004. So the headline isn't a clean exclusion of the line, and +0.07 isn't support for it.

## Consistency line, NOT INDEPENDENT of the grader
The 15 keys along ZN3's own path, gas × 10^d (M₂₀₀ moves by fair share; gas moves with it, so this isn't a zero-gas fit). χ² minimum at d +0.118 to +0.138 across both f★ and both h, Δχ² = 1 edges about ±0.018 (Z's correlated: indicative). All |Z| ≤ 2 at grid points +0.10 and +0.15, not at +0.05 or +0.20. The same shear graded ZN3, so this can't support ZN3. It says what scale the shear asks for: above every SZ figure here, by about 3.5 SE against (d) overall and about 2 stat SE against the low-z half. These are different clusters (next section).

## Limits
1. **Massive end only.** The completeness rule leaves 52 clusters (49 matched), lg Mg ≥ 13.6, M500 about 6–9e14. Under lg Mg 13.6 Planck detects too few (f ≤ 0.61), and matching alone would read high. The lensing sample's median M500 is 1.8e14, and only 17 % of it reaches X-COP's lightest (SM1). **This doesn't measure the offset where the keys live.**
2. **(b), (d) aren't free of X-ray flux calibration.** They're anchored on X-COP's XMM gas, and ask if eRASS1 sits low against X-COP through Y. Only (a) is free of that, and it's NOT POWERED.
3. **On the same clusters Y cancels,** so the brief's "matched" (b) is SM1 again with T. Done as a population comparison.
4. **(d)'s assumption:** one Y at one Mgas in both surveys. X-COP is Planck-selected: pure Y-limited selection would read d low by at most 0.017 (toy; not in SE), giving at most +0.046 and +0.066. Both still under the line by more than one SE. OLS slopes are 1.38 (eRASS1), 1.35 (X-COP) against the assumed 5/3; α 1.4–1.9 moves d by 0.005.
5. **Anchor:** 11 clusters; ZW1215 isn't in PSZ2. Scatter 0.074 dex, zero-point SE 0.022. Leave one out: +0.017 to +0.036, MSZ +0.044 to +0.052.
6. **Planck Y:** marginal over size. K2 on X-COP is fine at R500 (+0.021) but with scatter 0.115 dex, partly self-referent, since X-COP's outer pressure uses Planck's y. Y(MSZ) uses Planck's hydrostatic Y–M relation at h 0.7, Ω_m 0.3; its normalisation drops out, its size prior doesn't.
7. **No X-COP temperature on disk.** T_X comes from inverting M_FORW and the gas. Past the data M_FORW is wild (outer slopes −3 to +2.4), and the Y5/Y500 this gives (7.7, or 4.7 with M_NFW, against Planck's 1.79) is unreliable and unused. T inside R500 is stable, 0.984 with M_NFW. Route (d) doesn't use T.
8. **Catalogue rulers:** D_A, E(z) at Ω_m 0.3, h 0.70, the catalogues' convention. Ω_m 0.2–0.4 moves d by 0.002.
9. **A first run's bug,** disclosed: the same-cluster loop ran after the PSZ2 cut and lost ZW1215; K3 caught it (+0.087 vs SM1's +0.111). Fixed before any class was read as final, and it moved (d) from +0.040 to +0.029, MSZ from +0.060 to +0.049, through s +0.025 to +0.015 as frozen.

## Checks
K1 C 1.4159e-19 at μ_e 1.148 (0.01 %), uniform sphere 3e-16: PASS. K2 +0.021: PASS. K3 11 of 12, median sep 1.34′, false rate 0.1 %, SM1's +0.111 reproduced: PASS. K4 d +0.111 reproduces ZN3 |d| 0: PASS. **MUTATE as frozen could not be met, its statistic was mis-specified; replaced after the fact, AMENDMENT_A1:** +0.756 → +0.006 ± 0.149, bites. Injection −0.100 dex moves (d) +0.100. Rerun byte-identical.
