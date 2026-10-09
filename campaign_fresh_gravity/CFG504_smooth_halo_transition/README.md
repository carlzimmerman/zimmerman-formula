# CFG504: a continuous one-halo / infall / two-halo transition calibrated on our own PM boxes. G1 and G2 now pass; G3 (ALL) still fails, so MODEL STILL INADEQUATE and the clash verdict is NOT DECIDED

Criteria: `FROZEN_CRITERIA.md`, committed alone before any script, catalogue, fit or re-score (333a5fce4). The lane continues CFG502 (cacadd50d / 4dac09899) and CFG503 (f56e146a1 / b78648975). Their code is copied, not edited. Only local data and our own simulation snapshots were used; nothing was downloaded. Everything ran at nice 15 with at most 4 processes, and only one 512^3 particle load at a time (no other 512^3 job was running).
- kappa = 1/2 is FITTED. The footings 9.3603e-11 and 1.1312e-10 are scored separately and never pooled. a0 is flat.
- "Cold energy" means the cold clumping component. Its mass is still required, and no particle species is added.
- Nothing here says the data favour the framework. This is not "theory closed".

## Bottom line
1. **The calibration on our own boxes (`cfg504_pm.*`, `cfg504_calib.*`):**
   - **Inputs.** Two 512^3 S0 (LCDM-equivalent) z = 0 snapshots: 200 Mpc/h box, mesh cell 0.39 Mpc/h, m_p 5.2e9 Msun/h. Three 256^3 snapshots served only as a resolution check.
   - **Finder.** Spherical overdensity at Delta_ta (11.81 rho_bar) on particles, seeded by CIC density peaks, centred on the particles' centre of mass, and de-duplicated within r_ta. This gives about 19,000 halos with log M_ta >= 12.3 [Msun/h] per 512^3 box.
   - **Profiles.** Stacked xi_hm(r) from per-halo pair counts on 48 shells from 0.15 to 20 Mpc/h. These cover the one-halo, infall and two-halo regions together and are tabulated for every mass bin in `cfg504_calib_results.json`.
   - **Resolution limit.** A bin counts as resolved only if its median r_ta is at least 5 mesh cells. That means log M_ta >= 13.5 at 512^3, and only the top bin at 256^3.
   - **Extrapolation.** The KiDS lenses sit at log M_ta of about 12.5 (16-84%: 12.05-12.94). Their transition is therefore extrapolated by about 1 dex, assuming it is self-similar in r / r_ta.
   - **Fit.** The frozen form is the Diemer-Kravtsov transition f_t = [1 + (x/x_t)^4]^-2, x = r / r_ta, and Delta rho = [rho_own - rho_bar] f_t + rho_bar b zeta xi_NL (1 - f_t). Over the 8 resolved 512^3 fits, x_t = **0.910**, with sigma_tot = 0.196 (fit scatter; formal error 0.027). The two-halo nuisance A has a mean of 0.75 on the PM; it is not carried to KiDS.
   - **The form fits the PM badly.** The median step-2 chi2/dof is 40, so the frozen label **TRANSITION FORM POOR FIT ON PM** applies. Between 0.45 and 0.85 r_ta the PM halos carry more mass than the NFW-plus-window form allows; in R2 of run a, the measured profile is 16-62% above the best fit. That is an infall excess, or a mesh effect (mass pushed out of a softened core), or both.
   - **Mass trend.** x_t falls with mass: 1.20-1.27 at log M_ta 13.6, 0.71-0.89 at 14.6, and a slope of -0.30 per dex. The unresolved 512^3 bins prefer x_t of about 1.24-1.44.
   - **MUTATE SHUF passes.** With uniform-random particles around the real catalogue, the mean xi_hm over [0.5, 3] r_ta is 0.0000 +- 0.0003, against 1.02-1.05 in the real boxes, and A_shuf is 0.0000.
2. **The KiDS re-score with the primary transition (`cfg504_score.*`).** The window is applied to every model's own profile and to E alike, and nothing is fitted to lensing.
   - **G1, stack P (181,477 lenses):** LCDM chi2 34.34 → **18.53 / 15 (p = 0.24)**. PASS.
   - **G2, f30 (57,265):** 21.52 → **21.36 (p = 0.13)**. PASS.
   - **G3, ALL (605,531):** 73.99 → **50.91 / 15 (p = 8.6e-6)**. **FAIL**; the gate is p > 0.001.
   - By the frozen rule the result is **MODEL STILL INADEQUATE**. No per-model verdict and no clash verdict is drawn. The table below is for information only.
3. **What the smooth transition changed.**
   - With the sharp boundary, E dipped to 0.40 at 1.38 Mpc and 0.73 at 1.04 Mpc. With the smooth transition it is a flat 0.86-1.00 there.
   - The stack-P pulls at 1.38 / 1.04 Mpc go from +4.9 / +3.5 sigma to +3.1 / +2.8.
   - At 0.44-0.78 Mpc the total drops by 0.06-0.10 Msun/pc^2. Inside 0.25 Mpc it changes by less than 0.02.
