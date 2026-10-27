# What the microscopic current duality does and does not derive

Lane: CE-PARTICLE-DUAL-2026-10-18. Requested reference checkpoint CE-FM-084,
`3d8900c10d8b778e2756838f2d00779dc43510ab`; observed checkout during this
work `3cdf7e065a04d703903bb2f61aac0640e62fb0b6`. This is a new derivation and
self-audit, not a change to the CE082 action, a frozen claim, or a queue.
All lane files are confined to this directory. Input hashes and the actual
computation revision are recorded separately.

**Claim audited.** The microscopic global U(1), followed by a current/two-form
duality, derives CE082's positive settled density constraint and its local
rational polarization energy. **Verdict: refuted, with two separate smallest
counterexamples.** A neutral particle/antiparticle population can have zero
Noether density and positive rest density. Even on a positive-charge branch,
a pure gauge change of the dual potential leaves the current fixed while
changing the proposed local energy. The restricted constructive result is
given below: a conserved reference-charge density is a divergence, and an
antiparticle-free single-species nonrelativistic fluid has a local dual action
whose energy depends on that divergence and on the gauge-invariant current.

## 1. Exact current and exact conversion, before a fluid approximation

Use hbar=c=1, metric (+---), epsilon^{0123}=+1, and complex scalar kinetic
terms +|partial Phi|^2+|partial X|^2. The microscopic potential contains

\[
 V=m^2|\Phi|^2+M^2|X|^2+
 g(X^*\Phi^2+X\Phi^{*2})+\lambda|\Phi|^4+\cdots . \tag{1}
\]

The omitted terms are the selected masses, modulus potentials and portals,
each separately invariant under the two species phase rotations. The cubic
is the only relative-phase-dependent term in this selected action. It is
invariant under Phi -> exp(-i alpha) Phi, X -> exp(-2i alpha) X. Define the
unit-charge species currents and their total by

\[
 j_\Phi^\mu=i(\Phi^*\partial^\mu\Phi-
                    \Phi\partial^\mu\Phi^*),\qquad
 j_X^\mu=i(X^*\partial^\mu X-X\partial^\mu X^*),\qquad
 J^\mu=j_\Phi^\mu+2j_X^\mu .                                \tag{2}
\]

The field equations, with real g, give the local transfer equations

\[
 \partial_\mu j_\Phi^\mu=-4g\,\operatorname{Im}(X^*\Phi^2),
 \qquad
 \partial_\mu j_X^\mu=2g\,\operatorname{Im}(X^*\Phi^2),
 \qquad \partial_\mu J^\mu=0.                               \tag{3}
\]

Thus two independently source-free dual currents would be incorrect when
conversion is active. It is their weighted sum that can be dualized as a
closed current without retaining a conversion source.

On a smooth phase chart write

\[
 \Phi=f e^{-i\theta},\quad X=h e^{-i(2\theta+\delta)},\quad
 A=f^2+4h^2>0,\quad
 a_\mu={2h^2\over A}\partial_\mu\delta .                    \tag{4}
\]

Take f,h>0 for this chart; zeros and vortices need separate patches. Direct
completion of the phase square gives

\[
 \mathcal L=\mathcal L_0+A(\partial\theta+a)^2,\qquad
 \mathcal L_0=(\partial f)^2+(\partial h)^2+
 {f^2h^2\over A}(\partial\delta)^2-V(f,h,\delta),
 \quad V_{\rm conv}=2ghf^2\cos\delta,                        \tag{5}
\]

\[
 J^\mu=2A(\partial^\mu\theta+a^\mu).
\]

An equivalent first-order action on that chart is

\[
 \mathcal L_1=\mathcal L_0-{J_\mu J^\mu\over4A}
                    +J^\mu(\partial_\mu\theta+a_\mu).       \tag{6}
\]

Varying J gives (5); varying the smooth common phase gives (3). The relative
phase and both amplitudes remain dynamical. No phase locking, condensate,
equation of state, or positivity of J^0 was assumed in this algebra. Applying
it as a nonsingular global phase-only description of the zero-field vacuum
or of a neutral incoherent bath would be an additional, generally invalid,
step.

## 2. Local duality, normalization, and what density it represents

On an oriented contractible spacetime patch, a smooth conserved J has a
two-form potential B, unique only up to gauge and possible global sectors:

