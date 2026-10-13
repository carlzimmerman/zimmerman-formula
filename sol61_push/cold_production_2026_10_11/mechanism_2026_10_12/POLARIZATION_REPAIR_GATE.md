# A dynamical gate on borrowing a polarization mechanism

12 October 2026. Status: a conditional linear repair calculation, not a completed cold-energy mechanism. This extends the earlier POLARIZATION_SELECTOR.md audit to a published dynamical failure mode. The earlier density-only pressure obstruction is already in NONLINEAR_PORTAL.md and is not a new result here.

## External evidence and its scope

[Stahl et al., arXiv:2209.07831v1](https://arxiv.org/pdf/2209.07831), Sections 4.3–4.4 and Eq. (21), report a growing polarization mode in their spherical, deep-MOND dipolar-fluid simulations. Their initialized force relation deteriorates as the instability develops. Their leading reduced equation is Pi_ddot approximately 4 pi G rho_dm Pi. Here rho_dm is the monopolar fluid density, not the effective density from polarization. Weak clustering lengthens the growth timescale. These are model simulations, not observational detection of dipolar matter, and they do not establish formation from generic initial conditions. The potential coefficients are phenomenological; this source does not derive our carrier's interaction or kappa=1/2.

The calculations below are our own conditional extensions of that reduced equation. They neither reproduce RAMSES nor transfer its instability to every polarization theory. In particular, POSITIVE_POLARIZATION.md uses a different action, so its spectrum must be assessed separately.

## Exact damping obstruction in the reduced mode

Write a scalar mode amplitude q with omega_g squared = 4 pi G rho_dm > 0. A proposed passive friction repair gives

    q_ddot + gamma q_dot - omega_g^2 q = 0,  gamma >= 0.

The characteristic roots obey

    lambda_plus = 2 omega_g^2 / [sqrt(gamma^2+4 omega_g^2)+gamma] > 0,
    lambda_plus lambda_minus = -omega_g^2 < 0.

Thus every finite nonnegative friction coefficient leaves a growing root. This algebraic conclusion holds for this equation at every positive density. Friction dissipates the kinetic energy but cannot turn an inverted quadratic potential into a minimum. It can delay growth; it cannot produce an attractor. This does not exclude memory kernels, additional conservative degrees of freedom, or other equations.

The undamped e-folding time is t_e=1/sqrt(4 pi G rho_dm). This is defined from Eq. (21)'s root, not identified with the paper's approximate characteristic disruption time. Nonlinear disruption also depends on initial amplitude and mode evolution.

## Collision proxy and quantitative scale

For a diagnostic only, assign gamma=rho_dm S v, where S=sigma/m. This assumes an order-one conversion from collision frequency to polarization damping; the carrier action has no derived polarization variable, so this identification is not established. Take the current screening branch S=0.3 cm^2/g and a chosen v=200 km/s.

| Monopolar density, kg/m^3 | Undamped e-folding, Gyr | With collision proxy, Gyr |
|---:|---:|---:|
| 1e-27 | 34.60097 | 34.60108 |
| 1e-25 | 3.46010 | 3.46021 |
| 1e-23 | 0.346010 | 0.346123 |
| 1e-21 | 0.034601 | 0.034714 |

The high-density rows deliberately test a proposed identification with clustered carrier matter. They are not self-consistent weak-clustering solutions or claims that the published simulations used these densities.

To obtain t_e >= T by friction alone requires

    gamma >= max(0, omega_g^2 T - 1/T),
    S >= max(0, 4 pi G T - 1/(rho_dm T))/v.

At rho_dm=1e-21 kg/m^3 and T=10 Gyr, this is S approximately 13,234 cm^2/g under the proxy, about 44,113 times the benchmark. It still leaves an instability. This is a conditional required damping scale, not a cross-section exclusion or a new measured limit. Without damping, t_e >= 10 Gyr instead requires rho_dm <= 1.19723e-26 kg/m^3. A low-density separate medium therefore evades rapid growth in this simplified diagnostic, while giving up the direct identification with a dense carrier halo.

## What a conservative repair would need

A hypothetical local restoring term and spatial stiffness give

    q_ddot + gamma q_dot + (Omega_0^2 + c_p^2 k^2 - omega_g^2) q = 0.

For gamma>0 both roots have negative real part when the parenthesized coefficient is positive; a negative coefficient retains one positive root. Equality has a zero mode and does not establish attraction. With gamma=0, positive stiffness gives oscillations rather than decay.

Gradient stiffness alone cannot stabilize the k=0 mode in an infinite or periodic domain. For a scalar field on a ball with a specified zero-value boundary, the lowest Laplacian wavenumber is pi/R. Under that illustrative boundary condition, Omega_0=0 needs c_p>omega_g R/pi. At R=100 kpc and rho_dm=1e-21 kg/m^3 the threshold is about 900 km/s. At rho_dm=1e-25 it is about 9 km/s. A vector polarization field with other boundary conditions has a different mode problem; the scalar ball is not a galaxy model.

Both repairs also enter the static response. For example, a static source J in this toy equation produces q=J/(Omega_0^2+c_p^2 k^2-omega_g^2). The terms cannot be added to evolution while simply retaining a previously imposed constitutive force law. A full action must determine equilibrium and its perturbations together. These restoring coefficients and their microscopic origins have not been derived.

## Research decision

Do not splice the published dipolar equilibrium into the protected carrier and call the mechanism complete. Passive scattering is not a stability repair for the reduced growing mode. A viable next candidate needs a specified action that simultaneously supplies the extra response, a stable sourced configuration, and the acceleration coefficient. Its force must be computed after including the stabilizer. Separately, the link a0=(c/2)sqrt(G rho_DE) remains unproved; none of this calculation fixes it.

The cold carrier, an observed acceleration correlation, and a dynamically selected halo are three separate claims. Our work supports conditional cold production and identifies obstacles to the bridge; it has not built that bridge or established laboratory production of a new energy source.

## Reproducibility and review

polarization_repair.py, polarization_repair_contract.json and polarization_repair_run/ contain the inputs, output, logs and validated manifest. All 26 checks pass: characteristic-root identities, five independently integrated initial-value solutions, damping times, and four two-dimensional stability matrices. Resource limits were 30 seconds, 16,000 output bytes and one numerical-library thread. Floating calculations are not interval-certified. The universal friction conclusion follows from the displayed root product, not the finite checks. Self-review distinguishes the source's monopolar density, our illustrative collision proxy, e-folding time, finite-domain boundary assumption, and the unresolved microscopic coupling.
