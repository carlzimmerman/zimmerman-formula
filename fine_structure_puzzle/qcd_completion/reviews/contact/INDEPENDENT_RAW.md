# Independent derivation before reading the target

Recorded 2026-10-19 02:43 UTC by the fresh `contact_independent_review`
subagent. At this point I have not opened `anomaly_contact/DERIVATION.md`, its
code, contract, or outputs. This document is deliberately preserved separately
from the subsequent target audit. The mathematical object, rather than the
target implementation, is the starting point.

## Inputs and scope

Closed oriented round Euclidean S4, volume V=8 pi^2/(3 H^4), fixed positive
chi, q^2=4 pi^2 chi, integral flux int F=2 pi Q, Q integer, and
I=(1/(2q^2)) int F wedge *F - i theta Q. The compact abelian gauge measure
is the measure of Donnelly--Michel--Wall, arXiv:1611.05920v1, equations
(2.7), (2.9), (2.14), (2.19), with fixed mass scale mu. This is an abelian
effective theory calculation. Identifying its measure or coefficients with
the composite QCD three-form is a separate unproved matching problem.

Sources read as data: cached text of Donnelly--Michel--Wall, *Electromagnetic
duality and entanglement anomalies*, v1, 17 November 2016; and Dvali,
*Three-Form Gauging of axion Symmetries and Gravity*, hep-th/0507215v1,
21 July 2005, section 4. The latter explains three-form screening and explicitly
says the exact QCD function K(F) is unknown; it does not specify this compact
Gaussian measure or a curvature response. No full-QCD conclusion follows.

Cached PDF SHA256 values:

- 1611.05920v1: 65ece3e49ef8f7ea373ecd29af67a9ce9ddc1e151b6800b3d22b6654286accd2
- hep-th/0507215v1: 42bbf4af55c1ddece1da07db4d3000946e4a29e4b5742eea5edbdeb57ebd48a4

Cached text SHA256 values:

- 1611.05920v1: 9b1283e07c9417e198a952990b6eba14390df8f1711bd179521a96f7f16293f1
- hep-th/0507215v1: 1e29faadba164f77fc628b3526a7636bdeffe190d015e5f88f82aada4ed23b43

Metadata/version are checked against the cached first pages; external retrieval
authentication is not performed in this independent stage.

## Three-form oscillator and gauge zero modes

Write D_j=det'(Delta_j/mu^2). Including every ghost-for-ghost gives

    Zosc = D_3^(-1/2) D_2 D_1^(-3/2) D_0^2.

For positive modes let C_j denote the determinant on coexact j-forms.
Hodge decomposition gives D_j=C_j C_(j-1). Hodge star and d identify
the positive spectra C_3=C_0 and C_2=C_1 in four dimensions. Hence

    log Zosc = -1/2 log C_3 +1/2 log C_2
               -1/2 log C_1 +1/2 log C_0 = 0.

The cancellation pairs equal positive spectra; with a common zeta/spectral
regulator there is no residual H-dependent oscillator determinant. It does
not follow merely from the absence of propagating polarizations. There is
no multiplicative-anomaly step involving products of noncommuting operators.

On S4, b0=b4=1 and b1=b2=b3=0; there is no torsion. Only the last scalar
ghost-for-ghost zero-mode volume remains in equation (2.14), with Gamma_0=V:

    Zzero = (2 pi mu^8 V/q^2)^(-1/2)
          = sqrt(2 pi chi/V) mu^(-4).

Thus dropping the gauge zero-mode factor would introduce a spurious sqrt(V)
after Poisson resummation. The fixed-mu normalization can depend on q and the
Euler characteristic; this is not an H-dependent stress on a fixed topology.

## Flux sum, branch sum, and the sign of the response

The harmonic representative is F_Q=(2 pi Q/V) vol_g, so

    I_Q = Q^2/(2 chi V) - i theta Q,

    Z3 = sqrt(2 pi chi/V) mu^(-4)
         sum_Q exp[-Q^2/(2 chi V)+i theta Q]
       = N3 sum_k exp[-chi V (theta+2 pi k)^2/2],

    N3 = 2 pi chi mu^(-4).

The second line is Poisson summation, with its sqrt(2 pi chi V) Jacobian
explicit. N3 is independent of V when chi and mu are held fixed.

With rho defined by rho=-partial_V log Z3 at fixed theta, chi, mu,

    rho3 = (chi/2) <(theta+2 pi k)^2>_branches
         = 1/(2V) - <Q^2>_flux/(2 chi V^2).

