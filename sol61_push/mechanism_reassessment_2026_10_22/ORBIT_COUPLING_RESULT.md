# Frequency matches can have weak coupling in the cold branch

The sampled high-harmonic matches identified previously do not automatically provide efficient energy transfer. For the A10000 equilibrium, a normalized dilation trial potential has small third- and fourth-harmonic coupling on the orbits near the cold collective frequency. This is consistent with persistent ringing, but is not a self-consistent kinetic damping calculation.

## Trial potential and boundary choice

Use the actual infinitesimal canonical dilation of each finite-A equilibrium, xi=r. Continuity gives s=r³rho, delta m=-s, delta rho=-(3rho+r rho'). The chemical potential is an integral of R(q) plus gamma rho, so its first variation is

    delta mu(r) = -integral_r^Redge R'(q(x)) s(x)/x² dx
                  - gamma s'(r)/r².

Total mass is unchanged and the perturbation vanishes outside the finite-A support. The finite-A density vanishes sufficiently smoothly at its edge for this construction. The computation normalizes max|delta mu|=1 separately for each equilibrium, so cross-A absolute energy-transfer comparisons are not justified.

This is deliberately a dilation trial potential, not the cold-fluid eigenpotential. Directly transplanting an exactly cold eigenfunction is subtle: its Eulerian density perturbation can have a nonzero interior limit at the moving edge. Setting its chemical-potential perturbation to zero at that edge without treating the boundary displacement would alter the potential and contaminate high harmonics. The present finite-A variation avoids making that identification.

## Orbit Fourier calculation

Use the same1024 deterministic mass-sampled orbits per A as ORBIT_RESONANCE_RESULT.md. Map each half radial orbit to its elapsed-time phase. With period T and frequency Omega_r, compute

    C_n = (2/T) integral_0^(T/2) delta mu[r(t)] cos(n Omega_r t) dt.

The outward and inward halves have the same radial potential history, so this is the complex Fourier coefficient for an even radial signal; the real cosine-series amplitude is2 C_n. Compute n=1 through8, comparing1024 and2048 midpoint meshes in the regularized turning-point coordinate. The maximum absolute coefficient difference is below2.8e-7 over the tested sample.

For each n, define the exploratory proximity band |n Omega_r/.827760-1|<.05. Here .827760 is the cold-fluid reference frequency, not a finite-A kinetic eigenfrequency. Weight each orbit equally because the phase points sample the equilibrium mass distribution. The resulting sums are geometric coupling diagnostics; a linear kinetic susceptibility instead needs distribution derivatives, action-space measures and its self-consistent response denominator.

## A10000 result

| harmonic | sample in proximity band | mean C_n² within that band |
|---|---:|---:|
| 1 | 0 | not sampled |
| 2 | .195% | 2.69e-5 |
| 3 | 15.23% | 3.90e-5 |
| 4 | 13.57% | 8.71e-6 |
| 5 | 8.01% | see result JSON |
| 6 | 2.83% | see result JSON |
| 7 | .879% | see result JSON |
| 8 | 0 | not sampled |

Across the whole sample, mean C_1²=.02837. Thus the third/fourth harmonic proximity populations have much weaker coupling than the bulk first harmonic. They cannot be counted as equally effective resonances merely because their frequencies match.

Summing mass-weighted C_n² in the proximity bands gives7.3581e-6, versus .0296861 summed over all sampled orbits and harmonics1–8. Their ratio is .00024786, or .0248%. This is the fraction of this sampled, normalized, truncated harmonic power lying in the selected bands. It is NOT an absorbed-energy fraction, decay rate, cooling efficiency or probability of settling. The corresponding trial ratios for A10,100,1000 are7.58%,1.17%,1.45%; those warm comparisons use the same cold reference frequency and are not predictions for their own modes. The trend is not monotone.

## Interpretation and remaining work

The combination of colder orbital frequencies and weak high-harmonic coupling gives a concrete candidate explanation for reduced dephasing of the cold dilation response. It supports investigating a self-consistent kinetic response calculation rather than assuming all frequency matches damp efficiently. Rare orbits, narrower resonance surfaces, the actual mode shape and derivative weighting may materially change the result. No resonance exclusion or damping bound has been proved.

A derived coupling to another sector remains a possible route, but its energy source, conservation laws, static backreaction and parent action must be supplied. The existing independent-field radiation calculation is not already that coupling for the identified medium. This work identifies an obstacle and a sharper test; it does not deliver the requested formation mechanism or establish novelty.

## Evidence

The bounded orbit_coupling_run completes with five passing checks and a valid manifest. A centered finite dilation independently verifies the analytic potential variation; maximum normalized discrepancy across the four equilibria is 2.98e-09. Orbit periods, turning points, mass and Fourier refinement also pass their stated numerical gates. The evidence supports the finite sampled diagnostic only. Interpretation is self-reviewed.
