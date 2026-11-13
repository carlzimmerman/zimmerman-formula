# JNT2 FROZEN CRITERIA: the crossing-speed joint (law's layout below v*(z), cold dust above)

Written 2026-11-13, committed alone before any script or number of this lane. TEST lane: adopts nothing, relabels
nothing, registers nothing. Footings canonical (a0 = 9.3603e-11 m/s^2) and alt (1.1312e-10 m/s^2), graded separately,
never pooled. Cold dark energy is a gravitating field component; no particle. kappa = 1/2 and the share 5.41 are FITTED.
The settled-radius family (R_set = f x R_fold) is post hoc (chosen after FRZ1 failed); this boundary is post hoc to SRJ2
and JNT1. A blind twin (JNT2R) works on the same question; its folder is not opened by this lane.

## 1. The joint

**Source of the boundary.** `fable52_push/SHAPE_search/route_D_dark_energy_column.md`, check C5 (line 107 of its code):
the cold-clustering relation v^3 = 10 G M H with M = (1 + X) M_b, X = 5.41, meets the law's v^4 = G M_b a0 at one speed,
v* = a0 / (10 (1 + X) H). With H0 = 67.4 km/s/Mpc (route D's input) this is 669 / 808 km/s (canonical / alt).

**Redshift scaling (frozen).** v*(z) = v*(0) / E(z), E(z) = sqrt(Om (1 + z)^3 + 1 - Om), Om = 1 - 0.6847 (route D's
OL). a0 is held constant in z (physical), as FRZ1's a0c does. Equivalent mass form: v_L > v*(z) exactly when
M_b > M*(z) = v*(z)^4 / (G a0), i.e. when the law's flat speed (G M_b a0)^(1/4) exceeds v*(z). Hand values: log M*(0) =
13.21 / 13.45 (Msun), falling as -4 log E(z).

**The rule tested.** For each system at its redshift z: if its speed <= v*(z), the law's layout holds inside R_set =
f x R_fold (FLD1's fold radius via FZS1's `rfold_kpc`, FZS1's junction at R_set, the reference outside) exactly as in
SRH1 / SRJ1 / SRJ2's settled layout; if its speed > v*(z), the system keeps its share as cold dust in the reference layout
at every radius (f = 0 for that system). The law's layout inside R_set keeps FRZ1's own form choice at v_stiff
(galaxy / cluster form B) unchanged: v_stiff here is a layout ingredient, not the boundary.

**Membership (two rules; the model rule is PRIMARY and graded):**
- **Model virial speed (PRIMARY), the lemma's own convention:** v_L = (10 G M H(z))^(1/3), the 200 rho_crit(z) virial
  speed of the total mass M. For systems known by their baryons (SPARC, RC100, KiDS lenses and lens-table nodes):
  M = (1 + 5.41) M_b, so v_L > v*(z) iff M_b > M*(z). SPARC M_b: PD1's (for G3(b)) and FLD1's (for G3(a) coverage), as
  SRJ2. RC100: the table's logMbar. Lenses: M_b = k M_gal at the fitted k, as SRJ2's `lens_v`. For haloes on a mass grid
  (the forest): v200c of the halo, FRZ1's `v_vir(hb)` (M = M200c). For X-COP and Lovisari groups: SRJ1's `make_system`
  v200 from RB1's anchored M200 at 200 rho_crit(z) (M200 = (1 + 5.41) x anchored baryons, so this is the lemma's form).
- **Measured speed (SECONDARY, reported as a bracket; a changed row word under it marks the row FRAGILE):** SPARC Vflat
  (PD1 / Lelli table; if Vflat <= 0, the largest V_obs); RC100 the observed Vc_Re_kms; X-COP sqrt(G M_HSE(r_last) /
  r_last) (RB1's forward M_dyn at the r_last anchor); groups sqrt(G M500 / R500). KiDS lenses and forest haloes have no
  measured speed: model rule only (said in RESULT).
- **Reported only:** the FRZ1-halo speed (X ~ 56, SRJ2's `vgal`) against v*(z), to show how the bookkeeping moves the
  membership.

## 2. Rows (lines taken unchanged from the lanes that own them); f grid 0.75, 1.00, 1.25, 1.5, 2, 3

- **(M) membership.** Counts on each side of v*(z), both rules: SPARC 175; RC100 100 (by z bin < 1.5, 1.5-2, 2-2.5,
  >= 2.5); KiDS host-free lenses 40,667 (late / early) at the all-fit k of each f, and table nodes; X-COP 7 (+ R500
  anchor); Lovisari groups 20; forest grid haloes per z bin (count above, and the boundary M200c). Reported, not graded.
- **(G1) forest, matter level.** SRJ2's `srj2_forest.py` machinery (FRZ1's gate, FZS1 halo model, Delta chi^2 <= 4) with
  the split per halo at each z bin by v_vir > v*(z). Carried beside it, ungraded: SRF1 / SRF1R flux-level readings.
- **(G2) RC100.** SRH1's coverage line: every disc must be the law's at 2.2 R_e (2.2 R_e / R_fold <= f and the disc
  below v*(z)); 100 / 100 to pass. A disc above v*(z) is not covered at any f (the coverage row then FAILS ON COVERAGE).
  For discs above v*(z) the data row is SRJ3's: NO POWER, carried, not recomputed.
- **(G3) SPARC.** (a) SRH1 / SRJ2 coverage (R_last / R_fold <= f with FLD1 M_b, 175 / 175); (b) PD1's line (rms <= 0.066,
  |mean| <= 0.05, massive too) with galaxies above v* at g_N as SRJ2 graded it, if (a) fails. Any SPARC galaxy above
  v* under either rule gets JNT1's row S test (JNT1's jnt1.py statistics, members replaced); if none is above, that part
  is EMPTY (n = 0) and is not run.
