# Quantum production of a candidate cold field

2026-10-11. Research base inspected: `a14ce01931a730301447b53d8762af82e87eace6`.
Scope: this directory only. The run manifest records the execution revision
and dirty state separately because the repository has concurrent work.

**Result: an explicit finite quantum model converts a depleted source into
massive, low-momentum field excitations starting from their vacuum.** This
is a conditional production mechanism for a possible carrier, not a completed
origin of the repository's cold energy. The carrier's identity, cosmic amount,
survival after production, galaxy law and vacuum coupling remain open.

The previous chat's photon route established kinematics only. No photon
production rate or empirically allowed interaction was established. After the
user clarified theoretical formation, that hardware route was deferred.

## What is being made

The current [carrier proposal](../microscopic_carrier_2026_10_10/REPORT.md)
uses a nonrelativistic massive complex field. Its number-conserving evolution
cannot create an occupied field from zero. Cosmological misalignment is
already considered in [CFG288](../../campaign_fresh_gravity/CFG288_one_field_dark_sector/README.md)
and [CFG362](../../campaign_fresh_gravity/CFG362_inflation_amount/README.md).
Repeating that construction would not resolve its free initial energy.

Here the production target is narrower and explicit: begin with energy in a
source and zero daughter quanta; convert some of that energy to a massive
complex field with small momentum, accounting for source depletion. Success
on this target does not establish the full user goal.

## A stable candidate interaction

Use natural units, positive canonical kinetic terms, a real source field
chi and a complex daughter Phi. Declare

\[
 V=\rho_\Lambda+\tfrac12M^2\chi^2+m^2|\Phi|^2
       +\mu\chi|\Phi|^2+\lambda|\Phi|^4,
 \qquad m^2,M^2>0,\quad\lambda>\frac{\mu^2}{2M^2}.
\]

The exact identity

\[
 V-\rho_\Lambda=\frac{M^2}{2}
 \left(\chi+\frac{\mu|\Phi|^2}{M^2}\right)^2
 +m^2|\Phi|^2+
 \left(\lambda-\frac{\mu^2}{2M^2}\right)|\Phi|^4
\]

shows that the classical potential is bounded below and has its minimum at
zero fields. This is a tree-level stability statement, not a radiative
naturalness analysis. The interaction permits chi -> Phi + anti-Phi while
preserving Phi's U(1) charge. Equal particle and antiparticle production
has zero charge but positive total energy. It cannot generate a nonzero net
charge from a neutral source.

**Model change:** chi is an additional source degree of freedom. It is not
derived from the repo and does not satisfy a strict one-field requirement.
This is an optional extension, not an edit to the original theory. The
produced particle/antiparticle mixture also needs a two-component reduction;
it cannot silently be substituted for a single charged condensate.

## Making the products cold

For a source quantum at rest,

\[
 \omega=M/2,\quad k=\sqrt{M^2/4-m^2},\quad
 u=k/m,\quad \beta^2=\frac{u^2}{1+u^2}.
\]

Choosing M only slightly above 2m creates nonrelativistic products directly.
For u=0.001, M/(2m)-1=4.99999875e-7 and beta is approximately 0.001.
An isotropic population has P/rho=beta^2/3=3.33333000e-7 when interactions
are negligible. For just two opposite beams this is the trace of the stress
divided by three times the energy density; the stress is anisotropic.
Small P/rho alone is not a structure-formation or sound-speed test.

The mass splitting is a chosen parameter, not a prediction or protected
relation. Exactly at M=2m the continuum two-body phase space vanishes;
arbitrarily cold does not mean arbitrarily rapid production. For distinct
daughter and antidaughter, the dilute vacuum decay width is
Gamma=mu^2 beta/(16 pi M). It is not used as a many-body production rate here.
Parent motion would contribute additional daughter velocity dispersion.

## A one complex field realization

The separate-source construction is not necessary for the conversion vertex.
There is a second, explicit candidate using one complex order parameter
Phi=(X+iY)/sqrt(2), with canonical real components X and Y:

\[
 V(X,Y)=\rho_\Lambda+\frac{\lambda}{4}(X^2+Y^2-f^2)^2
                  +\frac{m^2}{2}Y^2,\qquad \lambda,f,m>0.
\]

This potential is nonnegative above rho_Lambda and has minima (X,Y)=(+/-f,0).
Around the +f vacuum put X=f+h, Y=y. Exactly,

\[
 V-\rho_\Lambda=\lambda f^2h^2+\tfrac12m^2y^2
       +\lambda f h(h^2+y^2)+\tfrac\lambda4(h^2+y^2)^2.
\]

The radial mode h has M^2=2 lambda f^2. The transverse, massive phase-like
mode y has mass m; its y -> -y parity forbids decay of a single y quantum
into only radial quanta. The h y y vertex has magnitude mu_eff=2 lambda f.
Choose M>2m to allow h -> y+y. For nonzero opposite momenta k,-k, the two
daughter modes are distinct oscillators even though they belong to the same
real field. Their resonant finite-mode Hamiltonian and matrix elements are
the ones tested below, with g=mu_eff/sqrt(8 M omega^2 V). The continuum
width instead has the identical-particle factor, Gamma=mu_eff^2 beta/(32 pi M).

