# CQ3_pressure_support_line: FROZEN CRITERIA

Committed alone, before any script or number of this lane. **Not blind**: the four excesses below are on record and their headline numbers were read to design the points (VS1 +0.12 dex slow minus fast, HX1 B 3-4 in the MaNGA ellipticals, KU1/KU2 +1.2 to +1.4 ln, CW6 red 1.313 / blue 0.878 canonical, 1.200 / 0.802 alt). No CQ3 number exists. κ = ½ FITTED and held fixed; footings canonical a0 = 9.3603e-11 and alt a0 = 1.1312e-10 are graded apart and never pooled. No particle, no cold sector, no new field. A description, not an action. Not theory closed. Nothing here says the data favour the framework. No downloads.

## Question
The record finds four times that dispersion-supported systems need more mass than the a0 law gives. Do the four excesses fall on ONE line of ONE pressure-support variable P, E = k P, with one constant k per footing? If yes, a pressure-aware coupling would be worth an action. If no, the idea is dropped.

## The common quantity
E = log10(M_needed / M_law), with the law's own baryons and the lane's own estimator, per footing. M_needed / M_law is the ratio of the measured to the law's total effective mass at the lane's radius (g_obs / g_law for the kinematic samples, sigma_obs^2 / sigma_law^2 for HX1's Jeans, the lensing amplitude A = data / model for CW6). Nothing is refitted: each lane's estimator is rerun or read as committed (K1 below).

## The pressure variable P, frozen
P = sigma^2 / (sigma^2 + V^2) at the effective radius, the kinetic energy fraction in random motion.
Where only the spin parameter lambda_R(Re) exists (every sample here), V/sigma comes from the lambda_R relation of Emsellem et al. 2007 (MNRAS 379, 401), lambda_R = kappa_E (V/sigma) / sqrt(1 + kappa_E^2 (V/sigma)^2) with kappa_E = 1.1 as quoted there (the constant is quoted from the paper's text, not re-read in this lane: no download). Inverting:

  P(lambda) = kappa_E^2 (1 - lambda^2) / [kappa_E^2 (1 - lambda^2) + lambda^2], lambda clipped to [0, 0.999].

A sample's P is the unweighted mean of P(lambda_i) over its members. No other mapping is allowed, and nothing is tuned.

## The ten points (per footing), frozen
Each sample enters as the points its own lane reports. P is footing-independent.

**S1 VS1** (rebuild_2026_10_22/VS1_rotation_split/vs1.json, 16 ATLAS3D / SLUGGS galaxies, per-galaxy offsets in dex and lambda_Re stored there). Two points: the slow-rotator group (4) and the fast group (12). E = group mean of the stored per-galaxy offset, sigma_E = within-group sd / sqrt(n) (ddof 1), independent. P from the stored lambda_Re. The SPARC disc arm (+0.012 +- 0.016 canonical, -0.018 +- 0.016 alt) is not a point: it is the P -> 0 inverse check, reported beside.

**S2 HX1** (rebuild_2026_10_22/HX1_hot_ladder, Tian et al. 2026 MaNGA ellipticals, 4 sigma quartiles). Four points, the MaNGA Q1-Q4 rungs, rebuilt by executing HX1's own text through its `tian` function (lines 1-37 of hx1_ladder.py, only the output-file line swapped for a null file). E_j = median over the rung of log10(sigma_O^2 / sigma_L^2) per galaxy. Errors: bootstrap of the rung median (300 draws, fixed seed) as independent part; the shared mass systematic as HX1 did it, E at +0.10 dex and -0.10 dex in log M, half the difference, **fully correlated across the four rungs** (C = diag(stat^2) + s s^T). P_j = mean P over MaNGA DynPop galaxies (KU1's selection, below) with u - r > 2.0 and Sigma_Re inside rung j's sigma interval, with edges the 25 / 50 / 75 per cent of the Tian MaNGA-elliptical sigma (the same edges HX1 used).

**S3 KU** (rebuild_2026_10_22/KU1_kappa_universality_rotators/ku1.py, MaNGA DynPop SDSSDR17_MaNGA_JAM_v2.fits in `_external_data`, KU1's selection and class cut copied verbatim: Qual >= 1, finite NSA elpetro and sersic masses, z > 0.005, finite lambda and eps, Sigma_Re > 0, at least 8 finite JAM models; slow = lambda < 0.08 + eps/4 and eps < 0.4; r_half and total mass median over the ten JAM models; H0 70; masses as stored). Two points, the slow and the fast class. E = class median of ln(g_obs / g_law) / ln 10 at r_half. Errors: bootstrap of the class median (300 draws) independent; the shared systematic is the quadrature of (i) the standard deviation across the ten single-model class medians and (ii) the class-median shift from NSA sersic mass instead of elpetro mass, **fully correlated between the two classes**. The h convention of the NSA masses is a caveat (below), not an error term.

**S4 CW6** (cw_lanes_2026_11_04/CW6_lensing_measured_gas/cw6_b21c.json, profile FIXED, B21 Fig-8 colour bins). Two points, red and blue. E = log10 A, sigma_E = sA / (A ln 10). Independent. P_red, P_blue = mean P over the DynPop galaxies of KU1's selection with u - r > 2.0, and u - r <= 2.0 (SI2's colour line, u - r from the NSA elpetro absolute magnitudes, bands 2 and 4 of the stored 7-vector). A colour-to-P map by population, not a per-lens measurement.

If a point has fewer than 30 members, or any E or P cannot be computed from the files named above, the label is NOT EVALUABLE.

## The fit and tests, frozen
N = 10 points, vector E, vector P, covariance C as above. Generalised least squares through the origin, one k per footing:
k = (P^T C^-1 E) / (P^T C^-1 P), sigma_k = (P^T C^-1 P)^(-1/2), chi2 = (E - kP)^T C^-1 (E - kP) on N - 1 degrees of freedom, p the upper tail.
For each sample s: its own k_s and sigma_ks from the same formula on its block of C, z_s = (k_s - k) / sigma_ks.

Labels, per footing:
1. **NOT EVALUABLE**: a point's P or E cannot be built, or k / sigma_k < 2 (the joint slope is not detected, so no line exists to test).
2. **ONE LINE**: chi2 p >= 0.05 and every |z_s| <= 2.
3. **NOT ONE LINE**: otherwise (chi2 p < 0.05, or any |z_s| > 2), with the sample or samples that break it named.

No label is merged across footings. The label is read off the primary fit only.

## Checks, frozen
- **K1 (reproduction, before the label)**: VS1's group means against vs1.json (1e-3); KU1's class medians against ku1.json abs_median_slow / abs_median_fast (1e-6); HX1's rung median B_need against hx1_ladder.json Bmed (1e-9); CW6 A against cw6_b21c.json (exact). Any miss voids the run.
- **K2 (planted line)**: E_j = 0.2 P_j plus noise drawn from C, 2000 draws, the real P: share labelled ONE LINE reported, must be >= 0.70 (with four 2-sigma tests the ceiling is about 0.8). With P shuffled across the ten points at the same draws, the share must be <= 0.10.
- **MUTATE twin** (`--mutate`): P shuffled across the ten points (seed 20261104), the same pipeline, printed not graded, exit 1 by design. It must not read ONE LINE. The share of 2000 shuffles that read ONE LINE on the real E is reported.

## Reported beside, not graded
(a) The fit without S3, without S2, and on S1 + S4 alone. (b) Each sample's E / P. (c) S3 with the NSA masses read as h = 0.7 (log M lowered by 0.31 dex). (d) P = 1 - lambda_Re in place of the Emsellem map (no kappa_E). (e) An affine E = E0 + k P fit (E0 free) and its chi2 p. (f) The disc arm's E against the line's value at a disc P = (11 / 200)^2 = 0.003 (sigma_HI 11 km/s from Leroy et al. 2008, V 200 km/s typical of the arm's mass range).

