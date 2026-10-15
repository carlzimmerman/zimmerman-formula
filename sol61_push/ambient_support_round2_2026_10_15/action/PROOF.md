# A varied neutral support current admits a finite polytropic exterior

NS-ACTION-001, 15 October 2026. Direct derivation and self-review. Primary
verdict: **conditional on a new neutral species, its EOS and normalization,
the displayed constitutive family, and the specified gravitational background**.
This supplies an on-shell material equation in a prescribed background; it
does not supply a microphysical carrier or a coupled Einstein solution.

The initial repository checkpoint is
`283acbcffe1c6c4a5e8f9860f66e43c4e3808ab3`. Authoritative inherited inputs are
the immutable files `../inputs/MC_MODES_PROOF.md`,
`../inputs/MC_BOUNDARY_PROOF.md`, `../inputs/RTM_REPORT.md`, and
`../inputs/CE053_FINITE_EDGE.txt`, pinned by `../inputs/source_manifest.json`.
The mode proof is conditional local principal analysis, not a theorem about
the full constrained Einstein system.

## 1. Claim and actual species

On the exterior `r >= R0 > sqrt(A)`, let

\[
 A=GM_Q/a_0>0,\qquad D_0=a_0/\sqrt{4\pi G},\qquad
 x(r)=D(r)/D_0=A/r^2\in(0,1).
\]

`M_Q` is the enclosed gauge charge in the old chi-mass normalization. It is
not the neutral support mass, the gravitating central mass `M0`, or a new
charge-to-mass ratio. There is no charged exterior number density. Fixed
enclosed charge and spherical Gauss law therefore give the displayed `D`.

Add one actual neutral conserved number current `N_s`, with positive rest
mass `m_s`, number density `n_s=sqrt(-N_s^2)>0`, rest mass density
`rho=m_s n_s`, and **chosen varied frame** `U=N_s/n_s`. Its minimal gauge
charge is `q_s=0`. The exterior action, in signature `-+++` and `c=1` for
covariant expressions, is

\[
 S=\int\sqrt{-g}\,d^4x\left[
 -\epsilon_s(n_s)+N_s^\mu
 (\partial_\mu\theta_s+\alpha_s\partial_\mu\chi_s)
 +L_e(\mathcal E)-\frac12\beta(\mathcal E,n_s)\mathcal B^2\right],
 \tag{1}
\]

where `E_mu=F_{mu nu}U^nu`, `B_mu=(*F)_{mu nu}U^nu`, and
`mathcal E=sqrt(E_mu E^mu)`. The electric derivative is

\[
 L_e'(\mathcal E)=D=\frac{\mathcal E}{1+\mathcal E/D_0}.
\]

Thus `L_e=D0 E-D0^2 log(1+E/D0)`, with zero constant at zero field.
The neutral support is a new material input. It is neither old charged chi
nor charged S, nor a charge-neutral displacement of those two species. It
contributes real stress, rest mass and gravity. Neutrality of its minimal
coupling does not remove its frame-dependent interactions in (1).

## 2. Why the exact static support equation is ordinary hydrostatics

At fixed metric,

\[
 \delta n_s=-U_\mu\delta N_s^\mu,\qquad
 \delta U^\nu=\frac{\delta^\nu{}_{\mu}+U^\nu U_\mu}{n_s}
                    \delta N_s^\mu,\qquad U\cdot\delta U=0.
 \tag{2}
\]

On a purely electric rest background, `B_mu=0` and

\[
 F_{\mu\nu}=U_\mu E_\nu-E_\mu U_\nu,\qquad
 E^\mu F_{\mu\nu}=-\mathcal E^2 U_\nu.
\]

Consequently the entire first frame variation is

\[
 \delta_U L_e=\frac D{\mathcal E}E^\mu F_{\mu\nu}\delta U^\nu
             =-D\mathcal E U_\nu\delta U^\nu=0. \tag{3}
\]

All first variations of `-beta B^2/2`, including its explicit number-density
derivative, vanish because `B_mu=0`. The result does not assume that `U` is
fixed before variation and does not discard the nonzero quadratic frame
inertia. No density derivative of `L_e` is present in the action chosen here.

Let `mu_s=d epsilon_s/d n_s`, `h_s=n_s mu_s=epsilon_s+P_s`. The current
equation at this background is therefore

