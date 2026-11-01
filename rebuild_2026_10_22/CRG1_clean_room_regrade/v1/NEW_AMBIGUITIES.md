# CRG1 BUILD: NEW AMBIGUITIES

Found while building. Primary is the plain first reading, fixed before the cell ran. Where a second reading is computed it sits beside the primary in `crg1_results.json`. NA4b, NA9b and NA13b were added after I had seen primary values; their primaries were not changed.

| Id | Where | Primary | Other reading | Computed? | Changes pass/fail? |
|---|---|---|---|---|---|
| NA1 | 4.2 `sh_P`: is "sh(r)" the core form, or with the GS1 tail to 2.2 R500'? | Core form, supported by 4.6's "no tail" | GS1 tail between R500' and 2.2 R500' | Yes, C4 K (`NA1b`). In the C1 chain it only seeds the iteration | C4 K fails either way; the failing set differs |
| NA2 | 6.3 unit conversion of S: set E (table 0: "Σ_core unit conversion") or D (section title) | E | D | Yes (`NA2b`) | No |
| NA3 | 4.5 C2's C*: on M_b, or on M_bf with the BCG? | M_b | M_bf | Yes (`NA3b`) | No |
| NA4 | 4.4 `x_e = min(x_edge)`: over the two bracketing mass nodes, or all three? | Two nodes | All three | Yes (`NA4b`), K and X | No |
| NA5 | 4.4, 4.5 `M_t = (...)/M☉`: chain uses set F's M☉; which divides? | F | E | No; a 3e-4 shift in mass inside S_N only | Not computed |
| NA6 | 8 K1 shear mock: no scatter, so bootstrap and jackknife sigma are rounding error and Z is about 1e14. The check passes only because both sides share that sigma | As written, kept | Twin: real-E Gaussian scatter with its OUTER sum over I removed, so A stays exact and sigma is real | Yes | Both pass; both fail under flip |
| NA7 | 5.3 `bmax` default when not stated | +inf | none plain | n/a | n/a |
| NA8 | 6.1 CSV also has "M31 dE" (3) and `indiv:` rows | Excluded: 6.1 and 6.2 list five classes | Include | No | Not computed |
| NA9 | 4.1 `Bst = Σ_i den/Σ_i den_r`: over all 326, or the key's set? | All 326, per h | Over I | Yes (`NA9b`), C1 primary | No |
| NA10 | 4.2 Kačanov "max relative change": of what? | Φ, per cell, denominator max(abs Φ, 1e-12) | μ, or a norm | No; own M agrees with the given table to under 1e-4 | n/a |
| NA11 | 4.3 mass-key bootstrap [200+t]: t = 0,1,2. σ isn't used for C1, C2, C4 | Reported as `own_sigma_stat` | n/a | Yes | n/a |
| NA12 | 4.4 fallback "A3 table at this f*": both f* entries are identical in scalars.json | f* 0.034 entry | 0.0615 entry | Same numbers | No |
| NA13 | 4.5 X-COP: contraction on uncapped M_bx as written, or capped M_b? `M_h(r_m)` has no min, 4.4 has one | M_bx as written | Capped | Yes (`NA13b`) | No |
| NA14 | 5.4 S1: R200 table is the same for both models and both footings (the map has no a0) | One T per bin | none | n/a | n/a |
| NA15 | 5.2 two-halo quadrature with a step at r_c | Integrate from the step: same integral, cleaner for the adaptive rule | Plain integrand with step | No | n/a |
| NA16 | Section 1: C3's K at alt: "same as C1", C1 is canonical only | C1's row with alt C* (A9b) | none plain | Yes | n/a |
| NA17 | 8 SPARC mock: g_B ≤ 0 points have v² ≤ 0 | Vobs = 0, so masked | n/a | n/a | n/a |
| NA18 | Which footing decides a candidate's verdict for C3, C4 | Canonical primary, alt listed, never pooled. Each footing's failed lines are in `_verdict` | Both must pass | Both listed | Alt adds failed lines to C3, C4 |

## Spec's A1 to A17: where they stand

| | Primary | Second reading |
|---|---|---|
| A1 | (a) literal 21.53 | (b) on S, Tl, LT, K, X, G |
| A2 | (a) | not available |
| A3 | (a) | (b) `A3b_basin_consistent` |
| A4 | (a) | (b) computed; largest difference in `detail` |
| A5 | (a) | (b) `crg1_results_A5b_oneset.json`, not graded |
| A6 | (a) | (b) `A6b` |
| A7 | (a) | both rows reported |
| A8 | (a) | (b) `A8b` |
| A9 | (a) | (b) `A9b_alt_Cstar` |
| A10 | (a) | (b) max dZ reported; under 0.10 everywhere, so no second Z table |
| A11 | (a) | (b) `A11b` |
| A12 | (a) | (b) `A12b_S_N` |
| A13 | (a) | (b) `A13b_mass_flag` |
| A14 | (a) | (b) `A14b_NR2` |
| A15 | (a) | numpy version in `_meta` |
| A16 | (a) | no other reading |
| A17 | (a) | (b) not computed, per the spec |

A13(b) flips C3's Dw at canonical, from pass to fail. The other second readings I checked don't flip a graded line at canonical. A6(b) moves C1's reported X out of the pass range at g = 10^0.111, and that reading isn't graded.
