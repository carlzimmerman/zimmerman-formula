# CFG600: KiDS catchment from the outer lensing profile. VOID by its own frozen controls; descriptively, the inner shortfall does not depend on the edge at all

κ = ½ is fitted. The footings (9.36e-11 / 1.13e-10, written can / alt) are never pooled. The cold energy's mass is still required. This is not a closed theory. Numbers come from `cfg600_native_catchment_results.json` and `cfg600_native_catchment.out`.

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (488e95c0c). **Scripts:** `cfg600_common.py` (CFG531 harness executed read-only up to its `EARLY = TYP == 1` line, cached tables, nothing rebuilt) and `cfg600_native_catchment.py` (about 1 min, nice 10, 1 thread). Nothing downloaded; no PM run.
- **Question (CFG594 rank 2, KiDS half):** take each system's catchment edge from the lensing profile beyond the edge instead of the ΛCDM-relative census f_ret. How far do the inner shortfall and the early-type split move?

## Result
- **Catchment from data.** Calibrating x = r_edge / r_ta,law on the six outermost bins (all f30 lenses) gives x\* = 0.55 / 0.50 (A can / alt) and 0.55 / 0.45 (B), against the census median 0.28 / 0.24. The data want the edge about twice as far out as the census puts it, as CFG559 found.
- **The inner shortfall does not move.** eps(K9) census → x\*: A can +0.366 → +0.382, A alt +0.241 → +0.262, B can +0.370 → +0.382, B alt +0.245 → +0.262; sigma about 0.09 / 0.084. Label **UNCHANGED** on both footings (|d| ≤ 0.021 ≪ 1 sigma). Z at x\* is +4.1 (can) and +3.1 (alt), so the shortfall is not closed.
- **Early-type split.** With x\* calibrated per class (early 0.70–0.80 can, 0.70 alt; late 0.28–0.36), the early-minus-late K9 difference is +1.146 → +1.156 (A can) with Z +6.5 in both; **UNCHANGED** on all four cells.
- **Why (post-freeze diagnostic, no verdict weight):** eps(K9) over all nodes x = 0.20–1.00 ranges only 0.029–0.036, about a third of its sigma. Inside the lensing bins used (≤ 445 kpc) every edge choice gives the same profile (CFG531 had noted census = LAW_RTA there). So an edge from data can change only the outer bins, never the inner nine.

## Controls (frozen), honestly reported: 2/4 pass
- PASS K1: the census path reproduces CFG531's committed BASE eps exactly. PASS K3: a noiseless mock at x = 0.50 recovers x\* = 0.50 and eps = 0.
- **FAIL MU2** (edge at x = 0.20 should cost ≥ 2× the outer chi2 of x\*): ratios 1.4–2.2, so on some cells the outer bins distinguish the edge only weakly (outer chi2 at x\* 15.6–20.7 vs 33–36 at 0.20).
- **FAIL MU1** (circular calibration on the inner nine should "close" the shortfall): it does not (Z 3.8 / 3.9 can, 2.8 / 2.9 alt), because the inner nine are edge-independent. By the frozen rule the estimator is **VOID** as a test of closure; the controls fail for the same reason the result is UNCHANGED.

## What this says and does not say
- A data-derived catchment, as built into the KiDS machinery, cannot repair the inner shortfall or the early-type split. The shortfall is a property of the law's own profile inside about 445 kpc, not of where the supply ends. That agrees with CFG531 (mechanism: none) and CFG559.
- It does not say the shortfall is real: the environment term (CFG529) and the SHMR (CFG601) still enter it.
- **Group half of rank 2 NOT done:** on-disk group data are Tian+2026 σ_los and Re only; a dynamical catchment from σ would be circular with the BFJR statistic. An independent zero-velocity or lensing group mass needs a download (owner's yes).
