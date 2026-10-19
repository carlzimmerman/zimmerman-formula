# Resumming a full singular photon polarization before the curvature limit

Coordinator hand derivation, FSP-005. Written after reading the physical
QED route's finite-soft-mode counterexample, but before receiving a fresh
Mellin derivation or executing a new experiment. This is an explicitly
nonlocal Gaussian test model, not a proposed local QCD current kernel.
No parameter is chosen to fit alpha or a cosmic observable.

## Defined model and common spectral subtraction

On S4_H let Delta_T be the coexact Maxwell Hodge operator. Its dimensionless
spectrum is x_l=(l+1)(l+2), degeneracy d_l=l(l+3)(2l+3)/2, l>=1.
Consider the positive quadratic photon operator

    P_eff=Delta_T[1+M^3 Delta_T^(-3/2)], M>0,
    t=(M/H)^3.

This is the full-spectrum version of a polarization that could generate an
order-charge H insertion. Its current Hessian is proportional to
Delta_T^(-1/2); it is not compatible with the ordinary gapped flat QCD
current representation. It is used to test the order-of-limits mechanism,
not to assert that QCD has this kernel. The canonical photon domain and
global gauge measure are the same on both sides of the determinant ratio.

Write zeta_T(s)=sum d_l x_l^(-s), analytically continued. The following
prescription defines the renormalized relative Gaussian action:

    delta W(t)=1/2 sum_l d_l[log(1+t/x_l^(3/2))-t/x_l^(3/2)]
                       +(t/2)zeta_T(3/2).                       (R1)

The bracket sum converges absolutely for fixed t: its tail is O(l^-3).
The last term is the common spectral finite part of the single ultraviolet
divergent linear trace. It is not set to zero by hand. This fixes a spectral
subtraction convention; finite local vacuum counterterms may still be
specified, and do not manufacture a linear-H term on the closed sphere.
No identity of separately zeta-factorized nonlocal determinants is assumed.

At small t, (R1) gives

    delta W=(t/2)zeta_T(3/2)+O(t^2),
    delta f=M^3 zeta_T(3/2) H/(2 Omega4)+O(M^6/H^2),
    Omega4=8pi^2/3.

The small-t condition is M<<H. It cannot be maintained while H tends to
zero at fixed nonzero M. If M^3=e^2 gamma Lambda^3, this is exactly a
zero-charge-before-curvature expansion, not the fixed-charge limit.

## Meromorphic data from the actual closed-sphere spectrum

Set n=l+3/2. Then x=n^2-1/4 and d=n^3-(9/4)n. Euler--Maclaurin gives

    K_T(u)=sum d_l exp(-u x_l)
           =1/(2u^2)-1/u+19/30+O(u),                 u->0+.

The leading integrals are integral_0^infinity n^3 exp(-u n^2)=1/(2u^2)
and integral n exp(-u n^2)=1/(2u). Multiplication by exp(u/4) gives the
coefficient -1/u. Finite lower-end changes and Euler--Maclaurin terms have
only integer powers of u. Expanding to arbitrarily many terms with its
remainder controls continuation to every finite strip. The large-u heat
trace decays exponentially because x_1=6.

The Mellin transform therefore implies that zeta_T(s) has only positive
poles s=2 and s=1, with residues 1/2 and -1. Apparent poles at nonpositive
integers are removed by the zeros of 1/Gamma(s). In particular it is
regular at s=3/2 and has zeta_T(0)=19/30. There is no pole at 3/2 to
support a term t in a fixed-M large-t expansion after consistent resummation.
The special value is imported from the separately derived QED spectral
calculation; absence of a linear-H term does not depend on its numerical
value.

## Mellin reconstruction and the cancellation of the tempting term

For 1<c<2, the absolutely subtracted scalar identity is

    log(1+y)-y=(1/(2pi i)) integral_(c-i infinity)^(c+i infinity)
                           [pi/(s sin(pi s))]y^s ds.

Choose 4/3<c<2 so that the spectral sum also converges absolutely. Interchange
the sum and integral at that line, obtaining

    delta W(t)=t zeta_T(3/2)/2
       +(1/2)(1/(2pi i)) integral
          [pi/(s sin(pi s))]zeta_T(3s/2)t^s ds.           (R2)

Shift the contour to Re s=-sigma, 0<sigma<1. The crossed poles are
s=4/3,1,2/3,0. Their contributions, respectively, are

    -pi t^(4/3)/(4sqrt(3)),
    -t zeta_T(3/2)/2,
    -pi t^(2/3)/sqrt(3),
    (zeta_T(0)/2)log t+(3/4)zeta_T'(0).

The s=1 residue cancels the explicit linear trace in (R2) exactly. This
is the mechanism that would be missed by retaining only the first order
in e^2. The completed relative action is

    delta W= -pi t^(4/3)/(4sqrt(3))-pi t^(2/3)/sqrt(3)
               +(19/60)log t+C+O(t^(-sigma)),
    C=(3/4)zeta_T'(0).                                  (R3)

The shift can be controlled directly, rather than assuming a formal
asymptotic series. Subtract finitely many integer heat terms in the Mellin
representation of zeta_T(z). In each fixed vertical strip the remaining
integrals are bounded and 1/Gamma(z) grows at most a polynomial times
exp(pi |Im z|/2). Thus zeta_T(3s/2) has a sufficient bound of exponential
type 3pi/4. The factor 1/sin(pi s) decays with type pi, leaving an
integrable exp(-pi |Im s|/4) envelope. The shifted integral and its fixed
number of t d/dt derivatives are O(t^(-sigma)). This supplies the
differentiated remainder needed for the stress, not just a formal absence
of a coefficient in the integrand.

## Fixed-M stress and precise physical limit

With f=delta W/(Omega4 H^-4), (R3) yields

    delta f= -pi M^4/(4sqrt(3)Omega4)
             -pi M^2 H^2/(sqrt(3)Omega4)
             +(19/(20Omega4))H^4 log(M/H)
             +(C/Omega4)H^4+O(H^(4+3sigma)).

The invariant stress is rho=(1-H partial_H/4)f, with M fixed:

    delta rho= -pi M^4/(4sqrt(3)Omega4)
                -pi M^2 H^2/(2sqrt(3)Omega4)
                +(19/(80Omega4))H^4+O(H^(4+3sigma)).

After the same flat subtraction, its coefficient A_rho of H is zero.
This is a statement about the fully resummed defined Gaussian model at
fixed M, not merely an order-e^2 insertion. The exact soft-mode example
in the QED route has the same nonuniformity with a finite mode sum; here
the infinitely many modes also generate the extensive and H^2 threshold
terms, while still not producing H.

The model supplies no alpha selector. gamma, Lambda and the relationship
to any microscopic response remain independent hypothetical data. Its
nonlocal flat current kernel violates the gapped QCD hypothesis. The
calculation does show that even deliberately supplying the proposed
singular infrared polarization is insufficient: a first-order H response
need not survive at fixed charge. A genuine QCD mechanism would require
a controlled full metric functional and resummation, not the insertion
coefficient alone. This result is awaiting fresh independent audit.
