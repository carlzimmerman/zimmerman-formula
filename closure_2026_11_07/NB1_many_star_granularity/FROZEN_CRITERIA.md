# NB1 FROZEN CRITERIA: does a body built from screened point stars show the same field as the smooth body? (2026-11-07)

Frozen before any script or number. TEST lane of the adopted action; adopts nothing, opens no sector, adds no switch key.
kappa = 1/2 FITTED. Not theory closed.

## Why this lane exists

QX17C (f504682c83) certified a solver and recorded, ungated, that an isolated point Sun reaches only 0.71 / 0.67 of
law S at 1e3 Lstar (canonical / alt), while a smooth 1e10 Msun ball of R = 0.5 kpc shows law S to 4e-6 at 1-30 kpc.
QX17C states that granularity is untested and must not be cited for galaxies. An outside review (Argon, 11-07) named
this the most dangerous open point of PAPER70: if a body made of screened stars does not reproduce the smooth-body field,
the disc result (SPARC, the one class that passes) is in doubt. Stellar spacing in a disc is ~1 pc, Lstar ~22 pc, so
d / Lstar ~ 0.05: every Lstar cell holds ~1e4 stars. This lane grades that, on the adopted action only.

## Action and equations

- Action: v3s with the adopted Pi^6 blend stiffness (AC21 iter_6, b = rho_DE; owner decision 71e4014cd5).
  The raw max(Pi,0)^2 switch is NOT run (AC16: no C1 solution in 3D).
- Equations: the static, weak-field (N = 1, flat leaf, khronon at rest) limit of QX17D's R2-certified field equations
  with that F. Derived symbolically in-lane, written into the script header.
- Footings: canonical (a0 9.3603e-11, Lstar 21.7 pc) and alt (a0 1.1312e-10, Lstar 22.9 pc). Labelled separately,
  never pooled.
- Isolated bodies: no external (Galactic or cluster) field. GR corrections are dropped (QX17C: full minus weak
  <= 4.1e-6 relative).

## Phase 0 (1D spherical, QX17C solver with the blend F): choose the 3D body by a frozen rule

- Grid: total mass M in {1e4, 1e6, 1e8, 1e10} Msun x ball radius R in {1, 2, 4, 8} Lstar, both footings.
- For each cell, solve a uniform ball (QX17C tanh edge) and a point mass of the same M (softened ball of radius
  eps = 1e-3 Lstar).
- Power P(M, R) = min over s in {2R, 5R, 10R} of |G_point / G_ball - 1|, with G the total radial acceleration.
- **Chosen body:** the cell with the largest min(P_canonical, P_alt). Ties go to the smaller R. Every cell's P is
  recorded (this also says whether the lone-star deficit is a mass effect or a size effect).
- If the chosen P < 0.15, the 3D test has NO POWER: point and smooth body agree at every scanned (M, R). It still runs.
  The label is then NO POWER and the record says so; it is never written up as HOLDS.

## Phase 1 (3D): the star ladder

- Body: the chosen (M, R). N equal stars of mass M / N at uniform random positions inside the ball, three seeds
  (11, 22, 33), N in {1 (at the centre), 8, 64, 512, 4096, 32768}. Plus the smooth ball (same tanh edge).
- Mean spacing d = R (4 pi / 3 N)^(1/3). If R = 1 Lstar, the finest rung has d / Lstar = 0.05, the disc value. If
  the chosen R is larger, the finest d / Lstar is larger; the record states how far the ladder falls short of 0.05.
- Each star is a softened ball of radius eps <= d / 4 (and <= 0.05 Lstar), deposited on the grid.
- Method free (stretched Cartesian grid, Newton-Krylov or multigrid), provided the known answers below pass.
- **Graded quantity:** D(N) = <G_r>_shell(N) / <G_r>_shell(smooth) - 1 at s in {2R, 5R, 10R}, where <>_shell is the
  mean of the radial total acceleration over the sphere of that radius about the centre of mass. Seeds are averaged.
  The seed spread is recorded as the error.

## Known answers (any failure: the lane is NO VERDICT, the physics is not graded)

- **KA0:** the derived 3D static equations, restricted to spherical symmetry, reproduce qx17c.py's scaled equation
  term by term (sympy, exact).
- **KA1:** the 3D smooth ball matches the Phase-0 1D ball at the three graded radii within 1 %.
- **KA2:** a single softened star at the centre (N = 1) matches the Phase-0 1D point at the three graded radii and at
  s = 1, 3, 10 within 2 %.
- **KA3:** two stars of mass M / 2 separated by 50 Lstar: each one's field within 2 Lstar of it matches the 1D lone
  star of mass M / 2 within 2 % (the far-apart limit).

## Convergence (a rung that fails these is NO VERDICT, never HOLDS or FAILS)

- **C1:** nonlinear residual (round-off-aware scale, as QX17C) <= 1e-8.
- **C2:** refining the grid by 1.5x in every direction changes each D by <= 0.01 (absolute).
- **C3:** doubling the outer box changes each D by <= 0.01.
- **C4:** halving eps changes each D by <= 0.01.

## Label (per footing)

Using the finest rung that passes C1-C4 (call it N_f; it must be >= 4096 or the label is NO VERDICT):

- **HOLDS:** |D(N_f)| <= 0.05 at all three radii, AND |D| is non-increasing over the last three converged rungs at
  every radius (trend toward the smooth body).
- **FAILS:** D(N_f) <= -0.10 at any radius (composite screened below the smooth body), AND |D| at that radius falls by
  less than half between the last two converged rungs (not converging away).
- **NO POWER:** Phase-0 P < 0.15 (see above).
- **NO VERDICT:** anything else. The D(N) table and trend are reported either way.

Scope of any HOLDS: an isolated ball, static, no external field, at d / Lstar down to the finest rung reached. A
real disc (external field, rotation, d / Lstar ~ 0.05 over 1e10 stars) is NOT tested by a HOLDS here unless the finest
rung reaches d / Lstar <= 0.05.

## Twins (MUTATE)

- **M1 (planted deficit):** the grader fed G_composite x 0.8 at every rung must read FAILS.
- **M2 (planted identity):** the grader fed the smooth solution as every rung must read HOLDS.
- **M3 (physics):** the N = 1 rung run through the grader as if it were N_f must read FAILS or NO POWER, never HOLDS,
  whenever Phase-0 P >= 0.15.

## Run rules

- Check that no 1024^3 run is live before launch. nice 15. Checkpoint on SIGTERM and resume (preemptible).
- Memory line 4 GB per process. If the 32768 rung does not fit, the ladder stops at 4096 and this is disclosed.
- Outputs: nb1_phase0.json/.out, nb1.json/.out, nb1_MUTATE.json/.out, RESULT.md. Mutation runs write separate outputs.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
