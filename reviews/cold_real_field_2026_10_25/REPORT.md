# Direct real-scalar evolution: localization survives, cluster supply does not follow

Date: 2026-10-25. Continuation of `cold_dense_relativistic_2026_10_25` at
082a94d0ab. All numerical claims below concern the specified spherical initial
states and fixed matter backgrounds. No new action coefficient was fitted.

## Finding

The fluid obstruction does **not** eliminate all localized real-field motion.
Direct evolution of the canonical scalar with its full potential leaves a
finite-time oscillating vacuum core. Its retained energy survives temporal,
spatial and outer-boundary checks. Prepared incoming shells also leave remnants
in the unrefined formation tests. This is evidence for nonlinear localization,
not for a stable relativistically self-gravitating object.

The tested remnants do not supply a parameter-free cluster component. Their
mass is about 10^-12 solar masses and their radii are of order 0.04–0.08 pc.
Even an optimistic snapshot packing estimate requires overlapping cores for
all 303 positive cluster source benchmarks. The tested restored matter case
loses almost all its central energy. Neither cosmological abundance nor a
radial cluster profile is selected by these calculations.

## Equation and controlled approximation

Let x=sec(q/2), d=rho_m/D, with the canonical variables inherited from the
preceding audits. Evolve

    q_tt = (r^-2 (r^2 q_r)_r) - (40x^3 - 48x + d) x tan(q/2)/2.

For d=0, q_v=2 asin(sqrt(1/6)) and the excitation potential is

    U_0(q) = 10 [sec^2(q/2)-6/5]^2.

For the restored comparison d=60, q_v=0. With z=sec(q/2)-1,

    U_d(q) = (d-8)z + 36z^2 + 40z^3 + 10z^4.

This is the full nonlinear real-scalar PDE, without a fluid EOS, cycle average
or complex-field number conservation. It is **not** the full Einstein–scalar–
baryon system: d is fixed, the metric is flat, evolution is spherical, and no
baryon feedback or galaxy-force calculation is performed.

The inherited units are L=0.0109620 pc, T=0.0357534 yr and
D_mass L^3=8.45840e-14 solar masses. Thus t=1000 is only 35.75 years.
The weak-gravity coefficient is kappa=8pi G D_mass L^2/c^2=9.28046e-24.
The excitation compactness estimate is kappa times the maximum enclosed
integral of excitation energy divided by radius (without the 4pi factor).
Initial tests give maxima of order 10^-23–10^-22. Background contributions
scale as kappa W_bg r^2/3, also tiny on the simulated domains. This justifies
neglecting gravitational corrections on these scales and durations; it is
not a solved metric constraint or a study of the strong-gravity branch.
The parameter normalization itself remains inherited, not microscopically
selected by this test.

## Numerical method and checks

Cell-centred spherical finite volumes use the exact shell volume divided by
4pi. Face gradients define both the radial Laplacian and the discrete gradient
energy. Velocity Verlet is combined with split momentum damping in only the
outermost 15 length units. The core r<10 is undamped. The outer value is fixed
to q_v, with its half-cell boundary gradient included in energy. Each damping
step debits its exact kinetic-energy loss into the absorbed-energy ledger.
A branch guard rejects |q| >= pi-0.01.

The initial five tests ran to t=200 at radius60, dx=.05, dt=.005. The adaptive
follow-up ran to t=1000, sampling every .1 unit, and compared final-quarter
mean core energy. The original inputs and follow-up plan are preserved in
FROZEN_CRITERIA.md and FOLLOWUP.md; the packing calculation was post-hoc.

| Initial state | Initial energy | Late mean core energy | Retained fraction |
|---|---:|---:|---:|
| Vacuum Gaussian A=.5, width3 | 26.25675 | 19.04912 | .725494 |
| Same, dt=.0025 | 26.25675 | 19.04912 | .725494 |
| Same, dx=.025, dt=.0025 | 26.25549 | 19.05323 | .725685 |
| Same, outer radius80 | 26.25675 | 18.92351 | .720710 |
| Vacuum Gaussian A=1.2, width3 | 87.20913 | 26.29372 | .301502 |
| Restored d=60, A=.8, width3 | 237.12986 | 1.31918 | .005563 |
| Incoming vacuum shell A=.1 | 235.80470 | 21.61926 | .091683 |
| Incoming vacuum shell A=.2 | 825.38246 | 25.23689 | .030576 |

