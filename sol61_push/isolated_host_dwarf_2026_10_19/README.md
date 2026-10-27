# Matched isolated and host dwarf experiment

Experiment authorized 19 October 2026; results recorded 20 October UTC.

**A diffuse cold cloud assembles a persistent, locally self-bound central concentration in isolation in the specified carrier equations. A resolved, approximately constant-density core is not established.** The isolated collisionless control assembles almost the same mass inside 300 pc, identifying ordinary gravitational collapse and redistribution as the dominant mechanism in this prepared example. A strong host tide leaves a smaller bound remnant and extensive tails. The host remnant's precise mass fails the declared numerical stability criterion.

This is a finite experiment in the original dilute daughter-carrier Newtonian kinetic reduction. It does not solve the full canonical polarization framework or derive the initial cold abundance and velocities from source production or cosmology.

## Equations actually evolved

The source is [MASTER_COLD_ENERGY_EQUATIONS.md](../cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md), equations at lines 183–195 and the elastic operator at lines 493–511:

\[
\partial_t f+\mathbf v\cdot\nabla_xf-\nabla\Phi_N\cdot\nabla_vf=C_{22}[f],
\qquad \nabla^2\Phi_N=4\pi G(\rho_\star+\rho_c).
\]

Stars evolve collisionlessly in the same gravity. Cold particles undergo elastic, isotropic contact scattering with the revised branch's threshold cross section \(\sigma_0/m=0.3\,\mathrm{cm^2/g}\), \(u_*=0.02\), and \(r_\lambda=2\). The implemented velocity dependence is

\[
\frac{\sigma(v)}m=\frac{\sigma_0}m
\frac{\left[(2-z/(1-z))/2\right]^2}{1+u_*^2z},
\qquad z=\left(\frac{v_{\rm rel}}{2u_*c}\right)^2.
\]

The driver rejects sampled pairs outside the declared below-resonance range. Sampled dwarf velocities remain far below resonance. [source_inputs.json](source_inputs.json) records source hashes and constants; [CONTRACT.md](CONTRACT.md) freezes the physical inputs and decision criteria.

Mutual gravity uses the softened pair potential \(-Gm_im_j/\sqrt{r_{ij}^2+\epsilon^2}\). The host adds the static Plummer potential \(-GM_h/\sqrt{r^2+b^2}\). The finite-support Monte Carlo collision method uses central impulses with incoming-angle weighting; it conserves each realized pair's energy, momentum and vector angular momentum and reproduces the isotropic contact distribution in a locally uniform limit. Finite support remains an approximation and is checked explicitly.

There is no profile target, imposed cold core, cooling drag, thermostat, reflecting boundary or particle deletion. No X sources are initially present. No polarization force or galaxy-law fit enters the dynamics. The energy-deficit drift used in CFG541 and the shell/profile constructions in other repository branches are excluded.

## The same prepared dwarf in two environments

The stellar mass is 574,273 solar masses. The assumed cold inventory is 53.64 times that mass, or 30.804 million solar masses. Initially the cold component fills a uniform ellipsoid with semiaxes 2,000, 1,600 and 1,200 pc. It has virial ratio \(2K/|W_{\rm vir}|=0.2\), with 10% of kinetic energy in ordered rotation about a tilted axis. Live stars start in a Plummer distribution of scale 193.22 pc with virial ratio 1.

These prepared, subvirial cold velocities favor collapse. The stellar distribution is already centrally concentrated; the cold distribution is diffuse. This tests whether a cold concentration can assemble dynamically for these inputs, rather than whether the theory selects them or predicts an observed dwarf.

The host has real mass \(6\times10^{11}\) solar masses and scale 10 kpc. The dwarf starts at 80 kpc with tangential speed 0.65 times the circular speed. Each isolated/host pair has exactly the same relative initial particle positions, velocities, masses and labels; only bulk translation and orbital velocity differ. The first orbital passage is near 24 kpc.

