# FRZ4 FROZEN CRITERIA (2026-11-13): the forest row graded at flux level, with the rare haloes realised bin by bin

Committed alone, before any script of this lane exists and before any flux number of this lane has been computed.
TEST lane: adopts nothing, relabels nothing (FRZ1, FRZ1R, FRZ3, FRZ3R, SRH1, SRH1R, SRF1, SRF1R keep their labels),
registers nothing. Footings (canonical a0 = 9.3603e-11 m/s^2, alt a0 = 1.1312e-10 m/s^2) graded separately, never pooled.
Cold dark energy is a gravitating field component; no particle is added. kappa = 1/2 is FITTED. The settled-radius
family (cases f = 1, 2, 3) is post hoc: it was chosen after FRZ1 failed. A HOLDS label is a hit that awaits an
independent blind re-grade, not a pass of the theory. Nothing here can say the data favour the framework.

## 1. Question and cases

Four flux-level builds of the forest row (FRZ3, FRZ3R, SRF1, SRF1R) have no graded label, each because a known answer
about the realised matter field failed. SRF1 traced its failure (known answer c1, over-realised 1.8 times at f = 1) to
sampling of the rare haloes (log M 12 to 14) that carry the change: one forced halo per 0.5 dex group, drawn from the
group's bins in proportion to expected count, one seed in most redshift bins. This lane repeats SRF1's build with the
sampling fixed, and grades:

- **Case A, f = inf: the full layout** (FRZ1's form-B profile to r_ta; SRH1's KA_T; the row of the paper's main failure).
- **Case B, f = 1, 2, 3: the settled layout** (law's layout inside R_set = f x R_fold, SRH1's lay_S, reference outside).

## 2. Reused code (copied into this folder and cited; physics unchanged)

- SRF1's `srf1_tables.py` (executes SRH1's `srh1_hm.py` prefix read-only; FRZ1's halo model, FLD1's fold radius) with the
  table list cut to f = 0, 1, 2, 3, inf. Nothing in the profile builder changes.
- SRF1's `srf1_run.py` painting and flux job, importing FRZ3R's `frz3r_core.py` read-only (lognormal smooth component,
  CIC painting on 0.1 dex bins, gas smoothing, FGPA with thermal broadening in 12 classes, saturation, mean flux matched
  by tuning A, 1D flux power along axis 2, 3D power). Box 20 Mpc/h, N 384, real space.
- Gas physics as FRZ3R and SRF1: T0 1e4 K, gamma 1.5 (beta = 2 - 0.7 (gamma - 1)), tau_eff(z) = 0.751 ((1+z)/4.5)^2.90
  - 0.132 (PROVISIONAL), **lambda_P = 79 comoving kpc** (Kulkarni et al. 2015, PROVISIONAL), held comoving.
- SRF1's `srf1_grade.py` gate set-up (FRZ3R's `frz3r_grade.py` prefix executed read-only: the record's
  `ss1_cosmo.forest_setup / forest_eval`, DESI DR1 P1D, full covariance, md5 33d7fc21...).

## 3. The one change: stratified realisation of the rare haloes, bin by bin

