# C003: the action-level gates behind clock-frame kicks

Base checkpoint: `1f0306787` (Claude L189 and Hermes C003). The concurrent
`5a87447af` commit concerns an unrelated music/numerology analysis and does not
alter this action calculation. Inputs are separately hashed in run manifests.

Credit: Carl Zimmerman proposed pursuing a primordial clock and a persistent
medium response. Claude/Fable introduced the C003 DE-triggered clock-frame-kick
candidate in L189; the Hermes registry supplies the proposed follow-up gates.
The present calculation audits that candidate, not a claim of its novelty.

## 1. The dust action really does need a stress-generating extension

Consider the explicit, restricted action (signature `-+++`, `c=1`)

\[
 S_d=\frac12\int d^4x\sqrt{-g}\,\rho
       [-g^{\mu\nu}\partial_\mu\tau\partial_\nu\tau-1].
\]

Variation of the multiplier, clock and inverse metric gives, respectively,

\[
 (\nabla\tau)^2=-1,\qquad
 \nabla_\mu(\rho\nabla^\mu\tau)=0,\qquad
 T_{\mu\nu}=\rho\tau_\mu\tau_\nu+g_{\mu\nu}L_d.
\]

On the constraint, `L_d=0`. Writing `u_mu=-tau_mu`, this is exactly
`T_mu_nu=rho u_mu u_nu`. Since second covariant derivatives of a smooth scalar
commute,

\[
 u^\mu\nabla_\mu u_\nu
 =u^\mu\nabla_\nu u_\mu
 =\tfrac12\nabla_\nu(u^\mu u_\mu)=0.
\]

`trigger.py` varies the density in all ten symmetric inverse-metric directions
at a local inertial point. The calculated tensor agrees identically with the
expression above; all sixteen reported residual entries are zero. This is a
local tensor calculation, not a formalized integration-by-parts proof.

Now apply the candidate's nonrelativistic additive kick generator to velocity
test functions, with isotropic unit vector `e`, speed `v_k` and local rate
`Gamma`. Direct angular integration gives

\[
 \langle v'_i-v_i\rangle=0,\qquad
 \langle v'_iv'_j-v_iv_j\rangle=\frac{v_k^2}{3}\delta_{ij},
 \qquad v'=v+v_k e.
\]

Consequently, for constant rate across the local distribution,

\[
 \boxed{\left.\dot\Pi_{ij}\right|_{\rm kick}
       =\frac{\rho\Gamma v_k^2}{3}\delta_{ij},\qquad
       \left.\dot E_{\rm kin}\right|_{\rm kick}
       =\frac12\rho\Gamma v_k^2.}
\]

These are collision-source terms, not the full expanding/self-gravitating
transport equations. For velocity-dependent rate, replace `rho Gamma` by the
mass-weighted integral of the rate. Number and mean momentum are conserved by
this idealized generator, but kinetic energy requires a reservoir.

**Conditional obstruction:** the unextended action `S_d` cannot remain exactly
pressureless and simultaneously realize nonzero isotropic Poisson recoil of
its own component. The collision source leaves the zero-dispersion subspace
immediately. This is NOT a no-go for the full cuscuton/braiding action, for a
non-barotropic clock medium, or for every MOND theory. Such an extension must
actually derive the stress, reservoir and exchange equations.

## 2. A clock frame is not automatically a multistream detector

The candidate assumes `step(v_rel)` vanishes in single-stream flow. A scalar
clock defines `n_mu=-partial_mu tau/sqrt(-grad(tau)^2)`; relative speed to `n`
is a meaningful invariant, but it is not velocity dispersion.

A single stream with velocity `(0.1,0,0)` relative to that frame has nonzero
relative speed and zero central covariance. Two equal counterstreams at
`(+0.1,0,0)` and `(-0.1,0,0)` have zero bulk velocity and covariance trace
`0.01`. The computation also verifies that central covariance is unchanged by
a common bulk-velocity shift. A rate depending on the relative speed of each
stream may act on the counterstreams, but it also acts on the single moving
stream unless a further alignment equation is supplied.

Trying to define the clock as the local bulk frame is not a universal repair.
Any smooth scaled gradient `n=f d tau` obeys

\[
 n\wedge dn=0.
\]

In Minkowski space, the rotating timelike one-form

\[
 n=\frac{-dt-\omega y\,dx+\omega x\,dy}
          {\sqrt{1-\omega^2(x^2+y^2)}}
\]

has

\[
 (n\wedge dn)_{txy}
 =\frac{-2\omega}{1-\omega^2(x^2+y^2)}\ne0
\]

inside the light cylinder when `omega != 0`. Thus one scalar clock cannot
coincide with **every** allowed rotating bulk frame. This is a kinematic
counterexample to an automatic identification, not a demonstrated rotating
solution of C003. Restricting the candidate's solution space to a special
irrotational class is an additional dynamical hypothesis requiring proof.

`ClockMoments.lean` certifies the scaled-gradient identity from symmetric
second jets, the rotating-form coefficient and its nonvanishing, and the
real two-stream identity

\[
 \langle v^2\rangle-\langle v\rangle^2
 =w(1-w)(v_1-v_2)^2>0
 \quad(0<w<1,\ v_1\ne v_2).
\]

It does not formalize the differential geometry, angular integral or action.

## 3. The DE trigger still needs an action definition

In the flat dust-plus-constant-Lambda GR background used by L189 only,

\[
 \frac{\Omega_\Lambda(a)}{\Omega_{\Lambda0}}
 =\frac{H_0^2}{H(a)^2}
 =\frac{1}{\Omega_{m0}a^{-3}+\Omega_{\Lambda0}}.
\]

This time dependence is due to the changing *fraction*, not changing vacuum
density. It neither derives a new DE history nor establishes the same
background for the candidate. Replacing `H` by the local clock expansion
`theta/3` gives `9 H0^2/theta^2`, which diverges as `theta -> 0` in a
nonexpanding patch. A global cosmological expansion and a local virialized
bulk frame cannot be silently interchanged. This only rejects that naive
replacement; it does not exclude other covariant triggers.

## 4. Correction concerning “frozen” coefficient functions

A fixed function `U(tau)` is not an externally prescribed function of coordinate
time when `tau` is a varied scalar. Its clock variation contains
`(partial L/partial U) U'(tau)`; it can already be part of a covariant action.
Promoting `U` to an independent field is **not necessary** merely because its
functional form was specified. It may add physical modes and needs a fresh
constraint analysis. The remaining problem is deriving/predicting the chosen
function and passing the dynamics, not covariance by itself. Likewise the
failure of four particular initial roots does not prove every initial state
of that unchanged action fails.

## What would actually advance closure

An admissible non-particle route would need a specified classical clock/medium
action whose derived, coarse-grained equations supply the velocity-dispersion
stress and its compensating energy exchange. The present `X -> X' + phi`
interpretation is a particle-decay model; it does not satisfy Carl's requested
non-particle closure merely by renaming `X` a clock. Numerical tracer particles
are permitted as a method, but are not a derivation of the medium's action.

Do not refit `v_k`, rates or coefficient functions to remove a failed gate.
First derive the existing candidate's coupling, frame, reservoir and metric
stress. Then its coupled metric/clock/medium equations—not a stock-GR proxy—
must decide MOND, lensing, constraints, PPN, stability and cosmology together.
