# CFG740 — sealed wide-binary prediction of the stiff-polarization construction (frozen criteria, committed alone)

Block CFG740–749 (reserved 2026-10-13). Written before any CFG740 number. κ = ½ fitted; both footings, never pooled; the cold
energy's mass is required; no particle species; not theory closed. **These are predictions, not results.** The frozen
pre-registration in `prep_2026/gaia_dr4_prep/` is read for its statistic only and is not touched.

## What is sealed
The construction of CFG691–696 (independent light polarization field, critical + saturating W, stiffness L* ≥ 5.75 pc,
free-fall basins) predicts, for a wide binary of total mass M at separation s inside its free-fall basin and inside ℓ_γ(M):
- anomaly = GM/L*² (constant; CFG691 inner limit);
- **γ_v − 1 ≃ ½ (s/L*)²**: log-slope exactly 2, mass-independent.

Here γ_v is the prereg's statistic, the velocity-boost (√ of the force ratio).

## Numbers to compute and seal (script `cfg740_predict.py`)
- **Grid.** γ_v − 1 at L* = L*_min = 5.754 pc (CFG691, a₀-free), the **upper envelope**, for the prereg's bins 2, 5, 10, 20,
  30, 50, 100, 236 kAU.
  - Use the full stiff profile S(s/ℓ_γ), not only the inner limit, for M = 1.5 M☉ (the prereg's reference mass) on both
    footings.
  - Check that every bin lies inside ℓ_γ and inside the binary's free-fall basin.
- **Shape.** The log-slope d ln(γ_v − 1)/d ln s between 50 and 236 kAU (expect 2.00).
- **Contrast** (read from the prereg, not recomputed):
  - the gated MI branch: 2–30 kAU band 1.0004–1.0006, exponent 3 beyond r_gate;
  - the record's no-EFE law: PAPER44 gamma_iso 1.01 / 1.06 / 1.197 / 1.511 at 2 / 5 / 10 / 20 kAU, a velocity statistic per
    PAPER44 (reported as given).

## Seal
`cfg740_predictions.json`, written deterministically (no timestamps). Its SHA-256 goes in `PREDICTIONS_HASH.txt`, committed
before Gaia DR4 (2026-12-02). Never edited after; any change goes in a new dated file.

## Falsifiers of the construction (declared now)
1. **Any boost above the envelope ½(s/5.754 pc)²** in a contamination-controlled DR4 sample, at any separation ≤ 236 kAU. In
   particular, γ_v ≥ 1.01 at s ≤ 50 kAU kills the construction (envelope 9e-4 there).
2. **An excess with log-slope inconsistent with 2** (for example the gated branch's 3, or the law's rising no-EFE boost).

## MUTATE (`CFG740_MUTATE=1`, exit 1 iff it bites)
No stiffness: the γ_v − 1 at 10 kAU must exceed 0.1 (the unscreened deep boost), so the sealed envelope depends on the
stiffness.
