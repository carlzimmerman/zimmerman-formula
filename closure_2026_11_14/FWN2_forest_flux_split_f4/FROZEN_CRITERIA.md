# FWN2 FROZEN CRITERIA (2026-11-14, written about 09:40 EST): the crossing-speed split at f = 4, at flux level, in both builds

Committed alone, before any script of this lane exists and before any new number of this lane has been computed.
TEST lane, NOT blind: adopts nothing, relabels nothing (FRZ6, FRZ6R, FWN1, FWN1R and every earlier lane keep their labels),
registers nothing. Footings (canonical a0 = 9.3603e-11 m/s^2, alt a0 = 1.1312e-10 m/s^2) are graded separately and never
pooled. Cold dark energy is a gravitating field component; no particle is added. kappa = 1/2 and the share 5.41 are FITTED.
The settled-radius family is post hoc (added after FRZ1 failed at matter level); f is a free constant; the crossing-speed
boundary is post hoc to SRJ2 and JNT1; rule 6 is a candidate, NOT ADOPTED. A HOLDS label is a hit that awaits an
independent blind re-grade, not a pass of the theory. Nothing here can say the data favour the framework.

## 0. What is known at the freeze (this lane is not blind)

The two builds' neighbouring points, read from their committed grade files:

| build | f = 3: D (SE) canonical / alt | f = 5: D (SE) canonical / alt | f = 5 label |
|---|---|---|---|
| A = FWN1's build (FRZ6's; SE = 2 sqrt(D N12) + N12, 12 seeds at z 2.2) | 1.144 (0.449) / 1.434 (0.532) | 8.085 (2.414) / 9.448 (2.790) | NO VERDICT (unresolved) |
| B = FWN1R's build (FRZ6R's, written blind; jackknife SE, 4 seeds in all 12 bins) | 0.572 (0.044) / 0.690 (0.047) | 8.834 (0.333) / 10.897 (0.564) | FAILS, FRAGILE |

f = 4 was run in neither build; FWN1 and FWN1R interpolated the ceiling (D + 2 SE = 4) at 3.6 / 3.4 and 4.24 / 4.07.
Both builds' scripts exist and are frozen in their folders; this lane copies them and changes the case list only. Their
files and parts are never edited.

## 1. Question and cases

Does the forest row hold or fail at flux level for the crossing-speed split with R_set = 4 R_fold? Per footing:

- **Build A, case S4:** FWN1's split (FRZ6's `lay_split`: reference layout "Rb" at every radius for a halo with FRZ1's
  v_vir > v*(z); SRH1's `lay_S` at f = 4 otherwise, R_set = min(4 R_fold, r_ta)). Control S5 (f = 5) at z 2.2, seeds 0 and 1.
- **Build B, cases J3.5, J4, J4.5:** FWN1R's `split_fn` at f = 3.5, 4, 4.5 (v*(z) as FWN1R; slower haloes carry the settled
  layout inside R_set = f R_fold, FZS1's `rset_com`, capped at r_ta). Control J5 (f = 5) in every part. Reported field U4:
  the same settled layout at f = 4 in EVERY halo (boundary removed; `split_fn` with v* = infinity).
  J3.5 and J4.5 are added in build B only, because a field there costs seconds; in build A each extra f costs about two
  hours, and its SE (section 0) is too large to separate half steps.

v*(0) = a0 / (10 (1 + 5.41) H0) = 668.5 / 807.9 km/s, v*(z) = v*(0) / E(z), copied through the two builds' own code.

## 2. Build A (copies of FWN1's files in this folder; `fwn2a_*`)