All runs evolve for 10 Gyr. The baseline has 2,048 cold and 256 stellar particles, gravitational softening 40 pc, collision support 200 pc, and leapfrog steps of 2 Myr in isolation and 0.5 Myr around the host. Controls disable collisions, halve the timestep, double particle count, or halve collision support. An additional isolated run halves softening at the already halved timestep. Doubling particle count samples the same initial distribution but changes the finite realization; it is not a nested sample or continuum proof.

## Formation, stripping and resolution

The initial cold mass inside 300 pc is only 0.211 million solar masses, with no cold particles inside 100 pc about the initial stellar centre. At 200 Myr the corrected isolated history already has 47.51% of its cold stock inside 300 pc after just **one** elastic collision. This timing, together with the collisionless control, identifies collapse and violent relaxation as the dominant early process.

Final masses below use independently located minima of the dwarf's self-potential, excluding the host potential. Units are million solar masses. These are aperture masses; locally self-bound aperture masses are also provided in the recorded JSON. Diagnostic replays have exactly the baseline particle states and are not additional independent physical realizations.

| Run | Isolated M100 | Isolated M300 | Host M100 | Host M300 |
|---|---:|---:|---:|---:|
| Baseline | 1.399 | 10.965 | 0.346 | 2.437 |
| Elastic collisions disabled | 1.745 | 10.995 | 0.797 | 3.384 |
| Half timestep | 1.670 | 11.236 | 0.496 | 3.444 |
| Double particle count | 1.782 | 11.461 | 0.677 | 4.979 |
| Collision support 100 pc | 1.895 | 11.311 | 0.842 | 3.264 |
| Softening 20 pc, half timestep | 2.422 | 11.446 | — | — |

The isolated baseline's mass inside 300 pc stays near 11.17 million solar masses over the final Gyr. Its final aperture contains 729 cold and 114 stellar particles. The host baseline retains 162 cold and 12 stellar particles inside 300 pc; all of that aperture's cold material passes the local instantaneous self-unbinding diagnostic. Its corrected final-Gyr mean is 2.60 million solar masses. Both environments first assemble a concentration; repeated host passages strip the satellite afterward.

For isolation, the final 300-pc mass changes by 2.47% on halving the timestep, 4.53% on doubling particle count, and 3.16% on halving collision support. The collisionless value differs by 0.27%. At matched timestep, halving gravitational softening changes the 300-pc mass by 1.87%, but the 100-pc mass by **45.05%**. Particle count and collision support also change the 100-pc mass by 27% and 35%. The inner density profile and a flat-density core radius are therefore unresolved. The collision count itself rises 38% when the isolated collision support is halved, so transport-rate convergence is also unproved.

For the host, halving timestep changes the 300-pc mass by **41.36%**, halving collision support by **33.95%**, and doubling particle count by **104.32%**. All exceed the contract's 20% stability gate. The sampled host masses span 2.44–4.98 million solar masses, versus 10.96–11.46 million in isolation. Even the endpoint classification relative to a 10%-of-stock threshold changes between these runs; no converged host core/no-core threshold classification is justified. In the doubled-particle pair, the host retains 43.44% of the isolated 300-pc mass. The broad loss of central material relative to the matched isolated dwarf is the supported trend; its amplitude is not converged. The particle-count comparison also changes the finite initial realization, so sampling, gravitational discreteness, stochastic scattering and chaotic orbital evolution are mixed in that sensitivity.

A separate [exact finite geometric check](GEOMETRIC_BOUND.md) proves that **any** 300-pc sphere in the saved baseline host endpoint contains at most 192 cold particles, 9.375% of the original stock. This centre-independent statement concerns that saved coordinate set only. It is compatible with the smaller bound remnant and does not remove the host's numerical sensitivity.

## Where energy and angular momentum go

All original particles are retained in the accounts, including distant tails. Energy is \(E=K+U_{\rm self}+U_{\rm host}\); internal and orbital terms use the centre of mass of all original dwarf particles. Each subgroup receives half of its cross-potential energy. All three angular momentum components are recorded. Host work and torque are accumulated separately at every leapfrog kick.