4. **What is still missing, located without tuning.** This reads the committed outputs only; it is not a verdict.
   - **(a) Mass near r_ta.** The data still sit above LCDM at R ~ r_ta: +3.1 / +2.8 sigma on stack P, and +3.3 sigma at 1.23 Mpc on ALL. The PM halos themselves show more mass at 0.45-0.85 r_ta than the frozen DK14 form can carry. Point 1 says why that excess is not yet trustworthy at KiDS masses: the form fits the PM poorly, the excess may be partly a mesh effect, and KiDS masses are about 1 dex below the calibrated range.
   - **(b) The one-halo normalisation of the full sample.** On ALL, the inner bins sit -1.8 to -3.3 sigma below LCDM at R < 0.13 Mpc and -1.9 sigma at 0.40 Mpc (inner-9 chi2 26.8). The transition cannot touch this. It is unchanged in kind since CFG502 and points to the central halo masses (SHMR / flux scale) or miscentring of the non-isolated sample.
   - Per the instruction, nothing was tuned after the gate failed, and the lane stops here.

## The frozen re-score (stack P, 15 bins, Hartlap 0.6735; SHMR propagated; the same window, E and stripping rule for every model). REPORTED ONLY: G3 failed

| model | canonical chi2 / 15 (p) | alt chi2 / 15 (p) | inner 9 / outer 6 (can) | CFG503 can / alt |
|---|---|---|---|---|
| (i) LCDM NFW (footing-free) | **18.53** (0.24) | 18.53 (0.24) | 7.7 / 11.6 | 34.34 / 34.34 |
| (ii) law to r_ta | 78.08 (1.6e-10) | 53.04 (3.8e-6) | 60.9 / 15.7 | 81.38 / 59.51 |
| (iii) 5.85 r_M edge (growth rule) | **395.30** | **397.08** | 243.0 / 121.2 | 416.69 / 417.68 |
| (iv) CFG487 V1 clock taper | 80.70 (5.2e-11) | 53.83 (2.8e-6) | 60.5 / 21.1 | 85.05 / 57.74 |
| (v) CFG495 drawdown F_dd | 13.68 (0.55) | 14.18 (0.51) | 5.3 / 13.0 | 24.68 / 25.01 |
| F_nodd (reported) | 15.25 | 17.33 | 9.4 / 8.7 | 26.81 / 29.44 |
| law to 0.5 r_ta (reported) | 77.48 | 51.54 | 60.6 / 19.4 | 87.29 / 59.93 |

- **Clash (edge vs lensing): NOT DECIDED by the frozen rule**, because G3 failed.
  - For information: the edge sits +381.6 (canonical) and +382.9 (alt) above the best model (F_dd). That is the CONFIRMED pattern for the fourth lane running, but on a template that still fails one of its own LCDM gates. Do not quote it as confirmed.
- **F_dd's low chi2 is the halo-mass degeneracy CFG495/502/503 named.** The drawdown lowers the cold halo almost uniformly. It is not a drawdown detection.
- The law-type models (ii) and (iv) still fail by a wide margin in the inner 9 bins (39-61), as in CFG503. The transition does not reach those bins.

## Nulls (frozen gates)
- **N1, f30:** LCDM 21.36 (p 0.13), passes G2.
  - Data-only chi2: Moster 27.67, Behroozi 20.67.
  - Pulls: -3.0 / -2.2 sigma at 2.17 / 1.82 Mpc, where the f30 outer signal is low; -2.7 at 0.25 Mpc.
  - F_dd 17.3 / 17.5; law to r_ta 68.9 / 52.8; V1 67.5 / 50.6; edge 256.0 / 262.4.
- **N2, ALL:** LCDM 50.91 / 15, fails G3.
  - Inner-9 chi2 26.8, outer-6 14.2.
  - Data-only chi2: Moster 87.1, Behroozi 64.8.
  - Pulls: +3.3 sigma at 1.23 Mpc; -1.8 to -3.3 at 0.04-0.13 Mpc; -1.9 at 0.40 Mpc.

## Reported variants (`cfg504_score.out`; none changes the verdict). Values are G1 / G2 / G3 LCDM chi2
| variant | G1 | G2 | G3 | edge - best (can / alt) |
|---|---|---|---|---|
| primary (x_t 0.910) | 18.53 | 21.36 | 50.91 | +381.6 / +382.9 |
| lo (x_t 0.714) | 15.92 | 23.47 | 49.10 | +372.9 / +374.3 |
| hi (x_t 1.106) | 24.63 | 19.17 | 55.58 | +389.0 / +390.3 |
| ext (x_t linear in log M_ta, about 1.44 at KiDS masses) | **40.34** (fail) | 16.12 | 69.10 | +399.1 / +401.0 |
| A carried (two-halo x 0.746) | 22.20 | 17.12 | 51.08 | +382.5 / +384.2 |
| E-only smoothing (own profiles kept sharp) | 15.93 | 21.69 | 48.70 | +382.6 / +383.7 |
| framework own windowed in own r_ta,law units | 18.53 | 21.36 | 50.91 | +381.6 / +382.9 |

