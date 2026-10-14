# Manufacturing pairs through the polarizability operator

2026-10-13. This extends the previous radiative matching result toward manufacture rather than pumping an existing inventory. Status: a conditional, leading-contact production channel has been calculated. No measured yield, complete ultraviolet model or prepared cold medium is established.

## Production process and normalization

Take the local operator already identified as necessary in the photon-portal EFT,

\[
\mathcal L_{\rm int}=-C_\phi\phi^*\phi F_{\mu\nu}F^{\mu\nu}.
\]

Here C_phi has mass dimension -2, metric is (+---), and hbar=c=1. Treat C_phi as a real, independent Wilson coefficient and compute this contact contribution alone. It permits

\[
\gamma(k_1)+\gamma(k_2)\longrightarrow\phi+\bar\phi.
\]

Up to an irrelevant overall sign the amplitude is

\[
\mathcal M=4C_\phi[(k_1\cdot k_2)(\epsilon_1\cdot\epsilon_2)
 -(k_1\cdot\epsilon_2)(k_2\cdot\epsilon_1)].
\]

It vanishes upon replacing either photon polarization by its momentum. Averaging over the four incoming transverse polarization combinations gives

\[
\overline{|\mathcal M|^2}=2C_\phi^2s^2,\qquad
\boxed{\sigma_{\gamma\gamma\to\phi\bar\phi}
=\frac{C_\phi^2s}{8\pi}\sqrt{1-\frac{4m^2}{s}}},\quad s\ge4m^2.
\]

Below threshold the cross section is zero. The final particles are distinguishable, so there is no final-state factor 1/2. The result is angle-independent at this contact order. Parallel linear photon polarizations give twice the unpolarized cross section; orthogonal linear polarizations give zero.

The phase-space normalization is the two-body scattering formula in [PDG Kinematics, 2024 edition](https://pdg.lbl.gov/2024/reviews/rpp2024-rev-kinematics.pdf), Eq. (49.33). Integrating over the kinematic interval Delta t=s beta gives sigma=beta averaged|M|²/(16 pi s). PDG supplies the scattering normalization, not evidence for this hypothetical operator or field.

This is not the full amplitude of the earlier cubic-plus-photon model. Light-field loops, interference, additional operators and matching must be included at a consistent chosen order. In particular the previous soft-background loop estimate is **not** automatically the coefficient of a full timelike pair-production amplitude near s=4m². No numerical physical C has been substituted here. Perturbative amplitudes and the derivative expansion must remain controlled.

## A cold source requires threshold control

For equal, head-on photons of energy E_gamma, the center of mass is at rest and

\[
s=4E_\gamma^2,\quad K=E_\gamma-m,\quad
\beta=\frac{\sqrt{K(2m+K)}}{m+K}.
\]

At m=1 MeV the computed examples are:

| K per product | Required energy per photon | Product speed |
|---:|---:|---:|
| 1 micro-eV | 1 MeV + 1 micro-eV | 424 m/s |
| 1 milli-eV | 1 MeV + 1 milli-eV | 13.4 km/s |
| 1 eV | 1 MeV + 1 eV | 424 km/s |
| 5 eV | 1 MeV + 5 eV | 948 km/s |

These are individual kinetic energies, not equilibrium temperatures. Nonrelativistic does not mean slow on laboratory scales. Near threshold, sigma is proportional to sqrt(K/m), and vanishes exactly at threshold. Beam energy spread, angular spread and unequal photon energies broaden or boost the output. A cold laboratory distribution therefore requires more than a mean energy setting.

For general photon energies and collision angle theta,

\[
s=2E_1E_2(1-\cos\theta).
\]

The earlier approximately visible-light drive cannot produce 1 MeV carriers through this two-photon channel. This statement does not rule out all multiphoton, time-dependent-background or alternative-mass mechanisms; none of their yields is calculated here.

## Neutral production does not supply a charged condensate

All the currently specified vertices preserve global U(1): charges are q_phi=1, q_chi=2, and photons carry zero. For an invariant quantum evolution U, [Q,U]=0. Starting in a Q=0 state therefore remains in the Q=0 sector. This forbids manufacturing net charge in an isolated neutral apparatus, but it permits positive energy in particle-antiparticle pairs and local charge with compensating charge elsewhere.

The original October 11 REPORT already identified this distinction for a different, real-source model. This is not a new conservation-law discovery. The new result is a direct photon production channel associated with the October 13 polarizability operator.

The same |phi|² F² potential acts equally on particles and antiparticles. By itself it is not a charge-sign-selective separator. The earlier one-sign nonrelativistic condensate, interface and pumping calculations cannot simply be applied to this two-component output. One must solve its interactions and losses, or specify a physical separation mechanism and account for the opposite charge. Reverse annihilation channels are also allowed; their medium kinetics have not been computed here.

Energy bookkeeping: creating equal masses of particles and antiparticles from photons costs at least their combined rest energy. If one retains 1 kg of one sign and discards an equal opposite-sign mass without recovering its energy, the ideal input is at least 2 c² = 1.7975e17 J per retained kg, before kinetic energy and inefficiency. This is not an irrecoverable bound if energy is recovered from the discarded component, nor a bound for a neutral medium retaining both signs.

## Verification and next decisive work

`check.py` passed 17 bounded checks: photon Ward identities, explicit transverse polarization sum against a covariant contraction, integrated cross-section normalization, vertex charge bookkeeping, five mass-shell cases and the optical threshold. The run manifest records inputs and outputs. These checks verify the specified calculation, not the field's existence, a universal production theorem or a Lean-certified result.

The route now has a specified ordinary input (photons), output, threshold and conditional rate. What prevents a manufacturing prediction is the undetermined physical coupling and full production amplitude, followed by a two-component capture/assembly calculation. A defensible next step is an explicit matched ultraviolet model with independent constraints; assigning a convenient C and declaring manufacture would not resolve that gap.
