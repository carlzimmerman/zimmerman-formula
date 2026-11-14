# XJ1 FROZEN CRITERIA (2026-11-14, written about 11:40 EST): the law exactly inside the settled radius, and a settled radius with no free constant

Committed alone, before any script of this lane exists and before any forest, lensing or matter-power number of this
lane has been computed. TEST lane, NOT blind: adopts nothing, relabels nothing (FZS1, SRH1, JNT2, JNT2R, FRZ6, FRZ6R,
FWN1, FWN1R and every earlier lane keep their labels), registers nothing. Footings (canonical a0 = 9.3603e-11 m/s^2,
alt a0 = 1.1312e-10 m/s^2) are graded separately and never pooled. Cold dark energy is a gravitating field component;
no particle is added. kappa = 1/2 and the share 5.41 are FITTED. Rule 6 is a candidate, NOT ADOPTED. A HOLDS label is a
hit that awaits an independent blind re-grade, not a pass of the theory. Nothing here can say the data favour the
framework.

## 0. Why, and what was seen before this freeze

**The junction.** Candidate rule 6 says: "the law's layout holds inside R_set". Every lane that has graded it (FZS1,
SRH1, JNT2, JNT2R, FRZ4 to FRZ6R, FWN1, FWN1R, WLJ1) built the inside with FZS1's junction: the cold component inside
R_set is the law's halo multiplied by s = C_R(R_set) / C_B(R_set), so that the enclosed cold mass at R_set equals the
reference's. FZS1 wrote this down as a choice ("the shape inside R_set (the law's, rescaled) is a choice"). Rule 4 gives
the law's halo from the baryons with no free amplitude, so a halo of s times the law's is the law only where s = 1.

**The constant.** The settled radius is f x R_fold with f read from data (window 1.25 to between 3 and 5). R_fold is
FLD1's fold reach, which depends on shell trajectories after their first crossing, where the action gives no answer
(COL1).

Seen before this freeze (this lane is not blind):

- Every committed number of the lanes named above, including FRZ6R's J2, J3 (0.024 / 0.029 and 0.572 / 0.691), FWN1R's
  J5, J10, Jinf (8.83 / 10.90, 194.5 / 288.0, 215.0 / 314.7), FRZ6's and FWN1's build-A numbers, and JNT2's stored
  matter-level numbers.
- From JNT2's `jnt2_hm.json`: s over the forest halo grid runs from 0.48 to 1.83 (f 1 to 3, z 2.2 to 4.4).
- Computed today from FRZ1's layouts only (no gate, no data), canonical, z 2.2 / 3.0 / 4.4, 13 haloes each: where
  C_R(r) = C_B(r). Light haloes (log M200c below about 9.5) have no such radius inside r_ta (the law's halo holds more
  cold mass than the reference at every radius, s < 1); heavier ones have one at 0.3 to 9 fold radii, rising with mass.
  So no single radius makes s = 1 for every halo.
- Computed today from FLD1's run files (column `R_ta_kpc`): R_ta / R_fold is 1.92 at z 0, 2.01 at z 0.2, 2.18 at z 1,
  2.31 at z 2.2, 2.45 at z 3.0, 2.57 at z 3.4, 2.90 at z 3.8, 3.35 at z 4.2 and 3.5 at z 4.4, the same within 2 % for
  log M_b 8 to 12 on both footings (larger at log M_b 6.5 and 7, up to 5, where FLD1 says its softening is not small).

No forest, lensing or matter-power number under the exact junction or under the zero-velocity surface has been
computed by anyone.

## 1. Definitions

All in FRZ1's halo model exactly as FZS1 and FWN1R use it (FZS1's `fzs1_hm.py` prefix, executed read-only). For a halo
at redshift z on a footing: M_B(r) FRZ1's layout mode "B", M_R(r) its mode "Rb", Bar(r) FZS1's `Bar`,
C_B = M_B - Bar, C_R = M_R - Bar, C_tot = C_R(r_ta) (equal to C_B(r_ta)).

- **Boundary (unchanged):** a halo with FRZ1's v_vir > v*(z) keeps M_R at every radius. v*(z) = v*(0) / E(z),
  v*(0) = a0 / (10 (1 + 5.41) H0) = 668.5 / 807.9 km/s, H0 67.4, Omega_Lambda 0.6847.
