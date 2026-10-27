# Local interface: energy and stationary-state tests

All statements below concern the inherited spherical effective energy, with
mass positions and baryon kinematics fixed. They are not a general theorem
about galaxies. Review: self-audit, not independent review.

## Constant stiffness has an irreducible exterior cost

Write x for the mixing angle, q=sin²(pi x/2), and

    E_grad = a0² ell²/(2G) integral r² (dx/dr)² dr.

For boundary difference Delta=x(Rin)-x(Rout), Cauchy–Schwarz gives

    Delta² <= [integral r² x'² dr] [1/Rin-1/Rout].

Thus E_grad >= a0² ell² Delta²/[2G(1/Rin-1/Rout)]. Equality is attained
by x=A+B/r. Taking Rout to infinity leaves the positive cost proportional
to Rin. An arbitrarily broad front does not remove it in three dimensions.
For q_in>=.95 and q_out<=.05 on the principal branch, Delta>=.7128674.
This is an energy requirement, not an exclusion against an unspecified
assembly-work supply. Ordinary gravitational energies cancel only in the
fixed-density phase experiment, not in actual formation.

At the last mass node R, the exact minimized vacuum exterior contributes
.5 (ell/rM)² R x_last² in dimensionless variables. Retaining this term
distinguishes a phase approaching zero at infinity from a no-flux boundary.
The vacuum phase field itself is an assumption inherited from the constant
stiffness model. A stiffness carried only by matter would be a different model.

## Sufficient exclusion in the discrete fixed-density model

Let A map q to dimensionless enclosed T field u, V be cell volumes, C>=0,
and L include the interior stiffness and exact exterior capacity. On
0<=x_i<=1, h'(x_i)>=0, all mass derivatives of the W energy are nonnegative,
and derivatives of F(u)=u²/(1-u) are nonnegative for 0<=u<1.
For s(x)=sin²(pi x)/pi², |s'(x)|<=2x. Hence

    x . grad E >= x^T [L - 2 beta diag(C V F(u0))] x,

where u0=A1 and F(u)<=F(u0). The terms omitted on the right are
nonnegative. A positive definite bracket excludes every nonzero interior
stationary point in this principal phase box. It also excludes a constrained
minimum: -x is a feasible direction, with strictly negative directional
derivative. This says nothing about a different phase winding, moving mass,
additional work reservoir, or altered energy. Decimal eigenvalues certify
the tested matrices numerically, not continuum positivity by interval proof.

The small-disk template has positive lowest generalized eigenvalue about
2836 at n64,128,256 with ell30 kpc. The large-disk template gives about
-7.06: that sufficient test is inconclusive there. Boundary continuation
supplies additional numerical evidence, not exhaustive branch exclusion.

## Response-weighted variant and its reciprocal terms

The new postulate replaces r² x'² by r² F(u) x'². In the discretization,
u_mid=A_mid h(x), d=Dx, and k are the constant-stiffness link weights:

    E_links = .5 sum k F(u_mid) d²
    grad E_links = D^T[k F(u_mid)d]
                  + h'(x) A_mid^T[.5 k F'(u_mid)d²].

The second term is essential. Its derivative produces both mixed terms,
the F'' term, and the h'' term included in response_stiffness.py. Changing
the stiffness without these terms is not the same energy-based mechanism.

In a vacuum exterior u=M/r². The inverse stiffness integral from R to L is

    integral dr/[r² F(M/r²)] = (L³-R³)/(3M²) - (L-R)/M.

Consequently E_tail=.5 ell² gamma(M) x_last², with a=(L³-R³)/3,
b=L-R, gamma=M²/(a-bM), gamma'=M(2a-bM)/(a-bM)², and
gamma''=2a²/(a-bM)³. These are included, with M=sum m_i h(x_i).
The M=0 limits are taken by the algebraic expression. L=2 or4 times the
reservoir radius is an explicit environmental boundary assumption.
Infinite L gives zero capacity as an infimum and is not substituted for
an attained finite-boundary minimizer.

## Energy bookkeeping and interpretation

The positive fixed dissipation metric M gives M xdot=-grad E and
Qdot=grad E^T M^-1 grad E, so d(E+Q)/dt=0. Q is independently integrated.
Its time normalization and microscopic carrier remain unspecified. Results
at time100 are relaxation experiments, not lifetimes in Gyr.

Uniform F has zero extra phase/field energy and remains stationary. All
extra energy terms are nonnegative. Damping alone therefore cannot form T
from exactly F. Formation needs explicit work; a finite-work pulse is not
a solution if the converted state then collapses. This motivates testing
preservation before adding another assembly pump.

The retained free mass is included in the conditional source diagnostic
log10[law(g_b+g_F)/law(g_b)]. This is NOT a computed acceleration residual
of the mixed dynamical system: phase/interface forces and mass motion would
also enter. No successful galaxy-law test is asserted from this diagnostic.
