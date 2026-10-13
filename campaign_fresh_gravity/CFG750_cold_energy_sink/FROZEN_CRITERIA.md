# CFG750 — is the central black hole a cold-energy drain? (frozen criteria, committed alone)

Block CFG750–759 (reserved 2026-10-13). Written before any CFG750 script or number. κ = ½ fitted; the cold energy's mass is
required; no particle species; not theory closed. **A hypothesis test. No black-hole data are used to set anything.**

## Hypothesis (named before scoring)
- CFG749: cold energy is bound only by the baryons, so cold energy carrying real orbital motion leaves.
- Cold energy arriving with near-zero angular momentum plunges to the centre, where a black hole can absorb it permanently.
  It then becomes Newtonian mass that the law counts.
- CFG747: the cold-energy profile is an attractor, so a drained centre is refilled.

**Question:** does this conveyor self-limit near the observed M_BH/M_bulge ≈ 1e-3–5e-3, or run away, or stall?

## Model (CFG748 code and dynamics, plus a sink)
- Units G = a₀ = 1; baryon point mass M_b = 1 (the bulge); seed black hole M_bh0 = 1e-4.
- Central Newtonian mass M_N = M_b + M_bh.
- Cold shells: r̈ = −M_N/r² + (m_out³ − m_in³)/(3 dm r⁴) + L_i²/r³. Self-gravity cancelled; cubic push; no law input.
- **Sink:** a shell reaching r < r_s = 0.1 is removed and its mass added to M_bh (its momentum discarded). There is no
  reflecting boundary. Cubic W (the saturating form differs only where u → a₀; disclosed).
- N = 4000, dt = 0.002, t_end = 4000.
- Initial: a uniform cold sphere of the law's mass on [0.1, 200], at rest radially.
- Angular momentum L_i = λ_i r_i v_c,law(r_i), with λ_i drawn uniform on [0, λ_max], seed 750:
  - **case A:** λ_max = 0 (purely radial);
  - **case B:** λ_max = 0.1 (well inside CFG749's bound regime).

## Tests
- **S1. Final ratio** M_bh(t_end)/M_b.
- **S2. Self-limiting:** growth in t ∈ [2000, 4000] < 20% of total growth.
- **Verdict per case:**
  - **CONSISTENT** iff 1e-3 ≤ M_bh/M_b ≤ 1e-2 and S2 holds;
  - **RUNAWAY** iff M_bh/M_b > 0.05;
  - **STALL** iff M_bh/M_b < 1e-4 + 1e-4 (no growth beyond the seed);
  - **OTHER** otherwise.
- **Reported:** the growth history at t = 100, 500, 1000, 2000, 4000; the bound cold mass; the escaped mass; m/r at r = 2, 5, 10.

## Reading rule (frozen)
- **CONSISTENT** in B: a framework-native reason for central black holes with a natural mass ratio. It is still not a proof:
  radial shells, point bulge, and the sink radius declared, not derived.
- **RUNAWAY:** the naive drain over-feeds (the σ⁴/Ga₀ problem), and a limiting physics is required.
- **STALL:** the attractor keeps cold energy out of the centre, and the drain idea fails.

## Controls
- **K1.** With the sink off (r_s → reflecting at 0.1), case B's m/r at r = 2, 5 is within 5% of the law at t_end.
- **K2.** Total energy, including the swallowed shells' energy at removal, is conserved to 1e-2.