- **FZS1's junction, "J" (the record's):** M = Bar + s C_B for r <= R_set, Bar + C_R beyond, s = C_R(R_set) / C_B(R_set).
- **The exact junction, "E" (this lane's):**
  - r <= R_set: M_E(r) = M_B(r). The law's layout, unscaled.
  - r > R_set: M_E(r) = Bar(r) + C_B(R_set) + t [C_R(r) - C_R(R_set)], t = [C_tot - C_B(R_set)] / [C_tot - C_R(R_set)].
    The rest of the halo's cold component keeps the reference's shape, so that M_E(r_ta) = M_ta.
  - R_set at r_ta gives M_B at every radius (the control's row); R_set = 0 gives M_R.
  - Mass is conserved inside r_ta, the cold component is counted once, and the inside is the law with no free amplitude.
    What E gives up is FZS1's condition that no cold mass crosses R_set.
- **Settled radii:**
  - f x R_fold, f = 1, 2, 3: FZS1's `rset_com` unchanged (FLD1's R_fold at the halo's M_b and z, capped at r_ta).
  - **The zero-velocity surface R_zv:** FLD1's R_ta(z, M_b), "the largest current radius among shells with radial
    velocity <= 0" (FLD1 section 2), read from the same primary run files (`hubble_<footing>_M<logMb>_zi10_N2400.json`,
    series column `R_ta_kpc`) with FZS1's interpolation unchanged (linear in z along each run's series; log R linear in
    log M_b between the 12 table masses; M_b^(1/3) beyond the ends), FZS1's M_b (`Mb_fold`) and FZS1's conversion to
    comoving Mpc/h, capped at the halo's r_ta. No constant multiplies it. Why this surface: rules 3 and 4 already
    split the clock into the part that falls with the expansion and the part that stands around the baryons; R_zv is
    where the clock has stopped receding. Every shell outside R_fold is uncrossed, so R_zv is computed where FLD1's
    shell equation is exact, which R_fold is not.
  - R_set = R_fold (f = 1) is the other radius with no free constant.

## 2. Cases

| key | junction | settled radius | role |
|---|---|---|---|
| R | - | - | reference |
| J5 | J | 5 R_fold | control: must reproduce FWN1R's stored parts and still fail |
| E1 | E | R_fold | graded |
| E2 | E | 2 R_fold | graded |
| E3 | E | 3 R_fold | graded |
| Ezv | E | R_zv | graded |

