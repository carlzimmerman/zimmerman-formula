# FRZ6R frozen criteria: blind, independent flux-level re-grade of the crossing-speed split

2026-11-13. Written and committed alone, before any script of this lane exists. TEST lane: adopts nothing, relabels nothing,
registers nothing. Footings (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2) are never pooled. Cold dark energy is a
gravitating field component; no particle is added. kappa = 1/2 and X = 5.41 are FITTED. Nothing here says the data favour the
framework.

## 0. Blindness

I have opened only: the lead's BRIEF.md; JNT2's `jnt2_common.py` and `jnt2_hm.py` (scripts); the `membership` block of
JNT2's `jnt2_hm.json` (n_above per z and footing, read by a one-line extractor that printed nothing else); FRZ1's
`frz1_hm.py`; the prefix of FZS1's `fzs1_hm.py` (diffed against SRH1's) and SRH1's `srh1_hm.py`; the CFG556 halo-model library
prefix; `ss1_cosmo.forest_setup` / `forest_eval`; FRZ3R's `RESULT_BLIND.md`, `AMENDMENT_A1`, `frz3r_core.py`,
`frz3r_run.py`, `frz3r_turn.py`, `frz3r_grade_turn.py`, the head of `frz3r_grade.py` and its run log; the folder listing of
FLD1's `runs/`. No earlier flux-level answer on the settled or split layouts has been seen.

## 1. The question and the layouts

Per halo of FRZ1's mass grid (321 masses, 1e8 to 1e16 Msun/h, FRZ1's `set_z` population at each z):

- reference R: FRZ1 layout mode "Rb" (turnaround scope, mass M_ta inside r_ta).
- split J(f): if FRZ1's `v_vir(hb)` > v*(z) = v*(0) / E(z), v*(0) = a0 / (10 (1 + 5.41) H0), H0 = 67.4 km/s/Mpc,
  E(z) = sqrt(0.3153 (1+z)^3 + 0.6847) (the split's own constants, JNT2 `jnt2_common.py`): the reference layout at every
  radius. Otherwise FZS1's settled layout with R_set = f x R_fold (FZS1's `rset_com`, capped at r_ta): the law's cold
  component (mode "B" minus the baryons `Bar`) rescaled by s = C_R(R_set) / C_B(R_set) inside R_set, the reference beyond.
  Implemented by me from the definition (the record's `layout`, `Bar`, `rset_com`, `CUR` executed read-only from FZS1's
  prefix; the switch and the splice are my own lines).
- cases: f = 1.25, 2, 3 (graded); f = 0 (known answer); control C = mode "B" for every halo (the law's layout everywhere,
  f = inf, no boundary).
- twin TW1 ("boundary removed"): the settled layout at f = 2 for every halo (v* = inf).
- twin TW2 ("difference doubled"): field R + 2 (J(2) - R).

## 2. Halo-model tables (my own)

At each z and footing, on my table grid KT = {0} U geomspace(4e-3, 160, 720) h/Mpc, I compute with CFG556's `U_set` (FRZ1's
mass grid and weights) the profiles U_X(k) for X in {R, J0, J1.25, J2, J3, C, TW1}, and with `spectra_ta`:
P_X,ta = p1_X + P_lin I_X^2. Expected matter ratio E_X(k) = P_X,ta / P_R,ta. Two-halo change D2_X = P_lin (I_X^2 - I_R^2).

## 3. Realisation in boxes (my own)

- Box L = 20 Mpc/h, N = 384 (dx = 52.1 kpc/h comoving), real space, periodic. Two threads.
- Haloes: every grid mass with M >= 1e8 Msun/h. Masses grouped in painting bins of 0.125 dex; within a bin each grid mass gets
  its own Poisson count (mean W_M V); positions uniform. One deposit per bin with a triangular-shaped-cloud (TSC) kernel,
  deconvolved by the TSC window (clamped at 0.01); the bin's profile is the realised-count-weighted mean of its masses'
  U_X / (rho_m dx^3). The positions and counts are shared by all cases and both footings at the same (z, seed).
- Smooth component (the two-halo term; all grid masses are painted, so its target is S = P_R,ta - p1_painted,expected):
  lognormal with target power S / fs^2, fs = 1 - painted mass / box mass (expected value for the target, realised value for
  the weight). Gaussian power from xi_G = ln(1 + xi_T) on the grid. Case X: delta_X = halo part_X + fs delta_s
  sqrt(max(1 + D2_X / S, 0)) in k space. The reference uses the factor 1.
