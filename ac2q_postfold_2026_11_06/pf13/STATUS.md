# PF13 — weak equations defined; native continuation still unresolved

**No defensible universal survive/fail/extension verdict has been obtained.**
The bounded weak formulation can now be written directly, so ambiguous products
in the differentiated solver are no longer the only formulation available.
Existence and uniqueness of a full coupled continuation remain unproved.

## Direct weak system

[Bounded weak formulation](BOUNDED_WEAK_FORM.md) and
[independent audit](review/WEAK_FORM_AUDIT.md) derive the scalar and polarization
Euler equations from the first-order auxiliary action, with the native switch
and KKT relation retained. For Lipschitz phi,A,Pi, BV clock gradient, compact
strict timelike/cap bounds and regular geometry, the equations use ordinary
bounded products and distributional divergences. All Einstein equations and
the native Hilbert stress are imposed as well.

This is a well-defined variational weak class extending the native smooth
system, with no new bulk physics. Defining it proves neither a solution exists
from the terminal data nor that it is unique. Equivalence to every possible
singular reading of the original higher-derivative action is not claimed.
Weak scalar/polarization stationarity alone does not automatically imply the
weak stress balance at jumps; the Einstein equations remain load-bearing.

## Actual test of an existence/uniqueness route

[Scalar balance and source check](SCALAR_BALANCE_AND_SOURCE.md), with
[independent audit](review/SCALAR_BALANCE_AUDIT.md), gives a local conservative
acoustic state (m,phi_x) on the positive-R subluminal packet domain. Its source
contains the unknown temporal auxiliary derivatives. It is not yet a closed
source map on a common BV state space.

The primary Colombo–Guerra nonlocal-source theorem was checked, including its
flux and L1-Lipschitz/variation assumptions and its restricted uniqueness class.
Those hypotheses have not been established for this constrained Einstein system.
The theorem supplies no native selection by itself.

The [collapsing-loop test](COLLAPSING_LOOP_TEST.md), with
[independent audit](review/COLLAPSING_LOOP_AUDIT.md), gives a concrete reason not
to promote the prebreak differentiated inverse to an L1-Lipschitz source without
further work. Its derivative forcing contains a nonexact one-form f(r)dtheta.
Small profiles can collapse to the same L1 lower-field limit while retaining
a nonzero forcing impulse. This is a local profile/operator test, not a native
time evolution or a same-data nonuniqueness example. A conservative reformulation
or additional native compactness could still avoid it.

## Verdict and remaining obligation

The prior native strong breakdown and regular shock/sheet exclusions stand.
No uniquely selected postbreak solution has been exhibited. Neither a universal
nonexistence proof nor two native continuations from identical incoming data
has been obtained. Therefore the conclusion remains: classical global evolution
fails for the proved packet family; a mathematical weak completion is required
to make later predictions; whether native equations uniquely provide it, or
new physical terms are necessary, is still open.

R1 resolved as a defined bounded variational weak system. R2's naive use of the
existing inverse/source estimate is insufficient, with an explicit local
forcing-path obstruction. R3 remains open: construct a closed conservative
coupled state/source formulation and establish its native admissibility and
constraint/stress preservation, or prove nonexistence directly in the defined
weak class. Concentration-capable classes beyond the bounded formulation also
remain open. These are deferred mathematical obligations, not claims that all
routes have been exhausted. Repeating the strong-solver estimate without
addressing the forcing paths would not resolve them.

## Verification

Research base a038c807c9. Seven exact algebra checks passed in algebra001 and
its evidence manifest validated. The bounded weak equations and scalar balance
received independent review, as did the scoped collapsing-loop test. The external source check is limited to the stated
theorem hypotheses; no general entropy selection has been imported. No new
native evolution simulation, physical regularizer, or modified action was used.
