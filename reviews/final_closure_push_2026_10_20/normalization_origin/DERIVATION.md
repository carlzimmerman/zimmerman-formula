# A normalization obstruction to the tracer compression construction

Base: `f659e6d8e1ee4cf2b756f091aff56b018da1fb1e`.
New local mathematical result; self-reviewed and then scope-restricted
following independent review. No external novelty claim.

**Verdict: refuted in the macroscopic continuum/mean-field regime under the
stated volume/source conventions.** The existing conditioned harmonic tracer
construction, in its declared x=10 finite-core window and with a smooth
macroscopic gravitating cloud, cannot reach unit gravitational susceptibility
while keeping its scalar self-gravity perturbatively small, if its source
length is at least the reference rms cloud radius. The smooth-gravity step
requires this continuum/mean-field hypothesis (normally N much greater than
one); it is not an implication for arbitrary finite N. In particular, N=1
has no gravitational self-pair. This does
not refute the full theory, every contact/collective state, or a physical
acceleration law. The source here remains a curvature/compression moment.

## Exact claim and dependency

Use the classical independent-particle model in
`sol61_push/nonlinear_origin_2026_10_19/canonical_response/CANONICAL_RESPONSE.md`,
but include its declared finite-core conditioning exactly. The core is
uniform, supported, of radius R, density rho_b and curvature
`kappa=4 pi G rho_b/3`. The cloud contains N particles of mass m at fixed
temperature T (k_B=1), and is conditioned to `r<R`. Define

```
x = m kappa R^2/(2T),  V=4 pi R^3/3,
Q = m sum_i r_i^2/(2L),  H(E)=H(0)+E Q,
chi = -d<Q>/dE = Var(Q)/T,  q=Nm/(V rho_b),
t = x r^2/R^2,  nu=3/2.
```

L is fixed under E variation. In particular, taking L equal to the
reference rms radius does not mean varying L with the cloud width.
These are the actual source and volume conventions; rescaling E by choosing
a different L changes this coefficient. No identity equates Q to a common
gravitational mass dipole.

Let `P=gamma(3/2,x)/Gamma(3/2)` and put

```
mu = gamma(5/2,x)/gamma(3/2,x),
v  = gamma(7/2,x)/gamma(3/2,x) - mu^2.
```

The probability density of t is `t^(1/2) exp(-t)/gamma(3/2,x)` on (0,x).
Direct integration gives `<r^2>=R^2 mu/x`,
`Var(r^2)=R^4 v/x^2`, and

```
C := 4 pi G chi/V = (3q v/(2x)) R^2/L^2.             (1)
q(C=1) = (2x/(3v)) L^2/R^2.                         (2)
rho_d(0)/rho_b = 4q x^(3/2)/(3 sqrt(pi) P).           (3)
```

Equation (1) uses the variance of the sum of independent variables and
`T/m=kappa R^2/(2x)`. It is exact for this conditioned tracer model.
Equation (3) follows by integrating its spherical one-particle mean density,
rather than replacing the peak by an arbitrary volume average. Equations
(1)-(3), as response and mean-density identities, hold for the independent
N-particle tracer distribution. To interpret (3) as a gravitational curvature
ratio, additionally treat this mean density as a smooth continuum source.
Under that hypothesis, spherical Newtonian gravity makes it exactly the
dark/baryon curvature ratio as r tends to zero, so small self-gravity
requires it small. No assumption about an outer dark profile is used in
that necessary continuum local test. It is not the curvature of a single
discrete particle configuration.

At the already-declared finite-core window x=10:

| fixed source length | q required by C=1 | central smooth/mean dark/baryon density |
|---|---:|---:|
| L=R | 4.490532482 | 106.840365954 |
| L=reference rms | 0.672852291 | 16.008744006 |

The second row supplies a lower bound on the necessary central ratio for
all `L>=reference rms`. At general L it scales as L^2. The exact values
used are `mu=1.498379742782376`, `v=1.484604931199120` and
`<r^2>/R^2=0.149837974278238`.

A separate continuum energy check strengthens the conclusion. Any spherical
nonnegative smooth density supported in radius R obeys

```
|W_self| >= G Md^2/(2R),
U_trap = (kappa/2) Md <r^2>,
|W_self|/U_trap >= q R^2/<r^2> = q x/mu.             (4)
```

For example, the first inequality follows from
`|W|=integral_0^Md G M/r(M) dM` and `r(M)<=R`.
At the first row's inventory the lower bound is **29.9693**; at the
second row's inventory it is **4.49053**. Thus both local-force and
global-energy tests fail the tracer approximation at unit normalization.
The sign is attractive; the neglected field cannot cancel itself.

For completeness, the exact finite-N correction in the independent product
reference distribution excludes self-pairs. If `W_smooth` is the density
functional in (4), then

```
<W_pairs> = (1-1/N) W_smooth,
|<W_pairs>|/<U_trap> >= (1-1/N) q x/mu.              (4a)
```

