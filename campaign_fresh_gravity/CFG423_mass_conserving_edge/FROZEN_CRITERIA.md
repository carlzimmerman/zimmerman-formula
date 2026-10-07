# CFG423 FROZEN CRITERIA: the law's edge from mass conservation, with no tuned radius (256³)
(owner 2026-10-07: "i don want anything chosen by hand ... it must all be from first principals". These criteria were committed before any run.)

**Idea.** In the working model the phantom IS cold fluid that has settled, so a halo cannot show more mass than it contains. Inside a halo's turnaround sphere the law's phantom can only grow until it has used the halo's own cold fluid:

M_b / (e^{r_M/r} − 1) ≤ M_cold(<r_ta) = ((1 − f_b)/f_b) · M_b,orig

This gives r_edge = r_M / ln(1 + f_ret · f_b/(1 − f_b)).

- **Simulation self-consistency:** the PM does not deplete baryons, so f_ret ≡ 1. The edge is then r_edge = r_M / ln(1/(1 − f_b)), using only the box's own f_b. This removes CFG416's census f_ret and its declared inconsistency.
- **Hand-set numbers removed:** the 0.4 cover radius (CFG414) and the census table (CFG416). The formula is exact, not CFG416's 5.364/f_ret approximation.
- **Still declared:**
  - the RES catchment width R_c, a hand-set number from CFG366. It is tested here, not removed.
  - f_b, the cosmic composition: the same input every cosmological box uses, and still the open "amount" problem.

**Runs.** CFG416's engine with the edge above, 256³, seed 359, canonical footing:
- P1: R_c = 3;
- P2: R_c = 1;
- MUTATE: R_c = 3 with f_ret = 0.01. This enlarges the edge about 10× so the law is effectively unconfined, and it must NOT be GROWTH OK.

Baseline: CFG359 S0 (seed 359, 256³). The comparison is CFG410 BASE (unconfined).

**Decision (CFG361 cuts: GROWTH OK means |σ₈−1| ≤ 5% and max|P−1| (k ≤ 1) ≤ 10%).**
- **ZERO-KNOB PASS:** P1 and P2 are both GROWTH OK, and |pdev(P1) − pdev(P2)| ≤ 0.03, so the result does not depend on R_c.
- **PASS, R_c-DEPENDENT:** P1 is GROWTH OK but the R_c condition fails.
- **FAIL:** P1 is not GROWTH OK.
- **The control:** if MUTATE is GROWTH OK, it is broken and the lane is INCONCLUSIVE.
- **Reported, not part of the verdict:** the median x_edge = r_edge/r_ON over resolved hosts at z = 0.

**Caveats (declared).**
- This is 256³, a check rather than a confirmation.
- The cold fluid is bookkeeping, not moved particle by particle.
- A pass makes the edge a consequence of mass conservation in the model. It does not derive κ, f_b or ρ_Λ.
