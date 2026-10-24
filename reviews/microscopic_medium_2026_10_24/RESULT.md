# Same microscopic medium: health, protected vacuum stress, and response freedom

**The requested microscopic selector has not been found.** This investigation reached a concrete common-medium candidate, followed its constrained exception and checked a published higher-energy construction. None fixes both a positive gravitating vacuum and an operational MOND response without independent data. The result is not a universal no-go theorem.

Base: 12df931233c546de03d3c675861946a0ba336e89. Initial criteria-only commit: 36c2d800d1. Adaptive constrained-branch criteria-only commit: 0e132d0606. Parent: ../a0_selection_2026_10_24/RESULT.md. Kappa=1/2 remains FITTED; CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 are separate observations, not inputs here. This packet makes no numerical kappa prediction.

## 1. A common medium has a nontrivial stability constraint

Use signature (-,+,...,+), c=1, n spatial dimensions. Let theta be a clock and phi^I material coordinates. Assume internal shifts and O(n) rotations and a regular first-derivative action P(X,B,C), where

    X=-g^munu theta_mu theta_nu,
    B^IJ=g^munu phi^I_mu phi^J_nu,
    C^I=g^munu theta_mu phi^I_nu.

Locally the isotropic background is theta=mu*t, phi^I=q*x^I, with mu,q nonzero. Write a=P_X, P_BIJ=b delta_IJ, and the quadratic C term as gamma C^I C^I. This is a Taylor expansion of a general isotropic function, not a microscopic specification of its coefficients. Remaining Hessian coefficients are retained as arbitrary elastic, clock-kinetic and mixing terms below.

Direct variation gives

    rho=-P+2mu^2 a,    p=P-2q^2 b,
    h=rho+p=2(mu^2 a-q^2 b).

For clock perturbation pi and material displacement sigma, C^I=-mu*sigma_dot^I+q*partial_I pi+O(perturbation^2). Their relevant quadratic coefficients are

    L2 contains K |sigma_dot|^2 + S |grad pi|^2,
    K=-b+gamma mu^2,    S=-a+gamma q^2,
    q^2 K-mu^2 S=h/2.                                      (1)

The last equation is the key identity. Positive kinetic energy for a retained material mode requires K>0; positive energy for an independent clock spatial gradient requires S<0. Therefore h>0 is necessary on this nondegenerate branch. Exact vacuum stress h=0 instead forces K/mu^2=S/q^2, incompatible with those two strict signs.

The longitudinal mixing does not repair the ordinary positive-elastic branch. Write its local quadratic action as

    A*pi_dot^2 + K*sigma_dot^2 + S*pi_x^2 - L*sigma_x^2
        +2M*pi_dot*sigma_x,

with A,K,L>0. The characteristic polynomial is

    A K omega^4 + (K S-A L-M^2) omega^2 k^2 - S L k^4.

At h=0, K>0 forces S>0. The product of the two omega^2 roots is negative for k nonzero, independent of M: one mode grows. A vanishing A or K invalidates this argument and requires constrained-mode analysis. A negative elastic modulus does not constitute positive-energy repair. We do not discard fields before applying the identity.

This is a local high-frequency/decoupling statement. It applies to a cosmological model only if a physical interval above curvature/mixing scales and below its cutoff exists. It is not a full FLRW constraint analysis or an exclusion of arbitrary higher derivatives, singular response functions, nonlocal states or degenerate theories. The n-independent identity follows from isotropy; the executable uses one longitudinal direction, sufficient to falsify generic positive energy.

Near vacuum there is no such absolute exclusion. For mu=q=1, any h>0 and 0<tau<1 allow

    a=b+h/2, gamma=b+tau*h/2,
    K=tau*h/2, S=-(1-tau)*h/2.

With fixed field normalization both coefficients vanish as h tends to zero. This establishes a shrinking kinetic/stiffness budget, not a universal strong-coupling scale or a prediction for a0. Other coefficients and interactions must be calculated to establish those.

## 2. The simplest exactly vacuum-like constrained branch

The determinant medium is a useful explicit exception. In d=n+1 dimensions set

    J=det(partial_mu phi^A)/sqrt(-g),    S_medium=int sqrt(-g) U(J),

on an invertible oriented field map. Variation of the cofactor and the Jacobian identity give

    cofactor(mu,A) partial_mu U'(J)=0,
    U'(J)=C,    T_munu=[U-J U']g_munu.

On a connected branch with U'' nonzero, J is constant. Thus rho=J U'-U and p=-rho, but C is an integration constant. For

    U=-epsilon+alpha(J-J0)^2/2,    alpha nonzero,

one obtains

    J=J0+C/alpha,
    rho=epsilon+J0*C+C^2/(2alpha).

This selects no absolute vacuum. It also has no independent local J fluctuation supplying a static MOND force on that branch. Singular U''=0 cases, boundaries and added operators are separate models. This is the medium version of the already known flux/integration-constant problem, not a newly discovered universal obstruction.

