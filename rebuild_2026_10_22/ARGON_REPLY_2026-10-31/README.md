# Argon's reply of 10-31, checked

Predictions recorded before any ZN1 read: `PREDICTIONS_ON_RECORD.md` (01c405354a). Recomputation: `argon_check.py`, `argon_check.out`. κ = ½ FITTED. Not theory closed.

**Why its replies scramble.** Both garbled stretches start right after `M_b(<R200)` and end at the next `>`. A `<` followed by a letter is being read as an HTML tag somewhere in the copy, and everything up to the next `>` becomes its attributes, de-duplicated and sorted. That's the "alphabetically sorted words". Argon should never write the characters `<` or `>`.

## Checks
| Argon's claim | Recomputed | Result |
|---|---|---|
| Ω_m(z_f 0.562) 0.770, Δ_c(z_f) 136.8 | 0.6175, 109.7 | wrong; used only in narrative |
| NFW c 5.72: R_52.87c/R_200c 1.79, M ratio 1.348 | 1.748, 1.413 | wrong, small; S +6.8 % agrees with MA1's own run, +6.5 % |
| σ(M) at 10¹², 10¹³, 10¹⁴: 2.05, 1.42, 0.94 | 2.286, 1.598, 1.033 | wrong table |
| η lower by 1.5 %, 3.2 % at z_obs 0.223, 0.5 through ν, slope −0.12 | slope −0.100 at 10¹³–10¹⁴: 1.2 %, 2.6 %. **But slope −1.07 at 10¹²–10¹³: 12 % at z_obs 0.223** | right only above 10¹³; below that much larger, and it would offset part of N3's × 1.26 |
| S × 1.26 is real; (1 + z_f) × 1.18 | formula right; (1 + z_f) × 1.123, squared 1.262 | conclusion right, number wrong |
| ET's need is "exactly 1.50" over N0 at every bin, using ET2's numbers | ET2: 1.49, 1.57, 1.68. ET1: 1.47, 1.49, 1.52 | true for ET1 only |
| That's "Version N1" | ET2/N1 0.97, 1.19, 1.41 | no: N1 isn't a constant boost |
| NFW bound gives +0.594 dex at the same S, so Draco passes at −0.104, J0946 R 7.9 | **my brief's error, which Argon inherited.** The cusp that fits the same halo has ρ_s r_s = 0.58–0.68 S, so the gain is +0.36 to +0.43 dex. Draco on N1 +0.076 (at c 15), J0946 R 12 | Draco is marginal, not a pass |
| HSB/LSB example r₀ 5.8 kpc | 4.04 kpc | wrong; test still runnable |
| −0.110 dex is −22 % in V | −22 % in g, −11.9 % in V | wrong |
| Fair share inside R₂₀₀ is biased low, Y_b 0.90–0.93 | X-COP's own gas inside R₂₀₀ over hydrostatic M₂₀₀: median 0.957 of cosmic before stars (9 clusters; A2319 is high at 0.246). With stars, about 1.0 | not supported by X-COP's own numbers |
| S1 "red" A_in 1.39, 0.99 | those are all of S1 | mislabelled |

The plan's structure is sound, and four of its lanes were already mine. ZK1 changes its costs: GD1 (run here as LC1) takes about an hour, not 18.
