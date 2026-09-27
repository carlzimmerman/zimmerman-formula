# D5 continuation: Fisher capillarity, one canonical pair, and the clock boundary

**Result: the local same-pair canonical bridge is derived exactly, and the
finite free-wave checks pass.** A wave representation need not add a classical
canonical pair on `rho>0`. It changes the global admissible domain when it
continues through nodes. A full gravitational clock requires more than regular
complex-wave evolution: its phase must define a global, appropriately timelike
foliation. That requirement is not established by the canonical bridge.

## Explicit action and local degree-of-freedom count

Extend the same first-order real-clock action used in `REPORT.md`:

\[
S=\int dt\,dx\left[
 \rho\Theta_t-\frac{\rho}{2}\Theta_x^2-U(\rho)
 -\frac{D^2}{8\rho}\rho_x^2\right],\qquad \rho>0.
\]

`D>0` has the normalization `D=hbar/m` if one adopts wave-mechanical notation;
no quantum-particle interpretation is needed for this classical calculation.
The extra term is a positive spatial-gradient energy. It introduces no new
time derivative and no second canonical pair: `(Theta,rho)` remains the sole
pair in this fixed-background model. Eliminating `rho` is now a spatial
equation, so the equivalence is not an assertion of a new local first-derivative
`K(Q)` action after elimination.

Set `phi=−Theta`, `v=phi_x`, and

\[
\Psi=\sqrt\rho\,e^{i\phi/D}=q+ip.
\]

Direct differentiation gives

\[
\frac{iD}{2}(\Psi^*\Psi_t-\Psi\Psi_t^*)
=-\rho\phi_t=\rho\Theta_t,
\]

\[
\frac{D^2}{2}|\Psi_x|^2
=\frac{\rho\phi_x^2}{2}
 +\frac{D^2\rho_x^2}{8\rho},\qquad
\det\frac{\partial(q,p)}{\partial(\rho,\phi)}=\frac1{2D}.
\]

The transformation is locally nonsingular on `rho>0`. The wave action is
first order in time, not two independent second-order real fields. In real
components its kinetic term is `D(p q_t−q p_t)`, differing from `2D p q_t`
by a total derivative. It has one canonical pair, as did the clock action.

For any differentiable local `U`, the wave equation is

\[
iD\Psi_t=-\frac{D^2}{2}\Psi_{xx}+U'(|\Psi|^2)\Psi.
\]

The bounded-DBI `U` from the pressure test may be inserted here, but its
nonlinear scattering was not simulated in this bounded follow-up. The exact
free-wave checks below use `U=0` and must not be relabeled as that nonlinear
test.

On a positive-density patch, the Eulerian equations are

\[
\rho_t+(\rho v)_x=0,
\]

\[
v_t+vv_x=-U''(\rho)\rho_x
 +\frac{D^2}{2}\partial_x
 \left[\frac{(\sqrt\rho)_{xx}}{\sqrt\rho}\right].
\]

This capillary stress differs from L374's minimal velocity-gradient correction,
which altered the continuity equation. Matching a linear `k^4` dispersion
does not make those nonlinear equations equivalent.

## Exact overlapping counterstreams

For `U=0`, the exact solution

\[
\Psi=e^{-iDk^2t/2}
 [A e^{ikx}+B e^{-ikx}]
\]

contains two counterpropagating Fourier modes. It is an exact coherent
overlapping-stream state, not a simulation of localized halo collisions.
For positive amplitudes,

\[
\rho=A^2+B^2+2AB\cos(2kx),\qquad
j=Dk(A^2-B^2),
\]

\[
\mathcal E=\frac{D^2k^2}{2}
 [A^2+B^2-2AB\cos(2kx)].
\]

The field and its energy are finite for all time, including balanced streams.
When `A=B`, the points `x=(pi/2+n pi)/k` are exact nodes at every time.
The phase is undefined there; a regular wave solution is not a globally
defined real-clock solution. Removable limits of some hydrodynamic observables
do not repair the missing phase.

