# CFG425: the zero-knob growth fix confirmed across seeds and at 512³. CONFIRMED

The criteria were committed first. The launcher is `run_425.py`, and the verdict comes from `cfg425_analysis.py`. The engine is CFG424's (RC = 0: turnaround-catchment mass conservation, f_ret ≡ 1).

| run | σ₈ ratio | max\|P−1\| | verdict |
|---|---|---|---|
| R1, 256³, seed 360 | 1.0024 | 0.022 | GROWTH OK |
| R2, 256³, seed 361 | 1.0026 | 0.017 | GROWTH OK |
| **R3, 512³, seed 359** | **1.0045** | **0.033** | **GROWTH OK** |

Overdraw is 0 everywhere.
- At 512³ the excess rises only from 0.027 (256³) to 0.033, well inside the 0.10 cut.
- Compare the hand-set and census rules at 512³: CFG414 alt 0.0996 and CFG416 alt 0.1009.
- With CFG424/426/427 (8/8 at 256³, both footings, DE branch, ε and filter insensitive), the zero-knob rule is the record's growth fix. Its inputs are κ (fitted) and f_b.

**Caveats.**
- The 512³ run is canonical only.
- The cold fluid is bookkeeping, not moved particle by particle.
- κ, f_b and ρ_Λ are not derived.
