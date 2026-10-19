# Massive-photon filters of the complete non-Born response

FSP-009 continuation; write scope `photon_mass/` only. Existing soft/finite
proton packages are frozen. This derivation and its exact input/contract/code
are fixed before the bounded run. These filters extract infrared information;
they do not recover the hard mass constant f(0), A_rho, R, or alpha.

## 1. Canonical regulator deformation and hypotheses

Let `u=e^2`, `s=lambda_gamma^2>0`, `t=Q_E^2`. Change only the photon propagator
to `delta_mu,nu/(Q_E^2+s)` in the order-u current convolution of pure QCD.
The renormalized QCD current tensor, its complete Born subtraction, and its
strong parameters are held fixed as s varies. Use infinite volume, positive
pion mass, and a mass-independent UV scheme. Include all Ward-identity
contacts and all quark contraction classes; longitudinal propagator terms
then decouple. This is a precise canonical path, not permission to vary
independent photon-mass-dependent matter interactions.

For the non-Born response write

    f(s)=M_u^NB(s)/M
        =integral_0^infinity dt g(t) t/(t+s)+local matching,
    g(t)=1/(32pi^3 M^2) integral_-1^1 dx sqrt(1-x^2)
              [-3t1^NB(i sqrt(t)x,t)+(1-x^2)t2^NB(i sqrt(t)x,t)]. (1)

The complete low-energy polarizability tensor gives

    g(t)=2 C t+O(t^2),
    C=3/(32pi M) [(alpha_E-beta_M)/u].                       (2)

The inherited derivation checked the relative normalization of both scalar
amplitudes against the complete Born tensor. Independently the Euclidean
local polarizability interaction is
`2pi[alpha_E E_E^2-beta_M B_E^2]`; isotropic photon contraction gives the
same (2), since each electric/magnetic trace has angular mean 3/2.

## 2. Logarithm and a positive third-derivative filter

For the exact local-polarizability benchmark g(t)=2Ct on `0<t<T`,

    f_loc(s)=C[T^2-2sT+2s^2 log((T+s)/s)].                  (3)

Thus the coefficient of `s^2 log(s/mu^2)` is

    c_log,NB=-2 C.                                         (4)

