# BH2_central_gas_load: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** BH1 missed because central gas was limited to the closed box (0.00615 M200) and the hot gas sits outside the core; its uncapped control
covered hot gas only. CL5 capped gas at what is in place. Neither tests a central gas load beyond that. How much central gas, lifted
by the black hole's energy through gravity alone, would soften these cusps enough? This is an upper-bound test: a reach gives the load
required, it does not show such a load existed.

**Machinery.** BH1 read-only: same masses (10¹⁴, 10¹³), cold NFW at CE1's η, Eddington ICs (N 200 000, seed 1), integrator, dt 0.5 Myr, 10 Gyr, η at the
500th-particle radius, E_BH, ramps 5 Myr out and 200 Myr back. The 5 Myr ramp is kept as a ceiling; CL5 considered it unphysical in a cluster core.

**Baryons.** Stars 0.0615 × 0.10 M200 at a_s = 0.015 R200, static. Central load L at a_s. Hot gas 0.10 − L at a_g = 0.2 R200, so total gas stays 0.10 M200.

**Load.** L = 0.02, 0.05, 0.10 M200, held for all 10 Gyr. ICs are rebuilt in each load's potential with the same cold NFW, so the halo starts in equilibrium at
CE1's η with no contraction from the load. This favours softening.

**Bursts.** N = 3, 10. Each moves the largest M_f ≤ L with lift energy ≤ ε E_BH / N, from a_s to 8 a_s; the rest of the load stays. ε = 1.

**Controls.**
- STATIC: each load and mass, no bursts. R = η/η_STATIC of the same load.
- UNCAPPED: L 0.10, N 10, all moved, no energy cap.
- MUTATE: L 0.05, N 3, ε 0.01.

**Targets.** LIMIT R ≤ 0.845 at 10¹⁴, 0.809 at 10¹³ (as BH1's graded values). CLEAN R ≤ 0.685.

**Verdict.** For each mass, the smallest L with a capped cell at LIMIT and at CLEAN.
- **REACHES CLEAN AT LOAD L:** both masses, L the larger of the two.
- **REACHES LIMIT AT LOAD L:** both masses at LIMIT, not both CLEAN.
- **NOT REACHED AT ANY LOAD:** either mass misses LIMIT at every L. Labelled energy-limited if UNCAPPED reaches LIMIT at both masses, channel-limited otherwise.
- **NOT DECIDED:** any check fails.
Report for each reaching cell L in solar masses and L against the closed-box 0.00615 M200.

**Checks.**
- **K1:** the wrapper with BH1's ICs, baryons and G1 N 3 schedule reproduces BH1's 14_G1_N3 final η to 1e-6.
- **K2:** work balance < 0.01, every run.
- **K3:** energy used ≤ ε E_BH, M_f ≤ L, every capped run.
- **K4:** every STATIC drifts within 3 %.
- **K5:** particle η at t = 0 within 5 % of analytic, every load.
- **MUTATE:** |1 − R| smaller than ε 1 (same mass, L, N), unless ε 1 moved it by < 0.03, then NOT INFORMATIVE.

**Limits stated up front.** Gas is prescribed, not hydrodynamic. Inner stars and gas share one radius. Spherical, one seed, no mergers. R is measured at x_c about 0.017 R200, targets
come from x_c 0.001. Inputs PROVISIONAL. Cluster η is ng 48 until A4. Nothing is derived: not L, N, ε or geometry. Only gravity reaches the cold component.

κ = ½ FITTED. Canonical and alt share these dynamics; footings are not pooled. Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating
field component, never a particle.
