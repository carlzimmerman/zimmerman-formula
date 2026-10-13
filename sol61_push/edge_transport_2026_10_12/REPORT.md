# From a sharp halo edge to transport and replenishment

12 October 2026. Checkpoint EDGE-TRANSPORT-2026-10-12; inspected base `eeb916a584acb5b0e62b6c5e95c51ebd2edc1a96`. This advances the outer-edge question left in [kinetic selector sections 7–8](../kinetic_selector_2026_10_11/RESULT.txt). It does not derive the cold-energy mechanism or its vacuum normalization. Analytical self-review, bounded numerical checks, and narrowly scoped Lean certificates are distinguished below. No claim of novelty in the broader literature.

Subsequent [assumption audit](INDEPENDENCE_AUDIT.md): the chosen half-drift is essential to the inverse-square-root profile and Brownian escape formula. A general-drift family and five additional Lean certificates make that dependence explicit. These remain conditional model calculations, not a derivation of the physical selector.

## Result and target

The previous construction supports a finite-density outer edge with an integrable energy singularity, but its stationary kinetic realization needs diffusion to vanish at that edge. This continuation tests three changes: an escape energy that fluctuates with the potential; a nonzero diffusion floor; and an open, absorbing boundary with replenishment.

The first does not remove the orbital diffusion in the specified weak stationary-noise model. The second softens the edge. The third permits a positive stationary distribution only with a maintained inward supply in the model examined here. An exact coordinate transformation provides an escape-time law for its ideal half-line extension. These results turn an arbitrary boundary prescription into explicit conditions on diffusion, drift and supply. They do not show that actual halos obey those conditions.

## 1. A fluctuating escape level does not remove nonzero orbital harmonics

Retain a fixed spherical mean potential, fixed angular momentum L, a noncircular regular orbit, and a fixed geometric radius R. Let

\[
H=H_0+\xi(t)h(r),\qquad
E_R(t,L)=E_{R0}(L)+\xi(t)h(R).
\]

The same weak noise drives the particle and escape-level fluctuations. Here xi is stationary, finite variance, independent of the initial orbital phase, and sufficiently regular for the displayed integration by parts; a smooth Gaussian covariance is used in the finite check. Define the instantaneous gap q=E_R-H. To first order on the unperturbed orbit,

\[
\dot q=\dot\xi\,[h(R)-h(r(t))],
\]

and consequently

\[
\Delta q=[\xi(h(R)-h(r))]_0^t+
\int_0^t\xi(s)\frac{d}{ds}h(r(s))\,ds.
\]

The endpoint term has bounded variance under these assumptions. If the integral has variance proportional to t, its covariance with the endpoint grows at most as sqrt(t), by Cauchy–Schwarz. Thus neither changes the diffusion coefficient obtained by dividing the variance by 2t in the separated-scale weak-noise calculation.

Writing the orbit function as h(theta)=sum h_n exp(i n theta), subtracting h(R) changes only n=0. The diffusion remains

\[
D_E=\frac12\sum_{n\ne0}(n\Omega_r)^2|h_n|^2S(n\Omega_r),
\]

