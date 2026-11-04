# FN4d_lg_discs_star_counts: FROZEN CRITERIA (committed alone, before any download, script or number of this lane)

The council's CY4 ("count stars, don't fit Υ"), taken under an FN4 id. It bears on the Milky Way row: whether the Milky Way's failure is generic to discs weighed without dynamics. κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Footings never pooled: canonical a0 9.3603e-11, alt 1.1312e-10 m/s².

**Gate: the owner's yes for each download below.** Nothing runs before that.

## Question
Does the law fit the Local Group's discs when the stellar mass comes from resolved stars, with no Υ freedom? The record has no M31 or M33 rotation-curve test (CFG843 is satellites only), and the Milky Way is RF1's.

## Galaxies and data
| Galaxy | Stellar mass from resolved stars | Gas | Rotation curve | Distance |
|---|---|---|---|---|
| M33 (primary) | PHATTER SFH or mass maps (Lazzarini+22); else the PHATTER HLSP photometry (MAST hlsps/phatter, 574,197,120 B per brick) | HI (Koch+18), CO (Druard+14) | HI, Corbelli+14 / Koch+18 | TRGB or Cepheid |
| M31 | PHAT SFH maps (Lewis+15; Williams+17) | HI (Braun+09 / Chemin+09), CO (Nieten+06) | HI, Chemin+09 / Corbelli+10 | TRGB or Cepheid |
| LMC, SMC | published SFH or mass maps where they exist (e.g. Harris & Zaritsky) | HI | Gaia EDR3 stellar kinematics, HI | eclipsing binaries |
| NGC 6822 | only if a published resolved-star mass map exists | HI | HI | TRGB |

The published maps and curves are VizieR tables; their sizes were not obtainable today (CDS did not answer). Each download goes to its own folder under `_external_data/fn4d_lg_discs_2026_11/` with a `FETCH_LOG.md` (URL, time, bytes, sha256). A galaxy with no published resolved-star map is dropped, not filled with a colour M/L.

## Method
- Baryons: Σ★(R) from the map, deprojected with the HI kinematic geometry; Σ_gas = 1.33 (Σ_HI + Σ_H₂). Newtonian in-plane field of a thick exponential-free disc (the maps' own radial profiles), scale height 0.3 kpc (bracket 0.1–0.5).
- The law: the record's (RQ3 `candidates/law.py`), with the host's Newtonian external field in ν in CZ1's corrected one-zone form: M31's on M33, the Milky Way's on the Clouds, both from FN4b's estimator.
- Per galaxy: E(R) = log(g_obs/g_law) over the curve's radial range, its median, and χ² with the curve's errors plus distance and inclination errors propagated. Also the Υ_[3.6] the map implies, where a 3.6 µm profile is published.

## Labels (frozen), per galaxy and footing
- **LAW FITS**: χ² ≤ χ²₀.₉₅(n) and |median E| ≤ 2σ_E, with σ_E from the curve, the distance, the inclination and the map's stated mass error added in quadrature.
- **LAW SHORT** (needs more mass): median E > +2σ_E. **LAW OVER**: median E < −2σ_E.
- **NOT EVALUABLE**: the map or curve is missing, or a known answer fails.
- Across galaxies: **COMMON OFFSET** if three or more discs are offset the same way beyond 2σ_E; it goes to the Υ-scale ledger (CW8) as evidence against the law or against SPARC's Υ line, not as a fix.

## Known answers
- **KA1** a synthetic disc with the law put in is recovered with |median E| < 0.01 dex.
- **KA2** for M33, the Newtonian baryon curve from the maps reproduces the published stellar and gas contributions (Corbelli+14) within 10 % at every published radius.
- **KA3** each galaxy's total stellar mass from its map is within the map paper's stated error of its quoted value.
- **MUTATE**: every stellar map × 3. The label of at least one galaxy must change; exit 1.

## Compute
One thread, `python3 -I`, `nice`, under 1 GB. If only HLSP photometry is available, the map-making (SFH fits on CMDs) is a separate lane and this one stops at NOT EVALUABLE for that galaxy.
