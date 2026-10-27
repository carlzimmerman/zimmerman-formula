# Moving-carrier collision width in the half-density reservoir

2026-10-13. A Born scattering calculation tests whether the ideal reservoir itself smears the proposed source threshold. It finds small collision widths in the specified range. This is a conditional consistency check, not a full spectral-function calculation or proof of manufacture.

## Model and observable

Use the previous half-density source window: m=1 MeV, neutral atom mass M_A=10510986.005756367 eV, n_A=5e24 m^-3, messenger mass M_S=10 MeV, h=1, and contact g=h/(4mM_S). The two-spin, noninteracting, unpaired atom gas has E_F=5.183544402e-4 eV. Products at the stipulated source pole have kinetic energy K=3.956180382e-11 eV each; pair excess D=2K=7.912360764e-11 eV.

We compute the scattering-out rate of a dilute moving carrier at that K, including bath emission and absorption. With natural units and v=sqrt(2K/m),

    omega = v q cos(theta) - q^2/(2m),
    Gamma_E = g^2/(2pi) integral_0^infinity q^2 dq
              integral_-1^1 dcos(theta) S(q,omega).

S is the number-density structure factor defined and derived in ../finite_temperature_kicks_2026_10_13/REPORT.md, including two bath spin states and delta(omega-energy). Its finite-T occupation formula, detailed balance and zero-transfer limit are implemented without subtracting nearly equal large logarithms. The chemical potential is solved at fixed density for each temperature.

Gamma_E has energy units. The corresponding collision rate is Gamma_E/hbar. In a weak-coupling quasiparticle approximation, the retarded amplitude has a damping term -i Gamma_E/2, giving an energy FWHM Gamma_E. We report 2 Gamma_E as an *independent-particle estimate* for the pair width. Correlated pair response, vertex corrections, collective modes, pure dephasing outside this approximation and the R propagator are not calculated. A collision rate is not automatically an exact experimentally observed line shape.

At T=0 and small momentum transfer within the bath's occupied phase space, angular integration gives

    S(q,omega)=M_A^2 omega/(2pi^2 q) for omega>0,
    Gamma_E = g^2 M_A^2 m^3 v^4/(30pi^3)
            = 2g^2 M_A^2 m K^2/(15pi^3).

An independent occupied/unoccupied Fermi-annulus integral verifies this limit. Combined with the previous T=0 energy-loss power, the mean loss per scattering event in this regime is 4K/7. This is a scattering-weighted mean, not a deterministic energy decrement.

For a resting carrier in the degenerate small-q finite-T limit,

    Gamma_E(K=0) = g^2 M_A^2 m T^2/(12pi).

This supplies another analytic normalization control. The physical rows below use the full finite-temperature response and nonzero K, not the resting formula.

## Numerical result

| Temperature | Collision rate (1/s) | Single-carrier width (eV) | Independent pair width / D |
|---|---:|---:|---:|
| 0, low-q limit | 7.061e-16 | 4.647e-31 | 1.175e-20 |
| 0.1160 microkelvin | 1.197e-15 | 7.877e-31 | 1.991e-20 |
| 11.60 microkelvin | 2.828e-12 | 1.861e-27 | 4.705e-17 |
| 1.160 millikelvin | 2.783e-8 | 1.832e-23 | 4.631e-13 |
| 0.1160 kelvin | 2.783e-4 | 1.832e-19 | 4.630e-9 |
| 1.160 kelvin | 1.914e-2 | 1.260e-17 | 3.185e-7 |

At the warmest tested temperature, the independent pair-width estimate is 1.260e-5 of the original vacuum total source linewidth 2e-12 eV. This reference linewidth is not silently re-used as the actual in-medium source width: phase space already changes its daughter width, and the source's medium self-energy is still missing.

The small Born parameter k_F a=3.793e-7, where a=g m_reduced/(2pi), supports perturbative impurity scattering in this stipulated bath. It does not validate the hypothetical atoms, their phase, a full ultraviolet theory, or all medium corrections. The computed Gamma_E/T is at most 1.26e-13 in the tested finite-T rows.

## Research consequence

This bath-collision channel alone does not erase the half-density sharp-threshold creation window. Weak scattering can coexist with the positive coherent mean potential. It also means collisions are inefficient as a rapid cooling mechanism. At the warm end, rare individual collisions can still put particles over a shallow wall even though their contribution to spectral broadening is tiny. Spectral resolution and long-term confinement are different requirements.

The missing real energy shifts must now be checked consistently, especially the source R's coupling to the same messenger medium. A static density susceptibility must not be substituted without justification for the response at a MeV-frequency source pole. The present result does not freeze those shifts by physical argument; it isolates one imaginary contribution only. It also excludes reciprocal carrier annihilation, finite-cavity leakage, actual source bandwidth and density noise.

## Verification and reproduction

Nineteen checks pass: two direct zero-T annulus controls, two resting thermal normalization controls, five fixed-density constraints, five 64-to-128 point angular/radial refinements and five thermal-cutoff comparisons. With u=q/sqrt(2mT), a=sqrt(K/T), integration ends at u=a+sqrt(a^2+cut), for cut=80 or 100. Beyond this boundary every allowed bath energy loss exceeds cut*T and the ideal response is thermally suppressed. Cutoff agreement is numerical convergence evidence, not an interval-certified error bound for all inputs.

The runner manifest validates against source/output hashes; stderr is empty. No new Lean theorem is claimed for this integral or the physical linewidth interpretation. The previously compiled source/bath algebra remains separate evidence. The model has no experimental validation.

Reproduce with:

    python3 sol61_push/carrier_collision_width_2026_10_13/check.py /tmp/carrier_collision_width_results.json

The bounded runner command and software versions are recorded in run/manifest.json and contract.json. Definitions and prior evidence are in ../neutral_reservoir_statistics_2026_10_13/REPORT.md, ../finite_temperature_kicks_2026_10_13/REPORT.md and ../source_bath_compatibility_2026_10_13/REPORT.md.