Thus an excited radial component can populate initially empty, massive
phase-like modes of the same complex field. The explicit m^2 Y^2 term
breaks the continuous U(1) symmetry, so this is **not** the repo's original
unbroken, number-conserving complex-field action. It proposes a replacement
potential, with a real massive low-energy daughter. The mass splitting,
initial radial energy, choice of one vacuum domain and coupling remain inputs.
Domain formation, radiative corrections and cosmological viability are untested.

There is a useful weak-coupling limit at fixed M: take f large and
lambda=M^2/(2 f^2). Then mu_eff=M^2/f and the quartic terms both decrease.
Conversion also slows. This gives a parametric route to controlling neglected
interactions at fixed finite occupation; it is not an error estimate or a
cosmological rate determination. Near-threshold inverse conversion is still
allowed, and the cold population still needs a survival mechanism.

## Finite quantum conversion with source depletion

In a periodic normalization volume V, retain a zero-momentum source mode b
and a daughter pair a_k, c_-k. The resonant, rotating-wave Hamiltonian is

\[
 H_0=M b^\dagger b+\omega(a^\dagger a+c^\dagger c),\qquad
 H_I=g(ba^\dagger c^\dagger+b^\dagger ac),
 \quad M=2\omega.
\]

For the declared field normalization, g=mu/sqrt(8 M omega^2 V). The model
retains spontaneous and stimulated production and the inverse process.
It neglects other momentum modes, counter-rotating terms and quartic
frequency shifts. Those omissions require weak-coupling and state-dependent
checks before using it as a reduction of the full field theory; no such
global error bound is claimed.

Both Q=N_a-N_c and I=N_b+(N_a+N_c)/2 commute with H. At resonance H_0=MI,
so the free source-plus-daughter energy also commutes with H_I. The total
Hamiltonian is conserved. Opposite daughter momenta conserve momentum.
For the real daughter in the one-complex-field realization, Q is the
opposite-mode occupation imbalance, not a conserved internal U(1) charge.

Starting from |N,0,0>, the exact invariant sector of this *truncated model*
is |N-n,n,n>, n=0,...,N. Its off-diagonal matrix element is

\[
 \langle n+1|H_I|n\rangle=g(n+1)\sqrt{N-n}.
\]

The +1 matters: at n=0 the matrix element is g sqrt(N), so the daughter
vacuum is not stationary while the source is occupied. A classical
zero-daughter field calculation misses this spontaneous quantum process.
For N=1, the exact converted probability is sin^2(gt), reaching one at
t=pi/(2g). No pre-existing daughter seed or undepleted external pump is used.

[check.py](check.py) evolves N=1,8,32,128 with Hermitian diagonalization and
checks selected times independently using a matrix exponential. On the
declared grid s=g sqrt(N)t in [0,10], the sampled maxima are:

| Initial source quanta | Largest sampled converted fraction | s at that sample |
|---:|---:|---:|
| 1 | 0.999964 | 7.86 |
| 8 | 0.811418 | 2.52 |
| 32 | 0.790012 | 3.26 |
| 128 | 0.784597 | 3.96 |

These are transient conversion fractions in a selected mode system, not
cosmological yields. Recurrences are present: for N=128 the fraction at s=10
is only 0.136464. Permanent production needs continuum escape, dephasing,
expansion or another derived mechanism suppressing the reverse transfer.
No physical timescale follows until mu, V and the source state are specified.

## Why a dilute decay equation is insufficient at the inherited light masses

For total number density n in a complex scalar and all momenta within a
ball p <= m u, the number of one-particle states per physical volume is
2(mu/hbar)^3/(6 pi^2) in consistent mass/momentum units; the factor two counts
particle and antiparticle. Equivalently in natural units,

\[
 \bar f=\frac{3\pi^2\rho_c}{m^4u^3}
\]

when rho_c denotes rest-energy density. This is the occupation averaged
over the full permitted momentum ball. A narrow shell increases occupation
in its populated modes; at least one occupied mode must reach the average.
It does not state that every mode has this occupation.

The screen uses the inherited normalization omega_c=0.120 and its a^-3
rest-mass scaling, not a new observational inference. For the illustrative
m=0.62 eV and u=0.001, the full-ball average is enormously above one at
z=1e5 and z=1e6; precise values are in [results.json](run/results.json).
All nine declared combinations of mass and redshift are retained there.

Thus the cosmological version cannot assume dilute daughters merely because
the coupling is small. Bose factors, inverse conversion and backreaction
must be included. The finite quantum calculation includes these within its
three modes; it does not replace the continuum kinetic calculation.

## Relation to existing research

