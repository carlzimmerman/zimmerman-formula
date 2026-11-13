# SRJ2: commit ids, the lead's re-run and one reader note (dated addition, 2026-11-12)

No number, word or line of the lane changes. RESULT.md stays as the lane wrote it.

## Commit ids (local / origin)

| Commit | Local | Origin |
|---|---|---|
| FROZEN_CRITERIA (alone) | b8a99499ad | e6d3c5212b |
| Scripts and outputs | 7671345425 | 68d08d57b0 |
| RESULT (122 lines) | c67c2ce0e8 | 9cbe2dc482 |
| RESULT shortened to 100 lines | 924aab9bfb | 1a84e7582a |

## Re-run by the lead

Every script from a copy, one thread, in the lane's order: `srj2_hm.py`, `srj2_forest.py` on both footings with twins
C and F2, `srj2_rc.py`, `srj2_lens.py` with twin F2, `srj2_clusters.py`, `srj2_grade.py`. All twelve JSON files and
all twelve `.out` files equal the committed ones once elapsed-time and peak-memory lines are removed. Exit codes: the
graded runs 0; every twin 1. Words reproduce: JOINT FAILS ON G2, G3, G4 (canonical) and JOINT FAILS ON G2, G4 (alt),
FRAGILE, with TRIVIAL beside the forest and beside clusters and groups.

A reproduction of the arithmetic, not an independent re-grade.

## Reader note (the lead's reading of SRJ1 and SRJ2 together; not graded)

Two joints were graded on 2026-11-12, both post hoc to the forest row's fail:

- SRJ1: the law's layout inside the fold radius in every system. It fails X-COP's shape gate: the law's layout is too
  light in cluster cores, and the reference layout passes.
- SRJ2: the same, with the reference layout kept above FRZ1's v_stiff boundary. The forest, clusters and groups then
  hold, trivially (the joint equals the reference there), but the boundary also takes the law away from 31 / 22 of
  RC100's 100 massive discs at z 1 to 2.5 (it falls at log M_b 10.93 / 11.04 there), so the coverage line G2 fails at
  every f; lensing by type misses its line by 0.012 / 0.037 sigma.

Read together: a boundary set by depth of the well alone cannot both exclude clusters and keep massive discs. Whatever
separates the two states would have to tell a disc from a group of the same depth. That is a statement about these two
candidates and this boundary, not a derivation, and G2 is a coverage line: whether the reference layout fits those
curves was not tested. No further variant was run from this result.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
