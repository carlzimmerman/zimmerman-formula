# DP2: DR4 sample-size / sigma_fit forecast and mock-triple injection (INFORMATION ONLY)

**Status: information only, no verdict weight** (owner decision `OWNER_DECISION_2026-11-05b_DR4_D7_D8.md` D8: sigma_sys(b)
stays frozen; a triple injection can never change sigma_sys, a band or a verdict). Criteria frozen first (`FROZEN_CRITERIA.md`,
commit c9d368f7e4). Mock numbers are MOCKS; DR3 numbers are NON-SCORING. kappa = 1/2 FITTED; footings never pooled; not theory closed.
Nothing here says the data favour the framework.

## Result first

1. **DR4 N under the frozen cuts: about 8,000 pairs (range 7,000-8,600), not 30,000.** Re-running the registered stage G on
   the DR3 caches with the frozen DR4 error scaling (sigma_pm x 0.372, sigma_plx x 0.718) gives **8,618** (noise-shrunk, central
   precision emulation; 8,608-8,627 over three Monte Carlo seeds) and 8,528 (errors-only). The gain over DR3's 6,210 is almost all in
   cut 15 (Banik eq. 10 sigma(vtilde)): its pass rate rises from 0.678 to 0.932. Cuts 4 and 5 change little (the plx S/N gain is
   offset by cut 5 in the errors-only case). After assumed extra DR4 screen losses (NSS from the Part 2 detection model, RV, RUWE):
   **low 7,025 / central 8,039 / high 8,618.** The 30,000 of the error model has no support in the frozen cuts: G < 17, d < 250 pc and
   s >= 2 kAU fix the parent sample, and DR3 is already complete there.
2. **sigma_fit at the central N:** registered 0.019 sqrt(30000/N) = **0.037**; DR3-calibrated 0.055 sqrt(6210/N) = **0.048**; the
   Newton mock at 8,600 gives rms **0.028**, profile 0.027. (DR3's own noise gave 0.055 at 6,210; DR4 should sit between the mock
   and the DR3-calibrated value.)
3. **Where the D2 edges land, central N, canonical (anchor 1.1614):**

   | sigma_fit model | sigma_sys | sigma | law-first excluded if gamma_hat <= | screened excluded if gamma_hat >= | Newton sky P(decisive) |
   |---|---|---|---|---|---|
   | registered 0.0367 | 0.020 | 0.042 | 1.036 | 1.125 | 0.80 |
   | registered 0.0367 | 0.0375 | 0.053 | **1.004** | 1.157 | **0.40** |
   | DR3-cal 0.0483 | 0.020 | 0.052 | 1.005 | 1.157 | 0.40 |
   | DR3-cal 0.0483 | 0.0375 | 0.061 | **0.978** | 1.184 | **0.12** |
   | mock 0.0287 | 0.020 | 0.035 | 1.056 | 1.105 | 0.94 |
   | mock 0.0287 | 0.0375 | 0.047 | 1.020 | 1.142 | 0.61 |

   Alt (anchor 1.1917) edges sit 0.030 higher: law-first edge 1.034 (registered, 0.0375), 1.008 (DR3-cal, 0.0375); P(decisive) 0.80 / 0.47.
   "P(decisive)" = probability that a Newtonian mock sky (mock mean 1.0115, rms 0.0287 at the central N; the pipeline's own small
   positive Newton bias included) lands at or below the law-first edge. With f_t = 0.10 hidden triples left after the NSS screen the
   probabilities drop by 0.15-0.2 (table in `dp2_summary.out`).
   **Reading: at the forecast N, a Newtonian DR4 sky is decisive against the bare law only if sigma_sys(b) comes out near 0.020;
   at DR3's measured sigma_sys(b) = 0.0375 it reads UNDECIDED more often than not on the canonical footing.** The sigma_sys(b)
   gate (< 0.048 / < 0.058) itself passes at both values. The screened-excluded edge is 1.10-1.18, so a boost sky at Arm A's floor
   (1.16) would be marginal.
4. **R statistic:** N_R ~ 0.0698 N ~ **560** (490-600); sigma_R (formula part) **0.14**; **KILL needs R >= 1.42** (1.41-1.45),
   not 1.22 as at 30,000.
