# BH1_cluster_bh_coupling: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** SH1's only full pass needs cluster and group cores softened, about R 0.685 (0.817 is a knife edge). CL4 says only
the black hole has the energy. Can a black hole's energy, moving gas and acting through gravity alone, soften a formed cusp
that far? Same gravity-only channel as CM1–CM3, at ceiling inputs: a miss at the ceiling closes this channel; a reach
does not establish it.

**Haloes.** M200 10¹⁴ and 10¹³. Cold NFW at the c giving CE1's η 16.91 and 17.67 (X81 estimator, x_c 0.001). R200 and the time
unit scale from CM1's halo at fixed mean density. Isotropic Eddington ICs in the total potential, N 200 000, seed 1,
CM1's integrator, dt 0.5 Myr, 10 Gyr, static η as reference, measured at each halo's 500th-particle radius.

**Baryons (round values from memory, PROVISIONAL, all chosen as ceilings).**
- M_gas 0.10 M200 (CL4), Hernquist a_g = 0.2 R200.
- Stars M★ = f★ M_gas with f★ 0.0615 (CL4's definition, the higher measured value), all in one central Hernquist a_s = 0.015 R200.
- E_BH = 0.1 × 0.005 M★ c² (CL4).

**Geometries.**
- **G1 (gas-rich central past):** closed box. Burst k moves gas from a_s to 8 a_s, from a pool M★(1 − k/N), like CM2. Stars are
  M★ minus the moved gas during the burst.
- **G2 (hot core):** burst moves gas from a_g to 8 a_g, from the pool M_gas.

**Energy cap.** Each burst's moved mass is the largest with lift energy ≤ ε E_BH / N (potential: stars, other gas, NFW, self). ε = 1.
Ramp out 5 Myr, back 200 Myr, as in CM1.

**Grid.** Each mass × G1, G2 × N 3, 10, 40.

**Controls.**
- STATIC per mass.
- UNCAPPED: G2, N 10, all gas moved, no energy cap (channel sensitivity; energy used reported against E_BH).
- MUTATE: G2, N 3, ε 0.01.

**Targets.** R = η/η_STATIC at 10 Gyr. CLEAN R ≤ 0.685 (SH1's pass). LIMIT R ≤ 14.3/η (0.846 at 10¹⁴, 0.809 at 10¹³).

**Verdict (best capped cell per mass).**
- **REACHES CLEAN AT CEILING:** both masses R ≤ 0.685.
- **REACHES LIMIT AT CEILING:** both masses at or under LIMIT, not both CLEAN.
- **NOT REACHED AT CEILING:** either mass misses LIMIT. Add whether UNCAPPED reaches, so a miss is labelled energy-limited
  (UNCAPPED reaches) or channel-limited (it does not).
- **NOT DECIDED:** any check fails.

**Checks.**
- **K1:** CM1's setup, ICs and schedule through this code reproduce CM2 K1's η at 1250 Myr to 1e-6 relative.
- **K2:** work balance |E − E0 − W|/|E0| < 0.01, every run.
- **K3:** energy used ≤ ε E_BH, moved mass ≤ pool, every capped run.
- **K4:** STATIC η drift within 3 %.
- **K5:** particle η at t = 0 within 5 % of analytic at the same x_c.
- **MUTATE:** |1 − R| smaller than at ε 1 (same mass, G2, N 3), unless ε 1 moved it by < 0.03, then NOT INFORMATIVE.

**Limits stated up front.** One spherical halo per mass, no mergers, no substructure, no satellite stars; gas is prescribed, not
hydrodynamic. Cluster η is ng 48 until A4. Only gravity reaches the cold component. A reach would not derive N, ε or geometry.

κ = ½ FITTED. Canonical and alt share these dynamics, which do not depend on the footing; the floor enters only in the grader.
Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating field component,
never a particle.
