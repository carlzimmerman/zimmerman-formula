# CFG764: an orbital formation clock also fits — cold energy forms within about half to one local orbit (window OPEN)

**Label: O1 OPEN (both footings). K1 PASS. MUTATE bites (exit 1).**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (9990bf4b1), 2026-10-13. Block CFG760–769.
- **Script:** `python3 cfg764.py` (seconds) → `cfg764.out`, `cfg764_results.json`. Young TDGs as CFG763 (code copied); raw SPARC last
  points via CFG760's `CFG691_copy.py`.
- **Settings:** κ = ½ FITTED; ν_mono with 1-D EFE; the cold energy's mass is required; no particle species; not "theory closed".

## Model and result
τ = k·t_orb, t_orb = 2πR/V at the measured radius; f = 1 − e^{−t/τ}.

| | canonical | alt |
|---|---|---|
| k_min,95 (young TDGs, ages at −1σ) | **0.46** | **0.52** |
| k_max (SPARC: f ≥ 0.9 after 8 Gyr at the slowest last-point orbit, 2.91 Gyr) | **1.20** | **1.20** |
| SPARC galaxies excluded at k_min | 0/175 | 0/175 |

k_max is 1.94 at the 5th-percentile galaxy and 4.6 at the median, so only the few slowest outer orbits bind.

## Reading
1. **Two clocks survive the data.** CFG763's universal τ ≈ 0.7–3.5 Gyr, and this local clock, in which cold energy forms in
   **0.46–1.2 local orbits**. The orbital form is the natural one for a medium that settles dynamically (CFG747/748 relaxed the inner
   halo within a few periods). Its constant k is of order one and is not tuned.
2. **They make opposite high-z predictions, which separates them.**
   - Compact z ≈ 2–4 discs have t_orb ≈ 0.1–0.3 Gyr. The orbital clock fills them within ~0.1–0.4 Gyr, so they should obey the
     **full law** (consistent with flat a₀(z)).
   - The universal clock leaves 1-Gyr-old baryons at 25–75%.
3. **The orbital clock also predicts a radial gradient** in young systems: the inner, fast-orbit regions fill first, and the deficit
   grows outward. Old TDGs (NGC 5557-E1, ~4 Gyr ≈ several orbits) should be on the law under both clocks; the FG001 hierarchy
   reading says Newtonian.

## Not tested
Radial structure inside a galaxy, non-first-order formation, TDG non-equilibrium, the formation microphysics (astra F1/F5).
