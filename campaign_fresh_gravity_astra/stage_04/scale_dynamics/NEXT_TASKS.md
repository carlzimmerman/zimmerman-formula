# Proposed small-model follow-ups for coordinator review

These are proposed tasks, not accepted conclusions. The coordinator owns the
shared queue and can publish them after reviewing SD1. Do not publish this
candidate as a closed theory.

## SD1-A: independent core-vacuum identification audit

Input: DERIVATION.md sections 1, 3 and 6 at the reported exact hash. Re-derive
the zero-gradient homogeneous chi equation and the units of the identity
a²=kappa² c² G rho_Lambda. Under the *explicit additional identification*
rho_Lambda c²=U_total(chi)/(4 pi G), establish or refute that
U_total=4 pi a_ref² exp(2chi)/kappa² and hence no finite stationary positive
vacuum exists. Check whether adding a constant changes the derivative result.
Separately audit the uniform-scale contradiction U'(chi_c)=T(g(x),a_c), T_g>0.

Success: a fresh exact derivation with every physical identification separated
from mathematical consequences. Refutation: an explicit finite stationary
counterexample satisfying the stated canonical action, pointwise density
identity and positive vacuum without an extra source. Do not change the action
class to manufacture a counterexample; alternatives are a separate deliverable.

## SD1-B: outer-boundary test of the spherical backreaction

Input: equation (7), same source B/a_ref=3r/(1+r²)^(3/2), same potential, S=5,20
and ell=0.2,1. Repeat Q/R solves at outer radii 8,16,32,64, fixing chi=0 at
each boundary. Compare chi and fractional force correction on r<=4. Derive
the far-field leading asymptotic chi(r)~sqrt(3)/(S r³), using deep-MOND T and
the radial scale equation, and test whether r³ chi approaches sqrt(3)/S away
from the imposed boundary.

Success: quantified interior boundary convergence and matching asymptotic
coefficient within the declared numerical tolerance. Refutation: the claimed
size-dependent correction vanishes, changes sign, or fails convergence after
verified solver convergence. No observational fit or physical length choice is
authorized by this test.

## SD1-C: coupled scale-plus-fluid instability polynomial

Conditional on acceptance of the stage-four matter lane's local background
conventions, combine its pressure fluid with SD1's two fields. At a uniform
equilibrium define D_phi=Lambda k²-K omega²/c² and
D_chi=J k²+m-J omega²/v_chi². Derive independently, including every sign,
whether the coupled density-mode polynomial is

    (D_phi D_chi-q² k_parallel²)(omega²-c_s² k²)
      +4 pi G rho0 k² D_chi = 0.

This displayed expression is a proposed starting target requiring verification,
not an additional accepted SD1 theorem. First check q=0, rho0=0 and K->0
limits against their exact reduced equations. Then determine whether a new
short-wave instability appears despite the field-only Schur bound; separate
any long-wave gravitational instability from a kinetic ghost or short-wave
ill-posedness. Use a bounded parameter grid only after deriving those limits.

Success: correct polynomial, limiting checks and scoped instability criterion.
Refutation: a sign/normalization counterexample or an unbounded short-wave
unstable branch under the declared positive kinetic/stiffness assumptions.
Do not assert that an unsupported uniform matter-plus-gravity background is an
exact global solution; use the matter lane's explicitly declared local setup.
