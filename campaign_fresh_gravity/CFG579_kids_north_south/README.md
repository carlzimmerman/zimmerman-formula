# CFG579: KiDS North/South split of CFG529's f30 census-edge fail. LOW POWER as frozen; the excess is shared by both regions in proportion

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (d2b13b22e). (owner chat 10-09, "do the KiDS north/south split")
- **Runner:** `cfg579_run.py` executes CFG529's `cfg529_score.py` unedited with three asserted run-time substitutions (region mask on f30, covariance, output paths). Env `CFG579_REGION` ∈ {ALL, NORTH, SOUTH}, `CFG579_COV` ∈ {scaled, regionjk}. Outputs `cfg579_<REGION>_<COV>.json/.out`. About 15–30 s per run.
- **Regions:** NORTH Dec > −15° (27,593 f30 lenses, 25 patches, lens-weight share 0.452), SOUTH Dec < −15° (29,672, 25 patches, 0.548); disjoint and complete (C1 pass).
- κ = ½ fitted; footings never pooled; cold energy's mass still required; not theory closed.

## Controls
- **C2 identity: PASS exactly.** Region = all f30 reproduces CFG529's ΛCDM and census χ² in every cell (max |d| = 0).
- **C3:** all four substitutions applied exactly once.
- Regional runs exit 1 because CFG529's K2/K5 compare the f30 χ² to the full-sample value; their stack-P and ALL parts reproduce exactly (|d| 0). Expected by construction, not a defect.

## Result (PRIMARY covariance: CFG529's 50-patch f30 jackknife scaled by lens-weight share)
χ²/15 (p); census PASS needs Δ ≤ 4 and p > 0.01.

| region | cell | ΛCDM | census | Δ | census | Δχ²(census−ΛCDM) | expected (full × share) | LAW_RTA p |
|---|---|---|---|---|---|---|---|---|
| NORTH | A can | 16.51 (0.35) | 28.33 (0.020) | +2.13 | PASS | +11.8 | 10.4 | 0.007 |
| | A alt | 16.51 | 23.68 (0.071) | +3.26 | PASS | +7.2 | 6.0 | 0.032 |
| | B can | 15.58 (0.41) | 31.25 (0.008) | +1.30 | FAIL | +15.7 | 14.3 | 0.004 |
| | B alt | 15.58 | 25.76 (0.041) | +2.21 | PASS | +10.2 | 9.0 | 0.029 |
| SOUTH | A can | 16.62 (0.34) | 26.08 (0.037) | +2.94 | PASS | +9.5 | 12.7 | 0.007 |
| | A alt | 16.62 | 20.86 (0.141) | +4.28 | FAIL | +4.3 | 7.3 | 0.033 |
| | B can | 17.17 (0.31) | 31.66 (0.007) | +1.85 | FAIL | +14.5 | 17.3 | 0.003 |
| | B alt | 17.17 | 25.33 (0.046) | +2.93 | PASS | +8.2 | 10.9 | 0.025 |

ΛCDM passes in every cell (p 0.31–0.41). Variant (region-only 25-patch jackknife, Hartlap 0.33): much noisier;
NORTH loses all power (LAW_RTA p 0.31–0.49, census−ΛCDM −3 to −0.5); SOUTH Δχ² +6 to +27.

## Verdict as frozen: NEITHER region replicates in all four cells → LOW POWER
- Replication cells: NORTH 1/4 (B canonical), SOUTH 2/4 (A alt, B canonical).
- **The tooth fails on the alt footing in both regions** (LAW_RTA p 0.025–0.033 > 0.01): the half-samples cannot
  reject even f_ret = 1 there, so the split has no power on alt. On canonical the tooth holds (p ≤ 0.007).
- Strictly, NORTH A canonical (expected 10.4 ≥ 10) passes the census edge, which by the frozen ladder reads NOT
  REPLICATED for that one cell; every other non-replicating cell sits at or below the power threshold.

## Reading (not a verdict)
- **The CFG529 tension is not carried by one sky region.** In every cell the census−ΛCDM excess in each half is
  close to the full-sample excess times that half's lens-weight share (NORTH 7–16 vs 6–14 expected; SOUTH 4–15 vs
  7–17), always with the same sign. That is what a sky-uniform effect looks like, and it argues against an
  area-specific KiDS systematic.
- It does NOT rule out a survey-wide systematic (shear calibration, photo-z, stellar masses), which both halves
  share. Only an independent survey (DES Y3) can test that.