\[
 J^\mu={1\over2}\epsilon^{\mu\nu\rho\sigma}
                         \partial_\nu B_{\rho\sigma}
       ={1\over6}\epsilon^{\mu\nu\rho\sigma}H_{\nu\rho\sigma},
 \quad H=dB,\qquad
 B_{\mu\nu}\longmapsto B_{\mu\nu}
                      +\partial_\mu\Lambda_\nu-
                       \partial_\nu\Lambda_\mu .             \tag{7}
\]

The proof is local: the charge-current three-form is closed by (3), and a
closed three-form on a contractible patch has a primitive. Conversely,
antisymmetry in (7) makes its divergence identically zero. Dropping the
smooth-phase boundary term in (6), the dual action is

\[
 \mathcal L_B=\mathcal L_0-{J(B)^2\over4A}+J(B)\cdot a .      \tag{8}
\]

Conversely, the B equation makes the one-form J/(2A)-a closed; on this
contractible patch it equals d theta and recovers (5). Thus conservation
alone has not silently replaced the original potential-flow equation.
This is a local classical change of variables with the stated chart and
boundary restrictions. It is not a globally complete quantum path-integral
equivalence without measure, compactness, and defect sectors. Every displayed
bulk occurrence of B in (8) is differentiated.

In Cartesian Euclidean space set

\[
 Q_i={1\over2}\epsilon^{ijk}B_{jk},\quad C_i=B_{0i},\quad
 P_i=mQ_i,\quad {cal A}_i=mC_i .                            \tag{9}
\]

The coefficient and time-component signs are fixed, not adjustable:

\[
 J^0=\nabla\cdot Q,\qquad
 \mathbf J=-\dot Q+\nabla\times C,\qquad
 \rho_Q\equiv mJ^0=\nabla\cdot P,\qquad
 \mathbf j_Q\equiv m\mathbf J=-\dot P+\nabla\times{\cal A}.
                                                                    \tag{10}
\]

Gauge transformations act as

\[
 P\longmapsto P+m\nabla\times\boldsymbol\Lambda,
 \qquad {\cal A}\longmapsto{\cal A}
       +m\dot{\boldsymbol\Lambda}-m\nabla\Lambda_0 .          \tag{11}
\]

Both expressions in (10) are invariant. The continuity equation for rho_Q
is an identity. There is no identity rho_Q>=0. The dimensions in mass units
are [J]=3, [B]=2, [P]=3 and [rho_Q]=4; K P has acceleration dimension when
[K]=[4 pi G]=-2.

With a charge-one phase of period 2 pi, a conventional compact two-form b
has surface holonomy exp(i integral b) and b=2 pi B. Then

\[
 J^\mu={1\over4\pi}\epsilon^{\mu\nu\rho\sigma}
                        \partial_\nu b_{\rho\sigma},\qquad
 N=\int J^0d^3x={1\over2\pi}\int db .                       \tag{12}
\]

For a vortex sheet the singular phase produces, with a fixed orientation,
the coupling integral_sheet b=2 pi integral_sheet B; this fixes the
normalization together with the integer winding. A charge-two-only
condensate leaves a residual Z_2 and changes the minimal vortex sector, so
one cannot import the charge-one winding convention without checking that
sector. Compact quantum charge quantization does not quantize the classical
expectation of charge in an arbitrary open subvolume.

On a curved spatial slice the corresponding statement is
D_i P^i=m n_mu J^mu with
P^i=m epsilon_symbol^{ijk}B_jk/(2 sqrt(h)); a coordinate divergence without
the spatial volume factor is not a proper density.

## 3. Positive mass is a separate condition, violated by the produced bath

At leading nonrelativistic order, resolve particle and antiparticle number
densities n_{Phi+}, n_{Phi-}, n_{X+}, n_{X-}. The actual charge and positive
rest density are

\[
 J^0=n_{\Phi+}-n_{\Phi-}+2(n_{X+}-n_{X-}),\qquad
 \rho_{\rm rest}=m(n_{\Phi+}+n_{\Phi-})
                    +M(n_{X+}+n_{X-}).                      \tag{13}
\]

Their exact difference at this order is

