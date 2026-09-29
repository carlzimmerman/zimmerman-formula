# CFG192 — independent referee re-derivation of CFG182 (is SPARC's a0 direction-dependent? the sky-dipole test): FROZEN CRITERIA (phase 1)

Written 2026-09-29, before any CFG192 script or number. Scratch dir: `.../scratchpad/cfg192/`. Nothing here says the theory is closed; kappa = 1/2 stays FITTED; a0 is FITTED in this test (a-bar0 free), so kappa enters no line; no claim that any data favour the framework; a null is a valid result; failed controls and wrong expectations are kept, never repaired.

## 0. What is read, what is not, and how blind this is

Read in phase 1 (only): `CFG182_a0_sky_dipole/FROZEN_QUESTION.md` (with its Addendum 1) and `README.md`; `CFG181_FROZEN_CRITERIA.md` (format and pitfalls only); `real_research/data/SPARC_Lelli2016c.mrt` (header/notes, and a table-level awk count of Q, Inc, f_D, see 2); the header of `sparc_lelli2016_table1_pos.tsv` and one `*_rotmod.dat` header; `campaign_fresh_gravity/CFG4_common.py` lines 1-265 (loader `load_sparc()` as a DATA DESCRIPTION, and the kernel list) and FP1's `nu_mono` source lines 122-144 (the kernel definition, read as a definition). NOT opened: any CFG182 `.py`, `.out`, `.json`, `.npz`, `.png`. They are opened in phase 2 only, after my own main and MUTATE runs are saved (`CFG192_main.*`, `CFG192_MUTATE_k.*`, `CFG192_attacks_*.*`).

**The README numbers are TARGETS I read, not blind predictions.** The hand estimates in 3 were made AFTER reading the README. For the null distribution, p and A95 I hand-checked the README's own numbers while reading (they came out mutually consistent, see 3, note H): those rows are a sanity check that the README is not obviously self-contradictory, NOT independent predictions. Independence lives in the code (written from the frozen question, not from CFG182's scripts), in the coordinate conversion, the optimiser, the seeds, and in the attacks.

## 1. What is re-derived, and where independence STOPS

Re-derived with my own code (numpy/scipy only; the repo enters ONLY as data files; no import from any campaign or chain module):
- the SPARC loader (rotmod files, master table, position table), the Equatorial J2000 -> Galactic (l, b) conversion (standard rotation matrix, own code; unit checks: Galactic centre (RA, Dec) = (266.405, -28.936) -> (l, b) = (0, 0); NGP (192.859, +27.128) -> b = 90),
- the sample selection and usable-point counts, the baryonic model V_bar^2 = Y_d Vdisk|Vdisk| + Vgas|Vgas| + Y_b Vbul|Vbul| (signed), g_bar = V_bar^2 / R,
- the law g_obs = nu(g_bar/a0) g_bar and the per-galaxy PROFILE curves chi2_i(log a0) (4 nuisances profiled at each grid value; own optimiser: bounded least-squares on the residual vector with prior terms, warm start along the grid plus a second cold start, cross-checked against a brute-force multi-start at 10 grid points x 5 galaxies),
- Birge scaling, the dipole fit (own optimiser: analytic gradient, 5 starts), permutations (simple and block), bootstrap, the Neyman A95, hemisphere statistic, distance-method splits, footprint analysis,
- the nu_mono kernel IMPLEMENTED FROM ITS DEFINITION (h = y/expm1(sqrt y); Y_P the root of h' = 0 in [1,5]; nu-1 = H_M(y)/y with H_M the trapezoid integral of max(h', 0.05 h_P/(y+Y_P)) over a log grid -14..14, 280001 points; y floored at 1e-14).

