# Independent audit: scalar balance and source-map obligation

**Verdict: the exact balance and local Legendre inversion pass on the
stated positive-R packet neighborhood; the cited theorem is not yet
applicable to the coupled weak system.** This is an explicit balance
representation, not an existence or uniqueness theorem.

Reviewed `pf13/SCALAR_BALANCE_AND_SOURCE.md`, SHA256
`5901b8de78adb48c8d89d83e47041cdc6e1e66d48ec6bb612e40bc19954886c8`.
Independent delegated algebra/application audit, 2026-11-06.

## Native algebra

On the on branch, J=K-A curl(dPi), K=E h n. For Lipschitz A,Pi the
distributional product identity is

    div(A curl(dPi))=A_t Pi_x-A_x Pi_t.

Consequently div K=A_t Pi_x-A_x Pi_t-E(V_phi+W_phi), with the sign given
in the candidate. Define a=phi_t,b=phi_x and m=exp(2 beta)h a/r. Then

    b_t-a_x=0,
    m_t+partial_x[-exp(2 beta)h b/r]=F,
    F=A_t Pi_x-A_x Pi_t-E(V_phi+W_phi).

No expanded BV product has entered these identities. At fixed b,A,alpha,beta,
direct differentiation using r_a=exp(-2 alpha)a/r gives

    m_a=exp(2 beta-2 alpha)(R a^2 r-h b^2)/r^3
       =exp(2 beta)R[cosh(theta)^2-c^2 sinh(theta)^2].

For R>0 and 0<c^2<1 this is positive, uniformly away from zero on the
compact packet neighborhood. Thus a is locally a function of m,b and the
auxiliary/metric coefficients, and the flux for (m,b) is (K^x,-a).
The positive-R qualification is necessary: the bare condition 0<c^2<1
does not exclude h,R both negative. The previously declared packet domain
does have R>0, so this is a clarification, not a change to that domain.

The inversion does not eliminate A or the metric. F contains A_t and
Pi_t, not a prescribed function/operator of the two scalar state entries.
Bounds for these terms along the incoming strong solution cannot be
substituted for a uniform source-difference estimate on a BV state domain.

## Primary-source check

Checked Colombo and Guerra, *Hyperbolic Balance Laws with a Non Local
Source*, [arXiv:0704.2031](https://arxiv.org/pdf/0704.2031), conditions
(F),(G) and Theorem 1.2, PDF pages 2--4. The returned PDF identifies v1,
16 April 2007, while its title-page date is November 18, 2018; the same
metadata distinction reported by the candidate is present. No local
full-text cache or source hash is asserted.

The theorem assumes an autonomous C4 strictly hyperbolic flux with the
stated genuinely nonlinear/linearly degenerate fields, and an L1-Lipschitz
source operator with a total-variation bound on a small-variation domain
on the real line. It constructs a local entropy process. Its uniqueness
statement has additional local approximation requirements; it is not an
unqualified uniqueness theorem for every distributional solution.

This authenticates the cited hypotheses, not their application to AC2q.
The flux/source identification, coupled constraints, and source estimates
are missing. Enlarging the state introduces repeated advective speeds
and does not automatically meet the theorem's strict-hyperbolicity
assumption. Periodicity needs a justified adaptation as well.

## Precise application gap

A proposed application must construct a closed state space and flux,
define its source map on that same domain, prove a uniform L1 difference
bound and the required variation estimate, and show the resulting
evolution preserves the native polarization and all Einstein equations.
It must also identify an admissibility class appropriate to the native
system; one cannot import entropy selection merely because the scalar
principal block has two characteristics.

The actual file accurately says these steps are unproved. No conclusion
about nonexistence or nonuniqueness follows from the failure to verify
this particular theorem's hypotheses. The direct bounded weak system
is nonetheless a defined object, so its existence and uniqueness can
now be investigated without assigning smooth-chain-rule products to BV
derivatives by fiat.
