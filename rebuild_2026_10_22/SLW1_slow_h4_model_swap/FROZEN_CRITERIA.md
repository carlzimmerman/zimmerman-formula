# SLW1 FROZEN CRITERIA: is the slow-rotator h4 pattern a JAM-model artefact?

Frozen before any per-model number is computed. kappa = 1/2 FITTED; footings never pooled; not theory closed.

## Origin (post hoc, stated first)
LAM6, LAM7 and LAM8 each printed an ungraded row: inside slow rotators, KU2's law residual at r_half rises with
integrated h4 (+0.088 LAM6, +0.110 LAM7, +0.077 LAM8, canonical), while fast rotators show about zero. The idea
for this lane came from those rows, and this sample overlaps theirs. So the best possible outcome here is a
LEAD that needs independent data, never a finding.

## Question
DynPop gives ten JAM models per galaxy (HDU 2-11): even HDUs cylindrical (beta_z), odd HDUs spherical (beta_r),
in five mass-model pairs (2/3 mass-follows-light, 4/5 free NFW, 6/7 fixed NFW, 8/9 gNFW, 10/11 power law;
mapping read from each HDU's columns). If the pattern comes from JAM's anisotropy assumption misfitting
radial-orbit slow rotators, it should change between cylindrical and spherical alignment.

## Sample
KU2's selection, KU2's slow class, LAM4's 1000 + LAM7's 5056 integrated fits, restricted to Sigma_Re >= 100 km/s
(the regime where LAM8's K1 passes). h4 = h4_int from `lam4_fit.jsonl` / `lam7_fit.jsonl`.

## Statistic
For each model k: residual r_k as in KU2 (`accel`, `resid`, that model's log_Mt_rhalf and rhalf_arcsec).
E_slow,k = OLS slope of within-cell (KU2 cell) demeaned r_k on demeaned h4, slow galaxies only, cells with >= 3
slow galaxies, x IQR(h4) over the whole cut sample. Delta_m = E_slow(cyl) - E_slow(sph) for each mass pair;
Delta_bar = mean over the five pairs. 2000 bootstrap draws over slow galaxies (seed 20261105), all models in
the same draw. Canonical and alt separately.

## Checks
- C1: slow galaxies in cells >= 150. C2: KU2's D reproduced exactly.
- M1 (MUTATE, outputs by mode): h4 shuffled within cells among slow; E_slow under KU2's chosen model must have a
  95 % interval including 0, else NO VERDICT.
- Known limit: K2 failed in LAM7 (h4 rms 0.038). Random h4 error attenuates slopes; it cannot create one.

## Labels, per footing, checked in this order
1. **ANISOTROPY-MODEL DEPENDENT**: |Delta_bar| >= 0.03 and its 95 % interval excludes 0.
2. **ROBUST LEAD**: E_slow >= 0.05 with a 95 % interval excluding 0 under all ten models.
3. **NOT ROBUST**: E_slow's 95 % interval includes 0 under >= 3 of the ten models.
4. otherwise **NO VERDICT**.

## Rows (ungraded)
E_fast,k for all ten models; E_slow under KU2's chosen model; Spearman(h4, fitted beta) among slow galaxies,
per model; E_slow on LAM7-new galaxies only.
