# SM1_cluster_sample_match: X-COP and the lensing clusters differ in mass, in radius probed and in gas-mass definition

Criteria: `FROZEN_CRITERIA.md` (6a0406f8a7, committed alone, before any graded number); no amendment. Data-only; no model
enters.

**Implementation note:** RA/Dec are read from each cluster's gas file, because not every X-COP cluster has a stellar
file. This was a code fix before any graded number.

κ = ½ FITTED. Not "theory closed". Nothing here says the data favour the framework.

## Verdict (frozen): **DEFINITION MISMATCH + SAMPLE MISMATCH**

**(a) Mass.**
- Lensing sample (326 eRASS1 × KiDS clusters), M500 at 5 / 50 / 90 / 95 %: 4.4e13 / 1.8e14 / 4.3e14 / 5.6e14 M☉.
- X-COP: 3.5e14–9.0e14, with a median of 5.7e14, at the lensing sample's **95th percentile**.
- Only 17 % of the lensing sample is as massive as X-COP's lightest cluster.

**(b) The same clusters under both definitions** (5 matches within 3′ and Δz < 0.01; none of them is in the lensing
sample):

| X-COP | dlog R500 (eRASS − X-COP) | dlog M500 | dlog Mgas500 |
|---|---|---|---|
| A644 | +0.034 | +0.103 | −0.055 |
| A1644 | +0.015 | +0.044 | −0.116 |
| A3158 | +0.035 | +0.103 | −0.064 |
| A3266 | −0.059 | −0.177 | −0.111 |
| ZW1215 | −0.035 | −0.105 | −0.111 |
| **median** | \|0.035\| (signed +0.015) | +0.044 | **−0.111** |

R500 agrees within the 10 % line. **eRASS1's Mgas500 is systematically about 0.11 dex (≈ 23 %) below X-COP's** for the
same clusters, which crosses the frozen 0.1 dex line.

**(c) Apertures.** The lensing bands in each cluster's R500 (median R500 0.78 Mpc, against X-COP's 1.23 Mpc) are:
- INNER: 0.23–0.49 R500;
- MID: 0.71–1.50 R500;
- **OUTER: 2.18–3.17 R500.**

X-COP is graded at 0.1–0.7 R500, so the two data sets constrain **different radial ranges**. They overlap only at INNER
and the inner edge of MID.

## Reading (stated, not graded)

1. **GX1's "contradiction" is largely two data sets probing different places in different clusters.** X-COP is massive
   clusters inside 0.7 R500. The lensing sample is median clusters 3× lighter, mostly at 0.7–3 R500. No single-sample
   contradiction is established.
2. **The lensing budget inherits eRASS1's gas masses**, which run ≈ 23 % below X-COP's for the same clusters. GX1's
   infall halo with its edge at r_ta failed the lensing MID / OUT bands **UNDER**, the direction a low gas budget gives.
   The frozen follow-up (GX2) re-grades GX1's PRIMARY halo with the lensing sample's Mgas500 raised by the matched
   median, +0.111 dex. That is a data-calibrated correction from 5 clusters, disclosed as such.

## Checks: 3/3

- **K0:** the inputs load; every X-COP Mgas500 is finite.
- **K1:** the matches are unique.
- **K2:** at least one match.
- **Rerun:** byte-identical.
- **MUTATE twin** (match radius 0): no matches, K2 fails, exit 1.
