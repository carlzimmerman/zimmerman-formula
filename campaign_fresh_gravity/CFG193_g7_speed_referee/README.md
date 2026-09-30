# CFG193 -- independent re-derivation ("referee") of CFG186: does SPARC's a0 depend on speed through the CMB frame? (door 11C, gate G7)

Frozen criteria, committed before any script: `CFG193_FROZEN_CRITERIA.md` (sha256 dc90bef8...; git subject "CFG193: frozen criteria"). Every script and output here is named `CFG193_*`. No new data, no network, nothing outside this directory edited, no absolute home path in any output (the repo root prints as `<repo>`). kappa = 1/2 stays FITTED and enters nothing; nothing here says the data favour the framework; a NON-DIAGNOSTIC result is valid.

## Bottom line
- **CFG186's headline holds: the test is NON-DIAGNOSTIC and G7 stays open.** My own Fisher row is 0.447 against CFG186's 0.453; my beta_det (2 sigma) is 2.56 (mocks 1.28) against the G7 line 0.10; every uncertainty figure I get (0.45 to 1.3) is 9 to 26 times the 0.05 that G7 needs.
- **The sample and the speeds reproduce.** The clean sample is 149 galaxies, the primary sample the same 68 galaxies (37 TRGB, 3 Cepheid, 26 Ursa Major, 2 SNIa), and no galaxy's u differs by more than 8.5 km/s (the limit was 20).
- **Why my beta_hat differs from CFG186's (corrected after the CFG186 owner's check; my first wording was wrong).** CFG186's beta_hat = +0.89 and shuffle p = 0.078 depend on one undeclared modelling choice in one galaxy. CFG186 bounds each galaxy's inclination to within 8 sigma_Inc of the catalogue value (and Upsilon to +-10 in 0.1-dex units); I did not (my bounds: log10 Upsilon in [-1.6, 0.8], inclination [5, 89] degrees; the frozen text says only "inclination Gaussian"). For NGC2403 at the distance floor (t = -4) and high a0 the data want an inclination of 38.2 degrees, 8.26 sigma from the catalogue 63.0 +- 3.0 degrees, outside CFG186's box [39.0, 87.0]. With CFG186's box imposed my fitter returns CFG186's stored value (771.306 by scipy bounded least squares, 771.319 by my batch profiler, against 771.310 stored). So CFG186's curve is **not** stuck in a local minimum of its own objective, and "numerical error" and "trapped" were wrong. Putting my box-constrained NGC2403 curve into my curves gives beta_hat = +0.931 (+0.936 with grid-node t only), close to CFG186's +0.887. Without the box: beta_hat = +0.49 (bootstrap sigma 0.70; shuffle p = 0.22; conservative 95% upper limit 3.0). So beta_hat moves by about 0.4 depending on whether one galaxy's inclination is boxed at 8 sigma. That is a fragility of the estimator, not an error in either lane, and it changes no verdict.
- **Where I am not independent:** the data files, the NED cz column, the nu_mono kernel, and the frozen design (section "Where independence stops").

## What was reproduced (my own code from the frozen text)
Own loader; own four-source velocity chain; own CMB-frame conversion, z_cos, u; own batch Levenberg-Marquardt profiler (Upsilon_disk, Upsilon_bul, inclination), 2D curves on the frozen grids; own Birge / tau weighting (Addendum 2 form); own statistic F(L, beta) with a cubic (Catmull-Rom) interpolation in log a0; own bootstrap, speed shuffles, Fisher row, mocks, Neyman construction. Only CFG186's *outputs* were read, and only after my main and MUTATE runs were saved (`CFG193_compare.py`).

