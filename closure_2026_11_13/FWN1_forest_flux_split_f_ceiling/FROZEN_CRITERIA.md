# FWN1 FROZEN CRITERIA (2026-11-13, written about 20:40 EST): the crossing-speed split's settled radius, how large can f be at flux level

Committed alone, before any script of this lane exists and before any new number of this lane has been computed.
TEST lane, not blind: adopts nothing, relabels nothing (FRZ4, FRZ5, FRZ6, JNT2 and every earlier lane keep their labels),
registers nothing. Footings (canonical a0 = 9.3603e-11 m/s^2, alt a0 = 1.1312e-10 m/s^2) are graded separately and never
pooled. Cold dark energy is a gravitating field component; no particle is added. kappa = 1/2 and the share 5.41 are
FITTED. The settled-radius family is post hoc (added after FRZ1 failed at matter level); f is a free constant; the
crossing-speed boundary is post hoc to SRJ2 and JNT1. A HOLDS label is a hit that awaits an independent blind re-grade,
not a pass of the theory. Nothing here can say the data favour the framework. This lane never opens the folder of the
running blind re-grade FRZ6R.

## 1. Question and cases

FRZ6 (criteria 569333ff30, amendment A1 352a7fe6ae, result 00481b407b) graded the split at f = 1.25, 2, 3 (12 seeds at
z 2.2). This lane asks for the ceiling: at flux level, how large can f be before the forest row fails, and does the split
with no settled radius at all hold or fail. Cases, per footing:

- **S5, S10: the crossing-speed split at f = 5 and f = 10.** A halo with FRZ1's v_vir(hb) > v*(z) keeps the reference
  layout (FRZ1 mode "Rb") at every radius; every other halo gets SRH1's `lay_S` at f (R_set = min(f R_fold, r_ta), SRH1's
  cap unchanged).
- **Sinf: the split with no settled radius (f = inf).** Above v*(z): the reference layout. Below: the record's full law
  layout for that halo, i.e. SRH1's `lay_S` at f = inf (R_set = r_ta), which is exactly FRZ4's / FRZ6's case C key `finf`
  (= SRH1 KA_T = FRZ1). Known answer (g) shows Sinf equals `finf` in every below-v* halo and the reference in every above.
- **Control S3 (f = 3)**, z 2.2 seeds 0 and 1, both footings: must reproduce FRZ6's S f = 3 spectra (known answer j1).
- **Control C (unsplit, f = inf)**: FRZ6's case C, graded by this lane's grader from FRZ6's (and FRZ4's) committed parts,
  never recomputed. It must keep its FRZ6 reading (known answer j2).

**Source of the split (copied, not re-derived):** `closure_2026_11_13/JNT2_crossing_speed_joint/jnt2_common.py` lines 7
to 18 (constants, E(z), `vstar0_kms`, `vstar_kms` mode "main"; v*(0) = a0 / (10 (1 + 5.41) H0) = 668.5 / 807.9 km/s,
v*(z) = v*(0) / E(z)) and `jnt2_hm.py` lines 29 to 45 (`above`, `lay_J`), as FRZ6's `frz6_tables.py` (`above`,
`lay_split`) copies them. Membership is per halo of FRZ1's mass grid at each redshift bin; the painted 0.1 dex bin profile
is the count-weighted mean over the bin's grid haloes (FRZ4's `binmean`), so a bin straddling v*(z) carries the change of
its below-v* haloes only.

## 2. Build (FRZ6's, copied into this folder; FRZ6's, FRZ4's, FRZ3R's and JNT2's files are never edited)

- Tables: FRZ6's `frz6_tables.py` copied, with the split keys S3.00, S5.00, S10.00, Sinf (S1.25 and S2.00 dropped). The U
  and C keys (f 0, 1, 2, 3, inf) and every other array are FRZ6's code unchanged, so the forced set (FRZ4's rule over the
  U and C cases) and the base box are FRZ6's and the reference field R is reproduced (known answer i).
- Fields: FRZ6's `frz6_run.py` copied (FRZ3R's `frz3r_core.py` imported read-only; FGPA, saturation, mean-flux match,
  P1D, P3D; box 20 Mpc/h, N 384, real space; forced rare bins in their own boxes, stratified estimator), with this lane's
  field plan (section 10). The share of each new case carried by non-forced rare bins and by common bins is reported.
- Gas inputs and brackets as FRZ4 / FRZ6 froze them: T0 1e4 K, gamma 1.5, tau_eff(z) = 0.751 ((1+z)/4.5)^2.90 - 0.132,
  lambda_P = 79 comoving kpc (all PROVISIONAL, inherited).
