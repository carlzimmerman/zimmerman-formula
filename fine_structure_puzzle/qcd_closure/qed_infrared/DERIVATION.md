# Physical order-e² current insertion on a smooth closed S4

FSP-005, QED infrared lane. Hand derivation, followed by a bounded exact/finite
spectral check. The target and sign convention are the frozen
`qcd_prediction/coordinator/METRIC_RESPONSE.md`; that file supplies the
observable definition, not a computed QCD result. No prior scientific file was
changed. The calculations below use physical electromagnetic charge and never
identify it with a Yang--Mills coupling.

## 1. Claim card and scope

Let g_H be the round metric on S4, radius a=H^-1, volume
V=Ω4 H^-4, Ω4=8π²/3, θ=0. Quark masses and all renormalized comparison inputs
are fixed on a specified matching path. A positive hadronic gap is assumed;
no chiral limit is taken. W=-log Z and f=W/V. The Euclidean convention is
δW=(1/2)∫sqrt(g) T_E^{ab} δg_ab. In the invariant sphere state,

    ρ_E = (1-D/4) f,        D=H∂_H.

In particular a linear term in f has 3/4 its coefficient in ρ_E. The desired
quantity is A_ρ, not a susceptibility or a coefficient of f. We investigate
f_1=∂_(e²)f|_(e²=0), including renormalized parameter counterterms.

**Precise result:** conditional on the uniform local matching, metric
clustering, global-state and differentiated-remainder hypotheses in section 5,
the order-e² insertion has no H term, so its projected linear coefficient is
zero. This does not establish those hypotheses for QCD, does not exclude a
nonlocal global response, and does not justify exchanging ∂_(e²) and H→0
without additional uniform control. Section 7 gives a quantitative loophole
and explicitly exhibits the exchange-of-limits problem.

## 2. Actual insertion and its metric derivative

Use a canonically normalized Maxwell field, S_γ=(1/4)∫F², and
S_int=i e∫A_μJ^μ. Gaussian photon integration gives

    W = W_QCD + W_γ + e² W_1 + O(e⁴),
    W_1 = (1/2) Tr_T(D_g K_g) + W_1^ct,
    K_g(x,y) = <J(x)J(y)>_QCD, including Ward contact terms,
    D_g = Δ_1,T^-1.

The notation Tr_T includes the integration measures and tensor contractions.
It is the expectation of the actual current-current insertion; all connected
and disconnected quark contractions are retained. W_1^ct contains the quark,
strong, vacuum and gravitational matching insertions. The sign follows
<exp(-i e A.J)>_γ=exp[-e²(J,DJ)/2]. This expansion and the need for contact
renormalization agree with de Divitiis et al., exact 1303.4896v1, section 2,
equations (2)-(7). Their finite-torus photon prescription is not imported as a
sphere prescription.

Gauge invariance of the external-current generating functional implies

    ∇_x^μ K_(μν)(x,y)=0

as a distribution, including contact terms. Therefore longitudinal propagator
changes drop out of the contracted insertion on the closed sphere. A bare
separated-point JJ kernel without its contacts is not sufficient. There is no
allowed local gauge-noninvariant photon mass term.

Metric differentiation is nevertheless more than the flat Ward identity:

    δ_g W_1 = (1/2)Tr_T[(δ_g D_g)K_g + D_g(δ_g K_g)] + δ_g W_1^ct.

Here δD=-D(δΔ_1)D on the transported transverse subspace, with its projector
and measure variations included. In δK there are explicit metric/current
contacts and the connected insertion

    -(1/2)∫sqrt(g) δg_ab(z) <T_QCD^{ab}(z) J(x)J(y)>_c.

Higher metric derivatives introduce T...TJJ cumulants and further contacts.
Diffeomorphism Ward identities constrain their divergences and contacts; they
do not prove their analyticity at zero metric momentum. This is the missing
logical step if one only cites a flat hadron mass spectrum.

## 3. What the flat current spectral gap actually implies

Fix the tensor sign by writing, in flat Euclidean space,

    K_μν(Q)=(Q²δ_μν-Q_μQ_ν) Π_E(Q²).

For a unitary conserved current the positive spectral measure ρ_J(s) gives,
after charge subtraction at Q²=0,

    Π_R(Q²)=Π_E(Q²)-Π_E(0)
           = -Q² ∫_(s0)^∞ ds ρ_J(s)/[s(s+Q²)],       s0>0.

