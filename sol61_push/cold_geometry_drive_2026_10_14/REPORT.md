# Can cold conversion produce geometric motion?

2026-10-14. CGD-001, base 2871dd1b857b009f81e1d2e218738da0767b9380.
Status: an exact required-stress calculation, not a realized engine. The cold
particles and conversion interaction remain hypotheses. This checkpoint advances
the curvature interpretation of the [previous propulsion study](../cold_conversion_propulsion_2026_10_14/REPORT.md).

**Result:** a prescribed moving bubble can have a flat cabin, a curved wall and
an exactly flat exterior. In the unit-lapse, flat-spatial-slice construction
tested here, its wall requires negative normal-observer energy density.
Ordinary baryons, outgoing light and a positive-energy cold dust component
cannot by themselves supply that required stress. Producing baryons is not
the missing geometric step. The missing step is a controlled cold-field
stress tensor that actually solves the coupled equations.

## 1. Write the geometry before naming its fuel

Use x0=ct and signature -+++. Let V=vs/c and prescribe

\[
 ds^2=-(dx^0)^2+dx^2+dy^2+[dz-V(x^0)f(r)dx^0]^2,
 \quad r^2=x^2+y^2+[z-z_s(x^0)]^2,\quad z_s'=V.
\]

The shift is beta=-V f ez. The lapse is one and each spatial slice has
Euclidean metric. This is the Alcubierre form with the travel direction
renamed. The original source supplies a metric and analyzes its exotic
stress requirement; it does not supply an engineering mechanism.
See [Alcubierre, gr-qc/0009013v1, equations 8–10,18–19](https://arxiv.org/pdf/gr-qc/0009013v1).

Choose a finite profile with a true cabin:

\[
 f=\begin{cases}
 1&r\le R/2,\\
 1-10u^3+15u^4-6u^5,&u=2r/R-1,\quad R/2<r<R,\\
 0&r\ge R.
 \end{cases}
\]

This profile is C2 at both boundaries, enough for the classical curvature
calculation; no delta-function wall is inserted. Its higher derivatives are
not all continuous, so it is not a proposed smooth solution of an arbitrary
higher-derivative gravity theory.

Inside, z'=z-zs turns the metric into Minkowski form. The central worldline
has zero proper acceleration even when a trajectory zs is prescribed. Outside
r>=R the metric is exactly Minkowski wherever that exterior is an open region.
These are properties of an imposed metric. A launch mechanism, stress evolution
and a massive craft have not been added. In particular, putting a real massive
craft in the cabin changes the field equations and this exact metric.

This is a useful distinction for isolation: a flat cabin is geometrically
possible in this ansatz. The wall remains a region of nonzero curvature;
ordinary matter crossing it need not be unaffected. Exact exterior flatness
here depends on an exotic source, rather than on a demonstrated gravitational
shield. No radiation-producing conversion process has yet been inserted.

## 2. The wall's necessary energy density

The unit future normal is n=(1,-beta). The Hamiltonian constraint gives

\[
 \rho_n=T_{\mu\nu}n^\mu n^\nu
 =\frac{c^4}{16\pi G}(K^2-K_{ij}K_{ij}),\qquad
 K_{ij}=\frac12(\partial_i\beta_j+\partial_j\beta_i).
\]

For the directed shift, Kzz=-V fz, Kxz=-V fx/2,
Kyz=-V fy/2. Therefore

\[
 \boxed{\rho_n=-\frac{c^4V^2}{32\pi G}
 [(\partial_x f)^2+(\partial_y f)^2].}
\]

It is negative on open parts of a nontrivial radial wall for every nonzero
V. Slowing this particular bubble reduces the magnitude but does not change
the sign. The independent four-dimensional check uses stationary beta_z=b(x)
and directly computes G(n,n)=-b'(x)^2/4, agreeing with the constraint.

For provenance, the general constraint and divergence identity below reproduce
known formulas after beta=-v and restoring SI units. Their overlap is
**known after translation**, not a new discovery. The source's broader
energy-condition conclusions require its additional hypotheses; this report
uses the displayed algebraic identities.
[Santiago, Schuster and Visser, arXiv 2105.03079v2, equations 4.1–4.6,7.6](https://arxiv.org/pdf/2105.03079v2).

## 3. Changing the flow does not freely remove the requirement

For a general sufficiently differentiable shift define
Jij=partial_i beta_j, A=Jij Jij, B=Jij Jji and
Wi=beta_i div(beta)-beta_j partial_j beta_i. Direct differentiation cancels
the second derivatives and gives div(W)=(div beta)^2-B. Also
|curl beta|^2=A-B and Kij Kij=(A+B)/2. Hence

\[
 \rho_n=\frac{c^4}{16\pi G}
 \left[\nabla\cdot W-\frac12|\nabla\times\beta|^2\right].
\]

For compact support, or falloff sufficient to make the boundary integral
vanish,

\[
 \int\rho_n\,d^3x=-\frac{c^4}{32\pi G}
 \int|\nabla\times\beta|^2d^3x.
\]

Nonzero curl therefore forces negative density somewhere in this class.
The curl-free case only makes this integral zero. If rho is continuous and
not identically zero it must then have both signs. If it vanishes identically,
this identity alone says nothing about the remaining stresses or all-observer
energy conditions. We do not close that exceptional case by assertion.

This integral is the density measured by these normals on these slices.
**It is not ADM energy, a fuel requirement or an invariant total energy.**
Indeed the exact compact ansatz has flat spatial metric and vanishing
extrinsic curvature at spatial infinity, hence zero ADM energy and momentum
under the usual asymptotically flat definitions. There is no contradiction:
the matter-density volume integral is not the ADM surface charge. A real
craft and apparatus require a different solution.

For the explicit quintic wall, exact integration gives

\[
 \int_0^\infty r^2 f'(r)^2dr=\frac{125}{77}R,\qquad
 \int\rho_n d^3x=-\frac{125}{924}\frac{c^4}{G}V^2R.
\]

At R=1 m and vs=1000 m/s this slice integral is -1.82169e32 J. It is an
illustration of this imposed profile, not a universal lower bound. The
canonical outputs include 12 radius/speed combinations. Changing lapse,
spatial curvature, asymptotics or field equations changes the problem.

## 4. What the conversion source would have to supply

The earlier conditional reaction chi+Sbar -> n+gamma transfers hidden baryon
number into an ordinary neutron and emits a photon. It does not specify a
negative-energy wall. Its momentum ledger remains necessary.

For classical components with nonnegative local energy density for every
timelike observer, their sum has the same property. Positive-density dust,
ordinary positive-energy particle distributions and classical Maxwell light
satisfy this condition. They cannot sum to the negative T(n,n) above.

A minimally coupled canonical real scalar with potential U>=0 has
rho_n=[(n.grad phi)^2+|D phi|^2]/2+U>=0. A positive vacuum energy has
Tmunu=-rhoLambda gmunu and T(n,n)=rhoLambda>=0. Negative vacuum pressure
does not turn this density negative. A cosmological vacuum is also not an
exact asymptotically flat exterior; these statements about its local stress
do not insert it into the flat-boundary ansatz.

The full proposed cold medium, interactions, quantum states and curvature
couplings have not been shown to obey these classical positivity assumptions.
They are therefore an unresolved possible source sector, not ruled out by
renaming them dust. An interaction binding energy or a quantum negative-energy
region cannot simply be assigned the required magnitude and lifetime either.
It needs an actual state and its complete stress, including its supports.

The precise remaining target is a solution of

\[
 G_{\mu\nu}[g]=\frac{8\pi G}{c^4}
 (T^{\rm cold}_{\mu\nu}+T^{\rm conversion}_{\mu\nu}
 +T^{\rm hardware}_{\mu\nu}+T^{\rm radiation}_{\mu\nu}),
\]

together with all matter equations, constraints and boundary data. Matching
only rho_n is necessary and insufficient: momentum density, anisotropic
pressures, energy exchange, finite apparatus and stability must also match.
Prescribing zs(t) by hand does not establish that the cold fields generate it.

Nonminimal curvature couplings may instead put additional terms on the left
side, or in an effective stress tensor on the right. Either notation still
requires solving that theory. The previous [scalar–Gauss–Bonnet feedback
study](../curvature_feedback_2026_10_14/REPORT.md) found a cone obstruction
for its particular homogeneous activation history; that is neither a solution
of this moving wall nor a universal obstruction for every modified theory.

## 5. Sphere curvature, activation and horizons are separate inputs

A sphere's intrinsic surface scalar curvature 2/R^2 is not spacetime
curvature. These slices have flat three-dimensional geometry even while the
wall has nonzero four-dimensional curvature. There is no universal
activation radius encoded by the word sphere.

If conversion is triggered solely by a local spacetime curvature invariant,
the exactly flat cabin has no such trigger. Conversion would need to occur
where the invariant is nonzero, or require an additional field, a retained
activated state, or a modified cabin geometry. None of those controls follows
from drawing a spherical boundary.

At constant V, axial null rays satisfy dz/dx0=Vf+-1. In coordinates moving
with the cabin their slopes are V(f-1)+-1. For 0<=V<1 and 0<=f<=1, the plus
slope is positive and the minus slope negative everywhere on the axis; no
axial stationary-light root appears. For V>1 the plus branch can have roots
at f=1-1/V. This is an axial causal diagnostic, not a proof of a complete
three-dimensional global event horizon for a finite-duration journey.

The wall's negative-density requirement already exists for V<1. It therefore
does not arise only when a horizon switches on. Nor does the horizon relation
supply a baryon-conversion threshold, dark-energy reservoir or black-hole
connection. Those require separate field equations and source dynamics.

## 6. Evidence and next discriminating task

The bounded run passed 28 assertions: exact gradient algebra, a full 4D Einstein
control, profile boundary values/derivatives, independent exact polynomial
integration, angular integration, scoped scalar/vacuum positivity and 12 SI
illustrations. Its input/output hashes validate. These checks support the
specified calculations, not the existence of the source.

Self-review: checked x0=ct units, shift sign, half factors, exterior support,
the normal normalization, positivity assumptions and the difference between
the slice integral and ADM energy. No independent agent review was used.
No novelty, complete literature survey or experimental viability claim.

The next source-level task is to derive the complete cold-field stress for
an inhomogeneous finite wall and test it against all Einstein components.
Positive-energy dust conversion is closed as the sole source of this exact
metric. A nonminimal/collective cold source remains open, pending its action,
state preparation and local stability. Broader lapse/spatial-metric families
are a separate open route and cannot inherit this class's obstruction.
