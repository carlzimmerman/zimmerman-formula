# FRZ3R READING: blind re-grade of the forest row at FLUX level

Committed alone, before any FRZ3R script is in the lane folder and before any flux-level number exists. TEST lane: adopts
nothing, relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), graded
separately, never pooled. Cold dark energy is a gravitating field component; no particle is added. A HOLDS reading is not a
pass: it is a hit that needs a further independent check. Nothing here says the data favour the framework.

## 0. Question, and what I have seen

Does rule 5's redistribution (FRZ1's layout at z 2.2 to 4.4) fail the record's forest gate (Delta chi^2 <= 4 on the 755 DESI
DR1 P1D points, full covariance) when the forest is computed at FLUX level (FGPA with saturation, thermal broadening, pressure
smoothing, mean flux matched), not through the record's linear matter projection?

Read before this freeze: FRZ3's FROZEN_CRITERIA (e56c67ae91), A1 (1483ae75ef), A2 (50dcbd956e) at their commits only; FRZ1's
criteria, RESULT, `frz1_hm.py`, `frz1_hm.json` structure; FRZ1R's READING, RESULT, code; `ss1_cosmo.py` lines 140 to 238
(`forest_setup`, `p1d_at`, `forest_eval`); CFG556's library prefix (lines 1 to 215, which FRZ1 executes); the record's
lognormal forest mock `nbody_2026/stage16_lognormal_forest_mock_2026.py` (for its IGM numbers) and RF5's assumption ledger
line A21; Kulkarni et al. 2015 (arXiv 1504.00366) abstract and HTML Sec. IV.5 / Eq. 16, read twice through WebFetch.

**Blindness breach, stated in full.** The session context of this lane listed recent repository commits, including FRZ3's
two result commits. Their subjects showed me, before I wrote anything: FRZ3's label "NO VERDICT / NO VERDICT (painting known
answer fails)"; its flux Delta chi^2 "4.71 / 2.58" against matter "4720 / 4120" on the same fields; "saturation is the step
that softens"; "brackets cross the gate on both footings"; "post hoc doubled difference about 18 / 10"; "painted fields
carry about half of FRZ1's matter redistribution"; and a lambda_P floor-off check. I did not open any FRZ3 file beyond the
three criteria commands. I cannot unsee these numbers; my hand estimate (section 8) was written knowing them.

## 1. Pre-freeze design checks (disclosed; no flux number, no Delta chi^2 was computed)

The lead asked for a realisation in which the matter-level known answer (b) can pass. Before freezing I ran halo-model and
matter-only field checks in a scratch directory (code that becomes `frz3r_core.py`). What I saw:

- FRZ1's R_cold is R_tot / R_bar with R = 1 + (P_X - P_Lta) / P_std: the change computed in the TURNAROUND-scope halo model,
  divided by the STANDARD (r200m) spectrum. At z 3, k 3 the turnaround-scope spectrum is about 2 x P_std (1.68 vs 0.87,
  canonical). So a field painted with turnaround-scope haloes on both sides gives P_B / P_Rb = 0.920 at z 3, k 3 against
  FRZ1's 0.845: about half the effect (the FRZ3 failure mode, found here independently in the halo model). Painting the
  plain difference (U_B - U_Rb) on a standard-halo-model field gives the same half (0.919 / 0.915 expected / realised).
- In FRZ1's spectrum difference P_B - P_Rb the two-halo part dominates at k <= 1 h/Mpc (z 3: one-halo -0.024, two-halo
  -0.031 at k 1; one-halo -0.121, two-halo -0.014 at k 3).
- Halo placement proportional to exp(b G_f) on the smooth field (clustered) moves the realised reference power far from
  P_std R_bar (0.29 to 1.29 of it at k 3 for G_f smoothing 0.15 to 0.8 Mpc/h), and with it the matter ratio; not used as
  primary (section 5 bracket instead).