\[
 \mu_sU_\mu+\partial_\mu\theta_s+
                 \alpha_s\partial_\mu\chi_s=0.
\]

The label equations advect `alpha_s,chi_s` with `U`. Taking the exterior
derivative and contracting with `U` gives

\[
 \mu_sa_\mu+(\delta_\mu{}^\nu+U_\mu U^\nu)
                         \nabla_\nu\mu_s=0,\qquad dP_s=n_s\,d\mu_s.
 \tag{4}
\]

For a static metric with lapse `N(r)>0`, zero shift and `U=N^{-1}partial_t`,
`a_r=partial_r log N`, so

\[
 \boxed{\quad P_s'=-h_s(\log N)',\qquad \mu_sN=\text{constant}.\quad}
 \tag{5}
\]

There is no `q_s E` force. This is an exact background statement under (1).
The conserved static current `N_s^mu=(n_s/N,0,0,0)` also satisfies its number
conservation equation. Static label potentials can realize the chemical first
integral. The purely electric constitutive stress still gravitates; (3) is not
a license to omit it from the metric equations.

For comparison with the central Newtonian problem, take
`N=1+Phi/c^2+...`, `Phi=-GM0/r`, and nonrelativistic pressure. Then (5) gives
the leading material equation

\[
 P'=-\rho GM_0/r^2. \tag{6}
\]

Below, (6) is treated exactly as a Newtonian comparison equation; retaining
the exact local EOS in the causal gate does not upgrade this background to
an exact covariant or self-gravitating solution.

## 3. Polytropic equilibrium and causal material inertia

Fix `n>0`, `K>0`, `Gamma=1+1/n`, and

\[
 P=K\rho^{1+1/n},\qquad \epsilon_{\rm mat}=\rho c^2+nP. \tag{7}
\]

`n` is the polytropic index, distinct from the number density `n_s`.
The chemical enthalpy per rest mass and the dimensionless sound square are

\[
 \frac{\mu_s}{m_s}=c^2+(n+1)K\rho^{1/n},\qquad
 s^2=\frac{dP}{d\epsilon_{\rm mat}}
    =\frac{(n+1)K\rho^{1/n}}
            {n[c^2+(n+1)K\rho^{1/n}]}.
\]

The inertia entering the inherited single-current principal gate is exactly

\[
 \boxed{\ h_{\rm eff}=h_s(1-s^2)
       =\rho c^2+\frac{(n+1)(n-1)}nP.\ } \tag{8}
\]

For completeness, in any prescribed static lapse tending to one, imposing
`rho -> 0` at infinity integrates the exact chemical equation (5) to

\[
 z=N^{-1}-1,\qquad
 \rho=\left[\frac{c^2z}{(n+1)K}\right]^n,\quad
 \frac P\rho=\frac{c^2z}{n+1},\quad
 h_{\rm eff}=\rho c^2\left[1+\frac{n-1}{n}z\right]. \tag{9}
\]

This requires `z>0` on the occupied exterior. It does not determine `N`.
If `z~GM_infinity/(r c^2)` with positive finite `M_infinity`, its asymptotic
mass and gate exponents are the same as those below.

Integrating (6), with `rho -> 0` at infinity, gives the unique zero-pressure
infinity branch

\[
 (n+1)K\rho^{1/n}=\frac{GM_0}r,\qquad
 \rho=\rho_0(R_0/r)^n,\qquad
 \rho_0=\left[\frac{GM_0}{(n+1)KR_0}\right]^n. \tag{10}
\]

A positive integration constant instead leaves nonzero density at infinity
and infinite mass. A negative one makes a finite zero-density boundary,
which fails the unchanged gate at nonzero `D`, as in the inherited boundary
proof. Thus the boundary condition in (10) is material to the result.

Define `eta=GM0/(R0 c^2)`, `y=R0/r`, and
`b=(n-1)eta/n`. Along (10),

\[
 h_s=\rho c^2(1+\eta y),\qquad
 s^2=\frac{\eta y}{n(1+\eta y)},\qquad
 h_{\rm eff}=\rho_0c^2 y^n(1+by). \tag{11}
\]

For the finite-mass range below, `n>3`, one has `0<s^2<1/n<1`.
The Newtonian comparison is physically controlled only for `eta << 1` and
small support self-gravity; algebraic validity of (10) for larger `eta` is
not a relativistic approximation estimate.

## 4. Exact finite-mass and all-exterior normalization condition

