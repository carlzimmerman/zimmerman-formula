# TP05 protected-gravity handoff — incomplete, unexecuted construction

Frozen at the user's immediate commit/push handoff request,1November2026.
No new calculation is authorized by this handoff. This subroute performed
source reads and hand algebra only: **no TP05 protected-gravity numerical
experiment, stationary-point solve, scalar/fermion spectrum or v2 run was
executed.** There is no completed embedding or validated photino survival
claim in this directory. Earlier TP01–04 science is unchanged.

Parent contract: ../CONTRACT.md. Starting shared revision:
`8a293ba8b8411e84c9e37bb9770d1a6f993f606e`. Ownership was only this
protected_gravity/ directory. No Git, queue, installation or production
simulation action was taken by this subagent.

## Starting model and the two dark-energy questions

The actual TP01–04 microscopic action is the collective SU5 model from
microscopic_vacuum_2026_10_28/INVERTED_HIERARCHY.md,

    W_micro=fX+(h/2)X Tr A²+(lambda/2)Tr A²B,
    K_micro=|X|²+Tr A†A+Tr B†B.

The distinct MODEL.md file first treats a singlet Shih model; it supplies
general gravity caveats, not a replacement SU5 spectrum. Do not stitch
those two matter models together. The collective commuting valley obeys

    A=i aD, B=bD, D=diag(2,2,2,−3,−3), Tr D²=30,
    a²=2fh/(30h²+lambda²), b=hX/lambda,
    T_flat=sqrt(30h²+lambda²)X/lambda,
    F_hidden=f lambda/sqrt(30h²+lambda²),
    W_micro|valley=fX=F_hidden T_flat.

The TP04 radiative photino benchmark has h=lambda=e=.003,
g=sqrt(29/200)e, mu=sqrt(f)=1.81707e7GeV and m_chi approximately1MeV.
Its raw matter F-energy exceeds the benchmark dark energy by about1.396e74.
Equating that raw energy to dark energy instead makes the original
radiative photino ultralight. This strong source-link obstruction is not
removed by calling a separately tuned net gravitational energy dark energy.

The weaker net gravitational link permits a specified cancellation and
then lets the residual positive V enter a0=kappa c sqrt(G rho_Lambda).
Such a residual remains a parameter/tuning; it does not derive rho_Lambda,
the microscopic stiffness ratio or the fitted kappa. This distinction is
essential to any continuation below.

## Hand-checked algebra: what exact no-scale actually cancels

Use reduced Planck mass M and a dimensionless added modulus tau. For

    K=−3M² log Y,
    Y=tau+taubar−K_micro/(3M²),
    W=W_micro+W0,  W_tau=0,
    f_SU5,gauge=constant,

direct inversion of the logarithmic Kähler metric gives

    V=Y^(−2) sum_i |W_micro,i|².

The W0 terms cancel themselves. The positive matter F-energy is not
canceled, and a modulus direction remains unstabilized/runaway once the
matter energy is present. Thus the phrase “no-scale protects it” alone is
not a solution of the requested cancellation/stationarity problem.

A useful hand-derived generalization, still with W_tau=0, is

    K=−nM² log[tau+taubar−K_micro/(nM²)], n=3−epsilon,
    V=Y^(−n)[Y sum_i|W_i|²−epsilon |W|²/M²].

This identity follows by explicitly retaining the inverse-metric
modulus/matter cross terms; treating K as a separable sum gives the wrong
matter tadpole. This is hand algebra, not an independently checked symbolic
certificate or numerical test. For epsilon>0 the negative W0 contribution
can be tuned against the matter F-energy. Before any stabilizing deformation,
the modulus potential has no controlled near-Minkowski minimum: fixing it
is a separate obligation.

At Y near1, the leading matter-valley R-breaking tadpole from this identity
is −2epsilon W0 f ReX/M². This differs from canonical SUGRA's
−4W0 f ReX/M². Canonical algebra independently checked with the gravity
agent is

    sum_i phi_i W_i=W_linear+3W_cubic,
    delta V_(linear W0)=2Re[W0*(sum_i phi_i W_i−3W_micro)]/M²
                       =−4Re(W0* fX)/M².

All leading cubic heavy-normal sources cancel in the canonical expression.
The protected case can suppress the matter tadpole at the cost of a larger
gravitino/modulus SUSY-breaking sector. Neither expression by itself proves
that the radiative vacuum remains stationary or stable.

## Proposed explicit stabilized model — not executed

The candidate to test was

    H=tau+taubar+b(tau+taubar−1)^4+c(tau−taubar)^4,
    Y=H−K_micro/(nM²),
    K=−nM² log Y, n=3−epsilon,
    W=W_micro+W0,
    f_SU5,gauge=constant with Re f=1/g².

This adds one chiral modulus, epsilon, two quartic stabilization parameters,
the chosen center Re tau=1/2, and W0. They are new physical data. A proposed
bounded benchmark was epsilon=1e−4 and b=c=1e8, with the TP04 e and mu
held initially fixed. No statement here selects those values dynamically.

For carrying the calculation forward, define

    P=H_tau, Q=H_(tau taubar), D_H=|P|²−H Q,
    F0=sum_i |W_micro,i|², S=sum_i phi_i W_micro,i.

On the real CP slice, the inverse-metric hand reduction gives

    V=Y^(−n){Y F0−epsilon |W|²/M²
             +Y Q |S−nW|²/[n D_H M²]}.

The complex-slice extension and all index/conjugation conventions still
need an independent direct metric inversion check before relying on this
as executed code. The K-positive domain requires Y>0 and a positive metric;
the corresponding Schur condition is D_H>0 when H>0. It must be checked at
the actual stationary point rather than assumed from the model's name.

