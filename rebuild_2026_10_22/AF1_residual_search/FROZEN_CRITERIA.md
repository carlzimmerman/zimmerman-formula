# AF1_residual_search: frozen criteria
Committed alone, before any script or number of this lane. Owner's go, 2026-11-02. Id AF1: no AF directory and no AF1 lane in git log.

**Not blind.** Read before freezing: READMEs of BF1, SL1, LW1, LM1, GM1, UX3, UX6, X21, NQ1's ranking, so I know the deficit tracks gas in relaxed clusters, that a pure gas term breaks discs and dies on the Bullet, that X21 detects KT and not gas mass, and the published misses of the law. I read loaders and file layouts, not new residuals. Any hit that re-finds those is not independent of them. kappa = 1/2 FITTED. Footings canonical 9.3603e-11, alt 1.1312e-10, reported separately, never pooled. No theory claim from a fit. Cold sector retired; if data point at a collisionless component that is stated as data. Not theory closed. Nothing here says the data favour the framework. No Planck or LCDM input.

## Target and rows
r = log10(g_obs / g_law), g_law = g_N/2 + sqrt(g_N^2/4 + a0 g_N). Fixed Upsilon 0.5, 0.7. Samples, one row per system or radius, measuring different things:
- SPARC, BF1's cuts, radius rows, circular speed.
- LITTLE THINGS, one outer point per galaxy, RT1's rows, IC 1613 removed.
- 63 groups, r = 2 x (log sigma_obs - log sigma_law), UR-record Jeans path with the law, a dispersion.
- X-COP, 7 clusters with stars on disk, x = 0.1, 0.2, 0.3, 0.5, 0.7, hydrostatic mass.
- Shear stacks: lg-gas-mass terciles x 8 radial bins, LM1's dump, r = log10(data/law), a projected excess surface density, gas +0 as dumped, f* 0.034, h 0.672. Cells with data/law <= 0 are dropped and counted. KT terciles are a second, overlapping view, used only inside shear and never pooled with the first.
- Local Group dwarfs, X1's systems in LW1's five classes, plain law, IC 1613 removed, half-light dispersion.
- Milky Way, Ou 2024 curve on the McMillan baryon model, radius rows.
Hydrostatic and lensing masses differ (LF1, GM1); nothing corrects for that here and the table says which method each row has.

## Stage 1 known answers (K)
K1 X-COP mean, rms +0.467, 0.476 canonical; +0.434, 0.444 alt, each within 0.002. K2 groups mean +0.0100, -0.0103, within 0.002. K3 IC 1613 E -0.593 canonical within 0.01. K4 all-cluster shear data/law within 0.02 of LM1's 8 values, by summing the terciles. K5 dwarf plain medians within 0.03 of LW1's five classes. K6 MW McMillan cell vc(R0) within 2 km/s of LW1's Newton 177.09 before the law. A failed K stops grading of that sample; it's reported and the sample left out.

## Stage 2 rules
Pi reduction by computing the rank of the dimension matrix. Variables that are functions of other groups (baryonic potential and baryonic dynamical time from y and ell) are declared redundant and not counted twice.
Each variable is tagged CLEAN (from baryons, photometry or environment) or LEAKY (sigma, T under hydrostatic, V, observed potential or time, anything containing g_obs). T on the shear rows is CLEAN since lensing doesn't use it. LEAKY rows are shown and can't survive.
**Statistics.** Spearman between systems (system means) and within systems (demeaned rows, sign-flip null per system that keeps a curve's autocorrelation); kNN mutual information as a second column. y partialled out (rank residual on a spline of log y) as a third column. Null: permutation, adaptive to 20000. Family: every CLEAN variable x sample x {between, within}, counted in the output; Holm at 0.05 per footing.
**Noise leak mock.** Each sample's rows regenerated from the law with per-system lognormal error in g_N (SPARC 0.10 dex, LT 0.15, groups 0.10, X-COP 0.05, shear 0.05, dwarfs 0.15, MW 0.05), no signal; a variable's |rho| must exceed twice its mock |rho|.
**SURVIVES WITHIN:** CLEAN, Holm-significant in at least one sample, on both footings, beats the mock.
**Sample identity.** A random per-sample constant is the label control. Reported per variable: AUC for cluster vs galaxy; pooled equal-sample-weight R^2 of r on V (binned), against V permuted inside samples, a null that keeps everything a label carries; leave-one-sample-out R^2 from a binned median of the other samples, with coverage of the left-out range.
**CARRIES ACROSS:** SURVIVES WITHIN, pooled excess p below the family's Bonferroni line, LOSO R^2 > 0 and above the label control in at least half of samples with coverage >= 0.5. **LABEL ONLY:** AUC >= 0.95, or pooled gain fails to exceed the stratified null. A variable can be neither.
**Separability:** for pairs among the top CLEAN variables, r on a 6x6 quantile table, f(a)+h(b) by backfitting, f(a) x h(b) by rank-1 SVD, full table as the ceiling, on the train half, scored on the held-out half, in clusters, in galaxies, and pooled. Readings: ADDITIVE, PRODUCT if within 10 % of the ceiling's rms-gain and the other isn't; NEITHER; NOISE-LIMITED if the ceiling doesn't beat constant.
Stage 2 is reported on its own. If no variable SURVIVES WITHIN, Stage 3 doesn't run, and that is the result.

## Stage 3, only on survivors
PySR 1.5.9 if it runs without any download, with fitted constants allowed and counted, y always offered. Train: half of each sample by sha256(system name) parity, frozen, each sample total weight 1, weight per row from 1/(sigma^2 + floor^2), floor 0.05. Holdouts never in fitting or selection: other half, the Bullet, IC 1613. Controls: scrambled (target permuted among systems inside samples) and planted (r replaced by a known form plus noise, must be recovered with holdout rms within 20 % of the noise).
Per Pareto equation: complexity, constants, per-sample holdout rms and median against the law and against the label control (law + train constant per sample).
**TRANSFERS:** holdout rms under the label control in at least 5 of 7 samples, no sample over 1.1 x the law's rms, canonical and alt, and better than the scrambled front at the same complexity. Margins printed beside frozen lines: X-COP |mean| <= 0.05, rms <= 0.10 (BF1); SPARC rms <= 1.3 x law, |median| <= 0.06 (BF1); groups |Z| < 2; dwarf classes |Z| < 2; shear cells chi^2; IC 1613 |Z| < 2 with sE 0.075; Bullet by UX6's classes where the equation has only local y, f, y_gas, else NOT EVALUABLE. **A margin isn't a pass of the keys:** the 15-key grader isn't run. **NO FORMULA TRANSFERS** is a result.
Stage 4 only for a constant in a TRANSFERS equation: combinations of c, G, rho_DE, a0, f_b counted, chance rate stated, a match labelled a match.

## Method
MUTATE twin: a0 x 1.5, K1 and K2 must fail. Planted Stage 2: add r -> r + 0.3 log10(1 + y_gas) on a noise copy, must rank first; a pure-noise variable must not survive. Stages 1, 2 rerun byte-identically. Failed checks are reported. One thread nice 15 for 1-2; Stage 3 behind BF1 and UX7, compute_queue if it can start, else nice 19, at most 2 threads, resumable. Commit this directory only, no push.
