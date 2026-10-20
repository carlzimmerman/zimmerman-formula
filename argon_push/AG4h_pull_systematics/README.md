# AG4h: the 13 large pulls are NOT distance or inclination errors. **SHAPE DOMINATES** (11 of 13)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (1f8c62e5d). A coverage-only pre-flight is disclosed there.
- **Run:** `OMP_NUM_THREADS=1 nice -n 10 python3 ag4h.py`: 0.7 s, 0.11 GB, exit 0. It ran beside NC2x under the owner's
  small-job rule.
  - MUTATE: 12 of 13 inner-half Υ × 3 mocks read SHAPE-DRIVEN, so it bites (exit 1).
  - AG4g's frozen definitions are executed read-only.
- **Settings:** κ = ½ fitted; not theory closed.
- **Wording correction, disclosed:** the criteria call f = 10^(−c_req) "D_true/D_SPARC". It is D_SPARC/D_true, the factor by
  which SPARC's distance would have to be too large. The numbers, n_D and the K2 test (recovering 1.3) are as frozen and
  correct with this label.

## Per galaxy (n=1, canonical a₀)
| galaxy | pull | Q | fD | Δχ² (Υ at SPS + free offset, vs Υ free) | distance factor needed | n_D | inclination needed | class |
|---|---|---|---|---|---|---|---|---|
| CamB | −3.3 | 2 | TRGB | 0.0 | 4.26 | 18.7σ | 65°→26° (7.8σ) | coherent, needs > 2σ |
| NGC1705 | +3.5 | 3 | TRGB | 0.1 | 0.52 | 13.0σ | impossible | coherent, needs > 2σ |
| IC2574 | −3.7 | 2 | TRGB | 32.9 | — | — | — | SHAPE |
| NGC0024 | +3.4 | 1 | TRGB | 6.9 | — | — | — | SHAPE |
| NGC4217 | −3.4 | 1 | UMa | 78.0 | — | — | — | SHAPE |
| NGC5985 | +3.55 | 1 | Hubble | 57.2 | — | — | — | SHAPE |
| UGC00128 | +3.5 | 1 | Hubble | 56.3 | — | — | — | SHAPE |
| UGC00731 | +4.9 | 1 | Hubble | 101.2 | — | — | — | SHAPE |
| UGC03580 | −5.0 | 2 | Hubble | 222.5 | — | — | — | SHAPE |
| UGC06787 | −5.0 | 2 | Hubble | 223.4 | — | — | — | SHAPE |
| UGC08286 | +3.7 | 1 | TRGB | 15.9 | — | — | — | SHAPE |
| UGC08837 | −3.6 | 2 | TRGB | 9.3 | — | — | — | SHAPE |
| UGC12506 | +3.1 | 2 | Hubble | 45.2 | — | — | — | SHAPE |

- **TD:** Cosmicflows-4 confirms all four TRGB distances it covers: CamB 1.018, NGC1705 0.977, UGC08286 0.910 and
  UGC08837 0.982 (CF4/SPARC).
- **K1** (AG4g pulls reproduced) and **K2** (injected 30% distance error recovered in 11/13) PASS.

## Reading
- Distance and inclination errors do not explain the excess of strongly pulled galaxies. For 11 of 13, no coherent shift can
  replace the change in Υ. The other two would need TRGB distances wrong by factors of 2 to 4.
- The pulls come from each rotation curve's **shape**, which a single SPS mass-to-light ratio plus the law cannot reproduce.
- Three causes remain, and on-disk data cannot separate them:
  1. **Non-circular motions or projection.** IC2574 has known strong non-circular motions; NGC4217 and UGC08837 are nearly
     edge-on.
  2. **Bulge–disc decomposition or radial M/L gradients.** UGC03580 and UGC06787 are bulge-heavy early spirals sitting at the
     Υ floor.
  3. **A real difference between the law's mass profile and the galaxy's.**
- **Post hoc, not graded:** the sign tracks data quality. Five of the six positive pulls (needing more mass) are Q = 1
  galaxies: NGC0024, NGC5985, UGC00128, UGC00731, UGC08286. Four of the five negative pulls are Q = 2.
  - Negative pulls fit cause 1, since non-circular motions make V_obs underestimate the circular speed.
  - The positive pulls in clean galaxies are the only place cause 3 could hide: about 3% of SPARC.
  - That is a short list for targeted follow-up (independent kinematic analyses, colour-based M/L gradients), not a detection.
- **To close it:** independent tilted-ring and non-circular-motion analyses for the 11 shape-driven galaxies, and resolved
  stellar-population (colour) M/L profiles for the positive-pull Q = 1 five. Neither is on disk; fetching needs the owner's OK.