\[
 \rho_{\rm rest}-mJ^0
   =2m n_{\Phi-}+(M-2m)n_{X+}+(M+2m)n_{X-}.                 \tag{14}
\]

For the selected M^2=4m^2(1+u_*^2), M>2m when u_* is nonzero. Equality
therefore requires no antiparticles and no occupied X, or the additional
threshold approximation M=2m on an antiparticle-free branch. Even then,
the exact stress-energy source contains kinetic, interaction, gradient,
mediator, and gravitational energy rather than just the leading rest
density. The conserved signed current is not a substitute for T_{mu nu}.

The produced neutral process h -> X X* -> 2 Phi + 2 Phi* has zero net charge
and positive mass. In its locally charge-symmetric state J^0=0 while
rho_rest>0. Consequently (10) cannot represent its positive mass as
div P with P the dual of this Noether current. A total particle-plus-
antiparticle count is also not this exact microscopic symmetry; number-
changing processes need their own controlled suppression or source law.

For a reaction progress rate R for X -> 2 Phi on the particle branch,
dot n_X=-R, dot n_Phi=2R, so

\[
 \dot J^0=0,\qquad
 \dot\rho_{\rm rest}=(2m-M)R.                               \tag{15}
\]

The released detuning energy has to appear in kinetic, field, or outgoing
energy. Charge conservation alone neither supplies its receiver nor makes
the two positive rest-mass stocks separately conserved.

A separately specified charged host plus real scalar mediator has the
same issue in a milder form. Its host number can be conserved and dualized,
and rho_0=m_0 n can be a conserved reference mass density. If the physical
rest energy per host is m(s), then
partial_t[m(s)n]+div[m(s)n v]=n D_t m(s); scalar energy and flux complete
the energy balance. A neutral mediator carries no host charge, although
its energy gravitates. Dualizing a conserved energy current in a stationary
background is possible as a different construction; it does not identify
that current with the common phase current or generate a constitutive W.

## 4. A constructive single-host nonrelativistic dual with gravity

For comparison, assume a single antiparticle-free Schrödinger host of fixed
mass m, density n>0, phase vartheta, density energy epsilon(n), and Newtonian
potential U. The canonical phase action, including quantum pressure, is

\[
 \mathcal L_{\rm NR}=-n\dot\vartheta
       -{n\over2m}|\nabla\vartheta|^2-\epsilon(n)-mnU
       -{|\nabla n|^2\over8mn}.                            \tag{16}
\]

This follows directly from psi=sqrt(n)exp(i vartheta) in the symmetrized
Schrödinger kinetic action. Introduce its number flux j with

\[
 \mathcal L_1=-n\dot\vartheta-\mathbf j\cdot\nabla\vartheta
       +{m|\mathbf j|^2\over2n}-\epsilon(n)-mnU
       -{|\nabla n|^2\over8mn}.                            \tag{17}
\]

Eliminating j returns (16), while varying vartheta gives number continuity.
Use (10), with rho=mn, to obtain the local dual action

\[
 \mathcal L_{\rm dual}=
 { |\dot P-\nabla\times{\cal A}|^2\over2\rho}
       -e(\rho)-\rho U-{ |\nabla\rho|^2\over8m^2\rho},
 \qquad \rho=\nabla\cdot P>0,
 \quad e(\rho)=\epsilon(\rho/m).                           \tag{18}
\]

The apparent singularity at rho=0 is the polar-coordinate vacuum boundary
of this hydrodynamic chart, not an equation authorizing a freely varied
negative density. A free edge requires the original field or a justified
weak/variational extension; (18) alone is not CE082's smooth-edge theorem.
Varying cal A imposes curl v=0 on this defect-free chart. The kinetic term
is fixed by the density and includes cal A; a constant-inertia dot P^2
term by itself is not the exact result.

Add the Newtonian action

\[
 \mathcal L_U=-{|\nabla U|^2\over2K}-\rho_bU,
 \qquad K=4\pi G.                                         \tag{19}
\]

Then Delta U=K(rho_b+rho). The host coupling is equivalently

\[
 -\rho U=P\cdot\nabla U-\nabla\cdot(UP).                   \tag{20}
\]

