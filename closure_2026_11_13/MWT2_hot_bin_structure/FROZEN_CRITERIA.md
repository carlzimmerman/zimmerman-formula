# MWT2 FROZEN CRITERIA: is RAW1's hot 30-40 kpc bin a structure?

Written 2026-11-13, before any script of this lane and before any number of this lane. TEST lane. Adopts nothing,
relabels nothing (RAW1, MWT1 keep their labels), registers nothing. Nothing is downloaded.

## 0. What is known beforehand (disclosed)

Read in full before writing: MWT1 (RESULT, FROZEN_CRITERIA, mwt1.py), RAW1 (RESULT, raw1.py; raw1_model.py's a0
values). Known numbers: per-bin counts 865 / 264 / 241 / 125; sigma_los 97.24, 106.74, 92.62, 95.30 km/s; alpha
5.289 +/- 0.169; beta 0.659 +/- 0.018; RAW1's f table (30-40: FW census 1.205 +/- 0.058 / 1.155 +/- 0.056, FW rc
1.135 / 1.114); MWT1: 30-40 is the only non-Gaussian bin (excess kurtosis -0.62, p 0.0085; bimodality coefficient
0.41, p 0.0075; other bins p 0.36-0.81); a 43 +/- 14 km/s dipole at 30-40 (p 0.015, not detected); a real cold
group in 40-55 (24 flagged stars, dispersion 9.3 km/s, MWT1's S2); north and south differ at 40-55 (p 0.006).
Also seen before freezing: the catalogue's column names (RVTAB holds FEH and FEH_ERR; GAIA holds PMRA, PMDEC and
errors). No velocity, metallicity, distance or proper-motion value was read in this lane before this file.

Data: RAW1's file `MWS_BHB.fits` (DESI DR1 MWS BHB VAC v1.0, sha256 5669c821...5246), held outside the
repository; the script checks the hash, takes the path as its argument and never prints it.

## 1. Sample, frame, line, footings (RAW1's, unchanged)

RAW1's sample and cuts (Sgr band 15 deg, |v_gsr| <= 400, R0 8.122, solar velocity (12.9, 245.6, 7.78)), bins
20-30, 30-40, 40-55, 55-80 kpc. Velocities: v_gsr (Galactic rest frame); errors: the quoted VRAD_ERR, deconvolved
in every fit (as RAW1 and MWT1's nominal; MWT1's error scale 1.31 moves f by <= 0.001 and is not applied).
RAW1's functions are reused by executing raw1.py's import, constant and function definitions (MWT1's method,
copied and cited); RAW1's files are read-only.
Line: the framework's no-field line g = nu(g_b/a0) g_b, nu(y) = 1/(1 - exp(-sqrt y)), external field dropped as
RAW1 (owner note 2026-11-12). a0 = 9.36e-11 (canonical) / 1.13e-10 (alt) m/s^2, raw1_model.py's values, so the
known answer matches. Headline cases: FW census (McMillan 2017 baryons), per footing. FW rc is labelled by the
same rule and reported. DESI NFW (H) and Newton baryons (N) reported, not graded.
Word per bin as RAW1: PASS if |f - 1| <= 2 sigma_f, HOT if f > 1 + 2 sigma_f, COLD if f < 1 - 2 sigma_f.

## 2. (a) Mixture: one Gaussian against two, every bin

Per bin, on v_gsr with errors e_i:
- M1: v_i ~ N(mu, s^2 + e_i^2).
- M2: v_i ~ w N(mu_1, s_1^2 + e_i^2) + (1 - w) N(mu_2, s_2^2 + e_i^2), fitted by extreme deconvolution (EM with
  per-star errors), dispersion floor s_k >= 5 km/s, from a fixed deterministic set of starts (median split;
  a 0.15-weight 15 km/s component at the 5, 20, 35, 50, 65, 80, 95th velocity percentiles; symmetric
  mu +/- 0.7 s with 0.7 s each; a 0.3-weight narrow (0.5 s) component at the mean); best likelihood kept.
