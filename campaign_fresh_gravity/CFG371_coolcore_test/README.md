# CFG371: cool-core vs non-cool-core clusters, a falsification test of the settling principle

Criteria: `FROZEN_CRITERIA.md`, committed alone first in b5624e3d8.

**Frozen verdict: SUPPORTED** (as computed): Spearman rho(t_c, X_in) = +0.75 (p = 0.031, N = 7, both footings); 12 clusters +0.81 (p = 0.001). MUTATE (permuted t_c) gives CONTRADICTED, rc 1.

**But the result is a shared-variable artifact (POST-FREEZE, labelled; `cfg371_robustness.py`).** t_c is proportional to 1/rho_gas(core), and X_in divides by M_b(<0.1 R500). Clusters with little core gas get BOTH a long t_c and a large excess-per-baryon.

| statistic (vs t_c) | 7 primary | 12 |
|---|---|---|
| frozen X_in = excess / (5.364 M_b) | +0.75 | +0.81 |
| excess / M_tot(<0.1 R500) (gas-free normalisation) | **+0.04** | **+0.10** |
| excess / M500 | **-0.71** | -0.47 |
| frozen X_in, partial given M500 | +0.93 | +0.85 |
| frozen X_in, partial given core gas fraction | +0.49 | **-0.03** |
| rho(t_c, core gas fraction) | -0.68 | -0.83 |

**Reading.** Once the normalisation does not divide by the gas, or the gas fraction is controlled, the correlation vanishes or reverses. The data show no evidence that fast-cooling cores carry less dark excess. **The cluster prediction of the cooling-settling principle is NOT supported.** (Mass is not the confounder: the partial given M500 stays high. The gas fraction is.) What the data DO show: excess per unit BARYON is large where the gas is depleted. That is the baryon-deficit / never-collected pattern (CFG364-365), not cooling.

Caveats: N = 7 / 12; isothermal kT; hydrostatic masses; inner radius 0.1 R500.
