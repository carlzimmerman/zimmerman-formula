# CFG17 — the cold budget with a stellar-mass-selected gas relation (xGASS)

Script: `CFG17_budget_xgass.py`, about 5 min.
- Outputs: `.out` and `_results.json`.
- MUTATE control: `_MUTATE.out` and `_MUTATE_results.json`. SPARC's gas is kept, the edges return to CFG12's, and H1 fails (rc = 1).
- The main run exits 1, because H1 and H2 failed.

Data: `real_research/data/xgass/`, with its provenance recorded.

## The question

CFG16 left CFG4's minimal conflict at the margin. The budget converts the GAMA stellar mass function into baryons using SPARC's gas fractions, and SPARC is HI-selected, so it over-weights gas-rich galaxies.

The xGASS representative sample (Catinella et al. 2018) measures gas at fixed stellar mass without that selection. It has 1179 galaxies, 375 of them HI non-detections, and weights that recover the same GAMA mass function.

## The method

This is CFG12's computation with the gas swapped.
- **Phantom ratio.** Each xGASS galaxy's phantom, with its own gas (1.33 M_HI), is divided by the phantom with SPARC's relation at the same M_*.
- **Rescaling.** The weighted mean ratio in 0.1-dex bins rescales the budget integrand. SPARC's relation is kept below 10⁹ M☉.
- **Grouping.** FG001's grouping ratio R (CFG11, D ≤ 15 Mpc) is recomputed with the xGASS mean gas.
- **Share.** The turned-around share is CFG12's.
- **Non-detections** are bracketed: gas at the upper limit (conservative), or zero.

## Results

**Controls**

| check | result |
|---|---|
| C1: with SPARC's gas, CFG11's committed R and CFG12's committed FG001 edges | reproduced exactly |
| C2: the xGASS weights against Baldry's SMF | within 4.9% per 0.25-dex bin |

**The phantom ratio, xGASS / SPARC relation (limits kept)**

| log M_* | 9.5 | 10.0 | 10.5 | 11.0 |
|---|---|---|---|---|
| ratio | 1.036 | 0.998 | 0.922 | 0.948 |

SPARC over-states the gas only above about 10^10.3 M☉. The swap is modest.

**The FG001 strict edge against CFG16's self-consistent KiDS floor**

| row | edge (limits kept / limits as zero) | KiDS floor | window |
|---|---|---|---|
| canonical P2 | **0.3483** / 0.3498 | 0.3409 | **open**, [0.341, 0.348] |
| canonical ν_mono | 0.3458 / 0.3472 | 0.3476 | closed by 0.0018 / 0.0004 |
| alt P2 | 0.2998 / 0.3011 | 0.3402 | closed by 0.040 |
| alt ν_mono | 0.2976 / 0.2989 | 0.3453 | closed by 0.048 |

- **H1** (canonical, both kernels) **FAILED**: ν_mono is 0.0018 short.
- **H2** (alt) **FAILED**.

## Standing

With the budget's gas measured on a stellar-mass-selected sample, CFG4's minimal conflict on the **canonical** footing sits within about ±2% in x:
- **P2** opens a window 0.007 wide.
- **ν_mono**, the contract kernel, misses by 0.0004–0.0018.

**This is at the margin, and not decidable at this precision.** The KiDS floor itself rests on:
- the lens bias (CFG16's upper estimate);
- the 2-halo template;
- CFG4's KIDS_TOL = +9.

The **alt** footing is closed, about 12% short.

The gas-fraction systematic that CFG4 flagged, "stars-only relaxes by ~30%", turns out to be small once the gas is measured: the budget edge moves by about +0.008.

Nothing here says the theory is closed.

## Update (CFG23 diagnostics, 2026-09-28)

This window was judged with CFG4's KiDS tolerance, +9 against the untruncated law. KiDS's own best edge (x_e ≈ 0.62, CFG21) beats that reference by 35–38. Against KiDS's own best, the budget's edge costs 40.9 (canonical P2), 47.8 (canonical ν_mono), 55.4 (alt P2) and 62.0 (alt ν_mono), which is 6.4–7.9σ (CFG23_diagnostics V4). The window is open only under the lenient tolerance. The caveat is the linear 2-halo template: it also makes Duffy-c NFW halos miss KiDS at R ≥ 0.6 Mpc. See CFG23_README.md.
