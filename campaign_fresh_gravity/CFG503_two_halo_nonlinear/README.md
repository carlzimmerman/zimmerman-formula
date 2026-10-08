# CFG503: a nonlinear two-halo term, stripping of leaked satellites, and the SHMR uncertainty for the KiDS isolated-lens stack. MODEL STILL INADEQUATE (gates G1 and G3 fail); the clash verdict is NOT DECIDED

Criteria: `FROZEN_CRITERIA.md`, committed alone before any script (f56e146a1). It continues CFG502 (cacadd50d / 4dac09899). CFG502's code is copied, not edited. On-disk data only; no downloads. nice 15, at most 4 threads.
- kappa = 1/2 is FITTED. The footings 9.3603e-11 and 1.1312e-10 are scored separately and never pooled. a0 flat.
- "Cold energy" = the cold clumping component. Its mass is still required, and no particle species is added.
- Nothing here says the data favour the framework. Not "theory closed".

## Bottom line
1. **Three standard upgrades, all fixed in advance.**
   - Two-halo term: b zeta(r) xi_NL outside r_ta (CAMB halofit, Takahashi+12; Tinker+05 radial bias).
   - Stripping: leaked satellites' own halos are cut at the circular-orbit Jacobi radius. The same r_t is applied to every model's own profile.
   - SHMR: Moster+13 is primary. The Behroozi+13 difference is carried as a rank-one covariance term.
   - Nothing was fitted to lensing.
2. **The upgrades move LCDM closer but do not pass.**
   - **G1, stack P (181,477 lenses):** chi2 45.92 → **34.34 / 15 (p = 0.0031)**. FAIL; the gate is p > 0.01, i.e. chi2 < 30.58.
   - **G2, f30 null (57,265):** 34.11 → **21.52 (p = 0.12)**. PASS.
   - **G3, ALL null (605,531):** 172.2 → **73.99 (p = 8.6e-10)**. FAIL; the gate is p > 0.001.
   - By the frozen rule the result is **MODEL STILL INADEQUATE**. No per-model verdict and no clash verdict is drawn. The table below is for information only.
3. **What is still missing, located without tuning (`cfg503_posthoc.*`).**
   - The primary misfit sits in two bins: 1.38 Mpc (+4.9 sigma) and 1.04 Mpc (+3.5 sigma). Those are R / r_ta = 1.2 and 0.9 for the pair-weighted median lens (r_ta 1.14 Mpc, 16-84% range 0.83-1.58).
   - Without those two bins, LCDM gives chi2 17.6 / 13 (p 0.17). That is post-hoc and not a validation.
   - The nonlinear term **raises** E beyond about 1.6 Mpc (0.47 → 0.60 at 1.82 Mpc) but **lowers** it at 1.0-1.4 Mpc (0.47 → 0.40 at 1.38 Mpc).
   - The reason is the sharp boundary at r_ta. Every model's own profile stops there, and E's two-halo term starts there. Extra mass just outside a sharp edge projects to a *negative* Delta Sigma just inside it.
   - The ALL null shows the same +6.4 sigma pull at 1.23 Mpc. It also keeps an inner overshoot of -2 to -3.3 sigma at R < 0.15 Mpc and at 0.4 Mpc, which is the one-halo normalisation of the full sample.
   - **The missing physics is a continuous one-halo-to-two-halo (splashback / infall) transition in place of the sharp r_ta truncation plus sharp exclusion.** A Diemer & Kravtsov-type profile, a smooth exclusion window, or a simulation-calibrated halo-matter profile through 0.5-3 r200 would supply it.
   - This boundary is the record's own lens-model convention: every model is truncated at r_ta. So it is not a choice that can be repaired inside E alone.
   - Per the instruction, nothing was tuned after the gate failed, and the lane stops here.

## The frozen re-score (stack P, 15 bins, Hartlap 0.6735; SHMR propagated; the same E and the same stripping rule for every model). REPORTED ONLY: the gate failed

| model | canonical chi2 / 15 (p) | alt chi2 / 15 (p) | inner 9 / outer 6 (can) | CFG502 can / alt |
|---|---|---|---|---|
| (i) LCDM NFW (footing-free) | **34.34** (3.1e-3) | 34.34 (3.1e-3) | 7.6 / 27.8 | 45.92 / 45.92 |
| (ii) law to r_ta | 81.38 (3.9e-11) | 59.51 (3.1e-7) | 60.7 / 21.2 | 53.92 / 38.29 |
| (iii) 5.85 r_M edge (growth rule) | **416.69** | **417.68** | 240.9 / 162.4 | 429.12 / 431.47 |
| (iv) CFG487 V1 clock taper | 85.05 (8.2e-12) | 57.74 (6.2e-7) | 60.1 / 33.0 | 57.22 / 34.33 |
| (v) CFG495 drawdown F_dd | 24.68 (0.054) | 25.01 (0.050) | 5.2 / 27.6 | 23.28 / 23.50 |
| F_nodd (reported) | 26.81 | 29.44 | 9.6 / 20.6 | 51.42 / 60.82 |
| law to 0.5 r_ta (reported) | 87.29 | 59.93 | 60.2 / 40.0 | 63.75 / 41.68 |

- Data-only chi2 (no SHMR term), Moster / Behroozi: LCDM 35.25 / 34.44; F_dd 33.41 / 46.46 (can); edge 424.6 / 430.7 (can). All rows are in `cfg503_score.out`.
- **Clash (edge vs lensing): NOT DECIDED by the frozen rule.** For information, the edge sits +392.0 / +392.7 above the best model (F_dd) on the two footings. That is the CONFIRMED pattern again, but on a template whose LCDM validation fails. Do not quote it as confirmed.
- **Stripping lowers the law-type models' scores.** The law to r_ta goes 53.9 → 81.4 (can) and V1 goes 57.2 → 85.1. Their satellites lose the phantom mass beyond r_t, which they needed at 0.1-0.4 Mpc. LCDM's inner chi2 goes the other way, 22.3 → 7.6.
- **F_dd's low chi2 is the halo-mass degeneracy CFG495/CFG502 named.** It is not a drawdown detection.

