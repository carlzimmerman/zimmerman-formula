# Goldstone protection: exact Ward identities and the wrong response

2026-10-20. Base b37b50b1c; criteria-only commit1d58a0851. This is P1
of `FROZEN_CRITERIA.md`. The original healthy microscopic xi=1/4 goal
remains open. No target, measured scale or chosen protected coefficient
is an action input. No new script, build, scan, download or Lean was used.
Primary versions and precise attribution limits are in `SOURCES_GOLDSTONE.md`.

## 1. The inherited action has no protecting internal shift

The inherited gravitational order parameter has

    L_chi=-Z^2(partial chi)^2/2-E(h,chi)-U(chi),
    E=M^2 h^2[f1(chi)+h^2 f2(chi)/(9a0^2)],
    f1=1/(1+chi^2), f2=chi^2, h=|grad Phi|,
    U_eta=epsilon+eta chi^6/(1+chi^2)^6.

Here the physical metric, fixed coefficients and arbitrary massive
matter source are held fixed. For an internal point generator
delta chi=epsilon_s Q(chi), variation of the canonical kinetic term
contains -Z^2 Q'(chi)(partial chi)^2. In this action no other retained
term can cancel that independent derivative structure. Thus Q'=0.
Independent h^2 and h^4 backgrounds then require

    Q f1'=0, Q f2'=0.

Since f1 and f2 are nonconstant, Q=0 is the only continuous generator.
The finite point isometries of the canonical line are chi->+/-chi+c;
preserving chi^2 sets c=0 and leaves only the reflection. It permits U_eta.
Rescaling a coupling or redefining the field is not an additional symmetry
of the fixed physical action. Transformations that move the metric, fluid
or matter sector are outside this internal-point classification and must
be checked on their full action rather than inferred from it.

The explicit broken-shift equation makes the failed Ward identity visible:

    J^mu=-Z^2 partial^mu chi,
    nabla_mu J^mu=-E_chi-U_chi on the chi equation,
    E_chi=2M^2 chi h^2[-1/(1+chi^2)^2+h^2/(9a0^2)],
    (U_eta)_chi=6eta chi^5(1-chi^2)/(1+chi^2)^7.

An exact shift would indeed forbid the nonconstant potential, but its
breaking insertion E_chi is already present before adding eta. Removing
all chi-dependent coefficients restores the shift and removes this
order-parameter mechanism for the algebraic MOND cubic. Small or
spurion-controlled breaking is not an exact Ward identity excluding eta.
No assertion that a particular loop necessarily generates eta is needed.

## 2. A genuine nonlinear DBI Ward identity

Take a position Goldstone pi for a codimension-one brane in flat five-space,
with induced metric gamma_mu_nu=eta_mu_nu+partial_mu pi partial_nu pi.
Pi has dimension length and X=(partial pi)^2 is dimensionless. The exact
broken-boost transformation of de Rham--Tolley Eq(2) is

    delta_b pi=b.x+pi b.partial pi.

It induces a field-dependent diffeomorphism of gamma with xi^mu=b^mu pi.
For a first-derivative scalar density P(X), direct variation gives

    delta_b P=partial_mu(pi b^mu P)
              +[2(1+X)P_X-P] b.partial pi.

The last term is a boundary for all pi if its bracket is a constant K.
Conversely, the Euler derivative of Q(X)b.partial pi, tested on independent
first/second-derivative jets, forces Q'=0. Hence within this
Lorentz-invariant first-derivative class

    2(1+X)P_X-P=K,
    P(X)=A sqrt(1+X)-K=-T sqrt(1+X)+B.

T>0 gives a positive canonical vacuum kinetic term, pi_c=sqrt(T)pi.
The scalar Ward identity fixes the square-root shape, while the constant
B is also invariant. It does not fix the value of P(0). A covariant
gravitating vacuum requires its specified metric/bulk sector; a flat-space
constant must not automatically be called an observed vacuum density.

For a static spacelike gradient h_pi=|grad pi|,

    E(h_pi)-E(0)=T[sqrt(1+h_pi^2)-1],
    E_h=T h_pi/sqrt(1+h_pi^2),
    E_hh=T/(1+h_pi^2)^(3/2)>0.

