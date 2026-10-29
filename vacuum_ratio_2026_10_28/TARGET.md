# VR28: derive the pressure/vacuum ratio

User request: keep investigating whether B relative to gravitating vacuum
energy can be derived rather than chosen. Parent checkpoint PN28; exact base
revision and input bytes are recorded in INPUTS.json. Owner is /root; no
delegation is authorized for this turn. New work is confined to this folder.

The target is a dimensionless positive B/V predicted by a specified physical
parent and state, without inputting the phenomenological acceleration target.
B in PN28 is both U_ss(0)/9 and its dense logarithmic pressure coefficient.
These definitions need not agree in a changed model. V must be the full
gravitating vacuum energy, not a subtracted sector contribution. Under the
separately adopted core-column dictionary, the old reduced log limit would
require B/V=1/(4 pi xi_q^2) for kappa=1/2. That value is comparison only.

Success requires a derived potential/state, a protected relation to total V,
and retention or explicit rederivation of the halo-to-acceleration mapping.
A free exponent, finite renormalization, vacuum uplift, or integration constant
replacing B/V is partial progress, not normalization selection.

## Portfolio and discriminators

1. Dilation/scaling: derive the potential constraints and their pressure law.
   First check: can a positive stable vacuum coexist with a fixed stiffness
   ratio? Opposite exponentials give a concrete candidate; test its exact EOS,
   high-density core, and additive vacuum deformation. No fitted exponent.
2. Gravitational vacuum: vary a minimal and a nonminimal scalar vacuum sector.
   First check: do de Sitter field equations and stability give an equality
   fixing B/V, or an open region? Do not assume that a vacuum-sector test is
   a covariant completion of the PN28 stream action.
3. Vacuum thermodynamics: translate the proposed dilation to a conserved
   medium coordinate. First check: does the thermodynamic identity connect
   stiffness and vacuum energy, or only identify them as separate response
   quantities? Check primary-source conventions before applying them.
4. If scaling yields a candidate, test the anomaly/near-marginal continuation
   and distinguish a sector vacuum energy from the full gravitating value.

Each route retains its exact obstruction, surviving conditional result and
next missing microscopic input. No global impossibility theorem or claim of
worldwide novelty is sought. Numerical examples supplement exact arguments.

## Pre-run finite discriminator

For the two-exponential candidate take Z=exp(2s), k>0, delta>0, and
U=V[delta exp(3s)+exp(-3 delta s)]/(1+delta), initially with no extra constant.
Test exact equilibrium/pressure/enthalpy identities and counterterm freedom.
Solve auxiliary hydrostatic cores for delta={0,0.001,0.01,0.1,1}, each with
y_c={10,1000,1000000}. Use a central core coordinate to avoid a missed tiny
core; stop at quarter density. Independently integrate the asymptotic core
equation and compare. The test is formal local-scalar Newtonian equilibrium,
not finite-gradient validity, stability, formation, observations or selection
of delta. Freeze software, tolerances, bounds and acceptance checks in the
computation contract before execution.
