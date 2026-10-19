# CFG845 FROZEN CRITERIA: does H-PRIM (CFG844), calibrated on the dSphs, over-predict SPARC's small rotating dwarfs? (before any script)

**Why.** CFG844's candidate mechanism puts a dense, early-collapsed free cold-energy core in every early-assembling small
system. SPARC's small gas-rich dwarfs also assemble early and sit on the law (CFG828: SPARC Δ +0.02–0.07 dex). If H-PRIM, with
the concentration calibrated on the dSphs and NO new parameter, predicts a clear excess in them, H-PRIM is excluded.

## Calibration (from CFG844 outputs only)
- log10 P = a + γ log10 x, fitted by least squares over CFG844's 25 dwarfs with an excess, x = r_1/2 / r_vir,
  P = ρ_need / ρ_vir,free (mean extra density inside r over the collapse-epoch virial mean of the free share).
- Predicted free-core mass inside radius R of any system: M_free(<R) = P(x) ρ_vir,free (4π/3) R³, x = R / r_vir, using the
  same recipe as CFG844 (f_ret 0.10, M_cat = 6.364 M_b/f_ret, native spectrum, EdS collapse, f_free 0.90), applied only for
  0.01 ≤ x ≤ 0.5 (the calibration span widened by ×2 at both ends; points outside are skipped).

## SPARC sample (fixed before any residual is seen)
- Galaxies with Q ≤ 2, Inc ≥ 30°, and M_b = 0.5 L[3.6] + 1.33 M_HI ≤ 3e9 M_⊙ (SPARC_Lelli2016c.mrt columns); points with
  errV/Vobs < 0.10. g_bar as CFG828 (Υ_disk 0.5, Υ_bul 0.7); g_law with ν_e (canonical a0).
- Predicted g_HPRIM = g_law + G M_free(<R)/R². Residuals Δ_obs = log10(g_obs/g_law), Δ_pred = log10(g_HPRIM/g_law).

## Statistic and classes
- D = mean over galaxies of [median over the galaxy's points of (Δ_obs − Δ_pred)]; error by bootstrap over galaxies (2000, seed 845).
- **H-PRIM EXCLUDED** if D ≤ −0.15 dex with D/σ_D ≤ −3 (it over-predicts the rotating dwarfs).
- **H-PRIM CONSISTENT** if |D| < 0.10 dex.
- **TENSION** otherwise. NOT DIAGNOSTIC if fewer than 8 galaxies have points in the x window.
- Report also the mean Δ_pred (how big an excess H-PRIM predicts there) and the mean Δ_obs.

## Controls
- K1: the calibration reproduces CFG844's median P at the median x within 10%.
- MUTATE (separate output): P set to 0 (no free core) → D must equal the mean Δ_obs (law-only residual).

κ = ½ fitted; cold energy mass required; not theory closed.
