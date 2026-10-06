# Recombination's clock and dark energy's geometry have different lever arms

Checkpoint SOL61-RECOMBINATION-2026-10-05. Base at start:
`3b06b67c4ed9180a3b7dc6692f3daf64f9625986`.
This coordinator calculation is a restricted flat-GR background discriminator,
not a recombination solver or a new dark-energy theory.

## Fixed assumptions and source dictionary

Use physical densities omega_i=Omega_i h^2, fixed baryon/cold/radiation
densities, T0=2.7255 K, omega_b=.02237, omega_c=.1200 and baseline h=.6736.
The Planck values are conditional base-LambdaCDM parameters, not measurements
of a unique microscopic cold species. The paper was checked in
[Planck 2018 VI, arXiv:1807.06209v4](https://arxiv.org/html/1807.06209v4),
Table 2 and sections 3.1/3.5, on 2026-10-05. Section 3.1 distinguishes the
last-scattering ruler from the baryon-drag ruler and uses their angular/distance
ratios. No Planck chain or likelihood was run here.

For the calculation, z_star=1090 is fixed, radiation has massless neutrinos
with N_eff=3.046, and omega_m=omega_b+omega_c. This omits the baseline massive
neutrino's exact interpolation. It is consequently an approximate illustrative
background, not a precision reproduction of Planck's sound horizon or theta.
Varying omega_Lambda changes the implied H0 while retaining flatness and the
physical densities. Holding H0 and all density fractions simultaneously fixed
would be a different, overconstrained variation.

## Exact sensitivity identity in this model

Write a_star=1/(1+z_star), H100=100 km/s/Mpc and

    H(a)^2/H100^2 = omega_r/a^4 + omega_m/a^3 + omega_Lambda,
    F(a) = omega_r + omega_m a + omega_Lambda a^4,
    R_b(a) = 3 omega_b a/(4 omega_gamma).

The comoving integrals are

    r_s = (c/H100) integral_0^a_star
                     da/[sqrt(3(1+R_b)) sqrt(F)],
    D_M = (c/H100) integral_a_star^1 da/sqrt(F),
    theta_star = r_s/D_M.

For either positive weight I=integral weight/sqrt(F), differentiation gives

    d ln I/d ln omega_Lambda = -1/2 <f_Lambda>_I,
    f_Lambda(a) = omega_Lambda a^4/F(a).

With positive matter/radiation densities f_Lambda increases monotonically
with a. Therefore the early ruler obeys the **uniform analytic bound**

    0 <= -d ln r_s/d ln omega_Lambda <= f_Lambda(a_star)/2.

The late distance samples much larger f_Lambda. This conclusion follows from
the weighted derivative, not from a finite grid. It assumes constant vacuum;
an evolving or interacting component requires its actual rho(a) and source
equations instead.

## Executed numbers and controls

The script derives omega_gamma from the blackbody energy density and derives
omega_r including the stipulated massless-neutrino factor. SciPy quadrature
and independent 50-digit differentiation of the complete mpmath integrals agree.
For this background:

| Quantity | Value |
|---|---:|
| Constant-vacuum fraction at z=1090 | 1.2751e-9 |
| d ln H_star / d ln omega_Lambda | 6.3756e-10 |
| d ln r_s / d ln omega_Lambda, fixed z_star | -1.1083e-10 |
| d ln D_M / d ln omega_Lambda | -0.0664493 |
| d ln theta_star / d ln omega_Lambda, fixed z_star | +0.0664493 |

The approximate r_s=144.43 Mpc is the ruler at the fixed last-scattering epoch,
not the drag ruler near 147 Mpc. Its numerical precision is not astrophysical
accuracy. The saved zero/half/double-vacuum variants make the separation explicit:
the early ruler barely changes while the distance changes substantially.

A separate local control adds a smooth early component with fraction f_e of
the new total density while keeping the other densities fixed. Then

    H_new/H_old = 1/sqrt(1-f_e).

At f_e=.1 this is a 5.41% change. This is **not** the tiny present constant
vacuum contribution extrapolated backward. A new switch, conversion reservoir
or field excitation can have early stress even when its MOND multiplier is
OFF. Its actual density and perturbations must be included. This control does
not solve the ionization response or bound early-dark-energy models with data.

## What this clue says about identity

Successful recombination mainly tests the atomic rates, baryon/photon ratio
and expansion at that epoch. The present constant vacuum is far too dilute
there to be read directly from its effect on the local clock in this model.
CMB sensitivity to that vacuum can enter through the late distance, lensing
and integrated potential evolution. Inferring a late component from that
geometry does not identify its microscopic nature.

Conversely, a cold-like source relevant before recombination is not optional
merely because the late acceleration is labeled dark energy. The growth lane
derives the density and velocity memory that connects the acoustic epoch to
later structure. A unified action must reproduce both roles and their stress,
sound speed and transfer; naming both terms one field does not provide that
derivation. A theory with different gravity must first derive its own H(a)
and perturbation equations before using these numbers.

Original objective: understanding and closure of the dark-sector mechanism
remain OPEN. The gain here is an explicit sensitivity dictionary separating
direct early stress from late geometric evidence. This is standard Friedmann
physics reconstructed for this program, not a worldwide novelty claim.

Reproduce with `expansion_levers.py --output <new result path>`.
The standard contract and run retain input/output hashes, software versions,
11 checks, stdout/stderr and independent quadrature/differentiation controls.
