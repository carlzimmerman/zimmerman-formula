# CFG432 FROZEN CRITERIA: does the unsettled cold mass in X-COP clusters have the gas's shape?

Frozen before any CFG432 script exists. kappa = 1/2 is FITTED; both footings reported, never pooled. No dark-matter particle; the cold fluid's mass is still required. On-disk data only, no downloads.

## Door
CFG379 (bookkeeping B) and DeepSeek T15: clusters hold about their full cosmic cold share, roughly half of it beyond the phantom target, inside R500. The surviving reading is cold fluid that sits inside R500 without settling. CFG371 (post-freeze) found the excess per baryon is large where the gas is depleted; the record's hypothesis is that the unsettled cold mass tracks the (depleted) gas. This lane turns that into a radial PROFILE test with no new fit.

Overlap disclosed: CFG440 session 05 (test K) already measured the slope of log(M_c/M_b), with M_b = gas + stars, over 100-1000 kpc at b = 0 and 0.2 (-0.33 +- 0.07, "NEITHER"). CFG432 differs: gas alone (the hypothesis's tracer), radii in units of each cluster's own R500, b = 0.3, a pre-declared constancy tolerance, a cluster-level constancy requirement, and an NFW-shape alternative with no fit. The CFG440 number is known in advance; the rule below is not tuned to it.

## Data (on disk)
`real_research/data/xcop/<cluster>/`: 12 X-COP clusters (Ettori+2019 / Eckert+2022 products).
- M_HSE(<r) = `M_FORW` (hydrostatic forward model), radius in kpc.
- M_gas(<r) = `MGAS` from `_fgas_profile.fits`, radius in R/R500 with the file's own `R500` header (kpc).
- M_star(<r) = `MSTAR_SMOOTHED` (HDU 2) for the 7 clusters with a stellar file; for the other 5, M_star = (median over the 7 of M_star/M_gas at each radius) x M_gas (the CFG440 / cluster_audit convention). Sensitivity reported (not decisive): M_star = 0.10 M_gas for the 5 (CFG371/379 convention).
- R200 for the NFW shape: `xcop_r500_ettori2019.json` (Mpc).

## Quantities
- Grid: 16 log-spaced radii from 0.1 to 1.0 R500 per cluster (own R500). Log interpolation of the tabulated profiles.
- M_b = M_gas + M_star; g_b = G M_b(<r)/r^2 (spherical, enclosed mass).
- Law: M_law = nu(g_b/a0) M_b with nu(y) = 1/(1 - exp(-sqrt(y))); M_ph = M_law - M_b.
- a0 footings: canonical 9.3603e-11, alt 1.1312e-10 m/s^2 (CFG4_common).
- Hydrostatic bias: M_true = M_HSE/(1 - b), b = 0 and b = 0.3, both reported.
- Unsettled cold mass: M_u(<r) = M_true - M_b - M_ph = M_true - M_law.
- Gas-tracking ratio Q_gas(r) = M_u/M_gas. NFW-shape ratio Q_nfw(r) = M_u/m_NFW(r) with m_NFW(<r) proportional to ln(1+c x) - c x/(1+c x), x = r/R200, c200 = 4 fixed for all clusters (no fit). c200 = 3 and 5 reported as sensitivity, not decisive.
- Points with M_u <= 0 are excluded from the slope; a cluster with fewer than 6 valid points of 16 is dropped from that cell, and the count is reported. A cell with more than 3 clusters dropped is flagged UNDERPOPULATED and cannot pass either shape.

## Statistic
Per cluster i: s_i = OLS slope of ln Q against ln r over the valid grid points (d ln Q / d ln r). Sample: S = median of s_i over clusters; sigma = std of the median over 2000 bootstrap resamples of clusters (seed 432). A zero bootstrap spread counts as z = 0 if |S| < 1e-12, else z = infinity.

Tolerance T = 0.15 (over one decade in r, Q changes by at most a factor 10^0.15 = 1.41).

For each shape (gas, NFW):
- **SHAPE-CONSISTENT** if |S| <= T AND |S|/sigma <= 2 AND at least 8 of 12 clusters have |s_i| <= 2T = 0.30.
- **SHAPE-EXCLUDED** if |S| > T AND |S|/sigma > 3.
- otherwise **SHAPE-INCONCLUSIVE**.

Cell verdict (per footing x b):
- **GAS-SHAPED**: gas CONSISTENT and NFW EXCLUDED.
- **NFW-SHAPED**: NFW CONSISTENT and gas EXCLUDED.
- **BOTH / NON-DISCRIMINATING**: both CONSISTENT.
- **NEITHER**: both EXCLUDED.
- **INCONCLUSIVE**: any other combination.

Discrimination check (C1, must pass for any shape verdict to count): the median over clusters of |d ln(m_NFW/M_gas)/d ln r| on the same grid must be >= 2T = 0.30. If it fails, every cell is NON-DISCRIMINATING by construction.

Headline: if all four cells (2 footings x 2 b) give the same verdict, that is the headline. Otherwise the headline is "DEPENDS ON b / FOOTING" with all four listed. The hypothesis "unsettled cold mass tracks the gas" is SUPPORTED only by GAS-SHAPED in all four cells, CONTRADICTED if gas is SHAPE-EXCLUDED in all four, otherwise NOT SETTLED.

## Controls
- C1 discrimination (above).
- C2 data identity: every profile positive and finite on the 0.1-1.0 R500 grid for all 12 clusters.
- C3 law identity: nu(y) -> 1 + 1/sqrt(y) form checked numerically: |M_law/M_b - nu| < 1e-12 at the grid; and nu(y) >= 1.

## MUTATE (`--mutate`, writes `cfg432_MUTATE.out` and `cfg432_results_MUTATE.json`)
Two deliberately broken inputs, both run on the canonical footing, b = 0:
- **M-A planted gas shape (positive control):** M_HSE replaced by M_law + q_i M_gas, with q_i = the cluster's real M_u/M_gas at 0.5 R500 (if that is <= 0, q_i = 0.5). The cell MUST return GAS-SHAPED.
- **M-B shuffled radii (negative control):** each cluster's M_HSE values on the grid are randomly permuted among the 16 radii (seed 432) before M_u is formed. The cell MUST NOT return GAS-SHAPED or NFW-SHAPED.
The MUTATE run exits 1 (= detected) only if BOTH M-A and M-B behave as required; otherwise it exits 0 and the main verdict is flagged as resting on an unvalidated test.

The main run exits 0 if C1-C3 pass, 1 otherwise (failures kept and reported, never hidden).

## Reported, not decisive
Per-cluster s_i table; Q_gas at 0.1, 0.5, 1.0 R500; fraction of points with M_u <= 0; the alternative stellar convention; c200 = 3 and 5; X-COP's own NFW-minus-baryons slope (not independent: fitted to the same hydrostatic data); the 3 relaxed clusters (A1795, A2029, A2142) alone.

## Caveats declared in advance
Inherited forward-model hydrostatic masses with tabulated (radially correlated) errors, which are not propagated into s_i; spherical symmetry; enclosed-mass g_b; 5 clusters use an imported stellar ratio; b is a scalar constant in r.