- The construction frozen in section 2 (matched difference, uniform halo positions, smooth lognormal with target power),
  one seed, N 256, z 3: realised matter ratio at k 1 / 3 / 5 = 0.9941 / 0.8276 / 0.6269 (canonical; FRZ1 0.9920 / 0.8446 /
  0.6646) and 0.9959 / 0.8135 / 0.6164 (alt; FRZ1 0.9916 / 0.8314 / 0.6695): inside the tolerance of section 4 (b). The
  plain painting on the same fields: 0.9995 / 0.9287 / 0.7719 (canonical). Realised reference power over P_std R_bar:
  1.13 / 0.82 / 0.76 at k 1 / 3 / 5.
- Timing smoke runs of a full anchor part at N 384 (z 3, seed 0, canonical), flux outputs never opened (only run time and
  peak memory: 140 to 215 s, about 16 GB peak; the frozen run is restartable by part and stays one job, 4 threads); a first
  attempt stopped on the mean-flux root finder because FFT broadening ringing gave negative tau, now clipped at 0. The smoke
  parts are deleted before the graded run; the lane folder starts empty of numbers.

## 2. Fields (fixed)

- **Halo model:** FRZ1's own code (`frz1_hm.py` prefix executed read-only, which executes CFG556's library), FRZ1's graded
  reading L (isothermal remainder), footing by footing. Check b0: my call reproduces FRZ1's stored R_cold at k 1, 3, 5 at
  each anchor to 1e-6.
