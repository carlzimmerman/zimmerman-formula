# CFG529 FROZEN CRITERIA: an f30-matched environment term (CFG503 construction and CFG504 smooth-transition construction, with the MEASURED f30 leaked-satellite fraction), validated first, then the equal-terms re-score of the census edge and the record's model set on the strictly isolated f30 KiDS lenses

Written 2026-10-09, before any CFG529 script exists and before any CFG529 chi2 has been computed. Committed alone. Nothing below
changes after a result is seen; departures go in the README, dated; this file is never edited.

kappa = 1/2 is FITTED. Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt) are scored separately and never pooled; a0 flat. Kernel
nu_mono (cfg100_lib). Census edge r_edge = r_M / ln(1 + f_ret f_b / (1 - f_b)), r_M = sqrt(G M_b / a0), f_ret = fret_census (CFG515 lib,
read-only). "Cold energy" = the cold clumping component; its MASS is still required (no particle species). On-disk data only, no
downloads; nice -n 10, <= 4 worker processes / threads (a simulation lane is running). Not "theory closed"; nothing here says the data
favour the framework. No knob is fitted to anything.

## 0. Why
CFG525 (7f99a4371 / b4a697ee6): on the strictly isolated f30 lenses (cfg96_isoflags `f30`, W = 30 Mpc photo-z window, 57,265 lenses, a
subset of stack P) the census edge passes the free-R^-0.8 two-halo harness on both footings (-0.24 / +1.00) and fails f_ret = 1 (+53 / +62).
But in the FIXED CFG503 environment built at the stack-P window (W = 10) with the measured stack-P leakage 0.2234 (CFG520 part B scaling;
"H3") the census edge fails both footings (direct rows +19.44 / +20.53 vs the best sharp edge in the same harness). No f30-matched version of
that fixed environment, with a measured f30 leakage, has been built. This lane builds it and judges the edge in it.

## 1. Inputs (all read-only, committed or on disk)
- Data: stack P (181,477) and f30 (mask `f30` of `cfg96_isoflags.npz`) ESD from `cfg110_perlens.npz`, 50-patch jackknife
  (`lr_esd_jackknife.npz`), Hartlap; ALL (605,531) from `_external_data/cfg502_work/cfg502_stage.npz`. Same code as CFG503/504.
- Environment pieces: `_external_data/cfg503_work/cfg503_env_table.npz` (construction A) and `_external_data/cfg504_work/cfg504_env_table.npz`
  (construction B), each with its W10 / W30 / ALL HOD leaked fraction grid f, b_c, b_h, T_host (B), hole and two-halo shapes.
- Own-profile tables: `cfg503_own_tables.npz` (A, sharp) and `cfg504_own_tables.npz` (B, `prim` window, x_t = 0.910 from CFG504's
  calib JSON) for LCDM, F_NODD, PROP (F_dd = F_NODD + PROP), LAW_RTA, LAW_X05, EDGE (5.85 r_M growth edge), V1; full and stripped with the
  W10 / W30 / ALL tidal weights; both SHMR (Moster+13 primary, Behroozi+13 rank-one).
- Census-edge and sharp-edge-node tables: stack-P W10 sharp from `_external_data/cfg525_work/cfg525_tables.npz` (CFG525); NEW W30 tables
  built here (section 3).
