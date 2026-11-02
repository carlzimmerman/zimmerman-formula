# LM1_law_missing_mass_map: FROZEN CRITERIA, committed alone before any script or new number

kappa = 1/2 FITTED. Model-free map of what the a0 law leaves unaccounted for in clusters. **No rule proposed, no mechanism fitted, no cold sector reinstated** (owner, 2026-11-01). a0 is allowed because this is the law, not the cold sector. Footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2, reported separately, never pooled. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. LW1 owns the law's pass or fail: **this lane gives no key grade.**

**Not blind.** Known before this freeze: CFG687 (A 2.51, 1.91, 1.01; slope 0.90 +- 0.21 against 0.47), X7 V3 (A_OUTER slope +0.83 to +1.00 per dex), M3A1's table and its split (flat A in the outermost bin and lighter half), LW1's partial output (keys rows, X-COP mean +0.467, factors 3.51 at 0.1 R500 falling to 2.16 at 0.7 R500, shares 0.71 to 0.53), FR1, HO1, CS2, DR1. So the X-COP radial look is post-hoc for certain and every look is post-hoc in some degree.

## Question
Delta M(r, M_gas, z) = lensing (or hydrostatic) minus the law on measured gas: what does it look like?

## Inputs (read only)
Shear: X7's per-cluster stack, 326 eRASS1 clusters, 8 bins 0.18-2.49 Mpc, h 0.672 and 0.686; n = W B0 (D - leakP), M3A1's `nsum`. Law: NF1's grader, DR1's tail and LW1's driving pattern, Msrc = r^2 g/G with g = nu(g_b) g_b, nu(y) = 1/2 + sqrt(1/4 + 1/y); GS1's gas tail, gas +0.005 (GS4); f* 0.034 primary, 0.0615 reported; V_law and Newton V_N per cluster per bin, in the grader's own weighted units including offset and reduced shear. X-COP: LW1's/CS2's FITS builder, x 0.1, 0.2, 0.3, 0.5, 0.7, 1.0. Groups: the grader's GROUPS (Tian 63), law's _grp estimator. BCG: CFG922's bcg_med, X40b's matching, 190 matched, unfilled. No new data.

## Quantities, no theory beyond the law
- e_ij = n_ij - V_law,ij. Surface: **dDS** = sum e / sum W, M_sun/pc^2, excess-density contrast.
- Ratio, projected: **Q** = sum e / sum V_N,gas with V_N,gas = V_N / (1 + f*); dimensionless, Delta M / M_gas in projection. Q_b = sum e / sum V_N for baryons.
- Enclosed projected: M2D_min(R) = pi R^2 [dDS(R) + 2 int_R^Rmax dDS dlnR]. Sheet at Rmax set to 0, so a lower bound if the sheet is positive, stated. Integral over the bins only.
- Enclosed 3D, reported conversion only: local power law, gamma = 1 - slope, M3D = pi R^2 dDS 4 Gamma(gamma/2) / (sqrt(pi) Gamma((gamma-1)/2) (gamma-1)). An approximation, used only to set lensing beside X-COP.
- X-COP: dM(x) = M_HSE - M_law, 3D; dM / M_gas(<x). Bracket HSE - 0.12 dex (LF1). X-COP has no shear chain, no +0.005 and no M3A1 row.
- g_N/a0 = G M_b(<R)/R^2 / a0, per footing. **g_N and mean baryon surface density Mb/(pi R^2) are the same variable up to pi G.** So the Sigma look uses the projected local baryon contrast V_N/W, a different thing, and states this.
- Groups: d = log10(sigma_obs/sigma_law), dM/M_law = 10^(2d) - 1 at Re, dM/M_b with M_law, M_b from the Hernquist profile at Re (estimate, anisotropy as in the estimator).

