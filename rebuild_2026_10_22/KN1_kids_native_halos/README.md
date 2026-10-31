# KN1_kids_native_halos: LAW on both mass choices. The native shape helps on EM1's masses (Δχ² +366 against +434) and fails badly on AM1's (+2850)

Criteria: `FROZEN_CRITERIA.md` (418a129bac), committed alone before any native shape went through this harness. `kn1_kids.py`, `kn1_grade_*.json`, `kn1_results_*.json`, `kn1_*.out`, `kn1_k1.out`. κ = ½ FITTED; footings never pooled; not theory closed.

## Frozen grade: X53's harness, Δχ²(H2H − L2H), z = 0.25 shape, "all"
| Halo | Δχ² canonical | Δχ² alt | H2H χ² | fitted b | class | against FC1 |
|---|---|---|---|---|---|---|
| FC1's rule (K1) | +434.4 | +463.7 | 588.7 | 0.25, 0.37, 0.65, 0.69 | LAW | |
| **Native shape, EM1's masses** | **+366.0** | +395.3 | **520.3** | 0.24, 0.34, 0.61, 0.63 | **LAW** | **NATIVE BETTER** (−68) |
| **Native shape, AM1's masses** | **+2849.6** | +2878.9 | **3004.0** | 0.20, 0.20, 0.19, 0.00 | **LAW** | **NATIVE WORSE** (+2415) |

The law's arm: L2H 154.3 canonical, 125.1 alt. On "primary" (Δχ²): FC1's +137.9, EM1 +136.4, AM1 +1628.4. Without the two-halo term removed by S1's exclusion at median R₂₀₀, EM1's reads +235.9, still LAW.

**Per mass bin, all, Δχ²:** EM1 +39.5, +108.2, +105.1, +138.5. AM1 +30.3, +67.6, +422.2, +2355.4.

## Reported
| Choice | EM1 | AM1 |
|---|---|---|
| FC1's normalisation | +348.5 | +3463.5 |
| z = 0 snapshot | +395.6 | +2261.2 |

## How this reads
- **The native profile beats the core rule on lensing, modestly.** It keeps mass beyond R₂₀₀, which FC1's truncated halo doesn't. But the law still leads by a wide margin on this photometric sample. SI3 shows how much of that sample's lead depends on the host veto.
- **Lensing rejects AM1's masses, and most of that is in the top two bins.** That agrees with AM1's warning that its bright-end count isn't trustworthy, and with the known point that rotation curves and lensing don't support a steep turnover for spirals. The lowest two bins move little (+30.3, +67.6 against +39.5, +108.2). So this doesn't test AM1's graded number at lg M_b 10 much, and it does say the 13.3 at lg M_b 11 can't be used.
- **Most lenses are clamped:** 5946 of 8034 shape evaluations on EM1 sit below the 10¹² tag. ZN2's low-mass continuation could improve this; no reason to expect +366 to close.

## Limits
EM1's relation is a fit. The harness's two-halo template has inherited ΛCDM initial conditions in X53's ledger, and it's fitted with 4 amplitudes, as in every X53 reading. Stellar masses are R0, not R2 (SI3 runs both). No neighbours in the one-halo term.

## Checks
K1 FC1's rule as a table through this path: H2H all 588.746 against 588.728, |d| 0.018 (limit 1.0); law's arm |d| 0. K2 X53's inherited checks: 10/10 in K1's path, 8/10 in the native runs. The two are `K_T_truncation`, which tests a halo cut at R₂₀₀, and these halos aren't, so it fails by construction. MUTATE r × 1.5: H2H χ² +156.3, BITES.
