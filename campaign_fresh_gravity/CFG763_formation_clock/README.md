# CFG763: a formation clock fits both the Newtonian young tidal dwarfs and the law-obeying old discs — window OPEN

**Label: F2 window OPEN (both footings). K1 PASS (CFG441 reproduced exactly). MUTATE bites (a law-obeying set leaves no lower
bound).**

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (5b747a56b), 2026-10-13. Block CFG760–769.
- **Script:** `python3 cfg763.py` (seconds) → `cfg763.out`, `cfg763_results.json`. Data: Lelli+2015 six (real_research/data/
  tidal_dwarfs) and Arp 72c (CFG441 data), read only; V_N and V_law code copied from CFG441.
- **Settings:** κ = ½ FITTED; ν_mono with the 1-D EFE at nominal host mass; the cold energy's mass is required; no particle species;
  not "theory closed".

## Model
Cold energy forms at rest at a first-order rate: a system whose baryons are t old holds f = 1 − e^{−t/τ} of the law's cold mass,
V² = V_N² + f(V_law² − V_N²).

| footing | τ_min,95 (ages at −1σ) | τ_min,95 (nominal ages) | upper bound from SPARC (f(8 Gyr) ≥ 0.9) |
|---|---|---|---|
| canonical | **0.72 Gyr** | 1.20 Gyr | 3.47 Gyr |
| alt | **0.83 Gyr** | 1.38 Gyr | 3.47 Gyr |

In orbital units the lower bound is τ ≳ 0.24–1.2 local orbits (0.4–2.0 at nominal ages).

## Reading
1. **Formation at rest survives the young-TDG data.** The CFG7/CFG441 "young tidal dwarfs are Newtonian" result (Δχ² +33/+39
   against the law) is what a formation time of ≳ 0.7–1.4 Gyr predicts: their baryons are 0.3–0.75 Gyr old.
2. **A sharp, framework-native prediction (not yet tested):** a system whose baryons assembled t ago holds
   1 − e^{−t/3.47} ≤ f ≤ 1 − e^{−t/τ_min}:
   - **at 1 Gyr: 25–75% of the law's cold mass;**
   - at 2 Gyr: 44–94%;
   - at 4 Gyr: ≥ 68%.
3. **Discriminator from FG001's hierarchy reading.** FG001 explains the same young TDGs by ownership (a TDG inside its host owns
   no cold energy), so on that reading old TDGs stay Newtonian. The clock says an old TDG holds ≥ 68% (NGC 5557-E1, ~4 Gyr:
   CFG441/448's 28–41 km/s band, not Newton's 16–24). The data are not available (CFG448: needs VLA-C ~90 h or uGMRT ~80 h).
4. **What it implies for high z.** Discs at z ≈ 2–4, whose baryons are ~1–2 Gyr old, should show a reduced boost. The record's
   high-z kinematics are calibration-limited (CFG213–229), so this is neither excluded nor supported. Frozen pre-registrations
   (CFG570/571) are not edited.

## Not tested
Formation laws other than first order; TDG non-equilibrium (all < 1 orbit); the formation microphysics itself (astra's F1/F5).
