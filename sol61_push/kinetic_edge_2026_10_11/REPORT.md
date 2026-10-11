# The sharp target edge has a kinetic formation obligation

2026-10-11. Criteria-only commit `af43cd3c5`; 20/20 checks pass. This audit
does not replace the live CFG626 kernel comparison or invalidate CFG620's
finite-bin stationary construction. It separates existence from formation.

## Claim and hypotheses

In a static spherical Newtonian potential with nonnegative enclosed mass,
consider a stationary collisionless population whose entire orbits remain
inside radius R. Suppose g(R)>0 is finite and the phase-space density is bounded
above by a finite fmax near the edge. Then its spatial density tends to zero
as r approaches R from below, at least as fast as sqrt(R-r). This holds with
arbitrary velocity anisotropy. A hard truncation with nonzero limiting inner
density therefore requires an unbounded distribution (or different hypotheses).

This is a necessary regularity result, not a novelty claim, observational
verdict, stability theorem or full failure of candidate B.

## Derivation

At radius r<R let A=1-r^2/R^2, D=Phi(R)-Phi(r), and L=r vt, where vt is the
magnitude of the two transverse velocity components. A confined orbit has

`E <= E_R(L) = Phi(R)+L^2/(2R^2)`,
`vr^2 + A vt^2 <= 2D`.

To see the first bound, use the effective potential Phi+L^2/(2r^2). Its radial
derivative has the sign of G M(r)r-L^2, a nondecreasing function for nonnegative
mass. Outside the circular-orbit minimum it increases, so an outer turning
point at or below R implies E<=E_R. At that turning point, L^2<=G M(R)R.
There is no reflecting material wall or imposed impulse at R in this argument.

The ellipsoid bounds the allowed velocity volume by

`Omega_v(r) = (4pi/3) (2D)^(3/2)/A`.

Since D=g(R)(R-r)+o(R-r) and A=2(R-r)/R+o(R-r),

`rho(r) <= fmax Omega_v(r)`
`       = fmax (4pi/3) sqrt(2) R g(R)^(3/2) sqrt(R-r) [1+o(1)]`.

The transverse speeds can remain finite at the edge, but the radial velocity
width still collapses. Anisotropy does not remove that phase-volume loss for
bounded f. With specified fmax, this bound would constrain the thickness of
any region retaining a specified density; no primordial fmax is known here.

## Explicit loophole: singular stationary distributions

An overbroad claim that no stationary sharp edge exists would be wrong. In a
prescribed spherical potential, take

`f(E,L) = C / sqrt(E_R(L)-E)`

on the confined-orbit domain and zero elsewhere. This is stationary because it
depends only on conserved E and L. It diverges at the outer-turning-point
energy boundary. The velocity integral gives

`rho(r) = 2 sqrt(2) pi^2 C D/A`,
`rho(R-) = sqrt(2) pi^2 C g(R) R > 0`.

For completeness, the ellipsoid is within the confined domain: using
`D <= G M(R)(1/r-1/R)` gives
`L_max^2 <= G M(R) R * 2r/(R+r) < G M(R)R`.
The effective potential then has its minimum inside R and the outer turning
point at or below R. This argument assumes the usual accessible-orbit region.
The Kepler example is a tracer equilibrium in a prescribed potential; no
self-consistent Poisson solution for its own density is claimed.

Use w_t=sqrt(A) vt and w=sqrt(2D) sin(theta) to evaluate the integral; the
Jacobian is 1/A. The same substitution shows f log f is integrable at the
velocity boundary. Its spatial entropy density grows logarithmically as r->R,
which is also locally integrable in radius. Finite entropy therefore does not
imply bounded f. This example is NOT identified with CFG620's entropy maximizer.

## What this requires of a formation mechanism

A regular Hamiltonian flow transports f without changing its value along
characteristics. More generally, smooth compressible phase transport with
bounded integrated negative divergence preserves a finite bound on initially
bounded f for finite time. Such a flow cannot produce the exact nonzero-density
hard edge from bounded initial data. This is distinct from the earlier central-
cusp obstruction in captured_profile_2026_10_11: it applies at a finite outer
radius even if the centre is entirely regular.

There are genuine loopholes. Primordial perfectly cold phase sheets are
singular already. A collision/relaxation operator can be singular, and
coarse-grained distributions need not equal fine-grained Hamiltonian states.
Those choices require an explicit physical account; this audit supplies none.
For example, a fixed-target BGK equation has
`f(t)=exp(-lambda t) f(0)+(1-exp(-lambda t)) f_target`.
If f_target is unbounded, this operator creates an unbounded component at any
t>0. It is not evidence for formation by a regular Hamiltonian flow.

## Handoff to the current theory work

For each repaired-kernel target, inspect the one-sided density at the declared
cutoff. Where it stays positive, the action must explain the requisite singular
phase structure, or derive a finite transition layer from physical initial
conditions and transport. An arbitrary taper would change the fixed target;
it must not be inserted just to pass a test. Neither an imposed orbit cutoff
nor a finite-bin maximum-entropy fit establishes this mechanism.

The point-baryon outer law illustrates why the hypothesis matters: in the RAR
regime `Mc(r)=Mb/[exp(rM/r)-1]` has strictly positive derivative at every finite
radius. Cutting it at a finite supply radius gives a nonzero inner edge density.
The precise repaired-kernel continuum value should be checked in CFG626's
target; no new footing-dependent target fit was run here. The theorem itself
is independent of a0 and applies conditionally on each footing separately.

## Evidence and limits

The code checks the energy ellipsoid, angular-momentum bound algebra, exact
edge coefficients, constant-f and singular-f velocity integrals, entropy
integrals, and the zero-width limits. Independent quadrature uses three Kepler
gaps 1e-2,1e-4,1e-6. Omitting the transverse Jacobian or holding the velocity
volume constant triggers the MUTATE checks. The mathematical proof above,
not the finite numerical range, supplies the general conclusion. It was
self-reviewed; no independent agent audit was performed.

The canonical 1024^3 run (PID17844), its launcher (PID17843), and CFG626
(PID45651) were confirmed live during this turn. No competing PM run was
started and no partial output was scored. The full action, carrier, derived
settling rate, growth verdict and required observational suite remain open.
Kappa remains fitted. Claude's lane and sealed predictions are unchanged.
