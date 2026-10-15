# Independent audit of the regular-source fluid/gauge energy join

JA-001, 15 October 2026. Independent subagent derivation from the proposed
background and the raw constitutive actions in `../inputs/RTM_REPORT.md` and
`../inputs/MC_MODES_PROOF.md`. Initial repository checkpoint:
`283acbcffe1c6c4a5e8f9860f66e43c4e3808ab3`.

**Normalized claim.** On all of Euclidean space, let a neutral barotropic
current define the varied constitutive frame, with the stated electric action
and a magnetic term `-beta(E,n) B_U^2/2`. Let both external source densities be
fixed in time, let their spatial gauge current vanish, and retain Newtonian
self-gravity sourced by the neutral rest density. About an actual static,
pure-electric, hydrostatic background, the constrained quadratic energy is the
sum of positive gauge/current squares and the ordinary fluid density Hessian
including Newtonian self-gravity. Spatially varying background coefficients
do not by themselves add an indefinite potential term to that energy.

**Primary verdict: correct only after a stated restriction.** The join is
valid for this explicitly specified Newtonian-gravity constitutive comparison,
with the density/current constraints and boundary hypotheses below. It is not
the full constrained Einstein/matter Hessian, a nonlinear stability theorem,
or a uniformly controlled radiation/vacuum completion. No negative quadratic
mode caused by the proposed inhomogeneous join was found. A missing term does
arise if one substitutes `-rho div xi` for the actual density variation, or
expands the electric energy in unconstrained `E` without implementing Gauss
law; neither substitution is justified here.

Two restrictions are substantial: the unchanged magnetic response does not
provide a differentiable nonlinear action on an open field neighborhood of
the center's `F=0`, and finite-amplitude outgoing radiation need not stay on
the admitted dilute-tail branch. The quadratic energy claim survives these
limitations; a global nonlinear health claim does not follow from it.

## 1. Background and retained gravitational approximation

Write `rho_bar` for the neutral rest density, `n_s` for its particle number
density, and use `c=1` below. The polytropic index is five, not `n_s`:

\[
 P=K\rho^{6/5},\qquad \epsilon=\rho+5K\rho^{6/5},\qquad
 u(\rho)=5K\rho^{6/5},\qquad h=\rho+6P.
\]

The fixed external mass and charge have enclosed profiles proportional to
`r^3/(r^2+b^2)^(3/2)`. The neutral proposed equilibrium is

\[
 \bar\rho(r)=\frac{3fM_0b^2}{4\pi(r^2+b^2)^{5/2}},\quad
 \Phi_0=-\frac{GM_0}{\sqrt{r^2+b^2}},\quad
 \bar\Phi_s=-\frac{GfM_0}{\sqrt{r^2+b^2}},\quad
 6K\bar\rho^{1/5}=-\Phi_0-\bar\Phi_s=:\Psi.
\tag{1}
\]

The static constitutive first variation with respect to `U` is zero at
`B_U=0`: `E^mu F_mu nu` is parallel to `U_nu`, while `U.delta U=0`.
The first variations of the magnetic term also vanish. Thus no additional
static neutral force has been omitted in (1). In particular, neutrality
removes minimal gauge force but does not remove the quadratic frame inertia.

The gravitational functional being audited is

\[
 V[\rho]=\int[u(\rho)+\rho\Phi_0]d^3x
 -\frac G2\iint\frac{\rho(x)\rho(y)}{|x-y|}\,d^3x\,d^3y.
\tag{2}
\]

Rest energy is constant on a fixed-rest-mass variation. Equation (1) gives
`V_rho=u'(rho_bar)+Phi0+Phi_s_bar=0` everywhere. This model retains rest mass
as the Newtonian gravitational source. Gravitating electric energy, internal
energy and pressure, lapse/metric perturbations, and the external sources'
motions require a different Hessian. Small compactness and a small omitted
field-energy gravitational budget are conditions for interpreting this
comparison as a controlled weak-field approximation; they are not proved by
the algebraic join alone.