The table follows fixed particle membership: the cold particles that end inside the remnant's 300-pc aperture, all other cold particles, and stars. Thus entry or exit through an aperture is not mislabeled as energy loss. “Internal exchange” means the subgroup's energy change minus its accumulated host work. Energy units below are \(10^8\,M_\odot\,\mathrm{pc^2/Myr^2}\).

| Environment and recipient | Internal energy exchange | Host work |
|---|---:|---:|
| Isolated final central cohort | −4.548 | 0 |
| Isolated other cold material | +4.544 | 0 |
| Isolated stars | +0.023 | 0 |
| Host final remnant cohort | −4.163 | +354.893 |
| Host other cold / tails | +4.969 | +6,498.067 |
| Host stars | −0.806 | +148.177 |

In isolation, almost all energy released by the central cohort appears in the outer cold material. The small stellar energy term is comparable to the total numerical energy drift and should not be interpreted precisely. There is no radiative or inelastic loss in this model.

The collapsing isolated cohort contracts from an own-centre-of-mass rms size of 1,145 pc to 197 pc. In the table's energy units, its own-frame kinetic energy rises from 0.4575 to 8.1162 while its cold-only self-energy becomes more negative, from −1.7788 to −4.2259. The concentration therefore forms through gravitational binding and energy redistribution while its internal kinetic energy increases. This measure includes rotation, streaming and shear; it is not a measurement of thermal heating after subtracting local mean flows.

The isolated central cohort's vector angular momentum changes by \((-2.655,-1.542,-4.908)\times10^9\,M_\odot\,\mathrm{pc^2/Myr}\). Other cold material receives \((+2.540,+1.376,+4.892)\times10^9\); stars receive \((+0.115,+0.165,+0.015)\times10^9\). The cohort loses about 81% of the magnitude of its angular momentum about the original dwarf's centre of mass. Its own intrinsic spin magnitude falls from 7.096 to 0.991 in the same \(10^9\) angular momentum units (86%); the host remnant cohort's intrinsic magnitude falls from 1.194 to 0.261 (78%). These own-frame spins are recorded separately from the global subgroup accounts.

Around the host, tidal work and torque transfer between internal and orbital motion; tails carry large shares. The host's central force exerts zero torque about the host origin, so the change of total dwarf internal angular momentum is balanced by orbital angular momentum. The large host-cohort entries include the remnant's bulk motion relative to the centre of mass of the stripped original cloud. They are not measurements of the remnant's intrinsic spin or heat deposited in a live host. The analytic host has no evolved response.

The final analysis also selects each environment's final central cohort and follows those **same particle identities through both environments**, with full vector transfers and host receipts in [same_material_transfer.json](analysis_run_001/same_material_transfer.json) and [CSV](analysis_run_001/same_material_transfer.csv). Of the 10.965 million solar masses ending in the isolated 300-pc aperture, only 1.489 million lies inside the host remnant's 300-pc aperture in the paired baseline run; that same cohort's median host-remnant radius is 50.75 kpc. The host's final central cohort overlaps, but is not identical to, the isolated one.

## Checks, diagnostic repair and interpretation

The original shrinking stellar centre becomes unreliable when most stars are stripped. It incorrectly reported zero late baseline host mass inside 300 pc. A postprocessing search using cold and stellar density seeds and the dwarf's self-potential finds the surviving remnant. A diagnostic replay changes only centring and data recording: both isolated and host initial and final particle positions, velocities, masses and labels are **bitwise identical** to their original evolution. The replay supplies the corrected baseline histories and per-particle host receipts.

The remnant centre is the deepest local potential minimum found by a finite seed search, not a certified global optimizer. Boundness means iterative instantaneous self-unbinding inside a stated 1-kpc cut, not a proof of future survival in a tidal field. Varying the baseline host cut from 0.5 to 2 kpc leaves the bound central 300-pc result unchanged. Legacy host-centred temporal means for unreplayed controls are retained as original diagnostics and are not used as remnant masses.

