# One aether function: common action, different invariant branches

2026-10-20. Base `431f22bd6`; criteria-only `89bf113b0`.
Analytic P3 packet, with no script, scan, download, build or Lean run.
Exact primary definitions and versions are in `SOURCES_FUNCTION.md`.

**Verdict.** This common-function construction supplies a positive
homogeneous vacuum and a strictly healthy linear clock/gravity sector
on an open de Sitter branch. It does not supply a healthy microscopic
selector or a same-state exact MOND cubic. A regular de Sitter branch
has a finite linear weak-source susceptibility. Its flat-static MOND
function samples a different invariant branch in the healthy class
analyzed below; a smooth deformation can leave that entire branch and
its UV offset fixed while moving the cosmological vacuum. The critical
endpoint is separate and remains open. No value of the requested
physical R is selected or evaluated by mixing these states.

## 1. Exact action and overlap boundary

Take signature `(-+++)`, `B=M_Pl^2>0`, a mass m>0, universal metric matter
`S_m[g]`, and a foliation clock T with

    u_mu=-partial_mu T/sqrt(-g^{rho sigma}partial_rho T partial_sigma T),
    gamma_mu nu=g_mu nu+u_mu u_nu,
    K_mu nu=gamma_mu^rho nabla_rho u_nu,
    K=K_mu^mu,       a_mu=u^rho nabla_rho u_mu.

The clock is assumed timelike. This is the hypersurface-orthogonal
subclass, not an independent vector with additional transverse modes.
Choose the luminal-tensor coefficients `c3=-c1`, `c4=0`. The generalized
aether invariant is then

    I=m^(-2)[c1 nabla_mu u_nu nabla^mu u^nu
              +c2(nabla_mu u^mu)^2
              +c3 nabla_mu u_nu nabla^nu u^mu]
     =(c2 K^2-c1 a_mu a^mu)/m^2,

because `nabla_mu u_nu=K_mu nu-u_mu a_nu`. The action, including the
usual Einstein boundary prescription, is

    S=(B/2) integral sqrt(-g)[R+m^2 F(I)]+S_m[g]
     =(B/2) integral N sqrt(gamma)
        [R3+KijKij-K^2+m^2F((c2K^2-c1a_i a^i)/m^2)]+S_m.

All c_i and F are dimensionless; `[m]=1`. No exact symmetry selecting
F, c1 or c2 is assumed. The primary general-aether action and the
khronometric restriction are authenticated; this particular coefficient
subclass and the constrained reductions below are explicit choices
and calculations, not a source-proved microscopic completion.

The prior `sol61_push/CANONICAL_CLOCK_RESULTS.md` and
`VARIABLE_CLOCK_MODES_RESULTS.md` already derive the preferred-clock
scalar constraints and de Sitter boundedness for their distinct
polarization/order-parameter actions. W4-08 `gravity_constraints`
already treats pure BM `f(a)` and `geometric_source` the c1 rational
model. Those mode calculations are inherited context, not new trials.
The new object here is the single F depending simultaneously on trace
expansion and acceleration, with its exact background-dependent Hessian,
source limit and opposite-argument deformation. The old UV moment sum
rule and vacuum-offset counterfamilies are not rerun.

## 2. Derive the flat-static constitutive law and physical source

Set the clock along a stationary rest foliation, so Kij=0, and use

    N=1+Phi,    gamma_ij=(1-2Psi)delta_ij,    h=|grad Phi|.

This is the leading weak-static metric expansion. At this order
`I=-c1 h^2/m^2`. With c1<0 it samples I>=0. Up to spatial boundaries,
the Einstein spatial action is

    (B/2)[2|grad Psi|^2-4 grad Phi dot grad Psi].

The matter lapse variation is `-rho Phi`. Varying Psi, with the harmonic
boundary mode fixed, gives `Delta(Psi-Phi)=0`, hence Psi=Phi. The
resulting sourced static Lagrangian and energy are

    L_static=-E_flat(h)-rho Phi,
    E_flat(h)=B h^2-(Bm^2/2)F(-c1h^2/m^2),
    div[mu(h) grad Phi]=rho/(2B),
    mu(h)=E_h/(2Bh)=1+(c1/2)F'(I).

This is a physical metric source, not an assigned electric or scalar
charge. A slow test body has acceleration `-grad Phi`. If F'(+infinity)
tends to zero and the aether correction is subleading in that force
regime, then the local high-acceleration Newton coefficient is

    G_UV=G_bare=1/(8pi B),       C2_flat=B.

The word UV denotes the actual high-acceleration force limit; it is not
the small-amplitude high-frequency limit of a cosmological perturbation.
The flat-static approximation itself requires weak potentials and
negligible cosmological/extrinsic-curvature corrections. A nonzero F(0)
does not make Minkowski an exact vacuum. It must not be combined with a
different background without checking that approximation.

