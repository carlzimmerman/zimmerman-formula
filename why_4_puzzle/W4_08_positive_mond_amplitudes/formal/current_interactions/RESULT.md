# Regular current and topological constraint results

2026-10-20. Base b760753a3; criteria-only commit 33e139648.
**The original why-4 goal is not achieved.** These results resolve specific
current constructions and formalize their energy algebra. No healthy
microscopic model selects 128pi/9 or the positive gravitating vacuum
normalization. None of these routes is a determinate candidate.

## A regular current interaction: exact charge, empty vacuum, quartic correction

Use D=partial-ieA, Psi=r exp(i theta), Q=r^2, nu=dot theta-eA0,
z=|grad phi|^2 and lambda>0. A preferred neutral clock defines the
time component. The interaction alpha i Psi* <->D0 Psi z gives

    L_time=Qnu^2-2alpha Qnu z,
    n=p_theta=2Q(nu-alpha z), div pi=e n,
    H_time=(n+2alpha Qz)^2/(4Q).

Gauss involves the FULL canonical charge, not the unshifted 2Qnu.
The complete matter Hamiltonian adds pr^2/4, |grad r|^2,
Q|grad theta-eA|^2 and lambda Q^3/3, all nonnegative. For
Psi=(x+iy)/sqrt(2), its temporal Hamiltonian is the regular polynomial

    [(pi_x-alpha z y)^2+(pi_y+alpha z x)^2]/2.

Thus polar denominators do not imply a Cartesian singularity. Positivity
of this Hamiltonian alone is not a full causal/quantum completion claim.

Without electric divergence or compensating charge, n=0. The homogeneous
amplitude energy is alpha^2 Qz^2+lambda Q^3/3, with its unique minimum
Q=0 for every z. The apparent gradient charge does not induce a vacuum
condensate. More generally, the empty Cartesian state gives zero matter
energy for prescribed static phi in this zero-charge sector.

At fixed n nonzero, the amplitude minimum satisfies

    lambda Q^4+alpha^2 z^2 Q^2=n^2/4,
    Q0=(n^2/(4lambda))^(1/4),
    E_n(z)=E_n(0)+alpha n z+alpha^2 Q0 z^2+O(z^4).

A compatible compensating source or electric boundary condition is needed
for a nonzero homogeneous n. The bare scalar stiffness must stabilize
the sign of alpha n. Removing the total quadratic coefficient leaves
a positive h^4 term, not the required h^3. This interaction escapes the
previous affine-gradient concavity hypothesis but gives the wrong power.

## A neutral conserved current cannot have arbitrary positive bulk charge

Suppose phi and its clock are gauge-neutral, J is independent of A,
and A_mu J^mu is a regular local interaction. Gauge invariance requires
the off-shell identity partial_mu J^mu=0. Assume compact scalar profiles
have no perturbation of current through the boundary. With T=t, suppose
the static perturbation density for every such profile were

    J0=k |grad phi|^2+div K.

Smooth compact time interpolation from phi=0 to phi=f preserves total
charge. Its proposed final-minus-initial value is
k integral |grad f|^2. Choose any nonconstant compact f: this forces k=0.
The argument works in every spatial dimension and at any finite local
derivative order under the stated boundary/regularity assumptions.

It does not exclude improvements such as

    J0=k[(grad phi)^2+phi Delta phi],
    Ji=-k partial_t(phi partial_i phi).

This current is identically conserved. The Laplacian term is indispensable:
integral Y J0=-k integral phi grad Y.dot.grad phi, up to boundary terms.
Dropping it on specially harmonic fields would manufacture the desired
bulk charge. Charged clocks, on-shell currents, nontrivial boundaries and
topological sectors are outside this restricted obstruction.

## Independent Jacobian charge: constructive local result, flux escape

In 2+1 dimensions set epsilon012=1 and add

    L_top=k epsilon^{mu nu rho} A_mu partial_nu u partial_rho v,
    j=k det(grad u,grad v), div pi=e n-j.

The neutral fields u,v are regular Cartesian scalars. This current is
identically conserved; its gauge variation is a boundary term. It is
independent of the charged amplitude. At A_i=0 the neutral canonical
momenta have their ordinary values; at general A_i the interaction
shifts them, leaving positive kinetic squares in the Hamiltonian.

IF div pi=0 is additionally imposed pointwise, Gauss fixes n=j/e. The
charged sextic amplitude then has the exact minimum

    min_Q>0[n^2/(4Q)+lambda Q^3/3]
       =(sqrt(2)/3)lambda^(1/4)|n|^(3/2).

Constant affine u,v and a constant charged amplitude can have E=B=0:
this homogeneous toy is not subject to the Chern-Simons magnetic
covariant-gradient objection below. It supplies an actual independent
charge constraint and a positive cubic in a common scaling of two
gradients. It does not identify j with |grad phi|^2. If u,v are both
functions of one phi their wedge vanishes. Positive ordinary u,v
gradient energies also supply quadratic infrared terms.

Local neutrality is NOT the fully relaxed Maxwell problem. For smooth
compact prescribed u_delta=delta u0, v_delta=delta v0 in the trivial
boundary sector, use the admissible trial

    Psi=0, n=0, A_i=0, B=0,
    pi_delta=-k delta^2 u0 (partial_2 v0,-partial_1 v0),
    neutral momenta=0.

