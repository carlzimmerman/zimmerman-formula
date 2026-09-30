# Equation completeness on a regular stationary vacuum patch

Verdict: proved under the explicit covariant completion and regularity
conditions below. This is self-review. It closes an independent-equation
gap in the expansion-bridge branch, not the original 32π goal. Base
b58f7e692c922c3efbc4c299081eb0040f0d9cbb; the previous own checkpoint was
23f9b36d8. Previous numerical profiles remain finite evidence, not exact
solutions certified by this implication theorem.

## Explicit theory and claim

Take signature (−,+,+,+), a scalar foliation field T with timelike gradient,
and a covector B_mu. Define

    u_mu=−partial_mu T/sqrt(−g^{alpha beta}partial_alpha T partial_beta T),
    h^{mu nu}=g^{mu nu}+u^mu u^nu,
    p^mu=h^{mu nu}B_nu, P=sqrt(p_mu p^mu),
    a_mu=u^nu nabla_nu u_mu,
    K_mu nu=h_mu^alpha h_nu^beta nabla_alpha u_beta,
    Theta=nabla_mu u^mu=K_mu^mu.

R3 denotes the intrinsic scalar curvature of the T leaves. Consider the
specific local action

    S=integral sqrt(−g) [M²/2(K_mu nu K^{mu nu}−lambda Theta²+R3)
       +2M² p^mu a_mu−M²P²−U−beta M²P³/Theta] d4x.

This supplies one covariant realization of the earlier preferred-foliation
action. It does not establish uniqueness, quantum protection, hyperbolicity,
absence of extra unhealthy modes, or viability. The denominator restricts
the branch. The proof uses smooth fields on an open patch with N>0,
R>0, R' nonzero, P>0 and Theta>0, and compactly supported variations.
The P=0 de Sitter background can be checked separately; no differentiability
claim at arbitrary zero-polarization configurations is needed here.

Claim: on such a spherical stationary vacuum patch, vanishing of the four
areal-gauge Euler equations for N,sigma,V,P implies the remaining angular
metric equation and the foliation-field equation for this specified action.
This is a conditional implication for exact profiles, not a statement that
the finite offset integrations vanish exactly or cross their critical point.

## Restore the radius before varying

Use an arbitrary radial coordinate x and areal-radius field R(x):

    ds²=−N²dt²+exp(2sigma)(dx+Vdt)²+R²dOmega².

Let A=exp(sigma), F=V'+V sigma', W=V R'/R,
Theta=−(F+2W)/N, Q=F²+2W²−lambda(F+2W)².
For outward polarization, the general-radius action per unit solid angle,
after integrating the intrinsic curvature term once, is

    L=M² A R² Q/(2N)+M²N[A+(R')²/A]+2M²N' R R'/A
      +2M²R²P N'−N A R²[M²P²+U+beta M²P³/Theta].

The curvature boundary is −2M²N R R'/A. Its derivative exactly accounts
for the difference from the raw intrinsic-curvature expression. Setting
R=x and R'=1 recovers the preceding areal action, including its boundary
convention. The metric-variable map to (g_tt,g_tx,g_xx,g_theta theta)
has Jacobian determinant 8N R A⁴, so it is locally invertible in this domain.

## Radial Noether identity supplies the angular equation

Write E_f=partial L/partial f−d(partial L/partial f')/dx.
Under a radial infinitesimal relabeling with parameter xi(x),

    delta N=xi N', delta R=xi R', delta P=xi P',
    delta sigma=xi sigma'+xi', delta V=xi V'−V xi'.

The Lagrangian is a radial density. Direct symbolic checks give

    L_sigma'−V L_V'=0,
    L_sigma−V L_V+N'L_N'+sigma'L_sigma'+R'L_R'+P'L_P'=L.

The first is the vanishing coefficient of xi'' and the second is its density
weight at xi'. Integrating the variation by parts yields the off-shell identity

    N'E_N+sigma'E_sigma+V'E_V+R'E_R+P'E_P
       −(E_sigma−V E_V)'=0.

There is an algebraic certificate as well. Since L has no explicit x,
sum f'E_f=d[L−sum f'L_f']/dx. The two density identities imply
E_sigma−V E_V=L−sum f'L_f'. Their derivatives therefore reproduce the
Noether identity exactly, without dropping a field equation.

If E_N,E_sigma,E_V,E_P vanish throughout the patch, then R'E_R=0.
Because R' is nonzero, E_R=0. In areal gauge R'=1. This is the angular
metric equation; it was not an independent missing equation in this domain.
At a turning point of R the division is unavailable and a separate chart
or unreduced analysis is required.

The previously used radial metric combination and lapse subtraction recover
E_sigma once the shift equation is imposed, so the four-equation closure
uses the required E_sigma rather than merely a Poisson approximation.

## Covariant identity supplies the clock equation

Use the variation convention

    delta S=integral sqrt(−g)[E^{mu nu}delta g_mu nu/2
                              +E_T delta T+E_B^mu delta B_mu] d4x.

Under a compactly supported spacetime diffeomorphism, integrate the Lie
variations by parts. Covariance gives the off-shell identity

    −nabla_mu E^{mu}{}_nu+E_T partial_nu T
       +E_B^mu nabla_nu B_mu−nabla_mu(E_B^mu B_nu)=0.

This derivation applies also to the higher derivative dependence through u,
K and R3; no second-order field-equation or health assumption is being made.
When all metric and B equations vanish on a neighborhood, it reduces to
E_T partial_nu T=0. The timelike gradient is nonzero, hence E_T=0.

Why the reduced equations suffice for these premises: spherical symmetry
leaves the four metric components represented by N,sigma,V,R. The stationary
invariants have no time dependence, so time derivatives of their variational
coefficients vanish on this sector. B has a redundant normal component,
since its projection p is unchanged under B_mu→B_mu+alpha u_mu. Its field
equation is consequently spatial. Rotational symmetry leaves only the
radial spatial component; the outward amplitude P parametrizes it. Thus
E_P=0 implies E_B=0 on this branch. The metric map is invertible after
these polarization equations are imposed, even though holding P fixed is
not identical to holding B fixed during metric variation: their difference
is proportional to E_B and vanishes on shell.

Together these facts give all stationary spherical metric equations and
then the T equation for the explicit completion. They do not constrain a
different dynamical theory that happens to share the same static reduction.

## Limits and corrected research state

The angular and foliation redundancies are now established for exact smooth
regular vacuum solutions of this action. This corrects the previous *untested*
completeness status; it does not rewrite the prior evidence as having already
checked these identities. Six symbolic certificates pass: curvature boundary,
highest radial gauge derivative, density weight, Euler combination, metric
Jacobian and recovery of the areal action. The accompanying bounded-run
manifest pins the exact script and results.

No error estimate for a derivative of a numerical residual is supplied.
The Noether identity contains (E_sigma−V E_V)', so small sampled residuals
alone cannot bound the angular error. A smooth exact construction or direct
numerical residual/derivative control is still needed near the critical point.

Matter would add its own Euler terms to the identities. A prescribed density
inserted only into the lapse equation is not enough: a conserved covariant
source and its equation of motion/stresses are required before applying the
same completeness conclusion to an interior. Boundary conditions, the
Theta=0 pole, a center R=0 and a critical crossing remain separate issues.

The next mathematical obligation is therefore the smooth critical-manifold
connection, followed by a conserved source and the chosen cosmological
boundary. The full dynamical/causal health and physical Newton/galaxy
dictionary remain unproved. These Noether identities hold for every allowed
beta and U; covariance does not select either parameter or derive 32π.
