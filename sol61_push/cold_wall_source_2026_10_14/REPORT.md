# A cold source for a moving curvature wall: source and stability tests

2026-10-14. CWS-001/002/003/004. Base b1dda1e6c63f8b01925e70ac16b05cca13b189fd.
This continues the [required-stress calculation](../cold_geometry_drive_2026_10_14/REPORT.md).

**The engine remains unsolved.** There is now a source-level obstruction to a
static radial scalar shell, including a regular positive scalar coupling to
Ricci curvature. A different, explicitly hypothetical time-dependent scalar
has a negative-density branch with positive time kinetic energy. Its scalar
perturbations can be stabilized in an ideal finite shell by an assumed
fourth-spatial-derivative operator and assumed reflecting boundaries. This
does not supply the moving wall's complete stress or establish gravitational
stability. A separate momentum test identifies the directional flow still
needed. Neither scalar is an identified cold-energy particle.

## 1. The target includes momentum, not only negative density

Set c=hbar=1, signature -+++, Mp^2=1/(8 pi G). At constant bubble speed V,
transform the previous metric to bubble coordinates z=z_lab-Vt. It becomes

\[
 ds^2=-dt^2+dx^2+dy^2+[dz+b(r)dt]^2,\quad
 b=V(1-f),\quad r^2=x^2+y^2+z^2.
\]

The shift is zero in the flat cabin and V outside. The outside is still
Minkowski in a uniformly translating coordinate system. The unit normal is
n=partial_t-b partial_z; ez=partial_z is a unit spatial direction.

For a general static b(x,y,z), direct four-dimensional calculation gives

\[
 G_{nn}=-\tfrac14(b_x^2+b_y^2),\quad
 G_{nz}=-\tfrac12(b_{xx}+b_{yy}),\quad
 G_{zz}=-\tfrac34(b_x^2+b_y^2).
\]

The required source is Mp^2 G. These expressions agree with the metric's
constraint formulas in the previous source-verified checkpoint. The code
here derives them afresh from the inverse metric, Christoffel symbols,
Ricci and Einstein tensors, rather than inserting the target expressions.

For the null vectors n+-ez, the sum of the two null contractions is
2(Gnn+Gzz)=-2(bx^2+by^2). At least one is negative wherever the transverse
gradient is nonzero. A negative scalar potential alone cannot fix this:
potential terms proportional to the metric vanish in a null contraction.

For a fixed shape, Gnz is order V/R^2 and Gnn is order V^2/R^2. At low
speed the momentum requirement is parametrically larger than the density
requirement in these units. Matching a negative density in isolation misses
a leading part of the source problem. T(n,ez) is a signed stress contraction;
the usual outward energy flux has the opposite sign.

## 2. A static radial scalar fails even with A(phi)R

Consider the new trial class

\[
 S=\int\sqrt{-g}\,[\tfrac12 M_p^2 A(\phi)R+P(\phi,X)],
 \qquad X=-\tfrac12\nabla_\mu\phi\nabla^\mu\phi.
\]

Assume a static radial scalar phi(r), positive regular A(r), and no added
normal-spatial momentum source. The field equation from metric variation is

\[
 M_p^2 A G_{\mu\nu}=T^P_{\mu\nu}
 +M_p^2(\nabla_\mu\nabla_\nu A-g_{\mu\nu}\Box A),\quad
 T^P_{\mu\nu}=P_X\phi_\mu\phi_\nu+Pg_{\mu\nu}.
\]

At the equator z=0, both ez.phi and n.phi vanish, so T^P(n,ez)=0.
Direct calculation of the Hessian gives

\[
 (\nabla\nabla A)_{nz}
 =\tfrac12(b_xA_x+b_yA_y)-b A_{zz}
 =\tfrac12 b'A'-bA'/r.
\]

The nz field equation therefore requires

