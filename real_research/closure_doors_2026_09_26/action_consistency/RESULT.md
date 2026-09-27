# Static identification, ADM kinetic inversion and the Ward obligation

Three exact calculations address the interfaces that component-level passes
cannot establish. `check.py`, its contract and `run1` record the actual symbolic
calculations. This is not a new complete action.

## Exact static law for general sources

The canonical target is AQUAL, not just a spherical relation. With a0=1 choose
Φ=(x²+2y²)/2, so g=(x,2y). For μ=1−exp(−|g|),

\[
\partial_x(\mu g_y)-\partial_y(\mu g_x)
=-\frac{2xy}{\sqrt{x^2+4y^2}}e^{-\sqrt{x^2+4y^2}}\ne0
\]

at (x,y)=(1,1). Therefore μg cannot generally be identified with the gradient
of a Newtonian potential. Equality of spherical AQUAL and QUMOND laws does not
supply the full general-source equation. The parallel response/inertia route
therefore integrates a direct acceleration primitive, with both physical metric
potentials varied before elimination, instead of treating that identification
as a theorem. This witness excludes that algebraic identification; it is not a
no-go theorem for all relations between the two theories.

## Actual kinetic inversion and the degree-count boundary

In adapted coordinates take the displayed kinetic density
KijKij−λK², with λ=1+c2, suppress its positive common prefactor, and use the
spatial metric to raise indices. Its momentum is proportional to
Pij=Kij−λK hij. For λ≠1/3,

\[
K_{ij}=P_{ij}-\frac{\lambda}{3\lambda-1}P h_{ij},\qquad
H_{\rm kin}=P_{ij}P^{ij}-\frac{\lambda}{3\lambda-1}P^2.
\]

The trace map is P=(1−3λ)K and the conformal kinetic Hessian is
6(1−3λ), so λ=1/3 is a genuine degeneracy. These expressions follow by
varying and Legendre-transforming a generic symmetric 3×3 matrix, rather than
assigning a mode count.

For the original localized C-H/K action in unitary gauge, N, the shift and U
have no independent physical-time velocities, whereas hij does. However,
primary momenta equal to zero are only the start of Dirac analysis. Preservation
produces functional lapse/auxiliary equations; their domains, null modes,
Poisson brackets and boundary conditions decide their class and preservation.
The fixed-N auxiliary convexity proof controls one of these equations, not the
full coupled constraint algebra. A generic nonzero-mode invertible lapse/U
block is consistent with two tensors plus one scalar, but this package does
not certify the full functional classification or rebrand that scalar as
ordinary matter. The λ=1/3, k=0 and zero-field sectors cannot be removed by
substituting into a formula derived on an invertible branch.

## Conservation requires the gate variation

For a diffeomorphism-invariant scalar/metric action, write its Euler derivatives
as Eg, Eτ, EU and the localized heat-field derivatives. Interior variation under
a compactly supported diffeomorphism gives the identity

\[
2\nabla_\mu E_g^{\mu\nu}
=E_\tau\nabla^\nu\tau+E_U\nabla^\nu U
+\int dz\,[E_W\nabla^\nu W+E_L\nabla^\nu L]
+E_{\lambda_0}\nabla^\nu\lambda_0,
\]

using variations with respect to the covariant metric and scalars, and the
action's endpoint equations. Omitting a field-dependent gate variation changes
the Euler derivatives on the right; the identity cannot then be borrowed from
the unmodified action. Minimally coupled ordinary matter has its separate Ward
identity and conserves its stress on its own matter equations. No violation of
that established identity is asserted here.

An explicit 1+1-dimensional check makes the gate term observable in an identity.
For

\[
L=\tfrac12(q_t^2-q_x^2+z_t^2-z_x^2)-F(z)V(q),
\]

the full energy obeys
\(\partial_t\mathcal E+\partial_x\mathcal J=q_tE_q+z_tE_z\).
Using the free z equation instead of its actual equation leaves the nonzero
term \(z_tF'(z)V(q)\). Treating F as a prescribed external field gives exactly
that exchange in the q sector. The symbolic calculation verifies all three
identities for arbitrary smooth functions; it is an illustration of the missing
term, not a proxy proof of the gravity model's full Ward identity.

The remaining obligation is to vary the chosen complete action, retain its
endpoint conditions and solve its actual functional constraint system. The
static, kinetic and Ward calculations above set concrete checks on that work;
none lets a collection of scalar algebra certificates stand in for it.
