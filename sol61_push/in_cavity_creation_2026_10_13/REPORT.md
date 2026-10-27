# Producing cold pairs inside a prescribed repulsive cavity

2026-10-13. This tests a way to avoid collisional capture: create the carrier already below the wall energy inside a hollow messenger medium. A prescribed static wall can strongly suppress tunnelling. However, the corresponding threshold production rate is extremely small in the matched messenger example. This is not a constructed cavity, an experimentally allowed model or a working manufacture protocol.

## Wall fixed by the preceding interaction

Retain h|Phi|²|S|² with m=1 MeV, M_S=10 MeV, h=1 and prescribed nonrelativistic messenger number density n_S=1e25 m^-3. The mean-field wall height is

\[
U=\frac{h n_S}{4mM_S}=1.9208764\times10^{-9}\ \mathrm{eV},
\]

where the SI density is converted to natural units in the evaluation. Let the cavity interior and exterior have zero potential, with a finite repulsive shell between them. The shell acts on both carrier charge signs. This is an imposed density profile, not a solved messenger configuration. Its electrical neutralization, mechanical stability, temperature, fluctuations and creation remain unestablished.

For a locally planar rectangular wall of thickness d and normal incident kinetic energy 0<K<U,

\[
T=\left[1+\frac{U^2\sinh^2(\kappa d)}{4K(U-K)}\right]^{-1},
\qquad \kappa=\frac{\sqrt{2m(U-K)}}{\hbar c}.
\]

At K=1e-9 eV the carrier speed is 13.41 m/s. A 10-micrometer wall transmits about 5.03% per planar incidence; a 100-micrometer wall transmits 5.14e-19. Near the top of the barrier, at K=1.8e-9 eV, the latter transmission rises to 1.35e-7. The full energy distribution therefore matters.

A finite positive shell with zero potential outside does not yield an ordinary negative-energy bound state. These figures describe leakage suppression, not exact permanent confinement. Curvature, cavity resonances, wall inelasticity, density noise and angular distributions need a separate calculation. No three-dimensional lifetime is inferred by multiplying this transmission by an assumed bounce frequency.

The one-dimensional 1 mm hard-box ground-energy scale is 1.92e-13 eV, below the chosen K. This is only a mode-spacing screen. It does not verify the free-space production amplitude in the actual finite cavity or justify ignoring all cavity effects.

## Production inside the interior

The messenger matched C=-4.8392072e-19 eV^-2. Use the leading free-space contact process gamma+gamma -> Phi+anti-Phi as a first yield estimate, with equal head-on photons of energy E_gamma=m+K:

\[
\sigma=\frac{C^2(4E_\gamma^2)}{8\pi}
\frac{\sqrt{K(2m+K)}}{m+K}.
\]

At K=1e-9 eV the SI cross section is 6.4902e-47 m². Take two **assumed** 1 MW beams, each with area 1e-6 m², overlapping over 2 mm. Their number density is n_gamma=P/(A E_gamma c), and the ideal uniform-overlap event rate is

\[
\dot N=2c\,n_\gamma^2\sigma\,A L
=3.3735\times10^{-14}\ \mathrm{s}^{-1}.
\]

The corresponding mean wait for one pair is about 939,000 years. This already neglects attenuation, source inefficiency, imperfect overlap and energy spread. It is not a laboratory prediction for an available source. Cavity-state production, correlations and possible stimulated effects are not computed.

Keeping K near 1e-9 eV around a 1 MeV rest energy requires control of the excess-energy scale at roughly 1e-15 relative precision, including knowledge of the physical carrier mass. Beam angle and energy imbalance also add center-of-mass motion. A bandwidth/pulse-duration scale hbar/K is about 0.658 microseconds; this uncertainty scale alone does not establish a source with the required simultaneous power, direction, linewidth and stability.

The code evaluates sqrt[K(2m+K)] directly, rather than subtracting nearly equal squared MeV energies, to avoid catastrophic floating-point loss of the small kinetic energy.

## What this does and does not resolve

Creating particles inside a barrier avoids requiring them to scatter before escape. It is logically different from the failed centimeter stopping reservoir. It also avoids a subsequent cooling stage **if** the input genuinely prepares the required low-energy modes. But it demands an unobserved charged messenger medium, a stable hollow profile and precision gamma photons, while yielding a negligible production rate in this example. It is not a practical creation recipe or a derivation of enhanced gravity.

The meaningful remaining route is a different production mechanism with a quantitatively larger rate at low final kinetic energy, not merely making this wall thicker. Any such route must retain the reservoir and energy-accounting obligations rather than assuming them away.

## Verification

Twelve checks pass: nine independent Schrödinger transfer-matrix integrations against the barrier formula, the subbarrier range, a finite-box energy-scale screen and photon energy-flux accounting. The thick physical-wall values use the analytic rectangular-barrier expression; the transfer integration tests its normalized form on the stated bounded cases. The manifest records executed inputs and outputs. No new Lean or empirical certification is claimed. The overall manufacture goal remains incomplete.
