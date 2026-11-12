# NMB1 FROZEN CRITERIA: the shape-measuring curves of DESI DR2 Results III against the framework's zero-parameter line

Committed alone, 2026-11-12, before any script and before any per-method value of the real Milky
Way was read. Nothing below is re-tuned after the run. TEST lane. Adopts nothing. Does not relabel
DW1, G238 or G239. kappa = 1/2 FITTED; not theory closed.

## Question

DR2REV (origin 114f008bf4) found that Table 4 of arXiv:2611.05518 is a calibrated amplitude whose
shape is partly imposed (emPDF is an NFW, GME's slope is its prior). The only curves whose shape is
measured are NIMBLE-A and NIMBLE-B (spherical Jeans, B-splines), for RR Lyrae and for BHB stars.
Does the framework's zero-parameter enclosed-mass line agree with those four curves, in amplitude
and in shape, on both footings?

## What was known when this was frozen

Known: Table 4 and Table 5 of the paper; the paper's text about the curves (NIMBLE-B agrees between
tracers; NIMBLE-A's RRL curve rises faster and flattens higher than its BHB curve beyond 30 kpc and
the authors attribute that to the tracer-density reconstruction; the joint lies closest to emPDF and
NIMBLE-B); the calibration-side content printed in DR2REV's `figdata_inventory.out` (true mock
profiles, the per-method mock biases of Figure 8, the residual correlation matrix at 80 kpc, the GME
posterior summaries); the structure of `fig10/desi-dr2-menc.csv` (methods, tracers, radii, column
names).

Not known: any value in `fig10/` for emPDF, GME, NIMBLE-A or NIMBLE-B; any per-mock method curve
in `figA1/` or `figA2/`; the correlation matrix at 30 kpc; any literature value in `fig13/`.

Hand estimates made before freezing, from Table 4 only (expectations, not results): if the NIMBLE
combination equalled the joint, the no-field line would sit at (-0.056, -0.048) dex (canonical) and
(-0.020, -0.010) dex (alt) at (30, 80) kpc, so canonical would be near the gate and alt inside it;
G239's external-field line at 80 kpc would sit at -0.106 / -0.095 dex and would probably fail low.
The external-field line at 30 kpc was not computed before freezing.

## Instrument

File: Zenodo 10.5281/zenodo.23712180, `desi-dr2-mw-mass-figdata.zip`, 2,652,537 bytes,
md5 `5b0cc3aa9947286eb9348e947d01182d`,
sha256 `1b132abc3f163887160efb29a88d294ce5fb0751d2e389951da9c4c237e35ee1`.

- **Data.** `fig10/desi-dr2-menc.csv`, methods `nimble-a` and `nimble-b`, tracers `rrl` and `bhb`:
  four curves, bias-corrected by the paper (Figure 10 caption). `Menc_med`, `Menc_lo`, `Menc_hi`
  are the median and the 16th and 84th percentiles in 10^11 Msun.
- **Radii.** 30 kpc and 80 kpc. 80 is the outermost radius the paper reports. 30 is where the bulk
  of the stars are and is the inner radius the paper itself uses in its Figures 7 and 9. Values off
  the tabulated grid are taken by linear interpolation in (log r, log M).
- **Data vector.** y = log10(Menc_med) for the four curves at the two radii, eight numbers.
  Statistical error of each: sigma = [log10(hi/med) + log10(med/lo)] / 2.
- **Calibration covariance, from the paper's own mocks.** `figA1/` (RRL mocks) and `figA2/` (BHB
  mocks): for each of the 24 mocks (halo, view) and each curve, the residual
  log10(M_est / M_true) at 30 and 80 kpc, with M_true from `truths.csv`. S is the sample covariance
  (divisor N - 1) of the eight residual series about their means. A mock that does not bracket both
  radii for every curve is dropped for all curves; N >= 20 is required.
  Shrinkage as in the paper's equation B6 with its value lambda = 0.5:
  S_res = (1 - lambda) S + lambda diag(S). R is the correlation matrix of S_res.
- **Total covariance**, the paper's B12 and B13 without the per-method floor (its values are not
  published): C = C_stat + S_res, with C_stat[m,n] = sigma_m sigma_n R[m,n].
- **Error calibration K.** The missing floor makes C too small. The same machinery is therefore run
  on all method-tracer curves at one radius at a time (30 kpc: emPDF, NIMBLE-A, NIMBLE-B for both
  tracers, six curves; 80 kpc: those plus GME, eight curves) and its combined error sigma_mine(r) is
  compared with the published joint error (0.022 dex at 30 kpc, 0.0345 dex at 80 kpc, from Table 4).
  k_r = max(1, sigma_published / sigma_mine). Rows and columns of C belonging to radius r are
  multiplied by k_r.
- **Estimate.** Generalised least squares for theta = (theta_30, theta_80), the common log mass at
  each radius: V = (X^T C^-1 X)^-1, theta = V X^T C^-1 y, X the 8 x 2 indicator matrix.

## The framework's line

