# CFG309 — MIGHTEE-HI catalogue W50 velocity frame: REST-FRAME by the frozen rule (documentary path b); the cube busy-fit test leans observed-frame but is inadmissible

*Criteria frozen in `FROZEN_CRITERIA.md` (commit `ec54de4ac`) before the paper text, the ALFALFA documentation or any spectrum was read. This is a convention check, not an a₀ measurement; the a₀ values below are a labelled consequence. κ = ½ is FITTED. No downloads, and no other lane's file was edited.*

## Bottom line
- **Frozen outcome: REST-FRAME, via path (b).** The catalogue paper's own worked numbers fix the conversion, and our column equals those numbers. No admissible data test contradicts this. So **CFG306's C1 is CONFIRMED**: CFG301's extra division by (1 + z) biases a₀ low by 0.098 dex.
- **What decides it is documentary, not independent data.**
  - T1: the paper never states the frame in words.
  - T2: the conversion is exact. In all five Appendix-D examples, the printed km s⁻¹ = channels × c Δν/ν_obs, with a constant +0.067 % offset (the paper uses c = 3 × 10⁵) and a spread of 1.4 × 10⁻⁵. So the channels are the measured quantity, and the km s⁻¹ values are rest-frame by construction.
- **Caveat, stated plainly.** The only independent quantitative test with power (T4, cube busy fits) **leans observed-frame**. Under the zero-offset assumption it reads:
  - m_R = −0.017 dex, whose 95 % interval excludes 0;
  - m_O = +0.003 dex.

  REST missed exclusion at the frozen 0.010 dex method tolerance by only 0.0004 dex. T4 is **inadmissible** because INJ-B failed: the REST world returned REST in only 13 of 20 realisations, so T4 cannot reliably confirm REST even in ideal injections.
  - Post hoc, using the catalogue's own definition (50 % of the *average* of the two peaks) removes +0.003 dex of the lean, leaving m_R −0.0095.
  - The z-tercile pattern is not the clean −log(1 + z) trend that OBS predicts: the middle tercile is lowest.
  - A residual method offset of about 0.01–0.02 dex is plausible from the different cube, beam, aperture, confusion and spectral filtering (CFG302 PH1/PH3). It is not demonstrated.

