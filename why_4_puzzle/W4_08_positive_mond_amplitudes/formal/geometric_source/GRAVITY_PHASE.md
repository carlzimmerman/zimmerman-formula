# A gravitational order parameter: universal MOND without a selected scale

2026-10-20. Base f4d7d0e7a; criteria-only commit1a46afd06.
The source is Khoury1602.05961v2,20April2016, not1602.05997. Exact pins
and overlap limits are in `SOURCES_PHASE.md`. The original healthy
microscopic xi=1/4 goal is not achieved. No empirical value or target is
used to set an action coefficient. This is an analytic EFT calculation;
no new script, build, download, scan or Lean module was used.

## 1. Actual action and the attractive universal source

Use c=hbar=1, signature(-+++), dimensionless metric potential Phi, and
write M=M_Pl. To distinguish the source's polytropic exponent from the
number of spatial dimensions, call that exponent p>1. The published
nonrelativistic action, Eqs(18),(24), is

    L=-Z^2(partial chi)^2/2
      -M^2 |grad Phi|^2[1/(1+chi^2)
                        +chi^2 |grad X|^2/(9m^2 a0^2)]
      +P(X)-rho_b Phi,
    X=thetadot-m Phi-|grad theta|^2/(2m),
    P(X)=Lambda^4 (X/m)^p/p.

At theta=mu t, grad X=-m grad Phi. Expanding P(mu-mPhi) only to first
order in the weak potential gives the source -rho_s Phi, with
rho_s=m P_X(mu)=Lambda^4(mu/m)^(p-1). Put h=|grad Phi| and y=1+chi^2.
The leading weak-static functional is therefore

    L=-Z^2(partial chi)^2/2-E(h,chi)-(rho_b+rho_s)Phi,
    E=M^2 h^2[1/y+h^2(y-1)/(9a0^2)],        y>=1.

This changes the gravitational potential's own action. There is no
separate phonon/baryon charge q. A minimally coupled slow test body has
force per mass -grad Phi, so positive source mass gives attraction.
The source includes superfluid and baryonic mass; it is not a baryon-only
law independent of the halo's gravitating mass profile.

For a local static functional E(h), its general n>=2 spatial Gauss law is

    div[(E_h/h)grad Phi]=rho,
    Omega_(n-1) r^(n-1) E_h=M_enclosed(r).

This is a formal static n-dimensional extension, not a claim that the
published four-dimensional covariant completion has been generalized.
In the ultraviolet chi=0 phase E=M^2 h^2, so

    h_UV=M_enclosed/[2M^2 Omega_(n-1)r^(n-1)].

In three space dimensions the force-calibrated Newton coefficient is
G=1/(8pi M^2). The physical weak-potential convention is g=c^2 h when
c is restored; the same universal metric source sets both force limits.

## 2. Exact algebraic minimum and the actual interpolation

Let x=h/(3a0). For 0<x<1, the two-term minimum is globally controlled by

    1/y+x^2 y-2x=(xy-1)^2/y>=0.

It occurs at y=1/x, or chi^2=3a0/h-1. For x>=1, the excess over y=1 is
(y-1)(x^2-1/y)>=0, so chi=0 is the global minimum. The broken-phase
functional, before restoring its retained gradients, is exactly

    E_min=M^2[2h^3/(3a0)-h^4/(9a0^2)],       0<h<3a0.

Thus the actual leading coefficients are

    C2=M^2,             C3=2M^2/(3a0).

The quartic correction matters for the interpolation. Its Gauss law is

    div[mu(h)grad Phi]=rho/(2M^2),
    mu(h)=h/a0-2h^2/(9a0^2)   for 0<h<3a0,
    mu(h)=1                  for h>=3a0.

Mu is continuous at the transition. The radial susceptibility is
E_min,hh=4M^2(h/a0)[1-h/(3a0)]>0 inside the broken phase and tends to
zero at its upper endpoint; it is 2M^2 above the transition. These static
facts are not a complete dynamical health theorem.

