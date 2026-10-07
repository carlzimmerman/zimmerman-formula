# CFG395: is there a "fossil a0" in the outer HI discs of early-type galaxies?

## Verdict

**NON-DISCRIMINATING on both footings.** The early types sit +0.09 ± 0.10 dex *above* the late types. The slow-settling fossil predicts about −0.02 to −0.03 dex at these accelerations. The data are consistent with both no fossil and the fossil (they lie 1.1σ above the −0.02 threshold). The test cannot see the predicted signal: σ_Δ is 0.099, five times the 0.02 power limit set in the frozen criteria.

| footing | Δ = med(ETG) − med(late) | σ_Δ (boot / M/L ETG / M/L late / gas / bulge) | expected fossil signal | power \|pred\|/σ | verdict |
|---|---|---|---|---|---|
| canonical 9.3603e-11 | **+0.087** | 0.099 (0.068 / 0.064 / 0.033 / 0.003 / 0.006) | −0.022 (late f=1.00) / −0.032 (f=1.06) | 0.22–0.33 | NON-DISCRIMINATING |
| alt 1.1312e-10 | **+0.092** | 0.099 (0.069 / 0.063 / 0.033 / 0.003 / 0.007) | −0.022 / −0.033 | 0.22–0.33 | NON-DISCRIMINATING |

- The deep-limit fossil signal, 0.5 log(0.87/1.00–1.06), is −0.030 to −0.043. The ETG points sit at y = 0.05–0.85, so the expected signal there is smaller.
- **Why no sample size fixes this:** the coherent ±0.1 dex ETG stellar M/L alone contributes 0.064 > 0.02. A −0.04 dex fossil is exactly degenerate with an ETG M/L 0.08 dex lower. The test would need the ETG-to-late-type M/L ratio known to about ±0.03 dex. Cutting the bootstrap term with more galaxies does not help.
- The positive sign is not a result either. Sensitivities on Δ (canonical):

  | change | Δ |
  |---|---|
  | Υ_[3.6] = 1.0 | +0.025 |
  | Υ_[3.6] = 0.6 | +0.17 |
  | ATLAS3D r-band (M/L)_SFH, Chabrier, point mass | +0.22 |
  | Cappellari+11 distances | +0.089 |
  | gas 0 / 1 enclosed | +0.090 / +0.084 |
  | point-mass bulge | +0.075 |

  The sign and size of Δ follow the M/L choice.
- Nothing here says the theory is closed, and nothing here favours the framework.

## Task 1: what the record already had (CFG41 / CFG53)

- **CFG41/CFG53** use Di Teodoro+2023's 15 massive HI discs (log M_* 11.0–11.7).
  - Four have RC3 T ≤ 0: NGC 1167 (T −3), NGC 5790 (0), UGC 12591 (0) and UGC 12811 (−2).
  - Their baryons are point masses (WISE M_* plus 1.36 M_HI) with M_gas/M_* ≈ 0.1, so **no outer point is gas-dominated**.
  - Three of the four reach g_bar < 10^-10.5 (UGC 12591 does not).
  - The sample carries CFG41's HI-width selection bias, +0.076 dex in log v (0.152 dex in log g).
- **SPARC** S0–Sa (T ≤ 1, Q ≤ 2) gives six galaxies with deep points (NGC 4138, UGC 2487, UGC 3546, UGC 3580, UGC 6614, UGC 6786). None is gas-dominated, which is why session 06 found zero.
- So **no early type with gas-dominated outer points exists in the record**, and none in the new data either. Every ETG test of the fossil is star-dominated and M/L-limited.

## Data (fetches in FETCH_LOG.md)

