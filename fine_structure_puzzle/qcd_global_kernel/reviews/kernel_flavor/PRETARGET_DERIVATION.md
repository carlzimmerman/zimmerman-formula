# Independent pretarget derivation

Saved 2026-10-19 by isolated reviewer `/root/kernel_flavor_review`, before
opening author derivations, reports, input files, scripts, result files or
manifests. Only the task statement, available-file names and sea source metadata
were seen. These are independently derived formulas, subject to later convention
and source checks. No complete QCD kernel or fitted alpha is inferred.

## 1. Normalized sea/valence response

Let expectations be normalized at eta=0, B the contracted valence observable,
U_a=L_a and H_ab=L_ab. Write cov(X,Y)=<XY>-<X><Y> (bilinear,
not Hermitian). Direct quotient differentiation gives

    C_ab = <B_ab> + cov(B_a,U_b) + cov(B_b,U_a)
           + cov(B,H_ab) + cum(B,U_a,U_b),

where cum(B,U,V)=<(B-<B>)(U-<U>)(V-<V>)>. This identity does not
require <U>=0. The terms are respectively valence-valence (including valence
seagull), mixed sea-valence, same-sea-loop (including sea seagull), and
separate-sea-loop. The last two are vacuum-subtracted; adding bare <BH> or
<BUU> would double count vacuum normalization.

For D_f=D0+m_f+q_f eta_a V_a+q_f^2 eta_a eta_b W_ab/2 with symmetric
W_ab and S_f=(D0+m_f)^-1,

    U_a = sum_f q_f Tr(S_f V_a),
    H_ab = sum_f q_f^2 Tr(S_f W_ab-S_f V_a S_f V_b).

The trace of the second term is symmetric under a,b by cyclicity. The determinant
second derivative is H_ab+U_a U_b, while log(det) has only H_ab. This
distinction fixes the same-loop minus sign and the two-loop plus sign.

For additive scalar masses and common vertices,

    S_l-S_s = delta S_l S_s = delta S_s S_l, delta=m_s-m_l,
    U_a = delta R_a,
    R_a = Tr(S_l S_s V_a)/3.

The charges 2/3,-1/3,-1/3 sum to zero but their squares sum to 2/3. Hence
U vanishes at SU(3) while H does not. If h_ab(S)=Tr(S W_ab-S V_a S V_b),

    H_ab=(5 h_ab(S_l)+h_ab(S_s))/9
        =2 h_ab(S_l)/3+[h_ab(S_s)-h_ab(S_l)]/9.

One exact split is

    h(S_s)-h(S_l) = -delta Tr(S_l S_s W)
      +delta Tr(S_l S_s V_a S_s V_b)
      +delta Tr(S_l V_a S_l S_s V_b).

Therefore mixed response is O(delta), separate-loop response is O(delta^2),
and the same-loop response is O(1), assuming the relevant valence observables
and moments remain uniformly regular as delta tends to zero. These are local
mass-splitting orders, not numerical physical-mass suppression guarantees.

Measurable absolute bounds follow from Cauchy-Schwarz with
sigma_X^2=<|X-<X>|^2>. For every a,b,

    |cov(B_a,U_b)| <= |delta| sigma_Ba sigma_Rb,
    |cov(B,H_ab)| <= sigma_B sigma_Hab,
    |cum(B,U_a,U_b)| <= delta^2 sigma_B
       sqrt(Var[(R_a-<R_a>)(R_b-<R_b>)]).

Triangle inequalities, followed by sums or integrals of absolute photon-kernel
weights, give conservative bounds for contracted responses. These are bounds
in terms of exact ensemble moments. Sample estimates need a confidence procedure,
autocorrelation treatment, existence of fourth moments and declared tail control
before they constitute certified population bounds.

Stochastic trace estimators must be unbiased conditional on the gauge field.
Multiplying two estimates made with the same noise adds a conditional noise
covariance. Independent noise families, off-diagonal U-statistics, or an exact
noise covariance subtraction avoids this bias. A stochastic B correlated with
trace noise likewise needs conditional treatment. Gauge covariance itself is
the physical signal. The usual N-1 covariance denominator corrects finite-sample
normalization for independent samples; autocorrelation must still be handled.

For the normalized vacuum functional, define the convention explicitly:
W=-log Z. Photon contraction with K_ab gives at first order in u=e^2

    W_u = -1/2 K_ab[<H_ab>+cov(U_a,U_b)] + W_u,ct,

up to the source's Euclidean i-current convention absorbed in V and K. For
W=+log Z the sign reverses. A normalized hadron correlator does not determine
this vacuum response. Metric derivatives additionally differentiate the measure,
vertices, seagulls, inverse operators, photon kernel, B, and local counterterms;
connected stress insertions alone omit contact terms. Mass tuning and UV local
counterterms are separate required inputs.

## 2. Full spin-averaged elastic/Born tensor

