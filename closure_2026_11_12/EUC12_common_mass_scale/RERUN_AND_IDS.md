# EUC12: commit ids, the lead's re-run, and the SLACS convention check (dated addition, 2026-11-12)

No number, word or line of the lane changes. RESULT.md stays as the lane wrote it.

## Commit ids (local / origin)

| Commit | Local | Origin |
|---|---|---|
| FROZEN_CRITERIA (alone) | bdaf5dcd26 | 6253a75fd6 |
| Scripts and runs | 339a88bf39 | 66dcab2d1a |
| RESULT | 7660adaacd | eade42f6d3 |

## Re-run by the lead

From a copy of the four scripts, one thread, no network: the chunked pass over the DESI DR1 CIGALE catalogue
(`euc12_cigale.py`, all 17,149,172 rows), then `euc12.py` and `EUC12_MUTATE=shift`, reading the Legacy Surveys rows the
lane left under `_external_data/euc12_common_mass_scale/`. All nine regenerated files equal the committed ones byte for
byte (two JSON, five CSV, two `.out`); the catalogue pass's log equals `euc12_cigale.out`. The main run exits 0; the
mutation twin exits 1. `euc12_fetch_ls.py` was not re-run, so the archive was not queried a second time.

A reproduction of the arithmetic. Not an independent re-grade.

## The SLACS reference: two mass conventions (checked by the lead; `lead_slacs_convention_check.py`, `.out`)

RESULT.md says it cannot reproduce "SLACS dynamics about +0.085" and suggests a different mass normalisation. That is
right, and the cause is this. The record's SLACS numbers (EUC1 K5 and EUC1-F's reference points +0.082 / +0.070; EUC5
J3 and J4, +0.085; A55, A70, A85) take each lens's stellar mass as Auger's Salpeter stellar fraction inside the
Einstein radius times the Einstein mass, divided by the light fraction inside the Einstein radius for n = 4 and Re(V).
Euclid's lenses are graded against the catalogue's total stellar mass. Auger's own total Salpeter mass (`logMs`) is the
like-for-like quantity for SLACS, and it is lower.

Through EUC1's own machinery, law S, lensing at the true source redshifts, the same 70 lenses (canonical / alt):

| Convention | b_med |
|---|---|
| (a) the record's, stellar fraction times Einstein mass | +0.0815 / +0.0696 |
| (b) Auger's total Salpeter mass | +0.1214 / +0.1089 |

Mass (a) over mass (b): median +0.0375 dex (16 to 84 per cent: +0.006 to +0.066).

Dynamics on convention (b), from the lane's `euc12_slacs.csv` (EUC5R's machinery, published dispersions):
+0.1319 / +0.1234 on those 70 lenses; +0.1517 / +0.1464 on all 79; +0.2652 / +0.2605 on the 9 outside the record's
sample. So the lane's "+0.15" is convention (b) plus nine extra lenses; on the record's sample it is +0.13.

What follows, as readings and not gates:

- Any comparison of Euclid's lens galaxies (catalogue total mass) with "SLACS +0.08" mixes the two conventions. On
  convention (b) SLACS reads +0.12 / +0.11 by lensing and +0.13 / +0.12 by dynamics.
- Euclid's typical class (Einstein radius below 1.3 arcsec, N 23) reads +0.129 / +0.127 by dynamics on the same
  machinery: equal to SLACS on convention (b). The lane's frozen word stays NO VERDICT (intervals about 0.18 dex wide).
- EUC1-F's lines (0.15 and 0.25) are not touched: they were set from stellar-mass systematics, not from the SLACS
  number, which EUC1 lists as a reference point only.
- Neither convention is wrong. Which one a statement uses must be said wherever a SLACS number is quoted.

Not checked: why Auger's stellar fraction times Einstein mass exceeds the total mass times the n = 4 light fraction by
0.04 dex (their profile, band and aperture conventions were not traced); the nine lenses outside the record's sample.
The like-for-like SLACS numbers have no independent re-grade.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
