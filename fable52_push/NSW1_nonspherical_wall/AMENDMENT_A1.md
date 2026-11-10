# NSW1 AMENDMENT A1 (committed alone, after the first run, before the second)

Criteria 052f87daad. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled. The frozen file is not edited.

**First run: NO VERDICT / NO VERDICT.** Its outputs are kept as nsw1_run1_noverdict.json / .out and run_main_run1.txt (one
warning line in the log carried a home path, which is cut).

## 1. What failed

Only B3's iteration, and only for R_d = r_M (six of the eighteen walls: three dispersions on two footings).
- The departure from a flat wall pressure grew by 1.72 per step (canonical, 17.5 km/s: 1.6e-3, 2.8e-3, 4.7e-3, 8.1e-3, ...).
  The walls ran 7 to 18 % away from the sphere, the Newton solves on them stopped converging, and two returned meaningless
  ratios (Gamma_F 7.4e6 and 1.7e4).
- Through those six walls: KA1(a) read 1.5e-6 against 1e-6, KA8 read 2.8 against 2e-2, "every solve converged" and "flat to
  1e-3" were false. Hence NO VERDICT as frozen.

## 2. What did not fail (disclosed: these numbers have been seen before this amendment)

- The 120 spheroid cases: every solve converged, the exterior mass equals M_b to 8e-13, and KA8 on their 50 admissible cases
  reads 0.4 %. Their ratios at equal reach: Gamma_F 1.00 to 1.21, Gamma_C 0.215 to 1.00.
- Every other known answer passed (KA1 b and c, KA2 to KA7, KA9, KA10). The four MUTATE arms bite. NSW1.lean compiles.
- The twelve B3 walls with R_d = 0.1 and 0.3 r_M were flat to under 1e-3 on SWT1's sphere at the first solve.
- So the label expected after this amendment is CAP HOLDS on both footings. The amendment is not written to reach it: it
  changes how one iteration steps, not where it stops.

## 3. Cause

The frozen rule moves each wall point by (p_wall - p_ext) / |dp/dn|, and I took |dp/dn| from the sphere (3 p / R in the deep
regime). The pressure responds more strongly to a displacement that varies over the wall. Hand derivation, deep limit, wall
an equipotential of the interior field: a displacement of Legendre degree l, dR / R = eps_l P_l, changes the pressure by
dp / p = -kappa_l eps_l P_l with

    kappa_l = 3 (1 + sqrt(l (l + 1) / 2)):   3, 8.2, 12.5, 16.7 for l = 0, 2, 4, 6.

With the l = 0 value in the step, the error in degree l is multiplied by -sqrt(l (l + 1) / 2) each time: -1.73 for l = 2,
which is the growth the first run shows. The rule as I coded it cannot converge on any wall that is not flat already.

## 4. Change (B3's step only)

The step is taken degree by degree: with pi = p_wall / p_ext - 1 analysed in even Legendre degrees up to 16,
eps_l -> eps_l + pi_l / kappa_l, and the wall is rho -> rho (1 + sum of the new terms). kappa_l is the hand value above,
unverified; it sets the step size only. A wrong kappa_l changes the number of steps, not the wall the iteration stops on,
which is still defined by the frozen line |p_wall / p_ext - 1| <= 1e-3 everywhere. At most 15 steps; a wall not flat by then
is reported NOT FLAT and the label stays NO VERDICT.

## 5. Not changed

B3's statement (the wall on which p_wall equals the uniform exterior pressure), its stopping line, pressures and sources;
every statistic, tolerance, line and label; the known answers; the MUTATE arms; the spheroid family.

## 6. The second run

It resumes from the first run's checkpoint, as Section 11 of the criteria provides. The 120 spheroid cases and the twelve
flat B3 walls are not solved again (this amendment does not touch their code path); the six diverged entries are removed and
solved with the new step; the known answers are recomputed.

## 7. Also disclosed from the first run

- Two disc cases change admissibility between the two grids: E0.3, q 0.5, a 100 (in-plane deviation 0.011 on the production
  grid, 0.059 on the finer one) and E1.0, q 0.7, a 30 (0.189, 0.030). The in-plane field of a thin disc is noisy at the 5 %
  line. The production grid decides, as frozen; both cases sit far from every line (Gamma_F 1.14 and 1.04, Gamma_C 0.45 and
  0.79). RESULT.md will carry them.
- The hand statement made at freeze that B3 returns spheres is wrong for R_d = r_M: on the sphere the wall pressure varies by
  0.16 to 0.57 %, two orders above (R_d / a)^2. In the deep regime a disc's l = 2 imprint falls only as r^(-1.73) against the
  monopole.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
