# D5: same-clock bounded-DBI transport through crossing

**Result: implementation and finite assertion verified in the stated range.**
The bounded square-root kinetic term is a real improvement over the bare
quadratic homogeneous clock: its large-charge equation of state tends to dust,
not stiffness. Its convex Hamiltonian nevertheless does not prevent crossing
in the tested converging flows. The same-clock nonlinear equations reach a
zero fluid Jacobian with converged event times and small energy error.

The exact high-charge limit explains the alternatives: weak convergence is
held up and rebounds; sufficiently fast convergence reaches infinite density.
This is a scoped obstruction to this conservative pressure completion. It is
not a theorem excluding every higher-gradient or dispersive clock action.

## What was tested, and why this is the same clock

The prior L374 file was read, not executed. Its minimal quadratic condensate
plus a velocity-gradient term conserves energy but loses positive density near
crossing. Its successful complex-wave comparison changes the underlying field
description. This calculation instead uses the explicit single canonical pair
already belonging to a real clock:

\[
S=\int dt\,dx\left[\rho\Theta_t-
\frac{\rho}{2}\Theta_x^2-U(\rho)\right],\qquad v=-\Theta_x,\quad\rho>0.
\]

There is no second phase, complex wave field, particle species, or extra
canonical pair. `rho` is the conjugate momentum of `Theta`; it has no independent
time-derivative term. Varying it gives
`Theta_t−Theta_x²/2=U′(rho)`. If `U″>0`, eliminating it algebraically returns the
one-clock kinetic Lagrangian `K(Theta_t−Theta_x²/2)`. The fluid mass coordinate
used below is a coordinate transformation while density stays positive, not a
new population of particles.

This is a nonrelativistic one-dimensional sector on a fixed background. Its
identification with a fully covariant gravitational clock, all metric/foliation
variations and the full constraint count remain outside this calculation.

Variation and spatial differentiation give the exact nonlinear equations

\[
\rho_t+(\rho v)_x=0,\qquad
v_t+vv_x=-U''(\rho)\rho_x,
\]

with pressure `p=rho U′−U`, sound speed squared `rho U″`, conserved momentum,
and Hamiltonian

\[
H=\int dx\left[\frac{\rho v^2}{2}+U(\rho)\right].
\]

## The actual bounded kinetic term

The repository's `doorB_quadratic_vs_dbi.py` supplies the family, with
`kappa=2 mu²` and `lambda=lambda_D` in its notation:

\[
K(u)=\frac{\kappa}{\lambda}
 [1-\sqrt{1-\lambda u^2}],\qquad
0<u<\lambda^{-1/2},\quad\kappa,\lambda>0.
\]

The positive-current branch has the exact Legendre transform

\[
\rho=K'(u)=\frac{\kappa u}{\sqrt{1-\lambda u^2}},\qquad
u=\frac{\rho}{\sqrt{\kappa^2+\lambda\rho^2}},
\]

\[
U(\rho)=\frac{\sqrt{\kappa^2+\lambda\rho^2}-\kappa}{\lambda},\qquad
U''(\rho)=\frac{\kappa^2}{(\kappa^2+\lambda\rho^2)^{3/2}}>0.
\]

Both kinetic and internal Hamiltonian terms are nonnegative on the physical
domain. Positivity/convexity therefore hold here, yet will not guarantee a
global fluid coordinate map. A fixed clock-rate term `Q0 rho` shifts the energy
and clock rate without changing these transport equations.

For homogeneous conserved charge `rho=J/a³`, total energy and pressure are
`epsilon=Q0 rho+U(rho)` and `p=rho U′−U`. The quadratic choice
`U=rho²/(2 kappa)` gives `p/epsilon→1` as `a→0`. The bounded choice gives

\[
\epsilon/\rho\longrightarrow Q_0+\lambda^{-1/2},\qquad
p/\epsilon\longrightarrow0.
\]

These limits are derived, not inferred from numerical samples. They repair
this particular stiff-background problem. They neither fix the initial charge
`J` nor establish a CMB/forest/halo fit. The older source's broad claims about
vanishing strong coupling are not used here.

## Exact fluid-coordinate dynamics

Set `x=X(m,t)`, where `dm=rho dx`, so `tau=X_m=1/rho>0` and `X_t=v`.
Then

\[
E=\int dm\,[v^2/2+e(\tau)],\qquad
e(\tau)=\tau U(1/\tau)
=\frac{\sqrt{\kappa^2\tau^2+\lambda}-\kappa\tau}{\lambda},
\]