The baseline joint refinement changes retained energy by .0216%; moving the
boundary changes it by .659%. Both pass the predeclared 5% retention criterion.
This is convergence of that observable, not of all phase-sensitive waveforms.
The maximum follow-up ledger error is 1.27e-4, below the .005 gate. The baseline
ledger error falls from 5.32e-5 to 1.33e-5 on halving dt, as expected for this
second-order integrator. Formation shells and the restored comparison do not
have independent resolution studies here, so their interpretation is provisional.

The incoming shell has support 12<r<18, delta=-A exp[1-1/(1-u^2)],
u=(r-15)/3, q=q_v+delta, p=delta'+delta/r. The momentum is an exact inward
condition for a massless linear radial wave; here it is a specified preparation,
not an exact one-way nonlinear solution. All its energy is supplied initially.
An empty exact vacuum stays empty under these deterministic equations.

The damping-ledger sign mutation fails (relative ledger error .123966); its run is retained
separately. This tests the energy diagnostic, not every possible discretization
error. Manifests preserve successful and failed execution artifacts.

## What the remnants imply for abundance

`packing.py` independently reconstructs the final discrete energy from q,p
snapshots and checks total and core energy against the integrator to 1e-9
relative accuracy. R90 encloses 90% of final r<10 energy. For an intentionally
optimistic packing estimate, assign **all** core mass to the R90 sphere:

    rho_pack / D = E_core / [(4pi/3) R90^3].

At t=1000, the baseline has M_core=1.626e-12 solar masses, R90=.03837 pc,
and rho_pack/D=.1070. Time, joint-grid and boundary comparisons give
rho_pack/D=.1070, .1094 and .1243. These are snapshot radii, not averaged
radii or proven lower bounds over all possible field states.

The inherited 303 positive shell requirements span rho_required/D=1.032–17469.
For the baseline, the required volume filling factor is 9.65–163206. Even the
most optimistic of the four baseline variants requires 8.31–140545. Therefore
none of these snapshot populations can be treated as dilute, independent,
non-overlapping copies while meeting the benchmark density. Overlapping real
scalar fields interact nonlinearly: summing clump masses is then not a solution.
This does not exclude a qualitatively different dense collective phase.

The baseline would require approximately 4.23e25–2.44e26 objects to match the
70 inherited R500 mass benchmarks. Those numbers are demands, not predicted
abundances; some inherited mass profiles contain negative shells and are not
fully physical population targets. The shell source requirements themselves
are benchmark inversions, not a new covariance-aware observational analysis.
Identifying scalar excitation mass with the required gravitating source is
also conditional on the framework's unresolved stress/metric matching.

Vacuum localization cannot simply be transported into cluster matter unchanged:
the matter term changes the potential and its minima. The d=60 test retains
only .56% centrally at late times. It is not a simulation of an established
vacuum core crossing an interface, nor a proof that all restored-background
states disperse. Earlier exact-breather exclusions for uniform d>=8 do not
apply to the vacuum double-well potential studied here.

## Galaxy law and remaining freedom

No population is selected by this PDE experiment. Initial amplitudes, widths,
number of packets and preparation times remain initial data. Choosing them to
fit clusters would add the freedom the user asked to remove. Vacuum localization
also offers no demonstrated cluster-only production trigger.

Under the earlier spherical phenomenological force mapping, the extra cold
mass must satisfy M_c(<r) <= delta L(r), where

    B=M_b(<r), A=a0 r^2/G, L=(B+sqrt(B^2+4AB))/2.

The tolerance delta must come from galaxy data. This work neither sets it nor
demonstrates the required galaxy suppression. It derives no new MOND law and
fixes no previously free vacuum/response ratio.

The next genuinely distinct target is a *dense, matter-coupled collective
phase*, with local energy production and nonradial stability checked together.
Repeating isolated vacuum cores at an arbitrary number density cannot solve
the present supply problem. A cosmological initial-state/production prescription
and coupled matter dynamics remain necessary before abundance is a prediction.

## Literature context and provenance

The term “oscillon-like” is descriptive. Real scalar oscillons can lose energy
through radiation; finite retention is not infinite stability. This general
context is supported by the primary paper [Classical Decay Rates of Oscillons](https://arxiv.org/abs/2004.01202),
whose abstract was checked on 2026-10-25. Its potentials and lifetime results
are not transferred to this framework. Our finite-time retention comes from
this directory's runs, not from that paper.

Reproduce the bounded runs with the commands recorded in each run manifest.
Run `python reviews/cold_real_field_2026_10_25/packing.py` for the snapshot
comparison. `packing_provenance.json` records hashes of its script, all read
snapshots, summaries and upstream benchmark inputs, and its output.
