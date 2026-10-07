# CFG378: two species with optimal-transport settling of real cold particles. GROWTH OK by the frozen cuts, but HOLLOW: settling barely fills the target

Criteria 18bfc1a98 with Amendment 1 (the corrected k_J, audit 5819dd616). Engine, controls and launcher are by the agent. Checks, analysis and README are by the orchestrator, run from the committed scripts.

**Frozen verdict (256³; ratios to this engine's S0).**

| run | footing | σ₈ ratio | max \|P−1\|, k ≤ 1 | target filled R (R₀ with no settling) | verdict |
|---|---|---|---|---|---|
| g = 1 (Γ = 1/t_dyn) | canonical | 1.017 | 0.059 | 0.486 (0.472) | GROWTH OK |
| g = 1 | alt | 1.023 | 0.092 | 0.445 (0.432) | GROWTH OK |
| g = 0.1 | canonical / alt | 1.002 / 1.002 | 0.006 / 0.009 | +0.001 | GROWTH OK |

**Why "GROWTH OK" is hollow.**
- The settling step closes only **2.6%** of the gap between the cold fluid and the phantom target (R 0.472 → 0.486), or 0.3% at g = 0.1.
- So in this run the cold fluid does NOT realise the law in switch-ON regions. Growth stays near Newtonian because almost nothing settles.
- The settling scheme (one linearised Monge–Ampère step, capped at 1 cell per step, momenta unchanged) is too weak to test whether a real settling that achieves the law keeps growth in bounds.
- This matches CFG390, where settling at the record's rates does not fill the target.

**Resolution note.** The g = 1 small-scale excess is LOWER at 256³ than at 128³ DEV (P_max 0.059 vs 0.110 canonical), the opposite of CFG361's K4. It is not scored.

**Controls (all pass).**
- C1 mass: relative error ≤ 2e-15, no overdraw.
- C2: no settling reproduces S0 to 9e-8.
- C3: the step algebra.
- MUTATE (target ×10) moves σ₈ by +13%.

**Scope.**
- The settling scheme is declared, not derived. CFG373's lapse channel is the candidate mechanism, and it needs CFG381's coupling.
- Momenta are unchanged on settling, and the whole box acts as the reservoir.
- κ = ½ is fitted. The cold fluid is still required.