The response is quadratic at small gradient and linear at large gradient.
It has no leading infrared cubic. Canonically normalizing or changing to
a physical potential q pi changes coefficients, not these powers.
The retained small fluctuations have the usual positive DBI principal
symbol on its regular branch; this is a local EFT check, not a complete
gravitational or microscopic UV theorem.

Flat-brane matter respecting this symmetry couples to gamma, transforming
under the induced diffeomorphism. Its actual field equation follows from
delta gamma_mu_nu=2 partial_(mu pi partial_nu)delta pi:

    partial_nu{sqrt(-gamma)[T gamma^(mu nu)-T_m^(mu nu)]partial_mu pi}=0.

Both stress/metric indices in this expression are contravariant.

At pi=constant this has no matter source, even in the presence of an
arbitrary matter density. The matter interaction starts quadratically
in partial pi and modifies the kinetic tensor, T eta^mu_nu-T_m^mu_nu.
It does not provide a universally charged MOND scalar.

If one separately adds -q rho pi, then in n>=2 spatial dimensions

    D=E_h=q M_source/[Omega_(n-1) r^(n-1)],
    h_pi=D/sqrt(T^2-D^2).

This artificial source gives an attractive scalar for the usual healthy
scalar sign, but breaks the stated exact symmetry with a fixed arbitrary
source. It is Newtonian in the infrared and reaches a finite-flux gradient
singularity, rather than producing h proportional to sqrt(D). This source
test is diagnostic, not an extra symmetry-preserving brane completion.

## 3. The strongest constructive alternative: AdS DBI and a geometric charge

In AdS5 of curvature radius ell, the induced metric is

    gamma_mu_nu=e^(-2pi/ell)eta_mu_nu+partial_mu pi partial_nu pi.

The nonlinear shift/dilation and broken boosts in source Eqs(13)--(16)
act on gamma as induced diffeomorphisms. Matter minimally coupled to it
can now be universally charged without an independently chosen q.
For a slow particle around a constant brane normalized to pi0=0,

    S_particle=-m integral e^(-pi/ell)dt+velocity terms,
    q_pi=-1/ell, q_canonical=-1/(ell sqrt(T)).

The local scalar kinetic term is -T(partial pi)^2/2. With the source
convention -q_pi rho pi, its weak static equation is
T Delta pi=q_pi rho. Therefore the physical scalar potential
q_pi pi=-M_source/[4pi T ell^2 r] is attractive, with

    G_scalar=1/(4pi T ell^2).

This is a real geometric source relation, stronger than simply assigning
an arbitrary baryon charge. Its infrared force is nevertheless 1/r^2,
not the MOND 1/r force.

The same symmetry separately allows brane tension and an AdS tadpole:

    L=-T e^(-4pi/ell)sqrt[1+e^(2pi/ell)(partial pi)^2]
          +A_t e^(-4pi/ell).

The tadpole coefficient here is renamed A_t; it is not the earlier eta
deformation. Both terms are separately invariant up to boundaries, so
their ratio is not fixed by the displayed nonlinear Ward identity.
For a constant flat brane the potential is

    V=(T-A_t)e^(-4pi/ell),
    V_pi=-(4/ell)(T-A_t)e^(-4pi/ell).

A stationary finite constant-brane vacuum requires A_t=T, giving V0=0.
This is the supersymmetric D-brane sign/choice used in source Eq(12).
This statement uses the displayed zero-additive-constant convention.
An added flat-probe constant B0 preserves its field Ward identity and
would give V0=-B0 after A_t=T. Its gravitational meaning needs the bulk
and metric completion; neither the height nor that completion is fixed
by this scalar Ward calculation.
A positive unmatched height is a monotonic potential, not a selected
positive constant-brane vacuum. We do not import a full BPS/gravity
completion from that probe formula or rule out other curved embeddings.

The source's larger second-order brane class includes induced curvature
and extrinsic-curvature/Lovelock terms with their own coefficients.
On an affine flat-bulk embedding, extrinsic and intrinsic curvatures vanish,
so they do not replace the DBI constitutive law by a local |grad pi|^3.
For a regular finite-position AdS background these operators are analytic
in small derivatives. Canceling their quadratic coefficient gives higher
analytic powers or a degenerate vacuum, not a positive |grad pi|^3 term
without a separately demonstrated critical elimination or singular limit.

