# CFG960 AMENDMENT A3 (2026-10-21, after the first 128³ validation, before any 1024³ job; committed alone): hybrid body painting

**Why.** S7 places quadrature points at dx/2 spacing in radius and angle, so a body costs ≈ (2π/3)(2 r_e/dx)³ points.
- At 128³ the bodies use 3.1e5 points in all (VC, z = 0; r_e up to 7.5 dx).
- At 1024³ the same bodies are 8× larger in cells, and smaller domains are added. The total would be ~1e7–5e7 points: 1–2 GB of extra
  memory and minutes per step of CIC work (`np.add.at`).
- That breaks the 46–47 GB envelope of the 1024³ jobs. This is an engineering defect of S7 found while estimating the cost (A2's
  numbers, from commit b5c942cc4, are unaffected by its discovery).

**Change (S7 only; the body's shape, mass, centroid rule and dynamics, S6 and S8, are unchanged).**
- **Inner part, r ≤ r_in = min(r_e, 4 dx).** As frozen: equal-width shells of ≤ dx/2 and antipodal Fibonacci sets with CIC
  deposit. They carry M_σ(<r_in), or M_c when r_e ≤ 4 dx.
- **Outer part, 4 dx < r ≤ r_e (bodies with r_e > 4 dx only).** Painted directly on mesh nodes (node i at i·dx, the CIC grid points).
  Radial shells of width ≤ dx/2 between r_in and r_e carry ΔM_σ. Each shell's mass is shared equally by the nodes whose distance
  from X_q falls in that shell. The outer part carries exactly M_c − M_σ(<r_in).
- **Force on the outer part.** Σ_nodes w g(node), with the same mesh acceleration field the particles see. The painted density is
  what the force uses, so the PM momentum book stays exact (a Poisson field exerts no net force on its own source).
- **Fallback radius.** The outer painting radius is capped at min(L/4, 128 dx); a body whose supply root lies beyond the cap puts
  the remainder in the last shell. This is counted and reported, and not expected at any resolution (the largest r_e at 128³ was 7.5
  dx; the estimate for 1024³ is ≲ 80 dx).

**What this does and does not change.**
- Total mass and the radial mass profile are exact at dx/2 resolution.
- The outer part's centroid can differ from X_q by a sub-cell sampling dipole of order dx/√n_nodes. S-TM's exact centroid holds for
  the inner points; for the outer nodes it holds to that sampling error, while momentum stays exact.
- Expected cost at 1024³: ≲ 5e6 inner points and ≲ 1e7 outer nodes per step (≈ 0.3 GB transient, a few seconds per step).

**Validation.** The whole 128³ job set (VS0, VK, VC, VSC, VSA, VMU), LAW and SCOREK are rerun with the amended engine under
A1's environment. All gates of FROZEN_CRITERIA.md §2 are re-graded on the rerun; LAW's bodies (r_e 12–16 dx) exercise the
outer-node painting. The first validation outputs (commit b5c942cc4) are superseded and kept in git history.

κ = ½ FITTED; footings never pooled; not theory closed.