Conditioned on a tagged particle position, its other N-1 particles have
mean density `(1-1/N) rho_d`; their ensemble-averaged force profile therefore
has `(1-1/N)` times the displayed smooth curvature ratio. Discrete force
fluctuations are not controlled by this mean profile. For N=1 both effects
are zero, so an unrestricted-N self-gravity obstruction would be false.
For N>=2 the expected pair-energy lower bounds are at least half those in
(4), namely 14.9846 for L=R and 2.24527 for L=rms; that energy diagnostic is
already non-perturbative in expectation, but is not a smooth-density or
per-realization curvature theorem. The principal stated result uses the
macroscopic continuum regime, where the factor tends to one.

Making the conditioning tail smaller does not repair this. As x increases,
`mu,v -> 3/2`. At L=rms, the central ratio at C=1 grows as
`[8/(9 sqrt(pi))] x^(3/2)`; at L=R it grows as
`[16/(27 sqrt(pi))] x^(5/2)`. Choosing L much smaller than the cloud
can avoid this particular obstruction, but chooses the normalization of
a curvature source; it supplies no physical map to acceleration dipoles.

Dependency graph: existing tracer Hamiltonian and the supported-core
convention -> elementary truncated Gaussian integrals -> actual variance
response -> required mass -> explicitly macroscopic continuum gravity ->
Newtonian central curvature/energy diagnostic. Finite-N pair expectations
instead use (4a), without identifying an individual configuration with its
one-particle mean density.
No fitted kappa, de Sitter unit, observed acceleration or portal tie enters.

## Executed backreaction continuation

To check the consequence of actually retaining self-gravity, use the
declared local isothermal free-energy closure

```
F[rho] = c_s^2 int rho(log(rho/rho*)-1)
       + (u/2) int rho^2 + (s kappa0/2) int rho r^2
       - (G/2) int int rho(r)rho(r')/|r-r'|,
c_s^2=T/m, u=g2/m^2>0, g2=lambda_rep/(2m^2).
```

This retains the original positive matched daughter contact. It is a
conditional mean-field thermal closure, not a proof that the full quantum
thermal action has this EOS over every chosen state. The uniform host,
confining/conditioned wall, temperature, mass, contact ratio and heat
receiver remain specified inputs. The host is supported; it is not a
live gravitational center-of-mass anchor.

In units `r0=c_s/sqrt(kappa0)`, put `R/r0=sqrt(20)`,
`eta=u rho_b/c_s^2`, `delta=rho(0)/rho_b`, `h=log[rho/rho(0)]`,
and `w=G M(<r)/(r0 c_s^2)`. The complete spherical stationary equations are

```
h' = -(s r + w/r^2)/(1+eta delta exp(h)),
w' = 3 delta r^2 exp(h), h(0)=w(0)=0,
w(R) = q R^3, q=4.490532482121004.                   (5)
```

Shoot in delta to preserve the same tracer-selected inventory. E is
`kappa0 L(s-1)` with L=R. Compute the full static width derivative, not
the tracer variance formula applied to the interacting density:

```
4 pi G chi/V = -(3q/(2R^2)) d<r^2>/ds.              (6)
```

Three stationary controls at s=1 give:

| eta | central density / rho_b | 4 pi G chi/V | compression fraction at s=2 |
|---|---:|---:|---:|
| 0.1 | ~6960.8 | ~0.0000111 | ~0.000253 |
| 1 | ~219.34 | ~0.003558 | ~0.007938 |
| 10 | ~9.5204 | ~0.13683 | ~0.041547 |

The unconditioned tracer rational formula would give 0.5 in the last
column; the exact x=10 finite-wall tracer gives approximately 0.4994594.
These
particular full stationary branches therefore preserve neither its
coefficient nor its source scale. Allowing an independently fitted source
scale can approximate some finite intervals; that is a different
state-dependent fit, not a universal prediction. We do not claim these
stationary branches are unique, physical thermal states, stable minima,
or a complete catalog of all stationary solutions.

## Evidence, review and precise continuation

`check_backreaction.py` uses only stdlib arithmetic, incomplete-gamma
recurrences, independent Simpson moment integrals and spherical RK4 mass
shooting. `run_004` is the current-source run. Its mesh and derivative
refinement checks have explicit tolerances; no interval certification is
claimed. Histories and actual statuses are preserved in the run manifests.
The exact argument above is distinct from those finite numerical controls.

Self-review checks: units of Q and E; actual finite-core variance rather
than an unconditioned formula; positive sign and central limit of Newtonian
gravity; shell-energy bound; fixed L during differentiation; one-copy
Poisson gravity; physical EOS hypotheses; and the absence of any uniform
acceleration operator bridge. External proof/source verification is not a
load-bearing leaf. Independent review remains available to the coordinator.

The scoped macroscopic target is resolved: one cannot normalize this declared
continuum tracer construction by adding the necessary inventory and continue
using its tracer response. No unrestricted finite-N statement is asserted.
The theory's normalization target remains open. The
cheapest continuation is to choose one independently supported live host
and measured/microscopic EOS, derive its complete source, and vary the
thermal receiver and loading at fixed microscopic constants while solving
the interacting response. Before fitting anything, test whether any
formation rule selects both the mass and susceptibility. A compression
state could still be useful, but it must first supply the missing map
from tidal/curvature operators to the acceleration-conjugate response.
Kappa=1/2 remains fitted under CFG908/CFG911; this calculation neither
selects a dark-energy portal nor derives a cold abundance.
