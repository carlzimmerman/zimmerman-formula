# WA1_wall_common_cause: PARTIAL, by the frozen rule. Shared shifts inside measured priors move many lines together, more than scrambled labels do, but no candidate comes near clearing. Every cell reads WALLS HOLD, joint p below 2.5e-4 on both footings, and the structural lines stay as they were

Criteria `FROZEN_CRITERIA.md` (90041a3158), committed alone first. `AMENDMENTS.md` (A1), post-result, written after one test fit of the law and before any other fit or label. **Not blind, heavily**: I knew every RQ3 row and the kills on BF2's forms, and chose the priors knowing which way each wall wants to go. Scripts `wa1_common.py`, `wa1_rows.py`, `wa1_resp.py`, `wa1_keys.py`, `wa1_fit.py`, `wa1_hat.py`, `wa1_report.py`, `wa1_k1_diag.py`, `wa1_m500.py`, `cand_bk2.py`, drivers `run_*.sh`. Numbers in `wa1.out` (full pull table per line), `wa1_results.json`, `wa1_summary.json`, `wa1_checks.json`, `wa1_checks_MUTATE.json`, `wa1_k1_diag.json`, `resp/`, `hat/`, `wa1_keys_min.json`. RQ3's harness is loaded unedited with its caches redirected here. kappa = 1/2 FITTED. Footings never pooled. No LCDM input, no Planck 5.364. The cold sector stays retired; the route-E row is a calibrator and reinstates nothing. Not theory closed. Nothing here says the data favour the framework.

## Answer
**The walls hold under honest marginalisation.** For every candidate on both footings, the best shared shift leaves chi^2 between 518 and 1219 on 45-53 lines, where mocks of a true candidate give a median near 50 and a 95 % line near 70. Empirical p is at the floor (2.5e-4 from 4000 mocks) in all 12 cells, the box fit (every shift within 2 sigma) is no better, and so is every sensitivity, including all priors doubled.

**The shared systematics are real, and they point somewhere, but not far enough.** Releasing nine nuisances removes 100 to 6000 in chi^2, and in 9 of 12 cells that drop beats scrambled line labels (p_scr < 0.05). That is the frozen PARTIAL. The fits use it by moving lines that share an input: Upsilon up 0.13-0.46 dex helps A5, A6, A26 and the stars-only rows together, and the hydrostatic shift moves X-COP and Lovisari together. But what's left is the same walls line-by-line grading named.

| Candidate | chi2_0 / chi2_prof, dim, canonical (alt) | Largest pulls, sigma | Still over |z| 2 at the fit (worst) | Label |
|---|---|---|---|---|
| a0 law | 4351 / 937, 53 (3892 / 960) | hse -6.5, lens -3.4, gas_abs +3.2 | X-COP to +11, B2, UFD +7.2, IC 1613, A17, A7 | WALLS HOLD |
| UX3, X-COP trained | 859 / 730, 45 (876 / 773) | lens -3.7, dist -2.0 (alt -3.7) | TDG +15, UFD +7.5, A30, IC 1613, G-OUT-all -3.4 | WALLS HOLD |
| BF2 P3 | 7129 / 1059, 50 (7118 / 1081) | lens -13, ups +3.9 | TDG +19, UFD, A5 driven to -5, A30 still +5 | WALLS HOLD |
| BF2 P7 | 6853 / 1215, 50 (6815 / 1219) | lens -12, ups +4.6 | TDG +23, A20 -5.0, A5 -5 | WALLS HOLD |
| MX1 cell P | 738 / 518, 53 (673 / 555) | lens -3.1, ups +2.1 | UFD +7.2, B2 R2500 +4.6, IC 1613, DF2, X-COP 0.1 -3.7, A17, A7 | WALLS HOLD |
| BK2 row (a) | 6081 / 976, 50 (5818 / 982) | lens -5.9, ups +3.8 | TDG +20, UFD, A5 -5, X-COP 0.7 -5.5, B2 +5 | WALLS HOLD |
| Route-E calibrator, no label | 653 / 372, 15 | dist +3.0, ups +2.6 | its own walls | none |

**Walls no shared shift touches:** MW ultra-faint dwarfs (+7 to +8 on every candidate), IC 1613 (-3.4 to -4.5), DF2 (-3.3 to -4.3), the TDGs for every gas-reading form (+15 to +23), and the MW scale length A17 and Upsilon step A7. **Structural lines stay as they were, as expected:** Bullet sign fails for all but MX1. Planets fail for all but BK2's row. MX1 fails equivalence on its own record. So no candidate could have reached CLEARS even with a passing p.

