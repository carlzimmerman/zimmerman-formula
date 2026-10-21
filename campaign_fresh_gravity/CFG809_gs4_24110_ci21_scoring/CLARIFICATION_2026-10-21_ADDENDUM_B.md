# CFG809 clarification, addendum B (2026-10-21; before any programme 2025.1.01377.L data; nothing frozen edited)

**MUTATE bite statistic.** Under addendum A §2 the GS4 MUTATE reads +2.90σ on MOCK GS4-a. That is a narrow bite, and its
residual is not line emission. The true-run mask is chosen where (window − continuum) ≥ 2σ, which favours pixels with low
continuum noise. The shifted continuum shares those channels, so subtracting it biases the masked sum upward. CFG942
(90bdb0153) shows the split in every MUTATE output: raw shifted window +0.57σ, continuum term +2.32σ. In ring copies that were
not selected on the data, the continuum term is −0.13 ± 0.65σ.

**Ruling.** The MUTATE flux is scored against a selection-aware null, built the same way as G1 (A-G13). At 200 random off-source
seeds:
1. grow the mask by the true run's procedure;
2. measure that mask's flux in the shifted window with the addendum-A continuum.

The bite statistic is (shifted flux − null mean) / null standard deviation. The control bites if it is below 3.

The old statistic and the addendum-A split are printed as information. A disjoint-continuum alternative was considered and
rejected: the true-run continuum uses every line-free channel, so a disjoint set is empty.

κ = ½ fitted; footings never pooled; cold energy mass required; not theory closed.
