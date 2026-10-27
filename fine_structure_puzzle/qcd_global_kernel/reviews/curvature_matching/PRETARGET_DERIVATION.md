# Independent constant-background curvature calculation

Saved 2026-10-19 before reading chiral_zero_mode/ or compact_chiral/ targets.
Only the delegated action and the source coefficient quoted in the task were
known. Source/basis checks follow separately; no source error is inferred.

Use the Euclidean action

    L2 = F2 Tr(partial U partial Udag)/4 - F2 M2 a0 + u C s(U),
    U=a0+i a.tau, a0 squared+|a| squared=1,
    s=a1 squared+a2 squared, u=e2, C=Z F4.

For the constant background U0, split U=U0 exp(i tau.pi/F). The kinetic term
is canonical to quadratic order, (partial pi_i) squared/2, independently of U0.
The right-exponential coordinate expansion is

    a0' = a0 - a.pi/F - a0 pi2/(2F2) + O(pi3),
    a_j' = a_j + b_j/F - a_j pi2/(2F2) + O(pi3),
    b = a0 pi - a cross pi.

With canonical common nonzero-mode scalar covariance
<pi_i pi_j>=delta_ij Gbar,

    <a0'> = a0[1-3 Gbar/(2F2)],
    <b_j squared>=(1-a_j squared)Gbar,
    <s(U)> = s + (2-4s)Gbar/F2.

Thus the first Gaussian contraction of the potential is

    delta L_mass = (3/2) M2 a0 Gbar,
    delta L_EM = (u C/F2)(2-4s)Gbar.

The EM expression contains an essential U-independent term. Aligned subtraction
of the classical potential does not allow its loop-generated gravitational
spurion term to be dropped. At the aligned background it also reproduces the
two charged pion mass shifts Delta M2=2uC/F2.

For a minimally coupled canonical scalar on a smooth background and d=4-2eps,

    K(t;x,x)=(4pi t)^(-d/2)[1+t R/6+...],
    Gbar_div=(R/6-Mref2)/(16pi2 eps).

Removing finitely many zero modes changes infrared/finite terms, not this local
UV pole. The R-dependent pole of the partial pion determinant is therefore

    delta L_div,R = R/(16pi2 eps)
       [M2 a0/4 + (u C/F2)(1/3-2s/3)].

Equivalently, its Hessian has trace

    Tr sigma_mass=3 M2 a0,
    Tr sigma_EM=(u C/F2)(4-8s),

and (1/2)Tr log(-lap+sigma) has curvature pole
R Tr sigma/(192pi2 eps). Counterterms are the negative of these poles.

For q=diag(2/3,-1/3), Q=e q,

    Tr(Q U Q Udag)=u(5/9-s),

so the EM curvature pole can equally be written

    delta L_div,R,EM = R/(16pi2 eps)
       [(2 C/(3F2)) Tr(Q U Q Udag) - u C/(27F2)].

This is a two-operator statement: a U-dependent EM curvature invariant and an
independent U-independent R Tr(Q squared)-type gravitational spurion invariant.
They cannot be conflated after aligned subtraction.

For the standard subtraction lambda_div=-1/(32pi2 eps), a strong counterterm
l13 R Tr(chi Udag+U chi dagger), chi=M2 I, with
l13_bare=l13^r+beta13 lambda, cancels the displayed mass pole when beta13=1/8.
This is an internal normalization benchmark, conditional on the exact source
operator convention.

For the separately quoted operator k15 F2 R Tr(Q U Q Udag), the displayed
**partial pion potential loop alone**, in this off-shell coordinate convention,
would assign a counterterm coefficient beta15,potential=4Z/3, plus the
independent gravitational spurion counterterm. This cannot immediately be
identified with the source's quoted beta15=1/2+2Z/3. The 1/2 term necessarily
involves sectors absent from this pure-pion potential contraction. The remaining
apparent factor two requires checking the source's full quadratic operator,
kinetic/EOM reduction, field coordinates, curvature/sign conventions and
normalization. This calculation alone does not establish either source error
or equivalence of the two assignments.

The required source-first follow-up is to derive the full off-shell basis
translation, including any operators removed by the LO EOM, and retain all
U-independent gravitational spurion terms. Physical on-shell equality does not
by itself identify off-shell constant-background effective potentials. No finite
matching constants, full global response or alpha are fixed by these pole terms.
