# CFG103 referee note: the capped-fluid growth suppression and engagement, re-derived with an independent solver

- **Scope.** The orchestrator asked for one headline per lane, re-derived with the referee's own code.
  - CFG103 re-derived CFG43: the a₀–Λ tie on a conserved fluid's stress cap.
  - The quantitative core of the obstruction is how the cap suppresses linear growth, ν_min(k), and how that compares with where the cap engages in galaxies, g0 = ν_M/(x_F ν_min).
- **Method.** `CFG103_referee_growth.py` (log `.out`) is the referee's own two-fluid linear solver (scipy LSODA, rtol 10⁻¹⁰). It implements CFG103's frozen specification (FROZEN_DOCSTRING A3(b)) and imports nothing from CFG43 or CFG103.

| quantity | CFG43 | CFG103 | this re-derivation |
|---|---|---|---|
| c_s²(z = 0) at ν* = 1 | 5.78 × 10⁻³ | 5.8 × 10⁻³ | 5.79 × 10⁻³ |
| growth ratio at ν* = 1, k = 0.5 / 2 / 10 / 30 Mpc⁻¹ | 0.140 / 0.099 / 0.080 (different settings) | 0.139 / 0.092 / 0.084 / 0.070 | 0.1393 / 0.0924 / 0.0836 / 0.0704 |
| ν_min(5%) at k = 0.5 / 2 / 10 / 30 Mpc⁻¹ | 2.24e4 / 2.00e5 / 2.16e6 / 1.12e7 | 2.17e4 / 1.74e5 / 1.95e6 / 1.01e7 | 2.168e4 / 1.741e5 / 1.948e6 / 1.013e7 |
| exponent of ν_min(k) | 1.48 | 1.501 | 1.501 (local 1.503, 1.501, 1.500) |
| a₀ at Ω_Λ = 0.685 | 9.3603 × 10⁻¹¹ (Ω_Λ 0.6847) | 9.3624 × 10⁻¹¹ | 9.3623 × 10⁻¹¹ |
| ν_M at M_b = 10⁹ / 3 × 10¹¹ | 3.587e5 | 3.587e5 / 2.071e4 | 3.5864e5 / 2.0706e4 |
| g0, frozen primary (M_h = M_b/f_b, k = π/R, F = ½), d = 5% / 20% | — | 0.205 / 0.606 | 0.205 / 0.606 (10⁹); 0.205 / 0.608 (3 × 10¹¹) |

**Verdict.** CFG103's growth and engagement numbers reproduce to three digits from an independent solver.
- **What that establishes:** the obstruction's quantitative core is not a code artefact.
  - Growth is suppressed below 5% only for ν* above about 10⁴–10⁷, scaling as k^1.5.
  - The cap engages in galaxies at ν_M ∝ M_b^−1/2.
  - At the frozen primary the ratio g0 is about 0.2, below 1, so the window is empty.
- **Differences from CFG43:** they are the settings CFG103 already identified (grid, z_i, Ω_c, radiation), not physics.

**Limits:**
- **Only the frozen primary and the four-k table are re-derived here.** CFG103's convention grid and its ceilings (11.3 up to about 10⁵) are not. Nor are the A1 dispersion and Dirac count, or the A2 FRW flatness.
- **The window's conclusions carry CFG103's caveats.** The loophole CFG103 flagged is a nonlinear or overdense collapse escaping the linear suppression, which is untested. Nor is the growth-suppression tolerance derived.

κ = ½ stays fitted. Nothing here says the data favour either model, or that the theory is closed.