The rest mass exterior to `R0` is

\[
 M_s=4\pi\int_{R_0}^\infty\rho r^2dr
     =\frac{4\pi\rho_0R_0^3}{n-3},\qquad n>3. \tag{12}
\]

It diverges for `n<=3`. For `n>3`, both the material energy and integrated
enthalpy are finite as well:

\[
 \frac1{c^2}\int\epsilon_{\rm mat}\,dV
 =M_s\left[1+\frac n{n+1}\eta\frac{n-3}{n-2}\right],\quad
 \frac1{c^2}\int h_s\,dV
 =M_s\left[1+\eta\frac{n-3}{n-2}\right]. \tag{13}
\]

The volume here is Newtonian `4 pi r^2 dr`; these are not relativistic ADM
mass formulas. They distinguish the rest mass budget from the CE053
integrated-enthalpy lower resource.

The inherited gate has

\[
 h_{\rm crit}=D_0^2\frac{x^3}{(1-x)^2},\qquad
 x_0=A/R_0^2\in(0,1),\qquad
 C=\frac{\rho_0c^2}{D_0^2x_0^3}.
\]

The exact ratio for the Newtonian atmosphere (10) is

\[
 \frac{h_{\rm eff}}{h_{\rm crit}}=C f(y),\qquad
 f(y)=y^{n-6}(1+by)(1-x_0y^2)^2,\qquad 0<y\le1. \tag{14}
\]

In particular, `h_eff~r^{-n}` and `hcrit~r^{-6}`. Therefore no finite
normalization can pass at every finite exterior radius if `n>6`. Combining
this obstruction with (12), the **necessary and attainable index interval** is

\[
 \boxed{\quad 3<n\le6,\qquad 7/6\le\Gamma<4/3.\quad} \tag{15}
\]

Attainability here means that a finite normalization exists in this prescribed
Newtonian comparison, with `K` chosen consistently through (10). It does not
imply an allowed abundance, small self-gravity, or stability of a live coupled
halo. No `h=lambda hcrit` has been imposed.

There is also an exact normalization test:

* If `3<n<6`, let `m=min_{0<y<=1} f(y)>0`. The minimum is attained because
  `f(y)->infinity` at zero. Passing at every finite `r>=R0` is equivalent to
  `C>1/m`.
* For `3<n<=5`, `m=f(1)=(1+b)(1-x0)^2`. Thus the **inner gate alone is
  necessary and sufficient**, with the pressure correction fully included:
  `rho0 c^2 (1+b)>D0^2 x0^3/(1-x0)^2`.
* For `5<n<6`, calculate `m` from `f(1)` and the values of `f` at the real
  roots in `(0,1)` of

  \[
  H(y)=(n-6)+(n-5)by-(n-2)x_0y^2-(n-1)bx_0y^3. \tag{16}
  \]

  The smaller positive root, if in `(0,1)`, is the only possible interior
  local minimum. Keeping all roots as candidates gives the same exact minimum
  and avoids any choice of cubic radicals.
* If `n=6`, the exact condition is

  \[
  \boxed{\quad C\ge1,\qquad C(1+b)(1-x_0)^2>1.\quad} \tag{17}
  \]

  Equality `C=1` can pass at every finite radius if `(1+b)(1-x0)^2>1`;
  its gap then tends to zero only at infinity. A uniform positive relative
  gap requires `C>1` in addition to the second inequality.

To prove the tests, multiply `f'/f` by the positive quantity
`y(1+by)(1-x0y^2)`. The result is (16). For `3<n<=5`, every nonzero
coefficient in `H` is negative. For `5<n<6`, `H(0)<0`,
`H''=-2(n-2)x0-6(n-1)b x0 y<0`, and `H` eventually tends to minus infinity.
There can be at most two positive roots: a minimum of `f` followed by a maximum.
For `n=6`, `H=y[b-4x0y-5b x0y^2]`; `f` increases then decreases, so its infimum
is the smaller of the endpoint limit `1` and `f(1)`. The limit endpoint is
unattained, while `y=1` is included, giving precisely (17).

The distinction in `5<n<6` is real even in a weak central field. For example,
`n=5999/1000`, `eta=1/100`, `x0=1/1000000` give `H(0)<0<H(1)` in exact
rational arithmetic. Hence an interior minimum is strictly below `f(1)`,
and some normalizations pass at the inner boundary while failing farther out.
This is a counterexample to using only the inner gate for all `n<6`.