More precisely, the retained hybrid variational comparison uses the flat
relativistic current and constitutive action for its kinematic terms, while
coupling the Newtonian potential to the *conserved lab rest density*
`rho_L=m_s N_s^0`. In addition to the neutral-current Clebsch action and the
constitutive action, its terms are

\[
 -\rho_L(\Phi_0+\Phi_s)-\frac{|\nabla\Phi_s|^2}{8\pi G}
 +j_{\rm ext}^{\mu}A_\mu,
 \qquad \Delta\Phi_s=4\pi G\rho_L,
 \qquad j_{\rm ext}^{i}=0.
\tag{2a}
\]

This defines internally the retained enthalpy inertia, static functional
(2), and perturbation equations. The neutral current is the **only dynamical
material current and the sole frame-defining current everywhere**, including
inside the overlapping fixed mass/charge profiles. The prescribed charge is
not an implicit charged-core medium contributing additional frame inertia.
This construction is not the exact covariant first integral `mu_s N=const`
in a metric solved from the same `Psi`; metric corrections of order
`P/(rho c^2)` and `Phi/c^2` remain outside this hybrid comparison.

## 2. Admissible first-order variables and constraints

Let `xi` be the neutral material displacement, `v=dot xi`, and `eta` its
Eulerian lab-rest-density variation. Because the background is at rest,

\[
 \eta=-\nabla\cdot(\bar\rho\xi),\qquad
 \dot\eta=-\nabla\cdot(\bar\rho v),\qquad
 \int\eta\,d^3x=0.
\tag{3}
\]

At this order the lab and proper density variations agree. Their second-order
difference is already accounted for by the material enthalpy inertia in the
relativistic current expansion. One cannot use
`eta=-rho_bar div xi` for this atmosphere. The omitted
`-xi.grad rho_bar` is a first-order term, including for rigid translations.

Let `d=delta D`, `b=delta B`, and `e=delta E` denote laboratory gauge
perturbations. For fixed external charge density and vanishing external
spatial current,

\[
 \nabla\cdot d=0,\qquad \nabla\cdot b=0.
\tag{4}
\]

The background obeys `div D_bar=sigma_ext(x)`, not zero. The zero right side
in (4) belongs only to the perturbation. There is no neutral `eta` on its
right side and no neutral minimal-current plasma term. A moving or perturbed
charged source would change this constraint and is outside this claim.

Begin with smooth compactly supported displacements and smooth finite-energy
solenoidal gauge data. Extend the quadratic form only by its weighted-energy
completion with the stated constraints. No artificial inner wall is present.
At the origin use regular three-dimensional fields. At infinity require the
boundary integrations in sections 4 and 6 to vanish, or explicitly retain the
outgoing flux. This is an admissible perturbation class, not a proof of a
global evolution theorem on its completion.

## 3. Pointwise quadratic constitutive expansion

At each point put

\[
 t=\frac{\bar D}{\bar E}=1-x,\quad p=\frac{dD}{dE}=(1-x)^2,
 \quad x=\bar D/D_0<1,\quad \Delta=t-\beta\ge0,
\]
\[
 \varepsilon=tI+(p-t)\hat E\hat E^T,\quad
 M=hI+\Delta(\bar E^2I-\bar E\bar E^T),\quad
 Qb=\Delta\,(b\times\bar E).
\tag{5}
\]

All quantities in (5) are background functions of position. Their displayed
limits at `E_bar=0` remove the apparently undefined direction `E_hat`.
For the chosen response `Delta>0` at `r>0`, with `Delta=0` at the center.
The current-defined frame has first variation `delta U^i=v^i`. Density
variations of that relation first affect `U^i` at second order and multiply
the vanishing first frame derivative of the constitutive action. Thus they
do not add a quadratic `eta e` or `eta v` term.

The quadratic action, after the standard barotropic current reduction, is

\[
 L_2=\int\left[
 \frac12 e^T\varepsilon e+\frac12v^TMv+v\cdot Qb
 -\frac12\beta |b|^2\right]d^3x-Q_f[\eta],
\tag{6}
\]
\[
 Q_f[\eta]=\frac12\int w\eta^2d^3x
 -\frac G2\iint\frac{\eta(x)\eta(y)}{|x-y|}d^3x\,d^3y,
 \qquad w=u''(\bar\rho)=\frac{\Psi}{5\bar\rho}>0.
\tag{7}
\]

