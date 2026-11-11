# FZS1 FROZEN CRITERIA: the forest row with the law's layout only inside the settled radius

Committed alone, before any FZS1 script exists and before any FZS1 number is computed. TEST lane, quarantined. Relabels
nothing, adopts nothing, registers nothing. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), graded
separately, never pooled. Cold dark energy is a gravitating field component; no particle is added anywhere.

**This rule is post hoc to FRZ1's fail.** It was written after FRZ1 (criteria 1835d8fb7d, result d1494aa68c) found
FOREST ROW FAILS / FOREST ROW FAILS (Delta chi^2 9916.2 / 9008.7). A HOLDS here is not a pass of form B: it needs an
independent re-grade, and it is not in PAPER72.

## 0. The question, and what was seen before this freeze

Does the forest row still fail if the law's layout applies only inside the region that has settled by each redshift?
FRZ1 laid each halo's cold dark energy out by rule 5 out to its turnaround radius at every DESI redshift, i.e. it assumed
every halo fully settled at z 2.2 to 4.4. FLD1 (`fable52_push/FLD1_fold_reach/`) found the folded region much smaller
early: R_fold / R_ta (its own shell R_ta) is 0.31 to 0.33 at z 4 and 0.43 to 0.44 at z 2.

Seen before this freeze: FRZ1's criteria, RESULT, `frz1_hm.py`, `frz1_forest.py`, `frz1_hm.out`; FLD1's RESULT and the
interpolation functions of `fld1_compare.py`; HLF1's RESULT (first 30 lines); CO1's stored z = 0 R_tot / R_cold at
k 0.05 to 8 (canonical R_tot 1.0033 / 1.0282 at k 1 / 3; alt 1.0076 / 1.0645); KL1's RESULT lines on R_tot (0.982 -> 0.972
at k 1 under its C2 response). From FLD1's run files (to check they load): R_fold in physical kpc at z 0 / 2 / 2.2 / 3 / 4 /
4.4, canonical, log M_b 9.4: 62.2 / 21.3 / 19.5 / 13.9 / 7.6 / 5.8; 10.45: 139.3 / 47.8 / 43.9 / 31.3 / 17.2 / 13.3;
10.9: 196.9 / 67.6 / 62.1 / 44.3 / 24.5 / 18.9; 12: 458.7 / 157.8 / 145.0 / 103.5 / 58.2 / 45.2; alt within 0.5 %. No
R_cold, R_tot or Delta chi^2 under this lane's rule has been computed by anyone.

## 1. The rule (graded reading)

For each footing, each DESI DR1 P1D bin z (2.2, 2.4, ..., 4.4) and each halo of FRZ1's population at z:

1. **Regime and baryon mass.** The regime is FRZ1's (v_vir against v_stiff, unchanged). The baryon mass that sets the
   fold is the halo's condensed baryons in FRZ1's graded reading L: galaxy regime M_b = (1 - FB) M_ta / X (Lagrangian
   scope); cluster regime M_b = FB M200c. Converted from Msun/h to Msun with CFG556's h. The same M_b is used in every
   bracket, including reading V.
