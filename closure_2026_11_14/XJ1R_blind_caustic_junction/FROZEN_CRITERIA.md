# XJ1R FROZEN CRITERIA (2026-11-14, written 13:47 EST by the clock): blind grade of the caustic junction for rule 6

Committed alone, before any script of this lane exists and before any number of this lane has been computed. Written by
the blind builder from `BLIND_BRIEF.md` (the lead's brief, committed alone before this file). TEST lane, BLIND: adopts
nothing, relabels nothing, registers nothing. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (a0 = 1.1312e-10
m/s^2) are graded separately and never pooled. Cold dark energy is a gravitating field component; no particle is added.
kappa = 1/2 and the share 5.41 are FITTED. Rule 6 is a candidate, NOT ADOPTED. A HOLDS word means "not excluded in this
build"; it does not say the data favour the framework over LCDM.

Seen before this freeze (all dated before 2026-11-14 or allowed by the brief): the brief; FLD1's `fld1_shells.py`,
FROZEN_CRITERIA.md, RESULT.md, the list of its `runs/` and the interpolation functions of `fld1_compare.py`; FZS1's
FROZEN_CRITERIA.md and `fzs1_hm.py`; SRH1's `srh1_hm.py` up to its run marker; FWN1's FROZEN_CRITERIA.md, RESULT.md,
`fwn1_tables.py`, `fwn1_run.py`, `fwn1_grade.py`, `fwn1_c0.py`, `run_all.sh`, `test_stages.sh`, the list of its parts,
and two stored numbers read to plan the control (FWN1's S5 canonical D 8.0854, SE 2.4138; its c0 chain S5 canonical
D_rec 50.5379); JNT2's `jnt2_common.py` and the `above` / `lay_J` lines of `jnt2_hm.py`; PD1's `pd1.py` (loader and
baryon mass lines) and QX8's `load_sparc`. Nothing of XJ1, CJ1, any memory directory, transcript or 2026-11-14 handoff
has been opened.

## 1. The statement graded (brief section 1, unchanged)

For k = 2 and k = 3 separately: in a system slower than v*(z) the cold component follows the law's own layout, unscaled,
inside R_set = R_k(z, M_b); outside R_set the rest of the system's cold component keeps the reference layout's shape; a
system faster than v*(z) keeps the reference layout at every radius.

## 2. Definitions (brief section 2, unchanged; how this build realises them)

- **Halo model.** FRZ1's, through SRH1's `srh1_hm.py` prefix executed read-only (as FWN1's tables do): M_B = FRZ1 mode
  "B", M_R = mode "Rb", Bar = FZS1's `Bar` (SRH1's copy), C_B = M_B - Bar, C_R = M_R - Bar, C_tot = C_R(r_ta), the value
  at the last node of the halo's radius grid (r_ta).
- **Boundary.** FWN1's `above()` (JNT2's `vstar_kms` mode "main": v*(0) = a0 / (10 (1 + 5.41) H0), H0 67.4, Omega_Lambda
  0.6847, flat, v*(z) = v*(0) / E(z)) against FRZ1's v_vir(hb). Above: M = M_R at every radius.
- **Exact junction** (below v*): R_set is inserted as a grid node (SRH1's `CUR` wrapper of FRZ1's `rgrid`). For r <=
  R_set, M(r) = M_B(r). For r > R_set, M(r) = Bar(r) + C_B(R_set) + t [C_R(r) - C_R(R_set)], t = [C_tot - C_B(R_set)] /
  [C_tot - C_R(R_set)]. If the capped R_set equals r_ta (no node outside), M = M_B everywhere. If R_set = 0, M = M_R.
  Haloes in FRZ1's regime "L" keep M_R, as SRH1's `lay_S` does (inherited; disclosed).
- **Caustics.** A copy of FLD1's `fld1_shells.py` in this folder with one addition: a per-shell passage counter, raised
  by one at every reflection at the wall (FLD1's "passage through the centre"). R_k(t) = the largest current radius
  among shells with counter >= k (0 if none), recorded beside FLD1's own R_fold column at FLD1's output times. Runs:
  FLD1's primary settings (12 masses log M_b 6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12; both footings; N
  2400; z_i 10; law on; mu 0; scaled grid) = 24 runs, written to `runs/` here. Nothing else in the equation changes.
- **Halo R_k.** FZS1's rules unchanged with the R_k column in place of R_fold: linear in z of each run's series; log R
  linear in log M_b between table masses (linear in R if any value at that z is <= 0); M_b^(1/3) scaling outside 6.5 to
  12; FZS1's `Mb_fold` (galaxy regime (1 - FB) M_ta / X; cluster regime FB M200c; Msun/h -> Msun with h); physical kpc ->
  comoving Mpc/h by x 1e-3 (1 + z) h; capped at r_ta. No constant multiplies R_k.
