# NH2: NGC 1052's measured mass against what tides on DF2 / DF4 need under form B

**Label as frozen: NO VERDICT / NO VERDICT** (canonical / alt). Two known answers fail: KA2 (KT2017's R_g) and KA4c
(mock-group estimators biased high). The criteria say grading is read only after every known answer passes.

**Under the post hoc reading A1** (named below; both failures make the group ceiling looser, never tighter, and neither
touches the GC ceiling):
- **DF4: TIDES CANNOT REACH / TIDES CANNOT REACH**, at 13.5, 19.4 and 20 Mpc. NGC 1052 cannot hold the ~1.4e14 Msun
  inside 165 kpc that B needs. Two independent ceilings give at most 0.32 to 0.41 of the need at 19.4 to 20 Mpc
  (0.65 to 0.82 at 13.5): the GC mass with a mean density that does not rise outward, and the whole group's mass.
- **DF2: NOT DECIDED / NOT DECIDED.** Only the GC ceiling falls below the need: 0.52 / 0.45 of it at 20 Mpc,
  0.55 / 0.47 at 19.4. At 13.5 Mpc canonical it does not (1.08). No tracer at or beyond 79 kpc confirms it. The group's
  members allow 1.7 to 5.2e13 Msun at 2 sigma (virial to radial PME), above DF2's 1.2e13 need.

**What this does to PAPER72 open item 9.** DF4 stays a LOW row that form B cannot rescue, now against a measured host,
not just "no measured mass on disk". DF2 stays open. The deciding measurement for DF2 is still a mass tracer at 50 to
80 kpc. **Row S:** B's own NGC 1052 (1e11 Msun of baryons under the law; the cap at 59.5 M_b binds only beyond
666 / 732 kpc) matches the GC mass inside 40 kpc at every distance and on both footings (B HOST CONSISTENT). For example,
at 20 Mpc canonical, B gives 3.87e11 and the GCs give 3.99e11, with a 2-sigma span of [1.9e11, 8.1e11].

