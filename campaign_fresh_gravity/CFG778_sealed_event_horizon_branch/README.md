# CFG778: event-horizon a₀ branch, SEALED before the November ALMA releases

**Label: SEALED.**
- sha256 `b9f3e827f79256c0509c15fdcd60c7fdc258ac45dbfa81be3d9b0ce554dc9aad` (`SEALED_EVENT_HORIZON.json`).
- K1 PASS: R_E(0) = 4906 Mpc, between c/H₀ and c/H∞; dR_E/dln a = R_E − c/H to 2.4e-11.
- K2 PASS: F-flat, F-DESI and R-H reproduce CFG571's stored GS4_24110 numbers exactly.
- MUTATE (Ω_Λ = 0): R_E diverges and the branch is flagged undefined (bites).

## Why
Astra proved (`sol61_push/claude_bh_followthrough_2026_10_14/`) that when vacuum is produced:
- a₀ ∝ √ρ_DE and a₀ ∝ c²/R_E evolve in **opposite** directions (R_E = actual future event horizon);
- "dark-energy density sets a₀" and "the horizon sets a₀" are therefore different, testable theories.

This lane seals the horizon branch alongside CFG571's (flat, DESI-tracking, a₀ ∝ H) and CFG775's (black-hole source).

## Branch ratios a₀(z)/a₀(0)

| z | E (constant Λ, Ω_m 0.308) | E-CCBH (astra, quoted) | flat | BH-k3 (CFG775) |
|---|---|---|---|---|
| 1.0 | 1.197 | — | 1 | 0.970 |
| 1.419 | 1.305 | 1.307 | 1 | 0.932 |
| 1.997 | 1.464 | 1.439 | 1 | 0.852 |

The event-horizon branch is nearly background-independent: 1.46 vs 1.44 at z = 2.

## Sealed required gas (log M_gas, R_g = R_d; canonical / alt)

| target | E | flat | DESI | BH-k3 | a₀ ∝ H |
|---|---|---|---|---|---|
| GS4_24110, log M* 10.89 | FLOOR / FLOOR | 9.46 / FLOOR | 9.82 / 9.11 | 9.87 / 9.31 | FLOOR / FLOOR |
| GS4_24110, log M* 10.76 | 10.06 / 9.75 | 10.36 / 10.24 | 10.43 / 10.33 | 10.44 / 10.34 | FLOOR / FLOOR |

U4_27928: the full V_c grid is in the JSON. The branches separate only for V_c ≥ 225 km/s.

## Reading
- In the November data:
  - flat and density-tracking a₀ need the most gas;
  - the horizon branch needs about 0.3 dex less;
  - a₀ ∝ H needs none.
- GS4_24110's integrated gas is already public (CFG572: tracers disagree by ~0.7 dex). The 11-28 release adds the resolved
  [CI](2-1) data. That is one disc, a demonstration, not a decision.

κ fitted; not theory closed.
