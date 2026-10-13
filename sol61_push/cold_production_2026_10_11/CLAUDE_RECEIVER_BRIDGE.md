# Review of current Claude/framework work and a receiver cross-check

2026-10-11. Read-only review of current committed framework outputs; no
concurrent research lane or running simulation was modified or messaged.
The recent repository history was inspected through 79e803632. The separate
chat "Analyze recent formula work" was also read for context; its current
wait on native simulation output is not a blocker for the calculation here.

## Current target changed: retain the kernel distinction

[CFG626](../../campaign_fresh_gravity/CFG626_kernel_recheck_anisotropic_target/README.md)
reruns the velocity-target work with repaired nu_mono. The compact/cluster
hollow and strong tangential anisotropy of the exponential kernel disappear;
its finite local isotropic-support tests pass. This removes that particular
obstruction from the current target. It does not prove an isotropic global
formation attractor, energy reachability, or an interaction-derived target.
Prior results in this folder about the *exact exponential kernel* remain
scoped to that kernel and must not be transferred to nu_mono.

The current framework explicitly treats kappa=1/2 as fitted. That is a
legitimate declared input for a conditional carrier construction; it is
not evidence that the microscopic action derives the coefficient. The two
numerical footings are kept separate below. This cross-check does not
require resolving kappa before testing energy exchange.

## The new energy requirement is signed

The neighboring analytic work supplies an unusually useful constraint:
[collective_energy_lower](../collective_energy_lower_2026_10_11/RESULT.txt)
requires energy import of 0.496-0.638 M_target V_f^2 for its cold IC-C states;
[collective_energy_gate](../collective_energy_gate_2026_10_11/RESULT.txt)
requires export for IC-B. These are fixed-potential, fixed-retained-mass
benchmark statements, not measurements or universal cosmological initial
conditions. A purely conservative closed *orbital* system or a one-way
receiver cannot reach both prescribed endpoints.

[regular_receiver_lift](../regular_receiver_lift_2026_10_11/RESULT.txt) makes
signed exchange regular, while [receiver_capacity](../receiver_capacity_2026_10_11/RESULT.txt)
shows that regularity alone does not supply available energy. A constant
vacuum offset cannot act as that supply. These are neighboring Codex
analytic results connecting to Claude's benchmark; they are not attributed
to Claude as original calculations.

## Cross-check: can our source mass gap be the receiver?

For the current detuned carrier, chi conversion releases rest energy
(M-2m)c^2 per source. If f_s is the initial source rest-mass fraction,
its maximum releasable gap energy per total mass is

    f_s eta c^2, eta=1-2m/M=4.999625e-5.

For required import h M_target V_f^2, a necessary capacity condition is

    f_s >= h V_f^2/(eta c^2).

This is a capacity test only. It assumes all released energy can be
retained in the target orbital component and neglects the O(eta) distinction
between source mass and charge fractions.

| Cell | Required source mass fraction | Conservative maximum target bound speed, km/s |
| --- | ---: | ---: |
| MW canonical | 0.0030221 | 524.3 |
| MW alternative | 0.0033154 | 546.9 |
| Cluster canonical | 0.1938146 | 6985.1 |
| Cluster alternative | 0.2130665 | 7324.0 |
| Compact canonical | 0.0039919 | 632.0 |
| Compact alternative | 0.0043842 | 660.4 |

The saved homogeneous Gaussian endpoint has source charge fraction
1.80684e-7, far below these requirements. That endpoint is not a predicted
halo abundance: later moving-source conversion and the entire formation
history remain unresolved. It cannot be used as evidence for a populated
halo receiver.

There is a more direct kinematic issue. Source decay at rest emits daughters
at 2997.775 km/s. To bound all target-orbit speeds, use the inherited
potential drop DeltaPhi and outer apocentre condition at R:

    E <= Phi(R)+j^2/(2R^2), j^2<=R^3 g(R),
    v^2(r)<=2[Phi(R)-Phi(r)]+R g(R).

The script conservatively replaces Rg(R) by total baryon mass plus retained
cold mass in the benchmark G=R=1 units; gravitational softening only lowers
this term. The resulting ceilings appear above. They exclude retention of
both free daughters from a rest decay in the MW and compact target
potentials. Inverse on-shell formation from two target-bound daughters is
likewise unavailable there at this mass gap. The cluster screen does not
exclude these processes; it does not establish their rate or retention.

This is not a no-go with rescattering, a time-dependent potential, nonlocal
energy transport or different source states. Those could redistribute the
large kick, but require an actual calculation. It rules out treating the
current large-gap channel as an already-established local, bidirectional
heat receiver in all six cells.

`receiver_bridge.py` reads the six current benchmark cells and energy bounds.
All six capacity-inversion checks pass; the run manifest validates current
inputs. Those checks audit arithmetic, not the inherited benchmark physics.

## Direction that survives this review

Use nu_mono when testing the current target. Keep the protected quantum
carrier as a conditional mass/stress construction, and derive signed heat
exchange from represented kinetic modes or a receiver with a justified
spectrum, state and capacity. Do not equate the cold-energy quantum number
with an independently identified dark-matter species; this is a candidate
field description, not a discovery of matter content.

An unresolved but concrete question is whether the unsettled/outer carrier
can supply and absorb the measured energy while conserving the energy of
the combined system. That would change the *closed target subsystem*
assumption of the benchmark, and must explicitly track boundary energy
flux and mass. It must not simply relax toward a fitted temperature.
The kernel, source abundance, transfer rate, halo formation and native-data
checks remain separate obligations; none is certified by a capacity number.
