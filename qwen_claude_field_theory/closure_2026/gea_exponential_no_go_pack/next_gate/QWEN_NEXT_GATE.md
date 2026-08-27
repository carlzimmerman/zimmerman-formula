# Qwen Next Gate — Two-Function Covariant Completion Search

## Mission

The standard single-function GEA branch is now a negative-result branch. Do **not** keep patching it with ad hoc parameter choices.

Search for a covariant theory with **independent control** of:

1. the MOND constitutive law,
2. the spin-1 kinetic/gradient sector,
3. the tensor speed.

Target phenomenology:

\[
\mu(y)=1-e^{-y},\qquad y=g/a_0.
\]

## Candidate starting point

Use a unit-timelike æther \(u^\mu\), \(u^\mu u_\mu=-1\), and a general covariant action of schematic form

\[
S=\frac{M_{\rm Pl}^2}{2}\int d^4x\sqrt{-g}
\left[R-2\Lambda+\mathcal L_{\rm AE}+\mathcal L_{\rm MOND}\right]+S_m.
\]

The base Einstein–æther kinetic sector may be written

\[
\mathcal L_{\rm AE}=-K^{\alpha\beta}{}_{\mu\nu}
\nabla_\alpha u^\mu\nabla_\beta u^\nu
+\lambda(u^\mu u_\mu+1),
\]

with four independent constants \(c_i\).

A second invariant function/operator may then encode the MOND constitutive response. A schematic ansatz is

\[
\mathcal L_{\rm MOND}=M^2 F_{\rm M}(I_\star/a_0^2),
\]

where \(I_\star\) is a genuinely covariant scalar built from \(g_{\mu\nu}\), \(u^\mu\), and their derivatives.

## Mandatory gates

For every candidate, derive all of the following from the same action. Do not import them from the desired phenomenology.

### Gate 1 — Covariant action

Give the exact action, units, field content, constraint, and definition of every invariant.

### Gate 2 — Weak-field MOND limit

Linearize around Minkowski space with a quasi-static weak gravitational potential. Derive the modified Poisson equation and prove that its constitutive factor is exactly

\[
\mu(y)=1-e^{-y}.
\]

Do not merely fit it numerically.

### Gate 3 — Quadratic tensor sector

Expand the action to second order in transverse-traceless tensor perturbations and derive

\[
Q_T>0,\qquad c_T^2=1
\]

(or a quantitatively acceptable observational bound).

### Gate 4 — Quadratic vector sector

Expand the action to second order in the spin-1 sector and derive the exact kinetic coefficient and gradient coefficient. Require

\[
Q_V>0,\qquad c_V^2>0.
\]

Crucially, test whether \(F_{\rm M}\) changes these coefficients at quadratic order.

### Gate 5 — Decoupling test

Show symbolically whether the MOND constitutive function can vary while the vector kinetic/gradient matrix stays inside the healthy region.

The desired structural result is:

\[
\frac{\partial(\text{MOND response})}{\partial(\text{vector stability data})}
\approx0
\]

at quadratic order, subject to the field equations and constraint.

### Gate 6 — Scalar sector

Derive the scalar kinetic and gradient matrix and check for ghosts, gradient instabilities, and singular denominators.

### Gate 7 — Newtonian/high-acceleration limit

Recover GR/Newtonian gravity as \(y\to\infty\). Identify the measured \(G_N\) exactly.

### Gate 8 — PPN / GW / Cherenkov

Check the preferred-frame PPN parameters and propagation constraints using the candidate's own parameters.

### Gate 9 — Black holes

Only after Gates 1–8 pass, examine spherical black-hole perturbations. The 2024 literature indicates that high-frequency black-hole odd-parity conditions reduce to the corresponding Minkowski-mode conditions in an æther-orthogonal frame; use this as a cross-check, not as a substitute for the Minkowski derivation.

### Gate 10 — Falsification

Try explicitly to kill the candidate. Search for hidden mixing terms, strong coupling, singular limits, superluminality, bad matter coupling, and failure of the MOND-to-GR transition.

## Hard prohibition

Do not declare a viable theory from a phenomenological ansatz alone. Do not use “healthy” unless the sign of the quadratic kinetic matrix and the gradient eigenvalues are explicitly derived.

Do not replace a difficult derivation with a numerical optimizer.

Do not assume an added MOND function is inert in the vector sector; that is the central question of this assignment.

## Deliverables

Produce:

1. `CANDIDATE_ACTION.md`
2. `WEAK_FIELD_DERIVATION.md`
3. `QUADRATIC_TENSOR.md`
4. `QUADRATIC_VECTOR.md`
5. `QUADRATIC_SCALAR.md`
6. `DECUPLING_TEST.md`
7. `BLACK_HOLE_CHECK.md`
8. `FALSIFICATION_REPORT.md`
9. symbolic Python scripts reproducing every nontrivial algebraic identity

The final status must be exactly one of:

- `CLOSED — VIABLE WITHIN TESTED DOMAIN`
- `CLOSED — NO-GO`
- `INCOMPLETE — SPECIFIC GATE FAILED`

Never use “viable” merely because no contradiction was found in a partial calculation.