The scale in the logarithm changes only an analytic s^2 term. With
`D=s partial_s`, `P3(D)=D(D-1)(D-2)=s^3 partial_s^3`,

    G3(s):=-s f'''(s)/4
      =(3s/2) integral dt g(t)t/(t+s)^4,
    lim_(s->0) G3(s)=C.                                   (5)

Analytic terms of degrees 0,1,2 are annihilated. The kernel is UV convergent
for the current-product OPE and nonnegative when applied to a positive g;
the physical non-Born g itself need not have a positive sign. For (3),

    G3_loc/C=[T/(T+s)]^3.                                  (6)

This is an exact cutoff correction, not a fit/extrapolation ansatz.

Here is a quantitative remainder statement. If
`|g(t)-2Ct|<=B t^2` for `0<t<T`, then

    |G3_(0,T)-C[T/(T+s)]^3|
      <= (3Bs/2) [log(1+T/s)-y-y^2/2-y^3/3],
    y=T/(T+s).                                            (7)

The bracket is the exact positive integral
`integral_0^T t^3/(t+s)^4 dt`. If the UV tail satisfies
`integral_T^infinity |g(t)|/t^3 dt < infinity`, its filter is bounded by
`(3s/2) integral_T^infinity |g(t)|/t^3 dt`. Consequently the full limit (5)
is established under these hypotheses, with a soft O(s log s) and hard O(s)
remainder. An unknown physical B/tail is not replaced by a numerical bound.

## 3. Coordinate kernel

The four-dimensional scalar Euclidean propagator is

    D_s(r)=sqrt(s) K1(sqrt(s)r)/(4pi^2 r)
          =integral_0^infinity d tau (4pi tau)^(-2)
             exp[-r^2/(4tau)-s tau].

Three derivatives of this Schwinger representation give exactly

    partial_s^3 D_s(r)=-r^2 K2(sqrt(s)r)/(32pi^2 s),
    -s partial_s^3 D_s(r)/4=r^2 K2(sqrt(s)r)/(128pi^2).     (8)

At r=0 the first expression has limit `-1/(16pi^2 s^2)`;
there is no sign change or omitted factor of two. A position-space
implementation must apply (8) to the complete Born-subtracted current
correlator, retaining its Ward contacts and normalization. It is not a
license to convolve a single measured temporal moment. The kernel probes
distances of order `1/sqrt(s)`; finite-volume control becomes harder as s
decreases.

## 4. Removing lower charged-Born powers without full form factors

For the standard on-shell Born convention, the inherited all-angle Born
kernel has the expansion

    B(z)=1+c z^2+d z^3+O(z^4),   z=Q/(2M),
    d=2+6 kappa+(3/2) kappa^2.                             (9)

The coefficient of z is exactly zero; it requires retaining the non-pole
Dirac Born term. Radius terms enter c, but cancel in d. Integrating
`B(z) z^2/(z^2+s/(4M^2)) /(2pi^2)` near zero yields

    f_B(s)=analytic
          -sqrt(s)/(8pi M)
          +c s^(3/2)/(32pi M^3)
          -d s^2 log(s/mu^2)/(64pi^2 M^4)+o(s^2 log s).

There is no `s log s`, precisely because the linear-z coefficient vanishes.
At this order in u, pure QCD with positive pion mass has no soft logarithms
inside the form factors; higher powers can be controlled by their local
analyticity. This is not a claim about finite-u multi-photon mass functions.

Define

    P5(D)=D(D-1/2)(D-1)(D-3/2)(D-2)
         =(15/4)s^3 partial_s^3+5s^4 partial_s^4+s^5 partial_s^5.

It annihilates `1,s^(1/2),s,s^(3/2),s^2` and sends `s^2 log s` to
`(3/2)s^2`. Therefore for the full canonical order-u response,

    L5:=lim_(s->0) P5(D)f_full(s)/s^2=(3/2)c_log,total,
    C_NB=-d/(128pi^2 M^4)-L5/3.                            (10)

This needs the QCD anomalous moment kappa, but no elastic form-factor curve
over all Q. It still leaves f_full(0) completely undetermined.
The exact derivative kernel used in the run is

    P5(D)[t/(t+s)]/s^2
      =-15ts(3t-s)(t-3s)/[2(t+s)^6].                       (11)

Unlike G3 it changes sign. This enhances cancellation/noise in a data
implementation. For (3) the corresponding non-Born estimator is

    -P5 f_loc/(3s^2 C)=16y^5-20y^4+5y^3,  y=T/(T+s).     (12)

## 5. Executed benchmark design, no fitted mass curve

The full finite-momentum HB pi-N functions in the frozen package are applied
directly to (5) and (11), with photon ball `0<Q<m_pi/2`. This uses their
actual two-variable amplitudes and seagull, not the soft polynomial. Define
`sigma=s/m_pi^2`, `A(r)=integral dx sqrt(1-x^2)[-3B1+(1-x^2)S2/C0]`,
`a0=9pi/32`, and `R(t)=A(sqrt(t))/(a0 t)`. Then, with
`y=t/(t+sigma)`, `t=sigma(exp(v)-1)`,

    G3_HB/C_HB=3 integral_0^ymax dy y^2 R(sigma y/(1-y)),
    -P5 f_HB/(3s^2 C_HB)
       =5 integral_0^ymax dy y^2(4y-1)(4y-3) R(sigma y/(1-y)). (13)

The v variable resolves small photon masses without a fitted curve. Six
lambda/m_pi controls and two quadrature orders are declared. We report both
the exact local cutoff factors (6),(12) and the computed full-function
corrections, recovering the analytically known C_HB without a numerical fit.
No global full-QCD remainder bound is claimed.

An independent elementary Dirac benchmark tests (10). With M=1 and
`B_D(z)=[sqrt(1+z^2)+2z]/[sqrt(1+z^2)+z]^2`, d=2, the prediction is
`L5_D=-3/(64pi^2)` and C_NB=0. We compare the all-momentum radial convolution
against the independently derived on-shell Feynman-parameter expression

    f_D(s)=constant-(1/(8pi^2)) integral_0^1 dx (1+x)
                            log[x^2+(1-x)s].              (14)

Its additive UV/mass-scheme constant is killed by P5. Derivatives are taken
analytically under the integral, never by a finite-difference fit. The radial
calculation subtracts the constant and quadratic B_D terms whose P5
integrals vanish identically, improving numerical cancellation. The local
benchmark (3), operator kernels, coordinate kernel and cutoff-remainder
integral provide further independent checks.

## 6. Matching, QED_M and finite-volume limits

The canonical deformation in section 1 is essential. Endres et al.,
[1507.08916v3](https://arxiv.org/abs/1507.08916v3), equation (3), establishes
the universal `-alpha Q^2 lambda/2` mass shift and an analytic lambda^2 term
with a matching coefficient. This agrees with our charge-stripped Born
`-lambda/(8pi M)`. Their general massive-photon hadron EFT permits extra
operators not constrained by gauge invariance; footnote 42 specifically
mentions `m_gamma^2 A_mu A_mu N^dagger N` at N3LO. Such a mass-dependent
two-photon contact can produce an `s^2 log s` tadpole. It is not annihilated
by P3/P5. Thus arbitrary source QED_M curves cannot be identified with
(10) until regulator-specific contact coefficients are matched to the
canonical conserved-current deformation. Fixed mass-independent *mass*
counterterms alone are harmless; unknown mass-dependent photon contacts
are a different obligation.

Footnote 42 does not specify that operator's order in u or determine its
matching coefficient. We have not shown contamination, an extra free O(u)
coupling, or an error in the paper's canonical microscopic theory. In the
canonical minimally gauged quark theory, the order-u answer is exactly the
fixed pure-QCD current tensor; any NR/EOM representation must reproduce it.
The broad-EFT example is an admission check when importing a differently
defined mass curve, not evidence against the canonical filter identity.

For example, if an extra contribution is defined as `h s I_R(s)`, with
`I_R(s)=s[log(s/mu^2)-1]/(16pi^2)`, it shifts c_log by `h/(16pi^2)` and
the G3 limit by `-h/(32pi^2)`. This illustrates the matching issue without
assuming that h is present or free in a correctly matched canonical theory.

The infinite-volume limit must precede the zero-photon-mass limit, or one
must show uniform control with `lambda L` large. Clark et al.,
[2201.03251v1](https://arxiv.org/abs/2201.03251v1), sections 2--3 and 5,
shows the nonperturbative role of QED_M zero modes. Charged correlators at
fixed finite volume are not the infinite-volume mass function in (1).
Born subtraction must use the same regulator, normalization and limit order;
subtracting just a dispersive pole would leave the forbidden spurious lower
terms. In the chiral limit the spectral gap disappears, so (2)--(7) cannot be
used with the same uniform constants or exchanged limits.

The numerical strong inputs inherited from AHLP are an explicit printed
source-parameter benchmark. In particular `m_pi=0.13957 GeV` is the printed
charged-pion benchmark, not an independently matched pure-QCD pion mass on
the fixed-MSbar path. Neither these computations nor a fit-free filter fixes
that calibration, missing full physical data, or the independent vacuum term.
No novelty claim is made: the construction is a translated low-energy/QED_M
infrared diagnostic. Its exact algebra and tested ranges are separate from
whether a usable full-QCD dataset exists.
