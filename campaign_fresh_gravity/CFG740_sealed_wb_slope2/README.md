# CFG740: sealed Gaia DR4 wide-binary prediction — log-slope exactly 2

**SEALED 2026-10-13, before Gaia DR4 (2026-12-02).** SHA-256 of `cfg740_predictions.json`:
`5336fd99043e75f57c1de57525a8121b80d38b601c2e2beaaee62ea4a27a944a` (`PREDICTIONS_HASH.txt`). Never edit these files; any change
goes in a new dated file. Predictions, not results.

- **Criteria:** `FROZEN_CRITERIA.md` (c4f88c6ee), committed alone first.
- **Script:** `python3 cfg740_predict.py` reproduces the JSON byte for byte (no timestamps). `CFG740_MUTATE=1` exits 1: without
  stiffness, γ_v − 1 at 10 kAU exceeds 0.1.
- **Settings:** κ = ½ FITTED; the prediction is the same on both footings (the inner pull GM/L*² has no a₀ in it). The frozen
  prereg in `prep_2026/gaia_dr4_prep/` was read for its statistic only and not touched.

## The prediction (upper envelope at L* = 5.754 pc; 1.5 M☉; free-fall basin 2.0 pc; ℓ_γ 350–385 pc)

| s [kAU] | 2 | 5 | 10 | 20 | 30 | 50 | 100 | 236 |
|---|---|---|---|---|---|---|---|---|
| γ_v − 1 | 1.4e-6 | 8.9e-6 | 3.5e-5 | 1.4e-4 | 3.2e-4 | **8.9e-4** | 3.5e-3 | **2.0e-2** |

- Log-slope 50–236 kAU: **1.993** (inner limit ½(s/L*)², exactly 2).
- Any L* > L*_min only lowers the curve, so this is an **upper envelope**.

## How it differs from the record's other branches (read from the prereg and PAPER44)
- **Gated MI branch:** 1.0004–1.0006 in 2–30 kAU, with an excess of **exponent 3** beyond r_gate.
- **Record's no-EFE law** (PAPER44 gamma_iso): 1.01 / 1.06 / 1.197 / 1.511 at 2 / 5 / 10 / 20 kAU.

## Falsifiers of the construction
1. Any boost above the envelope. In particular, **γ_v ≥ 1.01 at s ≤ 50 kAU kills it**.
2. An excess whose log-slope is inconsistent with 2.

**Power, honestly.** The envelope is 2% at 236 kAU. The prereg notes the shape test needs ~2000 clean pairs per bin beyond
50 kAU, which DR3 lacks. A DR4 null at the per-cent level is consistent with this construction and with the gated branch.
A detection of the law's boost at ≤ 20 kAU kills both.
