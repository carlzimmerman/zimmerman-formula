# FRZ6 FROZEN CRITERIA (2026-11-13): the settled layout and the crossing-speed split graded at flux level

Committed alone, before any script of this lane exists and before any new number of this lane has been computed.
TEST lane: adopts nothing, relabels nothing (FRZ4, FRZ5, JNT2, JNT2R and every earlier lane keep their labels),
registers nothing. Footings (canonical a0 = 9.3603e-11 m/s^2, alt a0 = 1.1312e-10 m/s^2) are graded separately and never
pooled. Cold dark energy is a gravitating field component; no particle is added. kappa = 1/2 and the share 5.41 are
FITTED. The settled-radius family is post hoc (chosen after FRZ1 failed) and the crossing-speed split is post hoc to SRJ2
and JNT1. A HOLDS label is a hit that awaits an independent blind re-grade, not a pass of the theory. Nothing here can
say the data favour the framework.

## 1. Question and cases

FRZ4 (criteria 199d710a9a, result b23f8b4aec) graded the full layout (FAILS / FAILS, 269.1 / 288.4) but could not grade
the settled layout: its seed-scatter known answer (e) failed with two seeds at z 2.2 (ungraded 0.10 / 0.11, 0.50 / 0.41,
2.20 / 2.04 at f = 1, 2, 3). No lane has run the crossing-speed split at flux level. This lane grades, per footing:

- **(U) unsplit settled layout**, f = 1, 2, 3: the law's layout inside R_set = f x R_fold in every halo (SRH1's `lay_S`,
  exactly FRZ4's case B).
- **(S) the crossing-speed split**, f = 1.25, 2, 3: a halo with v_vir(hb) > v*(z) keeps the reference layout (FRZ1 mode
  "Rb") at every radius; every other halo gets SRH1's `lay_S` at f. v*(z) = v*(0) / E(z), v*(0) = a0 / (10 (1 + 5.41) H0)
  = 668.5 / 807.9 km/s.
- **Control (C)**, f = inf: the full layout (FRZ4's case A), run through the same seed test and brackets; its FRZ4 label
  FAILS must reproduce.

**Source of the split (copied, not re-derived):** `closure_2026_11_13/JNT2_crossing_speed_joint/jnt2_common.py` lines
11 to 23 (constants, E(z), `vstar0_kms`, `vstar_kms` mode "main") and `jnt2_hm.py` lines 29 to 45 (`above(hb, foot)` =
FRZ1's `v_vir(hb)` > `vstar_kms(foot, z)`, evaluated after `set_z(z)`; `lay_J`: reference layout when above, else the
settled layout, whose code is line for line SRH1's `lay_S` with default options). Membership is per halo of FRZ1's mass
grid at each redshift bin (the switch halo mass follows from v_vir = v*(z); JNT2 reports the lightest M200c above:
5.81e11 / 1.03e12 Msun/h at z 2.2, 1.66e11 / 2.94e11 at z 3.0, 2.80e10 / 4.98e10 at z 4.4). The painted 0.1 dex bin
profile of the split is the count-weighted mean over the bin's grid haloes (FRZ4's `binmean`), so a bin that straddles
v*(z) carries the change of its below-v* haloes only.

## 2. Build (FRZ4's, unchanged except the added fields)

- Tables: FRZ4's `frz4_tables.py` copied with three added table keys S1.25, S2.00, S3.00 built from the split above.
  The U and f = inf keys and every other array are FRZ4's code unchanged.
- Fields: FRZ4's `frz4_run.py` copied (FRZ3R's `frz3r_core.py` imported read-only; FGPA, saturation, mean-flux match,
  P1D, P3D; box 20 Mpc/h, N 384, real space). Forced set, stratified base box, forced boxes and estimator exactly as
  FRZ4 section 3. **The forced set and the bracket subset for U and C are FRZ4's rule over the U and C cases only**, so
  every FRZ4 part is reproduced; the S fields are added to the same boxes. The share of each S case carried by
  non-forced rare bins is reported.
