# Nonspherical torque test: redistribution is not a selector

12 October 2026. Continuation of SETTLED_HALO_RESULT.md. Eight finite runs test whether breaking spherical symmetry in the baryon potential resolves the persistent initial-profile memory. It does not in this tested family. There is no claim of a universal obstruction to nonspherical cosmological assembly.

## Physical perturbation and initial conditions

Half of the fixed baryonic mass remains in a central Hernquist potential. The other half is split equally between two positive-mass Plummer spheres with softening a_b/2, at opposite rotating positions. Their displacement from the centre grows smoothly from zero to d during t=1 to 1.5 and subsequently rotates with angular frequency Omega=40 in code units. Thus the potential is sourced by positive masses rather than an arbitrary quadrupole that might imply negative density.

The two displacement choices d=0.01 and 0.04 target radii correspond to about 5.14 and 20.57 kpc. They are force brackets, not fitted Milky Way bars. Omega corresponds to approximately 13.14 radians/Gyr. The larger displacement deliberately perturbs a wider region. The prescribed driver is not a self-consistent stellar or gas dynamical solution.

The cold halos begin as circular shell equilibria with Plummer density scales b=0.15 or 0.30 target radii. Their initial circular speeds are computed from the actual initial force, including the coincident Plummer baryon pair. This baryon profile differs from the preceding pure-Hernquist baseline, so the static controls here are the appropriate comparisons. Initial mass profiles and baryonic masses are identical between a control and its driven counterpart. Self-gravity remains a softened spherical monopole; only the baryon forcing is nonspherical. No target force or thermostat is used.

There are static, narrow-pair and wide-pair cases at N=1024, dt=0.001 for both initial scales, plus wide-pair cases at N=2048, dt=0.0005. All finish at t=8 (24.35 Gyr of exploratory isolated model time), with one orbital-plane seed. This is not cosmological time evolution or a converged galaxy simulation.

## Work, torque and reservoir checks

As before, fixed-position changes of the external potential track driver work. After the growth phase, a rigid rotating potential satisfies

    partial_t Phi_b = -Omega partial_phi Phi_b,
    dE_c/dt = Omega dL_z,c/dt,
    E_c-Omega L_z,c = constant.

E_c includes cold self-energy once and the cold–baryon interaction. The identity uses total cold energy and angular momentum; it does not assert conservation of each particle's Jacobi energy in an evolving self-potential. The spherical self-force exerts no total external torque. All 16 declared work and Jacobi checks pass. Refined work discrepancies are below 2.6e-5 of initial binding energy and Jacobi discrepancies below 6.9e-6.

The rotating pair's nominal orbital angular momentum after growth is L_pair=f_g Mb d² Omega. Comparing cold angular-momentum gain after t=1.5 with that reservoir exposes the cost of externally maintaining the driver. The pair's internal Plummer structure is not assigned an additional spin reservoir.

## Results

| Initial scale | Driver | Maximum mass-profile error / supplied mass | Median absolute fractional particle angular-momentum change | Cold angular-momentum gain / nominal pair reservoir |
|---:|---|---:|---:|---:|
| 0.15 | Static, 1024 | 43.542% | roundoff | — |
| 0.15 | Narrow pair, 1024 | 43.542% | 0.000719% | 1.584 |
| 0.15 | Wide pair, 1024 | 43.464% | 0.01205% | 1.450 |
| 0.30 | Static, 1024 | 13.704% | roundoff | — |
| 0.30 | Narrow pair, 1024 | 13.704% | 0.000159% | 0.504 |
| 0.30 | Wide pair, 1024 | 13.606% | 0.002587% | 0.158 |
| 0.15 | Wide pair, refined | 43.444% | 0.01081% | 1.177 |
| 0.30 | Wide pair, refined | 13.606% | 0.002553% | 0.180 |

Angular-momentum exchange is concentrated in part of the population; medians do not describe the largest responders. The refined 90th-percentile changes are 0.538% and 0.0775%, respectively. The two refined final cumulative profiles remain separated by 37.061% of supplied mass at their most different scored radius. Their mass fractions inside the target radius remain 96.729% and 87.891%.

For the denser refined halo, the driver gives away about 118% of its nominal orbital angular momentum while being held at unchanged pattern speed and radius. That is not possible for this isolated rigid pair without replenishment. A live baryonic component must slow, deform, exchange with other components, or be fed. This is a limitation of the imposed history, not an exclusion of all bars. The other refined case demands 18%, still enough that backreaction merits calculation.

## What has and has not been resolved

Breaking spherical symmetry permits torque, and the torque/work identity is numerically satisfied. But those facts do not imply target-profile selection. The tested driver transfers angular momentum without erasing the large difference between two initial equilibria. In one regime its prescribed persistence also exceeds its own nominal reservoir.

The live missing implication remains: physically generated assembly and transport must select the target profile and acceleration normalization across galaxies. Neither a heat source, ordinary gas cycles, nor this rotating source has established that implication. All of these can modify cold-matter orbits; none of the tested mechanisms derives the vacuum-linked a0 or kappa=1/2.

Do not label the carrier theory solved. Further work needs a specified live baryon/accretion model and initial conditions, or a different derived interaction. Simply increasing an externally maintained torque until a target looks better would add unbudgeted energy/angular momentum and fit the answer by construction. This route remains open for live backreaction and nonspherical self-gravity, but those unperformed calculations must not be counted as evidence.

## Reproducibility

torque_halo.py, torque_halo_contract.json and torque_halo_run/ record the source, declared inputs, profiles, work, angular-momentum demand and validated manifest. Target errors concern 0.03–1 target radii. The numerical evidence is finite and model-dependent; no new observational support is claimed.
