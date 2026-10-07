# CFG442: expanding the gas-dominated a₀ rung. RUNG NOT ESTABLISHED; the expansion did not grow the usable anchor, and the verdict sample is still CFG397's 10 galaxies (log a₀ −9.953 ± 0.071)

Criteria dd851292c were committed before any script existed. Scripts: `cfg442_fetch.py` (downloads, FETCH_LOG.md) and `cfg442_rung.py` (about 2 min; most of it is the figure RANSAC). κ = ½ is fitted, never derived; both footings are reported. No DM particle; the cold mass is still required.

**Verdict as frozen.**
- C2 (the LT-route method control) FAILED, so per the frozen rule LITTLE THINGS is report-only.
- SR added no galaxy.
- The verdict sample is therefore S0 + SR = CFG397's anchor, unchanged: N 10, a₀ = 1.113e-10, σ 0.071 > 0.05. **NOT ESTABLISHED.**
- K1 passes (Υ 0.5 → 0.7: −0.033 dex).
- Against the reference values:
  - canonical 9.3603e-11: +0.075 dex (+1.1σ);
  - alt 1.1312e-10: −0.007 dex (−0.1σ);
  - PAPER43 8.3e-11: +0.127 dex (+1.8σ);
  - all consistent within 2σ.
- Even ignoring C2, the COMBINED sample (17 galaxies) has σ 0.096. It would be NOT ESTABLISHED on every route.

| sample | N gal (pts) | a₀ | log a₀ ± boot σ |
|---|---|---|---|
| S0 = CFG397 anchor (C0 reproduced exactly) | 10 (108) | 1.113e-10 | −9.953 ± 0.071 |
| SR (SPARC flow/UMa gas discs with CF4 TRGB/Cepheid) | 0 | — | — |
| LT only (report-only after the C2 fail) | 7 (126) | 6.79e-11 | −10.168 ± 0.318 |
| COMBINED S0+SR+LT (would-be primary) | 17 (234) | 9.81e-11 | −10.008 ± 0.096 |
| COMBINED without UGC 8508 (fallback distance) | 16 (216) | 8.94e-11 | −10.049 ± 0.093 |

**What happened, honestly.**
- **SR yielded nothing.** Of CFG397's 20 Hubble-flow/UMa gas galaxies, none has a CF4 TRGB or Cepheid modulus inside the frozen 1′ match. 4 are in CF4 with no ladder modulus; 16 have no CF4 entry within 1′.
  - Post-hoc note, not acted on: KK98-251's nearest CF4 entry (PGC 64824, 5.6′ away) carries TRGB 29.22. It is probably an NGC 6946-group neighbour. Even if it were the same galaxy, the rescale would be only ~3%.
- **LT route.**
  - Baryons come from the vector paths of the Oh+2015 arXiv-source disk–halo figures, calibrated on the VizieR total-curve markers. The axis calibration rms is 0.02–0.08 pt, and gas² + stars² reproduces the VizieR V_tot² − V_DM² to a median 0.03–0.17%. So the digitisation itself is faithful.
  - C1 removed IC 10 (calibration) and DDO 70 / NGC 1569 (V_bar mismatches of 26% / 40%).
  - DDO 216 and NGC 3738 have no gas-dominated points.
  - Seven new galaxies entered: CVn I dwA, DDO 52, 53, 133, 210, IC 1613, UGC 8508.
  - Their single-galaxy a₀ values scatter over the whole fit range: IC 1613 hits the lower bound (−10.80, with 57 points) and UGC 8508 the upper bound (−9.30). That is why LT's σ is 0.32.
- **C2 failure.** On the 3 overlap galaxies with ≥ 3 gas points in both routes, at the same distance, the LT route sits +0.196 dex above the SPARC route:
  - DDO 154: +0.08;
  - DDO 168: +0.49;
  - WLM: +0.31.
  - The difference lies in the rotation curves and gas maps (Oh's VLA curves with an asymmetric-drift correction vs SPARC's), not in the digitisation. Which one is right is not decided here.
- **Direction.** With LT included, a₀ moves down by 0.055 dex, from the alt footing toward the canonical one (9.8e-11). This sits between the footings and is not significant (σ 0.096). It comes from a route that failed its own control.

**Disclosed departures:**
- LT baryons are read from figure vector paths (arXiv source), not from a table;
- LT stars use the authors' SPS Υ_3.6, and K1 scales them by ×1.4;
- distance errors are not propagated (the same statistic as CFG397);
- UGC 8508's distance is the Hunter+2012 TRGB-paper fallback (DDO 70 and NGC 1569, the other two fallbacks, failed C1).

**MUTATE** (gas dropped): empty selection detected, exit 1.

**Owner items:**
1. Reaching σ ≤ 0.05 needs about 10 more ladder-distance gas-dominated discs with tabulated per-radius decompositions. Candidate sources:
   - Iorio+2017's online tables (MNRAS supplementary material, not on VizieR or in the arXiv source);
   - the EDD CMD/TRGB catalogue for SPARC flow galaxies outside CF4.
   Each needs a fetch go in the owner chat.
2. C2 says the Oh+2015 and SPARC curves of the same dwarfs give a₀ values up to 0.5 dex apart (DDO 168). Any future non-SPARC addition should pass the same overlap control.
3. The three fallback-distance assignments (Sakai+2004, Grocholski+2008, Dalcanton+2009) rest on Hunter+2012's reference choice. They were not re-verified against the papers.

**Files:**
- data/: VizieR Oh+2015 and Hunter+2012 tables, Sesame positions, and the figure sha256 manifest;
- ../_external_data/cfg442/: CF4 table2, the arXiv tarball and the extracted figures (git-ignored);
- outputs: `cfg442_rung.out`, `cfg442_rung_results.json` and `_MUTATE.out`.
