# SRJ2 FROZEN CRITERIA: the regime-split settled joint on the forest, rotation curves, galaxy lensing, clusters and groups

Committed alone, before any SRJ2 script exists and before any number of the split joint has been computed by anyone in
this lane. TEST lane, quarantined. Relabels nothing, adopts nothing, registers nothing. Footings canonical (a0 9.3603e-11)
and alt (1.1312e-10 m/s^2), graded separately, never pooled. Cold dark energy is a gravitating field component; no particle
is added anywhere. "The cold reference" is the record's own reference layout, not a standard graded against.

**This joint is post hoc three times over:** to FRZ1's forest fail (9916 / 9009), to FZS1's remaining miss at R_set = R_fold
(38.7 / 36.7, driven by cluster-regime haloes), and to SRJ1's cluster fail (X-COP inner shape +0.153 / +0.144 dex against a
line of 0.10, while the reference passes at -0.007). It was written to remove exactly those misses. Nothing here can be a
pass of the theory. A hold on every row is a one-sided hold that needs an independent blind re-grade. It is not in PAPER72.

## 0. What was seen before this freeze

- The lead's brief, with its numbers (FRZ1 9916 / 9009; FZS1 38.7 / 36.7; FZS1's diagnostic U_S / U_R 1.0000 to 1.0028 for
  1e10 to 1e12 Msun/h and 0.9909 / 0.8043 at 1e13; SRH1 WINDOW EMPTY, forest f <= 0.70, lensing f >= about 1.0, early-type
  lenses 0.003 sigma over the line at f = 1.00; SRH1R cannot tell f apart; SRJ1 +0.153 / +0.144 against 0.10, reference
  -0.007) and its estimate (below, section 8).
- FZS1: FROZEN_CRITERIA, RESULT, `fzs1_hm.py`, `fzs1_diag.out`. SRH1: FROZEN_CRITERIA, RESULT, AMENDMENT_A1, `srh1_lens.py`,
  `srh1_rc.py`, `srh1_forest.py`, the diff of `srh1_hm.py` against `fzs1_hm.py`, `srh1_rc.out`, the tail of `srh1_hm.out`,
  the head of `srh1_grade.out`, and from `srh1_lens.json` the gate lines at f 0, 0.75, 1.00, 1.25, 2.00 (canonical z all /
  late / early, chi^2, type-difference z: f 0 +1.8925 / -0.7772 / +2.1914, 4.4265, +1.4257; f 1.00 +1.6874 / -0.8191 /
  +2.0030, 3.7039, +1.4044; f 0.75 +1.8367 / -0.7856 / +2.1407, 4.2219; f 1.25 +1.4782 / -0.8679 / +1.8127, 3.0476; f 2.00
  +0.6458 / -1.0755 / +1.0358, 1.2648; alt f 0 +1.9176 / -0.7732 / +2.2149, 4.5146, +1.4300; f 1.00 +1.7218 / -0.8134 /
  +2.0369, 3.8126, +1.4106; f 0.75 +1.8676 / -0.7810 / +2.1715, 4.3289; f 1.25 +1.5187 / -0.8608 / +1.8517, 3.1617; f 2.00
  +0.7025 / -1.0648 / +1.0911, 1.3339). SRH1R's commit subject.
- FRZ1: `frz1_hm.py` lines 1 to 135 (layout, v_vir, VST, Xsh), its criteria lines 28 to 70, its RESULT bracket table.
- SRJ1: RESULT, `srj1.py` (constants, loaders, make_system, gates), and two lines of `srj1.out` ("systems with v200 <=
  v_stiff: 0" for the Lovisari groups, both footings).
- CO1 and PD1 grep hits for v_stiff (section 5).
- **Not computed or seen:** the v_vir of any SPARC galaxy, RC100 galaxy or KiDS lens; any number of the split joint on any
  row. SRF1 and SRF1R were not opened and will not be.

## 1. The joint (graded statement)

**REGIME-SPLIT SETTLED JOINT.** The law's layout holds only inside R_set = f x R_fold of galaxy-regime systems (v_vir <=
v_stiff). Everywhere else, outside R_set and at all radii in cluster-regime systems (v_vir > v_stiff), the cold dark energy
keeps the reference layout. FZS1's junction rule at R_set (enclosed cold mass at R_set equal to the reference's, s =
C_R(R_set) / C_B(R_set)). R_set, R_fold, the cap at r_ta and the junction are FZS1's / SRH1's, unchanged.

