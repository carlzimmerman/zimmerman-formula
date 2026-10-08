# CFG427: does the zero-knob growth fix depend on the two inherited settings? INSENSITIVE (256³)

The criteria were committed first. The launcher is `run_427.py`, and the verdict comes from `cfg427_analysis.py`. The engine is CFG424's (RC = 0), canonical, seed 359.

| run | σ₈ ratio | max\|P−1\| | verdict |
|---|---|---|---|
| ε = 0.0385 (half) | 1.0033 | 0.0273 | GROWTH OK |
| ε = 0.154 (double) | 1.0033 | 0.0273 | GROWTH OK |
| MIX-B gas filter | 1.0027 | 0.0262 | GROWTH OK |
| HOT1 (all gas hot) | 1.0038 | 0.0311 | GROWTH OK |

The reference is CFG424 canonical, at 0.0273. Overdraw is 0 everywhere.

**Reading.**
- Under mass conservation, the switch width does essentially nothing. I checked that it was applied: P differs by ≤ 0.03%.
- The gas filter moves the excess only between 0.026 and 0.031.
- So neither inherited setting carries the pass. The fix's inputs reduce to κ (fitted) and f_b (cosmology).

**Caveats.**
- This is 256³ and one seed.
- The cold fluid is bookkeeping, not moved particle by particle.
- κ, f_b and ρ_Λ are not derived.
