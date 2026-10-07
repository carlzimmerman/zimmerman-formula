# CFG415 FROZEN CRITERIA: two doors from the OpenAI release
(owner 2026-10-07: "yeah run them"; committed before any script)

## Door 1: shared catchments as the source of "unsettled" cold fluid (inspired by result 373, mixed optimal multi-marginal plans)
**Idea.** Cold fluid inside the turnaround spheres of two or more resolved hosts has no unique host to settle into, so it stays unsettled.

**Measurement** on CFG410's BASE z0 snapshots (256³, canonical and alt; read-only):
- Peaks and r_ON come from CFG413's machinery (cfg412_screen / cfg413_growth), using resolved hosts with r_ON ≥ 2 cells.
- Turnaround mass M_ta = (4π/3) r_ON³ Δ_ta ρ̄_m.
- For each host, the shared fraction s = (mass inside its sphere that is also inside ≥ 1 other host's sphere) / (mass inside its sphere).
- Mass bins: group-like 10^13.5 ≤ M_ta < 10^14.5 Msun/h; cluster-like M_ta ≥ 10^14.5. Galaxy hosts are unresolved at this mesh; that is stated.

**Verdict, against the bias-robust data ordering (groups carry about 2× clusters' excess per present baryon; CFG382 audit):**
- CONSISTENT: median s(groups) ≥ median s(clusters) on both footings.
- INCONSISTENT: otherwise.
- The mechanism is only a reading. A CONSISTENT verdict does not establish it.

## Door 2: does the settled phantom track √M_b? (from 374, via the DeepSeek stability result)
**Reduction.** In deep MOND, M_ph(<r) = r√(G M_b a₀)/G, so the √M_b tracking is the baryonic Tully–Fisher relation V⁴ ∝ M_b.

**Test.** On SPARC (Q ≤ 2, the record's loader), fit log V_flat against log M_b with the record's M/L convention (Υ_disk 0.5, Υ_bul 0.7). V_flat is the median of the last 3 points where the curve is flat to within 5%.
- CONSISTENT if the slope is 4 within 2σ (bootstrap).
- This is a re-check of a known relation, not a new test.

## MUTATE (CFG415_MUTATE=1, separate outputs)
- Door 1: shuffle the host masses. The group-vs-cluster ordering must lose its meaning, so report the shuffled difference.
- Door 2: multiply M_b by V² (break the relation). The slope must leave 4 by more than 2σ.

**Scope.** κ = ½ is fitted. The cold fluid is still required. No DM particle.
