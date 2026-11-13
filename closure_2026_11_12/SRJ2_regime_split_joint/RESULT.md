# SRJ2 RESULT: the regime-split settled joint

**JOINT FAILS ON G2, G3, G4 / JOINT FAILS ON G2, G4 (canonical / alt), FRAGILE (G4 passes at f = 1.25; the inherited
cluster R500 bracket crosses). TRIVIAL beside the forest and beside clusters and groups.**

This joint is post hoc three times over: to FRZ1's forest fail, to FZS1's remaining miss, and to SRJ1's cluster fail. It
was written to remove exactly those misses, and it does remove them, but only by handing the forest and the clusters back
to the cold reference. It then fails on high-redshift rotation curves (both footings), on KiDS early-type lenses by 0.01 /
0.04 sigma (both), and on SPARC under the frozen reading (canonical only). Nothing here is a pass of the theory.
TEST lane. Criteria b8a99499ad (alone, before any script or number). Scripts and outputs 7671345425. No amendment. Footings
never pooled. Cold dark energy is a gravitating field component; no particle. SRF1 and SRF1R were not opened.

## What the joint is

The law's layout holds only inside R_set = f x R_fold of galaxy-regime systems (FRZ1's v_vir <= v_stiff, 265.8 / 288.1
km/s, read from FRZ1's code). Everywhere else the cold dark energy keeps the reference layout. FZS1's junction applies at
R_set. f = 1.00 is graded; 0.75 and 1.25 are fixed points.

## Rows at f = 1.00 (0.75 ; 1.25), canonical / alt

| row | line | joint | word |
|---|---|---|---|
| G1 forest, matter level, Delta chi^2 | <= 4 | 0.048 (0.014 ; 0.089) / 0.081 (0.023 ; 0.153) | holds, **TRIVIAL** (< 1) |
| G2 RC100 covered at 2.2 R_e | 100 / 100 | 69 / 78 at every f (31 / 22 galaxies cluster-regime) | **FAILS** |
| G3 SPARC, (a) coverage | 175 / 175 | 172 / 175 (3 cluster-regime) / 175 / 175 | canonical (a) fails |
| G3 SPARC, (b) graded (cluster-regime at g_N) | rms <= 0.066, massive too | canonical 0.0968, massive 0.0886 | canonical **FAILS** / alt holds by (a) |
| G4 early-type z at 1.6 R_h | abs(z) <= 2 | +2.012 (+2.142 ; +1.843) / +2.037 (+2.172 ; +1.852) | **FAILS**, FRAGILE (1.25) |
| G4 all / late z, chi^2, type diff | 2, 2, 9.49, 2 | +1.70 / -0.82, 3.75, +1.41 / +1.72 / -0.81, 3.81, +1.41 | hold |
| X-COP (a) q at r_last; (b) shape bins | CONSISTENT; abs <= 0.10 | 1.095 [0.885, 1.259]; -0.007 / +0.033 / +0.006 / -0.030 / -0.041 | holds, **TRIVIAL**, FRAGILE (R500: 1.057 [1.046, 1.072] FAILS) |
| Lovisari groups q at R500 | CONSISTENT | 0.597 [0.556, 0.637] | holds, **TRIVIAL** |

The cluster and group numbers are RB1's reference numbers, recomputed (2e-13 from `rb1.json`). Joint minus reference is
0 exactly on every gate statistic. Both footings agree.

## Who sits on which side of v_stiff

- **Clusters and groups: all above.** X-COP v200 1213 to 1728 km/s. Lovisari groups 353 to 666 km/s. None is below, so
  no joint was computed for any of them.
- **Forest haloes:** 155 / 151 of FRZ1's 321 mass-grid haloes are cluster-regime at z 2.2. That is a count of grid points.
- **RC100: 31 / 22 of 100 are cluster-regime.** At z ~ 2 the boundary sits at log M_b 10.93 / 11.04. The reason is that
  FRZ1's halo for a galaxy has M_ta = X M_b / (1 - FB) with X about 56. Those 31 / 22 galaxies have R_set = 0, so the law
  covers none of their radii at any f.
- **SPARC, z 0 (boundary log M_b 11.32 / 11.43).**
  - With FLD1's M_b: 3 / 0 above (NGC6195, UGC02487, UGC02885).
  - With PD1's M_b: 9 / 2 above.
- **KiDS (40,667 host-free lenses: 10,282 late, 30,385 early).** Boundary log M_b 11.24 / 11.35 at z 0.3.
  - At the all-fit k (1.459 / 1.446): 224 / 0 above (118 late, 106 early / none).
  - At f 1.25: 1,671 / 0. At f 2: 8,091 / 43.

