# V3X amendments (each disclosed with when it was made and what had been seen)

No pass line, label rule or graded radius in `FROZEN_CRITERIA.md` (859c76bec3) is changed by either amendment, and
nothing is widened. K1 (W2) stays exactly as frozen, including its r_Saturn radius.

## A1 (W2 solver). Made after development smoke tests, before the production run

**What was seen first.** Development runs of Method A (canonical only, not kept) at (20,32)–(70,112):
- (40,64) reproduced V3W's graded Q2 to 3e-9 and (50,80) converged (23 Newton steps).
- (60,96) stalled at a scaled residual of 1.3e-5 after 60 steps, and (70,112)'s first step failed its line search.
- The cause is float64, not the solver: at the inner shells C6's row-scaled Jacobian adds the law's r² entries
  (≈ r²) to the grad-div stiffness entries (≈ Λ²/2dx²) inside the same matrix entries. Below r ≈ 1e-8 Λ/dx those
  entries fall under machine ε, so the stiffness's divergence-free null space is unresolved. That happens at
  r_in = 1e-4 from (60,96) on. Unshifted Newton steps then carry O(10) garbage in those directions.
- The first block solver also allowed pivoting only inside a super-block. It was replaced by Gaussian elimination
  with partial pivoting across block rows j and j + 1, which is banded LU's pivot set.
- At (50,80) the seen value of Q2 at 100 r_Saturn was 1.6309e-34. At (70,112), with the shift below, it was 1.6200e-34.

**The amendment.**
- Every Newton step (Methods A and B alike) solves (J_s + μ I_w) dU = −sF, with μ = 1e-12 added on the w rows of C6's
  row-scaled Jacobian.
- After the scaled residual first drops below 1e-9, up to 3 further Newton steps are taken while the line search
  still lowers it ("polish").
- C6's residual, row scaling, line search and convergence test (< 1e-9) are unchanged. The converged state solves the
  same discrete equations; the shift changes only the path.
- The same rung at μ = 1e-10 is reported as a float64 noise estimate.

## A2 (W4c known answer K4). Made before any W4c script or number

**Why.** K4 compares Route N's monopole of ρ̄_τ with the hedgehog M☉/(2πL★²r) for r ≤ 0.1 L★. That is the right known
answer only where the hedgehog dominates.

**Estimate.** From C6's own Route F kernel with the hedgehog subtracted, f = −2(1 − m)/(k²(1 − m + k²m/2)) (units of L★
and M☉), the remainder of ρ̄_τ is regular at r → 0. Its size is ≈ −(1/π²)⟨(π/2)√(2(1 − m)/m)⟩ ≈ −0.5 M☉/L★³ at
x_e ≈ 2.2. Against 1/(2πr), that is ≈ 30 % at r = 0.1 L★, ≈ 3 % at 0.01 L★ and ≈ 0.3 % at 1e-3 L★. This is an analytic
estimate, not a run of the lane.

**The amendment.** K4's range becomes **r ≤ 1e-3 L★** (still excluding the three innermost shells), with the same
1e-2 line. The frozen range (r ≤ 0.1 L★) is also computed and reported, with this explanation; it is not graded.