\[
 \boxed{A(b''+b'/r)+(b'-2b/r)A'=0.}
\]

**Scoped obstruction.** If the cabin ends at r0>0 with b(r0)=b'(r0)=0,
there is no nontrivial C2 shift b solving this equation on a connected radial
interval with A>0 and A at least C1. Indeed division by A gives the homogeneous
linear equation

\[
 b''+(1/r+A'/A)b'-2A'b/(rA)=0.
\]

Its coefficients are continuous. Write w=(b,b') and w'=C(r)w. On every
compact subinterval, C is bounded; the integral equation with w(r0)=0 and
the standard integral bound imply w=0 throughout. Continuing across compact
subintervals gives b identically zero. It cannot reach the required exterior
b=V for V nonzero. A classical full solution needs sufficient additional
regularity for its other Hessian components; the necessary momentum equation
already fails under the weaker regularity above.

This argument does not choose P or solve the scalar equation: it rules out
the trial source using a necessary metric equation alone. It also covers
additional static radial scalars whose minimal normal-spatial stress vanishes.
It does not cover nonradial fields, an extra current, singular/vanishing A,
other curvature operators, or another lapse/spatial metric. A separate
[time-dependent radial extension](RADIAL_TIME_EXTENSION.md) proves that
radial time dependence alone leaves the same obstruction.

The explicit quintic profile has an independent local diagnostic. Put
u=2r/R-1 and g=1-f=10u^3-15u^4+6u^5. The coefficient of A' vanishes when

\[
 (u+1)g_u-2g=2u^2(9u^3-25u+15)=0.
\]

There is exactly one root in 0<u<1, isolated exactly in (3/4,19/25):
u*=0.7548252216, r*/R=0.8774126108. At this root,
(u+1)g_uu+g_u=30u(1-u)(2-u-5u^2) is strictly negative.
Thus b''+b'/r is nonzero, and positive finite A cannot satisfy the boxed
equation by choosing A'. This pointwise test agrees with the uniform ODE proof.

If another source is added, its required signed momentum projection is

\[
 T^{\rm extra}_{nz}=-\tfrac12 M_p^2
 [A(b''+b'/r)+(b'-2b/r)A'].
\]

At r* the second term vanishes. An actual additional momentum source is
necessary there; changing the radial coupling slope cannot substitute for it.

## 3. A first-derivative scalar cannot simply be made healthy by its potential

For the minimally coupled P(phi,X) sector, T(k,k)=PX(k.phi)^2 for null k.
NEC violation therefore requires PX<0 wherever it occurs.

For a nonzero timelike scalar gradient choose its local rest frame with
phi_dot=q and X=q^2/2. The principal quadratic action is

\[
 L_2=\tfrac12(P_X+2XP_{XX})\dot\pi^2
 -\tfrac12 P_X|\nabla\pi|^2.
\]

Positive kinetic coefficient K=PX+2XPXX and stable spatial gradients require
K>0 and PX>0. PX<0 instead gives a gradient instability if K>0, or a ghost
if K<0. K=0 is degenerate and needs a separate analysis. For a nonzero
spacelike background gradient in its static frame, the time coefficient is
PX itself, so PX<0 gives a ghost. Null/degenerate gradients and theories with
other derivative operators are excluded from this local argument.

There is an additional algebraic control, even if stability is abandoned.
At a planar constant-shear point b=b(x), b'=s nonzero, b''=0, the mixed
required stress in the normal frame, divided by Mp^2 s^2/4, has eigenvalues
(1,1,-1,-3). A single P scalar has T^a_b=P delta^a_b+PX phi^a phi_b,
which is a rank-one update of P times the identity and has an eigenspace of
dimension at least three at eigenvalue P. The required planar tensor lacks
that structure. This is a local planar control, not a replacement proof for
all radial/nonminimal models.

The wider NEC/stability literature contains theories outside this restricted
argument. We do not promote it to an all-field no-go theorem; see the scope
discussion in [Dubovsky et al., hep-th/0512260v2](https://arxiv.org/pdf/hep-th/0512260v2).

## 4. An explicit different source branch, with a conditional stabilization

To test a possible escape, introduce a NEW speculative scalar sector:

\[
 P(X)=-X+X^2/M^4+M^4/4,\qquad
 X_0=(1-\delta)M^4/2,\quad0<\delta<2/3.
\]

This is an assigned homogeneous clock state, not the previously proposed
chi/S neutron portal or a derivation of the reciprocal tether medium.
Its stress and kinetic coefficients are

\[
 \rho=2XP_X-P=M^4(-\delta+3\delta^2/4)<0,\quad
 P_X=-\delta,\quad K=2-3\delta>0.
\]

At delta=0 its pressure and density both vanish in this chosen normalization.
The cancellation and state preparation have not been physically derived.
For delta>0 the scalar has positive time kinetic energy but negative
gradient coefficient. It is unstable in the unregulated infinite medium.

Now separately assume the following preferred-frame perturbation operator:

\[
 L_2=\tfrac K2\dot\pi^2+\tfrac\delta2|\nabla\pi|^2
 -\frac{K}{2M^2}(\Delta\pi)^2,
 \quad\omega^2=k^4/M^2-\kappa k^2,\quad
 \kappa=\delta/(2-3\delta).
\]

The term has fourth spatial derivatives and no extra time derivatives in
this quadratic description. It is an assumed regulator with a nominal scale
M; no covariant completion, actual cutoff or nonlinear strong-coupling scale
has been established for our source. On infinite space, modes
0<k<M sqrt(kappa) still grow. The fastest growth rate is kappa M/2 at
k=M sqrt(kappa/2), provided this lies in the effective theory's valid range.

Impose an ideal spherical shell a<r<a+d with the squared Dirichlet Laplacian:
pi=0 and Delta pi=0 at both boundaries. Its lowest Laplacian eigenvalue is
k1^2=pi^2/d^2. The radial eigenfunction sin[pi(r-a)/d]/r verifies this exactly;
angular variation adds a nonnegative angular-gradient term. A radial
one-dimensional Dirichlet bound on r*pi supplies the lower bound for all
angular sectors. Hence the stated quadratic operator is nonnegative iff

\[
 \boxed{Md\le\pi/\sqrt\kappa.}
\]

Strict inequality gives positive quadratic spatial energy; equality leaves
a zero-frequency mode and is only marginal. For delta=1e-4, Md=100 the
enumerated modes with k/M<=0.1 have no growing mode. At Md=1000 the first
two radial modes grow. The run records 15 parameter combinations and all
radial modes below that nominal momentum cap, rather than extrapolating a
finite table to a universal source claim.

**What this achieves:** negative background gravitational density and a
nonnegative scalar perturbation Hamiltonian can coexist in this deliberately
confined quadratic surrogate. It distinguishes an open route from merely
flipping the sign of a kinetic term.

**What it leaves open:** a physical phase boundary giving these two boundary
conditions, its energy/momentum budget, the exterior modes, all tensor/vector
modes, nonlinear evolution and the actual gravitational constraints. A flat
homogeneous delta>0 background is not an exact Einstein solution with its
nonzero stress; the calculation is a decoupled local perturbation surrogate.
Nor does the homogeneous pressure/density match a moving wall's anisotropic
stress. Shrinking the ideal cavity is not a demonstrated cold-energy trap.

The derivative-regulated clock-field idea has primary precedent in
[Arkani-Hamed et al., hep-th/0312099v1, equations 1.6–1.9](https://arxiv.org/pdf/hep-th/0312099v1).
Their gravity-coupled calculation develops a long-wavelength Jeans-type
instability, equation 7.8. Thus our decoupled shell calculation must not be
called a full gravity-stable realization, and the paper's 2003 observational
claims are not a present-day viability assessment of this new trial model.

## 5. The required flow has a transverse component

At first order in a shift beta in Einstein gravity with flat spatial slices,
the normal-spatial constraint is

\[
 G_{ni}=\tfrac12[\partial_i(\nabla\cdot\beta)-\Delta\beta_i].
\]

For Fourier wavevector k nonzero this becomes
Gni=(k^2/2) PT_ij beta_j, where PT=I-kk^T/k^2. It is transverse.
A directed localized radial shift has nonzero curl and a nonzero transverse
component; a pure scalar coordinate shift cannot account for that part.

A scalar perturbation of a homogeneous isotropic state contributes a vector
momentum of form ki times a scalar function of k^2 and frequency. Its
transverse projection vanishes. For minimal P(X), this is explicit at first
order: delta T0i=PX q partial_i pi. Adding scalar powers of the spatial
Laplacian does not manufacture an independent transverse source.

This statement assumes the standard Einstein vector constraint and this
linear isotropic setting. Nonlinear/nonradial backgrounds, vector fields and
curvature terms that change that constraint need their own analysis. The
unspecified covariant completion of the previous quadratic regulator is not
silently assumed to obey every such restriction.

An actual fluid can carry a transverse current. For small drift velocity wi
relative to n and positive enthalpy h, T(n,ei)=-h wi to first order. Choosing
wi=-Mp^2 Gni/h can match the momentum equation alone. It does not match the
required negative total density or anisotropic pressures, and it must solve
its continuity and force equations rather than have its velocity assigned.

The [reciprocal tether medium](../reciprocal_tether_medium_2026_10_14/REPORT.md)
already includes a varied current and Clebsch degrees of freedom for vorticity.
That makes a current-bearing, inhomogeneous source a relevant next route.
Its previous local cone certificate does not establish negative wall stress,
and the new clock scalar has not been identified with that medium.

## 6. Status and evidence

The three completed bounded runs passed 45, 12 and 7 assertions, respectively.
They cover the exact four-dimensional tensors, scalar-Hessian projection,
radial momentum equation, exact quintic root count/bracket, scalar principal
action, negative-density branch, ideal shell eigenfunction,15 finite spectral
cases and transverse-current identities. All three manifests validate with current
inputs and outputs. Universal conclusions here use displayed algebra and the
radial uniqueness argument; the finite table is only an illustration.

Source matching is now more specific: a successful model needs a controlled
inhomogeneous stress with both negative effective density and the required
directional momentum transport. The static radial A(phi)R/P source is closed
for this exact cabin/shift geometry. The regulated clock branch remains open
only as a conditional source/stability probe. A current-bearing multi-field
completion and broader metric families remain open.

The next discriminating task is a finite wall action containing a current
and a scalar control sector, with a derived interface and all
Einstein constraints. It must compute the stress from its fields and check
the coupled mode operator, including gravity. Assigning a trajectory,
negative density or reflecting boundary is not that solution. No baryon
production, horizon activation or propulsion demonstration follows yet.
