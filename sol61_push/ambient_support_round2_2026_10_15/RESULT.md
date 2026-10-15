# Finite neutral support with an exact regular core

AS2-2026-10-15-01, 15 October 2026. **Conditional mathematical advance; the
physical theory remains OPEN.** This round constructs finite-mass neutral
support around prescribed central sources, includes its rest-mass self-gravity,
and tests its perturbation energy. It supplies neither the original charged
carrier's equilibrium nor a full covariant galaxy/Einstein solution.

## What changed

The previous checkpoint showed why an unchanged smooth charged edge cannot
simply taper to empty vacuum. This round replaces an assigned support enthalpy
with a specified material current, EOS and pressure-supported equilibrium.
The neutral species, EOS normalization and central mass/charge profiles are
new inputs, stated in [the contract](CONTRACT.md). The recent-work review is
[recorded separately](RECENT_WORK.md); original criteria and failed gates are
preserved.

### The neutral stock can obey an actual support equation

Varying the current-defined material frame before specializing to the static
pure-electric state gives zero first constitutive force on that state. The
neutral chemical equation is therefore exactly `mu_s N=constant` in a prescribed
static metric. Neutrality does not remove the quadratic frame/gauge coupling.
The [action derivation](action/PROOF.md) states the current, action and species
accounting explicitly.

For the Newtonian point-mass exterior with `P=K rho^(1+1/n)` and zero pressure
at infinity, `rho~r^-n`. Finite mass requires `n>3`; the inherited constitutive
gate has `hcrit~r^-6`. The necessary and attainable exponent interval is
`3<n<=6`, equivalently `7/6<=Gamma<4/3`, with an explicit normalization test.
For `3<n<=5`, the exact inner gate is sufficient throughout the exterior.
These are conditional comparison equations, not an abundance prediction.

### Self-gravity is solved rather than assigned

A weighted integral contraction constructs an actual finite-mass exterior
Euler-Poisson solution for any `n>3` in an explicit small-stock range. With
`mu=4 pi rho_ref(R0) R0^3/[(n-3)M0]`, the certificate is

\[
 0<\mu<{(n-1)^{n-1}\over n^n},\qquad C={n\over n-1},\qquad
 q=n\mu C^{n-1}<1.
\]

The enthalpy lies between `GM0/r` and `C GM0/r`; the atmospheric mass lies
between `mu M0` and `mu C^n M0`. The first Picard correction and a rigorous
error bound are given in [the existence proof](self_gravity/PROOF.md).
For `3<n<=6` an explicit density lower bound also passes the local gate.
The same q supplies the missing equilibrium premise of the fixed-wall radial
energy estimate. This contraction threshold is sufficient for the proof,
not a nonexistence threshold above it. Matching the positive inner pressure
still requires a physical core; the next construction removes that wall.

### An exact regular-core example removes the inner wall

Prescribe a fixed central mass density

\[
 \rho_0={3M_0b^2\over4\pi(r^2+b^2)^{5/2}},\qquad
 \Phi_0=-{GM_0\over\sqrt{r^2+b^2}}.
\]

Choose neutral support `rho_s=f rho_0`, with `P=K rho_s^(6/5)` and

\[
 6K\left({3fM_0\over4\pi b^3}\right)^{1/5}
 ={GM_0(1+f)\over b}.
\]

This is an exact Newtonian Euler-Poisson equilibrium including support
self-gravity. Its support mass is `f M0`; its center is finite; its positive
`r^-5` tail has finite total mass and no finite vacuum interface. The central
source is prescribed, so its own force balance is still missing.

The support density Hessian satisfies an all-angular bound

\[
 Q[\eta]\ge {1-4f\over1+f}\int{c_{s,N}^2\over\rho_s}\eta^2\,d^3x,
 \qquad 0<f<1/4.
\]

The proof uses the actual gravitational Green kernel and includes the
self-gravity cross term. It is stronger than a sampled radial spectrum.
The weak-branch normalization turns at `f=1/4`, but that sufficient bound's
failure above the turn does **not** prove a mass-conserving instability.
See [the full construction](regular_core/PROOF.md) and the
[independent reconstruction](stability/PLUMMER_CHECK.md).

A fixed regular enclosed charge gives `x=q0 t/(1+t^2)^(3/2)`, `t=r/b`.
The assigned witness `q0=MQ/M0=1/2`, `GM0/(bc^2)=10^-6`, `f=10^-3`
passes the all-finite-radius local gate with
`h_eff/hcrit>30720` for `r>0`, while the fluid Hessian's gravitational fraction
is only `5/1001`. These are analytic bounds for chosen inputs, not fitted or
derived galactic parameters.