- **Control S5.** FWN1's case S5.00 unchanged (SRH1's `lay_S` at f = 5, i.e. FZS1's junction at 5 R_fold, inside FWN1's
  split).

## 3. What is graded

**(a) Forest at flux level, FWN1's build.** Copies here of FWN1's `fwn1_tables.py`, `fwn1_run.py`, `fwn1_grade.py`,
`fwn1_c0.py` (renamed xj1r_*), with the split keys replaced by **SEc2** (exact junction at R_2), **SEc3** (at R_3) and
the control **S5.00**. Everything else (U and C keys, forced set rule, base box, random streams, FGPA, saturation, mean
flux, P1D, P3D, estimator, `dchi2_sel`, `r_points`, DESI DR1 P1D 755 points with full covariance) is FWN1's code
unchanged. Statistic: FWN1's D, the 12-bin flux-level Delta chi^2 against the reference. **Gate: D <= 4.**

**(b) Rotation-curve containment.** SPARC's 175 galaxies, QX8's `load_sparc` (as PD1 imports it); M_b = PD1's baryon
mass: the largest enclosed baryon mass max_r [V_B^2 r / G] (floor 1e3 Msun) with V_B^2 = sgn(V_gas) V_gas^2 + Y V_disk^2
+ 1.4 Y V_bul^2 (PD1's 0.5 / 0.7 at Y = 0.5); Y = 0.5 graded, 0.3 and 0.8 reported. R_last = the largest measured
radius. R_k(z = 0; M_b) from this lane's runs by the rule of section 2 (physical kpc, no h). **Gate: no galaxy with
R_last > R_k at Y = 0.5.** Every galaxy beyond is named with its ratio R_last / R_k.

## 4. Seeds and stages (FWN1's plan, cut to this lane's cases)

- z 2.2: 12 seeds (0 to 11), both footings: R, B|SEc2, B|SEc3, D2|SEc2, D2|SEc3 in the base box and every forced box;
  base box also M1_lin (R, B|SEc2, B|SEc3); seed 0 also B|f0.00 (known answer a); seeds 0 and 1 also B|S5.00 (control).
- z 2.6, 3.0, 3.4, 3.8, 4.4: seed 0: R, B|SEc2, B|SEc3 (plus B|f0.00 at 3.0 and 4.4). Other bins interpolated in z.
- Brackets (FWN1's section 7): FWN1's eight specs plus the two measured-range specs on the subset (FWN1's rule with SEc2,
  SEc3 as the new cases) at z 2.2 and 3.0 seed 0; clustered placement z 2.2 seed 0.
- Why S5 is not recomputed at every seed: the control's graded number is taken from FWN1's committed parts through this
  lane's grader (j2); this lane recomputes S5 fields on z 2.2 seeds 0 and 1 to show the copy reproduces them (j1). This
  saves about a third of the heavy compute. If 12 seeds at z 2.2 are not reached for a case, that case is NO VERDICT
  (seed count not reached); a missing bin makes every case on that footing NO VERDICT (bins missing).

## 5. Known answers (each must pass where it applies, or the stated case and footing is NO VERDICT)

Caustics (any failure: every case on that footing NO VERDICT, and (b) NO VERDICT):
- **KS1** this lane's R_fold column reproduces FLD1's stored series (`fable52_push/FLD1_fold_reach/runs/hubble_<footing>_
  M<m>_zi10_N2400.json`) in all 24 runs: same number of rows, t and z columns and R_fold to 1e-9 relative (code identity).
- **KS2** R_1 reproduces FLD1's R_fold: |R_1 / R_fold - 1| <= 0.05 at every stored time with z <= 4.4 and R_fold > 0, all
  24 runs. (The two definitions differ: R_fold counts a shell once any neighbour has crossed it; R_1 counts a shell once
  it has itself reflected. The 5 % tolerance is fixed here before any number. The largest deviation at all times is
  reported.)
- **KS3** R_3 <= R_2 <= R_1 at every stored time of every run (exact).
- **KS4** FLD1's SPARC line reproduced from this lane's R_1 with FLD1's own mass (0.5 L[3.6] + 1.33 M_HI, its clamp):
  0 galaxies beyond, worst UGC00128 at 0.47 (printed digits), both footings.

Profiles (tables, every DESI z bin, both footings, every FRZ1 grid halo; failure: that case and footing NO VERDICT):
- **KP1** M = M_B exactly (abs difference 0) at every node r <= R_set.
- **KP2** |M(r_ta) - M_ta| / M_ta <= 1e-9 (reaches the turnaround mass).
- **KP3** non-decreasing: min diff(M) >= -1e-9 M_ta.
- **KP4** t >= -1e-12 in every below-v* halo with 0 < R_set < r_ta (round-off tolerance). The range of t is reported.
- **KP5** forcing R_set = r_ta gives the law's layout: the U row equals FWN1's `finf` U row (FRZ1 mode B) for every
  below-v* halo to 1e-12 relative of U(k = 0); forcing R_set = 0 gives the reference row exactly (abs 0); the formula
  evaluated with R_set at the first grid node agrees with the reference to 1e-6 M_ta (continuity, reported, graded).
- **KP6** every above-v* halo: U row of SEc2 and SEc3 equal to the reference row exactly (abs 0); membership counts at
  z 2.2, 3.0, 4.4 equal JNT2's `jnt2_hm.json` (FWN1's (f)).
- **KP7** per halo R_set,3 <= R_set,2.

Forest (FWN1's known answers, adapted; failure: that case and footing NO VERDICT):
- **(a)** f = 0 equals the reference (FWN1's (a)).
- **(b)** FRZ4's Poisson-only answer on FRZ4's parts (FWN1's (b)).
- **(c0)** D_rec of SEc2 and SEc3 through this lane's tables equals the same through an independent chain: JNT2's
  `jnt2_hm.py` prefix (FZS1's library, not SRH1's) with the exact junction re-implemented on that namespace, graded with
  FRZ1's `frz1_forest.py` route; within 1 % or 0.002 absolute. The chain's S5 must equal FWN1's stored c0 S5 (canonical
  50.53787, alt from `fwn1_c0_alt.json`) to 1e-9 relative.
- **(c1)** realised matter against the halo model's D_ta (FWN1's rule).
- **(d)** mean flux within 1e-4 of target.
- **(e)** seed scatter at n = 12: N12 <= 0.1 D or N12 <= 0.05.
- **(f)** split identity: in every forced box wholly above v*(z), B|SEc = R to 1e-12; membership as KP6.
- **(i)** R of every part (base and every forced box, primary and M1_lin; bracket and clustered specs on common boxes)
  equals FWN1's R of the same z, seed, footing and box: P1D 1e-12 relative, P3D 1e-6 relative (FRZ6 A1's tolerances, as
  FWN1). A failure makes every case on that footing NO VERDICT.
- **(j1) control S5 fields:** z 2.2 seeds 0 and 1, both footings: this lane's B|S5.00 equals FWN1's (`fin` parts) in the
  base box and every forced box, P1D 1e-12, P3D 1e-6. Failure: every case on that footing NO VERDICT.
- **(j2) control S5 graded:** this lane's grader run on FWN1's committed parts (inf + fin merged, oz, exactly FWN1's
  merge) gives S5's D and SE equal to FWN1's stored values (`fwn1_grade_<footing>.json`) to 1e-6 relative, and **D > 4**.
  Difference from the brief, said plainly: the brief says the control "must still fail". FWN1's own label for S5 was NO
  VERDICT (unresolved: D 8.09 / 9.45, D - 2 SE 3.26 / 3.87), so "fail" cannot mean FWN1's FAILS word; this lane reads it
  as the point estimate D above the gate. If j2 does not pass, no HOLDS is written on that footing (NO VERDICT (control)).

## 6. Twins (FWN1's, adapted; separate `_MUTATE` outputs; 12 seeds at z 2.2; must bite per case, or NO VERDICT)

- **T1** change doubled in every box (D2| fields): bites if the z 2.2 single-bin Delta chi^2 >= 1.5 x the primary's.
- **T2** saturation removed in the base box (M1_lin): bites if the base-box-only z 2.2 Delta chi^2 changes by >= 1.25 or
  <= 0.8 times.
- If a case's primary z 2.2 change is so small that a twin's ratio is undefined (primary 0), the twin does not bite.

## 7. Brackets (seed 0; FWN1's rule): lambda_P x 0.5, x 2, 100 proper kpc; gamma 1.2, 1.6; tau_eff x 0.9, x 1.1;
clustered placement. 12-bin estimate = D x (bracket / primary) on the subset at z 2.2 + 3.0 (z 2.2 alone for
clustered). FRAGILE (bracket named) if a frozen bracket's estimate lies on the other side of 4 from D; "[brackets
incomplete: ...]" if one is missing. Measured-range reading (Rorai et al. 2017, 91.4 and 138.6 comoving kpc) reported
beside the label, never the label.

