# DP2: DR4 sample-size / sigma_fit forecast and mock-triple injection. FROZEN CRITERIA

Written 2026-11-05, before any DP2 code or output exists. Committed alone. Never edited after commit; changes go in a new dated file.

**Status: INFORMATION ONLY, no verdict weight.** Owner decision `prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-05b_DR4_D7_D8.md`
D8: sigma_sys(b) stays as frozen; a mock-triple injection is information only and can never change sigma_sys, a band, or a verdict.
Nothing here edits a frozen file: not PREREGISTRATION_DR4.md or its amendments, not the D2 note or A1-A3, not the two 11-05 owner
decisions, not CFG740/CFG825/CFG943, not `wide_binary_pipeline.py` (sha256 7c884e0e...), not `catalog_builder/build_catalog.py`
(sha256 46452daf...). Frozen code is imported read-only (`python3 -B`); no output is written outside this folder. No network
(socket guard), no downloads. kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.

Compute limits: OMP_NUM_THREADS=1, nice -n 10, own RSS guard at 4 GB, total wall time a few tens of minutes. If repeats must be cut, the
README says so.

## Part 1. Forecast of the DR4 frozen-cut N, sigma_fit, the D2 edges and N_R

### 1.1 Inputs (all on disk)
- DR3 extract caches `real_research/data/widebinaries/dr3_extract/`: stage_A.npz (sources), stage_F.npz (cleaned pairs + R_chance),
  AV_sfd98.npz, stage_G_corr.npz and stage_G_corr_elbadry.npz (parallax-PM correlations).
- Reference catalogue `wide_binaries_dr3.csv`, sha256 6fff64d964ebaa72..., N = 6,210.
- Frozen DR4 error scaling (PREREGISTRATION_DR4.md section 1.4, `wide_binary_pipeline.py` line 203): sigma_pm x (66/34)^-1.5 = 0.372,
  sigma_plx x (66/34)^-0.5 = 0.718. This is the only DR4 precision scaling used. It is the record's own APPROX scaling, not a published DR4 table.

### 1.2 Method
The registered stage G of `build_catalog.py` is re-run from its own functions (`frozen_cuts`, `third_star_flags`, `vt_error_mc`, frozen
seed SEED) on the DR3 cached stage F pairs, in the same order as its `main()`. The correlation dictionary is the union of the two caches
on disk; any star not covered gets correlation 0 (counted and reported; never fetched).

Precision-dependent cuts (found by reading `frozen_cuts`): cut 4 parallax S/N >= 40 (errors), cut 5 parallax consistency
|d1-d2| < min(4 sd, 8 pc) (errors and the noise in d1-d2), cut 13 triple search (dpar, sdmu), cut 15 Banik eq. 10 sigma(vtilde) (the
3x3 Gaia covariance in the Monte Carlo). Cut 14 R_chance also uses errors (KDE features), but recomputing it needs the 30 shifted
realisations and the full KDE: **R_chance decisions are held at their DR3 values (assumption A-R)**. Stages C/D (pair search, cleaning)
are held at DR3 membership (assumption A-C: their tests are noise-normalised, so a true pair's pass probability is invariant under a
proportional error shrink).

Scenarios:
- **S0 (known answer)**: DR3 errors, the registered stage G. Must give N = 6,210 and the same pair set as the reference CSV.
- **S0b (identity of the emulation path)**: the S2 code path with factors (1, 1). Must give exactly the S0 pair set.
- **S1 errors-only**: parallax_error x 0.718, pmra/pmdec_error x 0.372 for every source; observed values unchanged. Biased LOW for cut 5
  (DR3 noise in d1-d2 is judged against DR4 errors) and stated as the low precision bound.
