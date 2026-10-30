# CM3_cadence_coupling_map: reaches only at coupling 1; at 30% it misses at every cadence. ROBUST at the ceiling.

Criteria: `FROZEN_CRITERIA.md` (80128789c6), committed before any script or number. R at 10 Gyr, needed ≤ 0.817.

| bursts | ε_c 1 | ε_c 0.3 | ε_c 0.1 |
|---|---|---|---|
| 10 (1 Gyr) | 0.573 reaches (CM2) | 0.894 misses | 0.974 misses |
| 20 (500 Myr) | 0.685 reaches | 0.956 misses | not run |
| 40 (250 Myr) | 0.898 misses (CM2) | not run | not run |

Robustness at 10 bursts, ε_c 1, each against its own STATIC: seed 2 0.579, M_b/M200 0.0675 0.615, M_b/M200 0.0858 0.565: **ROBUST**.
K1 (ICs identical), K2 (≤ 1.6e-5), K3, monotonic MUTATE pass.

## Reading
- The bursty result is not a one-seed accident, and it holds across the sample's 16–84% baryon fraction.
- It needs most of the supernova energy to go into lifting gas. The map has no cell reaching at 30%. The threshold lies
  between 30% and 100% and is not located here; the reaching runs used 60% (10 bursts) and 90% (20 bursts) of E_SN.
- So supernova-driven outflows work by gravity alone only at high coupling, large moved mass and low cadence. None of the
  three is derived. They remain undetermined inputs.

**Limits.** Prescribed histories at ceilings (all gas starting at the stellar scale). Only the median halo mass and the
median gas share were used. Halo formed at t = 0, spherical. Softened halos were not put through the full route E grader.
Clusters are not covered (CL4). κ = ½ FITTED. Not theory closed. Cold dark energy is a gravitating field component, never
a particle.
