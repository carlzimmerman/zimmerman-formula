# CFG827 (= CFG824b) — the dwarf age test with each dwarf's own SFH-based stellar M/L

Criteria: `FROZEN_CRITERIA.md` (055269e4d, before the script). Run: `python3 cfg827.py` (MUTATE `CFG827_MUTATE=1`). Seconds.
M/L: E-MILES v11.0 SSPs (Kroupa, Padova00; `real_research/data/dsph/emiles_ml_dl/`, downloaded 2026-10-18 from the IAC MILES
site, sha256 8b516912c37b99cf…) integrated over each dwarf's Weisz+14 SFH.

## Result — CLASS: **NO SIGNAL**. The age trend of CFG824 was stellar M/L; H-FOSSIL (as an age effect) is not supported.
| out-of-sample N = 28 | Spearman ρ | one-sided p | slope (per Gyr) |
|---|---|---|---|
| CFG824, Υ = 2 | +0.42 | 0.012 | +0.040 ± 0.012 |
| CFG824, crude C-ML | +0.24 | 0.113 | +0.026 ± 0.012 |
| **CFG827, SFH M/L, [M/H] −1.31** | **+0.09** | **0.33** | **+0.010 ± 0.012** |
| CFG827, [M/H] −1.71 / −0.71 | +0.10 / +0.09 | 0.31 / 0.32 | +0.010 / +0.011 |
| CFG827, alt footing | +0.08 | 0.35 | |

- SFH-based Υ_V runs from 0.44 (Leo A) and 0.47 (WLM) to 1.95 (And VII); young gas-rich dwarfs had been given 4× too much
  stellar mass at Υ = 2, which put them on the law and manufactured the age trend.
- With the right M/L, the excess is **nearly uniform**: 25 of 28 independent dwarfs sit above the law, mean
  E = ln(σ_obs/σ_law) = +0.38 (σ ×1.45, mass ×2.1 inside r_1/2), with no age dependence. (Gas is omitted, as declared; for the
  gas-rich dIrrs that overstates their E, so the uniform excess is an upper bound there.)
- UFD re-check (Υ 2.20 for a 13.3-Gyr burst): binary-corrected UFDs E +0.68 ± 0.21 vs the (now flat) trend +0.41 ± 0.18
  (z +0.99) and vs the flat mean +0.33 (z +1.38): consistent with both; the CFG826 discrimination is gone.
- **Reading:** dwarfs carry a roughly uniform ~×2 inner-mass excess over the galaxy law, independent of when they formed.
  That points away from a formation-epoch mechanism and toward something every dwarf shares (a uniform shortfall of the
  law at low mass/acceleration, or bound cold mass in proportion to the stars). It is consistent with CFG821–823.

## Controls
- K1 PASS: an SFH at the 12.59-Gyr node gives Υ 2.1592 = the table.
- MUTATE bites: a 1-Gyr burst gives Υ = 0.318 for every dwarf (= table); a τ90 shuffle gives ρ +0.12, p 0.27 (not SUPPORTS).

κ = ½ fitted; cold energy mass required; not theory closed.
