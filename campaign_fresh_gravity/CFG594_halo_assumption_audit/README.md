# CFG594: halo-assumption audit (are the framework's halos a side effect of ΛCDM, or standard-MOND, assumptions?)

- **Audit:** `HALO_ASSUMPTIONS_AUDIT.md`. It lists 59 ingredients of the settled-cold-energy halo picture and of the growth/lensing pipeline (CFG424/518/527/530/539/541/542/544/550/554/555/556/557/559/590/591/592/593), each with file:line. They fall into five classes:

  | class | count |
  |---|---|
  | DATA-FORCED | 10 |
  | FRAMEWORK-DERIVED (2 of them posited) | 13 |
  | ΛCDM-INHERITED | 17 |
  | STANDARD-MOND-INHERITED | 7 |
  | CONVENTION / NUMERICAL | 12 |

  The audit ends with a ranked list of the inherited items most likely to drive the excess, each with a framework-native test that would remove it.
- **Quick check:** criteria in `FROZEN_CRITERIA.md`, committed alone first (d7fbcc267).
  - Script: `cfg594_sensitivity.py`, about 2 min. Run it with `OMP_NUM_THREADS=2 nice -n 10 python3 cfg594_sensitivity.py`.
  - Outputs: `cfg594_sensitivity.out` and `cfg594_sensitivity_results.json`.
  - `CFG594_MUTATE=1` writes the `_MUTATE` files and exits 1, meaning both teeth bite.
  - CFG556's halo model is exec'd read-only with one-at-a-time substitutions. The check measures the CONTEXT statistic only; it plays no verdict role.
- **Settings:** κ = ½ is FITTED. The footings 9.3603e-11 / 1.1312e-10 are never pooled. The cold energy's MASS is still required. This is not "theory closed". No PM runs and no downloads; other lanes were read only.

**Headline.**
- **Not borrowed: the halo's shape.** It is the law's round phantom of the retained baryons, cut off where the supply is exhausted.
- **Borrowed: the halo's amount, the catchment and the yardstick.**
  - The amount comes from cold energy clustering like CDM until turnaround, inside the ΛCDM turnaround ball, plus the census f_ret, which is measured relative to ΛCDM halo masses.
  - The yardstick is S0, ΛCDM's own P(k).
- **Quick-check drivers of the halo-model excess** (DRIVER means |ΔE| ≥ 0.25):
  - census f_ret: DRIVER;
  - supply amount: DRIVER;
  - the ΛCDM c(M) reference: DRIVER;
  - standard-MOND EFE: DRIVER. It is the only item that removes the excess on both footings (y_ext = 0.03). The framework's data-chosen no-EFE rule R7 is part of why its halos are concentrated.
- **Not drivers:** σ8, the mass function and the SHMR split are MINOR. Δ_ta and the kernel's low-y form are MODERATE.
- **The PM's QUMOND phantom** is not round and carries an implicit EFE, against R6/R7. The on-disk core-mass ratio (0.94–1.14) bounds this to about 15%.

**Disclosure.** The first execution had a sign error in the numerical-edge fallback, affecting M3/M4 only. It was corrected before commit.
