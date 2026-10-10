# CFG585: do older early types carry more KiDS inner excess at fixed mass? NOT CONFIRMED [LOW POWER] as frozen — but older early types carry most of the excess (suggestive)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (6fc71e70f). (owner chat, "yes run the age test")
- **Scripts:** `cfg585_age.py` → `cfg585_age.out`, `cfg585_results.json`; MUTATE `CFG585_MUTATE=1` (random relabel) → `_MUTATE`;
  `cfg585_null.py` → `cfg585_null.out`, `cfg585_null_results.json` (POST HOC, disclosed, no verdict weight).
- **Machinery:** CFG531's `cfg531_kids.py` executed unedited up to its analysis (CFG529's validated f30 environment).
- **Age proxy:** u−r colour residual at fixed mass (KiDS LePhare, exact match for all 181,477 lenses). f30 early types 26,572;
  OLD = reddest third (8,843), YOUNG = bluest third (8,850); 0.254 mag apart; median log M* 10.800 / 10.800.
- κ = ½ fitted; footings never pooled; cold energy's mass still required; not theory closed.

## Result: ε = ΔM/M_pred
| cell | K-in: old / young | D (Z) | K9: old / young | D (Z) |
|---|---|---|---|---|
| A canonical | +0.763 / +0.117 | +0.646 ± 0.427 (+1.51) | +1.197 / +0.256 | +0.941 ± 0.354 (+2.66) |
| A alt | +0.616 / +0.025 | +0.592 ± 0.391 (+1.51) | +1.011 / +0.149 | +0.862 ± 0.324 (+2.66) |
| B canonical | +0.763 / +0.117 | +0.646 ± 0.427 (+1.51) | +1.195 / +0.257 | +0.938 ± 0.354 (+2.65) |
| B alt | +0.616 / +0.025 | +0.592 ± 0.391 (+1.51) | +1.009 / +0.150 | +0.859 ± 0.323 (+2.65) |

- **Verdict as frozen (K-in primary): NOT CONFIRMED [LOW POWER]** — D > 0 in every cell, Z = +1.51 (< 2).
- Controls 2/2: C1 matched masses; C2 CFG531's full-early ε(K-in) reproduced exactly (+0.5378).
- MUTATE (one random relabel): K-in |Z| = 0.70 in all cells, as required.
- **POST HOC (disclosed): 200 random relabels (A, canonical):** K-in real D +0.646 vs null +0.04 ± 0.44, one-sided p 0.085;
  **K9 real D +0.941 vs null 0.00 ± 0.33, p 0.005 (Z_emp +2.87)** — ≈ p 0.01 after a ×2 band-choice penalty.

## Reading (not a verdict)
- The shortfall sits mostly in the OLDEST (reddest) early types: young early types are close to the law (K9 ε ≈ +0.15–0.26),
  old ones far above it (≈ +1.0–1.2), at identical stellar mass. The direction matches the owner's settling-over-time idea.
- **It is suggestive, not established**, and colour at fixed mass is confounded:
  1. **Environment (most likely mundane cause):** redder early types at fixed mass are more often satellites / in denser
     surroundings; f30 still leaks 0.169 satellites (CFG519), and CFG509 found early lenses have 1.53× more massive
     neighbours. Colour-dependent leakage would add host-halo signal to OLD. Testable on disk with neighbour counts (no lensing).
  2. **Stellar M/L:** a residual M/L error correlated with colour; but closing ΔK9 needs ~0.5 dex in M_b between bins
     0.25 mag apart (deep-regime M_law ∝ √M_b), far above plausible colour–M/L slopes — an unlikely sole cause.
  3. Dust and metallicity also redden.
- A settling mechanism for cold energy still does not exist in the record; a positive environment-controlled result would
  make it the main lead.