## Row by row against CFG186 (classification: DEFINITION / NUMERICAL / README typo / FRAMING; "CFG186 error" where I can show one)
| quantity | mine | CFG186 | class |
|---|---|---|---|
| raw sample (Q<=2, Inc>=30, no point cut) | 153 (83/39/3/26/2) | not stated | see "153 vs 149" |
| clean sample (>=5 usable points) | 149 (81 HF, 37, 3, 26, 2) | 149 | match |
| primary sample | 68 = 37/3/26/2, same 68 names | 68 = 37/3/26/2 | match |
| velocity sources, all 175 (NED / UNGC / KT / 2MRS / none) | 126 / 20 / 12 / 3 / 14 | 126 / 20 / 16 / 2 / 11 | DEFINITION: CFG186 uses KT2017 for every match once 99% of groups have distinct member velocities; I test each group. No primary galaxy affected (cz identical on all 142 galaxies both have; only F583-1, a Hubble-flow galaxy, has a velocity in CFG186 and not in mine; 8 label-only "KT2017" vs "KT17"; UGC11914 labelled 2MRS vs KT17 with the same cz) |
| clean Hubble-flow galaxies with a velocity | 74 | 75 | DEFINITION (F583-1) |
| flagged source disagreements (>50 km/s) | UGC01281, ESO563-G021 | same two | match (README calls UGC01281 "the one gross mismatch"; the JSON lists two pairs, ESO563-G021 at 81 km/s: README wording only) |
| u, max abs difference over the 68 (my comoving D vs CFG186's luminosity-D convention, CFG186's cz) | 8.5 km/s (0 galaxies > 20) | -- | DEFINITION (CFG186's z_cos treats D as a luminosity distance; the frozen text says only "distance D"). With my luminosity variant the difference is 0.00 |
| sigma_u median TRGB / UMa | 15.6 / 168.7 km/s | 15.6 / 169.1 | match |
| rms z, r(u, V_LG.n) | 0.2357, 0.751 | 0.2351, 0.755 | NUMERICAL |
| median Birge s | 1.43 | 1.43 | match |
| median sigma_i | 0.1705 dex | 0.1681 | NUMERICAL |
| tau, L0 | 0.3397, -10.081 | 0.3445, -10.080 | NUMERICAL |
| three galaxies at the lower a0 grid edge | CamB, NGC2976, UGC07577 | same | match |
| **Fisher sigma_beta (W1, H0 67.66)** | **0.4469** | **0.4528** | NUMERICAL (-1.3%) |
| Fisher W2 / H0 = 73 | 0.596 / 0.402 | 0.607 / 0.409 | NUMERICAL |
| mock sigma_beta at beta = 0 | 1.28 (my point-level mocks, N=40) | 2.25 (curve-level mocks) | DEFINITION: different mock constructions; see below |
| beta_det (2 sigma) | 2.56 | 4.50 | DEFINITION (same reason); both >> 0.10 |
| **beta_hat** | **+0.494 (+0.931 with CFG186's box on NGC2403)** | **+0.887** | **DEFINITION (modelling choice, not an error): CFG186's inclination box of +-8 sigma_Inc, active for NGC2403; below** |
| log10 abar0 | -10.037 (9.18e-11) | -10.096 (8.02e-11) | follows from beta_hat |
| bootstrap sigma (16-84 half-width) | 0.702 | 0.666 | NUMERICAL (5%) |
| bootstrap 2.5-97.5% | [-0.345, +3.880] | [-0.047, +3.426] | follows from beta_hat |
| speed-shuffle p (two-sided) | 0.220 | 0.0785 | follows from beta_hat: my fitter on CFG186's curves gives 0.050 (400 permutations) |
| shuffle null 16-84% | [-0.23, +0.71] | [-0.50, +0.50] | DEFINITION: my beta lower bound (0.05 - 1)/z_max = -0.231 (z_max over all t) piles the lower tail up; CFG186 continues 1 + beta z below 0.05 with a penalty. The lower tail cannot matter for a positive beta_hat |
| within-method shuffle p | 0.331 | 0.104 | follows from beta_hat |
| noise-injection p | 0.415 (N=40) | 0.561 | DEFINITION / FRAMING: different noise nulls; both far above 0.003 |
| bootstrap 95th percentile | 2.81 | 2.78 | match |
| quoted 95% upper limit (largest of shuffle-Neyman and bootstrap) | 3.00 (shuffle-Neyman 3.00; two-sided [-0.65, +3.42]) | 2.78 (shuffle-Neyman 2.00) | DEFINITION (my Neyman grid, 200 trials, own null shape) + beta_hat; quoted limits agree to 8% |
| KM1 eps_min | 8.9e-7 | 9.6e-7 | NUMERICAL; KM1's window (beta 0.11-0.27) not reached in either |
| H0 = 73 beta | +0.402 (boot 0.705, p 0.267) | +0.818 (0.703, p 0.068) | shift from primary -0.09 vs -0.07 (NUMERICAL); levels follow beta_hat |
| z frozen | +0.409 (0.469) | +0.726 (0.478) | follows beta_hat |
| TRGB + Cepheid + SNIa | +0.355 (0.735) | +0.796 (0.611) | follows beta_hat |
| UMa only | +20.0 (pinned upper bound) | -5.0 (pinned lower bound) | DEFINITION (bounds): degenerate in both, no information |
| W2 | -0.249 (boot 0.000) | -0.449 (0.132) | both collapse at the pole; shuffle p 0.41 / 0.50 |
| LG-apex / antapex | +2.495 (p 0.025) / -0.371 (p 0.71) | +2.513 (p 0.020) / -0.036 (p 0.96) | apex agrees; antapex NUMERICAL |
| Galactic north / south | +0.412 / -0.416 | +0.719 / -0.998 | follows beta_hat / pole |
| no tau softening | +1.545 (1.228) | +1.522 (1.100) | match |
| no Birge scaling | +0.158 (1.112) | +0.865 (0.828) | follows beta_hat (tau re-estimated 0.382 vs 0.379) |
| free sky dipole | beta +0.130 (0.503), D 0.54 toward (224, -47) | +0.312 (0.613), D 0.41 toward (250, -50) | NUMERICAL; both: beta falls toward 0, dipole toward the southern sky |
| distance term | beta +0.407, gamma -0.104 | +0.921, gamma +0.019 | NUMERICAL (gamma is 0.1 dex/dex either way: nothing) |
| jackknife range | [+0.354, +1.358] | [+0.682, +1.288] | CFG186 lists NGC2403 as its largest mover (+0.40); consistent with the finding |
| MUTATE beta = 0.30 point-level | beta_hat +0.494 -> +0.912 (shift +0.417); curve-level expectation +0.394; gamma (real factor held) +0.327 | +0.887 -> +1.429 (+0.542); curve-level +0.567; gamma +0.335 | NUMERICAL: both pipelines recover the injection multiplicatively |
| README "1.8-sigma level" hint | beta/sigma_boot 0.70; sqrt(Delta F) = 1.17 | 1.33 and 1.68 from its own numbers | README typo/FRAMING (its own numbers give 1.3-1.7 sigma, not 1.8) |
| SECONDARY per-galaxy table | not reproduced (not in my frozen plan) | +0.30 +- 0.29 | not tested |

### Why beta_hat differs: the inclination box on NGC2403 (a modelling choice; corrected wording)
Facts from `CFG193_f_nodecheck.py` (`CFG193_f_nodecheck.out`), read from CFG186's stored `chi` grid and from my own files:
1. **The cell is a node.** (t = -4, log a0 = -9.04) is TGRID[0], XGRID[113] (both grids identical to mine). CFG186's value 771.31 is `cfg186_a_curves.npz['chi'][33, 0, 113]` (float32 771.3100), read directly; mine is `CFG193_curves.npz['C'][33, 0, 113] + t^2 = 751.8985`. No spline, no interpolation, no CFG186 code run.
2. **The stored curves agree with mine almost everywhere, and differ where CFG186's bounds bind.** Over 213,722 cells within Delta chi2 <= 25 of each galaxy's minimum, median difference 0.0000 and 95th percentile 0.0006. For NGC2403 the differing cells near its minimum are 21 (t index 0..17, x index 102..113, log a0 -9.26..-9.04); over the whole grid 2,461 of 3,828 feasible cells have CFG186's chi2 above mine by more than 0.1 (mine is never above), all in regions far from the minimum apart from those 21, because the unbounded solution needs an inclination beyond 8 sigma from the catalogue.
3. **My solution at the node** (60-start scipy least squares): log10 Upsilon_disk -0.099 (u_d = +2.02 in 0.1-dex units; catalogue-centre -0.301); Upsilon_bulge at the prior centre (-0.155; NGC2403 has no bulge); inclination **38.21 degrees = -8.26 sigma_Inc** (catalogue 63.0 +- 3.0); t = -4.00 fixed by the node (D' = 2.520 Mpc, prior t^2 = 16); a0 fixed by the node. No other nuisance exists. **This solution lies outside CFG186's box** (inclination [39.0, 87.0] degrees).
4. **Bounds and priors, mine next to CFG186's.**
   | | mine | CFG186 |
   |---|---|---|
   | Upsilon_disk, Upsilon_bulge | log10 Upsilon in [-1.6, 0.8] (u = -13.0..+11.0 disk, -14.5..+9.5 bulge in 0.1-dex units) | u in [-10, +10], i.e. log10 Upsilon0 +- 1.0 |
   | inclination | [5, 89] degrees, no sigma-based bound | Inc +- 8 sigma_Inc, capped to [5, 90] |
   | priors | Upsilon: ((log10 Upsilon - log10 Upsilon0)/0.1)^2 (0.5, 0.7); inclination ((i' - i)/e_Inc)^2; distance t^2 | identical form |
   | data, weights | published e_V, chi2 unscaled inside the profile | same |
   | model | signed V_disk\|V_disk\|; g_bar floor 1e-16 m/s^2; kpc 3.0856776e19 m | V_disk^2; S >= 1e-6 (km/s)^2; 3.0857e19 m (all three immaterial here: no negative V_disk, V_bulge, or fiducial V^2 <= 0 points among these four) |
   The only relevant difference is the box. The frozen question says "inclination Gaussian (e_Inc)" and does not mention a box, so neither implementation departs from it.
5. **Inside CFG186's box my fitter reproduces its stored value** (NGC2403 node: 771.306 by scipy bounded least squares, 771.319 by my batch profiler, 771.310 stored). The same holds for the other three galaxies:
   | galaxy, cell (t idx, x idx) | stored | mine, my bounds | mine, CFG186's box | my inclination (sigma_Inc) / u_d | inside CFG186's box? |
   |---|---|---|---|---|---|
   | NGC2403 (0, 113) | 771.310 | 751.898 | 771.306 | 38.21 deg (-8.26) / +2.0 | no (inclination) |
   | F571-8 (28, 115) | 354.660 | 339.845 | 354.660 | 84.03 deg (-0.19) / -12.1 | no (Upsilon_disk u < -10) |
   | UGC05764 (22, 16) | 187.896 | 177.108 | 187.897 | 83.72 deg (+2.37) / +10.3 | no (Upsilon_disk u > +10) |
   | UGC00731 (23, 1) | 132.330 | 131.338 | 132.331 | 65.21 deg (+2.74) / +10.4 | no (Upsilon_disk u > +10) |
   So for F571-8, UGC05764 and UGC00731 the box is on Upsilon_disk (|u| > 10), for NGC2403 on the inclination. A full-grid recomputation with CFG186-style bounds matches its stored grid to max |d| 0.026 (F571-8) and 0.035 (UGC05764) over all cells; UGC00731 matches at the cells above but shows a residual offset of about 0.15 in 364 cells (max 0.16), and NGC2403's recomputation with my batch clipped-LM has max |d| 8.7 over 2,181 cells away from the node (an implementation limit of my clipping of bounds, not investigated; the node itself agrees). I did not run CFG186's own `cell_cold`.
6. **The swap tests used CFG186's stored grid nodes** (33 t x 116 x) for the replaced curve, spline-interpolated in t onto the 0.05 fine grid by my own `Curves` class (the same as every fit), with cubic interpolation in x. Restricting the fit to the 33 grid-node t values only (no spline between nodes) changes the numbers by 0.01 to 0.03: CFG186 curves +0.869 -> +0.894; CFG186 curves with my (unbounded) NGC2403 +0.476 -> +0.494; my curves +0.494 -> +0.519; my curves with CFG186's NGC2403 +0.931 -> +0.936. So the difference is not a spline artefact.
7. **Consequence.** beta_hat = +0.89 +- 0.67 (CFG186, box at 8 sigma_Inc) and +0.49 +- 0.70 (mine, no box) are both valid implementations of the frozen text; the estimator is sensitive to the box because the profile is very flat (Delta F 0.4 between beta = +0.49 and +0.89) and NGC2403 sits at the distance floor. CFG186's README statement "do not cite +0.89 as a hint for KM1" stands, and the hint is fragile to an undeclared bound. Its Fisher row, verdict, limit and KM1 translation do not move.

## Pass lines (frozen section 4): verdicts
| line | verdict | numbers |
|---|---|---|
| R1 sample | **REPRODUCES** | 149 / 68 exact; 37/3/26/2 exact (U1). Source counts differ (definition, above); not load-bearing |
| R2 velocities | **REPRODUCES** | 0 of 68 differ by more than 20 km/s (max 8.5, median 1.5); sigma_u medians 15.6 (window 16 +- 2) and 168.7 (169 +- 17) |
| R3 Fisher row | **REPRODUCES** | 0.447 in [0.405, 0.495]; beta_det 2.56 > 0.10; smallest uncertainty figure 0.447 >= 0.25 |
| R4 fit | **PARTIAL** | bootstrap sigma 0.702 in [0.60, 0.74] pass; no SIGNAL (p 0.22 > 0.003) pass; beta_hat +0.494 outside +0.887 +- 0.15 FAIL; shuffle p 0.22 outside [0.04, 0.13] FAIL. Both failures follow from CFG186's inclination box on NGC2403 (a modelling choice; corrected wording) |
| R5 verdict | **REPRODUCES** | NON-DIAGNOSTIC, no G7 verdict, no SIGNAL |
| R6 lever arm | **REPRODUCES** | rms z = 0.236 in [0.22, 0.33] |
| R7 own controls | pass, with two kept first-run failures | C0/M0 fitter exactness 0.3000 (first version FAILED: 0.2906; piecewise-linear interpolation; changed to cubic before the main run; failure kept in `CFG193_c_M0_firstfail_smoke.out`); C1 three starts agree to 0.0012 (first version FAILED: worst 0.68 in UGC08699, a Hubble-flow galaxy, 45 LM iterations too few; raised to 100 before the main run; failure kept in `CFG193_b_curves_firstrun.*`); C2 zero non-finite; C3 spline 0.0715; C4 0.0052 |
| Disagreement rules (frozen section 8) | D-c TRIGGERED (beta_hat; cause CFG186); D-f TRIGGERED by its literal wording (below); D-a, D-b, D-d, D-e, D-g not triggered | |

## MUTATE outcomes (exit 1 = bites)
| control | result | outcome |
|---|---|---|
| MU1 inject beta = 0.30 at point level | beta_hat +0.494 -> +0.912 (+0.417); expected from the noiseless curve-level injection +0.394 (window +-0.10); gamma with the real factor held fixed +0.327 (window 0.25-0.40) | **BITES** (rc 1) |
| MU2 shuffle w, inject beta = 1.0 in the true pairing | median recovered -0.195 over 200 shuffles; unshuffled +1.759 | **BITES** (rc 1) |
| MU3 drop profiling | median sigma_i 0.170 -> 0.041 (drop 76%); tau 0.340 -> 0.351; Fisher 0.447 -> 0.420; beta_hat +0.680 | **BITES** (rc 1) |
| MU4 u -> u + 600 | rms(dz) 0.236 -> 0.806; predicted sigma ratio 0.292; measured Fisher ratio 0.302 (3.4% apart); bootstrap ratio 0.274; shuffle ratio 0.267 | **BITES** (rc 1). The Fisher ratio is close to a tautology (same formula); the independent ratios (bootstrap 0.274, shuffle 0.267) agree with the prediction to 6-9% |
| MU5 exponential-RAR kernel | beta_hat +0.495 vs +0.494 (0.00 sigma_boot) | did **not** bite (rc 3) = kernel-robust |
| MU6 constant u | Fisher sigma_beta infinite; beta_hat pinned at +20 | **BITES** (rc 1) |

## Attacks
**(a) Velocity construction and the +-0.45.**
- *Variants.* H0 = 73 moves u by a median -53 km/s (max 126; the +5.3 D km/s ladder bias is the same effect) and the Fisher sigma_beta by -10.1%; H0 = 70 by -3.9%; luminosity D +0.3% (u within 8.5 km/s); linear cz +0.1% (2 km/s); Planck v_sun 0.0% (0.3 km/s). So the velocity construction changes the +-0.45 by no more than 10%: robust (rule: < 15%).
- *Errors in variables.* With sigma_u = H0 e_D alone, z = u^2 is biased up by +0.034 (median z is 0.116) and beta_hat is attenuated by lambda = 0.75 (0.71 with 50 km/s and 0.56 with 100 km/s extra scatter per galaxy). The true-beta uncertainty is therefore about 0.447 / 0.75 = 0.60, not 0.45. The Ursa Major block has sigma_u = 169 km/s against median |u| 124 km/s: its z bias 0.079 exceeds its median z 0.043, so it is dominated by noise. (The Fisher value computed from the noisy z falls, 0.40 to 0.35: that is spurious lever arm, not information.)
- *The common motion.* r(u, V_LG.n) = 0.751; R^2 of z on the LG-aligned pattern (V_LG.n)^2 is 0.58 (weighted 0.55); with that template as a free nuisance sigma_beta rises to 0.668 (x1.50). More than half of the lever arm is the LG-aligned sky pattern, as the README says. Within 8 Mpc (31 of 68 galaxies) u tracks V_LG.n at r = 0.956, rms 91 km/s; W2 has rms z 0.168, Fisher 0.596 (beta_det from Fisher alone 1.19).
- *Source disagreements.* Dropping UGC01281 changes nothing (beta_hat +0.494).
**(b) Nuisances or lever arm?** Fisher sigma_beta: frozen 0.447; sigma_i -> 0 with tau fixed 0.402 (x0.90); tau -> 0 0.129 (x0.29); z spread doubled 0.223 (x0.50); no profiling with tau re-estimated 0.420 (x0.94; tau 0.351 is not smaller). Releasing one nuisance at a time: distance only, median sigma_i 0.101; Upsilon only 0.092; inclination only 0.080; none 0.041. So sigma_beta is set by the per-galaxy scatter tau (0.34 dex) and the lever arm in z, not by the profiled nuisances (perfect nuisance knowledge buys at most 10%). tau itself may contain unmodelled nuisance error; this lane cannot separate that. Weighting sensitivity: beta_hat is fragile to it (no tau +1.55; no Birge +0.16; neither +1.10; the pre-Addendum-2 weighting that scales the distance prior +1.94 (bootstrap 1.63, shuffle half-width 1.78) against +0.49), i.e. it moves by more than one bootstrap sigma; the pre-Addendum-2 weighting is what made the mocks run away in CFG186.
**(c) Power by injection.**
- *Noiseless real curves (C1).* The recovered beta_hat rises by +0.066, +0.132, +0.394, +1.265 for beta_inj 0.05, 0.10, 0.30, 1.0, not by the injected amounts: with beta_obs = 0.49 the composition is multiplicative, (1 + beta_obs z)(1 + beta_inj z). My own expectation E14 ("recovered within 5%") was wrong for the same reason CFG186's M1 window was, and D-f (recovery within 90-110%) is triggered by its literal wording (131% and 126%). The composition test in MU1 does pass. The exactness check on synthetic curves is 0.3000.
- *Speed-shuffle injection (C2, 300 shuffles, seed 193301).* Median recovered / detection rate at 2 sigma_0 (sigma_0 = 0.481): beta_inj 0: -0.05 / 0.10; 0.05: -0.02 / 0.12; 0.10: +0.02 / 0.14; 0.30: +0.20 / 0.23; 1.0: +0.97 / 0.50. Nothing below 0.3 is distinguishable from 0; even 1.0 is detected half the time.
- *Point-level generative mocks (C3, 40 per beta, seed 193302).* Median recovered: 0 -> +0.14 (mean +0.71); 0.05 -> +0.61; 0.10 -> +0.81; 0.30 -> +0.78; 1.0 -> +1.92; sigma at beta = 0 is 1.28; bias positive (the concave log10(1 + beta z) and the asymmetric curves), as CFG186's Addendum 3-4 says. E15 (median bias > +0.3 at beta = 0) is wrong for the median (+0.14) and right for the mean (+0.71). Caveat: my mocks are less scattered than the data (mock tau 0.27 vs 0.34, median sigma_i 0.155 vs 0.170), so their bias and width are lower bounds; the coarse-grid pipeline reproduces the real-data beta within 0.11.
- *Neyman (C5, 9,200 fits).* shuffle-Neyman one-sided 95% upper limit 3.00, two-sided [-0.65, +3.42]; bootstrap 95th percentile 2.81; quoted 3.00.
**(d) What would be diagnostic.** sigma_beta = ln10 s / (sqrt(N) rms z) reproduces my Fisher (0.450 vs 0.447). For sigma_beta = 0.05 (2 sigma = the G7 line) N rms(z)^2 >= (ln10 s / 0.05)^2:
  | s (dex) \ rms z | 0.27 (SPARC-like) | 0.5 | 1.0 | 1.39 | 2.0 |
  |---|---|---|---|---|---|
  | 0.43 | 5379 | 1569 | 392 | 203 | 98 |
  | 0.30 | 2618 | 763 | 191 | 99 | 48 |
  | 0.20 | 1164 | 339 | 85 | 44 | 21 |
  | 0.10 | 291 | 85 | 21 | 11 | 5 |
  At N = 68 and SPARC's lever arm sigma_beta is 0.51, 0.24 and 0.12 for s = 0.43, 0.20 and 0.10: it never reaches 0.05. A diagnostic sample therefore needs about 390 galaxies with independent distances (5%) and speeds spanning 0-1000 km/s (rms z about 1), or about 85 if the per-galaxy a0 scatter could be cut to 0.2 dex, or SPARC-like galaxies numbering several thousand. Repo tables: UNGC has 350 redshift-independent distances within 40 Mpc (TRGB, SBF, Cepheid, SN, RR, BS, HB; rms z 0.473, 2.0x SPARC's) but no rotation curves; its Tully-Fisher rows (rms z 1.45) are circular for a0; KT2017, 2MRS and ALFALFA carry flow-model distances; none supplies redshift-independent distances beyond about 40 Mpc. Nearby galaxies share the Local Volume's motion, so the lever arm cannot be large inside 40 Mpc; only 3D flow reconstructions give w.
**(e) First run vs second run vs final (CFG186, from its saved files).**
| quantity | first | second | final |
|---|---|---|---|
| N primary, z sd | 68, 0.2351 | 68, 0.2351 | 68, 0.2351 |
| tau, L0 | 0.3534, -10.0754 | 0.3534, -10.0754 | 0.3445, -10.0799 |
| median sigma_i | 0.1726 | 0.1726 | 0.1681 |
| Fisher sigma_beta | 0.4699 | 0.4699 | 0.4528 |
| beta = 0 mocks: sigma / mean | 5.403 / 5.596 | 5.175 / 5.212 | 2.249 / 2.373 |
| beta_det (2 sigma) | 10.81 | 10.35 | 4.50 |
| spline check | FAIL 0.687 | pass 0.040 | pass 0.040 |
- Confirmed: the first-run mocks ran away (Addendum 1: +5.6, 5.4); the Fisher change 0.470 -> 0.453 is exactly the change in sigma_i and tau caused by Addendum 2's weighting (sample and z identical); the spline check failure and its redefinition.
- Not checkable: Addendum 2's "median beta_hat about 4" for the second run: only the mean (+5.21) and sigma (5.17) were saved.
- Part B: first run vs final have identical beta_hat (+0.8866), bootstrap sigma (0.6656), shuffle p (0.0785) and noise p (0.5614): only calibration outputs were added, and the verdict is unchanged. Note: the "final" part-A outputs are timestamped after the part-B first run and part B's numbers are identical to all digits, so the part-A curves are deterministic. The verdict-relevant numbers do not depend on which run is used; the first-run beta = 0 mocks (mean 5.6) are calibration of an estimator that was later shown biased, not evidence about the data.
- The reruns all reproduce the same stored curves; the NGC2403 box was never an error (see above).

## The 153 vs 149 sample-count question
My frozen count of 153 was the master-table count with Q <= 2 and Inc >= 30 and **no** usable-point cut (83 Hubble-flow, 39 TRGB, 3 Cepheid, 26 UMa, 2 SNIa). CFG186's 149 includes its third cut, >= 5 usable points. Four galaxies each have only 4 usable points: D512-2 (HF), UGC00634 (HF), NGC6789 (TRGB), UGC07232 (TRGB). Removing them gives 81/37/3/26/2 = 149 and 68 primary, as CFG186 has. The usable-point definition was fixed before any count (U1: finite R, V, eV with R, V, eV > 0); the alternative U2 gives the same 149. Nothing was tuned; 153 was simply the count before a cut I had counted separately.

## Where independence stops (unchanged from the frozen text, plus what the runs added)
Shared: the SPARC rotmod and master-table files, the VizieR position table, UNGC/KT2017/2MRS tables, the NED cz column of `sparc_cosmicweb_match.csv`, nu_mono via `CFG4_common` (my own P2 and exponential-RAR kernels are the cross-check: MU5 shows no dependence), the memory-sourced v_sun and V_LG, and the frozen design (priors, Birge/tau weighting of Addendum 2, W1, w_ref = 600, the model log10 a0 = L + log10(1 + beta z)). So agreement tests implementation and numbers, not the design. Where I am independent and it mattered: the fitting stage (my fitter reproduces CFG186's beta_hat on its curves) and the curves (my batch profiler reproduces its stored grid wherever its box does not bind, and inside its box everywhere I tested); the decisive difference is the box, a modelling choice not stated in the frozen text.

## Failed controls and wrong expectations, kept
- M0 first version FAILED (0.2906): interpolation; changed to cubic before the main run.
- C1 first version FAILED (0.68): iterations; raised before the main run. MUTATE=1's C3/C4 checks first failed because they compared against un-injected data (a bug in the check; fixed, first output kept as `CFG193_b_curves_MUTATE1_firstrun.out`).
- **My first reading of the NGC2403 difference ("CFG186 numerical error / stuck in a local minimum", and the same for F571-8, UGC05764, UGC00731) was WRONG.** My 40-start check ran with my own wider bounds; my solution lay outside CFG186's box (inclination -8.26 sigma vs the +-8 sigma limit; Upsilon_disk beyond +-10 for the other three). The wording in `CFG193_compare.out` ("trapped") and in the phase-2 report is superseded by `CFG193_f_nodecheck.out` and this README.
- E6 (beta_hat within +-0.15 of 0.89), E8 (shuffle p in [0.04, 0.13]), E12 (median sigma_i in [0.20, 0.32]: mine 0.170; the 0.26 came from CFG182's unscaled widths), E14 (recovery within 5%: composition), E15 (median bias > +0.3), E16 at beta_inj 0.30 (detection 0.23, not < 0.20) were wrong. E1-E5, E7, E9-E11, E13, E17-E20 held (E5 at P 0.35, E11 at 0.65).
- The E14 check in `CFG193_c_fit_power.py` ends in `or True` (a vacuous pass, marked "reported"); the numbers it prints are the evidence, and I left the code as run.
- The pre-declared C3 noise wording "s_i e_V" was resolved as sqrt(s_i) e_V (Birge s_i is a variance ratio) before the run.
- Runtime: the frozen target of < 15 min per run was measured on a machine loaded by other jobs (load about 130 on 16 cores); the main c script took 2,295 s wall, the mock stage 1,338 s. I could not verify the 15-minute figure on an idle machine.

## Scripts and outputs (all `CFG193_*`, in this directory)
- `CFG193_common.py` (shared machinery), `CFG193_a_velocities.py`, `CFG193_b_curves.py`, `CFG193_c_fit_power.py`, `CFG193_d_design.py`, `CFG193_e_profile.py`, `CFG193_f_nodecheck.py` (reads CFG186's .npz; answers the owner's cell-level questions), `CFG193_compare.py` (phase 2, reads CFG186's files).
- Outputs: `*.out`, `*_results.json`, `CFG193_utable.csv/.npz`, `CFG193_curves*.npz`, `CFG193_c_nulls*.npz`, `CFG193_c_c2.npz`, `CFG193_c_c3.npz`, `CFG193_c_neyman.npz`; MUTATE runs `*_MUTATE<k>.*`; the U2 point-mask variant `*_U2.*`; first-run failures kept as `CFG193_b_curves_firstrun.*`, `CFG193_b_curves_MUTATE1_firstrun.out`, `CFG193_c_M0_firstfail_smoke.out`.
- The `CFG193_SMOKE=1` switch in the c script is a debugging shortcut and its outputs are never used.

## Exact re-run (from the repository root; `<repo>` = the repository root; each script under 15 min on an idle 14-core machine, unverified)
```
export ZF_REPO=<repo>; cd campaign_fresh_gravity/CFG193_*/
python3 CFG193_a_velocities.py
python3 CFG193_b_curves.py
for k in 1 3 5; do MUTATE=$k python3 CFG193_b_curves.py; done
python3 CFG193_c_fit_power.py
for k in 1 2 3 4 5 6; do MUTATE=$k python3 CFG193_c_fit_power.py; done     # exit 1 = bites; MU5 exits 3 when kernel-robust
python3 CFG193_d_design.py
python3 CFG193_e_profile.py
for s in b_curves c_fit_power e_profile; do CFG193_VARIANT=U2 python3 CFG193_$s.py; done
python3 CFG193_compare.py                                                    # phase 2: reads CFG186's .npz / .json
python3 CFG193_f_nodecheck.py                                               # reads CFG186's .npz
```
Exit codes: main scripts 0 (own check failure 2); MUTATE runs 1 (bites), 3 (did not bite), 2 (own check failed).

## In-place re-run (orchestrator)

`bash run_all.sh` (and afterwards `python3 CFG193_f_nodecheck.py`) was re-run in this directory with `ZF_REPO` set (`run_all.out`; about 90 minutes on a loaded machine): every main run exits 0; the c-script MUTATE 1-4 and 6 exit 1 (bite); MUTATE 5 exits 3 (kernel-robust, does not bite); the U2 variants, the compare script (opened after all of the above) and the node check exit 0. Every `_results.json` is identical to the referee's; every `.out` differs only in timing lines and, in `CFG193_d_design.out`, in the printed order of a method-count dictionary. The `_curves*.npz` profile arrays (14 MB, regenerated by the b script) are not committed. The frozen criteria are `../CFG193_FROZEN_CRITERIA.md` (f4470979d). The wording about NGC2403 in this README is the referee's corrected wording (the difference is CFG186's undeclared inclination box, not an optimiser error); `CFG193_compare.out` carries the superseded 'numerical error' wording as the compare script printed it.