On the commuting real matter slice, convenient exact raw contractions are

    W_micro=fX−15hXa²+15lambda a²b,
    F0=(f−15ha²)²+(15/2)lambda²a^4
                           +30a²(hX−lambda b)²,
    S=fX−45hXa²+45lambda a²b,
    K_micro=X²+30a²+30b².

These allow a small stationary solve without inverting a50-field metric.
Any full-spectrum claim must subsequently return to the nonaligned matter
directions, gauge Goldstones, D-flatness and proper kinetic normalization.

## Provisional scale estimates and critical caveats

Near Y=1, cancellation would require
epsilon |W0|²/M² approximately F_hidden², giving
m_3/2 approximately F_hidden/(sqrt(epsilon)M). The proposed benchmark
therefore suggests a gravitino mass of order2.4MeV. Quartic stabilization
suggests modulus masses of order sqrt(48b)m_3/2, around10²GeV for the trial
b. These are estimates from expansion, not measured eigenvalues. The
stationary modulus displacement was expected to be small, of order
epsilon/b; no solve confirmed it.

The suppressed radial tadpole suggested a few-percent shift of the global
finite-CW minimum at epsilon=1e−4, but no actual minimum, radial curvature
or R-axion mass was found. A sufficiently large tilt can destroy a shallow
local minimum, so an estimate of its initial shift is not an existence proof.
The full finite one-loop CW potential, not the old common-threshold
leading-log curvature, must be used for this test.

The modulus F-term would dominate the total SUSY breaking. **The old rigid
Goldstino cannot simply be retained as the eaten mode**, nor may its width
be rescaled by replacing F_hidden with F_total without checking new neutral
fermions. There is an additional orthogonal neutral fermion. In this
sequestered geometry its raw mass can be O(epsilon m_3/2), rather than
generically2m_3/2; loop stationarity contributes at the same order. Its pole,
mixing and photino transition current were not computed. In particular,
m_3/2>m_chi alone would not establish a stable photino: a light orthogonal
fermion plus photon channel can remain open.

Constant gauge kinetic data avoid a direct tree modulus-gaugino mass, but
anomaly mediation and finite heavy thresholds still require matching. A
small compensator auxiliary by itself is not a complete anomaly argument.
The physical matter metric and all anomaly terms must be retained. No
finite SUGRA threshold or corrected photino pole was calculated here.

No-scale breaking and quartic terms are EFT choices. The cutoff associated
with b,c must exceed the resulting modulus masses, and the required small
epsilon/stabilization coefficients need radiative/UV control. No UV origin
or radiative protection of these added parameters was established.

## Exact no-scale strong-link alternative: requested but untested

The coordinator suggested a different branch: keep exact n=3, let a large
modulus F cancel its own vacuum contribution, let the tiny matter F set
dark energy, and give the photino a mass through tau-dependent gauge
kinetic data. That **replaces the original radiative mass source**. It is
not a continuation of the TP04 photino spectrum/lifetime without a new
matching calculation. Its soft-gaugino vacuum loops can exceed dark energy
by many orders, and the much lighter charged matter may reopen fast
gaugino decays. Neither its spectrum, cancellation nor lifetime was tested.
It must be recorded as a separate untried route, not a solved escape.

## Authenticated primary sources read in this partial attempt

* [Ellis,Nanopoulos,Olive,Verner1903.05267v2](https://arxiv.org/pdf/1903.05267),
  displayed version21November2019: Eq1 is the SUGRA potential; Eq2 gives
  the logarithmic Kähler potential with real/imaginary quartic modulus
  stabilization. The discussion around Eq8 and the modulus masses on
  printedp3 gives their source-specific assumptions. It motivates the
  quartic mechanism, not a proof for the proposed n<3 SU5 embedding.
  The paper explicitly discusses parameter tuning of vacuum contributions;
  it does not derive the observed dark-energy hierarchy.
* [D'Eramo,Thaler,Thomas1202.1280v3](https://arxiv.org/pdf/1202.1280),
  displayed version12June2012: Eqs3.11–3.15 distinguish full anomaly-mediated
  gaugino mass, Kähler/current contributions and the gravitino term;
  Eq4.22 explains why a SUGRA Goldstino coupling need not equal the total
  gaugino mass divided by the flat-space F. This source was authenticated
  and shared as the next matching input. Its formula has not yet been
  applied to a solved protected stationary point or decoupled thresholds.

No external full source was downloaded or copied into this directory.

## Smallest remaining implication and continuation order

1. Freeze a numerical contract before running. Independently verify the
   exact inverse-metric potential, including the complex modulus/matter
   directions and the n=3 limit.
2. Solve the proposed finite-order potential for X,a,b,Re tau and W0,
   including the actual rigid finite-CW lift with its declared gravity/loop
   accuracy. Check all stationarity residuals, K-positive domain and the
   real/imaginary neutral Hessian with physical kinetic normalization.
   Report tuning to a target net V as tuning, not a predicted residual.
3. Check nonaligned transverse matter/gauge stability and the EFT cutoff.
   Then compute eaten/orthogonal neutral fermions, photino mixing and
   anomaly/heavy-threshold corrections. Reconstruct every open decay channel
   before importing the TP04 lifetime or production window.
4. Ask whether any protected relation fixes the tiny residual rather than
   retuning W0 after each loop/order. No such relation was found here.
   The strong raw-source dark-energy link remains obstructed; the proposed
   construction at most targets the weaker tuned net-V link.

Stop status: **incomplete, with an explicit unexecuted K,W proposal and
hand-derived algebra; no numerical evidence, completed model or new
physical viability claim.**
