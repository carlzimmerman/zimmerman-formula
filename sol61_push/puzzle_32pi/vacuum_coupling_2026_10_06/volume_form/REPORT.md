# Volume constraints: a boundary number and a mandatory scale reaction

Checkpoint 2026-10-06; supplied and observed entry HEAD
`310f0d1a46ca858e9a63cf37f699f10baa07ad3d`. Writes confined here.
**No vacuum coupling or 32pi selector is obtained.** Beyond the familiar
constant multiplier, this route derives two new discriminators: varying the
proposed acceleration-linked volume adds an Euler reaction that cannot be
omitted, and a local density-following multiplier either violates separate
matter conservation or changes the source sector's pressure/evolution.

## 1. Actual actions and the full stress trace in general dimension

Use signature (-,+,...,+), c=1, spacetime dimension d>2, and positive Einstein
coefficient K. A fixed-density multiplier action is

    S=integral d^d x {sqrt(-g)[K R/2+L_m]-lambda(x)[sqrt(-g)-epsilon_0]}.

Here epsilon_0 is a fixed positive coordinate density, not a new metric-dependent
matter weight. Its variation is not allowed. Include the usual gravitational
boundary term and fixed induced metric where there is a boundary. The equations
are

    sqrt(-g)=epsilon_0,
    K G_mu nu=T_mu nu-lambda g_mu nu.

For separately covariant matter minimally coupled to this metric, matter's
own on-shell identity gives nabla^mu T_mu nu=0. The Bianchi identity therefore
requires partial_nu lambda=0. The fixed measure does not itself weaken matter
conservation. Writing the metric equation in traceless form gives

    R_mu nu-R g_mu nu/d=(T_mu nu-T g_mu nu/d)/K,
    lambda=[(d-2)K R/2+T]/d.

Divergence of the traceless equation makes the last combination constant. It
contains the **full** stress trace: for a perfect fluid T=-rho+(d-1)p, and for
a pure constant vacuum T=-d rho_v. A dust trace must not be replaced by the
vacuum trace. In vacuum,

    Lambda_geom=(lambda+rho_v)/K,
    R=2d Lambda_geom/(d-2).

Thus the absence of vacuum from the traceless equation does not mean its
curvature coupling is 1/d or G per angular channel. Changing a constant
rho_v by delta rho_v while changing lambda by -delta rho_v preserves the same
metric. It requires a different multiplier/boundary value; it predicts no
particular preserved curvature.

A covariant local volume form replaces the fixed density by a vector density
B^mu or locally defined (d-1)-form:

    S_HT=integral {sqrt(-g)[K R/2+L_m-lambda]+lambda partial_mu B^mu}.

Varying lambda and B gives partial_mu B^mu=sqrt(-g) and partial_mu lambda=0.
For a finite domain, integral sqrt(-g)=integral_boundary B. Boundary conditions
must state whether B's flux or the conjugate lambda is fixed; an appropriate
boundary term changes that ensemble. On a closed compact domain, a globally
single-valued exact (d-1)-form cannot have nonzero total volume flux by Stokes.
Nonzero flux needs topology/patchwise form data, or a boundary; it cannot be
silently represented by one global exact potential.

There is no propagating lambda mode whose retarded Green function selects its
constant. In an initial-value problem, lambda is part of initial/boundary data
and B's later integrated value counts the accumulated volume. Fixing both a
future flux and initial data is a boundary-value restriction, not a retarded
local response. This distinction matters when a proposed volume condition
uses the whole future universe.

## 2. Measured gravity fixes the angular normalization

For d>3, define Newton G_N operationally by the force between nonrelativistic
masses g_N=G_N M/r^(d-2). Linearizing the same Einstein equation around flat
space gives

    Laplace Phi=(d-3)rho/[(d-2)K]
               =Omega_(d-2) G_N rho,
    K=(d-3)/[(d-2)Omega_(d-2)G_N].

