# Causal collective candidate: self-review

Verdict: **causal local field/response construction and finite numerical checks
passed; microscopic origin, gravitational assembly and population separation
remain incomplete.** Review is by the implementing agent, not independent.

## Claim and dependency map

Chosen singlet/vector neutral levels -> positive Maxwell/material Hamiltonian
-> local Maxwell-Bloch evolution -> Maxwell principal characteristic speeds.
Positive oscillator strength -> Hermitian linear mode problem -> real frequencies
and group speeds bounded by c. Chosen critical spectrum -> static dielectric law
-> conditional gravity matching -> one-parameter static calibration.

Canonical constituent sum rule + available mass -> response-frequency bound.
Same constituent dipole inventory -> required mass-times-size bound. These last
two conclusions are conditional on the stated constituent/mass description, not
theorems about arbitrary emergent media. The spectral exponent condition is
derived; the existence of the corresponding material is assumed, not proved.

## What the tests do and do not establish

- 405 static (chi, gap floor) combinations times 121 accelerations: deterministic
  finite calibration against the previously adopted function, no observational
  data. The reported best value is restricted to the gapless critical branch.
- 62 finite linear mode problems use 16/32 gap nodes and 31 wave numbers. A
  separate single-resonance polariton expression checks normalization. The causal
  proof comes from local principal characteristics and the Hermitian derivative
  bound, rather than extrapolating sampled velocities.
- Six homogeneous nonlinear integrations retain internal amplitudes and separate
  relativistic positive/negative carrier momenta. They conserve field+excitation+
  kinetic energy to the reported tolerance. Free number densities are fixed and
  homogeneous; net charge is zero by inventory. This does not test charge
  transport on an inhomogeneous particle mesh or an ionization reaction.
- Eight periodic 3D electrostatic solves test the NEW passive constitutive law.
  Grid/source operators alone are imported from the predecessor. Its old
  nonlinear displacement law is not called. Uniform compensating background
  appears only in the like-charge manufactured fixture. Opposite charges are
  explicit in the neutral-pair fixture. Neither fixture predicts their assembly.

The static continuum spectrum has gaps down to zero; every finite dynamic
quadrature has a lowest positive gap. Agreement on finite conservation tests
cannot establish an adiabatic critical state at arbitrarily low acceleration.
There is no relaxation or dissipation in these tests, so generic initial states
need not settle to the static ground branch. Adding a relaxation term without
an energy receiver would invalidate the conservation claim.

The nonlinear dimensionless fixtures are Hamiltonian tests, not a physical
species calibration. Their internal gap, dipole and free carrier rest masses
are not asserted to form actual bound states with that spectrum. A microscopic
bound/continuum theory must establish that separately.

## Matter transport, gravity and static fitting

The displayed field/material Hamiltonian specifies a rest-frame local medium;
its centers are fixed in the numerical tests. Translational medium dynamics,
pressure, gravitational source mass and momentum exchange would be required in
a galaxy calculation. A local field's causal characteristics do not complete
general relativity or provide those dynamics automatically.

The baryon-only static fit neglects medium gravity and enclosed free countercharge.
If either matters, the relation must be re-derived with those sources. The
all-dark-mass bound is deliberately optimistic about polarization strength and
does NOT justify neglecting that mass's gravity in the fit. Splitting the
reservoir between free carriers and neutral medium tightens the available budget.

The profile-specific length/frequency bounds each allocate the entire local
reservoir to the medium. They are NOT four independently adjustable microscopic
lengths or cutoff frequencies. A universal d,gap spectrum and chi imply one
medium density and response cutoff. Taking different optimistic bounds as
actual values for each galaxy would reintroduce forbidden type-dependent tuning.

For example, requiring one uniform medium across all four proxies restricts its
density to no more than the smallest available density. This means a common
dipole length of at least the cluster's 5.22 kpc optimistic bound, not choosing
8.7 pc in the disk and 5.22 kpc in the cluster. A different density in each galaxy
changes susceptibility unless a physical self-regulation law is derived.

The response numbers at x=1e-4 are angular-frequency-times-time bounds for
representative critical modes with s/s_max~x/f. They are not exact equilibration
times, a cumulative ionization probability, or a theorem that all initial
conditions fail. A static initially prepared state is a separate assumption.

The displayed physical table fixes epsilon=.1; it is not an exclusion for every
countercarrier mass. Keeping epsilon symbolic, the same optimistic sum-rule
bound gives

    Omega_relevant*t_dyn <= sqrt[18eta/(1+eta)] * x/(sqrt(epsilon)*f^(3/2)).

Requiring an adiabatic response factor A at this representative gap therefore
requires epsilon <=18eta*x²/[(1+eta)*A²*f³]. This is a conditional parameter
restriction for adiabatic following, not a derived universal choice of epsilon.
Making the negative carriers lighter also changes their free-plasma response;
that response cannot be held fixed while improving only the polarization time.

## Parameter accounting and status

The low-field exponent fixes the required critical spectral power p=1. Matching
the leading force and deep acceleration coefficient relates beta and the field
cutoff to chi,G,a0. Chi is calibrated, not derived. Dynamic cutoff, constituent
masses/mass ratio, density, microscopic ionization channel and initial conditions
remain physical inputs or constrained combinations. No claim of a one-parameter
complete theory is warranted.

The old maximum-displacement/core exclusion is not applicable to D=E+P here.
The previous vacuum q/m is replaced by sqrt(4piG(1+chi)); reusing it would spoil
the matching. The new medium instead faces passivity, mass and oscillator-strength
constraints derived in DERIVATION.md.

Both the unit tests and bounded experiment passed. Experiment stderr is empty.
Manifest hashes track all imported local code and input derivation/design files.
No predecessor source or evidence was changed, no live galaxy formation was
run, and no independent review, publication or commit is claimed.