This does derive the reciprocal Newtonian density coupling, with the
boundary term retained until its boundary conditions are imposed. Its
gauge variation is a boundary term. It does not derive an additional local
W(P). For e=kappa rho^2/2, the material energy is
kappa(div P)^2/2; it is not kappa|P|^2/2. Static variation without quantum
pressure gives e'(rho)+U=constant in each connected occupied component.
This is a derived hydrostatic response and still needs an occupied state,
its equation of state, supply, initial data, and a conversion/energy law.

## 5. Exact gauge obstruction to a bare W and its possible completions

The CE082 constitutive choice is

\[
 W(p)={-a_0u-a_0^2\log(1-u/a_0)\over K},\qquad
 u=Kp,\quad p=|P|<a_0/K,
 \qquad W_p={a_0Kp\over a_0-Kp}.                           \tag{21}
\]

A dual-potential interpretation requires invariance under (11). For
compactly supported Lambda its infinitesimal variation is

\[
 \delta\int W(|P|)\,d^3x
    =m\int\boldsymbol\Lambda\cdot
                      [\nabla\times W_P]d^3x.              \tag{22}
\]

This is not identically zero. The smallest local counterexample starts at
P=0 and uses Lambda_z=c y/m inside a patch, giving delta P=(c,0,0) and
unchanged zero charge density. A smooth cutoff gives a compactly supported
pure gauge on the whole space, still with div delta P=0. For nonzero
sufficiently small c, the rational W has strictly positive energy on part
of this pure gauge configuration, whereas its initial value was zero.
The gauge parameter can be scaled to stay below saturation everywhere.
The fixed-stock sector and boundary falloffs are unchanged. The same issue
affects |grad P|^2; allowed local spatial terms instead include (div P)^2
and its derivatives. Time derivatives must enter the current combination
in (18), or other explicitly gauge-invariant combinations.

This counterexample refutes deriving (21) as a local bulk functional of
the current's dual potential. It does not refute an independent physical
polarization field already assigned constitutive energy by another model.
Several logically different constructions remain possible:

1. **Fix the longitudinal representative.** With isolated boundary data,
   P_L=grad Delta^{-1} rho. Defining W on P_L is gauge invariant but nonlocal
   in the microscopic density. Already the quadratic term is

   \[
   \int W(|P_L|)= {K\over2}\int{d^3k\over(2\pi)^3}
                 {|\rho_k|^2\over k^2}+O(P_L^3).            \tag{23}
   \]

   Its functional derivative is
   -Delta^{-1} div[W_P(P_L)], with the chosen inverse and boundary data.
   Thus simply applying a local e(rho) chemical potential is incorrect.
   A new positive 1/k^2 interaction kernel is a matching obligation. The
   original massive scalar contact sector does not supply it by a change
   of current variables. Newtonian self-gravity supplies the opposite
   quadratic kernel, -K integral|P_L|^2/2. The matching of the first term
   of (21) to its cancellation is a physical tuning condition.

