# FROZEN A28: "LCDM fits the data just as well", per-galaxy fits with nuisances, and the reverse RAR

Frozen before any A28 number. Script `scripts/recipe30.py`, output `scripts/recipe30.out`, checkpoint `scripts/recipe30.json`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. A comparable fit to data is not a derivation, and a better or worse fit is not proof for either side. kappa = 1/2 FITTED; not theory closed.

## Question

The swoop: "LCDM halos fit SPARC as well as the law does, so the law is nothing special." Two parts. (1) Fit the OBSERVED rotation curves galaxy by galaxy, every model with the same nuisance freedom inside published priors, and compare fit quality with every parameter counted. (2) Reverse: from each LCDM model's best-fit curves and fitted nuisances, rebuild g_b and g_model and measure the radial acceleration relation the LCDM population produces. Does it come out as the law with the tied a0, or does it only reproduce the data?

## Data (as lib.load, plus the table)

The 171 galaxies and 3373 points of `lib.GS` (points with nominal V_b^2 > 0 at Upsilon 0.5/0.7, at least 5 points). Per point from the rotmod files: R, V_obs, errV, V_gas, V_disk, V_bul. Per galaxy from `SPARC_Lelli2016c.mrt`: D, e_D, Inc, e_Inc, L[3.6], R_disk, M_HI, Q. The point set is fixed at lib's; where a fitted Upsilon makes V_b^2 <= 0 at a point, g_b is clipped at 1e-14 m/s^2 for the law and counted (printed).

## Nuisances, all models (Li, Lelli, McGaugh, Schombert 2018, A&A 615, A3 style; prior widths from memory, not re-checked)

