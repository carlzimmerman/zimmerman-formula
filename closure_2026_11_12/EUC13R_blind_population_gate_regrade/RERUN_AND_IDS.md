# EUC13R: commit ids, the lead's re-run and the blindness check (dated addition, 2026-11-12)

No number, word or line of the lane changes. RESULT.md stays as the lane wrote it.

## Commit ids (local / origin)

| Commit | Local | Origin |
|---|---|---|
| READING (alone) | 865ef2116c | b1766ece5f |
| Code and runs | f02d4bda1d | d83f6968f1 |
| RESULT_BLIND | 5ab93fa25d | 11cc6cf20b |
| RESULT | 01ae63b6ae | fb4c1f7c1a |

## Re-run by the lead

From a copy of the three scripts, one thread, no network: `euc13r_checks.py` (which builds the lane's own COSMOS2020
grid from the raw slices), `euc13r.py`, then `EUC13R_MUTATE=newton`. `cosmos_counts_euc13r.csv`, `euc13r_checks.json`,
`euc13r_checks.out`, `euc13r.json` and `euc13r_newton.json` equal the committed files byte for byte. `euc13r.out` and
`euc13r_newton.out` are equal once the elapsed-time prefix of each line is removed; the committed `euc13r_newton.out`
also carries a final "exit 1" line written by the shell. The main run exits 0; the mutation twin exits 1. Words
reproduce: EUC13-P NO VERDICT / NO VERDICT; f25 CEILING BROKEN / CEILING BROKEN.

A reproduction of the arithmetic.

## Blindness, checked in the lane's tool log

Before the RESULT_BLIND commit (20:19:15 EST) the only files of other lanes the lane opened were EUC13's
FROZEN_CRITERIA.md and EUC1's FROZEN_CRITERIA.md. Its first read of any other EUC13 or EUC10 file came 12 seconds after
that commit. As READING records, its start-up context showed EUC13's two words in the subject of the lead's commit
ba46986e1d; that exposure was the lead's doing. So the numbers were computed independently of EUC13's, and the words
were not unseen.

## What the re-grade leaves untested

EUC13's second validation of the forward model (the known-source ECLIPSE lenses, where 7 of 8 sit lower in redshift
than the model puts them) could not be repeated blind: 4 evaluable lenses against the 5 the criteria need. So that
warning, which would push the forward-model member towards the DESI SLF IV member, stands on EUC13 alone.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
