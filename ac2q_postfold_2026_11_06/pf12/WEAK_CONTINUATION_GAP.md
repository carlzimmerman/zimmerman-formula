# Why the incoming estimates are not a postbreak evolution theorem

## The implication actually available

PF09 constructs a unique strong solution on its maximal interval. Within the
localized packet bootstrap, total variation of r and rapidity and the auxiliary
inverse norms stay bounded while the compressive first derivatives blow up.
This provides terminal data. It is not an approximation scheme producing
native solutions on an interval beyond the maximal strong time.

The proof smoothings in LOCAL_EVOLUTION.md have uniform bounds only on the
prebreak Lipschitz existence interval. They approximate the native cusp and
initial data for that proof. They do not furnish a uniform postbreak Lipschitz
estimate, a shock admissibility law, or a concentration-capable solution class.
Reusing them as a singular continuation would add an unproved step.

## Attempt to extend the auxiliary inverse to BV states

At a single compact clock slice, the periodic first-order auxiliary inverse has
bounded coefficients and coercivity. Its linear equation can handle a finite
measure forcing and bound the reconstructed response in an appropriate BV
class. This suggests using the prebreak variation estimate after blowup.
But the forcing equation for u=nA/r and v=nP/r was obtained by differentiating
constraints and substituting the classical scalar evolution. At a jump in r
or rapidity, expressions such as D_r n(r), R n(r), and the frame commutator
contain discontinuous coefficients times derivative measures. Their meanings
must follow from the original divergence equations, not be assigned by the
smooth expanded equation. Ordinary pointwise chain rules do not define them.

Consequently invertibility of that spatial operator alone neither identifies
its measure forcing with the native equations nor propagates all constraints
through a shock. The exact jump checks are a necessary compatibility test.
The small acoustic corner result fails that test for a regular nontrivial small acoustic
shock in the stated low-u neighborhood: scalar and polarization flux conditions and total stress conservation
cannot all hold. Choosing a convenient product convention does not repair it
without verifying equivalence to the original action/equations.

## What remains logically possible

A bounded, continuous but non-Lipschitz native solution might have no ordinary
jump to which the corner theorem applies. A diffuse oscillatory limit might
fail identification of native outer stress. A concentration could violate
regular side-flux or metric assumptions. None is constructed here, and the
failure of the naive BV-inverse argument proves neither existence nor
nonuniqueness of any such continuation.

To establish survival as written one needs a defined weak formulation of all
native equations, an existence construction from the terminal incoming data,
and uniqueness in that same class. To establish necessary extension generally
one needs to exclude the remaining classes, or prove the actual evolution must
stay in a class already excluded. Bounds on a nonexistent postbreak solution
cannot be inferred solely by continuation of the prebreak inequality.

The existing estimates establish incoming compactness and forbid specific
shock/sheet repairs. They do not establish complete postbreak predictivity.
This is the first missing implication in the attempted BV route, not a claim
of a general theorem that all BV native solutions fail.
