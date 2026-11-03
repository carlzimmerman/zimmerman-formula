# AN2 AMENDMENT A3: eta for the rows after KT. POST-RESULT, NOT BLIND

Committed with KT read and before any S1, KB at 128^3, KE or KG row is read. Lines of section 8 unchanged.

## What KT gave (N 64, shape B, canonical)
| Row | eta 0.05 | 0.025 | 0.0125 |
|---|---|---|---|
| T1 1e12, mu 0.1 | NO FOLD | NO FOLD | NO FOLD |
| T2 1e15, mu 56.6 | 5.7040 Gyr, filament | 5.7071 | 5.7063 |

T2 moves 0.054 % from 0.05 to 0.025 and 0.014 % from 0.025 to 0.0125. T1 has no t_q at any eta, so section 6's "t_q moves by <= 1 %" can't be met on it. **KT fails as frozen. The lane is NO VERDICT, numbers only** (it already was, by KZ and KE2).

## Eta for the rows
Section 6 doesn't say what eta to use when KT fails. The driver committed in ce4f1380c6 fell back to 0.0125. At that eta KB's (N 128, 2L) row had used 56 CPU min before reaching z = 0 and was heading for the 67.5 min cap. It was stopped by SIGTERM, not read, and its checkpoint taken out of the lane.

Rows now run at **eta 0.05**: T2 moves 0.05 % there, and T1 is NO FOLD at all three. This is chosen after seeing KT, and it's disclosed. The KT rows at 0.025 and 0.0125 stay in `an2_rows.jsonl`.

## Read in KT, allowed by section 8
T2, shape B at 64^3, folds at 5.70 Gyr (z 1.04) as a filament. AN1's spherical t_ref is 4.70 Gyr, so it's 21 % later. KE (e = 0 at 128^3) and KG decide whether that's the grid. T1 doesn't fold by z = 0 at 64^3, where AN1's reference folds at z 0.009, t 13.71 Gyr. At mu 0.1 this says little (A2 section 1).

kappa = 1/2 FITTED. Footings never pooled. A gravitating field, never a particle. The cold sector stays retired. S2 and S3 don't run. Not theory closed. Nothing here says the data favour the framework.
