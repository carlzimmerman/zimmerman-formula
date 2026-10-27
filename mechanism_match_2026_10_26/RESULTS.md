# MM01: explicit matched field theory with a surviving static branch

The requested field-level match is constructed and checked within the inherited
nonrelativistic finite-grid model. The original objective of a complete physical
mechanism and galaxy formation remains OPEN. Base and assessment HEAD:
15ba662fe3863e770de10acae1d470dd174c64c0. All new work is local to this directory;
no old source, checkpoint, global dashboard, commit or remote was changed.

## Matched object

[MATCH.md](MATCH.md) and [matched.py](matched.py) use the actual regular complex
T/F amplitudes and independent finite carrier. Gravity, response, F pressure,
binding, quantum gradient, alignment and carrier-density inertia are retained.
The old density-dependent scalar connection is replaced by a dynamical internal
field, with a single canonical Hamiltonian and no fitted damping.

The conversion rate follows from the inherited alignment interaction. The
compression/conversion source, scalar reaction, mediator reaction and material
chemical potential come from the same energy. Total mass and shift charge have
exact continuous conservation identities. The implementation remains finite
at zero T amplitude.

On the restricted surface s=lambda rho, with its new mediator gradient term
subtracted, the Hamiltonian equals the old CC action after the exact canonical
chart transformation. Its chain-rule material force also matches. This surface
is NOT invariant under finite-M dynamics, so matching is not permission to
reuse the old trajectory as a trajectory of the new action.

Eliminating the mediator consistently gives a nonlinear denominator in the
kinetic companion. Simply appending the MP01 fluid expression to the old
complex-field action would omit that denominator and double-count some forces.

## Force and conservation audit

[run_match/results.json](run_match/results.json) records:

* Hamiltonian matching error: -8.88e-16 Eunit.
* Chain-force finite-difference relative errors:1.33e-10 to3.36e-9.
* Species continuity maximum absolute defect:1.14e-15.
* Total mass derivative:5.41e-16; shift-charge derivative:4.84e-16.
* All seven canonical variable classes checked against fourth-order energy
  differences at three step sizes. The best relative errors range from2.12e-11
  to1.95e-5; the smallest scalar forces are limited by energy-subtraction
  precision. These are finite checks at a stated nontrivial perturbed state,
  not a universal numerical certificate.
* Exact symbolic check of the nonlinear mediator elimination; finite all-F
  endpoint evaluation with no division by component density.

## Recomputed static branch

The added mediator has a nonzero density-gradient cost at finite range. All
material density, composition and carrier variables were re-minimized with
total mass fixed and the exterior free. This is static optimization, NOT
formation, radiation or a physical time history.

Sensitivity family: g2=171.68027319658083 inherited; alpha=0.5921819758119414
chosen as2*g2^2*rho_max/c^2 using the original static rho_max. For each range
ell=c/M, h=M sqrt(alpha), lambda=g2/h. These coefficients are not predictions.
The factor2 only illustrates a cold acoustic inequality at the reference
density; it does not certify the actual nonlocal coupled theory's causal cone.

The initial L-BFGS study in run_static left the1,10,100pc cases unconverged.
Their intermediate law errors are not accepted final branch results. A separate
Torch implementation and force-based Newton solver then resolved the following:

| Mediator range | Galaxy-law error | Density KKT residual | Angle/carrier gradient | Verdict on static <1% target |
|---:|---:|---:|---:|---|
|0.01pc|0.709433%|6.74e-11|5.70e-10|Pass on inherited grid|
|0.1pc|0.709221%|7.96e-9|5.70e-10|Pass on inherited grid|
|1pc|5.161511%|5.92e-11|7.76e-9|Fail on inherited grid|

The unchanged near-zero-range reference gives0.709435%. These are three
sampled values, not an inferred universal upper bound or a fitted preferred
range. No mediator-profile or material-grid continuum convergence is claimed.

The independently implemented NumPy and Torch static energies agree within
7.11e-15 at the checked starts. Final states have positive cap slack and total
mass residual below9e-16. The0.1pc state has one boundary at56.3438kpc, a filled
transition, and exterior T fraction2.36e-15 by the inherited static diagnostic.
This does not establish long-term exterior nonconversion.

Evidence: [run_newton/results.json](run_newton/results.json), its individual
Newton records and saved states. Solver warnings from inherited code are
preserved: an infinite-bound ratio overflow and a Torch scalar conversion.
They did not produce nonfinite accepted states; actual force residuals, energy
agreement and cap/mass checks are reported rather than relying on process exit.

## Restoring force on the surviving branch

[run_hessian/results.json](run_hessian/results.json) evaluates the final0.1pc
state, rather than reusing a preceding optimizer Hessian. The805-dimensional
active constrained real-density/composition/carrier Hessian has smallest scaled
eigenvalue9.32565e-5, positive. The mediator is relaxed by its exact finite-grid
Schur complement. The density-relaxed boundary stiffness is

    k_R=0.0004112384577 Eunit/kpc^2 >0.

The independent radius directional-difference control is0.999999999962 for a
unit predicted displacement. This establishes a restoring response in the
stated STATIC tangent. It is not a live-boundary stability result, a proof for
inactive/new degrees of freedom, or nonradial/continuum stability.

## What the matching does not fix

1. The original Schrödinger quantum gradient produces a k^4 material dispersion.
   The matched theory is therefore not globally relativistically causal. MP01's
   homogeneous fluid-level causal result cannot be transferred to all wavelengths
   of the actual complex-field theory. The local acoustic inequality is only
   an effective long-wavelength condition.
2. h,lambda,M and the corresponding alpha/range remain underived. The successful
   rows show compatible static examples, not a framework prediction.
3. The latest sustained-transport lane finds weak direct overlap between the
   required inward transport and the leading radiating monopole. In the slow
   tracking limit this match recovers the same source structure. It does not
   automatically remove that transport bottleneck or demonstrate a new cascade.
4. No actual finite-M infall, all-F birth, galaxy population fit or cosmological
   evolution was run here. New degrees of freedom require their own initial
   conditions, force-consistent integrator and resolution controls.

The useful next calculation is a controlled dynamical reduction of this matched
Hamiltonian that retains its compulsory kinetic companion and actual transport
coupling. Another externally driven resonance scan does not settle formation.