2. **R_set(z, M_b) = FLD1's R_fold(z, M_b), same footing,** from FLD1's primary run files (`runs/hubble_<footing>_M<logMb>_
   zi10_N2400.json`, the 12 masses 6.5 to 12). In z: linear interpolation of each run's stored series (FLD1's `at_z`). In
   mass: log R linear in log M_b between table masses (FLD1's `rfold`). Outside log M_b 6.5 to 12: scaled as M_b^(1/3) from
   the end row (FLD1's stated scaling). FLD1 itself clamps at the ends; clamping would shrink R_set for the heaviest haloes
   and favour a hold, so it is not used. Physical kpc to FRZ1's comoving Mpc/h: x 1e-3 (1 + z) h. Capped at the halo's r_ta.
3. **The layout.** Let M_B(r) be FRZ1's form-B layout (mode "B") and M_R(r) its cold-reference layout (mode "Rb"), both
   with the same options. Let Bar(r) be the condensed baryons common to both (galaxy regime: M_b + (FB M_s - M_b) shape;
   cluster regime: FRZ1's `bar_cum`). Cold dark energy: C_B = M_B - Bar, C_R = M_R - Bar (FRZ1's "outside" term, identical
   in both, counts as cold). The settled layout is
   - M_S(r) = Bar(r) + s C_B(r) for r <= R_set, and M_S(r) = Bar(r) + C_R(r) for r > R_set,
   - with s = C_R(R_set) / C_B(R_set): **the enclosed cold mass at R_set equals the reference's.** Inside R_set the cold dark
     energy has the law's shape; outside it the cold reference's layout, untouched.
   R_set is inserted as a grid node (FRZ1's `rgrid` is wrapped at call time; FRZ1's code is not edited). R_set = 0 gives
   M_S = M_R exactly.
4. **R_cold,S(k, z) = R_tot,S / R_bar,** with R_tot,S = 1 + (P_S - P_Lta) / P_std and R_bar FRZ1's (its Rb layout), all
   with FRZ1's halo model at z (Tinker 2008 with its z-scaling, Tinker 2010 bias, Duffy c(M, z), Delta_ta(z), a0 constant in
   physical units, X by redshift).

FRZ1's code is executed unchanged: `frz1_hm.py` up to its "checkpointed run" marker and `frz1_forest.py` up to the line that
reads `frz1_hm.json`, each executed from its own path, read-only. Nothing is written in FRZ1's folder.

## 2. Gate

The record's forest gate exactly as FRZ1 used it: `ss1_cosmo.forest_eval` with form B's own CLASS reference (F1A B2 cold
fit), the amplitude ratio sqrt(R_cold,S) in each ZG column from its nearest DESI bin (FRZ1's `Rkz_z`, flat at its end
values outside CO1's k grid), DESI DR1 P1D, 755 points, md5 33d7fc21bfd3d745ed71a0bbe80ca433, full covariance.
**Delta chi^2 <= 4.** Per-bin values (own covariance block) reported.

## 3. Labels (per footing)

- **FOREST ROW HOLDS WITH A SETTLED RADIUS:** Delta chi^2 <= 4 under the rule of section 1.
- **FOREST ROW FAILS:** Delta chi^2 > 4.
- **NO VERDICT:** any known answer fails or any MUTATE arm does not bite.
- **Brackets, reported only:** R_set x 0.5; R_set x 2; reading V (FRZ1's virial scope, gal_scope "vir", for both M_B and
  M_R, with the same R_set). If a bracket lands on the other side of the gate from the graded reading, the label carries the
  qualifier "FRAGILE" with the crossing brackets named (FRZ1's rule); the label itself does not change.
- **Lane label:** HOLDS (both hold), FAILS (both fail), SPLIT, NO VERDICT.

## 4. Known answers (any failure: NO VERDICT)

- **KA-F:** FLD1's quoted radii from its files with this lane's interpolation: canonical R_fold at z 0 / 2 / 4 for log M_b
  9.4, 10.45, 10.7, 10.9 equal FLD1's RESULT table (62 / 21 / 7.6; 139 / 48 / 17.2; 169 / 58 / 21.0; 197 / 68 / 24.5) to
  its printed digits (0.6 kpc where printed to integers, 0.06 kpc where printed to one decimal).
- **KA-T:** R_set = r_ta (every halo) reproduces FRZ1's primary R_cold at all 12 bins to 1e-10 relative, its total Delta
  chi^2 (9916.2 / 9008.7, the stored values) to 0.01, and its stored per-bin values to 0.01.
- **KA-0:** R_set = 0 gives R_cold,S = 1 at every k and bin and Delta chi^2 = 0 (|value| <= 1e-10).
- **KA-M:** at z = 3, both footings, graded rule and the x 2 and reading-V brackets: M_S(r_ta) = M_ta to 1e-9 and M_S
  non-decreasing (to 1e-9 M_ta).
- **KA-Z0:** at z = 0 with R_set = r_ta the code returns CO1's stored primary R_tot (1e-10 relative).

## 5. MUTATE (each must bite; written to separate `_MUTATE` outputs)

- **MS1 (R_set x 10, capped at r_ta):** must FAIL the gate (Delta chi^2 > 4) on both footings. If FRZ1's fail is real, an
  R_set reaching the turnaround radius must bring it back.
- **MS2 (z dependence reversed):** bin z_i uses R_fold at z_(13-i) (2.2 <-> 4.4, 2.4 <-> 4.2, ...). Canonical: at z 2.2
  |R_cold,S(k 10) - 1| must fall, and at z 4.4 it must rise, each by at least 20 % of the graded value.

## 6. What counts against (reported whatever the label)

- **z = 0.** The same rule at z = 0 puts the law only inside R_fold(0) = 62 to 197 kpc at the KiDS masses, which FLD1 found
  short of the KiDS windows and of form B's cap. Reported in one table: R_tot at k 1 and 3 h/Mpc at z = 0 under the rule,
  beside CO1's (1.0033 / 1.0282 canonical, 1.0076 / 1.0645 alt) and KL1's quoted value (0.982 -> 0.972 at k 1, C2). Lensing
  is not re-graded.
- **R_fold comes from FLD1's law-dominated limit** (a softened point mass, radial shells, no cold dark energy mass in the
  shells' own gravity). That limit holds only for mu_K small (FLD1's brackets).
- **FRZ1's inherited ingredients stay inherited:** present-day baryon shapes, a halo list not measured at z 2 to 4
  (Tinker 2008 z-scaling and Duffy c(M, z) from memory, PROVISIONAL), a linear 1D projection with no thermal or absorption
  physics, and the layout put in by hand (the joint is not derived).
- **The rule itself is post hoc**, chosen after FRZ1's fail, and the shape inside R_set (the law's, rescaled) is a choice.

## 7. Hand estimate (before any number)

At z 3 R_fold is about 31 kpc physical for log M_b 10.45, i.e. about 0.08 Mpc/h comoving: about 0.35 r200m and about one
NFW scale radius (c near 3 at z 3). R_fold scales as M_b^(1/3), like r200m, so R_set / r200m is roughly 0.4 at z 2.2 and
0.25 at z 4.4 at every mass. Outside R_set nothing changes. Inside it, the law's shape (isothermal, M proportional to r
beyond r_M of a few kpc) replaces an NFW interior (M closer to r^2) at the same enclosed mass: the rule makes halo centres
cuspier, so R_cold,S should rise above 1, the opposite sign to FRZ1. The rearranged mass is about 10 % of M_ta inside
k R_set < 1 at k <= 5, so |R_cold,S - 1| is under 0.003 at k <= 5 and about +0.003 to +0.01 at k 10, held flat above
k 10 by the pipeline. Delta chi^2: 0.5 to 30, even odds of a hold on each footing; x 0.5 holds; x 2 more likely fails
(10 to 100); reading V close to the graded value. MS1 fails by thousands. The closure chat's estimate: holds or comes
close on the primary rule; the x 2 bracket may fail.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
