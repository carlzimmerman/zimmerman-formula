# CFG424: no hand-set numbers in the growth fix. ZERO-KNOB PASS (256³, seed 359)

The criteria were committed first. The engine is `cfg424_pm.py` (RC = 0 mode), the launcher `run_424.py`, and the verdict comes from `cfg424_analysis.py`.

**Rule.** The phantom excess lives inside the mass-conserving edge r_M/ln(1/(1−f_b)) (CFG423 / T10). The cold fluid it uses is drawn from the same halo's turnaround catchment, in proportion to the cold density there, so the added source sums to zero on every catchment. There is no cover radius and no catchment width.

| run | σ₈ ratio | max\|P−1\| | verdict |
|---|---|---|---|
| canonical | 1.0033 | 0.027 | GROWTH OK |
| alt | 1.0031 | 0.029 | GROWTH OK |
| MUTATE (no compensation) | 1.0326 | 0.154 | TENSION (the control works) |

**Diagnostics.**
- Overdraw is 0. At most 30% of a catchment's cold fluid is used (q_max 0.30 at z = 0).
- The source sum is about 4e-4 against Σe ≈ 2e5, so mass is conserved.

**Inputs that remain:**
- κ (fitted);
- f_b;
- the T1 switch ε and the MIX-A filter (inherited, not tuned here).

Confirmation is CFG425: seeds 360/361 are GROWTH OK (0.022 / 0.017), and the 512³ run is queued.

**Caveats.**
- The cold fluid is bookkeeping, not moved particle by particle.
- κ, f_b and ρ_Λ are not derived.
