# Static elimination must retain the wall compatibility term

With notation of ROOT_DERIVATION, put f=C rho xi-q eta and A=lambda>0.
At fixed xi,eta, minimize I[psi]=integral A(psi'+f/A)^2/C dx over
psi in H^1_0. Euler variation gives A psi'+f=k, a spatial constant.
The condition integral psi'=0 fixes

k = [integral f/A dx]/[integral 1/A dx].

Thus the minimum is [integral f/A dx]^2/[C integral1/A dx], attained by
psi(x)=integral_left^x (k-f)/A ds. For an arbitrary admissible psi,
I=I_min+integral A(psi'-psi_min')²/C dx; the cross term vanishes because
both derivatives integrate to zero. This is an exact positive rank-one
contribution to the reduced static (xi,eta) energy. Dropping the whole square
in a sufficient lower bound is safe; claiming its pointwise cancellation
under Dirichlet conditions is generally false.

Negative-control fixture: constant A,C,rho>0, eta=0,
xi=sin(pi x/D) on [0,D]. Its integral f/A is nonzero, so the naive
psi'=-f/A integrates to a nonzero potential jump and violates the second
Dirichlet endpoint. The correct k produces both zero endpoint values.
This is an algebraic variational fixture, not a hydrostatic background.

This eliminates psi in the static potential form only. The full tau>0
potential has independent kinetic degrees of freedom; a static minimization
does not provide a frequency-dependent dynamic elimination. Eliminating eta
next requires its complete boundary operator and may fail if that operator
is not positive/invertible. That is an unresolved longer-slab obligation,
not an implied stability proof.