Equation (6) is a pointwise Taylor expansion of an action with no derivatives
of `U`; it does not freeze the spatial coefficients. No `grad E_bar` term is
generated by that Taylor expansion. Coefficient gradients appear when its
Euler equations are differentiated in space.

For the magnetic term,

\[
 \mathcal B_U^2=O((b,v)^2),\qquad
 \beta(\mathcal E,n_s)=\bar\beta+O(e,\eta,v),
\]

so every `beta_n` or `beta_E` contribution starts at cubic order. Their
absence is specific to `B_U_bar=0`. A magnetic background or electric action
`L_e(E,n_s)` would require a new derivation and would generally introduce
density couplings. This argument does not discard spatial derivatives of
the *background value* `beta_bar` in the linear gauge equations.

## 4. Constrained Hamiltonian and background first variations

The linear momenta are `d=epsilon e` up to the conventional sign of the
potential momentum, and `pi_xi=Mv+Qb`. Legendre transformation of (6) gives

\[
 \boxed{\quad H_2=\frac12\int\left[
 d^T\varepsilon^{-1}d+
 (\pi_\xi-Qb)^TM^{-1}(\pi_\xi-Qb)+\beta |b|^2\right]d^3x
 +Q_f[\eta].\quad}
\tag{8}
\]

This is a local positive-square expression restricted to the nonlocal
constraint subspace, not a claim that all physical potential variables have
independent local coordinates. With `beta>0`, `p,t>0`, and `h>0`, its displayed
integral term is nonnegative. `Qb` cannot be dropped in canonical momenta. In
velocity variables the same integral is
`(e.epsilon.e+v.M.v+beta b^2)/2`.

There are two useful checks that (8) has not omitted an inhomogeneous
background term.

**Electric background.** Use the canonical displacement `D`, for which Gauss
law with fixed source is affine. On every exact admissible path `D_lambda`,

\[
 \int\bar E\cdot(D_\lambda-\bar D)d^3x
 =-\int\nabla\bar\phi\cdot(D_\lambda-\bar D)d^3x=0.
\tag{9}
\]

This uses (4) and the vanishing boundary term. It removes first-order terms
and the first derivative paired with a second-order path correction. A naive
unconstrained Hessian of the electric energy written as a function of `E`
instead of `D` contains extra `E_bar d epsilon/dE` terms; (9), including
second-order Gauss, is essential to their cancellation. This is a genuine
constraint issue, not an assumption that the source or field is uniform.

**Fluid background.** Along a mass-conserving material path `rho_lambda`,
the first derivative of (2) is a spatial constant at equilibrium. Its pairing
with every first- or second-order mass variation vanishes. Thus the
quadratic coefficient on the material path is exactly (7), with (3). In a direct
displacement expansion, tidal and background-pressure-gradient terms combine
to this expression; retaining some of them a second time would double count.

Global elimination of the electric potential also preserves positivity.
With `e=-dot a-grad phi`, the linear Gauss equation is the variable-coefficient
elliptic equation `div[epsilon(dot a+grad phi)]=0`. Its solution minimizes the
positive electric quadratic functional over `phi`. For a fixed global bound
`x_max<1`, `epsilon >= (1-x_max)^2 I`; this reduction cannot generate a
negative kinetic term. A frozen Fourier `K_A` is not needed for this step.

## 5. A direct sufficient density-Hessian bound

This section independently checks a sufficient stability input; it is not
needed merely to identify the join. Equation (1) implies

\[
 G\int\frac{\bar\rho(y)}{|x-y|}d^3y
 =\frac{GfM_0}{\sqrt{r^2+b^2}}
 =\frac{5f}{1+f}\,w(x)\bar\rho(x).
\tag{10}
\]

Use `2|eta(x)eta(y)| <= eta(x)^2 rho_bar(y)/rho_bar(x)
+ eta(y)^2 rho_bar(x)/rho_bar(y)` in the symmetric Newton kernel. It gives