- **S2 noise-shrunk (central precision emulation)**: as S1, and for each stage-F pair the two component parallaxes are pulled to their
  inverse-variance mean by 0.718 (p_i' = p_w + 0.718 (p_i - p_w)), because a true pair shares one parallax and DR4 noise is 0.718x DR3.
  Proper-motion values are not changed (true orbital motion and noise cannot be separated); stated.
- **MC jitter**: S2 is also run with two more vt_error_mc seeds (SEED+1, SEED+2) and the spread of N is reported (Amendment 18's flip noise).
- **MUTATE (must bite)**: S2 with factors inverted (sigma_pm x 1/0.372, sigma_plx x 1/0.718, i.e. a worse-than-DR3 release). Bites if
  N_mutate <= 0.95 x 6,210. If it does not bite, Part 1 is NOT DIAGNOSTIC.

Non-precision screens (assumptions, labelled A-NSS, A-RV, A-RUWE; no record scaling exists): DR4's NSS tables, RVs and RUWE may remove
more pairs than DR3's. The N range applies, on top of the precision forecast N_prec(S2):
- **high**: no extra loss (screens as DR3);
- **central**: extra NSS loss = the fraction of a mock catalogue removed by the Part 2 physical NSS detection model at hidden-triple
  fraction f_t = 0.10, plus extra RV loss 1.7 % (DR3's own RV-screen loss, assumed doubled by DR4's larger RV set);
- **low**: N_prec(S1) instead of S2, extra NSS loss at f_t = 0.20, extra RV loss 3.4 %, extra RUWE loss 5 %.
No fainter-source gain is credited: the frozen cuts keep G < 17 both and s >= 2 kAU at d < 250 pc (theta >= 8 arcsec), where DR3 is
already complete (derivable; stated). The DR4 base-table choice (curated gaia_source vs all_source, Amendment 15 draft) is not modelled.

### 1.3 Derived quantities (arithmetic, for each of low / central / high N and for N = 30,000 and 6,210 as references)
- sigma_fit, three models: registered 0.019 sqrt(30000/N); DR3-calibrated 0.055 sqrt(6210/N) (D2 note section 5); and the Part 2 mock
  Newtonian-sky value measured at the central N (max(mean profile sigma, rms across repeats), the pipeline's own rule).
- sigma = sqrt(sigma_fit^2 + sigma_sys^2) for sigma_sys 0.020 and 0.0375 (owner 11-05 table 2c).
- Edges (owner 11-05 section 2c): law-first excluded iff gamma_hat <= anchor - 3 sigma, anchor 1.1614 canonical / 1.1917 alt (Arm A);
  screened excluded iff gamma_hat >= 1 + 3 sigma; the UNDECIDED band between (or the overlap, D5 BOTH EXCLUDED).
- **Is a Newtonian sky decisive?** For each row: P(gamma_hat <= law-first edge) with gamma_hat ~ Normal(mu_N, rms_N) from the Part 2
  f_t = 0 mocks at that N (mu_N, rms_N interpolated as rms ~ 1/sqrt(N) from the central-N and 30k runs), and also with the f_t = 0.10
  NSS-on mean shift added. "DECISIVE (>= 0.95)", "LIKELY (0.5-0.95)", else "UNDECIDED-likely". Also flagged: the sigma_sys(b) gate
  (< 0.048 canonical / < 0.058 alt) passes for 0.020 and 0.0375 both; stated.
- N_R = 0.0698 x N (CFG943 A0: 2,095 of 30,000); sigma_R = max(hypot(0.019 sqrt(30000/N_R), 0.020), sigma_boot), sigma_boot not modelled
  (the formula part only); kill needs R >= 1 + max(0.01, 3 sigma_R).

### 1.4 Checks (Part 1)
- K1: S0 gives N = 6,210 and the identical (source_id1, source_id2) set to the reference CSV. FAIL = no forecast is reported as valid.
- K2: S0b equals S0 exactly.
- K3: S0 cut flow equals `build_report_dr3.json` at every step.
- K4: MUTATE bites (N <= 5,900).
- K5: frozen files hashed before and after; unchanged.

## Part 2. Mock-triple injection (information only)

### 2.1 Generator, estimator, model
- Sky: `campaign_fresh_gravity/CFG943_dr4_readiness/cfg943_common.py` `mock_population` (the exact replica of the frozen
  `make_population`, DR4 noise), with `velocities` for vtilde, oversampled and randomly cut to N_cat as `make_catalogue` does; the
  CFG943 A0 class (Newton, no catalogue cuts). Imported read-only.
- Estimator: frozen `W.bin_medians(boot=200)` + `W.fit_gamma` on the frozen grid; model medians = CFG943's
  `cfg943_model_medians.npz` (frozen 3,000,000-pair master, DR4 noise; sha256 497992db...), read-only. Both footings.
- The generator has **no triple and no NSS model**. DP2 adds one (assumption A-T, stated as such), applied to a fraction f_t of the
  catalogue pairs (pairs that survive every other screen, i.e. f_t is the hidden-triple fraction of the NSS-off catalogue):
  - host: primary or secondary with probability 1/2; inner companion mass m = q M_host, q ~ U(0.1, 1);
  - inner period: log10 P[d] ~ Normal(5.03, 2.28) (Raghavan+2010), redrawn until P >= 1 d and a_in <= r_3D/3 (stability);
    circular inner orbit, isotropic orientation, uniform phase;
  - light ratio eps = q^4; photocentre fraction beta = q/(1+q) - eps/(1+eps);
  - proper-motion kick: photocentre velocity beta v_rel projected on the sky, times the baseline average
    |sin(pi T/P)/(pi T/P)|, T = 5.5 yr (66 months), added to the host star's PM (sign into the relative PM by host);
  - mass: the outer orbit's true velocity is scaled by sqrt((M_t + m)/M_t); the photometric mass M_obs is unchanged (companion light ignored).
- NSS detection models (assumption A-D), applied to triples only, no false positives:
  - **Dphys**: astrometric signal S = alpha for P <= T, S = alpha (1 - cos(pi T/P)) for P > T, alpha = beta a_in parallax [mas];
    detected iff S >= 0.10 mas (DR4 at G < 17) ;
  - **Dphys-DR3 analog**: T = 2.83 yr (34 months) for both the kick average and the signal, threshold 0.30 mas (a separate sky, same seeds);
  - **flat p = 0.5** and **flat p = 0.9**.
- NSS-off catalogue = the full mock; NSS-on = the same mock minus detected triples (paired, so the shift has little sample noise).

### 2.2 Runs
- f_t in {0, 0.05, 0.10, 0.20, 0.30}; N_cat = Part 1 central N rounded to the nearest 100, and N_cat = 30,000.
- K = 30 repeats per (f_t, N_cat) (CFG943 used K = 100; cut for compute; stated). Seeds `default_rng([2026, 1105, n_cat, f_index, k])`.
- Reported per f_t: mean gamma_hat (NSS-off, and NSS-on per detection model), rms, mean shift Delta = gamma_off - gamma_on, the fraction of
  pairs removed by each detection model, and the shift's contamination share. In a Newtonian mock every bit of gamma_off - 1 is
  contamination plus pipeline bias, so **contamination removed = gamma_off - gamma_on**, and **contamination left = gamma_on - gamma_on(f_t=0)**.
- The f_t that reproduces DR3's two record numbers is read off the curves (interpolation, Dphys-DR3 analog): (i) the NSS-off probe
  +0.075 canonical / +0.058 alt, (ii) the 1.205 (looser Banik-like dry run, El-Badry catalogue) minus 1.075 (reference build) = +0.13.
  Both are stated as rough analogs (DR3 data were fitted with the DR4-noise model; the DR3 probe is a rebuilt catalogue, see 2.3).

### 2.3 DR3 decomposition of the NSS-off probe (data, NON-SCORING)
The D2 NSS-off probe (+0.075 canonical) compares the reference catalogue (6,210) with the CFG825 variant catalogue cut at s < 30 kAU
(6,302; `CFG816_dr4_r_statistic_scoring/wide_binaries_dr3_variant.csv`). The variant differs by NSS-flagged pairs AND by the reseeded
vtilde-error Monte Carlo (~2.2 % of pairs out, ~2.2 % in; CATALOGUE_VARIANT_2026-10-18.md). DP2 fits, with the same estimator and 30
bootstrap seeds each (mean and sd reported):
- A reference (6,210); B variant s < 30 kAU; C = B minus pairs with a DR3 non_single_star flag on either component (stage_A);
  D = A plus the NSS-flagged pairs of B.
- contamination part of the probe = gamma(B) - gamma(C) and gamma(D) - gamma(A); reseed part = gamma(C) - gamma(A).
- Known answers: A within 0.03 of 1.0750 canonical, B within 0.03 of 1.1500 canonical (D2 S1 tolerance, estimator jitter ~0.02).
(Lane DP1 reproduces the probe; DP2 only decomposes it.)

### 2.4 Checks (Part 2)
- T1 known answer: f_t = 0, N_cat = 30,000: mean gamma_hat canonical within max(3 x 0.0168/sqrt(K), 0.005) of CFG943 A0's 1.0037.
- T2 null: f_t = 0.10 with the kick and the mass term both zeroed gives gamma_hat identical to f_t = 0 at the same seeds (k = 0..4).
- T3 null: detection probability 0 gives Delta = 0 exactly.
- T4 MUTATE (must bite): f_t = 0 sky with the frozen boost shape at gamma_inf = 1.10 (W.gamma_of_y, canonical y_extN) applied to the true
  velocity: mean gamma_hat must rise by >= 0.05 over f_t = 0 (K = 10). If not, Part 2 is NOT DIAGNOSTIC.
- T5 monotone: mean gamma_off rises with f_t (information; a failure is reported, not repaired).
- T6 frozen files unchanged.

## Reporting
README.md, result first: N range (low/central/high) with assumptions, sigma_fit by model, the edge table, "Newtonian sky decisive or
UNDECIDED", N_R and the R kill line, the triple table, the DR3 decomposition, every check PASS/FAIL, caveats. Outputs `.out` / `.json`
in this folder. No verdict word on gravity is used anywhere.
