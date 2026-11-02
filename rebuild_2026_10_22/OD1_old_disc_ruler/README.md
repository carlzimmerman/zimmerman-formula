# OD1_old_disc_ruler: NOT SEPARATED [JEANS-DEPENDENT] [HZ-DEPENDENT]. Old-star dispersions remove DiskMass's support for light discs, and don't establish heavy ones. The answer turns on a correction known only to between about 1.2 and 1.9

Criteria: `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (fc5face2a5), committed alone first. `od1.py`, `sources.json`, `od1.out`, `od1_results.json`, MUTATE twins. **Not blind.** Owner's go, 2026-11-01. A data-side audit, no new mechanism. kappa = 1/2 FITTED. Cold dark energy is a gravitating field component, never a particle. Not theory closed. Nothing here says the data favour the framework. The 0.50 line isn't moved, and FG1, SP3, UL1 aren't edited. **No pass of anything.**

## Frozen result
r_old = r / c on UR3's one-zone estimator, 30 DiskMass galaxies, 1.5 h_R. c = σ_old / σ_single: S1 solar K-giants 1.431, S2 NGC 628 1.414, S3 NGC 6946 1.517. Line 0.90-1.10.

| Group | Row | r | c_lo 1.414 | c_mid 1.431 | c_hi 1.517 | J + H at c_mid |
|---|---|---|---|---|---|---|
| LAW | round rule, canonical | 1.250 | 0.884 | **0.874** | 0.824 | 1.004 |
| LAW | phantom disc, canonical | 1.475 | 1.043 | 1.031 | 0.972 | 1.160 |
| RESPONSE | native total EM1 f_Q | 1.080 | 0.764 | **0.755** | 0.712 | 0.848-0.864 |
| RESPONSE | hand EM1 f_Q | 1.088 | 0.769 | **0.760** | 0.717 | 0.854-0.871 |
| OFF | hand EM1 off | 1.365 | 0.965 | 0.954 | 0.900 | 1.072-1.092 |
| OFF | native total EM1 off | 1.282 | 0.906 | 0.896 | 0.845 | 1.006-1.026 |
| REF | Newton, no halo | 1.494 | 1.057 | 1.044 | 0.985 | 1.173-1.196 |

All rows are in `od1.out`. **Label: NOT SEPARATED at all three c.** HEAVY DISCS needs the law's row in the line or above it; the one-zone round rule falls 3-8 % below. J is the exact Jeans integral (CFG577), H the S4G thickness (CFG578), both tags only. With both, the round rule is IN at all three c (0.947-1.016) and the response rows stay below (0.800-0.881). **So the lean at the frozen c's is toward heavy discs, as a lean, not a label.**

Implied Υ at 3.6 μm, ungraded, from K with SP3's bracket 1.0-1.3: uncorrected 0.19-0.28; at the frozen c's 0.45-0.77. The response needs 0.32-0.42 at 150-250 km/s.

## What this changes
- **DiskMass's low Υ was the single-population reading.** MUTATE (a), no correction, returns LIGHT DISCS, with the response IN and the law above: that is SP3's and UL1's reading. It needs c near 1. S1, S2 and S3 all reject c near 1 in their inner discs.
- **SP3's DiskMass leg becomes conditional on c.** UL1's GSWLC leg and the Milky Way leg don't use c and aren't touched here. CFG576-578 already warned of this, and SP3 listed the young-tracer σ_z as open.
- **The 0.50 line isn't confirmed.** Implied Υ spans it, and NGC 6946 reads 0.4.

## Post-result, no verdict: c isn't one number
The frozen rule took each paper's stated summary. Their own tables, `od1.out`:

| Tracer | c | Where |
|---|---|---|
| Integrated light, the same 5100 Å region DiskMass uses | 1.65-2.21, median 1.88 | 0.6-1.2 h_dyn, errors ±0.2 to ±0.5 |
| Planetary nebulae | 1.02-1.28, median 1.21 | 1.4-3.6 h_dyn |
| Nearest 1.5 h_dyn, where r is computed | 1.21, 1.28, median 1.24 | NGC 6946, NGC 628 |

| c | Round rule, one-zone / J+H | Native f_Q, one-zone / J+H | Newton, one-zone / J+H |
|---|---|---|---|
| 1.24 | 1.007 / 1.157 | 0.870 / 0.987 | 1.204 / 1.365 |
| 1.43 | 0.874 / 1.004 | 0.755 / 0.856 | 1.044 / 1.185 |
| 1.88 | 0.664 / 0.763 | 0.574 / 0.651 | 0.794 / 0.900 |

**With J+H, the law and the response swap at c about 1.31-1.37.** Below it, the response is in and the law above. Above it, the reverse. The nearest-radius planetary nebulae point one way, and the stated summaries and integrated light the other. c 1.88 puts every row under the line, a pure Newtonian disc only just on it, so it can't carry across the sample at 1.5 h_R, or the integrated-light c and the planetary nebula c measure different things. The jump from about 2.0 at 1.1-1.2 h to about 1.25 at 1.4-1.6 h, at the change of tracer, looks like method as well as physics. I can't separate those here.

## Reported, no weight: two galaxies with same-population dynamics
| | NGC 628, V_max 180 | NGC 6946, V_max 170, SPARC V_flat 159 |
|---|---|---|
| Υ_3.6 | 0.75 ± 0.18 | stated 0.4; my weighted mean 0.356 ± 0.071, plain mean 0.444 ± 0.082 |
| V_bar / V_max at 2.2 h | 0.78 ± 0.11 | 0.76 ± 0.14 |
| Z against response 0.32-0.34 at 150-200 | +2.3, +2.4 | +0.2 to +1.5 |
| Z against law 0.46 at 150-200 | +1.6 | −1.45 to −0.19 |

- **The two galaxies disagree with each other** by more than the gap between the models. S3 ties NGC 6946's low value to its high star formation and non-stellar 3.6 μm flux, and says a 30 % correction would raise it to about 0.7. SPARC's luminosities aren't corrected the same way, so uncorrected 0.4 is the fair comparison.
- SPARC fits of NGC 6946 itself: law 0.43, response 0.31, off 0.53-0.57. Against 0.4 the law and response are about equally close. NGC 628 isn't in SPARC.
- Combined V_bar/V_max 0.772 ± 0.086. Median DiskMass rows: law 0.717 (Z +0.64), hand off 0.822 (−0.58), native off 0.817 (−0.51), native f_Q 0.627 (+1.69, at 1.5 h_R, not 2.2), Blumenthal 0.557 (+2.49). A mild lean against the full response, on rows from other galaxies.

## Limits
- **c from one neighbourhood and two galaxies, carried to 30 others.** No DiskMass spectrum was decomposed. A galaxy-by-galaxy two-component fit is what would decide this, and it isn't possible from published tables.
- S2 and S3 use planetary nebula and integrated-light fits that can trade σ_cold against σ_hot; their cold values at some radii are upper limits. Errors on Σ are 30-40 %.
- **Vertical factor:** S2 and S3 use the isothermal sheet, K = 2 in UR3's notation; the primary uses K = 1.5. CFG576: k = 2 raises round rule from 1.25 to 1.44. That's an upward push like J, and probably overlaps it. I didn't add them.
- Bracket K/3.6 is SP3's, not measured here. Response rows have no galaxy ids, so no [V-DEPENDENT] test on them; round rule at V >= 150 reads r 1.241, 0.867 at c_mid, 16 of 30.
- EM1 is fitted in every EM1 row. Background A only. κ fitted in law rows.

## Sources
arXiv:1511.06047, 1802.00465, 2010.03991. Numbers were read from PDF text, not a summariser, so nothing is tagged PROVISIONAL. The fetch tool cached the three PDFs (4.6, 2.0, 3.2 MB) in the session's cache. They aren't in the repo; `sources.json` holds the numbers, locations and sha256 prefixes. Search also found a 2016 A&A reanalysis of DiskMass and a 2026 NGC 628 planetary nebula sample, arXiv:2604.16045. Neither was read, and neither enters c.

## Checks
K1 1.4943, 0.8210. K2 all 13 rows read from file within 0.0006 of record. K3 three c's from `sources.json`. K4 identity draws. K5, K6 pass, and are weak: they're near-identities on this ratio statistic. Byte-identical rerun of `od1.out`, `od1_results.json`.
MUTATE: (a) c = 1 gives LIGHT DISCS, RESPONSE IN, differs from the real run. (b) Groups swapped on the real run stay NOT SEPARATED. (c) S1 × 3 trips K3, exit 1, NO VERDICT.

## Expectation on record
HEAVY DISCS 45 %, NOT SEPARATED 45 %, LIGHT DISCS 10 %. NOT SEPARATED came out, by the route I named: the round rule lands under the line. I expected this to weaken the lead, and it does, without killing it.

## Judgments, mine, not measurements
- Spiral discs at 150-250 km/s really are near Υ 0.3-0.4 as a sample median: about 30 %, down from SP3's 45 %. The main thing holding it up is GSWLC, the Milky Way and the planetary nebula c.
- What decides this: two-component fits to DiskMass-class spectra, or old-star dispersions and same-population thickness for a dozen or more galaxies. Neither is on disk, and neither can be run here.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
