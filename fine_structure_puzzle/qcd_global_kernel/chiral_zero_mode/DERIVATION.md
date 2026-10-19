# Matched compact chiral mode and its first nonconstant-pion contraction

FSP-008 continuation, 2026-10-19. This packet owns only this directory.

## 0. Ancestry correction and actual new work

The initial dispatch described the compact Haar/Dashen integral as a new
calculation. On opening the nearest antecedent, that description was false:
`qcd_prediction/controlled_model/qcd_zero_modes/REPORT.md`, sections 2, 4,
6--9, and `qcd_prediction/coordinator/ZERO_MODE_QED_RAW.md` already contain
the exact group integral, axes, canonical Gaussian matching, leading charge
response and metric cancellation. They remain frozen. This packet does not
count that integral or its old grid as new evidence.

The new continuation executes the replacement factor proposed in its section
9, differentiates it at finite charge including covariances, and derives the
first interaction of the compact mode with nonconstant PIONS on S4. It also
subtracts the aligned Gaussian nonconstant-mode tadpole already present in a
massive determinant. The new numerical grid tests those new quantities.

## 1. Fixed conventions and inherited exact integral

Use natural units, theta=0, two equal quark masses and leading SU(2) chiral
fields. Write U=a0 I+i a.tau, a0^2+|a|^2=1, Q=I/6+tau3/2,
u=e^2, a=F^2 M^2, b=u C, x=a V, y=b V. F,C are independent, unfitted
matching inputs. Q has dimensionless quark charges (2/3,-1/3).

The Euclidean source potential is

    S0=-x a0+y s,       s=a1^2+a2^2.                         (1)

Pauli algebra gives Tr(Q U Q Udag)=5/9-s. Before removal of its
U-independent local volume term, the Dashen contribution instead produces
Z_full=exp(5y/9) Z. Its W and rho shifts are -5y/9 and -5b/9;
they must be restored if that convention is desired. An arbitrary matched
vacuum contact is not fixed by this subtraction. The mass-aligned vacuum
factor is exp(x); we expose it separately below.

With normalized Haar measure integral dU=1, SU(2)=unit S3 has coordinates

    a1=sqrt(s) cos psi, a2=sqrt(s) sin psi,
    a0=sqrt(1-s) cos phi, a3=sqrt(1-s) sin phi,
    dU=ds dphi dpsi/(4 pi^2), 0<=s<=1.                     (2)

The coordinate endpoint degeneracies have zero Haar measure. Thus

    Z(x,y)=integral_0^1 exp(-ys) I0(x sqrt(1-s)) ds,        (3)
    Z(x,0)=2 I1(x)/x, Z(0,y)=(1-exp(-y))/y, Z(0,0)=1.

These are inherited results, reproduced here to specify the normalization,
not rerun as a new finite-grid achievement. This is the theta=0 SU(2)
ensemble, with topology summed; a fixed-topology U(2) integral is different.

The primary Urech source authenticates the LO mass/Dashen operator and
charge convention; finite-volume ChPT sources authenticate treating the
constant group mode exactly while constraining the other modes to have zero
average. Transfer to S4 in (1) only uses that a constant scalar potential
integrates to V. Those flat finite-volume sources do not compute the full
curved QCD functional. Source receipts are in SOURCES.json.

## 2. Exact finite-charge replacement, rather than adding a second zero mode

For x>0 and d=x+2y>0 the aligned Gaussian saddle in the SAME Haar
normalization is

    ZG(x,y)=sqrt(2/pi) exp(x)/[sqrt(x)(x+2y)],
    Qrep=Z/ZG,       Wrep=-log Qrep.                       (4)

Near U=1 the canonical constant-pion variable is q0=F sqrt(V) phi.
Its three-dimensional measure converts normalized local Haar by
N0=sqrt(pi/2)(mu_R F sqrt(V))^3. Then

    N0 exp(-x) ZG=mu_R^3/[M (M^2+2uC/F^2)],
    N0 exp(-x) Z=Qrep mu_R^3/[M (M^2+2uC/F^2)].            (5)

