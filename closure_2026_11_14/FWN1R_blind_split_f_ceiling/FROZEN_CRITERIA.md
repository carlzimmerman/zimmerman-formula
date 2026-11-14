# FWN1R frozen criteria: blind flux-level ceiling on f for the crossing-speed split, and the split with no settled radius

2026-11-14. Committed alone, before any script exists in this folder and before any new number is seen. TEST lane: adopts nothing,
relabels nothing, registers nothing. Footings (canonical a0 9.3603e-11, alt 1.1312e-10 m/s^2) never pooled. Cold dark energy is
a gravitating field component; no particle is added. kappa = 1/2 and 5.41 are FITTED. Nothing here says the data favour the
framework.

## 0. Blindness and build

The build is my own FRZ6R build (criteria 4314f23c90, amendment 4265c14111, scripts and parts 394f36e3c9, result 1aedb882d0),
copied into this folder and adapted; nothing in the FRZ6R folder is edited, and its parts are read read-only. The FRZ6R forbidden
list stays forbidden, plus `closure_2026_11_13/FWN1_forest_flux_split_f_ceiling/` and
`closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/`. I know my own FRZ6R numbers (f = 1.25, 2, 3 and the control);
I have seen nothing for f = 5, 10 or infinity.

## 1. Cases

Split as in FRZ6R (boundary v*(z) = v*(0) / E(z), v*(0) = a0 / (10 (1 + 5.41) H0), H0 67.4, OL 0.6847; FRZ1's v_vir; haloes
faster than v* keep the reference layout "Rb" at every radius).
- J5, J10: slower haloes carry the settled layout at R_set = f x R_fold (FZS1's rset_com, capped at r_ta), f = 5 and 10.
- Jinf (f = infinity): slower haloes carry the law's layout at every radius, i.e. FRZ1's mode "B" called directly (the control's
  layout for that halo, not the splice at r_ta, so that it is bitwise the control's row).
- Also recomputed in every part: R (reference), J3 (f = 3) and C (control: mode "B" for every halo), for the reproduction known
  answers and the twin.

## 2. Unchanged from FRZ6R

Tables (KT grid, U_set, spectra_ta), box (L 20 Mpc/h, N 384, real space), halo realisation (0.125-dex bins, per-mass Poisson,
uniform positions, TSC with deconvolution), lognormal two-halo component with the factor |I_X / I_R|, seeds
(SeedSequence([6, 61, iz, s])), gas (Gaussian smoothing exp(-0.5 (k lambda_P)^2), lambda_P 79 comoving kpc, floor 1e-6), the FGPA
step reused from FRZ3R (`tau_field`, `tune_A`, `p1d`, `dv_cell`), gamma 1.5, T0 1e4 K, tau_eff(z) = 0.751 ((1+z)/4.5)^2.90 - 0.132,
the forest data (`ss1_cosmo.forest_setup`), the estimator (ratio of seed sums), D (12-bin flux Delta chi^2, full covariance), the
jackknife SE over the seed index, the anchor statistic A (z 2.2, 3.0, 4.4), 4 seeds (0 to 3) in all 12 bins, no optional
stopping. Parts are one (z, seed) per process; brackets one (z, seed, bracket) per process.

## 3. Known answers (all must pass for HOLDS)

- KA-INF: at every z and footing, the Jinf table's row for every halo slower than v*(z) equals the control's row bitwise, and
  for every faster halo equals the reference's row bitwise. Flux: at z 3.0, seed 0, a field built from a table assembled row by
  row from the control and reference tables by the v* mask gives the same flux P1D as Jinf (|ratio - 1| <= 1e-6 at every mode).
- KA-3: the recomputed J3, R and C flux P1D equal FRZ6R's stored primary parts (same z, seed, footing) with |ratio - 1| <= 1e-6
  at every mode k_v > 0, in all 96 part files.
- KA-C: the control's D equals FRZ6R's (323.0468 / 395.8263) within 1e-6 relative, and it fails (D - 2 SE > 4).
- KA-N: the grid haloes above v*(z) equal JNT2's membership counts at every z and footing.
- KA-F: |<F> - exp(-tau_eff)| <= 1e-4 for every flux field.
- KA-M: at the anchors, the realised matter ratio (ratio of seed sums of P3D) at k 1, 3, 5 h/Mpc is within 0.01 + 0.3 |E - 1| of the
  halo model's E, for J5, J10, Jinf.
- KA-S, per case: D_noise (the jackknife standard error of R^ at each point, through the covariance) <= 0.1 max(D, 4).

## 4. Twins (designed for these cases; must bite)

- TW-A, boundary removed at f = infinity: the control C (the law's layout in every halo) compared with Jinf, on the full 12-bin D.
  It bites if D_C / D_Jinf >= 1.25 or <= 0.8, and |D_C - D_Jinf| > 2 sqrt(SE_C^2 + SE_Jinf^2). Why a correct build must bite:
  - Jinf differs from C only in the haloes faster than v*(z): M200c above about 8e11 Msun at z 2.2 and about 4e10 at z 4.4.
    These hold most of the turnaround-scope mass and most of the one-halo matter change.
  - In FRZ6R the control moved the flux power by 3 to 9 % at z 2.2. A split that leaves all those haloes in the reference must
    move it measurably less, while C's own seed SE is about 1.5 to 2 % of D.
  - Unlike FRZ6R's TW1, both sides of this comparison have large D, so the absolute and noise problems that stopped TW1 do not
    apply.
- TW-B, difference doubled at f = 10: field R + 2 (J10 - R), anchor statistic. It bites if A_TWB / A_J10 >= 2.5 (linear response
  predicts 4; FRZ6R's doubled twin gave 3.3 to 3.4). A correct build must bite because the flux response to a small field
  difference is close to linear and was so in FRZ6R.
- If a twin does not bite: the label rule stands (no HOLDS for any case), FAILS is still given where D - 2 SE > 4, and
  RESULT_BLIND.md states which twin failed, by how much, and that the build has then not shown the sensitivity needed to call a
  HOLDS. No redesign follows the numbers.

## 5. Labels (per case J5, J10, Jinf and footing)

FOREST ROW HOLDS AT FLUX LEVEL if every known answer passes, both twins bite and D + 2 SE < 4 (a hit, not a pass). FOREST ROW
FAILS AT FLUX LEVEL if D - 2 SE > 4. Otherwise NO VERDICT. FRAGILE (bracket named) when a frozen bracket's 12-bin estimate lies on
the other side of 4 from D. Known-answer and twin failures are named beside any label. Before writing HOLDS anywhere I re-check
that both twins bite and that the control fails.

## 6. Brackets (anchors, seeds 0 and 1, fields R, J5, J10, Jinf; 12-bin estimate D x A_br / A_prim on the same seeds)

lambda_P x 0.5 and x 2, gamma 1.2 and 1.6, tau_eff x 0.9 and x 1.1. Reported beside the label: the measured-range reading at
lambda_P = 91.4 and 138.6 comoving kpc (Rorai et al. 2017, Table S2, z = 3.0; PROVISIONAL, from the lead's FRZ6R brief, not looked
up).

Grid resolution, plainly: the cell is 52.1 kpc/h = 77 comoving kpc. lambda_P x 0.5 (40 ckpc) is below one cell and is NOT
resolved. The primary 79 ckpc is about one cell, so it is only marginally resolved. 91.4, 138.6 and 158 ckpc (x 2) span 1.2 to 2
cells. Brackets in gamma and tau_eff do not depend on resolution beyond the primary's.

## 7. Ceiling on f (reported, never a label)

Points: f = 2 and 3 (FRZ6R's D and SE, which KA-3 shows are the same build), 5, 10 and infinity (placed at f = 1e3 for the
interpolation; if the crossing lies beyond f = 10, it is reported as "above 10" with the 5-to-10 log slope extrapolation given
separately). Per footing, f_ceil is where U(f) = D + 2 SE reaches 4, by linear interpolation of ln U in ln f between the adjacent
points that bracket 4. Uncertainty: the same interpolation with U replaced by D - 2 SE and by D + 4 SE gives the range. If no point
brackets 4, report the side.

## 8. Hand estimate (before any number)

FRZ6R's own D grew by about 24 from f = 2 to f = 3 (0.024 to 0.57 canonical), as R_set reaches the outskirts. The growth should
slow once R_set is capped at r_ta for many haloes. Estimate (canonical; alt about 20 % higher): D(f = 5) 3 to 20, D(f = 10) 15 to
80, D(f = infinity) 30 to 150, against the control's 323. Labels: f = 5 NO VERDICT or FAILS, f = 10 and infinity FAIL. f_ceil
about 4 (range 3.5 to 6). Twins bite. Low confidence on how fast D saturates.

## 9. Compute

At most two part processes at once, `nice -n 19`, 2 threads each. Physical-footprint guard of 16 GB after every flux step. Before
each part: free disk at least 10 GB and free plus inactive memory at least 24 GB, else wait; stop below 8 GB disk or above 14 GB
swap. A detached runner with a pid file and a done marker. Small JSON parts only. About 4 h.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
