# AC24: the moving Sun with a powered control: NO VERDICT as frozen (the q_B reading's convergence)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: FROZEN_CRITERIA.md, committed alone first
(local 81e48c2a3c) and pushed before any script existed (origin 845f922d4e). It builds on AC15 (340f89b737).

- Scripts: hydro_ac24.py (AC15's solver plus `--res fine`; the whole diff is hydro_ac24.diff), run_all.sh
  (9 runs, 4 at a time, nice 15), ac24_grade.py.
- The grader execs AC15's field() and grade_snap() verbatim, with one patched line for the plant.
- Outputs: GRADE.json, grade.out. AC15's parts are loaded read only; AC24's new runs are in parts/.

## What AC24 fixed from AC15

- **Power: PASS.** The planted known-size anomaly is a source term in the anomaly's Poisson equation:
  - MONO shells for G1 at Earth, Mars and Saturn;
  - QUAD (P2) shells for G2;
  - a QUAD3 shell for G3 Cassini.
  - Their amplitudes are set analytically from the continuum Legendre field.
  - P1: the planted-only field is recovered to within 4.6 % (line 5 %) on every bracket, cell and gate,
    at k = 2 and k = 0.1. The residual is the grader's nearest-edge readout radius.
  - P2: k = 2 reads over its line in every cell, every bracket, on both q and q_B.
  - P3: k = 0.1 reads under its line everywhere, with no near-failures.
  - So the grader has power at the line. AC15's repulsive-Sun MUTATE could not show this.
- **KA3: PASS.** On three rungs: coarse 1.20e-2, medium (the base) 4.55e-3 against a 1e-2 line, fine
  2.16e-3. Observed order 1.40 and 1.08, against a 0.8 line.
- **KA0: PASS.** It reproduces AC15's 140 graded medium numbers exactly (relative difference 0), and
  hydro_ac24.py differs only in the fine choice.

## Why the label is still NO VERDICT

The frozen convergence line fails. At t = 1000, the largest change in any graded ratio from medium to fine
is 0.496 (M234) and 0.572 (M490), against the 0.30 line. No label flips.

The two readings behave differently:

| Reading | Max change, medium to fine (M234 / M490) | Behaviour |
|---|---|---|
| q (simulated charge) | 0.111 / 0.065 | converged, inside the line |
| q_B (Bernoulli charge from simulated w) | 0.496 / 0.572 | falls monotonically at every gate: coarse > medium > fine |

q_B is the shock-proxy check. It is M_inf^2 times the small difference (1 - w^2), so it amplifies velocity
truncation error. It shrinks under refinement at every gate on both M_inf runs. Read after the data, that
makes the medium q_B numbers upper bounds. The criteria said the worse reading governs, and the frozen line
applies to both, so that reading is not the label.

Also reported, not graded: medium t = 1000 against t = 3000 changes by 0.68 / 0.53, and those are the q_B
readings again. The q reading is steady (5 % or less) on every UNIFORM-start bracket.

## Graded numbers

Worst ratio to the line over all 12 cells, both footings, every medium bracket (TRANSMIT, ABSORB, REFLECT
at M234 and M490, plus the HEDGEHOG start), q and q_B. Envelopes are inflated where runs are NOT STEADY.

| G1 Earth | G1 Mars | G1 Saturn | G2 Earth | G2 Mars | G2 Saturn | G3 Cassini |
|---|---|---|---|---|---|---|
| 0.033 | 0.20 | 0.073 | 0.0092 | 0.044 | 0.049 | 0.028 |

- The worst cell is G1 Mars, on the q_B reading of M490 REFLECT medium.
- On the q reading every ratio is 9.4e-3 or less; the worst q number is the HEDGEHOG start's envelope.
- Every number is under its line, in every bracket, on both footings, for v3s and AC2q. AC2q differs by
  s^2/rho0 ~ 4e-6 in the charge, as in AC15.

## Reading (post-data, not the label)

- **PASS** on the q reading, which converged and is steady.
- On the q_B shock proxy, the medium numbers are upper bounds (at most 0.20 of the line), and they fall
  under refinement.
- To make this a frozen label, a new criteria file would have to set a convergence test for q_B before
  running. For example: monotone decrease plus a Richardson bound, on a fourth rung or at t = 3000 fine.
  That needs about 7 h of single-thread time per fine run.

## Disclosed

- A smoke test of the grader ran on AC15's five existing medium brackets before the new runs finished, with
  nothing written. It showed P1-P3 passing there. No line was changed after it; the lines were frozen before
  any AC24 script existed.
- The plant tests grade each bracket's final snapshot.

Scope as in AC15: PN order, mu_K = 0, screening term dropped, axisymmetric, the Sun as a point mass outside
2 R_A plus the Bernoulli core cap, and the Euler shock proxy. No PPN alpha_1 or alpha_2 is claimed.
