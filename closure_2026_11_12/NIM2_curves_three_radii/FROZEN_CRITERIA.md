# NIM2 FROZEN CRITERIA: does a third radius (50 kpc) add power to NMB1's gate?

Written 2026-11-12, before any script of this lane and before any value of the real-galaxy curves
or of the mock curves at 50 kpc was read. Nothing below is re-tuned after the run. TEST lane.
Adopts nothing. Does not relabel NMB1, MWG1, MWJ1, DW1, G238 or G239.

## Question

NMB1 graded the framework's zero-parameter Milky Way enclosed-mass line against the four
shape-measuring curves of DESI DR2 Results III (NIMBLE-A and NIMBLE-B, RR Lyrae and BHB) at 30 and
80 kpc with a covariance from the paper's 24 mocks. Every case passed, but the gate could not
separate the no-field (E0) and field (E1) readings, nor the framework from the paper's own NFW.
Does adding 50 kpc, with NMB1's method otherwise unchanged, add power: does it separate E0 from E1,
or the framework from the NFW, on either footing?

## What was known when this was frozen (disclosed)

Known: everything NMB1 read (its criteria, RESULT and output: the four curves at 30 and 80 kpc,
the two-radius estimate 11.4059 +/- 0.0270 and 11.8047 +/- 0.0567, correlation +0.18, slope
0.936 +/- 0.137, k_30 = 1.000, k_80 = 1.392); Table 4 of the paper, including the joint at 50 kpc
(All 11.654 +0.025 -0.026; RRL 4.81, BHB 4.34 x 10^11); MWG1's MB15 hot-gas profile; MWJ1's
McMillan 2017 M_sph function.

Not known: any fig10 value at 50 kpc for any method; any mock residual at 50 kpc; the 50 kpc
error calibration k_50.

Model values computed before freezing (from the model only, no data; scratch, not committed):

| case | 30 / 50 / 80 kpc [10^11 Msun] | slope 30-50 | slope 50-80 | curvature |
|---|---|---|---|---|
| E0 canonical, census | 2.331 / 3.684 / 5.691 | 0.896 | 0.925 | +0.029 |
| E0 canonical, MB15 | 2.368 / 3.800 / 6.035 | 0.926 | 0.984 | +0.058 |
| E1 canonical, census | 2.326 / 3.613 / 4.977 | 0.863 | 0.681 | -0.182 |
| E1 canonical, MB15 | 2.363 / 3.735 / 5.423 | 0.896 | 0.794 | -0.103 |
| E0 alt, census | 2.526 / 4.013 / 6.219 | 0.906 | 0.932 | +0.025 |
| E0 alt, MB15 | 2.565 / 4.138 / 6.593 | 0.936 | 0.991 | +0.055 |
| E1 alt, census | 2.517 / 3.900 / 5.109 | 0.857 | 0.575 | -0.283 |
| E1 alt, MB15 | 2.557 / 4.034 / 5.633 | 0.893 | 0.711 | -0.182 |
| paper's NFW | 2.485 / 4.174 / 6.205 | 1.015 | 0.844 | -0.171 |

Hand expectation (not a result): if the NIMBLE combination at 50 kpc sits about 4 per cent below
the joint (as it did at 30 kpc), i.e. near 4.33 x 10^11, the canonical lines at 50 kpc are 0.07 to
0.08 dex low and the alt lines 0.03 to 0.05 dex low; with a 50 kpc error near 0.04 dex the
canonical cases may move toward the gate. The curvature differences between readings (at most
0.3) are expected to be smaller than the curvature error, so the expectation is little or no gain
in separating power. This expectation is disclosed so the result can be read against it.

## Instrument (NMB1's, unchanged except for the third radius)

File: Zenodo 10.5281/zenodo.23712180, `desi-dr2-mw-mass-figdata.zip`, 2,652,537 bytes,
md5 `5b0cc3aa9947286eb9348e947d01182d`,
sha256 `1b132abc3f163887160efb29a88d294ce5fb0751d2e389951da9c4c237e35ee1`. Kept outside the
repository; the script takes its path as an argument.

