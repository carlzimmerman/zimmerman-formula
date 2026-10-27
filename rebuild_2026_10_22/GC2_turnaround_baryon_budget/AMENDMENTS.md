# GC2_turnaround_baryon_budget: AMENDMENTS

## A1 (code-only fix after a Step-0 S0b STOP; before any verdict was printed)

S0b's per-cluster budget log keyed clusters by `round(Mg500/MSUN, 3)`, but Mg500 is already in M☉ at that point, so every
cluster collapsed onto one key. S0b then reported "1 cluster" and stopped the run.

- **The fix:** log Mg500 as is and key by six significant figures.
- **Unchanged:** model, gates and verdict logic.
- **The physics runs of the first launch** completed. Their per-run files are overwritten by the rerun.