- **f = 1.00 is primary.** f = 0.75 and f = 1.25 are two fixed points reported beside it (they set FRAGILE, section 4).
  No scan.
- **The regime boundary and v_stiff are FRZ1's, read from its code, unchanged:** v_vir = sqrt(G M200c (1 + z) / r200c) with
  FRZ1's comoving units (its `v_vir`), regime "cluster" iff v_vir > VST, VST = 265.8 / 288.1 km/s, constant in z. No new
  number.
- **The only change from FZS1's rule:** cluster-regime systems keep the reference layout inside R_set too.

### How each row decides a system's regime (each row's own halo, nothing new)

- **G1 (forest):** FRZ1's halo population at each DESI bin; regime by FRZ1's `v_vir(hb) > VST` (FZS1's `regime`). Cluster
  regime: M_S(r) = M_R(r) at every r (FRZ1 mode "Rb").
- **G4 (KiDS lenses):** SRH1's own lens halo: M_ta = X M_b h / (1 - FB), X = ONE1's XP, at z_lens, FRZ1's
  `halo_basics_z` with Duffy c(M, z) and Delta_ta(z) (SRH1's `halo`). v_vir from that halo's M200c, r200c with FRZ1's formula
  and G. Applied on SRH1's table grid (log M_b step 0.05, z step 0.05): at cluster-regime nodes the table holds the
  reference profile (SRH1's f = 0 profile). Since M_b = k M_gal with k fitted, a lens's regime follows the fitted k. The
  trilinear interpolation blends the two profiles across one table cell at the boundary (disclosed, not bracketed).
  Neighbours: ONE1's counted-once halos as in SRH1 (unchanged). Counts reported: host-free lenses (1.0 R_h set) above and
  below v_stiff at each fit's k, by type.
- **G2 (RC100):** each galaxy's halo M_ta = Xsh(z_i) M_b h / (1 - FB) (FRZ1's X by redshift: z < 1 the z = 0 median,
  else the z = 1 median), M_b = 10^logM, at z_i with FRZ1's `set_z(z_i)` concentration and Delta_ta. Cluster regime: R_set
  = 0, so the galaxy is not covered.
- **G3 (SPARC):** the same halo at z = 0 (X = FRZ1's z = 0 median, SRH1's `ref_halo` construction). Line (a) uses FLD1's M_b
  (0.5 L36 + 1.33 M_HI); line (b) uses PD1's M_b (`Mbs` from the baryon curve). Each line decides the regime with its own
  M_b. Cluster regime: R_set = 0. In (a) the galaxy is not covered. In (b) SRH1's truncated form at R_trunc = 0 is its
  limit, g = g_N (no law term, no leftover).
  - Reported beside (not graded, not a bracket): (b) with cluster-regime galaxies read as the joint's own layout, g = g_N +
    G C_R(R) / R^2 (SRH1's family-layout form with R_set = 0, the reference NFW cold mass).
- **Clusters and groups:** SRJ1's `make_system` v200 = sqrt(G M200 / R200) at 200 rho_crit(z) (RB1's anchored M200; FRZ1's
  definition). Every system with v200 > v_stiff keeps the reference: RB1's numbers, as SRJ1's K1 reproduced them, are
  quoted and recomputed with SRJ1's code at f = 0. Any X-COP cluster (gates a, b) or Lovisari group (gate c) with v200 <=
  v_stiff gets the joint computed with SRJ1's `make_system` at f (its law layout with fc = 0 there), and its gate statistic
  is recomputed with that system changed.

## 2. Rows and gates (copied unchanged from their owning lanes)

- **G1 forest, matter level.** FZS1's machinery (`fzs1_hm.py` / `fzs1_forest.py`, copied with only the case list, the
  layout switch and the output names changed; they execute FRZ1's prefixes unchanged). DESI DR1 P1D, 755 points, full
  covariance, form B's own CLASS reference. **Holds iff Delta chi^2 <= 4.** Flux level is not computed here.
- **G2 high-z rotation curves.** SRH1's line: holds iff 2.2 R_e <= R_set(z_i, M_i) for all 100 RC100 galaxies.
- **G3 SPARC.** SRH1's line: (a) all 175 R_last <= R_set(0, M_b); if (a) fails, (b) PD1's P2-SPARC line with R_trunc =
  R_set: rms <= 0.0660 and |mean| <= 0.05, for all and for the massive tail (Vflat >= 250 km/s). Holds iff (a) or (b).
- **G4 KiDS lensing by type.** ONE1's frozen gate as SRH1 ran it at the 1.6 R_h veto, KO1 tie rule, k fitted on the inner
  window: G-K1 |z| <= 2 for all, late, early; G-K2 chi^2 <= 9.49; G-K3 type difference |z| <= 2.
- **Clusters (X-COP) and groups (Lovisari).** RB1's gates as SRJ1 ran them: (a) X-COP q at r_last CONSISTENT; (b) X-COP
  shape, every graded bin |D| <= 0.10 dex; (c) groups q at R500 CONSISTENT. Brackets inherited from SRJ1 (R500 aperture,
  M_NFW) are reported; the R500 aperture bracket sets FRAGILE as in SRJ1.

## 3. Words (per footing, at f = 1.00)

- **JOINT HOLDS ON EVERY GRADED ROW (ONE-SIDED):** G1, G2, G3, G4 and the cluster/group gates all hold.
- **JOINT FAILS ON <row(s)>:** any row fails; every failing row is named.
- **NO VERDICT:** a check of section 6 fails, a twin does not bite, or a row cannot be evaluated (no k crossing, a run
  does not finish).
- **FRAGILE:** beside a word if f = 0.75 or f = 1.25 lands on the other side of any row's line from f = 1.00, or if an
  inherited cluster bracket crosses; the crossing points are named. The word itself does not change.
- **TRIVIAL:** beside any row where the joint's prediction is indistinguishable from the reference's:
  - G1: the joint's Delta chi^2 (the reference's is 0 by construction) is below 1.
  - G4: every gate z (all, late, early, type difference) within 0.10 and chi^2 within 0.10 of the reference row (f = 0).
  - Clusters / groups: every graded system above v_stiff (the joint equals the reference by construction, difference 0).
  - G2, G3: TRIVIAL does not apply (the reference covers no galaxy: SRH1's f = 0 G2 fails). For them the RESULT states
    whether the split changed SRH1's f row at all.

## 4. Brackets (fixed now; no scanning)

- f = 0.75 and f = 1.25 (all rows).
- **v_stiff: no bracket exists in FRZ1 or PD1.** FRZ1's criteria table lists v_stiff as a form choice, constant in z, not
  bracketed; FRZ1's RESULT bracket table has no v_stiff entry; PD1 A1 / A2 record v_stiff = 265.8 / 288.1 with no bracket.
  CO1 carries a different bracket (regime boundary at M200m 1e13 Msun/h instead of v_stiff); it is CO1's, it replaces the
  boundary rather than moving v_stiff, and it is not used. So no v_stiff bracket is run.
- Inherited cluster brackets from SRJ1/RB1 (R500 aperture; M_NFW at r_last), reported.

## 5. Reported, never graded

- z = 0 redistribution factor R_tot at k 1 / 3 h/Mpc under the joint at f = 1 (FZS1's z = 0 table), beside SRH1's f = 0
  and f = 1 values: what the joint does to form B's lensing-amplitude content.
- G1 per-bin Delta chi^2; the number of cluster-regime haloes per DESI bin.
- G4 per-type numbers, the counts of lenses on each side, k.
- G3(b) with cluster-regime galaxies read with the reference NFW (section 1).
- G2 / G3 names of the cluster-regime galaxies and their v_vir.

## 6. Checks (any failure: NO VERDICT)

- **C1, split off at f = 1 reproduces FZS1 and SRH1's f = 1.00 row:** G1 38.741 / 36.658 (+- 0.01); G2 lower limit
  0.3912 / 0.3914 and 100 / 100 covered (1e-4); G3(a) 0.4671 / 0.4672 and 175 / 175 covered; G4 z all / late / early and
  chi^2 equal SRH1's stored values (+- 0.005 in z, +- 0.01 in chi^2) and the status FAIL / FAIL.
- **C2, f = 0 reproduces SRH1's reference row:** G1 0 (|value| <= 1e-10); G4 equals SRH1's f0 row (same tolerances);
  G2 fails.
- **C3, regime constants read from FRZ1's code:** VST = 265.8 / 288.1 and FRZ1's `v_vir` formula; the lane's own v_vir
  function equals FRZ1's `v_vir` on FRZ1's own halo list at z = 2.2 and z = 0 to 1e-12.
- **C4:** inside the G1 copy, FZS1's KA-0 (R_set = 0 gives 1) and FRZ1's KA2 / KA3 pass; the split joint's M_S is
  non-decreasing and conserves M_ta at z = 3 (FZS1's KA-M) for f = 0.75, 1, 1.25.
- **C5:** SRJ1's K1 (f = 0 against `rb1.json`) re-run inside this lane's cluster check, 1e-6.

## 7. Mutation twins (each must bite, each writes `_MUTATE` outputs and exits 1)

- **TW-C, the law's layout restored in cluster-regime systems (f = 1):** this is FZS1's rule, so G1 must return FZS1's
  38.741 / 36.658 (+- 0.01). It bites if that holds and it differs from the graded joint's G1 by more than 1. (It is the same
  computation as check C1; disclosed.)
- **TW-F2, the joint at f = 2:** must move as SRH1's table moves from f 1 to f 2 (G1 up, G4 early-type z down). It bites if
  G1 rises by more than 1 or the canonical G4 early-type z falls by more than 0.10, against the joint's own f = 1 values.

## 8. Estimates before any number (disclosed; may be wrong)

**The lead's (UNVERIFIED, possibly wrong):** G1 falls far under the gate (galaxy-regime profiles barely change): a TRIVIAL
hold that leaves the forest to the cold reference. G2 and G3 unchanged. G4 at risk: moving massive early-type lenses to the
reference could push f = 1.00 back toward the reference's miss (+2.19 early). Likeliest: holds on forest, rotation curves,
clusters and groups, lensing by type failing by a fraction of a sigma on one sub-line.

**Mine:** G1 TRIVIAL hold (Delta chi^2 under 1, 85 %). Clusters and groups: all above v_stiff, TRIVIAL hold with the
inherited R500 FRAGILE (90 %). G4: early-type z at f = 1 moves from +2.003 toward +2.19, FAIL at f = 1.00 and probably at
1.25 too (65 %). **G2 and G3 are not safe:** with X near 56 to 59, a galaxy of M_b about 1.5e11 Msun sits in a halo whose
v_vir is near v_stiff at z = 0, higher at z ~ 2. If any RC100 galaxy is cluster-regime, G2 fails at every f (60 %); if any
SPARC galaxy is, G3(a) fails and G3 turns on (b), where g = g_N for the massive galaxies may fail the massive-tail line
(40 %). So my likeliest word is JOINT FAILS ON G2 and G4 (one or both), not a one-sided hold.

## 9. Files (planned)

- `srj2_hm.py` -> `srj2_hm.json` / `.out` (G1 halo model; copy of FZS1's with the case list and the regime switch).
- `srj2_forest.py` -> `srj2_forest_<footing>.json` / `.out` (G1 gate).
- `srj2_rc.py` -> `srj2_rc.json` / `.out` (G2, G3).
- `srj2_lens.py` -> `srj2_lens.json` / `.out` (G4).
- `srj2_clusters.py` -> `srj2_clusters.json` / `.out` (regime check of X-COP and groups, reference numbers).
- Twin outputs `*_MUTATE.*`; `srj2_grade.py` -> `srj2_grade.json` / `.out` (words).
- `RESULT.md` last. Any change after numbers: `AMENDMENT_A1.md`, committed alone, post hoc, frozen word kept beside.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
