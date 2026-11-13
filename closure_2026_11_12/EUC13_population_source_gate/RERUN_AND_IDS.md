# EUC13: commit ids, the lead's re-run and two notes (dated addition, 2026-11-12)

No number, word or line of the lane changes. RESULT.md stays as the lane wrote it.

## Commit ids (local / origin)

| Commit | Local | Origin |
|---|---|---|
| FROZEN_CRITERIA (alone) | 486c59d12a | 825553a28c |
| Scripts and outputs | 871b86be61 | b830a0f3e1 |
| AMENDMENT_A1 (alone, post hoc) | 9dd8ef58a2 | 8e5e5abec9 |
| A1 reading | 525d4752f4 | 30fbdc962f |
| RESULT | 63f7821b86 | b064bab650 |
| RESULT trim to 100 lines | 46891ba8cb | 7ca6a8ce18 |

## Re-run by the lead

From a copy of the three scripts and the committed COSMOS2020 counts table, one thread, no network: `euc13.py`,
`euc13_posthoc.py`, then `EUC13_MUTATE=newton`. The three JSON files, both CSV files, `euc13_posthoc.out` and
`euc13_MUTATE_newton.out` equal the committed ones byte for byte. `euc13.out` differs in two elapsed-time lines only.
The main run exits 0; the mutation twin exits 1. Words reproduce: EUC13-P NO VERDICT / NO VERDICT; f25 CEILING BROKEN
/ CEILING BROKEN. `euc13_fetch_cosmos.py` was not re-run, so the archive was not queried a second time.

A reproduction of the arithmetic. Not an independent re-grade.

## The field-galaxy table, rebuilt from the raw slices

`euc13_cosmos2020_counts.csv` was rebuilt by the lead with separate code from the twelve raw COSMOS2020 slices the lane
left under `_external_data/euc13_population_gate/` (each galaxy assigned to one slice by its magnitude; the same 0.1 mag
by 0.05 redshift grid): 714,201 rows read, 713,374 in the grid, and all 14,400 cells equal the committed table.
Median photometric redshift at 23.5 < i < 24.5 from the raw rows: 1.017 (the lane's check on the binned table: 0.994).

## Two notes for a reader

1. **The SLACS figure in RESULT.md section 7 is on the record's older mass convention.** "SLACS: 1.17 x at measured
   redshifts" is +0.0696 (alt) with the stellar mass taken as stellar fraction times Einstein mass. Graded the way
   Euclid's lenses are, against Auger's total Salpeter mass, the same SLACS lenses read +0.121 / +0.109 by lensing
   (1.32 x / 1.29 x): see `closure_2026_11_12/EUC12_common_mass_scale/RERUN_AND_IDS.md` and EUC1 RESULT.md section 9.
   The lane was written before that was found. Its known answer KA1 (+0.0815 / +0.0696) is the record's convention
   and is correct as a check of the machinery. No word here depends on the SLACS figure.
2. **What the two words say together.** The gate word is on the median lens and reads NO VERDICT. The second
   statistic is on the fraction above 1.78 x Salpeter and reads CEILING BROKEN, as frozen ("reported beside the gate
   word, not the gate word"). They do not conflict: a median near +0.21 to +0.30 with the catalogue's per-lens scatter
   puts 43 to 58 per cent of lenses above +0.25. By class the excess is carried by the 553 lenses with Einstein radius
   of 1.3 arcsec and above (+0.43 to +0.50, above the sealed band in every member); the 2,639 below 1.3 arcsec sit
   inside their sealed bands in every member.

Not done: an independent blind re-grade of the population gate; a forward-model member built from Euclid's own
photometric redshifts.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