\[
X_{tt}=\partial_m e'(X_m),\qquad
e''(\tau)=\frac{\kappa^2}{(\kappa^2\tau^2+\lambda)^{3/2}}.
\]

Choose unit mean Jacobian and wavenumber, let
`eta=kappa/sqrt(lambda)` and measure time in units of
`c_infinity=sqrt(kappa²/lambda^(3/2))`. Removing constant and linear terms from
the energy, which do not affect the periodic equations, gives

\[
\widehat e(\tau)=\frac{\sqrt{1+\eta^2\tau^2}-1}{\eta^2}
=\frac{\tau^2}{\sqrt{1+\eta^2\tau^2}+1},\qquad
\widehat e''(\tau)=(1+\eta^2\tau^2)^{-3/2}.
\]

The rationalized expression avoids cancellation at small `eta`. The coefficient
remains finite and positive at `tau=0`; the Hamiltonian provides no infinite
barrier to a vanishing map Jacobian.

## The exact cold/high-charge limit

At `eta=0`, the equation is exactly `X_tt=X_mm`. With uniform initial density
and `v(m,0)=−M sin(m)`, an exact solution is

\[
X=m-M\sin m\sin t,\quad
v=-M\sin m\cos t,\quad
\tau=1-M\cos m\sin t.
\]

This linear equation is for the map of the same nonlinear clock fluid. It is
not a newly postulated wave species. In Eulerian variables its constitutive
law is the inverse-density/Chaplygin pressure limit of the bounded kinetic term.

For `0≤M<1`, `tau≥1−M>0` for every mass coordinate and time. A valid smooth
fluid solution thus exists in this particular family for all time. It rebounds:
at `t=pi`, `X=m` and `v=+M sin(m)`, opposite the initial velocity. Collisionless
free streaming would continue as `X_ballistic=m−M t sin(m)`, with its first
crossing at `t=1/M`.

For `M>1`, the first zero Jacobian is at `m=0` and

\[
t_* = \arcsin(1/M),\qquad
\rho(0,t)\longrightarrow+\infty\quad(t\uparrow t_*).
\]

The first-event statement follows from `cos(m)≤1` and the strict increase of
`sin(t)` from zero to `1/M` on this initial interval. At `M=1`, the Jacobian
first vanishes at `t=pi/2`. At `M=2`, `t*=pi/6≈0.523599` versus ballistic `0.5`.
As `M` increases, `M arcsin(1/M)→1`: cold high-Mach collapse approaches ballistic
crossing rather than being removed.

The exact conserved energy is

\[
E=2\pi(1/2+M^2/4),\qquad P=0,\qquad\mathcal M=2\pi.
\]

Continuing the analytic map beyond `tau=0` continues the wave equation but
leaves the positive-density, single-valued clock-fluid domain. Energy
conservation alone must not be mistaken for a valid physical continuation.

## Controlled finite-eta calculation

The code discretizes the mass-coordinate action, with edge Jacobians
`tau_j=1+(u_(j+1)−u_j)/dm` and discrete Hamiltonian
`sum dm [v_j²/2+ehat(tau_j)]`. Its acceleration is the exact negative gradient
of this discrete Hamiltonian. Velocity Verlet splits the kinetic and potential
flows; periodic momentum is conserved by telescoping forces. Every trajectory
stops at the first step whose minimum Jacobian is nonpositive. Event time is
interpolated inside that step; no post-crossing state is claimed physical.

The amplitude variable called `mach` in the code is `M=V/c_infinity`. The
actual initial Mach number is `M (1+eta²)^(3/4)`; the distinction matters because
the finite-eta initial sound speed is smaller than the limiting sound speed.

| eta | M | N=128 event | N=256 event | N=512 event | ratio of successive spatial differences |
|---|---:|---:|---:|---:|---:|
| 0.10 | 2 | 0.523692367 | 0.523531336 | 0.523491134 | 4.01 |
| 0.25 | 2 | 0.523082697 | 0.522920085 | 0.522880778 | 4.14 |
| 0.50 | 2 | 0.521197038 | 0.521029932 | 0.520993405 | 4.57 |

All three finite-eta branches lose positive density in the fluid-map sense.
The finest-grid trajectories' energy drift is at most `1.0e−6`, including the
one step that brackets the event. Halving the time step twice at `eta=.25`,
`M=2`, `N=512` changes the interpolated event by at most `3.67e−7`.

