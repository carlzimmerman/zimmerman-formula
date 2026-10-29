# SM1_cluster_sample_match: FROZEN CRITERIA (committed alone, before any graded number of this lane)

Written 2026-10-28, at the owner's request: "freeze and run a data-only comparison of the X-COP and eRASS1 x KiDS cluster
samples (mass range, R500 definitions, apertures) to see whether the shape tension is a sample or definition mismatch."

**Why.** GX1 (9319e09bc2) found that the derived infall halo fixes X-COP *or* the eRASS1 × KiDS lensing outskirts, not
both.

**Seen before freezing (disclosed).** The lensing sample's M500 percentiles: 5 %, 50 % and 95 % are 4.4e13, 1.8e14 and
5.6e14 M☉. The X-COP R500/M500 table shows 3.5–9e14 M☉.

**Standing rules.**
- κ = ½ FITTED.
- Not "theory closed". Nothing here may say the data favour the framework.
- No downloads; data-only (no model enters).

## 1. Comparisons (frozen)

**(a) Mass overlap.**
- **Inputs:** X-COP M500 (Ettori+19 table on disk) and the lensing sample's eRASS1 M500 (`x7_measure_percluster.npz`,
  326 clusters).
- **Reported:** the fraction of the lensing sample with M500 ≥ X-COP's minimum, and X-COP's median percentile within the
  lensing sample.

**(b) The same clusters under both definitions.**
- **Matching:** X-COP clusters are matched to the eRASS1 catalogue (on disk) within 3 arcmin and |Δz| < 0.01.
- **Per match:**
  - log(R500_eRASS / R500_X-COP);
  - log(M500_eRASS / M500_X-COP);
  - log(Mgas500_eRASS / Mgas500_X-COP), with X-COP Mgas500 from its own `fgas_profile` at R500.
- **Disclosed:**
  - eRASS1 M500 comes from its weak-lensing-calibrated scaling relations;
  - X-COP M500 is hydrostatic;
  - their cosmologies are as published, with no conversion (the record's L8 convention).

**(c) Apertures.**
- **Lensing bins:** INNER 0–2, MID 3–5, OUTER 6–7. Their physical radii come from the harness (X7 `Rmean` per
  cluster).
- **Conversion:** to units of each cluster's own R500.
- **Reported:** the median R/R500 range of each band.
- **Compared with:** X-COP's graded x = 0.1–0.7 R500.

## 2. Verdict (frozen)

| verdict | condition |
|---|---|
| **DEFINITION MISMATCH** | for matched clusters (≥ 3), the median \|log R500 ratio\| > 0.04 (10 %) or the median \|log Mgas500 ratio\| > 0.1 |
| **SAMPLE MISMATCH** | not a definition mismatch, but X-COP's median M500 lies above the lensing sample's 90th percentile, **or** the lensing OUTER band lies mostly beyond 1 R500 (median > 1.0) while X-COP stops at 0.7 R500 |
| **COMPARABLE** | otherwise |

Both mismatches can hold; both are reported. The label lists every condition met.

## 3. Checks and twin

- **K0.** The X-COP table and the npz load; N_lensing = 326. Every X-COP Mgas500(R500) is finite.
- **K1.** Each match is the nearest eRASS1 source within the cuts, and is unique.
- **Rerun.** The results JSON is byte-identical.
- **MUTATE (`SM1_MUTATE=1`, separate outputs).** The match radius is set to 0, so K1's "≥ 1 match" check (K2) fails and
  the run exits 1.

**Run:** `PYTHONHASHSEED=0 python3 -I sm1_cluster_sample_match.py`