Deep in the formal broken regime, the n-dimensional force is

    h_IR=sqrt[a0 M_enclosed/(2M^2 Omega_(n-1))]
          r^(-(n-1)/2).

Only n=3 gives h=sqrt(G M_enclosed a0)/r. For a genuine same-state
gravitating vacuum epsilon, the corresponding three-dimensional ratio is

    R=epsilon C3^2/C2^3=4epsilon/(9M^2 a0^2),
    xi=a0^2/(G epsilon)=32pi/(9R).

Here a0 is already present in the source action. Its coefficient is not
deduced from Z2 or from the superfluid equation of state. Restoring units,
xi=a0_phys^2/(G rho_mass c^2)=a0_phys^2/(G epsilon_energy).

## 3. Retaining chi prevents a uniform algebraic infrared limit

The field chi has the ordinary kinetic coefficient Z^2>0. At the broken
minimum its exact canonical fixed-background mass is

    m_chi^2=8M^2 h^4[1-h/(3a0)]/(9Z^2 a0^2).

It vanishes both as h tends to zero and at the phase transition. Positivity
away from those endpoints is a useful local check, not permission to
discard chi. Its static equation is Z^2 Delta chi=E_chi; the algebraic
profile chi_*(h(x)) generally has Delta chi_* nonzero.

The exact gradient cost evaluated on that profile is

    Z^2 |grad chi_*|^2/2
      =9Z^2 a0^2 |grad h|^2/[8h^3(3a0-h)].

For an exterior three-dimensional deep-MOND point-source profile
h=A_h/r, A_h=sqrt(G M_source a0), chi_* is proportional to sqrt(r).
Consequently |grad ln chi_*| tends to 1/(2r), and

    (chi gradient energy)/(leading cubic functional)
      ~9Z^2 r^2/[16M^2(G M_source)^2].

For every fixed Z>0 this grows with radius. Equivalently the necessary
adiabatic condition |grad ln chi_*|<<m_chi eventually fails. The source's
Eqs(32)--(43) make a parametric finite-window EFT argument; their use of
1/r in this estimate is an order-unity scaling, whereas the exact profile
gives 1/(2r). No observational values from those bounds are inputs here.
Setting Z=0 would change the retained field theory, remove its kinetic
term and invalidate its finite-Z perturbative estimates.

At h=0 the undeformed flat-space chi potential is zero for every finite
constant chi. The relaxed h>0 minimum runs to chi=infinity as h tends to
zero; it is not a selected finite zero-field vacuum. At any fixed finite
chi0 the small-h functional instead starts as M^2h^2/(1+chi0^2).
The Einstein prefactor on the runaway branch also tends to zero. This
does not prove that every possible UV completion is a ghost; it identifies
the nonuniform field/derivative limit of this particular reduction.

## 4. Finite-density matter energy is not the missing vacuum

The relativistic LO source action is P(Y), with
Y=-(partial Theta)^2/2 and P=Lambda^4(Y/m^2-1/2)^p/p. Its stress is

    T_mu_nu=P_Y partial_mu Theta partial_nu Theta+P g_mu_nu,
    epsilon_sf=2Y P_Y-P,       pressure=P.

Writing r_Y=Y/m^2-1/2 near the nonrelativistic regime gives

    epsilon_sf=Lambda^4[r_Y^(p-1)+(2-1/p)r_Y^p].

Its leading positive density is the mass density rho_s; its small positive
equation-of-state ratio is approximately r_Y/p. It is neither an invariant
vacuum stress nor a cosmological constant. The constant P(mu) discarded
when obtaining the local weak-static source equation cannot be relabeled
as gravitating epsilon. At its zero-density boundary r_Y=0, this displayed
LO potential contributes no positive vacuum energy for p>1.

A covariant addition -U(chi) gives T_mu_nu=-U g_mu_nu on a constant chi
state. That is a different, explicit source of vacuum energy. The source
paper leaves dark energy unresolved; it does not derive this U or relate
its value to a0. Its n=2 Bose-gas example supplies a conventional origin
for a LO equation of state, not a derivation of the special NLO function.