M_b = 6.681 x 10^10 Msun (McMillan 2017, the census DW1 used); spherical enclosed fractions from
DW1's committed output: M_sph/M_b = 0.9777 at 30 kpc and 0.9972 at 80 kpc. Kernel
nu(y) = 1 / (1 - exp(-sqrt(y))). Baryon amplitude A = 1. No fitted parameter. Footings:
canonical a0 = 9.36e-11, alt a0 = 1.13e-10 m/s^2.

- **E1, the record's operative reading since G239:** the QUMOND angle average in a uniform external
  field, e_N = 0.01273 (in units of a0, the repository's Local Group value):
  M = (M_sph / g_b) * (1/2) * integral over mu from -1 to 1 of
  nu(sqrt(g_b^2 + e_N^2 + 2 g_b e_N mu)) (g_b + e_N mu), g_b = G M_sph / (r^2 a0).
- **E0, the no-field limit:** M = nu(g_b) M_sph. An external field only lowers the line, so E0 is
  the highest amplitude any external-field treatment can give.

Four graded cases: E1 canonical, E1 alt, E0 canonical, E0 alt. Labels are quoted in that order.

Not graded: the matched-field AQUAL values of today's correction lane (4.49 / 4.58 x 10^11 at
80 kpc, point mass, a different kernel). The record holds no 30 kpc value for them. Their pull at
80 kpc is reported.

## Gate

mu = (log10 M_line(30), log10 M_line(80)). Q = (theta - mu)^T V^-1 (theta - mu), two degrees of
freedom.

- **PASSES** if Q <= 6.180 (the two-sigma equivalent for two degrees of freedom, p = 0.0455).
- **FAILS** otherwise, tagged "2 to 3 sigma" if Q <= 11.829 and "beyond 3 sigma" above that.
- Direction, from z_30 = (mu_30 - theta_30)/sqrt(V_11), z_80 likewise, and the slope pull
  z_s = (p_line - p_data)/sigma_p with p = (value at 80 - value at 30)/log10(80/30) and
  sigma_p^2 = (V_11 + V_22 - 2 V_12)/log10(80/30)^2: **LOW** if z_30 and z_80 are both negative,
  **HIGH** if both positive, **MIXED** otherwise; **SHAPE** is added if |z_s| > 2. Negative z means
  the line is below the data.
- **FRAGILE** is appended if any of these pre-named variants lands on the other side of 6.180:
  NIMBLE-A curves only; NIMBLE-B curves only; NIMBLE-A RRL dropped (the curve the authors
  distrust); lambda = 0 with the inverse covariance multiplied by (N - p - 2)/(N - 1); lambda = 1;
  k_r = 1.
- **NO VERDICT** if any known-answer check below fails (the script stops before printing a graded
  number). **NO POWER** if a mutation below does not bite.

Reported, not graded: the bands as published with no mock covariance (R = identity, S_res = 0);
the internal consistency of the eight numbers about theta (chi-square, six degrees of freedom); the
amplitude A* that minimises Q for each case and Q at A*; the paper's own NFW (M200c = 1.19e12,
c200c = 12, h = 0.6777) through the same gate; the emPDF and GME values at 80 kpc.

## Known-answer checks (all before any graded number)

| id | check | pass condition |
|---|---|---|
| KA1 | the file is the one named above | md5 equal |
| KA2 | units and reading of `fig10`: its `joint` rows against Table 4's RRL and BHB columns | 26 values, each within 0.011 x 10^11 |
| KA3 | residual construction: median of M_est/M_true - 1 over the mocks against Figure 8's file | NIMBLE-B RRL at 80 (-6.50 %), NIMBLE-A BHB at 80 (-7.54 %), NIMBLE-A RRL at 30 (+5.91 %), NIMBLE-B BHB at 30 (-1.19 %), each within 2.5 points |
| KA4 | the machinery, before K, on all curves at one radius reproduces the paper's joint | central value within one published sigma of Table 4's All column: 11.423 +/- 0.022 at 30 kpc, 11.804 +/- 0.035 at 80 kpc |
| KA5 | the estimator and the gate on synthetic data | two correlated measurements match the closed form to 1e-10; 20,000 seeded draws from N(mu, C) give mean Q in 2.00 +/- 0.05 and a rejection rate in 0.0455 +/- 0.005 |
| KA6 | the line reproduces the record at 80 kpc | E0 5.691 / 6.219 and E1 4.977 / 5.109 x 10^11, each within 0.5 % |

## Mutations (each must bite)

| id | mutation | must give |
|---|---|---|
| M1 | E0 with the baryons doubled (A = 2), both footings | FAILS HIGH |
| M2 | E0 with the baryons halved (A = 0.5), both footings | FAILS LOW |
| M3 | a point mass: mu_30 = mu_80 = theta_80 | FAILS with SHAPE |

Mutation runs write `nmb1_mut.out`, never the graded output.

## What a label will and will not mean

A PASS says the line agrees with the four shape-measuring curves within a covariance calibrated on
six LambdaCDM haloes with no LMC; it is not a confirmation of the law. A FAIL is against that same
covariance and against the McMillan baryon census at A = 1; A* says how much of it is the known
baryon liability. Neither moves a frozen verdict of another lane.
