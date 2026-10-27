# X52_dwarf_tidal_truncation — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** X51 (cooling-floor halo masses) fits all five LG dwarf classes on canonical. On alt the MW ultra-faints are
over-predicted (Z −2.77), and Crater II sits at −0.97, with halo stripping not modelled. **Does tidal truncation of hosted
dwarfs' halos by their route-E host close it?**

Standing rules: κ = ½ FITTED. Footings never pooled. Route E, Newtonian, a₀-floor Burkert dwarf halos with X51's M200 rule.
Cold dark energy is not matter. Not "theory closed". Nothing here may say the data favour the framework.

## 1. The truncation

- **Host:** baryons from X1's MHOST (MW 6×10¹⁰, M31 10¹¹ M☉) as a point mass, plus a route-E halo. M200 comes from EM1's
  relation on the host's baryons. The core is X43's rule with c_f = 4 (η = 14.83; disclosed, since the host's M(<d) at
  30–250 kpc barely depends on the core).
- **Jacobi radius** at the **current** distance d (X1's `d_host_kpc`). This is a lower bound on stripping; pericentres are
  not on disk for M31.
  - r_t = d · [ m(<r_t) / ((2 − γ_h) M_host(<d)) ]^{1/3}, where γ_h = d ln M_host / d ln r at d. Solved by fixed point.
  - m includes the dwarf's stars.
- **Truncation:** M_h,dwarf(<r) = M_h(<min(r, r_t)). Field dwarfs (LG field) are not truncated.
- **Prediction and grade:** as X51 (g_pred at r₁₂, per-class bootstrap, |Z| < 2 for all five classes, on both footings).
  The label is **TRUNCATION CLOSES THE DWARFS** or **FAIL: <classes>**.
- **Reported:** r_t / r₁₂ per class (median); Crater II, Antlia II and Sagittarius individually; how many systems have
  r_t < r₁₂.

## 2. Checks (all must pass; `--mutate` must fail K1)

- **K0:** with truncation off, X51's class medians are reproduced to 1e-9.
- **K1:** for a point-mass host (γ_h = 0) and point-mass satellite, r_t equals d (m/2M)^{1/3} to 1e-8.
- **K2:** truncation never raises g_pred (checked for every system).
- **K3:** peak RSS < 1 GB; seconds.
- **MUTATE:** the Jacobi denominator uses (2 + γ_h); K1 must fail. (At γ_h = 0 it is unchanged, so K1 is evaluated at
  γ_h = 1 under the mutation.)
