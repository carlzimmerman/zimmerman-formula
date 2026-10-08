# CFG423: the law's edge from mass conservation, with no tuned radius. PASS, R_c-DEPENDENT (256³)

The criteria were committed first (FROZEN_CRITERIA.md). The engine is `cfg423_pm.py` (CFG416 copy, exact edge, f_ret ≡ 1), the launcher `run_423.py`, and the verdict comes from `cfg423_analysis.py`.

**Edge.** r_edge = r_M / ln(1/(1 − f_b)) ≈ 5.85 r_M (corrected 10-08 from 5.84: the engine's f_b = 0.02237/0.14237 gives 5.850). This is where the phantom has used up the halo's own cold fluid. It is the T10 r_supply (deepseek_push/openai_math_cross_analysis_2026-10/t10), read as mass conservation, with no census input because the PM never depletes baryons.

| run | σ₈ ratio | max\|P−1\| (k ≤ 1) | verdict |
|---|---|---|---|
| P1, R_c = 3 | 1.0036 | 0.042 | GROWTH OK |
| P2, R_c = 1 | 1.0003 | 0.005 | GROWTH OK |
| MUTATE, f_ret = 0.01 (edge ×10) | 1.0160 | 0.139 | TENSION (the control works) |
| CFG410 BASE, unconfined | 1.0193 | 0.153 | TENSION |

**Reading.**
- With no hand-set cover radius, the edge fixes growth as well as CFG414's hand-picked x = 0.4 (0.041 in the same universe).
- The RES catchment width still matters: |ΔP| = 0.037 against an allowed 0.03. At R_c = 1 the law is nearly erased on these scales, as in CFG366.
- So R_c is the last hand-set number. The next step replaces the Gaussian catchment with each halo's own turnaround sphere.

**Caveats.**
- This is 256³, one seed, canonical footing only.
- The cold fluid is bookkeeping, not moved particle by particle.
- A pass does not derive κ, f_b or ρ_Λ.
