# AC15: the moving Sun, nonlinear: NO VERDICT as frozen; every graded number is far under its line

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md (b089f97024), with
AMENDMENT 1 (aa2612a47c, made before any graded hydro run). Scripts: s1_sympy.py (S1), hydro.py (axisymmetric
solver), grade.py, run_all.sh (16 runs, 4 at a time, one thread each, nice 10, checkpointed). v3s and AC2q
are the same calculation here, since AC2q only adds s^2/rho0 ~ 4e-6 to the charge. Astra's AZ37 is read
only.

## What is new

- **S1 (sympy, all PASS): the khronon charge obeys global Bernoulli.** The P equation is
  grad(Xi + gamma q) = K M_theta P. The screening term on the right is at most 1.2e-10 at 10 AU, so it is
  dropped. For a pattern stationary in the Sun's frame, Xi = phi + (w^2 - V^2)/2 exactly. Together:
  - gamma q = c_gal^2 + Phi_N + (V^2 - w^2)/2, with one constant for the whole flow, not one per streamline.
  - The static C6P hedgehog is the V = w = 0 case (KA1).
  - AC12's equation is this one with the charge held fixed (KA2).
  - The evolution is barotropic Euler with h = gamma q (S1c), i.e. a Gamma = 2 gas past a point mass.
- **The Sun moves hypersonically through its own Galactic khronon.** The upstream Mach number V/c_gal is
  234-490 over every cell. The flow is gravity-dominated only inside the accretion radius
  R_A = 2GM/V^2 = 0.037 AU (V = 220 km/s) or 0.013 AU (369 km/s). The planets sit at 27-735 R_A.
- **Result of the 2D solve: the wind sweeps the static hedgehog away.**
  - Upstream and to the sides, the charge equals the pressureless point-mass focusing density to 1.0e-3
    (KA5): about rho0, not Phi_N/gamma.
  - The excess charge collects inside R_A and in a downstream column.
  - Starting from the static hedgehog (HEDGEHOG start), the hedgehog drains away. At t = 3000 it is still
    relaxing, but Earth's number already matches the UNIFORM start.
  - The static hedgehog anomaly GM/Lstar^2, which C6P graded at 0.03-0.21 of the planetary bounds, is
    therefore not present at the planets in the moving state.

## Graded numbers (ratio to line; worst over all 12 cells, both footings)

| Bracket | G1 Earth | G1 Mars | G1 Saturn | G2 Mars | G3 (Cassini, 5.2e-27) |
|---|---|---|---|---|---|
| TRANSMIT M234 medium, q | 4.3e-4 | 1.3e-3 | 3.6e-5 | 2.4e-4 | 2.5e-6 |
| TRANSMIT M490 medium, q | 4.3e-4 | 1.2e-3 | 2.6e-5 | 1.4e-4 | 1.8e-6 |
| ABSORB M234 / M490 medium, q | 4.2e-4 | 1.2e-3 | 2.8e-5 / 2.0e-5 | 6.8e-5 / 2.6e-5 | 2.4e-6 / 1.7e-6 |
| REFLECT M234 medium / M490 coarse, q | 4.2e-4 / 4.4e-4 | 1.2e-3 / 1.1e-3 | 2.8e-5 / 1.9e-5 | 9.0e-5 / 3.6e-5 | 2.4e-6 / 1.6e-6 |
| HEDGEHOG start, coarse, q (NOT STEADY, envelope) | 8.7e-4 | 8.7e-3 | 8.7e-3 | 4.2e-3 | 6.8e-3 |
| **Worst over every bracket, q and q_B** | **0.036** | **0.25** | **0.11** | **0.092** | **0.050** |

- **Where the q column comes from.** It is dominated by the conservative Bernoulli cap on the excised core
  (r < 2 R_A). The simulated flow charge alone gives at most 1.7e-4 of the bound at Mars.