TEST lane. It adopts nothing, relabels nothing (RB2's labels stand) and registers nothing. kappa = 1/2 FITTED; not theory
closed. Cold dark energy is a gravitating field component, never a particle. The footings are never pooled. Criteria:
FROZEN_CRITERIA.md, committed alone as 7d6ec1b5e7 before any script or number.

## Numbers per radius, footing and distance (nh2.out)

M_need is RB2's need, recomputed at each distance with RB2's own code (KA3 reproduces it at 20 Mpc exactly). C1 is the
GC ceiling: the largest 97.7th-percentile tracer mass over 27 (alpha, gamma, beta) corners, times (d / r_out)^3.
C3 is the whole group's ceiling: the largest 97.7th percentile of the virial, PME-isotropic and PME-radial estimators.
C2 is the outer-tracer Monte Carlo; it shows p_max over 48 corners for C2a (KT2017 members) and C2b (adding DF2 / DF4's
cited velocities). All masses are in Msun.

| D (Mpc) | dwarf | d (kpc) | footing | M_need | B's own M(<d) | C1 ceiling (/ need) | C2a / C2b p_max | C3 ceiling (/ need) | cell |
|---|---|---|---|---|---|---|---|---|---|
| 13.5 | DF2 | 53.5 | can | 3.76e12 | 4.92e11 | 4.05e12 (1.08) | 1.00 / 1.00 | 3.44e13 (9.13) | NOT DECIDED (no ceiling below) |
| 13.5 | DF2 | 53.5 | alt | 4.44e12 | 5.35e11 | 4.05e12 (0.91) | 1.00 / 1.00 | 3.44e13 (7.74) | NOT DECIDED (C1 only) |
| 13.5 | DF4 | 111.6 | can | 4.46e13 | 9.66e11 | 3.67e13 (0.82) | 0.40 / 0.32 | 3.44e13 (0.77) | CANNOT REACH |
| 13.5 | DF4 | 111.6 | alt | 5.28e13 | 1.06e12 | 3.67e13 (0.70) | 0.28 / 0.22 | 3.44e13 (0.65) | CANNOT REACH |
| 19.4 | DF2 | 76.9 | can | 1.07e13 | 6.82e11 | 5.85e12 (0.55) | 1.00 / 1.00 | 4.96e13 (4.64) | NOT DECIDED (C1 only) |
| 19.4 | DF2 | 76.9 | alt | 1.24e13 | 7.45e11 | 5.85e12 (0.47) | 1.00 / 1.00 | 4.96e13 (4.00) | NOT DECIDED (C1 only) |
| 19.4 | DF4 | 160.4 | can | 1.28e14 | 1.37e12 | 5.30e13 (0.41) | 0.069 / 0.047 | 4.96e13 (0.39) | CANNOT REACH |
| 19.4 | DF4 | 160.4 | alt | 1.49e14 | 1.50e12 | 5.30e13 (0.36) | 0.041 / 0.027 | 4.96e13 (0.33) | CANNOT REACH |
| 20.0 | DF2 | 79.3 | can | 1.16e13 | 7.02e11 | 5.99e12 (0.52) | 1.00 / 1.00 | 5.24e13 (4.51) | NOT DECIDED (C1 only) |
| 20.0 | DF2 | 79.3 | alt | 1.35e13 | 7.66e11 | 5.99e12 (0.45) | 1.00 / 1.00 | 5.24e13 (3.89) | NOT DECIDED (C1 only) |
| 20.0 | DF4 | 165.3 | can | 1.40e14 | 1.41e12 | 5.43e13 (0.39) | 0.060 / 0.038 | 5.24e13 (0.38) | CANNOT REACH |
| 20.0 | DF4 | 165.3 | alt | 1.62e14 | 1.54e12 | 5.43e13 (0.34) | 0.038 / 0.019 | 5.24e13 (0.32) | CANNOT REACH |

The floor for CAN REACH is the smallest 2.3rd-percentile GC mass, 1.3 to 1.9e11. That is 2 to 3 orders of magnitude
below every need. Both dwarfs stay LOW at all three distances.

**Measured masses (D 19.4 / 20 Mpc):**
- GC tracer mass (alpha 0.22, gamma 2.9, isotropic): 3.87e11 inside 39.5 kpc and 3.99e11 inside 40.7 kpc. The
  bootstrap 2-sigma range is [2.8, 5.2]e11; the span over all corners is [1.8, 8.1]e11.
- Whole group (16 members): sigma_v 144 km/s. Virial 4.9 to 5.0e12; PME isotropic 1.42 to 1.46e13; PME radial 2.8 to
  2.9e13.
- HI (van Gorkom 1986 via Forbes+19, reported, not raw): 3.1e11 inside 23 kpc. B gives 2.45e11 there (canonical).

## Why DF2 is not decided and DF4 is

- B's need is a minimum **mean density** inside d, because the Jacobi condition goes with M(<d)/d^3.
- The GCs measure the mean density inside 40 kpc well. Any density that does not rise outward caps the mean density
  beyond that.
- For DF4, two independent bounds agree. The GC ceiling and the whole group's mass both sit near 5e13. B needs 1.3 to
  1.6e14 at 19.4 to 20 Mpc. Even the most lenient group estimator (PME with radial orbits, which KA4 shows is biased
  2 to 4 times high) stays below it.
- For DF2, the group allows enough mass (2-sigma ceilings 1.7e13 virial to 5.2e13 radial PME, against a 1.2e13 need).
  Only the density argument puts that mass outside 79 kpc.
- The outer tracers (C2) cannot help. A Monte Carlo cannot tell mass inside 79 kpc from mass at 300 kpc, and the group's
  members move fast: 13 members beyond 79 kpc give p = 1.0, so they welcome a heavy host. As written in the criteria
  beforehand, the few galaxies beyond 40 kpc make any estimate there weak.

## Known answers and MUTATE (nh2.out, nh2_MUTATE.out)

- **KA1 PASS.**
  - 76 of the paper's 77 GCs are in the TeX source; GC2 is absent.
  - Mean velocity 1502.3 km/s (paper: 1503 +- 15). Dispersion 132.9 km/s (132 +- 15). r_out 39.5 kpc (40).
  - Tracer mass inside r_out 3.87e11 (Forbes+19: 4.14 +- 0.71e11; -6 %). Inside 23 kpc 2.49e11 (2.44e11).
- **KA2 FAIL.**
  - 16 members. sigma_v 144.1 km/s (143). KT2017's sigma_v and R_g put into the virial form give log M 12.8428 (12.844).
  - R_g = N^2 / sum_{i<j} 1/R_ij gives 228 kpc, not 373. With Tully's pi/2 projected-to-3D factor it gives 358 kpc
    (-4 %). That factor is A1.
  - No graded ceiling changes. C3 is set by the radial PME, which exceeds the pi/2 virial (2.7e13 at 20 Mpc).
- **KA3 PASS.** RB2's needs at 20 Mpc are reproduced with relative difference 0.
- **KA4 FAIL on (c) only.**
  - (a) The mock GC tracer mass median is 0.999 of the true mass.
  - (b) C2's size is 1.5 %; its power against a host 10 times lighter is 100 %.
  - (c) Mock groups give medians of 1.53 (virial), 2.14 (PME isotropic) and 4.28 (PME radial).
  - The frozen mock gave a truncated tracer set the velocities of an untruncated sphere. A self-consistent truncated mock
    (A1) gives 0.94, 1.06 and 2.11. The radial PME's high bias is real, but it only loosens C3.
- **KA5 PASS.** The mean enclosed density does not increase for the isothermal, NFW, Hernquist and law profiles.
- **MUTATE, all three bite:**
  - **M1** (velocity offsets times 4): every cell becomes NOT DECIDED (no ceiling below).
  - **M2** (needs divided by 100): DF2 becomes TIDES CAN REACH and DF4 NOT DECIDED.
  - **M3** (planted host of 4.19e14): HOST CAN RESCUE on both footings.
- **Determinism:** a rerun is identical except for the runtime line. Each run takes 15 to 25 s with a peak RSS of 0.25 GB.

## Post hoc reading A1 (named; not frozen)

- KA2's R_g definition is replaced by Tully's pi/2 form.
- KA4c's frozen mock is replaced by the self-consistent truncated mock.
- Both affect only C3, and only by making it looser. C1 and the DF4 / DF2 cells are unchanged by either.
- The labels above "under A1" are those cells. They are not a pass: they need A1's acceptance to stand.

## Not graded, and limits

- **Split distance.** DF2 / DF4 at 13.5 Mpc with NGC 1052 at 19 to 20 Mpc puts the dwarfs megaparsecs from the host, so
  no tide acts at all. This is stated, not computed.
- **C1 assumptions.** C1 assumes spherical symmetry and a mean density that does not rise outward. To break it, the
  group's mass would have to sit in a shell between 40 and 165 kpc around NGC 1052.
- **Equilibrium and velocities.** Every estimator assumes equilibrium. KT2017's galaxy velocities differ from the NED
  values that Forbes+19 quote by up to 150 km/s. KT2017 is used as the raw table. Interlopers and NGC 1052's own motion
  only inflate the velocities, which makes the ceilings more lenient.
- **Cited, not raw:** DF2's and DF4's velocities (1803 and 1444 km/s, used only in C2b), the HI mass and Forbes+19's
  4.14e11.
- **M1 twin detail.** C3 places NGC 1052 at 1510 km/s instead of scaling its 1590 km/s KT velocity. This is
  immaterial: the twin bites anyway.
- **Not done:** no new measurement, nothing downloaded. Group PGC1 9843's luminosity mass (log M_K 13.17) is
  LCDM-calibrated and is not used.

## Files and commits

- nh2.py; nh2.out and nh2.json; nh2_MUTATE.out and nh2_MUTATE.json.
- Run commands: `OMP_NUM_THREADS=1 python3 -I nh2.py` and `OMP_NUM_THREADS=1 python3 -I nh2.py --mutate`.
- Data, read only:
  - `../_external_data/forbes2019_ngc1052_gcs_2026_11_10/src/N1052.tex` (outside the repo; sha256 in its FETCH_LOG.md);
  - `campaign_fresh_gravity/CFG393_group_catalogue_rar/data/kt2017_table{2,3}.tsv`;
  - RB2's needs (closure_2026_11_09/RB2_form_b_hosted_rows).
- Commits, local / origin:
  - criteria: 7d6ec1b5e7 / 67a8b35d87;
  - script, outputs and this file: 6a54620345 / d67b51c885;
  - this ids line: a follow-up commit, ids in its own message.
- Pushed by replaying the commits onto origin/main with merge-tree + commit-tree (no worktree, no force).

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