\[
 G\iint\frac{|\eta(x)\eta(y)|}{|x-y|}d^3x\,d^3y
 \le\frac{5f}{1+f}\int w\eta^2d^3x,
\]
\[
 Q_f[\eta]\ge\frac12\frac{1-4f}{1+f}
                  \int w\eta^2d^3x.
\tag{11}
\]

Consequently `0<f<1/4` is an explicit sufficient condition for a positive
density block, even on the larger space before imposing zero total mass.
Together with (8), this proves a nonnegative conserved quadratic energy of
the retained fluid/gauge comparison, for solutions on which the stated
integrations are justified. It does not establish instability for
`f>=1/4`. In particular, the equality direction of this Schur bound is
proportional to `rho_bar` and does not conserve total mass.

Here `w=4 pi G(1+f)(r^2+b^2)^2/(15 f b^2)`, so `w~r^4` at infinity.
Finite `int w eta^2` implies `eta` is integrable because `int 1/w` is finite.
Thus zero total mass is a meaningful closed restriction in this density norm.

## 6. Direct energy identity: coefficient gradients and source work

Define `delta Phi=-G int eta(y)/|x-y| dy` and
`chi=w eta+delta Phi`. The linear equations from (6) include

\[
 \partial_t(Mv+Qb)=-\bar\rho\nabla\chi,\qquad
 \dot\eta=-\nabla\cdot(\bar\rho v),
\]
\[
 \dot d=\nabla\times(\beta b-Q^Tv),\qquad
 \dot b=-\nabla\times e,\qquad d=\varepsilon e.
\tag{12}
\]

The background coefficients in (12) are time independent but fully spatially
varying. Multiply the first equation by `v`, use the continuity equation in
the derivative of (7), and pair the two gauge equations with `e` and `beta b`.
Integration by parts cancels both `int v.Q.dot b` terms and both
`int rho_bar v.grad chi` terms. Hence `dot H2=0` when the boundary fluxes
vanish. In particular, `curl(beta b-Q^T v)` retains the derivatives of
`beta`, `Delta`, and `E_bar`; these derivatives do not leave a bulk source of
quadratic energy. This is a direct verification beyond a frozen principal
symbol.

The external charged source contributes power proportional to
`j_ext.E`. Its spatial current is identically zero, so its electromagnetic
power is zero. Its holder can supply a changing force at zero velocity
without supplying power. The fixed gravitational potential contributes no
explicit time derivative. This justifies conservative perturbation energy
for *these* prescribed sources; it says nothing about a dynamical charged
core, a force-responsive holder, charge injection, or a moving source.

Boundary hypotheses can be stated as the vanishing of the gauge surface
integral of `e cross (beta b-Q^T v)`, the fluid integration term involving
`rho_bar v chi`, and the usual Poisson integration-by-parts terms. Smooth
compact initial data with enough decay are a clean starting class. On all
space, finite-energy radiation can be included with the corresponding
asymptotic flux bookkeeping. For an exterior control volume, outward
radiation flux makes the energy inside decrease; incoming radiation is an
energy input. A finite material truncation with nonzero background pressure
would be a different boundary problem and cannot silently replace (1).

## 7. Limits that remain material

1. **No uniform vacuum or nonlinear theorem.** Here `rho_bar~r^-5`, while
   `hcrit(E_bar)~r^-6`. Every finite radius is occupied, but inertia tends to
   zero. The energy norm does not force a small perturbation to remain small
   relative to `rho_bar` everywhere. Density derivatives of `beta` absent
   from (8) can grow in the tail and matter at higher order. A branch defined
   only for `h_eff>hcrit(E)` need not contain any uniform global nonlinear
   neighborhood of this atmosphere.
2. **Radiation illustrates the limitation.** For a finite-amplitude outgoing
   wave with electric amplitude proportional to `r^-1`, its own small-field
   `hcrit` scales like `r^-3`, whereas the unperturbed material inertia is
   proportional to `r^-5`. Such a wave can eventually leave the admitted
   finite-density constitutive branch. This does not make (8) negative and
   is not a quadratic instability; it prevents inferring a global nonlinear
   radiation solution from the background's local gate.