An easily used, somewhat stronger sufficient condition for the whole interval
(15) is

\[
 \rho_0c^2>h_{\rm crit}(R_0). \tag{18}
\]

Indeed, `y^(n-6)>=1`, `1+by>=1` and
`(1-x0 y^2)^2>=(1-x0)^2`. This bound can avoid the cubic when only existence
is needed. The exact rest mass normalization for `3<n<6` is equivalently

\[
 M_s>\frac{4\pi R_0^3D_0^2x_0^3}{(n-3)c^2m}.
 \tag{19}
\]

For fixed `M0,R0`, the bound is a restriction on `K` through (10), rather
than a predicted material abundance. If an independent upper mass inventory
is below the right side of (19), this candidate fails that inventory.

## 5. What the inherited local construction then supplies

At every finite occupied point satisfying (14), choose the same response as
in the pinned principal proof, now with **one** neutral current:

\[
 R=h_{\rm eff}/h_{\rm crit}>1,\quad t=1-x,\quad p=(1-x)^2,\quad
 \beta_L=p\frac{R-1}{R-(1-x)},\qquad
 \beta=\beta_L\frac R{R+1}. \tag{20}
\]

This yields `0<beta<betaL<p<t`, nonnegative frozen principal energy, and
propagating principal roots strictly inside the metric light cone, under
the inherited finite-density, pure-electric, no-entrainment assumptions.
It is compatible with (5), because neither `beta` nor its density derivative
adds a first background force at `B=0`. For this single exterior species the
frame weight is exactly one and the gate inertia is (8), with no harmonic
multispecies replacement or charge-weighted rest mass.

This does not remove the reciprocal frame perturbations. Their quadratic
inertia and magnetic mixing remain. They are precisely why (8), rather than
bare rest mass alone, must enter the gate. Nor is (20) a microscopic derivation
of a constitutive response; it is an admitted density-dependent construction.

## 6. Source, boundary and open obligations

1. `R0` is an exterior matching radius with positive pressure `P(R0)` and
   positive density. It cannot be an unsupported free material surface. The
   central object must supply the stress, the support must continue inward,
   or a counted wall/interface must be derived. This exterior theorem alone
   does not regularize a point source or remove that matching obligation.
2. The charged core supplies `M_Q`, and some central configuration supplies
   `M0`. Their relation and the core's own species force balance are inputs.
   The old charged chi/S bookkeeping cannot be replaced silently by `q_s=0`.
   Extra occupied exterior species would require their forces and the chosen
   frame to be rederived. No new production or conversion action is supplied.
3. At every finite radius the atmosphere is occupied; it has no finite smooth
   nonscreened edge. At infinity both density and field tend to zero. Thus
   the finite-edge continuity obstruction is avoided without asserting a
   regular off-shell vacuum action, uniform hyperbolicity, or finite-density
   behavior for nearby independent perturbations at zero current.
4. The support's gravity, pressure, constitutive field energy and the charged
   source must all be included in a coupled metric calculation. A small finite
   integrated budget alone is not its existence theorem. Full Einstein
   constraints, lower-order gravity/Jeans effects, finite background drift,
   magnetic backgrounds, nonlinear evolution and long-term stability are
   outside this local principal and prescribed-background result.
5. No change to the observed galaxy law, lensing, portal identity, abundance,
   `a0`, or any laboratory prediction follows merely from this construction.

The smallest closed implication is now: a *new counted neutral polytropic
stock* can solve its own static exterior material equation while passing the
unchanged finite-density local causal gate with finite mass. The missing step
is a sourced, matched, self-gravitating solution and its actual physical carrier.

## 7. Checks and provenance

`check_neutral_support.py` verifies the pure-electric projected frame force,
the thermodynamic identity (8), hydrostatic integration, the gate ratio,
derivative cubic, endpoint controls and finite resource formulas in exact
SymPy arithmetic. It also checks the weak-field interior-minimum
countercontrol above. These are implementation checks of displayed analytic
identities, not a sampled proof of (15) or a coupled solution.

`computation_contract.json` and `run_exact/manifest.json` pin the proof,
script and inherited snapshots. The exact command and package versions are
recorded in the manifest; `REPRODUCE.txt` gives the bounded replay. No external
mathematical theorem or source lookup is used in the derivation above.
