# CFG782 erratum (2026-10-14, written after a one-line arithmetic check and before any script exists)

The frozen file's hand-computed control values are slightly wrong. The selector's definition is unchanged.

| quantity | frozen (hand) | correct |
|---|---|---|
| c_s(1.5e4 K, μ 0.59) | 14.6 km/s | 14.49 km/s |
| V_th at 1 / 1.5 / 2 × 10⁴ K | 16.9 / 20.7 / 23.9 | 16.73 / 20.49 / 23.66 km/s |
| V_init(10⁶ M☉, canonical a0) | 10.4 km/s | 10.56 km/s |

K1 and K2 as frozen (tolerance 1e-3 against the hand values) would FAIL on the hand arithmetic, not on the code. The script
scores K1/K2 against the correct analytic values. The README will report the frozen-vs-correct discrepancy. Every gate (S1,
S2, verdict) and every setting is unchanged.
