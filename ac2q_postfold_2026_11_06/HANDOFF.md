# PF08 continuation handoff

Latest evidence: pf08/STATUS.md and pf08/CURRENT_WORK.md. Read these before the
historical PF07 handoff below. The target remains unachieved; no full-action
failure or unique singular continuation has been established.

# PF07 continuation handoff

Live entry: README.md and pf07/STATUS.md, 2026-11-06.
Owner: current Codex chat; authorized write scope ac2q_postfold_2026_11_06 only.
Target: determine native full-action avoidance/unique postfold completion versus
necessary extension. This target has NOT been declared achieved.

## New durable results

1. Solver repair: canonical r_mom subtracts the exact curvature contribution;
   stage momentum reconstruction plus padded nonlinear evaluation removes the
   observed early aliasing instability. Homogeneous, chain-rule, linear, physical
   field space/time/padding, raw constraint and projection checks are recorded.
   n127/n255 and evaluation-grid refinement agree through t=1 in the chosen
   dimensionless constant-V fixture. This is not the canonical astrophysical
   parameter footing or a validated weak continuation.
2. Later accuracy stops: stricter raw momentum criterion stops n127 at1.2425
   (both evaluation sizes255/381) and n255 at1.33375. The finite q,X,cap values
   and increased gradients do not prove physical blowup. Earlier q-only runs
   to~1.5 cannot override the stricter checks. Last failing steps are not accepted.
3. Time-dependent regular corner: partial Legendre transform adds -JvT, affine
   in v. Scalar normal flux shifts equally; normal stress and convexity
   obstruction are unchanged. Stationary field profiles are no longer required.
4. Finite-measure polarization storage excluded by the weighted native current's
   fixed-sign cone and no-dipole condition on timelike interfaces.
5. Finite-measure scalar storage excluded by the exact current-clock contraction
   and div(phi J) product identity, requiring uniform phi convergence, bounded
   current total variation, controlled source and C1 positive timelike trace.
6. Matter Hilbert surface stress excluded by the auxiliary/KKT action and
   clock-slice variation estimates: Q/r bounded from a crossing boundary;
   positive Pi variation bounded; strong endpoint matching forces off-branch
   multiplier mass to vanish. Require bounded frame-clock components, regular
   metric coefficients, cap separation and strong endpoint control. Invariant
   X bounds alone are insufficient. Gravitational defects require separate
   metric regularity assumptions.

Proofs and independent audits: coupled/time_layer_review/REVIEW.md,
POLARIZATION_MEASURE.md, AUXILIARY_STRESS.md, and MATCHING_BRIDGE.md. The final bridge explicitly requires identification
of native bulk stresses/currents from outer states, without a bulk oscillatory
defect. Under the intersected hypotheses it proves the restricted no-layer
connection, including layers that visit the off branch internally.
Nine root exact identities pass; reversed-topological-sign control fails its
intended equation. Independent earlier review has eight additional identities.
The numerical reviewer identified reporting gaps that the final comparisons
address. Keep original reviews and failed runs as provenance.

## Research routes still open

N1 formation/avoidance: derive a full coupled breakdown theorem or obtain a
controlled finite-amplitude continuation farther toward a physical event. Do
not import a local-source shock theorem without treating the spatial constraint.
The current solver is useful before its accuracy stop. A future reformulation
may evolve only mean p_lambda and reconstruct its spatial part consistently;
then verify the differentiated constraint/evolution equations, not merely the
small reconstructed residual. Adaptive resolution and an independent stable
formulation are possible continuations, not executed proofs of an endpoint.

N2 singular native escape: the bounded, continuous-field finite-measure layer
route has strong exclusions. Remaining possibilities must explicitly demonstrate
loss of one relevant bound (cap/source concentration, clock/frame degeneration,
nonmeasure currents, discontinuous P traces, singular gravity or bulk oscillatory
defects) and still establish finite observables, field equations and unique
selection from smooth incoming data. Naming a loophole is not a completion.
These routes remain open; none has been shown to exist or to be unique.

E1 extension: a viscosity, entropy rule, new stress carrier or new operator needs
explicit equations, charge/stress budget and stability. No particular extension,
coefficient, empirical refit or manuscript change was adopted. For a finite
corner obeying all intersected hypotheses, an ordinary native layer cannot
supply its completion; this conditional statement is not universal failure of
the full action.

## Provenance

Earlier PF01–03 criteria/results and PF04–06 evidence remain in Git and their
own manifests. PF07 base e50f32a0a7, criteria48c08b18e5. Individual amendments
were recorded before their runs and hashed by the runner. Independent agent
records identify inspected source hashes. pf07/VERIFICATION.json checks all
available computation manifests; it validates provenance, including failed runs,
not scientific success of each run. validation001 failed on NumPy-boolean JSON
serialization; validation002 fixes output conversion and passes all five tests.
Exploratory diagnose_modes.py was a diagnostic, not a load-bearing registered run.

No unrelated working-tree files were edited. No postfold outcome or native
surface stress was invented. Scientific closure still requires the unresolved
formation/avoidance and singular-selection implications above.