- **No VizieR tables exist.** den Heijer+2015 (J/A+A/581/A98), Serra+2016 and Lelli+2017 all returned "not found".
- **den Heijer+2015 has no rotation curves.** It gives one outer HI circular velocity per galaxy.
- The measurement radius R_HI is tabulated in **Serra+2016 Table 1**. The [3.6] luminosity and the exponential-disc R_d and Σ_d come from **Lelli+2017's ETG table**, which uses Υ = 0.8 for rotating ETGs.
- `parse_sources.py` rebuilds `etg16_serra16_lelli17.tsv` from the two e-prints, checking their sha256 values.
- So the headline is **16 points, one per galaxy, at 8–28 kpc**, not rotation curves.

## Method (as frozen in FROZEN_CRITERIA.md, commit 7ee1f29dc)

- **ETG points:** g_obs = V_HI²/R_HI at Lelli's distances.
- **ETG baryons:** g_bar = Υ 0.8 × [Freeman thin disc + Hernquist bulge (a = R_eff,[3.6]/1.8153)] + 0.5 × 1.33 M_HI as a point mass.
- **Late types:** SPARC T ≥ 8, Q ≤ 2, Υ 0.5/0.7, every point inside the ETG g_bar window 10^-11.21 to 10^-10.10. That gives 51 galaxies and 335 points.
- **Kernel:** ν_mono, the FP1 kernel via CFG4_common, read-only.
- **Uncertainty:** galaxy bootstrap (4000 draws) plus coherent M/L, gas and bulge brackets, added in quadrature.

## Controls (failed ones kept)

- **C1 PASS.** Serra's V_HI equals den Heijer's v_circ for all 16 galaxies.
- **C2 FAIL (kept).**
  - The kpc part matches den Heijer's stated values: R_HI 7.9–28.2 kpc, mean 15.1, against 8–28 and 15.
  - The R_HI/R_eff part does not: 4.17–15.96 (mean 7.57) against den Heijer's 3.4–13.7 (7.3). Den Heijer evidently used a different R_eff than Serra's Table 1.
  - R_eff (Lelli's [3.6] value) enters only the Hernquist scale, and the point-bulge bracket moves Δ by 0.012.
- **C3 FAIL (kept).** For NGC 3626, NGC 3941 and NGC 5582, 2πΣ_d R_d² exceeds the total L. Lelli's decomposition is non-parametric, so the extrapolated central disc surface brightness over-counts. The disc was capped at L with no bulge (disclosed departure). The over-count is 1.2%, 6.3% and 16.5% respectively.
- **C4 PASS.** The session-06 SPARC late-type count of 27 is reproduced.
- **MUTATE (detected).** Adding −0.04 to the ETG residuals shifts the canonical Δ by −0.0400 and the run exits 1. The verdict stays NON-DISCRIMINATING.

## Secondary arms (reported only, as frozen)

- **S1, SPARC T ≤ 1:** 6 galaxies, 51 deep points. Δ = +0.053 ± 0.101 canonical, +0.055 alt.
- **S2, Di Teodoro T ≤ 0:** three S0s, 20 deep points. After subtracting the 0.152-dex selection bias, Δ = +0.095 ± 0.131 canonical, +0.099 alt.
  - Departure note: the frozen text said "0.076 dex". CFG41's bias is in log v, so it was applied as 2 × 0.076 in log g.

All three arms land on the positive side and none is below −0.02. Each has σ ≈ 0.10–0.13, so none can discriminate.

## Files

- `FROZEN_CRITERIA.md` (committed alone, first).
- `cfg395_fossil_a0_etg.py`, with `.out` and `_results.json`; the `_MUTATE` pair.
- `parse_sources.py` and `etg16_serra16_lelli17.tsv`.
- `FETCH_LOG.md`.

## What would make this test work

- Needed: early types with **gas-dominated** outer HI points, or an M/L calibration of ETGs relative to late types good to about 0.03 dex.
- Possible routes, all needing fresh approval: resolved outer HI rotation curves of gas-rich S0s (e.g. MeerKAT or WALLABY lenticulars), or dynamical M/L from inner stellar kinematics applied consistently to both types.
- Neither exists in the record. Without them, ETG HI cannot tell the fossil from no fossil.