Choi, Gong, Joh, Park and Seto, *Light cold dark matter from non-thermal decay*,
[arXiv:2304.07462v2](https://arxiv.org/html/2304.07462v2), dated 2023-09-06,
studies nonthermal decay production and free streaming, including axion and
Q-ball examples. Sections 2--4 were located; the general production context
and section 2 momentum-redshift relation were checked on 2026-10-11.
That paper supplies adjacent precedent, not verification of this action,
its tuned mass splitting, its finite quantum dynamics or the repo's law.
No novelty claim or borrowed observational exclusion is made. This bounded
search used arXiv and journal primary sources; no local PDF was retained.

## Self-review and remaining theory

Primary audit verdict for the full goal: **incomplete, with the smallest
missing implication being survival and the distribution of the produced
field in the expanding continuum theory.** The stable classical potential,
resonant quantum matrix elements, conserved operators and N=1 conversion
are algebraic results under the stated assumptions. Numerical evidence is
restricted to the finite matrices and nine occupancy benchmarks.

The computation passed 56/56 checks, including an intentionally incorrect
version omitting the spontaneous term, which stays in the daughter vacuum
and is rejected as a production model. The manifest validator confirms
provenance and result hashes; it does not validate physical applicability.
This was self-review, not independent agent review.
The one-field potential expansion also passes 45 exact rational spot checks
in [one_field_run](one_field_run/manifest.json). A preliminary floating-point
check exceeded its 1e-11 threshold by cancellation near a minimum; exact
rational arithmetic resolves the identity without relaxing that threshold.

There are further indispensable gaps:

* The initial source energy is supplied as an initial condition. A source
  population at rest already carries massive gravitating energy. Conversion
  changes its carrier; it does not explain the origin of the total amount.
* The constant rho_Lambda has zero field derivative. It cannot power this
  conversion or select its amount. A dynamical vacuum connection remains absent.
* Neither the mass, splitting nor coupling is fixed by the repo. The near-threshold
  tuning and neglected quartic shifts need explicit control.
* No universal halo profile, roundness, stream selection, fitted kappa or
  relation a0=kappa c sqrt(G rho_DE) follows from this action.

Next executable route: include several opposite-momentum pairs coupled to
the same depleted source and expansion-driven detuning. Test whether
production survives instead of recurring, while accounting for cosmological
pressure work. Then check the approximation regime and continuum limit.
This finite-mode step has now been executed in [EXPANSION.md](EXPANSION.md):
the declared expanding system has a positive bound on the limiting daughter
population. The continuum and cosmological qualifications remain open.
The one-complex-field realization above supplies a concrete action for that
alternative, but its initial radial state and reduction to the finite-mode
Hamiltonian must be checked in the same expanding calculation. Neither
route is closed by this checkpoint.

## Continuation: continuum production and source stability

[LINEAR_BAND.md](LINEAR_BAND.md) derives the exact cold daughter instability
band for the nonexpanding linear field equation. [ENVELOPE.md](ENVELOPE.md)
then treats quantum seeding, stimulated production, source depletion and
expansion in a Gaussian narrow-band approximation. At the chosen benchmark,
three resolved quadratures agree on a transient daughter-pair fraction
0.928523 at x=200; no final relic yield is claimed.

[RADIAL_BAND.md](RADIAL_BAND.md) identifies an additional source instability.
Its exact momentum band is parametrically narrower at small source amplitude,
but its coupled nonlinear effect remains uncomputed. This is a candidate
conversion mechanism with explicit evidence and limitations, not a completed
identification or creation of the repo's cold medium.

[HARTREE_BOUND.md](HARTREE_BOUND.md) bounds the retained daughters' direct
self-interaction detuning at full conversion. It is small at the benchmark,
but the bound is conditional on the Gaussian truncation and does not bound
nonlinear scattering or fragmentation.

A subsequent [inverse-channel check](INVERSE_CHANNEL.md) shows that the
produced spectrum permits regeneration of moving source particles, which
the homogeneous-source truncation excludes. The channel may redistribute
energy while staying cold; its rate and backreaction have not been computed.
The 0.928523 endpoint fraction must therefore remain a truncation result.

[PRESSURE_BOUND.md](PRESSURE_BOUND.md) proves an all-momentum pressure bound
for an on-shell, weighted-number-conserving reaction description. At the
benchmark the combined material has P/rho <= 3.33334e-7 regardless of inverse
redistribution. Coherent stress and violations of the weighted number in the
original action remain unbounded, so this is not yet a full-field theorem.

[CHARGED_ACTION.md](CHARGED_ACTION.md) develops a distinct two-complex-field
action with exact charge, a positive energy-charge functional, and a full
classical time-averaged pressure bound in fixed Minkowski volume. It also
has a cold linear production band. This strengthens coherent survival
control, but changes the action and inherits none of the earlier yield.
Cosmological and quantum production remain open.

[CHARGED_EXPANSION.md](CHARGED_EXPANSION.md) extends the alternative action's
energy-charge control to smooth classical FLRW solutions with monotone
nonnegative H<m/3. The benchmark surplus remains below 1.087e-5 through
a millionfold expansion. This is an analytic survival bound, not a quantum
production or relic-abundance calculation.

[CHARGED_PRODUCTION.md](CHARGED_PRODUCTION.md) computes a new Gaussian
quantum-seeded production history for the protected action, including its
required quartic normal and anomalous terms. Resolved grids and tighter
integration support a transient daughter charge fraction about 0.94881
at x=200. This does not close the gap between approximate quantum production
and the exact classical survival bounds.

[CARRIER_MATCHING.md](CARRIER_MATCHING.md) finds exact tree-level threshold
cancellation in the minimal protected action and an exact pressureless
classical rotating family. The minimal action therefore does not supply
the repo carrier's positive contact coupling. Adding a separate positive
quartic preserves classical energy protection but introduces new input and
requires a new production/transport calculation.

[REPULSIVE_EXTENSION.md](REPULSIVE_EXTENSION.md) executes one positive-contact
extension. It retains about 91.8% transient daughter conversion in the
Gaussian calculation, but its threshold repulsion is extremely weak and
its constant-contact description fails near the production resonance.
Carrier transport and halo selection remain unproved.

A subsequent [3D spatial pilot](SPATIAL_CONVERSION.md), using an explicitly
classical seed, populates moving sources and shows order-one changes in
transient conversion relative to its matched uniform-source control. It
does not replace the quantum initial state, but confirms that homogeneous
source yields cannot be promoted to full nonlinear predictions.

[QUANTUM_HANDOFF.md](QUANTUM_HANDOFF.md) replaces the arbitrary spatial seed
with finite-box Gaussian vacuum growth and correlated daughter sampling.
Two early handoffs give closely agreeing spatial endpoints in one draw,
but source-charge adjustment is a declared approximation and the coarse
box has only 12 effectively occupied pairs. Ensemble, box, expansion and
quantum-correction checks remain necessary.

[ENSEMBLE_AND_BOX.md](ENSEMBLE_AND_BOX.md) tests five matched spatial
realizations: endpoint daughter fractions span 0.5966–0.6827, with substantial
moving sources in every draw. Larger-box Gaussian handoffs reduce early
relative sampling noise, but their nonlinear spatial evolution has not yet
been tested. No precise or continuum yield is established.

[LARGER_BOX.md](LARGER_BOX.md) extends the matched nonlinear evolution to
a twice-wide box with the same Fourier cutoff. One draw ends with 0.6927
daughter and 0.2711 moving-source charge; substantial conversion persists,
but no precise box-independent yield is established.
[SPATIAL_ENERGY_BOUND.md](SPATIAL_ENERGY_BOUND.md) separately bounds the
kinetic budget by a positive square identity within this envelope.

[EXPANDING_SPATIAL.md](EXPANDING_SPATIAL.md) carries the imposed radiation
background through both Gaussian vacuum growth and correlated spatial
evolution. One small-box draw ends with 0.5919 daughter and 0.2604 moving-source
charge; a halved time step confirms expansion-work accounting. This remains
an approximate, single-realization formation history with a supplied source.

[SOURCE_PREPARATION.md](SOURCE_PREPARATION.md) supplies an exact, externally
controlled quadratic pulse that turns an uncharged displaced source into
circular charged motion. Its switch energy and integrated charge torque pass
124 checks. The initial displacement, phase selection and autonomous clock
remain inputs; this is a preparation construction, not a vacuum-origin or
abundance solution. It quantifies the precision needed to retain the small
excess-energy budget.

[AUTONOMOUS_CLOCK.md](AUTONOMOUS_CLOCK.md) replaces the prescribed source-
preparation switches with an additional dynamical real scalar and a compact
positive interaction. Coupled evolution includes backreaction and conserves
total energy; three tuned finite cases prepare nearly circular source motion,
with 27 checks passing. Clock energy, initial displacement/phase, and the
interaction profile are additional inputs. An autonomous cosmological origin
and the repo's full medium are still not established.

[CLOCK_FLUCTUATIONS.md](CLOCK_FLUCTUATIONS.md) tests linear spatial modes of
the tuned J=10 autonomous preparation. It finds finite amplification and
nonzero source/clock vacuum excitations outside the cold daughter band;
113 numerical checks pass. A momentum-integrated energy and UV-tail check
is required before the uniform pulse can be treated as sufficiently cold.
This is not a nonlinear stability or cosmological abundance result.

[CLOCK_ENERGY.md](CLOCK_ENERGY.md) integrates a phase-independent envelope
for the preparation's linear vacuum excitation energy over
0.001<=p/M<=10000. At the inherited illustrative mass and density, the
finite-band envelope estimate is 1.434e-47 of source energy, negligible
against the initial coldness budget. All 23 checks pass. Uncomputed infrared
and ultraviolet tails, primordial classical fluctuations and the broader
formation/halo requirements remain open.

[CLOCK_TAIL_BOUNDS.md](CLOCK_TAIL_BOUNDS.md) derives conditional analytical
IR/UV bounds instead of extrapolating the sampled spectrum. Under duration
and edge-crossing assumptions supported by the numerical clock trajectory,
the combined tail energy is below 2.797e-33 of the stipulated source density.
This supports negligible linear vacuum heating; premises are not interval
certified and no primordial or nonlinear fluctuation bound is supplied.

[CLOCK_LOADING.md](CLOCK_LOADING.md) extends the autonomous clock with a
symmetric moving minimum. Three finite homogeneous histories begin with
zero source field and velocity, transfer about one-sixth of clock energy
into the source, and prepare nearly circular motion; 42 checks pass.
This removes supplied nonzero source initial data but chooses the displacement
scale/direction and coupling profiles. The new loading/release stages need
their own fluctuation audit; previous isolated-pulse bounds do not certify
the full history. Abundance and the repo's halo/vacuum relation remain open.

[LOADING_FLUCTUATIONS.md](LOADING_FLUCTUATIONS.md) audits seven linear modes
through the entire R=100 loading history and checks clock-speed sensitivity
against nonlinear homogeneous runs. A corrected local-time calculation passes
115 checks; the original failed run is retained. The estimated single-parameter
clock-speed tolerance for initial eta<1e-5 is about 0.054%, and unequal source
components are not damped during loading. This is a tuned preparation route,
not a demonstrated generic attractor or full energy-spectrum bound.

[RESONANT_KINETICS.md](RESONANT_KINETICS.md) derives the Bose gain/loss operator
for the retained source channel and evaluates one source mode in a fixed
Gaussian daughter bath. One stipulated halo-like example gives a 0.856 Gyr
mode relaxation time despite an enormous vacuum lifetime; 95 checks pass.
This motivates coupled momentum transport but is explicitly not a halo
heat-flow, settling or profile-selection time. The bath and incoherent kinetic
closure are assumptions, not outputs of the formation calculation.

[COUPLED_KINETICS.md](COUPLED_KINETICS.md) replaces the fixed bath with a
conservative isotropic two-species collision calculation. In one stipulated
halo-like Gaussian bath, roughly 41% of charge is in sources after 5.57 Gyr;
daughter kinetic energy decreases while total charge/energy stay conserved.
Four grids pass 28 checks, with a remaining 0.004 endpoint refinement shift.
This is population/energy redistribution, not spatial heat flow, halo settling
or the missing acceleration/vacuum selector.

[KINETIC_HEAT_CURRENT.md](KINETIC_HEAT_CURRENT.md) adds linear angular
dipoles to the evolving collision calculation. A current with zero leading
bulk momentum falls to about 57% after 5.57 Gyr, while charge, energy and
momentum remain conserved; 28 checks pass. This supplies a collision response
of the energy current, not a conductivity or spatial halo heat-flow law.
The earlier single-mode rate cannot be used as a heat-relaxation time.

[KINETIC_STREAMING.md](KINETIC_STREAMING.md) adds Fourier streaming and higher
angular moments to the evolving collision model. Over 23.3 Myr, collisions
change the tested 10-kpc energy contrast by at most 0.59% of its initial
amplitude; a 1-Mpc control shows a larger effect over a longer interval.
All 23 checks pass, including a collisionless Bessel benchmark. This favors
an orbital transport treatment for the example rather than an assumed local
diffusion law. Gravity, boundaries and energy-grid convergence remain absent.

[JEANS_BASELINE.md](JEANS_BASELINE.md) adds a collisionless self-gravity
baseline for the stipulated homogeneous bath. It gives a 44.47-kpc Jeans
wavelength and a 46.39-Myr growth time at 100 kpc, much shorter than the
previous single source-mode relaxation time. Independent dispersion and
Volterra calculations pass 12 checks. This is a mean-subtracted homogeneous
problem, not a finite halo; it rules out treating the long-wavelength
no-gravity control as an established stable halo at that density.

[BOUND_HALO_REACTIONS.md](BOUND_HALO_REACTIONS.md) evaluates initial reactions
in a finite Plummer equilibrium. Newly formed sources are provably more
bound than the parents' average at NR order, with reaction support restricted
by escape speed. About 90.6% of initial births occur inside the chosen
30-kpc scale radius; 351 checks pass. The profile is a test input, rates are
initial derivatives, and the escape calculation is geometry only—not actual
evaporation or an evolved halo result.

[SOURCE_ORBITS.md](SOURCE_ORBITS.md) follows the initial source-birth
population through fixed-potential orbital residence averages. About 92.5%
of residence lies inside the chosen 30-kpc scale radius, versus 90.6% of
births; the RMS radius falls 4.9% and velocity dispersion rises. All 28 checks
pass, including orbital virial identities. This is conservative tracer
redistribution, not a final equilibrium, irreversible cooling or a
self-consistent halo evolution.

[ORBITAL_REACTION_MEMORY.md](ORBITAL_REACTION_MEMORY.md) integrates the
stimulated net gain–loss coefficient along the bound source orbits. In the
fixed daughter bath, mean occupation memory is 0.877 after one radial period
and 0.678 after three; 16 checks pass. This supports—but does not rigorously
certify—an orbit-averaged treatment and rules out treating the collisionless
source residence profile as permanent. Occupation memory is not particle
survival, and bath/potential backreaction remains absent.

[INITIAL_HALO_RESPONSE.md](INITIAL_HALO_RESPONSE.md) derives the first
self-consistent Boltzmann-Poisson response of the combined source/daughter
matter. Reaction kinetic-pressure loss gives inward mass current at order
t^2 and a deepening potential/enclosed-mass increase at order t^3 for the
chosen initial Plummer state. All 38 checks pass. These are initial Taylor
derivatives, not a finite-time evolution, permanent core or halo-law proof.

[VIRIAL_CAPACITY.md](VIRIAL_CAPACITY.md) derives a finite reaction-energy
reservoir and necessary stationary endpoint constraints. In the isolated
fixed-mass NR test halo, r_g,f/r_g,0=1/(1+1.271478483 F_f), hence any such
endpoint has ratio at least 0.44024; contraction raises kinetic energy.
All 39 checks pass. The result selects neither F_f nor an equilibrium,
is not an all-time bound, and does not bound central core radius or prevent
collapse. Finite-time coupled transport/gravity remains unresolved.

[UNBOUND_DAUGHTERS.md](UNBOUND_DAUGHTERS.md) computes the initial Bose-stimulated
production of positive-orbital-energy daughters by newborn source decay.
Their charge fraction begins as 1.010074742e-4 [t/Gyr]^2, with no finite-time
extrapolation established. Three quadrature resolutions agree; angular
antiderivative and normalization checks pass. This is an unbound population,
not permanent escape or outward flux. It shows why the next coupled halo
model must retain an escape channel and why the no-escape virial endpoint
cannot be assumed. An ordinary global finite-temperature Bose equilibrium
also has infinite mass without confinement or a cutoff.

[VACUUM_SELECTOR_AUDIT.md](VACUUM_SELECTOR_AUDIT.md) checks the original
vacuum-dependent halo-law requirement. Direct Lambda gravity is outward
and only 1.49e-5 of the target acceleration at the 200-km/s comparison's
transition radius. A fixed fraction of turnaround has V^4 proportional to
M^(4/3), not M. An optional Ricci mass portal needs a large coefficient and
also senses matter curvature; it is not an implemented or validated action.
All 13 arithmetic/identity checks pass. These are scoped obstructions,
not a no-go theorem for cosmological selection or other vacuum couplings.

[CURVATURE_DISCRIMINATOR.md](CURVATURE_DISCRIMINATOR.md) derives a Ricci
invariant that cancels dust curvature exactly but retains kinetic pressure
and anisotropic stress. Its central vacuum-curvature bias is 7.42% in the
current illustrative halo. Exact identities also expose the vacuum/matter
split ambiguity without an equation of state, and the proposed square-root
invariant is nondifferentiable at a pure-vacuum background. All 41 checks
pass. This improves the selector audit but supplies no validated new action
or derivation of the halo law.

[FOUR_FORM_PORTAL.md](FOUR_FORM_PORTAL.md) constructs an optional fixed-flux
four-form coupling with positive kinetic coefficient. Correct fixed-flux
reduction shifts the aligned carrier/source masses while retaining the
positive-square potential, charge symmetry and threshold mass-squared gap.
All 40 checks pass. This supplies a classical vacuum-dependent coupling,
but at fixed flux it is exactly a mass reparametrization of the old local
scalar theory. It does not generate a halo selector, initial charge, flux
value or the requested acceleration law; quantum stability is unproved.

[NONLINEAR_PORTAL.md](NONLINEAR_PORTAL.md) tests vacuum-mediated pressure
against the source/halo density hierarchy. A quadratic interaction strong
enough for the illustrative halo makes the original-amplitude source
radiation-like. A positive convex interaction that becomes linear at high
density instead gives the chosen halo pressure while retaining source
eta=1.76e-6 and the initial pair-instability band. All 33 checks pass.
The crossover and support scale are chosen; nonlinear production, stability
and halo evolution remain untested for this new action. A universal
barotropic pressure alone also cannot support different flat speeds over
an overlapping density range under the stated equilibrium assumptions.

[PORTAL_HYDROSTATIC.md](PORTAL_HYDROSTATIC.md) solves finite self-gravitating
spheres for the nonlinear portal's coherent pressure-only EOS. With common
chosen parameters, sampled radii are about 33–37 kpc. Virial balance,
homologous energy curvature, the low-density analytic limit and ODE
refinement pass 32 checks. The homology curvature is positive, which is
not a stability proof; the mass-family turnover motivates a full radial
mode calculation. No baryons, kinetic stress, reactions or formation are
included. A first-run JSON serialization failure is preserved; v2 fixes
only that output conversion.

[PORTAL_RADIAL_MODES.md](PORTAL_RADIAL_MODES.md) extends the pressure-only
stability test beyond uniform rescaling. An exact positive quadratic-form
identity gives sufficient linear radial stability for central density
rho_c/rho_0<=0.859678. Radial trial functions give negative-energy witnesses
at sampled ratios 2, 3, 10 and 30 despite their positive homology curvature.
All 39 consistency checks pass. The values are numerical variational upper
bounds, not a full spectrum; full-field stability and branch selection
remain unproved.

[PORTAL_PRODUCTION.md](PORTAL_PRODUCTION.md) includes the softened portal
in a dense spatial classical conversion pilot. Its common mass shift is
absorbed in the frequencies and its residual force retained. The fine run
has about 63.6% daughter charge at x=30, with moving sources; all eight
checks pass. The minimum sampled density remains over 6e8 times the portal
crossover, explaining the roundoff-level difference from a matched
linear-mass control. This is not quantum production, a permanent yield,
or an evolution through the later pressure-support regime.

[PORTAL_COSMOLOGY.md](PORTAL_COSMOLOGY.md) follows the same coherent pressure
law through a declared cosmological dilution history. The mean-density
crossover occurs near z=75 and sound speed peaks at 209 km/s near z=67.
A one-fluid linear screen gives strong growth suppression at several
Mpc and sub-Mpc wavelengths; eight checks pass. This is not a full
Boltzmann transfer function or observational exclusion. It identifies an
intermediate-density problem that dense production and static halos alone
do not address, and motivates deriving the produced multimode field's
actual coarse-grained stress response.

[PORTAL_AVERAGED_STRESS.md](PORTAL_AVERAGED_STRESS.md) reproduces the fine
production endpoint and averages the nonlinear pressure over its saved
13,824 local intensities. Frozen-shape averaging lowers the response peak
to 185 km/s but increases its wings; the conditional growth suppression
persists. Three production-reproduction checks and 15 response checks pass.
This is a fixed-distribution partial derivative, not a dynamical sound-speed
closure: evolving correlations, reactions and kinetic stress remain missing.

[PORTAL_ENERGY_PRESSURE.md](PORTAL_ENERGY_PRESSURE.md) proves a distribution-
independent bound on mean portal pressure at fixed mean intensity and a
limited excess-energy budget. It uses the convex identity p=f(x-u), so
arbitrary clumping cannot erase this pressure contribution without sufficient
energy. Nineteen checks pass. The example budgets are declared, not evolved
cosmological bounds; the result is neither a bound on total instantaneous
stress nor a dynamical sound-speed closure.

[PORTAL_VLASOV.md](PORTAL_VLASOV.md) replaces the fluid evolution by a
velocity-resolved collisionless hierarchy while retaining the stipulated
mean-field coefficient. It reproduces the growth suppression closely at
the small redshifted velocity dispersion; 16 checks pass, including an
independent Gaussian phase-mixing control. Thus rapid thermal equilibrium
is not required for that result. The nonlinear mean-field closure and
actual reactive two-species state remain unproved.

[PORTAL_COHERENT_MODES.md](PORTAL_COHERENT_MODES.md) derives a phase-locked
stationary branch and its long-wavelength phase speed directly from the
full two-field action, retaining the induced source. The crossover speed
is 199.999777 km/s, close to the former 200-km/s NR pressure estimate.
Thirty checks pass. This establishes the coherent response without an
assumed fluid closure, but the branch's tiny source fraction differs from
the produced multimode mixture; its realization and relaxation remain open.

[PORTAL_MIXTURE_IDENTITY.md](PORTAL_MIXTURE_IDENTITY.md) derives the local
portal force for arbitrary classical fields at leading NR order. Conversion
preserves the same local charge density and commutes with the local portal
phase flow; changing mixture alone does not remove the density force.
All 35 checks pass. Spatial transport and averaged stress remain dynamical.

[PORTAL_RETUNING.md](PORTAL_RETUNING.md) optimizes the crossover while keeping
the same illustrative halo support. An analytic matter-era minimum occurs
at rho_h/rho_cross=sqrt(2/7); the declared finite-history minimum sound
distance is 1.111 Mpc, only 11.45% below the original. Eleven checks pass.
This is a bound/optimization within the stated EOS family, not an
observational exclusion or a universal no-go result.

[CARRIER_MASS_FAMILY.md](CARRIER_MASS_FAMILY.md) returns to the original
kinetic-support carrier and rescales mass at fixed source energy, u,
epsilon and coupling ratio. Threshold sigma/m grows as m^5 while contact
pressure stays fixed; initial resonant halo conversion grows as m. An
illustrative 1-cm^2/g threshold target occurs near 31 eV but gives an initial
Plummer reciprocal conversion rate of about 1.6 hours. All 43 checks pass.
These are distinct rate diagnostics, not settling times or an observational
exclusion; the threshold cross section alone is misleading near resonance.

[DETUNED_CARRIER.md](DETUNED_CARRIER.md) moves the original carrier resonance
above the chosen halo escape speed (u=0.01, m=193.525 eV) while matching an
illustrative threshold cross section of 1 cm^2/g. Six parameter checks pass.
The preliminary Gaussian production run fails late numerical checks and is
preserved. An equivalent Bogoliubov formulation with finer momentum grids
passes 27 checks and reaches a transient charge conversion fraction
0.999999819 at x=200 (6.80 ns). This is homogeneous Gaussian production,
not spatial survival, relic abundance, or a derived vacuum/halo law.

[DETUNED_MOVING_RESPONSE.md](DETUNED_MOVING_RESPONSE.md) identifies a
continuum moving-source response omitted by homogeneous production. A fixed
Gaussian daughter-shell calculation gives a secular Born response; it is
not the actual production history and breaks down at appreciable conversion.
Six checks pass. At x=200 its coherent low-momentum region requires roughly
895 grid points per axis to coexist with a daughter cutoff of q=2, so the
earlier small spatial boxes cannot test detuned survival.

[DETUNED_RADIAL_RESPONSE.md](DETUNED_RADIAL_RESPONSE.md) integrates the
continuum moving-source response over the saved produced radial spectrum.
Finite width changes the frozen free-field response by less than one percent
at elapsed response time 200; 21 finite checks pass. This supports retaining
moving sources, not a nonlinear decay fraction. The distinction between
daughter survival and the classical combined-system coldness bound remains
explicit, including the missing quantum-to-classical justification.

[NR_QUANTUM_BOUND.md](NR_QUANTUM_BOUND.md) proves a positive operator
decomposition for the specified regulated leading NR two-field Hamiltonian.
It protects the combined kinetic-energy budget under full quantum unitary
evolution without assuming a classical handoff or a pure daughter state.
A two-cell many-body audit passes 26 checks. This is not a full stress bound,
a continuum renormalization result, or a halo-law derivation.

[NR_QUANTUM_PRESSURE.md](NR_QUANTUM_PRESSURE.md) extends the regulated
quantum model to integrated pressure and homogeneous expansion work.
Positive operator forms bound stress without a Gaussian/classical state
assumption. At the detuned parameters the conservative |P|/rho bound stays
below 0.000373 through a millionfold expansion. All 80 matrix/derivative
checks pass. This is not a sound-speed, continuum-QFT or halo-law result.

[COLLISION_AGE_SELECTOR.md](COLLISION_AGE_SELECTOR.md) tests a one-collision
per cosmic-age radius as a possible halo selector. In the declared
isothermal family the detuned tree cross section implies acceleration
growth at least as sqrt(V), with a measured factor 3.91 across 20–300 km/s.
The age-only vacuum scaling is rho_Lambda^(1/4), not the target square root.
Fourteen consistency checks pass; this rejects this conditional selector,
not all formation mechanisms or the protected carrier itself.

[PHONON_SELECTOR_GATE.md](PHONON_SELECTOR_GATE.md) derives the original
carrier coherent phase branch and compares it with a primary-source
superfluid force proposal. The dilute phase action is quadratic, the
illustrative detuned halo fails the ideal-gas condensation screen, and a
linear baryon-phase source breaks the conserved charge used for protection.
Seven arithmetic/Legendre checks pass. This gates direct reuse of the
existing carrier as that mediator; it is not a general superfluid no-go.

[POLARIZATION_SELECTOR.md](POLARIZATION_SELECTOR.md) audits a primary-source
dipolar-medium alternative and its constitutive requirements. Square-root
forces require a critical quadratic response and a cubic norm term; the
vacuum offset remains independent of the force coefficient. Twenty-five
checks pass. Ordinary positive-mass bound pairs have no gravitational
dipole about their center of mass, so this effective medium has not been
constructed from the protected scalar carrier.

[CLAUDE_RECEIVER_BRIDGE.md](CLAUDE_RECEIVER_BRIDGE.md) reviews current
CFG626 and neighboring signed-energy/receiver work following the user’s
request to inspect Claude. The repaired kernel removes the old hollow
obstruction. A new six-cell comparison shows our large source gap has
conditional capacity but excessive free-decay kicks for the galaxy target
orbits, and no justified halo source population. Six arithmetic checks pass.
This connects production research to the current benchmark without claiming
a settled halo or a completed energy receiver.

[POSITIVE_POLARIZATION.md](POSITIVE_POLARIZATION.md) preserves a separate
phenomenological scalar/polarization extension with positive source-free
energy and a regulated low-frequency mode. Eighty-four finite checks pass.
Its force coefficient, critical tuning, cubic norm, microscopic link and
vacuum relation are inputs or open; it is not a replacement completed model.
