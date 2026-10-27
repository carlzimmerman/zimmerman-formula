# Checkpoint MP01: a local parent and a physical outlet, not full closure

Original objective: identify the mechanism of the user's framework. Outcome:
partially advanced; full objective OPEN. Base HEAD
2bfdeb83a93861f936cc8d943f52ba8581fde2e5; assessment observed HEAD
15b4863c1f074151700d397aea70675b800debd1. Other work advanced the repository.
This phase is local and uncommitted; no push or shared-status edit was made.

## Concrete advance

The proposed mechanism is compression -> change of a local internal field ->
derivative driving of an outgoing scalar -> reciprocal energy loss from the
moving medium. In a two-component extension, actual conversion contributes to
the same source. [DERIVATION.md](DERIVATION.md) provides an explicit classical
action, rather than naming a cooling term. It generates g2=h lambda together
with a positive kinetic companion alpha=h^2/M^2. The companion cannot be omitted.

The homogeneous pure-component quadratic Hamiltonian is positive for the
stated w>0, 0<c_s^2<1, M>0 assumptions. Its principal cone is subluminal when
M^2 lambda^2 n^2/w <=1-c_s^2. This is a local linear conditional result, not
health of the complete framework. It addresses the earlier local fast-cone
defect by changing the action in a specified way.

The completed-square potential and its parameters are assumptions. This is
a mechanism candidate, not a derivation of the actual microphysics or the
numerical coefficient kappa=1/2. Finite M also changes static gradient energy;
the existing galaxy fit and old CC simulations are not inherited.

## Evidence

* [run_checked/result.json](run_checked/result.json): five symbolic identity
  checks;2460 linear mode cases from60 parameter sets; positive Hessians and
  agreement between canonical evolution and the frequency matrix. The sets
  deliberately include acausal controls; causal status follows the inequality,
  not positivity alone. Worst normalized matrix residual1.83e-13.
* The static mediator minimization agrees with a separate periodic-grid solve,
  with error reduction approximately4 per grid doubling. This verifies the
  nonzero static cost rather than hiding it.
* One deliberately displaced linear mode, with chi=chi_t=0 initially, develops
  nonzero chi. Relative energy drift1.09e-11; endpoint agreement with a matrix
  exponential5.94e-10. This is reversible exchange in a mode, not radiation.
* [run_escape_checked/result.json](run_escape_checked/result.json):55 finite
  spherical response cases at70-digit precision; independent boundary matching,
  direct radial quadrature, the vacuum form factor and exact work/flux passivity
  agree. [ESCAPE.md](ESCAPE.md) derives the outgoing solution.
* [run_poles/result.json](run_poles/result.json): outgoing self-consistent
  collective-mode poles decay with backreaction included. These use arbitrary
  dimensionless illustrative m=R=1, K=.01, C=.2; no galaxy time is inferred.

| Interior scalar inertia A | Mode frequency | Amplitude decay rate | Energy e-fold time |
|---:|---:|---:|---:|
|1|.0976914|.000181849|2749.54|
|10|.0976120|.000193992|2577.43|
|100|.0964135|.000414855|1205.24|
|250|.1109664|.002144697|233.13|
|1000|.1007718|.000017139|29173.86|

The resonance region can enhance decay, but larger inertia can suppress it.
This is a sensitivity calculation, not a selection of A=250 for the framework.
The weak-coupling control agrees within0.21% with the compact approximation.
[run_pole_refinement/result.json](run_pole_refinement/result.json) uses twice
as many coupling-continuation steps and a matching-solved susceptibility rather
than the closed form; all five roots agree to relative7e-17. It is not an
exhaustive search for every mode or a proof of arbitrary initial-state decay.

All four successful run manifests passed the installed validator with current
input hashes. See [SELF_REVIEW.md](SELF_REVIEW.md) for scope and failed runs.

## Routes and remaining obligations

1. Constant conserved-current derivative coupling: bulk source is zero. Closed
   for pure-component compression; conversion or nonconstant coupling changes
   the premise and belongs to a different route.
2. Unshifted density mediator: brings an unwanted local density energy together
   with g2. Closed only as an exactly statics-preserving construction. It could
   be studied as a different EOS, but that does not satisfy this route's target.
3. Tracking mediator: local action and conditional stability established;
   two-state source bridge in [TWO_STATE_BRIDGE.md](TWO_STATE_BRIDGE.md).
   Full regular-field/carrier matching remains OPEN. Its next discriminator is
   a joint force/charge/Hessian audit on the actual two-state variables, with
   finite-M static changes retained. This is a new model; existing trajectories
   cannot certify it.
4. Escape: passive exact fixed-body response and selected damped coupled poles
   established. Full mobile-body radiation is OPEN. Its next discriminator is
   deriving the actual density-mode profiles and their couplings from the
   matched action; assigned oscillator parameters are insufficient.
5. Parameter prediction and global framework: OPEN. h,lambda,M, the EOS,
   microscopic phase conversion, kappa and cosmological matching are not fixed
   here. No full formation calculation is justified by selecting their values
   to make the table favorable. The static law alone does not select a unique
   derivative sector: these interactions vanish on a homogeneous static state
   while producing different dynamic responses.

This checkpoint completes a conditional local-parent calculation. It does not
close the user's research objective, certify a galaxy, or rule out other
mechanisms. The next work is model matching and parameter constraints, not
another unconstrained radiation-resonance scan.
