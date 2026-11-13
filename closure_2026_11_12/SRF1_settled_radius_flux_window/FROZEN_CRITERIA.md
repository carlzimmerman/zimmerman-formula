# SRF1 FROZEN CRITERIA (2026-11-12): the settled-radius window with the forest graded at flux level

Committed alone, before any script of this lane exists and before any flux number at any f has been computed.
TEST lane: adopts nothing, relabels nothing (SRH1, FZS1, FRZ3, FRZ3R keep their labels), registers nothing. Footings
(canonical a0 = 9.3603e-11 m/s^2, alt a0 = 1.1312e-10 m/s^2) graded separately, never pooled. Cold dark energy is a
gravitating field component; no particle is added. kappa = 1/2 is FITTED. **The settled-radius family is post hoc**: it
was chosen after FRZ1 failed. A window found here is a hit that awaits an independent blind re-grade, not a pass of form B.

## 1. Question

SRH1 laid the law's layout only inside R_set = f x R_fold(z, M_b) (FLD1), with the cold reference's layout outside and the
reference's enclosed cold mass at R_set (FZS1's junction). Graded at MATTER level through the record's projection, the
forest (G1) allowed f <= 0.722 / 0.725 and KiDS lensing (G4) wanted f >= 1.004 / 1.050: WINDOW EMPTY. Here G1 is graded at
FLUX level. **Does a single constant f pass G1 (flux level) together with SRH1's G2, G3 and G4 as committed, and is f = 1
inside?** Only G1 is computed anew. G2, G3, G4 are taken from SRH1's committed `srh1_grade.json` / `.out` unchanged:
G2 lower edge 0.391 / 0.391 (f 0.30, 0.35 fail on the grid); G3 holds at every f; G4 FAIL at every grid f <= 1.00 and PASS
at every grid f >= 1.25, interpolated lower edge 1.004 / 1.050 (SRH1's linear interpolation of the early-type z = 2 line).

## 2. The layout (reused, not changed)

SRH1's `srh1_hm.py` is executed read-only up to its `# ---... checkpointed run` marker (this executes FRZ1's `frz1_hm.py`
prefix and reads FLD1's run files). Its `lay_S(foot, z, fac)` gives the settled profile M_S(r) of every halo; mode "Rb"
gives the reference profile; `fac = inf` gives FRZ1's form-B profile to r_ta (SRH1's KA-T). Nothing in that code is edited.

## 3. The flux build (FRZ3R's reading T, reused, one change)

