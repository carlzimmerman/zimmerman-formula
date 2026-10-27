# All photon scales, with the heavy-photon matching endpoint

FSP-010, parent FSP-009. Scope: `hard_bridge/`. This derivation is frozen
before the new numerical execution. The target is full `f(0)=M_u/M`, with
`u=e^2`; neither an infrared coefficient nor a finite momentum band suffices.
We vary only the canonical photon propagator, `D_s(Q)=1/(Q^2+s)`, at fixed
renormalized QCD parameters. In particular, no new independent microscopic
photon-mass-dependent matter interaction is introduced.

## 1. A reconstruction theorem, rather than another infrared limit

Use the inherited full-current normalization

    f(s)=renormalized integral_0^infinity dt g(t)t/(t+s),
    g(t)=1/(32 pi^3 M^2) integral_-1^1 dx sqrt(1-x^2)
         [-3 T1(i sqrt(t)x,t)+(1-x^2)T2(i sqrt(t)x,t)].       (1)

All contraction classes, current contacts and local quark/gluon insertions
are part of the renormalized expression. Define, for positive integer n,

    h_n(s)=(-1)^n s^(n-1) f^(n)(s)/(n-1)!
          =n s^(n-1) integral_0^infinity dt g(t)t/(t+s)^(n+1).
                                                               (2)

In particular `h_1=-f'` and `h_3=2s G3`, for the FSP-009
`G3=-s f'''/4`. The exact normalization of the ALL-SCALE kernel is

    integral_0^L ds n s^(n-1)t/(t+s)^(n+1)=[L/(t+L)]^n,
    integral_0^infinity ds n s^(n-1)t/(t+s)^(n+1)=1.        (3)

Thus an integrable g, an s-independent local term c, and a dominated limit
give `f(0)=c+integral_0^infinity h_n(s)ds`. The derivative integral cannot
determine c. Absolute convergence/Fubini suffices; positivity of physical
g is not assumed. For a charged state, `f(s)-f(0)=O(s^1/2)` ensures the
lower endpoint of the following integration by parts vanishes. More
generally require `s^k f^(k)(s)->0` at zero for `1<=k<n` and continuity
of f at zero. Then for every finite L,

    f(0)=integral_0^L h_n(s)ds
         +sum_(k=0)^(n-1) (-L)^k f^(k)(L)/k!.             (4)

This is a direct consequence of n integrations by parts. It remains valid
for a renormalized f with logarithmic UV behavior, provided the positive-s
derivatives and integrals exist. Equations (2)-(4), not the small-s limit
of G3, are the changed mechanism relative to FSP-009.

For the explicit single-log class assume, with S0>0,

    f(s)=-a log(s/S0)+B+r(s),
    s^k r^(k)(s)->0 for 0<=k<n,                           (5)

and the subtracted integral below converges, for example
`h_n(s)-a/s=O(log(s)/s^(1+delta))` for some delta>0.
Writing `H_j=sum_(k=1)^j 1/k`, with H0=0, (4) gives

    f(0)=B+a H_(n-1)
         +integral_0^infinity ds [h_n(s)-a/(s+S0)].        (6)

The harmonic term is compulsory. For n=3 it is `3a/2`.
The subtraction a fixes the logarithm; B fixes the constant. Shifting
`f->f+c` shifts B by c and leaves every h_n unchanged. A canonical fixed
scheme supplies B by matching: it is not a newly admitted free coupling.
Derivative information, Ward identities or a decoupling slogan alone do
not perform that matching.

## 2. Fully specified all-momentum Dirac check

This control is one elementary unit-charge Dirac field, not a proton model.
Set M=mu=1 in numerical work. Dimensional MSbar subtraction, including the
evanescent numerator term inherited from FSP-008, gives at every s>=0

    f_D(s;mu)=1/(8 pi^2) integral_0^1 dx
          [-(1+x) log((x^2 M^2+(1-x)s)/mu^2)-x].          (7)

In the underlying d-dimensional numerator the massive photon changes only
Delta; the finite `-x` term remains. This extension follows directly from
combining one photon and one fermion denominator; no fitted mass function
is used. At zero, (7) reproduces the inherited
`[4+3 log(mu^2/M^2)]/(16 pi^2)`.

At large s, the integrable logarithm gives

    a_D=3/(16 pi^2),
    B_D=[5/2+3 log(mu^2/S0)]/(16 pi^2),
    f_D(s)=-a_D log(s/S0)+B_D+O((M^2/s)log(s/M^2)).       (8)

Indeed `integral(1+x)log(1-x)dx=-7/4` and `integral x dx=1/2`.
This is the massive-photon threshold, not the earlier PV-to-MSbar
conversion constant. A photon made heavy in a mass-independent scheme
therefore does not yield f(infinity)=0 at fixed MSbar mass. The finite
threshold and logarithm renormalize the low-energy mass parameter. One may
retune that parameter so a low-energy theory decouples; such retuning
changes the parameter path being differentiated.

The two independent convergent derivative representations are

    h_n^FP(s)=s^(n-1)/(8 pi^2) integral_0^1 dx
       (1+x)(1-x)^n/[x^2+(1-x)s]^n,
    h_n^rad(s)=n s^(n-1)/(2 pi^2) integral_0^infinity dz
       B(z) 4z^2/(4z^2+s)^(n+1),
    B(z)=[sqrt(1+z^2)+2z]/[sqrt(1+z^2)+z]^2.              (9)

