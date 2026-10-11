# Reciprocal gravity redirects streams, but does not select their core mass here

2026-10-11. Source base `add3cae0a`; follows the completed inner-orbit checkpoint
`85ae78f2b`. The preceding goal turn was progress: it derived kernel-dependent
orbital requirements and committed checked evidence. This continuation executes
its proposed transfer experiment. The original theory objective remains OPEN.

**Result:** a positive baryonic mass distribution can redirect passing streams
with exact reciprocal energy and angular-momentum exchange. However, fewer core
crossings do not guarantee less mass in the core. In the finite ensembles tested,
the rotating source reduces time-averaged core mass for one incoming orbital
mixture and increases it for another with the same total conserved quantities.
This experiment therefore does not establish a common density-selection rule.

## A finite Hamiltonian with a physical energy reservoir

Use two equal positive Plummer mass profiles, whose centres lie at
`R_b +/- a e(theta)`. Their shapes and separation are maintained by ideal
constraints; their spherical internal profiles do not spin. They form a
constrained body with mass M and orbital moment of inertia `I=M a^2`.
The body can translate and rotate. Its potential on a stream element is

\[
 \Phi(x,\theta)=-\frac{GM}{2}\sum_{\sigma=\pm1}
 [|x-\sigma a e(\theta)|^2+s^2]^{-1/2},\qquad x=r-R_b.
\]

The nonnegative source density is the sum of the two ordinary Plummer
densities `3(M/2)s^2/[4 pi (distance^2+s^2)^(5/2)]`. The numerical stream
parcels discretize a phase-space population; no new particle species is
identified. Parcels do not interact gravitationally with one another in this
prototype. The Hamiltonian is

\[
 H=\frac{M|V_b|^2}{2}+\frac{L_b^2}{2I}
   +\sum_i m_i\left[\frac{|v_i|^2}{2}+\Phi(r_i-R_b,\theta)\right].
\]

With `A_i=-grad Phi`, and `tau_i=(x_i cross A_i)_z=partial_theta Phi`, the
reciprocal body equations are

\[
 M\dot V_b=-\sum_i m_i A_i,\qquad
 \dot L_b=-\sum_i m_i\tau_i,\qquad \dot\theta=L_b/I.
\]

They conserve H, total linear momentum and total inertial angular momentum.
For the particles' inertial orbital energies,

\[
 \dot E_i=V_b\cdot A_i+\Omega\tau_i,\qquad
 \Delta E_{\rm streams}=-\Delta K_{\rm body,COM}-\Delta K_{\rm body,spin}.
\]

Thus the source cannot supply uncounted spin work. This extends the previous
externally imposed rotating potential. It remains a planar constrained-body
model, not a live deforming galaxy or a self-gravitating cold halo.

The axisymmetric control is the exact planar azimuthal average of the same
positive source, a circular ring of Plummer centres:

\[
 \bar\Phi(r)=-\frac{2GM}{\pi\sqrt S}K(m),\quad
 S=(r+a)^2+s^2,\quad m=4ar/S.
\]

Here K takes the elliptic parameter m. Its spin angle decouples. Comparing the
pair and ring tests the full nonaxisymmetric field, including radial multipoles
and torques. It does not isolate torque alone.

## Inputs and what the measurement means

Dimensionless inputs are `G=M=1`, `a=.2`, `s=.05`, stream mass `.01`, initial
radius 2, initial orbital energy `E_i=-.2`, and 24 equally weighted incident
phases paired with opposite angular momentum. Compare `|j_i|=.05` and `.3`.
The rotating source begins at `Omega=.5`; a separate freely evolving source
begins at zero spin. The interval is `0 <= t <= 40`, only a few passages.

Every pair/ring rotating cell starts with `H=.003`, `J=.02`, and `P=0` to
roundoff. The two initially nonrotating cells match each other, but have
`H=-.002`, `J=0`; changing initial spin changes the conserved totals.

The density-relevant diagnostic is residence, not just crossing count:

\[
 f_R=\frac1{NT}\sum_i\int_0^T\mathbf1[|r_i-R_b|<R]dt.
\]

The time-averaged enclosed stream mass is `M_stream f_R`. All original
parcels stay in the denominator, including distant or outgoing ones. This is
a finite-time enclosed-mass average, not a final density or stationary flux.

## Main outcome at R=.1

| Source | Initial j magnitude | Inward entries | Residence fraction f_R | f_R / matching ring |
|---|---:|---:|---:|---:|
| Rotating pair | .05 | 48 | .00111378 | .34771 |
| Ring | .05 | 96 | .00320318 | 1 |
| Rotating pair | .30 | 58 | .00168806 | 1.93514 |
| Ring | .30 | 96 | .00087232 | 1 |
| Initially nonrotating pair | .05 | 52 | .00125222 | .39093 |
| Initially nonrotating pair | .30 | 58 | .00157029 | 1.80013 |

The last two rows compare occupation with the corresponding ring radial
control, but their total initial spin energy differs from that ring. The next
symmetry experiment removes spin work exactly.