Consequently a scalar determinant already containing its three massive
constant modes is multiplied by Qrep for this replacement. The mass-aligned
classical vacuum was subtracted in (5); retain exp(x) separately if desired.
Adding Z, N0 Z, or another constant Gaussian on top of that determinant
double counts its constant sector.

Let m=<a0>, q=<s>, va=Var(a0), vs=Var(s), c=Cov(a0,s), all in (3).
With W=-log Z,

    W_x=-m, W_y=q, W_xx=-va, W_yy=-vs, W_xy=c.             (6)

On round S4, V=kappa H^-4, kappa=8pi^2/3, R=12H^2. All a,b,F,C,
the renormalization scale and matching constants are FIXED in the metric
derivative. D=V partial_V=x partial_x+y partial_y, and
rho=partial_V W=-H partial_H W/(4V). Therefore

    V rho_rep=x(1-m)+yq-3/2,                              (7)
    partial_u Wrep=C V [q-2/(x+2y)],
    partial_u rho_rep=C [q+x c-y vs].                     (8)

The x c and -y vs terms differentiate the distribution, not only the
explicit Dashen insertion. The -3/2 in (7) removes the Gaussian Haar
ln V already matched to the canonical measure. For normalized charge
differences ΔWrep=Wrep(x,y)-Wrep(x,0), Δrho follows by subtracting (7).
It equals the charge difference of the group-model stress because the
Gaussian charge factor is V-independent at fixed a,b. A charge-independent
unknown multiplicative normalization cancels from that difference. A general
QCD normalization N(H,u), local charge contacts or higher EFT terms do not.

For reference, the inherited unsubtracted compact stress is
rho_zm=-a m+bq. Its derivative with V is

    partial_V rho_zm=-Var(-a a0+b s)<=0.                  (9)

This identity is a useful independent consistency check; it is not the
absolute QCD stress or a statement about the replacement stress alone.

## 3. Positive-mass saddle: the first replacement correction

Expand (2) near a0=+1 with rc=(a1,a2), r3=a3. The Haar density is
d^3r/[2pi^2 sqrt(1-r^2)], and the exponent is
x-x r^2/2-y rc^2-x r^4/8+... . Gaussian moments give

    Qrep=1+k(a,b)/V+O(V^-2),
    k=1/[2(a+2b)]+1/(8a)-a/(a+2b)^2.                    (10)

For fixed a>0,b>=0 the OTHER saddle is exponentially suppressed. Thus

    Wrep=-k/V+O(V^-2), rho_rep=k/V^2+O(V^-3),
    Δrho_rep=b(3a+2b)/[a(a+2b)^2 V^2]+O(V^-3),
    partial_u rho_rep=C(3a-2b)/[(a+2b)^3 V^2]+O(V^-3).    (11)

At b=0, k=-3/(8a), agreeing with the next Bessel-saddle coefficient.
The sign of the finite-charge differential response need not be positive:
its leading saddle value changes sign at b=3a/2. This is obscured if the
covariance terms in (8) are omitted. The bounded run checks the expansion
and a negative response at new, declared mathematical points.

The V^-2 scaling is H^8 for this isolated replacement at fixed a,b; there
is no H-linear term in this expression. This is only a saddle statement
about the group function. A fixed-positive-mass H->0 limit leaves the
epsilon regime, so it is not an independent physical QCD extrapolation.

## 4. First interaction with nonconstant pions

Use U(z)=U0 exp(i tau.pi(z)/F), integral sqrt(g) pi(z)=0. At leading
epsilon order the nonconstant pion fields are massless, canonically
normalized, and have coincident contraction

    <pi_i(z) pi_j(z)>=delta_ij Gbar(H), g=Gbar/F^2.        (12)

Here Gbar excludes the constant scalar harmonic and requires a UV scheme.
Right multiplication of quaternions gives the exact quadratic averages

    <a0(z)>_pi=(1-3g/2)a0,
    <s(z)>_pi=(1-4g)s+2g.                                (13)

The code verifies these coefficients by independent polynomial contraction.
The +2g is essential. Relative to a MASSLESS nonconstant Gaussian baseline,
the first source-dependent correction is

    Z=normalization * exp(-2yg)
        Z(x(1-3g/2),y(1-4g))+O(epsilon^4),
    δW_pion,massless=g T,
    T=2y+(3x/2)m-4yq.                                    (14)

