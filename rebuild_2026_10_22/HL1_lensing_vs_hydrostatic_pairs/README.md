# HL1_lensing_vs_hydrostatic_pairs: NOT POWERED, by a hair and conditional on AMENDMENT_A1. g = +0.069 ± 0.043 dex on 50 clusters with both masses. A labelled bracket, never a framework grade

Criteria: `FROZEN_CRITERIA.md` (e9212275db, committed alone), `AMENDMENT_A1.md`. `hl1.py`, `hl1.out`, `hl1_results.json`, `hl1_MUTATE.out`. κ = ½ FITTED; not theory closed. Nothing here says the data favour the framework.

**As frozen, K1 fails** (3.31 % against 3 %), so there's no verdict. The amendment replaced K1 before any hydrostatic or gas value was read, and it needs the owner's acceptance. Under it, SE 0.043 is just over the 0.04 power line, so the class is NOT POWERED, and the ±0.014 offset doesn't change that.

## Numbers, Mahdavi+13, all at r500^WL, LITERATURE-INPUT
- **g = median log(M_WL/M_hydro) = +0.069 ± 0.043,** mean +0.050, rms 0.178. That's 1.6 SE from no gap and 1.2 SE from LF1's 0.12. It separates neither.
- **log Y_WL −0.097 ± 0.022, log Y_hyd −0.046 ± 0.023** (f★ 0.034); −0.085, −0.034 (f★ 0.0615).

## Post-result reading, not graded
| | this sample, one set of clusters | our other reads, different clusters |
|---|---|---|
| share on lensing mass, R500 | −0.097 to −0.085 ± 0.022 | LF1 M3, KiDS: −0.124 to −0.104 ± 0.054 |
| share on hydrostatic mass, R500 | −0.046 to −0.034 ± 0.023 | X-COP: −0.042, −0.031 |

Each column pair agrees within errors. That's suggestive: the same split between lensing and hydrostatic shares shows up inside one sample, so a KiDS-only shear bias or X-COP's selection alone looks less likely as the whole story. It's not established: the gap itself is 1.6 SE here, the masses are NFW fits, and the comparison was chosen after seeing the numbers.

Splits: M_WL above 6e14, g +0.108 ± 0.036; below, −0.022 ± 0.049. z above 0.232, +0.086 ± 0.052; below, +0.022 ± 0.056. **The mass split is cut on M_WL, whose noise itself drives g high above and low below, so it isn't evidence of a mass trend.**

## Limits
- Gas and M_hydro are read at r500^WL, so WL scatter moves all three together.
- X-ray-luminous sample, not eRASS1's. It says nothing about which of the two masses is right.
- Own KiDS shear on the same clusters can't do this: 3 hydrostatic clusters in the 326, none of X-COP's.

## Checks
K1 as frozen FAIL; A1 offset −3.31 %, width 2.0 %, PASS. K2 50 of 50 rows. MUTATE swap flips g exactly; shuffle rms 0.178 → 0.324, both BITE. Rerun byte-identical.
