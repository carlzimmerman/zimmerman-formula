# Assembly captures streams; tides do not provide a universal exclusion

2026-10-11. Base checkpoint: `43730771f161904fa9a77c8fb360dac732143344`.
The preceding turn published the reciprocal-transfer experiment and capture
work order. This continuation executes that work order. The theory remains
OPEN: carrier, abundance, universal profile, vacuum coupling and kappa are
not derived by these experiments.

**Result:** prescribed baryonic contraction can turn initially unbound
isolated streams into permanently bound orbits in the final static potential.
With physical incoming states matched, a host tide sometimes reduces the
guaranteed-retention count, but can also enable retention where the isolated
case captures nothing. Thus an absolute distinction between galaxy retention
and stellar non-retention does not follow from this mechanism alone.

## Model and finite contract

Use positive Plummer baryonic density with `G=M=1`, scale radius `b_i=.5`
contracting to `b_f=.05`, and

\[
 \Phi(r,t)=-\frac{1}{\sqrt{r^2+b(t)^2}},\qquad
 b(t)=b_i+(b_f-b_i)(3u^2-2u^3),\quad
 u=\min(1,\max(0,t/T)).
\]

The body is held fixed and its contraction is prescribed. Streams are planar
test particles without self-gravity. This is a transfer diagnostic, not a
closed action for baryonic formation or a galaxy-mass cold halo. No vacuum
scale or desired density is inserted.

Incoming states have radius 2, isolated specific energy `.03`, `.3` or `.8`,
signed angular momenta `+/-.05,+/-.25,+/-.6`, and eight uniformly spaced
azimuths, giving 48 equal-weight parcels. All move radially inward initially.
Contraction durations are `.5,2,8`. Static initial-profile and final-profile
controls use identical positions and velocities. Even the deeper final
static control has positive initial isolated energy (minimum `.01523`).

The embedded comparison uses a point-host planar Hill tide with
`Omega^2=1/3`, hence Hill scale `r_H=1`:

\[
 \ddot x=2\Omega\dot y+3\Omega^2x-\frac{x}{(r^2+b^2)^{3/2}},\qquad
 \ddot y=-2\Omega\dot x-\frac{y}{(r^2+b^2)^{3/2}}.
\]

The model's rotating-frame energy and work identity are

\[
 E_J=\frac{v_{\rm rot}^2}{2}+\Phi-\frac32\Omega^2x^2,
 \qquad \dot E_J=\frac{b\dot b}{(r^2+b^2)^{3/2}}.
\]

The code integrates the right-hand side independently along every orbit and
compares it with the energy change. For isolation set `Omega=0`. The Hill
identity is Jacobi-work accounting; it is not total inertial energy conservation
of a live host, contracting source and streams. The host orbit and assembly
reservoir are prescribed. In inertial relative coordinates the host supplies
the rotating tidal tensor `R diag(2 Omega^2,-Omega^2) R^T`; energy exchange with
that host has not been closed by a reciprocal host evolution.

## A physical retention boundary

For general `mu=GM` and `r_H^3=mu/(3 Omega^2)`, with `0<b<r_H`, the escape
saddles are at `x=+/-x_L`, where

\[
 x_L=\sqrt{r_H^2-b^2},\qquad
 E_s=-\frac{3\mu}{2r_H}+\frac{\mu b^2}{2r_H^3}.
\]

On the circle `r=x_L`, the effective potential obeys
`U-E_s=mu y^2/(2 r_H^3) >= 0`. Inside that circle U increases radially from
the origin. An actual phase point with `E_J<E_s` and `r<x_L` therefore lies
in the bounded central allowed component. Equivalently one may use
`|x|<x_L`: at a physically allowed below-saddle point in that strip,
`r>=x_L` would imply `U>=E_s>E_J`, a contradiction. Both implementations
agree in the numerical checks.

The exact moving-barrier identity is

\[
 \boxed{\frac{d}{dt}(E_J-E_s)=
 \mu b\dot b\left[(r^2+b^2)^{-3/2}-r_H^{-3}\right].}
\]

Contraction lowers energy relative to escape inside `r<x_L` and raises it
outside. A particle that becomes below-saddle inside cannot leave during
continued monotone contraction: its energy deficit increases and the
bounding circle expands. Once contraction stops, the fixed energy barrier
guarantees retention in this model. The extra 12 time units of integration
check consistency; that finite interval is not the basis of the permanence
argument. Isolated negative-energy retention follows from the final static
potential with zero at infinity.

This counts a sufficient retained subset in the Hill problem. Above-saddle
orbits can undergo temporary or other bounded motion; zero counted particles
does not prove zero trapping. Every input is outside the closed central
component, but is not asserted globally unbound in the complete host problem.

## Matched inflow: the comparison that matters

The first Hill run used identical *coordinate* velocities. That did not match
the isolated physical inflow: `v_inertial=v_rot+Omega cross r`.
[matched_inflow.py](matched_inflow.py) corrects this through an explicit
adapter, leaving the historical module and evidence intact. The incoming
positions and satellite-relative inertial velocities now match to below
`1e-14`; inertial angular-momentum labels are corrected too.

Retained parcel counts, each out of 48:

| Initial isolated energy | Contraction duration | Isolated | Matched Hill |
|---:|---:|---:|---:|
| .03 | .5 | 0 | 0 |
| .03 | 2 | 48 | 0 |
| .03 | 8 | 48 | 6 |
| .30 | .5 | 0 | 0 |
| .30 | 2 | 48 | 6 |
| .30 | 8 | 0 | 8 |
| .80 | .5 | 0 | 0 |
| .80 | 2 | 32 | 6 |
| .80 | 8 | 0 | 0 |