- **Profiles per halo mass M (1e8 to 1e15 Msun/h, FRZ1's grid):** U_std (NFW to r200m, mass M), U_Lta (NFW to r_ta), U_Rb
  (FRZ1's comparison layout), U_B (rule 5, reading L). Reference halo profile U_ref = U_std + (U_Rb - U_Lta): the standard
  halo plus the zero-mass condensation of the baryons, so the reference field's spectrum is FRZ1's denominator P_std R_bar.
- **Graded difference ("matched", M):** the zero-mass profile C1(k) = -U_ref + sqrt(U_ref^2 + U_B^2 - U_Rb^2), i.e. the
  per-halo change whose one-halo power change equals FRZ1's (U_B^2 - U_Rb^2); plus FRZ1's two-halo difference
  P_lin (I_B^2 - I_Rb^2) / norm^2 realised on the smooth component as a k-space factor sqrt(1 + D_2h / S). In expectation
  the field ratio is FRZ1's R_cold exactly. This is a construction to carry FRZ1's matter-level redistribution into a
  density field with the one-halo change localised on each halo; it is not derived from rule 5 in real space.
- **Reported, never graded ("plain", P):** the same haloes with U_B - U_Rb painted directly, no two-halo change.
- **Box:** periodic L = 20 Mpc/h, N = 384 (cell 0.052 Mpc/h). Halo catalogue: Poisson counts in 0.1 dex bins from FRZ1's mass
  function (count-weighted mean profile per bin), positions uniform (unclustered: section 7), CIC deposit with the CIC window
  divided out (floor 0.05), profiles applied in k-space by linear interpolation in ln k on a 900-node table to 400 h/Mpc.
- **Smooth component:** weight f_s = 1 - painted mass / box mass; a lognormal field (Gaussian power from
  xi_G = ln(1 + xi_T) on the grid, negative modes clipped) with target power S / f_s_exp^2, S = P_std R_bar - (expected
  one-halo power of the painted reference haloes). Linear spectrum: CFG556's EH no-wiggle at sigma8 0.811 x D(z)^2.
- **Seeds:** white noise seeded by the seed only (same at every z); the same white noise, halo positions and smooth field
  serve both footings and every variant. Anchors z 2.2, 3.0, 4.4: seeds 0 to 3. Other nine DESI bins: seeds 0 and 1, primary
  fields only (R and M).

## 3. Gas, flux, statistic (fixed)

- **Gas:** 1 + delta_gas = (whole matter field) x exp(-k^2 lambda_P^2 / 2); gas traces total matter above lambda_P.
  lambda_P = 79 comoving kpc = 0.0532 Mpc/h, held fixed in comoving units at every z (Kulkarni et al. 2015, F_real power fit
  exp(-k^2 / k_ps^2) with lambda = 1/k_ps = 79 comoving kpc at z 3, fiducial thermal model; PROVISIONAL, WebFetch read twice).
  Pixels with 1 + delta_gas < 1e-6 are floored at 1e-6; the floored fraction is recorded per field.
- **FGPA:** tau = A (1 + delta_gas)^beta, beta = 2 - 0.7 (gamma - 1); T = T0 (1 + delta_gas)^(gamma - 1); T0 = 1e4 K,
  gamma = 1.5 (beta 1.65), the record's lognormal mock defaults (stage16, PROVISIONAL). Thermal broadening: Gaussian
  exp(-v^2 / b^2), b = 12.85 sqrt(T / 1e4 K) km/s, applied along the line of sight in 12 classes of log b (class-centre b),
  by FFT; FFT ringing that makes tau negative is clipped at 0. Real space (no peculiar velocities) in the primary.
- **Mean flux:** A tuned separately in each field so <F> over the box = F_bar(z) = exp(-tau_eff), tau_eff = 0.751
  ((1 + z) / 4.5)^2.90 - 0.132 (Becker et al. 2013 as written in the record, stage16 and RF5 A21; PROVISIONAL).
- **Skewers:** every grid line along axis 2 (147,456 per field, 384 pixels). P1D_F per mode of delta_F = F / <F> - 1.
  Velocity per cell from H(z) of FRZ1's flat cosmology (h 0.6736, Om 0.3138).
- **Flux ratio:** R_F(k_v) = P1D_F(M) / P1D_F(R) per seed; graded R_F = mean over seeds of the per-seed ratios.
- **Gate (flux level):** at every DESI point (forest_setup, md5 33d7fc21bfd3d745ed71a0bbe80ca433) r = R_F(k_data) linear in k
  between box modes, flat at the first mode below the box fundamental; d = (r - 1) P_data; Delta chi^2 = d C^-1 d with the
  full covariance; gate Delta chi^2 <= 4. All 12 bins computed (no z interpolation).
- **Matter level of the same fields:** R_paint(k) = 3D power ratio M / R of the unsmoothed fields, seed mean, 40 log bins
  from 0.3 h/Mpc; fed to the record's projection exactly as FRZ1 / FRZ1R did (`forest_eval` with form B's CLASS reference,
  amplitude sqrt(R) on the (KG, ZG) grid, nearest DESI bin, R_paint used for 0.3 <= k <= 10 h/Mpc and flat at its end
  values outside). Reported beside the label: Delta chi^2(flux), Delta chi^2(matter, same fields), their ratio
  (the softening), and FRZ1's own 9916.2 / 9008.7.
- Reported, not graded: the gas-level 1D ratio; per-bin Delta chi^2 (own covariance block); per-seed Delta chi^2;
  the plain painting's flux and matter Delta chi^2.

## 4. Known answers (any failure: NO VERDICT)

- **(a)** B = R + 0 x (difference) through the same code path: R_F = 1 exactly at every mode, Delta chi^2 = 0 (each anchor,
  each seed, both footings); the gate returns 0 at R = 1; DESI md5 matches.
- **(b) matter level:** seed-mean R_paint at k 1, 3, 5 h/Mpc (log-interpolated between bins) at each anchor z, both footings,
  within |R_paint - R_FRZ1| <= 0.01 + 0.25 |R_FRZ1 - 1| of FRZ1's stored R_cold (reading L).
- **(c) thin limit:** beta = 1, no broadening, no pressure smoothing, 1 - <F> = 1e-7 (seed 0, anchors): R_F equals the 1D
  ratio of the unsmoothed matter along the same skewers at every mode with k_v <= the DESI maximum of that bin, within
  1e-3 + 0.01 |R_matter,1D - 1| (both from the same floored field, floor 1e-6).
- **(d)** |<F> - F_bar| <= 1e-4 in every field and variant that uses exp(-tau) with the target mean (not the thin limit,
  where 1 - <F> = 1e-7 by construction; M1 matches the mean exactly by construction and is checked too).
- **(e) seed scatter:** at each anchor and footing, E = rms over the DESI-range modes (box fundamental to the bin's DESI
  maximum) of (R_F - 1); S = rms over the same modes of the standard error of the seed mean (std / sqrt 4). NO VERDICT if
  S > E / 3 anywhere. Reported: per-seed Delta chi^2 (anchor bins) and its spread against the mean.

## 5. Mutations (anchors, all seeds; written to `*_MUTATE*` outputs; each must bite, or NO VERDICT)

- **M1 saturation removed:** F = 1 - A tau (tau, broadening and beta kept; A tuned so <F> = F_bar). Bites if the anchor-bin
  Delta chi^2 (three anchor bins, joint covariance block) differs from the primary's by a factor >= 1.25 either way, both
  footings. Its direction (toward or away from the matter level) is reported.
- **M2 redistribution doubled:** B = R + 2 x (matched difference, both its one-halo and two-halo parts). Bites if the
  anchor-bin Delta chi^2 rises by a factor >= 2, both footings. Floored fraction reported.

## 6. Brackets (frozen; anchors; reported beside the label; any bracket on the other side of the gate -> FRAGILE)

lambda_P x 0.5 and x 2; lambda_P = 100 proper kpc (the record's stage16 value, about x 5 at z 3); gamma 1.2 and 1.6;
mean flux with tau_eff x 0.9 and x 1.1; resolution N 256 (same box, seeds 0 and 1); peculiar velocities on (linear theory
from the smooth field's Gaussian, same in both fields; seeds 0 and 1); clustered halo placement (positions proportional to
exp(b G_f), G_f the smooth field's Gaussian smoothed at 0.5 Mpc/h; seeds 0 and 1; its own matter ratio reported, (b) not
required of it). A bracket's 12-bin value = Delta chi^2(primary, 12 bins) x [Delta chi^2(bracket) / Delta chi^2(primary)]
on the three anchor bins (joint block), each with the seeds it has and the primary on the same seeds.

## 7. Physics left out (stated in the result)

Hydrodynamics (gas follows matter above lambda_P only), shock heating and the hot halo gas, self-shielding and damped
systems in haloes, UV-background and temperature fluctuations, metals, continuum errors; halo positions uncorrelated with the
smooth IGM in the primary (bracketed); velocities in the primary (bracketed); form B's change of halo velocities and
potentials (not modelled: velocities, where included, are the same in both fields); haloes below 1e8 Msun/h; the matched
difference is a construction (section 2). Box 20 Mpc/h: DESI points below the fundamental (about 0.0024 to 0.0031 s/km)
take the first mode's ratio.

## 7b. Compute plan (frozen)

Stages in this order, one job, `nice -n 19`, 4 threads, a part file per (stage, z, seed, footing), SIGTERM stops between
parts (exit 75), done-file at the end: anchors (z 2.2, 3.0, 4.4; seeds 0 to 3; every variant); the nine other bins (seeds 0,
1; primary); resolution N 256 (anchors, seeds 0, 1); clustered placement (anchors, seeds 0, 1). If time runs short the
later stages are dropped in reverse order and the missing brackets are reported as not computed; the graded number needs
only the first two stages.

## 8. Labels (per footing, never pooled)

- **FOREST ROW FAILS AT FLUX LEVEL:** Delta chi^2(flux) > 4 and every bracket > 4.
- **FOREST ROW FAILS AT FLUX LEVEL, FRAGILE:** Delta chi^2(flux) > 4, some bracket <= 4 (named).
- **FOREST ROW HOLDS AT FLUX LEVEL (not a pass; a hit awaiting a further independent check)**, with FRAGILE if any bracket > 4.
- **NO VERDICT:** a known answer (a) to (e) fails, or a mutation does not bite. The numbers are then reported ungraded.

## 9. Hand estimate (written knowing FRZ3's leaked numbers, section 0)

The matched field carries FRZ1's full matter change: about -1 % at k 1 (mostly the two-halo part, on the smooth IGM, which
the flux sees almost linearly) and -15 to -35 % at k 3 to 5 inside haloes. Saturation hides most of the halo-core change;
lambda_P = 0.053 Mpc/h smooths little at k 3 to 5 (FRZ3 used about four times larger). I expect R_F - 1 of -0.5 % to -3 %
over the DESI range, flux Delta chi^2 of 20 to 300 (softening 0.003 to 0.03 against the same fields' matter-level value of
order 1e4), label FAILS AT FLUX LEVEL on both footings, with the lambda_rec and gamma or mean-flux brackets the likeliest to
come near the gate; about 25 % chance a bracket crosses (FRAGILE), about 10 % chance of HOLDS. The plain painting should give
roughly a quarter of the matched flux Delta chi^2.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
