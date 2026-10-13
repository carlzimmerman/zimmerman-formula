# CFG743 — settle time of the collapsed cold medium (nonlinear identification; frozen criteria, committed alone)

Block CFG740–749. Written before any CFG743 number. κ = ½ fitted; both footings; the cold energy's mass is required; no
particle species; not theory closed.

## Why
The CFG699 addendum: the FAIL holds for the linear identification (inertia at the cosmic mean). The nonlinear identification
named here is 4πG P = −g_c, the cold matter's own gravitational field. Then:
- the critical quadratic of W is the cold matter's self-gravity energy, which the tether cancels (CFG698 J1, restated);
- the nonlinear residual sets g_c = √(a₀ g_N), the law (CFG694 D-form);
- a cold element's inertia is its own mass at the **local** cold density ρ_c(r), not ρ̄_c.

## Test
- **T1.** For a point baryonic mass M_b ∈ {10⁹, 10¹⁰, 10¹¹, 10¹²} M☉ and y = g_N/a₀ ∈ {0.1, 1}:
  - take the radius where g_N = y a₀;
  - take the law's cold density there, ρ_c = (4πG r²)⁻¹ d(r² u)/dr with u = g − g_N (simple μ, CFG695);
  - compute the element period T = 2π/√(4πG ρ_c [(1 − x)⁻² − 1]), x = u/a₀ (CFG699's restoring term at the local density).
- Both footings.
- **PASS iff T ≤ 1.38 Gyr for every M_b and both y** (10 periods in 13.8 Gyr, as in CFG699).

## Verdict
- PASS: candidate B with a mechanism (CFG698, nonlinear form) is not excluded on settle time. Its data failures (C3, D2) are
  unchanged.
- FAIL: it is excluded on settle time too.
- **Not claimed:** collisionless relaxation to the profile (phase mixing, violent relaxation). That is a separate, open
  question (CFG461, CFG665).

## MUTATE (`CFG743_MUTATE=1`, exit 1 iff it bites)
Replace ρ_c with the cosmic mean ρ̄_c. This must reproduce CFG699's periods (60.4 Gyr at y = 1, canonical) within 1e-3.