FRZ3R's `frz3r_core.py` is imported read-only (grid, lognormal smooth component, Poisson halo painting on 0.1 dex bins,
gas smoothing, FGPA with thermal broadening in 12 classes, saturation, mean-flux matching by tuning A, 1D flux power).
Box 20 Mpc/h, N 384, z bins 2.2 to 4.4 (DESI DR1's 12), gamma 1.5 (beta 1.65), T0 1e4 K, mean flux tau_eff(z) =
0.751 ((1+z)/4.5)^2.90 - 0.132 (FRZ3R's, PROVISIONAL), pressure-smoothing scale **lambda_P = 79 comoving kpc**
(Kulkarni et al. 2015, as FRZ3R; PROVISIONAL web read), held in comoving units. Reference field R = FRZ3R's reading T
reference (haloes painted with U_Rb at Poisson positions, smooth lognormal with target P_Rb,ta - one-halo(U_Rb)).
Form-B field at f: B_f = R + (sum over haloes of U_S(f) - U_Rb) + f_s delta_s (sqrt(1 + D2h_f / S) - 1), where D2h_f is the
two-halo difference P_lin (I_S(f)^2 - I_Rb^2) of FRZ1's turnaround-scope halo model (whole mass grid) and S FRZ3R's smooth
target. This is FRZ3R's reading T with U_B replaced by U_S(f). Same positions, same smooth field, for every f.

**The one change: rare haloes (stratified one-halo estimator).** FZS1 found the settled layout's change at z 2.2 is carried
by cluster-regime haloes (about 1e13 Msun/h and up); a 20 Mpc/h box holds well under one of them at z 2.2, so a plain
Poisson box would realise almost none of the change and show a spurious window. Therefore:
- A mass bin is **common** if its expected count in the box E_b = W_b V >= 30, **rare** otherwise (frozen threshold).
- **Base box:** every bin is painted at its Poisson positions in R and B (as FRZ3R); the difference U_S - U_Rb is painted
  only on common-bin haloes; rare-bin Poisson haloes carry U_Rb in both fields. The two-halo term is realised in full.
- **Forced boxes:** rare bins are grouped into contiguous 0.5 dex groups g (log M edges 8.0 + 0.5 j). For each group with
  E_g = sum E_b > 0, n_g = 12 extra haloes are drawn from the group's bins with probability proportional to E_b (own random
  stream per z, seed, group), placed uniformly, and added to the base catalogue (painted U_Rb in R_g, U_S(f) in B_g; f_s
  recomputed from the painted mass). Only the forced haloes carry the difference; no two-halo term is added.
- Estimator, per f, for any power spectrum X (1D flux or 3D matter): Delta X(f) = [X(B_base) - X(R_base)] +
  sum_g (E_g / n_g) [X(B_g) - X(R_g)]; ratio R_X(f) = 1 + Delta X(f) / X(R_base). Each field's mean flux is matched to the
  target separately.
- **Poisson-only reading** (FRZ3R's method, every halo's difference at its Poisson position; reported, not graded) at f =
  1.00, 1.25, 2.00 and inf.

## 4. Grid, seeds, statistic, gate

- **f grid (primary, all 12 bins):** 0.30, 0.50, 0.70, 0.80, 0.90, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 2.00, 3.00, inf;
  plus f = 0 at the anchor bins (known answer a) and MU2 (R_set doubled at f = 1) at the anchors. SRH1's 0.35, 0.40, 0.45,
  0.55, 0.60, 0.65, 0.75 are left out of the flux run for compute (SRH1 already has them at matter level below its own
  edge); the halo-model numbers (matter level, record convention and turnaround scope) are computed at every SRH1 grid f
  plus the points above.
- **Seeds:** anchors z 2.2, 3.0, 4.4 seeds 0 and 1; the other nine bins seed 0. Ratios are seed means per bin.
- **Statistic (as FRZ3R applied the gate):** the flux ratio R_F(k_v, z) multiplies DESI DR1's P1D at its 755 points
  (shared `ss1_cosmo.forest_setup`, md5 33d7fc21...), Delta chi^2 = d^T C^-1 d with d = (R_F - 1) P_D and the full
  covariance. **Gate: Delta chi^2 <= 4.** Matter level: the record's projection (`forest_eval` with sqrt(R) of the 3D ratio,
  FRZ3R's `amp`) of the realised 3D ratio, k <= 10 h/Mpc.
- **G1 upper edge f_max:** the smallest f at which the grid's flux Delta chi^2 first exceeds 4, interpolated linearly in
  log Delta chi^2 against f from the grid point below; if no grid f <= 3.00 exceeds 4, f_max >= 3.00 (grid end) and the
  f = inf value is reported. If Delta chi^2 is not monotone in f, every crossing is reported and the window uses the
  first.

## 5. Labels (per footing)

f_lo = max(G2 edge 0.391, G4 edge 1.004 canonical / 1.050 alt); f_hi = f_max (flux level). G3 holds everywhere.
- **WINDOW OPENS AT FLUX LEVEL [f_lo, f_hi]**, "f = 1 INSIDE" if f_lo <= 1 <= f_hi, else "f = 1 OUTSIDE", with FRAGILE if
  section 8 says so, with MARGINAL if f_hi - f_lo < 2 x SE(f_hi) (section 6e). A hit awaiting an independent blind re-grade;
  not a pass of form B.
- **WINDOW EMPTY AT FLUX LEVEL**: f_hi <= f_lo; the gap f_lo / f_hi is given.
- **NO VERDICT**: a known answer (a) to (e) fails, or a mutation does not bite.
Reported beside the label, ungraded: f_max on its own; the window with SRH1R's blind finding (lensing as graded cannot see
f, so f_lo = 0.391); flux and matter Delta chi^2 at every f and their ratio; the record-convention matter Delta chi^2
(SRH1's numbers); the Poisson-only reading; one plain sentence on what a window would mean.

## 6. Known answers (all must pass or the label is NO VERDICT)

- (a) f = 0: U_S = U_Rb and D2h = 0 exactly; at the anchors the B flux power equals R's element by element (exact).
- (b) f = inf, Poisson-only path: per part (z, seed, footing) the R and B flux power equal FRZ3R's `turn_*` parts within
  1e-4 relative at every k_v (same code, same seeds); its 12-bin flux and matter Delta chi^2 equal FRZ3R's recomputed on
  the same seed subset within 1 %.
- (c0) halo-model chain: my record-convention R_cold(f) (FRZ1's convention, from my KT-grid spectra interpolated to FRZ1's
  KK) equals SRH1's stored R_cold within 1e-4 absolute at every z and k in [0.3, 10] h/Mpc, at every SRH1 grid f, and its
  forest Delta chi^2 equals SRH1's within 1 % (f = 1 gives 38.7 / 36.7 = FZS1).
- (c1) realisation: the stratified realised matter-level Delta chi^2 D_mat(f) against the halo model's own
  turnaround-scope expectation D_ta(f) (ratio P_S,ta / P_Rb,ta through the same projection) within a factor 0.67 to 1.5 at
  f = 1.00, 1.30 and 2.00, on both footings (where D_ta < 1 both, the check reads |D_mat - D_ta| <= 1). The fraction of the
  record-convention change carried, q(f) = D_mat / D_rec, is reported at every f: the turnaround-scope convention is
  expected to carry about half (FRZ3R: 0.51 at f = inf); it is handled by bracket B-conv (section 8), not by rescaling the
  primary.
- (d) every field's mean flux equals the target within 1e-4.
- (e) scatter at the edge: at the grid f nearest f_max, the anchor-bin Delta chi^2 of the half seed difference
  (R_s0 - R_s1) / 2, scaled to 12 bins by Delta chi^2(12) / Delta chi^2(anchors), is <= 1.0; SE(f_max) = that noise
  carried through the local slope, reported.

## 7. Mutations (separate `*_MUTATE*` outputs; must bite)

- M1 saturation removed (F = 1 - A tau, linear), anchors seed 0, at f = 1.00, 1.30, 2.00: the anchor Delta chi^2 must
  change by at least x 1.25 at f = 1.30.
- M2 R_set doubled at f = 1 (independent switch in the profile builder): anchor Delta chi^2 at least x 2 that of f = 1;
  reported against the f = 2.00 grid row (should be equal).

## 8. Brackets (frozen; anchors, seed 0, f = 1.00, 1.30, 2.00; 12-bin estimate = primary 12-bin x bracket / primary
anchors at the same seed; f_max re-interpolated on those three points scaled)