## Caveats kept as caveats, not as error terms or excuses
- **KU's absolute level is uncalibrated.** NSA masses are stored with no stated h convention (an h = 0.7 reading is worth 0.31 dex in mass), kcorrect masses run low, and the JAM mass is sphere-enclosed. See rebuild_2026_10_22/LAM9_imf_from_spectra/FROZEN_CRITERIA.md.
- **HX1's need is model-dependent**: inside Re the law is close to Newton and the stellar IMF moves the Newtonian dispersion, so a bottom-heavy IMF would also raise it. S2 and S3 are the same survey (MaNGA) with different estimators, apertures and mass models, so they are not independent.
- **The colour map is a population map**: MaNGA galaxies stand in for KiDS lenses, with different mass distributions, and the lensing amplitude is a halo-scale quantity while P is a half-light one.
- The Emsellem constant is quoted, not re-read. Estimator errors are the lanes' own: VS1 scatter only, no shared systematic.

## Expectations on record
NOT ONE LINE on both footings 75 %; NOT EVALUABLE 15 %; ONE LINE 10 %. The expected breaker is S3 (the absolute level), and the expected small effect is that slow and fast P differ by only about 0.1 on this map while VS1's E differs by 0.12 dex.

## Run
```
cd cq_lanes_2026_11_04/CQ3_pressure_support_line
export OMP_NUM_THREADS=1 PYTHONHASHSEED=0
nice -n 10 python3 -I cq3_line.py            # primary, writes cq3_line.{out,json}
nice -n 10 python3 -I cq3_line.py --mutate   # twin, writes cq3_line_MUTATE.{out,json}
```
One thread, small memory. Files: this file, `cq3_line.py`, outputs, `README.md`.