3. **Zero displacement modes remain.** `div(rho_bar xi)=0` gives zero density
   potential energy. The energy controls currents and density, not every
   displacement label; polynomial displacement drift is not excluded.
4. **Center regularity is limited by the chosen response.** The smooth
   source gives `D_vector=O(r_vector)`, and `E_vector` is finite and C1 at the
   origin. Because `L_e` contains a `|E_vector|^3` Taylor term, it is C2,
   rather than C-infinity, as a vector-field function there; spatial
   constitutive Hessians can be only Lipschitz. This does not invalidate the
   quadratic form or its weak energy identity, but a theorem requiring a
   smooth classical background must address it. There is a stronger
   off-shell issue for the unchanged magnetic response: at fixed positive
   density, `beta=1-2|E_U|/D0+O(|E_U|^2)`. Hence its action contains
   `+|E_U| B_U^2/D0`. This is not differentiable in the electric vector at
   `E_U=0, B_U!=0`, however small `B_U` is. Such points occur in every open
   field neighborhood of the center. The term is cubic at `E_U=B_U=0`, so
   its background quadratic Taylor form exists, but a C1 nonlinear action
   neighborhood has not been supplied.
5. **Gravity is only the stated comparison.** Including perturbed metric
   constraints and the electric/material stress in the gravitational source
   adds density/gauge/metric terms absent from (2). Smallness or a positive
   margin in (11) does not supply their signs automatically. Physical
   identity, EOS, abundance, source equilibrium and microscopic completion
   are separate inputs.

## 8. Audit of the actual regular-core proof and checks

After deriving (3)-(12), this audit read the actual bytes of
`../regular_core/PROOF.md`, `check_regular_core.py`, and the separate
`check_regular_core_v2.py`. No correction to the regular-core algebra was
needed. The exact audited hashes, including the historical and final run
manifests, are recorded in `SOURCE_HASHES.txt`.

For fixed `K,M0,b`, the EOS normalization gives
`mu=f/(1+f)^5`, with derivative `(1-4f)/(1+f)^6` and maximum
`256/3125` at `f=1/4`. This weak branch is consistent with the sufficient
positive density-Hessian interval proved independently in (11). It does
not predict the stock or establish instability of the other branch.

For the gauge normalization, introduce
`q0=G M_Q/(a0 b^2)`, `gamma_Q=M_Q/M0`, `epsilon0=G M0/(b c^2)` and `t=r/b`.
Direct substitution, including `D0^2=a0^2/(4 pi G)`, gives

\[
 x=q_0\frac{t}{(1+t^2)^{3/2}},\qquad
 \frac{h_{\rm crit}}{\bar\rho c^2}
 =\frac{\epsilon_0\gamma_Q^2q_0}{3f}
   \frac{t^3}{(1+t^2)^2(1-x)^2}.
\tag{13}
\]

The maxima `x_max=2q0/(3 sqrt(3))` and
`max t^3/(1+t^2)^2=3 sqrt(3)/16` follow by direct differentiation at
`t=1/sqrt(2)` and `t=sqrt(3)`, respectively. The sufficient all-radius
bound in the root proof, including its factor `sqrt(3)/16`, is correct.
For `q0=gamma_Q=1/2`, `epsilon0=10^-6`, `f=10^-3`, the stricter rational
envelopes `x<1/5` and `t^3/(1+t^2)^2<1/2` give

\[
 \frac{h_{\rm crit}}{\bar\rho c^2}<\frac{25}{768000},\qquad
 \frac{h_{\rm eff}}{h_{\rm crit}}>30720,\qquad
 \frac{5f}{1+f}=\frac5{1001}<1.
\tag{14}
\]

Here `h_eff=rho c^2+(24/5)P >= rho c^2`; the relativistic EOS sound
fraction is `Psi/[5(c^2+Psi)]`, distinct from Newtonian `c_s,N^2=Psi/5`.
The center has `hcrit=0` and the quadratic Maxwell limit; (14)'s ratio is
understood for `r>0`. The limit itself does not repair section 7's nonlinear
center differentiability problem.