An induced R[gamma] coefficient in the probe model is also not automatically
a force-calibrated four-dimensional Newton constant: gamma there is built
from pi and a fixed bulk metric, not an independent massless graviton.
Bulk gravity/brane bending and matter mixing must be reduced together.
The source explicitly distinguishes its probe modulus from the DGP mode
and notes that coupling gravity changes the nonlinear-symmetry problem.

## 4. Galileon protection forbids the potential but gives a different Gauss law

The Galileon transformation is delta pi=c+b_mu x^mu. In four spacetime
dimensions, within the local Lorentz-invariant class with second-order
equations, the primary classification gives five Wess--Zumino terms:
a tadpole, a quadratic kinetic term and cubic/quartic/quintic derivative
terms. A generic nonconstant U(pi) is excluded, but the leading operators
contain Hessians of pi; their protected cubic is not (partial pi)^3.
For example L3=-(partial pi)^2 Box pi/2 is invariant up to a boundary.
The MOND operator -C[(partial pi)^2]^(3/2) is not: shifting its gradient
changes its Euler equation for generic off-shell pi, whereas a Galileon
equation depends only on the invariant Hessian.

With an explicitly admitted universal scalar source, a cubic Galileon
diagnostic is

    L=-c2(partial pi)^2/2-c3(partial pi)^2 Box pi/(2Lambda^3)
          -q rho pi.

Its general n>=2 spatial spherical equation integrates to

    c2 r^(n-1) h+(n-1)c3 r^(n-2)h^2/Lambda^3
       =q M_source/Omega_(n-1),       h=pi'.

For c2>0, large-radius response is h proportional to r^(-(n-1)).
Where the cubic Hessian term dominates, h is proportional to
r^(-(n-2)/2), giving r^(-1/2) in three space dimensions. Its nonlinear
force screens toward smaller radius; it is not the desired infrared law.

After choosing a stationary asymptotic background with the tadpole removed
from its perturbation equation (d1=0), the four-dimensional Galileon gives,
including the quartic term,

    d2(h/r)+2d3(h/r)^2+2d4(h/r)^3=q M_source/(4pi r^3).

An untuned tadpole would instead add a background/r^3 contribution and
is not covered by this localized-source polynomial. The quintic static
equation vanishes because the four-dimensional
Hessian has zero time eigenvalue. A single dominant power gives force
exponents r^(-2), r^(-1/2), or r^0. There is no r^(-1) asymptote among
them. Positive retained quadratic coefficient d2>0 fixes the far-field
linear response; deleting it loses that regular vacuum and still does
not give the MOND exponent. This is a statement about this finite local
Galileon class, not every higher-derivative/multifield critical theory.

The pi T coupling itself does not preserve the fixed-source Galileon
symmetry; a full gravitational construction must justify its breaking
and source normalization. The familiar nonrenormalization claim concerns
pi loops under its hypotheses, not every matter/gravity loop, and does
not determine separately allowed invariant coefficients. Nor does an
internal Galileon Ward identity forbid a pi-independent vacuum term or
fix its gravitating value after a metric sector is specified.

## 5. Decision and remaining microscopic implication

Exact internal point shifts do not coexist with the required inherited
chi-dependent operators. Genuine brane/Goldstone symmetries can exclude
arbitrary potentials, but they select different derivative structures.
Flat DBI has no linear symmetry-preserving matter charge. AdS DBI has a
geometrically fixed attractive charge, a quadratic infrared response and
zero potential on its displayed stationary flat-brane choice. The sourced
Galileon has a different radial response and needs its actual gravity/
matter completion. These are physical failures before any numerical fit.

No tested Ward identity simultaneously preserves the inherited MOND
mechanism, forbids its eta deformation, and fixes a positive gravitating
vacuum to its actual force coefficients. No R=128pi/9 follows. A new
multifield, curved-brane or microscopic construction remains possible,
but must display a full exact transformation, source action, retained
regular spectrum and selecting equation. This bounded result is not a
classification of every possible nonlinearly realized microscopic symmetry.
