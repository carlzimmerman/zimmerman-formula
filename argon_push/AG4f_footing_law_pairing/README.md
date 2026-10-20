# AG4f: footing–law pairing. **PAIRS DEGENERATE (by construction)**; not mix-dependent; R sits 2.5σ above 1/√Ω_Λ

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (ff7df583f).
- **Run:** `OMP_NUM_THREADS=1 nice -n 10 python3 ag4f.py`, 152 s, 0.68 GB peak, exit 1 because K2 failed as frozen (below).
  `AG4F_MUTATE=1`: 166 s, 0.64 GB, R = 1 everywhere, so it bites.
- **Deviation from the frozen settings (disclosed):** the criteria said "runs only after NC2x ends". The owner relaxed the rule
  on 2026-10-20 ("small jobs under 1 GB RSS, single thread, a few minutes may run beside a 1024³ run"), so both runs went
  beside the live NC2x job. NC2x's swap did not grow (3.95 → 3.89 GB). Nothing statistical changed.
- **Settings:** κ = ½ fitted; not theory closed. T = a₀_alt/a₀_canonical = 1/√Ω_Λ = 1.20851 is an identity of the footing
  definitions, used only as a target.

## Result
| quantity | value |
|---|---|
| n=1 best a₀ (data) | 9.376e-11 ± 0.034 dex: on the canonical footing (+0.0007 dex) |
| n=2 best a₀ (data) | 1.159e-10 ± 0.032 dex: on the alt footing (+0.0105 dex) |
| R_obs = a₀(n=2)/a₀(n=1) | 1.2359 ± 0.0108; (R − T)/σ = +2.54 |
| W1 mocks (n=1 true, canonical a₀) | R = 1.2252 ± 0.0060: consistent |
| W2 mocks (n=2 true, alt a₀) | R = 1.2241 ± 0.0063: consistent |
| splits (deep fraction / SBdisk / gas fraction) | Δ z = +1.49 / −0.78 / −1.32: none reaches 3σ |

## What it means
- **The pairing is a calibration fact, not physics.** Whichever law is true, fitting the other law to SPARC-like data moves its a₀
  by the same factor, about 1.22–1.24. In W1 (n=1 true), n=2 returns about the alt footing's a₀. In W2 (n=2 true), n=1 returns
  about the canonical a₀. SPARC cannot say which pair is real.
- **The bookkeeping gain is real.** On SPARC, choosing the law and choosing the footing are one choice, not two.
- **The ratio is not exactly the footing ratio.** It sits 2.5σ above 1/√Ω_Λ, and it does not drift with galaxy type at the 3σ
  line.
- The closeness to 1/√Ω_Λ (about 2%) is therefore a near-coincidence of magnitude, not an identity. Counting it as evidence
  for the pairing would break the no-tautology rule.
- **The only discriminator is redshift.** If the alt footing follows its own density, as the canonical footing follows ρ_DE,
  the n=2 world is the a₀ ∝ H(z) world. That world is sealed as FLOOR at GS4_24110 for both stellar masses (AG4d, alt footing,
  R-H branch). The 2026-11-28 resolved gas decides it.

## Controls
- **K1:** AG4b's S3 is reproduced to 0.01 dex. PASS.
- **K2: FAILED as frozen.** The W1 mock with seed 101, fitted with n=1, returned 8.91e-11, which is −0.0214 dex from truth
  against the 0.02 dex line.
  - Across the 20 W1 mocks the per-galaxy MAP-Υ estimator recovers a₀ low by a median of 0.011 dex (W2: 0.006 dex).
  - The reading compares R_obs with mock R from the same estimator, so the bias cancels in the ratio and the reading is
    unaffected.
  - The tolerance was not changed after the fact.
- **MUTATE:** ν₂ := ν₁ gives R = 1 on the data and every mock. It bites.