## 5. A regular positive vacuum and an explicit normalization deformation

First add U=epsilon+Z^2 m_chi0^2 chi^2/2 with epsilon,m_chi0^2>0. This is
a positive Z2-preserving stabilizing potential. Define
b=Z^2 m_chi0^2/(2M^2). Algebraic symmetry breaking now requires

    h^2/(9a0^2)+b/h^2<1.

When b<9a0^2/4 this gives a finite interval between

    h_+/-^2=(9a0^2/2)[1+/-sqrt(1-4b/(9a0^2))].

At sufficiently small h the vacuum is chi=0 and the response is quadratic.
The broken-interval minimum, when present, is

    E_min=epsilon+2M^2 h sqrt[h^4/(9a0^2)+b]
                    -M^2[h^4/(9a0^2)+b].

This repair is an explicit regular same-field potential, not an FI source.
It supplies a positive vacuum at the cost of the asymptotic infrared
cubic; epsilon remains an independently allowed constant.

There is a sharper test of selection that preserves the source's formal
cubic branch instead. Add the bounded positive real-analytic potential

    U_A(chi)=epsilon+A chi^6/(1+chi^2)^6,
    epsilon>0, A>=0.

At chi=0, U_A=epsilon and U_A-epsilon=O(chi^6). Therefore changing A at
fixed epsilon leaves the entire chi0 homogeneous background, vacuum
stress, Einstein coefficient and first/second variations of the covariant
action unchanged, including metric/fluid variations. For h>=3a0, chi=0
also remains the exact global static minimum: the original gravitational
excess and the added potential excess are both nonnegative. Actual C2
and the Newtonian force therefore remain unchanged in this approximation.

On the low-h branch let y=s/h. The plateau tail gives

    E_min-epsilon=C3(A)h^3+O(h^4),
    C3(A)=min_(s>0) {M^2[1/s+s/(9a0^2)]+A/s^3},
    s_A^2=(9a0^2/2)[1+sqrt(1+4A/(3M^2 a0^2))].

The displayed positive root is the unique minimum, since its derivative
changes sign once and the second derivative is positive. The envelope
derivative is dC3/dA=1/s_A^3>0. At A=0 it recovers 2M^2/(3a0).
Thus, even keeping the positive vacuum epsilon and all retained quadratic
and ultraviolet data fixed, an allowed Z2/diffeomorphism-preserving
operator changes the leading static cubic. Its operational acceleration
would be a_eff=2M^2/(3C3(A)), not the unchanged parameter called a0.

This is an actual normalization counterfamily, not parameter counting.
It operates at the same leading weak-static order as the source action;
the potential's additional gravitating stress and curvature must also
be included in a full halo solution. It does not cure the retained-gradient
problem or certify microscopic health of the covariant completion.
A plateau falling faster than chi^-6 can leave this leading cubic
unchanged, but its constant height still has no selecting equation.

## 6. Covariant completion, curvature and the limits of the source claim

The source's proposed covariant action, Eq(73), is

    L=M^2[R/2-(2 Box n_f/3+Box Y/m^2)] F
      -Z^2(partial chi)^2/2+P(Y)+L_b,
    F=1/(1+chi^2)+chi^2(partial Y)^2/(9m^4 a0^2),
    n_f=sqrt det(g^mu_nu partial_mu phi^I partial_nu phi^J).

It uses the normal fluid's three comoving scalars. The added Box terms
cancel undesired grad F terms in the leading weak-static metric constraint,
giving Phi=Psi there, unlike the naive RF coupling. This is a derived
weak-static lensing/source statement, not an all-background completion.

The displayed truncation also needs its normal-fluid variation. With
B^IJ=g^mu_nu partial_mu phi^I partial_nu phi^J, twice integrating by parts
gives S_n=-(2M^2/3) integral sqrt(-g) n_f Box F. Consequently

    delta n_f=n_f(B^-1)_IJ partial^mu phi^J partial_mu delta phi^I,
    nabla_mu[n_f(Box F)(B^-1)_IJ partial^mu phi^J]=0.

