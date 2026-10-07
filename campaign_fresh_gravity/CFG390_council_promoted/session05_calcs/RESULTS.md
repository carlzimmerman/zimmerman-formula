# Session 5 calcs: results (2026-10-06) — clusters at 0.6

Criteria: `FROZEN_CRITERIA.md` (frozen before the script). κ = ½ fitted; both footings. Promoted into committed lane CFG390 (scripts and outputs byte-identical to the exploratory run). MUTATE: see the correction below.

| test | script | frozen verdict | key numbers |
|---|---|---|---|
| K: shape of X-COP's missing mass M_c = M_HSE − M_law over 100–1000 kpc (12 clusters) | `cluster_shape.py` | **NEITHER** (canonical and alt; b = 0 and 0.2) | slope of log(M_c/M_ph) = **−0.464 ± 0.068**; slope of log(M_c/M_b) = **−0.332 ± 0.071**. All 12 clusters are negative on both. Relaxed 3: "BARYON-SHAPED" by the rule, at 1.9σ on N = 3 (weak). Stellar-file 7: non-discriminating |
| post-hoc (reported only) | `cluster_shape_posthoc.py` | — | d ln M / d ln r: M_c **+1.39**; X-COP NFW minus baryons +1.47; M_HSE +1.54; baryons +1.76; phantom +1.91 |

## What this settles
- **The settling model's natural cluster prediction fails.** If the excess cold fluid settled into the law's target (the model's only attractor), M_c would have the phantom's shape. Instead the excess is more centrally concentrated than the phantom (about 7σ) and than the baryons (about 5σ). The 0.6 component is not target-shaped and not baryon-tied.
- **Post-hoc, its shape resembles an ordinary NFW-like dark halo** (r^1.39 against X-COP's NFW-minus-baryons r^1.47). This is not independent: the NFW columns are X-COP's own fits to the same hydrostatic data.
- **Reading:** where the cold fluid exceeds what the target needs, it behaves like ordinary collisionless cold matter under gravity, not like a settling fluid. In clusters, the working model reduces to a ΛCDM-like halo plus the law.
- Caveats: hydrostatic masses are inherited forward-model reconstructions; spherical symmetry; 5 clusters use an imported stellar ratio; the law uses enclosed-mass g_b.

**CORRECTION (10-06, found while promoting to CFG390):** the original run reported "MUTATE detected (exit 1)", but that exit 1 was a ZeroDivisionError: an exactly baryon-shaped excess has a ratio slope of exactly 0 with zero bootstrap spread. With the guard fixed, the MUTATE runs and returns NON-DISCRIMINATING, NOT BARYON-SHAPED. An exactly baryon-shaped excess sits at slope(M_c/M_ph) = −0.144 ± 0.052 (2.8σ), just short of the frozen 3σ, so **the frozen MUTATE does not fire**. This shows the test separates target-shaped from baryon-shaped excess at only ~2.8σ. The NEITHER verdict does not rest on that separation: it rests on the observed excess being far from BOTH shapes (−0.46 ± 0.07 and −0.33 ± 0.07). The main output is byte-identical after the fix.