- Seeds: the white noise and the halo catalogue of (z bin index iz, seed s) come from numpy SeedSequence([6, 61, iz, s]) (two
  spawned streams). Cases and footings share them (paired).
- Gas: 1 + delta smoothed by exp(-0.5 (k lambda_P)^2), lambda_P = 79 comoving kpc = 0.0532 Mpc/h (h = 0.6736); pixels below
  1e-6 are floored to 1e-6 and the floored fraction is reported.
- Flux (FGPA, REUSED from FRZ3R `frz3r_core.py`: `tau_field`, `tune_A`, `p1d`, `dv_cell`, unchanged; worker count set to 2):
  tau proportional to rho^beta, beta = 2 - 0.7 (gamma - 1), gamma = 1.5, T0 = 1e4 K thermal broadening along axis 2, real space;
  amplitude tuned per field so <F> = exp(-tau_eff(z)), tau_eff = 0.751 ((1+z)/4.5)^2.90 - 0.132. P1D of F / <F> - 1 along
  axis 2, averaged over all N^2 skewers.

## 4. Redshift bins and seeds

All 12 DESI bins z = 2.2, 2.4, ..., 4.4 are computed; none is filled. Seeds per bin: n = 4 (s = 0, 1, 2, 3), the same in every
bin. Reasoning: the jackknife below needs n >= 3; FRZ3R's paired seed scatter on the full layout was S_mean / E = 0.02 to 0.1
with 2 to 4 seeds, so the noise Delta chi^2 is expected near (S/E)^2 D, of order 0.01 D, well below the 0.1 floor of KA-S; four
seeds keep about a factor 3 margin for a split whose difference sits in rarer or noisier haloes. No optional stopping: the seed
count is not changed after any number is seen. Order (time budget about 10 h): stage S1 = seeds 0, 1, 2 in all bins (all cases,
anchor known answers and twins); stage S2 = seed 3 in all bins; stage S3 = brackets at the anchors (z 2.2, 3.0, 4.4), seeds 0, 1.
If the budget ends before S2 is complete, every case is graded with the seeds present in all 12 bins (n = 3) and this is named;
missing brackets are named.

## 5. Statistic D and SE (exact)

For case X, footing, bin z, seed s: P_X,s(k_v) and P_R,s(k_v) (primary flux P1D, same seed). Estimator (ratio of seed sums):
R^_z(k_v) = sum_s P_X,s / sum_s P_R,s. At each of the 755 DESI DR1 points (`ss1_cosmo.forest_setup`, executed read-only; md5
33d7fc21bfd3d745ed71a0bbe80ca433) r_i = R^_z interpolated linearly in ln k_v on the box modes k_v > 0; below the first mode,
the first mode's value. D = d^T C^-1 d, d_i = (r_i - 1) Pd_i, C the full covariance (the record's Cholesky factor, as the last
line of `forest_eval`). D is the 12-bin flux Delta chi^2.

SE (delete-one jackknife over the seed index): D_(j) = D with seed j removed in every bin (j = 0 .. n-1);
SE = sqrt((n-1)/n sum_j (D_(j) - mean_j D_(j))^2).

Anchor statistic A (used by twins and brackets): the same with only the points at z 2.2, 3.0, 4.4 and their joint covariance
block.

## 6. Known answers (all must pass for HOLDS)

- KA-0: f = 0 profile tables equal the reference bitwise at every z and footing; at the anchors, seed 0, the f = 0 field's flux
  P1D equals the reference's with |ratio - 1| <= 1e-6 at every mode.
- KA-C (control): the control's 12-bin D lies within +-35 % of FRZ3R's reading T (363.26 canonical / 424.50 alt), and the
  control FAILS by the rule of section 8 (D - 2 SE > 4).
- KA-N: the number of grid haloes above v*(z) (of 321) equals JNT2's membership n_above for every z and footing (exact).
  JNT2's counts: canonical 170 176 181 187 192 197 202 206 211 215 219 223; alt 160 166 172 177 182 187 192 196 201 205
  209 213 (z 2.2 to 4.4).
