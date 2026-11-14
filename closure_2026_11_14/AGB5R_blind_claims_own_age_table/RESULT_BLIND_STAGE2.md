# AGB5R — blind re-grade of AGB5, stage 2 (AGB5's amendment 1 applied)

2026-11-14. Opened `AGB5_claims_own_age_table/AMENDMENT_1.md` only after stage 1 was committed (627eb1aede). The
amendment quotes AGB5's own K4 ratios and its primary amplitude (A = +0.82 ± 0.17); those were seen at this point and
not before. Nothing else of AGB5 (README, scripts, outputs) was opened. Stage 1 files are untouched; stage 2 writes
`agb5r_stage2.py`, `agb5r_K4_boot.{json,out}`, `agb5r_L_boot.{json,out}`, `agb5r_collect_stage2.py`,
`agb5r_collect_stage2.out`, `agb5r_results_stage2.json`.

## The amended rule, as I applied it
1. Every slope that enters L1 and its forks takes as its error the standard deviation (ddof 1) of Â over 400 bootstrap
   resamples of the hosts of that table, `numpy.random.default_rng(20261119)`, a fresh generator for each (fork, table)
   fit. The point estimate stays the full-sample fit. Combined rows weight the tables by these errors. The structural
   fork is bootstrapped too (structural fit re-maximised on every resample, three starts, the full-sample maximum among
   them).
2. K4 amended, per table: (a) the bootstrap error (the primary step-free plain fit, seed 20261119) within [0.8, 1.25] of
   the stated (formal) error; (b) the shuffle with the fitted signal removed: HR − β̂ age − ĝ (L − ½), then (age, L)
   permuted together, 400 permutations, the frozen shuffle seed 20261118 (the amendment names none), scatter of Â
   within [0.8, 1.25] of the stated error. The frozen file's mean condition (|mean Â| ≤ 0.2 σ_A) is not in the amended
   list; it is printed and passes on both tables, so it does not matter.
3. L1 judged by the frozen word table on these numbers, tagged "(amendment 1)".

## Word

**L1 (amendment 1): AGE BIAS REQUIRED AT 3 SIGMA / FRAGILE (table 1 alone, structural) (amendment 1).**
Primary: Â = +0.8124 ± 0.1873 (bootstrap), Δχ²(A=0) = 18.82, Δχ²(A=1) = 1.00.
L1 as frozen (stage 1) stays **NOT EVALUABLE** (K4 failed). Both readings are reported.

## Checks

| check | stage 1 (frozen) | stage 2 (amended) |
|---|---|---|
| K1 | PASS | PASS (unchanged) |
| KA | PASS | PASS (unchanged) |
| K3 | PASS | PASS (unchanged) |
| K4 table 1 | PASS: shuffle sd 1.227, bootstrap sd 1.041 (seed 20261118) | PASS: bootstrap sd 1.113 (seed 20261119); shuffle, signal removed, 1.133 |
| K4 table 2 | **FAIL**: shuffle sd 1.345 | PASS: bootstrap sd 1.138; shuffle, signal removed, 1.125 |

Ratios are to the stated (formal) σ_A: 0.2233 (table 1), 0.2501 (table 2). The fitted signal that the amended shuffle
removes is 0.052 mag rms (table 1) and 0.084 mag (table 2).

## L1 rows: stated errors (stage 1) against bootstrap errors (stage 2)

| row | stage 1: Â ± σ (stated) | Δχ²(0) | Δχ²(1) | word | stage 2: Â ± σ (bootstrap) | Δχ²(0) | Δχ²(1) | word (amendment 1) |
|---|---|---|---|---|---|---|---|---|
| **primary** | +0.8195 ± 0.1666 | 24.20 | 1.17 | REQUIRED AT 3 SIGMA | **+0.8124 ± 0.1873** | **18.82** | **1.00** | **AGE BIAS REQUIRED AT 3 SIGMA** |
| table 1 alone | +0.5322 ± 0.2233 | 5.68 | 4.39 | NEITHER | +0.5322 ± 0.2486 | 4.58 | 3.54 | AGE BIAS FAVOURED |
| table 2 alone | +1.1797 ± 0.2501 | 22.25 | 0.52 | REQUIRED AT 3 SIGMA | +1.1797 ± 0.2847 | 17.17 | 0.40 | AGE BIAS REQUIRED AT 3 SIGMA |
| shared dropped from t1 | +0.7748 ± 0.1818 | 18.15 | 1.53 | REQUIRED AT 3 SIGMA | +0.7851 ± 0.2093 | 14.07 | 1.05 | AGE BIAS REQUIRED AT 3 SIGMA |
| t1 original residuals | +0.6742 ± 0.1666 | 16.38 | 3.82 | REQUIRED AT 3 SIGMA | +0.6738 ± 0.1895 | 12.64 | 2.96 | AGE BIAS REQUIRED AT 3 SIGMA |
| redshift term | +0.7515 ± 0.1737 | 18.72 | 2.05 | REQUIRED AT 3 SIGMA | +0.7596 ± 0.1992 | 14.54 | 1.46 | AGE BIAS REQUIRED AT 3 SIGMA |
| structural | +2.0140 ± 0.5891 | 11.69 | 2.96 | REQUIRED AT 3 SIGMA | +2.1848 ± 1.7661 | 1.53 | 0.45 | UNDECIDED |

