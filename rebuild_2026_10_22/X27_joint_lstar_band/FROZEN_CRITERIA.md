# X27_joint_lstar_band — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** Can L★ be pinned from first principles? Two sides constrain it:
- **Lower side:** D10 / V3_FULL_PICTURE §4.7 put the outer-globular floor at 21.682 (canonical) / 22.849 (alt) pc, after
  the switched re-solve. This is read, not recomputed.
- **Upper side:** the dwarfs. X25 (63a4001236) found that raising L★ lowers every dwarf prediction. CFG821 found the
  classical dSphs want L★ ≤ 22 pc, and flagged that bound as CONDITIONAL: it reflects the dwarf mass shortfall.

This lane computes the dwarf upper bound in two frozen modes and states the joint band per footing.

Standing rules: κ = ½ FITTED. Footings never pooled. No new constant enters the verdict mode M0. M1 uses X24's floor c₀
only as a profiled nuisance, so that the mass shortfall cannot fake an L★ bound. Not "theory closed". Nothing here may say
the data favour the framework.

## 1. Data (read-only)

X1 `x1_per_system.csv`, per footing. Systems: MW ultra-faint (31), bright M31 (25), M31 others (5), MW classical (8),
LG field (13). That is N = 82. The individually reported systems (Crater II, Antlia II, CVn I, Sagittarius) and the M31
dEs are reported separately.
- For L★ ∈ {0, floor, 24, 90}: Δ_L = `Delta[AQUAL + EFE L*0 (exact MOND + EFE)]`, `Delta[v3 L*floor]`, `Delta[v3 L*24]`,
  `Delta[v3 L*90]` (E-W, v3s statics = v3 where D·P ≥ 0), with s_L their sdMC.
- Between grid points, Δ is interpolated linearly in log L★, from the floor to 90 pc. The grid is coarse between 24 and
  90 pc, so any bound that lands there is reported as the bracket "(24, 90)" alongside the interpolated value.
- g_obs = 3σ_c²/r₁₂ (X24's σ_c, binary-corrected). g_pred(L★) = g_obs · 10^(−Δ_L).

## 2. Modes (per footing)

- **M0 (verdict): literal v3s, no extra.** χ²(L★) = Σ (Δ_L/s_L)².
  - L★,up = the smallest L★ > L★,min where χ² − χ²_min = 3.84, with the minimum taken on [floor, 90].
  - Absolute fit quality is reported as χ²_min/N.
- **M1 (reported qualifier, verdict-bearing only if stated in §3): v3s + floor nuisance.**
  - Residual: r = log g_obs − log(g_pred(L★) + 3c₀²/r₁₂). c₀ is profiled (bounded 0–30 km/s) at each L★ grid point.
  - L★,up is defined as in M0, on the profiled χ².
- In each mode, if χ² is monotone rising from the floor and never reaches Δχ² = 3.84 by 90 pc, L★,up is "> 90" (no bound).

## 3. Joint band and verdict (per footing; the class needs both footings to agree)

Band = [floor, L★,up(M0)].
- **PINNED** if the band is non-empty and narrower than a factor 1.5 (L★,up / floor < 1.5).
- **BOUNDED** if it is non-empty and wider.
- **EMPTY** if L★,up(M0) < floor.

The M1 band is reported as the qualifier: "with the dwarf shortfall supplied by a floor, the band is …". If M0 and M1
disagree in class, the label carries [SHORTFALL-DRIVEN].

## 4. Checks (all must pass; `--mutate` must fail K0)

- **K0:** X19's H plain medians of the iso column are reproduced (as X24). The four Δ columns are present for all
  82 systems. The floors read 21.682 / 22.849.
- **K1:** at L★ = floor, interpolation returns the floor column exactly; at 24 and 90 likewise (1e-12).
- **K2:** M1 at c₀ = 0 equals M0, to 1e-10 in χ².
- **K3:** peak RSS < 1 GB.
- **MUTATE:** the sign of every Δ_L − Δ_0 difference is flipped (screening made to raise g_pred). K0's column check stays
  valid, so the mutation must also fail **K4**.
- **K4:** χ²(M0) is non-decreasing from the floor to 24 pc on both footings. X25's sign result predicts this; under the
  mutation it must fail.