- G3 fails in every variant (48.7-69.1, against < 37.7).
- G1 is sensitive to how x_t is extrapolated. With the trend-extrapolated x_t (about 1.44, which is also what the unresolved 512^3 bins prefer), G1 fails again (40.3). So the G1 pass depends on the self-similarity assumption that was frozen as primary. Both readings are reported.
- The "own r_ta,law" variant gives the same LCDM / F_dd numbers by construction. Its law-model rows are 82.5 / 60.1 (ii) and 81.3 / 55.1 (iv).

## Controls and MUTATE
- **Pass:**
  - C1: stack P data = CFG377, exact.
  - C0: the copied CFG503 path rebuilds CFG503's E tables and HOD pieces, exact.
  - C10 (load-bearing): finder vs CFG502's peak code on the 256^3 seed360 run. 1501 of 2442 halos with log M_ta >= 13.3 match within one cell, with median |d log M_ta| 0.0095 dex. The unmatched ones are centres that moved more than a cell under CoM refinement, or that CFG502's cell-centre de-duplication removed.
  - C11: per-halo pair counts sum to the dual-tree count, exact.
  - C12: a window with x_t → infinity is the identity, and the continued grid reproduces the record grid.
  - C13: the sharp own variants equal CFG503's committed own tables, exact.
- **M0 (load-bearing) PASS.** The sharp window through this lane's code reproduces CFG503's 14 stack-P chi2 (max difference 0.0000), G2 21.524 and G3 73.994.
- **MUTATE SHUF (load-bearing) PASS** (see Bottom line 1).
- **C9 (reported) FAIL.** The steep window (beta 64, gamma 128) differs from the sharp E by up to 0.17 sigma per bin, against the 0.05 tolerance. f_t(1) = 0.25 for any beta, gamma, so a "steep" DK14 window is not a step at x_t = 1. The load-bearing sharp-limit check is M0, which passes.
- **Disclosed:**
  - The finder pre-screens seeds at log M_ta >= 12.0 before re-centring (a 0.3 dex margin); this is stated in the script header.
  - The numpy matmul RuntimeWarnings are the known Accelerate quirk; every table is finite.

## Limits
- Labels:
  - "transition PM-calibrated at log M_ta >= 13.5 (z = 0, 512^3, mesh 0.39 Mpc/h) and extrapolated ~1 dex to KiDS masses assuming self-similarity in r / r_ta";
  - "TRANSITION FORM POOR FIT ON PM".
- The calibration is at z = 0 only and is applied in units of each lens's r_ta(z).
- The PM force is softened below about 2 cells, so halo cores are puffier than NFW. Some of the 0.45-0.85 r_ta excess in the boxes may be this mass moved outward.
- Not modelled, the same for every model:
  - lens photo-z in R and Sigma_crit;
  - miscentring;
  - source-lens association / boost;
  - the satellites' own E.
- **What would close the gap:**
  - A higher-resolution LCDM box (finer PM mesh or a tree / P3M code) that resolves halos down to log M_ta ~ 12. That would calibrate the transition at KiDS masses directly, with a form that can carry an infall excess (e.g. a DK14 outer term fitted freely, or a tabulated xi_hm).
  - For G3, a one-halo normalisation / miscentring model for the non-isolated ALL sample.
  - **Needs owner go (unchanged):** the KiDS-bright x GAMA overlap and the MICE KiDS-bright mock.
- **Until a template passes all three LCDM gates, no KiDS isolated-lens verdict beyond the inner ~0.1 Mpc should be read as decisive.** That covers verdicts from CFG352, 413, 486, 487, 495, 498, 501, 502, 503 and this lane.

## Run
```
nice -n 15 python3 -u cfg504_pm.py        # ~10 min; catalogues + per-halo pair counts (2 x 512^3 sequential, 3 x 256^3, SHUF) -> _external_data/cfg504_work
nice -n 15 python3 cfg504_calib.py        # ~2 min; stacked xi_hm, DK14-window fits, primary x_t, SHUF check
nice -n 15 python3 -u cfg504_env.py       # ~6 min; E tables (sharp rebuild + smooth windows), both SHMR
nice -n 15 python3 -u cfg504_own.py       # ~70 min at nice 15 (4 processes); own profiles continued + windowed, all variants
nice -n 15 python3 -u cfg504_score.py     # frozen re-score, gates, verdict, reported variants
CFG504_MUTATE=1 nice -n 15 python3 -u cfg504_score.py
```
Needs CFG502's `cfg502_stage.npz` and CFG503's `cfg503_env_table.npz` / `cfg503_own_tables.npz` in `../../../_external_data/cfg50[23]_work/`. Large arrays (`cfg504_pm_*.npz`, `cfg504_env_table.npz`, `cfg504_own_tables.npz`) live in `../../../_external_data/cfg504_work/` and are not committed.
