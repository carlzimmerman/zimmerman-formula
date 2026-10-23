# Slow baryonic growth assembles a specified cold seed without friction

The first successful live cold-shell experiment follows a prescribed baryonic amplitude from beta=.1 to1. Increasing the quintic ramp duration from100 to400 reduces final excitation energy by approximately264 at both tested resolutions. For duration400 the final mass-weighted position error relative to the discrete target equilibrium is.16–.19%. No friction, thermostat or particle removal is introduced.

This is conditional assembly from a prepared cold equilibrium in a nonzero baryonic seed. It is not primordial cold-population formation, a unique attractor, or a full dynamical parent.

## Model and checks

COLD_SHELL_DISCRETIZATION.md derives the discrete Hamiltonian, pressure force and external-work balance. Use unit cold mass, gamma=.01, Plummer scale1 and zero shell angular momenta. Before each evolution solve an equilibrium of the same discrete force at beta=.1 and at beta1. Stationary force residuals are below2.6e-11. A directional energy finite difference checks the force, with relative discrepancy below5.7e-6.

The imposed history is beta(t)=.1+.9(10s³-15s⁴+6s⁵), s=t/T. The baryonic source supplies work through its time-dependent potential. Velocity Verlet evolves ordered shells, and an independently accumulated work integral checks H(T)-H(0). Runs terminate at the end of the ramp; no later settling is inferred.

| shells | step | T | remaining excitation energy | relative position RMS | energy-minus-work residual |
|---|---:|---:|---:|---:|---:|
|64|.0005|100|.00404046|.04566|-3.82e-8|
|128|.00025|100|.00408102|.03687|-4.13e-7|
|64|.0005|400|1.53454e-5|.001856|-4.11e-13|
|128|.00025|400|1.53112e-5|.001642|-1.05e-13|

Excitation energy is final discrete H minus the stationary discrete H at beta1, with the same mass. Position RMS is weighted by the nodal kinetic masses and normalized by the equilibrium's weighted squared radius. The slower runs retain mostly kinetic excitation at the endpoint, so the small position error alone would understate the remaining motion. These are dimensional-model units, not physical cosmic times or observational acceleration errors.

Duration400 excitation differs by about.22% between the two resolutions. Duration100 excites narrow shells: the minimum gaps are about4.12e-4 and1.69e-4, and outer radii differ appreciably between resolutions. Thus the faster trajectory is not established as converged even though its excitation energies are similar. The slower trajectories have minimum gaps.0162/.00817 and much better consistency. Spatial resolution and time step changed together; separate temporal refinement is still required for a controlled error estimate.

## Failures retained

The first cold_live_assembly_run failed to initialize the weak-baryon continuum background from a direct guess. The v2 script used the previously successful continuation procedure, but then failed in the T20 ramp at the shell-ordering/q-domain guard with the coarser explicit step. That exception did not distinguish shell crossing from the q limit, and the attempt did not save a trajectory; no physical-collapse conclusion follows.

The v3 experiment used four-times-smaller steps and tested T100/400, retaining the earlier scripts and failed manifests. This is a changed experimental range, not a repaired demonstration that T20 succeeds. The new results do not resolve the fast-ramp failure.

## What advances and what remains

The previously computed equilibrium sequence now has a live realization in this reduced model over beta.1–1: sufficiently slow external assembly ends near the desired cold equilibrium with small residual excitation. This avoids relying on the approximately1900-period provisional kinetic damping time, because little excitation needs to be generated in the first place. It also avoids the specific warm-to-cold angular-momentum and occupation mismatch by starting with cold material. Those are conditions on the initial state, not derived consequences.

The external baryonic history is prescribed, so reciprocal baryon dynamics and total source-plus-medium energy are not modeled. The seed is already bound and cold; beta0 has no finite isolated equilibrium under the earlier virial assumptions. This calculation does not select its mass, explain primordial occupation, test nonspherical evolution, demonstrate an observational law throughout assembly, or prove long-time stability. A cold fluid can also cease to represent collisionless matter after crossing; no crossing was encountered in the successful finite runs.

Evidence: cold_live_assembly_v3_run completed and its manifest validates. Four checks pass: force derivative, work balance, shell ordering and lower excitation for the slower ramp at each resolution. The script and exact execution contract are pinned in the manifest. The Hamiltonian derivation and interpretation are self-reviewed. No novelty claim is made.