Omega_(d-2) is the unit-sphere area. In d=4, K=1/(8piG_N). The vacuum equation
then is

    Lambda_geom=[(d-2)Omega_(d-2)/(d-3)]G_N(lambda+rho_v),
    H^2=2Omega_(d-2)G_N(lambda+rho_v)/[(d-1)(d-3)].

The same Gauss normalization that calibrates matter introduces the solid
angle; a volume multiplier does not divide it away. d=3 lacks the ordinary
mass Newton force used for this calibration, and d=2 is excluded. If additional
scalar/vector forces alter a laboratory measurement, they must be included
rather than relabeling K as the measured total force constant.

For a concrete same-action acceleration parameter, append a classical scalar
P(X) with deep spacelike branch -C(-X)^(3/2), and massive baryon worldlines
-m exp(alpha phi) ds, alpha>0. Its local source and force give

    gamma=3C/(2sqrt2),
    r^(d-2) gamma (phi')^2=alpha M/Omega_(d-2),
    g_phi=alpha phi',
    a0=alpha^3/[Omega_(d-2)gamma G_N].

That expression uses the Einstein-sector Newton coefficient; it must be
converted before comparing with a physical force calibration. Supply an
explicit static continuation P_X=Z gamma u/(Z+gamma u), Z>0, u=sqrt(-2X).
It has the same cubic deep limit and P_X tends to Z at large gradient. Its
real spacelike primitive is

    P=-Z[u^2/2-(Z/gamma)u+(Z/gamma)^2 log(1+gamma u/Z)].

Then high-gradient force calibration gives
G_phys=G_N+alpha^2/[Omega_(d-2)Z], while the operational deep scale is
a0_phys=alpha^3/[Omega_(d-2)gamma G_phys]. The vacuum curvature continues
to use K, hence the Einstein G_N, not an automatically substituted G_phys.
In d=4 these are G_phys=1/(8piK)+alpha^2/(4piZ) and the actual scalar
MOND scale alpha^3/(4pi gamma G_phys). Once G_phys is measured, K,alpha,Z
still need a tensor/source dictionary; the extra coupling does not derive a
solid-angle division. In the volume formulas below a0 denotes this operational
a0_phys. This is an explicitly declared extra matter coupling and kinetic
branch, not the full P2 law or a verified post-Newtonian theory. It breaks the
scalar's total shift symmetry.
For the compact vacuum control below, baryon worldlines are absent and the
vacuum energy U is a separate phi-independent action term; phi is constant.
A universally conformal quantum matter vacuum would source phi and is **not**
assumed to disappear. No global healthy completion is asserted for this cubic
scalar; its vacuum is kinetically degenerate and its static longitudinal mode
is superluminal. The purpose is an operational, independently specified a0
inside the same declared action, not a new successful scalar model.

## 3. A genuine volume variation fixes curvature after a boundary choice

A rigid global multiplier imposing a proper volume V_0 has the Euclidean action

    I=-K integral R vol_g/2 + U integral vol_g
      +lambda(integral vol_g-V_0).

On the closed constant-scalar round S^d branch this is a boundary-free saddle
problem. The scalar static-gradient sector vanishes there; its real Euclidean
static continuation at constant phi adds no stress or scalar source. This is
a classical saddle calculation, not a well-defined quantum path integral or
a positive fluctuation determinant. A preferred time-like foliation action
cannot automatically be imported to this compact sphere; it is not used here.

Variation gives V=V_0 and Lambda_geom=(U+lambda)/K. For a round sphere of radius
L,

    V=Omega_d L^d,
    Lambda_geom=(d-1)(d-2)/(2L^2),
    Lambda_geom=[(d-1)(d-2)/2](Omega_d/V_0)^(2/d).

Here Omega_d=2pi^((d+1)/2)/Gamma((d+1)/2) is the unit S^d volume, not the
Newton flux sphere Omega_(d-2). This is a real variational selection of
curvature **given V_0**. A change of constant U is compensated by lambda;
the geometric result depends on V_0, not on its vacuum origin.
The independent source-normalized a0 remains a coupling parameter, so

    C=Lambda_geom/a0^2
     =[(d-1)(d-2)/2][Omega_d/(V_0 a0^d)]^(2/d).

In d=4 the proposed C=32pi is equivalent to

    V_0 a0^4=3/128.

This exact rational volume number is a useful alternate boundary target,
not its derivation. Every positive dimensionless V_0 a0^d gives a different
positive C. Holding V_0 fixed gives d ln C/d ln a0=-2 and
holding a0 fixed gives d ln C/d ln V_0=-2/d.

Lorentzian volume requires a specified domain. For a flat FRW de Sitter patch
with fixed initial spatial volume V_c and proper duration T,

    V=V_c [exp((d-1)HT)-1]/[(d-1)H].

It increases strictly with H at fixed positive T, so V_0 can determine H once
V_c,T and compatible boundary conditions are supplied. It does not give the
round Euclidean sphere's invariant volume. Fixing both endpoint induced
metrics already fixes de Sitter expansion; the volume becomes a consistency
condition. Leaving an endpoint free requires its own boundary variation, not
an assumed one-parameter family. Changing duration, spatial cell or future
flux changes the constraint. No causal universal a0 follows from this patch.

## 4. Promoting a0 to a varied scale adds the missing Euler reaction

Attempt a stronger construction: let the action's operational MOND scale be
a rigid positive variable chi, enforce V_0=v_star chi^(-d), and vary chi too.
The cubic source coefficient gamma now depends on chi so that its static
a0=chi. On the constant-scalar vacuum branch that gradient dependence has
zero first variation, but a vacuum potential U(chi) and the volume term remain:

    I=-K integral R vol_g/2 + U(chi)V
      +lambda[V-v_star chi^(-d)].

Scale variation and the volume constraint give

    U'(chi)V+d lambda v_star chi^(-d-1)=0,
    lambda=-chi U'(chi)/d,
    Lambda_geom=[U(chi)-chi U'(chi)/d]/K.                 (1)

This is a mandatory same-action reaction. Keeping lambda arbitrary after
varying chi drops an equation. If U=0, lambda=0 and there is no positive
compact de Sitter saddle. The volume term alone cannot generate the vacuum.
If U is constant and positive, lambda=0; chi is determined by that chosen
vacuum height plus v_star, so the numerical ratio is still chosen by v_star.
A varying constant vacuum height changes the operational acceleration scale;
this is a different theory from fixing a0 while its multiplier compensates.

For U=K u chi^2,

    Lambda_geom/chi^2=u(1-2/d).

The volume equation requires that number equal
[(d-1)(d-2)/2](Omega_d/v_star)^(2/d). Scale cancels: compatibility imposes a
relation between chosen u and v_star, while chi is undetermined on this scale
family. In d=4 obtaining 32pi requires u=64pi and v_star=3/128, explicit inputs.
A degree-d homogeneous potential U proportional to chi^d gives zero residual
in (1), so the naive scale-homogeneous repair also supplies no positive sphere.
For a general potential, roots depend on its full shape and boundary data;
there is no universal impossibility theorem for an independently derived
microscopic potential. Equation (1) identifies the new implication it must
satisfy before any vacuum selector is claimed.

## 5. Local density-following rules: conservation versus source reaction

Suppose one imposes the Einstein-form equation

    K G_mu nu=T_mu nu-F(rho)g_mu nu.

If T is separately conserved, Bianchi gives F'(rho)partial_nu rho=0. Wherever
rho explores a nonconstant interval, F must be constant there. For arbitrary
inhomogeneous or expanding sources this excludes a nontrivial local scalar
response F(rho) within these premises. A pure **constant** vacuum is an escape:
its density has no gradient, and F at that one density is just a freely chosen
constant. This statement does not forbid a selective vacuum mechanism in a
larger theory with extra fields, boundary data or matter exchange.

If separate conservation is abandoned, the phenomenological closure instead
requires nabla T=partial F. For a barotropic homogeneous fluid in d=4,

    [1+F'(rho)]rho_dot+3H(rho+p)=0,
    rho_eff=rho+F(rho), p_eff=p-F(rho),
    c_eff^2=[p'(rho)-F'(rho)]/[1+F'(rho)].

This is an algebraic perfect-fluid exchange closure, **not** conserved
constant-mass cold particles. For dust and F'=kappa-1 constant,

    rho proportional a^(-3/kappa), c_eff^2=(1-kappa)/kappa.

Positive susceptibility and causal nonnegative sound speed in this closure
require 1/2<=kappa<=1. If one applies the putative vacuum replacement
Lambda_geom=G_N rho rather than 8piG_N rho to this evolving dust density,
kappa=1/(8pi) gives c_eff^2=8pi-1≈24.13 and dilution exponent 24pi≈75.40.
This is a sharp observable failure of that all-density prescription. It is
not a refutation of constant vacuum-only correction. For a varying isolated
vacuum p=-rho, conservation gives kappa rho_dot=0: any nonzero residual
fraction requires constant density unless another sector exchanges energy.
With dust plus a varying vacuum and F=F(rho_v), the required transfer is
rho_d_dot+3Hrho_d=-(1+F')rho_v_dot, a direct additional observable.

A simple actual action does not reproduce the imposed closure by substitution.
For a conserved particle current with energy epsilon(n)=rho(n)+F(rho(n)),
metric/fluid variation gives

    p_eff=p+F'(rho)(rho+p)-F(rho),

including the reaction term F'(rho)(rho+p). For constant-mass dust rho=mn
and F=c rho, epsilon=(1+c)mn and p_eff=0: the change rescales inertial and
gravitating particle mass, rather than adding vacuum pressure -F. Calibrating
physical masses removes that common rescaling from a force measurement.
Implementing a genuine vacuum-like F(rho) stress needs another constrained or
exchanging sector and its own variation; inserting the density-dependent
multiplier after metric variation silently misses this reaction.

## Literature, overlap and bounded evidence

Primary sources checked directly: Buchmueller and Dragon,
[The cosmological constant as a boundary term](https://arxiv.org/pdf/2203.15714),
v3, section 2 equations 4-10, explicitly gives the three-form equations and
the boundary volume interpretation. Fiol and Garriga,
[Semiclassical Unimodular Gravity](https://arxiv.org/pdf/0809.1371), v3, discusses
fixed-volume semiclassical sectors; our compact and scale variations are
independent calculations, not claims extracted from that work. The historical
Henneaux-Teitelboim publisher abstract was located; the exact conventions were
verified in the primary 2022 action rather than inferred from that abstract.
No quantum-equivalence, path-integral stability or graviton-loop result is used.

Project comparison includes the previous sequestering/scalar reports and the
Sonnet puzzle four-form summary. They already identify constant residual data.
This checkpoint adds the general-d operational source calibration, the genuine
proper-volume boundary target, the varied-scale Euler reaction, and the local
tracking conservation/fluid-action discriminator. Novelty is bounded to those
inspected project records.

`checks.py` and `contract.json` specify 17 exact/local assertions. Fresh
`runs/main_a/` passes; `runs/ignore_scale_a/` is an expected failed mutation
retaining an arbitrary multiplier after scale variation. Version-2 manifests
record actual hashes, HEAD, logs and caps and validate against unchanged
inputs. CPU20s/process, wall30s, 1MiB logs, cooperative one-thread libraries;
no memory/affinity cap. The formulas and proofs above carry the claims; the
finite controls do not establish a global healthy theory.

The next missing implication is a physically derived boundary volume/scale
potential and its consistent local matter reaction. A chosen V_0 a0^d or
F(rho_v) value merely rewrites the target. A candidate must vary its scale,
retain the measured source normalization and distinguish constant vacuum
stress from evolving dust before being evaluated as a selector.
