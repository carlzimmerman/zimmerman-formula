# Finite kinetic halos and radial stability

18 October 2026. Checkpoint ZAR-2026-10-18-02, continuing ZAR-2026-10-18-01 at Git baseline `3c01aa2861bf576f4c2d942251eb9d2f89cae108`. The parent [kinetic model](../KINETIC_PARTITION.md) is unchanged.

**Finite boundary matching is possible in this effective model, and radial stability can be proved for specified finite families.** The strongest result preserves the exact deep halo profile on an interior annulus, tapers smoothly to cold vacuum, and has positive coupled radial displacement energy. It uses circular orbits with randomly oriented planes: nonzero tangential dispersion, but zero radial dispersion. A second construction gives genuinely warm, regular isotropic finite halos and a sufficient linear stability bound, proved attainable in a dilute regime. These results do not establish a smooth, halo-dominated, isotropic galaxy that is stable against general disturbances.

No scientific script, simulation, numerical shooting, registered statistic, or array analysis was executed. No running process was inspected or changed. Claude's calculations and all frozen criteria were left alone.

## Results and their limits

| Construction | Finite core and outer matching | Galaxy-law annulus | Stability established |
|---|---|---|---|
| Sharp truncation of the old isotropic r^-2 profile | Impossible without changing the distribution or boundary problem | Exact up to a sharp edge was attempted | Refuted by the phase-space velocity-support bound |
| Smoothly tapered circular-orbit populations | Hollow cold core; smooth outer density; finite mass and energy; no wall | Exact M_c = A r on any chosen interior annulus | Linear stability for coherent spherical radial shell maps that conserve each shell's angular momentum |
| Compact isotropic cutoff populations | Regular core with extended smooth baryons; density and pressure vanish at each phase edge | Not required by the elementary construction | Radial linear stability when the explicit susceptibility bound holds; attainable for nonzero dilute populations |
| Lowered exponential populations with a small tethered component | Regular finite core and cutoff | Arbitrarily close to A r on a chosen finite-width logarithmic annulus | Not established for the concentrated annulus branch |

The amplitude A = sqrt(a0 M_b/G) and population fraction remain chosen inputs where used. No result selects kappa or the cold abundance. All symbolic claims hold independently for either positive a0 footing. The calculations use the parent model's spherical deep cubic force, with no finite stiffness or relativistic completion.

## The boundary result that changes the next step

For an isotropic finite population with cutoff energy E_c = Phi(R), write psi = Phi(R) - Phi(r). Particle speeds satisfy v^2 <= 2 psi, hence its one-dimensional dispersion obeys sigma^2 <= 2 psi/3. Cutting the previous r^-2 profile at R and merely adjusting its Jeans integration constant instead gives sigma^2/psi -> 1. Thus zero surface pressure alone does not make that truncated Jeans solution physically realizable. A taper or a change of orbital distribution is essential.

[BOUNDARY_MATCHING.md](BOUNDARY_MATCHING.md) gives that proof, the exterior potentials, an explicit smooth finite circular family, regular isotropic existence, and the approximate-annulus continuation.

## The radial stability result

Let mu_i = M_i' and xi_i be a coherent radial displacement of each circular population, preserving its angular momentum. The complete second variation, including the response and orbital energy, is

\[
W''=\int\left[
\mu_t\kappa_t^2\xi_t^2+\mu_f\kappa_f^2\xi_f^2
+\frac{G\mu_t\mu_f}{r^2}(\xi_t-\xi_f)^2\right]dr>0
\]

for nonzero admitted displacements. The positive final term controls relative displacement between the populations. With fixed point baryons and support inside R, kappa_i^2 >= G M_b/R^3. Adding radial kinetic energy gives a conserved coercive linear energy. This proves linear Lyapunov stability in a weighted displacement and velocity norm for that radial shell class; it does not control shell crossing or nonradial motions.

[RADIAL_STABILITY.md](RADIAL_STABILITY.md) gives the full derivation and a separate kinetic energy-Casimir bound for smooth isotropic populations. Potential energy alone has an indefinite Hessian, so neither a static force balance nor a positive cubic interaction suffices to claim general stability.

## A new obstacle to generic isotropic matching

The constant-f, two-temperature isothermal asymptote is a saddle when one integrates outward in radius. Its composition mode has a growing spatial exponent

\[
\lambda_+=\frac{-1+\sqrt{1+8f}}2>0.
\]

This does not prove a dynamical instability. It says that generic regular core conditions do not automatically land on the old infinite constant-f solution. A finite halo may need a varying fraction, a selected core trajectory, or an orbital distribution different from the isotropic ansatz. The derivation is in [BOUNDARY_MATCHING.md](BOUNDARY_MATCHING.md#the-mixed-isothermal-profile-is-a-spatial-saddle).

## What is still open

The remaining physical target is one finite halo with a substantial tethered component, a regular phase-space distribution, the required galaxy-law annulus, counted formation and transfer, and stability under the disturbances that its actual dynamics admit. The results here resolve narrower parts of that target and identify a concrete next analytic route: broaden the radially cold circular distributions while preserving the positive radial energy and solve the resulting finite transition layer. The concentrated isotropic approximate-annulus family is another open stability route; the dilute bound must not be transferred to it without checking its susceptibility.

Full three-dimensional stability additionally needs a three-dimensional action. The present nonlocal spherical energy does not define arbitrary angular perturbations, so no nonspherical verdict follows from these radial proofs. Cosmological supply, the depletion region, formation, light bending and parameter selection remain separate obligations.

The independent checks, prior overlap, exact claim scopes and continuation record are in [AUDIT_AND_HANDOFF.md](AUDIT_AND_HANDOFF.md). Input and output hashes are in [CHECKPOINT.json](CHECKPOINT.json). There is no claim of global scientific novelty or empirical validation.