This is a first-order expansion in g, not permission to resum the shifted
arguments beyond the retained order. The interactions of the kinetic
action and the collective-coordinate Jacobian are independent of U0 at
this order. Their normalization cancels from the source ratios considered
here, but can contribute to the absolute metric response.

An already MASSIVE nonconstant Gaussian determinant contains its own
first mass insertion, in the SAME regulator and scheme:

    δW_nz,Gaussian=(V Gbar/2)(M^2+2[M^2+2uC/F^2])
                  =g(3x/2+2y).                          (15)

Therefore the genuine ADDITION to massive determinant + exact/Gaussian
constant replacement is

    δW_extra=g B, B=T-(3x/2+2y)
                    =(3x/2)(m-1)-4yq.                   (16)

Using gT with the massive determinant would double count (15). The
normalized charge difference of the EXTRA correction is

    ΔδW_extra=g[(3x/2)(m(x,y)-m(x,0))-4yq(x,y)].           (17)

At x=0,y small, T=y^2/3+O(y^4), while B=-2y+y^2/3+... .
The latter cancels the +2yg already present in (15). This is an explicit
zero-charge check of the seagull/normalization-sensitive constant in (13).

The frozen sphere determinant uses mass-dependent decoupling subtractions.
Equations (12)--(17) are a common-regulator assembly identity; one must
translate the tadpole's local finite terms into that same subtraction
scheme before combining actual numbers. We do not silently identify the
convenient zeta tadpole scheme below with that decoupling scheme.

## 5. Metric and charge derivatives of the extra interaction

Put gdot=Dg, with the renormalization scale held fixed, and define

    E=(3/2)x^2 va-(11/2)xy c+4y^2 vs,
    DB=B+E,
    B_y=-4q-(3/2)x c+4y vs.                               (18)

For third central cumulants kaa_s=<δa0^2 δs>, ka_ss=<δa0 δs^2>,
ksss=<δs^3>,

    D B_y=-(11/2)x c+8y vs-(3/2)x^2 kaa_s
                      +(11/2)xy ka_ss-4y^2 ksss.         (19)

The actual fixed-parameter derivatives of the first correction are

    δrho_extra=[gdot B+g DB]/V,
    partial_u δrho_extra=C[(gdot+g)B_y+g D B_y].          (20)

The run checks (18)--(20) against independent finite differences in the
radius/volume and charge, not just differentiation of the same displayed
formula. Finite g,gdot values used in these controls are dimensionless
test inputs, not fitted QCD constants or a numerical physical matching.

## 6. S4 tadpole and curvature matching at the same order

For the minimal massless scalar, l=1,2,...,
lambda_l=H^2 l(l+3), d_l=(l+1)(l+2)(2l+3)/6. Define

    zeta_D(p)=sum_(l>=1) d_l/[l(l+3)]^p,
    Gbar_zeta=FP_(eps=0) (H^2/kappa)(mu^2/H^2)^eps
                                      zeta_D(1+eps).    (21)

The nonconstant heat trace has coefficients
K'(t)=1/(6t^2)+1/(3t)+O(1). In particular

    Res_(p=1) zeta_D(p)=1/3,
    Gbar pole=H^2/(8pi^2 eps)=R/(96pi^2 eps).             (22)

Removing the l=0 harmonic does not change either UV coefficient.
This curvature divergence vanishes on a flat torus; importing a finite
torus shape constant to S4 would miss it.

One explicitly defined finite part, derived rather than used as a physical
matching condition, is

    FP zeta_D(1)=2 EulerGamma/3-8/9,
    Gbar_zeta=H^2/(8pi^2)
                 [log(mu^2/H^2)+2 EulerGamma-8/3],
    Dg=-g/2+H^2/(16pi^2 F^2).                            (23)

For the derivation, set n=l+3/2, A=5/2, c0=9/4. Expand
(n^2-c0)^-p to express zeta_D(p) as

    (1/3) sum_(k>=0) (p)_k c0^k/k!
        [zeta_H(2p+2k-3,A)-zeta_H(2p+2k-1,A)/4].         (24)