### The inhomogeneous gauge and fluid energies can be joined

The [independent constrained-energy derivation](joint_audit/REPORT.md) retains
`eta=-div(rho_s xi)`, the affine Gauss constraint for fixed external charge,
and all spatial coefficient gradients. It gives positive gauge/current
canonical squares plus the fluid Hessian above. The direct energy identity
has no leftover indefinite background-gradient term. This goes beyond a
frozen principal calculation in the specified comparison.

The exact scope is a hybrid variational model: the constitutive/current
inertia is retained, while gravity couples to conserved laboratory rest
density through Newtonian potentials. It is not the full metric-constrained
covariant action. External source densities are fixed and their spatial gauge
current vanishes. The conclusion assumes existing finite-energy linear
solutions and the stated vanishing boundary fluxes.

### A separate constitutive candidate repairs the occupied center

The unchanged magnetic response has the zero-field regularity defect below.
A [new explicit patch](patch/PROOF.md) replaces it by one quarter near zero
electric field and smoothly blends back to the parent response outside a
density-dependent field scale. The exact cone numerator is affine in beta;
convex blending preserves the positive cone window. The constant-quarter
region has a conservative cone margin of `131/400`.

This changes a specified magnetic constitutive input and the zero-field dark
gauge speed to `c/2`. It preserves the pure-electric static background and
fluid Hessian, gives a C2 action neighborhood at each occupied zero-field
point, and fits the same quadratic-energy join. It is not a microscopic
response derivation. It also has two distinct coefficient limits toward
vacuum, so it explicitly **does not** supply a continuous vacuum continuation.
The [separate audit](patch/AUDIT.md) states that boundary of the result.

## Limits that decide the next work

- The exterior atmosphere with a fixed impermeable inner radius has positive
  fluid energy. Allowing its inner surface to move against constant prescribed
  pressure gives an explicit negative radial trial quotient. Thus a boundary
  condition is part of the mechanism, not a harmless numerical choice. The
  regular-core example avoids that wall by keeping its central source fixed;
  it does not establish a live central body's stability.
- Positive quadratic energy controls a stated weighted perturbation norm.
  It does not supply a uniform frequency gap, nonlinear smooth evolution,
  radiation stability, or a physical formation/settling history.
- At the center, the unchanged engineered magnetic response behaves as
  `beta=1-2|E_U|/D0+O(|E_U|^2)`. Its action contains `|E_U| B_U^2/D0` and
  is not differentiable at `E_U=0, B_U!=0`. The background quadratic form at
  zero field is defined, but this family does not provide a differentiable
  nonlinear action on an open field neighborhood of the center. The separate
  patch above repairs this occupied-center defect by changing beta.
- In the infinite tail, support falls as `r^-5`; a finite-amplitude outgoing
  field can fall more slowly than the density-dependent gate permits. The
  background's large margin therefore gives no uniform nonlinear radiation
  neighborhood. A vacuum/asymptotic phase still needs its own action.
- Central mass and charge are external inputs; the new neutral matter is not
  the original charged cold stock. Its identity, EOS, abundance and production
  remain open. Newtonian rest-mass gravity omits field/pressure gravitational
  corrections and the full metric constraints.

The concrete next task is to define an actual asymptotic/vacuum phase and
matching action, carrying forward the occupied-center patch only as its own
chosen candidate. Then solve and perturb a **dynamical, counted central charged
source** with the neutral stock in that same action.
Only after that join should one attempt its production/settling history and
recompute galaxy, lensing and cosmological predictions. Current empirical
passes do not validate these new inputs.

## Reproducible evidence

| Lane | Bounded checks | Analytic conclusion |
|---|---|---|
| Neutral action | 36 exact checks | Static variation, EOS, finite mass and exterior gate |
| Self-gravity | 56 exact checks | Exterior contraction, finite mass and certified error |
| Regular core v2 | 19 exact identities; 3 potential quadratures; 7 gate samples | Exact regular equilibrium and uniform analytic bounds |
| Center patch | 15 exact identities; 12 blend controls | Cone-safe occupied-center repair and failed vacuum coefficient continuation |
| Stability and join | Direct independent derivations | Boundary counterexample, all-angular density bound and constrained quadratic energy |

Finite checks support the displayed proofs and do not replace their quantified
arguments. Core v1 remains a valid 17-identity historical run; v2 adds direct
dimensional gate and EOS coefficient controls. All records, commands and
scopes are in [REPRODUCE.md](REPRODUCE.md) and [AUDIT.md](AUDIT.md). No new
empirical pass or global novelty claim is made.