Polynomial UV contacts are fixed by the stated renormalizable matching; the
constant Π_E(0) is the charge threshold. The minus sign is part of our tensor
convention. With the opposite tensor convention the usual polarization scalar
has the opposite sign. Positivity follows by inserting a complete set of
physical states into the transverse current spectral density. The mass gap
then gives analytic continuation for |Q²|<s0 and, for example,

    Π_R(Q²)=-M1 Q² + M2 Q⁴ - ...,
    Mn = ∫_(s0)^∞ ds ρ_J(s)/s^(n+1),
    |Π_R(Q²)| <= |Q²| M1/(1-|Q²|/s0).

Convergence of these once-subtracted moments assumes the ordinary tempered
short-distance current behavior. No numerical QCD value is inserted here.
This controls the flat two-current channel. It does not assert that all soft
metric limits of T...TJJ have the same spectral gap or a uniform radius limit.

As a normalization check, one free unit-charge massive Dirac field has

    ρ_D(s)=[(1+2m²/s)sqrt(1-4m²/s)]/(12π²),  s>=4m²,
    M1,D = 1/(60π² m²).

This follows directly by the two-particle current cut. The substitution
u=sqrt(1-4m²/s) reduces the moment to
∫_0^1 u²(3-u²)du/(48π²m²). It is a benchmark for charge and moment
normalization, not a model of QCD and not a claim about its curvature LECs.

## 4. Massless Maxwell field: domain, global measure and anomaly

The ordinary smooth compact-U1 theory is used. S4 has H¹(S4,Z)=H²(S4,Z)=0:
there is no harmonic photon one-form and no U1 flux sector. The constant scalar
gauge transformation remains in the gauge group and must be divided out.
These statements concern the photon bundle; they do not remove QCD instanton
sectors or prove anything about their metric dependence.

