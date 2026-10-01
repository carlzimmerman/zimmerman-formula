# CFG274 stage 1 — the blind pre-flight: the eight Amvrosiadis+25 discs sit in the near-Newtonian regime, so none can be an a₀ point

> **κ = ½ FITTED. No velocity column was loaded; no g_obs, D, δ or s\* of any of the eight discs was formed. A forecast, not a measurement. No sentence says the data favour a law.**
> Criteria `FROZEN_CRITERIA.md` (**a7c4f7eef**) + `ADDENDUM_1.md` (after the first run, before any velocity was loaded). Script `cfg274_amvrosiadis_eight.py` (shared machinery `../HZQ_common/hzq_core.py`); outputs `cfg274_stageA.out`, `cfg274_stageA_results.json`; the first run is kept as `cfg274_stageA_firstrun.*`.

## Bottom line
1. **All eight discs are ILL-CONDITIONED (near-Newtonian at 2 r_e): none is drawable as an a₀ point.** The baryon-side acceleration g_bar at r = 2 r_e (stars + gas in one thin exponential disc with the CO half-light radius) gives **y = g_bar/a₀ = 15.6, 16.7, 52.8, 21.5, 29.6, 11.1, 75.1, 6.0** for 007.1, 022.1, 041.1, 049.1, 065.1, 066.1, 071.1, 075.1 (median 19.1; P6 25.5). The law at s = 1 would give D = ν_mono(y) = **1.044, 1.041, 1.014, 1.033, 1.024, 1.061, 1.010, 1.110**: a 1–11 % excess over Newton. A 0.03 dex change in the baryon mass destroys the root for seven of the eight in the noiseless world (their lever is unbounded for the rule); 075.1, the least Newtonian, has a lever of −11.5.
2. **What that means for the measurement.** A root exists only if the measured D exceeds 1, and a root slightly above the floor implies a large a₀ (D = 1.1 at y ≈ 20 gives s\* of several); the implied a₀ of these discs is a statement about a residual D − 1 of a few per cent, far below the stated V errors. The coverage test (noiseless world on each galaxy's baryons, a declared 10 % V error and the published M\* and gas errors) confirms it: **the 68 % interval covers the truth in 0.00–0.43 of the mocks for seven of the eight** (075.1 0.78) and the 95 % interval in 0.48–0.99; the intervals are conditional on having a root, so they are biased high. The failure is the finding, as the criteria said.
3. **Baryon knobs move g_bar by:** stars at 2 R_e,CO −0.04 to −0.24 dex (largest for the massive discs, −0.20 to −0.24; smallest for 065.1 and 075.1); R_e × 1.5 −0.118; R_e / 1.5 +0.023; spherical −0.126; helium × 1.36 +0.01 to +0.11 (largest for the gas-rich 049.1, 065.1, 075.1). In the near-Newtonian regime each of these moves the floor distance by its own size (0.1–0.2 dex), which is larger than the 1–11 % headroom: **the existence of a root is decided by the baryon model, not by the law.**
4. **2 r_e is below the beam major axis for seven of the eight discs** (0.31–0.83; 066.1 at 1.00): r_e is a deconvolved CO size and V_circ(2 r_e) comes from a kinematic model with the beam inside it.

## Decisions (the frozen map)
- **PF-D1 ESTIMATOR VALIDATED: True** (C1–C5 pass in the rerun). **PF-D2 ILL-CONDITIONED: 8 of 8.** **PF-D3 DRAWABLE as an a₀ point: none.** Every row is drawn as a marker only (a floor triangle if it has no root; a labelled open symbol with its interval otherwise), never as a measurement.

## Controls
- **C1** (rows, ids, finite inputs, CSV hashes) pass; **C2** (Freeman peak 0.3870, far field 1.0006, `gdisc` equal to CFG229's) pass; **C4** (estimator bit-equal to CFG223's) pass; **C5** (noiseless identity 7e-15) pass; **C6** reported (fails for the near-Newtonian rows by construction).
- **C3 FAILED in the first run and is restated by Addendum 1:** the frozen 1e-6 tolerance cannot be met by a CSV that prints five significant digits; all eight g_bar values equal CFG227's printed strings exactly (deviation up to 4.6e-5 is the file's rounding). The restated control passes. The first run is kept.

## Hand estimates (frozen before any number; kept as they fall)
- **HE1: the y clauses hit, the last clause misses.** y ≥ 5 for all eight and ≥ 10 for 007.1, 022.1, 066.1, 071.1 (hit); the lever clause is satisfied in the flagged sense (no root within ±0.03 dex); **"049.1 and 065.1 are the least ill-conditioned" is wrong** — compact discs have a high g at 2 r_e (y = 21.5, 29.6); the least ill-conditioned are 075.1 (y = 6.0) and 066.1 (11.1).
- **HE2 hit** (8 of 8 ILL-CONDITIONED, 0 drawable). **HE3 misses** (the noiseless-world rooted-draw 68 % half-widths are 0.41–0.44 dex for every row, not above 1 dex: conditioning on a root compresses and biases the interval).
- HE4–HE8 are scored at stage B.

## Disclosures
- The data entered only through the parent and best-fit tables' baryon and geometry columns (the velocity columns were excluded by `usecols`), and CFG227's committed `g_bar` column for the control C3 (no other column of that file was used).
- The first run used the flagged-lever reading of the ILL-CONDITIONED rule; Addendum 1 records it.