- KA-A (boxes wholly above v*): with v* set to 0 (every halo above), the split's profile tables equal the reference bitwise at
  every z and footing, and at z 3.0, seed 0 the flux P1D ratio is 1 within 1e-6.
- KA-F: |<F> - exp(-tau_eff(z))| <= 1e-4 for every flux field computed (primary, twins, brackets scaled by their own tau).
- KA-M (matter carried): at the anchors, the realised 3D matter ratio (ratio of seed sums of P3D, unsmoothed fields) at
  k = 1, 3, 5 h/Mpc is within 0.01 + 0.3 |E_X - 1| of the halo model's E_X, for each graded case and the control.
- KA-S (seed scatter), per case and footing: sigma_z(k_v) = jackknife standard error of R^_z(k_v)
  (sqrt((n-1)/n sum_j (R^_z,(j) - mean)^2)); e_i = sigma(k_i) Pd_i; D_noise = e^T C^-1 e. Pass if D_noise <= 0.1 max(D, 4).

## 7. Twins (must bite; anchors, all seeds, case f = 2)

- TW1 boundary removed: bites if |A_TW1 - A_J2| >= max(0.25 A_J2, 1.0).
- TW2 difference doubled: bites if A_TW2 / A_J2 >= 2.5 (linear response predicts 4).

## 8. Labels (per case f = 1.25, 2, 3 and footing; footings never pooled)

- FOREST ROW HOLDS AT FLUX LEVEL: every known answer passes (KA-S and KA-M for that case), both twins bite, and D + 2 SE < 4.
  A HOLDS is a hit, not a pass of the theory. Before writing HOLDS anywhere I re-check that both twins bite and the control
  fails.
- FOREST ROW FAILS AT FLUX LEVEL: D - 2 SE > 4.
- Otherwise NO VERDICT.
- FRAGILE (bracket named) is added when a frozen bracket's 12-bin estimate lies on the other side of 4 from D.
- A known-answer failure is named beside any label.

## 9. Brackets (frozen; anchors, seeds 0, 1; fields R, J1.25, J2, J3, C)

lambda_P x 0.5 and x 2; gamma 1.2 and 1.6 (beta and broadening follow); tau_eff x 0.9 and x 1.1. 12-bin estimate:
D_br = D x A_br / A_prim, with A on seeds 0, 1 only for both. Reported beside the label, never replacing it: a measured-range
reading with lambda_P = 91.4 and 138.6 comoving kpc (Rorai et al. 2017, Table S2, z = 3.0; PROVISIONAL, taken from the lead's
brief, not looked up), same scaling; the range of D over the two ends and the label the rule gives at each end.

## 10. Compute

One job, `nice -n 19`, 2 threads; restart if peak RSS > 16 GB (checked after each part, exit 75); one JSON part per
(stage, z, seed, footing); `run_all.sh` under nohup with `logs/run_all.pid` and `run_all.done`; disk >= 8 GB and swap
used <= 8 GB checked before each stage. Parts are small JSON (P1D and P3D arrays); no field array is kept.

## 11. Hand estimate (before any number)

The control should come out near FRZ3R's reading T, a few hundred. The split removes two pieces. (a) Haloes above v* keep the
reference: v*(z) falls from about 200 to about 95 km/s (canonical) between z 2.2 and 4.4, so haloes above about 8e11 Msun at
z 2.2 and about 4e10 Msun at z 4.4 are untouched; at high z most halo mass in forest-relevant haloes is reference. (b) Below v*,
the change is confined inside f R_fold (about 15 to 50 physical kpc, against r_ta about 60 to 150 kpc), so the outskirts beyond
R_set that drove the full-layout flux response are reference. Estimate (canonical; alt about 10 % higher): D(f = 3) 30 to 120,
D(f = 2) 10 to 60, D(f = 1.25) 2 to 25; SE about 10 to 25 % of D. Expected labels: f = 3 and f = 2 FAIL; f = 1.25 FAIL or
NO VERDICT. Low confidence: the response could be dominated by z 2.2 to 2.6 haloes just under v*, where it is least reduced.

## 12. Physics left out

Hydrodynamics (gas follows matter above lambda_P), shock heating, self-shielding, UV and temperature fluctuations, peculiar
velocities, halo clustering (positions uniform; the two-halo term is carried by the smooth component), haloes below 1e8 Msun/h,
modes below the box fundamental, form B's change of velocities.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