Use relativistic one-particle normalization, spin averaging, and dimensionless
amplitudes defined so the complete Born tensor is

    T1^B(nu,Q2)=Q4 G_M(Q2)^2/(Q4-4m2 nu2)-F1(Q2)^2,
    T2^B(nu,Q2)=4m2 Q2 [F1(Q2)^2+tau F2(Q2)^2]
                         /(Q4-4m2 nu2),
    tau=Q2/(4m2), G_M=F1+F2.

Overall factors in alternative definitions of the current-current tensor must
be translated together with the Cottingham prefactor. The nonpole term -F1^2
is essential. Equivalently T1^B(0)=G_M^2-F1^2 and the remaining once-subtracted
pole contribution is G_M^2 nu2/(nu_B2-nu2), nu_B=Q2/(2m).

For Euclidean Q0=Q x, x in [-1,1], the photon trace is

    -3 T1^B(iQx,Q2)+(1-x2)T2^B(iQx,Q2).

The exact radial e2-normalized kernel (delta m=e2 integral dQ K_B) is

    K_B(Q)=Q/(8m pi3) integral_-1^1 dx sqrt(1-x2)
       [-3 T1^B(iQx,Q2)+(1-x2)T2^B(iQx,Q2)].

Set t=Q/(2m), r=sqrt(1+t2), A=F1^2+t2 F2^2 and
C=A(1+t2)-3t2 G_M^2. The two elementary integrals

    I0=integral sqrt(1-x2)/(t2+x2) dx=pi(r/t-1),
    I2=pi/2-t2 I0

give the complete angular integral

    K_B(Q)={C(r-t)+t(3F1^2-A)/2}/(4 pi2).

This is the full elastic Born sector, not a full inelastic QCD mass. A pole-only
kernel, an elastic structure-function contribution without its Born subtraction,
or a Thomson contact without the pole produces a different expression.

For physical charge Z=F1(0) and arbitrary finite Pauli moment kappa=F2(0),
with form factors analytic in Q2 near zero,

    K_B(Q)=Z2/(4pi2)+O(Q2),

and the Q-linear coefficient cancels exactly: C(r-t) supplies -Z2 t and
t(3F1^2-A)/2 supplies +Z2 t. For Z=1, ignoring F1 slopes only in the displayed
coefficient, the t2 coefficient is -3/2-6kappa-2kappa2. Form-factor slope
contributions are O(Q2) and do not affect the cancellation. This expansion is
local to Q much smaller than both m and the first hadronic threshold scale;
the chiral limit and Q->0 limit need not commute. The Q2 slope is not determined
by charge and magnetic moment alone.

## 3. Point Dirac normalization, cutoff and double-PV check

For F1=1,F2=0 the full kernel reduces to

    K_D(Q)=[(1-2t2)sqrt(1+t2)+2t3]/(4pi2).

Independent direct Feynman-gauge on-shell self-energy spin trace gives

    delta m/e2 = integral d4Q/(2pi)^4
       2m(Q2+2Q02)/[Q2(Q4+4m2 Q02)],

which reproduces K_D after the full S3 angular integration. The finite Euclidean
cutoff band [Qlo,Qhi] is m/(2pi2)[J(t_hi)-J(t_lo)], where

    J(t)=t sqrt(1+t2)(1-2t2)/4+3 asinh(t)/4+t4/2.

In particular K_D=1/(4pi2)[1-3t2/2+2t3+O(t4)] at small Q and
K_D=3m/(8pi2 Q)+O(m3/Q3) at large Q. The UV logarithm is the expected
3e2 m/(16pi2) log Lambda2, a normalization cross-check.

For P_Lambda(Q2)=1/[(1+Q2/Lambda2)(1+2Q2/Lambda2)],

    integral_0^infty dQ P = pi Lambda(sqrt(2)-1)/2,
    integral_0^infty dQ Q2 P = pi Lambda3(1-1/sqrt(2))/2.

For Lambda much smaller than m and hadronic scales, the leading physical proton
Born contribution is e2 Lambda(sqrt(2)-1)/(8pi). The Q2 correction uses physical
form-factor slopes; extending the soft expansion to all Q is invalid. For the
point theory only, the first correction is

    delta m_PV/e2 = Lambda(sqrt(2)-1)/(8pi)
        -3 Lambda3(1-1/sqrt(2))/(64pi m2)
        +O(Lambda4 log(m/Lambda)/m3).

The point large-cutoff finite constant follows from
J(T)=3 log(2T)/4+3/16+o(1) and
integral_0^infty dy/y [P(y2)-theta(1-y)]=-log 2:

    delta m_PV/e2 = m/(16pi2)[3 log(Lambda2/m2)+3/2-6 log 2]+o(1).

For the elementary Dirac theory, the conventional one-loop pole-minus-MSbar
mass is m/(16pi2)[3 log(mu2/m2)+4] in e2 normalization. If this conventional
formula is authenticated, the finite matching to add to the PV result is

    m/(16pi2)[3 log(mu2/Lambda2)+5/2+6 log 2].

The latter is a separate elementary-theory scheme match, not a physical proton
mass renormalization or a determination of QCD counterterms. These constants
will be checked against primary conventions and independent bounded numerics.
