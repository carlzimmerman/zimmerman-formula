# CFG950 AMENDMENT A1 (2026-10-21, POST HOC)

**When.** Written after the first complete main run of `cfg950.py`. That run's outputs are kept as
`cfg950_firstrun_f3frozen.out` and `cfg950_results_firstrun_f3frozen.json`. This file is committed alone, before any script
change.

**Scope.** No pass line of any other test changes, and no class rule changes. The frozen result and the frozen class are
reported alongside the amended ones, and the amended class is labelled post hoc wherever it appears.

## A1.1 The frozen f3 metric cannot converge (a design flaw of the criteria, shown by a diagnostic)

**What was frozen.** Criteria §2 (f) f3 evaluates the discrete merged equilibrium "at shell mass midpoints inside
0.9 r_e,merged", with the lines ≤ 1e-3 at 2N₀ and ≤ 0.6 × the N₀ value.

**Why that cannot converge.** With equal-mass shells, the innermost shell sits where the medium's enclosed mass is
≈ dm/2, so r₁² ∝ dm. Its field step δu₁ = dm/r₁² ≈ 0.73 is then independent of N. The midpoint comparison carries an
O(δu²) error, so it is pinned at that shell for every N.

**Diagnostic** (scratch script outside the lane, the same functions as `cfg950.py`; 1:1 toy):

| N₀ | r₁ | δu₁ | max dev, all shells (frozen) | where | max dev, r ≥ 0.5 | max dev, r ≥ 1 | discrete identity ⟨R⟩ = g_b |
|---|---|---|---|---|---|---|---|
| 300 | 0.166 | 0.729 | 1.21e-1 | r₁ | 1.74e-3 | 1.34e-4 | 7.9e-12 |
| 600 | 0.116 | 0.738 | 1.21e-1 | r₁ | 4.00e-4 | 3.64e-5 | 1.4e-11 |
| 1200 | 0.082 | 0.745 | 1.20e-1 | r₁ | 1.15e-4 | 8.98e-6 | 3.6e-11 |

At fixed radius the deviation converges quadratically. The single-label force balance reproduces the discrete law
⟨R⟩_{[u_k, u_{k+1}]} = g_b(r_k) exactly (round-off of the root solve). The frozen FAIL is therefore a property of the metric,
not of the merged state.

**Amended f3** (both parts must hold, for both mass ratios):
- **f3-A.** The exact discrete identity holds for every shell of the merged single label: max |⟨R⟩_k/g_b(r_k) − 1| ≤ 1e-9.
  ⟨R⟩_k = ∫_{u_k}^{u_{k+1}} R du / δu, with u_k = k dm/r_k².
- **f3-B.** The midpoint deviation is ≤ 1e-3 at 2N₀, and ≤ 0.6 × the N₀ value, on the resolved range
  r ∈ [r_res, 0.9 r_e,merged]. Here r_res = √(10 dm_{N₀}): the radius beyond which the per-shell field step at the coarser
  resolution is ≤ 0.1. With dm_{N₀} = 0.02, r_res = 0.447 for both ratios. This is a resolution criterion, but it was chosen
  after the diagnostic was seen; the post-hoc label covers it.

(f) and the class are reported twice: under the frozen f3, and under A1.

## A1.2 Reported toy quantities affected by the discrete wall (no grade changes)

**What happens.** In the 1:1 toy the two labels' innermost shells coincide in radius. The instantly merged innermost
interval therefore has u = 2dm/r₁² > 1, beyond the W_full wall, so the discrete ΔE_merge = +∞. The continuum superposition
has u₁ + u₂ ≤ 0.78 < 1.

**What changes in the report.**
- The 1:1 discrete ΔE_merge is reported as +∞ with this explanation.
- The flow's heat is measured from its first finite-energy state.
- f2's monotonicity is counted from that state.

The same effect appears physically, not as a discretization artefact, in the NGC-3198-like concentric merger of (e): the
summed field crosses the wall in the core. That result already stood in the first run and is unchanged here.

κ = ½ FITTED; footings never pooled; not theory closed.