## Why each row came out as it did

- **G1.** Galaxy-regime haloes change U(k) by at most 0.3 %, as FZS1's diagnostic showed. R_cold is 1.00149 / 1.00207 at
  k 10, z 2.2. The forest then sees almost nothing. The joint leaves the forest to the cold reference.
- **G2.** This is the new fail. The haloes the joint must hand back to the reference to save the forest are the same mass
  range that hosts RC100's massive discs at z 1 to 2.5. G2 is a coverage line, not a fit to their curves. Whether the
  reference layout fits those 31 / 22 curves was not tested here.
- **G3, canonical.** The fail rests on the frozen reading: cluster-regime galaxies at g = g_N, which is SRH1's truncated
  form at R_trunc = 0. Under the joint's own layout (reference NFW cold mass) the same line holds: rms 0.0640, massive
  0.0387 canonical; 0.0559 / 0.0332 alt. That reading was reported, not graded, as frozen. Read it as a soft fail.
- **G4.** Almost no lenses cross the boundary at f = 1. So the joint reads like SRH1's f = 1 row: +2.003 -> +2.012
  canonical, and unchanged on alt. It fails the early-type line by 0.012 / 0.037 sigma. f = 1.25 passes (+1.84 / +1.85).
  SRH1R found this lensing gate cannot tell one f from another.
- **Clusters and groups.** By construction they equal the reference, which passes RB1's gates. The R500 aperture bracket
  fails for the reference too.

## Checks and twins (all pass or bite)

- **C1, split off at f 1:**
  - G1 38.741 / 36.658 = FZS1 (R_cold to 0).
  - G2 0.391237 / 0.391383, G3(a) 0.467132 / 0.467178 = SRH1.
  - G4 equals SRH1's stored f 1 row exactly.
- **C2, f 0:** G1 0; G4 equals SRH1's f0 row exactly.
- **C3:** VST and v_vir equal FRZ1's, to 0.
- **C4:** M_S conserves M_ta to 6.6e-16 and never decreases.
- **C5:** RB1 reproduced, 2.4e-13.
- **TW-C (law's layout restored in cluster-regime haloes):** 38.741 / 36.658 = FZS1. Bites; exits 1.
- **TW-F2 (joint at f 2):**
  - G1 rises only to 0.42 / 0.58, so the G1 part does not bite.
  - The G4 early z falls +2.012 -> +1.420 and +2.037 -> +1.142, so it bites. Exits 1.

## What the joint gives up, and what it leaves open

- **The forest and the clusters are now the reference's,** not the law's. The joint predicts nothing different there.
- **At z = 0 it removes form B's redistribution.** R_tot at k 1 / 3 is 0.9975 / 0.9783, against the reference's 0.9975 /
  0.9784; CO1's law-to-r_ta value is 1.0033 / 1.0282. That is the content behind form B's lensing amplitude.
- **Every system above v_stiff loses the law,** including about a quarter to a third of RC100 and the most massive SPARC
  galaxies.
- **Not addressed:**
  - the weak-lensing amplitude;
  - hosted dwarfs;
  - the two fitted constants;
  - why v_stiff, a form choice with no bracket in FRZ1 or PD1, should be a layout switch.

## Estimates against the outcome

- **The lead's:** forest TRIVIAL hold, right. Clusters and groups hold, right (TRIVIAL). G4 fails by a fraction of a
  sigma, right (0.01 / 0.04). Rotation curves unchanged, **wrong**: G2 fails on both footings.
- **Mine:** G1 TRIVIAL, right. Clusters and groups TRIVIAL with FRAGILE, right. G4 fail at f 1, right; my 1.25 fail,
  wrong (it passes). G2 fail, right. G3 at risk, right on canonical only.

## What is not verified

- The regime of an observed galaxy uses FRZ1's halo (X about 56 to 59, Duffy c, Delta_ta). A smaller X would move the
  boundary up and the G2 count down. No bracket was frozen for that.
- The G4 table switches at grid nodes, and the trilinear interpolation blends across one cell. G4 neighbours keep ONE1's
  halos.
- G1 inherits FRZ1's halo model (PROVISIONAL inputs) and is at matter level only.
- G2 is coverage only.

## Files

`FROZEN_CRITERIA.md` (b8a99499ad). Scripts and outputs (7671345425):
- `srj2_hm.py`, `srj2_forest.py` (G1, TW-C, TW-F2);
- `srj2_rc.py` (G2, G3);
- `srj2_lens.py` (G4, TW-F2);
- `srj2_clusters.py`;
- `srj2_grade.py`.

The console logs stay local (gitignored). Owners' code is executed read-only from its own path. Nothing was fetched or
pushed.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