For `A>B>0`, density is bounded below by `(A−B)^2`, so the local canonical
chart is valid. At destructive interference, the phase velocity is

\[
v_{max}=\frac{Dk(A+B)}{A-B}.
\]

It diverges as `B` approaches `A`, although wave energy remains finite.
For `A=1,Dk=.6`, the values are:

| B | minimum density | maximum phase velocity |
|---:|---:|---:|
| 0.6 | 0.16 | 2.4 |
| 0.9 | 0.01 | 11.4 |
| 0.99 | 0.0001 | 119.4 |
| 0.999 | 0.000001 | 1199.4 |

These are normalized classical velocities, not proposed astrophysical values.
Their unbounded growth is the structural point. If the physical clock uses a
fixed background rate plus this phase, the timelike-gradient condition must
be checked independently. A fixed finite rate does not control this entire
near-cancellation family. It is possible to choose a sufficiently large rate
for a fixed node-free member; that is not a uniform global-clock construction.

There is a second global issue in periodic geometry: the node-free `A>B`
solution has phase winding `k`. A periodic real-valued clock requires a global
lift or different boundary conditions. On the real spatial line one can use
local/global phase lifts away from nodes, but the equal-amplitude nodes still
block a regular clock phase.

## Controlled computation

Nine exact symbolic identities check the symplectic/energy transformation,
two-mode density/current/energy, the free wave equation and dispersion.
Deterministic Fourier evolution uses `A=1`, `B=.6` and `1`, `k=3`, `D=.2`,
grids `N=96,192,384,768`, and times `0,.125,1.234`.

- Maximum field error against the exact solution: `6.34e−15`.
- Maximum relative energy error: `4.44e−16`.
- An independent centered-difference energy check converges with orders
  `1.99444,1.99861,1.99965` for both amplitude choices.
- The capillary/kinetic energy identity is checked only on positive-density
  points. Nodes are explicitly marked outside the phase chart.

Exact Fourier evolution of finitely many resolved modes is an especially
strong benchmark for the stated family; it is not evidence for arbitrary
nonlinear wave evolution. The independent finite-difference check verifies
the spatial-energy normalization and its continuum limit.

## Relativistic and global cost

The displayed continuum wave model has dispersion
`omega=D k²/2` and group velocity `D k`, unbounded with wavenumber. It therefore
does not supply a fundamental finite propagation cone. An effective-theory
cutoff or a relativistic completion would be additional specified structure,
not a conclusion of this calculation.

The fixed-background canonical equivalence also does not establish the full
gravitational lapse/shift constraints, preservation of a timelike foliation,
behavior at nodes, or the mapping of a clock-defined MOND gate through the
transformation. In particular, a gate needing the unit clock normal can fail
even when the complex wave and its energy remain regular.

**Strongest safe conclusion:** Fisher capillarity supplies a local classical
wave repair using the same canonical pair; a categorical claim that every
wave repair necessarily adds a new classical degree of freedom is too strong.
Its extension through nodes changes the clock's admissible domain. A quantum
particle ontology does not follow from this classical variable change. The
remaining constructive task is a covariant same-clock completion whose global
domain includes the required transport states and whose causal/constraint
structure survives there, or a precisely delimited restriction that preserves
the needed phenomenology while excluding the problematic states.

## Evidence

`fisher_run_001/manifest.json` is the validated version-2 computation record;
runtime was 0.79 seconds with a 110-second wall-clock cap. The exact source,
software, command and result hashes are recorded there. The final Lean file
also includes local polar-gradient, Fisher-energy and canonical-Jacobian
identities, plus counterwave peak-velocity and nodal algebra. These formal
lemmas do not certify a full covariant field theory.

The combined transport/Fisher file compiled with exit 0: 18 theorems, no
warnings, no admitted proofs, and axiom dependencies confined to `propext`,
`Classical.choice`, `Quot.sound`. See `lean_record.json` and `lean_final.log`
for the final source hash, exact command and theorem-level output.

No external source theorem is used to justify the transformation: its local
identities are differentiated and checked directly. No dependency installation
or expensive pre-existing simulation was run.
