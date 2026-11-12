# AZ2R RESULT: blind re-grade of AZ2 (flat a0 at z 2.33, DESI DR2 Lya AP pair)

## Blind label (unchanged from RESULT_BLIND.md, commit d1acf1ba7e)

- Canonical: **FLAT HOLDS / EXPANSION-MODEL DEPENDENT**. T2 Om 0.30: sqrt X(2.33) 1.320, D_band 1.76, D_rival 361.8.
- Alt: **FLAT HOLDS / EXPANSION-MODEL DEPENDENT**. T2 Om 0.30: sqrt X(2.33) 1.322, D_band 1.79, D_rival 361.3.
- Flag: T2 at Om 0.25 (D_band 71) and Om 0.35 (D_band 15, X5 < 0) are FLAT FAILS. Validation KA1, KA2, KA3 all PASS;
  mutation (D_H -5 sigma) bites (1.320 -> 1.789, D_band 1.76 -> 22.15).
- A FLAT HOLDS is not a pass for the theory: constant dark energy (LCDM) gives the same sqrt X = 1; it separates nothing.

## COMPARISON: AGREES WITH DIFFERENCES THAT DO NOT MOVE A LABEL (against AZ2's amended A2 reading)

Against AZ2's FROZEN reading (NO VERDICT / NO VERDICT) the label differs; the cause is AZ2's code, not the statistic (below).

Cell by cell (mine vs AZ2, canonical; alt likewise):

| cell | sqrt X(2.33) | D_band | D_rival | label |
|---|---|---|---|---|
| T2 Om 0.30 | 1.320 vs 1.320 | 1.76 vs 1.76 | 361.8 vs 361.8 | FLAT HOLDS both |
| T2 Om 0.25 | 2.026 vs 2.026 | 71.3 vs 71.3 | 169.1 vs 169.1 | FLAT FAILS both |
| T2 Om 0.35 | 0 (X5 -0.99) both | 15.2 vs 15.2 | 569 vs 569 | FLAT FAILS both |
| T1 Om 0.25 / 0.30 / 0.35 | 1.965 / 1.195 / 0 both | 3.21 / 0.01 / 1.00 both | 7.1 / 13.6 / 19.8 both | FLAT HOLDS all |
| alt T2 Om 0.30 | 1.322 vs 1.322 | 1.79 vs 1.79 | 361.3 vs (not tabled) | FLAT HOLDS both |

Om-profiled rows (reported only) agree: T2 Om 0.260, sqrt X 1.92; T1 Om at the 0.45 edge with X5 < 0. KA1 digits agree
(7.408 / 12.080 / 5.976). Mutation agrees to the quoted digits (1.789 / 1.790; 22.15 / 22.27). Every graded number agrees to
the 0.01 printed; no label differs in any cell, footing or mutation.

Differences, sizes and causes:
1. Frozen KA3. AZ2's frozen KA3 failed (gap -0.357 / -0.373) because its X5 profile was a coarse grid that missed the free
   X5 1.74. My profile is continuous (Brent inside the band, plus the free fit's own X5), so the frozen KA3 passes as written
   (|gap| <= 6e-9). The frozen statistic therefore gives FLAT HOLDS / EXPANSION-MODEL DEPENDENT when computed without that grid
   artefact; this confirms AZ2's A2 diagnosis (free fit fine, grid coarse) and that A1 was a misread. It does not relabel AZ2's
   frozen record, which stays NO VERDICT for AZ2's own code.
2. X5 95 % intervals (reported only, coarse grids both sides): e.g. T1 Om 0.25 mine [1.0, 4.36] vs AZ2 [0.96, 8.0]; my grid
   stopped at X5 4 (+ free X5 +- 0.5), so my upper edges there are grid-capped; T2 Om 0.35 [-1.49, -0.25] vs [-1.49, -0.49]
   (grid step). Not graded.
3. Not computed by me (reported-beside items, not label inputs): D_X1, and the new-pair T1/T2 Delta chi^2 and T3 AP chi^2
   (AZ2: 8.14 / 12.00, 7.06). Not checked here.
4. I re-read the new pair from https://arxiv.org/html/2607.27410v3 (Eq. 26: 39.32 +- 0.33, 8.600 +- 0.066, rho 0.225) and it
   matches AZ2's input; PROVISIONAL (web summariser read), which AZ2's lead had not checked.

Shared with AZ2, so not independent: the DESI DR2 BAO table and Pantheon+ cuts taken from CFG681, the model definition, the new
pair, the criteria. Independent: the fit and profile code. Blindness caveat: AZ2's amendment files, readable before the blind
commit, already quoted its headline numbers (READING.md).

Commits: READING 17552835ff (alone); code + KA1 941d329a4a; runs bf4f890e3c; RESULT_BLIND d1acf1ba7e; this file next.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
