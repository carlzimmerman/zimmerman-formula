# AC24 frozen criteria: the moving Sun with a powered control (v3s and AC2q)

Frozen before any AC24 script or run exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing.
No dark-matter particle. Shared rules: closure_2026_11_06/SWARM_BRIEF.md. AC15's files are read only:
its code is imported or copied, and its parts are loaded, never edited.

## Why

AC15 (340f89b737) is NO VERDICT as frozen, although every graded number is far under its line. Two items
failed:

1. KA3 missed on the coarse grid (1.20e-2 against 1e-2; medium gave 4.55e-3).
2. Its MUTATE (a repulsive Sun) cannot reach the frozen 0.1-of-bound size, because every effect in this
   problem is about 1e-3 of the bounds. So the grader was never shown to have power at the line.

AC24 keeps AC15's physics, solver, observables and lines. It changes three things:

- the medium grid becomes the base;
- a fine rung is added for convergence;
- the MUTATE is replaced by a planted control of known size.

AC15's labels are not changed; its coarse KA3 miss stays on its record.

## Solver and grader (reused)

- Solver: AC15's hydro.py, copied verbatim to hydro_ac24.py. The only change adds `--res fine`
  (dln r = 0.0125, 320 theta cells: half of medium in both directions). The diff is committed.
- Graded observables G1, G2 and G3 use AC15's field() and grade_snap(), copied verbatim into ac24_grade.py.
  The only addition is an optional planted charge `plant` (below), added to dq inside field() after the
  reading (q or q_B) is formed.
- The same lines apply: per-planet bounds 8.7e-15 / 1.4e-15 / 7.0e-15 m/s^2 for Earth / Mars / Saturn, and
  the Cassini Q_eff line 5.2e-27 s^-2.
- Cells: both footings, every Lstar and V, as in AC15. M_inf runs are 234 and 490, rescaled as in AC15.
- v3s and AC2q are the same calculation here (AC2q adds s^2/rho0 ~ 4e-6 to the charge), as in AC15.

## Which reading governs (stated now)

Both readings are graded: q (the simulated charge) and q_B (the charge recomputed from global Bernoulli
with the simulated w). The label uses the worse of the two in every cell and bracket. A cell passes only if
it passes on both.

## Base grid, brackets

- The base is the medium grid.
- Graded brackets, all medium, t_end 3000:
  - TRANSMIT M234 and M490, UNIFORM start;
  - ABSORB M234 and M490;
  - REFLECT M234 and M490;
  - TRANSMIT M234 with the HEDGEHOG start.
- Parts AC15 already holds are loaded from AC15/parts. Two are new: M490 REFLECT medium and the HEDGEHOG
  start medium.
- Steadiness is as in AC15: a run is steady if every graded number changes by 5 % or less over the last
  20 % of t_end. A NOT STEADY run has its envelope graded, inflated by its change, as in AC15.

## Known answers

- KA0 (code identity). ac24_grade.py on AC15's medium parts reproduces AC15 GRADE.json's graded numbers
  (q and q_B, final and envelope) to 1e-12 relative. hydro_ac24.py differs from hydro.py only in the
  `fine` choice: a diff check.
- KA3 (gravity off, uniform wind, TRANSMIT, t = 50, r >= 5), on coarse, medium and fine.
  - The scheme is MUSCL-minmod with HLL and RK2. It is formally second order in smooth regions, and first
    order at clipped extrema and at the axis, which is where AC15's residual sits.
  - Line: medium (the base) max |q - 1| <= 1e-2.
  - Line: the observed order p = log2(e_coarse/e_medium) and log2(e_medium/e_fine) is >= 0.8 for both
    pairs (first order, with margin).
- KA4, KA5 and S1 are carried from AC15 (all PASS there) and are not rerun.

## Convergence on the graded numbers (fine rung)

The fine runs are TRANSMIT M234 and M490, UNIFORM start, t_end 1000. A t_end-3000 fine run costs about 7 h
of single-thread time. Matching coarse and medium runs at t_end 1000 are also made.

- Line: every graded ratio (G1, G2 per planet, G3, worst over cells, q and q_B) changes by <= 30 % between
  medium and fine at t = 1000, and no label flips (no ratio crosses 1).
- Reported, not graded: the coarse-to-medium change at t = 1000, the observed order, and medium at t 1000
  against t 3000 (the time dependence).

## Powered control (replaces AC15's MUTATE as the power test)

A planted anomaly of known size is added as a source term of the anomaly's Poisson equation,
del^2 phi = 4 pi G (dq + dq_plant). It is graded by the same readout.

For each cell and each planet p at radius r_p (in that cell's R_A units), the plants are:

- MONO(p, k): a monopole shell dq = A on 0.5 r_p <= r <= 0.9 r_p. A is set analytically so that the
  planted acceleration at r_p is k times that planet's G1 bound. It tests G1_p.
- QUAD(p, k): a quadrupole shell dq = A P2(cos theta) on the same shell. A is set analytically so that the
  planted max-minus-min over theta of |a| at r_p is k times the bound. It tests G2_p.
- QUAD3(k): the same quadrupole shell inside Saturn, with A set so that the planted Q_eff = k times
  5.2e-27. It tests G3.

The analytic amplitude uses the continuum Legendre field of a thin-shell moment. It does not come from the
grader. The plant is divided by AC15's per-cell rescale factor, so the graded SI value is the target.

Lines:

- P1, recovery. On every medium base bracket, the planted vector field equals field(with plant) minus
  field(without plant), component by component. Graded through G1, G2 and G3, it must equal k to within
  5 %, for k = 2 and k = 0.1, every planet and gate, every cell.
- P2, power. Plant k = 2 on every base bracket. The plant is graded on the reading that governs the
  label: the full field, real plus plant, worst of q and q_B. The planted gate must read over its line in
  every cell.
- P3, no false alarm. Plant k = 0.1. The planted gate must read under its line in every cell where the
  unplanted gate plus 0.1 is under 1. A cell where base + 0.1 >= 1 counts as a real near-failure, not a
  P3 failure; it is reported.

If P1 or P2 fails, the grader has no shown power and the label is NO VERDICT.

AC15's repulsive-Sun MUTATE is reported for continuity and not graded.

## Lines (label)

- **PASS (moving Sun, scoped).** Every cell has G1 (Earth, Mars, Saturn), G2 and G3 under their lines in
  every medium bracket, on both q and q_B. In addition KA0, KA3, convergence and P1-P3 pass, with KA4, KA5
  and S1 carried.
- **FAIL.** Some cell is over a line in every bracket, with the checks above passing.
- **UNDECIDED.** A cell is over in some brackets and under in others; the splitting bracket is named.
- **NO VERDICT.** KA0, KA3, convergence, P1 or P2 fails.

Scope is AC15's: PN order, mu_K = 0, screening term dropped, axisymmetric, the Sun as a point mass outside
r_in = 2 R_A plus AC15's Bernoulli core cap, and the Euler shock proxy checked by q_B. No PPN alpha_1 or
alpha_2 is claimed. The fine rung is checked at t = 1000 only.

## Compute

At most 4 processes, one thread each, nice 15, checkpointed (hydro's own SIGTERM checkpoint). If the load
average is above 45, wait before launching.