The `eta=0`, `M=.5` exact benchmark at grids `64,128,256,512` gives maximum
displacement convergence orders `2.00055,2.00013,2.00002` over a complete
acoustic period. Finite-eta `M=.5` runs retain positive Jacobians through that
period; at the finest grid the minima are `0.497829`, `0.486661`, and
`0.450121`. This is a finite-time result for those initial data, not a global
well-posedness theorem at nonzero eta.

Across all 25 trajectories, the largest relative discrete-energy drift is
`4.28e−5`; momentum error is below `1e−11`. Total mass is fixed exactly by the
mass-coordinate domain, so it is not an independent empirical accuracy test.
The exact solution, measured second-order convergence, momentum telescoping
and independent time-step refinement provide the independent controls.

## Exact local multistream obstruction

For two positive streams of weights `a,b` and distinct speeds `va,vb`, define
`rho=a+b`, `j=a va+b vb`, and `Pi=a va²+b vb²`. Then

\[
\rho\Pi-j^2=ab(v_a-v_b)^2>0.
\]

Equal-weight streams at velocities `+V,-V` all have `rho=1,j=0`, but their
stress is `Pi=V²`. No pressure law that depends only on the same local density
and current can match both `V=1` and `V=2`. The actual single-clock barotropic
closure has exactly that limitation. This is not a claim that a scalar with
spatial oscillations, dispersive stress or additional state information can
never approximate multistream moments after coarse graining.

## Formal certificate and remaining door

`fable_independent_2026/lean_2026/DoorsTransport20260926.lean` contains exact
moment identities, strict variance, the explicit map's derivative equations,
subcritical positive-Jacobian theorem, supercritical zero-Jacobian witness and
half-period rebound. The final compiler record and axiom report are stored
beside this report; numerical results and the action reduction have a separate
scope. No full-theory certification is claimed.

The final Lean run compiled all 18 transport/Fisher statements with exit 0 and
no warnings. `lean_record.json` binds the final source hash to the successful
command, runtime and every axiom report; `lean_final.log` is the accepted log.
All dependencies lie in `{propext, Classical.choice, Quot.sound}`. No proof
admissions or custom source axioms occur. The initial draft's compile errors
and a 110-second timeout are retained separately and are not accepted evidence.
The final bounded retry used `lake env lean -j 1 DoorsTransport20260926.lean`
and completed in 126.36 seconds under a 180-second cap. All scientific Python
runs completed in under two seconds.

The Fisher follow-up in `FISHER_BRIDGE.md` constructs and checks a local
canonical capillarity bridge using the same pair, then identifies its nodal
and timelike-clock limitations. The remaining transport door is a global
conservative higher-spatial-gradient completion of this *same clock*, with its action, canonical count and physical
domain stated explicitly, that maintains a valid continuation and reproduces
the necessary coarse-grained stress. A positive quadratic spectrum or convex
local kinetic term does not supply that missing implication. The pressure-only
DBI completion tested here does not supply it in the high-Mach family.

## Reproduction and source provenance

`run_002/manifest.json` is a validated computation-audit version-2 record with
the exact command, software versions, input/result hashes, elapsed time and
110-second wall-clock cap. Runtime was 1.17 seconds. The numerical-library
thread cap was cooperative; no memory cap or platform CPU-affinity claim was
made. No network access, dependency installation or existing expensive lane
execution was used.

The result can be reproduced with the command recorded in that manifest, using
a fresh output directory. Validate the current record with:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py real_research/closure_doors_2026_09_26/transport/run_002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Read-only reference SHA-256 values:

| Source | SHA-256 |
|---|---|
| L374 source | `e3248164fc68b129d235c3c07f6e13482fa85d499c49d07a4de27b9506843ee3` |
| L374 result | `7605cdfc92f1b8264e7be7d6b3413fafad9b27f46bbee91233911ff9a4ac8667` |
| `doorB_quadratic_vs_dbi.py` | `3a040a5f9512337d4c71049944e492b6c874f1754206206ab2e3d669b358c940` |

The external-paper attributions in old comments were not needed to derive or
run this explicit action. No external literature claim is promoted by this
calculation. The original action/interpretation remains conditional on its
identification with the desired full theory.

The first computation record (`run_001`) predates an added exact inverse-current
identity. It is retained as development provenance; `run_002` is the accepted
record matching the final source. Numerical results are unchanged.

Final self-review checked the new equations, sign conventions (`v=-Theta_x`),
the positive-density domain, the distinction between exact and finite-range
claims, and the local versus global canonical interpretation. No claim of
full theory closure or quantum-particle ontology is made.