Shared elements (independence STOPS here; they are inputs, not tested by me):
1. **The data files themselves** (175 rotmod curves, the master table, the VizieR position table). If a file is wrong, both lanes are wrong. I cross-check only what can be cross-checked from inside the repo (positions vs `sparc_cosmicweb_match.csv` if I read it in phase 2; the D, Inc columns of the mrt vs the rotmod header distance).
2. **The frozen question's declared design** is adopted for the reproduction and attacked in the attacks: the LML 2018 priors (Y_d 0.5 lognormal 0.1 dex; Y_b 0.7, 0.1 dex; D Gaussian with e_D; Inc Gaussian with e_Inc — quoted from the frozen question, NOT checked against the LML paper), the Birge scaling s_i = max(1, chi2_min,i/(N_i - 1)), the grid (-11.3 to -9.0, step 0.01), |D| <= 0.95, the permutation schemes, 2000 bootstrap, 5000 permutations, the Neyman construction, the pass lines S1-S3. The premise a0(n) = a-bar0 (1 + A n.d) is the declared model, not a test of it.
3. **The kernel definition** nu_mono (FP1's). My implementation is from the definition; the numerical cross-check against the repo's `nu_mono` is a PHASE 2 compare-script item (max relative difference over y in 1e-8..1e4, tolerance 1e-6). Kernel variants P2 (sqrt(1+1/y)) and simple (1/2 + sqrt(1/4 + 1/y)) are my own one-liners.
4. **The published claims** (arXiv:1707.00417, 1803.08344): known to me only from the CFG182 text (abstract-level numbers 0.37 +/- 0.04 at (175.5, -6.5); 0.25 +/- 0.04 at (171.30, -15.41)); their methods are unverified and I cannot read them (no network). See section 6E.
5. Numerics (numpy, scipy versions; Accelerate matmul noise): tolerances below exceed it. Threads pinned to 1.

Declared ambiguities in the frozen question that I resolve myself (each is also an attack cell, none decided after seeing results):
- (i) chi2_min in the Birge ratio: primary = the profiled chi2 INCLUDING the four prior terms, dof N_i - 1 (as written); variant: velocity-only chi2.
- (ii) whether e_V rescales with the trial inclination: primary NO (e_V fixed, as published); variant: e_V x sin i/sin i'.
- (iii) inclination bounds i' in [5, 90] deg (reflecting bound at 90), D' in [0.2 D, 3 D], Y_d in [0.05, 3], Y_b in [0.05, 3] (declared; bound hits are counted and printed).
- (iv) a galaxy with no bulge (max Vbul = 0) has no Y_b parameter.
- (v) points with V_bar,trial^2 <= 0 during profiling: y floored at 1e-14 (V_pred^2 = nu(y) g R with g floored); the point set itself is fixed at the fiducial (Y_d 0.5, Y_b 0.7) as declared.
- (vi) block permutation: the position multiset = the 123 non-UMa positions + ONE mean UMa position; the 124 positions are permuted among the 124 units (UMa = one unit whose 26 members all take the assigned position). The observed fit uses the true individual positions.
- (vii) hemisphere scan: my own 3072-point Fibonacci sphere of axes (NOT HEALPix nside 16, no healpy assumed); >= 10 galaxies per hemisphere; a declared deviation.
- (viii) curves are interpolated by a cubic spline in the dipole fit; outside the grid, linear extrapolation of the edge slope, and the number of galaxies clamped is printed.

## 2. Headline pinned with the README's numbers (targets read, not blind)

| id | README value |
|---|---|
| N (clean) | **149 galaxies, 3150 points**; by method 81 Hubble-flow (f_D=1), 37 TRGB (2), 3 Cepheid (3), 2 SNIa (5), 26 Ursa Major (4); all-usable variant 171 |
| footprint | \|<n>\| = 0.60 toward (142, 55); 117 of 149 galaxies at b > 0 |
| no-dipole a-bar0 (nu_mono, LML priors) | 1.13e-10 m/s^2 |
| Birge factor | median 1.72; per-galaxy Delta chi2 = 1 half-width median 0.26 dex (Addendum 1); best log a0 16-84% span -10.61 to -9.57 |
| **best dipole** | **A = 0.238 toward (l, b) = (237.2, -44.2)**; Delta chi2 = 10.3 (3 params) |
| sigma_A | bootstrap **0.201**; Fisher 0.082 |
| cones | 68% within 59 deg, 95% within 115 deg |
| **permutation p_A** | **0.772 simple, 0.774 block** (pass line uses the larger); null A-hat median 0.34, 95% quantile 0.62; Delta chi2 p 0.73 / 0.76 |
| Gaussian nulls | curve level (tau = 0.34 dex) p = 0.89; point level (100 mocks) p = 0.010, mocks reduced chi2 0.68 vs data 4.20 |
| hemisphere | H_max = 0.595 toward (295, 5), null median 0.51, 95% 0.73, p = 0.24; at Zhou axis H = 0.15 +/- 0.22 |
| distance split | H: A = 0.47 toward (259, 46); I (TRGB/Ceph/SNIa): A = 0.40 toward (183, -62); vectors differ p = 0.11; along the full-sample direction -0.76 sigma (H) and +1.41 sigma (I): S2 fails |
| footprint alignment | footprint axis 53 deg from the fitted axis, inside the 115 deg cone: S3 fails |
| PV template (H only) | 209 km/s, Delta chi2 12.2, p = 0.58 |
| variants | no Birge A = 0.61, p = 0.12; kernel P2 0.23, p = 0.78; kernel simple 0.22, p = 0.84; all 171: 0.31, p = 0.59 |
| **A95 (random direction)** | **0.425** (simple 0.425, block 0.375; MC noise about +/-0.05) |
| fixed-direction upper ends | CMB 0.24; bulk flow 0.36; Virgo 0.19; UMa 0.19; Chang 0.55; Zhou 0.53. Along Chang: 0.11 +/- 0.23; at Zhou axis H = 0.15 +/- 0.22 |
| scatter | per-galaxy best a0 scatter 0.39 dex (MAD) vs median profile width 0.26; tau = 0.34 dex; 19 of 149 with \|pull\| > 3 |
| MUTATE (CFG182's) | A = 0.20 injected toward (114.6, -41.9): fitted vector moved 0.151, 22 deg off; mutated p = 0.56; recovery about 0.77 of the injection |
| verdict | NULL: S1 (p<0.003) FAILS, S2 FAILS, S3 FAILS |

Data-description counts I did make in phase 1 (an awk pass on the master table, not a pipeline run): table rows 175; Q <= 2: 163; Inc >= 30: 163; **Q <= 2 and Inc >= 30: 153** (H 83, TRGB 39, Cepheid 3, SNIa 2, UMa 26). The README's 149 therefore implies 4 further losses at the "at least 5 usable points" step (README by method: 81/37/3/2/26 = 2 H and 2 TRGB lost), and 171 = 175 - 4 says the same four are lost in the all-usable sample. That is a checkable prediction (F1 below).

Hand-check remarks (made while reading the README; labelled, not predictions): (a) the fitted direction (237.2, -44.2) is 62 deg from Chang (171.3, -15.4) and 127 deg (53 deg as an axis) from the footprint vector (142, 55), both as the README says. (b) The null A-hat law in the README is Maxwell-like: median 0.34 gives sigma_comp = 0.221; then P(A-hat >= 0.238) = 0.76 (README 0.77) and the 95% quantile is 2.80 sigma = 0.618 (README 0.62). (c) The Neyman construction with noncentral-chi3 (sigma 0.221) gives A95 about 0.40 (README 0.425 simple, 0.375 block). (d) The bootstrap sigma_A = 0.20 is about sigma_comp = 0.22, and the Fisher 0.082 is 2.7x too small: that mismatch is the over-dispersion (tau = 0.34 dex vs per-galaxy width 0.26). (e) Chang 95% upper end 0.11 + 1.96 x 0.23 = 0.56 (README 0.55, fine). Structural remark: because the null is Maxwell with sigma about 0.22, the whole test is set by the 0.34-dex between-galaxy scatter of best-fit a0; anything that changes that scatter (nuisance treatment, weighting, sample) changes the answer, so the attacks in 6B are the heart of this referee.

## 3. Hand ESTIMATES (made after reading the README) with reproduction probabilities

"Reproduces" = within the pass line in 4. Direction is weakly determined (68% cone 59 deg), so its probability is low by construction.

| row | my hand estimate | P(reproduces) |
|---|---|---|
| N clean = 149, points = 3150, method counts 81/37/3/2/26 | 149 (153 table-level minus 4 at the 5-point cut); 3150 to within 30 | N = 149: 0.80; points exact: 0.60; method counts exact: 0.75 |
| a-bar0 no-dipole | 1.13e-10 +/- 4% | within 5%: 0.70 |
| A-hat | 0.24 | within 0.03: 0.55 |
| direction (l, b) | 237, -44; a near-degenerate ridge running toward/away from the footprint axis is likely | within 15 deg: 0.35 (within 45 deg: 0.65) |
| permutation p (larger of simple, block) | 0.75 (Maxwell hand check 0.76) | within 0.05: 0.65; verdict NULL (p > 0.003, S1 FAILS): 0.97 |
| null A-hat median / 95% | 0.34 / 0.62 | within 0.03 / 0.05: 0.70 |
| sigma_A (bootstrap) | 0.20 | within 0.03: 0.55 |
| S2 fails, S3 fails | S2: vectors differ p about 0.1 (0.05-0.3); S3: cone > 90 deg so footprint axis inside | S2 fail: 0.85; S3 fail: 0.95 |
| A95 (random direction) | 0.40 (noncentral-chi3 hand check); range 0.35-0.50 | within 0.06 of 0.425: 0.55 |
| hemisphere H_max, p | 0.55-0.65; p about 0.2-0.3 | H_max within 0.06: 0.55; p within 0.08: 0.60 |
| recovery of an injected dipole (curve level, mult. form) | about 0.75 of the injection along the true direction | within [0.6, 0.95]: 0.75 |
| MUTATE A = 0.20: vector change 0.15 at about 20 deg | 0.15 +/- 0.05, 20-30 deg | 0.60 |
| all-usable (171) variant A about 0.3, p about 0.6 | | within 0.05 / 0.15: 0.50 |

Estimates for the attacks (labelled, made after reading the README; they are meant to be wrong sometimes):
- 6A: no leave-out or sample variant produces p_perm < 0.01: P = 0.80; the largest single-galaxy influence on D-hat below 0.10: P = 0.60.
- 6B: fixed nuisances give a LARGER between-galaxy scatter of best a0 (nothing absorbs the D/Y_d/i errors) with narrower per-galaxy widths, so the null still holds, p_perm > 0.05: P = 0.65; looser priors (2x widths): null holds: P = 0.90; simple per-galaxy a0 fit + regression: null holds: P = 0.75. Random-effects (fitted tau) likelihood gives an amplitude within 0.10 of the Birge fit: P = 0.60.
- 6C: mean recovery along the injected direction 0.75 +/- 0.10; mean A-hat at A_inj = 0.1, 0.2, 0.3, 0.5 of about 0.36, 0.39, 0.44, 0.60 (noise-dominated: the amplitude estimator is biased high by the Maxwell noise, ~1.6 sigma at A_inj = 0); median direction error at A_inj = 0.5 about 30 deg (0.1: about 75 deg); detection power at permutation p < 0.05: about 0.06 / 0.08 / 0.12 / 0.35; at the S1 line p < 0.003: about 0.01 / 0.01 / 0.02 / 0.08. Sensitivity to the footprint: the least-constrained direction lies within 30 deg of the footprint axis with sigma there 2-4x that of the best direction: P = 0.65; the (log a-bar0, D parallel to footprint) correlation |rho| > 0.6: P = 0.75.
- 6D: A95 by my Neyman = 0.40-0.45 for a random direction; coverage of the limit procedure under a random-direction ensemble >= 0.93 at A_true in {0.1, 0.2, 0.3, 0.5}: P = 0.80; coverage for injections along the footprint axis and toward the southern pole (worst-constrained and best-constrained): fails (< 0.90) in at least one: P = 0.45.
- 6E: no simple-estimator variant of mine reproduces both A_fix (Chang) in [0.20, 0.30] AND sigma <= 0.06: P = 0.75. The true published claims are neither confirmed nor excluded here: P(README verdict "neither" is reproduced) = 0.85.

## 4. Exact pass lines (reproduction)

Class REPRODUCES iff ALL hold in the main run (primary sample, primary kernel nu_mono, Birge on, LML priors):
- **sample count exact: 149** (and points = 3150 +/- 30; method counts exactly 81/37/3/2/26);
- **A-hat within 0.03 of 0.238**;
- **direction within 15 deg of (237.2, -44.2)**;
- **p_A (larger of simple and block, N = 5000 each) within 0.05 of 0.774**;
- verdict NULL with S1 FAIL, S2 FAIL, S3 FAIL (each individually);
- a-bar0 within 5% of 1.13e-10; bootstrap sigma_A within 0.03 of 0.201 (2000 resamples); null median within 0.03 of 0.34 and 95% within 0.05 of 0.62;
- A95 (my Neyman, 1000 trials, grid 0-0.9 step 0.025) within 0.06 of 0.425 (the README's own noise is +/-0.05).
Class PARTIAL: verdict NULL with the same three failures, but at least one numeric row above missed (each miss listed). A miss in direction alone, with A-hat and p in tolerance, is recorded as PARTIAL-DIRECTION (expected outcome for a 59-deg cone; not a disagreement).
Class DISAGREES: (a) any of S1-S3 flips (S1 p < 0.003), or (b) p_A differs from 0.774 by more than 0.15, or (c) A-hat differs by more than 0.10, or (d) N differs by more than 2 from 149 (this signals a sample-definition or data-reading disagreement), or (e) A95 differs by more than 0.15 from 0.425.
Secondary rows (reported, not classified): distance-split amplitudes and directions (0.47, 0.40), PV template (209 km/s), hemisphere H_max/p, variants (no-Birge 0.61/0.12; P2; simple; 171), inclination split p (0.42), distance trend beta (+0.02).
Exit codes: main exits 0 whenever the script completes and prints its class (a disagreement is a finding, printed, never repaired); 2 on an internal error only.

## 5. MUTATE controls (each flips a load-bearing cell; `MUTATE=k python CFG192_main.py`, outputs `CFG192_MUTATE_k.out/.json`; exit 1 iff the control BITES, 0 if it does not; a control that does not bite is kept and reported)

1. **M1: point-level injection of a known dipole** A = 0.50 in a seeded random direction (seed 19211, drawn uniformly on the sphere and printed) into V_obs: V_obs -> V_obs sqrt(nu(y')/nu(y)), y = g_bar,fid/a0,ref, y' = g_bar,fid/(a0,ref (1 + D_inj.n_i)), a0,ref = 1.13e-10, e_V unchanged; the whole pipeline reruns. BITES iff the change of the fitted vector D-hat_mut - D-hat_obs has amplitude in [0.25, 0.55] (recovery 0.5-1.1) AND points within 25 deg of the injection AND the mutated permutation p (N = 2000) < 0.05. (Flips the cell "the pipeline can see a sky dipole".) Expectation: recovery about 0.75, angle about 20-30 deg, p about 0.2-0.5: P(bites) = 0.55; the p leg is the likely miss; recorded either way.
2. **M2: matched-amplitude injection A = 0.20** at the same seed direction (a like-for-like of CFG182's control): BITES iff change vector amplitude in [0.10, 0.27] and angle <= 30 deg. Expected from the README (0.151, 22 deg): P(bites) = 0.65. The permutation p is reported, not required (power statement).
3. **M3: position shuffle after injection**: inject A = 0.50 (seed 19211 direction) at the point level using the TRUE positions, then fit with the sky positions shuffled among galaxies (one fixed permutation, seed 19213). BITES iff the recovered component along the injected direction is < 0.10 (signal destroyed: the injection lives in the galaxy-position association) and the fitted amplitude is within 0.25 of the null median (0.34), i.e. the fit returns a null-like A-hat. Flips the cell "positions are attached to galaxies". P(bites) = 0.85.
4. **M4: drop the nuisance profiling** (nuisances fixed at Y_d 0.5, Y_b 0.7, catalogue D and Inc; curves = fixed-nuisance velocity chi2, Birge scaling on). BITES iff the median per-galaxy Delta chi2 = 1 half-width shrinks by >= 1.5x AND the Fisher sigma_A shrinks by >= 1.5x (the profiling is what sets the error scale). Also reported: the permutation p and A-hat of this fit (informative for 6B). P(bites) = 0.80.
5. **M5: antipodal-sign control**: inject A = 0.50 (seed 19211) with the sign convention flipped in the FIT (fit with n -> -n; equivalent to a mis-signed Galactic conversion). BITES iff the recovered direction is within 25 deg of the ANTIPODE of the injection. Flips the cell "direction convention". P(bites) = 0.80. (The unit check of the conversion is part of main; this is the end-to-end version.)
6. **M6: wrong law**: kernel nu = 1 (Newtonian, no MOND) in the profiles. BITES iff the median Birge factor rises above 3x its primary value or best log a0 hits a grid edge in >= 50% of galaxies (the a0-fit is meaningless without the law). P(bites) = 0.90.
7. **M7: null-injection control (zero)**: inject A = 0 exactly (a pipeline no-op) — must NOT change the fit: BITES iff the fitted vector changes by more than 1e-6 (i.e. this control exits 1 only on a pipeline defect; expected exit 0). Included as the safety-of-controls check.

Additional non-MUTATE built-in checks in main (load-bearing, each named): optimiser check (profile minimum vs brute-force multi-start), finiteness, positions (unit checks above; every position within a declared 0.5-deg tolerance of `sparc_cosmicweb_match.csv` in phase 2), no-residual exact recovery (a synthetic set of Gaussian-free curves centred exactly on a0_i = a-bar0 (1 + D.n_i) returns the injected D to 1e-4, the analogue of CFG182's "exact recovery"), single-start vs 5-start agreement in A-hat over 100 permutations (< 1e-4), determinism (in-place re-run byte-identical .out; done by run_all.sh).

## 6. Attacks: frozen procedures and what pass/fail means (all with fixed seeds; outputs `CFG192_attacks_<x>.out/.json`; declared now, no cell added or dropped after seeing results)

Seeds (SeedSequence(192) children by name): perm simple 19201, perm block 19202, bootstrap 19203, Neyman 19204, injection mocks 19205, synthetic mocks 19206, stratified perms 19207, jackknife none (deterministic), MUTATE 19211-19213, injection directions 19214. Variant runs use N_perm = 1000, N_boot = 500 and grid step 0.02 (a grid-step consistency check at primary: step 0.01 vs 0.02 agree in A-hat within 0.01, in p within 0.03, else all variants are flagged "grid-limited").

**A. Clean-sample definition and leave-out sensitivity** (`CFG192_attacks_AB.py`).
- A1: sample ladder, reporting N, points, A-hat, direction, sigma_A, p_perm(simple) for: primary (Q<=2, Inc>=30); Q = 1 only; Inc >= 45; Inc >= 60; no Inc cut (Q<=2); Q <= 3 (all usable, N about 171); >= 10 points; drop UMa (26); drop Hubble-flow; drop TRGB/Cepheid/SNIa; drop galaxies with bulge; keep only |b| > 10.
- A2: leave-one-galaxy-out jackknife: the D-hat shift for all 149; the 5 most influential galaxies; the fit with the 10 most influential and (separately) the 10 largest-|pull| galaxies removed (CFG182 says A = 0.19, p = 0.74 for the latter, a TARGET; I redo it independently).
- A3: leave-one-UMa-out is irrelevant; instead a block jackknife over 12 sky sectors (12 equal-area Fibonacci cells): remove each sector; report the range of A-hat and direction.
- Meaning: NULL ROBUST iff no cell gives p_perm < 0.01 and A-hat stays < 0.60; SAMPLE-DEPENDENT if any cell gives p_perm < 0.01 (then that cell is reported as a candidate signal, NOT a detection, with its look-elsewhere count = the number of cells); FRAGILE-FOR-DIRECTION if the direction moves > 90 deg across cells (expected).

**B. Nuisance profiling vs simpler treatments** (`CFG192_attacks_AB.py`).
- B1: fixed nuisances (M4's fit), Birge on and off, per-galaxy curves from velocity chi2 only.
- B2: profile Y_d and Y_b only (D and Inc fixed at catalogue).
- B3: profile D and Inc only (Y fixed).
- B4: looser priors: Y sigma 0.2 dex; Y sigma 0.3 dex; D and Inc sigma x2; all three together. Tighter: Y sigma 0.05 dex.
- B5: the "simple per-galaxy a0 fit": each galaxy's best log a0 and 1-sigma (fixed nuisances, no profiling), then the weighted and the unweighted regression of log a0_i on log10(1 + D.n_i) with a-bar0 free (own nonlinear least squares); permutation null on the same regression.
- B6: random-effects likelihood: marginalise a Gaussian intrinsic scatter tau per galaxy (fitted jointly with a-bar0, D on the profile curves), reporting A-hat, tau, sigma_A from the profile in A, and the LR statistic; permutation p on the profile-likelihood-ratio.
- B7: Birge variants: none; chi2 velocity-only; dof N_i; cap s_i at 3; e_V sin i rescaling (ambiguity ii).
- B8: degeneracy diagnostics: per-galaxy best log a0 versus log D, versus the fitted Y_d pull, versus Inc (Spearman), the correlation matrix of the nuisance minimiser at the primary a-bar0, and the fraction of galaxies whose nuisances hit a bound.
- Meaning: NULL SURVIVES the nuisance treatment iff p_perm > 0.05 in B1-B7 (A-hat need not be small); NUISANCE-DEPENDENT iff any variant has p_perm < 0.01 (reported as a finding: the null then depends on the treatment, the direction and amplitude of that variant are tabulated); the "5x larger errors than the published" statement is CONFIRMED iff the fixed-nuisance Fisher/bootstrap sigma_A (B1) is >= 2x below the profiled bootstrap sigma_A AND the published +/-0.04 is reachable (sigma_A(B5 weighted, fixed nuisances, Fisher) <= 0.08); otherwise the README's explanation is LABELLED AS NOT REPRODUCED.

**C. SPARC's sky footprint and the estimator's sensitivity: injection on mock skies** (`CFG192_attacks_CD.py`).
- C1 (analytic footprint response, no injection): the covariance of the position vectors (weights = 1/half-width^2 of the Birge-scaled curves), eigenvalues/eigenvectors, sigma along each axis by linearised Fisher with a-bar0 marginalised, the correlation of (log a-bar0, D along the footprint vector), the least-constrained direction and its angle to the footprint axis and to the fitted direction.
- C2 (curve-level injection, base = position-permuted real curves, the exchangeable null base): for A_inj in {0 (control), 0.1, 0.2, 0.3, 0.5}, N = 1000 trials each, injected direction uniform on the sphere (seed 19214), curve shift log10(1 + D_inj.n_i); refit with free direction (5 starts). Report per A_inj: mean and median A-hat; the mean component of D-hat along the true direction divided by A_inj (unbiased recovery ratio); median and 68% angular error; detection power at (a) A-hat above the 95th, (b) above the 99th, (c) above the 99.7th percentile of the A_inj = 0 control's own A-hat distribution (the S1 analogue), and (d) a nested check at A_inj in {0.3, 0.5}: 200 mocks with 499 fresh permutations each, power at p < 0.05.
- C3 (base = REAL positions and real curves, i.e. injection on top of the real sky's own realisation): N = 1000 at the same A_inj; recovery ratio and A-hat distribution; compare with C2 (difference = the effect of the real realisation).
- C4 (form/level attenuation, testing the README's explanation for the ~0.77 recovery): injection level in {curve, point} x form in {multiplicative log10(1 + D.n), log-linear 10^(D.n)} with the FIT form matched to the injection form, plus the mismatched pairs. If the attenuation is genuinely the "multiplicative fit to over-dispersed values", the matched log-linear/log-linear cell must recover ~1.0.
- C5 (footprint dependence): fixed injection directions: the footprint axis, the antipode of the footprint, the southern Galactic pole, the Galactic-plane directions l = 60, 150, 240, 330, the CMB dipole direction; N = 500 each at A_inj = 0.3 and 0.5: recovery ratio and power per direction.
- C6 (synthetic mock skies, exact-model check of the estimator): positions bootstrapped from the real footprint, Gaussian curves with the real per-galaxy widths and an additional intrinsic scatter tau = 0.34 dex, generated exactly from a0_i = a-bar0 (1 + D_inj.n_i); N = 2000 per A_inj. This isolates the estimator from the nuisance-profile curve shapes; C2 - C6 differences are the profile-shape effect.
- Pass/fail meaning: the ESTIMATOR IS FOOTPRINT-SENSITIVE iff the recovery ratio in C5 differs between the best and worst direction by > 0.15 or the power differs by > 2x; the README's null-hypothesis reading "SPARC cannot see a sky dipole below about 40%" is CONFIRMED iff the C2 power at p < 0.05 is < 0.5 at A_inj = 0.3 and > 0.2 at A_inj = 0.5 (a detection floor of roughly 0.4-0.6 in amplitude); if the power at 0.3 exceeds 0.5 the README's "about 40%" is LABELLED TOO PESSIMISTIC, if it is below 0.2 at 0.5 it is LABELLED OPTIMISTIC. A recovery ratio in [0.6, 0.95] at C2 matches the README's 0.77; outside, DISAGREES on the attenuation, and C4 diagnoses which cell.

**D. The 95% upper limit** (`CFG192_attacks_CD.py`).
- D1: my own Neyman (definition as frozen: for A_inj = 0 to 0.9 step 0.025, dipoles of amplitude A_inj in random directions injected into position-permuted curves; A95 = the smallest A_inj with P(A-hat >= A-hat_obs) >= 0.95); 1000 trials per cell (README: 300), simple and block permuted bases; monotonicity of P(A_inj) checked; MC noise from 3 independent seeds (19204 + 0, 1, 2); grid-refinement check at step 0.0125 near the crossing.
- D2: coverage of the limit procedure: from the C2 mocks (injected A_true in {0.1, 0.2, 0.3, 0.5}, random directions), compute each mock's own A95 by table lookup on the D1 table P(A-hat >= x | A_inj); fraction of mocks with A95 >= A_true (must be >= 0.95 for a valid 95% upper limit). Also for the fixed-direction ensembles of C5 (footprint axis, southern pole, CMB), where a random-direction Neyman table need not cover.
- D3: alternative definitions, reported next to A95: (i) the likelihood-ratio ordering (limit on A from Delta chi2 with the permutation-calibrated null), (ii) the bootstrap-percentile limit A-hat + 1.645 sigma_boot (one-sided), (iii) the Rayleigh/Maxwell approximation sigma_comp = 0.22 (the hand check).
- D4: the direction-specific limits A_fix + 1.96 sigma along CMB, bulk flow, Chang, Zhou, and Virgo (CFG182's numbers 0.24/0.36/0.55/0.53/0.19 are targets), each with a coverage check of the A_fix +/- 1.96 sigma interval by injection along that direction (500 trials at A_inj = 0.3).
- Meaning: A95 REPRODUCES iff within 0.06 of 0.425 (see 4). The limit is VALID (holds under injection) iff D2 coverage >= 0.93 in the random-direction ensemble; it is FLAGGED DIRECTION-DEPENDENT iff any fixed-direction ensemble covers < 0.90; it is FLAGGED "conditional on the scatter being noise" always (the Neyman base carries the real 0.34-dex scatter; if the scatter were partly an unmodelled dipole-like systematic the limit would be wrong in sign); D3 spread across (i)-(iii) > 0.15 is reported as definition-dependence.

**E. What the two published claims would have looked like in this pipeline** (`CFG192_attacks_E.py`).
Only repo files exist; the papers' data selection, distance handling, estimator and error model are UNKNOWN to me (abstract-level numbers relayed by CFG182 and unverified). So what I test is a family of plausible simple estimators and the question: could a pipeline of that kind produce 0.25 +/- 0.04 along Chang's direction or H = 0.37 +/- 0.04 at Zhou's axis on this SPARC copy?
- E1: estimator family on the real data (each with its own free dipole, fixed-direction A_fix along (171.30, -15.41), hemisphere H at (175.5, -6.5), bootstrap sigma with 500 resamples, and a permutation p): (a) primary; (b) fixed nuisances + Birge; (c) fixed nuisances, no Birge, global point-level chi2 with equal weights per point; (d) per-galaxy median deep-point estimator (2 log g_obs - log g_bar, g_bar < 4e-11, fixed nuisances) with equal weights on all 171; (e) same on the primary 149; (f) global fit with per-point weights but all Q.
- E2: reachability: does ANY variant give A_fix(Chang) in [0.20, 0.30] with sigma <= 0.06? and any give H(Zhou) in [0.30, 0.44] with sigma <= 0.08? Reported with its permutation p. If yes, the published number is REACHABLE by a simple estimator here and the tension is with the error model, not the data; if no variant does, the claims cannot be reproduced on this data by any of my simple estimators (a statement about my family, not about the papers).
- E3: significance of the published statistics at their pre-chosen axes under the exchangeable null: p_fixed(H >= H_obs at the Zhou axis) and p_fixed(A_fix along Chang >= A_fix,obs), without look-elsewhere; and the look-elsewhere version (max over axes). This is the "would 0.37 be unremarkable" claim of the README, testable without the papers.
- E4: retro-injection: inject an A = 0.25 dipole along Chang's direction (curve level, N = 500) and A = 0.37 along Zhou's axis; power of this pipeline to detect them (S1 line and p < 0.05) and the recovered mean A_fix. If power < 0.3, the pipeline cannot confirm a published-size dipole even when it is real.
- Meaning: the README's verdict "neither confirmed nor excluded" REPRODUCES iff (i) my A_fix along Chang has 0.25 inside its 95% interval, (ii) H at the Zhou axis has 0.37 inside its 95% interval, and (iii) E4 power < 0.5. CONTRADICTED if 0.25 lies outside my 95% interval (then "excluded" would be the correct wording, in this pipeline only). What CANNOT be tested: whether their +/-0.04 errors are correct, what sample/selection they used, whether their direction came from a fixed-Y fit; the statement about "fixed distances" is a hypothesis about their method, not a result.

## 7. Script plan (each < 15 min; actual expected 1-12 min; no absolute home path printed; the repo is resolved from `ZF_REPO` or by walking up from `__file__` and printed as `<repo>`)

- `CFG192_common.py` — loader, coordinates, kernels (nu_mono from its definition, P2, simple), profile engine, dipole fit, permutation/bootstrap helpers, Neyman helpers; prints nothing on import; no repo imports.
- `CFG192_profiles.py` — builds the per-galaxy curves (`CFG192_profiles.npz`, MUTATE=k writes `CFG192_profiles_MUTATE_k.npz`); about 3-4 min at step 0.01.
- `CFG192_main.py` — sample, unit and built-in checks, dipole fit, bootstrap (2000), permutations (5000 simple + 5000 block), splits (distance, inclination), footprint, hemisphere scan, PV template, class line; `MUTATE=1..7` -> `CFG192_MUTATE_k.out/.json`; exit 0 main / 1 iff MUTATE bites / 2 on error. About 6-8 min.
- `CFG192_attacks_AB.py` — attacks A and B (about 10-12 min at grid step 0.02, N_perm 1000, N_boot 500); exit 0.
- `CFG192_attacks_CD.py` — attacks C and D (C2 1000 x 5, C3, C4, C5, C6, D1 with 3 seeds; about 12 min; if a projected run would exceed 15 min the trial counts are cut in half and the cut is printed, never silently); exit 0.
- `CFG192_attacks_E.py` — attack E (about 4 min); exit 0.
- `CFG192_compare.py` — PHASE 2 ONLY: runs after all of the above are saved; reads CFG182's `*_results.json` (only then) and diffs every row of 2 and the S1-S3 lines against mine; also the nu_mono cross-check (imports `CFG4_common` read-only for the kernel; prints `<repo>`); exit 0.
- `run_all.sh` — runs profiles, main, MUTATE 1-7, the attack scripts, compare (phase 2 only); a second in-place run must be byte-identical (sha256 of every .out, timing lines excluded by writing timings only to stderr).

## 8. What counts as disagreement

DISAGREES: as defined in 4 (a)-(e) — any of S1-S3 flips; p_A off by more than 0.15; A-hat off by more than 0.10; N off by more than 2; A95 off by more than 0.15. Additional findings that I will report as disagreements with the README's reading even if the numbers reproduce: (1) any A/B cell with p_perm < 0.01 (the null depends on the sample or the treatment); (2) the recovery ratio outside [0.6, 0.95], or the C4 matched-form cell recovering ~1.0 (the README's explanation of the 0.77 would then be the fitted form, but the amplitude convention would need restating), or not (the explanation would be wrong); (3) D2 coverage < 0.93 (the A95 is not a valid 95% limit for the ensemble it claims); (4) the detection floor statement ("cannot see a dipole below about 40%") violating the C2 power rules in 6C; (5) the "5x larger than published" explanation not reproduced (6B); (6) the S3 line: because the 95% cone (115 deg) covers most of the sphere, S3 can only pass for a strongly detected signal, so S3 is not an independent test of footprint alignment; I will report S3's status under the primary definition and, additionally, a footprint-alignment statistic that does not depend on the cone (angle between the fitted and footprint axes versus the same angle in the permutation nulls; p reported). Not counted as disagreement: direction misses with A-hat and p in tolerance; MC-noise-level differences in A95 (within 0.06); differences in Monte Carlo p within 0.05.

The referee will not say the framework's flow is excluded or supported. A null on SPARC's a0 dipole bounds only readings in which the flow modulates a0 with sky direction at the 40%-level; a uniform flow predicts no sky dipole at all (CFG182's own statement, adopted).
