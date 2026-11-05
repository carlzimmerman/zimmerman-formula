# AZ37 — moving Sun, lane 5(c)

Freeze before graded computation. Base0dadc61a63. AS3 part1 and H4/X3
equations inspected. Do not transfer AeST's alpha_1 result to v3s without
checking its action. Kappa = 1/2 FITTED; not theory closed.

## Target and possible verdicts

Determine the moving-Sun response in the khronon frame, with constraints,
initial/boundary data and the adopted switch retained. A full PASS needs
the physical moving branch on a Galactic charged background, a regular
solution over the claimed region and its metric response. A full FAIL
needs a physical inconsistency or measured exclusion of that branch.
An exact alternative branch or a linear local response alone gives
NO VERDICT on the complete moving-Sun prediction. In particular a static
potential divided into a moving gravitomagnetic coefficient is not alpha_1.

## 1. Exact branch and known answers

For v3s, check P=0, Q=1 and a geodesic hypersurface-orthogonal khronon.
Show the extra action's value and first variation vanish: P.A with A=0,
W(0)=W'(0)=0, F(0)=F'(0)=0, K(Q) and K'(Q) zero at Q=1. This is an exact
conditional GR branch, not a branch-selection theorem. Check the geometry
on Schwarzschild, f=1-2M/r, tau=E t+T(r), T'=sqrt(E²-f)/f:
Q²=1, normalized acceleration zero, and the unit constraint exactly.
Use symbolic E plus known E=1,13/12,5/3. The P-free, mu-free metric reduces
to GR. Alpha_1=alpha_2=0 refers only to this GR metric with its own G.
Do not infer a full preferred-frame bound from this conditional branch.

MUTATE constructs a flat-space congruence (omit M in T') but tests it on
the Schwarzschild metric. It must fail unit Q=1/geodesic consistency.
This is deliberately inconsistent input, not a second adopted theory.

## 2. Geodesic incoming-flow diagnostic

Trace Schwarzschild timelike geodesics of asymptotic speeds220 and369km/s,
with impact parameters b/r_capture=2,5,10,20 and r_capture=GM/v². Use
GM_sun=1.32712440018e20 SI and c=299792458. Incoming radial start at
R0=sqrt(100²+B²), R=r/r_capture. Set E=(1-v²/c²)^(-1/2), conserved
L/(r_capture)=E(v/c)B; set the incoming polar angle by the geodesic angular
integral from infinity, not a straight-line finite-start guess.

Integrate the radial second-order geodesic equation, polar angle and
coordinate time to an axis crossing or dimensionless proper time1000.
Known answers: conserved energy and angular momentum; Newtonian limit
of the radial equation; flat control has a straight ray with no focus.
DOP853 tolerances1e-9/1e-11, absolute tolerances1e-11/1e-13; convergence
of crossing coordinate/time and closest radius <=1e-5 relative. Scaled
energy drift max|E_measured²-E²|/(v²/c²)<=1e-7 on the fine trajectory.
Use paired angular quadrature tolerances1e-10/1e-12, agreement<=1e-8.

Require periapsis above the illustrative solar radius6.957e8m before
interpreting a vacuum trajectory. Axis focusing is a caustic warning for
the single-valued congruence, not failure of the GR metric and not a proof
that every v3s solution is singular. Record whether all tested rays focus.
MUTATE omits the mass also in the ray construction, while diagnostics still
use Schwarzschild: it must defeat the focusing witness and energy check.
Both footings are recorded separately; these geodesic quantities do not
depend on a0, which is an exact property of this branch.

## 3. Charged-background forced response

Derive from continuity, Bernoulli, polarization and Poisson at mu_K=0:

 rho_tau_ddot + Omega² rho_tau = K rho0 rho_source,
 Omega²=K rho0 [M_theta-1+(L_star²/2)k²].

Use a Fourier source exp(-i k.v t) switched on at t0 with zero response
and zero response velocity. This is a local frozen-coefficient PN test,
not a nonlinear Solar halo. Compare an exact50-digit convolution/oscillator
solution to DOP853 tolerance pairs1e-9/1e-11; relative error normalized by
max(1,|normalized response|)<=1e-7. Check resonance with its finite-time
limit rather than divide by zero. Known answers: zero-frequency source,
zero forcing, zero time and the explicit resonant oscillator.

Inputs: rho0=0.0447/0.0514 Msun/pc³ (H4's recorded Galactic phantom,
provisional background transcription), x_e=1.15/2.6, M_theta=(1+x_e)²;
L_star canonical21.68,24,27pc and alt22.85,24,24.60pc; v220,369km/s;
k=1/r for r1 and9.58AU; direction cosine0,Omega/(kv),1 when the middle
value is <=1; final times r/v and10r/v. No data likelihood or PPN exclusion
is graded from this finite-time response. Determine whether moving steady
forcing has a resonant direction. A pole invalidates a uniform static-to-
moving transfer, but finite-time growth alone is not a physical exclusion.

Use actual adopted canonical a0=9.3603e-11 and alt1.1312e-10 m/s² in
reporting each footing; never pool them. MUTATE may keep this invariant
linear-response subtest unchanged; the global negative control bites in
the independent geodesic construction. No invented failure of invariants.

## Execution and interpretation

Single thread, <1GB, minutes, no downloads. Separate main/mutant results,
input hashes, exact derivation, convergence pairs and README. Do not edit
AS3 or any older lane. Preserve the distinction between local GR branch,
caustic warning, charged-background response and an actual globally selected
moving-Sun solution. Identify the remaining nonlinear matching calculation.