where S is the two-sided noise spectrum. One strictly positive summand suffices for positive diffusion. This is consistent with the orbital-harmonic method in [Binney's author lecture, section 1.3.2](https://ned.ipac.caltech.edu/level5/Sept17/Binney/Binney3.html); the equations and normalization above are derived here rather than transcribed from its image equations.

**Scope:** this tests a fluctuating scalar escape energy at fixed R. A genuinely evolving catchment, changing L, phase-correlated collective response, secularly unbounded boundary motion or separatrix is not covered. It is not a universal moving-boundary no-go. The actual moving-catchment problem remains open.

## 2. A diffusion floor gives an explicit softened edge

Use the previous local constant-period model at fixed L. Its energy density n obeys

\[
\partial_t n=-\partial_qJ,\qquad
J=A n-\partial_q(Dn).
\]

Take the specified extension

\[
A=d/2,\qquad D=dq+D_0=d(q+q_0),\qquad q_0=D_0/d,
\quad d>0,\ D_0>0.
\]

The old drift is retained while a diffusion floor is added. This is a conditional model choice, not a derivation of the drift produced by baryonic noise. Units: q and q0 are specific energy, d is specific energy/time, D0 is specific energy squared/time.

Zero flux gives

\[
\boxed{n_{\rm refl}(q)=B(q+q_0)^{-1/2}}.
\]

This is a reflecting/no-flux benchmark and is not normalizable on the whole half-line. At constant radial period, f is proportional to n. For the fixed-L contribution to spatial density let

\[
\delta(r,L)=E_R(L)-V_{\rm eff}(r,L)>0.
\]

The density integral, with the common phase-space prefactor suppressed, is

\[
I_{\rm refl}(\delta)=
\int_0^\delta\frac{dq}{\sqrt{q+q_0}\sqrt{\delta-q}}
=2\arctan\sqrt{\delta/q_0}.
\]

For the original singular edge the corresponding integral is pi. Therefore

\[
\boxed{\frac{\rho_{L,\rm refl}}{\rho_{L,\rm sharp}}
=\frac2\pi\arctan\sqrt{\delta/q_0}}.
\]

At delta/q0 = 0.01, 1, 100 the ratio is approximately 0.06345, 0.5, 0.93655. As delta approaches zero the density vanishes as sqrt(delta), instead of ending in a finite jump. At a nondegenerate outer turning point, delta approximately equals a(L)(R-r), with a(L)>0, so the characteristic spatial transition is q0/a(L). Angular-momentum integration is a weighted mixture of these transitions; a universal single-width total profile is not asserted.

## 3. An absorbing boundary changes the stationary solution

When crossing q=0 removes a particle from the selected population, the diffusion floor makes an absorbing boundary a possible model: n(0)=0. A real apocentre crossing is not necessarily permanent escape; recapture and connected-region transport must be computed separately for a physical halo.

The general constant-current solution is

\[
n(q)=\frac{B}{\sqrt{q+q_0}}-\frac{2J}{d}.
\]

For q0>0, n(0)=0 and J=0 imply B=0: there is no nonzero, stationary, zero-flux member of this family. A nonzero stationary population instead has

\[
\boxed{n_{\rm abs}(q)=C\left(1-\sqrt{\frac{q_0}{q+q_0}}\right),
\qquad J=-dC/2,\qquad C>0.}
\]

Negative J is outward transport toward the escape boundary. A finite occupied interval needs an equal incoming supply at its other end. The associated fixed-L spatial integral is

\[
I_{\rm abs}(\delta)=2C\left[\sqrt\delta-
\sqrt{q_0}\arctan\sqrt{\delta/q_0}\right]
\sim\frac{2C}{3q_0}\delta^{3/2}.
\]

Thus the open and reflecting boundary models predict different edge powers, three-halves and one-half respectively, in this local constant-period approximation. A soft edge by itself does not identify the interaction or fix the mass–velocity normalization.

## 4. Exact transformation and conditional escape time

Inside q>0 the Ito process is

\[
dq=\frac d2\,dt+\sqrt{2d(q+q_0)}\,dW_t.
\]

Set x=sqrt(q+q0). Ito's formula cancels its drift:

\[
\boxed{dx=\sqrt{d/2}\,dW_t},
\qquad x_{\rm edge}=\sqrt{q_0}.
\]

For the **ideal half-line model killed at the lower boundary**, the standard Brownian reflection principle gives

\[
\boxed{P(\tau>t\mid q_i)=
\operatorname{erf}\left(
\frac{\sqrt{q_i+q_0}-\sqrt{q_0}}{\sqrt{dt}}
\right)}.
\]

The mathematical source is [MIT's Brownian-motion lecture, theorem 1 and its hitting-time consequence](https://ocw.mit.edu/courses/15-070j-advanced-stochastic-processes-fall-2013/aca1518a09539a09ddd37428ab0d0268_MIT15_070JF13_Lec7.pdf). Its standard variance-t Brownian motion becomes variance-dt/2 here. The survival expression is also checked by direct integration of the absorbing heat kernel.

The dimensionless median times at qi=1, d=1 are:

| q0 | Median exit time |
|---:|---:|
| 0 | 4.39622 |
| 0.01 | 3.60051 |
| 0.1 | 2.35934 |
| 1 | 0.75427 |
| 10 | 0.10473 |

The q0=0 entry is the killed extension, not the nonabsorbing squared-Brownian process in the earlier record. The half-line mean hitting time is infinite despite a finite median. No time in this table is a prediction in Gyr: d is undetermined, the constant-period approximation is local, and extending it to an unbounded energy interval is an idealization.

## 5. Verification, limitations and next decision

The current numerical run is [run_v2](run_v2/manifest.json): 93/93 checks, including three numerical mutation checks. It verifies spectral versus time-covariance diffusion, constant-boundary-shift invariance for a three-harmonic orbit, both density integrals and their edge powers, currents, the absorbing heat-kernel integral, and median survival. The initial [run](run/manifest.json) remains preserved: 91/93 passed because default relative quadrature accuracy was weaker than the comparison tolerance at the two largest absorbing integrals. `check_v2.py` tightens the integration accuracy; no equations or acceptance tolerances changed. Both input versions remain on disk.

[EdgeTransport.lean](EdgeTransport.lean) contains 13 exact conditional theorems. They certify the finite spectral-sum invariance and positivity, stationary-current algebra, absorbing-boundary amplitude condition, flux sign, transformed drift/diffusion algebra, and rationalized boundary distance. [lean_run](lean_run/manifest.json) checks every theorem's axioms and rejects three damaged proofs. These theorems do **not** formalize stochastic calculus, the reflection principle, the infinite harmonic limit, or astrophysical applicability.

Self-review checked the definitions of mean versus instantaneous energy, endpoint covariance scaling, the factor of two in diffusion, the distinction between n and f, velocity-integral Jacobians, current sign, normalization at a finite versus infinite interval, and the different q0=0 boundary extensions. The calculus is self-reviewed, not independently refereed.

The three routes yield a sharper requirement: a kinetic completion must derive the actual noise/drift and catchment boundary together. A scalar fluctuating escape level is insufficient in the tested class; a reflecting boundary maintains a benchmark distribution by assumption; an absorbing boundary needs a transport budget. No physical selection of a0, kappa, total abundance or the galaxy density profile was obtained.

The next substantive calculation is a finite catchment with physically calculated injection and recapture, evolving its potential and its orbit-dependent noise/drift. The relevant observable is the edge profile and its change with environment/history, not merely whether a relaxation code returns a preselected target. This continuation remains open because those physical inputs have not been supplied; another run of the same imposed diffusion would not determine them.
