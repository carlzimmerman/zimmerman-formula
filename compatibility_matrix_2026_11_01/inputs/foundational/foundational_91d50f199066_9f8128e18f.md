# Central entropy floor: preservation proved, uniform seeding open

The full requested theorem for the virgin collapse is **not yet established**.
This phase proves long-term preservation from a wider central seed, without
an eternal outer guard, and global continuation of every exact finite mesh.
Uniform production of that seed remains the one load-bearing missing input.
The physical law and every coefficient are unchanged.

The quantified target is [TARGET.md](TARGET.md): one positive lower bound in
the cells intersecting the inner 5% of mass, independent of N>=32, valid for
all times after one common finite time. The objects proved about are exact
semidiscrete solutions, not finite-tolerance accepted states or dense output.

## Proved: a wider seed protects a smaller core forever

Suppose at a finite time t_s every cell intersecting a central mass prefix
of mass at least M_s has K>=k_0>0. For every smaller mass M_c<M_s,

\[
 \boxed{K_i(t)\ge k_0
       \left(\frac{M_s-M_c}{M-M_c}\right)^3,
 \qquad t\ge t_s,\quad m_{<i}\le M_c.}
\]

Here m_<i is the mass interior to cell i. A single k_0 and fixed mass margin
give a constant independent of resolution, moving density, heat-transfer
rates and elapsed time. Every cell intersecting the requested material
interval is covered; this is not just a central-cell or average-entropy bound.

The proof uses an auxiliary source-free heat flow along the actual geometry,
initialized at k_0 in the wider prefix and zero outside. Cooperative comparison
puts the actual K above this auxiliary solution. The auxiliary retains
descending K ordering, has maximum at most k_0, and has nondecreasing physical
entropy. Its seed entropy and these two bounds force the displayed floor.
The actual heated profile need not retain descending ordering.

The exact equal-mass formula is

\[
 K_i(t)\ge k_0\left(\frac{j_s-i+1}{N-i+1}\right)^3,
 \qquad 1\le i\le j_s.
\]

A tail version permanently protects any finite-mesh cell after it becomes
positive. Together with the compression threshold for never-heated cells
and exact conserved energy, it prevents finite-time shell collisions or
unbounded state on every fixed mesh. These continuation constants may
deteriorate with N. No continuum regularity or convergence theorem follows.

Full proof: [preservation_route.md](preservation_route.md).
Independent reconstruction: [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md).

## Proved reduction: one startup-compression estimate suffices

The exact cold phase is homologous for every N. All cells reach rho_q at
the common time t_a=0.5907973398405..., with compression
C_a=5.41458496044... . For each fixed N, continuity seeds positive K;
the resulting interval and lower bound have not been made uniform in N.

A source-driven version of the auxiliary argument gives a precise sufficient
uniform statement. If, for one common 0<T<=1/4,

\[
 C_i(t_a+s)\ge4,\qquad i\le\lceil N/4\rceil,
 \quad 0\le s\le T,\quad\text{every }N\ge32,                 \tag{UC}
\]

then rho>=exp(4s), and the original mechanical heater alone supplies

\[
 Q_i\ge64s^2(3-8s),\qquad B(T)=64T^3(1-2T).
\]

The heat flux cannot defeat the source-driven entropy comparison, so

\[
 \boxed{\inf_{t\ge t_a+T}\min_{i\le\lceil N/20\rceil}K_i(t)
       \ge\frac{64}{125}T^3(1-2T)>0.}
\]

The ceil-index ratio is at least 1/5 on every mesh. For example T=.005
would imply epsilon=6.336e-8 in the tested units. **That numerical constant is
conditional on (UC); it is not asserted as an established all-N floor.**
The source-driven argument handles heat losses directly; no new entropy floor,
insulation rule, material memory, sorting or energy injection is introduced.

The source proof, activation expansion, conditional small-stress bounds and
failed scalar-stress shortcut are in [seed_route.md](seed_route.md).

## What prevents promotion to the requested theorem

The old collapse heater itself introduces parabolic velocity diffusion as
soon as the density gate activates. Thus a sharp unaffected dust interior
cannot be justified by finite acoustic propagation. The free-surface
compression correction has an N^2 s^3 leading term at each fixed N; local ODE
continuity does not give a uniform global remainder. This is a failure of
that proof route, not a counterexample in the central quarter.

The total-stress equation has a heat cross term with no scalar minimum-principle
sign. Dropping it is invalid. A separate route proves an explicit penetration
bound for the homogeneous principal graph, uniformly for N>=32 and T=.001.
It isolates one exact nonlinear Duhamel remainder estimate, (NE), sufficient
to complete startup. That remainder retains geometry, variable bulk viscosity,
thermal pressure and memory damping; its required bound remains unproved.

See [startup_energy_route.md](startup_energy_route.md) and its
[independent audit](STARTUP_ENERGY_AUDIT.md). The
[adversarial route](obstruction_route.md) finds no counterexample for the
specified initial data. Ordered stationary cusps from other initial data do
not refute this initial-value claim. The bounded
[literature comparison](LITERATURE_NOTE.md) supplies no theorem transfer.

## New finite startup discriminator

The [current probe](startup_probe_v2.py) uses the existing exact cold phase,
then the unchanged full transport RHS at 81 actual warm diagnostic times
over s=0..0.005 on each of N=32,64,128,256,512,1024.
All six runs complete. At every retained time, central-quarter compression
is above 5.4145849595. Final minimum inner-5% K is about 3.61600127e-5.
Original-energy accepted-state bounds are below 2.155e-10 and the maximum
recorded sample error is below 2.168e-10.

These are finite sampled checks of (UC), not an interval-certified or all-N
proof. The [result](startup_finite_v2/result.json) and
[manifest](startup_finite_v2/manifest.json) preserve all 81 scalar traces.
The [first probe](startup_finite/result.json) is retained historically: its
proportional sample allocation left only two warm rows per grid despite a
nominal samples=81 argument. V2 corrects the observation schedule and keeps
the same physical handoff and law. [PROVENANCE.md](PROVENANCE.md) records this
distinction and fresh checks.

Energy conservation and conditional forest inactivity are inherited exactly:
shared luminosities telescope, mechanical damping supplies its own heat,
and h=0 makes local pressure/heaters/viscosity and both faces vanish. The proof
does not identify the chosen gate with actual observed forest histories.

Current state and next mathematical move: [STATUS.md](STATUS.md). The next
required work is an actual uniform nonlinear startup estimate, not another
late-time grid or an assumption of homogeneous motion after activation.