- LR = 2 (lnL_M2 - lnL_M1). p from a parametric bootstrap: B = 1,000 samples drawn from the bin's own M1 fit with
  the bin's own errors, each refitted with the identical procedure; p = (1 + #{LR_b >= LR}) / (B + 1).
- TWO COMPONENTS if p < 0.01 AND the minor component (lower weight) has weight >= 0.10 AND w_minor N >= 15.
  Reported for every bin: weights, means, dispersions (with 68 per cent errors from 200 bootstrap refits of M2
  on resampled stars), LR, p.

## 3. (b) Identity: does the second component separate in anything else? (for every TWO-COMPONENT bin)

Candidate group = the component with the smaller dispersion (debris is colder); the other is the smooth halo.
(If the dispersions agree within 10 per cent, the candidate is the lower-weight component.) Membership by posterior
responsibility q: core group q_g >= 0.8, core halo q_g <= 0.2; if a core has fewer than 15 stars, split at 0.5.
Four families of quantities, each with 2,000 seeded permutations of the core labels (two-sided, p = (1 + #) /
2001); a family's p is the smallest of its tests times its number of tests (Bonferroni):
- SKY: |mean unit vector (group) - mean unit vector (halo)| (heliocentric directions); KS on |B_Sgr| (Majewski
  frame, RAW1's code). 2 tests.
- DISTANCE: KS on Galactocentric r within the bin. 1 test.
- CHEMISTRY: KS on FEH (stars with finite FEH and FEH_ERR < 0.5; NOT EVALUABLE if either core has < 10 such
  stars). 1 test.
- TANGENTIAL MOTION: for stars with usable PMs (RAW1's pmok), the 3D Galactocentric velocity from v_gsr and the
  PMs at the catalogue distance (solar motion added), then KS on v_phi and KS on the tangential speed
  |V - (V . r_hat) r_hat|. 2 tests. NOT EVALUABLE if either core has < 10 such stars.
DISTINCT GROUP if at least two families have family p < 0.01. Disclosed: SKY also responds to a sky dipole in the
mean velocity (MWT1's 43 km/s at 30-40), which is why one family is not enough; the tangential velocities carry
a small share of v_los through the non-radial part of the line of sight (sin eta <= 0.27 at 30 kpc).

## 4. (c) Consequence, every bin

For each bin, RAW1's statistic redone with the smooth component only:
- (c1) MIXTURE f (headline): v_i ~ (1 - w_g) N(mu_h, f^2 P_i + e_i^2) + w_g N(mu_g, s_g^2 + e_i^2), P_i RAW1's
  constant-beta Jeans prediction with RAW1's alpha and beta; (w_g, mu_h, mu_g, s_g) re-maximised at each f;
  f profiled with RAW1's prof_interval (Delta lnL 0.5); sigma_f = stat + alpha (alpha +/- its sigma) + beta
  (RAW1's per-bin beta range) in quadrature, nuisances re-maximised in each variant.
- (c2) as (c1) with the tracer density re-counted without the group's stars (q_g > 0.5 removed from RAW1's
  alpha fit; alpha and its sigma refitted).
- (c3) bracket: hard removal of q_g > 0.5 and RAW1's fit_f on the rest.
Applied as graded only where (a) and (b) say DISTINCT GROUP; computed and reported (marked "forced") for every
bin regardless, so the symmetric effect is visible. Report any RAW1-passing bin whose graded word changes.

## 5. Labels (per footing; on the 30-40 bin, FW census headline, FW rc by the same rule)

1. NO POWER if the mutation G (section 6) is not found, or the bin has < 100 stars.
2. If 30-40 is not TWO COMPONENTS by (a), or is TWO COMPONENTS but not a DISTINCT GROUP by (b):
   HOT BIN IS ONE POPULATION (the non-Gaussian shape is not a second group by the frozen rule). Say which step.
3. If DISTINCT GROUP: the (c1) word of 30-40 decides
   PASS -> HOT BIN IS A DISTINCT GROUP PLUS A SMOOTH HALO AND THE SMOOTH PART PASSES (a HIT, not a pass of the
   theory; awaits an independent re-grade; say what the group is if the data identify it);
   HOT -> HOT BIN HAS TWO COMPONENTS BUT THE SMOOTH PART STILL FAILS;
   COLD -> HOT BIN IS A DISTINCT GROUP PLUS A SMOOTH HALO AND THE SMOOTH PART FAILS COLD (a case the brief does
   not name; added here before any number).
FRAGILE if the label changes under any frozen bracket: (a) threshold p < 0.05 or < 0.001; minor weight 0.05 or
0.15; dispersion floor 3 or 10 km/s; (b) family threshold 0.05 or 0.001; (c) (c2) or (c3) in place of (c1).

## 6. Controls

- K0 known answer: RAW1's per-bin counts, sigma_los, alpha, beta, and every f and sigma_f (FW census and rc,
  both footings, H, N) reproduced within 5e-4 of raw1_results.json with nothing removed.
- K1 the (c1) mixture f with w_g fixed at 0 equals RAW1's fit_f to 1e-5; the M2 fitter on a synthetic two-Gaussian
  sample (N 400, weights 0.7 / 0.3, means 0 / 120, dispersions 90 / 20, errors 5) recovers each parameter within
  3 of its bootstrap sigma.
- K2 SI: g of FW census canonical at 30 kpc in m/s^2, M = g r^2 / G against raw1_model.M_of_g to 1e-9; V printed.
- TWIN (shuffle): velocities (with their errors) permuted among all 20-80 kpc stars, 20 seeded shuffles; each bin
  graded by (a) against that bin's real-data bootstrap null (the LR null depends on N and the errors, not the
  scale), then (b) where (a) says TWO COMPONENTS. Passes if at most 3 of the 80 bin-shuffles are TWO COMPONENTS
  (P(>= 4 | 80, 0.01) < 0.01) and at most 1 is a DISTINCT GROUP.
- MUTATION G (moving group), `*_MUTATE*` output: into 40-55 kpc (Gaussian by MWT1), add 40 synthetic stars on the
  sky positions and distances of the 40 bin stars nearest a seeded bin star (copies of their positions, errors,
  FEH and PMs), velocities mu_bin + 150 + N(0, 15) km/s, PMs shifted by a common 60 km/s tangential offset at
  each star's distance. Must be TWO COMPONENTS (own bootstrap, B = 500) and a DISTINCT GROUP, and (c1) on the
  mutated bin must return the un-mutated bin's RAW1 f (FW census canonical) within 0.03.
- MUTATION S (scatter only), `*_MUTATE*` output: 40-55 kpc velocities v -> v + N(0, 50) km/s (seeded), no group.
  Must NOT be TWO COMPONENTS-and-DISTINCT-GROUP; its f rise is reported.

## 7. Expectation and hand estimate (written before any number)

A flat-topped single population with excess kurtosis k is fitted by two near-equal Gaussians at mu +/- d with
dispersion s: for an equal-weight symmetric pair k = -2 d^4 / (s^2 + d^2)^2, so k = -0.62 gives
d^2 / (s^2 + d^2) = 0.557: d about 80 km/s, s about 71 km/s for the bin's 106.7. Radially biased orbits
(beta 0.69 at 30-40) naturally give a platykurtic v_r, so a symmetric split is what one population would show.
Expected: 30-40 TWO COMPONENTS at p about 0.005-0.05 (near the threshold), weights near 0.5, means near +/- 80,
dispersions near 70; the components do NOT separate in two families (SKY maybe, through the dipole; others no):
HOT BIN IS ONE POPULATION on both footings. Other bins: one component, except perhaps 40-55 (MWT1's cold group of
24 stars is about 10 per cent of the bin at 9 km/s, near the weight floor). If a group were declared with
dispersions near 70, (c1) would give f about 0.80 at 30-40: COLD, not PASS; so the HIT label is not expected.

## 8. Changes

Never edited after this commit. Departures only as dated AMENDMENT files committed alone, as-frozen reading first.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