- **(C) clusters and groups.** RB1's gates via SRJ1's `run_all` with SRJ2's `make_split` (boundary replaced): X-COP
  (a) q at r_last CONSISTENT, (a) R500 bracket (FRAGILE marker as SRJ1 / SRJ2), (b) shape bins |bin| <= 0.10;
  groups (c) q at R500 CONSISTENT.
- **(G4) KiDS by type.** SRJ2's `srj2_lens.py` (SRH1's gate: |z| <= 2 for all / late / early at 1.6 R_h, chi^2 <= 9.49,
  type difference |z| <= 2) with each table node at the reference (f = 0) when its node v_L > v*(z_node).

**Marks.** TRIVIAL: the joint equals the reference on that row (G1 Delta chi^2 < 1, SRJ2's mark; G4 max |dz| <= 0.10 and
|dchi^2| <= 0.10 against f = 0; clusters joint - reference = 0 on every statistic). EQUAL TO THE LAW: the joint equals
the boundary-removed settled family at the same f (no system above v*, or the same tolerances). NO POWER: as the owning
lane found (SRJ3 for RC100 data; G4 cannot see f, SRH1R) or n < 5 for any data row of this lane. A row that passes only
trivially never counts as support.

## 3. Labels per footing (primary membership)

1. **NO VERDICT** if any known answer fails, or TW-S / TW-0 fail to reproduce, or TW-H or TW-D fails to bite.
2. **JOINT FAILS ON <rows>** if some row fails at every grid f (say data or coverage). G2's coverage fails at every f
   as soon as one RC100 disc is above v*(z).
3. Else **JOINT COMPLETE ON POWERED ROWS [f window]**, the set of grid f at which G1, G2, G3, C and G4 all pass. A HIT, not
   a pass: it awaits the blind twin and an owner decision; the family is post hoc; the two constants stay fitted.
Also reported (not the label): the window of the rows other than G2.

## 4. Twins (separate *_MUTATE* outputs) and known answers

- **TW-S** boundary = FRZ1's v_stiff with SRJ2's membership (X ~ 56 halo): must reproduce SRJ2's words (G2 FAILS 31 / 22;
  G4 FAILS at f 1; G1 TRIVIAL hold; clusters TRIVIAL). **TW-0** boundary removed (v* -> infinity): must reproduce SRH1's
  words at f 1 (G1 FAIL 38.741 / 36.658; G4 FAIL) and SRJ1's (X-COP shape FAILS at f 1). **TW-H** v*/2 and **TW-D** 2 v*,
  run at f 1.25 and 2 on G1, G4, C (G2 / G3 counts too): bite = a row word changes at either f, or a powered statistic
  moves beyond G1 |dDelta chi^2| > 1, G4 early |dz| > 0.10, C median q > 0.02 or a shape bin > 0.05. G2 counts alone do
  not count as a bite (coverage, not data).
- **KA-1** TW-S G1 at f 1 equals SRJ2's stored dchi2 (0.048 / 0.081) to 1e-6 relative, and its G4 equals SRJ2's stored
  on_f1.00 (z early +2.0121 / +2.0369) to 0.005. **KA-2** TW-0 G1 f 1 equals 38.741 / 36.658 (FZS1 / SRH1) to 0.01 and G4
  f 1 equals SRH1's stored f1.00 to 0.005. **KA-3** v*(0) from SI constants rounds to 669 / 808 km/s. **KA-0** f = 0 equals
  the reference (G1 0; G4 = SRH1 f0; clusters = rb1.json to 1e-6).

## 5. Expectation and hand estimate (before any number)

- v*(z) canonical / alt: 669 / 808 (z 0), ~374 / 451 (z 1), ~221 / 267 (z 2), ~178 / 215 (z 2.5).
- SPARC: 0 above under both rules (M_b <= ~3e11 against 1.6e13; Vflat <= ~330 km/s). G3 EQUAL TO THE LAW, holds.
- KiDS: ~0 lenses above (M*(0.3) ~ 8e12). G4 EQUAL TO THE LAW = SRH1's: FAIL at 0.75 and 1, PASS from 1.25.
- X-COP all above (TRIVIAL hold, R500 FRAGILE); groups all below on the model rule (v_L ~ 300-670), 0-1 above on the
  measured rule; groups get the law's layout, as SRJ1 (hold, q ~ 0.65).
- Forest: the boundary at z 2.2 falls near M200c ~ 9e11 Msun, below SRJ2's; more haloes are the reference's, so G1 holds,
  TRIVIAL at f <= 2; f = 3 uncertain.
- RC100: ~10-30 / ~5-20 discs above on the model rule at z >= 2, more on the measured rule (Vc ~ 250-350 km/s). So my
  expected label is **JOINT FAILS ON G2 (coverage) on both footings**, with the other rows' window [1.25, 2 or 3].
  P(G2 passes on a footing) ~ 0.1. TW-H may fail to bite (P ~ 0.35), which would make the label NO VERDICT.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