2. **Introduce a physical mediator displacement.** The convex constrained
   energy min_{div P=rho} integral W(|P|) has a local scalar-potential dual
   if W is inserted as constitutive input. Its Legendre partner is

   \[
   F(E)=W^*(E)={a_0E-a_0^2\log(1+E/a_0)\over K},\quad
   p=F'(E)={a_0E\over K(a_0+E)},\quad E=W'(p).              \tag{24}
   \]

   For example, the auxiliary extremum of
   integral[W(P)-s(div P-rho)] gives W_P+grad s=0 and
   div[F'(|grad s|) grad s/|grad s|]=-rho. Here P is a physical
   displacement of this new mediator, not an arbitrary B potential.
   An electric displacement can have precisely this status under a
   one-form mediator's Gauss law. Its source is signed gauge charge; an
   extra charged-population condition is again needed for positive mass.
   A canonical scalar gradient energy gives a quadratic Legendre partner,
   not (24); nonlinear F, its scale a0, sign, health, coupling, and source
   assignment remain new microscopic obligations. The constrained
   convex energy alone does not establish the healthy sign of a full
   propagating relativistic scalar action.

3. **Retain extra compensating fields.** Gauge-invariant combinations
   B-dC can support undifferentiated constitutive terms if C transforms
   with Lambda. Unless those fields are already derived and matched,
   this adds a physical sector or a redundancy completion; the common
   phase duality (6)-(8) does not generate it.

Spherical symmetry does not remove this issue. In a chosen regular radial
representative P_r=M_Q(r)/(4 pi r^2), (21) is a possible functional of the
enclosed charge. That radial rewriting is nonlocal in density, depends on
the physical center and boundary prescription, and supplies no nonspherical
gauge-invariant local completion by itself.

## 6. Boundary, topology, and finite stock

For a smooth localized density on R^3, (10) gives

\[
 S_Q=\int\rho_Qd^3x
       =\lim_{r\to\infty}\oint_{S_r}P\cdot d\mathbf S.
                                                                    \tag{25}
\]

In a regular radial representative, P_r=S_Q(r)/(4 pi r^2); positive finite
stock therefore has an exterior S_Q/(4 pi r^2) tail even when the material
density has a compact edge. Requiring compact support of P or P=o(r^-2)
would force zero total stock. Outside a finite source, the associated
spatial B is closed and carries its surface period; that period cannot be
removed by a smooth globally defined gauge transformation. Fixing the
stock fixes this boundary flux and requires delta S_Q=0 in variations.
It does not forbid the compact pure gauge counterexample in section 5.

On a closed compact spatial three-manifold a single global smooth B with
H=dB has integral H=0 by Stokes. Nonzero total charge needs a prescribed
cohomology/flux sector H=H_top+dB or patchwise two-form connections. The
general local potential argument never supplies those sectors or chooses
their charge. On a noncompact domain the nonzero charge can instead be
carried by boundary behavior as in (25). A homogeneous positive density
likewise needs growing/background B or a compact flux sector; it cannot
be represented by a decaying periodic primitive with zero background.

## 7. Dependency and obligation audit

| Arrow / obligation | Basis | Status |
|---|---|---|
| Cubic conversion -> one weighted conserved U(1) current | Scalar Euler equations (1)-(3) | Passed |
| Common smooth phase -> first-order dual action | Square completion (4)-(8), A>0 chart | Passed with chart/boundary restriction |
| Conserved current -> local B potential | Closed current three-form; contractible patch | Passed locally; global sector conditional |
| mJ^0 -> positive inertial density for original bath | Required identification (13) | Failed by neutral population (14) |
| NR positive single host -> div P density and gravity coupling | Fixed-mass NR assumptions (16)-(20) | Passed within stated approximation |
| Bare W(|P|) -> dual-gauge-invariant local energy | Gauge transformation (11) | Failed by compact pure gauge |
| Longitudinal W -> local density EOS | Inverse Laplacian (23) | Failed; nonlocal kernel is explicit |
| Constitutive W -> scalar Legendre formulation | Convexity below saturation (24) | Passed conditionally on inserting W |
| Microscopic particle action -> rational W, a0 and healthy mediator | No matching supplied | Not established |
| Boundary flux -> finite available positive cosmic stock | Flux identity (25) only | Not established |

External literature is recorded in SOURCE_RECORD.md. The internal algebra
was independently derived here; the external source verifies the standard
restricted phase/two-form relationship, not its application to the original
neutral bath or the rational W. There is no novelty claim, no ledger update,
and no claim of independent review. The exact finite symbolic checks and
their limits are in contract.json, check_exact.py, and run_002/manifest.json
(30 exact residual assertions; completed and validated against current code).
The failed first run is retained: it required a logarithmic positivity
assumption absent from its symbolic p parameter. Run 002 parametrizes the
physical domain by E>0 and p=a0 E/[K(a0+E)] without changing the formulas.

The older reciprocal_anchor_2026_10_13/COUPLED_RESULT.txt section 4 concerns
an independently introduced actual/reference split Jbar=J-div B_pol, its
quadratic reference EOS, and a standalone scalar rewrite. Its own text
states that the standalone scalar pulse is not inherited by the combined
parent. That auxiliary polarization construction does not identify
B_pol with this microscopic common-phase dual B, and supplies no missing
positive-mass or rational-W implication here.

The cheapest remaining microscopic discriminator is a matched static kernel
and source assignment for an actual occupied charge-resolved state. A
positive 1/k^2 kernel with the coefficient in (23), a justified nonlinear
continuation (24), and a positive-mass/current dictionary would be needed
before substituting the current dual into CE082's full constitutive action.
Charge duality alone satisfies none of those three obligations.