- Gas physics and brackets as FRZ4 froze them: T0 1e4 K, gamma 1.5, tau_eff(z) = 0.751 ((1+z)/4.5)^2.90 - 0.132,
  lambda_P = 79 comoving kpc (all PROVISIONAL, inherited).
- **Reuse of FRZ4's parts.** FRZ4's primary parts (z 2.2 seeds 0 and 1; seed 0 at z 2.6, 3.0, 3.4, 3.8, 4.4) and
  bracket and clustered parts supply the U and C fields at those (z, seed). This lane's new parts at the same (z, seed)
  carry the R field and the S fields; FRZ4's U fields are merged in only after **known answer (i)** passes for that part.

## 3. Seeds (frozen; no optional stopping)

- **z 2.2: 12 seeds (0 to 11), both footings**, every case (U, S, C) in every seed. Seeds 0 and 1 reuse FRZ4 for U and C.
  Why 12: FRZ4's 2-seed noise N12 must fall by about 3x (f = 2, 3) to 9x (alt f = 1) for (e) to pass; the noise of the
  seed mean falls as 1/n; 12 seeds give 6x against 2. More seeds do not fit the budget (one new seed part with eight
  fields costs about 15 min per footing).
- **z 2.6, 3.0, 3.4, 3.8, 4.4: seed 0 only** (FRZ4's for U and C; new parts for S). The six other DESI bins are estimated
  by linear interpolation in z as FRZ4 (section 4 there). The z 2.2 bin is the seed mean of 12 seeds; the others are
  single seeds; this is a stated limit, carried into the label only through (e)'s scaling (below).
- If the run cannot reach 12 seeds at z 2.2 on a footing, every case on that footing is **NO VERDICT (seed count not
  reached)**; what was reached is reported, ungraded.

## 4. Statistic and gate

As FRZ4 section 5: flux ratio R_F at DESI DR1's 755 points, Delta chi^2 = d^T C^-1 d, d = (R_F - 1) P_D, full covariance,
via `ss1_cosmo.forest_setup / forest_eval` (FRZ3R's grading set-up executed read-only). **Gate: Delta chi^2 <= 4.**
D = the 12-bin flux Delta chi^2 of the case (z 2.2 = 12-seed mean ratio). Matter level of the same fields as FRZ4.

## 5. Known answers (every one that applies must pass, or that case and footing is NO VERDICT)

- **(a)** f = 0 equals the reference: in every box at z 2.2, 3.0, 4.4 seed 0 (FRZ4's parts and this lane's new parts),
  max over k_v of |P_F(B_f0) / P_F(R) - 1| <= 1e-12, and the stratified Delta chi^2 at f = 0 <= 1e-12. All cases.
- **(b)** FRZ4's Poisson-only known answer, inherited on FRZ4's parts (re-evaluated, must PASS). All cases.
- **(c0)** record-convention D_rec through the same chain: U and C as FRZ4 (SRH1 / FZS1 / FRZ1 / SRF1 within 1 %);
  **S: D_rec equals JNT2's stored G1 matter-level Delta chi^2 (`jnt2_forest_<footing>.json`, cases f1.25, f2.00, f3.00:
  0.0008 / 0.0492 / 1.9898 canonical, 0.0050 / 0.1456 / 6.4321 alt) within 1 % or 0.002 absolute.** Per case.
- **(c1)** realised matter-level Delta chi^2 against the halo model's D_ta, as FRZ4 (ratio 0.67 to 1.5; per computed bin
  with halo-model single-bin value >= 1, ratio 0.5 to 2). **Generalisation for a tiny change (stated now): when D_ta < 1
  the ratio test is replaced by D_mat <= 1** (the realised field may not create a matter-level change the halo model
  lacks); the per-bin rule is unchanged. Per case.
