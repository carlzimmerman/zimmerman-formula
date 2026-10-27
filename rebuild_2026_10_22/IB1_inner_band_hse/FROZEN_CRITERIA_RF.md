# IB1 part 2, RF (regression fill): FROZEN CRITERIA (committed alone, before the script exists or any graded number)

Written 2026-10-26, at the owner's request: "replace the tercile sigma fill with sigma predicted from each cluster's own
Mgas500 via the KT clusters' sigma-Mgas500 relation, then regrade HG on all 15 cells, both footings."

Standing rules: κ = ½ FITTED. Footings never pooled. Cold dark energy, not matter. No ΛCDM number in the rule. Nothing
here says the data favour the framework. Not "theory closed".

## 0. What changes

HG (`FROZEN_CRITERIA.md`, 0669ca3fc9) is unchanged except for σ for the 220 clusters without kT.

**Fill RF.** This is the record's own alternative fill, IC1 D5, `IC1_inner_cluster_band/ic1b_diagnostics.py` (ef9496bfd5),
defined there before this lane:

    log10 σ = a + b log10 Mgas500

- Fit by OLS on the 106 KT clusters.
- σ is σ_KT = (kT/0.6 m_p)^½ in km/s.
- Mgas500 is the catalogue column `MY["Mgas500"]`, taken raw, without h rescaling, exactly as D5.
- One fit serves every footing and h cell.
- Applied to the 220 clusters without kT. The 106 keep their own kT.

Seen before freezing: IC1 D5 reports slope b = 0.139, and its core-law (not HG) G-IN-Mall under this fill. No HG number
under RF exists.

## 1. Which cells can move (stated now)

RF changes only clusters without kT. So the KT-only cells are **identical** to HG's run by construction: G-IN-all, G-MID-*,
G-OUT-all, G-OUT-T1..T3 and G-OUT-b. In particular, G-OUT-all (HG Z −2.02 / −2.27) still fails. **The 15-cell class can
therefore be at best TRADES.** It is reported, by `FROZEN_CRITERIA.md` §2's rule.

The informative grade is on the five cells that RF can move: G-IN-Mall, G-OUT-Mall and G-OUT-M1..M3.

## 2. Grade (per footing; a cell passes if |Z| ≤ 2 at both h; the verdict needs both footings to agree, else UNDECIDED)

| class | rule |
|---|---|
| **FILL-RESOLVED** | all five MGAS cells pass |
| **PARTIAL** | not all pass, but G-OUT-M3's max over h of \|Z\| is below HG-tercile's (5.02 canonical / 5.02 alt), and no MGAS cell that passed under HG-tercile fails |
| **NOT RESOLVED** | anything else |

**Reported:**
- the 15-cell class (by the frozen §2 rule);
- the fit (a, b, rms scatter in dex, n);
- the OUTER pred/meas split KT / filled per MGAS tercile, as `ib1_post_outer`.

## 3. Checks

- **K0.** With the tercile fill, the script reproduces HG's committed cells (`ib1_hse_halo_results.json`) to 1e-12.
- **K1.** The fit reproduces IC1 D5's slope, 0.139 at 3 decimals.
- **K2.** Peak RSS < 2 GB.
- **MUTATE** (`--mutate`, `_MUTATE` outputs). The fill uses slope −b, with the intercept refit through the KT means. K1 is
  run on the mutated slope and must FAIL, and the script exits 1. The grades are reported only.

## 4. Inherited (flagged)

- The OLS direction (σ on Mgas500) is the record's. Scatter and selection in Mgas500 make the slope shallower than an
  orthogonal fit. That is not corrected; other directions are not tried (stop rule).
- Mgas500 is from the ΛCDM-processed eRASS1 catalogue, as before.
- Everything in `FROZEN_CRITERIA.md` §6 still applies.

Outputs: `ib1_rf.py` → `ib1_rf.out` and `ib1_rf_results.json` (`_MUTATE`).
