# CFG566: the record's high-z estimators cannot tell feedback-ΛCDM from a₀ tracking ρ_DE (NON-DISCRIMINATING)

**Verdict: NON-DISCRIMINATING.**
- No row reaches power 1. The power is 0.06 for KMOS3D PT1 and 0.00–0.04 for the RC100 native quartiles.
- No truth is disfavoured on any row, including flat a₀.

The setup:
- Criteria were committed first, alone: **379260732**.
- Script: `cfg566_forward.py` (~30 s, niced).
- κ = ½ is fitted. The cold mass is still required and no dark-matter particle is added.
- ΛCDM is the comparator. Nothing here says the data favour the framework or ΛCDM, and the theory is not closed.

**One line (ledger):** CFG566: the committed high-z estimators (CFG270 KMOS3D PT1, CFG303 RC100 B Q1–Q4) were forward-modelled under a₀ ∝ √ρ_DE, flat a₀ and CFG565's feedback-ΛCDM. Result: NON-DISCRIMINATING (power ≤ 0.06), and the halo adds only ~0.17 dex in s★ at 2.2 r_d, not CFG565's ×4.9 g†.

## What was done
CFG565's ×4.9 is a g† fitted over a full z = 0 RAR. The record's high-z numbers are something else: CFG223's median-residual implied-a₀ estimator on one near-Newtonian point per galaxy. To compare like with like, this lane built mocks on each committed row's own galaxies (catalogue masses, measured radii and redshifts) and pushed them through the committed estimator. The estimator was exec'd from source, unedited. Three truths:
- **(A)** a₀(z) = a₀ × M-DEC(z), the chart's DESI curve (0.85 at z = 2.23). Both footings.
- **(B)** flat a₀. Both footings.
- **(C)** CFG565's machinery at each galaxy's z: Moster+13(z), DC14 and Dutton-Macciò c(M, z), with g_obs = g_bar + g_halo at the same radius.

The noise model, declared in advance:
- 0.20 dex per-galaxy mass error.
- 0.15 dex on g_obs.
- A shared ±0.15 dex baryon zero-point.
- For KMOS3D, the committed 0.61 dex recipe half-width (pressure, inclination, geometry, kernel).

## Results (median predicted s★; 16–84 %)
| row (committed value) | A canonical / alt | B flat canonical / alt | C feedback-ΛCDM | power |
|---|---|---|---|---|
| KMOS3D PT1, z 2.23, no gas in truth (obs 2.44) | 0.61 / 0.86 (0.001–4.7) | 0.77 / 1.06 | 1.10 (0.09–6.9) | 0.06 |
| KMOS3D PT1, CFG270 B2 scaling gas in truth | 8.3 / 9.2 (1.6–40) | 9.4 / 9.9 | 10.2 (2.0–49) | — |
| RC100 B Q1, z 0.81 (obs 1.48) | 0.97 / 1.26 | 0.94 / 1.28 | 0.94 | 0.02 |
| RC100 B Q2, z 1.36 (obs 1.01) | 0.93 / 1.24 | 1.01 / 1.26 | 0.99 | 0.03 |
| RC100 B Q3, z 2.01 (obs 0.84) | 0.81 / 1.20 | 0.98 / 1.23 | 1.23 | 0.00 |
| RC100 B Q4, z 2.26 (obs no root) | 0.78 / 1.10 (floor 29 %) | 1.01 / 1.23 | 1.39 (floor 18 %) | 0.04 |

- Every committed value lies inside every truth's central range.
- The tail probabilities are p_lo 0.66–0.73 for KMOS3D with no gas, p_lo 0.19–0.23 with B2 gas, and p ≥ 0.18 for every RC100 row (minimum: C on Q4, p_lo 0.185).
- **Diagnostic only, not a verdict input:** with no recipe systematic and no shared zero-point, KMOS3D PT1 gives A 0.89 (alt 1.04) against C 1.32. The power is 0.48, still below 1.

## Reading
1. **Through the record's estimator, the feedback halo barely shows.**
   - The halo raises the predicted s★ by about 0.17 dex (diagnostic medians 1.32 against 0.89). That is far from CFG565's ×4.9 in g†.
   - The likely reason is that the estimator samples one point per galaxy at 2.2 r_d (or R_e), where these compact discs are baryon-dominated (CFG270: median y 2.2). CFG565's g† rise is set by the whole RAR, including the low-acceleration outskirts where denser high-z halos dominate. The two numbers are different statistics, so CFG565's ×4.9 does not translate into a ×4.9 rise in the chart's s★.
2. **Even the ~0.2 dex that does survive is buried in the mass lever.**
   - With a ±0.15 dex shared baryon zero-point and the 0.61 dex KMOS3D recipe, each truth's 16–84 % range of s★ spans about 1–4 dex (floors included).
   - Removing both systematics still leaves power 0.48. The 0.20 dex per-galaxy masses and the 0.15 dex g_obs noise, acting through the near-Newtonian lever, are enough to hide it.
   - This is the expected outcome, shown here with numbers: **the separation needs resolved outer kinematics (low g_bar) plus measured gas, not more inner points.**
3. **Gas matters more than the law.**
   - Adding CFG270's B2 scaling gas to the truth moves every prediction from ~1 to ~8–10. The shift is the same for all three truths.
   - The committed 2.44 sits between the no-gas and B2-gas predictions for every truth. This repeats CFG270's point (B2 gas overshoots the dynamics) in forward-model form.

## Controls
4 of 4 pass (`cfg566_forward.out`):
- **K1:** CFG270 PT1 is reproduced from its own inputs: 2.4414 against the committed 2.4413.
- **K2:** RC100 B Q1–Q4 are reproduced through CFG223's `analyse` (1.4834 / 1.0143 / 0.8418 / no root).
- **K3:** a noiseless injection returns the median a₀(z_i)/a₀ of 0.8495 exactly, and flat returns 1.000000.
- **K4:** the Moster z-terms vanish at z = 0.

**MUTATE** (`--mutate`; the A and C labels are swapped): the C-labelled KMOS3D median moves by 0.199 dex, which is detected (exit 1). The verdict word does not change (it stays NON-DISCRIMINATING), as expected for an unpowered test. Files: `cfg566_forward_MUTATE.out` / `_results.json`.

**Hand estimates (kept as they fall):**
- **HE1 MISSED:** A predicted 0.61, not 0.6–1.2 on the low edge, and C predicted 1.10, not ≥ 2. The feedback prediction through this estimator is much lower than expected.
- **HE2 hit:** the power is < 1.
- **HE3 MISSED:** the diagnostic power is 0.48, not ≥ 1.

## Disclosures and scope
- **MUSE-DARK native routes were not run**, as declared in the criteria. Their g_obs is a DC14 halo-fit output, they sit at z ≤ 1.2, and their recipe widths are 0.74–0.93 dex.
- KMOS3D PT1 and RC100 share 14 galaxies, so the rows are not independent. They were never combined.
- C is built as follows:
  - The halo mass comes from Moster at the catalogue stellar mass.
  - DC14 is used at its z = 0 calibration, as in CFG565.
  - CFG565's size-evolution law is not used, because the measured radii are.
  - The C model spread is the per-galaxy SHMR (0.15 dex) and concentration (0.11 dex) scatter. CFG565's 16–84 % g† spread is a different statistic and was not transferred.
- The recipe half-width is treated as 1σ and added only to rooted realisations.

## Files
`FROZEN_CRITERIA.md`, `cfg566_forward.py`, `cfg566_forward.out`, `cfg566_forward_results.json`, `cfg566_forward_MUTATE.out`, `cfg566_forward_MUTATE_results.json`.