J2 and J3 are not recomputed: they are read from FRZ6R's and FWN1R's committed parts (same boxes: known answer KA-5
shows this lane's R equals theirs).

## 3. Build B (graded today): FWN1R's library, read-only

Everything of FWN1R section 2 unchanged: `fwn1r_lib.py` imported from its folder (tables' grid KT, `U_set`,
`spectra_ta`, box L 20 Mpc/h, N 384, real space, halo realisation, lognormal two-halo component with |I_X / I_R|,
seeds SeedSequence([6, 61, iz, s]), gas smoothing lambda_P 79 comoving kpc with floor 1e-6, FRZ3R's FGPA step, gamma
1.5, tau_eff(z) = 0.751 ((1+z)/4.5)^2.90 - 0.132, the forest data through `ss1_cosmo.forest_setup`, the estimator
(ratio of seed sums), D = 12-bin flux Delta chi^2 on DESI DR1 P1D with full covariance, the jackknife SE over the seed
index, the anchor statistic A at z 2.2, 3.0, 4.4). **4 seeds (0 to 3) in all 12 bins; no optional stopping.** The
only new code is this lane's layout function for E and for R_zv and a copy of `tables` that calls it; J5 goes through
FWN1R's own `split_fn`. Gate: Delta chi^2 <= 4.

Fields per primary part: R, J5, E1, E2, E3, Ezv; at the anchors also TWB = R + 2 (E3 - R). Brackets (anchors, seeds 0
and 1): R, E1, E2, E3, Ezv under lambda_P x 0.5 and x 2, gamma 1.2 and 1.6, tau_eff x 0.9 and x 1.1, and the
measured-range pair 91.4 and 138.6 comoving kpc (Rorai et al. 2017, Table S2, z 3.0; PROVISIONAL, inherited).

## 4. Known answers (each that applies must pass, or the case on that footing is NO VERDICT)

- **KA-5:** the recomputed R and J5 flux P1D equal FWN1R's stored primary parts with |ratio - 1| <= 1e-6 at every
  mode k_v > 0 in all 96 files; J5's D and SE from this lane's parts equal FWN1R's stored values within 1e-6 relative;
  J5 still reads D - 2 SE > 4.
- **KA-C, KA-INF:** not recomputed; read from FWN1R's committed `fwn1r_grade.json`, where they must be passes.
- **KA-N:** the grid haloes above v*(z) equal JNT2's membership counts at every z and footing.
- **KA-F:** |<F> - exp(-tau_eff)| <= 1e-4 for every flux field.
- **KA-M, per case:** at the anchors the realised matter ratio (ratio of seed sums of P3D) at k 1, 3, 5 h/Mpc is within
  0.01 + 0.3 |E - 1| of the halo model's expected ratio.
- **KA-S, per case:** D_noise <= 0.1 max(D, 4) (FWN1R's rule).
- **KA-E (the exact junction, on the tables' profiles, every z and footing, every halo below v*(z)):**
  (i) M_E(r) = M_B(r) at every grid node r <= R_set, to 1e-12 relative; (ii) M_E(r_ta) = M_ta to 1e-9 relative;
  (iii) M_E non-decreasing (to 1e-9 M_ta); (iv) t >= 0; (v) with R_set forced to r_ta the row equals the control's
  (mode "B") to 1e-12, and with R_set forced to 0 it equals the reference's exactly; (vi) every halo above v*(z) has
  the reference's row exactly.
- **KA-Z (the surface reader):** (i) this lane's reader pointed at the `R_fold_kpc` column and multiplied by 3 equals
  FZS1's `rset_com(hb, foot, z, 3.0)` to 1e-12 relative for every halo, z and footing; (ii) pointed at `R_ta_kpc` it
  reproduces FLD1's RESULT table (R_ta at z 0: 19, 40, 88, 120, 190, 268, 325, 378, 476, 600 kpc at log M_b 7, 8, 9,
  9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, canonical) to the printed digits (0.6 kpc).

## 5. Twins (must bite, or no HOLDS for any case; FAILS is still given where D - 2 SE > 4)

- **TW-A, boundary removed at f = infinity:** not recomputed; read from FWN1R's committed grade file, where it must
  read "bites".
- **TW-B, difference doubled at E3:** anchor statistic of TWB against E3's; bites if the factor is >= 2.5 (linear
  response predicts 4). It gates every E case. Why a correct build must bite: the flux response to a small field
  difference is close to linear; it was 3.3 to 3.4 in FRZ6R.
- **Reported, not a gate (decided now):** the junction's own effect, D(E2) against FRZ6R's D(J2) and D(E3) against
  D(J3), with FWN1R's bite rule (ratio >= 1.25 or <= 0.8 and |difference| > 2 sqrt(SE^2 + SE^2)). If the junction makes
  no difference, that is a result about the junction, not a fault of the build, so it does not gate a label.

## 6. Labels

Per case E1, E2, E3, Ezv and footing (FWN1R section 5):

- **FOREST ROW HOLDS AT FLUX LEVEL** if every known answer that applies passes, both twins bite and D + 2 SE < 4.
- **FOREST ROW FAILS AT FLUX LEVEL** if D - 2 SE > 4.
- **NO VERDICT** otherwise, with the cause named.
- **FRAGILE** (bracket named) when one of the six frozen brackets' 12-bin estimates (D x A_br / A_prim on seeds 0 and
  1) lies on the other side of 4 from D. The measured-range reading is reported beside the label, never as the label.
  FWN1R's statement on resolution stands: the cell is 77 comoving kpc, so lambda_P x 0.5 is not resolved.

Lane words, per footing, from those labels:

- **Q1, the junction.** "THE HOLD SURVIVES THE EXACT JUNCTION AT f = <list>" naming every f of 2 and 3 where E reads
  HOLDS (FRAGILE named); "THE HOLD DOES NOT SURVIVE THE EXACT JUNCTION" if E2 and E3 both read FAILS; otherwise
  "NOT RESOLVED", each case's word given. If it does not survive, the record's forest holds at f = 2 and 3 belong to a
  layout whose inside is not the law, and that is said plainly in RESULT.md.
- **Q2, a settled radius with no free constant.** For each of E1 (the fold) and Ezv (the zero-velocity surface):
  "HOLDS WITH NO FREE CONSTANT (<surface>)" if it reads HOLDS (a hit awaiting a blind re-grade, not a pass);
  "FAILS (<surface>)" if it reads FAILS; otherwise "NOT RESOLVED (<surface>)".

A hold at flux level means "not excluded by the forest in this build". It does not separate the framework from LCDM.

## 7. Reported beside the labels (never a label of this lane)

- **Matter level, the record's convention:** each E case through JNT2's G1 route (the tables' R_cold fed to FRZ1's
  `forest_eval`, gate 4), with the word PASS or FAIL beside the number, next to JNT2's stored J numbers (f 2: 0.0492 /
  0.1456; f 3: 1.9898 / 6.4321). Reason it is not the label: since FRZ4 the record grades the forest row at flux
  level; the matter-level number multiplies the data by a matter power ratio with no gas physics.
