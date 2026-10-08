# CFG493 FROZEN CRITERIA: a combined measurement of kappa from independent M/L-insensitive routes

Written and committed before any script for this lane exists and before the combination, the WALLABY re-run on the framework kernel, or any lever below has been computed. kappa = 1/2 is FITTED; here kappa is MEASURED, never derived. Both footings are reported. No dark-matter particle; the cold mass is still required. On-disk data and committed results only; nothing is fetched.

## 0. What I have already seen (disclosure)

The inclusion rules below were written AFTER reading these committed route-level numbers, so they cannot be called blind. They are listed so the reader can judge.

- MNRAS v3 estimators (paper_numbers.json, Planck-consistent convention): A 0.450 +- 0.073, B 0.584 +- 0.184, C 0.434 +- 0.077 (kappa on the rho_Lambda footing); the gas-calibration floor eq. (9.5 per cent; s_Upsilon 0.17, s_g 0.115).
- CFG397 / CFG442 / CFG449: SPARC gas-dominated points on ladder distances, nu_mono. CFG449 verdict sample (12 galaxies) log a0 -10.069 +- 0.090; CFG397 anchor (10) -9.953 +- 0.071; SPARC Hubble-flow gas points (19) -10.180 +- 0.085; K1 Upsilon 0.5 -> 0.7: -0.031 dex. Two LITTLE THINGS reductions sit +0.16 / +0.20 dex above SPARC on the same dwarfs (C2 failed twice).
- CFG309 / CFG306: MIGHTEE-HI catalogue width chain, rest frame (k = 0): a0 1.311e-10 at the catalogue's H0 = 70, 1.208e-10 at H0 = 67.4; recipe terms delta 0.098, M* 0.069, D_HI 0.026, H0 0.036 dex; HI-only flux-shift grid (P3, P3b); kernel table (P2); SPARC M_HI minus ALFALFA +0.053 dex (P6).
- CFG304: MIGHTEE catalogue / ALFALFA flux, code 1: median -0.1945 dex (68 per cent -0.250 to -0.156).
- PAPER43 / p43: WALLABY DR2 gas points 7.28e-11 +- 23 per cent at H0 = 73 with the QUADRATURE kernel sqrt(1 + 1/y); H0 70 6.67e-11; CMB-frame table distances 4.88e-11; flux uncorrected 8.35e-11; AD 8 km/s 7.68e-11; R_d x0.5 / x2 8.13 / 6.79e-11; EFE maxclu +8.5 per cent. PAPER43 pool 8.3e-11 +- 13 per cent.
- CFG261 KiDS: late-type s* 1.67 (z 0.2) / 0.68 (z 0.4), early-type 2.48 / 4.12; M* lever -1.1; joint rows fail one s (p 4.6e-6).

NOT seen: WALLABY on nu_mono at H0 = 67.4; any lever of this lane; the combined value; any verdict.

## 1. Quantity and footings

L = log10 a0 [m s^-2]. kappa_Lambda = a0 / (c sqrt(G rho_Lambda)), kappa_crit = a0 / (c sqrt(G rho_crit)), with H0 = 67.4 and Omega_Lambda = 0.685 (the record's canonical footing: kappa = 1/2 <=> a0 = 9.3603e-11; alt footing kappa = 1/2 <=> a0 = 1.1312e-10). One combined a0 is converted to both footings; the footing is a denominator, not a separate fit. Kernel: nu_mono (owner decision 09-26), identical to the exponential RAR kernel for y <= 2.34, which covers every point used here. Other kernels are a reported variant (law definition), not an error term.

## 2. Routes and inclusion rules

A route enters the combination only if ALL hold:
- I1 its a0 is in a committed artifact, or is recomputed here from on-disk data with a control that reproduces the committed number (tolerances in section 6);
- I2 it is M/L-insensitive: a +-17 per cent change of the stellar mass scale moves its log a0 by <= 0.05 dex;
- I3 it passed its own lane's load-bearing controls (a route whose own lane failed a load-bearing control, or whose sub-samples are not described by one a0 at p >= 0.01, is excluded);
- I4 no galaxy enters two included routes (one route per survey);
- I5 its distances can be put on the footing's convention (Hubble-flow distances at H0 = 67.4; ladder distances unchanged).

Primary routes (declared now):
- **P1 SPARC gas-dominated points, ladder distances** = CFG449's verdict sample S0 + SR (12 galaxies), recomputed with CFG449's statistic (bounded min of weighted log-g residuals, nu_mono, galaxy bootstrap 500, seed 7).
- **P2 MeerKAT MIGHTEE-HI widths** = CFG309's rest-frame (k = 0) chain at H0 = 67.4 (CFG306 P7: 1.2078e-10), moved to the single-dish flux scale (section 3).
- **P3 WALLABY DR2 gas points** = p43's method re-implemented in this lane with the kernel switched to nu_mono and Hubble-flow distances at H0 = 67.4 (p43's catalogue flux correction kept).

