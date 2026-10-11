# Inner stream selection: separate the scale formula from the kernel

Checkpoint 2026-10-11, source base `19d8c776494f0995d5b6b9330dd3ca5065025f5e`.
Original research objective remains OPEN under [RESEARCH_CONTRACT](../RESEARCH_CONTRACT.md).
The previous turn verified a push and proposed an experiment; this checkpoint
adds mathematical results and bounded computational evidence.

**The useful result is a kernel-dependent route to kinetic support.** The
repository's existing repaired kernel admits a positive isotropic
high-binding-energy distribution for its inner cusp. The exponential kernel
instead requires very strong low-angular-momentum suppression in the
bounded-energy class examined here. These are different physical obligations,
even though both kernels use the same separate acceleration-scale formula.
Neither result derives formation or identifies a new substance.

## What changed in the latest record

[CFG620](../../campaign_fresh_gravity/CFG620_anisotropic_velocity_target/README.md)
constructs stationary orbit weights conditional on the entire exponential
density. Its success in supporting that density is not an independent density
selection. [CFG623](../../campaign_fresh_gravity/CFG623_merger_stopwatch_v5/README.md)
allows the sampled alpha=0 node, excludes 0.1, 0.3 and infinity, and leaves
1--10 unscorable under its frozen rule. This keeps collisionless transport and
formation history relevant; it does not exclude every finite settling rate.

## 1. The exponential target specifies an orbital tail

For compact baryons, `mu=G M_b`, `r_M=sqrt(mu/a0)`, and a fixed bounded
orbital-energy band, an explicit compatible inner distribution is

\[
 f(E,j)\sim F(E)j^{-8}\exp[-2\mu r_M/j^2].
\]

The independently derived velocity integral gives
`rho_c ~ const r^(-4) exp(-r_M/r)`, with its normalization in
[DERIVATION](DERIVATION.md), equations (5)--(6). A finite algebraic low-j
population instead gives a power-law density. The compatible exponential
distribution is a construction, not a unique inverse or a dynamically
selected state. Positivity prevents cancelling unwanted inner traffic with
another positive orbit family.

For an explicitly specified fixed-energy diffusion, equation (9) in that note
translates the desired tail into a condition on measured drift and variance.
It is therefore possible to test a proposed torque mechanism before running
a large halo simulation. A first-order uniformly phased quadrupole kick has
algebraic leakage at low angular momentum even when it increases mean-square
angular momentum; that is a useful control against mistaking spin growth for
core evacuation. General coherent or energy-coupled torques remain open.

These are exterior point-source asymptotics. They require an annulus between
the baryonic size and r_M, and cannot be extrapolated through finite baryons
or a relativistic compact-object interior.

## 2. The existing repair supplies a less restrictive inner construction

The continuous repaired interpolation already used in the repository has
`h=y(nu-1)` with a logarithmic high-y tail. Its exact splice starts at
`y_s=2.337412405`, and its logarithmic coefficient is
`b_log=0.032380512`. It yields positive effective cold density for every
nonnegative spherical baryon density. Outside compact baryons its cusp is

\[
 \rho_c(r)\sim\frac{a_0 b_{\log}}{\pi G r}\log(r_M/r).
\]

This is compatible locally with an isotropic distribution of passing bound
orbits. In a Kepler-dominated inner potential, write
`rho=A Psi log(Psi/E0)+C Psi+O(log Psi)`, with `A>0`. The corresponding
high-binding asymptotic is

\[
 f(\mathcal E)\sim
 \frac{A\log(\mathcal E/E_0)+C+A(1+\log4)}
 {\sqrt8\,\pi^2\sqrt{\mathcal E}}.
\]

It is positive at sufficiently high binding energy. A separately constructed
DF, cut below `E=1` in dimensionless units, verifies the first two density
terms by direct forward integration, with a subleading `O(sqrt(Psi))`
remainder. That finite construction does not reproduce the exact repaired
density's smaller remainder. The analytic inversion, source translation,
and coefficient derivation are in [SOURCES_AND_KERNEL](SOURCES_AND_KERNEL.md).

The high-binding construction uses an unbounded energy range at the
mathematical point source. It is outside the bounded-energy hypothesis of
the exponential-tail argument. The two results are consistent.

The repair is prior work, not a new interpolation or data fit. Its table
implementations eventually clamp the logarithm; their literal far-inner
cusp is `1/r`. A complete positive distribution, finite source, physical
outer boundary and stability have not been established here. Its known
planetary anomaly when assigning a halo to the Sun means host ownership
still needs a physical derivation. Removing an inner hollow does not remove
that obligation.

## 3. Transfer is possible; normalization remains an independent gap

The small rotating-quadrupole integration changes angular momentum while
conserving `E-Omega_p L_z` to `5.78e-9` over 40 dimensionless time units.
Its maximum `|Delta L_z|` is `0.00803`. This verifies an implemented exchange
channel and its work accounting, not a density selector. The imposed pattern
is an external energy reservoir; baryonic backreaction was not simulated.
The standard identity is also discussed by
[Dillamore and Sanders](https://academic.oup.com/mnras/article/542/2/1331/8220894).

In the exponential construction, define `K=2 G M_b r_M`, with units of
specific angular momentum squared. Then

\[
 a_0=\frac{4(GM_b)^3}{K^2},\qquad
 \kappa=\frac{4(GM_b)^3}{K^2c\sqrt{G\rho_{DE}}}.
\]

Thus `kappa=1/2` would require `K^2=8(GM_b)^3/[c sqrt(G rho_DE)]`.
Choosing K to reproduce the density inserts this relation; it does not
derive it. The current torque equations contain no vacuum coupling. With
`Lambda=8 pi G rho_DE/c^2`, the coefficient remains `32 pi`, not `32 pi^2`.

## Evidence, review and next execution

The successful [run_v2 manifest](run_v2/manifest.json) validates, with all 55
finite assertions passing. It includes two independent quadrature variables,
polynomial low-j controls, direct density differentiation, the positive
cutoff-DF reconstruction and the rotating-potential conservation check.
Three mutation checks reject the wrong exponential scale, kernel substitution
and pattern-work sign. Resource limits were 45 wall seconds, 35 CPU seconds
and cooperative one-thread library limits; the actual run took under one
second. No cosmological job was launched or disturbed.

The initial [run](run/manifest.json) passed 54/55. A centered derivative
straddled the C1 splice, where its usual quadratic error assumption fails.
Decreasing its step showed linear error; a one-sided second-order derivative
on a single branch resolved it without changing the tolerance or physics.
The original source is preserved as [run/input_check.py](run/input_check.py),
matching the old manifest's source hash. That historical manifest refers to
the then-current check.py; its old path is intentionally stale after the
correction. It must not be presented as current-input validation.

Independent review rederived the main coefficients and identified two
qualifications now included in DERIVATION: differentiating an asymptotic
requires a derivative bound, and pericenter lifting cannot discard perturbing
potential work merely because the perturbation is weak. Review agreement is
not a proof certificate; the displayed reductions provide the arguments.

The immediate executable continuation is a **reciprocal baryonic rotor**:
use a specified positive baryonic density, evolve its spin along with passing
streams, and compare prograde/retrograde populations at matched conserved
totals. Measure core traffic and energy transfer, rather than final fitted
orbit weights. It remains a transfer-channel test, not a kappa derivation.
The repaired-kernel global support route is separately open; it needs a
physical outer boundary before a global inversion can be claimed. Formation,
the cold component's identity and abundance, host ownership, the vacuum
coupling and the common observational dynamics remain unresolved.
