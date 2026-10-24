# ZT5: Z★'s red-lens prediction from gas loss is SPLIT. Canonical FAIL (z +2.52, against an upper-bound prediction), alt PASS (z +0.80). The row turns on red stellar masses

Criteria **2e8ab8f42f** (committed alone first); test frozen in `Z1_successor_design/TEST_PLAN.md` (0d1959a4f5). Script
`zt5_red_lenses.py` (seconds, 0.06 GB). `--mutate` (no gas) fails KM as it should (exit 1). κ = ½ FITTED. Footings never
pooled. No dark-matter particle. Not "theory closed". Nothing here says the data favour the framework.

**Prediction.** In Z★ a red lens is a former blue owner that lost its gas but kept the dust it owned, so its lensing sits
above the law on its present baryons by √(1 + f_gas,blue) at matched M★ (deep regime, Z1 K9). The RAW gas scaling is ALFALFA-SDSS
(Durbala+20, 28,267 galaxies). It is HI-selected, so f_gas is an **upper bound** at fixed M★, and so is the prediction. The 88,079 KiDS
red lenses have median log M★ 10.744, where ALFALFA's median f_gas is 0.281. The lens-averaged prediction is **1.154**.

| footing | S2 red A (data / v3) | z vs 1.154 | class | reported z: g−i ≤ 0.9 (1.216) / B21 relation (1.093) / baseline-consistent (1.039) |
|---|---|---|---|---|
| canonical | 1.313 ± 0.063 | **+2.52** | **FAIL** (ROBUST: data above the upper bound) | +1.54 / +3.49 / +4.34 |
| alt | 1.200 ± 0.058 | +0.80 | **PASS** | −0.28 / +1.85 / +2.78 |

Blue lenses stay at S2's 0.878 / 0.802 by construction (blue owners keep their gas). Checks KS, KG, KN, KM, KR: all PASS.

**Reading.**
- The frozen line splits by footing. Z★'s retention mechanism explains at most about half of the red excess on the canonical
  footing (0.154 of 0.313), even with the gas-richest sample on disk.
- The S2 baseline already gives red lenses B21 cold gas and a 0.5 M★ hot CGM. Measured against that baseline, the
  prediction drops to 1.039, and both footings fail (reported only).
- The red A values depend on red stellar masses. With S2's own red-M★ corrections (CFG667 +0.123 dex: A 1.191 canonical; plus IMF:
  1.023), the excess the prediction must explain mostly disappears. Z-T5 cannot be graded more firmly until red M★ is settled
  (CFG667 §3 leaves the estimator choice open).
