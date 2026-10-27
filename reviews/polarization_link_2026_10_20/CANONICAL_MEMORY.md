# Does the unchanged polarization field have two static memory states?

Coordinator derivation from canonical S2. This tests fixed baryonic sources,
fixed boundary conditions and a fixed convex class of admissible fields.
It does not repeat the earlier live-host relaxation calculation: eliminating
a deformable host changes the energy and can invalidate the convexity below.

## 1. Eliminate the same Newtonian potential, counting the critical term once

Write `K=4piG`, `u=K|P|`, and use the actual static action

\[
 L=-{1\over2K}|\nabla\Phi-KP|^2-\rho_b\Phi
       -W(u)-{\gamma\over2}|\nabla P|^2,
 \qquad K W'(u)={u^2\over a_0-u},\quad0\le u<a_0.    \tag{1}
\]

Assume regular finite-energy fields with boundary terms vanishing, or a
compatible finite regulator/boundary problem where the following orthogonal
longitudinal/transverse decomposition is valid. Let `P=P_L+P_T` with
`div P_T=0`; solve `Delta Phi_b=K rho_b` with the same gravitational
boundary convention. The `Phi` equation gives

\[
 \Delta\Phi=K(\rho_b+\nabla\cdot P),\qquad
 \nabla\Phi=\nabla\Phi_b+KP_L.                       \tag{2}
\]

In Fourier variables the second equality follows directly at nonzero
wave number. Harmonic/boundary modes must be fixed consistently; they are
not implicitly available as an extra switch.

The two identities needed for substitution are

\[
 \int\nabla\Phi_b\cdot P_T=0,\qquad
 \int\rho_b\Phi_P=-\int\nabla\Phi_b\cdot P,
 \quad\Phi_P=\Phi-\Phi_b.
\]

The on-shell static potential energy is minus the on-shell Lagrangian.
After subtracting the fixed baryon self-energy, it is exactly

\[
 \boxed{\mathcal E[P]={K\over2}\|P_T\|_2^2
 +\int W(K|P|)\,d^3x+{\gamma\over2}\|\nabla P\|_2^2
 -\int\nabla\Phi_b\cdot P\,d^3x.}                  \tag{3}
\]

There is no additional longitudinal `K|P_L|^2/2`: the critical term and
the field's Newtonian self-attraction already cancel there. Adding it
again would change the canonical force law. The transverse term remains
positive. In spherical symmetry `P_T=0`, (3) reduces to the earlier
linear baryon/tether interaction plus full remainder and stiffness.

## 2. Strict convexity and the exact domain of the conclusion

With `W(0)=0`,

\[
 W(u)={a_0^2\over K}
   [-\ln(1-u/a_0)-u/a_0-u^2/(2a_0^2)].              \tag{4}
\]

It is increasing and strictly convex on the nonnegative canonical
interval; `W''(u)>0` for `u>0`. At zero its Hessian vanishes, but the
leading positive cubic still makes `W(K|P|)` strictly convex as a vector
function. For distinct vectors this follows from the triangle inequality
and the strict scalar convexity; parallel and nonparallel cases both give
a strict inequality.

The other quadratic terms in (3) are convex and the source term is
linear. Hence (3) is strictly convex on any fixed convex admissible class.
The pointwise branch domain `K|P|<a0` is convex; linear constraints or
fixed boundary/flux conditions preserve this property when imposed
consistently. Therefore:

\[
 \boxed{\text{There is at most one static energy minimum in that class.}}
                                                               \tag{5}
\]

Every local minimum of a convex functional is global: if a point had a
lower-energy competitor, arbitrarily short convex interpolation toward it
would lower the energy. Strictness excludes two distinct global minima.
Existence on an infinite domain is not asserted: finite supply, boundary
conditions and infrared energy convergence require their own hypotheses.

Thus the unchanged field energy alone does not provide two metastable
on/off polarization minima in the same fixed environment and admissible
class. This does not exclude a dynamically prepared transient, conserved
action sectors, nonconvex microscopic phases or boundary/domain changes.
It also does not refute the prior live-host attraction: that route
varied an additional gravitating responder rather than keeping `rho_b`
fixed. Its separate dynamical accessibility obstruction remains in the
conversion-dynamics packet.

## 3. Forcing zero response does not make it a stationary branch

Where arbitrary small material variations are admissible, the first
variation of (3) at `P=0` is

\[
 D\mathcal E[0](\delta P)
       =-\int\nabla\Phi_b\cdot\delta P\,d^3x.         \tag{6}
\]

If `grad Phi_b` is nonzero in an open such region, a smooth compactly
supported small variation aligned with it lowers the energy. The zero
state is not a stationary responding-medium solution. A vacuum or an
active material constraint might forbid that variation; deriving such
a state-dependent constraint is exactly the missing physical selector,
not a consequence of (1) by itself.

There is also an explicit field-energy comparison when the nonzero
stationary field `P_*`, the zero field and the scaling variation `P_*`
are all admissible, with homogeneous boundary terms absent. Pairing the
Euler equation with `P_*` gives

\[
 \int\nabla\Phi_b\cdot P_*
   =K\|P_{*,T}\|_2^2+\gamma\|\nabla P_*\|_2^2
       +\int u_*W'(u_*).
\]

Consequently

\[
 \mathcal E[0]-\mathcal E[P_*]
 = {K\over2}\|P_{*,T}\|_2^2
 +{\gamma\over2}\|\nabla P_*\|_2^2
 +\int[u_*W'(u_*)-W(u_*)]>0                         \tag{7}
\]

for a nonzero field. The integrand is positive for `u_*>0`: its derivative
is `u_*W''(u_*)>0` and it vanishes at zero. Equation (7) is a field-energy
difference under its admissibility hypotheses, not a universal heat cost
or a capture/release rate. If fixed mass/flux excludes the zero field or
the scaling variation, (7) is not a permitted physical switching protocol.

## 4. Memory implication

A binding-dependent response switch must therefore do something beyond
following the same canonical energy to another local minimum. It must
derive a different physical state/domain or an additional dynamical
variable from the existing microscopic fields, and show the resulting
energy and source equations. The phase and current routes in this packet
test those possibilities rather than assume a binary mask.

No new fitted coefficient, potential, receiver or damping rate is used
in (1)-(7). No retention clock follows from a static functional. Review
provenance: coordinator analytic self-review and separately scoped
reconstruction in `audit/RESULT.md`. Exact canonical input bytes are
pinned with the packet's verification record.
