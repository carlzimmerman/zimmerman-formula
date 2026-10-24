# Quantum metric protection: cancellation, source and vacuum together

The requested parameter-free microscopic mechanism remains unresolved. This calculation closes one concrete minimal candidate: obtaining the vacuum and response from the same universally coupled quantum matter sector. Exact protection of its redundant scalar removes the direct baryonic source; the minimal mixed-gravity extension has a quadratic scalar and no healthy stable positive-vacuum stationary point. These are conditional action-level results, not a theorem about all quantum gravity.

Kappa=1/2 remains FITTED. CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 remain distinct and unused. No a0 or cosmological measurement enters the executable.

## Source support and scope

[Heat kernel expansion, hep-th/0306138v3](https://arxiv.org/html/hep-th/0306138v3), equations 4.26-4.28 and section 8.1, supplies the local covariant expansion and its mass-gap/slow-background limitations. Vacuum and Einstein operators are distinct terms; the expansion does not fix their finite microscopic matching data. The heat-kernel coefficient called a0 is unrelated to MOND acceleration.

[Scalar-tensor theories, trace anomalies and the QCD-frame, 1202.2105v2](https://arxiv.org/html/1202.2105v2), sections II and IV, supports preservation of universal matter-metric coupling by matter loops with an appropriate regulator. It does not claim preservation of a vanishing scalar kinetic coefficient, a vacuum/response amplitude identity, or a MOND law. Gravity and scalar loops are outside that protection statement.

These are source applicability checks. The algebra below is our own application, not a claimed theorem from either paper. Existing SUSY counterexamples in ../../why_4_puzzle/W4_08_positive_mond_amplitudes/formal/symmetry_protection/LOCAL_SUSY.md are inherited; they are not counted as new results here.

## Minimal microscopic matching hypothesis

Let a massive matter sector see only

    gtilde_mu_nu=A(theta)^2 g_mu_nu, A=exp(q theta).

Integrating out heavy fluctuations leaves, to two derivatives,

    Gamma_m = integral sqrt(-gtilde)[b Rtilde-v] + higher derivatives.

Keep light probes coupled to the same physical metric. Add B R/2-Vd in the g frame. B is a separate gravitational coefficient, not a baryonic density. b and v denote renormalized coefficients, including necessary finite matching terms; neither their sign nor value is presumed universal. This is not a calculation of the complete Standard Model determinant, and massless matter, finite-density effects and quantum gravity are not integrated out.

Use signature -+++, D=d+2>2, and P=Mref^d>0. Up to a boundary term the scalar-tensor action is

    L=F R/2-Z(partial theta)^2/2-V,
    F=B+2b A^d,
    Z=-2b d(d+1)q^2 A^d,
    V=Vd+v A^D.

The negative sign of Z for positive b is not by itself a physical diagnosis: scalar-metric mixing must first be removed. Boundary terms are assumed treated consistently and do not affect the local bulk test.

## Physical quadratic coefficient and source

Transform to gE=(F/P)^(2/d) g on F>0. The diagonal scalar coefficient and matter coupling are

    K=P[Z/F+(d+1)/d (F'/F)^2]
     =-2b d(d+1)q^2 A^d B P/F^2,
    AE=A(P/F)^(1/d),
    qE=d log(AE)/d theta=q B/F.

For B=0 and b>0, both K=0 and qE=0. The pure-induced Einstein frame is a constant rescaling of the matter metric. With Vd=0 as well, theta is a redundant parametrization of this sector, not an independently sourced MOND mediator. Appending a scalar interaction can break that redundancy, but does not recreate a direct matter charge in this limit. Other sourced backgrounds or additional portals require a separate calculation.

For B>0, b!=0 and q!=0, qE survives but K is nonzero. In this minimal action b>0 gives K<0, a ghost at the constant-scalar vacuum; b<0 can give K>0 where F>0. Setting b=0 is an exception, not a consequence of metricity. Additional scalar terms can repair or cancel K, but their coefficients require a matching/protection mechanism.

An explicit extra original-frame kinetic coefficient that would cancel K is

    Zct=2b d(d+1)q^2 A^d B/F.

Choosing it simply imposes the required relation; the universal matter-metric identity has not derived it. Bare power counting or an original-frame scalar coefficient alone would miss this distinction.

## Vacuum stationarity does not rescue the minimal model

In D=4, let w=A^2>0, F=B+2bw and P=Mref^2. The Einstein-frame potential is

    U=P^2(Vd+v w^2)/F^2,
    U_theta=4q P^2 w(v B w-2b Vd)/F^3.

A finite nondegenerate stationary point requires

    wstar=2b Vd/(v B)>0, Fstar>0,
    Ustar=P^2 v Vd/(v B^2+4b^2 Vd).

Scaling (v,Vd) by the same positive factor leaves wstar, K and qE unchanged but scales Ustar. These are allowed matching changes of this specified effective action, not a proof that every change has a quantum-gravity completion. Stationarity therefore does not select the vacuum amplitude.

There is a stronger health test. At the finite stationary point, exact differentiation gives

    m_theta^2=U_theta_theta/K=-4 Ustar/(3P).

For a healthy K>0 and positive vacuum, the Einstein equation gives H^2=Ustar/(3P), hence

    m_theta^2=-4H^2.

This is a tachyon, not a stable attractor. The homogeneous linearized de Sitter scalar obeys ddot(delta theta)+3H dot(delta theta)-4H^2 delta theta=0, with an exponentially growing exp(Ht) mode and a decaying exp(-4Ht) mode. The growth rate is an analytic consequence of the mass identity, not a cosmological simulation. If K<0 the branch is already a ghost. If K=0, canonical mass division is invalid and the pure-induced limit must be treated separately as above. Boundary/runaway limits are not finite stationary vacua and are not excluded by this mass test.

The relation is exact only for the displayed two-derivative action. Higher operators, additional fields, a different matter portal, or a critical/nonlocal response can change it. No whole-theory health claim or general de Sitter no-go is made.

## Why this does not yet give a0

A gapped local derivative expansion in this setting does not supply a leading nonanalytic static |grad theta|^3 operator about a smooth zero-gradient vacuum. Adding that operator with coefficient C would be additional EFT data. The pure-induced limit removes its direct baryon source, while the mixed model has the kinetic/vacuum problems above. No relation selecting C, q and positive U has been derived; no physical a0 or kappa follows.

The specific remaining research obligation is to find a nonredundant dynamical sector whose identity protects the physical kinetic cancellation while retaining qE, selects a stable positive vacuum, and computes the cubic response. Metricity alone is insufficient. Calling a field-redefinition cancellation a quantum protection mechanism would have given the wrong answer here.

## Evidence

Criteria committed before any executable: 09a5823e84. Fourteen exact symbolic checks pass. Reversing the induced kinetic sign causes four expected baseline failures, including the pure-induced cancellation and stationary mass identity; mutation exits 1. Manifest validation is separate from mathematical interpretation. No independent agent review, full determinant computation, quantum-gravity flow or numeric fit was performed.