Combined amplitudes move a little (0.8195 → 0.8124) because the bootstrap errors re-weight the two tables.

Per-table errors, stated → bootstrap (ratio): table 1 0.2233 → 0.2486 (× 1.113); table 2 0.2501 → 0.2847 (× 1.138);
table 1 without shared hosts 0.2649 → 0.3088 (× 1.166); table 1 original residuals 0.2233 → 0.2540 (× 1.137); with the
redshift term 0.2411 → 0.2790 (× 1.157) and 0.2505 → 0.2844 (× 1.136); **structural 0.9496 → 4.3052 (× 4.53) and
0.7512 → 1.9366 (× 2.58)**. The plain bootstrap errors were re-derived with a second least-squares route (same digits).

## What changed
1. **The check.** The amended K4 passes on both tables, so L1 now carries a word; as frozen it carries none.
2. **The plain rows barely move.** Every plain error grows by 11 to 17 per cent; the primary Δχ²(A=0) falls from 24.2
   to 18.8 and stays above 9, Δχ²(A=1) stays near 1. The four plain forks that agreed in stage 1 still agree.
3. **Table 1 alone** moves from NEITHER to AGE BIAS FAVOURED (Δχ²(A=1) drops under 4). It differs from the primary
   word in both stages, so it is named either way.
4. **The structural fork flips** from AGE BIAS REQUIRED AT 3 SIGMA to UNDECIDED. Its bootstrap distribution is
   heavy-tailed: table 1's 68 % range is +0.86 to +2.64 (half-width 0.89, close to the curvature error 0.95), but a few
   resamples run off to A = −62 and +43. These are true maxima of the likelihood, not minimiser failures: the eight most
   extreme draws per table were refitted with the full 27-start fit and land on the same points; every one with |A| of
   about 3 or more has the true-age spread inside the mass groups collapsed to τ = 0.08 to 0.37 Gyr (against stated age
   errors near 2 Gyr), where the slope is barely identified. The standard deviation the amendment asks for counts those tails in full.
   Reading only, not a word: with the 68 % half-width as the error the structural row is A = +1.77 ± 0.74,
   Δχ²(A=0) 5.71, Δχ²(A=1) 1.08 (AGE BIAS FAVOURED); with the standard deviation inside the 1st to 99th percentile,
   +1.89 ± 1.03, 3.34 / 0.74 (UNDECIDED); with 1.4826 × the median absolute deviation, +1.78 ± 0.65, 7.60 / 1.46
   (AGE BIAS FAVOURED). Under none of these bootstrap spreads does the structural row reach REQUIRED AT 3 SIGMA, so
   its change of word does not hang on the choice of spread statistic; only the curvature error (stage 1) gets it there.
5. So the second word is FRAGILE, naming table 1 alone and the structural fit. The first word, on the primary row,
   is the same in both stages.

## Against the amendment's own numbers (seen only now)
The amendment prints AGB5's K4 ratios: shuffle 1.248 (table 1) and 1.43 (table 2); bootstrap 1.09 and 1.16; shuffle
with the signal removed 1.11 and 1.23; and a primary A = +0.82 ± 0.17. Mine: shuffle 1.227 and 1.345 (frozen seed;
1.32 to 1.44 over five other seeds and a one-generator convention, `agb5r_K4S.out`); bootstrap 1.041 and 1.186 at seed
20261118, 1.113 and 1.138 at seed 20261119; signal removed 1.133 and 1.125; primary A = +0.8195 ± 0.1666. The pass/fail
pattern is the same in both builds (table 2's shuffle fails, every other leg passes, the amended K4 passes). The ratios
differ by about 0.1 at most, which is the random-number convention: their spread over seeds in my build is of that size.
The primary amplitude with stated errors agrees to the printed digits (+0.82 ± 0.17).
The amendment's χ²/dof (1.35, 1.42) and signal rms (0.05, 0.08 mag) match mine (1.349, 1.421; 0.052, 0.084).

kappa = 1/2 FITTED; not theory closed.
