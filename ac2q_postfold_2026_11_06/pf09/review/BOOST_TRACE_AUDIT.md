# Independent audit: boost-only finite surface stress

**Verdict: proved as written, with the stated strong uniform slice,
coarea, finite-measure and regular-contraction hypotheses understood
literally.** For bounded invariant state and a regular timelike interface,
the total matter surface stress vanishes even without an upper bound on
unit-clock rapidity. This does not assert that the two boost-dependent
terms vanish separately.

Audited input: `pf09/BOOST_TRACE_ROUTE.md`, SHA256
`2189b4e1e58fd6a4e0a5908f5725a6f6ad9e367cf607993ec077787a2773a999`.
Repository HEAD at inspection: `70bbb84f45399f04b1ca5b3978f84cd52824bd2c`.
Independent delegated proof audit, 2026-11-06; no numerical evidence is
needed for this implication.

## Claim and dependencies

Consider smooth native layers shrinking onto a regular timelike planar
interface, with r bounded above and away from zero, bounded A and P,
uniform cap separation, and bounded potential on the clock-label range.
Assume the metric converges uniformly to a nondegenerate continuous metric
with the regularity required by the stated limiting conservation law.
Assume uniform same-clock endpoint Pi matching, uniformly bounded clock
labels on compact interface regions, and finite total-variation bounds
for the coordinate components of the **total** stress measures. Identify
the regular outer bulk limit and its surface remainder S. The conclusion
is S=0, provided the limiting conservation law has no normal dipole.

The dependency chain is: bounded D positive part plus Pi matching gives
vanishing multiplier mass; Lorentzian coarea transfers that estimate to
spacetime; the exact boost-independent trace identity gives zero surface
trace; symmetry and the no-dipole condition on a timelike interface then
force the entire longitudinal surface tensor to vanish. The transverse
components are bounded directly. Each step passes under these hypotheses.

## Slice and coarea check

In a regular conformal base chart, a future timelike clock gradient has
phi_t>0 and |phi_x/phi_t|<1. Each clock level is therefore a graph with

    dt/dx=-phi_x/phi_t,    |dt/dx|<1,
    d ell=exp(alpha) sqrt(1-(dt/dx)^2) dx.

Its proper length through a coordinate strip of width epsilon is at most
C epsilon. A large boost decreases this proper length; it does not spoil
the upper bound. For a moving interface the same estimate holds locally
with a constant depending on a strict timelike slope margin: crossing
x-X(t) is monotone because 1-X'(t) dt/dx stays positive. A compact regular
timelike segment supplies this margin. Crossings occur within O(epsilon)
coordinate time, so endpoint controls must cover that slightly enlarged
segment.

The exact full-switch identities are

    e Pi=exp(2 beta) D,
    D=(Ar-1)/gamma-r^2-mu,    mu>=0.

Thus D_+ is uniformly bounded. The positive variation of Pi on each
crossing is O(epsilon). If its signed endpoint difference is uniformly
o(1), its negative variation is o(1) as well. Bounded positive metric
weights imply integral D_- d ell=o(1). On multiplier support Ar=1,
so mu=-D-r^2<=D_-; consequently integral mu d ell=o(1).

For each smooth layer the exact base-volume change of variables is

    dVol_base=(1/r) dphi d ell.

For example, dt dx=dphi dx/phi_t and
d ell=exp(2 alpha) r dx/phi_t, which verifies the formula even as the
level graph approaches null. Including transverse volume adds the
bounded factor exp(2 beta). No upper bound on phi_t or inverse boost is
needed. Uniform phi convergence on a compact enlarged coordinate region
places its clock labels in a fixed bounded interval. Uniform slice o(1)
and r>=r_min then give integral_layer mu dVol=o(1).

Pointwise-in-label matching alone would not justify this integral step.
Uniform matching as stated, or an explicitly integrable replacement,
is essential. Regular outer traces alone also do not identify the inner
same-clock endpoint difference unless the stated strong matching holds.

## Trace and distributional tensor check

The native longitudinal stress and its exact base trace are

    T_ab=H h_ab+(r H_r-mu Q)n_a n_b,
    h^ab T_ab=2H-r H_r+mu,

using h(n,n)=-1 and mu Q=mu. With r,A,P in the declared compact set,
H and r H_r are bounded. The preceding multiplier estimate therefore
implies that the base trace has no surface measure. Likewise
T_perp=H+P W_P is bounded and has no surface concentration.

Uniform convergence of h^{-1}, together with a uniform total-variation
bound on the total stress, permits contraction to commute with weak
measure convergence: the error is bounded by the metric sup-norm error
times that total variation. No separate measure bounds on mu n n or
r H_r n n are needed. Finite distributional convergence without the
stated measure bound would not support this argument.

The coefficient of the normal delta derivative in conservation is
N^a S_ab. Its absence gives N^a S_ab=0. Symmetry gives the corresponding
condition in the second slot. In a longitudinal orthonormal basis
(T,N), with T the unit timelike tangent, this leaves only

    S_ab=s T_a T_b,    h^ab S_ab=-s.

These are identities of measures, so they also cover a coefficient s
singular along the interface. Zero base trace gives s=0. Planar symmetry
removes longitudinal-transverse mixed components, and the bounded
transverse stress removes the remaining components. Thus S=0.

The timelike condition is load-bearing: on a null interface a nonzero
null tensor can be tangent and trace free. Nor can undefined singular
metric-stress products be replaced by the regular contraction step.

## Scope and remaining question

There is no missing implication within the stated boost-only class.
Its exclusion concerns the total finite surface stress, allowing large
opposing contributions to cancel; it establishes no individual bound
on mu n_a n_b. Uniform metric convergence, total stress measure control,
bulk identification, strong Pi matching, and compact clock-label control
remain actual assumptions, not consequences of bounded invariants.

This result cannot be combined with the separate large-r/bounded-boost
lemma to cover simultaneous r and rapidity escape. It also supplies no
singular continuation, entropy rule, or outgoing-state uniqueness.