- Gate: DESI DR1 P1D, 755 points, full covariance, via `ss1_cosmo.forest_setup / forest_eval` (FRZ3R's grading set-up,
  executed read-only, exactly as FRZ6's grader). **Gate: Delta chi^2 <= 4.**

## 3. Seeds (frozen; no optional stopping)

- **z 2.2: 12 seeds (0 to 11), both footings**, every new case in every seed.
- **z 2.6, 3.0, 3.4, 3.8, 4.4: seed 0 only.** The six other DESI bins are interpolated linearly in z (FRZ4 section 4).
- If 12 seeds at z 2.2 are not reached for a case on a footing, that case is **NO VERDICT (seed count not reached)** there;
  what was reached is reported, ungraded. If a z bin other than 2.2 is missing, every case on that footing is NO VERDICT
  (bins missing).

## 4. Statistic

D = the 12-bin flux Delta chi^2 of the case (z 2.2 = 12-seed mean stratified ratio; other computed bins seed 0; the rest
interpolated), computed with FRZ6's `est`, `r_points`, `dchi2_sel` unchanged. Seed noise as FRZ6 (e): N22 =
[1 / (n (n - 1))] sum_s Delta chi^2_22(R_s - R̄), D22 = Delta chi^2_22(R̄ - 1), N12 = D N22 / D22,
**SE = 2 sqrt(D N12) + N12.** Matter level of the same fields as FRZ6.

## 5. Known answers (every one that applies must pass, or that case and footing is NO VERDICT)

- **(a)** f = 0 equals the reference: B|f0.00 fields at z 2.2, 3.0, 4.4 seed 0 (this lane's parts), max over k_v of
  |P_F(B_f0) / P_F(R) - 1| <= 1e-12 in every box, and the stratified Delta chi^2 at f = 0 <= 1e-12. All cases.
- **(b)** FRZ4's Poisson-only known answer on FRZ4's parts (re-evaluated, must PASS, as FRZ6). All cases.
- **(c0)** record-convention D_rec of each case through this lane's tables equals the same quantity through an
  independent chain: JNT2's `jnt2_hm.py` executed read-only up to its case loop (FZS1's library, not SRH1's), its
  `ratios_J(foot, z, fac)` at fac = 3, 5, 10, inf over FRZ1's twelve z bins, graded with JNT2's `jnt2_forest.py` route
  (FRZ1's `frz1_forest.py` prefix, `Rkz_z`, `forest_eval`). Pass: within 1 % or 0.002 absolute. In addition the chain's
  fac = 3 value must equal JNT2's stored G1 f3.00 (1.9898 canonical / 6.4321 alt) within 1 % (the chain is the record's).
- **(c1)** realised matter-level Delta chi^2 against the halo model's D_ta, FRZ6's rule (ratio 0.67 to 1.5 when D_ta >= 1,
  else D_mat <= 1; per computed bin with halo-model single-bin value >= 1, ratio 0.5 to 2). Per case.
- **(d)** every field's mean flux equals the target within 1e-4.
- **(e)** seed scatter at n = 12, per case: **pass if N12 <= 0.1 D or N12 <= 0.05** (FRZ4 / FRZ6 rule).
- **(f) split identity** (FRZ6's): in every new-case field of every forced box whose 0.1 dex bin lies wholly above v*(z),
  B equals R to 1e-12 relative at every k_v; the number of FRZ1 grid haloes above v*(z) at z 2.2, 3.0, 4.4 equals JNT2's
  `jnt2_hm.json` membership (170 / 192 / 223 canonical, 160 / 182 / 213 alt).
- **(g) f = inf identity.** (g1) Table level, every z bin and footing: the Sinf profile of each FRZ1 grid halo equals the
  `finf` profile (U row) exactly for every halo at or below v*(z) and the reference ("Rb") profile exactly for every halo
  above (max abs difference 0). (g2) Field level, z 2.2 all 12 seeds: in every forced box whose bin lies wholly below v*(z)
  (no grid halo of the bin above), this lane's B|Sinf P1D equals the B|finf P1D of FRZ6's part (seeds 2 to 11) or FRZ4's
  part (seeds 0, 1) for the same z, seed, footing and box to 1e-12 relative (P3D to 1e-6, the single-precision tolerance
  of FRZ6's amendment A1). Applies to Sinf.
- **(i) identity with FRZ6** (a priori tolerance, citing FRZ6's AMENDMENT_A1 which established it): in every part of this
  lane at a (z, seed, footing, spec) FRZ6 also computed, the reference field R of the base box and of every forced box
  equals FRZ6's R **to 1e-12 relative for P1D and 1e-6 relative for the single-precision 3D power**, at every k_v / every
  3D bin with modes. Bracket parts: the same on boxes and specs common with FRZ6's `bracketS` parts. Pass-2 parts (section
  10) carry a base-box R that must equal the pass-1 part's R to 1e-12 (P1D) before any pass-2 field is merged. A failure
  makes every case on that footing NO VERDICT.
- **(j1) control S3:** at z 2.2 seeds 0 and 1, both footings, this lane's B|S3.00 equals FRZ6's B|S3.00 in the base box
  and every forced box to 1e-12 (P1D) and 1e-6 (P3D). A failure makes every case on that footing NO VERDICT.
- **(j2) control C:** this lane's grader, run on FRZ6's committed parts (merged with FRZ4's exactly as FRZ6's grader merges
  them), gives the case-C flux D and SE equal to FRZ6's stored values (`frz6_grade_<footing>.json`: D 256.1 / 282.3) within
  1e-6 relative, and its label rule gives D - 2 SE > 4 (fails). If C does not still fail, no HOLDS is written on that
  footing (the case becomes NO VERDICT (control)).

## 6. Twins (separate `*_MUTATE*` outputs; graded at the 12 seeds at z 2.2; must bite, per case, or NO VERDICT)

- **T1, layout change doubled in every box** (base box and every forced box: B - R doubled in density, D2| fields).
  Bites if the 12-seed z 2.2 single-bin Delta chi^2 is >= 1.5 x the primary's. Why it cannot fail for FRZ6's reason:
  FRZ6's T1 doubled the base box only, so where the base box's change and the forced boxes' change had opposite signs the
  doubled part cancelled against the undoubled part. Here every term of the stratified change is doubled together, so at
  linear order the ratio's deviation doubles exactly whatever the signs, and Delta chi^2 grows by about 4x; it can fail to
  reach 1.5x only through flux saturation non-linearity, or a construction error, which is what it is there to catch.
- **T2, saturation removed in the base box** (FRZ6's: F = 1 - A tau with mean flux matched linearly, the M1_lin spec on the
  base box's R and B). Bites if the 12-seed z 2.2 base-box-only Delta chi^2 changes by a factor >= 1.25 or <= 0.8.

## 7. Brackets (seed 0; FRAGILE if any frozen bracket's 12-bin estimate lies on the other side of 4 from D)

FRZ6's eight, unchanged: lambda_P x 0.5, x 2, 100 proper kpc; gamma 1.2, 1.6; tau_eff x 0.9, x 1.1; clustered placement.
12-bin estimate = D x (bracket / primary) on the bracket subset at z 2.2 + 3.0 (z 2.2 alone for clustered), seed 0.
Subset: FRZ4's rule with this lane's new cases (S5, S10, Sinf) in place of U: the forced bins by descending max share of
the new cases' change at k 3 until the cumulative share >= 0.8 at every new case, at most 10 bins; the base box always.
**Measured-range reading (reported beside the label, never the label):** the three lambda_P brackets replaced by Rorai et
al. 2017 (Science 356, 418), Table S2, z = 3.0, systematics-corrected 16 to 84 % range lambda_P = 91.4 and 138.6 comoving
kpc (PROVISIONAL, as FRZ6 section 9), with gamma, tau_eff and clustered unchanged.

## 8. Labels (per case S5, S10, Sinf, per footing)

- **NO VERDICT** if a known answer that applies fails; a twin does not bite; 12 seeds at z 2.2 not reached; a bin missing;
  or |D - 4| <= 2 SE (unresolved).
- **FOREST ROW HOLDS AT FLUX LEVEL** if every known answer passes, both twins bite, and **D + 2 SE < 4**; written as a hit
  that awaits an independent blind re-grade, not a pass of the theory. Before it is written: the twins are re-checked at
  12 seeds and control C must still fail (j2).
- **FOREST ROW FAILS AT FLUX LEVEL** if every known answer passes, both twins bite, and **D - 2 SE > 4**.
- **FRAGILE (bracket named)** when a frozen bracket's estimate crosses the gate; "[brackets incomplete: ...]" if a bracket
  part is missing.

## 9. Reported, never a label

- **The ceiling.** Per footing, Q(f) = D + 2 SE at f = 2 and 3 (FRZ6's stored S2.00, S3.00 values,
  `frz6_grade_<footing>.json`), 5, 10 (this lane) and inf. f*: the first consecutive pair (fa, fb) of 2, 3, 5, 10 with
  Q(fa) < 4 <= Q(fb), interpolated log-linearly (ln Q linear in ln f). If Q(10) < 4 <= Q(inf): "f* > 10, not
  interpolable". If Q(2) >= 4: "f* < 2". If Q < 4 at every f: "no ceiling up to inf". The same interpolation of D alone
  and of D - 2 SE is reported as the band. The uncertainty is stated plainly (two to three grid points, FRZ6's and this
  lane's values from different seeds-of-record at f 2, 3, interpolation form chosen a priori, inherited gas inputs).
- FRZ5's refit reading of each case (FRZ6's `frz6_refit.py` route: `frz5_refit.py` executed read-only up to "reading G").
- Flux and matter Delta chi^2, D_ta, D_rec, per-bin values, R_F at k_v 0.003 / 0.005 / 0.01 / 0.02 / 0.03 s/km, N12, SE,
  single-seed z 2.2 values, Sinf minus C, the measured-range reading's labels.

## 10. Compute (one heavy slot)

One part process at a time, `nice -n 19`, 3 flux threads (at most 4), exit 76 and restart above 16 GB peak resident
memory, one JSON per box (restartable), runner `run_all.sh` under nohup with `logs/run_all.pid` and a `run_all.done`
marker, waited on by pid / marker, never `pgrep -f`. Before each part: `df -g .` (stop below 8 GB free) and
`sysctl vm.swapusage` (stop above 8 GB used). The first part of every stage (and the first bracket part) is tested before
the stage is left unattended. Stage order (frozen):

0. tables for the twelve z bins; the c0 chain (light, single thread).
1. **pass 1 ("inf")**, z 2.2 seeds 0 to 11, footings alternating: fields R, B|Sinf, D2|Sinf in the base box and every
   forced box; base box also M1_lin (R, B|Sinf); seed 0 also B|f0.00 everywhere.
2. **pass 2 ("fin")**, z 2.2 seeds 0 to 11, footings alternating: base box R (identity with pass 1 only) and B|S5.00,
   B|S10.00, D2|S5.00, D2|S10.00 in the base box and every forced box; base M1_lin (R, B|S5.00, B|S10.00); seeds 0 and 1
   also B|S3.00 everywhere (control j1). The grader takes R of every forced box from the pass-1 part.
3. **other bins**, seed 0 at z 3.0, 4.4, 2.6, 3.4, 3.8: R, B|S5.00, B|S10.00, B|Sinf (plus B|f0.00 at 3.0, 4.4).
4. **brackets**: z 2.2 bracket specs (FRZ6's eight specs incl. M1_lin, plus the two measured-range specs) on the new
   subset; clustered z 2.2; z 3.0 bracket specs.

Budget about 9 h wall from about 20:45 EST. If it runs out, grade what this section allows and name what is missing.
Regenerable arrays and tables are deleted at the end; parts are committed (each under 60 MB). `python3 -I -B`; nothing
written outside this folder; no downloads.

## 11. Hand estimate (before any number)

Record anchors (no new number): FRZ6 split D + 2 SE = 0.50 / 0.65 (f 2), 2.04 / 2.50 (f 3); unsplit C D = 256 / 282;
the split's matter-level D_rec rises steeply with f (0.05 / 0.15 at f 2, 1.99 / 6.43 at f 3); R_set = min(f R_fold, r_ta)
saturates at r_ta for many haloes by f 10.

- **Sinf:** most of C's flux change sits in haloes above v*(z) (M200c above about 6e11 / 1e12 Msun/h at z 2.2) but the
  below-v* haloes still carry the full law layout out to r_ta. Expect D about 20 to 120 on each footing.
  FAILS 75 %, NO VERDICT 20 % (a known answer or unresolved), HOLDS 5 %. If it fails, FRAGILE through no bracket 55 %.
- **S10:** close to Sinf (cap at r_ta), D about 10 to 90: FAILS 65 %, NO VERDICT 25 %, HOLDS 10 %.
- **S5:** D about 2 to 20: FAILS 40 %, NO VERDICT (unresolved) 35 %, HOLDS 25 %, alt likelier to fail than canonical.
- Ceiling f* (D + 2 SE = 4) between 3 and 5 on both footings: 60 %; between 5 and 10: 25 %; above 10: 5 %; below 3
  (FRZ6's f 3 Q is 2.0 / 2.5): 10 %.
- Twins: T1 bites in every case (95 %); T2 bites (95 %, FRZ6 factors 700 to 2000).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