## Nulls (frozen gates)
- **N1, f30 (E at W = 30):** LCDM 21.52 (p 0.12), passes G2. Data-only: Moster 29.62, Behroozi 21.29. Pulls -2.6 sigma at 2.17 Mpc and at 0.25 Mpc. F_dd 14.2 / 14.1; law to r_ta 63.9 / 51.1; V1 58.2 / 43.0; edge 234.7 / 240.2.
- **N2, ALL (no isolation, f = f_par):** LCDM 73.99 / 15, fails G3. Inner 27.3, outer 41.7. Data-only: Moster 119.9, Behroozi 93.8.
  - The SHMR term absorbs a large share here, because the Behroozi-Moster difference is large compared with ALL's small errors. Without it the ALL fit is much worse.
  - Pulls: +6.4 sigma at 1.23 Mpc, +2.7 at 0.93; -2.1 to -3.3 at 0.04-0.13 Mpc and at 0.40 Mpc.

## MUTATE (`cfg503_score_MUTATE.*`)
- **M0 PASS (load-bearing).** Halofit off with CFG502's colossus EH xi_lin, zeta = 1, stripping off, Moster only, data covariance only. It reproduces CFG502 exactly: all 14 stack-P chi2 (max difference 0.0000), N1 34.113 and N2 172.189.
- **MH, halofit off only** (CAMB linear xi, zeta = 1; stripping and SHMR on). G1 42.79 (fail), G2 15.86 (pass), G3 72.35 (fail).
  - So, from linear to nonlinear-with-zeta, G1 improves 42.8 → 34.3 but G3 barely moves.
  - b xi_NL without zeta (reported) is worse: G1 42.6, G2 38.7, G3 185.6.
- **MS, stripping off only** (halofit, zeta and SHMR on). G1 **31.26** (p 0.008), G2 24.01, G3 70.39.
  - Stripping helps the inner bins (inner-9 9.45 → 7.60) but costs more in the outer bins (23.0 → 27.8). So G1 is closer to the gate *without* stripping, 31.26 against 34.34. Both fail.
  - The frozen "stripping visible" check passes: the largest inner-bin shift is 0.96 sigma (> 0.5). The inner-9 |d| is 1.85, below the alternative criterion of 2.

## Controls
- **Pass:**
  - C1: stack P data = CFG377, exact.
  - C2a: the unstripped Moster LCDM and F_dd per-group tables equal CFG495's, exact.
  - C0e: the copied CFG502 path rebuilds CFG502's E tables, exact.
  - C3n: T2h with xi_NL by the shell projector equals the Hankel form, 2e-4.
  - C7: the stripping code with r_t beyond r_ta returns the unstripped vector, exact.
- **Reported:**
  - C3l: CAMB linear xi vs colossus EH, 1.1% at 1-20 Mpc/h.
  - C8: for log M* 10.5 at z 0.25, the median leaked satellite has r_t = 0.061 Mpc (0.31 r200c). It keeps 22% of its NFW mass inside 0.5 Mpc.
  - Behroozi+13 and Moster+13 agree to within 0.07 dex in log M* at log M200c 11.5-13 (z 0.1, 0.3). So the SHMR swing is small for stack P, and large only against ALL's errors.
- **Disclosed fix:** the first MUTATE run crashed because the M0 path asked for a Behroozi EH table that is not built (EH exists for Moster only, by design). M0 now uses Moster only, as the criteria state. The main run was re-executed after the fix with identical numbers.
- The numpy matmul RuntimeWarnings are the known Accelerate quirk; every table is finite.

## Limits
- Labels: "nonlinear 2h NOT CROSS-CHECKED BY PM". CFG502's 256^3 PM cannot resolve the transition, and it was not re-run.
- CFG502's companion-count check (0.85) stands for the Moster HOD.
- Not modelled, the same for every model:
  - lens photo-z in R and Sigma_crit;
  - miscentring;
  - source-lens association / boost;
  - the satellites' own E (hole and T2h keep CFG502's form after stripping).
- **Needs owner go (unchanged from CFG502):** the KiDS-bright x GAMA overlap, the MICE KiDS-bright mock, and a 512^3 halo catalogue with substructure. The last is what would calibrate the 0.5-3 r200 transition this lane now identifies.
- **Until a template passes its LCDM gate, no KiDS isolated-lens verdict beyond the inner ~0.1 Mpc should be read as decisive.** That covers verdicts from CFG352, 413, 486, 487, 495, 498, 501, 502 and this lane.

## Run
```
nice -n 15 python3 -u cfg503_env.py            # ~2 min; CAMB xi tables, E tables (2 SHMR x 4 xi modes x W10/W30/ALL), r_t weights
nice -n 15 python3 -u cfg503_own.py            # ~3 min, 4 processes; own profiles full + stripped, both SHMR, both footings
nice -n 15 python3 -u cfg503_score.py          # frozen re-score, gates, verdict
CFG503_MUTATE=1 nice -n 15 python3 -u cfg503_score.py
nice -n 15 python3 cfg503_posthoc.py           # POST-HOC diagnostics (not a verdict)
```
Needs CFG502's staged `cfg502_stage.npz` and `cfg502_env_table.npz` in `../../../_external_data/cfg502_work/`. Large arrays (`cfg503_env_table.npz`, `cfg503_own_tables.npz`) live in `../../../_external_data/cfg503_work/` and are not committed.