Its divergence is -k delta^2 det(grad u0,grad v0)=-j_delta, so it obeys
the full Gauss constraint. All topological momentum shifts vanish here.
If E_bare is the prescribed neutral static energy, positivity and this
trial give

    0<=E_rel(delta)-E_bare(delta)<=C delta^4,
    C=(k^2/2) integral u0^2 |grad v0|^2 < infinity.

This excludes a positive leading C3 |delta|^3 in the excess fully relaxed
energy near zero. A longitudinal projection preserves the trial's
divergence and lowers its Maxwell energy if an electrostatic trial is
required. No scalar field equation for the prescribed u,v is assumed.

The bound assumes no separately fixed nonzero occupation, clock charge
or neutral momentum excluding the empty trial; any fixed-profile
potential belongs in E_bare. Grand potentials and nontrivial winding or
boundary charge require a different analysis. It is not a universal
topological-current exclusion. In particular the homogeneous and compact
limits cannot be interchanged without controlling this flux escape.

## Chern-Simons flux attachment: retained spatial terms and vacuum check

In a separate 2+1 model use the normalization

    L=K epsilon a f/4+|D Psi|^2-lambda Q^3/3, D=partial-ia.

Static Gauss ties charge to b=f12. Its energy is
|Di Psi|^2+K^2 b^2/(4Q)+lambda Q^3/3. Dropping the spatial term yields
an exact algebraic lower envelope A |b|^(3/2), where

    C=K^2/4, A=(4/3)lambda^(1/4)C^(3/4).

It is not an established magnetic equation of state: at b nonzero,
[D1,D2]Psi=-ib Psi forbids Di Psi=0 on a nonzero condensate. Magnetic
and radial scales are of the same order at a fixed self-dual coupling.
The omitted term can therefore change the leading coefficient.

Direct square completion gives the self-dual potential
V=Q(Q-v^2)^2/K^2, with lambda=3/K^2 at v=0. Its minima have zero
classical energy. An additive epsilon0 leaves the Gauss equation and
vacuum-subtracted square completion unchanged. This does not fix a
positive gravitating vacuum energy.

Primary source: Arias-Ireson-Schaposnik-Tallarita, arXiv:1505.06705v3,
17 August 2015, Eqs. 4-9, 24-25, 32 and 34. Its bosonic and SUSY sections
use different CS coefficients: with a=eA, Eq.4 maps K=kappa/e^2, whereas
Eq.32 maps K=2kappa/e^2. The SUSY potential Eq.34 then agrees with our
square completion. No numerical self-dual coupling was copied across
these normalizations. The source does not prove a MOND dictionary.

Even a cubic Legendre transform of |b|^(3/2) is a magnetic chemical
potential pressure, not a sourced attractive scalar gradient energy.
Ordinary positive-energy electric gauge exchange is repulsive between
like charges; an attractive scalar or vortex force requires its own
source derivation. Abelian A wedge F^m is intrinsically odd dimensional.
A planar p=3 scalar force scales sqrt(M)/sqrt(r), whereas MOND's
sqrt(M)/r requires p=3 in THREE spatial dimensions.

## A 3+1 axion-current test includes the magnetic constraint

For the specified static zero-external-flux action

    L=|grad Y|^2/2+P(Y)-Z|grad theta|^2/2-B^2/2
       +k Y B.dot.grad theta, div B=0,

magnetic stationarity gives B=k P_T(Y grad theta), the orthogonal
projection onto the zero-fixed-flux divergence-free L2 variation space.
Assume Y grad theta, B and the displayed energy terms have finite norms,
and all electric boundary and harmonic-flux terms vanish. Gauss is
-Delta Y+P'(Y)+k B.dot.grad theta=0. Multiplying by Y and integrating gives

    integral[|grad Y|^2+Y P'(Y)]
       +k^2 ||P_T(Y grad theta)||^2=0.

For P=gamma |Y|^3/6, gamma>0, every term is nonnegative and Y=0.
Thus this interaction gives the wrong balance even with div B enforced.
External/harmonic magnetic flux adds a cross term and is outside this
specific result; it is a distinct physical state requiring stress checks.

## Dimension, normalization and remaining obligations

In n space dimensions the direct pullback point-charge current uses n
independent neutral gradients. Conformal charged matter has fixed-charge
energy proportional to |n_charge|^((n+1)/n). Under uniform gradient
scaling h, this produces h^(n+1): cubic for n=2, quartic for n=3. This
restricts that direct conformal extension, not every current interaction.
Fixed gradients, layers or nonconformal matter change the argument and
introduce parameters and stress that must be calculated.

All surviving microscopic/current couplings and embedding choices remain
free. The earlier temporal-vector model still requires the independent
relation epsilon0=16pi gamma b^3 for the requested ratio. No current
constraint, fixed sextic coefficient or self-duality result here selects
that relation. The goal stays active. Possible continuations are boundary
sectors or nonconformal/current constraints that remove the empty-flux
trial, or an off-shell protected auxiliary completion. None has yet
provided a regular three-dimensional attractive MOND force together with
positive vacuum-like stress and a forced amplitude.

The current/gauge calculations were independently reconstructed; the
compact-flux trial received a separate independent audit. The formal
files prove only the displayed algebra under their explicit inputs,
not the full field-theory, integration, quantum or source bridges.