Demanding a positive deep-MOND constitutive law `mu(h)=h/a+o(h)`, a>0,
requires

    F'(0+)=-2/c1,
    F(I)=F0-2I/c1-[4m/(3a(-c1)^(3/2))]I^(3/2)+o(I^(3/2)),
    E_flat(h)=-(Bm^2/2)F0+2B h^3/(3a)+o(h^3),
    C3_flat=2B/(3a)>0.

Where differentiated asymptotics are justified, `F''` has a negative
`I^(-1/2)` divergence. This cusp, rather than a regular Taylor coefficient,
is essential. A spherical source obeys
`r^2 mu(h)h=G_UV M_source`, so this formal deep branch gives
`h=sqrt(G_UV M_source a)/r`. These statements derive the source and
coefficient of the flat-static branch; they do not yet prove that branch
is realized on the positive cosmological vacuum.

## 3. The same F in the homogeneous vacuum

For flat FRW, `u=partial_t`, `K=3H`, a_i=0 and

    I0=9c2 H^2/m^2.

Vary the lapse before setting it to one. In vacuum the exact constraint is

    3H^2=(m^2/2)[2I0 F'(I0)-F(I0)].

The metric aether stress, restoring the B factor, has homogeneous
density and pressure

    epsilon_A=(Bm^2/2)(2I F'-F),
    p_A=-epsilon_A-3B c2[F'+2IF''] Hdot.

At a constant-H positive root it has `p_A=-epsilon_A` and
`epsilon_A=3B H^2>0`. This is the total varied aether stress on that
state, not `-Bm^2F0/2` and not a finite-density pressure relabeled as
vacuum energy. Preferred foliation remains present even though this
background stress is isotropic and of vacuum form.

For later use set all derivatives at I0 and define

    Q=F'+2I0 F'',
    lambda_eff=1-c2 Q,       alpha_eff=-c1 F',
    S=3lambda_eff-1.

Adding a small homogeneous matter density and differentiating the
constraint yields

    partial[3H^2-(m^2/2)(2IF'-F)]/partial(H^2)=(3/2)S,
    G_cos=response coefficient=2G_bare/S.

This is a homogeneous response at that background. It is not the local
Newton coefficient G_UV or the small-source Newton coefficient below.
These are separate variations of the same action and need not coincide.

## 4. Raw de Sitter quadratic from F, before constraints

Assume F has the needed finite derivatives near I0, H>0, and write
`a_dS=exp(Ht)`. Unitary clock gauge T=t leaves the scalar in the metric;
it does not remove the physical scalar mode. Use spatial scalar gauge

    N=1+n, gamma_ij=a_dS^2 exp(2zeta)delta_ij,
    N_i=partial_i chi,   b=a_dS^(-2)Delta chi,
    U=zetadot-Hn,        X=k_com^2/a_dS^2>0.

Here `delta K=3U-b`. A compact way to retain all F-induced terms is

    KijKij-K^2+m^2F(c2K^2/m^2)=sigma_ij sigma^ij+G(K),
    G(K)=-2K^2/3+m^2F(c2K^2/m^2),
    G(K0)-K0 G_K(K0)=0,       K0=3H,
    G_KK(K0)=-4/3+2c2 Q.

The constant `G_K(K0) integral N sqrt(gamma) K` is exactly a temporal
and spatial boundary: `N sqrt(gamma)K=partial_t sqrt(gamma)
-partial_i(sqrt(gamma)N^i)`. Drop it with fixed endpoint data and
vanishing/controlled spatial boundary flux. The remaining quadratic
trace term is `G_KK(delta K)^2/2`; the acceleration term contributes
`alpha_eff |grad n|^2`. This also explains why replacing F' by a fixed
constant before differentiating misses the `2I0 F''` term.

With `lambda=lambda_eff`, `alpha=alpha_eff` for brevity, the exact
quadratic scalar bracket, normalized by `B a_dS^3/2`, is

    -3S U^2+2S U b+(1-lambda)b^2
                    +X(2zeta^2+4n zeta+alpha n^2).

The first line includes the shift. No scalar field or clock fluctuation
has been discarded by an additional equation; the lapse and shift are
nondynamical constraints at this order. Spatial integrations use a
nonzero Fourier mode or equivalent vanishing boundary data. The two
transverse-traceless tensor modes have their GR action

    S_T2=(B/8) integral a_dS^3[gamma_TTdot^2-X gamma_TT^2].

There is no independent transverse aether mode in the chosen
hypersurface-orthogonal theory. This is not a health result for the
unrestricted vector theory.

## 5. Eliminate shift and lapse, keeping redshift boundaries

For lambda>1 define

    C=2S/(lambda-1)>0,       D=C H^2+alpha X.

The shift equation and the lapse equation after that substitution give

    b=S U/(lambda-1),
    L_after_shift/(B a_dS^3/2)
      =C(zetadot-Hn)^2+X(2zeta^2+4n zeta+alpha n^2),
    n=(CH zetadot-2X zeta)/D.

The lapse is regular for alpha>0. Substitution produces a mixed term
`4CHX zeta zetadot/D`. Its temporal boundary is

    d[a_dS^3(2CHX/D)zeta^2]/dt,
    a_dS^(-3)d[a_dS^3(2CHX/D)]/dt
      =2CH^2X(CH^2+3alpha X)/D^2,

using `Xdot=-2HX`. Treating X as constant here would give the wrong
curvature restoring term. After this boundary subtraction,

    S_scalar2=(B/2) integral a_dS^3[K_z zetadot^2-V_z zeta^2],
    K_z=C alpha X/D,
    V_z=2X^2[C(alpha+2)H^2+alpha(2-alpha)X]/D^2.

For the strict open interval `lambda>1`, `0<alpha<2`, both coefficients
are positive for every finite k_com!=0. The scalar is retained and its
kinetic coefficient is positive. Its principal short-wavelength speed is

    c_s^2=2(2-alpha)/(C alpha)
         =(lambda-1)(2-alpha)/[alpha(3lambda-1)]>0.

The exact time-dependent equation has friction
`3H+K_zdot/K_z=H+2alpha HX/D>0` and restoring frequency

    Omega^2=V_z/K_z
      =2X[C(alpha+2)H^2+alpha(2-alpha)X]/(C alpha D)>0.

For each fixed initial finite k, the coefficients approach friction H
and zero restoring with errors O(exp(-2Ht)). The first-order system for
`(zeta,zetadot)` is therefore an integrable perturbation of a constant
system with eigenvalues 0 and -H and bounded propagator. Variation of
constants and Gronwall give future boundedness. This is a fixed-mode
linear de Sitter statement, not a uniform high-k bound, nonlinear
stability, quantum vacuum or cutoff/strong-coupling theorem.

Strict k=0 has no shift-divergence variable to divide by. Its homogeneous
lapse equation sets U=0 when S and H are nonzero; it does not furnish
the finite-k scalar kinetic limit. The regular cosmological root fixes H,
and homogeneous slicing/scale-coordinate variations must be treated with
their residual gauge and boundary data. No all-vacuum regularity is
inferred from `K_z ->0` as k approaches zero.

## 6. What the actual weak source sees on this state

Assume the strict healthy interval above and an EFT window
`c_s k_physical >> H`, below its actual cutoff. Take source amplitude
to zero at fixed such spatial scale. In that limit nonlinear F terms
are perturbative around I0, not around the flat-static argument zero.
Leading quasistatic spatial metric variation gives Psi=Phi; the lapse
constraint gives

    Delta Phi=rho/[B(2-alpha_eff)]
                +controlled subcurvature/time-derivative corrections,
    G_bg=G_bare/(1-alpha_eff/2).

Corrections are suppressed in the usual slow-source, subcurvature
expansion with `H/(c_s k_physical)` small. This is an operational
small-amplitude linear Newton response on the same de Sitter state.
It is inconsistent with an exact leading positive local cubic, which
would instead produce a square-root dependence on source amplitude.
The existence of this scale window is an extra EFT validity condition;
it is not proved by a positive quadratic action alone.

At a local fixed-expansion jet the acceleration shifts the invariant as
`I=I0-c1h^2/m^2`. A twice continuously differentiable F at I0 has a
regular expansion in h^2, not h^3. More generally a regular local
elimination with an invertible stationary Hessian preserves that
regularity. This local observation is not a theorem replacing the full
nonlinear metric/clock boundary problem: the actual K and shift must be
solved, and nonlocal or degenerate reductions are outside it. The weak
source calculation above supplies the controlled actual-response test.

### Critical endpoints remain separate

At alpha=2 with lambda>1 the de Sitter coefficients still satisfy
`K_z>0,V_z>0` for finite k,H, but the principal k^2 sound speed vanishes.
One must not use the weak-source formula by dividing by `2-alpha`.
This endpoint requires its full constrained nonlinear source, interaction
and quantum/cutoff calculation; curvature positivity alone is not a
proof of the desired MOND response. At lambda=1 the shift equation
instead sets U=0 and the reduced action is proportional to
`alpha X zetadot^2/H^2`, with zero restoring. It is the separate
pure-BM-type corner, not a limit justified by dividing by lambda-1.

Installing a new cusp `|I-I0|^(3/2)` at a nonzero cosmological I0 is also
not a regular cure. Its first variation includes

    delta I=(6c2 H/m^2)delta K,

so it gives a nonquadratic `|delta K|^(3/2)` term and no finite expansion
Hessian in that direction. A constraint might change the mode count or
eliminate that direction, but this must be derived; it is not automatic
health and the regular quadratic formulae above then do not apply.
The c2=0 or H=0 exceptions remove this particular linear variation;
they are different limits, not a positive-expansion solution of it.

## 7. Opposite-branch freedom without changing the flat-static UV offset

For c1<0, F'>0 and Q>0 at the de Sitter root, the strict lambda>1
condition requires c2<0. Thus `I0<0`, whereas the entire aligned
flat-static law samples I>=0. This sign separation is conditional on
this healthy subfamily; other nonlinear branches are not classified.

Define one global deformation with a dimensionless coefficient eta:

    F_eta(I)=F(I)+eta g(I),
    g(I)=I exp(-1/I^2) for I<0,       g(I)=0 for I>=0.

The function g is smooth and flat at zero and real analytic on each
open branch. It leaves every positive-I value/derivative, F0 and the
entire positive-I UV normalization and offset exactly unchanged. It
does not worsen the required MOND cusp at zero. On I<0,

    2I g'-g=(I+4/I)exp(-1/I^2),
    d(H^2)/deta=m^2(2I0 g'(I0)-g(I0))/(3S) !=0.

The derivative follows by implicit differentiation of the actual
Friedmann constraint. S>0 makes the root simple. For sufficiently small
eta, H^2>0 and the strict local conditions on F', Q, lambda and alpha
remain true by continuity. Thus the cosmological vacuum can move without
altering any flat-static positive-I operator. This is functional freedom
inside the same one-function covariant class, not an additive constant
shift or the already studied UV moment argument.

The deformation is permitted by diffeomorphism covariance, clock
reparameterization and the stated real differentiability. A separately
proved microscopic analyticity/dispersion/duality relation could exclude
it. Such a principle is not provided by the common F ansatz; global real
analyticity at zero is already incompatible with the required exact
I^(3/2) static cusp. No claim is made about every possible microscopic
analytic continuation across a physical branch cut.

This is **not** a counterfamily of established healthy same-state MOND
halos. The strict de Sitter branch has the linear response in section 6,
and a full finite-gradient bridge is unproved. It demonstrates why
assigning one symbol F to the two sectors is not a selecting equation.

## 8. Explicit common-function toy, without a target input

Set `c1=c2=-1`, `c3=1`, `c4=0`, and take the fixed dimensionless function

    F(I)=-4/(1+sqrt(I))+2/(1+sqrt(I))^2,                I>=0,
    F(I)=-2+2I+5I^2+(17/3)I^3+2I^4,                  I<0.

It is C1 at zero, with the intended non-C2 MOND cusp. On I>=0,

    F'(I)=2/(1+sqrt(I))^3,
    F(I)=-2+2I-4I^(3/2)+O(I^2),       F(+infinity)=0,
    mu(h)=1-(1+h/m)^(-3),
    a_flat=m/3,      C2_flat=B,       C3_flat=2B/m.

All coefficients are stated independently of the target; this is an
explicit algebraic example, not a scan or a microscopic selection claim.
The negative branch has at I0=-1

    F=-8/3,    F'=1,    F''=0,
    H=m/3,    epsilon_A=Bm^2/3>0,
    lambda_eff=2,    alpha_eff=1,    C=10,    c_s^2=1/5.

It therefore realizes the strict linear de Sitter tensor/scalar health
conditions just derived. On this actual state the three couplings are

    G_UV=G_bare,       G_cos=(2/5)G_bare,       G_bg=2G_bare.

The zero-argument constant would instead give `-Bm^2 F0/2=Bm^2`;
it is not the actual de Sitter energy `Bm^2/3`. Weak sources on the
actual state have linear response, not the flat-static cubic law.
The different finite-gradient regime, crossing I=0, retained constraint
health, cutoff and quantum completion are all unproved. In particular
the example is not a globally healthy MOND model and supplies no
operational same-state R to compare with 128pi/9.

## 9. Strongest surviving construction and missing microscopic equation

This route does improve on assigning independent vacuum and force
actions: one explicit covariant F gives their background and local
quadratic equations, with actual metric matter and distinguishable
Newton/cosmological responses. A regular positive root can have healthy
retained linear clock and tensor modes, as the toy verifies.

The exact same-state infrared MOND response is the next bottleneck, and
the functional shape/branch relation is independently unselected. A
microscopic principle would need to fix that relation, remove the
allowed branch deformation, retain regular constrained dynamics through
the critical response, and supply a physical UV quantum state. Neither
general covariance, clock reparameterization, a shared mass m nor
linear de Sitter health does this. No universal aether/gravity no-go,
full halo theorem, microscopic completion or target selection follows.
