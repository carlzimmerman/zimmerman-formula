# DPR1: commit ids, the lead's re-run and one reader note (dated addition, 2026-11-12)

No number, class or line of the lane changes. RESULT.md stays as the lane wrote it. Nothing was sealed by the lane and
nothing is sealed here.

## Commit ids (local / origin)

| Commit | Local | Origin |
|---|---|---|
| FROZEN_CRITERIA (alone) | ded8ccd8e4 | e742adb2ee |
| Scripts and outputs | bcfea35c0d | 11dfd5e008 |
| RESULT (117 lines) | 2114feaa93 | 7834f2bb4c |
| RESULT trimmed to 99 lines | 0bfc6a6f37 | ba55130dc3 |

## Re-run by the lead

From a copy, one thread, no network, reading the KiDS cache the lane had rebuilt in scratch: `dpr1_ko2_r1.py` at the
median lens redshift and at z 0 (`DPR1_ZREF=0 DPR1_TAG=_z0`), then `dpr1_candidates.py`. `dpr1_ko2_r1.json`,
`dpr1_ko2_r1_z0.json`, `dpr1_candidates.json` and `dpr1_candidates.out` equal the committed files byte for byte; the two
`dpr1_ko2_r1*.out` logs differ only in elapsed-time and peak-memory stamps. 9 of 9 checks pass in both runs. (Run in the
wrong order, with the candidate table first, the table reports the cold reference as "not computed": it reads the two
JSON files.) The rebuild of KO2's cache itself was not repeated by the lead.

A reproduction of the arithmetic, not an independent re-grade. Its inputs marked PROVISIONAL in RESULT.md (Euclid's
area, shear products and source densities) were not checked.

## Reader note (the lead's reading; not graded)

The lane's answer is structural. On every candidate, form B as adopted lands on one of its two rivals: on the law
wherever a galaxy's own halo is probed, on the cold reference wherever the large scale is probed. So dated data can
kill it (Gaia DR4, Euclid's own-field statistic, the a0(z) units) and none can confirm it. A prediction of its own
would have to come from the joint between the two states, which no lane has found; two candidates for it were graded
the same day and failed (`closure_2026_11_12/SRJ1_settled_joint_clusters/`, `closure_2026_11_12/SRJ2_regime_split_joint/`).

One number from the lane's new computation, recorded here as post hoc and ungraded exactly as RESULT.md records it:
on KiDS the early-type own-field statistic reads 0.487 +- 0.071, against 0.034 / -0.001 for form B, 0.135 to 0.187 for
the record's cold reference and 1.00 for the law. The record's cold reference is an isolated halo with form B's own
share, not a full account of a galaxy's surroundings, so its distance from the data is not evidence about any rival.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