## 3. A genuine protected exception, and the operator it still permits

The literature contains symmetry-protected Lambda-media with nontrivial perturbations despite vacuum-like background stress. Their constrained modes prevent applying section 1 indiscriminately. We followed this exception rather than closing the route on the generic stability test; exact source pins are in SOURCES.md.

For a solid let Y=u^mu partial_mu theta, tau_m=Tr(B^m). The internal rescaling theta -> lambda^(-n) theta, phi^I -> lambda phi^I permits functions of

    Q=Y*tau1^(n/2),    r=tau2/tau1^2-1/n,

and higher normalized shape invariants. The accompanying chemical shift theta -> theta+f(phi) leaves Y invariant. The equation-of-state Ward operator is

    D=Y partial_Y -(2/n) sum_m m*tau_m partial_tau_m,
    DQ=Dr=0.

Thus the same symmetry that enforces the vacuum-like equation of state permits both

    delta U=eta*r,    delta U=eta*r^2.

At B=q^2 times the identity, r=0 and its full first matrix variation vanishes. The first deformation preserves background stress and changes shear stiffness. The second also preserves all quadratic data while changing nonlinear response. On the explicit positive trace-preserving strain B/q^2=diag(1+s,1-s,1), |s|<1,

    r=2s^2/9,
    (eta*r)'' at s=0 =4eta/9,
    (eta*r^2)'''' at s=0 =32eta/27.

The algebraic statement is exact. It does not prove that every eta preserves all constraints or full nonlinear stability. It proves the listed internal symmetries do not impose a unique response function. A constant addition to U also obeys the Ward identity and changes gravitating vacuum stress.

Formally r^(3/2) has a strain cubic. That is nonanalytic at isotropy and is not a regular microscopic interaction derived here. Most importantly, strain is not gravitational acceleration: neither deformation is automatically the MOND operator. A complete microscopic matching calculation would need to establish that dictionary. No strain coefficient is renamed a0.

## 4. Following the exception to a higher-energy construction

We inspected the cited vector-condensation construction of Blas and Sibiryakov (arXiv:1410.2408v2). It introduces vector fields coupled to material coordinates, with mixing m_A V_a^i partial_i phi^a and a separate constant V0. On its displayed branch mu^2=m_A M_V; its cosmological equations contain vacuum density V0-3mu^4/2. The article explicitly adjusts V0 to cancel that contribution. Therefore its higher-energy dynamics does not remove the independent vacuum datum. It also does not establish the exact Lifshitz symmetry or MOND response needed here. This is a higher-energy completion of a related massive-gravity phase, not a demonstrated completion of the full Lambda-medium selector. See SOURCES.md for equations and scope.

This is a substantive failure of a specified candidate: even after following the response degrees of freedom to an explicit vector-condensation parent, the positive vacuum and response are not fixed together. We have not recomputed its loops or classified all vector completions.

## 5. Higher derivatives: an infrared qualification, not an automatic repair

For the unmixed clock example with A>0, S>0, add positive spatial energy D(laplacian pi)^2, D>0. Then

    omega^2=(-S k^2+D k^4)/A,
    k_c^2=S/D,
    k_fast^2=S/(2D),    growth_fast=S/(2 sqrt(A D)).

The k^4 term stabilizes high momentum but leaves a low-momentum band in this approximation. Whether the band lies inside a physically controlled subhorizon region requires H, the cutoff, mixing and the state. This calculation alone does not rule out a finite-horizon or constrained repair. D is additional matching data, not a selector for the original response coefficient.

## Evidence, review, and continuation

- check.py: 15/15 exact symbolic checks; run/ stores result and bounded provenance.
- run_MUTATE/: incorrect portal and k^4 signs produce failures and exit 1, as expected.
- constrained_check.py: 9/9 exact identities; constrained_run/ stores provenance.
- Computation validates algebra, not the existence of a microscopic quantum state or its measured gravity law. Self-review only; no independent audit.
- Self-audit separates generic nondegenerate modes from protected degeneracies, mean pressure from full anisotropic stress, strain from acceleration, and related UV models from an exact completion. It retains finite-horizon and higher-derivative qualifications.
- No forbidden numerical acceleration input appears in the scripts; no numerical kappa is output. Scaling, rename, pi-weight and significance tests for numerical hits are inapplicable, not passed. No claim of novelty, universal impossibility, or completion.

The common-medium route remains open only with additional microscopic input. A concrete resumption needs a specified microscopic theory that realizes the constrained symmetry and fixes the function U and its absolute vacuum, or a controlled nonlocal/higher-derivative state whose constraints evade section 1. Merely choosing U, V0 or eta is not such input. The published parent tested here does not provide it. The first unproved bridge remains a healthy, calculable acceleration response and absolute stress from one microscopic state. No available calculation here warrants presenting a mechanism as found.