No LO normal-fluid function of n_f is displayed in Eq(73); P(Y) has no
n_f dependence. At chi=0, F=1 exactly, while its first nonconstant
variation begins at chi^2. Thus the normal-fluid scalars have no bulk
quadratic action in this truncation; mixing delta n_f times delta^2 F
starts at cubic order. The background n_f can nevertheless enter the
quadratic chi potential through Box n_f. This is an absent quadratic
normal-fluid dynamics/degeneracy observation, not a demonstrated propagating
ghost or a theorem about a completed fluid EFT.

Away from chi=0 the Euler equation above cannot be discarded. For example,
the flat static rest diagnostic phi^I=x^I requires partial_i Delta F=0.
The leading spherical deep-MOND F is proportional to 1/r and satisfies
this exterior condition. To include the actual algebraic quartic force
correction, set z=h/(3a0) and b_r^2=G M_source/(9a0). Its Gauss law gives
z^2-(2/3)z^3=b_r^2/r^2, hence formally z=b_r/r+b_r^2/(3r^2)+O(r^-3).
Then F=2z-z^2=2b_r/r-b_r^2/(3r^2)+O(r^-3), so
Delta F=-2b_r^2/(3r^4)+O(r^-5) is not constant. This expansion is a
diagnostic of the algebraic static branch, not an all-radius retained-Z
solution.
This diagnoses an additional background equation, not a halo exclusion:
the metric, fluid profile and retained corrections must be solved together.
Adding a genuine normal-fluid LO action would change this problem and
requires its own stress, source and kinetic specification.

The published action has higher time derivatives. The source argues that
the would-be ghost becomes heavy as c_s tends to zero and lies beyond the
EFT cutoff. It supplies no microscopic Hamiltonian/UV completion here.
The bare positive chi kinetic and LO phonon sound speed alone cannot
replace a constrained spectrum and cutoff audit of the full theory.

Positive vacuum curvature is also load bearing. Define
Q_curv=R/2-2 Box n_f/3-Box Y/m^2. On a homogeneous de Sitter diagnostic
with comoving n_f proportional to a^-3 and constant Y, Box n_f=Box Y=0,
Q_curv=6H^2. At chi=0 the fixed-background canonical curvature mass is
12M^2H^2/Z^2, in addition to any U_chichi/Z^2. This explains why the
cosmological branch can differ from the flat-static broken branch.
This is a fixed-background diagnostic: constant Y at nonzero P_Y does
not generally solve a^3 P_Y Thetadot=constant in de Sitter. It is not
being asserted as a constructed finite-density vacuum solution.

It is not legitimate to add epsilon and silently use the Minkowski
algebraic solution down to h=0. A halo background needs its own metric,
superfluid and normal-fluid equations; background curvature competes
with the static potential when their terms are comparable. No inequality
such as sqrt(6)H<h<3a0 is asserted as a halo theorem: it would presume
an unproved additive background and fluid configuration. The present
calculation neither establishes nor excludes a covariant MOND window
on an arbitrary positive-vacuum background.

## 7. Decision

This action genuinely removes the separate phonon/baryon charge and
produces the attractive metric MOND functional and the correct order of
force limits in its algebraic static EFT window. It is therefore a
distinct constructive route from the prior electric susceptibility and
direct-phonon models. The scale a0 is nevertheless an input, the
same-field adiabatic limit fails at sufficiently small gradient for finite
Z, and the finite-density superfluid is not the required positive vacuum.
The explicit positive potentials either restore quadratic infrared
response or permit the cubic to vary at fixed vacuum/UV/quadratic data.
Z2 supplies no equation excluding that variation.

No independently normalized microscopic equation forces epsilon/a_eff^2,
and no healthy ultraviolet theory or complete formal bridge has been
established. The covariant curved-halo and UV obligations remain open;
this restricted calculation is not a no-go theorem for every superfluid
completion. It does not force R=128pi/9 or xi=1/4.