## 8. Labels

Per case (SEc2, SEc3) and footing, FWN1's section 8 with control S5 in place of control C:
- NO VERDICT if a known answer that applies fails, a twin does not bite, 12 seeds at z 2.2 are not reached, a bin is
  missing, or |D - 4| <= 2 SE (unresolved); cause named.
- **FOREST ROW HOLDS AT FLUX LEVEL** if all pass, both twins bite, D + 2 SE < 4 and control S5 passes (j1, j2).
- **FOREST ROW FAILS AT FLUX LEVEL** if all pass, both twins bite and D - 2 SE > 4.
- FRAGILE as section 7.

Lane word, per footing and per k (brief section 3, unchanged): "CAUSTIC k HOLDS, BLIND" if (a) reads HOLDS and (b) finds
no galaxy beyond (FRAGILE carried); "CAUSTIC k FAILS THE FOREST, BLIND" if (a) reads FAILS; "CAUSTIC k CUTS ROTATION
CURVES, BLIND" if (b) finds a galaxy beyond at Y = 0.5 (may stand beside either forest word); otherwise "NOT RESOLVED"
with the cause. The forest grader prints the (a) label; the containment script prints (b); the lane word is assembled
from both in RESULT.md by the rule above, with no other input.

Reported, never a label: R_k / R_fold by redshift and mass; t per case (range and median over below-v* haloes per z);
per-bin D; D_rec (the record's older matter-level route, from the c0 chain); R_F; N12, SE; single-seed values.

## 9. Compute plan

- Light (now, `nice -n 19`, `python3 -I -B`): 24 shell runs (FLD1 needed about 12 min each single-threaded; run 6 at a
  time), KS1 to KS4, containment (b), tables for the 12 z bins with KP1 to KP7, the c0 chain, one small test part (z 2.2
  seed 0 canonical stopped after its base box and first forced box; the runner resumes it).
- Heavy: `run_r.sh` under nohup (pid in `logs/run_r.pid`, log `logs/run_r.log`), one part process at a time, 3 flux
  threads, FWN1's physical-footprint guard (exit and restart above 14 GB). A part starts only when at most two other heavy
  forest processes are alive (command lines containing xj1b_run.py, xj1b2_run.py, xj1a_run.py, fwn2a_run.py, fwn2b_run.py
  or xj1r_run.py; the counting command excludes itself) and free disk >= 10 GB; the runner stops below 8 GB free disk or
  above 14 GB swap. Order: z 2.2 seeds 0 to 11 (footings alternating), other bins, brackets, clustered. 40 parts. The
  marker `run_r.done` is written when the last part is done. Expected wall about 4 to 6 h if not held by the guard.
- The grader is committed before any heavy part is read; the lead runs it per footing. Temporary tables and arrays (tmp/)
  are not committed.

## 10. Hand estimate (before any number)

- **Caustic radii.** Secondary-infall caustics shrink with passage number; with the law's near-isothermal field the
  apocentres shrink more slowly than in a point-mass field. Guess R_2 / R_1 = 0.5 to 0.75 and R_3 / R_1 = 0.35 to 0.6 at
  z 0, smaller at z 2 to 4.4 (R_2 may be zero at z 4.4 for the smallest masses).
- **Forest.** R_set = R_k is below R_fold, far inside FWN1's f = 3 to 5 range where S3 had D about 1.1 to 1.4. The
  exact junction keeps the law's unscaled cold mass inside R_set (no factor s) and rescales the outer reference by t;
  at R_set about 0.1 to 0.2 r_ta the law's enclosed cold mass and the reference's are of the same order, so t should be
  within about 20 % of 1. Guess D = 0.05 to 1.5 for SEc2 and 0.02 to 1 for SEc3. Words: SEc2 HOLDS 60 %, NO VERDICT 30 %
  (a twin or a known answer, or KP4 if t < 0 somewhere), FAILS 10 %; SEc3 HOLDS 65 %, NO VERDICT 30 %, FAILS 5 %.
  FRAGILE through lambda_P x 0.5 or gamma 1.6: 25 %.
- **Containment.** FLD1's worst SPARC galaxy sits at 0.47 R_fold. With R_2 about 0.6 R_1 the worst ratio is about 0.8:
  k = 2 cuts a rotation curve 35 %; with R_3 about 0.45 R_1 the worst ratio is about 1.05: k = 3 cuts 55 %.
- **Control.** S5 reproduces FWN1 (95 %) and D > 4 (it is 8.09 / 9.45 by the record).
- **Twins.** T2 bites (95 %); T1 bites (85 %; a very small change can scale close to 4x, which bites).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
