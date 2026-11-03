# KT22_filter_mw_share_threshold — FROZEN CRITERIA (before the script or any number)

Question: KT18 found no Milky Way pass under KT17's eps = 0.55 filter at the star-count thick share 0.12, and KT17's passes
sat at 0.26-0.35. The box has nothing in between. **At what thick-disc share does the filter first pass?** Star counts give
0.12 +- 0.04 (RF1 A4, BH&G16 §5.1.3), so the shares run are **0.16 (+1 sigma) and 0.20 (+2 sigma)**.

κ = 1/2 FITTED, held fixed. Both footings, never pooled. Not theory closed. No download.

**Not blind:** KT18's best cells are known (alt D 1.12 at fk 0.12, missing K by 0.5 and Ou by 4; canonical D 1.72). I expect
alt to pass somewhere between 0.16 and 0.26 and canonical to need more.

Method: `kt22.py` is KT18's `kt18.py` with one change: every BV and BV2 cell with fk 0.12 is copied at fk 0.16 and at 0.20
(all other cell keys unchanged), the in-prior tags (R_d 2.38-2.90, M* 3.80-8.36e10) recomputed for the new share, and those
cells solved. Field equation, eps 0.55, xi quantisation, lines L1, L2a, L2b, L3, strict h and Q5 unchanged.

Labels per footing: **PASSES WITHIN +1 SIGMA** (at least one in-prior fk 0.16 cell passes all four); **PASSES WITHIN +2 SIGMA**
(none at 0.16, at least one at 0.20); **NEEDS MORE THAN +2 SIGMA** (neither). Per share: cells, passing count, line counts,
best D with its failing line; strict h beside.

Checks: C1 the fk 0.12 best cell per footing from `KT18_filter_mw_star_count_share/kt18.json` re-solved here reproduces its v_c
and K to 1e-6 relative; C2 KT18's smoothing mass checks on the lightest and heaviest cell per share (2e-3); MUTATE not rerun
(KT17's covers the code path), stated. Exit 0 only if C1 and C2 pass.

Limits: one star-count share measurement (BH&G16), PROVISIONAL in RF1; the heights and scale lengths are KT17's box.
