# CFG741: P-wave heating cannot be the two-sector selector

**Label: CLOSED.** The energy the polarization radiates while settling is E_rad = (2/3) M_b V_f² ln Λ, exactly (sympy). It
could heat at most 50% of the cold component it would need to evict from a galaxy, even with perfect absorption. And the
ratio is the same for galaxies and clusters, because the budget is scale-free.

- **Criteria:** `FROZEN_CRITERIA.md` (c659126e2), committed alone first.
- **Script:** `python3 cfg741.py` (sympy, seconds, exit 0) → `cfg741.out`, `cfg741_results.json`. `CFG741_MUTATE=1` exits 1: a
  non-SI quadratic W_nl breaks the ln Λ form.
- **Settings:** κ = ½ FITTED; the cold energy's mass is required; no particle species; not "theory closed".

| ln Λ | Q galaxy, C/b = 5.3 | Q galaxy, C/b = 10 | Q cluster, C/b = 5.3 |
|---|---|---|---|
| 2 | 0.17 | 0.09 | 0.17 |
| 4 | 0.34 | 0.18 | 0.34 |
| 6 | 0.50 | 0.27 | 0.50 |

Q = E_rad/E_need = (4/9) ln Λ/(C/b), with no M_b and no a₀.

## Reading
1. **Too little energy.** The deep-regime energy density at the minimum is −√a₀ g_N^{3/2}/(6πG), so the whole halo releases
   only (2/3) ln Λ in units of M_b V_f². Lifting the cosmic share of cold mass to the galaxy's dispersion costs (3/2)(C/b) in
   the same units.
2. **No discrimination.** The law is scale-invariant in its deep regime, so any energy budget it sets is the same fraction of
   the binding energy for every system. Galaxies cannot be singled out from clusters this way. Galaxies with missing baryons
   are evicted *less*.
3. **Consequence for the two-sector problem.** A selector that keeps cold mass out of galaxies but in clusters must carry a
   scale that the deep law does not have:
   - a **velocity scale** between galaxy and cluster dispersions (about 250–700 km/s; a "warm" cold component);
   - or a dependence on the baryon fraction or gas state of the system.

   Neither is in {G, a₀, c} as a natural combination, so either would be a new constant or new physics.