- Upsilon_disk: log-normal, centre 0.5, sigma 0.1 dex.
- Upsilon_bulge: log-normal, centre 0.7, sigma 0.1 dex; only for galaxies with any V_bul > 0.
- Distance: Gaussian, centre D, sigma e_D (table).
- Inclination: Gaussian, centre Inc, sigma e_Inc (table), bounded to [10, 90] deg.
Each nuisance is fitted in prior-pull units z, bounded |z| <= 5. Scalings: r -> r f_D, V_k^2 -> V_k^2 f_D for every baryon component, f_D = D_fit/D; V_obs and errV -> times sin(Inc)/sin(Inc_fit). For model R the inputs L, M_HI scale with f_D^2, R_disk with f_D, M_* = Upsilon_disk,fit x L (lib's convention, bulge light inside L), M_b = M_* + 1.33 M_HI, enclosed baryon mass from the refitted V_b.

## Models (per galaxy)

- (L) the law, g = (g_b + sqrt(g_b^2 + 4 g_b a0))/2, a0 = lib A0 = 9.3625e-11 m/s^2 from the tie with kappa = 1/2. 0 global knobs tuned here; kappa = 1/2 was itself FITTED elsewhere, so a second count with 1 global is printed. Free: nuisances only (3 or 4 per galaxy).
- (N) plain LCDM NFW: dark mass (1 - f_b) M_NFW(r; M200, c), f_b = min(M_b/M200, 0.5) (the recipes' convention), total g = g_b + G M_dark/r^2. Free per galaxy: log M200 in [8.5, 15.5] and log c in [0, 2], plus nuisances. Priors: SHMR, (log M_*,fit - log M_*^Moster13(M200))/sigma_SHMR with sigma_SHMR = 0.15 dex (lib's Moster et al. 2013 z = 0 coefficients N 0.0351, log M1 11.59, beta 1.376, gamma 0.608; scatter value from memory); concentration, (log c - log c_Diemer19(M200, z=0))/0.11 (colossus diemer19, 200c; 0.11 dex from memory). No halo-mass-function weighting (stated). Sensitivity row N20: sigma_SHMR = 0.20 dex.
- (R) R11b, `recipe18.gal3(g, K11B, [])` with all 14 global knobs frozen at K11B (tuned in A4 on the LAW's curves, not on data). Free: nuisances only. 14 global parameters counted.
- (C) coreNFW (Read et al. 2016 form, as in A18): M_dark,core = M_dark,NFW(r) tanh(r/r_c)^n, r_c = 1.75 x 1.68 R_disk,fit, n in [0, 1] flat prior (no Gaussian term). Same M200 and c priors as N. Free per galaxy: log M200, log c, n, plus nuisances.

Fit: per galaxy, scipy least_squares on the residual vector [(V_obs,fit - V_model)/errV_fit over points; the Gaussian prior pulls]. Starts: L and R one start (z = 0) plus one at z_Upsilon = +-1 (best kept); N and C three starts (prior centre, log M200 +-0.5 dex), C each at n 0.1 and 0.9. Cost chi2_post = chi2_data + sum of prior pulls^2.

## Statistics, all frozen now

- Per model: total chi2_data, total chi2_post, total free parameters k (nuisances + per-galaxy halo + globals), AIC = chi2_post + 2k, BIC = chi2_post + k ln N with N = 3373 data points.
- Acceptable fit per galaxy: p >= 0.01, from chi2_post with dof = N_g + n_gauss - k_g (n_gauss Gaussian prior terms, k_g free parameters in that galaxy: dof = N_g for L, N, R; N_g - 1 for C). Secondary: p from chi2_data with dof = max(N_g - k_g, 1). Reported also on the Q < 3 and Inc >= 30 subset.
- Prior pulls: for each model, the fraction of fitted nuisances with |z| > 2 (overall and per kind: Upsilon_disk, Upsilon_bulge, D, Inc), and for N and C the fractions with |z_SHMR| > 2 and |z_c| > 2; fraction at the |z| = 5 bound.
- Pairwise per-galaxy: median delta chi2_post (N - L, R - L, C - L) and the number of galaxies where each beats L.

## Reverse question (the RAR the fits produce)

For each model X in {L, N, N20, R, C}: rebuild per point g_b,X = (V_gas^2 + Upsilon_d,fit V_disk^2 + Upsilon_b,fit V_bul^2) f_D / (r f_D) (clipped as above) and g_model,X = V_model^2/(r f_D); also g_obs,X = V_obs,fit^2/(r f_D).
- a_X = lib.fit_a(g_b,X, g_model,X) (least squares in log over all points); intrinsic scatter s_X = rms of log g_model,X - log law(g_b,X, a_X); rms to the tied law t_X = rms of log g_model,X - log law(g_b,X, A0); worst 0.5-dex g_b bin mean of the tied residual (>= 50 points).
- The same three numbers for the data under that model's nuisances (g_obs,X against g_b,X): the observed RAR each model's nuisances imply.
- Recovery gates for the LCDM rows (N, N20, C, R): Ra |log10(a_X/A0)| <= 0.05 dex; Rs s_X <= 0.057 dex (Li et al. 2018's quoted RAR rms after their fits, from memory); Rt t_X <= 0.02 dex and worst bin <= 0.02 (E1/E3-type). "Recovers the law's relation and the tied a0" only if Ra, Rs, Rt all pass. A pass would still say the fit's curves look like the law on these galaxies, not that LCDM produces it; L passes by construction (control: s_L = t_L = 0, a_L = A0).

## Expected in advance

- L: most galaxies acceptable (about 80 to 90 % at p >= 0.01), small pulls (under 10 % beyond 2 sigma), as Li et al. 2018 found.
- N: chi2 comparable or somewhat worse than L in total, with two more parameters per galaxy; BIC worse than L; many galaxies pulled off the SHMR or c(M) beyond 2 sigma (20 to 40 %), mostly low c / cored dwarfs; acceptable fraction somewhat below L.
- R: close to L (R11b sits 0.0275 dex from the law) but slightly worse total chi2; BIC worse than L by the 14 globals plus the chi2 gap.
- C: best raw chi2 of the LCDM rows; BIC still worse than L.
- Reverse: N and C curves give a RAR with a_X within about 0.1 dex of A0 (they track the data, which track the law) but scatter s_X 0.05 to 0.1 dex and t_X above 0.02: they reproduce the data, not the law (Ra may pass, Rs or Rt fail). R recovers it best (t near 0.03, built from the law), still failing Rt.

## Pre-run disclosure

A timing test fitted the first 6 galaxies with each model (times only printed: 0.4, 1.1, 0.7, 2.9 s); no fit number was read. No criterion changed. Full run 160 s, 88 MB RSS, single thread.

## RESULTS (written after the run, `scripts/recipe30.out`; criteria above unchanged, no bug found)

Fit quality, all 171 galaxies, 3373 points:

| model | globals | k total | chi2_data | chi2_post | AIC | BIC | acceptable (p >= 0.01) | on data chi2 | Q<3, Inc>=30 (149) |
|---|---|---|---|---|---|---|---|---|---|
| L law, tied a0 | 0 (1 if kappa counted) | 545 (546) | 13668.4 | 15316.8 | 16406.8 (16408.8) | 19744.2 (19752.3) | 79 | 88 | 66 |
| N NFW, SHMR 0.15 | 0 | 887 | 11135.2 | 12955.6 | 14729.6 | 20161.2 | 96 | 91 | 81 |
| N20 NFW, SHMR 0.20 | 0 | 887 | 10969.7 | 12675.1 | 14449.1 | 19880.7 | 100 | 95 | 85 |
| R R11b frozen K11B | 14 | 559 | 15708.3 | 17366.0 | 18484.0 | 21907.0 | 86 | 87 | 71 |
| C coreNFW | 0 | 1058 | 7816.0 | 9209.9 | 11325.9 | 17804.6 | 119 | 114 | 102 |

Prior pulls beyond 2 sigma (nuisances; halo terms): L 0.215 (Upsilon_disk 0.374, Upsilon_bulge 0.375, D 0.170, Inc 0.070; 14 at the |z| = 5 bound); N 0.073 (SHMR 0.175, c 0.228, median z_c -0.38); N20 0.066 (SHMR 0.164, c 0.222); R 0.206 (Upsilon_disk 0.298, Upsilon_bulge 0.438; 17 at bound); C 0.057 (SHMR 0.146, c 0.205, median n 0.33). Against L per galaxy, median delta chi2_post: N -2.85 (beats L in 111), N20 -3.65 (115), R -0.86 (103; mean +11.98), C -12.51 (154).

Reverse RAR from the fitted curves and fitted nuisances:

| model | a_fit | log a/A0 | scatter about law(a_fit) | rms to tied law | worst bin | Ra | Rs | Rt |
|---|---|---|---|---|---|---|---|---|
| L (control) | 9.363e-11 | +0.000 | 0.0000 | 0.0000 | 0.0000 | - | - | - |
| N | 1.186e-10 | +0.103 | 0.1254 | 0.1310 | 0.0617 | FAIL | FAIL | FAIL |
| N20 | 1.209e-10 | +0.111 | 0.1230 | 0.1296 | 0.0579 | FAIL | FAIL | FAIL |
| R | 9.344e-11 | -0.001 | 0.0323 | 0.0323 | 0.0183 | PASS | PASS | FAIL |
| C | 1.065e-10 | +0.056 | 0.1368 | 0.1383 | 0.0524 | FAIL | FAIL | FAIL |

The data under each model's own nuisances: L a 8.63e-11 (-0.035 dex), scatter 0.1144; N +0.045 dex, 0.1636; N20 +0.053, 0.1611; R -0.042, 0.1171; C +0.036, 0.1659.

Verdict. On fit quality the swoop holds, in rival terms: per-galaxy LCDM halos with priors fit the observed curves better than the tied law in raw chi2 (chi2_post N -15.4 %, C -39.9 %), and coreNFW is better on AIC and BIC too; plain NFW is better on AIC, worse on BIC by 417.0 (342 more parameters; N20 by 136.5). R11b, built on the law, fits slightly worse than the law. But the fits do not recover the law: the LCDM populations' own curves give a relation with a 0.06 to 0.11 dex above the tied A0 and 0.12 to 0.14 dex scatter about it, wider than the law's zero and no tighter than the data. They reproduce the data, not the relation or the tied a0. Only R11b recovers the scale and a tight relation (0.032 dex), because its 14 knobs were tuned to the law's curves; that is the A4 result, not a derivation, and it still fails Rt. A comparable or better fit to data is not a derivation; a better or worse fit is not proof for either side.

Against expectation: L acceptable in only 79 of 171 (expected 80 to 90 %), with Upsilon_disk beyond 2 sigma in 37 % (high 23 %, low 14 %); C landed best on BIC, not expected; N beat L on AIC, not expected. Data chi2 is dominated by a few galaxies with small listed errors (top five carry 29 to 38 % of each total: UGC06787, NGC2403, IC4202, UGC02953 and others), and SPARC's errV carry no systematic floor, so absolute p-values are harsh for every model alike.

Post-run checks (diagnostics, not gates):
- Code: at the prior centre, model L and R reproduce lib's law and recipe18 gal3 curves, and the rebuilt g_obs reproduces lib's, to 2e-15 dex.
- Optimiser: 12 extra starts per galaxy (Upsilon_disk, D, Inc at +-2 sigma, c shifted for N): L improves 0.0 in total, R 0.9, N 87.6 (3 galaxies over 1, largest 76.8). So N's table chi2 is high by about 0.7 %; no row ordering or verdict changes.
- Robust spread of the model-curve residual to the tied law: median per-galaxy rms N 0.085, C 0.090, R 0.018; 1.4826 MAD N 0.090, C 0.092, R 0.017. On the Q<3, Inc>=30 subset: N 0.128, C 0.137, R 0.031. The N and C failures are not driven by a few galaxies.

Provisional or from memory: Li et al. 2018 prior widths (0.1 dex Upsilon, e_D, e_Inc from the table) and their 0.057 dex RAR scatter used for Rs; SHMR scatter 0.15/0.20 dex and c scatter 0.11 dex; the Read et al. 2016 r_c = 1.75 R_half with R_half = 1.68 R_disk. No web look-up, no download. Not done: halo-mass-function weighting of the SHMR prior, adiabatic contraction in N, a per-galaxy a0 or Upsilon-free law row, a velocity error floor.


Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
