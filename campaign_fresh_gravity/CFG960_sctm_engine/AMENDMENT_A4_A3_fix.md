# CFG960 AMENDMENT A4 (2026-10-21, implementation fix to A3; before any graded output of the amended engine; committed alone)

**What happened.** The post-A3 rerun of the 128³ job set crashed in VC, VSC, VSA and VMU at step ~100, when the first bodies with r_e
just above 4 dx appeared.
- For such a body the outer region (4 dx, r_e] is thinner than a cell and can contain no mesh node, so A3's empty-shell fallback had
  no filled shell to move the mass to (`argmin` of an empty sequence).
- A3's claim "an empty shell never occurs at r > 4 dx" was wrong for thin outer regions.
- VS0, VK, LAW and SCOREK completed; their numbers are not affected, because none of them paints an outer region except LAW, whose
  bodies have r_e of 12–16 dx.
- macOS `/usr/bin/time` returned 0 for the crashed runs. Completeness is therefore checked from the run JSONs (runtime and all six
  snapshots present), not from exit codes.

**Fix.**
- **Switch boundary.** A body is painted entirely with CIC points (S7 as frozen) when r_e ≤ 5 dx. Only bodies with r_e > 5 dx use A3's
  outer mesh nodes, on (4 dx, r_e]. The outer region is therefore at least 1 dx thick, and each of its ≤ dx/2 shells holds ≳ 100
  nodes.
- **Remaining fallback.** If an outer region nevertheless has no node at all, its mass is painted as one CIC point shell at the mid
  radius; this is counted.
- Mass, shape, centroid rule and dynamics are as A3. The point-count bound per body becomes (2π/3)·10³ ≈ 2.1e3, which leaves the 1024³
  cost estimate essentially unchanged.

**Validation.** The whole 128³ set (VS0, VK, VC, VSC, VSA, VMU), LAW and SCOREK is rerun with the fixed engine. All gates of
FROZEN_CRITERIA.md §2 are re-graded on that rerun.

κ = ½ FITTED; footings never pooled; not theory closed.
