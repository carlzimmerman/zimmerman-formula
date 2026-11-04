# KT38 intermediate-length dwarf continuation

This adaptive continuation was authorized after the initial Milky Way scan bracketed a possible intermediate-length tradeoff. Its five common physical lengths were written to CONTINUATION_PLAN.md and contract_continuation.json before the new run. The original physical inputs, 24 objects, 41 Upsilon values, two a0 footings, cuts and numerical gates are unchanged. Initial KT38 results and source files were preserved.

| Common ell (kpc) | Canonical virial-screen passes | Alternate passes |
| --- | --- | --- |
| 1.5 | 17/24 | 17/24 |
| 1.75 | 17/24 | 17/24 |
| 2.0 | 16/24 | 17/24 |
| 2.25 | 16/24 | 17/24 |
| 2.5 | 16/24 | 16/24 |

Plain isolated simple QUMOND remains19/24 on each footing. Fornax and Leo I retain sampled passes at all five lengths on both footings. Sculptor passes canonical1.5/1.75 but fails2/2.25/2.5; on the alternate footing it passes through2.25 and fails2.5. Canonical sigma(U=3) for Sculptor at ell1.75 is6.490815km/s against the unchanged lower cut6.4; alternate atell2.25 is6.429163km/s. These are numerical41-point statements, not continuous-Upsilon conclusions.

The two initial lost plain passes at ell1.5 and1.75 on both footings are Leo II and Leo T. At larger continuation lengths the additional loss is Sculptor as specified above. No new plain-failing object is promoted.

All original numerical checks passed. Maximum dispersion change across resolution/domain checks: 0.000310549778km/s; maximum direct/weak/energy virial relative disagreement: 7.32805143e-15; actual-energy finite-difference discrepancy: 9.01544512e-09. Passing object sets are identical across all three radial grids. All variances are positive and no negative total radial gradient appears on any evaluated continuation grid. This absence is finite coverage, not a global positive-force proof.

The continuation adds9,840 distinct configurations to the initial9,840, for19,680 across ten distinct physical lengths, with three quadrature grids each. The nonlinear action, fixed exponent and shared primitive were not refit. No external field, Upsilon monotonicity assumption, equilibrium-distribution construction, or new observational rejection rule is introduced.

Evidence: continuation.py, CONTINUATION_PLAN.md, contract_continuation.json, continuation_001/results.json, its completed validated manifest, and CONTINUATION_CHECKPOINT.json.
