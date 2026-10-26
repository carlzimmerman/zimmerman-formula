# X49_dwarfs_route_e_floor — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** THEORY_STATEMENT_2026-10-26 lists the dwarf spheroidals as not regraded. Under route E with X43's core
rule, Σ_core = max(a₀/(2πG), η Σ_coll), do the Local Group dwarfs fit?

Every dwarf here is far below the ~10¹² M☉ crossover, where Σ_coll ≪ the floor. So the halos are **pure a₀-floor Burkert
halos**, ρ₀r₀ = a₀/(2πG), and the grade is independent of c_f (X48 A2 still running).

Standing rules: κ = ½ FITTED. Footings never pooled. Route E: Newtonian gravity on baryons + cold dark energy. Cold dark
energy is not matter. Not "theory closed". Nothing here may say the data favour the framework.

## 1. Data and prediction

- **Data:** X1 `x1_per_system.csv` per footing.
  - g_obs = 3σ_c²/r₁₂ (E-W, r₁₂ = (4/3) rh), with σ_c binary-corrected by X1's rule (as X24).
  - The error on log g_obs is `sdMC[Newton]` (the data-side MC spread).
  - M_b = 10^logMstar (Υ_V = 2), and M_b(<r₁₂) = M_b/2.
- **Halo mass (PRIMARY):** EM1's committed SPARC relation, lg M200 = 11.18 + 0.90 (lg M_b − 10) (background A),
  **extrapolated** below SPARC's baryon range (disclosed). R200 is at 200 ρ_c(0), with h from background A.
- **Halo:** Burkert with ρ₀r₀ = Σ_core(M200), from X38's solver with its A1 compact-root and saturation rule (counted). The
  check that Σ_coll < floor is printed for every system.
- **Prediction:** g_pred(r₁₂) = G [M_b/2 + M_h(<r₁₂)] / r₁₂². E = log(g_obs / g_pred). Hosted dwarfs are treated as
  isolated (no tidal stripping of the halo; disclosed, and it can only lower g_pred).
- **Reported variant:** M200 = 6.364 M_b (fair share, a lower bound for systems that lost baryons).

## 2. Grade (per footing)

- **Classes:** MW ultra-faint, bright M31, M31 others, MW classical, LG field (X19/X24 conventions). Crater II, Antlia II,
  CVn I, Sagittarius and the M31 dEs are reported individually.
- **Per class:** median E, with a bootstrap sd (10 000 resamples, seed 20261026, E_i ~ N(E_i, s_i)), and Z = median/sd.
- **REPRODUCED** if |Z| < 2.
- **Verdict:** **FLOOR HALOS FIT THE DWARFS** if all five classes are REPRODUCED on both footings. Otherwise **FAIL:
  <classes with sign>** (UNDER = the data above the prediction).
- **Reported:**
  - Spearman(E, log M★) over all five classes, i.e. whether X24's mass trend survives;
  - the fair-share variant;
  - comparison with X24's c₀ floor;
  - the median r₀ per class;
  - the saturated count.

## 3. Checks (all must pass; `--mutate` must fail K1)

- **K0:** X24's per-class plain medians of the X1 iso column are reproduced (data loaded correctly).
- **K1:** at M200 = 10¹² M☉ the solver returns ρ₀r₀ = Σ_a₀ to 1e-10, and M(<R200) = M200 to 1e-8.
- **K2:** with the halo switched off, E equals X1's `Delta[Newton]` to 0.03 dex (MC medians vs point values).
- **K3:** peak RSS < 1 GB; one thread; seconds.
- **MUTATE:** Σ_core = Σ_a₀ / 10 (the floor broken by a factor of 10); K1 must fail.
