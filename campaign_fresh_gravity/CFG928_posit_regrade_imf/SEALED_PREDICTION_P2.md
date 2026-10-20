# CFG928 SEALED PREDICTION: P2 (velocity-space capture) for pressure-supported ultra-diffuse galaxies

**Seal.** Written on 2026-10-20, after the main run of results commit 82a69be8f, which was graded under criteria ba971914e.
- The file is committed ALONE, before the README.
- This lane has opened no UDG data before the seal. L23's data are not opened at all.
- The numbers below are copied from `cfg928.out` and from the `sealed_numbers` block of `cfg928_results.json` in that commit.
  The committed `cfg928.py` computes them from declared inputs only; no object data enter.

## Why P2 is sealed, and how weak its standing is

Under C1 (CFG926 R5's IMF-corrected red lenses) and C2 (clusters a separate class), P2 is the only posit that SURVIVES on the
galaxy-scale facts. It does so on both footings. Its standing is weak for five reasons:
- **The test is post hoc.** It was designed after CFG921's failures and after CFG926 were seen.
- **It is conditional.** C1 needs disc galaxies to stay near Chabrier.
- **It is FRAGILE.** Without CFG667's +0.123 dex (V7), P2 FAILS on the canonical footing.
- **It is C1-DEPENDENT.** Under the weaker SLUGGS and CFG850-window variants, canonical P2 is UNDERDETERMINED.
- **It FAILS on all facts.** It predicts no cluster excess.

So P2's fit is "best of 20 posit-framings tried" and is not evidence for it. This prediction is the test.

## The posit and its constant

- **Surplus:** s = Σ_k m_k (v_2/σ_k)³ exp(−v_rot,k²/2σ_k²). This is the cold energy's capture at its own velocity, in the
  unsaturated limit (CFG921, section 4).
- **Excess:** E = ln(1 + sφ).
- **Constant:** v_2 is fixed on the 83 LVD dwarfs (CFG921 calibration, unchanged here).

| footing | v_2 (σ_g 10, nominal) | θ+ / θ− (dwarf mean ± se) | v_2 at σ_g 6 / 20 |
|---|---|---|---|
| canonical (a0 9.3603e-11) | 6.9503 km/s | 7.8478 / 6.1025 | 6.6795 / 7.0294 |
| alt (a0 1.1312e-10) | 6.4575 km/s | 7.3437 / 5.6167 | 6.2150 / 6.5282 |

## The sealed formula (per UDG; baryonic inputs only)

**Inputs:**
- L_V;
- the projected half-light radius R_e;
- M_g,in, the cold gas inside r12 (0 if gas-free);
- σ_g = 10 km/s, the declared gas dispersion.

**Definitions** (the CFG880/914/919/921 dwarf conventions):
- M* = 2 L_V and r12 = (4/3) R_e.
- g_bar = G (M*/2 + M_g,in) / r12².
- ν = ν_e(g_bar/a0) = 1/(1 − exp(−√(g_bar/a0))), and φ = 1 − 1/ν.
- σ_law² = r12 g_bar ν / 3.
- w = (M*/2)/(M*/2 + M_g,in).

**Prediction:**
- Solve u² = 1 + φ [w (v_2/(u σ_law))³ + (1 − w)(v_2/σ_g)³] for u ≥ 1.
- Then E_pred = 2 ln u and σ_pred = u σ_law.

**Observable:** E_obs = 2 ln(σ_obs/σ_law), where σ_obs is the measured stellar or globular-cluster line-of-sight dispersion.

E is taken relative to the ISOLATED law: EFE-free, like the record's dwarf numbers. The posit carries no host variable, so the
prediction applies to UDGs in every environment.

## Numbers for the declared representative inputs (no object data)

Gas-free (w = 1) is the primary case. In the table, ± is the θ± spread σ_pred. The gas-bearing variant has M_g,in = M*/2.

**Canonical:**

| M* (M☉) | R_e (kpc) | log g_bar | σ_law (km/s) | E_pred (ln) | dex | ± | σ_pred (km/s) | gas M*/2: E at σ_g 6 / 10 / 20 |
|---|---|---|---|---|---|---|---|---|
| 3e7 | 1.5 | −12.282 | 12.22 | +0.131 | +0.057 | 0.039 | 13.05 | +0.495 / +0.172 / +0.063 |
| 3e7 | 2.5 | −12.725 | 12.13 | +0.137 | +0.059 | 0.040 | 12.99 | +0.512 / +0.180 / +0.067 |
| 3e7 | 4.0 | −13.134 | 12.08 | +0.140 | +0.061 | 0.041 | 12.96 | +0.522 / +0.184 / +0.069 |
| 1e8 | 1.5 | −11.759 | 16.77 | +0.056 | +0.024 | 0.019 | 17.24 | +0.455 / +0.141 / +0.034 |
| 1e8 | 2.5 | −12.202 | 16.54 | +0.061 | +0.026 | 0.020 | 17.05 | +0.484 / +0.153 / +0.037 |
| 1e8 | 4.0 | −12.611 | 16.42 | +0.063 | +0.028 | 0.021 | 16.95 | +0.501 / +0.159 / +0.040 |
| 3e8 | 1.5 | −11.282 | 22.60 | +0.022 | +0.010 | 0.008 | 22.85 | +0.403 / +0.118 / +0.021 |
| 3e8 | 2.5 | −11.725 | 22.09 | +0.026 | +0.011 | 0.009 | 22.38 | +0.450 / +0.134 / +0.025 |
| 3e8 | 4.0 | −12.134 | 21.81 | +0.028 | +0.012 | 0.010 | 22.11 | +0.478 / +0.144 / +0.027 |

**Alt:**

| M* (M☉) | R_e (kpc) | σ_law (km/s) | E_pred (ln) | dex | ± | σ_pred (km/s) | gas M*/2: E at σ_g 6 / 10 / 20 |
|---|---|---|---|---|---|---|---|
| 3e7 | 1.5 | 12.79 | +0.099 | +0.043 | 0.033 | 13.44 | +0.419 / +0.140 / +0.047 |
| 3e7 | 2.5 | 12.71 | +0.103 | +0.045 | 0.034 | 13.38 | +0.433 / +0.145 / +0.050 |
| 3e7 | 4.0 | 12.66 | +0.105 | +0.046 | 0.035 | 13.34 | +0.440 / +0.149 / +0.052 |
| 1e8 | 1.5 | 17.53 | +0.041 | +0.018 | 0.015 | 17.89 | +0.387 / +0.116 / +0.026 |
| 1e8 | 2.5 | 17.31 | +0.044 | +0.019 | 0.016 | 17.70 | +0.410 / +0.124 / +0.029 |
| 1e8 | 4.0 | 17.19 | +0.046 | +0.020 | 0.017 | 17.59 | +0.423 / +0.129 / +0.030 |
| 3e8 | 1.5 | 23.58 | +0.016 | +0.007 | 0.006 | 23.77 | +0.345 / +0.098 / +0.017 |
| 3e8 | 2.5 | 23.09 | +0.019 | +0.008 | 0.007 | 23.31 | +0.382 / +0.110 / +0.020 |
| 3e8 | 4.0 | 22.82 | +0.020 | +0.009 | 0.008 | 23.05 | +0.405 / +0.118 / +0.021 |

## The prediction in words

1. **Gas-free UDGs are nearly on the law.** For M* = 3e7–3e8 M☉, P2 predicts E = +0.02 to +0.14 (+0.01 to +0.06 dex)
   canonical and +0.016 to +0.105 alt.
   - The σ_obs predicted is 1.01–1.07× σ_law.
   - This is at most about 1/6 of the LVD dwarf class mean (+0.856 / +0.765).
2. **The excess is set by σ_law, not by size.** At fixed M*, R_e from 1.5 to 4 kpc changes E by less than 0.01. As σ_law
   rises from about 12 to about 23 km/s, E falls roughly as φ(v_2/σ_law)³.
3. **Cold gas would raise it.** A cold gas component inside r12 raises the excess through the (v_2/σ_g)³ term. With
   M_g,in = M*/2, E is +0.10–0.18 at σ_g 10 km/s and up to +0.5 at σ_g 6 km/s. Pressure-supported UDGs with measured
   dispersions are mostly gas-poor, so the gas-free row is the prediction.
4. **No other rise is allowed.** P2 allows no rise of E with low surface brightness, size or environment at fixed σ_law and
   gas content.

## Kill line (form frozen in criteria section 6)

**Sample.** A future lane assembles N ≥ 5 pressure-supported UDGs with measured σ_obs. It then:
- computes, for each galaxy, E_obs with the estimator above (M* = 2 L_V, Wolf σ at r12 = 4/3 R_e, M_b/2 inside r12, the
  isolated ν_e law);
- computes E_pred from that galaxy's own inputs through this formula;
- carries σ_pred from θ±.

**Verdict.** On a footing, P2 is EXCLUDED if |mean E_obs − mean E_pred| ≥ 3 √(se_obs² + σ_pred²). Both footings are scored
separately and never pooled.

**Example.** Take a gas-free sample at M* ≈ 1e8 with se_obs ≈ 0.10. P2 is excluded on the canonical footing if the sample-mean
E_obs ≥ +0.06 + 0.30 = +0.36 ln (≈ +0.16 dex).

## Disclosure (NOT blind with respect to the record)

- **What was seen.** The LEDGER headlines read while choosing this class (criteria section 2) include:
  - CFG31: the Coma UDGs carry a stars-only offset of **+0.397 / +0.357 dex** above the isolated law, in L23's data and
    estimator.
  - CFG58: the Coma UDGs and DF2/DF4 under the cold-mass rule.
- **What it implies.** At Coma-like inputs (M* ≈ 1e8, R_e ≈ 2.5 kpc), P2 predicts about +0.03 dex. If CFG31's offset holds under
  this estimator, P2 is already excluded.
  - That comparison is NOT made here. The estimator, Υ and sample differ, and L23's data are not opened.
  - The comparison is left to a separate lane, using the kill line above.
- **Outside knowledge.** It is also known from the literature, not from data read here, that some group UDGs (DF2/DF4) have
  low dispersions. P2's excess grows steeply as σ_law falls below v_2 ≈ 7 km/s. That regime lies below the declared inputs and
  is not tabulated.

κ = ½ FITTED; footings never pooled; not theory closed. P2's survival is conditional and post-hoc-motivated. Nothing here says
the data favour the framework.
