# Recombination and structure growth: clues to the dark sector

Fourth Sol61 research lane, created at Carl's request on 2026-10-05.
Starting checkpoint: `3b06b67c4ed9180a3b7dc6692f3daf64f9625986`.
**The standard mechanism is mathematically understood; the physical identity
and complete action of this program's dark sector remain OPEN.** This folder
separates what the early universe requires from what those requirements cannot
uniquely identify. It contains executed calculations, source checks and audits.

## Why recombination worked

Cooling alone is insufficient as an explanation. A dilute electron/proton
gas has a large translational entropy, and photons outnumber baryons by about
1.6 billion to one. Chemical equilibrium therefore favors ionization long
after the temperature falls below hydrogen's 13.6 eV binding energy. The
ground-state Saha equation is

    x_e^2/(1-x_e) = (m_e kT/2pi hbar^2)^(3/2)
                    exp(-chi/kT)/n_H.

The hydrogen-only calculation gives half ionization at about 3734 K in
equilibrium, with chi/kT about 42. These are model calculations at the
specified baryon abundance, not newly measured constants. An exponential
photon-tail inventory by itself does not derive this milestone.

Real neutralization is delayed by reionization and trapped line photons.
Stable ground-state atoms accumulate through **both** two-photon 2s decay
and Lyman-alpha escape as expansion redshifts photons away from resonance.
The effective escape probability is

    C = (Lambda_2s + R_escape)/(Lambda_2s + R_escape + beta),
    R_escape = 8pi H/[lambda_Lya^3 n_H(1-x_e)].

The controlling net capture rate involves C n_H alpha_B/H. The individual
8.2-per-second two-photon rate is enormously faster than the expansion rate;
its smallness compared with ordinary atomic transitions is not by itself
the cosmological freeze-out criterion. The actual populations, reverse rates
and optical depth supply the rest of the argument.

As free electrons disappear, scattering opacity falls. Photon last scattering,
baryon momentum-drag release and later thermal decoupling are distinct events.
The separation between their dates is not the last-scattering width. The
[atomic report](atomic_recombination/REPORT.md) derives their definitions,
solves a controlled hydrogen-only rate system, and corrects earlier shortcuts.
It is not a precision multilevel recombination or CMB likelihood calculation.

## Why structure could grow afterward

Before drag release, baryons share photon pressure: the coupled fluid has
sound speed squared c^2/[3(1+R_b)] and oscillates. A sufficiently cold,
weakly photon-coupled gravitational source can preserve a growing mode and
support the potentials. Recombination releases baryons from that large
photon-pressure coupling; it does not create the required cold source.
Radiation-era growth, equality and matter-era growth must all fit the same
history. In the matter-dominated pressureless limit, delta_m grows as a
and its gravitational potential approaches a constant.

The [growth report](growth_and_identity/REPORT.md) derives the exact linear
relative invariant, for common gravity and pressureless drag-free species,

    a^2 d(delta_b-delta_c)/dt = constant.

The metric sources cancel, so this statement does not require a matter-only
background or a subhorizon Poisson approximation. Pressure, photon drag,
different forces or changed continuity equations modify it in specified ways.
For an explicit nonrelativistic wave, quantum pressure contributes a k^4
term in its applicable regime. This is a diagnostic for the candidate action,
not a unique particle-identification experiment.

The matter-era transfer also preserves **both density and velocity** at drag:

    A_growing = [3 delta_m,drag + 2 d(delta_m)/dln a|drag]/5.

Baryons catching up to the cold density does not erase acoustic information
already projected into that growing amplitude. Actual predictions require
physical transfer functions, not the report's chosen demonstration modes.

## Putting the small clues together

