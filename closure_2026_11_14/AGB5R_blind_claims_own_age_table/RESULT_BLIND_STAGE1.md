# AGB5R — blind re-grade of AGB5, stage 1 (as frozen)

2026-11-14. Second, independent implementation of AGB5 from its `FROZEN_CRITERIA.md` alone (reading in `READING.md`,
committed alone before any fit). AGB5's amendment, README, scripts and outputs, and the results of every other AGB lane,
were not opened before this file was committed. Own code: `agb5r_data.py` (loaders), `agb5r_fit.py` (plain line,
structural fit, word table), `agb5r_run.py MODE` (K1, KA, K3, K4, K4S, L1, REP, PP), `agb5r_collect.py`.

## Word

**L1 (as frozen): NOT EVALUABLE — K4 fails** (table 2's shuffle scatter is 1.345 σ_A, above the 1.25 ceiling).
Reading of the numbers, which the frozen rule turns into no word: AGE BIAS REQUIRED AT 3 SIGMA / FRAGILE (table 1 alone).

## Checks

| check | result | detail |
|---|---|---|
| K1 tables | PASS | 199 and 102 rows; 33 shared, 268 in all; all 301 ids in the SDSS-II table; table 1's residual columns differ in 198 of 199 rows (rms 0.040 mag); FSPS mass for 187 and 101 |
| KA published slopes | PASS | plain, no step: −0.03849 (t2, target −0.038), −0.02459 (t1, −0.025), combined −0.03040 (−0.030); structural, no step: −0.06263 ± 0.01360 (t2, −0.062), −0.04816 ± 0.01543 (t1, −0.047), −0.03884 ± 0.01561 (t1 bracketed, −0.037); largest miss 0.0018 against 0.004 |
| K3 twins | PASS (exit 3) | A_true 1 and 0, both tables: Â exact to 10⁻¹⁰, g = 0.05, α = 0.1, χ² ~ 10⁻²⁷ |
| K4 error bar | **FAIL** | table 1: shuffle mean +0.013 σ_A, shuffle sd 1.227 σ_A, bootstrap sd 1.041 σ_A (all pass); table 2: shuffle mean −0.056 σ_A (pass), **shuffle sd 1.345 σ_A (fail)**, bootstrap sd 1.186 σ_A (pass) |

σ_A in K4 and in the word is the formal weighted-least-squares error, weights 1/(σ_HR² + 0.10²), not rescaled
(READING item 1). χ²/dof at the step-free fit: 248.2/184 (table 1), 139.3/98 (table 2).

K4's fail does not hang on the random-number convention (`agb5r_K4S.out`, reading only): with one generator for both
tables, or with seeds 20261118 + 1 … + 5, table 2's shuffle sd is 1.323 to 1.439 σ_A, every time above 1.25. Table 1's
sits on the edge (1.227 to 1.271; one of six alternatives above 1.25). Bootstrap sd 1.07 to 1.25 σ_A (table 2's
reaches 1.251 once).

## L1 rows (plain line, mass step free, combined by inverse variance; structural row with curvature errors)

| row | Â | σ_A | Δχ²(A=0) | Δχ²(A=1) | first word (reading) |
|---|---|---|---|---|---|
| **primary (both tables)** | **+0.8195** | **0.1666** | **24.20** | **1.17** | AGE BIAS REQUIRED AT 3 SIGMA |
| table 1 alone (n 187) | +0.5322 | 0.2233 | 5.68 | 4.39 | NEITHER |
| table 2 alone (n 101) | +1.1797 | 0.2501 | 22.25 | 0.52 | AGE BIAS REQUIRED AT 3 SIGMA |
| shared hosts dropped from table 1 (n 154 + 101) | +0.7748 | 0.1818 | 18.15 | 1.53 | AGE BIAS REQUIRED AT 3 SIGMA |
| table 1 original residuals | +0.6742 | 0.1666 | 16.38 | 3.82 | AGE BIAS REQUIRED AT 3 SIGMA |
| redshift term added | +0.7515 | 0.1737 | 18.72 | 2.05 | AGE BIAS REQUIRED AT 3 SIGMA |
| structural in place of plain | +2.0140 | 0.5891 | 11.69 | 2.96 | AGE BIAS REQUIRED AT 3 SIGMA |

Per table, primary: β = −0.01597 ± 0.00670 (table 1), −0.03539 ± 0.00750 mag/Gyr (table 2); step g = +0.0588 ± 0.0285
and +0.0407 ± 0.0361 mag (positive = low-mass hosts fainter). Design power: σ_A = 0.1666 with the step (frozen file
0.17), 0.1307 without (0.13). Redshift-term fork: c_z = +0.34 ± 0.16 (t1), −0.25 ± 0.30 (t2). Structural fork:
table 1 A = +1.53 ± 0.95 (τ 0.84 Gyr, σ_int 0.124), table 2 A = +2.32 ± 0.75 (τ 1.10 Gyr, σ_int 0.117); the curvature
errors agree with the profile-likelihood Δ(−ln L) = ½ intervals to 6 % (checked in a scratch run).

Reading only (no word): with each table's σ_A scaled by √(χ²/dof), the primary row is Â = +0.811 ± 0.196,
Δχ²(A=0) 17.18, Δχ²(A=1) 0.93; the same first word in every plain fork except table 1 alone (AGE BIAS FAVOURED).

## Reported only

- L0, no step, combined on all rows: A = +1.013 ± 0.131 (the published 0.030 back). On the step sample: +1.043 ± 0.134.
- Step g without / with the age term: table 1 +0.0995 ± 0.0228 / +0.0588 ± 0.0285; table 2 +0.1401 ± 0.0293 /
  +0.0407 ± 0.0361; table 1 bracketed residuals +0.1093 ± 0.0228 / +0.0885 ± 0.0285.
- Slope inside each mass group (A): table 1 high-mass (n 128) +0.73 ± 0.25, low-mass (n 59) −0.20 ± 0.49; table 2
  high-mass (n 77) +1.17 ± 0.27, low-mass (n 24) +1.23 ± 0.62; table 1 bracketed residuals +0.48 ± 0.25 and −0.49 ± 0.49.
- Structural fit, combined, σ_age × 1 / 0.5 / 0: no step A = +1.88 ± 0.34 / +1.24 ± 0.20 / +0.98 ± 0.15; step free
  A = +2.01 ± 0.59 / +1.09 ± 0.27 / +0.80 ± 0.19. With the step free and any of the three scalings, Δχ²(A=0) ≥ 11.7 and
  Δχ²(A=1) ≤ 3.0.
- Pantheon+ (AGB4's fit; 196 of the 268 hosts; 8 bins in zHD, a x1 + b c free, weights 1/C_ii): table-1 age for the
  30 shared hosts, no step A = +0.452 ± 0.184 (Δχ² 6.02 / 8.84), step free A = +0.388 ± 0.202 (Δχ² 3.67 / 9.16,
  g = +0.019 ± 0.025); table-2 age for them, step free A = +0.369 ± 0.199 (3.45 / 10.07); table-1 hosts only
  (n 161) step free +0.522 ± 0.229; table-2 hosts only (n 65) step free +0.090 ± 0.323. Solver cross-checked with a
  second least-squares route (same digits).

## What the criteria leave open or get wrong (as I see it)

1. **K4's shuffle leg cannot pass when the weights are too small.** The plain weights add 0.10 mag in quadrature; the
   residuals want more (χ²/dof 1.35 and 1.42; the structural fits put σ_int at 0.117 to 0.132).
   Shuffling (age, mass) also moves the real age and mass signal into the residual, so the shuffle scatter exceeds even
   the χ²-scaled error. K4 is doing its job: the formal σ_A is too small by 15 to 20 per cent here, and the frozen word
   rests on it. The criteria do not say whether σ_A is formal or rescaled; "power from the design alone" implies formal.
2. **The second word mixes power with data.** "Table 1 alone" has σ_A 0.22 against 0.17 for the combination, so it can
   change the first word by losing power alone. It is the one fork that changes the reading here (NEITHER: Â = 0.53
   is 2.4σ from 0 and 2.1σ from 1).
3. Seeds: the bootstrap has none; I used the shuffle's (fresh generator per table). The numbers above show the
   convention moves table 1's shuffle sd across the 1.25 line once in six, table 2's never.
4. The Pantheon+ row is ambiguous for the 30 hosts of both tables (two ages); both choices are printed and agree to 0.02 in A.
5. The structural fit's τ is not specified per mass group; I used one shared τ. Within the mass groups the true-age
   spread τ (0.8 to 1.1 Gyr) is well below the stated age errors (rms 2.1 and 2.2 Gyr), so the attenuation correction is large
   and the structural row's error is three to four times the plain one; the frozen file's own note that the stated errors
   exceed the age variance applies here with more force.
6. KA compares slopes against published values rounded to the third decimal; with a 0.004 tolerance that is harmless.

## Files

`agb5r_K1|KA|K3|K4|K4S|L1|REP|PP.{json,out}`, `agb5r_collect.out`, `agb5r_results.json`. Run:
`python3 -I agb5r_run.py MODE` for each mode, then `python3 -I agb5r_collect.py` (BLAS threads 2; total under a minute).

kappa = 1/2 FITTED; not theory closed.
