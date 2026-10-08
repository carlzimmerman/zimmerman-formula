# CFG439: the zero-knob growth fix at 512³ on the alt footing and with a₀ tracking DE. CONFIRMED

The criteria were committed first. The launcher is `run_439.py`, and the verdict comes from `cfg439_analysis.py`.

| run (512³) | σ₈ ratio | max\|P−1\| | verdict |
|---|---|---|---|
| FLAT, alt | 1.0054 | 0.040 | GROWTH OK |
| DE, canonical | 1.0045 | 0.034 | GROWTH OK |

Overdraw is 0.
- With CFG425 R3 (FLAT canonical, 0.033), the zero-knob rule passes at 512³ on both footings and with DE-tracking a₀, with 2.5× margin to the 0.10 cut.
- The census edge (CFG416) and the hand-set edge (CFG414) sat at the cut.

**Caveats.**
- One seed at 512³.
- The cold fluid is bookkeeping, not moved particle by particle.
- κ, f_b and ρ_Λ are not derived.