- **(d)** every field's mean flux equals the target within 1e-4.
- **(e) seed scatter, generalised to n seeds.** At z 2.2 with n seeds, per case: R_s the stratified ratio of seed s, R̄
  their mean. N22 = [1 / (n (n - 1))] x sum_s Delta chi^2_22(R_s - R̄), where Delta chi^2_22(x) is the full-covariance
  Delta chi^2 of the ratio 1 + x at the z 2.2 bin's points (all other points at 1). This is the expected Delta chi^2 of
  the standard error of the seed-mean ratio; at n = 2 it equals FRZ4's half-difference statistic exactly.
  D22 = Delta chi^2_22(R̄ - 1). Scaled to 12 bins as FRZ4: **N12 = D x N22 / D22. Pass if N12 <= 0.1 D or N12 <= 0.05**
  (FRZ4's rule). Graded at n = 12.
  **Seed standard error of D: SE = 2 sqrt(D N12) + N12** (FRZ4's form).
- **(f) split identity.** In every S field of every forced box whose 0.1 dex bin lies wholly above v*(z) (every grid
  halo of the bin above), B|S equals R to 1e-12 relative at every k_v; and the number of FRZ1 grid haloes above v*(z) at
  z 2.2, 3.0, 4.4 equals JNT2's `jnt2_hm.json` membership (170 / 192 / 223 canonical, 160 / 182 / 213 alt). S cases only.
- **(i) identity with FRZ4.** In every new part at a (z, seed, stage) that FRZ4 also computed, the R field of the base box
  and of every forced box equals FRZ4's to 1e-12 relative at every k_v (P1D and P3D), for every spec both computed.
  In addition **one whole part is reproduced**: z 2.2 seed 1 canonical is run with the U and C fields too, and every U
  and C field of every box must equal FRZ4's to 1e-12 relative. A failure voids the reuse: U and C are then NO VERDICT
  on that footing.

## 6. Twins (separate `*_MUTATE*` outputs; graded at the same 12 seeds at z 2.2; must bite, per case, or NO VERDICT)

- **T1, layout change doubled in the base box.** In every z 2.2 seed the base box's B - R is doubled in density
  (forced boxes unchanged). Bites if the 12-seed z 2.2 single-bin Delta chi^2 is >= 1.5 x the primary's. (The base box is
  where FRZ4 found the settled flux change and the seed noise.)
- **T2, saturation removed in the base box** (F = 1 - A tau, mean flux matched linearly; FRZ4's M1 applied to the base
  box's R and B). Bites if the 12-seed z 2.2 base-box-only Delta chi^2 changes by a factor >= 1.25 or <= 0.8 against
  the primary's base-box-only value.
- Reported, not graded: FRZ4's M1 (bracket subset) and M2 (all boxes, seed 0) on FRZ4's parts for U and C; M1 on this
  lane's S bracket subset.

## 7. Brackets (seed 0, as FRZ4; label FRAGILE if any 12-bin estimate lies on the other side of 4 from D)

FRZ4's eight, unchanged: lambda_P x 0.5, x 2, 100 proper kpc; gamma 1.2, 1.6; tau_eff x 0.9, x 1.1; clustered placement.
12-bin estimate = D x (bracket / primary) on the bracket subset at z 2.2 + 3.0 (z 2.2 alone for clustered), seed 0.
U and C use FRZ4's bracket parts and subset (FRZ4's numbers re-scaled to this lane's D). **S uses its own subset:**
FRZ4's forced bins by descending max share of the S cases' change, until the cumulative share >= 0.8 at every S case,
at most 10 bins (FRZ4's rule with the S cases in place of U); the base box is always included.

## 8. Labels (per case, per footing)

- **NO VERDICT** if: a known answer that applies fails; a twin does not bite; 12 seeds at z 2.2 not reached; or
  |D - 4| <= 2 SE (unresolved at 12 seeds).
- **FOREST ROW HOLDS AT FLUX LEVEL** if every known answer passes, both twins bite and **D + 2 SE < 4**. Written as a hit
  that awaits an independent blind re-grade, not a pass of the theory.
- **FOREST ROW FAILS AT FLUX LEVEL** if every known answer passes, both twins bite and **D - 2 SE > 4**.
- **FRAGILE** added when a frozen bracket's estimate crosses the gate (section 7), naming it; "[brackets incomplete]"
  if any bracket part is missing.
- Before HOLDS is written anywhere: re-check twins at 12 seeds and that the control (f = inf) still FAILS.

## 9. Reported beside each label (never replacing it)

- **(i) FRZ5 refit reading:** FRZ5's primary refit (`frz5_refit.py` up to its "reading G" marker, executed read-only:
  P1D3's per-bin amplitude, tilt and smoothing template, profiled Asimov Delta chi^2) applied to this lane's 755-point
  ratio of each case. It is a template, not a physical gas model.
- **(ii) measured-range reading:** the lambda_P brackets (x 0.5, x 2, 100 proper kpc) replaced by the published measured
  range at z = 3: **Rorai et al. 2017 (Science 356, 418; arXiv 1704.08366), Table S2, z = 3.0: lambda_P = 113.8
  (+23.9 / -21.4) comoving kpc, systematics-corrected 16 to 84 % range 91.4 to 138.6 comoving kpc** (PROVISIONAL: read
  from the paper's web text, not downloaded; their lambda_P is defined through their simulations' gas smoothing and may
  not equal FRZ3R's Gaussian filter scale one for one). Two new bracket specs lambda_P = 91.4 and 138.6 comoving kpc
  (plus 113.8 for U and C, reported) at z 2.2 and 3.0 on the same subsets; the label word under this reading uses these
  two plus gamma, tau_eff and clustered unchanged. Note: the primary 79 comoving kpc lies below this range.
- Flux and matter Delta chi^2, D_ta, D_rec, per-bin values, R_F at k_v 0.003 / 0.005 / 0.01 / 0.02 / 0.03 s/km, N12, SE,
  the single-seed z 2.2 values of every seed, U minus S at f = 2 and 3.

## 10. Compute

One heavy job at a time, `nice -n 19`, 2 flux threads; a process exits (code 76) and is restarted when its peak resident
memory passes 16 GB; part files per box (restartable); runner under nohup with a done marker. Free disk checked before
each stage (stop below 8 GB) and swap (stop above 8 GB used). Stage order: tables; z 2.2 seeds 0 and 1 (S parts, seed 1
canonical whole); z 2.2 seeds 2 to 11 alternating footings; S parts at 3.0, 4.4, 2.6, 3.4, 3.8; S brackets z 2.2;
S clustered z 2.2; S brackets z 3.0; measured-range U and C brackets z 2.2 and 3.0. Budget about 10 h wall from 12:30
EST; if it runs out, grade what this section allows and name what is missing. Tables and base-box arrays are deleted at
the end; parts committed (target under 60 MB).

## 11. Hand estimate (before any number)

- C, f = inf: D about 270 / 290, SE about 50; **FAILS / FAILS** reproduces (90 %).
- U: seed-mean D about 0.1 / 0.1, 0.4 / 0.4, 1.5 to 2.5 / 1.5 to 2.5 at f = 1, 2, 3. (e) passes at f = 2, 3 (70 %), at
  f = 1 canonical 60 %, alt 40 %. f = 3: SE about 1, so D + 2 SE near or above 4: NO VERDICT (unresolved) 50 %, HOLDS 40 %.
  HOLDS at f = 1, 2 where (e) passes; FRAGILE through lambda_P x 0.5 almost surely (FRZ4: 7 to 25).
- S: the change sits below v*(z) (M200c below about 6e11 to 1e12 Msun/h at z 2.2), which FRZ4 found carries nearly all
  the settled flux change, so S is close to U: about 0.05 to 0.15 (f = 1.25), 0.3 to 0.5 (f = 2), 1 to 2 (f = 3).
  Expect HOLDS, FRAGILE (lambda_P x 0.5) at f = 1.25 and 2; f = 3 as U. Under the measured-range reading FRAGILE from
  lambda_P goes away (larger smoothing lowers D). FRZ5 refit lowers each by 1.2 to 3x.
- Probability that at least one settled or split case on a footing is graded HOLDS: 65 %.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