**Which nuisance helps most.** By the frozen census, `lens`: largest release in 5 cells. Read it carefully. That's P3's and P7's galaxy-lensing cutoff (A30 chi^2 near 880) asking for shear calibration 20 sigma off, which isn't a common cause. Next: `ups`, largest in 4 cells (MX1, BK2) and D >= 4 in all 12; then `hse`, largest for the law. Without priors, the law needs hse -8 sigma, gas +30 sigma and distance +13 sigma. MX1, the closest by chi^2, needs Upsilon +2.4 sigma, which is within reach, but its walls sit in dwarfs, groups and the Milky Way, where no shared shift reaches.

## Checks
| Check | Result |
|---|---|
| K0, every line against the scorecards on file at no shift | **PASS**, 0 difference on 15-38 rows and 15 keys per cell. My copies of B1, B2, X-COP reproduce RQ3 to print precision |
| Keys patch with tilt 0 against RQ3's cache | **PASS**, max dZ 0 |
| K4, BK2's row reproduces BK2's G8 M3 | **PASS**, max diff 0.003 |
| K1 known answer, single nuisance at 1.5 sigma | **PASS**, all five informed nuisances, both footings |
| **K1, combined injections (all +-1)** | **FAIL**, both footings: gas_abs recovered 1.37 / -0.02 against +-1, lens 0.58 / 0.24 against 1. The diagnostic (`wa1_k1_diag.py`, post-result) holds the uninformed nuisances still and it still fails. So the cause is cross terms the separable quadratic omits: lens with Upsilon in A30's chi^2, gas with hse and distance in X-COP and B2. **Pulls on gas_abs and lens are good to about 0.4-0.8 sigma, no better** |
| Closure, real rows rerun at the fit | **NOT CONVERGED in 11 of 12 cells** (rms 0.5 to 6.0). Fits sit beyond the 2-sigma nodes, where the quadratic extrapolates. Box fits inside 2 sigma don't do better (chi^2 522-4368) |
| K2 noise with priors, mean pull against shrinkage | **PASS**, max diff 0.034 / 0.046 |
| K3 mock calibration | **PASS**, 0.041-0.043 past the 95 % line |
| MUTATE, response signs flipped | **bites**: K1 fails all 14 injections on both footings |
| Byte-identical rerun of the final stage | **PASS**, sha256 6b3f1344... both runs |

**How strict the label is.** A true candidate drawn from these priors passes p and all pulls in 83-86 % of mocks, but only 61-69 % once untouched lines must also sit within |Z| 2. That gate is strict, frozen as briefed, and it changed nothing here. Line-only gates and structural lines can't be mocked.

## Sensitivities, no label
All 12 cells stay at p <= 1e-3 with every one of these: priors doubled; A12 in place of A13; RQ3's disputed rows dropped (12-14 lines left, chi^2 89-232); **post-result**, a 0.05 dex floor per X-COP bin, or X-COP dropped (the law falls to 556 / 585; MX1 to 494 / 532).

## What this says about the lines
- **X-COP's per-bin errors are tight** (cluster scatter about 0.01-0.03 dex), so X-COP drives the law's fit, and no flat hydrostatic shift fixes radial shape. A radially varying hse would be a new nuisance with no prior on disk.
- **Upsilon is the one place where common cause has teeth.** Every candidate wants it up 0.06-0.46 dex. But once A5, A6 are helped, A2's window (0.50-0.80 taken against U / 10^u) fails at the fit for every candidate. RQ3 had flagged this A2-A5 collision.
- **Line-only gates at the fit:** A2 and A21 fail for all; B24 fails for the law and MX1.

## Unfinished, and failed checks
- K1's combined injections fail: no cross terms in the response model. The fix would be a quadratic with interactions on A30, X-COP and B2, which isn't in the criteria and wasn't done. It can't turn chi^2 near 500 into a pass, but the gas_abs and lens pulls aren't to be quoted tighter than about 0.5 sigma.
- Closure NOT CONVERGED wherever a fit needs shifts beyond 2 sigma. The p values don't depend on it, since the box fit fails too.
- Keys weren't rerun at any fit, since no cell earned it.
- No cross-block statistical covariance exists on disk. Blocks are independent apart from the nuisances.
- Priors marked PROVISIONAL (ups, hse, dist, lens) come from web search summaries, not the papers. gas_abs has no independent absolute measurement on disk.
- Look-elsewhere: 12 cells, 108 single-release looks. BF2's and BK2's search trials (1.7e11, 2.7e10) can't be corrected here.
- A partial, gitignored directory `cache_keys/` from a killed run with a wrong mass unit is still on disk. A safety check refused its removal; the owner can delete it. Nothing reads it.