- **Measured leaked-satellite fractions, from CFG519's committed JSON (`cfg519_satfrac_results.json`, "main"):**
  - stack P (W10, ISO): f_obs = 0.22342746446430256 (sigma_tot 0.0044) - as CFG520 / CFG525.
  - **f30 (W30): f30_obs = 0.16863265651220682, sigma_stat 0.0060348** (CFG519's 12-region jackknife). sigma_tot for f30 is DECLARED here
    as sqrt(0.0060348^2 + 0.0028483^2) = 0.00667, adding CFG519's stack-P sigma_sys (IterCen vs BCG + reweighting) in quadrature, since
    CFG519 gives no f30-specific sigma_sys. CFG519 has an f30-specific value with an error, so no recomputation is needed.
  - ALL parent: f_par_obs = 0.3133864614828175.

## 2. The environment, two constructions, measured leakage
For window K in {W10 (stack P), W30 (f30), ALL} and SHMR s in {moster, behroozi}:
- **Scaling rule (CFG520 part B, unchanged):** f'_K = clip(s_K f_K, 0, 1), s_K = f_meas,K / X_K, X_K = the HOD grid's pair-weighted value over
  that sample's lenses with the OUTERMOST-bin weights WW[:, 0] (CFG506 / CFG520 convention; group-interpolated grid). Separate X_K per SHMR.
  At W10 this reproduces CFG520's s_M = 1.2374 / s_B = 1.2358. The shape in (log M*, z) is kept.
- **Construction A (CFG503, sharp boundary; = CFG525's H3 recipe):** E_A = HOLE + b_c,K S2H_nlz + f'_K XF_K, where the leaked piece
  XF_K = (E_nlz_K - HOLE - b_c,K S2H_nlz) / f_K is recovered from the committed table (rebuild check, 1e-9). Own vector per group =
  (1 - f'_K) full + f'_K tr_K (stripping with window K's tidal weights).
- **Construction B (CFG504, smooth DK14 transition, primary x_t):** E_B = HS_prim + (1 - f'_K) b_c,K SS_prim + f'_K (T_host,K + b_h,K SS_prim)
  (CFG504's E_table with f replaced by f'); own = (1 - f'_K) prim-full + f'_K prim-tr_K.
- chi2 = r^T (C / h + delta delta^T)^-1 r, r = data - model(Moster), delta = model(Behroozi) - model(Moster) (CFG503 / 504 propagation),
  15 bins; inner-9 / outer-6 reported.

## 3. New tables (cfg529_tables.py; every f30 group = every CFG503 group holding >= 1 f30 lens)
Per group, per footing, using CFG503's `kids_Md` / `kids_fin` / `truncate` and CFG504's `kids_Md_ext` / `window` (copied code paths,
libraries imported read-only), with CFG503's W30 tidal weights (`{s}_W30` rt_weights):
- Profiles: (a) the census edge, direct, exactly as CFG525's direct rows (group M_gal, f_ret = fret_census(M_gal), edge = min(r_edge, r_ta));
  (b) CFG413's sharp edge at x r_ta for the CFG525 nodes with x >= 0.20: {0.20, 0.22, ..., 0.30, 0.33, 0.36, 0.40, 0.45, 0.50, 0.55, 0.60,
  0.70, 0.80, 0.90, 1.00} (best-x = min over these, CFG413's rule); (c) f_ret = 1 direct (MUTATE T1).
- Variants: A: full (sharp, = CFG525 node/direct "full"), tr_{s}_W30 and tr_{s}_W10 (sharp); B: prim-full_{s} and prim-tr_{s}_W30
  (the edge is model-intrinsic: phantom settled to the edge, frozen beyond it, continued flat to r_ext = max(8 x_t, 6) r_ta,LCDM exactly as
  CFG504 treats the 5.85 r_M edge, then windowed with f_t(r / r_ta,LCDM(s)), x_t = 0.910).

## 4. Statistics and verdicts
**4a. Environment validation, per construction (A, B).** LCDM (footing-free), SHMR-propagated chi2:
- **G1m** stack P, W10 environment with f_obs = 0.2234: p > 0.01 (chi2 < 30.58).
- **G2f** f30, W30 environment with f30_obs = 0.1686: p > 0.01.
- **G3m** ALL, ALL environment with f_par_obs = 0.3134: p > 0.001 (chi2 < 37.70). COMPUTED AND REPORTED, NOT required for f30 validity.
  Declared reason (before any number): f30 is a subset of stack P; G3 tests the one-halo normalisation / miscentring of NON-isolated lenses,
  which CFG504 located in the inner bins (R < 0.13 Mpc) and which no environment term touches. This is a DEPARTURE from CFG503/504's
  all-three rule, declared now. If G3m fails, every verdict of this lane carries the label "G3 (ALL) FAILS - environment validated for
  isolated samples only; CFG504's three-gate rule not met".
- **ENVIRONMENT VALID (construction K)** iff G1m and G2f both pass in K. **ENVIRONMENT VALID (lane)** iff at least one construction is valid;
  **ENVIRONMENT INVALID** otherwise. Reported only: G2f at f30_obs +- sigma_tot.

**4b. Census edge on f30, per valid construction and footing.** Delta_K = chi2_K(census) - min over nodes x >= 0.2 of chi2_K(sharp edge
at x r_ta), same construction, sample (f30), footing. **Edge PASS in K iff Delta_K <= 4 AND p_K(census) > 0.01** (CFG525's placement
statistic and CFG503's absolute per-model rule, both required); else FAIL. Lane verdict per footing: **PASS** iff PASS in every valid
construction; **FAIL** iff FAIL in every valid construction; **CONSTRUCTION-DEPENDENT** otherwise (not a pass).

**4c. Model re-score on f30 (only for a valid construction; otherwise information only, labelled, no verdict).** Models: (i) LCDM NFW,
(ii) law to r_ta, (iii) 5.85 r_M growth edge, (iv) CFG487 V1 clock taper, (v) CFG495 F_dd; plus the census edge; reported F_nodd and law to
0.5 r_ta. Per model and footing: PASS iff p > 0.01 on f30 (CFG503 rule). Reported: chi2 minus the best of (i)-(v) and of (i)-(v) + census.

## 5. Controls (load-bearing; the run exits 1 if any fails)
- K1 stack P data = CFG377 primary (1e-10).
- K2 construction A with the HOD f (unscaled) reproduces CFG503's committed 14 stack-P chi2, its f30 LCDM 21.524 and ALL LCDM 73.994 within 0.01.
- K3 construction A with the W10 scaling reproduces CFG520 part B's 14 scaled stack-P chi2 (LCDM 26.13) within 0.01, s_M / s_B within 1e-4.
- K4 construction A, stack P, CFG525 tables: the direct census Delta_H3 reproduces CFG525's +19.440 / +20.528 and the best-x H3 chi2
  (63.145 / 44.657 at x = 0.70) within 0.01. (This is the CFG525 fixed-environment FAIL, reproduced at the stack-P window.)
- K5 construction B with the HOD f reproduces CFG504's committed 14 stack-P chi2, G2 21.36 and G3 50.91 within 0.01.
- K6 new tables: the sharp full and tr_W10 census / node rows of this lane equal CFG525's for the same groups (1e-9 relative, 1e-3 floor);
  the windowing path applied to the 5.85 r_M EDGE reproduces CFG504's committed `EDGE|prim|full_{s}` and `tr_{s}_W30` for 20 test groups
  (1e-9 relative).
- K7 the scaled grids give stack-weighted f' = f_meas within 1e-9 (W10, W30, ALL; both SHMR).

## 6. MUTATE (`CFG529_MUTATE=1`, outputs `*_MUTATE.*`)
- **T1 (load-bearing, must FAIL):** f_ret = 1 in the f30-matched environment fails (Delta > 4) on both footings in every construction.
- **T2 (load-bearing, must FAIL):** the stack-P environment (W10, 0.2234) on stack-P data through this lane's code reproduces CFG525's
  fixed-environment census fail (= K4: Delta > 4 on both footings, matching +19.440 / +20.528 within 0.01).
- **T3 (load-bearing teeth):** the mismatched stack-P environment (W10 E, W10 stripping, 0.2234) applied to the f30 data must differ from the
  matched f30 environment by > 0.5 sigma_f30 in at least one bin of the LCDM model vector (construction A). Its census and LCDM rows are reported.
- **T4 (load-bearing teeth):** leakage set to 0 (f' = 0 in E and in the own mixing) on f30: the LCDM model vector must move by > 0.5 sigma_f30
  in at least one bin (both constructions). Whether G2f and the census edge then fail is REPORTED (expected direction not guaranteed).
A failed load-bearing MUTATE is a failed control.

## 7. Reported only (no verdict weight)
f30 leakage at f30_obs +- sigma_tot; the sum-of-bins weighting convention for X_K (CFG519's own weighting); E-only scaling (own mixing at the
HOD f); the census edge at stack P in construction B is NOT built (not needed for any gate). Post-hoc readings, if any, are labelled.

## 8. Outputs
`cfg529_tables.py` (-> `_external_data/cfg529_work/`), `cfg529_score.py`; `.out`, `_MUTATE.out`, results JSON, plain README. `git add` this
lane folder only, specific paths, never -A; commit locally; no push; never rewrite history.
