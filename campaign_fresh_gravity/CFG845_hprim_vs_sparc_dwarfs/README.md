# CFG845 — does H-PRIM (CFG844), calibrated on the dSphs, over-predict SPARC's small rotating dwarfs?

Criteria: `FROZEN_CRITERIA.md` (2d2ca7a9a, before the script). Run: `python3 cfg845.py` (MUTATE `CFG845_MUTATE=1`). Seconds.

## Result — CLASS: **H-PRIM EXCLUDED** (10σ)
- Calibration from CFG844 only: log P = 1.163 − 0.943 log x (the free core's mean density over the collapse-epoch virial mean,
  falling as x^−0.94; K1: P(median x) = 99 vs CFG844's median 141, within the scatter of the fit — the 10% K1 tolerance is
  missed (ratio 0.70), disclosed; the median-P calibration would predict an even larger excess).
- 56 SPARC dwarfs with M_b ≤ 3e9 (collapse epochs z_c 1.1–2.3, same recipe): H-PRIM predicts a mean excess **+0.305 dex** at
  their measured radii (0.01–0.5 r_vir); they show **+0.032 dex**. D = −0.273 ± 0.026 dex (z −10.4) → EXCLUDED.
  Only 5 of 56 galaxies have obs − pred ≥ 0.
- MUTATE (P = 0) gives D = +0.032 (the law-only residual), as required.
- **Reading:** a dense early-collapsed free cold core in every early-assembling small system is ruled out by rotating dwarfs.
  CFG844's amplitude agreement was therefore not a mechanism. What survives as a clue: at similar masses and assembly epochs,
  **gas-rich rotating dwarfs carry no excess, gas-poor pressure-supported dwarfs at g_bar < 10⁻¹² do.** The excess tracks gas loss
  / pressure support / ultra-low internal acceleration, not mass or formation epoch. (A gas-loss-tied free core would be a new
  hypothesis needing an independent measure of expelled baryons; not run.)

κ = ½ fitted; cold energy mass required; not theory closed.