Report-only (never in the primary combination), with the reason: SPARC estimators A, B, C (same galaxies as P1, I4; A and C are M/L-entangled, I2); SPARC Hubble-flow gas points (same survey as P1, I4); LITTLE THINGS (I3: C2 failed in CFG442 and CFG449); KiDS-1000 lensing (I2: M* lever -1.1; I3: joint rows p 4.6e-6); Desmond 2023 (SPARC, I4; literature); PAPER43 pool (contains P1-like and P3-like data, I4).

## 3. Systematic model

Each route r has L_r = L_true + sum_k lambda_rk delta_k + e_r. The shared parameters delta_k are Gaussian with mean 0:
- **S_gas** gas-mass scale (absolute single-dish HI scale 10 per cent, helium 1.33-1.40, CO-dark/H2 0-10 per cent, in quadrature): sigma 0.0473 dex (11.5 per cent, the MNRAS committed s_g). Lever lambda_r,gas = d log a0 / d log M_gas, measured per route (P1: re-fit with gas x 1.1; P2: CFG306 P3 k = 0 HI-only grid, slope between R = 0 and R = -0.1945; P3: re-fit with Sigma_HI x 1.1).
- **S_star** stellar mass zero point: sigma 0.068 dex (17 per cent). Lever measured per route (P1: Upsilon 0.5 -> 0.7; P2: CFG306 recipe M* term 0.069 dex per 0.25 dex; P3: ups_scale 1.0 -> 1.4).
- **S_HF** Hubble-flow distance scale (local H0 relative to 67.4): sigma 0.0174 dex (half the Planck-SH0ES gap log10(73.04/67.4)). Lever on P2 and P3 measured (P2: CFG306 H0 70 -> 67.4; P3: re-fit at H0 70 and 67.4); P1 lever 0 (ladder).

