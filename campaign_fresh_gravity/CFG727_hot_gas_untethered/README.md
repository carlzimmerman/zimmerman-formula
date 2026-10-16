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

## Post-hoc diagnostic: eRASS1 by gas-mass tercile (`diag_terciles.py`, not a verdict)

| tercile (log M_gas) | plain law MID | **CFG727 MID (canonical)** | CFG727 OUTER | CFG727 INNER |
|---|---|---|---|---|
| ≤ 12.88 | 1.39 ± 0.26 | 1.29 ± 0.23 | 0.89 ± 0.32 | 1.24 |
| 12.88–13.23 | 2.24 ± 0.17 | **1.32 ± 0.11** (Z +2.9) | 1.19 ± 0.15 | 0.43 |
| > 13.23 | 2.00 ± 0.19 | **0.64 ± 0.06** (Z −6) | 1.03 ± 0.09 | 0.16 |

**The 318-cluster pass is partly a cancellation.**
- The middle tercile is still short: Z +2.9 canonical, and +5 on the alt footing (MID 1.65 ± 0.13).
- The heaviest tercile is overshot (Z −6), with its inner band ~6× over-predicted.
- That heavy-end overshoot is the same failure ACCEPT shows (×2).
- The hot-gas rule frees **too much** cold energy in the most massive systems and **not enough** at intermediate mass.
- It does flatten the plain law's large core excess in every tercile (2.0–2.2 → 0.6–1.3), which is real progress. The
  mass dependence is wrong, though.

**Note added (CFG812 finding):** in eRASS1 and ACCEPT the catchment f_ret is pinned at 0.60 by the condensed-fraction floor (condensed fixed at 0.20 M_gas), so census/retention changes did not act there; see CFG812 README.