## Fit
e_i = C v_i x_i^p, chi^2 with 1/w_i, C free, p on a grid -3 to +3 step 0.01; v = W (dDS), v = V_N,gas (Q). M_piv 1e13. Errors: cluster bootstrap 2000, seed 20261101; 30-patch jackknife (grader's PATCH); sigma = the larger. Radial: C R^p on stacked bins, sigma from bootstrap, p on the same grid. A resample with no maximum in range is counted and reported. Band fits for gas-tail clusters use catalogue gas, tested for Eddington below.

## Bands
Radial physical: INNER bins 0-2, MID 3-5, OUTER 6-7 (grader). x = R/R500 per cluster: [0.2, 0.5), [0.5, 1), [1, 2), [2, 5). Gas terciles M1-M3 are the grader's T3M; terciles at each ordering are the same membership.

## Frozen list of looks (L01-L31), counted per footing, 62 tests
Radial shape:
L01, L02, L03 slope of dDS in INNER, MID, OUTER, null = the 8-bin slope. L04 one power law across 8 bins, chi^2 with bootstrap covariance, shrink 0.05 to diagonal. L05 slope over MID + OUTER, M1 minus M3, null 0. L06, L07 X-COP slope of dM with r, x 0.1-0.3 and 0.3-1, null: their mean slope.
Scaling with gas at fixed r/R500:
L08-L11 exponent s of dDS on M_gas in each x band, null s = 0. L12 row 10: OUTER physical, T2's own log-stack statistic on terciles for data and law, on this chain; null 0.47 (law's value here computed), and s of e at OUTER by the fit, reported. L13 same for MID.
Ratio:
L14-L17 exponent r of Q on M_gas in each x band, null 0 (a constant fraction of gas). L18 slope of Q on x, all clusters, 0.2-5, null 0. L19 X-COP dM/M_gas slope on x, null 0. L20 X-COP dM/M_gas at x 0.3-0.7 against M_gas, 7 clusters, null 0.
Redshift:
L21, L22 exponent of dDS on (1+z) fitted jointly with M_gas (grid on z exponent after removing the band's own M_gas exponent), MID, OUTER, null 0.
BCG:
L23, L24 exponent of dDS on BCG stellar mass after removing M_gas exponent, INNER, MID, 190 matched, null 0. Spearman of BCG with M_gas reported, since the two aren't independent.
Scales, comparing Q_b across gas terciles at fixed ordering variable (5 equal-log bins over the range all three terciles share; chi^2 of tercile values around each bin's weighted mean, bootstrap diagonal errors, dof sum(n_t - 1); correlation between bins ignored, stated):
L25 g_N/a0. L26 V_N/W (local projected baryon contrast). L27 r/R500. L28 R in Mpc. L29 curvature of lg Q_b against lg(g_N/a0) on all clusters, quadratic term, null 0: is there a break. L30 same-g_N comparison: X-COP rows against groups, lg(M_obs/M_law), where their g_N/a0 ranges overlap, null equal. L31 slope of groups' d against lg(g_N/a0), null 0.

Report the deficit's own surface density and the Q ordering table plainly. A scale is only called preferred if its ordering collapses (L25 or L26 labelled CONSTANT), the others don't, and the groups agree (L30 CONSTANT). Anything else: no preferred scale found. The scan was post-hoc; a scale found is a suggestion.

## Labels per look
t = (value - null)/sigma. Look-elsewhere: 62 tests, Sidak at 0.05, two-sided p 8.27e-4, **|t| >= 3.34**.
- **TREND:** |t| >= 3.34.
- **CONSTANT:** |t| < 2 and sigma small enough to mean it: sigma <= 0.20 for exponents on gas; <= 0.30 for radial slopes and the quadratic term; <= 1.0 for the (1+z) exponent, whose range is short; <= 0.10 dex for L30.
- **NOISE-LIMITED:** everything else; 2 <= |t| < 3.34 tagged [hint], not a result.
Chi^2 looks (L04, L25-L28): TREND at p <= 8.27e-4; CONSTANT at p > 0.05 with median fractional error below 0.30; otherwise NOISE-LIMITED. X-COP looks tagged [N=7]; the bootstrap on 7 clusters is optimistic, so their sigma is doubled before the label. Labels are per footing; a disagreement is stated, not averaged. No overall pass or fail.

## Systematics, M3A1's rows
Each row applied as M3A1 applies it: C1a (Tweedie; M3 only as M3A1 reads, plus an all-cluster version with shift zero where catalogue error > 0.2 dex, my addition, because M3A1's all-326 version is broken by M1's tail), C2a (pointed gas on M3), C4a (each tercile's own boost), C4c (F(z) printed in `m3a1.out`, a bound, per h; if h 0.686 is not printed use F(h 0.672) and say so), C4d (extended randoms), C4e (per-tile leakage), m 2 % ceiling, quadrature of M3A1's s terms for the outer M3 number. Report dDS by band and tercile and outer exponent and row-10 slope under: each row, net as frozen (all), net without C4c, lowering only. **Survival statement:** per band and tercile, fraction of baseline dDS left under lowering-only; which labels change under net and under lowering-only. C4d and C4e overlap, stated.

## Checks (failed check: no reading)
K1 keys: run _keys in the same process; Z and preds against DR1's and LW1's JSON at gas +0.005, f* 0.034, 0.0615, both footings, |d| <= 1e-6. K1b dump sums vC, V reproduce those preds on M1-M3, Mall, G-IN-Mall, G-OUT-T1-3, |d| <= 1e-6. K2 n sums reproduce the grader's meas for the same keys, |d| <= 1e-6. K3 CFG687's npz through my T2 statistic reproduces 0.90 +- 0.21 and 0.47, |d| <= 0.005 (jackknife seedless). K4 X-COP builder: +0.4675, 0.4763, alt +0.4345, 0.4442, against LW1, |d| <= 1e-4. K5 synthetic: inject e = C v x^p + bootstrap of real noise at p = 0.7; recover within 2 sigma; p = 0 reads CONSTANT or NOISE-LIMITED, not TREND. K6 M3A1's rows on M3A1's own dumped V: C4a, C4d, C4e on M3 at f* 0.034 h 0.672 reproduce +4.36, +3.96, +3.73, |d| <= 0.01. K7 Groups: _grp's mean and Z reproduce DR1/LW1's row, |d| <= 1e-6. K8 one thread, RSS under 2 GB.
**MUTATE:** a0 x 1.5 in the law, gas +0.005, f* 0.034, separate outputs: every band's dDS must move, and X-COP. A part that doesn't move has failed. Flips aren't results.

## Expectation on record
Radial: dDS falls with R, slope near -0.7 in MID, not one clean power law, no clean concentration from 8 noisy bins, so L01-L03 NOISE-LIMITED or nearly so. Gas: dDS at fixed x rises with M_gas with s 0.3-0.8, TREND in at most two bands. Q at fixed x near flat or falling, CONSTANT to NOISE-LIMITED. Q falls outward; X-COP dM/M_gas falls from about 7 to about 4. BCG NOISE-LIMITED. z NOISE-LIMITED. g_N collapses no better than r/R500, no preferred scale; groups near zero deficit at g_N where X-COP's is a factor of 3, so L30 TREND. Under lowering-only, most of the MID deficit in M2-M3 survives and M1's OUTER is consistent with zero or negative. One line: missing mass roughly proportional to the gas within a band, not a scale. I'd bet on no acceleration scale.

One thread, nice 15. Local commits only. kappa = 1/2 FITTED. Not theory closed.
