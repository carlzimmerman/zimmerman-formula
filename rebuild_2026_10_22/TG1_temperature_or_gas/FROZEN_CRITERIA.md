# TG1_temperature_or_gas: FROZEN CRITERIA (committed alone, before any script or new number)

Owner's go, 2026-11-02. Id checked: no TG1 directory, no TG1 in git log. **Not blind.** Read before this: READMEs of X21, UX3, UX7, LM1, GM1, GT1 (both), SM1, LW1; X21's script and table, so I know KT's slope reads Z about 3.0-3.1 alone and 1.7 at fixed MGAS500, unbinned MGAS500 Z about 1.9, rho(KT, MGAS500) +0.58 on 106 clusters; KT terciles A_MID 1.10, 1.65, 2.13 on X2's C*; G-MID-T3 is the law's worst key on LW1 and is a KT tercile. I have not computed anything on these 106 at fixed other variable beyond X21's Z_b|M. No file's error columns were tabulated; UX7 reports KT median error 0.75 keV.

A measurement: no rule, no mechanism, no pass or fail for any law. kappa = 1/2 FITTED. Cold sector retired; nothing here reinstates it. No particle. Footings canonical 9.3603e-11, alt 1.1312e-10, never pooled. Not theory closed. Nothing here says the data favour the framework.

**Expectation, before any number:** NOT SEPARABLE 70 %, F under 3 on both footings. If split anyway: temperature leans 60 %, gas 15 %, neither 25 %.

## Inputs, read only
- `X7_cluster_core_significance/x7_measure_percluster.npz`: shear per cluster and bin; n = W B (D - leak), W = 1/E^2 where E < 1e8, as LM1's `nsum`.
- `LM1_law_missing_mass_map/cache_BASE_f034/dump.npz` (primary) and `cache_BASE_f0615/dump.npz` (bracket): law V and Newton VN per cluster and bin, measured chain, gas +0.005, both footings, both h; PATCH. These caches are gitignored in LM1; regenerate with `lm1_grade.py`.
- `real_research/data/erass1cl_primary_v3.2.fits`, by NAME: KT, KT_L, KT_H, MGAS500, its _L, _H, M500, L300kpc, BEST_Z. Sample: KT > 0, finite; about 106. Clusters with W = 0 in the band drop out, count stated.