- Tables: `fwn1_tables.py` copied with the split keys S4.00 and S5.00 (control). U and C keys unchanged, so the forced set
  (FRZ4's rule) and the base box are FWN1's.
- Fields: `fwn1_run.py` copied (box 20 Mpc/h, N 384, real space, FGPA, saturation, mean-flux match, forced rare bins in
  their own boxes, stratified estimator; T0 1e4 K, gamma 1.5, tau_eff(z) = 0.751 ((1+z)/4.5)^2.90 - 0.132, lambda_P 79
  comoving kpc; all PROVISIONAL, inherited). Field plan:
  1. **stage f4**, z 2.2, seeds 0 to 11, footings alternating: base box R, B|S4.00, D2|S4.00 (primary) and R, B|S4.00
     (M1_lin); every forced box B|S4.00, D2|S4.00; seeds 0 and 1 also B|S5.00 everywhere. The reference field R of every
     forced box is taken from FWN1's committed pass-1 ("inf") part of the same seed and footing, after this lane's base-box
     R is shown equal to that part's base-box R (known answer i).
  2. **stage oz**, seed 0 at z 3.0, 4.4, 2.6, 3.4, 3.8: R and B|S4.00 in the base box and every forced box. The six other
     DESI bins are interpolated linearly in z (FRZ4 section 4).
  3. **brackets**, seed 0: FWN1's ten specs (lambda_P x 0.5, x 2, 100 proper kpc; gamma 1.2, 1.6; tau_eff x 0.9, x 1.1;
     M1_lin; the two measured-range specs 91.4 and 138.6 comoving kpc) at z 2.2 and 3.0, and clustered placement at z 2.2,
     fields R and B|S4.00, on the bracket subset (FRZ4's rule with S4.00 as the only new case).
- Statistic, gate and SE exactly as FWN1 section 4: D = 12-bin flux Delta chi^2 on DESI DR1 P1D (755 points, full
  covariance, `ss1_cosmo.forest_setup / forest_eval` through FRZ3R's set-up); gate Delta chi^2 <= 4;
  SE = 2 sqrt(D N12) + N12 from the 12 seeds at z 2.2. No optional stopping: 12 seeds, or NO VERDICT (seed count).
- Known answers (each that applies must pass, or S4 on that footing is NO VERDICT). FWN1's letters are kept:
  - (a) f = 0 equals the reference and (b) FRZ4's Poisson-only answer: re-evaluated by this lane's grader on FWN1's and
    FRZ4's committed parts (not recomputed); must pass as they did.
  - (c0) record-convention D_rec of S4.00 through this lane's tables equals JNT2's chain (`ratios_J` at fac = 4, graded by
    JNT2's forest route) within 1 % or 0.002; the chain's fac = 3 must equal JNT2's stored value within 1 %.
  - (c1) realised matter-level Delta chi^2 against the halo model's D_ta, FWN1's rule.
  - (d) every field's mean flux within 1e-4 of the target. (e) N12 <= 0.1 D or N12 <= 0.05 at 12 seeds.
  - (f) split identity in every forced box wholly above v*(z) (B = R to 1e-12); membership counts equal JNT2's.
  - (i) identity with FWN1: this lane's base-box R (primary and M1_lin, every z 2.2 seed) equals FWN1's pass-1 base-box R,
    and the R of every box of every oz part equals FWN1's oz part, to 1e-12 relative (P1D) and 1e-6 (P3D); bracket parts
    the same on boxes and specs in common with FWN1's bracket parts.
  - (j1) control S5: at z 2.2 seeds 0 and 1, this lane's B|S5.00 equals FWN1's in the base box and every forced box to
    1e-12 (P1D) and 1e-6 (P3D).
  - (j2) control C from FRZ6's parts keeps FRZ6's D and SE to 1e-6 and still fails (D - 2 SE > 4).
  - (j3) grader identity: this lane's grader, run on FWN1's committed parts, gives FWN1's stored S5.00 flux D and SE
    (`fwn1_grade_<footing>.json`) within 1e-6 relative.
- Twins (12 seeds at z 2.2; must bite or NO VERDICT), FWN1's: **T1** the layout change doubled in every box (D2| fields),
  bites if the z 2.2 single-bin Delta chi^2 is >= 1.5 x the primary's; **T2** saturation removed in the base box (M1_lin),
  bites if the base-box-only Delta chi^2 changes by a factor >= 1.25 or <= 0.8.
- Brackets and FRAGILE as FWN1 section 7 (12-bin estimate = D x bracket / primary on the subset at z 2.2 + 3.0, seed 0;
  clustered at z 2.2). Measured-range reading (reported beside the label, never the label): the three lambda_P brackets
  replaced by 91.4 and 138.6 comoving kpc (Rorai et al. 2017, Table S2, z 3.0; PROVISIONAL).
- Label for S4 per footing, FWN1 section 8: NO VERDICT (cause named) / FOREST ROW HOLDS AT FLUX LEVEL (every known answer
  passes, both twins bite, D + 2 SE < 4, control C still fails) / FOREST ROW FAILS AT FLUX LEVEL (D - 2 SE > 4, known
  answers pass, twins bite) / FRAGILE (bracket named).
- Not done here: FRZ5's refit reading (FWN1 reported it; it is not a label).

## 3. Build B (FWN1R's library imported read-only from its folder; runner and grader copied as `fwn2b_*`)

- Unchanged from FWN1R section 2: tables, box (20 Mpc/h, N 384), halo realisation, lognormal two-halo component, seed
  streams (SeedSequence([6, 61, iz, s])), gas, FGPA step, forest data, estimator (ratio of seed sums), D, the jackknife SE
  over the seed index, the anchor statistic A (z 2.2, 3.0, 4.4), **4 seeds (0 to 3) in all 12 bins**, no optional stopping.
- Fields per primary part: R, J5, J3.5, J4, J4.5, U4; at the anchors also TWB4 = R + 2 (J4 - R). C, J3, J10 and Jinf are
  not recomputed. Brackets (anchors, seeds 0 and 1): R, J3.5, J4, J4.5 under lambda_P x 0.5 and x 2, gamma 1.2 and 1.6,
  tau_eff x 0.9 and x 1.1, and the measured-range pair 91.4 and 138.6 comoving kpc.
- Known answers (all must pass for HOLDS; FWN1R's names):
  - KA-5 (in place of KA-3): the recomputed R and J5 flux P1D equal FWN1R's stored primary parts with |ratio - 1| <= 1e-6
    at every mode k_v > 0 in all 96 files, and J5's D and SE from this lane's parts equal FWN1R's stored values within 1e-6
    relative and J5 still reads D - 2 SE > 4.
  - KA-C and KA-INF: not recomputed; read from FWN1R's committed `fwn1r_grade.json` and must be passes there.
  - KA-N (membership counts equal JNT2's), KA-F (mean flux within 1e-4), KA-M per case (realised matter ratio at k 1, 3, 5
    h/Mpc at the anchors within 0.01 + 0.3 |E - 1| of the halo model's E), KA-S per case (D_noise <= 0.1 max(D, 4)).
- Twins: **TW-A** (boundary removed at f = infinity, FWN1R's own): not recomputed; read from FWN1R's committed grade file,
  where it must read "bites". **TW-B4** (difference doubled at f = 4, the graded f): anchor statistic of TWB4 against J4's,
  bites if the factor is >= 2.5 (linear response predicts 4). It gates all three cases J3.5, J4, J4.5.
- **Reported, not a gate (decided now, with the reason):** the boundary-removed twin at f = 4, D(U4) against D(J4), with
  FWN1R's TW-A bite rule evaluated on it (ratio >= 1.25 or <= 0.8, and |difference| > 2 sqrt(SE^2 + SE^2)). It tests whether
  the boundary does work at f = 4, which is a different question from whether the build would see a fail-sized change; the
  second is what a HOLDS needs, and it is tested by TW-B4 and by the control J5 failing in the same parts. FRZ6R's
  boundary-removed twin did not bite at f = 2 and 3; whether it bites at f = 4 is reported either way.
- Brackets and FRAGILE as FWN1R section 6 (12-bin estimate D x A_br / A_prim on seeds 0 and 1; six frozen brackets); the
  measured-range reading reported beside the label. Grid resolution as FWN1R stated: the cell is 77 comoving kpc; lambda_P
  x 0.5 is below one cell and is not resolved; the primary 79 is about one cell.
- Label per case and footing, FWN1R section 5: FOREST ROW HOLDS AT FLUX LEVEL if every known answer passes, both twins
  bite and D + 2 SE < 4 (a hit, not a pass); FOREST ROW FAILS AT FLUX LEVEL if D - 2 SE > 4; otherwise NO VERDICT;
  FRAGILE (bracket named).

## 4. Read across the two builds (reported, per footing; never a label on the theory)

- **f = 4 HOLDS IN BOTH BUILDS** if S4 and J4 both read HOLDS (FRAGILE named if either is).
- **f = 4 FAILS IN BOTH BUILDS** if both read FAILS.
- **THE BUILDS DISAGREE AT f = 4** if one reads HOLDS and the other FAILS.
- **f = 4 NOT RESOLVED** otherwise (at least one NO VERDICT); each build's word is given.
- The ceiling, updated: build A's Q(f) = D + 2 SE at f = 2, 3 (FRZ6), 4 (this lane), 5, 10 (FWN1), and build B's at 2, 3
  (FRZ6R), 3.5, 4, 4.5 (this lane), 5, 10 (FWN1R); the crossing of 4 is interpolated log-linearly between the adjacent
  points, with the same for D and D - 2 SE as the band. The bracket of f between the largest f that HOLDS in both builds
  and the smallest f that FAILS in both is stated plainly; if no f fails in both, that is said.

## 5. Compute

At most two heavy processes in total: one build-A part process (3 flux threads) and one build-B runner (2 threads);
a second build-B runner may start only after build A has finished. `nice -n 19`. Physical-footprint guard 14 GB (A) and
16 GB (B) with restart. Before every part: wait unless free disk >= 10 GB and free + inactive memory >= 24 GB; stop below
8 GB disk or above 14 GB swap. One JSON per box (A) or per part (B), restartable. The first part of each stage is checked
before the stage is left to run. `python3 -I -B`; nothing written outside this folder; no downloads. Regenerable arrays and
tables are deleted at the end; parts are committed. Budget about 3 h wall from about 10:15 EST.

## 6. Hand estimate (before any number of this lane)

Log-linear interpolation of the section 0 anchors (ln D against ln f, between f = 3 and 5):

- **Build A, S4:** D about 3.4 canonical / 4.1 alt, SE about 1.2 / 1.4. So |D - 4| is inside 2 SE on both footings:
  NO VERDICT (unresolved) 80 %, FAILS 12 %, HOLDS 8 %. T1 and T2 bite (95 %).
- **Build B, J4:** D about 2.7 / 3.3, SE about 0.14 / 0.19, so D + 2 SE about 2.9 / 3.6: HOLDS 60 % canonical and 45 %
  alt, otherwise NO VERDICT; FRAGILE through a lambda_P bracket more likely than not. **J3.5:** D about 1.3 / 1.6, HOLDS
  85 %. **J4.5:** D about 5.0 / 6.2, FAILS 60 % / 75 %, otherwise NO VERDICT.
- TW-B4 factor 3.3 to 4, bites (95 %). U4 against J4: ratio 1.2 to 2; it bites FWN1R's rule 50 %.
- Read across: f = 4 NOT RESOLVED on both footings 75 %; HOLDS IN BOTH 8 %; DISAGREE 5 %; FAILS IN BOTH 2 %; other 10 %.
  If it lands as expected, the ceiling in build B sits between 4 and 4.5 and build A cannot tell.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