Fourteen focused tests pass, checking gravity against an independent implementation, force/potential consistency, Galilean invariance, central torque, collision conservation and angular sampling, same-dwarf initial conditions, and remnant recovery despite tails. All **115** final output checks pass across 11 physical runs and two diagnostic replays: no particle or mass deletion, finite phase space, energy error below 1% of the initial **internal dwarf binding** rather than the much larger orbital binding, vector angular momentum closure, subgroup partition closure, paired initial-state identity, and replay bitwise identity. All 13 evolution manifests, the final analysis manifest and the successful geometric-check manifest validate against their recorded input/output hashes. The five source hashes in source_inputs.json also match the current source bytes.

The baseline maximum total energy errors are 0.588% in isolation and 0.707% around the host, measured over every integration step. Halving timestep lowers these to about 0.133% and 0.177%, respectively. Passing conservation does not imply a converged host remnant mass or inner density profile. All runs have finite particle noise, gravitational relaxation, softening and collision support; this is one assembly history and orbit.

The stronger stripping of stars also means that reduced absolute cold mass does not automatically imply a reduced observed mass discrepancy. No stellar kinematic inference, Draco fit, isolated-dwarf population comparison or “20 dwarfs would decide it” sample-size calculation was performed here.

## Data and reproduction

The primary record is [analysis_run_001/manifest.json](analysis_run_001/manifest.json), with completed status, frozen analysis inputs and output hashes. It records:

- [analysis.json](analysis_run_001/analysis.json): remnant diagnostics, own-frame spin/energy, numerical comparisons and original bookkeeping.
- [comparison.csv](analysis_run_001/comparison.csv): every completed case's endpoint masses, particle counts and energy error.
- [audit.json](analysis_run_001/audit.json): all 115 finite checks and replay identity results.
- [same-material transfers](analysis_run_001/same_material_transfer.csv): fixed cohort transfers across environments.
- [Standalone comparison figure](analysis_run_001/isolated_host_comparison.png): corrected baseline histories and profiles, energy recipients and angular momentum transfers. The host curve is a representative baseline realization, not a converged remnant-mass prediction. The dotted isolated collisionless curve uses the original stellar centre; endpoint comparisons in the table use the remnant diagnostic consistently.

The final figure was visually inspected. Working previews and legacy root-level summaries are superseded by analysis_run_001. The finite geometric certificate is [geometric_run_001/retry_cpu_bounded/result.json](geometric_run_001/retry_cpu_bounded/result.json), with its [validated manifest](geometric_run_001/retry_cpu_bounded/manifest.json).

The evolution is in [run_dwarf.py](run_dwarf.py), [dynamics.py](dynamics.py) and [direct_gravity.c](direct_gravity.c). The diagnostic-only replay is [run_dwarf_remnant.py](run_dwarf_remnant.py), with [remnant.py](remnant.py). Contracts and per-run manifests record source hashes, commands, initial/final arrays, numerical versions, runtime and declared resource limits. Initial coarse timing pilots are retained but excluded from scientific conclusions. The geometric check's failed macOS address-space-limit launch is also retained; its explicitly linked retry is the successful evidence.

From this directory, the original launches were:

```bash
cc -O3 -dynamiclib direct_gravity.c -o direct_gravity.dylib
/usr/bin/python3 -m unittest discover -v
/usr/bin/python3 launch.py base_iso base_host nocoll_iso nocoll_host dt_iso dt_host n_iso n_host h_iso h_host
/usr/bin/python3 launch_extra.py eps_iso
/usr/bin/python3 launch_replay.py iso host
/usr/bin/python3 finalize.py
```

Launchers require new output directories and intentionally refuse to overwrite their recorded runs. For an independent rerun, copy the source files, CONTRACT.md, source_inputs.json and DIAGNOSTIC_REFINEMENT.md into a new sibling experiment directory, excluding generated `run_*`, `analysis_run_*`, and `contracts` directories. Keep the case names and rebuild there before executing the listed commands; preserve the original evidence. Rebuilding a compiled library may change its hash even with unchanged source, which the new run must record. The final standalone postprocessing can be reproduced into a fresh directory with `/usr/bin/python3 audit_outputs.py --output NEW_DIRECTORY`. Manifest validation uses the computation-audit skill's `scripts/validate_manifest.py` with this repository supplied as `--root`.