With the canonical L2 mode measure at a fixed mass scale μ, Hodge decomposition
and the gauge quotient give

    Z_γ = C(e,μ) V^-1/2 [det'(Δ0/μ²)]^(1/2)
                           [det_T(Δ1/μ²)]^(-1/2).

The scalar prime excludes the constant ghost eigenfunction; its role is
replaced by the displayed canonical group volume. C is metric independent.
The general compact-manifold formula is verified in Donnelly--Michel--Wall,
1611.05920v1, PDF equations (2.9), (2.14), (2.19). Their connection variable is
rescaled to the canonical photon here; rescaling must also transform the
measure. Charge-dependent factors such as log(e) in W can be normalization
singular at e=0, but are metric-independent W terms and yield f∝H⁴ with zero
round-sphere stress. They cannot supply A_ρ. The connected insertion is defined
after fixing this convention.

The Hodge Laplacian on coexact one-forms is Δ1=-∇²+Ric. Its exact spectrum is

    λ_l=H² x_l,   x_l=(l+1)(l+2),
    d_l=l(l+3)(2l+3)/2,       l=1,2,... .

The lowest eigenvalue is 6H² with multiplicity 10. Killing one-forms are not
zero modes of this Maxwell operator. Scalar nonzero eigenvalues are
H² l(l+3), multiplicity (l+1)(l+2)(2l+3)/6, l>=1. Kluth--Litim,
1910.00543v2, Table 4 gives the rough-Laplacian spectrum; adding Ric=3H²
produces the Hodge spectrum above.

Define ζ_T(s)=Σ_l d_l x_l^-s, continued from Re(s)>2. Set n=l+3/2,
q=5/2, b=1/4. Then

    ζ_T(s)= Σ_(k>=0) (s)_k b^k/k!
        [ ζ_H(2s+2k-3,q) - (9/4)ζ_H(2s+2k-1,q) ].

The expansion is uniformly convergent for the continued tail because
b/q²=1/25<1. At s=0 or -1 one must retain the product of a vanishing Pochhammer
factor and a Hurwitz-zeta pole. Directly substituting s before continuing loses
these contributions. Using ζ_H(-j,q)=-B_(j+1)(q)/(j+1),

    ζ_T(0)=ζ_H(-3,q)-(9/4)ζ_H(-1,q)-17/64 = 19/30,
    ζ_T(-1)=ζ_H(-5,q)-(5/2)ζ_H(-3,q)
                         +(9/16)ζ_H(-1,q)+13/384 = 5/63.

The nonzero minimal-scalar zeta value is ζ_0'(0)=-61/90; here the prime labels
excluded zero modes, not a derivative in s. Accordingly

    dW_γ/dlog(a) = -ζ_T(0)+ζ_0'(0)+2 = 31/45.

The final +2 is d[log(V)/2]/dlog(a). Dropping it gives the wrong anomaly.
In the stipulated Euclidean convention,

    f_γ = -(31/(45Ω4)) H⁴ log(H/μ) + const·H⁴,
    ρ_γ = +(31/(180Ω4)) H⁴.

This is the free Maxwell scale anomaly, a=31/180 in the usual central-charge
normalization. It is independent of the electromagnetic coupling in the
low-energy free photon theory. Heavy thresholds renormalize local curvature
terms and irrelevant operators; the free anomaly is not an e²Λ³H effect.
A conformal-anomaly action can be nonlocal, but its sphere scaling is H⁴ (and
H⁴logH in f), not H. There is no boundary or independent thermal circle here.

An independent heat expansion is

    Tr_T exp[-t Δ1/H²] = 1/(2t²) - 1/t + 19/30 - (5/63)t + O(t²).

The finite spectral run checks it without replacing the current insertion by
an anomaly or susceptibility.

## 5. Conditional exclusion and the hypotheses it needs

Here are sufficient hypotheses, distinguished from established QCD inputs.

1. A fixed positive-gap θ=0 QCD phase has a gauge- and diffeomorphism-covariant
   regulator and local counterterms. Renormalized masses, strong scale and
   charge convention remain fixed as g_H varies. The weak-curvature family
   stays in the same phase and state.
2. After the local contact subtractions, connected QCD cumulants T...TJJ and
   the parameter-matching scalar insertions have uniform exponentially
   integrable tree-distance bounds and sufficiently many coordinate moments.
   The bounds hold for the metric derivatives used below, not only for flat
   JJ. Metric response admits the resulting covariant local Taylor expansion
   with a controlled remainder in each fixed-size patch. This last uniform
   Taylor/remainder property is explicit; flat spectral positivity alone does
   not establish it.
3. The closed-sphere state/global sum has no extra radius-sensitive sector
   outside that uniformly local matching. A precise sufficient bound for its
   residual contribution r to f_1 is |D^j r| <= C_j H^(-N_j) exp(-c m_gap/H),
   j=0,...,4, with c>0 and finite constants C_j,N_j independent of H. This is
   a substantive global-state condition, not something proved by measured
   hadron masses. More general bounds can suffice, but are not assumed here.
4. The massless photon uses precisely the canonical smooth-sphere domain and
   measure of section 4. It is the only gapless field. Renormalization and
   the differentiated small-H expansion commute to the order stated.

Under these hypotheses, integrate out QCD at a fixed Wilsonian scale ν with
H<<ν<<sqrt(s0). Gauge invariance makes the order-e² induced photon action
quadratic in F, with analytic covariant derivative/curvature coefficients.
Contact and high-frequency photon contributions supply local gravitational
terms. At finite derivative order the reason for locality is concrete:
weighted exponential moment bounds let one Taylor-expand the background in
normal coordinates. On S4 every local curvature insertion carries H². For
the tail one may take patch size L=(N/m_gap)log(m_gap/H); the exponential bound
beats any prescribed power of H, while H²L² tends to zero. The uniform
metric-Taylor remainder in hypothesis 2 and the differentiated control in
hypothesis 3 are needed to justify this procedure. They have not been proved
for the full QCD sphere partition function here.

The low-energy Maxwell trace is then a trace of analytic local differential
operators, treated with the same covariant regulator. Fixed-scale hard modes
produce local terms; the actual massless low modes scale with H and give
H⁴ times a dimensionless spectral quantity, or additional even powers H² per
irrelevant insertion. Logarithmic scale terms remain possible. Thus through
the orders relevant to the linear projection,

    f_1(H) = b0 + b2 H² + b4 H⁴
             + O(H⁴ log^p H) + O(H⁶ log^q H) + r(H),

with controlled D derivatives and r=o(H). In the decoupled free-Maxwell EFT
the unsuppressed anomaly coefficient itself has no e² derivative; the broader
logarithmic bound suffices for this conditional statement. Local matching
coefficients need not be known for this conclusion. Since P(D)=D(D-2)(D-4),

    lim_(H→0) P(D)(1-D/4)f_1(H)/(3H)=0.

This proves the **order-e² insertion projection** under the named hypotheses.
To identify it with ∂_(e²) A_ρ requires a further uniform interchange of
∂_(e²), the derivatives D, and H→0. The conclusion is neither an unconditional
QCD no-go nor a theorem inferred from the hadron gap alone.

## 6. Nontrivial leading curvature/charge EFT response

Keep a specific common zeta/covariant local subtraction convention for the
photon trace. Through photon dimension six, the quadratic action on S4 can be
written

    Γ_γ^(2) = (1/2)<A, Δ1[1+e²(κ0+c_R H²+c_λ Δ1)]A> + O(e²∂⁶/m_gap⁴),
    c_λ = -M1 = -∫ds ρ_J(s)/s² .

κ0 is fixed by charge matching (zero in the chosen zero-momentum subtraction).
Both c_R and c_λ have mass dimension -2. c_R denotes the particular round-S4
combination of RF², Ric_μν F^{μλ}F^ν_λ, and Riem_μνρσ F^{μν}F^{ρσ}
coefficients. It is defined by the displayed quadratic kernel, eliminating
factor ambiguities in individual operator conventions. Those curvature
operators require a TJJ matching calculation. A flat JJ spectral function
cannot determine c_R. Terms proportional to (∇_μF^{μν})² contribute to c_λ.

The order-e² trace is exactly linear, so

    W_(1,γ) = (κ0/2)ζ_T(0)
                +(H²/2)[c_R ζ_T(0)+c_λ ζ_T(-1)]+O(H⁴/m_gap⁴),

and the dimension-six portion is

    δf_(γ,6) = e² H⁶/(2Ω4) [(19/30)c_R+(5/63)c_λ],
    δρ_(γ,6) = -e² H⁶/(4Ω4) [(19/30)c_R+(5/63)c_λ].

The minus sign in the stress is the actual metric factor 1-6/4=-1/2.
The charge-matching κ0 term gives a radius-independent W, hence zero sphere
stress. This is an explicit nonzero curvature/charge response in a declared
EFT; no observed α or dark-energy coefficient has been fitted.

For the **minimal spectral-lift diagnostic** c_R=0 and one free unit-charge
Dirac spectral density, the displayed photon-trace contribution is

    δρ_(γ,6) = e² H⁶/(8064 π⁴ m²).

This is not the full curved-space Dirac-QED result: setting c_R=0 is a declared
spectral-lift model, and actual matter has its own curvature matching. For QCD,
M1 can in principle be determined independently from the charge-normalized
current spectrum or lattice QCD. It was not determined here.

Even once M1 and c_R are supplied, the **full** order-e² H⁶ coefficient contains
independent local pure-gravity matching b6, in addition to the lower b0,b2,b4
and parameter-retuning insertions. It is not a universal vacuum-energy
prediction. A field redefinition removing the redundant (∇F)² operator shifts
this local trace through its Jacobian and gravitational matching. Fixing the
measure/subtraction makes the displayed trace well defined; treating it as a
scheme-independent total would be an error. None of these local dimension-six
ambiguities affects the linear-H projection.

## 7. Quantitative infrared loopholes and noncommuting limits

Let F_l(H)=K_l(H)/λ_l. Then the genuine order-e² insertion obeys

    f_1(H) = H⁴/(2Ω4) Σ_l d_l F_l(H) + local matching,

with the sum renormalized in the common regulator. An H term therefore
requires a nonlocal remainder with regulated trace growing as H^-3. For a
flat-like scalar form factor F(k²)~C(k²)^(-p), the soft four-dimensional
integral scales as H^(4-2p); the required exponent is p=3/2. Equivalently,
K(k)~C/|k|, since the photon inverse propagator contributes k². A
F~C/|k|³ polarization gives the continuum missing-soft-mode estimate
3C H/(16π²), before the actual sphere geometry and subtraction are supplied.
The coefficient 3 counts off-shell transverse components; this cutoff estimate
is a scaling diagnostic, not a sphere observable. It is forbidden by the
analytic gapped **flat** current representation of section 3.

But a global sphere response can escape pointwise flat spectroscopy. For an
explicit kinematic example add to the source-current Hessian

    δK_H = γ Λ³ H^-1 χ(Δ1/H²) P_T,

where χ is the spectral projector onto l=1,2,3 on the round sphere. It can be
defined covariantly on a near-round family from the spectrum and
H=(Ω4/V)^(1/4). It is transverse, diffeomorphism-covariant as a nonlocal
functional, and a positive quadratic operator for γ>0. Its coordinate kernel
is O(Λ³H³) at fixed separation and vanishes in the pointwise flat limit: each
normalized one-form kernel supplies H⁴ and its eigenvalue supplies H^-1.
The gapped local flat JJ spectrum is therefore unchanged. Nevertheless,

    δF_l=γ(Λ/H)³/x_l,       l=1,2,3,
    Σ_(l=1)^3 d_l/x_l = 259/30,
    δf_1 = (259 γΛ³/(60Ω4)) H,
    δρ_1 = (259 γΛ³/(80Ω4)) H.

This example violates the required **uniform** metric clustering: at a
separation proportional to a the tail is a power H³ rather than exp(-m/H).
Its positivity as a quadratic operator is not proof of Osterwalder--Schrader
reflection positivity or existence as a local QCD theory. It is a countermodel
to the inference from pointwise flat gap plus Ward identities alone.
No such term has been derived from the QCD measure or topology sum.

There is a second, crucial limitation. If this quadratic kernel is used in an
otherwise Gaussian photon theory at finite e, its exact contribution is

    δW(e,H)=(1/2)Σ_(l=1)^3 d_l
                   log[1+e²γ(Λ/H)³/x_l].

For fixed nonzero e it grows only as log(H), giving f=O(H⁴logH), and not H.
The order-e² expansion requires e²γ(Λ/H)³<<1 and is not uniform as H→0.
Thus its nonzero insertion projection does **not** imply nonzero
∂_(e²)A_ρ, much less a physical alpha selector. Any proposed loophole must
supply both the H^-3 infrared enhancement and a controlled fixed-charge
resummation or an independent global contribution with the correct full
metric response.

A separate factor exp[-e² cΛ³ V^(3/4)] would trivially give a genuine H term
while leaving normalized flat local correlators unchanged, but it is an
added nonlocal metric-dependent normalization, not an allowed local
counterterm or a derivation from the canonical QCD+QED path integral. It is
not used as evidence of a physical mechanism. QCD global/topological and state
control, rather than arbitrary normalization, remains the relevant open arrow.

## 8. Evidence, audit and continuation

The exact analytic continuation and EFT reduction above are hand arguments.
`PRECONTRACT.json` was saved before execution. `spectral_check.py` independently
checks exact Bernoulli arithmetic, eight finite spectral heat sums (l=1..300,
four t values, 60/80 digits), the flat Dirac moment, and the finite soft-mode
sum. `run_001` is preserved as launch-failed: the macOS pre-exec memory limit
failed before Python launched. `run_002` completed after dropping that memory
cap while keeping 30s wall, 25s CPU, one conventional numerical thread and
100000 output bytes. Both v2 manifests validate and have unchanged input
hashes. The finite heat estimates approach 5/63 from 0.0797165 at t=.02 to
0.0794088 at t=.0025. This is a consistency check, not a proof from a finite
table. The programmed tail bound is evaluated by high-precision quadrature;
its formula is a valid monotone integral majorant, but the reported decimal
bound is not interval certified.

The self-review checks signs, Hodge versus rough spectrum, scalar zero-mode
subtraction, anomaly group factor, residue limits, flat-versus-curved matching,
operator redundancy, and the nonuniform e² countermodel. No fresh reviewer
was spawned by this lane. No novelty claim is made. Exact primary source
receipts are in `SOURCES.json`.

The cheapest physical next check is a regulated QCD calculation of the soft
TJJ response (with its contact/matching terms) or the radius-dependent
transverse current kernel K_l(H) on the same closed-sphere state. It must test
uniform bounds for low l as H→0 and exclude the H^-1 current eigenvalue
behavior above, while separately controlling the global QCD sector sum and
four scale derivatives. Flat M1 can calibrate c_λ but cannot complete this
check. This lane establishes the conditional arrow and a nontrivial exact
spectral/EFT benchmark; full A_ρ(α)/m_p³ remains uncalculated.