5. **Triples (mock, Newton sky, model of DP2's own):** hidden triples raise gamma_hat slowly: +0.004 / +0.015 / +0.025 / +0.037
   at f_t = 0.05 / 0.10 / 0.20 / 0.30 (N 8,600, NSS-off; +0.006 / +0.012 / +0.028 / +0.042 at N 30,000), because the estimator works on bin medians and anchors kappa on
   high-acceleration bins. **A physical NSS screen (66-month astrometric orbit/acceleration detection) removes about half of the
   triples but moves gamma_hat by only -0.009 to +0.001; its NSS-off shift is ~0 or negative**: it removes mostly compact,
   short-period companions, which sit preferentially at small separation (the kappa anchor bins) and do little to the deep-bin
   medians, while the wide, long-period companions that do inflate vtilde escape detection. Random (flat) detection gives the
   naive positive shift (p = 0.9: +0.014 / +0.020 / +0.037 at f_t = 0.10 / 0.20 / 0.30). **No f_t <= 0.30 in this model reproduces
   DR3's NSS-off probe (+0.075)** and none reproduces 1.205 - 1.075 = +0.13.
6. **DR3's +0.075 NSS-off probe is mostly not contamination removal** (DR3 data, same estimator, 30 bootstrap seeds per set):
   probe B - A = +0.069 canonical = **+0.013 from the 100 NSS-flagged pairs** + **+0.055 from the reseeded stage-G Monte Carlo**
   (142 pairs out, 134 in; the vtilde-error cut's random stream shifts when the pair array changes). Adding the 100 NSS pairs
   to the reference catalogue moves it by +0.012. Alt: +0.038 = +0.017 NSS + +0.022 reseed. The record's stage-G seed spread
   (Q-G50) is SD 0.025 canonical, with the 51-build mean at 1.109 against the reference build's 1.075; so the reference build
   is itself a low draw and the probe's size is mostly seed noise. As frozen (D8 (a)), sigma_sys(b) on DR4 will include this
   seed noise; DR4's cut 15 passes 93 % instead of 68 %, so fewer pairs sit near its threshold (an expectation, not measured here).

## Checks

| id | check | result |
|---|---|---|
| K1 | S0 (DR3 errors, registered stage G) gives N = 6,210 and the identical pair set to the reference CSV (sha 6fff64d9...) | PASS |
| K2 | the noise-shrink code path with factors 1 equals S0 | PASS |
| K3 | S0 cut flow equals build_report_dr3.json at every step | PASS |
| K4 | MUTATE (factors inverted, worse than DR3) must drop N <= 5,900 | BITES (N = 2,322) |
| K5 | frozen files unchanged | PASS |
| T1 | f_t = 0, N 30,000: mean gamma_hat canonical 1.0053 vs CFG943 A0 1.0037 (tol 0.0092) | PASS |
| T2 | kick and mass term zeroed = f_t 0, identical | PASS |
| T3 | detection probability 0 gives shift 0 exactly | PASS |
| T4 | MUTATE: gamma_inf 1.10 boost on the Newton sky must raise gamma_hat >= 0.05 | BITES (+0.098 / +0.100) |
| T5 | gamma_off rises with f_t (canonical) | yes at both N |
| T6 | frozen files unchanged | PASS |
| 2.3 | DR3 reference refit 1.0844 vs 1.0750 (tol 0.03); variant 1.1529 vs 1.1500 (tol 0.03) | PASS / PASS |

## Triple-injection table (K = 30, the frozen run; canonical; N_cat 8,600 / 30,000)

| f_t | gamma_off (NSS-off) | Dphys removed | gamma_on Dphys | shift off-on Dphys | shift p 0.5 | shift p 0.9 | DR3-analog shift |
|---|---|---|---|---|---|---|---|
| 0 | 1.0112 / 1.0053 | 0 | = | 0 | 0 | 0 | 0 |
| 0.05 | 1.0153 / 1.0117 | 0.026 | 1.0151 / 1.0122 | +0.000 / -0.001 | +0.002 / +0.003 | +0.003 / +0.006 | -0.003 / -0.003 |
| 0.10 | 1.0265 / 1.0172 | 0.051 | 1.0259 / 1.0202 | +0.001 / -0.003 | +0.010 / +0.005 | +0.014 / +0.011 | -0.004 / -0.006 |
| 0.20 | 1.0358 / 1.0332 | 0.102 | 1.0431 / 1.0369 | -0.007 / -0.004 | +0.010 / +0.015 | +0.020 / +0.025 | -0.014 / -0.012 |
| 0.30 | 1.0483 / 1.0473 | 0.154 | 1.0575 / 1.0568 | -0.009 / -0.010 | +0.021 / +0.021 | +0.037 / +0.036 | -0.021 / -0.018 |

Paired shift rms per repeat 0.004-0.029, so K = 30 means carry ~0.001-0.005 errors. Alt footing in `dp2_triples.out`.
"Contamination removed" = gamma_off - gamma_on (the sky is Newtonian); "contamination left" = gamma_on - gamma(f_t 0): at
f_t 0.10 and N 8,600 that is +0.015 after the Dphys screen.

### K = 300 extension (declared after the freeze; same code; `dp2_triples_K300.*`; canonical, N 8,600 / 30,000)

| f_t | gamma_off - gamma(0) | shift Dphys | shift p 0.5 | shift p 0.9 | DR3-analog shift |
|---|---|---|---|---|---|
| 0.05 | +0.007 / +0.006 | -0.002 / -0.001 | +0.003 / +0.003 | +0.005 / +0.005 | -0.004 / -0.003 |
| 0.10 | +0.013 / +0.010 | -0.003 / -0.004 | +0.006 / +0.005 | +0.011 / +0.010 | -0.006 / -0.007 |
| 0.20 | +0.022 / +0.025 | -0.008 / -0.006 | +0.012 / +0.013 | +0.021 / +0.023 | -0.013 / -0.013 |
| 0.30 | +0.042 / +0.044 | -0.009 / -0.007 | +0.022 / +0.022 | +0.038 / +0.039 | -0.020 / -0.018 |

Newton mean at f_t 0: 1.0065 (rms 0.031) at 8,600 and 1.0051 (rms 0.016) at 30,000; the K = 30 run's 1.0112 at 8,600 was a
high draw, so the K = 30-based P(decisive) values in the table above are slightly conservative. With K = 300 the physical-screen
shift is negative at every f_t > 0 (errors ~0.001), confirming item 5: in this model the NSS-off minus NSS-on shift is never positive.

## Method and assumptions (full text in FROZEN_CRITERIA.md)

- Part 1 re-runs the registered stage G (`build_catalog.frozen_cuts`, `third_star_flags`, `vt_error_mc`, frozen seed) imported
  read-only, on cached DR3 stage F. Precision-dependent cuts: 4 (plx S/N), 5 (plx consistency), 13 (triple search), 15 (sigma(vtilde)).
  Assumptions: A-R (R_chance decisions held at DR3; recomputing needs the full KDE), A-C (stages C/D membership held; their tests are
  noise-normalised), A-NSS/A-RV/A-RUWE (extra DR4 screen losses: none / NSS at f_t 0.10 + RV 1.7 % / S1 + NSS at f_t 0.20 + RV 3.4 %
  + RUWE 5 %). Proper-motion values are not de-noised. Uncovered correlation stars set to 0: 4 in S0 (as in the record's builds),
  168 in S2. No fainter-source gain (G < 17, theta >= 8 arcsec, DR3 complete). The DR4 base-table choice (Amendment 15 draft) and the
  real DR4 error table are not modelled; the 0.372 / 0.718 scaling is the record's APPROX scaling.
- Part 2: CFG943's replica generator (class A0) and frozen model medians; triple model A-T (Raghavan log-normal periods, stability
  a_in <= r_3D/3, q ~ U(0.1, 1), L ~ M^4 photocentre, circular inner orbit, baseline-averaged photocentre velocity added to the PM,
  outer orbit sped up by sqrt((M_t+m)/M_t), photometric mass unchanged); detection model A-D (Dphys: signal >= 0.10 mas, T = 66
  months; DR3 analog 0.30 mas, 34 months; flat p 0.5 / 0.9). The DR3 analog uses the DR4 noise model throughout (rough).
- **Declared deviations from the frozen text:** (i) the sky seed is `default_rng([2026, 1105, n_cat, 0, k])` for every f_t (one
  shared sky per repeat, so f_t comparisons are paired); the triple draws use `[2026, 1105, n_cat, f_index, k]` as frozen.
  (ii) N_cat "central" = 8,600 = the S2 precision forecast rounded, because the assumption-based screen losses need Part 2's own
  output; the central N after losses (8,039) enters the summary through rms ~ N^alpha interpolation. (iii) An extra K = 300 run
  (`dp2_triples_K300.*`) was added after the freeze, more repeats only, same code.

## Caveats

- The forecast N rests on the record's approximate DR4 error scaling and on DR3's parent sample; a published DR4 error table, a
  different base table, or DR4 RUWE/NSS behaviour can move it by more than the low-high range.
- The mock sigma_fit is lower than the registered model at N ~ 8,000 (0.028 vs 0.037); real DR3 data gave 0.055 at 6,210.
  Which applies to DR4 is unknown; the table gives all three.
- The triple model is one model; the record's `wb_threshold_audit` needs f_triple ~ 0.19-0.20 to absorb the DR3 deep-bin excess
  with a different contamination model. DP2's model makes triples much gentler on the median estimator.
- Lane DP1 reproduces the DR3 NSS-off probe; DP2 only decomposes it.

## Files

`dp2_forecast.py` (+ `.out`, `_results.json`, `_MUTATE.*`), `dp2_triples.py` (+ `.out`, `_results.json`, `_MUTATE.*`, `_K300.*`),
`dp2_dr3_nssoff.py` (+ `.out`, `_results.json`), `dp2_summary.py` (+ `.out`, `_results.json`), run logs `run_*.log`.
Run: `OMP_NUM_THREADS=1 nice -n 10 python3 -B <script>`; dp2_triples.py takes `--ncat 8600,30000 --K 30`.
