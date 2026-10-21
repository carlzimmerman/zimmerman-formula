# CFG940 AMENDMENT A1 (POST HOC, 2026-10-20, after the frozen K-stage failed, BEFORE any residual of this lane)

Frozen criteria: 798e98d78. Written after the first K-only run (`--mode K`) exited 2 on K3, and before any rotator residual,
g_bar, mean E, D or class of this lane was computed (the K-only mode stops right after the K-tests; the only residuals it
computes are the record reproductions K5/K6). The failed run's outputs are kept as `cfg940_K_preA1.out` and
`cfg940_results_K_preA1.json`.

## A1-1. K3's R_max tolerance ignored the integer-arcsec rounding of D_PV

**What failed.** K3 requires the recomputed R = (D_PV/2) × Dist to match the tabulated R_max to ≤ 0.051 kpc (the 0.05 kpc
rounding of R_max plus 0.001 slack). Measured: max |dR| = 0.053 kpc. The galaxy is AGC111164: D_PV = 28 arcsec, Dist = 5.11
Mpc gives R = 0.347 kpc, tabulated 0.4. (V_rot passed: max |dV| 0.92 km/s ≤ 1.0.)

**Why it is the tolerance, not the data.** D_PV is tabulated as an integer (arcsec), so it carries its own ±0.5 arcsec
rounding, which the frozen tolerance left out. At 5.11 Mpc that is ±0.012 kpc. Any D_PV in [28.26, 28.5) arcsec gives
R ∈ [0.350, 0.353] kpc, which rounds to the tabulated 0.4 and lies within 0.006 kpc of the recomputed 0.347. The two tabulated
numbers are consistent once both roundings are counted.

**The change.** K3's R_max tolerance becomes, per galaxy, **tol_R = 0.051 kpc + 0.5 arcsec × Dist** (in kpc). Nothing else
in K3 changes (V_rot ≤ 1.0 km/s stays).

**What does NOT change.** The primary R stays the recomputed (D_PV/2) × Dist (criteria section 3). It is the more precise of
the two: its rounding error is about ±2 % for AGC111164, against ±12.5 % for the tabulated 0.4. Variant V16 (tabulated R_max)
still reports the other choice.

## A1-2. Disclosure from the same K run (no rule changed)

- **K2 (helium):** the best passing factor is f_He = 1.36 (max |diff| 0.013 dex). f_He = 1.33 misses the 0.015 bar on at least
  one galaxy (max 0.018). By the frozen rule (f_He ≥ 1.33 → helium included), M_bary is used **as tabulated** in estimator A.
  Estimator B keeps the frozen 1.33 × M_HI for gas, so B's gas is about 2 % (0.01 dex) lower than the paper's helium
  convention. B is a bracket, and this is far below its spread.
- **K1:** passes with V_cor (25/25); with V_rot only 17/25 pass, so the paper's log M_dyn uses V_cor.
- **K4 (decision):** the inclination error is already inside e_Vrot/e_Vcor (rms residual 0.33 km/s with the i-term vs 2.88
  without), so it is not added again.
- K0, K5 (CFG828 exact), K6 (CFG919 DW exact), K7 passed.

κ = ½ FITTED; footings never pooled; not theory closed.