- **Data vector.** `fig10/desi-dr2-menc.csv`, methods `nimble-a`, `nimble-b`, tracers `rrl`, `bhb`,
  at r = 30, 50, 80 kpc: y = log10(Menc_med), 12 numbers. Off-grid values by linear interpolation
  in (log r, log M). sigma = [log10(hi/med) + log10(med/lo)] / 2.
- **Mock covariance.** `figA1/` (RRL) and `figA2/` (BHB), each of the 24 mocks: residual
  log10(M_est / M_true) for each of the 12 (curve, radius) items, M_true from `truths.csv`. A mock
  that does not bracket every radius for every curve is dropped for all; N >= 20 required. S is the
  sample covariance (ddof 1); S_res = 0.5 S + 0.5 diag(S) (paper's B6, lambda = 0.5); R its
  correlation matrix. C = C_stat + S_res, C_stat[m,n] = sigma_m sigma_n R[m,n] (B12, B13 without the
  unpublished floor).
- **Error calibration K.** Per radius, the same machinery on all method-tracer curves at that radius
  alone: 30 kpc emPDF, NIMBLE-A, NIMBLE-B (six curves, as NMB1); 50 kpc and 80 kpc emPDF, GME,
  NIMBLE-A, NIMBLE-B (eight curves). k_r = max(1, sigma_published(r) / sigma_mine(r)), with
  sigma_published = 0.022 (30), 0.0255 (50; Table 4: +0.025 -0.026), 0.0345 (80). Rows and columns
  of C at radius r are multiplied by k_r.
- **Estimate.** GLS for theta = (theta_30, theta_50, theta_80): V = (X^T C^-1 X)^-1,
  theta = V X^T C^-1 y, X the 12 x 3 indicator matrix.

## The cases (the framework's line, no fitted parameter)

M_b = 6.681 x 10^10 Msun (McMillan 2017). Spherical enclosed fractions: 0.9777 at 30 and 0.9972 at
80 kpc (DW1's committed values, as NMB1); at 50 kpc f_50 = M_sph(50) / M_sph(3000 kpc) from MWJ1's
M_sph function, copied (expected 0.9952). Kernel nu(y) = 1 / (1 - exp(-sqrt(y))). Footings
canonical a0 = 9.36e-11, alt a0 = 1.13e-10 m/s^2.

- **E0** (no field): M = nu(g_b) M_bar, g_b = G M_bar / (r^2 a0).
- **E1** (G239's QUMOND angle average, e_N = 0.01273 in a0 units): as NMB1.
- **Baryons:** census, M_bar = A f(r) M_b with A = 1; and **MB15**, census plus
  M_hot(<r) = 4.3 x 10^10 Msun (r / 250 kpc)^1.5, spherical (MWG1's model, as published).

Eight graded cases: {E0, E1} x {canonical, alt} x {census, MB15}. Comparator, graded through the
same gate but not a framework case: the paper's NFW, M200c = 1.19 x 10^12, c200c = 12, h = 0.6777.

## Gate and statistics

mu = log10 M_line at (30, 50, 80). Q = (theta - mu)^T V^-1 (theta - mu), 3 degrees of freedom.

- **PASSES** if Q <= 8.02 (two-sigma equivalent, p = 0.0455). **FAILS** otherwise, tagged
  "2 to 3 sigma" if Q <= 14.16 and "beyond 3 sigma" above.
- Direction: z_r = (mu_r - theta_r)/sqrt(V_rr) at each radius. **LOW** if all three negative,
  **HIGH** if all three positive, **MIXED** otherwise.
- Slope pull z_s: p = (value at 80 - value at 30)/log10(80/30), as NMB1. **SHAPE** appended to a
  FAIL if |z_s| > 2.
- **Curvature statistic:** c = (theta_80 - theta_50)/log10(80/50) - (theta_50 - theta_30)/log10(50/30),
  sigma_c^2 = g^T V g with g the gradient of c. The model's c_line likewise from mu.
  z_c = (c_line - c_data)/sigma_c. **CURVATURE** appended to a FAIL if |z_c| > 2; noted in brackets
  on a PASS if |z_c| > 2. The curvature is reported for every case and the NFW.
- **FRAGILE** appended if any pre-named variant lands on the other side of 8.02: NIMBLE-A curves
  only; NIMBLE-B curves only; NIMBLE-A RRL dropped; lambda = 0 with the inverse covariance times
  (N - p - 2)/(N - 1) and its own k; lambda = 1 with its own k; k_r = 1.
- **NO VERDICT** if a known-answer check fails (the script stops before any graded number).
  **NO POWER** if a mutation does not bite.

## Separation labels (per footing)

- **E0 vs E1**, for census and for MB15 separately: **SEPARATES** if exactly one of E0, E1 passes;
  **DOES NOT SEPARATE** if both pass or both fail.
- **Framework vs NFW**: for each of the four framework cases of that footing, whether it lands on
  the other side of 8.02 from the NFW. Footing label: **SEPARATES** if all four do, **PARTLY
  SEPARATES** if some do, **DOES NOT SEPARATE** if none do.

## Power comparison with NMB1 (reported plainly, not a pass/fail)

- Errors: sqrt(V) at 30 and 80 kpc and the 30-80 slope error, three-radius vs NMB1's two-radius.
- Noncentrality lambda = (mu_a - mu_b)^T V^-1 (mu_a - mu_b) between E0 and E1 (each footing, each
  baryon set) and between each framework case and the NFW, computed with NMB1's two-radius V (on
  30, 80) and with the three-radius V (on 30, 50, 80); and the power P(noncentral chi-square(dof,
  lambda) > gate) with (2 dof, 6.180) and (3 dof, 8.02). "No gain" is reported if the three-radius
  power is not larger.

## Known-answer checks (all before any graded number)

| id | check | pass condition |
|---|---|---|
| KA1 | the file | md5 equal |
| KA2 | fig10 `joint` rows vs Table 4 RRL and BHB columns (as NMB1) | 26 values within 0.011 x 10^11 |
| KA3 | mock residuals vs Figure 8 medians (as NMB1) | four values within 2.5 points |
| KA4 | machinery on all curves at one radius vs Table 4 All | 30: 11.423 +/- 0.022 (6 curves); 50: 11.654 +/- 0.0255 (8 curves); 80: 11.804 +/- 0.0345 (8 curves); central value within one published sigma, N >= 20 |
| KA5 | NMB1 reproduced with the 50 kpc rows dropped | theta 11.4059 +/- 0.0270 and 11.8047 +/- 0.0567, each value and error within 0.0005; Q 4.89, 2.91, 2.40, 0.05 (E1 can, E1 alt, E0 can, E0 alt) each within 0.01 |
| KA6 | estimator and gate on synthetic data | closed form to 1e-10; 20,000 seeded draws from N(X mu, C_12x12): mean Q 3.00 +/- 0.06, rejection rate at 8.02 within 0.0455 +/- 0.005 |
| KA7 | the line and the inputs | E0 5.691 / 6.219 and E1 4.977 / 5.109 at 80 kpc within 0.5 %; M_sph fractions at 30 and 80 kpc within 0.001 of 0.9777 and 0.9972; MB15 gives 3.8 x 10^9 inside 50 kpc within 3 % |

## Mutations (each must bite; written to `nim2_mut.out`)

| id | mutation | must give |
|---|---|---|
| M1 | E0 census with the baryons doubled (A = 2), both footings | FAILS HIGH |
| M2 | a point mass: mu_30 = mu_50 = mu_80 = theta_80 | FAILS with |z_s| > 2 or |z_c| > 2 |

## What a label will and will not mean

A PASS is "not excluded by the shape-measuring curves at three radii" under a covariance calibrated
on six LambdaCDM haloes with no LMC; the three radii share stars, so the third radius is strongly
correlated with the other two and its added information may be small. A FAIL is against that
covariance and the stated baryons. Neither moves another lane's frozen verdict.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
