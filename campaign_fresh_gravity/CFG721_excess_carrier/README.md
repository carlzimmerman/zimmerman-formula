# CFG721: colour and structure carry the early-type lensing excess about equally

**Labels as frozen:** Part A **BOTH / UNDECIDED**; Part B **UNDECIDED** (continuous colour trend mildly preferred, Δχ² = −2.5).

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (94c4b06b3), 2026-10-13. Block CFG720–729.
- **Settings:** raw lensing only; no law, κ, footing or ΛCDM ingredient. Not "theory closed"; nothing here says the data favour the
  framework.
- **Script:** `cfg721.py` → `cfg721.out`, `cfg721_results.json`. MUTATE `CFG721_M=M1` (bin swap) and `M2` (colour shuffle within mass
  deciles) each exit 1 (both bite).

## Results

**Part A (B21 released isolated stacks, same g_bar, the 12 bins with g_bar ≤ 1e-12):**

| split | Δ = log10(ESD_2/ESD_1) | Z |
|---|---|---|
| colour (u−r ≥ 2.5 vs < 2.5) | +0.220 ± 0.030 | +7.4 |
| Sérsic (n ≥ 2 vs < 2) | +0.181 ± 0.029 | +6.2 |
| colour − Sérsic | +0.040 ± 0.042 | +0.95σ → BOTH / UNDECIDED |

**Part B (own stacks, matched Ks baryonic mass; u−r sextiles relative to the whole f30 sample, K9):**

| sextile median u−r | 1.38 | 1.64 | 1.84 | 2.08 | 2.30 | 2.40 |
|---|---|---|---|---|---|---|
| A | −0.11 ± 0.23 | −0.27 ± 0.16 | −0.11 ± 0.10 | −0.03 ± 0.06 | +0.01 ± 0.06 | +0.21 ± 0.08 |

- Step at u−r = 2.0: b = +0.208 ± 0.084, χ² 4.5 / 4. Continuous: c = +0.40 ± 0.14 per mag, χ² 2.0 / 4. Δχ² = −2.5 → UNDECIDED (continuous
  mildly preferred).
- MUTATE M2 (colour shuffled within mass deciles): b +0.11 ± 0.07, c +0.12 ± 0.14 (both within 2σ of zero): the trend is carried by
  colour, not by the reweighting.

## Disclosure (2026-10-13)

- The Part A covariance propagation raised a numpy `matmul` overflow warning. The inputs are moderate (covariance ≤ 51, ESD ≥ 0.43), and
  an independent pure-Python propagation reproduces both offsets exactly (+0.2204 ± 0.0300, +0.1806 ± 0.0290). The warning is spurious
  (a known Accelerate-BLAS artefact); the numbers stand.

## Reading

1. **The excess is not colour alone.** At the same baryonic acceleration, the structural split (Sérsic index) separates the lensing
   almost as strongly as the colour split (+0.18 vs +0.22 dex, both > 6σ, difference 1σ). With these data, a stellar-population property
   and a structural/dynamical property cannot be told apart; they are correlated in the sample.
2. **Within colour it looks like a smooth trend, not a switch.** At matched near-IR baryonic mass the lensing rises across the colour
   range (+0.40 per mag, about 2.9σ), with the reddest sextile carrying the most; a sharp step at the early/late boundary fits slightly
   worse. Not decisive.
3. **What would separate them:** a cross-split (red discs vs blue spheroids at matched mass). B21 released only the separate splits,
   and our lens table has no structural parameter. That is the next data need, not a calculation.
4. For the mechanism: whatever extra ingredient the law needs must correlate with both colour and structure. Dynamical state
   (pressure- vs rotation-supported) and halo-level formation history both qualify; stellar-population age inside early types does not
   (CFG667, CFG669).