The flux expectation may be complex away from theta=0; the branch formula
is positive and real. At theta=0,

    rho3 = 2 pi^2 chi <k^2>
         ~ 4 pi^2 chi exp[-2 pi^2 chi V].

In particular the coefficient of H is zero for the flat-subtracted response
in this specified model. The correction is exp[-constant*chi/H^4]. Inserting
an unspecified metric-dependent multiplicative factor into Z changes rho;
none is fixed by matching only the flat susceptibility.

## Compact singlet constant mode

Let phi in [-pi,pi), a compact angle with canonically normalized field f phi,
and let B>=0. Set

    W_k(phi;theta)=B(1-cos phi)+chi(theta+phi+2 pi k)^2/2.

The normalized scalar zero eigenfunction is 1/sqrt(V), so its coefficient
is a0=f sqrt(V) phi. The canonical bosonic zero-mode measure is

    mu da0/sqrt(2 pi)=mu f sqrt(V) dphi/sqrt(2 pi).

Consequently the exact constant-mode partition function, including the same
three-form normalization as above, is

    Z0 = N3 mu f sqrt(V/(2 pi))
         int_[-pi,pi) dphi sum_k exp[-V W_k(phi;theta)]
       = N3 mu f/sqrt(chi) exp[-BV]
         sum_Q I_Q(BV) exp[-Q^2/(2 chi V)] exp[i Q theta].

Here I_Q(x)=(1/(2 pi)) int_[-pi,pi) exp[x cos phi] exp[i Q phi] dphi.
Both formulas fix the global branch/flux normalization. A Haar probability
measure dphi/(2 pi) is a different, metric-dependent convention relative
to the canonical coefficient measure; it cannot be substituted silently.

At B=0, summing branches unfolds the compact integral to the real line:

    int dphi sum_k exp[-chi V(theta+phi+2 pi k)^2/2]
      = sqrt(2 pi/(chi V)),

    Z0(B=0)=N3 mu f/sqrt(chi).

Thus Z0 is exactly independent of V and theta: rho0=0 and susceptibility=0.
Equivalently I_Q(0)=delta_(Q,0). A residual 1/(2V) here diagnoses a
measure error or a duplicated scalar zero mode.

## Large volume at theta=0 and limits

At theta=0 unfold x=phi+2 pi k and use periodicity of cos:

    Z0=N3 mu f sqrt(V/(2 pi)) int_R exp[-V W(x)] dx,
    W(x)=chi x^2/2+B(1-cos x).

For chi>0, B>=0, W has the unique global zero at x=0 and
lambda=W''(0)=chi+B>0. The ordinary Laplace expansion gives

    Z0=(N3 mu f/sqrt(lambda))
        [1+A1/V+A2/V^2+O(V^(-3))],
    A1=B/(8 lambda^2),
    A2=-B/(48 lambda^3)+35 B^2/(384 lambda^4),
    log Z0=log(N3 mu f/sqrt(lambda))
       +B/(8 lambda^2 V)+B(3B-chi)/(48 lambda^4 V^2)+O(V^(-3)),
    rho0=B/(8 lambda^2 V^2)
          +B(3B-chi)/(24 lambda^4 V^3)+O(V^(-4)).

This constant-mode approximation therefore has leading H^8 behavior for
B>0 at theta=0, with the B=0 response vanishing identically. A massive
nonzero-mode scalar determinant is additional to this calculation; its
zero eigenvalue must be omitted if Z0 is already included. A conventional
one-loop Hessian at the dominant constant saddle, multiplied by the exact
Z0, is an approximation to the interacting field theory, not an exact
factorization when the Hessian depends on phi.

For theta near zero, minimization yields the infinite-volume susceptibility
chi_eff=chi B/(chi+B), since phi_*=-chi theta/(chi+B)+O(theta^3).
At theta=0 both iterated B->0, V->infinity limits of rho0 and Z0 agree.
For fixed theta not 0 modulo 2 pi, E_B(theta)=min W_k>0 for every B>0.
Then Z0(theta)/Z0(0)->0 when V->infinity first, while B->0 first gives
the ratio identically one. These limits do not commute for that ratio
(or for the unnormalized Z at theta!=0), despite commuting for the
limiting energy density and susceptibility. Any assertion of commuting
limits needs to name its observable and theta range.

## Open dependencies

Nothing above supplies the QCD matching of B, f, chi or gravitational
counterterms; higher F terms; the full chiral flavor manifold; the global
measure of the composite Chern--Simons field; a response in other states
or boundary geometries; or a nonlocal massless-QCD curvature theorem.
In particular this calculation does not calculate the fine-structure
constant or settle an arbitrary QCD coefficient linear in H.
