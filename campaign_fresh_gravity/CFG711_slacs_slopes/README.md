# CFG711: SLACS total density slopes vs the law — NOT DIAGNOSTIC (M1 tooth fails); T1 TENSION, T2 WEAK

Criteria 60d8c7737 (committed alone first; block CFG710–719). `cfg711.py` → `cfg711.out`, `cfg711_results.json`; MUTATE
`CFG711_MUTATE=1` → `_MUTATE` files (exit 0: M1 does not bite). Data: Auger+2010 Table 1 from the paper's TeX (59 lenses).
Control: the power-law mapping recovers γ = 1.7 / 2.0 / 2.3 exactly. κ = ½ FITTED; cold energy mass required; not "theory closed".

| | canonical | alt |
|---|---|---|
| T1 median γ′_pred − γ′_obs | −0.161 ± 0.038 → **TENSION** | −0.172 ± 0.039 → **TENSION** |
| median γ′ pred / obs | 1.927 / 2.090 | 1.917 / 2.090 |
| T2 Spearman (pred vs obs) | ρ = +0.28, p = 0.031 → **WEAK** | same |
| scatter: rms(obs − law) vs rms(obs − mean) | 0.274 vs 0.221 (law adds scatter) | 0.280 vs 0.221 |
| median Δlog σ (pred − obs) | −0.026 | −0.028 |
| implied M* − SPS | +0.34 (Chabrier), +0.09 (Salpeter) | +0.33, +0.08 |

**MUTATE:** M2 (shuffled r_e) bites (ρ 0.28 → −0.09). **M1 does not:** pure Hernquist stars give median γ′ = 2.00 vs the law's 1.93
(+0.07, frozen requirement > 0.3). The frozen expectation was wrong: at r_e/2 (g ≈ 10 a0) the law's cold mass moves this statistic
by only 0.07, so **γ′ from lensing + isotropic Jeans cannot discriminate the law from stars alone** → lane label NOT DIAGNOSTIC.

**Reading:** the observed SLACS slopes (2.09) are steeper than even stars-only Hernquist models under Auger's own mapping (2.00).
Any extended dark component — the law's or a ΛCDM halo — makes the predicted γ′ shallower, so both need a steepening ingredient
(stellar M/L gradient / IMF gradient, de Vaucouleurs vs Hernquist structure, radial anisotropy changes the inferred γ′). The law
lands 0.16 shallow (TENSION, not rescued) and its per-lens ranking is weak. Contrast with CFG710 (B1938): there the observable (κ
slope at θE ≈ 2 R_e) was sensitive (stars 3.26 vs law 2.30) and matched; here the observable is insensitive.