lambda_P x 0.5, x 2, and 100 proper kpc; gamma 1.2 and 1.6; mean flux tau x 0.9 and x 1.1; clustered halo placement (FRZ3R's
clustered bracket, base box only); resolution N 256; B-conv: flux Delta chi^2 x D_rec(f) / D_mat(f) (the record's
convention). **FRAGILE** if any bracket moves f = 1 across the gate, or opens or closes the window (f_max crosses f_lo),
named in the label. Rare-bin threshold and n_g are not bracketed (compute); stated as left out.

## 9. Expectation and hand estimate (written before any number)

- From FRZ3R: flux/matter about 0.07 to 0.10 for the full layout, saturated gas does the softening. The settled change sits
  inside R_set of the most massive haloes (densest, most saturated gas), so I expect stronger softening: 0.02 to 0.07.
- Turnaround-scope matter change about half the record's: D_mat(1) about 19, D_mat(1.3) about 80, D_mat(2) about 230.
- Flux: Delta chi^2(1) about 0.4 to 1.4; (1.3) 1.6 to 6; (1.5) 3 to 10; (2.0) 5 to 16. Hand f_max about 1.3 (1.15 to 1.6).
- So I expect **WINDOW OPENS AT FLUX LEVEL, about [1.004, 1.3] / [1.05, 1.3], f = 1 OUTSIDE** (only because G4's
  interpolated edge is 1.004 on canonical; G4 fails at the grid point f = 1.00), likely FRAGILE through lambda_P x 0.5:
  55 %. NO VERDICT (the stratified estimator fails c1 or the scatter test): 25 %. WINDOW EMPTY: 20 %.
- With SRH1R's reading (f_lo = 0.391) f = 1 would be inside if f_max > 1.

## 10. Compute and conduct

One heavy job at a time, `nice -n 19`, at most 4 threads, peak memory under 20 GB, restartable part files, SIGTERM stops
between parts (exit 75). Halo-model tables are written as temporary npz files and deleted at the end. Stage order:
tables, primary anchors, primary other bins, brackets and mutations, clustered, resolution. Budget about five hours; if a
stage cannot finish, RESULT says which and the label carries "brackets incomplete". Paths relative to the scripts' folder.
Commits path-limited, not pushed. Later changes only as dated amendments committed alone; the as-frozen reading first.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
