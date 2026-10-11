# CFG589: ACE late-type colour clock at exactly matched mass. UNDECIDED as frozen: early clock robust, late clock positive but not significant

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (939124651). Model: `../MODEL_accumulating_cold_energy_2026-10-10.md`.
- **Scripts:** `cfg589_late.py` → `cfg589_late.out`, `cfg589_results.json`; MUTATE `CFG589_MUTATE=1` → `_MUTATE`;
  `cfg589_null.py` → `cfg589_null.out`, `cfg589_null_results.json` (POST HOC, disclosed: prompted by the MUTATE draw reaching Z ≈ 2).
- **Construction:** mass-stratified colour tertiles (thirds inside each of ten mass bins) — both classes' tertiles share one mass
  distribution exactly (C1 spread 0.000 dex for both; fixes CFG588's late-type C1 failure).
- κ = ½ fitted; footings never pooled; cold energy's mass still required; not theory closed.

## Result (K9 primary)
| cell | early ε (blue→red) | late ε (blue→red) | b_early (Z) | b_late (Z) | difference |
|---|---|---|---|---|---|
| A canonical | +0.08 / +0.75 / +1.23 | −0.47 / −0.46 / +0.08 | +4.46 ± 1.30 (+3.44) | +1.65 ± 1.00 (+1.66) | 1.38σ |
| A alt | −0.01 / +0.60 / +1.04 | −0.52 / −0.50 / −0.01 | +4.08 ± 1.18 (+3.44) | +1.51 ± 0.91 (+1.66) | 1.38σ |
| B canonical | +0.08 / +0.75 / +1.23 | −0.47 / −0.45 / +0.08 | +4.44 ± 1.29 (+3.44) | +1.65 ± 1.00 (+1.66) | 1.38σ |
| B alt | −0.01 / +0.60 / +1.04 | −0.52 / −0.50 / −0.01 | +4.06 ± 1.18 (+3.43) | +1.51 ± 0.91 (+1.66) | 1.38σ |

- **Verdict as frozen: UNDECIDED** in all four cells (late slope Z +1.66 < 2; slopes differ by only 1.38σ, so neither SAME CLOCK
  nor NO LATE CLOCK). K-in reported: early Z +1.74, late Z +0.30.
- Controls 3/3: C1 exact mass match in both classes; C2 early slope Z ≥ 2 in every cell.
- MUTATE (δc shuffled within class × mass bin): late |Z| < 2 (passes), but that single draw reached early Z +2.03 / late +1.82.

## POST HOC calibration (100 shuffles, A canonical, K9)
| class | real slope | null mean ± sd | median jackknife σ in null | Z_emp | empirical p | null draws with jk Z ≥ 2 |
|---|---|---|---|---|---|---|
| early | +4.46 | −0.14 ± 1.26 | 1.07 | +3.65 | ≤ 0.01 | 1% |
| late | +1.65 | −0.23 ± 1.20 | 1.01 | +1.58 | 0.089 | 2% |

- The jackknife errors understate the true scatter by ≈ 18–20%; deflate the jackknife Z values of CFG585–589 by about that
  factor. The MUTATE's Z ≈ 2 draw was a ≈ 2% tail event.
- The early-type clock survives calibration (Z_emp +3.65). The late-type clock does not reach significance (Z_emp +1.58).

## Reading (not a verdict)
- At exactly matched mass, redder early types carry much more excess (≈ +0.1 → +1.2 across 0.25 mag): a robust within-class clock.
- Late types show a positive slope about a third as steep (≈ +1.6 vs +4.5 per mag), not significant (p ≈ 0.09), and not
  significantly different from early types either (1.4σ). ACE's "same clock everywhere" is neither confirmed nor excluded;
  the data mildly prefer a weaker clock in discs.