| Clue | What it constrains | What it does not identify |
|---|---|---|
| Saha equilibrium and kinetic neutralization | Hydrogen number density, atomic energies, capture/reverse rates and expansion combinations | A vacuum value, 32pi or a cold particle species |
| Opacity and baryon loading | The ordinary Thomson-coupled electron/baryon component | All gravitating matter cannot be relabeled hydrogen without changing these observables |
| Acoustic potential support and later growth | A cold-like perturbation source with the required pressure, stress and initial transfer | Whether that source is particles, a massive wave or another admissible field |
| Relative baryon/cold invariant | Equal-force and pressure assumptions of a specific action | Nonlinear mergers, feedback or multistream identity |
| Tiny constant vacuum fraction at recombination | Present constant vacuum scarcely affects the direct early clock in the stated background | Evolving early dark energy or new field/switch stress need not be tiny |
| Late distance, growth suppression and pressure | The late background/perturbation stress history | Its unique microscopic decomposition |

The [expansion calculation](EXPANSION_LEVERS.md) makes the different lever
arms explicit. With fixed physical matter/radiation densities, fixed z_star
and constant vacuum in an approximate flat-GR model, its fraction of the
density at z=1090 is 1.275e-9. The early sound ruler's logarithmic response
to that vacuum is about -1.11e-10; the late distance response is about -0.06645.
Thus using the CMB to infer late geometry is different from measuring vacuum
through recombination chemistry. These derivatives change H0 consistently
with flatness and are not Planck likelihood constraints.

An exact ambiguity survives even when growth is included. For a universally
metric-coupled constant-pressure dark fluid,

    p = -rho_Lambda,
    T_mu_nu = rho_c u_mu u_nu - rho_Lambda g_mu_nu,
    rho = rho_Lambda + C_initial a^-3.

Before dust caustics this is the same stress as dust plus vacuum. The cold
amplitude C_initial remains independent of rho_Lambda. Calling both roles
one fluid does not select that amplitude or explain the vacuum. Conversely,
a scalar with the same background but different pressure perturbations can
fail the acoustic/growth tests. The stress, couplings and admissible state
must be derived, not inferred from the field's name.

## Candidate-specific work toward closure

The next useful step is an action-to-observable dictionary joining this lane
to [the main theory](../main_theory/README.md),
[the cold component](../cold_component/README.md) and
[the coefficient puzzle](../puzzle_32pi/README.md):

1. Derive H(a), physical baryon/electron currents, temperature evolution and
   any photon/heat injection from one retained action, including switch stress.
2. Derive its photon-baryon oscillator and cold perturbation pressure/shear;
   predict the relative invariant or its explicit sourced violation.
3. Supply actual density **and velocity** transfer functions through equality,
   recombination and drag; initialize later structure with both.
4. Pass the physical atomic rates to an authenticated multilevel solver and
   the same perturbation system to a Boltzmann solver before joint fitting.
5. Test whether any proposed cold/vacuum unification removes independent
   charge, offset or coupling freedom. If it does not, retain that freedom
   honestly and seek a discriminating pressure/force/energy-transfer prediction.

Prior CFG253/288 already tested recombination-era cold creation and its
energy/CMB problems. Those failures were read and not rerun here. Atomic
neutralization is not a newly discovered reservoir for cosmological cold mass.
No particle identity, vacuum origin, 32pi derivation or complete theory is
claimed from these clues.

## Evidence and review

- Atomic laboratory: `atomic_recombination/contract.json` and
  `atomic_recombination/runs/atomic_lab_v2_sources/`; primary-source versions/URLs/hashes
  are recorded in `atomic_recombination/sources.json`.
- Growth: 23 passing checks with independent coupled ODE controls; the
  omitted-initial-velocity mutation has two expected failures, retained in
  `growth_and_identity/runs/velocity_drop_a/`.
- Expansion: 11 passing checks, including an independent 50-digit integral
  differentiation, in `runs/expansion_a/`.
- Independent sibling derivations: [expansion review](review/EXPANSION_REVIEW.md)
  and [growth review](review/GROWTH_REVIEW.md). Root separately inspected the
  atomic equations, conventions and derivative/opacity distinctions.

All numerical statements are confined to their declared approximate models.
The main theoretical identities have separate written derivations; passing
checks and valid manifests do not prove the requested fundamental identity.
Downloaded reference copies remain a local cache; reproducible source
acquisition requires the versions and hashes in the source registry.