- Mass bins are FRZ3R's 0.1 dex painting bins (log M 8 to 15). Expected count in the box E_b = W_b V. A bin is **rare**
  if E_b < 30 (SRF1's threshold).
- **Forced set.** Per (z, footing), with s_b(f) = E_b [(U_R,b + dU_b(f))^2 - U_R,b^2] at k = 3 h/Mpc (the
  turnaround-scope one-halo difference, SRF1's share quantity) and p_b = E_b U_R,b^2 at k = 3 (reference one-halo
  power): a rare bin is forced if |s_b(f)| / |sum over all bins of s_b(f)| >= 0.005 at any of f = 1, 2, 3, inf, or
  p_b / sum p_b >= 0.005. At most 32 bins per (z, footing), the largest by max share if more qualify (the rest are
  then non-forced and reported).
- **Base box.** FRZ3R's Poisson draw over every bin in FRZ3R's random-stream order (seed 7919 + seed), so that the
  Poisson-only path is FRZ3R's reading T exactly. Two accumulations from the same draw:
  - the **all-bin path** (FRZ3R's reading T: every halo painted, f_s = 1 - painted mass / (rho V)); used only for known
    answer (b) and the reported Poisson-only reading;
  - the **stratified base**: every halo of a NON-forced bin, painted with U_Rb in R and U_S(f) in B (the change at its
    Poisson position); haloes of forced bins are left out. Smooth amplitude f_s fixed at the expected value fs_exp
    (FRZ3R's smooth target, same lognormal field). B_base = R_base + sum dU (non-forced) + fs_exp delta_s T2(f), T2 the
    two-halo factor sqrt(1 + D2h_f / S) - 1 as SRF1.
- **Forced boxes.** One box per forced bin b: R_b = R_base + ONE halo of bin b (the bin's count-weighted mean profile
  U_Rb, uniform random position from its own stream [seed, 10 z, b, 104729]); B_b = R_b + dU_b(f). Weight w_b = E_b.
  No draw between bins: every forced bin is realised, each with its own weight, so the within-group draw that broke
  SRF1 is gone.
- **Estimator** for any power X (1D flux or 3D matter), per f:
  X_R = X(R_base) + sum_b E_b [X(R_b) - X(R_base)], X_B = X(B_base) + sum_b E_b [X(B_b) - X(R_base)],
  ratio R_X(f) = X_B / X_R. Numerator and denominator are both stratified (SRF1 left the rare reference haloes at Poisson
  positions in its denominator). Each field's mean flux is matched to the target separately.

## 4. Sampling and compute plan (budget about 5 h wall, one heavy job, 2 flux threads, peak memory under 20 GB)

- **Redshift bins computed:** z = 2.2, 2.6, 3.0, 3.4, 3.8, 4.4 (6 of DESI DR1's 12), both footings, seed 0.
  **Estimated bins:** 2.4, 2.8, 3.2, 3.6, 4.0, 4.2: the flux ratio R_F - 1 at that bin's DESI points, and the 3D matter
  ratio R - 1 on the k grid, interpolated linearly in z between the two computed neighbours. Every table marks them
  "estimated". The 12-bin Delta chi^2 uses computed and estimated bins together.
- **Seeds:** seed 0 everywhere; seed 1 at z 2.2 (both footings, full part) for known answer (e). The z 2.2 ratio is the
  seed mean.
- **Fields per box:** R and B at f = 1, 2, 3, inf (5). Base box adds the all-bin R and its Poisson-only B at f = inf
  (known answer b). At z 2.2, 3.0, 4.4 seed 0 every box adds B at f = 0 (known answer a). At z 2.2 seed 0 every box adds
  the doubled change at f = 1, 2, 3, inf (mutation M2).
- **Brackets and M1:** z 2.2 and 3.0, seed 0, both footings, on the base box plus the bracket subset (forced bins in
  descending max share until the cumulative share >= 0.8 at every f, at most 10 bins); clustered placement at z 2.2 on
  the same subset.
- **Order of stages:** tables (all 12 z, needed for the halo-model numbers); primary 2.2, 3.0, 4.4, 2.6, 3.4, 3.8; seed 1
  at z 2.2; brackets z 2.2; clustered z 2.2; brackets z 3.0. If the budget runs out, the stages not run are named in
  RESULT; a missing primary bin is estimated as above and marked; missing brackets put "brackets incomplete" on the label
  (bracket estimates then use z 2.2 alone).
- Restartable part files per box; SIGTERM stops between boxes (exit 75); `nice -n 19`; a process exits and is restarted
  when its peak resident memory passes 12 GB. Temporary tables and base-box arrays are deleted at the end.

## 5. Statistic and gate (as FRZ3R and SRF1 applied them)

The flux ratio R_F(k_v, z) multiplies DESI DR1's P1D at its 755 points; Delta chi^2 = d^T C^-1 d, d = (R_F - 1) P_D,
full covariance. **Gate: Delta chi^2 <= 4.** Matter level of the same fields: the record's projection (`forest_eval`
with sqrt of the 3D ratio, FRZ3R's `amp`) of the realised 3D ratio, k <= 10 h/Mpc.

## 6. Known answers (all that apply must pass, or that case and footing is NO VERDICT)

- **(a)** f = 0: in every box at z 2.2, 3.0, 4.4 seed 0, max over k_v of |P_F(B_f0) / P_F(R) - 1| <= 1e-12 (rounding
  allowed at the 1e-12 level), and the stratified 12-bin flux Delta chi^2 at f = 0 <= 1e-12. Applies to every case.
- **(b)** Poisson-only path at f = inf: per computed base box, the all-bin R and B flux power equal FRZ3R's `turn_*` part
  of the same (z, seed, footing) within 1e-4 relative at every k_v; the flux and matter Delta chi^2 of this path on the
  computed bins (others set to 1) equal FRZ3R's on the same bins and seeds within 1 %. Applies to every case.
- **(c0)** halo-model chain: record-convention D_rec equals SRH1's committed numbers within 1 %: f = 1: 38.74 / 36.66
  (SRH1 = FZS1); f = 2: 452.12 / 275.1 (SRH1); f = inf: 9916 / 9009 (SRH1's KA_T = FRZ1); f = 3 has no SRH1 point and is
  checked against SRF1's own 679.7 / 480.5 within 1 %. Per case.
- **(c1) the one that matters**: the realised matter-level Delta chi^2 D_mat (12 bins, estimated bins included) lies
  within **0.67 to 1.5** of the halo model's own turnaround-scope value D_ta (ratio P_S,ta / P_Rb,ta through the same
  projection), per case and per footing; AND, for every computed z bin whose halo-model single-bin Delta chi^2 is >= 1,
  the realised single-bin value lies within 0.5 to 2 of it (catches SRF1's per-bin over- and under-realisation).
- **(d)** every field's mean flux equals the target within 1e-4.
- **(e)** seed scatter at z 2.2: N12 = Delta chi^2 of the half seed difference (R_s0 - R_s1)/2 in the z 2.2 bin, scaled to
  12 bins by (12-bin Delta chi^2 / z 2.2-bin Delta chi^2 of the seed mean). Pass if N12 <= 0.1 D or N12 <= 0.05, D the
  case's flux Delta chi^2. SE = 2 sqrt(D N12) + N12 is reported; **MARGINAL** is added if |D - 4| < 2 SE. Per case.

## 7. Mutations (separate `*_MUTATE*` outputs; must bite or the label is NO VERDICT)

- **M1 saturation removed** (F = 1 - A tau, linear; mean flux matched linearly): z 2.2 bracket subset, seed 0; bites if
  the flux Delta chi^2 on that subset changes by at least x 1.25 (either direction) at every case f.
- **M2 layout change doubled** (B - R doubled in density, base and forced boxes, z 2.2 seed 0 all boxes): bites if the z
  2.2 flux Delta chi^2 is at least 1.5 times the primary's at every case f.

## 8. Brackets (frozen; FRAGILE if the 12-bin estimate of any bracket lies on the other side of 4 from the primary)

lambda_P x 0.5, x 2, and 100 proper kpc; gamma 1.2 and 1.6 (temperature-density slope); tau_eff x 0.9 and x 1.1 (mean
flux); clustered placement (base box by FRZ3R's clustered sampler, forced haloes by the same sampler with their bin's bias).
12-bin estimate = primary 12-bin x (bracket / primary), both on the bracket subset at z 2.2 + 3.0 (z 2.2 alone for
clustered placement). Not bracketed, stated as left out: the rare threshold 30, the 0.005 forcing cut, one halo per
forced box, uniform placement in the primary, box size, resolution.

## 9. Labels (per case, per footing)

- **FOREST ROW FAILS AT FLUX LEVEL**: flux Delta chi^2 > 4. **FOREST ROW HOLDS AT FLUX LEVEL**: <= 4 (not a pass of the
  theory; a hit that awaits an independent re-grade). Either may carry FRAGILE (section 8) and MARGINAL (section 6e).
- **NO VERDICT**: a known answer that applies fails, or a mutation does not bite. If c1 fails, no tuning after the fact:
  NO VERDICT for that case, with the sampling that would be needed. A later change is a dated amendment committed alone,
  with the as-frozen reading first.
- Reported beside each label: flux and matter Delta chi^2 of the same fields and their ratio; D_ta and D_rec; per-bin
  values and R_F at k_v 0.003 / 0.005 / 0.01 / 0.02 / 0.03 s/km for computed bins; the record-convention reading (flux x
  D_rec / D_mat, reported, not a bracket); the Poisson-only reading; the share of the flux and matter Delta chi^2
  carried by haloes above and below FRZ1's boundary speed (SRH1's `regime`, per forced bin by majority of its grid
  masses; the base box counted below the boundary, with the halo-model share of its change that lies above reported).

## 10. Expectation and hand estimate (written before any number)

- Case A, f = inf: the realised field is FRZ3R's reading T plus the rare haloes it lacked. D_mat about D_ta = 4983 /
  4398 (SRF1's halo model); flux about 300 to 500 (FRZ3R's T 363 / 425 at matter 5035 / 4377; ratio 0.07 to 0.1). No
  bracket reaches 4 (FRZ3R's lowest 35.7). Expect **FAILS / FAILS**, c1 passes: 75 %.
- Case B: SRF1 (over-realised 1.8x) read 0.068 / 0.072 at f = 1, 0.32 / 0.23 at f = 2, 0.67 / 0.58 at f = 3; SRF1R 0.008 /
  0.005, 0.19 / 0.14, 1.7 / 1.5. Hand estimate here: f = 1: 0.02 to 0.06; f = 2: 0.15 to 0.3; f = 3: 0.4 to 1.5. Expect
  **HOLDS / HOLDS at f = 1, 2, 3**, f = 3 possibly FRAGILE through gamma 1.6 or lambda_P x 0.5. Probability that c1
  passes at every settled case: 60 %; NO VERDICT on at least one settled case: 40 %.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
