# Two-state dark medium: bounded prototype

Checkpoint TS-2026-10-24-A. Base Git revision:
36c2d800d1a2e10a732367626067c2ca23188d7a (tracked tree clean at inspection).
User target: explain extra bound mass in dwarfs and clusters while retaining
the galaxy acceleration relation. This is an executable research prototype,
not a fitted theory, a manuscript update, or a claim of a new particle.

## Chosen construction

Equal positive rest mass in states T (tethered) and F (free). Both source the
same Newtonian potential. Only T contributes to the polarization. The model
is spherical, isolated, nonrelativistic, and unscreened. It is deliberately
limited to radii well above the stiffness scale; it cannot test small dwarfs,
the Solar System, satellite tides, cosmology or lensing. No empirical data
fit or transfer of old observational passes is authorized by a toy success.

Use the paper's full tether energy with the ordinary gravitational energy
included once. A state change preserves position, velocity and rest mass;
the energy difference must be exchanged with a receiver. Include a constant
specific binding offset epsilon for T. Test the simplest universal offset
before invoking an environment-dependent interaction.

## Alternatives and why this test

1. Fixed T/F mixture: already obstructed in CFG941 R2 because F gravitates and
   enters the tether source. Keep this as a control, not a new solution.
2. Two states with conversion and an explicit energy receiver: chosen by the
   user; this adds an actual missing degree of freedom and tests retention.
3. Retarded response without a persistent internal state: deferred because
   a delay alone does not guarantee a durable free population.

## Three checks, with criteria recorded before execution

TS1: Derive and evaluate the coexistence equilibrium and free-mass budget.
Use a conservative *illustrative* disk tolerance of 0.05 dex in acceleration,
and also report 0.10 dex; these are not observational confidence intervals.
Show the excess mass needed for factors 1.8 and 3 in acceleration. Never
equate these directly with published velocity or lensing mass residuals.

TS2: Construct a finite T halo from the simple law and convert all of it to F.
Track the full tether energy exported and evolve the resulting live, positive
mass free shells after retaining 10% of the initial baryonic mass. Require
relative energy error <0.005 in each numerical run and the retained fractions
at two resolutions to differ by <0.05. A negative snapshot orbital energy is
only a finite-time binding diagnostic, not an asymptotic stability theorem.
All-at-once conversion is an imposed experiment, not a derived transition.

TS3: Test whether one constant binding energy epsilon can favor conversion
at a representative dwarf radius while forbidding it at both representative
disk radii. An overlap is only feasibility; no overlap refutes only that
specific selector on those toy profiles. The profile chemical potential is
evaluated before conversion, not presented as a final phase equilibrium.

## Inputs and non-claims

Use a0=9.3603e-11 m/s^2, G=4.30091e-6 kpc (km/s)^2/Msun,
and a nominal finite reservoir of 5.364 times the initial baryon mass.
These are inherited/fitted inputs, not derived here. Four idealized Plummer
profiles (not data): dwarf (3e5 Msun, 0.3 kpc), dwarf disk (1e8, 1 kpc),
large disk (6e10, 3 kpc), cluster (1e14, 300 kpc). Test radii b, 2b, 2b,
and 500 kpc respectively. Full radial functions enter the calculation.

No invented galaxy-type label is allowed inside the energy or force laws.
If the selector fails, preserve the retention result but do not call the
joint scientific target achieved. The missing transition coupling is a
separate research obligation.

Nearest prior records: CFG939 (crossing does not untether), CFG941 (free
gravity changes the source), core_open_problems_2026_10_20 (physical origins
remain open). Those reports were read, not independently reproduced here.
