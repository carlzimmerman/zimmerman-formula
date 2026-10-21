# CFG954 AMENDMENT A1: implementation stage (2026-10-21). Made after the 4-cluster smoke runs, before any full-data run

**When.** After smoke runs of all four stages on the first 4 eRASS1 clusters (`CFG954_NMAX=4`; every output written outside the
repository, to `../_external_data/cfg954_work/` from the repository root). No full-data run had been made. `FROZEN_CRITERIA.md`
(68a43b4ff) is not edited.

**What the smoke runs showed (disclosed, since they are numbers this lane saw):**
- The four-cluster scores carry jackknife errors of order 1–2, so their (a1)/(a2) classes mean nothing.
- The Bullet, toy, UDG and selector parts do not depend on the cluster sample. Their smoke numbers are the real ones:
  - R1 [P-S] Bullet φ = 1 at every d_p; φ_J is UNDERDETERMINED.
  - Toy J: R1 [P-S] 0.65–0.88 (the E₂ jump at absorption), R1 [P-I] 0.08–0.29, R2 0.08–0.39, R3 0.047–0.22.
  - Coma UDGs: R1 [P-S] z +5.75 / +3.87; keep-own-phantom z +1.61 / +1.42.
  - Selector: CHOICE.
- Two implementation points are corrected here.

## 1. (f) R1 at its trigger: the check on the discretised member
- **Frozen statement.** The absorption at the trigger conserves momentum identically: the whole member domain is comoving with zero
  net 𝒮 charge, and the recompute is spherical with zero net charge. This is "verified on the discretised member".
- **What the first implementation did.** It took the member's net charge from the harness's `prog_halo` cumulative phantom.
  `prog_halo` (CFG637 `phantom_trunc`, inherited from CFG726) places the edge at the first grid point past the supply root, so its
  enclosed phantom exceeds the supply by up to one grid step (Δ ln r = 0.0128): 0.45–1.2% of S. That residual (0.48 / 0.61 m₂ in
  the toy, i.e. 0.9% / 1.1% of the domain's momentum) is an inherited grid artefact, not a property of SCT. It would have put the
  R1 primary on the 1% line by accident.
- **What is used now.**
  - The toy builds the discretised member with the exact (log-interpolated) supply root.
  - P-S rest cold S₂ is spread uniformly in ln r between the root and r_ta,2, and the zero-sum draw q is fixed by the shell sums.
  - The net charge is the sum of shell weights (active − rest), divided by the domain's momentum (m₂ + S₂)V.
  - The harness-grid residual is reported alongside, with no class weight.
- The cluster harness's R1 value stays 0 by the identity. The global-recompute bracket is unchanged.

## 2. Convergence reporting (reported only)
- **What the smoke showed.** R1 [P-S] and R1 [P-I] sit in a 2-cycle at the innermost grid nodes, r ≤ 2 kpc, where the cored
  harness gas has M_b ≈ 0. There, a member node with no tidal radius (pericentre at the grid floor, 3 − γ ≤ 0) persists. The largest
  relative change beyond 100 kpc was 5.7e-7, against 0.17 at 1 kpc.
- **What is added.** The frozen convergence test (max |ΔM/M| over the whole grid ≤ 1e-4) and the frozen non-convergence rule (last
  two iterations of different class ⇒ UNDERDETERMINED) are applied unchanged. Alongside them, the same statistic restricted to
  r ≥ 10 kpc is reported, with no weight.

## Not changed
Every rule, test, class rule, bracket, K test and MUTATE item in `FROZEN_CRITERIA.md`. COMPUTE, K, MUTATE and MAIN are run from
the final script after this file is committed.

κ = ½ FITTED; footings never pooled; not theory closed.