The computation contract uses exact positive-parameter symbolic identities
and rational inequalities, plus three 60-digit shell-potential quadratures
at `r/b=0.1,1,10` with error threshold `10^-45`, and seven positive rational
gate samples. The final script adds two useful independent checks to the
historical version: the EOS normalization is checked before taking a fifth
root, and the normalized ratio (13) is derived from the dimensional
`D0`, `x`, and density definitions. The source uses no random sampling or
hidden radial cutoffs. Its shell-potential substitution has the correct
`rho(1/y)/y^3` outer integrand. The original Schur-coefficient identity is
algebraically redundant by itself, but the analytic kernel proof and Poisson
profile checks supply the needed nonnumerical implication.

Existing final run output reports **19 exact identities, three potential
quadratures, and seven local-gate samples**. Its manifests are checked
against the actual input/output hashes by the validation commands recorded
in `SOURCE_HASHES.txt`; this is an audit of the existing run, not a claim
that a new independent simulation was run. Passing the bounded quadratures
and samples does not prove an all-radius assertion. Equations (10)-(14)
provide the direct uniform argument.

## 9. Dependency and obligation record

The dependency chain is: neutral-current constitutive action and fixed
sources -> static current equation plus constrained Taylor expansion ->
(6)-(9) and exact energy identity (12); independently, the explicit
Euler-Poisson background -> positive-kernel inequality (10) -> bound (11).
Their join is (8) on the perturbation domain (3)-(4). The field-stress and
metric extension, nonlinear tail domain, and center action regularity are
not leaves supplied by either chain.

| Obligation | Result | Evidence |
|---|---|---|
| Actual neutral rest background obeys its material equation | Passed for (1) in the retained Newtonian model | Static frame first variation; `u'+Phi0+Phi_s=0` |
| Correct inhomogeneous density/current perturbation | Passed | Equation (3), mass-conserving displacement |
| Fixed-source Gauss law and its second-order path terms | Passed with boundary restriction | Equations (4), (9) |
| Density derivatives of magnetic response at `B=0` | Passed | Cubic-order Taylor count in section 3 |
| Reciprocal boost inertia and magnetic mixing | Passed | Equations (5), (6), retained `Qb` momentum shift |
| Inhomogeneous gradient/source-work terms in the quadratic energy | Passed for stationary prescribed sources and stated fluxes | Direct energy identity (12) |
| Positive density block for `0<f<1/4` | Passed as a sufficient condition | Direct symmetric-kernel inequality (10)-(11) |
| Exact gate normalization and rational witness in the root artifact | Passed | Independent dimensional substitution (13)-(14); final check source reviewed |
| Arbitrary `f`, optimal mass-constrained threshold | Not addressed | The Schur sufficient bound is not an instability criterion |
| Full Einstein constraints and relativistic source backreaction | Out of scope | Not present in functional (2) |
| Global nonlinear evolution, uniform tail domain and radiation completion | Not addressed | Explicit tail obstruction in section 7 |

No external theorem or literature result is used in this derivation. No
simulation or sampled spectral calculation was run by this auditor. The raw source copies
are pinned in `SOURCE_HASHES.txt`. The audit read the existing neutral-action
derivation for notation but did not adopt its verdict. Its fluid-energy and
join derivation preceded the later inspection of the parent's actual proof
and computation. It writes only inside `joint_audit/`.

**Strongest safe statement.** With fixed rest sources and the precise
Newtonian gravitational functional (2), a regular all-space polytropic
equilibrium satisfying the pointwise finite-density constitutive gate and
`0<f<1/4` admits the positive quadratic fluid/gauge energy (8), on the stated
constrained finite-energy perturbations. The join itself has no additional
negative background-gradient term, and the energy identity holds for
solutions with the stated regularity and boundary fluxes. The cheapest next discriminator for a
stronger physical claim is an explicitly specified gravitational truncation
including field stress, or an off-shell low-density constitutive completion;
repeating the frozen principal calculation cannot establish either.