Only k=0,1 give the pole at p=1. The regular tail combines to
(3/2) sum_(n=A,A+1,...) 1/[n(n^2-c0)], which is
[2psi(A)-psi(4)-psi(1)]/3. Together with
zeta_H(-1,A)/3+3/8-(2/3)psi(A), this gives (23).
The run compares a bounded Hurwitz-series Laurent subtraction with this
closed form, including a tail bound; no fitted cutoff constant is used.

A finite change of UV prescription changes Gbar by a local multiple of R.
It changes (14) by that multiple times T/F^2, which has precisely the
mass-source, Dashen-source and U-independent source structures requiring
curved EFT matching. In epsilon counting, L~epsilon^-1,
M^2,u~epsilon^4, R~epsilon^2, so R M^2 V and R u V are BOTH
O(epsilon^2), the same order as gT. Independent strong curvature
l13 R Tr(chi Udag+U chi_dag), electromagnetic curvature k15 and pure-source
contacts therefore cannot be omitted. The primary Kubis--Meissner v2
source verifies these independent operators; their finite LECs remain
unfitted. Equation (23) is a conditional scheme coefficient, not a new
universal finite-volume QCD number.

## 7. Photons and validity are load-bearing

This is the first NONCONSTANT-PION contraction, not a complete NLO QCD+QED
epsilon partition function. Even a constant charged orientation gives
from the gauged kinetic term

    S_seagull=(uF^2/2) s integral sqrt(g) A_mu A^mu.        (25)

Since u~epsilon^4 and A~epsilon, its expectation is O(epsilon^2).
The related photon determinant and two pion-photon mixing insertions
can enter at that order as well. Individual seagulls are gauge dependent;
the complete photon, mixing, ghost/gauge-volume and local-counterterm
combination must be assembled. None is included by the pion tadpole (14).

Controlled use requires F/H>>1, H<<Lambda_chi, M/H<<1 and
sqrt(M^2+2uC/F^2)/H<<1, with x,y O(1) in the strict epsilon scaling.
Pure curvature vacuum terms and heavy-QCD normalization are separate.
Holding x,y fixed as H decreases changes M^2 and u as H^4; it is not the
fixed physical charge/mass metric path. Mathematical large-x tests of Qrep
do not certify a physical epsilon expansion at every test point.

## 8. Truly massless/tensionless corner and derivative order

At a=0 the inherited compact expression is finite:

    Z(0,y)=(1-exp(-y))/y,
    V rho_zm=1-y/(exp(y)-1),
    partial_u rho_zm/C=[(y-1)exp(y)+1]/[exp(y)-1]^2.       (26)

At finite V, a=b=0, Z=1 and rho_zm=0, but
partial_u rho_zm=C/2 and partial_u^2 rho_zm=-C^2 V/6.
Taking b->0 before V->infinity leaves C/2; taking V->infinity at
any fixed b>0 first gives zero. These are different response limits of
the group model. Finite-volume m=<a0> is zero at a=0; taking a->0
after the formal positive-a infinite-volume saddle instead leaves m=1.

Qrep itself is defined using a positive-mass Gaussian denominator. It
vanishes as x->0 at y=0 and its log diverges. That divergence cancels the
Gaussian constant-mode divergence in (5). At exactly massless parameters
one must use the compact factor with a nonconstant-mode determinant,
not evaluate a singular full Gaussian determinant and a zero replacement
factor separately. N0 contributes a V-dependent collective-coordinate
factor; nonconstant determinants, gauge factors and unknown matching are
still needed for the absolute stress. A normalized charge ratio at fixed
mass cancels a charge-independent N0 and N(H), but cannot constrain an
unknown N(H,u) or independent curvature/source LEC.

No result in this packet computes the full QCD+QED sphere response,
its H-linear coefficient, a proton denominator, or a selected alpha.
At fixed declared LECs partial_alpha=4pi partial_u is a conditional source
derivative, not a solution for alpha and not a fully matched QED running
and Thomson-limit calculation.