In the high-j rotating cell, visits last about 3.20 times as long as in the ring
on average. Entry counts fall while enclosed mass rises. The low-j rotating
cell instead has shorter visits and less enclosed mass. At R=.2 and .4,
crossing numbers remain comparable (96--106 in the rotating pair versus 96
in the ring), so the change is concentrated toward the source region.

All 48 main-cell parcels recross radius 2 outward at least once. The rotating
low/high-j cells finish with 8/16 parcels beyond radius 4, outward moving and
with positive instantaneous orbital energy. These are **escape candidates**,
not a proof of permanent escape in a time-dependent field. The rotating
source loses spin energy and heats the streams by total `.00069455` and
`.00120965`; its final spin is `.46397` and `.43534`.

Similar final mean |j| (`.28913` versus `.28817`) does not summarize the cohorts'
preceding core residence. It does not establish equal simultaneous phase-space
distributions or a stationary density. No universal late-time claim is made.

## A sharper control: redirection without cooling or spin work

The follow-up changes the incident phases to `(k+1/2)2pi/Nphase`, retaining
both j signs. This finite sample has exact reflection and inversion symmetry.
Uniqueness of the smooth ODE then preserves a resting source, and each
particle's orbital energy is constant. This is a controlled example, not a
claim that arbitrary streams maintain those symmetries.

| Total parcels | Initial j magnitude | Inward entries at .1 | Residence fraction |
|---|---:|---:|---:|
| 48 | .05 | 56 | .00131757 |
| 48 | .30 | 64 | .00168615 |
| 96 | .05 | 100 | .00121397 |
| 96 | .30 | 108 | .00151706 |

The source's maximum |Omega| is below `4.3e-13` and each parcel's energy
drift is below `1.1e-8`. The opposite effects on low/high-j core occupation
survive phase refinement, although their sizes change; continuum convergence
is not claimed. The ring radial trajectories are independent of initial
azimuth and the sign of j, so its normalized residence values above provide
the same control for either phase grid.

Consequently, nonaxisymmetric gravitational scattering can redirect a stream
without cooling it. That mechanism alone has not selected the required orbit
population or an initial-condition-independent density in this experiment.

## Verification and retained failures

Authoritative records are [run_v4](run_v4/manifest.json), **73/73**, and
[reflection_run_v3](reflection_run_v3/manifest.json), **32/32**. Both manifests
validate against current execution inputs. Controls include independent force
differences, angular averaging, an asymmetric recoil case, a deliberately
wrong reciprocal-torque sign, a tighter orbit integration, two detector grids,
and analytic grazing/turning-point trajectories.

Maximum main-cell errors in total energy, angular momentum and linear momentum
are respectively `8.4e-10`, `3.3e-12`, and `1.1e-17`. The reported exchange
residual is algebraically the total-energy residual, not independent evidence.
The wrong-sign control produces errors of order `.002`, and is rejected.

The first run failed its detector comparison (62/63): fixed-time samples
missed a shallow incursion. Turning-point brackets fixed that issue. An
independent reviewer then found exact sampled-zero and tangent cases that
two aligned grids could both miss. The final detector brackets across sampled
zeros and includes turning points among residence-integration boundaries.
Analytic tests exercise all these cases. The recorded physical crossing and
residence numbers did not change in the latter two corrections. Unresolved
multiple turns within one bracketing interval remain a numerical limitation;
the stated grid and integration refinements are finite checks, not a certified
interval enclosure of every trajectory.

Older runs and source snapshots are retained. Their manifests identify the
historical input hashes, which intentionally differ from current source.
`run/input_experiment.py`, `run_v2/input_experiment.py`, and
`run_v3/input_experiment.py` recover those revisions. The initial reflection
script is in `reflection_run/input_reflection_control.py`. Historical records
must not be presented as current-input validation.

The two final runs each use cooperative one-thread numerical-library limits,
explicit wall/CPU caps and fewer than 100 stream parcels per cell. Independent
review checked Hamiltonian signs, recoil, ring averaging and detector semantics.
Review agreement does not replace the displayed identities and reproducible
numerical evidence.

## Decision toward the full theory

Reciprocal transfer is now demonstrated in this scoped model. A universal
reduction of core mass from torque is not: residence responds differently to
the two incoming mixtures. The theory needs a selected joint distribution of
orbital energy and angular momentum, including residence and replenishment.
An angular-momentum average or crossing-count reduction is insufficient.

No a0, c or vacuum density enters these equations. The experiment neither
identifies the cold carrier nor fixes its abundance or kappa, and cannot
derive 32 pi from its absent vacuum coupling. The core aperture also lies
within the baryonic source, so it does not test the prior point-source
exponential asymptotic. Global self-gravity, three-dimensional dynamics,
assembly/capture, a physical host-ownership mechanism and the common
observational law remain open. No other lane or frozen criterion was changed.

The recommended next experiment and its assumption audit are recorded in
[NEXT_CAPTURE.md](NEXT_CAPTURE.md): measure capture during baryonic contraction
and subsequent retention, with an embedded-star control. That experiment has
not yet been executed.