## Tests
| test | result |
|---|---|
| **T1, the paper's text** (MM26, arXiv:2605.28731) | **IMPLICIT-{REST, OBS}.** No sentence gives the frame. "rest frame", "observed frame", "(1+z)", "convention" and "cosmological broadening" never occur. The only statement is that the channel velocity width is "calculated for the given redshift" (5.5 km s⁻¹ at z = 0), which excludes RADIO. The column description (§4.7, col. 13) says only "measured at 50% of the flux peak ... not inclination corrected". §4.5 defines W50 at 50 % of the **average of the two peaks** of an emcee-fitted busy function (n = 2). |
| **T2a, conversion** | **REST.** For each of the 5 examples, dev_REST = +0.00066 to +0.00068 against allowances of 0.0027–0.0062. OBS is off by −0.016 to −0.083, and RADIO by +0.017 to +0.091; both are excluded in 5 of 5. W100 and the printed `vchannel` agree with REST. |
| **T2b, link to our column** | **1** (identity), in 4 of 5 examples. Example 1 (MGTH_J100404.9+014303: printed 237.858, catalogue 223) instead matches the radio-like ÷(1 + z), to 0.47 km s⁻¹. It is the row with the 3-decimal z (CFG304 K2). Disclosed as an anomaly. The paper's Table 3 W50 equal our CSV in 8 of 8 rows. |
| **T2c, exactness** | **EXACT** (spread 1.4 × 10⁻⁵, limit 2 × 10⁻⁴). This excludes the reading in which the channel counts were derived from catalogue km s⁻¹. |
| **T3a, ALFALFA frame** | **ALFA-OBS.** The CDS ReadMe calls W50 "Observed velocity width". The H18 documentation applies instrumental broadening correction only, with no cosmological stretch correction. |
| **T3b** (CFG304's 15 code-1 pairs, median z 0.028) | **UNDECIDED, as predicted.** median(d + x) = +0.0025 (95 % −0.023 to +0.024); median(d) = +0.000 (95 % −0.033 to +0.005). The hypotheses differ by only 0.012 dex. Theil–Sen slope +0.29. **C-SHUF PASS** (0.037 against a shuffled 1st percentile of 0.100). |
| **T4, busy fits** (54 of 58 GOOD) | **m_R −0.0168** (95 % −0.0267 to −0.0096); **m_O +0.0028** (−0.0048 to +0.0120); T4L UNDECIDED. **Slope −0.22** (95 % −2.13 to +1.51); T4S UNDECIDED. Primary vote UNDECIDED. In the level test, variants V1 (no neighbour) and V2 (n = 4) exclude REST, and V4's slope favours REST; no variant vote is the opposite frame. **R0 PASS** (≤ 4 × 10⁻¹⁰). **INJ-A PASS** (bias −0.0033 dex). **INJ-B FAIL** (REST world 13/6/1 REST/UNDECIDED/OBS; OBS world 20/20 OBS), so T4 is **INADMISSIBLE**. |

## Consequence for CFG301 (`cfg309_cfg301chain_FRAME.py`: CFG301's committed source exec'd with k = 0)
| frame | pooled a₀ (m s⁻²) | 68 % | 95 % | vs 9.3603e-11 | vs 1.1312e-10 | κ (canonical / alt footing) |
|---|---|---|---|---|---|---|
| **REST (decided), k = 0** | **1.311 × 10⁻¹⁰** | 1.273–1.418 | 1.206–1.669 | +0.146 dex | +0.064 dex | **0.700 / 0.580** |
| OBS (CFG301 as committed), k = 1 | 1.046 × 10⁻¹⁰ | 1.012–1.145 | 0.936–1.311 | +0.048 dex | −0.034 dex | 0.559 / 0.462 |

- **The k = 0 run in detail:** recipe half-width 0.128 dex; windows 1.348 / 1.305 / 1.416 × 10⁻¹⁰ (W3 − W1 +0.022 dex); CC1, CC3 and "calibrated" all still pass (W1 vs SPARC +0.050 dex); A1 BTFR (i) 1.530 × 10⁻¹⁰.
- **Controls:** C-ID reproduces CFG301 to 0.0, and C-CONS agrees with CFG306's 1.3111e-10 to 2 × 10⁻¹⁶ dex.
- **What this does not say.** Both footings fall outside the 95 % *statistical* interval on the catalogue flux scale; the recipe half-width of 0.128 dex covers both. The flux-scale systematic (CFG304/CFG306 M1, gas-only 0.90–1.06 × 10⁻¹⁰) is separate and is not addressed here.

## Controls and checks
- **Main run: 10 of 11 checks pass.** INJ-B is the one FAIL, and it is kept.
- **MUTATE (W50 × (1 + z)): 11 of 12 pass.**
  - **M-a PASS:** the link moves 1 → (1 + z).
  - **M-c PASS:** the decision flips from REST-FRAME to OBSERVED-FRAME. T4's raw vote becomes OBS (m_O −0.017, REST excluded).
  - **M-b FAIL, kept:** Δ_MUT − Δ_main = −log(1 + z) to 3.8 × 10⁻¹¹, against a 1 × 10⁻¹² tolerance. This is a design flaw in the check: it reads the main Δ back from a CSV written with `%.10g`. The fits are identical, but the check cannot show that at 1e-12.
- **Harness: 3 of 3 pass.**

## Errors and corrections
- **The in-script post hoc line in the main run is WRONG.** `POSTHOC_avg_two_peaks` (m_R +0.27; W50avg/W50max 1.95) took far-wing numerical bumps as "peaks". It is superseded by `cfg309_posthoc.py` PH1, which uses peaks of at least 0.2 P (W50avg/W50max 1.007). No frozen number used it.
- **The harness crashed silently on its first attempt.** CFG301 ends with `sys.exit`; the harness now catches `SystemExit`. No harness output existed before the fix.
- **Hand estimates:**
  - HE1 hit. HE2 hit. HE3 hit.
  - HE4: INJ-B failed, as I had leaned.
  - HE5: m_R −0.017 is in range; the vote was UNDECIDED.
  - HE6: REST-FRAME via (b), hit.
  - HE7 hit. HE8 hit.

## Files
- `FROZEN_CRITERIA.md`
- `cfg309_width_frame.py`: writes `cfg309_width_frame{,_MUTATE}.out` and `_results.json`, and `cfg309_per_galaxy{,_MUTATE}.csv`.
- `cfg309_cfg301chain_FRAME.py`: writes `cfg309_cfg301chain_stageB_{FRAME,IDENTITY}.*` and `cfg309_cfg301chain_FRAME_summary.{out,json}`.
- `cfg309_posthoc.py`: writes `.out` and `_results.json` (not frozen).
- **Reproduce:** `python3 cfg309_width_frame.py; MUTATE=1 python3 cfg309_width_frame.py; python3 cfg309_cfg301chain_FRAME.py; python3 cfg309_posthoc.py`. The run takes about 5 minutes, and the cubes come from `$MIGHTEE_R1P0_DIR`.