Every static control captures zero into its below-threshold component.
At `.30,T=8`, host tides **together with assembly** produce retained particles
where the isolated evolution retains none. Static tides alone are not shown
to capture them. Raw Hill and isolated energy numbers use different energy
functions and must not be compared as one observable.

Angular refinement gives:

| Matched Hill cell | N=48 | N=96 | N=192 |
|---|---:|---:|---:|
| E=.03, T=2 | 0 | 0 | 0 |
| E=.30, T=2 | 6 | 2 | 10 |
| E=.30, T=8 | 8 | 10 | 26 |
| E=.80, T=8 | 0 | 0 | 2 |

These are counts, with changing denominators. The reversal at `.30,T=8`
survives all three grids; no continuum capture fraction is established.
The isolated results are independent of azimuth by exact spherical symmetry.
Tighter integration preserves the positive matched masks at `.30,T=2,8`;
their maximum final-energy disagreements are below `3e-8`.

All ensembles are finite shells with selected energies, angular momenta and
arrival times. They are not measured stellar or galactic incident distributions,
steady incoming fluxes, or astrophysical capture rates. Hill parameters are
dimensionless; a real star requires its actual host orbit and source history.

## Evidence and corrections

| Record | Checks | Role |
|---|---:|---|
| [run_v2](run_v2/manifest.json) | 181/181 | Isolated results; initial coordinate-matched Hill exploration |
| [phase_run](phase_run/manifest.json) | 30/30 | Sampling check of the initial Hill convention |
| [critical_run](critical_run/manifest.json) | 28/28 | Tighter checks of its positive captures and isolated mixed case |
| [matched_run](matched_run/manifest.json) | 157/157 | Correct physical-inflow comparison |
| [matched_positive_run](matched_positive_run/manifest.json) | 46/46 | Positive matched cases, integration and phase refinement |

The initial [run](run/manifest.json) failed three strict energy checks:
162/165 passed, with residuals up to `3.23e-7`. Tightening the integration
(without relaxing thresholds) reduced the baseline maximum to `2.53e-8`.
Its source and contract snapshots remain in `run/input_experiment.py` and
`run/input_contract.json`; that historical manifest does not validate against
the current source. Successful current manifests validate their input and
output hashes. A deliberately reversed work sign is rejected. Independent
review verified the work sign, retention proof and frame adapter.

Residence fractions are also recorded using two midpoint grids, but are
approximate finite-window occupation measures. They are not stationary
density profiles. Classification uses an energy margin `1e-7`; in the
positive matched refinement records the smallest absolute final gap is
`.0166`, far above the work residuals (below `9.2e-8`). Two numerical
settings do not constitute rigorous interval certification.

## What this changes for the theory

Assembly provides a concrete recruitment mechanism without a prescribed
partner label or target mass cut. But tides are not a universal prohibition
on embedded capture, and assembly time strongly changes the retained set.
The previous suggestion that a tide might simply enforce galaxy ownership
is now too strong. Its quantitative, population-dependent version remains open.

At a fixed source history, the predicted retained density has the form

\[
 \rho_{\rm ret}(x,t)=\int f_{\rm in}(\Gamma_0)
 \chi_{\rm ret}(\Gamma_0)\delta^{(3)}(x-X_t(\Gamma_0))\,d\Gamma_0.
\]

This expression is the three-dimensional continuum target for a follow-up;
the present experiment samples a planar finite analogue. It is linear in
incident mass density while the field is prescribed. Rescaling the input
mass rescales the captured mass. Capture alone therefore cannot select an
absolute cold abundance or the law's normalization in this test-particle class.

**Next live route:** compute the orbit-averaged density actually produced by
the retained distribution, then compare its shape with the specified law
without imposing that law as a relaxation target. Use an explicitly normalized
finite input distribution and retain both the exponential and repaired-kernel
distinction. If this step works, include self-gravity and a finite baryonic
assembly reservoir before claiming a formation mechanism for an entire halo.
Physical three-dimensional inflow and stellar limits remain required.

The microscopic carrier and vacuum coupling are separate unresolved leaves.
No `c`, `rho_DE`, or `a0` occurs in the capture equations, so these results
do not derive `kappa=1/2`, `32 pi`, or the user's `32 pi^2` convention.
The existing identity `Lambda c^4/a0^2=8 pi/kappa^2` remains unchanged.

## Literature overlap

Capture through a contracting gravitational potential is already known.
Eroshenko, *Capture of the free-floating planets and primordial black holes
into protostellar clouds*, [arXiv:2303.05200v1](https://arxiv.org/pdf/2303.05200v1),
9 March 2023, studies recruitment during cloud contraction (Introduction and
section 2). This confirms mechanism overlap; its population probabilities do
not transfer to our chosen shell ensembles or Hill boundary.

Capela, Pshirkov and Tinyakov, *Adiabatic contraction revisited: implications
for primordial black holes*, [arXiv:1403.7098v2](https://arxiv.org/pdf/1403.7098v2),
13 October 2014, starts with a core-bound distribution and distinguishes
instantaneous inner mass from elongated orbits crossing the star (sections
1--2). That distinction also supports keeping occupation separate from
entry counts. Its subsequent stellar energy-loss capture is not the same
as our purely gravitational recruitment into a final bound orbit.

Checked 2026-10-11 in the primary PDFs. Search scope: gravitational capture
during star formation, baryonic contraction and collisionless phase-space
limits; two primary candidates inspected, no exhaustive novelty search.
PDF bytes were not retained locally. Classification: known general mechanism,
with adjacent source results; the scoped repository test and boundary
calculation are not claimed as a new discovery in the literature.