- **The worst row is the q_B reading.** That is the shock-proxy check, where the charge is recomputed from
  global Bernoulli and the simulated w. It is noisy: q_B is M^2 times the small difference (1 - w^2), and its
  runs are NOT STEADY to 5 %, so their envelopes are graded.
- **For comparison, the static hedgehog's own ratios:** Earth 0.034, Mars 0.212 and Saturn 0.042
  (canonical, Lstar 21.68 pc, the tightest cell).
- **Every number is under its line,** in every bracket (three inner boundaries, two starts, both M_inf
  values, q and q_B) and on both footings.
- **Convergence (coarse to medium) PASSES:** graded ratios change by 12-27 %, against the 30 % line.

## Why the label is NO VERDICT

The frozen lines need every known answer and the MUTATE control to pass. Two do not:

- **KA3 FAILS narrowly.** Gravity off, the coarse grid holds the uniform wind to 1.20e-2 against the
  amended line of 1e-2. Medium gives 4.55e-3, 2.6x smaller as required. The residual sits in the
  downstream-axis cells next to the inner boundary, and it is truncation error.
- **MUTATE FAILS (no power at the line).** With a repulsive Sun the flow empties a cavity (q_min to the
  floor) and the flow-only radial anomaly at Earth changes sign (-4.8e-21 to +8.8e-22 m/s^2). But the
  frozen criterion asked for G1 Earth >= 0.1 of the bound. Every effect in this problem is 1e-3 of the bound
  or smaller, and G1 is dominated by the BC-independent core cap, which the mutation does not touch (G1
  0.00044 in both). So the control cannot reach the frozen size. That is the frozen consequence: the
  grader is not shown to have power at the line, so no PASS stands.

## Bugs found and fixed before the graded run (first run kept: grade_run1_axisbug.*)

The first full run failed KA3, KA4 and KA5 and convergence (changes up to 1.9x). All three known answers
caught real defects.

1. **The axis cells used point values sin(theta_c) as finite-volume averages.** That is a 25 % error in the
   axis cell, independent of resolution. Charge piled up on the axis (q ~ 5.7).
   - Fix: the wind state is set as exact cell averages, <sin> = Int sin^2 / Int sin and
     <cos> = Int cos sin / Int sin.
   - v is reconstructed as v/<sin>, which is exact for the uniform wind. The discrete right-hand side then
     vanishes to 1e-16 in mass.
2. **TRANSMIT's zero-gradient q drained the hydrostatic hedgehog** (KA4 0.33).
   - Fix: q is extrapolated log-linearly, and the power-law index is capped at 2 (the hedgehog's is 1).
     The first uncapped version blew up on infall at t ~ 6 and was rerun.
   - KA4 now gives 8.7e-4 (TRANSMIT) and 1.1e-3 (REFLECT).
   - No line was changed after these runs. The KA3 coarse miss is kept.

## Checks

S1a/S1a_size/S1b/S1c/KA1/KA2 PASS. FIELD_TEST (added, not frozen) PASS: a synthetic static hedgehog gives
C6P's GM/Lstar^2 to 6.6e-5, and the code-to-SI conversion is exact to 2e-16. KA3 FAIL (above). KA4, KA5 and
CONV PASS. MUTATE FAIL (above).

## Scope and what is still open

- **Scope:** PN order, mu_K = 0, screening term dropped, axisymmetric (the Sun's velocity along the axis),
  the Sun as a point mass outside 2 R_A, and the Euler shock proxy (checked by q_B). There is no PPN
  alpha_1 or alpha_2 and no gravitomagnetic split.
- **What would turn the label into a verdict:**
  - a MUTATE that bites at a resolvable size, e.g. graded against the flow-only field, or with a planted
    anomaly of known size;
  - KA3 on a finer coarse rung.
- **Not graded:**
  - galaxies moving through their own khronon, where the same sweeping would act on the phantom charge;
  - the Euler-vs-potential shock conditions inside the column.

Snapshots: only each run's final snapshot is committed (parts/*/snap_04.npz). run_all.sh regenerates the
rest deterministically, in about 1.5 h on 4 cores.
