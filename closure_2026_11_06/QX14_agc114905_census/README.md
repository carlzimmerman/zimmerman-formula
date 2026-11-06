# QX14: AGC 114905's environment does not supply the external field. NOT RESCUED (EFE excluded), both footings

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. One galaxy excludes nothing. Criteria: FROZEN_CRITERIA.md
(922b5e8167), committed alone before any download or graded number. The owner approved these catalogue queries in
chat on 11-06 (../QX4_udg/NEEDS_OWNER.md).

## Result

| | canonical | alt |
|---|---|---|
| QX4 window (Newtonian g_e/a0), reproduced (KA2) | 0.0756-0.2909 | 0.0768-0.2925 |
| M_req, Newtonian reading (tidal-limited) | 1.0e12 Msun at d >= 141 kpc | 1.8e12 Msun at d >= 172 kpc |
| Census neighbours with a spectroscopic cz within +-500 km/s and R_p < 1 Mpc | **none** | **none** |
| 2MPZ photo-z candidates, upper-bound masses (x 3) placed at R_p | 7, largest M_up 5.5e10; none qualifies | none qualifies |
| Large-scale field, record's Chae estimator (ks115): noclu-maxclu band | 5.5e-4 to 4.95e-3 a0 (E1 1.65e-3) | 4.6e-4 to 4.1e-3 a0 |
| Band top, maxclu + 1 sigma (0.453 dex) | 1.4e-2 a0, 5.4x below the window | 1.16e-2 a0 |
| Completeness at M_req | yes (2MPZ M* limit 2.3e9) | yes |
| **Label** | **NOT RESCUED (EFE excluded)** | **NOT RESCUED (EFE excluded)** |

- **AGC 114905 is isolated.** Within 0.75 deg and 3,500-7,500 km/s, NED and HyperLEDA list only AGC 114905
  itself, plus a supernova (ATLAS25fyt) about 12" from it. ALFALFA's other sources in the cone sit at about
  2,700 km/s or 14,651 km/s. The galaxy's environment field is about 1e-3 a0, typical of SPARC galaxies, against
  the 0.076 a0 the rescue needs.
- **The label does not depend on how g_e is read.** Under QX4's reading (g_e as the host's MOND field,
  M_req 3.4e9 / 6.4e9), no census object qualifies either, and the census is still complete there (2.3e9 <= 3.4e9).
- **The reading itself is corrected.** QX4's host bound read g_e as the host's MOND field. The 1D estimator puts g_e
  inside nu, so it is the Newtonian field. On that reading a rescuing host must be cluster-scale (about 1e12 Msun),
  and a Milky-Way-mass host at 100 kpc gives only 0.009 / 0.007 a0. That miss was stated in advance; it rescues only
  under QX4's reading. QX4's own CONDITIONAL label is unchanged by this lane.

AGC 114905's door therefore goes to **FAIL**. Every mechanism in the action fails it: QX4 iterations 1 and 3, and
now the environment for iteration 2.

## Known answers and controls

- KA2: the window recomputed from UD1 through QX4's law_v reproduces iter2.json exactly (|diff| 0).
- **KA1 MISSED its frozen 1e-6 line.** The record's estimator reproduces gext_vectors.csv to 2e-6 dex on CamB and
  UGCA444 but only 4.8e-5 dex on NGC 6195 (D = 127.8 Mpc). The CSV stores D to 0.1 Mpc and positions to 1e-4 deg, so
  the test inputs, not the estimator, set a floor of about 1e-4 dex. The line was set below the CSV's own precision.
  The miss is kept on the record. It is 4 orders of magnitude below the 0.7-dex gap between the field and the
  window. The 'full' mode is off by 0.003-0.03 dex, which confirms that 'ks115' is the record's mode.
- MUTATE-1: a planted host of 2 x M_req at its best distance is RESCUED on both footings, so the control bites.
- MUTATE-2: with no neighbours and a zero field, the result is NOT RESCUED, as required.
- Directed plant, reported: a Milky-Way-mass host (6e10 Msun) at 100 kpc does not rescue on the Newtonian reading
  and does on QX4's reading, as stated in the criteria.

## Downloads (owner-approved; raw files in _external_data/qx14_agc114905/, not committed)

| Query | Rows | Bytes | sha256 (first 12) |
|---|---|---|---|
| NED name lookup (srs/ObjectLookup) | 1 | 637 | 4b54e6c9a8ec |
| NED TAP cone, 0.75 deg, z not null | 777 | 64,426 | 616483ca364c |
| HyperLEDA meandata box (atlas.obs-hp.fr mirror) | 393 | 33,182 | a190b0e38589 |
| ALFALFA a.100 (VizieR J/ApJ/861/49 table2, CfA mirror), 0.75 deg | 8 | 5,352 | 0a70c4502ad0 |
| 2MPZ cone (SSA freeform SQL) | 46 | 4,636 | e458374705e6 |

Full URLs, UTC times and hashes are in QUERY_LOG.json. A generic User-Agent was used.

### Disclosed

- The first run failed at the NED TAP step: the column is prefphytype, not pretype. leda.univ-lyon1.fr redirected
  to its home page, and the CDS VizieR host timed out. After those fixes everything was re-downloaded; only the
  final run is logged.
- **Not in the criteria, decided before any graded number:** a neighbour with no photometry would take the 2MPZ Ks
  limit as its mass. No neighbour needed this rule.
- 2MPZ's kCorr column is the extinction-corrected Ks magnitude, the column NV2 also used.

## Files

FROZEN_CRITERIA.md, qx14_download.py, QUERY_LOG.json, qx14.py, qx14.{out,json}, qx14_MUTATE1.{out,json},
qx14_MUTATE2.{out,json}, census.csv (derived census table).
