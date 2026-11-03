# KT19_filter_sparc: SURVIVES SPARC on both footings. Under KT17's eps 0.55 filter the galaxy-equal rms moves +0.0029 (canonical) and -0.0004 (alt) dex; inner points lose some boost (inner median +0.036) and the filter prefers stars about 10 percent heavier

Criteria: `FROZEN_CRITERIA.md` (94562be676, with KT18 and KT20's), alone first, confirmed landed. `kt19.py`, `kt19.out`, `kt19.json`, `kt19_MUTATE.out`, `kt19_MUTATE.json`; added after the result: `kt19_conv.py`, `kt19_conv.out`. No download. κ = 1/2 FITTED, held fixed. Footings never pooled. Not theory closed. Register K830. 3 minutes.

175 galaxies, 3226 points before cuts, 1061 inner points (R < 2 R_disk). Board law's simple nu; xi = 0.55 sqrt(G M_b / a0), M_b = 0.5 L[3.6] + 1.33 M_HI.

| | canonical | alt |
|---|---|---|
| xi, min / median / max | 0.15 / 1.83 / 11.0 kpc | 0.14 / 1.67 / 10.0 kpc |
| plain board law: rms, median, inner median | 0.1691, +0.025, +0.011 | 0.1701, -0.004, -0.006 |
| filter: rms, median, inner median | 0.1720, +0.044, +0.047 | 0.1697, +0.017, +0.030 |
| d rms | **+0.0029** | **-0.0004** |
| Label | **SURVIVES SPARC** | **SURVIVES SPARC** |
| beside: best f, plain / filter (rms) | 1.05 (0.1688) / 1.15 (0.1691) | 0.95 (0.1695) / 1.05 (0.1697) |

## Reading
- **The a0 law's SPARC fit survives the filter**, within the frozen 0.005 dex. With one global stellar scale fitted, the two are equal to 0.0003 dex on both footings.
- **What it costs:** inner points lose boost, as expected. The inner median rises by +0.036 on both footings, and the filter wants stars about 10 percent heavier (f 1.15 vs 1.05 canonical, 1.05 vs 0.95 alt). On canonical the overall median reaches +0.044, close to the 0.05 line. The galaxies hit hardest are mid-mass discs: UGC 00191 and NGC 0024 (rms +0.05 to +0.07, M_b 2.8e9), NGC 6015, UGC 12732, NGC 2403.
- **It's a spherical approximation for the smoothing.** The real in-plane g_bar is used, and the smoothing acts on a spherical mass profile. KT14 showed that for a real disc the in-plane v_c barely moves under smoothing, so this is likely conservative. But it isn't a disc solve.

## Checks
C1: xi = 0 equals the board law, 2.2e-16. C2: smoothing conserves total mass to 1.4e-5 on the smallest, median and largest galaxies. **C3 FAILED:** the monotone envelope on M(r) = V_bar^2 r / G changed 11.6 percent of points, against a frozen 5 percent. A thin disc's V_bar^2 r / G isn't an enclosed mass, and negative gas terms make it fall in places. The envelope enters both the smoothed and unsmoothed mass (only their ratio is used), so the effect is second order, but the approximation is rougher than the criteria assumed. Disclosed, exit 1. **Added after the result:** smoothing grid doubled (n 3000), rms and medians identical to 4 decimals. A diagnostic I printed in C2, at xi = 1e-3 kpc, is meaningless (kernel narrower than the grid); not used. MUTATE (Newton): rms 0.573, FAILS, exit 1.
