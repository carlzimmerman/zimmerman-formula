# Magnetic storage from the reduced muon source

2026-10-13. Conditional leading-operator calculation, not a manufacturing protocol.
The source is the reduced muon-loop alternative in
../ordinary_lepton_source_2026_10_13/REPORT.md. No charged S wall is retained.

## Interaction inherited from the source

At soft photon and mediator momenta the magnitude of the muon-induced coupling is

    |g_soft| = 2 alpha |y_mu|/(3 pi m_mu) = 2.93123248e-15 eV^-1.

This follows from the heavy-lepton limit of the loop formula checked in the source
report. It is not exactly the on-shell coupling inferred from the decay width:
that magnitude is larger by 2.09019e-5 fractionally. Use the soft value for this
static calculation. Widths determine magnitudes, not the relative sign with mu.
Take the relative sign giving an attractive magnetic energy for illustration.

With L = -MR^2 R^2/2 -mu R|phi|^2 -g R F^2/4, integrating out R at tree level gives

    R = -(mu|phi|^2+g F^2/4)/MR^2,
    L_eff contains +mu*g |phi|^2 F^2/(4 MR^2).

Writing that term as -C |phi|^2 F^2 gives C=-mu*g/(4MR^2).
For MR=2e6 eV, m=1e6 eV and |mu|=27.72246466 eV,

    C = -5.07881180e-27 eV^-2,
    U_B = C B_nat^2/m,
    B_nat = 195.3527711 (B_SI/tesla) eV^2.

The conversion follows by equating magnetic energy densities:
B_nat^2/2 = [B_SI^2/(2 mu0)] (hbar*c)^3/(joules per eV).
The shift also follows independently from the magnetic R tadpole and
U=mu R/(2m). It applies to both charge signs of phi.

At 10 tesla the attractive shift has magnitude 1.93821e-26 eV.
The assigned vacuum daughter kinetic energy is 1e-9 eV. Extrapolating the
leading expression to equal this energy gives 2.27143e9 tesla. That number is
a scale comparison, not a controlled strong-field calculation or a construction
specification. Additional operators, matter response and nonlinear electromagnetic
physics have not been included. Independent photon counterterms could change
the answer; no such new coefficient is predicted by this calculation.

## Quantum localization is a separate condition

As an optimistic mathematical comparison, assume an ideal spherical attractive
square well of depth V and radius a. The s-wave radial matching condition is

    x cot(x) = -sqrt(z0^2-x^2),
    z0 = a sqrt(2mV)/(hbar*c).

The first negative-energy bound state exists only when

    V a^2 > pi^2 (hbar*c)^2/(8m).

Equality is a zero-energy threshold, not a normalizable bound state. This follows
by taking the exterior decay constant to zero, so x approaches pi/2. The matching
conditions are also given in [Andrew Cumming's PHYS 457 lecture](https://andrewcumming.github.io/phys457/lecture13.html).
The script checks roots at z0=1.6, 2 and 3; positivity of both matching terms
excludes roots for the two sampled subthreshold values 1 and 1.5. The threshold
argument, not those five samples alone, establishes the ideal-well criterion.

At the 10 T depth the radius must exceed approximately 1.574 km. At radius 1 cm,
the threshold depth is 4.80378e-16 eV, corresponding formally to 1.57431e6 T.
No magnetic geometry realizing a spherical square well is supplied. These results
are not a general bound on every trap: a repulsive shell, time-dependent fields,
additional interactions and many-particle states are different problems.

## Creation inside an attractive well does not automatically load it

There is a separate kinematic obstacle, even if a well supports bound states.
For a parent at rest with unchanged pole excess delta=MR-2m, local independent
daughter energies satisfy

    K_born = (delta-2U)/2,
    E_each relative to its free rest mass = K_born+U = delta/2.

For an attractive well U=-V, creation increases local kinetic energy by V.
With the assigned positive delta=2e-9 eV, each daughter remains above the free
escape threshold. Increasing well depth does not change that energy identity.
This excludes direct loading into two negative-energy bound states under these
assumptions; it does not exclude scattering, cooling, pair correlations, transient
resonances or a subsequent change of the trap. The field cannot capture a particle
arriving from infinity through a conservative static potential alone either.

A possible revised kinematic window would instead use a below-vacuum-threshold
parent with

    -2V < delta_eff < 0,
    delta_eff = MR(in field)-2m.

This is a necessary local energy window, not a calculated capture channel.
Quantum levels, source linewidth, overlap and actual in-field production must
also be matched. The old vacuum carrier partial width would then be closed and
must not be reused to claim the old production rate. A static repulsive shell
around a low-potential production cavity offers a different possible geometry;
its finite barrier supports metastability and needs its own wave calculation.

The fixed-pole identity is explicitly conditional. The muon loop also generates
higher operators including R^2 F^2, which can shift the source pole. The current
calculation does not match them or claim that the actual parent pole is unchanged.
They must be included before deciding an in-field source spectrum or asserting
that a particular negative delta_eff can be realized. The scalar potential's
stability, electroweak completion and empirical constraints remain open too.

## Verification and consequence

Ten symbolic/numerical checks pass. The bounded run records the prior source
results as a hashed input. Four Lean lemmas certify square completion, the
fixed-pole energy identity, its positive-excess implication and the subthreshold
energy-window equivalence. They do not certify loop matching, measured particle
existence, a trap geometry, the Schrödinger spectral theorem or physical capture.

The inherited photon interaction does not supply a demonstrated small static
storage device at this benchmark. Simply making particles colder does not solve
quantum localization; simply deepening an attractive well does not solve loading
from an above-threshold parent. Further work must calculate the full field-dependent
source and daughter spectrum or introduce and constrain another storage interaction.
The creation/storage research objective remains open.

Reproduce numerical checks:

    python3 sol61_push/muon_portal_magnetic_storage_2026_10_13/check.py /tmp/muon_magnetic_results.json

Lean command and captured diagnostics are in lean_record.json and lean_stdout.txt.
Constants follow the existing source conventions and [NIST/CODATA](https://physics.nist.gov/cuu/Constants/Table/allascii.txt); displayed digits are computational, not new measurement precision.
