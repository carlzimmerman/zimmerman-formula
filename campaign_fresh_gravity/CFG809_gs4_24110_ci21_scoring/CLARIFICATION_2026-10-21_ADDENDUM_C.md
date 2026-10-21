# CFG809 clarification, addendum C (2026-10-21; before any programme 2025.1.01377.L data; nothing frozen edited)

**Addendum B's MUTATE null was the wrong scale.** Its masks were grown on noise: median 20 px. A well-detected line's mask is far
larger: 18,083 px on MOCK GS4-a. The null standard deviation therefore came out about 40× too small, and a small residual
bias scored +151.7 (CFG942, 9dcfc3ce4). Addendum B's statistic is withdrawn.

**Ruling (replaces addendum B).** The MUTATE null is an injection null that matches both the mask's size and its selection:
1. At 200 off-source positions, inject a copy of the true run's beam-convolved moment-0 model into the real cube's noise, with the
   same line profile and the same flux.
2. Grow the mask by the true run's procedure.
3. Measure that mask's shifted-window flux with the addendum-A continuum.

The statistic is (true-run shifted flux − null mean) / null standard deviation. The control bites if it is below 3.

If the line is not detected (G1 fails), MUTATE is non-diagnostic, as FROZEN_CRITERIA §5 already says. The addendum-A statistic,
the addendum-B statistic and the mask sizes are printed as information.

κ = ½ fitted; footings never pooled; cold energy mass required; not theory closed.