## The quantity
Excess e_ij = n_ij - V_ij, stack dDS = sum e / sum W (M_sun/pc^2), physical bins only, so no R500 sets an aperture. **Primary band MID, bins 3,4,5 (X21's).** Report band IM, bins 1-5. Report the ratio A = sum n / sum V in the same cells. t = lg(KT/median), g = lg(Mg/median).

## Primary statistic: split stacks
- **b_T | g:** sort by g, 3 equal-count bins. In each, split at the bin's median t. D_k = dDS(high) - dDS(low), dt_k = mean t(high) - mean t(low), means W-weighted. omega_k = 1/(1/sumW_high + 1/sumW_low). b_T = sum omega_k D_k / sum omega_k dt_k, per dex.
- **b_G | t:** same with t and g swapped.
- Report residual imbalance: dg_k in the T split, dt_k in the G split, dz_k in both.

Cross-check, joint WLS, unbinned: e_i = W_i (c + b_T t + b_G g), band-summed. Report row with lg(1+z) added.

## Errors
Data sigma = max(bootstrap 2000 clusters on fixed cell assignment, 30-patch jackknife, sd of b over H0 mocks with every shared nuisance). Z = b / sigma. Margins are |Z| - 3.

## Forecast first: committed before the split runs
`tg1_forecast.py` computes no conditional statistic on the real data. It uses the real catalogue, weights and residuals only to build mocks. Marginal fits only, for plant size. Its output is committed before `tg1_split.py` is written to run on data.

**Truth for each mock.** Intrinsic covariance of (t, g) = sample covariance minus mean error covariance, floored at intrinsic sd 0.02. Each cluster's true (t, g) is drawn from its Gaussian posterior given observed values and its own catalogue errors, sigma = half of lg(hi/lo) (missing errors take the sample median, count stated).

**Observed for each mock.** True + catalogue error, then shared nuisances, below.

**Shear for each mock.** n_mock,ij = V_true,ij + W_ij phi_j s_i/<s>_W + q_i r_ij, where
- phi_j is the 106-cluster excess profile in that bin, clipped at 0; s_i the plant; <s>_W normalises the stack to the data's;
- r_ij = e_ij - W_ij phi_j, the cluster's real residual profile, q_i = +-1 per cluster (wild bootstrap: heavy tails kept, bins of a cluster kept together). Report row: q per patch.
- V_true = V (Mg_true/Mg_obs,data)^gamma_ij, V_mock = V (Mg_mock,obs/Mg_obs,data)^gamma_ij, gamma_ij = dln g/dln g_N at nu = V/VN by the law. So gas error enters the excess with its true sign, the only route by which X-ray noise reaches shear.

**Hypotheses.** H0: s = 1. HT: s = (T_true/T0)^alpha. HG: s = (Mg_true/Mg0)^beta. Hboth: half of each exponent. alpha, beta: the marginal one-variable best fits of e on observed variable, grid -3 to 3 by 0.01, per cell. Report row with fixed alpha 1.5, beta 1.

**Shared nuisances, one draw per mock, so the sd over mocks sees them.** All my own adopted widths, PROVISIONAL, none looked up:
- **Mass calibration tilt:** g_obs += eps_g (lg M500 - median), eps_g ~ N(0, 0.10). This is the shared-calibration problem: catalogue M500 is a count-rate relation calibrated on shear including KiDS (UX7), Mg500 is taken to its R500, so a tilt in M500 is a tilt in Mg500; R500 ~ M^(1/3), Mg ~ R^1.2 gives 0.4 per dex for a tilt of 1, and 0.10 is generous for a tilt of 0.25.
- **Mass calibration level:** all Mg_obs x 10^d, d ~ N(0, 0.05); moves V by gamma d. SM1's 0.11 dex and GS4's zero sit either side.
- **KT scale tilt:** t_obs += tau t_true, tau ~ N(0, 0.15). No independent temperature for this sample is on disk.
- **Shear level:** multiplicative m ~ N(0, 0.02) on n.
- **Correlated X-ray error:** rho between t and g errors ~ U(-0.5, 0.5); both come from the same image.

**Forecast statistic.** For each mock, Z_T = b_T/s_T, Z_G = b_G/s_G, with s the sd over H0 mocks in that cell, and Delta = Z_T - Z_G. 2000 mocks per hypothesis per cell (4 cells).
F = |mean Delta(HT) - mean Delta(HG)| / sqrt((var Delta(HT) + var Delta(HG))/2).
Classifier: nearest of HT, HG in Mahalanobis distance on (Z_T, Z_G) with each cloud's own mean and covariance; accuracy on fresh mocks of each.

**Forecast label, per footing:** **SEPARABLE** if F >= 3 and accuracy >= 0.90 for both hypotheses, in both h. Otherwise **NOT SEPARABLE**. Same line as UX7's 3, on a statistic that sees shared systematics.

Report rows, never labels: nuisances off; T errors x 0.5, x 2; band IM; fixed exponents; q per patch; how many clusters at this noise F would need to reach 3, scaling F as sqrt(N), stated as a scaling, not a fetch.

## Verdict, per footing, primary f* 0.034, h 0.672 and 0.686
Run in every case; F does not stop the split, it controls the label.
- **NOT SEPARABLE:** forecast label NOT SEPARABLE. The Z and any lean are reported, and the label is not overruled.
- **TEMPERATURE CARRIES:** Z_T >= 3 in both h; p(|Z_T| at least observed | HG mocks) < 0.01; p(|Z_G| at least observed | HT mocks) >= 0.05.
- **GAS CARRIES:** swapped.
- **BOTH:** Z_T, Z_G >= 3 in both h, and each rejected at 0.01 under the other's cloud.
- **NEITHER:** both |Z| < 2 in both h, and p(|Z_T| | HT) < 0.05 and p(|Z_G| | HG) < 0.05.
- **UNDECIDED:** anything else, including the split and joint rows differing in the sign of a carrying variable.
- **CALIBRATION-DEPENDENT** replaces a carrying label if: L300kpc in place of MGAS500 as the gas variable (no R500 in it; Mg proxy; report row, data only) flips the sign of the carrying slope or takes its |Z| under 2. V still inherits R500 in that row; said in the README.

Bracket f* 0.0615: same statistics on data, no label.

## Checks, every failure published
- **K0:** n.sum(0)/V.sum(0) over all 326 equals LM1's `obs_over_law`, canonical h 0.672 f* 0.034, to 1e-10. Dump's I equals KT > 0 index.
- **K1:** MGAS500 x 1e11 by NAME equals the npz Mgas500, rel 1e-10.
- **K2:** noiseless plant e = W(c + b t) returns (b, 0) in joint to 1e-9; split on the same recovers sign and is within 25 % of b, value reported.
- **K3:** split balance: W-weighted |dg_k|/|dt_k| in T split <= 0.5, and |dt_k|/|dg_k| in G split <= 0.5. Fail is reported and the label gains "IMBALANCED".
- **K4, controls that must react:** T errors x 3 lowers F by at least 10 % (primary cell); plants off gives F <= 0.5; eps_g sd x 10 raises sd Z_G in HT by at least 10 %. If one doesn't react, the forecast is not trusted and the footing's label is NOT SEPARABLE, tagged.
- **K5:** H0 mocks: |median Z_T|, |median Z_G| <= 0.25; sd within 0.1 of 1.
- **K6:** peak RSS < 4 GB; one thread; nice 15.
- **K7:** rerun byte-identical on all outputs.
- **MUTATE:** KT labels shuffled across clusters. K0's I-check and a KT-order check must fail, exit non-zero; b_T must collapse. Plus a plant MUTATE: forecast with HT plant exponent x 3 must raise F.

Any failed check stays in the README under these labels. No amendment changes a label after a graded number.

## Limits known now
KT on 106 of 326, flux-selected. KT is a depth proxy too: "temperature" here can't be told from M500 or potential depth, and the gas row can't be told from anything tied to the same X-ray image; only KT versus Mg500 is asked. Keys are KiDS; HSC's disagreement is outside this lane. X-ray quantities share one image. No download.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