For finite L, analytically performing the photon-mass integral gives

    I_n^rad(L)=1/(2 pi^2) integral_0^infinity dz
                     B(z)[L/(4z^2+L)]^n,
    J_n^FP(L)=1/(8 pi^2) integral_0^1 dx (1+x)
       [log(1+L/c)-sum_(k=1)^(n-1) y^k/k-log(1+L)],
    c=x^2/(1-x), y=L/(L+c),
    J_n(L)=I_n(L)-a_D log(1+L).                           (10)

At infinity, `J_n=a_D(1/2-H_(n-1))`. In particular `J_1=a_D/2`
and `J_3=-a_D`. Both give `f_D(0)=4/(16 pi^2)` through (6),
with no alpha input or mass/cosmological calibration.

An orthogonal all-momentum proof sets
`g_D(t)=B(sqrt(t)/2)/(8 pi^2 sqrt(t))` and
`g_ref(t)=a_D/(t+1)`. With z=sinh(v), r=exp(-2v),

    integral_0^infinity [g_D(t)-g_ref(t)]dt
      =a_D integral_0^1 dr [-1/3+r+r^2-r^3/3]/(1-r+r^2)
      =a_D/2.                                            (11)

Polynomial division leaves `2/3-r/3+(2r-1)/(r^2-r+1)`;
the logarithmic endpoint vanishes. The reference renormalized function is
`f_ref(s)=-a_D s log(s)/(s-1)`, with f_ref(0)=0 and B_ref=0.
It makes explicit why a finite density-difference integral still requires
the physical local boundary B_D. Without B_D the n=1 reconstruction misses
`5/(32 pi^2)`; retaining B_D but omitting the n=3 harmonic term misses
`9/(32 pi^2)`.

## 3. Transfer to QCD and the actual remaining endpoint

QCD running generally invalidates the simple constant-a assumption (5).
Use the finite identity (4) with a matched RG-improved endpoint, or subtract
the complete known running reference, rather than transplant (8) to QCD.
At large photon mass, integrating out the photon produces local QCD
operators with Wilson coefficients, plus suppressed higher-dimensional
operators. For the connected proton energy these include `m_q qbar q`
and `G^2`; the unit operator drops out. Equations (56)-(57),(64) of the
corrected Gasser et al. source verify precisely that operator obligation.

At leading order in strong-coupling matching, the quark mass part alone is

    f_p(s)|mass =sum_q (sigma_q/M) Q_q^2
                [-3 log(s/mu^2)+5/2]/(16 pi^2)+...,
    sigma_q=m_q partial M/partial m_q.                    (12)

Equation (12) translates the independently derived hard Dirac Wilson
coefficient into a scalar matrix element. It is not the full QCD endpoint:
mixed strong corrections, gluonic matching, RG evolution, all relevant
flavors and higher-operator remainder bounds are needed. No sigma terms
or measured mass are imported numerically in this package. The fixed
canonical theory fixes the coefficients and matrix elements; the present
calculation does not evaluate them. A perturbative renormalon subtraction
can redistribute the Wilson coefficient and matrix element consistently;
it cannot replace either missing nonperturbative input by a Ward identity.

Even granting the trace identity in a common renormalization convention,

    M=sum_q (1+gamma_m) sigma_q
         +(beta_s/(2g_s)) <p|G^2|p>/(2M),                (13)

it fixes one linear combination. With equal light anomalous dimensions,
the formal variation `(delta sigma_u,delta sigma_d)=(d,-d)` preserves
(13) but changes the leading charge-weighted logarithm coefficient by
`delta a=d/(16 pi^2 M)`, because Q_u^2-Q_d^2=1/3.
This is rank underdetermination of the stated Ward data, not construction
of two microscopic QCD theories with arbitrary sigma terms. State-specific
scalar information supplies the missing equation. Flavor or scalar Ward
identities alone do not do so.

In the Euclidean path integral, let C_p(T) be a proton two-point function
and `S_u=(1/2) integral JJ D` plus required parameter/contact insertions.
With the standard large-T mass limit,

    M_u=lim_(T->infinity) [<S_u>_(C_p)-<S_u>]/T,
    W_u=<S_u>.                                            (14)

Differentiating in a scalar source gives the corresponding connected
insertions in EACH ensemble. It does not identify the proton-conditioned
distribution with the unconditioned vacuum distribution. A scalar Ward
identity cannot erase that exact difference. Dispersion reconstruction
also needs every required subtraction/fixed-pole/contact datum: spectral
discontinuities alone do not determine a local term with no discontinuity.
The inspected source explicitly assumes Reggeon dominance for its extra
subtraction-function relation; that assumption is not proved by us.

## 4. Scope and continuation

The theorem (4)/(6), the kernel normalization (3), and the independent Dirac
check are the strongest current result. All-scale derivatives CAN recover
the hard constant given the physically matched UV endpoint. Soft limits
alone cannot. For actual QCD the required new data are the full matched
canonical proton h_n(s) over all masses (or complete g), and scalar/gluonic
operator matrix elements and Wilson matching at a high endpoint with an
error-controlled tail. Neither is supplied by a soft polarizability or
vacuum scalar expectation. The curved vacuum A, R and alpha remain open.
This leaves a concrete, conditional measurement/reconstruction route open;
it is no general no-go for another dynamical QCD relation.
