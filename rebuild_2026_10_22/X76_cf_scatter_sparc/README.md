# X76_cf_scatter_sparc: SCATTER FAILS (canonical P_line 0.001; alt 0.000). Native c_f scatter makes SPARC worse, not better

Criteria: `FROZEN_CRITERIA.md` (12d45b6b56), committed before the script. Script `x76_cf_scatter.py`. Outputs:
`x76_cf_scatter.out` / `_results.json`, MUTATE `x76_cf_scatter_MUTATE.*`, and the base exec's `x74_*_c4_*` (X74 run at c_f 4,
redirected here).

**Door.** X48 FP1 shows c_f is a per-halo distribution. Each SPARC galaxy draws its own c_f from A3's nine ng 64
per-seed values (2.44–15.09), with 10 000 assignments.

| set | footing | P_line (both bgs) | median Υ 16/50/84 (A bg) | rms 50 % | label |
|---|---|---|---|---|---|
| A3 nine (graded) | canonical | **0.001** | 0.37 / 0.41 / 0.45 | 0.0831 | **SCATTER FAILS** |
| A3 nine (graded) | alt | 0.000 | 0.31 / 0.34 / 0.36 | 0.0843 | SCATTER FAILS |
| pooled 18 (reported) | canonical | 0.000 | 0.33 / 0.36 / 0.38 | 0.0860 | SCATTER FAILS |
| pooled 18 (reported) | alt | 0.000 | 0.30 / 0.30 / 0.34 | 0.0871 | SCATTER FAILS |

For comparison, one median c_f 7.74 for every galaxy (pre-read P2) gives Υ 0.47, and c_f 4 for every galaxy (X73) gives 0.56.

**Mechanism.** η ∝ c^{5/4} is convex, and the rule is a max(). A galaxy that draws a low c_f only switches the rule off,
so its Υ is capped near the c_f 4 value (0.56). A galaxy that draws a high c_f (9–15) switches the rule on even at
moderate mass, and its core mass grows like c^{5/4}. With the median c_f near the switch-on point, more galaxies are
pushed down than lifted, and the median Υ falls from 0.47 to 0.41.

FP2 says the high-c members are lower bounds, so the true scatter would push the median Υ further down.

**Checks:**
- **K1:** all galaxies at c = 4 reproduce X73's SPARC numbers exactly.
- **K2:** all galaxies at c = 7.74 reproduce pre-read P2 exactly.
- **K3:** the base exec's X74 K1 identity passes.
- **MUTATE:** c × 2 moves the canonical median Υ from 0.41 to 0.30, so the harness is sensitive.

**Not covered:** clusters and groups are not regraded. With scatter, the convex η raises the stacked cores further.

**Reading.**
- With native collisionless c_f, whether used as a median or as its own scatter, route E's collapse branch over-masses
  the cores of bright galaxies and fails the SPARC Υ floor.
- The canonical pass needs c_f(10¹²) ≤ 7.0 for every galaxy. The native distribution puts about half the halos above
  that, so the c_f 4 pass rests on the external c_f.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

## Definition note (fix-forward, 2026-10-29; affects X72/X74/X76 equally; reported)
X43/X70's η matches the core at **r₀ = r_f/c_f, where r₀ is the core radius**. X48 measures **c_f = r_vir/r₋₂**. For the smooth core ρ ∝ (1+x²)^{−3/2}, the slope is −3x²/(1+x²), so r₋₂ = √2 r₀. For Burkert, r₋₂ ≈ 1.52 r₀.

- **The consistent native input** to η is therefore √2 × c_f(X48): the median goes from 7.74 to about 10.9, and η rises by 2^{5/8} = 1.54.
- **The external c_f = 4**, read as r_vir/r_s of a formation-time NFW (r_s = r₋₂), corresponds to a core c of 4√2 = 5.66, not 4.
- **X74 as frozen plugs X48's number in directly.** The frozen criteria fixed "X48's definition r_vir/r₋₂, unchanged", so X74's grade stands as frozen. On SPARC this makes X74 lenient: canonical median Υ falls monotonically with c (0.56 at 4, 0.51 at 7, 0.48 at 7.74). The consistent mapping fails SPARC harder.
- **Clusters:** the same √2 raises the cluster c too. The c_f 8 sensitivity (`sens_cf8.log`) already shows six keys going OVER.

None of this changes any frozen grade. It means the native-c_f fail is conservative.
