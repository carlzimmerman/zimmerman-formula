# CFG727: hot gas untethered (free cold energy from the hot-gas budget) in groups and clusters. FAIL as frozen (2 of 4 pass)

| test | primary (P), both kernels and both footings | pass rule | result |
|---|---|---|---|
| **eRASS1, 318 clusters** | **A_MID 0.93 ± 0.06, A_OUTER 1.05 ± 0.09** (canonical; alt 1.08/1.14) | MID and OUTER within 2σ | **PASS** |
| **eFEDS, 131 groups** | χ² 18.7–19.9 on 8 dof, p 0.011–0.017 | p ≥ 0.01 | **PASS** (narrowly) |
| ACCEPT, 8 massive clusters | A_OUTER 0.48–0.50 (Z −3.8 to −4.3), ×2 overshoot | OUTER within 2σ | FAIL |
| KiDS early − late | pred −0.034 vs obs +0.280 (Z +3.8); no free mass at galaxy scale | — | FAIL (predetermined, pre-run addendum) |

**Reading.**
- **The eRASS1 cluster-core problem is solved under this rule.** The record's ×1.8 core excess (CFG721: A_MID 1.90) becomes
  0.93 ± 0.06 across 318 clusters, robust to every placement bracket. eFEDS groups also pass.
- Two things remain:
  - **the most massive clusters (ACCEPT)**, which it overshoots about ×2;
  - **the galaxy-scale early-type excess**, where the rule makes no free mass at all.
- The frozen verdict needs all four tests, so it is **FAIL**.
- **Disclosed:** the INNER band (not graded) is over-predicted (A_INNER 0.31). The ALL-source variant fails eRASS1 (MID
  1.40) but passes ACCEPT, so no single source rule passes both eRASS1 and ACCEPT.

**Run.**
- The eRASS stage was parallelised (`par727.py`, implementation only). It used the lane's own functions with the same
  inputs and order, and reproduced the serial run's first 40 clusters exactly before writing.
- The serial stage had been interrupted at 16:42 and again at 17:59.

**Controls.** M0 (the law reproduces CFG687, 1.6e-15) and C1 (supply = settled + free) pass. MUTATE M1 (free mass removed:
MID 1.72) and M2 (shuffled: MID 0.99) bite.

κ fitted; cold energy mass required; not theory closed.