Flux tie (every route put on the single-dish scale): P1 applies the committed SPARC-minus-ALFALFA M_HI offset (-0.0527 dex on M_gas, CFG306 P6); P2 applies CFG304's -0.1945 dex (catalogue -> ALFALFA, M_HI raised by 0.1945); P3 keeps p43's catalogue correction. Transfer uncertainty, uniform rule: half the applied shift in a0 (P2 also adds CFG304's 68 per cent half-width 0.047 dex in M_HI, times its lever).

Route-unique terms e_r (Gaussian, independent):
- P1: galaxy bootstrap SD; rotation-curve reduction = half the mean committed SPARC-vs-LITTLE-THINGS overlap offset ((0.196 + 0.16)/2/2 = 0.089 dex); ladder zero point 0.01 dex in distance times the measured distance lever; flux-tie transfer.
- P2: bootstrap SD (CFG306 k0_boot sd_dex); width recipe = quadrature of CFG306's k = 0 delta and D_HI terms (the M* and H0 terms are the shared S_star / S_HF and are not double counted), taken as 1 sigma; flux-tie transfer.
- P3: bootstrap 68 per cent half-width in dex (200 resamples, seed 43); distance frame = half |log a0(HF) - log a0(CMB-frame table)|; asymmetric drift = full 8 km/s shift; R_d = larger |shift| of x0.5 / x2; EFE = half p43's committed maxclu shift (0.5 x log10 1.085); flux-tie transfer = half |log a0(corrected) - log a0(uncorrected)|.

Combination: generalised least squares on L with C = diag(e_r^2) + Lambda Sigma Lambda^T. Output: L_hat, sigma_hat, GLS weights; consistency chi^2 with 2 dof; **ROUTES IN TENSION** flag if p < 0.05 (reported with the verdict, which is still computed).

## 4. Power label (computed from the error model alone, printed before any central value)

The nearest competitors to kappa = 1/2 on the canonical footing are 0.0355 dex (cH_Lambda/2 pi) and 0.0522 dex (1/sqrt pi) away. Excluding a competitor at 2 sigma when the truth is 1/2 needs sigma_hat <= gap/2 (with no noise luck). Label: **POSSIBLE** if sigma_hat <= 0.0178 dex (all competitors), **PARTIAL** if 0.0178 < sigma_hat <= 0.0261 (1/sqrt pi and 0.6 only), **NOT POSSIBLE** otherwise. Also printed: the shared-systematic floor (sigma_hat with every unique term set to 0) against the goal of 2-3 per cent (0.0087-0.0128 dex).

## 5. Verdict (per footing)

Candidates, as a0: canonical footing kappa_Lambda in {1/2 (9.3603e-11), 1/sqrt pi (0.5642), 0.6, Milgrom cH0/2 pi (kappa_Lambda 0.5567), cH_Lambda/2 pi (kappa_Lambda 0.4607)}; alt footing kappa_crit in {1/2 (1.1312e-10), 1/sqrt pi, 0.6, cH0/2 pi (kappa_crit 0.4607)}. Pull = |L_hat - L_c| / sigma_hat.
- pull(1/2) >= 2: **INCONSISTENT WITH 1/2**;
- else every competitor of that footing has pull >= 2: **CONSISTENT WITH 1/2 & DISCRIMINATING**;
- else **CONSISTENT BUT NOT DISCRIMINATING**.
Also reported: the pull between the two footings' 1/2 values (9.36e-11 vs 1.131e-10). A pull below 2 is never a detection; a lean is reported as a lean.

## 6. Controls (load-bearing unless marked)

- K1 footing identities: c sqrt(G rho_Lambda) from constants reproduces 2 x 9.3603e-11 to 0.1 per cent; kappa_crit = kappa_Lambda sqrt(Omega_Lambda) exactly.
- K2 reproductions: P1 log a0 -10.0686 (tol 1e-4 dex) and bootstrap SD 0.0897 (tol 2e-3); P3 control with p43's settings (quadrature, H0 73) 7.282e-11 and H0 70 6.667e-11 (tol 0.5 per cent each); P2 inputs read from CFG306's JSON equal 1.2078e-10, 1.3111e-10 and 9.0133e-11 (tol 1e-3 relative).
- K3 coverage: 4000 mock route vectors from N(L_1/2, C): mean pull within +-0.05, SD 0.95-1.05; fraction with consistency p < 0.05 within 0.035-0.065.
- K4 GLS weights sum to 1 (1e-12); three identical inputs return the input.
- I2 is checked numerically for every primary route.

## 7. MUTATE (separate run, --mutate, outputs *_MUTATE.*)

Inject +10 per cent (+0.04139 dex) into the primary route with the largest GLS weight.
- M1 (load-bearing) L_hat moves by w_r x 0.04139 (1e-9).
- M2 (reported, no pass requirement) at the real errors: the route's pull against the others and whether ROUTES IN TENSION fires. If it does not, that is the power statement (a 10 per cent single-route shift is invisible at present errors), not a failure.
- M3 (load-bearing) precision world: every route's unique sigma set to 0.0107 dex (2.5 per cent) and every shared sigma to 0.005 dex; with the same +10 per cent injection the flag must fire (p < 0.05), and must not fire without it.

## 8. Variants (reported, never the verdict)

V1 SPARC route = estimator C (committed total sigma as unique, no shared levers); V2 = estimator A (same treatment); V3 kernel = quadrature sqrt(1 + 1/y) for all three routes (P1, P3 re-fit; P2 via CFG306's closed-form k = 0 row); V4 no flux tie (each route on its own flux scale); V5 P2 flux offset -0.087 (CFG306 S2 z-trend extrapolation); V6 Hubble-flow distances at H0 = 73.04 with rho_Lambda kept at 67.4; V7 footing rebuilt at H0 = 73.04 (Omega_Lambda fixed; Hubble-flow distances at 73.04); V8 KiDS late-type rows added as a fourth route (CFG261 jackknife SD plus the inner +-0.17 dex M* band); V9 no P1 rotation-curve reduction term; V10 recipe and transfer half-widths as uniform (/sqrt 3); V11 P1 = CFG397's 10-galaxy anchor.

## 9. Dominant systematic

Terms are grouped (statistics; S_gas; S_star; S_HF; ladder zero point; flux-tie transfer; P1 rotation-curve reduction; P2 width recipe; P3 distance frame; P3 AD/R_d/EFE). The group whose removal lowers sigma_hat most is named dominant; the kernel (V3 shift) is reported beside it as the law-definition term.

## 10. Hand estimates (before running)

HE1 P1 after the flux tie about -10.03 +- 0.13. HE2 P2 about -10.08 +- 0.14. HE3 P3 on nu_mono at H0 = 67.4 about -10.25 (+-0.1), +-0.15 total. HE4 combined about -10.10 +- 0.08 (kappa_Lambda about 0.43). HE5 power label NOT POSSIBLE. HE6 verdict CONSISTENT BUT NOT DISCRIMINATING on the canonical footing. HE7 dominant group: S_gas or a route-unique reduction term. HE8 MUTATE M2 does not flag.

## 11. Outputs

cfg493_kappa_combined.py -> .out, _results.json; --mutate -> _MUTATE.out, _MUTATE_results.json; README.md in plain language. Committed locally; not pushed.
