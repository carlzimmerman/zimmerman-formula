# CFG952 AMENDMENT A1 (2026-10-20, PRE-RESULT)

Written after the criteria commit (844ce293d) and before any CFG952 script existed or any number was computed. It is committed
alone. No pass line, MUTATE tooth or class rule changes. Every item comes from a paper estimate made while planning the code.

## A1.1 Peak smoothing: σ = 2 cells, not 1

On paper, H's cold at r ≈ 5 has ρ ≈ 1.5e-3, which is about 4 particles per cell. A σ = 1-cell Gaussian kernel holds about 16
particles, so fluctuations are about 25%. The profile changes by only about 30% across one cell, so noise maxima above ρ_ta would
appear, be resolved, and split H's particles among spurious labels at t = 0.

At σ = 2 cells the kernel holds about 500 particles (4% noise), against a 76% profile change across the kernel. The peak rule is
otherwise unchanged.

## A1.2 Internal velocities

The criteria fix only bulk velocities. Particles get isotropic Gaussian velocities from the Jeans equation of each object's
isolated spherical model. That model is built with the same rules as the prototype:
- its truncated Plummer profiles;
- its r_ON (from the same node rule) and edge;
- the spherical QUMOND phantom;
- the deficit and the uniform-q draw.

Without this, each object would collapse in about one dynamical time, and the collapse would swamp J_Φ and the books. Hx uses
its symmetric model, with the cold centred on its own centre.

## A1.3 Merger run (c): initial approach velocity 1.0

Beyond r_ON each object's zero-sum source adds no net mass, so A and B attract as Newtonian masses of 3.18 each. The relative
acceleration at separation 14 is about 0.03. The free-fall time is then at least 25, so at rest the merger would not happen by
t = 30.

A and B therefore start with ∓0.5 along x (relative speed 1.0). The separation (14), the y offset (0.5), dt and t_end are
unchanged.

## A1.4 DIPSLAVE draw shape: positive exponential tilt (primary); the frozen linear form is kept as a reported variant

**Why.** Conservation needs D_s = Ḋ_s = 0 at switch-on (CFG947's R term for a switch-on ∝ s̈ D_natural). So the draw must cancel
the asymmetric toy's natural dipole from the first step.

For Hx (cold offset 1.5, shell r_e ≈ 3.5 to r_ON ≈ 9.5, q ≈ 0.6) the paper estimate is:
- required draw dipole about the shell-cold centroid ≈ −1.2 Σe ≈ −1.9;
- M2_xx ≈ 37;
- linear β_x ≈ −0.086, hence |β·d| up to ≈ 0.9–1.1, so q(1 + β·d) up to ≈ 1.17 > 1.

The frozen linear form would therefore probably clip. That is a property of the linear shape, not of dipole-preserving draws.

**Primary rule (DIPSLAVE, and DIPFREE with target 0).**
- Draw: comp_X = ρ_c,X min(1, exp(λ_X + β·d_X)) on X's shell, with d_X = x − X_c,X.
- One λ per component (each component is zero-sum) and one β per sector (the sector's realised dipole equals its target).
- Solved by damped Newton on the convex dual
  Φ = Σ_X w_X [Σ ρ_c,X F(λ_X + β·d_X) dV − λ_X Σe_X] − β·T,
  where F(u) = eᵘ for u ≤ 0 and F(u) = 1 + u for u > 0, and T is the target of Σ_X w_X Σ comp_X d_X.

Properties:
- positive and ≤ ρ_c by construction;
- reaches any dipole in the attainable set;
- zero-sum and dipole hold to the Newton tolerance.

Components capped at q = 1 have comp = ρ_c fixed and enter T as constants. "Clipping" for this rule means the Newton solve fails
to reach |∇Φ| ≤ 1e-12 of its scale (an infeasible target). b1 and c2 are graded on this rule.

**Reported variant DIPSLAVE-LIN.** The frozen linear form, with its clipping rule, is run on (b) and reported with no class
weight.

## A1.5 Merge-rule cadence

The MR2 trigger is evaluated at every step, after the drift and before the force. The merged sector C′ is solved with the dual
of A1.4: per-component λ_A, λ_B, λ_C, a common β, and weights (1 − w, 1 − w, w).

## A1.6 Snapshot choice in (a)

The (a) diagnostics are computed at every refresh step and at the stop step. The d = 12 / 8 / 5 snapshots are chosen after the
run, as the computed steps whose d is nearest to each value (5 → the minimum d reached if 5 is not reached).

κ = ½ FITTED; footings never pooled; not theory closed.