- **Lensing, G4:** JNT2's G4 chain (`jnt2_lens.py`, ONE1's KiDS gate as SRH1 ran it) with the lens profile built by
  the exact junction (inside x_set: the law's halo unscaled; outside: X_in + t [C_R(x) - C_R(x_set)], t as in section
  1) at f = 1, 2, 3 and at R_zv(z_lens, M_b); JNT2's gate words (PASS / FAIL) reported. SRH1R found this gate cannot
  see f in a blind build; that stands. If the chain cannot be run today it is reported as not run.
- **How far the record's junction sits from the law at z = 0:** s under FZS1's junction at z = 0 for log M_b 8 to 11.5
  at f = 1.25, 2, 3 and at R_zv, from SRH1's lens `profile` (its own s). Stated beside the scorecard's "EQUALS THE LAW"
  rows as a fact about the built layout; no row is relabelled here.
- t (min, max) and s (min, max) per case, z and footing; per-bin D; R_F at k_v 0.003 / 0.01 / 0.03 s/km; the share of
  haloes below v*(z) whose R_zv is capped at r_ta; the ceiling plot points.

## 8. Build A (FWN1's build; a second, independently written implementation; reported when it lands)

A separate agent implements section 1 from this text alone (not from build B's code), in copies of FWN1's
`fwn1_tables.py`, `fwn1_run.py`, `fwn1_grade.py`, `fwn1_c0.py` with split keys SE2 (exact junction at 2 R_fold) and
SEzv (exact junction at R_zv) and control S5 (seeds 0 and 1), 12 seeds at z 2.2 and seed 0 at z 3.0, 4.4, 2.6, 3.4,
3.8, FWN1's known answers, twins, brackets and label rule (its section 8) unchanged, plus KA-E and KA-Z of this file on
its own tables. It does not read build B's parts, logs or outputs. Its heavy stage starts only after FWN2's build A has
finished. Read across (per footing, reported, never a label on the theory): HOLDS IN BOTH BUILDS / FAILS IN BOTH BUILDS /
THE BUILDS DISAGREE / NOT RESOLVED, for E2 and for Ezv. If build A has not landed when RESULT.md is first written, that
is stated and the read-across is added by a dated note.

## 9. What counts against (reported whatever the labels)

- Both ideas are post hoc. The window for f, the holds at f = 2 and 3 and the fails at f >= 5 were known when R_zv was
  proposed, and R_zv / R_fold (2.3 to 3.5 at the forest's redshifts) lies inside that window by inspection. A hold of
  Ezv is therefore expected of the family; what would be new is only that a surface with no free constant sits inside
  the window, with the law exact inside it.
- The exact junction is itself a choice for the outside (the remaining cold mass in the reference's shape). The
  action derives no junction.
- R_zv comes from FLD1's construction (radial shells, a softened point mass, a cold start at z 10, the law-dominated
  limit, no cold-component self-gravity beyond the enclosed charge); FLD1's start-redshift brackets move R_fold at z 2
  by 6 to 8 %.
- The gas inputs are provisional and inherited; build B's grid marginally resolves the smoothing scale; the forest gate
  fits no gas parameter (FRZ5).
- The boundary v*(z), the coverage line that fails (RC100), form B's failing rows and the fitted constants are untouched.

## 10. Compute

One build-B runner at first (2 threads, `nice -n 19`, one part per process, FWN1R's guards: wait unless free disk >=
10 GB and free + inactive memory >= 24 GB; stop below 8 GB disk or above 14 GB swap; physical-footprint guard 16 GB);
a second runner only when no more than two other heavy processes are alive. Small JSON parts, committed. `python3 -I
-B`. Nothing downloaded; nothing written outside this folder. About 3 h wall.

## 11. Hand estimate (before any number of this lane)

The exact junction moves cold mass across R_set (up to about half of what the law's halo holds there, in either
direction), out to r_ta, where FZS1's junction only reshapes the inside. So D should be larger than FZS1's at the same
f. Guess, build B, canonical (alt about 20 % higher): E1 0.02 to 0.5; E2 0.1 to 3; E3 2 to 20; Ezv 0.5 to 10.
Labels: E1 HOLDS 75 %; E2 HOLDS 55 %, NO VERDICT 15 %, FAILS 30 %; E3 FAILS 55 %, HOLDS 25 %; Ezv HOLDS 40 %,
FAILS 40 %. TW-B bites (90 %). The junction comparison bites at f = 3 (80 %). Matter level: E2 above the gate on alt
(60 %). Lensing G4: passes at f 2, 3 and R_zv (70 %); f = 1 uncertain (JNT2's J at f 1 read +2.003 / +2.037).
Low confidence throughout: nobody has computed this layout.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
